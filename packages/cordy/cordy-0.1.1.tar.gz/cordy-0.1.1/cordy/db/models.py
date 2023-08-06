from uuid import uuid4

from marshmallow_peewee import ModelSchema
from peewee import UUIDField, make_snake_case, Metadata as BaseMetadata

from cordy import Cordy
from cordy.conf import settings

if getattr(settings, 'DATABASE', None) is None:
    from peewee import Model as BaseModel
else:
    db_url = getattr(settings, 'DATABASE', {}).get('URL', '')
    if db_url.startswith('postgresext'):
        from playhouse.postgres_ext import Model as BaseModel
    elif db_url.startswith('sqliteext'):
        from playhouse.sqlite_ext import Model as BaseModel
    else:
        from peewee import Model as BaseModel


class Metadata(BaseMetadata):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self._additional_keys.remove('abstract')
        except KeyError:
            pass

    def get_app_name(self):
        name = self.model.__module__.rsplit('.', 2)
        if name[-1] == 'models':
            return name[-2]
        return name[-1]

    def make_table_name(self):
        table_name = super().make_table_name()
        return f'{make_snake_case(self.get_app_name())}_{table_name}'

    @property
    def app(self):
        return self.get_app_name()


class Model(BaseModel):

    _serializer = None
    _input_serializer = None

    id = UUIDField(primary_key=True, default=uuid4)

    class Meta:
        database = Cordy.db
        model_metadata_class = Metadata

    def __str__(self):
        if not self.id or self.id is None:
            return f'New {self.__class__.__name__}'
        return f'{self.__class__.__name__} #{self.id}'

    @classmethod
    def get_serializer(cls):
        if cls._serializer is None:

            class Schema(ModelSchema):

                class Meta:
                    model = cls

            cls._serializer = type(f'{cls.__name__}Schema', (Schema, ), {})

        return cls._serializer()

    @classmethod
    def get_request_serializer(cls):
        if cls._serializer is None:
            cls.get_serializer()

        if cls._input_serializer is None:

            class Schema(cls._serializer):

                class Meta:
                    model = cls
                    exclude = ('id', )

            cls._input_serializer = type(f'{cls.__name__}InputSchema', (Schema, ), {})

        return cls._input_serializer()
