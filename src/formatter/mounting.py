import util
import watermark

from util import *
from util import menu
from app import output
from app import workspace
from app import appconfig
from PIL import Image

targets: list[image] = []

CONFIG = appconfig.get('mounting', [
    util.field('width',     0.1),
    util.field('height',    0.08),
    util.field('color',     color('#FFFFFFFF')),
    util.field('watermark', False),
    util.field('wstyle',    watermark.style.default(), watermark.style.self_validate)
])

@errhandler
def main():
    m = menu.menu('Lekco Visurus - 图像装裱', 'Q')
    m.add(menu.display(display))
    m.add(menu.splitter('- 装裱参数 -'))
    m.add(menu.option('W', '边距宽度', lambda: margin_main('width'),  lambda: margin_value('width')))
    m.add(menu.option('H', '边距高度', lambda: margin_main('height'), lambda: margin_value('height')))
    m.add(menu.option('B', '裱褙颜色', set_color,                     get_color))
    m.add(menu.option('E', '图像水印', e_main,                        e_value))
    m.add(menu.option('S', '水印样式…', CONFIG.wstyle.set,            enfunc=lambda: CONFIG.watermark))
    m.add(menu.option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(menu.splitter('- 导入与导出 -'))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
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

def margin_main(attrname: str):
    m = menu.menu('Lekco Visurus - 边距尺寸')
    m.add(menu.option('F', '固定尺寸', lambda: margin_fixed(attrname)))
    m.add(menu.option('S', '指定比例', lambda: margin_propotion(attrname)))
    m.add(menu.option('Q', '返回'))
    m.run()

@errhandler
def margin_fixed(attrname: str):
    print_output('请输入尺寸值(正整数):')
    value = int(input())
    if value <= 0:
        raise ValueError('尺寸值必须为正整数.')
    setattr(CONFIG, attrname, value)

@errhandler
def margin_propotion(attrname: str):
    print_output('请输入比例(%):')
    value = float(int(input()) / 100)
    if value <= 0:
        raise ValueError('比例值不得为负.')
    setattr(CONFIG, attrname, value)

def margin_value(attrname: str):
    attr = getattr(CONFIG, attrname)
    if isinstance(attr, int):
        return attr
    else:
        return f'{attr * 100}%'

def set_color():
    CONFIG.color = color.input()

def get_color() -> str:
    return CONFIG.color.hex

#region 图像水印

def e_main():
    m = menu.menu('Lekco Visurus - 图像水印')
    m.add(menu.option('E', '启用', e_enable))
    m.add(menu.option('D', '关闭', e_disable))
    m.run()

def e_enable():
    CONFIG.watermark = True

def e_disable():
    CONFIG.watermark = False

def e_value() -> str:
    return '启用' if CONFIG.watermark else '关闭'

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
    if isinstance(CONFIG.width, int):
        x      = CONFIG.width
        width += x * 2
    else:
        x      = int(CONFIG.width * image.width)
        width += x * 2
    if isinstance(CONFIG.height, int):
        y       = CONFIG.height
        height += y * 2
    else:
        y       = int(CONFIG.height * image.height)
        height += y * 2
    if CONFIG.watermark:
        image = watermark.process(CONFIG.wstyle, image)
    result = Image.new('RGBA', (width, height), CONFIG.color)
    result.paste(image, (x, y), image)
    return result
