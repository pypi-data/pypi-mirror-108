from cordy.db.models import Model

import peewee as pw


class Page(Model):

    title = pw.CharField()
    body = pw.TextField(null=True)
    in_menu = pw.BooleanField(default=True)
