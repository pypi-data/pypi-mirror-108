import os

import coloredlogs
from simple_settings import LazySettings

from cordy import logging

log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

env = os.environ.get('ENV', 'prod')
log.debug(f'Current environment is {env}')

to_load = ['cordy.conf.default']

settings_module = os.environ.get(f'{os.environ.get("CORDY_PREFIX", "")}SETTINGS_MODULE', None)
if settings_module is None:
    to_load.append(f'settings.{env}')

else:
    to_load.append(settings_module)

to_load.append(f"{os.environ.get('CORDY_PREFIX', '')}.environ")

log.debug(f'Loading settings from {to_load}')
settings = LazySettings(*to_load)
