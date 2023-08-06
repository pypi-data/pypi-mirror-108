from collections.abc import Mapping
import functools

from webargs.djangoparser import DjangoParser as Parser
from webargs.multidictproxy import MultiDictProxy
from webob.multidict import MultiDict

from cordy.db.models import Model
from cordy.http.exceptions import JSONException
from cordy.logging import getLogger


_UNKNOWN_DEFAULT_PARAM = "_default"

log = getLogger(__name__)


class CordyParser(Parser):

    location = 'json_or_form'

    def get_request_from_controller_args(self, view, args, kwargs):
        if len(args) > 0:
            return args[0].request
        return None

    def get_argmap_from_controller_args(self, view, args, kwargs):
        if len(args) > 0:
            self.argmap = args[0].Model.get_request_serializer()
            return self.argmap
        return None

    def get_default_request(self):
        return None

    def _raw_load_json(self, req):
        return req.json

    def load_cookies(self, req, schema):
        return MultiDictProxy(req.cookies, schema)

    def load_headers(self, req, schema):
        return MultiDictProxy(req.headers, schema)

    def load_files(self, req, schema):
        files = ((k, v) for k, v in req.POST.items() if hasattr(v, "file"))
        return MultiDictProxy(MultiDict(files), schema)

    def _update_args_kwargs(self, args, kwargs, parsed_args, as_kwargs):
        if as_kwargs:
            if isinstance(parsed_args, Model):
                kwargs.update(self.argmap.dump(parsed_args))
            else:
                kwargs.update(parsed_args)
        else:
            # Add parsed_args after other positional arguments
            args += (parsed_args,)
        return args, kwargs

    def use_args(self, argmap=None, *, location=None, unknown=_UNKNOWN_DEFAULT_PARAM,
                 as_kwargs=False, validate=None, error_status_code=400, error_headers=None):
        location = location or self.location
        request_obj = None
        # Optimization: If argmap is passed as a dictionary, we only need
        # to generate a Schema once
        if isinstance(argmap, Mapping):
            argmap = self.schema_class.from_dict(argmap)()

        def decorator(func):
            req_ = request_obj
            map_ = argmap

            self.argmap = argmap

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                req_obj = req_
                argmap = map_

                if not req_obj:
                    req_obj = self.get_request_from_controller_args(func, args, kwargs)

                if not argmap:
                    argmap = self.get_argmap_from_controller_args(func, args, kwargs)

                parsed_args = self.parse(argmap, req=req_obj, location=location,
                                         validate=validate, error_status_code=error_status_code,
                                         error_headers=error_headers)
                args, kwargs = self._update_args_kwargs(args, kwargs, parsed_args, as_kwargs)
                return func(*args, **kwargs)

            wrapper.__wrapped__ = func
            return wrapper

        return decorator

    def handle_error(self, error, req, schema, *, error_status_code, error_headers):
        if error_status_code is None:
            error_status_code = 400
        response = JSONException(error_status_code, error.args[0])
        log.warning(error)
        raise response


parser = CordyParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
