from cordy.http.exceptions import HTTPException


class BasePermission:

    def check_and_forward(self, controller, method, args, kwargs):
        check = getattr(self, f'can_{controller.request.action}', None)
        if check is not None:
            check(controller.request.user, **kwargs)
        return method(*args, **kwargs)


class AllowAll(BasePermission):
    pass


class AnonymousReadonlyLoggedInWrite(BasePermission):

    def is_logged_in(self, user):
        if user is None:
            raise HTTPException(403)

    def __getattr__(self, name):
        if name in ('can_new', 'can_update', 'can_delete'):
            return self.is_logged_in
        raise AttributeError(name)


class LoginRequired(AnonymousReadonlyLoggedInWrite):

    def __getattr__(self, name):
        if name.startswith('can_'):
            return self.is_logged_in
        raise AttributeError
