import util
import watermark

from app import output
from app import workspace
from app import appconfig

from PIL import Image

targets: list[util.InImage] = []

CONFIG = appconfig.get('mounting', [
    util.Field('width',     0.1),
    util.Field('height',    0.08),
    util.Field('color',     util.Color('#FFFFFFFF')),
    util.Field('watermark', False),
    util.Field('wstyle',    watermark.Style.default(), watermark.Style.self_validate)
])

@util.errhandler
def main():
    m = util.Menu('Lekco Visurus - 图像装裱', 'Q')
    m.add(util.Display(display))
    m.add(util.Splitter('- 装裱参数 -'))
    m.add(util.Option('W', '边距宽度', lambda: margin_main('width'),  lambda: margin_value('width')))
    m.add(util.Option('H', '边距高度', lambda: margin_main('height'), lambda: margin_value('height')))
    m.add(util.Option('B', '裱褙颜色', set_color,                     get_color))
    m.add(util.Option('E', '图像水印', e_main,                        e_value))
    m.add(util.Option('S', '水印样式…', CONFIG.wstyle.set,            enfunc=lambda: CONFIG.watermark))
    m.add(util.Option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(util.Splitter('- 导入与导出 -'))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('O', '执行导出…', execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def choose_targets():
    global targets
    targets = workspace.c_main()

def display():
    util.print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        util.print_left(f'{i + 1}. ' + targets[i].formated_name())
    util.print_splitter()

def margin_main(attrname: str):
    m = util.Menu('Lekco Visurus - 边距尺寸')
    m.add(util.Option('F', '固定尺寸', lambda: margin_fixed(attrname)))
    m.add(util.Option('S', '指定比例', lambda: margin_propotion(attrname)))
    m.add(util.Option('Q', '返回'))
    m.run()

@util.errhandler
def margin_fixed(attrname: str):
    util.print_output('请输入尺寸值(正整数):')
    value = int(input())
    if value <= 0:
        raise ValueError('尺寸值必须为正整数.')
    setattr(CONFIG, attrname, value)

@util.errhandler
def margin_propotion(attrname: str):
    util.print_output('请输入比例(%):')
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
    CONFIG.color = util.Color.input()

def get_color() -> str:
    return CONFIG.color.hex

#region 图像水印

def e_main():
    m = util.Menu('Lekco Visurus - 图像水印')
    m.add(util.Option('E', '启用', e_enable))
    m.add(util.Option('D', '关闭', e_disable))
    m.run()

def e_enable():
    CONFIG.watermark = True

def e_disable():
    CONFIG.watermark = False

def e_value() -> str:
    return '启用' if CONFIG.watermark else '关闭'

#endregion

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for img in targets:
        result = process(img.image)
        out.append(util.OutImage(result, img))
    if len(out) > 0:
        output.main(out)

@util.errhandler
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
