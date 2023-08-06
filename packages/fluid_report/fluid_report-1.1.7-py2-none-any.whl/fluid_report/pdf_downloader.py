from xml.etree import ElementTree
import cgi  # Import html in python 3
import datetime
import re

from six.moves import urllib
import flog
import requests

logger = flog.get_logger('mqbot.fluid_report.pdf_downloader')
TOKEN_REGEX = re.compile(r'(\$[a-zA-Z][^\$]*\$)')


def download_pdf(configs, app_name, report_name, **tokens):
    splunk_uri = configs['host']['current']
    splunk_user = configs['credentials']['username']
    splunk_pass = configs['credentials']['password']
    dashboard = requests.get(
        "{}/servicesNS/{}/{}/data/ui/views/{}".format(splunk_uri, splunk_user, app_name, report_name),
        auth=(splunk_user, splunk_pass),
        verify=False,
    )

    if dashboard.ok:
        logger.debug("Got dashboard XML for report {}".format(report_name))
    else:
        err = "Could not fetch dashboard {}".format(report_name)
        logger.error(err)
        raise Exception(err)

    xmler = ElementTree.fromstring(dashboard.text)
    entry = xmler.findall('{http://www.w3.org/2005/Atom}entry')[0]
    content = entry.find('{http://www.w3.org/2005/Atom}content')
    splunkdict = content.find('{http://dev.splunk.com/ns/rest}dict')
    dashboard_xml = [c.text for c in splunkdict.getchildren() if c.get('name') == 'eai:data'][0]

    missing_tokens = set(TOKEN_REGEX.findall(dashboard_xml)) - set(tokens.keys())

    if missing_tokens:
        logger.error("ERROR: no substitutions found for token(s): {}.".format(missing_tokens))

    # Replace all tokens in the XMLCode
    for token, value in tokens.items():
        dashboard_xml = dashboard_xml.replace(token, cgi.escape(value.decode('utf-8')))
    logger.debug("Transformed dashboard XML.")

    # Send XML code to endpoint, answer should be a pdf file
    report = requests.post(
        '{}/services/pdfgen/render'.format(splunk_uri),
        auth=(splunk_user, splunk_pass),
        params={
            'input-dashboard-xml': urllib.parse.quote(dashboard_xml.encode('utf-8')),
            'paper-size': 'a4-landscape',
        },
        verify=False,
    )
    logger.debug("Got response {} from pdf generator.".format(report))

    # Send XML code to endpoint, answer should be a pdf file
    if report.ok:
        if False:
            logger.debug("Got PDF information, writing to file.")
            with open('{}__{}.pdf'.format(app_name, report_name), 'wb') as pdf_file:
                pdf_file.write(report.content)
                logger.debug("Wrote PDF File, we're done here.")
        return {'PDF_OUTPUT': report.content}
    return {}


if __name__ == '__main__':
    configs = {
        'credentials': {'username': 'portal', 'password': 'p0r5@Lu$3r'},
        'host': {'current': 'https://splunk.lodgenet.com:8089'},
    }

    # report_name = 'sonicast_weekly_overview_mz'
    # report_name = 'portal_log_exploring'
    # report_name = 'sonicast_monthly_overview__0064288'
    report_name = 'sonicast_site_report'  # Download Weekly Report for Site
    app_name = 'sonicast'
    # app_name = 'search'

    property_id = '0010055'
    property_name = "PROPERTY_NAME"
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d for {}'.format(property_name))
    tokens = {
        '$propertyId$': property_id,
        # '$field1.latest$': 'now',
        # '$field1.earliest$': '-15d',
        '$latest$': 'now',
        '$earliest$': '-31d',
        '$result.today$': now,
        '$today$': now,
    }

    download_pdf(configs, app_name, report_name, **tokens)
