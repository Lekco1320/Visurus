from enum import Enum

class horizonal_alignment(Enum):
    LEFT   = 0
    CENTER = 1
    RIGHT  = 2

class vertical_alignment(Enum):
    TOP    = 0
    CENTER = 1
    BOTTOM = 2

class anchor:
    def __init__(self, position: tuple[int, int], offset: tuple[int, int], halign = horizonal_alignment.LEFT, valign = vertical_alignment.TOP):        
        self._position = position
        self._offset   = offset
        self._halign   = halign
        self._valign   = valign

    @property
    def position(self):
        return self._position
    
    @property
    def hAilgn(self):
        return self._halign
    
    @property
    def vAlign(self):
        return self._valign
    
    def real_position(self, size: tuple[int, int]) -> tuple[int, int]:
        width, height = size
        x, y = self._position
        if   self._halign == horizonal_alignment.RIGHT:
            x -= width
        elif self._halign == horizonal_alignment.CENTER:
            x -= width / 2
        if   self._valign == vertical_alignment.BOTTOM:
            y -= height
        elif self._valign == vertical_alignment.CENTER:
            y -= height / 2
        x += self._offset[0]
        y += self._offset[1]
        return (int(x), int(y))
