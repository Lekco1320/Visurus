from util import *
from util import menu
from util import color
from util import output
from util import workspace

from PIL import Image
from PIL import ImageFilter

from config import Config

targets = []
shadow  = wrapper(Config['shadow.color'])
offset  = wrapper(Config['shadow.offset'])
blur    = wrapper(Config['shadow.blur'])
limit   = wrapper(Config['shadow.limit'])

def main():
    targets.clear()
    
    m = menu.menu('Lekco Visurus - 添加阴影', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('S', '阴影效果…', style_main))
    m.add(menu.option('O', '执行导出…', execute))
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
    m.add(menu.option('C', '阴影颜色', lambda: set_color(shadow),  lambda: get_color(shadow)))
    m.add(menu.option('O', '阴影偏移', lambda: set_offset(offset), lambda: get_offset(offset)))
    m.add(menu.option('L', '范围限制', lambda: set_limit(limit),   lambda: get_limit(limit)))
    m.add(menu.option('B', '模糊程度', lambda: set_blur(blur),     lambda: get_blur(blur)))
    m.add(menu.option('Q', '返回'))
    m.run()

def set_color(shadow: wrapper):
    shadow.data = color.input().hex

def get_color(shadow: wrapper) -> str:
    return shadow.data

@errhandler
def set_offset(offset: wrapper):
    print_output('请输入偏移量 x,y :')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    offset.data = (ans[0], ans[1])

def get_offset(offset: wrapper) -> str:
    return offset.data.__str__()

@errhandler
def set_limit(limit: wrapper):
    print_output('请输入范围限制 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    limit.data = (ans[0], ans[1])

def get_limit(limit: wrapper) -> str:
    return limit.data.__str__()

@errhandler
def set_blur(blur: wrapper):
    print_output('请输入模糊程度(>=0):')
    ans = int(get_input())
    if ans < 0:
        raise ValueError(f'模糊程度 \'{ans}\' 无效.')
    blur.data = ans

def get_blur(blur: wrapper) -> str:
    return blur.data.__str__()

def process(image: Image.Image) -> Image.Image:
    return _blur(image, (offset.data[0], offset.data[1]), (limit.data[0], limit.data[1]), color(shadow.data), blur.data)

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
