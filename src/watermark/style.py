import os
import resources

from util import *
from util import config
from util import menu

#region 变量

class style(config.config):
    FIELDS = [
        config.field('content',  '文字'),
        config.field('font',     resources.font.TIMES_REGULAR),
        config.field('color',    color('#0000007F')),
        config.field('text',     'Lekco'),
        config.field('psource',  '无'),
        config.field('opacity',  100),
        config.field('aligns',   ['居中对齐', '底部对齐']),
        config.field('scale',    ['固定尺寸', ('*', 20)]),
        config.field('position', '图像下中央'),
        config.field('offset',   (0, 0))
    ]
    
    DEFAULT = None
    
    @staticmethod
    def default() -> 'style':
        ret = style()
        ret.validate(style.FIELDS)
        return ret
    
    def __init__(self) -> None:
        super().__init__('')
        self.validate(style.FIELDS)
    
    def self_validate(self) -> bool:
        return super().validate(style.FIELDS)
    
    def set(self):
        main(self)

style.DEFAULT = style.default()

#endregion

# 主函数

def main(style: style):
    m = menu.menu('Lekco Visurus - 水印样式', 'Q')
    m.add(menu.option('W', '水印内容', lambda: w_main(style),      lambda: w_value(style)))
    m.add(menu.option('F', '水印字体', lambda: f_main(style),      lambda: f_value(style),     lambda: style.content == '文字'))
    m.add(menu.option('C', '文字颜色', lambda: set_color(style),   lambda: get_color(style),   lambda: style.content == '文字'))
    m.add(menu.option('T', '文字内容', lambda: set_text(style),    lambda: get_text(style),    lambda: style.content == '文字'))
    m.add(menu.option('S', '图片源',   lambda: set_psource(style), lambda: get_psource(style), lambda: style.content == '图片'))
    m.add(menu.option('O', '不透明度', lambda: set_opacity(style), lambda: get_opacity(style), lambda: style.content == '图片'))
    m.add(menu.option('A', '对齐方式', lambda: a_main(style),      lambda: a_value(style)))
    m.add(menu.option('Z', '缩放方式', lambda: z_main(style),      lambda: z_value(style)))
    m.add(menu.option('P', '水印位置', lambda: p_main(style),      lambda: p_value(style)))
    m.add(menu.option('E', '位置偏移', lambda: set_offset(style),  lambda: get_offset(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

#region 水印内容

def w_main(style: style):
    m = menu.menu('Lekco Visurus - 水印内容')
    m.add(menu.option('T', '文字', lambda: w_text(style)))
    m.add(menu.option('P', '图片', lambda: w_picture(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def w_text(style: style):
    style.content = '文字'

def w_picture(style: style):
    style.content = '图片'

def w_value(style: style) -> str:
    return style.content

#endregion

#region 水印字体

@errhandler
def f_main(style: style):
    style.font = resources.font_main(style.font)

def f_value(style: style) -> str:
    return fomit_path('* F | 水印字体: {} *', style.font.__str__())

#endregion

#region 文字颜色

@errhandler
def set_color(style: style):
    style.color = color.input()

def get_color(style: style) -> str:
    return style.color.hex

#endregion

#region 文字内容

def set_text(style: style):
    print_output('请输入水印内容:')
    style.text = get_input()

def get_text(style: style) -> str:
    return fomit_str('* T | 水印内容: {} *', style.text)

#endregion

#region 图片源

@errhandler
def set_psource(style: style):
    print_output('请输入图片源路径:')
    ans = get_input()
    if not os.path.exists(ans):
        raise ValueError(f'无效的图片路径 \'{ans}\'.')
    style.psource = ans

def get_psource(style: style) -> str:
    return fomit_path('* S | 图片源: {} *', style.psource)

#endregion

#region 不透明度

@errhandler
def set_opacity(style: style):
    print_output('请输入不透明度(%):')
    opc = float(get_input())
    if opc < 0 or opc > 100:
        raise ValueError(f'无效不透明度值 \'{opc}%\'.')
    style.opacity = opc

def get_opacity(style: style) -> str:
    return f'{style.opacity}%'

#endregion

#region 对齐方式

def a_main(style: style):
    m = menu.menu('Lekco Visurus - 对齐方式', 'Q')
    m.add(menu.option('H', '水平对齐', lambda: a_set_hailgn(style), lambda: a_get_halign(style)))
    m.add(menu.option('V', '垂直对齐', lambda: a_set_vailgn(style), lambda: a_get_valign(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def a_set_hailgn(style: style):
    m = menu.menu('Lekco Visurus - 水平对齐')
    m.add(menu.option('L', '左对齐',   lambda: a_set_hleft(style)))
    m.add(menu.option('C', '居中对齐', lambda: a_set_hcenter(style)))
    m.add(menu.option('R', '右对齐',   lambda: a_set_hright(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def a_set_hleft(style: style):
    style.aligns[0] = '左对齐'

def a_set_hcenter(style: style):
    style.aligns[0] = '居中对齐'

def a_set_hright(style: style):
    style.aligns[0] = '右对齐'

def a_get_halign(style: style) -> str:
    return style.aligns[0]

def a_set_vailgn(style: style):
    m = menu.menu('Lekco Visurus - 垂直对齐')
    m.add(menu.option('T', '顶部对齐', lambda: a_set_vtop(style)))
    m.add(menu.option('C', '居中对齐', lambda: a_set_vcenter(style)))
    m.add(menu.option('B', '底部对齐', lambda: a_set_vbottom(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def a_set_vtop(style: style):
    style.aligns[1] = '顶部对齐'

def a_set_vcenter(style: style):
    style.aligns[1] = '居中对齐'

def a_set_vbottom(style: style):
    style.aligns[1] = '底部对齐'

def a_get_valign(style: style) -> str:
    return style.aligns[1]

def a_value(style: style) -> str:
    return f'{style.aligns[0]}, {style.aligns[1]}'

#endregion

#region 缩放方式

def z_main(style: style):
    m = menu.menu('Lekco Visurus - 缩放方式', 'Q')
    m.add(menu.option('M', '缩放模式', lambda: z_set_mode(style), lambda: style.scale[0]))
    m.add(menu.option('S', '尺寸大小', lambda: z_set_size(style), lambda: z_get_size(style),            lambda: style.scale[0] == '固定尺寸'))
    m.add(menu.option('A', '缩放参考', lambda: z_set_ref(style),  lambda: style.scale[1],               lambda: style.scale[0] == '比例缩放'))
    m.add(menu.option('P', '缩放比例', lambda: z_set_proportion(style), lambda: z_get_propotion(style), lambda: style.scale[0] == '比例缩放'))
    m.add(menu.option('Q', '返回'))
    m.run()

def z_set_mode(style: style):
    m = menu.menu('Lekco Visurus - 缩放模式')
    m.add(menu.option('F', '固定尺寸', lambda: z_fixed_scale_mode(style)))
    m.add(menu.option('S', '比例缩放', lambda: z_proportion_scale_mode(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def z_fixed_scale_mode(style: style):
    if style.scale[0] == '固定尺寸':
        return
    style.scale = ['固定尺寸', ('*', '*')]
    if style.content == '文字':
        style.scale[1] = ('*', 15)

def z_proportion_scale_mode(style: style):
    if style.scale[1] == '比例缩放':
        return
    style.scale = ['比例缩放', '宽', 0.1]

@errhandler
def z_set_size(style: style):
    print_output('请输入尺寸大小 w,h:')
    print_ps('输入\'*\'自适应大小')
    ans = list(map(str, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的尺寸 \'{ans}\'.')
    for i in range(2):
        if ans[i].strip() == '*':
            ans[i] = '*'
        else:
            ans[i] = int(ans[i])
    if ans == ('*', '*') and style.content == '文字':
        raise ValueError('文字水印的尺寸大小不得为长宽自适应.')
    style.scale[1] = ans

def z_get_size(style: style) -> str:
    size = style.scale[1]
    return f'{size[0]}x{size[1]}'

def z_set_ref(style: style):
    m = menu.menu('Lekco Visurus - 缩放参考')
    m.add(menu.option('W', '宽', lambda: z_width_ref(style)))
    m.add(menu.option('H', '高', lambda: z_height_ref(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def z_width_ref(style: style):
    style.scale[1] = '宽'

def z_height_ref(style: style):
    style.scale[1] = '高'

@errhandler
def z_set_proportion(style: style):
    print_output('请输入缩放比例(%):')
    p = float(get_input())
    if p <= 0:
        raise ValueError(f'非法缩放比例 \'{p}%\'.')
    style.scale[2] = p / 100

def z_get_propotion(style: style) -> str:
    return f'{style.scale[2] * 100}%'

def z_value(style: style) -> str:
    if style.scale[0] == '固定尺寸':
        return f'{style.scale[0]} @{style.scale[1][0]}x{style.scale[1][1]}'
    else:
        return f'{style.scale[0]} @{style.scale[1]}x{style.scale[2] * 100}%'

#endregion

#region 水印位置

def p_main(style: style):
    m = menu.menu('Lekco Visurus - 水印位置')
    m.add(menu.option('1', '图像左上角', lambda: p_1(style)))
    m.add(menu.option('2', '图像上中央', lambda: p_2(style)))
    m.add(menu.option('3', '图像右上角', lambda: p_3(style)))
    m.add(menu.option('4', '图像正左侧', lambda: p_4(style)))
    m.add(menu.option('5', '图像正中央', lambda: p_5(style)))
    m.add(menu.option('6', '图像正右侧', lambda: p_6(style)))
    m.add(menu.option('7', '图像左下角', lambda: p_7(style)))
    m.add(menu.option('8', '图像下中央', lambda: p_8(style)))
    m.add(menu.option('9', '图像右下角', lambda: p_9(style)))
    m.add(menu.option('X', '指定位置',   lambda: p_pose(style)))
    m.add(menu.option('R', '随机位置',   lambda: p_random(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def p_1(style: style):
    style.position = '图像左上角'

def p_2(style: style):
    style.position = '图像上中央'

def p_3(style: style):
    style.position = '图像右上角'

def p_4(style: style):
    style.position = '图像正左侧'

def p_5(style: style):
    style.position = '图像正中央'

def p_6(style: style):
    style.position = '图像正右侧'

def p_7(style: style):
    style.position = '图像左下角'

def p_8(style: style):
    style.position = '图像下中央'

def p_9(style: style):
    style.position = '图像右下角'

@errhandler
def p_pose(style: style):
    print_output('请输入水印位置 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    for i in ans:
        if i < 0:
            raise ValueError(f'非法的坐标 \'{ans[0]}, {ans[1]}\'.')
    style.position = (ans[0], ans[1])

def p_random(style: style):
    style.position = '随机'

def p_value(style: style) -> str:
    return style.position.__str__()

#endregion

#region 位置偏移

@errhandler
def set_offset(style: style):
    print_output('请输入位置偏移 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    style.offset = (ans[0], ans[1])

def get_offset(style: style) -> str:
    return style.offset.__str__()

#endregion
