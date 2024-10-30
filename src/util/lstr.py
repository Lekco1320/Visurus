from typing import Any

class lstr:
    def __init__(self, text: str = '') -> None:
        self._textlist = []
        self._raw      = text
        self._id       = 0
        self.raw       = ''
        self._split(text)
    
    @property
    def text(self):
        return self._raw
    
    def _split(self, text: str):
        left = []
        if len(text) == 0:
            return
        self._textlist.append((text[0], None))

        for i in range(1, len(text)):
            c = text[i]
            self._textlist.append((c, None))
            if c == '(':
                left.append((i, len(self._textlist) - 1))
            if c == ')' and len(left) > 0:
                self._textlist[left[-1][1] - 1] = (text[left[-1][0] - 1], text[(left[-1][0] + 1):i])
                del self._textlist[left[-1][1]:]
                del left[-1]
        
        for pair in self._textlist:
            self.raw += pair[0]
    
    def __len__(self) -> int:
        return len(self._textlist)
    
    def __iter__(self) -> 'lstr':
        self._id = 0
        return self
    
    def __next__(self) -> tuple[str, Any]:
        if self._id >= len(self._textlist):
            raise StopIteration
        self._id += 1
        return self._textlist[self._id - 1]
    
    def __str__(self) -> str:
        return self._raw
