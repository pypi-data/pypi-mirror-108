class CordyBaseException(Exception):
    pass


class FileNotFoundException(CordyBaseException, FileNotFoundError):
    pass


class NotImplementedException(CordyBaseException, NotImplementedError):
    pass


class CommandException(CordyBaseException):
    pass


class ImproperlyConfigured(CordyBaseException):
    pass
