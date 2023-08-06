import os
import time

import redis
from routes.route import Route

from cordy.base.decorators import action
from cordy.conf import settings
from cordy.http.exceptions import HTTPException, WSDisconnect
from cordy.http.responses import HTMLResponse, StaticFileResponse
from cordy.utils import get_uwsgi


class ControllerMeta(type):

    def __new__(mcls, cname, bases, body):
        return super().__new__(mcls, cname, bases, body)


class Controller(metaclass=ControllerMeta):

    response_class = HTMLResponse
    filter_fields = None
    search_fields = None

    def __init__(self, request):
        self.request = request

    @classmethod
    def get_default_prefix(cls):
        return cls.__name__

    @classmethod
    def get_routes(cls, prefix=None, **kwargs):
        if prefix is None:
            prefix = cls.get_default_prefix()

        routes = []

        for action_name in dir(cls):
            try:
                action = getattr(cls, action_name)
            except AttributeError:
                continue

            if not hasattr(action, 'methods'):
                continue

            if action.url_path == '/':
                path = f'{prefix.lower()}/'
            else:
                path = f'{prefix.lower()}/{action.url_path}{action.trailing}'
            if action.needs_id:
                path = f'{path}{{id}}{action.trailing}'

            if path[0] != '/':
                path = f'/{path}'

            url_name = action.url_name
            if prefix != '':
                url_name = f'{prefix}_{url_name}'

            # if prefix is not None and prefix != '':
            #     path = f'{prefix.lower()}/'
            # else:
            #     path = ''

            # if action.needs_id:
            #     path = f'{path}{{id}}'
            #     if action.url_path != '/':
            #         path = f'{path}/{action.url_path}'
            # elif action.url_path != '/':
            #     path = f'{path}{action.url_path}'

            # if path[-1] != action.trailing:
            #     path = f'{path}{action.trailing}'

            # if path[0] != '/':
            #     path = f'/{path}'

            # print(prefix, action.needs_id, action.url_path, action.trailing)
            # print(path)


            controller = f'{cls.__module__}.{cls.__name__}'
            conditions = action.kwargs.get('conditions', {})
            conditions['method'] = action.methods

            routes.append(Route(url_name, path, controller=controller, action=action_name,
                                conditions=conditions, **kwargs))

        return routes

    @action(methods=['OPTIONS'], needs_id=False, url_path='/')
    def get_schema(self):
        return HTMLResponse(204)

    def render_response(self, status_code=200, content=None):
        return self.response_class(status_code, content=content)


class StandAloneWSController(Controller):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        connection = self.request._enviro.get('HTTP_CONNECTION', '').lower()
        upgrade = self.request._enviro.get('HTTP_UPGRADE', '').lower()

        if 'upgrade' not in connection or upgrade != 'websocket':
            raise HTTPException(405)

    def on_connect(self):
        pass

    def on_message(self, message):
        pass

    def on_disconnect(self):
        pass

    def run(self):
        uwsgi = get_uwsgi()

        message = uwsgi.websocket_recv_nb()
        if len(message) > 0:
            self.on_message(message)

    def _connected(self):
        pass

    def _disconnected(self):
        pass

    @action(needs_id=False)
    def connect(self):
        uwsgi = get_uwsgi()

        uwsgi.websocket_handshake()
        self._connected()
        self.on_connect()

        try:
            while True:
                self.run()
                time.sleep(.01)
        except OSError as e:
            self.on_disconnect()
            self._disconnected()
            raise WSDisconnect(*e.args)

    def send(self, message):
        uwsgi = get_uwsgi()

        uwsgi.websocket_send(message)


class Publisher:

    channel = 'cordy'

    _redis = redis.Redis()

    @classmethod
    def publish(cls, channel, message):
        cls._redis.publish(channel, message)

    @classmethod
    def broadcast(cls, message):
        cls._redis.publish(cls.channel, message)


class PubSubMixin(Publisher):

    channel = 'cordy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pubsub = self._redis.pubsub()

    def _connected(self):
        super()._connected()
        self._pubsub.subscribe(self.channel)
        self._pubsub.get_message()

    def _disconnected(self):
        super()._disconnected()
        self._pubsub.close()

    def on_receive(self, message):
        pass

    def run(self):
        super().run()
        item = self._pubsub.get_message()
        if item is not None:
            self.on_receive(item)

    def join(self, channel):
        self._pubsub.subscribe(channel)

    def leave(self, channel):
        self._pubsub.unsbscribe(channel)


class WSController(PubSubMixin, StandAloneWSController):
    pass


class TemplateView(Controller):

    template_name = None
    response_class = HTMLResponse

    def get_template_name(self):
        return self.template_name if self.template_name is not None else f'{self.__class__.__name__.lower()}.html'

    def __init__(self, *args, **kwargs):
        from cordy import Cordy

        super().__init__(*args, **kwargs)
        self.template_env = Cordy.templates

    def get_context(self, **kwrags):
        return {}

    def is_safe(self, template_name):
        return True

    @action(needs_id=False)
    def index(self, template_name=None, **kwargs):
        return self.render_template(template_name=template_name)

    def render_template(self, template_name=None, context=None):
        template_name = template_name if template_name is not None else self.get_template_name()
        if not self.is_safe(template_name):
            raise HTTPException(405)
        template = self.template_env.get_template(template_name)

        return self.render(template, context)

    def render(self, template, context=None):
        if context is None:
            context = self.get_context()
        return template.render(**context)


class StaticFiles(Controller):

    def is_safe(self, path_info):
        dest = os.path.abspath(os.path.join(settings.STATIC_ROOT, path_info))
        return dest[0:len(settings.STATIC_ROOT)] == settings.STATIC_ROOT

    def serve(self, path_info=None):
        path_info = self.request.path[1:]

        base_path = None
        if settings.DEBUG is True:
            from importlib import import_module
            from cordy.base.exceptions import FileNotFoundException
            from cordy.resolvers import FSResolver

            dirs = [os.path.abspath(os.path.dirname(import_module(a).__file__))
                    for a in getattr(settings, 'INSTALLED_APPS', [])]
            resolver = FSResolver(dirs)
            try:
                base_path = resolver.resolve(path_info, return_file=False)
            except FileNotFoundException:
                pass

        if base_path is None:
            base_path = settings.BASE_DIR

        if settings.DEBUG or self.is_safe(path_info):
            return StaticFileResponse(self.request._enviro, base_path)

        raise HTTPException(404)
