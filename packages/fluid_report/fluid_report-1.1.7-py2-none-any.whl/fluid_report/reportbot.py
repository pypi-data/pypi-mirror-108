#!/usr/bin/env python
import traceback

from fluid_report import workers
from fluid_mq import mq_bot, exceptions as mq_exceptions


class ReportBot(mq_bot.MQBot):

    def callback(self, message):

        self.messages += 1

        self.logger.debug('Got message body: %s' % message.body)
        self.logger.debug('Got message delivery info: %s' % message.delivery_info)
        self.logger.info('Got report generation request for {0[job_uri]}'.format(message.body_dict))

        try:
            message._active_worker_ = worker = workers.Worker(message.body_dict['job_uri'], configs=self.configs)
            self.logger.debug('Got worker {0}'.format(worker))
            worker.work()
            self.logger.debug('{0} completed without raising exceptions, HUZZAH!'.format(worker))
            self.success += 1
        except Exception as e:
            self.logger.exception('Failed to generate report for {0[job_uri]}'.format(message.body_dict))
            if (
                isinstance(e, mq_exceptions.NonrecoverableException) or
                isinstance(e, mq_exceptions.RecoverableException)
            ):
                raise
            else:
                raise mq_exceptions.RecoverableException(
                    'Encountered potentially recoverable error generating report',
                    last_error=traceback.format_exc(),
                )

    def notify_error(self, message, error):
        message._active_worker_.notify_error(error)

    def notify_success(self, message):
        message._active_worker_.notify_success()


def main():
    config = {
        'bindings': [
            {
                'exchange_name': 'reporting',
                'routing_keys': [
                    'sonicast.status',
                ],
            },
        ],
        'queue_name': 'reportbot',
        'durable': True,
        'type': 'topic',
        'log_name': 'mqbot.reportbot',
    }
    ReportBot(**config).listen()

if __name__ == '__main__':
    main()
