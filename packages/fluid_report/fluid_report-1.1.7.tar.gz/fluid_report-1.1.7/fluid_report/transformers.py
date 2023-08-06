import flog
from datetime import timedelta
from collections import defaultdict

logger = flog.get_logger('mqbot.fluid_report.transformers')


def __collate_data(transformed_data):
    for label, weeks in transformed_data.items():
        for week, values in weeks.items():
            if 'average' in label.lower() or '%' in label.lower():
                transformed_data[label][week] = sum(values) / len(values)
            elif label == 'Apps used':
                app_casts = {}
                for v in values:
                    app_casts[v['appName']] = app_casts.get(v['appName'], 0) + v['count']
                transformed_data[label][week] = [{'appName': k, 'count': v} for k, v in app_casts.items()]
            else:
                try:
                    transformed_data[label][week] = sum(values)
                except TypeError:
                    logger.error("Could not sum data set '{}'".format(values))
                    try:
                        transformed_data[label][week] = sum([int(v) for v in values])
                    except ValueError:
                        logger.exception(
                            "Could not work with data '{}' for week '{}' with label '{}'".format(values, week, label),
                        )
                        continue
    return transformed_data


def __get_number(datum, label):
    datum = __normalize_string(datum)
    try:
        if (
            datum.endswith('%') or
            label == u'Average # of SoniCast uses per stay' or
            label == u'Average # of STAYCAST uses per stay'
        ):
            datum = float(datum.replace('%', '')) * 100
        datum = int(datum)
    except Exception:
        print('EXCEPTION parsing "{}"'.format(label))
    return datum


def __get_seconds(time_str):
    h, m, s = time_str.split(':')

    if '+' in h:
        d, h = h.split('+')
        h = int(h)
        h += int(d) * 24

    return int(h) * 3600 + int(m) * 60 + int(s)


def __normalize_apps_used(metric):
    retty = []
    logger.debug(metric)
    metric = metric.strip(',').replace('\n', '')
    for app in metric.split('),'):
        name, count = app.rstrip(')').rsplit('(', 1)
        retty.append({
            'appName': name.strip(),
            'count': int(count),
        })

    return retty


def __normalize_datum(datum, label):
    if hasattr(datum, 'lower'):
        if ':' in datum:
            datum = __get_seconds(datum)
        else:
            datum = __get_number(datum, label)

    if label == '% stays that cast' and not isinstance(datum, int):
        datum = 0

    return datum


def __normalize_string(datum):
    return datum\
        .replace('buys', '')\
        .replace('guests', '')\
        .replace('rooms', '')\
        .replace('stays', '')\
        .replace('uses', '')\
        .strip()


def __transpose_metrics(data):
    transformed_data = {}
    for site, metrics in data.items():
        for metric in metrics:
            label = metric.pop('Metric')

            if label not in transformed_data:
                transformed_data[label] = {}

            for week, datum in metric.items():
                if week not in transformed_data[label]:
                    transformed_data[label][week] = []

                if label == 'Apps used':
                    transformed_data[label][week] += __normalize_apps_used(datum)
                else:
                    transformed_data[label][week].append(__normalize_datum(datum, label))
    return __collate_data(transformed_data)


def __generate_expected_reports(lower_bound, latest_date):
    while latest_date > lower_bound:
        earliest_date = latest_date - timedelta(days=7)
        yield '{0:%m/%d/%y} - {1:%m/%d/%y}'.format(
            earliest_date,
            latest_date - timedelta(days=1),
        )
        latest_date = earliest_date


def sonicast_property_performance(data, groups={}, start_date=None, end_date=None, **kwargs):
    """
    const PropertyPerformanceDatum = Record({
      property: undefined,
      performance: undefined
    });

    const PropertyPerformance = List;

    May be able to do this with the data from SONICAST_USAGE_SUMMARY (Monthly), but averaged over the weeks
    in the month.

    Use the %stays that cast metric

    """
    if not data:
        return data

    expected_subreports = list(__generate_expected_reports(start_date, end_date))
    summary_key = '{0:%m/%d/%y} - {1:%m/%d/%y} Summary'.format(
        start_date,
        end_date - timedelta(days=1),
    )

    transformed_data = defaultdict(list)
    for site_id, group in groups.items():
        site_data = data.get(site_id, [])
        site_tabulation = {
            'site_id': site_id,
            'name': group['name'],
            'group_id': group['id'],
        }
        metric_label = '% stays that cast'
        metric = next((m for m in site_data if m.get('Metric', '') == metric_label), {})
        performace_summary = 0
        for week_range in expected_subreports:
            # Extract the performance metric
            performance = __normalize_datum(metric.get(week_range), metric_label)

            # Collect metric for summary calculation
            performace_summary += performance

            # Add the metric to the output data
            entry = {'performance': performance}
            entry.update(site_tabulation)
            transformed_data[week_range].append(entry)

        # Calculate the summary and add it to the output data
        summary = {'performance': int(performace_summary / len(expected_subreports))}
        summary.update(site_tabulation)
        transformed_data[summary_key].append(summary)

    return transformed_data


def sonicast_apps_casted(data, **kwargs):
    """the frontend expects a list of objects each with a `appName` and `count` field curently"""
    if not data:
        return data

    transformed_data = __transpose_metrics(data)

    return transformed_data.get('Apps used', [])


def sonicast_property_map(data, groups={}, **kwargs):
    for datum in data:
        datum['group_id'] = groups[datum['site_id']]['id']
    return data


def sonicast_usage_summary(data, **kwargs):
    if not data:
        return data

    transformed_data = __transpose_metrics(data)
    whitelist = [
      'Contracted STAYCAST Rooms',
      'Number of STAYCAST uses',
      '# of stays that cast',
      'Average duration of one use',
      'Average # of STAYCAST uses per stay',
      'Average total duration per stay',
      '% stays that cast',
    ]

    return {key: value for key, value in transformed_data.iteritems() if key in whitelist}


def identity(data, **kwargs):
    logger.debug("No transformer defined, using `identity`")
    return data


def transformer_factory(report_type):
    # If you want to add a report transformer, add a function named as the lower-case version of that report's type
    return globals().get(report_type.lower(), identity)


if __name__ == '__main__':
    import json
    import pprint
    with open('/src/lodgenet-mq/python/fluid_report/fluid_report/tests/sonicast_weekly_dumps.json') as jfile:
        data = json.load(jfile)
    pprint.pprint(sonicast_usage_summary(data['MULTISITE_RAW_DUMP']))
