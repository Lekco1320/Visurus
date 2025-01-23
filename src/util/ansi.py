from bisect import bisect_right

from enum import Enum
from enum import Flag

from typing import *

class AnsiColor(Enum):
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

class AnsiStyle(Flag):
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
    AnsiStyle.BOLD          : 1,
    AnsiStyle.FAINT         : 2,
    AnsiStyle.ITALIC        : 3,
    AnsiStyle.UNDERLINED    : 4,
    AnsiStyle.SLOW_BLINK    : 5,
    AnsiStyle.RAPID_BLINK   : 6,
    AnsiStyle.SWAP_COLOR    : 7,
    AnsiStyle.HIDE          : 8,
    AnsiStyle.STRIKETHROUGH : 9
}

class AnsiFormat: 
    CONTROL_CODE = '\033['
    
    def __init__(self, style = AnsiStyle.DEFAULT,
                 foreground  = AnsiColor.DEFAULT,
                 background  = AnsiColor.DEFAULT) -> None:
        self._style      = style
        self._foreground = foreground
        self._background = background
    
    @property
    def style(self) -> AnsiStyle:
        return self._style
    
    @style.setter
    def style(self, value):
        self._style = value
    
    @property
    def foreground(self) -> AnsiColor:
        return self._foreground
    
    @foreground.setter
    def foreground(self, value):
        self._foreground = value
    
    @property
    def background(self) -> AnsiColor:
        return self._background
    
    @background.setter
    def background(self, value):
        self._background = value
    
    @property
    def enable_ansi(self) -> str:
        ret = self.disable_ansi
        for style in self._style:
           ret += f'{AnsiFormat.CONTROL_CODE}{STYLE_DICT[style]}m'
        if self._foreground != AnsiColor.DEFAULT:
           ret += f'{AnsiFormat.CONTROL_CODE}3{self._foreground.value % 8}' + \
                  (';1' if (self._foreground.value & 8) > 0 else '') + 'm'
        if self._background != AnsiColor.DEFAULT:
           ret += f'{AnsiFormat.CONTROL_CODE}4{self._background.value % 8}' + \
                  (';1' if (self._background.value & 8) > 0 else '') + 'm'
        return ret
    
    @property
    def disable_ansi(self) -> str:
        return f'{AnsiFormat.CONTROL_CODE}0m'
    
    def copy(self) -> 'AnsiFormat':
        return AnsiFormat(self._style, self._foreground, self._background)
    
    def __eq__(self, value: object) -> bool:
        if  not isinstance(value, AnsiFormat):
            return False
        return self._style == value._style and \
               self._foreground == value._foreground and \
               self._background == value._background
    
    def __repr__(self) -> str:
        return f'AnsiFormat{{{self._style}, {self._foreground}, {self._background}}}'
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __hash__(self) -> int:
        hash((self._style, self._foreground, self._background))

DEFAULT_FORMAT = AnsiFormat()
ERROR_FORMAT   = AnsiFormat(foreground=AnsiColor.BRIGHT_RED)
PS_FORMAT      = AnsiFormat(foreground=AnsiColor.BLUE)

class AnsiStr:
    def __init__(self, text: str, format: AnsiFormat) -> None:
        self._text   = text
        self._format = format
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, value: str):
        self._text = value
    
    @property
    def format(self) -> AnsiFormat:
        return self._format
    
    @format.setter
    def format(self, value: AnsiFormat):
        self._format = value
    
    def copy(self) -> 'AnsiStr':
        return AnsiStr(self._text, self._format.copy())
    
    def append(self, text: str):
        self._text += text
    
    def __iter__(self):
        return iter(self._text)
    
    def __str__(self) -> str:
        return self._format.enable_ansi + self.text + self._format.disable_ansi
    
    def __repr__(self) -> str:
        return f'AnsiStr{{"{self._text}", {self._format}}}'
    
    def __len__(self) -> int:
        return self._text.__len__()
    
    def __getitem__(self, key) -> 'AnsiStr':
        if isinstance(key, slice):
            start, stop, step = key.start, key.stop, key.step
            return AnsiStr(self._text[start:stop:step], self._format)
        return AnsiStr(self._text[key], self._format)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AnsiStr):
            return False
        return self._format == value._format and self.text == value.text
    
    def __hash__(self) -> int:
        return hash((self._format, self._text))
    
    def __add__(self, other: Union[str, 'AnsiStr', 'AnsiStream']) -> 'AnsiStream':
        if isinstance(other, str):
            astr = AnsiStr(other, AnsiFormat())
            return AnsiStream([self, astr])
        if isinstance(other, AnsiStr):
            return AnsiStream([self, other])
        if isinstance(other, AnsiStream):
            ret = other.copy()
            ret._astrs.insert(0, self)
            return ret
        raise ValueError('Unsupported type.')
    
    def __radd__(self, other: Union[str, 'AnsiStr', 'AnsiStream']) -> 'AnsiStream':
        if isinstance(other, str):
            astr = AnsiStr(other, AnsiFormat())
            return AnsiStream([astr, self])
        if isinstance(other, AnsiStr):
            return AnsiStream([other, self])
        if isinstance(other, AnsiStream):
            ret = other.copy()
            ret._astrs.append(self)
            return ret
        raise ValueError('Unsupported type.')

