from cordy.base.exceptions import NotImplementedException
from cordy.http.exceptions import HTTPException


def login_required(group=None):

    def decorator(func):

        def decorated(self, *args, **kwargs):

            _group = group

            user = getattr(self.request, 'user', None)
            if user is None:
                raise HTTPException(401)
            if _group is not None:
                from cordy.auth.models import Group
                if isinstance(_group, Group):
                    _group = _group.name
                if hasattr(user, 'groups'):
                    try:
                        user.groups.where(Group.name == _group).get()
                    except Group.DoesNotExist:
                        raise HTTPException(403)
                elif hasattr(user, 'group'):
                    if user.group.name != _group:
                        raise HTTPException(403)
                else:
                    raise NotImplementedException('unable to check group for now')

            return func(self, *args, **kwargs)

        rv_func = decorated
        rv_func.__name__ = func.__name__
        return rv_func
    return decorator


def authorize_with(permission_class):

    def decorator(klass):
        cls_kwargs = {}
        checker = permission_class()

        for method_name in dir(klass):
            if hasattr(getattr(klass, method_name), 'url_path'):
                cls_kwargs[method_name] = lambda self, *args, **kwargs: checker.check_and_forward(
                    self,
                    getattr(super(klass, self), self.request.action),
                    args,
                    kwargs
                )

        rv = type(klass.__name__, (klass,), cls_kwargs)
        rv.__module__ = klass.__module__

        for method_name in cls_kwargs.keys():
            func = getattr(rv, method_name)
            if callable(func):
                for attr in dir(getattr(klass, method_name)):
                    if attr.startswith('__') and attr not in ('__name__', '__doc__'):
                        continue

                    setattr(func, attr, getattr(getattr(klass, method_name), attr, None))
        return rv

    return decorator
