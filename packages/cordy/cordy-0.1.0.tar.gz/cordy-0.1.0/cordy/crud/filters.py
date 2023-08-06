from marshmallow import Schema
from marshmallow.fields import Str
from marshmallow_peewee import ModelSchema
from peewee import Field

from cordy.http.parser import parser


class FieldsFilterModelSchema:

    def apply(self, controller, pw_query):

        class BaseSchema(ModelSchema):

            class Meta:
                model = controller.Model
                fields = controller.filter_fields

        self.FieldsSchema = type(f'{controller.Model.__class__.__name__}FieldsSchema', (BaseSchema, ), {})

        validated = parser.parse(self.FieldsSchema, req=controller.request, location='querystring', validate=False)
        filter_data = {field: getattr(validated, field)
                       for field in controller.filter_fields
                       if getattr(validated, field) is not None}

        return pw_query.filter(**filter_data)


class SearchFilterSchema:

    def apply(self, controller, pw_query):
        q = getattr(controller, 'search_query_param', 'q')
        cls_kwargs = dict(((q, Str()), ))

        self.SearchSchema = type(f'{controller.Model.__class__.__name__}SearchSchema', (Schema, ), cls_kwargs)

        validated = parser.parse(self.SearchSchema, req=controller.request, location='querystring', validate=False)
        if q in validated:
            fields = [f if isinstance(f, Field) else getattr(controller.Model, f) for f in controller.search_fields]
            query = fields.pop().contains(validated[q])
            for field in fields:
                query |= field.contains(validated[q])

            pw_query = pw_query.where(query)

        return pw_query