class AnsiStream:
    @overload
    def __init__(self, strs: None) -> None:
        ...
    
    @overload
    def __init__(self, astr: AnsiStr) -> None:
        ...
    
    @overload
    def __init__(self, astrs: Iterable[AnsiStr]) -> None:
        ...
    
    @overload
    def __init__(self, stream: 'AnsiStream') -> None:
        ...
    
    def __init__(self, strs: Union[None, AnsiStr, Iterable[AnsiStr], 'AnsiStream'] = None) -> None:
        self._astrs: list[AnsiStr] = []
        if  isinstance(strs, AnsiStr):
            self._astrs.append(strs)
        elif isinstance(strs, AnsiStream):
            for astr in strs._astrs:
                self._astrs.append(astr.copy())
        elif isinstance(strs, Iterable):
            for astr in strs:
                if not isinstance(astr, AnsiStr):
                    raise ValueError('Unsupported type.')
                self._astrs.append(astr.copy())
    
    def copy(self) -> 'AnsiStream':
        ret = AnsiStream()
        for astr in self._astrs:
            ret._astrs.append(astr.copy())
        return ret
    
    def plain_text(self) -> str:
        return ''.join(astr.text for astr in self._astrs)
    
    def append(self, text: str):
        if len(self._astrs) > 0:
            self._astrs[-1].text += text
        else:
            self._astrs.append(AnsiStr(text, AnsiFormat()))
    
    def __str__(self) -> str:
        return ''.join(astr.__str__() for astr in self._astrs)
    
    def __repr__(self) -> str:
        return f'AnsiStream{{{", ".join(repr(astr) for astr in self._astrs)}}}'
    
    def __len__(self) -> int:
        return len(self.plain_text())
    
    def __iter__(self):
        return iter(self.plain_text())
    
    def __iadd__(self, other: Union[str, AnsiStr, 'AnsiStream']) -> 'AnsiStream':
        if isinstance(other, str):
            self._astrs.append(AnsiStr(other, AnsiFormat()))
        if isinstance(other, AnsiStr):
            self._astrs.append(other)
        if isinstance(other, AnsiStream):
            for astr in other._astrs:
                self._astrs.append(astr)
        return self
    
    def __add__(self, other: Union[str, AnsiStr, 'AnsiStream']) -> 'AnsiStream':
        ret = self.copy()
        if isinstance(other, str):
            ret._astrs.append(AnsiStr(other, AnsiFormat()))
            return ret
        if isinstance(other, AnsiStr):
            ret._astrs.append(other)
            return ret
        if isinstance(other, AnsiStream):
            for astr in other._astrs:
                ret._astrs.append(astr)
            return ret
        raise ValueError('Unsupported type.')
    
    def __radd__(self, other: Union[str, AnsiStr, 'AnsiStream']) -> 'AnsiStream':
        ret = self.copy()
        if isinstance(other, str):
            ret._astrs.insert(0, AnsiStr(other, AnsiFormat()))
            return ret
        if isinstance(other, AnsiStr):
            ret._astrs.insert(0, other)
            return ret
        if isinstance(other, AnsiStream):
            for astr in self._astrs:
                ret._astrs.append(astr)
            return ret
        raise ValueError('Unsupported type.')
    
    def __getitem__(self, key) -> 'AnsiStream':
        ret       = AnsiStream()
        intervals = []
        index     = 0
        plain_str = self.plain_text()
        full_len  = len(plain_str)
        for astr in self._astrs:
            intervals.append(index)
            index += len(astr)
        last_index = None
        
        if isinstance(key, slice):
            for i in list(range(full_len))[key]:
                index = bisect_right(intervals, i) - 1
                if index == last_index:
                    ret._astrs[-1]._text += plain_str[i]
                else:
                    ret._astrs.append(AnsiStr(plain_str[i], self._astrs[index]._format))
                    last_index = index
            return ret
        
        if not 0 <= key < full_len:
            raise IndexError('Index out of range.')
        index = bisect_right(intervals, i) - 1
        ret._astrs.append(AnsiStr(plain_str[i], self._astrs[index]._format))

strLike     = Union[str, AnsiStr]
strOrStream = Union[str, AnsiStr, AnsiStream]

FORMAT_VALUE   = AnsiFormat(foreground=AnsiColor.CYAN)
FORMAT_TITLE   = AnsiFormat(AnsiStyle.BOLD, AnsiColor.WHITE)
FORMAT_ERROR   = AnsiFormat(foreground=AnsiColor.RED)
FORMAT_SUCCESS = AnsiFormat(foreground=AnsiColor.GREEN)
FORMAT_PS      = AnsiFormat(style=AnsiStyle.FAINT)
FORMAT_OPTION  = AnsiFormat(foreground=AnsiColor.YELLOW)
FORMAT_ANNO    = AnsiFormat(AnsiStyle.ITALIC | AnsiStyle.FAINT)

__all__ = [
    "AnsiColor", "AnsiStyle", "AnsiFormat", "DEFAULT_FORMAT",
    "ERROR_FORMAT", "PS_FORMAT", "AnsiStr", "AnsiStream",
    "FORMAT_VALUE", "FORMAT_TITLE", "FORMAT_ERROR", "FORMAT_SUCCESS",
    "FORMAT_PS", "FORMAT_OPTION", "FORMAT_ANNO", "strLike", "strOrStream",
]
