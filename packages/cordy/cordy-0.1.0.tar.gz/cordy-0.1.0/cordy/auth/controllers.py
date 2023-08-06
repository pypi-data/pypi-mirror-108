from marshmallow import ValidationError

from cordy.auth.models import get_user_model
from cordy.auth.serializers import LoginSchema
from cordy.base import Controller
from cordy.base.decorators import action
from cordy.http.exceptions import HTTPException
from cordy.http.responses import Response


class AuthController(Controller):

    @action(needs_id=False, methods=['POST'])
    def login(self):
        try:
            result = LoginSchema().loads(self.request.body)
        except ValidationError as e:
            rv = HTTPException(400, e.messages)
            rv.headers['Content-Type'] = 'application/json'
            raise rv

        try:
            user = get_user_model().get(email=result['email'])
        except get_user_model().DoesNotExist:
            raise HTTPException(401, 'Invalid email or password')

        if user.check_password(result['password']):
            user.login(self.request)
        else:
            raise HTTPException(401, 'Invalid email or password')

        return Response(204)

    @action(needs_id=False, methods=['POST'])
    def logout(self):
        get_user_model().logout(self.request)
        return Response(204)

    @action(needs_id=False)
    def me(self):
        user = self.request.user
        if user is None:
            email = 'Anonymous'
        else:
            email = user.email

        return Response(content=email)
