from marshmallow import Schema
from marshmallow.fields import Int

from cordy.http.parser import parser


class PageNumberPagination:
    query_param = 'page'
    size_param = 'page_size'
    total_key = 'total'
    next_key = 'next'
    previous_key = 'previous'
    default_size = 10

    _data = None

    def __init__(self, controller, qs):
        self.controller = controller
        self.qs = qs
        super()

    def get_schema(self):
        cls_kwargs = dict((
            (self.size_param, Int()),
            (self.query_param, Int()),
        ))
        return type('PaginationSchema', (Schema, ), cls_kwargs)

    def parse(self):
        self._data = parser.parse(self.get_schema(), req=self.controller.request,
                                  location='querystring', validate=False)

    def get_size(self):
        if self._data is None:
            self.parse()

        size = self._data.get(self.size_param, None)
        if size is None:
            size = self.controller.page_size
        if size is None:
            size = self.default_size

        return size

    def get_page(self):
        if self._data is None:
            self.parse(self.controller)

        page = self._data.get(self.query_param, None)
        if page is None:
            page = 1

        return page

    def limit(self, qs):
        page_size = self.get_size()
        return qs.limit(page_size)

    def offset(self, qs):
        offset = (self.get_page() - 1) * self.get_size()
        return qs.offset(offset)

    def get_meta_data(self, data):
        data[self.query_param] = self.get_page()
        data[self.total_key] = self.qs.count()
        data[self.previous_key] = (data[self.query_param] - 1) if data[self.query_param] > 1 else None
        data[self.next_key] = (data[self.query_param] + 1) \
            if data[self.query_param] * self.get_size() < data[self.total_key] \
            else None
