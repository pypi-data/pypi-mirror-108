import os
import signal
import subprocess

import click

from cordy import logging
from cordy.base.management import BaseCommand
from cordy.conf import settings


log = logging.getLogger(__name__)


class Server(BaseCommand):

    @click.command(help='Run development server')
    @click.option('--host', '-h', default='127.0.0.1')
    @click.option('--port', '-p', default='9090')
    @click.option('--gevent', default='1000', help='Number of greenlets')
    @click.option('--websocket/--no-websocket', default=True)
    @click.argument('host_with_port', nargs=-1)
    def runserver(self, host_with_port, host, port, gevent, websocket):
        args = ['uwsgi', '--wsgi-file', os.path.join(settings.BASE_DIR, 'app.py'),
                '--master', '--py-autoreload', '2']

        if len(host_with_port) == 0:
            args += ['--http', f'{host}:{port}']
        else:
            args += ['--http', host_with_port[0]]

        args += ['--gevent', gevent]
        if websocket is True:
            args.append('--http-websocket')
            args += ['--workers', '16']

        subprocess_env = os.environ.copy()
        sigint_handler = signal.getsignal(signal.SIGINT)

        try:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            log.debug(args)
            subprocess.run(args, check=True, env=subprocess_env)
        finally:
            signal.signal(signal.SIGINT, sigint_handler)
