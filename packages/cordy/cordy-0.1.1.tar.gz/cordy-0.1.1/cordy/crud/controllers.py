from marshmallow_jsonschema import JSONSchema

from jinja2.exceptions import TemplateNotFound

from cordy.base import Controller, TemplateView
from cordy.base.decorators import action, marshall, with_pagination
from cordy.conf import settings
from cordy.crud.filters import FieldsFilterModelSchema, SearchFilterSchema
from cordy import Cordy
from cordy.http.exceptions import HTTPException
from cordy.http.parser import use_kwargs
from cordy.http.responses import JSONResponse, HTMLResponse
from cordy.logging import getLogger


log = getLogger(__name__)


def template_for_field(fields, fieldname):
    field_type = fields['properties'][fieldname]['type']
    if isinstance(field_type, list):
        field_type = field_type[0]
    return [f'crud/fields/{fieldname}.html', f'crud/fields/{field_type}.html']


class BaseCRUDViewSet(Controller):

    Model = None
    response_class = JSONResponse
    serializer = None
    filters = None
    filter_fields = None
    pagination_class = None
    page_size = None

    _paginator = None

    @classmethod
    def get_default_prefix(cls):
        return cls.Model.__name__

    def get_paginator(self, qs=None):
        if self._paginator is None and self.pagination_class is not None:
            self._paginator = self.pagination_class(self, qs)
        return self._paginator

    def limit(self, qs):
        if self.pagination_class is None:
            return qs
        return self.get_paginator(qs).limit(qs)

    def offset(self, qs):
        if self.pagination_class is None:
            return qs
        return self.get_paginator(qs).offset(qs)

    def get_list(self):
        qs = self.apply_filters(self.Model.select())
        return self.offset(self.limit(qs))

    def apply_filters(self, pw_query):
        filters = self.filters
        if filters is None:
            filters = []
        if self.filter_fields is not None and FieldsFilterModelSchema not in filters:
            filters.append(FieldsFilterModelSchema)
        if self.search_fields is not None and SearchFilterSchema not in filters:
            filters.append(SearchFilterSchema)

        if filters is not None:
            for filter in filters:
                pw_query = filter().apply(self, pw_query)

        return pw_query

    def get_object(self, id):
        try:
            return self.get_list().where(self.Model.id == id).get()
        except self.Model.DoesNotExist:
            raise HTTPException(404, f'{self.Model.__name__} with id {id} was not found')

    @with_pagination()
    @marshall(many=True)
    def list(self):
        return self.get_list()

    @action(url_path='/')
    @marshall()
    def get(self, id):
        return self.get_object(id=id)

    @action(methods=['POST'], needs_id=False, url_path='/', default_response_code=201)
    @use_kwargs()
    @marshall()
    def create(self, **data):
        instance = self.Model.create(**data)
        return 201, instance

    @use_kwargs()
    def update(self, id, **data):
        return self.do_update(id, **data)

    @use_kwargs()
    def partial_update(self, id, **data):
        return self.do_update(id, **data)

    @marshall()
    def do_update(self, id, **data):
        instance = self.get_object(id=id)

        for k, v in data.items():
            if k == 'id':
                continue
            setattr(instance, k, v)
        instance.save()

        return instance

    @action(methods=['DELETE'], url_path='/', default_response_code=204)
    def delete(self, id):
        instance = self.get_object(id=id)

        instance.delete_instance()
        return 204,

    def get_serializer(self):
        if self.serializer is None:
            return self.Model.get_serializer()
        return self.serializer


class CRUDViewSet(BaseCRUDViewSet):
    @action(methods=['OPTIONS'], needs_id=False, url_path='/')
    def get_schema(self):
        return JSONSchema().dump(self.get_serializer())

    @action(methods=['PUT'], url_path='/')
    def update(self, id):
        return super().update(id)

    @action(methods=['PATCH'], url_path='/')
    def partial_update(self, id):
        return super().partial_update(id)

    @action(needs_id=False)
    def index(self):
        return self.list()


class HTMLCRUDViewSet(BaseCRUDViewSet, TemplateView):
    response_class = HTMLResponse
    fields = None

    @action(methods=['OPTIONS'], needs_id=False, url_path='/')
    def get_options(self):
        return JSONResponse()

    def get_fields(self):
        serializer = self.get_serializer()
        fields = JSONSchema().dump(serializer)['definitions'][serializer.__class__.__name__]
        attribute = f'fields_for_{self.request.action}'
        filter_fields = getattr(self, attribute, None)

        if filter_fields is None and self.fields is None:
            return fields
        elif self.fields is not None:
            filter_fields = self.fields

        properties = fields.pop('properties')
        fields['properties'] = {k: v for k, v in properties.items() if k in filter_fields}
        return fields

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)
        context['fields'] = self.get_fields()
        context['fields']['properties'].pop('id', None)
        for field, value in context['fields']['properties'].items():
            if callable(value.get('default', None)):
                value['default'] = str(value['default']())
        context['headers'] = \
            [{'text': v['title'], 'value': k} for k, v in context['fields']['properties'].items()] + \
            [{'text': '', 'value': '__actions'}]
        context['XSRF'] = {'cookie': settings.CSRF_COOKIE_NAME, 'header': settings.CSRF_HEADER_NAME}
        print(context)
        return context

    @action(needs_id=False)
    def new(self):
        pass

    @action(methods=['POST'], url_path='/')
    def update(self, id):
        return super().update(id)

    @action(needs_id=False)
    def index(self):
        if Cordy.templates is not None:
            Cordy.templates.filters['template_for_field'] = template_for_field
        return self.list()

    def render_response(self, status_code=200, content=None):
        template_name = f'crud/{self.request.action}.html'
        context = self.get_context()
        if content is not None:
            if 'results' in content:
                context['items'] = content['results']
            else:
                context['item'] = content
        try:
            return self.response_class(status_code, content=self.render_template(template_name, context))
        except TemplateNotFound as e:
            log.warning(f'Unable to find template {e}')
            return JSONResponse(status_code, content=content)


class OpenAPIView(TemplateView):

    template_name = 'crud/swagger-ui.html'

    @action(url_path='specification.json', needs_id=False, trailing='')
    def get_spec(self, path):
        import json

        if Cordy.docs is None:
            raise HTTPException(status_code=404)

        return JSONResponse(status_code=200, content=json.dumps(Cordy.docs[path].to_dict()))
