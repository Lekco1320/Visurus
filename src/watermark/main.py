import util
import random

from .scaler import *
from .anchor import *
from .mark   import *
from .style  import Style

from app import output
from app import workspace
from app import resources
from app import appconfig

from PIL import Image

targets = []
CONFIG  = appconfig.get('watermark', [
    util.Field('style', Style.DEFAULT, Style.self_validate)
])

#region 主函数

def main_menu():
    m = util.Menu('Lekco Visurus - 添加水印', 'Q')
    m.add(util.Display(display))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('S', '水印样式…',     CONFIG.style.set))
    m.add(util.Option('Y', '保存当前设置',  lambda: appconfig.save(CONFIG)))
    m.add(util.Option('O', '执行导出…',     execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        util.print_left(f'{i + 1}. ' + targets[i].formated_name())
    util.print_splitter()

#endregion

# 选择图片对象

def choose_targets():
    global targets
    targets = workspace.c_main()

#region 图像处理

def get_scaler(style: Style, size: tuple[int, int]) -> Scaler:
    sscaler = None
    if  style.scale[0] == '固定尺寸':
        sscaler = FixedScaler(style.scale[1][0], style.scale[1][1])
    else:
        ref     = ScaleRef.HEIGHT if style.scale[1] == '高' else ScaleRef.WIDTH
        sscaler = ProportionScaler(ref, style.scale[2], size)
    return sscaler

def get_position(style: Style, size: tuple[int, int]) -> tuple[int, int]:
    if   style.position == '随机':
        return (random.randint(0, size[0]), random.randint(0, size[1]))
    elif isinstance(style.position, tuple):
        return style.position
    key  = style.position[2:]
    if   key == '左上角':
        return (0, 0)
    elif key == '上中央':
        return (int(size[0] / 2), 0)
    elif key == '右上角':
        return (size[0], 0)
    elif key == '正左侧':
        return (0, int(size[1] / 2))
    elif key == '正中央':
        return (int(size[0] / 2), int(size[1] / 2))
    elif key == '正右侧':
        return (size[0], int(size[1] / 2))
    elif key == '左下角':
        return (0, size[1])
    elif key == '下中央':
        return (int(size[0] / 2), size[1])
    elif key == '右下角':
        return (size[0], size[1])

def get_anchor(style: Style, position: tuple[int, int]) -> Anchor:
    haligndict = {
        '左对齐'   : HorizonalAlignment.LEFT,
        '居中对齐' : HorizonalAlignment.CENTER,
        '右对齐'   : HorizonalAlignment.RIGHT
    }
    valigndict = {
        '顶部对齐' : VerticalAlignment.TOP,
        '居中对齐' : VerticalAlignment.CENTER,
        '底部对齐' : VerticalAlignment.BOTTOM
    }
    return Anchor(position, style.offset, haligndict[style.aligns[0]], valigndict[style.aligns[1]])

def get_mark(style: Style, anchor: Anchor, scaler: Scaler) -> MarkBase:
    mark = None
    if  style.content == '文字':
        mark = LabelMark(anchor, scaler, resources.get(style.font), style.color, style.text)
    else:
        mark = ImageMark(anchor, scaler, style.psource, style.opacity)
    return mark

def process(style: Style, img: Image.Image) -> Image.Image:
    position = get_position(style, img.size)
    anchor   = get_anchor(style, position)
    scaler   = get_scaler(style, img.size)
    mark     = get_mark(style, anchor, scaler)
    return mark.mark(img)

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        util.print_output(f'正在处理 {srcimg.name}...')
        processed = process(CONFIG.style, srcimg.image)
        out.append(util.OutImage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)

#endregion
