from cordy.auth.models import BaseUser, Group
from cordy.db.models import Model

import peewee as pw


class ToDo(Model):

    description = pw.TextField()
    is_done = pw.BooleanField(null=True)


class User(BaseUser):

    groups = pw.ManyToManyField(Group, backref='users')


UserGroup = User.groups.get_through_model()
