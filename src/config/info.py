from config import *
from util import *

class info:
    def __init__(self, category: str, name: str, key: str, menukey: str, setter, getter = None) -> None:
        self._category = category
        self._name     = name
        self._key      = key
        self._menukey  = menukey
        self._setter   = setter
        self._getter   = getter
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def key(self) -> str:
        return self._key
    
    @property
    def menukey(self) -> str:
        return self._menukey
    
    def set(self):
        self._setter(Config[self._key])
    
    def get(self):
        if callable(self._getter):
            return self._getter(Config[self._key])
        return None
    
    def show(self):
        if callable(self._getter):
            print_kv(self._name, self.get())
        else:
            print_left(f'{self._name}:…')
