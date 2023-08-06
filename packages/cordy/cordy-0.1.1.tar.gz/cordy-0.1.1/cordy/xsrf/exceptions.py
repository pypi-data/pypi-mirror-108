# The following code is mostly copied from https://github.com/gregorynicholas/flask-xsrf/
from cordy.http.exceptions import HTTPException


class XSRFException(HTTPException):
    pass


class XSRFMissing(XSRFException):
    pass


class XSRFNoReferer(XSRFException):
    pass


class XSRFMalformedReferer(XSRFException):
    pass


class XSRFInsecureReferer(XSRFException):
    pass


class XSRFBadReferer(XSRFException):
    pass


class XSRFBadOrigin(XSRFException):
    def __init__(self, content=''):
        return super().__init__(content=content)


class XSRFTokenMalformed(XSRFException):

    def __init__(self, status_code=406, content=''):
        return super().__init__(status_code, content=content)


class XSRFTokenExpiredException(XSRFException):

    def __init__(self, status_code=403, content=''):
        return super().__init__(status_code, content=content)


class XSRFTokenInvalid(XSRFException):

    def __init__(self, status_code=401, content=''):
        return super().__init__(status_code, content=content)


class XSRFTokenUserIdInvalid(XSRFTokenInvalid):
    pass
