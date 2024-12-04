from util import *
from util import config
from util import menu
from util import output
from util import workspace

from PIL import Image
from PIL import ImageFilter

targets = []

CONFIG = config.get('shadow', {
    'color'  : color('#0000007F'),
    'offset' : (10, 10),
    'limit'  : (8, 8),
    'blur'   : 5,
})

def main():
    targets.clear()
    
    m = menu.menu('Lekco Visurus - 添加阴影', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('S', '阴影效果…',     style_main))
    m.add(menu.option('Y', '保存当前设置',  lambda: config.save(CONFIG)))
    m.add(menu.option('O', '执行导出…',     execute))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        print_left(f'{i + 1}. ' + targets[i].formated_name())
    print_spliter()

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

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

def style_main():
    m = menu.menu('Lekco Visurus - 阴影效果', 'Q')
    m.add(menu.option('C', '阴影颜色', set_color,  get_color))
    m.add(menu.option('O', '阴影偏移', set_offset, get_offset))
    m.add(menu.option('L', '范围限制', set_limit,  get_limit))
    m.add(menu.option('B', '模糊程度', set_blur,   get_blur))
    m.add(menu.option('Q', '返回'))
    m.run()

def set_color():
    CONFIG.color = color.input()

def get_color() -> str:
    return CONFIG.color.__str__()

@errhandler
def set_offset():
    print_output('请输入偏移量 x,y :')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    CONFIG.offset = (ans[0], ans[1])

def get_offset() -> str:
    return CONFIG.offset.__str__()

@errhandler
def set_limit():
    print_output('请输入范围限制 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    CONFIG.limit = (ans[0], ans[1])

def get_limit() -> str:
    return CONFIG.limit.__str__()

@errhandler
def set_blur():
    print_output('请输入模糊程度(>=0):')
    ans = int(get_input())
    if ans < 0:
        raise ValueError(f'模糊程度 \'{ans}\' 无效.')
    CONFIG.blur = ans

def get_blur() -> str:
    return CONFIG.blur.__str__()

def process(image: Image.Image) -> Image.Image:
    return _blur(image, CONFIG.offset, CONFIG.limit, CONFIG.color, CONFIG.blur)

# https://code.activestate.com/recipes/474116-drop-shadows-with-pil/
def _blur(image: Image.Image, offset: tuple, limit: tuple, color: color, depth: int) -> Image.Image:
    """
    Add a gaussian blur drop shadow to an image.
    image       - The image to overlay on top of the shadow.
    """
    # Create the backdrop image -- a box in the background colour with a shadow on it.
    totalWidth = image.width + abs(offset[0]) + 2 * limit[0]
    totalHeight = image.height + abs(offset[1]) + 2 * limit[1]
    back = Image.new("RGBA", (totalWidth, totalHeight), (0, 0, 0, 0))
    # Place the shadow, taking into account the offset from the image
    shadowLeft = limit[0] + max(offset[0], 0)
    shadowTop = limit[1] + max(offset[1], 0)
    back.paste(color.tuple, [shadowLeft, shadowTop, shadowLeft + image.width, shadowTop + image.height])
    # Apply the filter to blur the edges of the shadow.  Since a small kernel
    # is used, the filter must be applied repeatedly to get a decent blur.
    for _ in range(depth):
        back = back.filter(ImageFilter.BLUR)
    # Paste the input image onto the shadow backdrop  
    imageLeft = limit[0] - min(offset[0], 0)
    imageTop = limit[1] - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))
    return back
