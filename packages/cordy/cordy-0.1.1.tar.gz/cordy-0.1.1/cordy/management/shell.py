import click

from cordy.base.exceptions import CommandException
from cordy.base.management import BaseCommand


class Shell(BaseCommand):

    shells = ['ipython', 'bpython', ]  # 'python']

    def ipython(self, options):
        from IPython import start_ipython
        start_ipython(argv=[])

    def bpython(self, options):
        import bpython
        bpython.embed()

    # def python(self, options):
    #     import os
    #     import code
    #     # Set up a dictionary to serve as the environment for the shell, so
    #     # that tab completion works on objects that are imported at runtime.
    #     imported_objects = {}
    #     try:  # Try activating rlcompleter, because it's handy.
    #         import readline
    #     except ImportError:
    #         pass
    #     else:
    #         # We don't have to wrap the following import in a 'try', because
    #         # we already know 'readline' was imported successfully.
    #         import rlcompleter
    #         readline.set_completer(rlcompleter.Completer(imported_objects).complete)
    #         # Enable tab completion on systems using libedit (e.g. macOS).
    #         # These lines are copied from Python's Lib/site.py.
    #         readline_doc = getattr(readline, '__doc__', '')
    #         if readline_doc is not None and 'libedit' in readline_doc:
    #             readline.parse_and_bind("bind ^I rl_complete")
    #         else:
    #             readline.parse_and_bind("tab:complete")

    #     # We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
    #     # conventions and get $PYTHONSTARTUP first then .pythonrc.py.
    #     if not options['no_startup']:
    #         for pythonrc in OrderedSet([os.environ.get("PYTHONSTARTUP"), os.path.expanduser('~/.pythonrc.py')]):
    #             if not pythonrc:
    #                 continue
    #             if not os.path.isfile(pythonrc):
    #                 continue
    #             with open(pythonrc) as handle:
    #                 pythonrc_code = handle.read()
    #             # Match the behavior of the cpython shell where an error in
    #             # PYTHONSTARTUP prints an exception and continues.
    #             try:
    #                 exec(compile(pythonrc_code, pythonrc, 'exec'), imported_objects)
    #             except Exception:
    #                 traceback.print_exc()

    #     code.interact(local=imported_objects)

    @click.command(help='Open a python shell with Cordy pre-loaded')
    def shell(self):
        for shell in self.shells:
            try:
                return getattr(self, shell)({})
            except ImportError:
                pass
        raise CommandException(f"Couldn't import {shell} interface.")
