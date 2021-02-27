import builtins
import datetime


def print(string, silent: bool = False, logging: bool = False, path_log: str = 'log.log', end: str = '\n',
          sep: str = ' '):
    """ Wrapper over builtins print. Allows logging"""
    if logging:
        with open(path_log, 'a') as file:
            file.write(str(datetime.datetime.now()) + ' ' + string + end)
    if not silent:
        builtins.print(string, sep=sep, end=end)
