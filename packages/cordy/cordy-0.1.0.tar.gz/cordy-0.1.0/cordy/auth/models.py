import json

import peewee as pw

from cordy.auth.hashers import get_hasher, make_password
from cordy.auth.serializers import LoginSchema
from cordy.conf import settings
from cordy.db.models import Model
from cordy.utils import import_string
from cordy.xsrf import rotate_token


class Group(Model):

    name = pw.CharField(unique=True)


class BaseUser(Model):

    email = pw.CharField(unique=True)
    _password = pw.CharField(max_length=128)

    class Meta:
        abstract = True

    @property
    def password(self):
        if self._password is None:
            return None
        return json.dumps(get_hasher().safe_summary(self._password))

    @password.setter
    def password(self, value):
        self._password = make_password(value)

    def check_password(self, value):
        return get_hasher().verify(value, self._password)

    def login(self, request):
        if settings.USE_CSRF:
            rotate_token(request)
        request.session['user_id'] = self.id
        request.user = self
        request.session.save()

    @classmethod
    def logout(cls, request):
        request.session.invalidate()
        request.session.pop('user_id', None)
        request.user = None
        request.session.save()
        request.session.delete()
        if settings.USE_CSRF:
            rotate_token(request)

    @classmethod
    def get_request_serializer(cls):
        return LoginSchema


def get_user_model():
    return import_string(settings.USER_MODEL)
