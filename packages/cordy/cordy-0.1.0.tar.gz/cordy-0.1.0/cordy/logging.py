import logging

from log_symbols import LogSymbols


class LoggerWrapper:

    def __init__(self, logger):
        self._log = logger

    def __get__(self, name):
        return getattr(self._log, name)

    def debug(self, message, *args, **kwargs):
        return self._log.debug(f'{message}  {LogSymbols.SUCCESS.value}', *args, **kwargs)

    def info(self, message, *args, **kwargs):
        return self._log.info(f'{message}  {LogSymbols.INFO.value}', *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        return self._log.warning(f'{message}  {LogSymbols.WARNING.value}', *args, **kwargs)

    def error(self, message, *args, **kwargs):
        return self._log.error(f'{message}  {LogSymbols.ERROR.value}', *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        return self._log.critical(f'{message}  {LogSymbols.ERROR.value}', *args, **kwargs)


def getLogger(*args, **kwargs):
    return LoggerWrapper(logging.getLogger(*args, **kwargs))
