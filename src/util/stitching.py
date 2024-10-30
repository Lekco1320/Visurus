from util import *
from util import menu
from util import output
from util import workspace
from util import color

from PIL import Image
from config import Config

targets    = []
direction  = wrapper(Config['stitching.direction'])
clip       = wrapper(Config['stitching.clip'])
halign     = wrapper(Config['stitching.halign'])
valign     = wrapper(Config['stitching.valign'])
spacing    = wrapper(Config['stitching.spacing'])
background = wrapper(Config['stitching.background'])

def main():
    m = menu.menu('Lekco Visurus - 图像拼接', 'Q')
    m.add(menu.display(display))
    m.add(menu.splitter('- 拼接选项 -'))
    m.add(menu.option('D', '拼接方向', lambda: d_main(direction),          lambda: d_value(direction)))
    m.add(menu.option('L', '裁切模式', lambda: l_main(clip),               lambda: l_value(clip)))
    m.add(menu.option('A', '对齐模式', lambda: ah_main(halign),            lambda: a_value(halign),    enfunc=lambda: direction.data == '垂直方向'))
    m.add(menu.option('A', '对齐模式', lambda: av_main(valign),            lambda: a_value(valign),    enfunc=lambda: direction.data == '水平方向'))
    m.add(menu.option('P', '图像间距', lambda: set_spacing(spacing),       lambda: get_spacing(spacing)))
    m.add(menu.option('B', '背景颜色', lambda: set_background(background), lambda: get_background(background)))
    m.add(menu.splitter('- 导入与导出 -'))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('S', '更变图像顺序',  change_order))
    m.add(menu.option('O', '执行导出…',     execute))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    if len(targets) > 0:
        print_left('目标图像顺序:')
        for i in range(len(targets)):
            print_left(f'{i + 1}. ' + targets[i].formated_name())
    else:
        print_left('目标图像为空.')
    print_spliter()

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

@errhandler
def change_order():
    if len(targets) == 0:
        raise ValueError('目标图像为空.')
    print_output('请输入图像顺序: ')
    print_ps('请使用 , 分隔序号.')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != len(targets):
        raise ValueError('图像数量不匹配.')
    for id in range(1, len(targets) + 1):
        if id not in ans:
            raise ValueError(f'序号为{id}的图像顺序未知.')
    old = targets.copy()
    targets.clear()
    for id in ans:
        targets.append(old[id - 1])

#region 拼接方向

def d_main(direction: wrapper):
    m = menu.menu('Lekco Visurus - 拼接方向')
    m.add(menu.option('H', '水平方向', lambda: d_horizion(direction)))
    m.add(menu.option('V', '垂直方向', lambda: d_vertical(direction)))
    m.add(menu.option('Q', '返回'))
    m.run()

def d_horizion(direction: wrapper):
    direction.data = '水平方向'

def d_vertical(direction: wrapper):
    direction.data = '垂直方向'

def d_value(direction: wrapper) -> str:
    return direction.data

#endregion

#region 裁切模式

def l_main(clip: wrapper):
    m = menu.menu('Lekco Visurus - 裁切模式')
    m.add(menu.option('L', '扩展至最长边', lambda: l_longest(clip)))
    m.add(menu.option('S', '裁切至最短边', lambda: l_shortest(clip)))
    m.add(menu.option('C', '自定义',      lambda: l_custom(clip)))
    m.add(menu.option('Q', '返回'))
    m.run()

def l_longest(clip: wrapper):
    clip.data = '扩展至最长边'

def l_shortest(clip: wrapper):
    clip.data = '裁切至最短边'

@errhandler
def l_custom(clip: wrapper):
    print_output('请输入裁切宽/高:')
    l = int(get_input())
    if l <= 0:
        raise ValueError(f'非法宽/高值 \'{l}\'.')
    clip.data = l

