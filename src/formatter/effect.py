import util
import watermark

from app import output
from app import workspace
from app import appconfig

from formatter import shadow
from formatter import round_corner

from PIL       import Image

CONFIG = appconfig.get('effect', [
    util.Field('shadow',    False),
    util.Field('sstyle',    shadow.Style.DEFAULT,       shadow.Style.self_validate),
    util.Field('round',     False),
    util.Field('rstyle',    round_corner.Style.DEFAULT, round_corner.Style.self_validate),
    util.Field('order',     ('阴影', '圆角', '水印')),
    util.Field('watermark', False),
    util.Field('wstyle',    watermark.Style.DEFAULT,    watermark.Style.self_validate),
])

targets = []

def main():
    m = util.Menu('Lekco Visurus - 图像效果', 'Q')
    m.add(util.Display(display))
    m.add(util.Splitter('- 效果设置 -'))
    m.add(util.Option('H', '图像阴影',  h_main,    h_value))
    m.add(util.Option('A', '阴影效果…', CONFIG.sstyle.set, enfunc=lambda: CONFIG.shadow))
    m.add(util.Option('R', '图像圆角',  r_main,    r_value))
    m.add(util.Option('D', '圆角参数',  CONFIG.rstyle.set, enfunc=lambda: CONFIG.round))
    m.add(util.Option('W', '图像水印',  w_main,    w_value))
    m.add(util.Option('T', '水印样式…', CONFIG.wstyle.set, enfunc=lambda: CONFIG.watermark))
    m.add(util.Option('E', '效果顺序', set_order, get_order))
    m.add(util.Option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(util.Splitter('- 导入与导出 -'))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('O', '执行导出…',    execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        util.print_left(f'{i + 1}. ' + targets[i].formated_name())
    util.print_splitter()

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

#region 图像阴影

def h_main():
    m = util.Menu('Lekco Visurus - 图像阴影')
    m.add(util.Option('E', '启用', h_enable))
    m.add(util.Option('D', '关闭', h_disable))
    m.run()

def h_enable():
    CONFIG.shadow = True

def h_disable():
    CONFIG.shadow = False

def h_value() -> str:
    return '启用' if CONFIG.shadow else '关闭'

#endregion

#region 图像圆角

def r_main():
    m = util.Menu('Lekco Visurus - 图像圆角')
    m.add(util.Option('E', '启用', r_enable))
    m.add(util.Option('D', '关闭', r_disable))
    m.run()

def r_enable():
    CONFIG.round = True

def r_disable():
    CONFIG.round = False

def r_value() -> str:
    return '启用' if CONFIG.round else '关闭'

#endregion

#region 图像水印

def w_main():
    m = util.Menu('Lekco Visurus - 图像水印')
    m.add(util.Option('E', '启用', w_enable))
    m.add(util.Option('D', '关闭', w_disable))
    m.run()

def w_enable():
    CONFIG.watermark = True

def w_disable():
    CONFIG.watermark = False

def w_value() -> str:
    return '启用' if CONFIG.watermark else '关闭'

#endregion

#region 效果顺序

@util.errhandler
def set_order():
    util.print_output('请输入效果顺序:')
    util.print_ps('例: 阴影 圆角 水印')
    ans = util.get_input().strip().split()
    add = set()
    for effect in ans:
        if effect not in ['阴影', '圆角', '水印']:
            raise ValueError('未知的效果名称')
        add.add(effect)
    if len(add) != 3:
        raise ValueError('效果数量错误.')
    CONFIG.order = tuple(ans)

def get_order() -> str:
    return '→'.join(CONFIG.order)

#endregion

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        util.print_output(f'正在处理 {srcimg.name}...')
        processed = process(srcimg.image)
        out.append(output.OutImage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)

def apply_shadow(image: Image.Image) -> Image.Image:
    return shadow.process(CONFIG.sstyle, image) if CONFIG.shadow else image

def apply_round(image: Image.Image) -> Image.Image:
    return round_corner.process(CONFIG.rstyle, image) if CONFIG.round else image

def apply_watermark(image: Image.Image) -> Image.Image:
    return watermark.process(CONFIG.wstyle, image) if CONFIG.watermark else image

@util.errhandler
def process(image: Image.Image):
    for effect in CONFIG.order:
        if   effect == '阴影':
            image = apply_shadow(image)
        elif effect == '圆角':
            image = apply_round(image)
        elif effect == '水印':
            image = apply_watermark(image)
    return image

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        util.print_output(f'正在处理 {srcimg.name}...')
        processed = process(srcimg.image)
        out.append(output.OutImage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)
