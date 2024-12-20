from .printer    import *
from .ansi       import *
from .decorators import *

from abc    import ABC
from abc    import abstractmethod
from enum   import Enum
from typing import overload

class Item(ABC):
    def __init__(self, enfunc = None) -> None:
        super().__init__()
        self._enfunc = enfunc
    
    @property
    def enabled(self):
        return self._enfunc() if callable(self._enfunc) else True
    
    @abstractmethod
    def show(self):
        pass

class Option(Item):
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
        elif isinstance(self._valfunc, AnsiStr):
            return self._valfunc
        elif isinstance(self._valfunc, AnsiStream):
            return self._valfunc
        return None
    
    def show(self):
        print_option(self._key, self._text, self.value)
    
    def jump(self):
        if callable(self._jmpfunc):
            self._jmpfunc()
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Option):
            return self._key == value._key
        return False
    
    def __hash__(self) -> int:
        return hash(self._key)

class FixedOptionPlacement(Enum):
    TOP    = 0
    BOTTOM = 1

class FixedOption(Option):
    def __init__(self, key, text, jmpfunc=None, valfunc=None, enfunc=None, placement=FixedOptionPlacement.BOTTOM):
        super().__init__(key, text, jmpfunc, valfunc, enfunc)
        self._placement = placement
    
    @property
    def placement(self):
        return self._placement

class Splitter(Item):
    def __init__(self, text: str, enfunc = None):
        super().__init__(enfunc)
        self._text = text
    
    @property
    def text(self):
        return self._text
    
    def show(self):
        if isinstance(self._text, str):
            print_center(AnsiStr(self._text, AnsiFormat(AnsiStyle.BOLD, AnsiColor.WHITE)))
        else:
            print_left(self._text)
    
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Splitter):
            return self._text == value._text
        return False

    def __hash__(self) -> int:
        return hash(self._text)

class Display(Item):
    def __init__(self, content):
        self._content = []
        self._content.append(content)
    
    @property
    def content(self):
        return self._content
    
    def show(self):
        for item in self._content:
            if callable(item):
                item()
            else:
                print_left(item.__str__())

class Menu:
    def __init__(self, title: str, retsign: str = None, pagesize: int = 32) -> None:
        self._title    : str               = title
        self._retsign  : str               = retsign
        self._displays : list[Display]     = []
        self._items    : list[Item]        = []
        self._foptions : list[FixedOption] = []
        self._flag     : bool              = True
        self._pagesize : int               = pagesize
        self._pages    : list[list[Item]]  = []
        self._curpage  : int               = 0
    
    @property
    def title(self):
        return self._title
    
    @property
    def retsign(self):
        return self._retsign
    
    @property
    def display(self):
        return self._displays
    
    @property
    def items(self):
        return self._items
    
    @property
    def pagesize(self):
        return self._pagesize
        
    @overload
    def add(self, option: Option) -> None: 
        ...
    
    @overload
    def add(self, fixed_option: FixedOption) -> None:
        ...
    
    @overload
    def add(self, splitter: Splitter) -> None:
        ...
    
    @overload
    def add(self, display: 'Display') -> None:
        ...
    
    def add(self, obj: Item):
        if   isinstance(obj, FixedOption):
            self._foptions.append(obj)
        elif isinstance(obj, Option):
            self._items.append(obj)
        elif isinstance(obj, Splitter):
            self._items.append(obj)
        elif isinstance(obj, Display):
            self._displays.append(obj)
        else:
            raise TypeError(f'Unsupported type \'{type(obj).__name__}\'.')
    
    def exit(self):
        self._flag = False
    
    def _show(self):
        true_clear_screen()
        print_title(self._title)
        for display in self._displays:
            display.show()
        if len(self._pages) == 0:
            return
        for item in self._pages[self._curpage]:
            if item.enabled:
                item.show()
        print_splitter()
        if len(self._pages) > 1:
            print(f'* 按下\'Enter\'以切换页面({self._curpage + 1}/{len(self._pages)}).')
    
    @nohistory
    def _get_key(self) -> str:
        return get_input().strip().upper()
    
    def _jump(self, key: str) -> bool:
        if key == self._retsign:
            return True
        if len(self._pages) == 0:
            return False
        for item in self._pages[self._curpage]:
            if isinstance(item, Option) and item.key == key and item.enabled:
                up_line()
                print_output(f'{item.key} | {item.text}')
                item.jump()
                break
        return self._retsign == None
    
    def _fill_page_top(self, page: list[Option]):
        index = 0
        while len(page) < self._pagesize and index < len(self._foptions):
            if self._foptions[index].placement == FixedOptionPlacement.TOP:
                page.append(self._foptions[index])
            index += 1
    
    def _fill_page_bottom(self, page: list[Option]):
        index = 0
        while len(page) < self._pagesize and index < len(self._foptions):
            if self._foptions[index].placement == FixedOptionPlacement.BOTTOM:
                page.append(self._foptions[index])
            index += 1
    
    def _fill_page(self, page: list[Option], index: int) -> int:
        if len(self._foptions) >= self._pagesize:
            self._fill_page_top(page)
            self._fill_page_bottom(page)
            return len(self._items)
        
        self._fill_page_top(page)
        item = self._items[index]
        if self._pagesize > 1 and not isinstance(item, Splitter):
            last_splitter = None
            for i in range(index - 1, -1, -1):
                if isinstance(self._items[i], Splitter):
                    last_splitter = self._items[i]
                    break
            if last_splitter != None:
                page.append(last_splitter)
        
        insert = len(page)
        self._fill_page_bottom(page)
        while index < len(self._items) and len(page) < self._pagesize:
            page.insert(insert, self._items[index])
            index  += 1
            insert += 1
        return index
    
    def _divide_pages(self):
        self._pages.clear()
        self._curpage = 0
        index         = 0
        while index < len(self._items):
            page  = []
            index = self._fill_page(page, index)
            self._pages.append(page)
    
    def _change_page(self):
        pcount = len(self._pages)
        if pcount > 0:
            self._curpage = (self._curpage + 1) % pcount
    
    def run(self):
        self._divide_pages()
        while self._flag:
            self._show()
            key = self._get_key()
            if   key == '':
                self._change_page()
            elif self._jump(key):
                break

__all__ = [
    "Option", "Display", "FixedOptionPlacement",
    "FixedOption", "Splitter", "Menu"
]
