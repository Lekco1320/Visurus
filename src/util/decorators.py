import readline

from .printer import print_error

def errhandler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print_error(ex.args[0])
    return wrapper

def nohistory(func):
    def wrapper(*args, **kwargs):
        readline.clear_history()
        return func(*args, **kwargs)
    return wrapper

__all__ = ["errhandler", "nohistory"]
