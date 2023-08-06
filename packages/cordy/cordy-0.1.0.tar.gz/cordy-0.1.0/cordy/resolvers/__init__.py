import os

from cordy.base.exceptions import FileNotFoundException
from cordy.conf import settings


class FSResolver:

    config_var = 'STATIC_ROOT'
    default_value = []

    def get_dirs_for(self, var):
        rv = settings.get(var, self.default_value)
        if not isinstance(rv, list) and not isinstance(rv, tuple):
            rv = [rv]
        return rv

    def __init__(self, dirs=None):
        self.dirs = dirs if dirs is not None else self.get_dirs_for(self.config_var)

    def resolve(self, name, return_file=True, **kwargs):
        for directory in self.dirs:
            path = os.path.join(directory, name)
            if os.path.exists(path):
                if return_file is True:
                    return self.open(path, **kwargs)
                else:
                    return directory
        raise FileNotFoundException

    def open(self, path, **kwargs):
        if 'mode' not in kwargs:
            kwargs['mode'] = 'r'

        return open(path, **kwargs)
