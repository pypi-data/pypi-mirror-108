import json

from webob import Response as WebObResponse


class Response(WebObResponse):

    STATUS_CODES = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        103: 'Early Hints',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        218: 'This is fine',
        226: 'IM Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        306: 'Switch Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        417: 'Expectation Failed',
        418: "I'm a teapot",
        419: 'Page Expired',
        420: 'Method Failure',
        421: 'Misdirected Request',
        422: 'Unprocessable Entity ',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Too Early',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        430: 'Request Header Fields Too Large',
        431: 'Request Header Fields Too Large',
        450: 'Blocked by Windows Parental Controls',
        451: 'Unavailable For Legal Reasons',
        498: 'Invalid Token',
        499: 'Token Required',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        509: 'Bandwidth Limit Exceeded',
        510: 'Not Extended',
        511: 'Network Authentication Required',
        526: 'Invalid SSL Certificate',
        529: 'Site is overloaded',
        530: 'Site is frozen',
        598: 'Network read timeout error',
    }

    status_code = 200
    content_type = 'text/plain'
    charset = WebObResponse.default_charset

    def __init__(self, status_code=200, content='', **kwargs):

        if int(status_code) not in self.STATUS_CODES:
            raise Exception(f'Unknown status code: {status_code}')

        self._status = f'{status_code} {self.STATUS_CODES[int(status_code)]}'

        return super().__init__(status=status_code, body=content, content_type=self.content_type)


class HTMLResponse(Response):

    content_type = 'text/html'


class JSONResponse(Response):

    content_type = 'application/json'

    def __init__(self, status_code=200, content='', **kwargs):
        if isinstance(content, dict) or isinstance(content, list):
            content = json.dumps(content)
        super().__init__(status_code=status_code, content=content, **kwargs)


class StaticFileResponse(Response):

    def __init__(self, enviro, path):
        super().__init__()
        self.path = path
        self.enviro = enviro

    def __call__(self, enviro, start):
        from static import Cling
        app = Cling(self.path)
        return app(enviro, start)
