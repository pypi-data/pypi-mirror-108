from urllib.parse import urlparse
from webargs.core import parse_json
from webob import Request as WebObRequest


class Request(WebObRequest):

    controller = None
    action = None

    def __init__(self, enviro, *args, **kwargs):
        rv = super().__init__(enviro, *args, **kwargs)

        self.META = {}

        # TODO: Is this still needed? parse_jason might be better than json.loads?
        if 'json' in self.content_type:
            try:
                self.json = parse_json(self.body, encoding=self.charset)
            except Exception:
                self.json = None

        self.user = enviro.get('cordy.user', None)
        self.session = enviro.get('beaker.session', None)

        return rv

    @property
    def _enviro(self):
        return self.environ

    def scheme(self):
        return self.environ.get('wsgi.url_scheme', 'http')

    def is_secure(self):
        return self.scheme() in ('https', 'wss')

    def origin(self):
        return self.environ.get('HTTP_ORIGIN', None)

    def host(self):
        return urlparse(self.host_url).netloc
