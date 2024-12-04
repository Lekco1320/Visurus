import copy
import pickle

from pathlib import Path
from typing  import Any

from .printer    import print_success, wait
from .appdir     import APPDIR
from .errhandler import errhandler

class config:
    def __init__(self, name: str, default: dict[str, Any]) -> None:
        self._name = name
        self._default = default
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def default(self) -> dict[str, Any]:
        return self._default

    @default.setter
    def default(self, value: dict[str, Any]):
        self._default = value
    
    def set_default(self) -> bool:
        has_set = False
        for key, value in self._default.items():
            if not hasattr(self, key):
                setattr(self, key, value)
                has_set = True
        return has_set
    
    def cut_attrs(self):
        has_cut = False
        items   = dict(self.__dict__.items())
        for key, _ in items.items():
            if not key.startswith('_') and key not in self._default:
                delattr(self, key)
                has_cut = True
        return has_cut

CONFIG_FILE: Path          = APPDIR / "config.bin"
configs: dict[str, config] = {}

@errhandler
def load():
    global configs
    if not CONFIG_FILE.exists():
        configs = {}
        return

    with open(CONFIG_FILE, 'rb') as file:
        configs = pickle.load(file)

@errhandler
def _save() -> bool:
    with open(CONFIG_FILE, 'wb') as file:
        pickle.dump(configs, file)
        return True
    return False

@errhandler
def save(config: config):
    configs[config.name] = config
    if _save():
        print_success('首选项保存成功.')

def get(name: str, default: dict[str, Any]) -> config:
    need_save = False
    ret       = None
    if name not in configs:
        ret = config(name, default)
        need_save |= ret.set_default()
        configs[name] = ret
    else:
        ret = configs[name]
        ret.default = default
        need_save |= ret.cut_attrs()
        need_save |= ret.set_default()
    if need_save:
        _save()
    return copy.deepcopy(ret)

def clear():
    global configs
    configs = {}
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()

load()
