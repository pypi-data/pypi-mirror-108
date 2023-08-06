import datetime
import os
import time

from six.moves.urllib.parse import urlparse
import yaml
import iso8601
import splunklib.client as splunk_client
import splunklib.results as splunk_results

import requests_toolbelt

from fluid_mq import mq_bot_logger, workers, exceptions
from fluid_report import transformers, exceptions as report_exceptions, pdf_downloader

LOADJOB_TYPES = ('SONICAST_USAGE_SUMMARY', 'SONICAST_PROPERTY_PERFORMANCE', 'SONICAST_APPS_CASTED',)


def _serialize_date_(date):
    # TODO: should we really be hard coding the offset here?
    #       perhaps we should be converting the date to that offset then serializing
    return date.strftime('%Y-%m-%dT%H:%M:%S+00:00')


class SplunkReporter(workers.Worker):

    def __new__(*args, **kwargs):
        """
        Overriding __new__ to allow for direct instantiation without the parent's type discovery in
        the way, should that be necessary (i.e. from unit tests).
        """
        return object.__new__(SplunkReporter)

    def __init__(self, *args, **kwargs):
        self.loadjob_timeframe = 'Weekly'
        self.logger = mq_bot_logger.MQBotLogger('mqbot.fluid_report.workers')
        self.brand_name = None
        return super(SplunkReporter, self).__init__(*args, **kwargs)

    def _perform_safe_file_upload(self, uri, filedata, mimetype, **fields):
        fields['file'] = ('mq_generated_file', filedata, mimetype)
        fields['mimetype'] = mimetype
        data = requests_toolbelt.MultipartEncoder(fields=fields)

        return self._perform_safe_post_request(
            uri,
            data,
            headers={'Content-Type': data.content_type},
        )

    def __connect_client(self):
        host_parts = urlparse(self.configs['splunk']['host']['current'])
        self.client = splunk_client.connect(
            host=host_parts.hostname,
            port=host_parts.port,
            scheme=host_parts.scheme,
            app="search",
            **self.configs['splunk']['credentials']  # noqa
        )

    def __build_search_query_string(self, report_type, groups):
        query_file = self.configs['splunk'].get(
            'query_file',
            os.path.dirname(os.path.abspath(__file__)) + '/queries.yaml',
        )
        with open(query_file) as query_file:
            query_dict = yaml.load(query_file)

        orred_property_ids = ' OR '.join(sorted(['propertyId={}'.format(cms_id) for cms_id in groups]))
        cms_ids = tuple(sorted([str(cms_id) for cms_id in groups]))  # Should be a tuple so it reprs with parens
        loadjob_timeframe = self.loadjob_timeframe

        try:
            search_query = query_dict[report_type]
        except KeyError:
            raise report_exceptions.InvalidReportTypeError(
                "Only reports of types {} are able to be generated at this time.".format(query_dict.keys()),
            )

        if hasattr(search_query, 'keys') and 'pdf_gen' in search_query:
            search_query = search_query.pop('pdf_gen')

            if len(cms_ids) > 1:
                # Multi-site query
                search_query['report_name'] = search_query['multi_site_report_name']
                property_name = self.brand_name if self.brand_name is not None else cms_ids

                search_query['$multisitesqlpropertyId$'] = str(cms_ids)
                property_id = orred_property_ids
            else:
                property_id = list(groups.keys())[0]
                property_name = groups[property_id]['name']

            for token, value in search_query.items():
                if value == 'REPORT_LABEL':
                    search_query[token] = datetime.datetime.utcnow().strftime(
                        '%Y-%m-%d for {}'.format(property_name.encode('utf-8')),
                    )
                elif token == '$propertyId$':
                    search_query[token] = property_id
                # TODO: Also handle `$earliest$` and `$latest$` properly
        else:
            try:
                search_query = search_query.format(**locals())
            except KeyError as e:
                raise report_exceptions.QueryStringFormattingException(
                    "Query string requested local {}, but it was not found among {}".format(e, locals().keys()),
                )
            except ValueError:
                raise report_exceptions.QueryStringFormattingException("Could not format string properly...")

        self.logger.debug("Built search query parameters:")
        self.logger.debug(search_query)
        return search_query

    @workers.step(description='Got target report ({}) from job.')
    def __get_report(self, report_uri):
        return self._perform_safe_get_request(report_uri)

    @workers.step(description='Got Group CMS IDs {result} for group {} from report.')
    def __get_group_data(self, group_uri):
        group = self._perform_safe_get_request(group_uri)

        if group.get('children', []):
            self.brand_name = self.brand_name or group.get('name')
            return [self._perform_safe_get_request(child) for child in group['children']]

        return [group]

    @workers.step(description='Computing report timeframes')
    def __extract_times(self, report):
        if report['window'] == 'MANUAL':
            return (
                iso8601.parse_date(report['start_date']),
                iso8601.parse_date(report['end_date']),
            )

        created_timestamp = iso8601.parse_date(self.job['created'])
        end_timestamp = created_timestamp
        adjust_hour_span = True

        _, cardinality, window_unit = report['window'].split('_')
        cardinality = int(cardinality)

        if window_unit.startswith('HOUR'):
            self.loadjob_timeframe = 'Hourly'
            adjust_hour_span = False
            end_timestamp = end_timestamp.replace(minute=0, second=0)
            start_timestamp = end_timestamp - datetime.timedelta(hours=cardinality)  # TODO
            start_timestamp = start_timestamp.replace(minute=0, second=0)

        elif window_unit.startswith('DAY'):
            self.loadjob_timeframe = 'Daily'
            start_timestamp = end_timestamp - datetime.timedelta(days=cardinality)

        elif window_unit.startswith('WEEK'):
            self.loadjob_timeframe = 'Weekly'
            while not end_timestamp.strftime('%A') == 'Monday':
                end_timestamp = end_timestamp - datetime.timedelta(days=1)
            start_timestamp = end_timestamp - datetime.timedelta(days=7 * cardinality)

        elif window_unit.startswith('MONTH'):
            self.loadjob_timeframe = 'Monthly'
            end_timestamp = end_timestamp.replace(day=1)

            year_offset = 0
            month_offset = end_timestamp.month - cardinality
            while month_offset < 0:
                year_offset += 1
                month_offset += 12

            start_timestamp = end_timestamp.replace(day=1, month=month_offset, year=end_timestamp.year - year_offset)

        elif window_unit.startswith('YEAR'):
            end_timestamp = end_timestamp.replace(day=1, month=1)
            start_timestamp = end_timestamp.replace(year=end_timestamp.year - cardinality)

        if adjust_hour_span:
            end_timestamp = end_timestamp.replace(hour=0, minute=0, second=0)
            start_timestamp = start_timestamp.replace(hour=0, minute=0, second=0)

        return (
            start_timestamp,
            end_timestamp,
        )

    @workers.step(description='Got report data for report {}.')
    def __get_report_data(self, report_type, groups, search_params={}):

        if not hasattr(self, 'client'):
            self.__connect_client()

        search_query = self.__build_search_query_string(report_type, groups)

        if search_query == 'TODO':
            self.logger.warn("RETURNING EMPTY BECAUSE THERE WAS NO QUERY FOR {}".format(report_type))
            return []

        # Ensure timestamps are serialized properly if needed
        if isinstance(search_params.get('earliest_time', ''), datetime.datetime):
            search_params['earliest_time'] = _serialize_date_(search_params['earliest_time'])
        if isinstance(search_params.get('latest_time', ''), datetime.datetime):
            search_params['latest_time'] = _serialize_date_(search_params['latest_time'])

        if report_type == 'SONICAST_USAGE_DETAIL':
            params = {'configs': self.configs['splunk']}
            params.update(**search_query)
            return pdf_downloader.download_pdf(**params)

        job = self.client.jobs.create(search_query, exec_mode='normal', **search_params)

        while not job.is_done():
            # TODO: Check with portal to see if job is canceled, if so, cancel the Splunk query
            time.sleep(2)

        try:
            return [row for row in splunk_results.ResultsReader(job.results(count=0))]
        except Exception:
            return []
        finally:
            job.cancel()  # Stops the current search and deletes the results cache

    @workers.step(description='Transforming report data {}.')
    def __transform_report_data(self, report_type, data, groups=[], start_date=None, end_date=None):
        return transformers.transformer_factory(report_type)(
            data,
            groups=groups,
            start_date=start_date,
            end_date=end_date,
        )

    def __data_has_changed(self, data, start_date, end_date):
        return (
            self.report.get("data", {}) != data or
            (not (start_date == self.report['start_date'] and end_date == self.report['end_date']))
        )

    def __adjust_time_brackets(self, report_type, data, start_date, end_date):
        if report_type not in LOADJOB_TYPES or not data:
            return start_date, end_date

        # find a representative sample of data for nested loadjob responses
        if "Number of STAYCAST uses" in data.keys():
            data = data["Number of STAYCAST uses"]

        def safestrp(string):
            try:
                return datetime.datetime.strptime(string.replace(" Summary", ""), "%m/%d/%y")
            except ValueError:
                return None

        try:
            dates = {safestrp(date) for key in data.keys() for date in key.split(" - ")}
            dates.remove(None) if None in dates else ''
        except Exception:
            dates = []

        if dates:
            return min(dates), max(dates) + datetime.timedelta(days=1)
        else:
            return start_date, end_date

    @workers.step(description='Sent report data to portal for report {}.')
    def __send_report_data_to_portal(self, report_uri, data, start_date, end_date):
        start_date = _serialize_date_(start_date)
        end_date = _serialize_date_(end_date)

        if 'PDF_OUTPUT' in data:
            return self._perform_safe_file_upload(
                report_uri,
                data['PDF_OUTPUT'],
                'application/pdf',
                start_date=start_date,
                end_date=end_date,
            )
        if self.__data_has_changed(data, start_date, end_date):
            self._perform_safe_patch_request(report_uri, {
                'data': data,
                'start_date': start_date,
                'end_date': end_date,
            })
        else:
            raise report_exceptions.UnchagedDataException()

    def work(self):
        try:
            self._update_status(description='Just started')

            report_uri = self.job['targets'][0]

            # STEP 1: Load the report information from the portal
            report = self.__get_report(report_uri)
            self.report = report

            # STEP 2: Retrieve the CMS IDs for the group that own the given report
            groups = {g['cms_id']: g for g in self.__get_group_data(report['group'])}
            self.logger.debug("Got CMS ID's {}".format(groups.keys()))

            # STEP 3: Extract time windows
            start_date, end_date = self.__extract_times(report)

            # STEP 4: Get the report data from Splunk
            if report['type'] in LOADJOB_TYPES:
                data = {}
                for cms_id in sorted(groups.keys()):
                    data[cms_id] = self.__get_report_data(report['type'], [cms_id])

            elif report['type'] == 'SONICAST_DAILY_USAGE' and report['window'] == 'LAST_4_WEEKS':
                lower_bound = start_date
                latest_date = end_date
                data = {}
                summary_key = '{0:%m/%d/%y} - {1:%m/%d/%y} Summary'.format(
                    lower_bound,
                    latest_date - datetime.timedelta(days=1),
                )

                # Collect summary report
                data[summary_key] = map(
                    lambda x: {k: v for k, v in x.iteritems() if not k.startswith('Week of')},
                    self.__get_report_data(report['type'], groups, {
                        'earliest_time': lower_bound,
                        'latest_time': latest_date + datetime.timedelta(days=7),
                    })
                )

                while latest_date > lower_bound:
                    earliest_date = latest_date - datetime.timedelta(days=7)
                    subreport_key = '{0:%m/%d/%y} - {1:%m/%d/%y}'.format(
                        earliest_date,
                        latest_date - datetime.timedelta(days=1),
                    )

                    # Collect active week's report
                    data[subreport_key] = self.__get_report_data(report['type'], groups, {
                        'earliest_time': earliest_date - datetime.timedelta(days=28),
                        'latest_time': latest_date,
                    })

                    # prepare for next iteration
                    latest_date = earliest_date
            else:  # Is a query, not a loaded job
                data = self.__get_report_data(report['type'], groups, {
                    'earliest_time': start_date,
                    'latest_time': end_date,
                })

            # STEP 5: Transform the report data
            data = self.__transform_report_data(
                report['type'],
                data,
                groups=groups,
                start_date=start_date,
                end_date=end_date,
            )

            # Adjust the start/end dates to match the data
            start_date, end_date = self.__adjust_time_brackets(report["type"], data, start_date, end_date)

            # STEP 6: Send the report data to the portal
            self.__send_report_data_to_portal(
                report_uri,
                data,
                start_date=start_date,
                end_date=end_date,
            )

        except Exception as e:
            self.logger.exception('Splunk report generation failed')
            if not isinstance(e, exceptions.PortalResourceLocked):
                self._update_status(
                    status='PENDING',
                    description='Job failed with exception: \'{}: {}\'.'.format(e.__class__.__name__, e),
                )
            raise


