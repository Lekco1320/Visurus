import pickle
import readline

from pathlib     import Path
from .errhandler import errhandler
from .appdir     import APPDIR

HISTORY_FILE: Path              = APPDIR / 'history.bin'
histories: dict[str, list[str]] = {}

@errhandler
def read_history():
    global histories
    if not HISTORY_FILE.exists():
        histories = {}
        readline.clear_history()
        return
    
    with open(HISTORY_FILE, 'rb') as file:
        histories = pickle.load(file)

def load_history(key: str):
    if not key in histories:
        histories[key] = []
    items = histories[key]
    for item in items:
        readline.add_history(item)

@errhandler
def save_distory(key: str):
    items = histories[key]
    items.clear()
    for i in range(readline.get_current_history_length()):
        item = readline.get_history_item(i + 1).strip()
        if item != '' and item not in items:
            items.append(item)
    with open(HISTORY_FILE, 'wb') as file:
        pickle.dump(histories, file)

def clear_history():
    global histories
    histories = {}
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()

def history(key: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            readline.clear_history()
            load_history(key)
            ret = func(*args, **kwargs)
            save_distory(key)
            return ret
        return wrapper
    return decorator

def nohistory(func):
    def wrapper(*args, **kwargs):
        readline.clear_history()
        return func(*args, **kwargs)
    return wrapper

read_history()
