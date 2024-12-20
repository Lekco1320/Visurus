import util
import os

from app import input
from app import resources

#region 变量

class Style(util.Config):
    FIELDS = [
        util.Field('content',  '文字'),
        util.Field('font',     resources.Font.TIMES_REGULAR),
        util.Field('color',    util.Color('#0000007F')),
        util.Field('text',     'Lekco'),
        util.Field('psource',  '无'),
        util.Field('opacity',  100),
        util.Field('aligns',   ['居中对齐', '底部对齐']),
        util.Field('scale',    ['固定尺寸', ('*', 20)]),
        util.Field('position', '图像下中央'),
        util.Field('offset',   (0, 0))
    ]
    
    DEFAULT = None
    
    @staticmethod
    def default() -> 'Style':
        ret = Style()
        ret.validate(Style.FIELDS)
        return ret
    
    def __init__(self) -> None:
        super().__init__('')
        self.validate(Style.FIELDS)
    
    def self_validate(self) -> bool:
        return super().validate(Style.FIELDS)
    
    def set(self):
        main(self)

Style.DEFAULT = Style.default()

#endregion

# 主函数

def main(style: Style):
    m = util.Menu('Lekco Visurus - 水印样式', 'Q')
    m.add(util.Option('W', '水印内容', lambda: w_main(style),      lambda: w_value(style)))
    m.add(util.Option('F', '水印字体', lambda: f_main(style),      lambda: f_value(style),     lambda: style.content == '文字'))
    m.add(util.Option('C', '文字颜色', lambda: set_color(style),   lambda: get_color(style),   lambda: style.content == '文字'))
    m.add(util.Option('T', '文字内容', lambda: set_text(style),    lambda: get_text(style),    lambda: style.content == '文字'))
    m.add(util.Option('S', '图片源',   lambda: set_psource(style), lambda: get_psource(style), lambda: style.content == '图片'))
    m.add(util.Option('O', '不透明度', lambda: set_opacity(style), lambda: get_opacity(style), lambda: style.content == '图片'))
    m.add(util.Option('A', '对齐方式', lambda: a_main(style),      lambda: a_value(style)))
    m.add(util.Option('Z', '缩放方式', lambda: z_main(style),      lambda: z_value(style)))
    m.add(util.Option('P', '水印位置', lambda: p_main(style),      lambda: p_value(style)))
    m.add(util.Option('E', '位置偏移', lambda: set_offset(style),  lambda: get_offset(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

#region 水印内容

def w_main(style: Style):
    m = util.Menu('Lekco Visurus - 水印内容')
    m.add(util.Option('T', '文字', lambda: w_text(style)))
    m.add(util.Option('P', '图片', lambda: w_picture(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def w_text(style: Style):
    style.content = '文字'

def w_picture(style: Style):
    style.content = '图片'

def w_value(style: Style) -> str:
    return style.content

#endregion

#region 水印字体

@util.errhandler
def f_main(style: Style):
    style.font = resources.font_main(style.font)

def f_value(style: Style) -> str:
    return util.fomit_path('* F | 水印字体: {} *', resources.font_name(style.font))

#endregion

#region 文字颜色

@util.errhandler
def set_color(style: Style):
    style.color = input.input_color()

def get_color(style: Style) -> str:
    return style.color.hex

#endregion

#region 文字内容

def set_text(style: Style):
    util.print_output('请输入水印内容:')
    style.text = util.get_input()

def get_text(style: Style) -> str:
    return util.fomit_str('* T | 水印内容: {} *', style.text)

#endregion

#region 图片源

@util.errhandler
def set_psource(style: Style):
    util.print_output('请输入图片源路径:')
    ans = util.get_input()
    if not os.path.exists(ans):
        raise ValueError(f'无效的图片路径 \'{ans}\'.')
    style.psource = ans

def get_psource(style: Style) -> str:
    return util.fomit_path('* S | 图片源: {} *', style.psource)

#endregion

#region 不透明度

@util.errhandler
def set_opacity(style: Style):
    util.print_output('请输入不透明度(%):')
    style.opacity = input.input_float(lLimit=[0, True], uLimit=[100, True])

def get_opacity(style: Style) -> str:
    return f'{style.opacity}%'

#endregion

#region 对齐方式

def a_main(style: Style):
    m = util.Menu('Lekco Visurus - 对齐方式', 'Q')
    m.add(util.Option('H', '水平对齐', lambda: a_set_hailgn(style), lambda: a_get_halign(style)))
    m.add(util.Option('V', '垂直对齐', lambda: a_set_vailgn(style), lambda: a_get_valign(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def a_set_hailgn(style: Style):
    m = util.Menu('Lekco Visurus - 水平对齐')
    m.add(util.Option('L', '左对齐',   lambda: a_set_hleft(style)))
    m.add(util.Option('C', '居中对齐', lambda: a_set_hcenter(style)))
    m.add(util.Option('R', '右对齐',   lambda: a_set_hright(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def a_set_hleft(style: Style):
    style.aligns[0] = '左对齐'

def a_set_hcenter(style: Style):
    style.aligns[0] = '居中对齐'

def a_set_hright(style: Style):
    style.aligns[0] = '右对齐'

def a_get_halign(style: Style) -> str:
    return style.aligns[0]

def a_set_vailgn(style: Style):
    m = util.Menu('Lekco Visurus - 垂直对齐')
    m.add(util.Option('T', '顶部对齐', lambda: a_set_vtop(style)))
    m.add(util.Option('C', '居中对齐', lambda: a_set_vcenter(style)))
    m.add(util.Option('B', '底部对齐', lambda: a_set_vbottom(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def a_set_vtop(style: Style):
    style.aligns[1] = '顶部对齐'

def a_set_vcenter(style: Style):
    style.aligns[1] = '居中对齐'

def a_set_vbottom(style: Style):
    style.aligns[1] = '底部对齐'

def a_get_valign(style: Style) -> str:
    return style.aligns[1]

def a_value(style: Style) -> str:
    return f'{style.aligns[0]}, {style.aligns[1]}'

#endregion

#region 缩放方式

def z_main(style: Style):
    m = util.Menu('Lekco Visurus - 缩放方式', 'Q')
    m.add(util.Option('M', '缩放模式', lambda: z_set_mode(style), lambda: style.scale[0]))
    m.add(util.Option('S', '尺寸大小', lambda: z_set_size(style), lambda: z_get_size(style),            lambda: style.scale[0] == '固定尺寸'))
    m.add(util.Option('A', '缩放参考', lambda: z_set_ref(style),  lambda: style.scale[1],               lambda: style.scale[0] == '比例缩放'))
    m.add(util.Option('P', '缩放比例', lambda: z_set_proportion(style), lambda: z_get_propotion(style), lambda: style.scale[0] == '比例缩放'))
    m.add(util.Option('Q', '返回'))
    m.run()

def z_set_mode(style: Style):
    m = util.Menu('Lekco Visurus - 缩放模式')
    m.add(util.Option('F', '固定尺寸', lambda: z_fixed_scale_mode(style)))
    m.add(util.Option('S', '比例缩放', lambda: z_proportion_scale_mode(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def z_fixed_scale_mode(style: Style):
    if style.scale[0] == '固定尺寸':
        return
    style.scale = ['固定尺寸', ('*', '*')]
    if style.content == '文字':
        style.scale[1] = ('*', 15)

def z_proportion_scale_mode(style: Style):
    if style.scale[1] == '比例缩放':
        return
    style.scale = ['比例缩放', '宽', 0.1]

@util.errhandler
def z_set_size(style: Style):
    util.print_output('请输入尺寸大小 w,h:')
    util.print_ps('输入\'*\'自适应大小')
    ans = input.input_size(xRange=[input.Operator.GREATER, 0], \
                           yRange=[input.Operator.GREATER, 0])
    if ans == ('*', '*') and style.content == '文字':
        raise ValueError('文字水印的尺寸大小不得为长宽自适应.')
    style.scale[1] = ans

def z_get_size(style: Style) -> str:
    size = style.scale[1]
    return f'{size[0]}x{size[1]}'

def z_set_ref(style: Style):
    m = util.Menu('Lekco Visurus - 缩放参考')
    m.add(util.Option('W', '宽', lambda: z_width_ref(style)))
    m.add(util.Option('H', '高', lambda: z_height_ref(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def z_width_ref(style: Style):
    style.scale[1] = '宽'

def z_height_ref(style: Style):
    style.scale[1] = '高'

@util.errhandler
def z_set_proportion(style: Style):
    util.print_output('请输入缩放比例(%):')
    style.scale[2] = input.input_float(lLimit=[0, False]) / 100

def z_get_propotion(style: Style) -> str:
    return f'{style.scale[2] * 100}%'

def z_value(style: Style) -> str:
    if style.scale[0] == '固定尺寸':
        return f'{style.scale[0]} @{style.scale[1][0]}x{style.scale[1][1]}'
    else:
        return f'{style.scale[0]} @{style.scale[1]}x{style.scale[2] * 100}%'

#endregion

#region 水印位置

def p_main(style: Style):
    m = util.Menu('Lekco Visurus - 水印位置')
    m.add(util.Option('1', '图像左上角', lambda: p_1(style)))
    m.add(util.Option('2', '图像上中央', lambda: p_2(style)))
    m.add(util.Option('3', '图像右上角', lambda: p_3(style)))
    m.add(util.Option('4', '图像正左侧', lambda: p_4(style)))
    m.add(util.Option('5', '图像正中央', lambda: p_5(style)))
    m.add(util.Option('6', '图像正右侧', lambda: p_6(style)))
    m.add(util.Option('7', '图像左下角', lambda: p_7(style)))
    m.add(util.Option('8', '图像下中央', lambda: p_8(style)))
    m.add(util.Option('9', '图像右下角', lambda: p_9(style)))
    m.add(util.Option('X', '指定位置',   lambda: p_pose(style)))
    m.add(util.Option('R', '随机位置',   lambda: p_random(style)))
    m.add(util.Option('Q', '返回'))
    m.run()

def p_1(style: Style):
    style.position = '图像左上角'

def p_2(style: Style):
    style.position = '图像上中央'

def p_3(style: Style):
    style.position = '图像右上角'

def p_4(style: Style):
    style.position = '图像正左侧'

def p_5(style: Style):
    style.position = '图像正中央'

def p_6(style: Style):
    style.position = '图像正右侧'

def p_7(style: Style):
    style.position = '图像左下角'

def p_8(style: Style):
    style.position = '图像下中央'

def p_9(style: Style):
    style.position = '图像右下角'

@util.errhandler
def p_pose(style: Style):
    util.print_output('请输入水印位置 x,y:')
    style.position = input.input_int_coordinate(xRange=[input.Operator.GREATER_EQ, 0], \
                                                yRange=[input.Operator.GREATER_EQ, 0])

def p_random(style: Style):
    style.position = '随机'

def p_value(style: Style) -> str:
    return style.position.__str__()

#endregion

#region 位置偏移

@util.errhandler
def set_offset(style: Style):
    util.print_output('请输入位置偏移 x,y:')
    style.offset = input.input_int_coordinate()

def get_offset(style: Style) -> str:
    return style.offset.__str__()

#endregion
