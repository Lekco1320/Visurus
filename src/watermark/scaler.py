from abc import ABC
from abc import abstractmethod
from enum import Enum

class scaler(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @property
    @abstractmethod
    def width(self):
        pass
    
    @property
    @abstractmethod
    def height(self):
        pass
    
    @property
    @abstractmethod
    def size(self):
        pass

class fixed_scaler(scaler):
    def __init__(self, width: int | str, height: int | str) -> None:
        super().__init__()
        
        self._width  = width if width != '*' else None
        self._height = height if height != '*' else None
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def size(self):
        return (self._width, self._height)

class scale_ref(Enum):
    WIDTH  = 0
    HEIGHT = 1

class proportion_scaler(scaler):
    def __init__(self, scale_ref: scale_ref, proportion: float, ref: tuple[int, int]) -> None:
        super().__init__()
        
        if proportion <= 0:
            raise ValueError(f'Invalid proportion value \'{proportion}\'.')
        
        self._proportion = proportion
        self._scale_ref  = scale_ref
        self._ref        = ref
    
    def _check(self):
        if not isinstance(self._ref, tuple):
            raise TypeError(f'Unsupported scale reference type \'{type(self._ref).__name__}\'.')
        if self._ref[0] < 0 or self._ref[1] < 0:
            raise ValueError(f'Invalid size value \'{self._ref}\'.')
    
    def _calculate(self) -> tuple[int, int]:
        self._check()
        if self._scale_ref == scale_ref.WIDTH:
            return (int(self._ref[0] * self._proportion), None)
        if self._scale_ref == scale_ref.HEIGHT:
            return (None, int(self._ref[1] * self._proportion))
    
    @property
    def reference(self):
        return self._ref
    
    @property
    def width(self):
        return self._calculate()[0]
    
    @property
    def height(self):
        return self._calculate()[1]
    
    @property
    def size(self):
        return self._calculate()
    
    @property
    def proportion(self):
        return self._proportion
    
    @property
    def scale_ref(self):
        return self._scale_ref
    
    @scale_ref.setter
    def scale_ref(self, value):
        self._ref = value
