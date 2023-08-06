import marshmallow as ma

from cordy.http.responses import Response


def with_pagination(**kwargs):
    result_key = kwargs.pop('result_key', 'results')

    def decorator(func):

        def decorated(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if isinstance(response, tuple) and len(response) == 2:
                data = response[1]
            elif not isinstance(response, tuple):
                data = response
            else:
                return response

            data_with_pagination = {
                'count': len(data),
                result_key: data,
            }

            paginator = self.get_paginator()
            if paginator is not None:
                paginator.get_meta_data(data_with_pagination)

            if isinstance(response, tuple) and len(response) == 2:
                return response[0], data_with_pagination

            return data_with_pagination

        rv_func = decorated
        rv_func.__name__ = func.__name__
        return rv_func
    return decorator


def marshall(with_schema=None, many=False, **kwargs):

    def decorator(func):

        def decorated(self, *args, **kwargs):
            with_ = with_schema
            many_ = many

            response = func(self, *args, **kwargs)

            if isinstance(response, tuple) and len(response) == 2:
                data = response[1]
            elif not isinstance(response, tuple):
                data = response
            else:
                return response

            if with_ is None:
                if many_:
                    if len(data) > 0:
                        with_ = data[0].get_serializer()
                    else:
                        return []
                else:
                    with_ = data.get_serializer()

            if isinstance(with_, type) and issubclass(with_, ma.Schema):
                with_ = with_()

            if isinstance(response, tuple) and len(response) == 2:
                return response[0], with_.dump(data, many=many_)
            elif not isinstance(response, tuple):
                return with_.dump(data, many=many_)
            return None

        rv_func = decorated
        rv_func.__name__ = func.__name__
        return rv_func
    return decorator


# Code heavily inspired by Django REST Framework
def action(methods=None, needs_id=True, name=None, url_path=None, url_name=None,
           input_serializer=None, serializer=None, default_response_code=200,
           trailing='/', **kwargs):

    methods = ['GET'] if methods is None else methods
    methods = [m.upper() for m in methods]

    def decorator(func):

        description = func.__doc__ or None
        func_name = func.__name__

        func.url_path = url_path if url_path is not None else '/' if func_name == 'index' else func_name
        func.url_name = url_name if url_name is not None else func_name.replace('_', '-')
        func.methods = methods
        func.needs_id = needs_id
        func.trailing = trailing
        func.kwargs = kwargs
        func.kwargs['description'] = description
        func.kwargs['default_response_code'] = default_response_code

        return func

    return decorator
