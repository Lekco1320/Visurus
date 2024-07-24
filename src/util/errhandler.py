import util.printer as prt

def errhandler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            prt.error(ex.args[0])
    return wrapper