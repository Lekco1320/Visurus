from util import *
from util import config
from util import menu

from PIL import Image
from PIL import ImageFilter

class style(config.config):
    FIELDS = [
        config.field('color',  color('#0000007F')),
        config.field('offset', (10, 10)),
        config.field('limit',  (8, 8)),
        config.field('blur',   5),
    ]
    
    DEFAULT = None
    
    @classmethod
    def default(cls) -> 'style':
        ret = style()
        ret.validate(style.FIELDS)
        return ret
    
    def __init__(self) -> None:
        super().__init__('')
        self.validate(style.FIELDS)
    
    def self_validate(self) -> bool:
        return super().validate(style.FIELDS)

    def set(self):
        style_main(self)

style.DEFAULT = style.default()

def style_main(style: style):
    m = menu.menu('Lekco Visurus - 阴影效果', 'Q')
    m.add(menu.option('C', '阴影颜色', lambda: set_color(style),  lambda: get_color(style)))
    m.add(menu.option('O', '阴影偏移', lambda: set_offset(style), lambda: get_offset(style)))
    m.add(menu.option('L', '范围限制', lambda: set_limit(style),  lambda: get_limit(style)))
    m.add(menu.option('B', '模糊程度', lambda: set_blur(style),   lambda: get_blur(style)))
    m.add(menu.option('Q', '返回'))
    m.run()

def set_color(style: style):
    style.color = color.input()

def get_color(style: style) -> str:
    return style.color.hex

@errhandler
def set_offset(style: style):
    print_output('请输入偏移量 x,y :')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    style.offset = (ans[0], ans[1])

def get_offset(style: style) -> str:
    return style.offset.__str__()

@errhandler
def set_limit(style: style):
    print_output('请输入范围限制 x,y:')
    ans = list(map(int, get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'错误的坐标分量数 \'{len(ans)}\'.')
    style.limit = (ans[0], ans[1])

def get_limit(style: style) -> str:
    return style.limit.__str__()

@errhandler
def set_blur(style: style):
    print_output('请输入模糊程度(>=0):')
    ans = int(get_input())
    if ans < 0:
        raise ValueError(f'模糊程度 \'{ans}\' 无效.')
    style.blur = ans

def get_blur(style: style) -> str:
    return style.blur.__str__()

def process(style: style, image: Image.Image) -> Image.Image:
    return _blur(image, style.offset, style.limit, style.color, style.blur)

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
