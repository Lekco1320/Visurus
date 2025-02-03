import util
import watermark

from . import shadow
from . import round_corner

from app import input
from PIL import Image

class Style(util.Config):
    FIELDS = [
        util.Field('shadow',    False),
        util.Field('sstyle',    shadow.Style.DEFAULT),
        util.Field('round',     False),
        util.Field('rstyle',    round_corner.Style.DEFAULT),
        util.Field('watermark', False),
        util.Field('wstyle',    watermark.Style.DEFAULT),
    ]
    
    def __init__(self, fname: str) -> None:
        super().__init__(fname)
        self._fields = Style.FIELDS.copy()
        self._fields.append(util.Field('order', ('阴影', '圆角', '水印', self.name), self.order_validate))
        self.validate(self._fields)
    
    def order_validate(self, value: list[str]) -> bool:
        return not \
            (len(value) == 4 and \
            '阴影' in value and \
            '圆角' in value and \
            '水印' in value and \
            self.name in value)
    
    def self_validate(self) -> bool:
        return super().validate(self._fields)
    
    def set(self):
        main(self)
    
    def process(self, pfunc, img: Image.Image) -> Image.Image:
        for o in self.order:
            if self.shadow and o == '阴影':
                img = shadow.process(self.sstyle, img)
            if self.round and o == '圆角':
                img = round_corner.process(self.rstyle, img)
            if self.watermark and o == '水印':
                img = watermark.process(self.wstyle, img)
            if o == self.name:
                img = pfunc(img)
        return img

def main(style: Style):
    m = util.Menu('Lekco Visurus - 效果与水印', 'Q')
    m.add(util.Option('H', '图像阴影',  lambda: h_main(style), lambda: h_value(style)))
    m.add(util.Option('A', '阴影效果…', style.sstyle.set, enfunc=lambda: style.shadow))
    m.add(util.Option('R', '图像圆角',  lambda: r_main(style), lambda: r_value(style)))
    m.add(util.Option('D', '圆角参数',  style.rstyle.set, enfunc=lambda: style.round))
    m.add(util.Option('W', '图像水印',  lambda: w_main(style), lambda: w_value(style)))
    m.add(util.Option('T', '水印样式…', style.wstyle.set, enfunc=lambda: style.watermark))
    m.add(util.Option('E', '效果顺序',  lambda: set_order(style), lambda: get_order(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

#region 图像阴影

def h_main(style: Style):
    m = util.Menu('Lekco Visurus - 图像阴影')
    m.add(util.Option('E', '启用', lambda: h_enable(style)))
    m.add(util.Option('D', '关闭', lambda: h_disable(style)))
    m.run()

def h_enable(style: Style):
    style.shadow = True

def h_disable(style: Style):
    style.shadow = False

def h_value(style: Style) -> str:
    return '启用' if style.shadow else '关闭'

#endregion

#region 图像圆角

def r_main(style: Style):
    m = util.Menu('Lekco Visurus - 图像圆角')
    m.add(util.Option('E', '启用', lambda: r_enable(style)))
    m.add(util.Option('D', '关闭', lambda: r_disable(style)))
    m.run()

def r_enable(style: Style):
    style.round = True

def r_disable(style: Style):
    style.round = False

def r_value(style: Style) -> str:
    return '启用' if style.round else '关闭'

#endregion

#region 图像水印

def w_main(style: Style):
    m = util.Menu('Lekco Visurus - 图像水印')
    m.add(util.Option('E', '启用', lambda: w_enable(style)))
    m.add(util.Option('D', '关闭', lambda: w_disable(style)))
    m.run()

def w_enable(style: Style):
    style.watermark = True

def w_disable(style: Style):
    style.watermark = False

def w_value(style: Style) -> str:
    return '启用' if style.watermark else '关闭'

#endregion

#region 效果顺序

@util.errhandler
def set_order(style: Style):
    util.print_output('请输入效果顺序:')
    util.print_ps(f'例: 阴影 圆角 水印 {style.name}')
    style.order = input.input_valid_sequence(['阴影', '圆角', '水印', style.name])

def get_order(style: Style) -> str:
    return '→'.join(style.order)

#endregion
