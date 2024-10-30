from util import *

class color:
    def __init__(self, value: tuple | str) -> None:
        self._r, self._g, self._b, self._a = color.check(value)
    
    @staticmethod
    def check(value: tuple | str) -> tuple[int, int, int, int]:
        r, g, b, a = 255, 255, 255, 255
        if  isinstance(value, tuple):
            r = color._check_channel(value[0])
            g = color._check_channel(value[1])
            b = color._check_channel(value[2])
            a = color._check_channel(value[3]) if len(value) > 3 else 255
        elif isinstance(value, str):
            if value.startswith('#'):
                value = value[1:]
            r = color._check_channel(value[0:2])
            g = color._check_channel(value[2:4])
            b = color._check_channel(value[4:6])
            a = color._check_channel(value[6:8]) if len(value) > 7 else 255
        return (r, g, b, a)
    
    @staticmethod
    def _check_channel(channel) -> int:
        i = channel if isinstance(channel, int) else int(channel, 16)
        if i < 0 or i > 255:
            raise ValueError(f'非法颜色通道值 \'{channel}\'')
        return i
    
    @property
    def hex(self) -> str:
        return f'#{self._r:02x}{self._g:02x}{self._b:02x}{self._a:02x}'
    
    @property
    def channels(self) -> str:
        return self.tuple.__str__()
    
    @property
    def tuple(self) -> str:
        return (self._r, self._g, self._b, self._a)
    
    def __str__(self) -> str:
        return self.hex
    
    @staticmethod
    @errhandler
    def input() -> 'color':
        print_output('请任选一种格式输入颜色值:')
        print_ps('分量表示: R,G,B')
        print_ps('十六进制表示: #??????')
        ans = get_input()
        c   = None
        if ans.startswith('#'):
            c = ans
        else:
            c = tuple(map(int, ans.split(',')))
        c = color(c)
        print_output('请任选一种格式输入不透明度:')
        print_ps('百分比表示: ??%')
        print_ps('十进制表示: 0~255')
        print_ps('十六进制表示: #??')
        ans = get_input()
        if   ans.endswith('%'):
            opc = int(ans[:-1]) / 100 * 255
        elif ans.startswith('#'):
            opc = int(ans[1:], 16)
        else:
            opc = int(ans)
        if opc < 0 or opc > 255:
            raise ValueError(f'非法不透明度值 \'{opc}%\'.')
        c._a = int(opc)
        return c
