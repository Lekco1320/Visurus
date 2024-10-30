from util import printer

def errhandler(func):
    def wrapper(*args, **kwargs):
        #try:
            return func(*args, **kwargs)
        #except Exception as ex:
        #    printer.print_error(ex.args[0])
    return wrapper