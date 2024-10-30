import os

from util import *
from util import menu

from config import Config

#region 变量

content  = wrapper(Config['watermark.content'])
font     = wrapper(Config['watermark.font'])
fcolor   = wrapper(Config['watermark.color'])
ftext    = wrapper(Config['watermark.text'])
psource  = wrapper(Config['watermark.psource'])
opacity  = wrapper(Config['watermark.opacity'])
aligns   = wrapper(Config['watermark.aligns'])
scale    = wrapper(Config['watermark.scale'])
position = wrapper(Config['watermark.position'])
offset   = wrapper(Config['watermark.offset'])

#endregion

# 主函数
def main():
    m = menu.menu('Lekco Visurus - 水印样式', 'Q')
    m.add(menu.option('W', '水印内容', lambda: w_main(content),      lambda: w_value(content)))
    m.add(menu.option('F', '水印字体', lambda: f_main(font),         lambda: f_value(font),        lambda: content.data == '文字'))
    m.add(menu.option('C', '文字颜色', lambda: set_color(fcolor),    lambda: get_color(fcolor),    lambda: content.data == '文字'))
    m.add(menu.option('T', '文字内容', lambda: set_text(ftext),      lambda: get_text(ftext),      lambda: content.data == '文字'))
    m.add(menu.option('S', '图片源',   lambda: set_psource(psource), lambda: get_psource(psource), lambda: content.data == '图片'))
    m.add(menu.option('O', '不透明度', lambda: set_opacity(opacity), lambda: get_opacity(opacity), lambda: content.data == '图片'))
    m.add(menu.option('A', '对齐方式', lambda: a_main(aligns),       lambda: a_value(aligns)))
    m.add(menu.option('Z', '缩放方式', lambda: z_main(scale),        lambda: z_value(scale)))
    m.add(menu.option('P', '水印位置', lambda: p_main(position),     lambda: p_value(position)))
    m.add(menu.option('E', '位置偏移', lambda: set_offset(offset),   lambda: get_offset(offset)))
    m.add(menu.option('Q', '返回'))
    m.run()

#region 水印内容

def w_main(content: wrapper):
    m = menu.menu('Lekco Visurus - 水印内容')
    m.add(menu.option('T', '文字', lambda: w_text(content)))
    m.add(menu.option('P', '图片', lambda: w_picture(content)))
    m.add(menu.option('Q', '返回'))
    m.run()

def w_text(content: wrapper):
    content.data = '文字'

def w_picture(content: wrapper):
    content.data = '图片'

def w_value(content: wrapper) -> str:
    return content.data

#endregion

#region 水印字体

@errhandler
def f_main(font: wrapper):
    print_output('请输入字体名:')
    f = get_input()
    font.data = f

def f_value(font: wrapper) -> str:
    return font.data.__str__()

#endregion

#region 文字颜色

@errhandler
def set_color(color: wrapper):
    print_output('请输入颜色值 R,G,B :')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 3:
        raise ValueError(f'错误的颜色分量通道数 \'{len(ans)}\'.')
    for i in ans:
        if i < 0 or i > 255:
            raise ValueError(f'无效颜色分量值 \'{i}\'.')
    print_output('请输入不透明度(%):')
    opc = float(get_input())
    if opc < 0 or opc > 100:
        raise ValueError(f'无效不透明度值 \'{opc}%\'.')
    color.data = (ans[0], ans[1], ans[2], int(opc * 255 / 100))

def get_color(color: wrapper) -> str:
    return color.data.__str__()

#endregion

#region 文字内容

def set_text(text: wrapper):
    print_output('请输入水印内容:')
    text.data = get_input()

def get_text(text: wrapper) -> str:
    return text.data

#endregion

#region 图片源

@errhandler
def set_psource(psource: wrapper):
    print_output('请输入图片源路径:')
    ans = get_input()
    if not os.path.exists(ans):
        raise ValueError(f'无效的图片路径 \'{ans}\'.')
    psource.data = ans

def get_psource(psource: wrapper) -> str:
    return psource.data

#endregion

