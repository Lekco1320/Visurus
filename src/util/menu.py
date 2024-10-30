from util import *
from util import ansi

from abc import ABC
from abc import abstractmethod

class item(ABC):
    def __init__(self, enfunc = None) -> None:
        super().__init__()
        
        self._enfunc = enfunc
    
    @property
    def enabled(self):
        return self._enfunc() if callable(self._enfunc) else True
    
    @abstractmethod
    def show(self):
        pass

class option(item):
    def __init__(self, key: str, text: str, jmpfunc = None, valfunc = None, enfunc = None):
        super().__init__(enfunc)
        
        self._key     = key
        self._text    = text
        self._jmpfunc = jmpfunc
        self._valfunc = valfunc
    
    @property
    def key(self) -> str:
        return self._key
    
    @property
    def text(self) -> str:
        return self._text
    
    @property
    def value(self):
        if   callable(self._valfunc):
            return self._valfunc()
        elif isinstance(self._valfunc, str):
            return self._valfunc
        elif isinstance(self._valfunc, ansi.ansi_str):
            return self._valfunc
        elif isinstance(self._valfunc, ansi.ansi_stream):
            return self._valfunc
        return None
    
    def show(self):
        print_option(self._key, self._text, self.value)
    
    def jump(self):
        if callable(self._jmpfunc):
            self._jmpfunc()
    
    def __eq__(self, value: object) -> bool:
        if   isinstance(value, option):
            return self._key == value._key
        elif isinstance(value, str):
            return self._key == value
        return False
    
    def __hash__(self) -> int:
        return hash(self._key)

class splitter(item):
    def __init__(self, text: str, enfunc = None):
        super().__init__(enfunc)
        
        self._text = text
    
    @property
    def text(self):
        return self._text
    
    def show(self):
        if isinstance(self._text, str):
            print_center(ansi.ansi_str(self._text, ansi.ansi_format(ansi.style.BOLD, ansi.color.WHITE)))
        else:
            print_left(self._text)
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, splitter):
            return self._text == value._text
        return False

    def __hash__(self) -> int:
        return hash(self._text)

class display(item):
    def __init__(self, content):
        self._content = []
        self._content.append(content)
    
    @property
    def content(self):
        return self._content
    
    def show(self):
        for item in self._content:
            if   callable(item):
                item()
            else:
                print_left(item.__str__())

class menu:
    def __init__(self, name: str, canceller: str = None) -> None:
        self._name      = name
        self._canceller = canceller
        self._display   = []
        self._items     = []
        self._flag      = True

    @property
    def name(self):
        return self._name
    
    @property
    def canceller(self):
        return self._canceller
    
    @property
    def display(self):
        return self._display
    
    @property
    def items(self):
        return self._items
    
    def add(self, obj: item):
        if   isinstance(obj, option):
            self._items.append(obj)
        elif isinstance(obj, splitter):
            self._items.append(obj)
        elif isinstance(obj, display):
            self._display.append(obj)
        else:
            raise TypeError(f'Unsupported type \'{type(obj).__name__}\'.')
    
    def exit(self):
        self._flag = False
    
    def run(self):
        while self._flag:
            clear_screen()
            print_title(self._name)
            
            for display in self._display:
                display.show()
            
            for item in self._items:
                if item.enabled:
                    item.show()
            print_spliter()
            
            key = get_input().strip().upper()
            result = [item for item in self._items if isinstance(item, option) and item.enabled and item == key]
            if len(result) < 1:
                continue
            
            opt = result[0]
            up_line()
            print_output(f'{opt.key} | {opt.text}')
            
            opt.jump()
            if key == self._canceller:
                break
            if self._canceller == None:
                break
