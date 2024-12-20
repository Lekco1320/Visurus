from .printer    import *
from .decorators import *

from typing import overload

class Color:
    @overload
    def __init__(self, value: tuple) -> None:
        """value: (R, G, B, A)"""
        ...
    
    @overload
    def __init__(self, value: str) -> None:
        """value: '#RRGGBBAA'"""
        ...
    
    def __init__(self, value: tuple | str) -> None:
        self._r, self._g, self._b, self._a = Color.check(value)
    
    @staticmethod
    def check(value: tuple | str) -> tuple[int, int, int, int]:
        r, g, b, a = 255, 255, 255, 255
        if  isinstance(value, tuple):
            r = Color._check_channel(value[0])
            g = Color._check_channel(value[1])
            b = Color._check_channel(value[2])
            a = Color._check_channel(value[3]) if len(value) > 3 else 255
        elif isinstance(value, str):
            if value.startswith('#'):
                value = value[1:]
            r = Color._check_channel(value[0:2])
            g = Color._check_channel(value[2:4])
            b = Color._check_channel(value[4:6])
            a = Color._check_channel(value[6:8]) if len(value) > 7 else 255
        return (r, g, b, a)
    
    @staticmethod
    def _check_channel(channel) -> int:
        i = channel if isinstance(channel, int) else int(channel, 16)
        if i < 0 or i > 255:
            raise ValueError(f'非法颜色通道值 \'{channel}\'')
        return i
    
    @property
    def hex(self) -> str:
        return f'#{self._r:02x}{self._g:02x}{self._b:02x}{self._a:02x}'.upper()
    
    @property
    def channels(self) -> str:
        return self.tuple.__str__()
    
    @property
    def tuple(self) -> str:
        return (self._r, self._g, self._b, self._a)
    
    def __str__(self) -> str:
        return self.hex

__all__ = ["Color"]
