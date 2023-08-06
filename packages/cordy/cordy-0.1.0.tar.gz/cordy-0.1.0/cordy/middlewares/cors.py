from cordy.conf import settings
from cordy.middlewares import BaseMiddleware


class CORSMiddleware(BaseMiddleware):

    def before(self, enviro):
        self.enviro = enviro

    def after_response(self):
        response = self.response
        if hasattr(settings, 'CORS_ALLOW_ORIGIN'):
            if hasattr(self, 'request'):
                origin = self.request.origin()
            else:
                origin = self.enviro.get('HTTP_ORIGIN', None)

            if settings.CORS_ALLOW_ORIGIN == '*':
                response.headers['Access-Control-Allow-Origin'] = settings.CORS_ALLOW_ORIGIN
            elif origin in settings.CORS_ALLOW_ORIGIN:
                response.headers['Access-Control-Allow-Origin'] = origin
            else:
                response.headers['Access-Control-Allow-Origin'] = ','.join(settings.CORS_ALLOW_ORIGIN)
        if hasattr(settings, 'CORS_ALLOW_METHODS'):
            response.headers['Access-Control-Allow-Methods'] = ','.join(settings.CORS_ALLOW_METHODS)
        if hasattr(settings, 'CORS_ALLOW_HEADERS'):
            response.headers['Access-Control-Allow-Headers'] = ','.join(settings.CORS_ALLOW_HEADERS)
        if hasattr(settings, 'CORS_ALLOW_CREDENTIALS'):
            response.headers['Access-Control-Allow-Credentials'] = 'true' if settings.CORS_ALLOW_CREDENTIALS else 'false'
        if hasattr(settings, 'CORS_MAX_AGE'):
            response.headers['Access-Control-Allow-Origin'] = str(settings.CORS_MAX_AGE)
        return super().after_response()
