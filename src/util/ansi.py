from enum import Enum
from enum import Flag
from typing import *

class color(Enum):
    DEFAULT        = -1
    BLACK          = 0
    RED            = 1
    GREEN          = 2
    YELLOW         = 3
    BLUE           = 4
    MAGENTA        = 5
    CYAN           = 6
    WHITE          = 7
    BRIGHT_BLACK   = 8
    BRIGHT_RED     = 9
    BRIGHT_GREEN   = 10
    BRIGHT_YELLOW  = 11
    BRIGHT_BLUE    = 12
    BRIGHT_MAGENTA = 13
    BRIGHT_CYAN    = 14
    BRIGHT_WHITE   = 15

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

STYLE_DICT: dict = { 
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

class ansi_format: 
    CONTROL_CODE = '\033['
    
    def __init__(self, style = style.DEFAULT,
                 foreground  = color.DEFAULT,
                 background  = color.DEFAULT) -> None:
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
    
    @property
    def enable_ansi(self) -> str:
        ret = self.disable_ansi
        for style in self._style:
           ret += f'{ansi_format.CONTROL_CODE}{STYLE_DICT[style]}m'
        if self._foreground != color.DEFAULT:
           ret += f'{ansi_format.CONTROL_CODE}3{self._foreground.value % 8}' + \
                  (';1' if (self._foreground.value & 8) > 0 else '') + 'm'
        if self._background != color.DEFAULT:
           ret += f'{ansi_format.CONTROL_CODE}4{self._background.value % 8}' + \
                  (';1' if (self._background.value & 8) > 0 else '') + 'm'
        return ret
    
    @property
    def disable_ansi(self) -> str:
        return f'{ansi_format.CONTROL_CODE}0m'
    
    def copy(self) -> 'ansi_format':
        return ansi_format(self._style, self._foreground, self._background)
    
    def __eq__(self, value: object) -> bool:
        if  not isinstance(value, ansi_format):
            return False
        return self._style == value._style and \
               self._foreground == value._foreground and \
               self._background == value._background
    
    def __repr__(self) -> str:
        return f'format{{{self._style}, {self._foreground}, {self._background}}}'
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __hash__(self) -> int:
        hash((self._style, self._foreground, self._background))

DEFAULT_FORMAT = ansi_format()
ERROR_FORMAT   = ansi_format(foreground=color.BRIGHT_RED)
PS_FORMAT      = ansi_format(foreground=color.BLUE)

class ansi_str:
    def __init__(self, str: str, format: ansi_format) -> None:
        self._str    = str
        self._format = format
        
    @property
    def str(self) -> str:
        return self._str
    
    @str.setter
    def str(self, value: 'str'):
        self._str = value
    
    @property
    def format(self) -> ansi_format:
        return self._format
    
    @format.setter
    def format(self, value: format):
        self._format = value
    
    def copy(self) -> 'ansi_str':
        return ansi_str(self._str, self._format.copy())
    
    def __iter__(self):
        return iter(self._str)
    
    def __str__(self) -> 'str':
        return self._format.enable_ansi + self.str + self._format.disable_ansi
    
    def __repr__(self) -> 'str':
        return f'ansi_str{{"{self._str}", {self._format}}}'
    
    def __len__(self) -> int:
        return self._str.__len__()
    
    def __getitem__(self, index) -> 'str':
        return self._str[index]

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ansi_str):
            return False
        return self._format == value._format and self.str == value.str
    
    def __hash__(self) -> int:
        return hash((self._format, self._str))
    
    def __add__(self, other: Union['str', 'ansi_str', 'ansi_stream']) -> 'ansi_stream':
        if isinstance(other, str):
            astr = ansi_str(other, ansi_format())
            return ansi_stream([self, astr])
        if isinstance(other, ansi_str):
            return ansi_stream([self, other])
        if isinstance(other, ansi_stream):
            ret = other.copy()
            ret._astrs.insert(0, self)
            return ret
    
    def __radd__(self, other: Union['str', 'ansi_str', 'ansi_stream']) -> 'ansi_stream':
        if isinstance(other, str):
            astr = ansi_str(other, ansi_format())
            return ansi_stream([astr, self])
        if isinstance(other, ansi_str):
            return ansi_stream([other, self])
        if isinstance(other, ansi_stream):
            ret = other.copy()
            ret._astrs.append(self)
            return ret

class ansi_stream:
    @overload
    def __init__(self, strs: None) -> None:
        ...
    
    @overload
    def __init__(self, astr: ansi_str) -> None:
        ...
    
    @overload
    def __init__(self, astrs: Iterable[ansi_str]) -> None:
        ...
    
    @overload
    def __init__(self, stream: 'ansi_stream') -> None:
        ...
    
    def __init__(self, strs: Union[None, ansi_str, Iterable[ansi_str], 'ansi_stream'] = None) -> None:
        self._astrs: list[ansi_str] = []
        if  isinstance(strs, ansi_str):
            self._astrs.append(strs)
        elif isinstance(strs, ansi_stream):
            for astr in strs._astrs:
                self._astrs.append(astr.copy())
        elif isinstance(strs, Iterable):
            for astr in strs:
                if not isinstance(astr, ansi_str):
                    raise ValueError('Unknown str type.')
                self._astrs.append(astr.copy())
    
    def copy(self) -> 'ansi_stream':
        ret = ansi_stream()
        for astr in self._astrs:
            ret._astrs.append(astr)
        return ret
    
    def plain_str(self) -> str:
        return ''.join(astr.str for astr in self._astrs)
    
    def __str__(self) -> str:
        return ''.join(astr.__str__() for astr in self._astrs)
    
    def __len__(self) -> int:
        return sum([astr.__len__() for astr in self._astrs])
    
    def __iter__(self):
        return iter(''.join(astr._str for astr in self._astrs))
    
    def __add__(self, other: Union[str, ansi_str, 'ansi_stream']) -> 'ansi_stream':
        ret = self.copy()
        if isinstance(other, str):
            ret._astrs.append(ansi_str(other, ansi_format()))
            return ret
        if isinstance(other, ansi_str):
            ret._astrs.append(other)
            return ret
        if isinstance(other, ansi_stream):
            for astr in other._astrs:
                ret._astrs.append(astr)
            return ret
    
    def __radd__(self, other: Union[str, ansi_str, 'ansi_stream']) -> 'ansi_stream':
        if isinstance(other, str):
            ret = self.copy()
            ret._astrs.insert(0, ansi_str(other, ansi_format()))
            return ret
        if isinstance(other, ansi_str):
            ret = self.copy()
            ret._astrs.insert(0, other)
            return ret
        if isinstance(other, ansi_stream):
            ret = other.copy()
            for astr in self._astrs:
                ret._astrs.append(astr)
            return ret
    
    def __getitem__(self, index) -> str:
        for astr in self._astrs:
            if 0 <= index < astr.__len__():
                return astr[index]
            index -= astr.__len__()
        raise IndexError('Index out of range.')

FORMAT_VALUE   = ansi_format(foreground=color.CYAN)
FORMAT_TITLE   = ansi_format(style.BOLD, color.WHITE)
FORMAT_ERROR   = ansi_format(foreground=color.RED)
FORMAT_SUCCESS = ansi_format(foreground=color.GREEN)
FORMAT_PS      = ansi_format(style=style.FAINT)
FORMAT_OPTION  = ansi_format(foreground=color.YELLOW)
FORMAT_ANNO    = ansi_format(style.ITALIC | style.FAINT)
