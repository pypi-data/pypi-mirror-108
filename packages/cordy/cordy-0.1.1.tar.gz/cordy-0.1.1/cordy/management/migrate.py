from types import FunctionType
import click

from cordy.base.management import BaseCommand
from cordy.conf import settings
from cordy import Cordy
from cordy.db.models import Model
from cordy import logging
from cordy.utils import import_module

from peewee import ModelBase
from playhouse.migrate import SchemaMigrator, migrate
from playhouse.reflection import generate_models


log = logging.getLogger(__name__)


class Migrations(BaseCommand):

    @click.command(help='Simplistic migration tool')
    @click.argument('apps', nargs=-1)
    def migrate(self, apps=()):
        if settings.DATABASE is None:
            log.warning('Unable to migrate a project with no database')
            return

        if Cordy.db is None or Cordy.db.obj is None:
            Cordy.init_db()

        declared = self.get_declared_models(apps)
        existing = generate_models(Cordy.db.obj)

        to_execute = []
        migrator = SchemaMigrator.from_database(Cordy.db.obj)

        with Cordy.db.atomic():
            for deleted in [n for n in existing.keys() if n not in declared]:
                if len(apps) > 0:
                    do_continue = True
                    for app in apps:
                        if existing[deleted]._meta.app.startswith(app):
                            do_continue = True
                            break
                    if do_continue:
                        continue
                if input(f'{deleted} seems to have been deleted. Remove table? (y/n)') == 'y':
                    existing[deleted].drop_table(cascade=True)

            to_create = [m for n, m in declared.items() if n not in existing]

            Cordy.db.create_tables(to_create)

            for model_name in [n for n in existing.keys() if n in declared]:
                for field in [n for n in existing[model_name]._meta.fields.keys()
                              if n not in declared[model_name]._meta.fields]:
                    to_execute.append(migrator.drop_column(model_name, field))
                for field in [n for n in declared[model_name]._meta.fields.keys()
                              if n not in existing[model_name]._meta.fields]:
                    to_execute.append(migrator.add_column(model_name, field,
                                                          declared[model_name]._meta.fields[field]))

            migrate(*to_execute)

    def get_declared_models(self, apps=()):
        declared = {}
        if len(apps) == 0:
            apps = getattr(settings, 'INSTALLED_APPS', [])
        for app in apps:
            app_models = f'{app}.models'
            try:
                module = import_module(app_models)
            except ImportError:
                continue

            for model in [m for n, m in module.__dict__.items()
                          if not n.startswith('__')
                          and not isinstance(m, FunctionType)
                          and ((getattr(m, '__module__', '') == app_models
                                and (issubclass(m, Model) or isinstance(m, ModelBase))
                                and getattr(m._meta, 'abstract', False) is False)
                               or (hasattr(m, 'name') and m.__name__.endswith('Through')))
                          ]:

                declared[model._meta.table_name] = model
        return declared
