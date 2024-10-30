import random
import watermark.style as style

from .scaler import *
from .anchor import *
from .mark import *

from util import *
from util import menu
from util import output
from util import workspace

from PIL import Image

# 变量
targets = []

#region 主函数

def main():
    m = menu.menu('Lekco Visurus - 添加水印', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('S', '水印样式…', style.main))
    m.add(menu.option('O', '执行导出…', execute))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        print_left(f'{i + 1}. ' + targets[i].formated_name())
    print_spliter()

#endregion

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

#region 图像处理

def get_scaler(size: tuple[int, int]) -> scaler:
    sscaler = None
    if  style.scale.data[0] == '固定尺寸':
        sscaler = fixed_scaler(style.scale.data[1][0], style.scale.data[1][1])
    else:
        ref     = scale_ref.HEIGHT if style.scale.data[1] == '高' else scale_ref.WIDTH
        sscaler = proportion_scaler(ref, style.scale.data[2], size)
    return sscaler

def get_position(size: tuple[int, int]) -> tuple[int, int]:
    if   style.position.data == '随机':
        return (random.randint(0, size[0]), random.randint(0, size[1]))
    elif isinstance(style.position.data, tuple):
        return style.position.data
    key  = style.position.data[2:]
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

def get_anchor(position: tuple[int, int]) -> anchor:
    haligndict = {
        '左对齐'   : horizonal_alignment.LEFT,
        '居中对齐' : horizonal_alignment.CENTER,
        '右对齐'   : horizonal_alignment.RIGHT
    }
    valigndict = {
        '顶部对齐' : vertical_alignment.TOP,
        '居中对齐' : vertical_alignment.CENTER,
        '底部对齐' : vertical_alignment.BOTTOM
    }
    return anchor(position, style.offset.data, haligndict[style.aligns.data[0]], valigndict[style.aligns.data[1]])

def get_mark(anchor: anchor, scaler: scaler) -> markbase:
    mark = None
    if  style.content.data == '文字':
        mark = label_mark(anchor, scaler, style.font.data, style.fcolor.data, style.ftext.data)
    else:
        mark = image_mark(anchor, scaler, style.psource.data, style.opacity.data)
    return mark

def process(img: Image.Image) -> Image.Image:
    position = get_position(img.size)
    anchor   = get_anchor(position)
    scaler   = get_scaler(img.size)
    mark     = get_mark(anchor, scaler)
    return mark.mark(img)

@errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        print_output(f'正在处理 {srcimg.name}...')
        processed = process(srcimg.image)
        out.append(output.outimage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)

#endregion
