import util
import copy
import pickle

from . import about
from . import appdir

from pathlib import Path

CONFIG_FILE: Path            = appdir.APPDIR / "config.bin"
APP_CONFIGS: util.AppConfigs = None

@util.errhandler
def load():
    global APP_CONFIGS
    if not CONFIG_FILE.exists():
        APP_CONFIGS = util.AppConfigs(about.VERSION)
        return

    with open(CONFIG_FILE, 'rb') as file:
        APP_CONFIGS = pickle.load(file)

@util.errhandler
def _save() -> bool:
    with open(CONFIG_FILE, 'wb') as file:
        pickle.dump(APP_CONFIGS, file)
        return True
    return False

@util.errhandler
def save(config: util.Config):
    APP_CONFIGS[config.name] = config
    if _save():
        util.print_success('首选项保存成功.')

def get(name: str, fields: list[util.Field]) -> util.Config:
    if APP_CONFIGS == None:
        load()
    
    need_save = False
    ret       = None
    if name not in APP_CONFIGS:
        ret = util.Config(name)
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
    APP_CONFIGS = util.AppConfigs(about.VERSION)
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
