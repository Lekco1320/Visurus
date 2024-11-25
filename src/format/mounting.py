import watermark

from util import *
from util import menu
from util import output
from util import workspace

from config import Config
from PIL import Image

targets: list[image] = []

mwidth      = wrapper(Config['mounting.width'])
mheight     = wrapper(Config['mounting.height'])
bcolor      = wrapper(Config['mounting.color'])
enwatermark = wrapper(Config['mounting.enwatermark'])

@errhandler
def main():
    m = menu.menu('Lekco Visurus - 图像装裱', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('W', '边距宽度', lambda: margin_main(mwidth),  lambda: margin_value(mwidth)))
    m.add(menu.option('H', '边距高度', lambda: margin_main(mheight), lambda: margin_value(mheight)))
    m.add(menu.option('B', '裱褙颜色', lambda: set_color(bcolor),    lambda: get_color(bcolor)))
    m.add(menu.option('E', '图像水印', lambda: e_main(enwatermark),  lambda: e_value(enwatermark)))
    m.add(menu.option('S', '水印样式…', watermark.style.main,        enfunc=lambda: enwatermark.data))
    m.add(menu.option('O', '执行导出…', execute))
    m.add(menu.option('Q', '返回'))
    m.run()

def choose_targets():
    global targets
    targets = workspace.c_main()

def display():
    print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        print_left(f'{i + 1}. ' + targets[i].formated_name())
    print_spliter()

def margin_main(margin: wrapper):
    m = menu.menu('Lekco Visurus - 边距尺寸')
    m.add(menu.option('F', '固定尺寸', lambda: margin_fixed(margin)))
    m.add(menu.option('S', '指定比例', lambda: margin_propotion(margin)))
    m.add(menu.option('Q', '返回'))
    m.run()

@errhandler
def margin_fixed(margin: wrapper):
    print_output('请输入尺寸值(正整数):')
    value = int(input())
    if value <= 0:
        raise ValueError('尺寸值必须为正整数.')
    margin.data = value

@errhandler
def margin_propotion(margin: wrapper):
    print_output('请输入比例(%):')
    value = float(int(input()) / 100)
    if value <= 0:
        raise ValueError('比例值不得为负.')
    margin.data = value

def margin_value(margin: wrapper):
    if isinstance(margin.data, int):
        return margin.data
    else:
        return f'{margin.data * 100}%'

def set_color(bcolor: wrapper):
    bcolor.data = color.input().hex

def get_color(bcolor: wrapper) -> str:
    return bcolor.data

#region 图像水印

def e_main(enwatermark: wrapper):
    m = menu.menu('Lekco Visurus - 图像水印')
    m.add(menu.option('E', '启用', lambda: e_enable(enwatermark)))
    m.add(menu.option('D', '关闭', lambda: e_disable(enwatermark)))
    m.run()

def e_enable(enwatermark: wrapper):
    enwatermark.data = True

def e_disable(enwatermark: wrapper):
    enwatermark.data = False

def e_value(enwatermark: wrapper) -> str:
    return '启用' if enwatermark.data else '关闭'

#endregion

@errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for img in targets:
        result = process(img.image)
        out.append(outimage(result, img))
    if len(out) > 0:
        output.main(out)

@errhandler
def process(image: Image.Image) -> Image.Image:
    width  = image.width
    height = image.height
    x, y   = 0, 0
    if isinstance(mwidth.data, int):
        x      = mwidth.data
        width += x * 2
    else:
        x      = int(mwidth.data * image.width)
        width += x * 2
    if isinstance(mheight.data, int):
        y       = mheight.data
        height += y * 2
    else:
        y       = int(mheight.data * image.height)
        height += y * 2
    if enwatermark.data:
        image = watermark.process(image)
    result = Image.new('RGBA', (width, height), color(bcolor.data).tuple)
    result.paste(image, (x, y), image)
    return result
