from cordy.base.exceptions import CordyBaseException
from .responses import Response, JSONResponse


class BaseHTTPException(CordyBaseException):
    pass


class HTTPException(BaseHTTPException, Response):

    def __init__(self, status_code=400, content=''):
        if int(status_code) < 400:
            raise Exception('Exception status_code must be >= 400')
        Response.__init__(self, status_code=status_code, content=content)
        Exception.__init__(self)

    @property
    def message(self):
        return self.content


class JSONException(BaseHTTPException, JSONResponse):

    def __init__(self, status_code=400, content=None):
        if int(status_code) < 400:
            raise Exception('Exception status_code must be >= 400')
        JSONResponse.__init__(self, status_code=status_code, content=content)
        Exception.__init__(self)


class WSDisconnect(CordyBaseException):
    pass
