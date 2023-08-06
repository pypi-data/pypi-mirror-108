from beaker.middleware import SessionMiddleware as BeakerSession

from cordy.middlewares import BaseMiddleware
from cordy.conf import settings


class SessionMiddleware(BaseMiddleware):

    def get_session_opts(self):
        return {
            'session.type': settings.SESSION_TYPE,
            'session.cookie_expires': settings.SESSION_EXPIRES,
            'session.auto': settings.SESSION_AUTO,
            'session.httponly': settings.SESSION_HTTP_ONLY,
            'session.secure': settings.SESSION_SECURE,
            'session.validate_key': settings.SECRET_KEY,
        }

    def __init__(self, handler):
        super().__init__(handler)
        self._handler = BeakerSession(handler, self.get_session_opts())

    def handle(self, enviro, start):
        return self._handler(enviro, start)
