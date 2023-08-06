
class Error(Exception):
    pass


class NotConfigured(Error):
    pass


class WrongKey(Error):
    pass


class InternalError(Error):
    pass


class Unavailable(Error):
    pass
