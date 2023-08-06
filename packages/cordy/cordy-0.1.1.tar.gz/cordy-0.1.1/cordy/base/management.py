import copy
import warnings

import click

from cordy.conf import settings
from cordy.utils import import_module


class ClickInstantiator:
    klass = None
    command = None

    def __init__(self, command, klass):
        self.command = command
        self.klass = klass

    def __call__(self, *args, **kwargs):
        return self.command(self.klass(), *args, **kwargs)


class BaseCommand:
    pass


def find_final_command(target):
    """Find the last call command at the end of a stack of click.Command instances"""
    while isinstance(target.callback, click.Command):
        target = target.callback
    return target


def find_commands():

    groups = []

    for app in getattr(settings, 'INSTALLED_APPS', []):
        module_name = f'{app}.management'
        try:
            module = import_module(module_name)
        except ImportError:
            continue

        group = click.Group(name=app)

        for classname in dir(module):
            if classname.startswith('__'):
                continue
            klass = getattr(module, classname)
            if not getattr(klass, '__module__', '').startswith(module_name):
                continue
            if not issubclass(klass, BaseCommand):
                continue

            for name in dir(klass):
                command = getattr(klass, name)
                if repr(command).startswith('<function command.'):
                    warnings.warn(
                        f'{classname}.{name}  is wrapped with click.command without parens, please add them'
                    )
                    continue

                if not isinstance(command, click.Command):
                    continue

                command_target = find_final_command(command)
                if not isinstance(command_target.callback, ClickInstantiator):
                    command_target.callback = ClickInstantiator(command_target.callback, klass)
                else:
                    # this is a subclass function, copy it and replace the klass
                    setattr(klass, name, copy.deepcopy(command))
                    command = getattr(klass, name)
                    find_final_command(getattr(klass, name)).callback.klass = klass

                group.add_command(command, name)

        groups.append(group)

    return groups
