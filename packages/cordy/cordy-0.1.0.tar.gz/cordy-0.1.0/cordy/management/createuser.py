from getpass import getpass

import click

from cordy import Cordy, logging
from cordy.auth.models import get_user_model
from cordy.base.management import BaseCommand
from cordy.conf import settings


log = logging.getLogger(__name__)


class Command(BaseCommand):

    @click.command(help='Create user')
    @click.argument('email')
    def createuser(self, email):
        assert settings.DATABASE is not None, 'Unable to create user without DATABASE setting'
        assert settings.USER_MODEL is not None, 'USER_MODEL not set'

        User = get_user_model()

        password = ''
        while password == '':
            password = getpass('Please choose a password: ')
        confirm = getpass('Please confirm the choosen password: ')

        assert password == confirm, 'Passwords do not match'

        if Cordy.db is None or Cordy.db.obj is None:
            Cordy.init_db()

        user = User.create(email=email, password=password)

        log.info(f'User created for {user.email}')