#region 不透明度

@errhandler
def set_opacity(opacity: wrapper):
    print_output('请输入不透明度(%):')
    opc = float(get_input())
    if opc < 0 or opc > 100:
        raise ValueError(f'无效不透明度值 \'{opc}%\'.')
    opacity.data = opc

def get_opacity(opacity: wrapper) -> str:
    return f'{opacity.data}%'

#endregion

#region 对齐方式

def a_main(aligns: wrapper):
    m = menu.menu('Lekco Visurus - 对齐方式', 'Q')
    m.add(menu.option('H', '水平对齐', lambda: a_set_hailgn(aligns), lambda: a_get_halign(aligns)))
    m.add(menu.option('V', '垂直对齐', lambda: a_set_vailgn(aligns), lambda: a_get_valign(aligns)))
    m.add(menu.option('Q', '返回'))
    m.run()

def a_set_hailgn(aligns: wrapper):
    m = menu.menu('Lekco Visurus - 水平对齐')
    m.add(menu.option('L', '左对齐',   lambda: a_set_hleft(aligns)))
    m.add(menu.option('C', '居中对齐', lambda: a_set_hcenter(aligns)))
    m.add(menu.option('R', '右对齐',   lambda: a_set_hright(aligns)))
    m.add(menu.option('Q', '返回'))
    m.run()

def a_set_hleft(aligns: wrapper):
    aligns.data[0] = '左对齐'

def a_set_hcenter(aligns: wrapper):
    aligns.data[0] = '居中对齐'

def a_set_hright(aligns: wrapper):
    aligns.data[0] = '右对齐'

def a_get_halign(aligns: wrapper) -> str:
    return aligns.data[0]

def a_set_vailgn(aligns: wrapper):
    m = menu.menu('Lekco Visurus - 垂直对齐')
    m.add(menu.option('T', '顶部对齐', lambda: a_set_vtop(aligns)))
    m.add(menu.option('C', '居中对齐', lambda: a_set_vcenter(aligns)))
    m.add(menu.option('B', '底部对齐', lambda: a_set_vbottom(aligns)))
    m.add(menu.option('Q', '返回'))
    m.run()

def a_set_vtop(aligns: wrapper):
    aligns.data[1] = '顶部对齐'

def a_set_vcenter(aligns: wrapper):
    aligns.data[1] = '居中对齐'

def a_set_vbottom(aligns: wrapper):
    aligns.data[1] = '底部对齐'

def a_get_valign(aligns: wrapper) -> str:
    return aligns.data[1]

def a_value(aligns: wrapper) -> str:
    return f'{aligns.data[0]}, {aligns.data[1]}'

#endregion

#region 缩放方式

def z_main(scale: wrapper):
    m = menu.menu('Lekco Visurus - 缩放方式', 'Q')
    m.add(menu.option('M', '缩放模式', lambda: z_set_mode(scale), lambda: scale.data[0]))
    m.add(menu.option('S', '尺寸大小', lambda: z_set_size(scale), lambda: z_get_size(scale),            lambda: scale.data[0] == '固定尺寸'))
    m.add(menu.option('A', '缩放参考', lambda: z_set_ref(scale),  lambda: scale.data[1],                lambda: scale.data[0] == '比例缩放'))
    m.add(menu.option('P', '缩放比例', lambda: z_set_proportion(scale), lambda: z_get_propotion(scale), lambda: scale.data[0] == '比例缩放'))
    m.add(menu.option('Q', '返回'))
    m.run()

def z_set_mode(scale: wrapper):
    m = menu.menu('Lekco Visurus - 缩放模式')
    m.add(menu.option('F', '固定尺寸', lambda: z_fixed_scale_mode(scale)))
    m.add(menu.option('S', '比例缩放', lambda: z_proportion_scale_mode(scale)))
    m.add(menu.option('Q', '返回'))
    m.run()

def z_fixed_scale_mode(scale: wrapper):
    if scale.data[0] == '固定尺寸':
        return
    scale.data = ['固定尺寸', ('*', '*')]
    if content.data == '文字':
        scale.data[1] = ('*', 15)

