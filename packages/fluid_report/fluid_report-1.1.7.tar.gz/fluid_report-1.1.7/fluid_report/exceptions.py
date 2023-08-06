from fluid_mq import exceptions


class InvalidReportTypeError(Exception):
    pass


class QueryStringFormattingException(Exception):
    pass


class UnchagedDataException(exceptions.NonrecoverableException):
    def __init__(self, last_error=None):
        msg = "Job data did not change, not performing an update."
        exceptions.NonrecoverableException.__init__(self, msg.format(), last_error=last_error)
