from cordy.auth.decorators import login_required, authorize_with
from cordy.auth.permissions import AllowAll
from cordy.base import Controller as CordyController, WSController as CordyWSController, TemplateView
from cordy.base.decorators import action
from cordy import Cordy
from cordy.crud.controllers import CRUDViewSet, HTMLCRUDViewSet
from cordy.crud.pagination import PageNumberPagination
from cordy.http.responses import HTMLResponse

from .models import ToDo


class Controller(CordyController):

    @action(needs_id=False)
    def index(self):
        return HTMLResponse(content="<h1>Hello World</h1>")


class Routes(TemplateView):

    def get_context(self, **kwargs):
        context = super().get_context(**kwargs)

        url_map = Cordy.mapper._routenames.values()
        context['items'] = [
            (r.name, r.regpath)
            for r in url_map
        ]

        context['user'] = self.request.user

        return context


class ToDoViewSet(CRUDViewSet):

    Model = ToDo
    pagination_class = PageNumberPagination
    page_size = 2
    filter_fields = ['is_done']
    search_fields = ['description', ]


@authorize_with(AllowAll)
class ToDoHTML(HTMLCRUDViewSet):

    Model = ToDo

    @action(needs_id=False)
    @login_required()
    def index(self, *args, **kwargs):
        return super().index(*args, **kwargs)


class WSController(CordyWSController):

    def on_connect(self):
        print('WS Connect')

    def on_receive(self, data):
        self.send(data['data'])

    def on_message(self, message):
        print('Received message:', message)

    def on_disconnect(self):
        print('WS Disconnected')

