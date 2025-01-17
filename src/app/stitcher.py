import util

from . import input
from . import appconfig
from . import output
from . import workspace

from PIL import Image

targets: list[util.InImage] = []

CONFIG = appconfig.get('stitcher', [
    util.Field('direction',  '垂直方向'),
    util.Field('clip',       '扩展至最长边'),
    util.Field('halign',     '左对齐'),
    util.Field('valign',     '顶部对齐'),
    util.Field('spacing',    0),
    util.Field('background', util.Color('#FFFFFFFF')),
])

def main():
    m = util.Menu('Lekco Visurus - 图像拼接', 'Q')
    m.add(util.Display(display))
    m.add(util.Splitter('- 拼接选项 -'))
    m.add(util.Option('D', '拼接方向', d_main,         d_value))
    m.add(util.Option('L', '裁切模式', l_main,         l_value))
    m.add(util.Option('A', '对齐模式', ah_main,        a_value, enfunc=lambda: CONFIG.direction == '垂直方向'))
    m.add(util.Option('A', '对齐模式', av_main,        a_value, enfunc=lambda: CONFIG.direction == '水平方向'))
    m.add(util.Option('P', '图像间距', set_spacing,    get_spacing))
    m.add(util.Option('B', '背景颜色', set_background, get_background))
    m.add(util.Splitter('- 导入与导出 -'))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('S', '更变图像顺序',  change_order))
    m.add(util.Option('Y', '保存当前设置',  lambda: appconfig.save(CONFIG)))
    m.add(util.Option('O', '执行导出…',     execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    if len(targets) > 0:
        util.print_left('目标图像顺序:')
        for i in range(len(targets)):
            util.print_left(f'{i + 1}. ' + targets[i].formated_name())
    else:
        util.print_left('目标图像为空.')
    util.print_splitter()

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

@util.errhandler
def change_order():
    if len(targets) == 0:
        raise ValueError('目标图像为空.')
    util.print_output('请输入图像顺序: ')
    util.print_ps('请使用 , 分隔序号.')
    ans = list(map(int, util.get_input().split(',')))
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

def d_main():
    m = util.Menu('Lekco Visurus - 拼接方向')
    m.add(util.Option('H', '水平方向', d_horizion))
    m.add(util.Option('V', '垂直方向', d_vertical))
    m.add(util.Option('Q', '返回'))
    m.run()

def d_horizion():
    CONFIG.direction = '水平方向'

def d_vertical():
    CONFIG.direction = '垂直方向'

def d_value() -> str:
    return CONFIG.direction

#endregion

#region 裁切模式

def l_main():
    m = util.Menu('Lekco Visurus - 裁切模式')
    m.add(util.Option('L', '扩展至最长边', l_longest))
    m.add(util.Option('S', '裁切至最短边', l_shortest))
    m.add(util.Option('C', '自定义',      l_custom))
    m.add(util.Option('Q', '返回'))
    m.run()

def l_longest():
    CONFIG.clip = '扩展至最长边'

def l_shortest():
    CONFIG.clip = '裁切至最短边'

@util.errhandler
def l_custom():
    util.print_output('请输入裁切宽/高:')
    l = int(util.get_input())
    if l <= 0:
        raise ValueError(f'非法宽/高值 \'{l}\'.')
    CONFIG.clip = l

def l_value() -> str:
    if isinstance(CONFIG.clip, str):
        return CONFIG.clip
    return f'{CONFIG.clip}px'

#endregion

#region 对齐模式

def ah_main():
    m = util.Menu('Lekco Visurus - 对齐模式')
    m.add(util.Option('L', '左对齐',   ah_left))
    m.add(util.Option('C', '居中对齐', ah_center))
    m.add(util.Option('R', '右对齐',   ah_right))
    m.add(util.Option('Q', '返回'))
    m.run()

def ah_left():
    CONFIG.halign = '左对齐'

def ah_center():
    CONFIG.halign = '居中对齐'

def ah_right():
    CONFIG.halign = '右对齐'

def av_main():
    m = util.Menu('Lekco Visurus - 对齐模式')
    m.add(util.Option('T', '顶部对齐', av_top))
    m.add(util.Option('C', '居中对齐', av_center))
    m.add(util.Option('B', '底部对齐', av_bottom))
    m.add(util.Option('Q', '返回'))
    m.run()

def av_top():
    CONFIG.valign = '顶部对齐'

def av_center():
    CONFIG.valign = '居中对齐'

def av_bottom():
    CONFIG.valign = '底部对齐'

def a_value() -> str:
    return CONFIG.valign

#endregion

#region 图像间距

@util.errhandler
def set_spacing():
    util.print_output('请输入图像间距:')
    ans = int(util.get_input())
    if ans < 0:
        raise ValueError(f'非法的图像间距 \'{ans}\'.')
    CONFIG.spacing = ans

def get_spacing() -> str:
    return f'{CONFIG.spacing}px'

#endregion

#region 背景颜色

def set_background():
    CONFIG.background = input.input_color()

def get_background() -> str:
    return CONFIG.background.hex

#endregion

#region 图像处理

def valign_pos(imgh: int, backh: int) -> int:
    if   CONFIG.valign == '顶部对齐':
        return 0
    elif CONFIG.valign == '居中对齐':
        return int((backh - imgh) / 2)
    else:
        return backh - imgh

def h_process(imgs: list[Image.Image]) -> Image.Image:
    height = 0
    if   CONFIG.clip == '扩展至最长边':
        height = max(img.height for img in imgs)
    elif CONFIG.clip == '裁切至最短边':
        height = min(img.height for img in imgs)
    else:
        height = CONFIG.clip
    width = sum(img.width for img in imgs) + (len(imgs) - 1) * CONFIG.spacing
    back  = Image.new('RGBA', (width, height), CONFIG.background.tuple)
    x     = 0
    for img in imgs:
        back.paste(img, (x, valign_pos(img.height, height)), img)
        x += img.width + CONFIG.spacing
    return back

def halign_pos(imgw: int, backw: int) -> int:
    if   CONFIG.halign == '左对齐':
        return 0
    elif CONFIG.halign == '居中对齐':
        return int((backw - imgw) / 2)
    else:
        return backw - imgw

def v_process(imgs: list[Image.Image]) -> Image.Image:
    width = 0
    if   CONFIG.clip == '扩展至最长边':
        width = max(img.width for img in imgs)
    elif CONFIG.clip == '裁切至最短边':
        width = min(img.width for img in imgs)
    else:
        width = CONFIG.clip
    height = sum(img.height for img in imgs) + (len(imgs) - 1) * CONFIG.spacing
    back   = Image.new('RGBA', (width, height), CONFIG.background.tuple)
    y      = 0
    for img in imgs:
        back.paste(img, (halign_pos(img.width, back.width), y), img)
        y += img.height + CONFIG.spacing
    return back

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    imgs = [img.image for img in targets]
    out  = None
    if CONFIG.direction == '水平方向':
        out = h_process(imgs)
    else:
        out = v_process(imgs)
    
    out = util.OutImage(out, targets[0])
    output.main([out])

#endregion
