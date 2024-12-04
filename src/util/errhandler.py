from .printer import print_error

def errhandler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            print_error(ex.args[0])
    return wrapper
