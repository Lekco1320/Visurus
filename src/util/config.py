import copy
import pickle

from pathlib import Path
from typing  import *

from .about      import VERSION
from .printer    import print_success
from .appdir     import APPDIR
from .errhandler import errhandler

class field:
    @staticmethod
    def _void(value: Any) -> bool:
        return False
    
    @overload
    def __init__(self, name: str) -> None:
        ...
    
    @overload
    def __init__(self, name: str, default: Any) -> None:
        ...
    
    @overload
    def __init__(self, name: str, default: Any, predicate: Callable) -> None:
        ...
    
    def __init__(self, name: str, default: Any = None, predicate: Callable = _void) -> None:
        self._name      = name
        self._default   = default
        self._predicate = predicate
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def default(self) -> Any:
        return self._default
    
    @property
    def predicate(self) -> Callable:
        return self._predicate
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, field):
            return self._name == value._name and \
                   self._default == value._default and \
                   self._predicate == value._predicate
        return False
    
    def __hash__(self) -> int:
        hash(self._name) ^ hash(self._default) ^ hash(self._predicate)

class config:
    def __init__(self, name: str) -> None:
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    def validate(self, fields: list[field]) -> bool:
        ret = False
        all = set(self.__dict__.keys())
        for field in fields:
            name = field.name
            if not hasattr(self, name) or field.predicate(getattr(self, name)):
                setattr(self, name, field.default)
                ret = True
            all.discard(name)
        for other in all:
            if other.startswith('_'):
                continue
            delattr(self, other)
            ret = True
        return ret

class app_configs:
    def __init__(self) -> None:
        self._version = VERSION
        self._configs = dict()
    
    @property
    def version(self) -> str:
        return self._version
    
    def __getitem__(self, name: str) -> config:
        return self._configs[name]
    
    def __setitem__(self, name: str, value: config):
        self._configs[name] = value
    
    def __delitem__(self, name: str):
        del self._configs[name]
    
    def __contains__(self, name: str) -> bool:
        return name in self._configs

CONFIG_FILE: Path        = APPDIR / "config.bin"
APP_CONFIGS: app_configs = None

@errhandler
def load():
    global APP_CONFIGS
    if not CONFIG_FILE.exists():
        APP_CONFIGS = app_configs()
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
    APP_CONFIGS = app_configs()
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