def z_proportion_scale_mode(scale: wrapper):
    if scale.data[1] == '比例缩放':
        return
    scale.data = ['比例缩放', '宽', 0.1]

@errhandler
def z_set_size(scale: wrapper):
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
    if ans == ('*', '*') and content.data == '文字':
        raise ValueError('文字水印的尺寸大小不得为长宽自适应.')
    scale.data[1] = ans

def z_get_size(scale: wrapper) -> str:
    size = scale.data[1]
    return f'{size[0]}x{size[1]}'

def z_set_ref(scale: wrapper):
    m = menu.menu('Lekco Visurus - 缩放参考')
    m.add(menu.option('W', '宽', lambda: z_width_ref(scale)))
    m.add(menu.option('H', '高', lambda: z_height_ref(scale)))
    m.add(menu.option('Q', '返回'))
    m.run()

def z_width_ref(scale: wrapper):
    scale.data[1] = '宽'

def z_height_ref(scale: wrapper):
    scale.data[1] = '高'

@errhandler
def z_set_proportion(scale: wrapper):
    print_output('请输入缩放比例(%):')
    p = float(get_input())
    if p <= 0:
        raise ValueError(f'非法缩放比例 \'{p}%\'.')
    scale.data[2] = p / 100

def z_get_propotion(scale: wrapper) -> str:
    return f'{scale.data[2] * 100}%'

def z_value(scale: wrapper) -> str:
    if scale.data[0] == '固定尺寸':
        return f'{scale.data[0]} @{scale.data[1][0]}x{scale.data[1][1]}'
    else:
        return f'{scale.data[0]} @{scale.data[1]}x{scale.data[2] * 100}%'

#endregion

#region 水印位置

def p_main(position: wrapper):
    m = menu.menu('Lekco Visurus - 水印位置')
    m.add(menu.option('1', '图像左上角', lambda: p_1(position)))
    m.add(menu.option('2', '图像上中央', lambda: p_2(position)))
    m.add(menu.option('3', '图像右上角', lambda: p_3(position)))
    m.add(menu.option('4', '图像正左侧', lambda: p_4(position)))
    m.add(menu.option('5', '图像正中央', lambda: p_5(position)))
    m.add(menu.option('6', '图像正右侧', lambda: p_6(position)))
    m.add(menu.option('7', '图像左下角', lambda: p_7(position)))
    m.add(menu.option('8', '图像下中央', lambda: p_8(position)))
    m.add(menu.option('9', '图像右下角', lambda: p_9(position)))
    m.add(menu.option('X', '指定位置',   lambda: p_pose(position)))
    m.add(menu.option('R', '随机位置',   lambda: p_random(position)))
    m.add(menu.option('Q', '返回'))
    m.run()

def p_1(position: wrapper):
    position.data = '图像左上角'

def p_2(position: wrapper):
    position.data = '图像上中央'

def p_3(position: wrapper):
    position.data = '图像右上角'

def p_4(position: wrapper):
    position.data = '图像正左侧'

def p_5(position: wrapper):
    position.data = '图像正中央'

def p_6(position: wrapper):
    position.data = '图像正右侧'

def p_7(position: wrapper):
    position.data = '图像左下角'

def p_8(position: wrapper):
    position.data = '图像下中央'

def p_9(position: wrapper):
    position.data = '图像右下角'

@errhandler
def p_pose(position: wrapper):
    print_output('请输入水印位置 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    for i in ans:
        if i < 0:
            raise ValueError(f'非法的坐标 \'{ans[0]}, {ans[1]}\'.')
    position.data = (ans[0], ans[1])

def p_random(position: wrapper):
    position.data = '随机'

def p_value(position: wrapper) -> str:
    return position.data.__str__()

#endregion

#region 位置偏移

@errhandler
def set_offset(offset: wrapper):
    print_output('请输入位置偏移 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    offset.data = (ans[0], ans[1])

def get_offset(offset: wrapper) -> str:
    return offset.data.__str__()

#endregion
