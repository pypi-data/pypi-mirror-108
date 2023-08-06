from collections import defaultdict
from functools import reduce
import os
import traceback

from peewee import DatabaseProxy
from routes import Mapper
from routes.route import Route

from cordy.base.exceptions import NotImplementedException
from cordy.conf import settings
from cordy.http import Request
from cordy.http.exceptions import BaseHTTPException, HTTPException, WSDisconnect
from cordy.http.responses import Response
from cordy import logging
from cordy.utils import import_string


log = logging.getLogger(__name__)


def _make_response(response, controller, action):
    if not isinstance(response, Response) and hasattr(controller, 'render_response'):
        if isinstance(response, tuple):
            if len(response) == 1:
                response = response + (None, )
            if len(response) > 2:
                raise HTTPException('Malformed response')
            return controller.render_response(*response)
        else:
            return controller.render_response(
                getattr(getattr(controller, action), 'default_response_code', 200),
                content=response
            )

    if not isinstance(response, Response):
        return Response(content=response)

    return response


class Cordy:

    db = DatabaseProxy()
    templates = None
    docs = None
    mapper = None

    def _process_map(self, mapper, prefix=None):
        routes = [r for r in mapper if isinstance(r, Route)]
        self.__class__.mapper.extend(routes, prefix)
        sub_maps = [r for r in mapper if not isinstance(r, Route)]
        for sub_mapper, prefix in sub_maps:
            self._process_map(sub_mapper, prefix)

    @classmethod
    def init_templates(cls):
        template_engine = getattr(settings, 'USES_TEMPLATES', None)
        if template_engine is not None and cls.templates is None:
            log.debug(f'Initializing template engine {template_engine}')
            init_method = f'_init_templates_{template_engine}'
            if not hasattr(cls, init_method):
                raise NotImplementedException(f'{template_engine} is not an implemented template engine')
            getattr(cls, init_method)()

    @classmethod
    def _get_jinja2_loader(cls):
        from jinja2 import FileSystemLoader, ChoiceLoader

        if getattr(settings, 'TEMPLATE_DIRS', None) is not None:
            loaders = [FileSystemLoader(os.path.join(settings.BASE_DIR, d))
                       for d in getattr(settings, 'TEMPLATE_DIRS', [])]

        if getattr(settings, 'TEMPLATES_FROM_APP', False):
            from importlib import import_module

            for app in getattr(settings, 'INSTALLED_APPS', []):
                module = import_module(app)
                try:
                    loaders.append(FileSystemLoader(
                        os.path.join(module.__path__[0], 'templates')
                    ))
                except TypeError:
                    loaders.append(FileSystemLoader(
                        os.path.join(module.__path__._path[0], 'templates')
                    ))

            module = import_module(cls.__module__)
            loaders.append(FileSystemLoader(
                os.path.join(os.path.abspath(os.path.dirname(module.__file__)), 'templates')
            ))

        return ChoiceLoader(loaders)

    @classmethod
    def _init_templates_jinja2(cls):
        from jinja2 import Environment, select_autoescape

        cls.templates = Environment(
            loader=cls._get_jinja2_loader(),
            autoescape=select_autoescape(['html', 'xml']),
            extensions=settings.TEMPLATES_JINJA_EXTENSIONS
        )

    @classmethod
    def init_db(cls):
        log.debug('Connecting to DB')
        from playhouse.db_url import connect
        cls.db.initialize(connect(settings.DATABASE.get('URL', 'sqlite:///:memory:')))

    def __init__(self):

        self.__class__.mapper = Mapper()

        log.debug('Initializing...')

        if hasattr(settings, 'DATABASE') and settings.DATABASE is not None:
            self.init_db()

        self.init_templates()

        if settings.DOCUMENT_API is True:
            self.docs = {}

        try:
            mapper = import_string(f'{settings.URLS}.url_map')
        except ImportError:
            log.warning(f'Unable to load {settings.URLS}.url_map')
            traceback.print_exc()
            mapper = None

        if mapper is not None:
            self.register_urls(mapper)

    def register_urls(self, mapper):
        log.debug('Registering URLs')
        self._process_map(mapper)

    def __call__(self, enviro, start):
        from .utils import import_string

        class Handler:

            handler = None
            _after_response = None
            _after_request = None

            def _call_after_request(self, request):
                    if (callable(self._after_request)):
                        _after_request = self._after_request
                        _after_request(request)

            def __call__(self, enviro, start):
                from .utils import import_string

                to_call = Cordy.mapper.match(environ=enviro)
                request = Request(enviro)

                if to_call is None:
                    request._dont_enforce_csrf_checks = True
                    self._call_after_request(request)

                    wrong_action = Cordy.mapper.match(enviro['PATH_INFO'])
                    if wrong_action is None:
                        response = HTTPException(404)
                    else:
                        response = HTTPException(405)
                else:
                    action = to_call.pop('action')
                    controller_class = to_call.pop('controller')

                    request.action = action

                    try:
                        controller = import_string(controller_class)(request)
                        method = getattr(controller, action)
                        request._dont_enforce_csrf_checks = getattr(method, '_dont_enforce_csrf_checks', False)
                        self._call_after_request(request)
                        response = method(**to_call)
                        response = _make_response(response, controller, action)
                        log.info(f'{enviro["REQUEST_METHOD"]} {response.status_code} - {enviro["PATH_INFO"]}')
                    except BaseHTTPException as http_e:
                        response = http_e
                        log.warning(f'{enviro["REQUEST_METHOD"]} {response.status_code} - '
                                    f'{enviro["PATH_INFO"]} - {http_e.__class__.__name__}')
                    except WSDisconnect:
                        return []
                    except Exception as e:
                        log.error(f'{enviro["REQUEST_METHOD"]} 500 - '
                                f'{enviro["PATH_INFO"]} - {e.__class__.__name__} - {e.args}')
                        traceback.print_exc()
                        response = HTTPException(500, e.args)

                self.handler = response

                if (callable(self._after_response)):
                    _after_response = self._after_response
                    _after_response()
                return response(enviro, start)

            def after_response(self):
                pass

            def after_request(self, request):
                pass

        resolved_middlewares = [import_string(m) for m in reversed(settings.MIDDLEWARES)]

        handler = Handler()
        chained = reduce(lambda h, m: m(h), resolved_middlewares, handler)
        handler._after_response = chained.after_response
        handler._after_request = chained.after_request

        return chained(enviro, start)

    def document(self, path, spec):
        from cordy.utils import import_string

        paths = defaultdict(dict)
        for route in self.__class__.mapper._routenames.values():
            if not route.regpath.startswith(path):
                continue

            controller = route.defaults.get('controller', None)
            action = route.defaults.get('action', None)
            if controller is None or action is None:
                continue

            try:
                controller_class = import_string(controller)
                func = getattr(controller_class, action)
            except ImportError:
                continue
            except AttributeError:
                continue

            if not hasattr(func, 'kwargs'):
                continue

            input_serializer = func.kwargs.get('input_serializer', False)
            if input_serializer is True or input_serializer == 'many':
                if f'{controller_class.Model.__name__}Input' not in spec.components._schemas:
                    schema = controller_class.Model.get_request_serializer()
                    spec.components.schema(f'{controller_class.Model.__name__}Input', schema=schema)

            serializer = func.kwargs.get('serializer', False)
            if serializer is True or serializer == 'many':
                if controller_class.Model.__name__ not in spec.components._schemas:
                    schema = controller_class.Model.get_serializer()
                    spec.components.schema(controller_class.Model.__name__, schema=schema)

            actions_path = route.regpath.replace('%(', '{').replace(')s', '}')

            for method in route.conditions.get('method', ['GET']):
                schema = None
                if serializer is True:
                    schema = controller_class.Model.__name__
                elif serializer == 'many':
                    schema = {
                        'type': 'array',
                        'items': controller_class.Model.__name__
                    }
                if serializer is True or serializer == 'many':
                    paths[actions_path][method.lower()] = {
                        'parameters': [],
                        'responses': {func.kwargs['default_response_code']: {
                            'content': {
                                controller_class.response_class().headers.get(
                                    'Content-Type',
                                    'text/plain'
                                ): {'schema': schema}
                            }
                        }}
                    }
                else:
                    paths[actions_path][method.lower()] = {
                        'parameters': [],
                        'responses': {func.kwargs['default_response_code']: {
                            'content': {
                                controller_class.response_class().headers.get(
                                    'Content-Type',
                                    'text/plain'
                                ): {}
                            }
                        }}
                    }

                if getattr(func, 'needs_id', False) is True:
                    for key in route.minkeys:
                        paths[actions_path][method.lower()]['parameters'].append({
                            'in': 'path',
                            'required': True,
                            'name': key,
                            'schema': {'type': 'string'}
                        })
                if input_serializer is True or input_serializer == 'many':
                    schema = None
                    if input_serializer is True:
                        schema = f'{controller_class.Model.__name__}InputSchema'
                    elif input_serializer == 'many':
                        schema = {
                            'type': 'array',
                            'items': f'{controller_class.Model.__name__}InputSchema'
                        }

                    paths[actions_path][method.lower()]['parameters'].append({
                        'in': 'body',
                        'name': 'body',
                        'required': True,
                        'schema': schema
                    })

        for actions_path, operations in paths.items():
            spec.path(path=actions_path, operations=operations)

        self.docs[path] = spec
