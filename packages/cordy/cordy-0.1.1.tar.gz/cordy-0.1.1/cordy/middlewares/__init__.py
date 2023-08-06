from cordy.http.responses import Response


class BaseMiddleware:

    def before(self, enviro):
        pass

    def after(self, content, start):
        pass

    def after_response(self):
        # print(f'decorating from {self.__class__.__name__}')
        # response = self.response
        # print(f'************* *********** ******* response is {response}, {type(response)}')
        self.handler.after_response()

    def after_request(self, request):
        self.request = request
        self.handler.after_request(request)

    @property
    def response(self):
        response = self.handler
        try:
            while not isinstance(response, Response):
                # print(f'response is {response}, {type(response)}')
                response = response.handler
            return response
        except AttributeError:
            return None

    def handle(self, enviro, start):
        return self.handler(enviro, start)

    def __init__(self, handler):
        self.handler = handler

    def __call__(self, enviro, start):
        self.before(enviro)
        rv = self.handle(enviro, start)
        self.after(rv, start)
        return rv


class EnviroLogMiddleware(BaseMiddleware):

    def before(self, enviro):
        import pprint

        pprint.pprint(enviro)
