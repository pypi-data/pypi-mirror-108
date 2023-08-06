from cordy.auth.models import get_user_model
from cordy.middlewares import BaseMiddleware


class SessionMiddleware(BaseMiddleware):

    def before(self, enviro):
        session = enviro.get('beaker.session', None)
        if session is None:
            return
        if 'user_id' not in session:
            return

        User = get_user_model()
        try:
            enviro['cordy.user'] = User.get(id=session['user_id'])
        except User.DoesNotExist:
            session.invalidate()
            session.save()