def l_value(clip: wrapper) -> str:
    if isinstance(clip.data, str):
        return clip.data
    return f'{clip.data}px'

#endregion

#region 对齐模式

def ah_main(halign: wrapper):
    m = menu.menu('Lekco Visurus - 对齐模式')
    m.add(menu.option('L', '左对齐',   lambda: ah_left(halign)))
    m.add(menu.option('C', '居中对齐', lambda: ah_center(halign)))
    m.add(menu.option('R', '右对齐',   lambda: ah_right(halign)))
    m.add(menu.option('Q', '返回'))
    m.run()

def ah_left(halign: wrapper):
    halign.data = '左对齐'

def ah_center(halign: wrapper):
    halign.data = '居中对齐'

def ah_right(halign: wrapper):
    halign.data = '右对齐'

def av_main(valign: wrapper):
    m = menu.menu('Lekco Visurus - 对齐模式')
    m.add(menu.option('T', '顶部对齐', lambda: av_top(valign)))
    m.add(menu.option('C', '居中对齐', lambda: av_center(valign)))
    m.add(menu.option('B', '底部对齐', lambda: av_bottom(valign)))
    m.add(menu.option('Q', '返回'))
    m.run()

def av_top(valign: wrapper):
    valign.data = '顶部对齐'

def av_center(valign: wrapper):
    valign.data = '居中对齐'

def av_bottom(valign: wrapper):
    valign.data = '底部对齐'

def a_value(align: wrapper) -> str:
    return align.data

#endregion

#region 图像间距

@errhandler
def set_spacing(spacing: wrapper):
    print_output('请输入图像间距:')
    ans = int(get_input())
    if ans < 0:
        raise ValueError(f'非法的图像间距 \'{ans}\'.')
    spacing.data = ans

def get_spacing(spacing: wrapper) -> str:
    return f'{spacing.data}px'

#endregion

#region 背景颜色

def set_background(background: wrapper):
    background.data = color.input().hex

def get_background(background: wrapper) -> str:
    return background.data

#endregion

#region 图像处理

def valign_pos(imgh: int, backh: int) -> int:
    if   valign.data == '顶部对齐':
        return 0
    elif valign.data == '居中对齐':
        return int((backh - imgh) / 2)
    else:
        return backh - imgh

def h_process(imgs: list[Image.Image]) -> Image.Image:
    height = 0
    if   clip.data == '扩展至最长边':
        height = max(img.height for img in imgs)
    elif clip.data == '裁切至最短边':
        height = min(img.height for img in imgs)
    else:
        height = clip.data
    width = sum(img.width for img in imgs) + (len(imgs) - 1) * spacing.data
    back  = Image.new('RGBA', (width, height), color.color(background.data).tuple)
    x     = 0
    for img in imgs:
        back.paste(img, (x, valign_pos(img.height, height)), img)
        x += img.width + spacing.data
    return back

def halign_pos(imgw: int, backw: int) -> int:
    if   halign.data == '左对齐':
        return 0
    elif halign.data == '居中对齐':
        return int((backw - imgw) / 2)
    else:
        return backw - imgw

def v_process(imgs: list[Image.Image]) -> Image.Image:
    width = 0
    if   clip.data == '扩展至最长边':
        width = max(img.width for img in imgs)
    elif clip.data == '裁切至最短边':
        width = min(img.width for img in imgs)
    else:
        width = clip.data
    height = sum(img.height for img in imgs) + (len(imgs) - 1) * spacing.data
    back   = Image.new('RGBA', (width, height), color.color(background.data).tuple)
    y      = 0
    for img in imgs:
        back.paste(img, (halign_pos(img.width, back.width), y), img)
        y += img.height + spacing.data
    return back

@errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    imgs = [img.image for img in targets]
    out  = None
    if direction.data == '水平方向':
        out = h_process(imgs)
    else:
        out = v_process(imgs)
    
    out = output.outimage(out, targets[0])
    output.main([out])

#endregion
