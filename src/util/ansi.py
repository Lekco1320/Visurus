from enum import Enum
from enum import Flag

class color(Enum):
    DEFAULT = 8
    BLACK   = 0
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    MAGENTA = 5
    CYAN    = 6
    WHITE   = 7

class style(Flag):
    DEFAULT       = 0
    BOLD          = 1
    FAINT         = 2
    ITALIC        = 4
    UNDERLINED    = 8
    SLOW_BLINK    = 16
    RAPID_BLINK   = 32
    SWAP_COLOR    = 64
    HIDE          = 128
    STRIKETHROUGH = 256

STYLE_DICT : dict = { 
    style.BOLD          : 1,
    style.FAINT         : 2,
    style.ITALIC        : 3,
    style.UNDERLINED    : 4,
    style.SLOW_BLINK    : 5,
    style.RAPID_BLINK   : 6,
    style.SWAP_COLOR    : 7,
    style.HIDE          : 8,
    style.STRIKETHROUGH : 9
}

class format:
    CONTROL_CODE = '\033['
    
    def __init__(self, style = style.DEFAULT, foreground = color.DEFAULT, background = color.DEFAULT) -> None:
        self._style      = style
        self._foreground = foreground
        self._background = background
    
    @property
    def style(self) -> style:
        return self._style
    
    @style.setter
    def style(self, value):
        self._style = value
    
    @property
    def foreground(self) -> color:
        return self._foreground
    
    @foreground.setter
    def foreground(self, value):
        self._foreground = value
    
    @property
    def background(self) -> color:
        return self._background
    
    @background.setter
    def background(self, value):
        self._background = value
    
    def enable(self) -> str:
        ret = format.disable()
        for style in self._style:
            ret += f'{format.CONTROL_CODE}{STYLE_DICT[style]}m'
        if  self._foreground != color.DEFAULT:
            ret += f'{format.CONTROL_CODE}3{self._foreground.value}m'
        if  self._background != color.DEFAULT:
            ret += f'{format.CONTROL_CODE}4{self._background.value}m'
        return ret
    
    @staticmethod
    def disable() -> str:
        return f'{format.CONTROL_CODE}0m'

class fstr:
    def __init__(self, text : str, format = format()) -> None:
        self._text   = text
        self._format = format
        self._ptr    = 0
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
    
    @property
    def format(self) -> format:
        return self._format
    
    @format.setter
    def format(self, value):
        self._format = value
    
    def __str__(self) -> str:
        return self._format.enable() + self._text + format.disable()
    
    def __len__(self) -> int:
        return self._text.__len__()
    
    def __add__(self, _str) -> 'fstrs':
        if   isinstance(_str, fstr):
            return fstrs(self, _str)
        elif isinstance(_str, str):
            return fstrs(self, fstr(_str))
        elif isinstance(_str, fstrs):
            return self + _str
        else:
            raise TypeError(f'Unsupported type \'{type(_str).__name__}\'.')

    def __radd__(self, _str) -> 'fstrs':
        if   isinstance(_str, fstr):
            return fstrs(_str, self)
        elif isinstance(_str, str):
            return fstrs(fstr(_str), self)
        elif isinstance(_str, fstrs):
            return _str + self
        else:
            raise TypeError(f'Unsupported type \'{type(_str).__name__}\'.')

    def __mul__(self, times : int) -> 'fstr':
        return fstr(self._text * times, self._format)
    
    def __iter__(self) -> 'fstr':
        self._ptr = 0
        return self
    
    def __next__(self) -> str:
        if self._ptr >= self._text.__len__():
            raise StopIteration
        self._ptr += 1
        return self._text[self._ptr - 1]

class fstrs: 
    def __init__(self, *args) -> None:
        self._fstrs = []
        self._ptr  = 0
        self._text = ''
        for str in args:
            self._fstrs.append(str)

    def __add__(self, _fstr : str | fstr) -> 'fstrs':
        if isinstance(_fstr, fstr):
            self._fstrs.append(_fstr)
        elif isinstance(_fstr, str):
            self._fstrs.append(fstr(_fstr))
        elif isinstance(_fstr, fstrs):
            for fs in _fstr._fstrs:
                self._fstrs.append(fs)
        return self

    def __radd__(self, _fstr : str | fstr) -> 'fstrs':
        if isinstance(_fstr, fstr):
            self._fstrs.insert(0, _fstr)
        elif isinstance(_fstr, str):
            self._fstrs.insert(0, fstr(_fstr))
        elif isinstance(_fstr, fstrs):
            for fs in _fstr._fstrs:
                self._fstrs.insert(0, fs)
        return self

    def __len__(self) -> int:
        len = 0
        for str in self._fstrs:
            len += str.__len__()
        return len

    def __str__(self) -> str:
        ret = ''
        for str in self._fstrs:
            ret += str.__str__()
        return ret
    
    def __iter__(self) -> 'fstrs':
        self._ptr  = 0
        self._text = ''
        for fstr in self._fstrs:
            self._text += fstr.text
        return self
    
    def __next__(self) -> str:
        if self._ptr >= self._text.__len__():
            raise StopIteration
        self._ptr += 1
        return self._text[self._ptr - 1]

def clear_all():
    print(f'{format.CONTROL_CODE}2J', end='')
    print(f'{format.CONTROL_CODE}1;1H', end='')

def clear_line():
    print(f'{format.CONTROL_CODE}2K', end='')
    print(f'{format.CONTROL_CODE}H', end='')

def upper_line():
    print('\033[1A', end='')