if __name__ == '__main__':
    import json
    from fluid_mq import get_config

    def update_status_mock(*args, **kwargs):
        print(kwargs['description'])
        return

    def get_request_mock(uri):
        if uri == 'http://example.com/api/reports/1':
            return {
                # 'type': 'SonicastStatus',
                # 'type': 'SONICAST_PROPERTY_MAP',
                # 'type': 'SONICAST_APPS_CASTED',
                # 'type': 'SONICAST_SNC_STATUS',
                # 'type': 'SONICAST_BANDWIDTH',
                # 'type': 'SONICAST_DAILY_USAGE',
                'type': 'SONICAST_USAGE_SUMMARY',
                'group': 'http://example.com/api/groups/1',
                # 'start_date': int(time.mktime((datetime.datetime.now() - datetime.timedelta(weeks=4)).timetuple())),
                # 'end_date': int(time.time()),
                'start_date': '2015-11-18T11:13:36.000-06:00',
                'end_date': '2019-11-19T11:13:36.000-06:00',
                # 'window': 'MANUAL',
                'window': 'LAST_1_WEEKS',
            }
        elif uri == 'http://example.com/api/groups/1':
            return {
                # 'cms_id': '0069415',
                # 'cms_id': '0010055',
                'cms_id': '0064288',
            }
        return {}

    def patch_request_mock(uri, data):
        print('Patching {} with {}'.format(uri, json.dumps(data)))
        return

    worky = SplunkReporter('http://example.com/api/jobs/1', get_config())
    worky.job = {
        'uri': 'http://example.com/api/jobs/1',
        'targets': ['http://example.com/api/reports/1'],
        # 'created': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000-00:00'),
        'created': datetime.datetime.utcnow().strftime('%Y-%m-31T%H:%M:%S.000-00:00'),  # REMOVE THIS, loadjob needs EoM
    }
    worky._update_status = update_status_mock
    worky._perform_safe_get_request = get_request_mock
    worky._perform_safe_patch_request = patch_request_mock
    worky.work()

workers.Worker.register_type_provider('GENERATE_REPORT', SplunkReporter)
Worker = workers.Worker
