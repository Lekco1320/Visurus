import copy
import pickle

from .              import about
from .              import appdir
from pathlib        import Path
from util.config    import *
from util.decorators import errhandler
from util.printer   import print_success

CONFIG_FILE: Path        = appdir.APPDIR / "config.bin"
APP_CONFIGS: app_configs = None

@errhandler
def load():
    global APP_CONFIGS
    if not CONFIG_FILE.exists():
        APP_CONFIGS = app_configs(about.VERSION)
        return

    with open(CONFIG_FILE, 'rb') as file:
        APP_CONFIGS = pickle.load(file)

@errhandler
def _save() -> bool:
    with open(CONFIG_FILE, 'wb') as file:
        pickle.dump(APP_CONFIGS, file)
        return True
    return False

@errhandler
def save(config: config):
    APP_CONFIGS[config.name] = config
    if _save():
        print_success('首选项保存成功.')

def get(name: str, fields: list[field]) -> config:
    if APP_CONFIGS == None:
        load()
    
    need_save = False
    ret       = None
    if name not in APP_CONFIGS:
        ret = config(name)
        ret.validate(fields)
        APP_CONFIGS[name] = ret
        need_save         = True
    else:
        ret       = APP_CONFIGS[name]
        need_save = ret.validate(fields)
    if need_save:
        _save()
    return copy.deepcopy(ret)

def clear():
    global APP_CONFIGS
    APP_CONFIGS = app_configs(about.VERSION)
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
