class GummyFNAsyncException(Exception):
    pass


class InvalidParameters(GummyFNAsyncException):
    pass


class NotFound(GummyFNAsyncException):
    pass
