from util import *
from util import config
from util import menu

from PIL import Image
from PIL import ImageDraw

class style(config.config):
    FIELDS = [
        config.field('radius', 10),
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
    m = menu.menu('Lekco Visurus - 圆角效果', 'Q')
    m.add(menu.option('R', '圆角半径', lambda: set_radius(style), lambda: get_radius(style)))
    m.add(menu.option('Q', '返回'))

@errhandler
def set_radius(style: style):
    print_output('请输入圆角半径:')
    value = int(get_input())
    if value < 0:
        raise ValueError(f'非法的圆角半径值 {value}')
    style.radius = value

def get_radius(style: style) -> str:
    return f'{style.radius}px'

# https://www.pyget.cn/p/185266
def process(style: style, image: Image.Image) -> Image.Image: 
    radii = style.radius
    circle = Image.new('L', (radii * 2, radii * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)

    w, h = image.size

    alpha = Image.new('L', image.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))

    image.putalpha(alpha)
    return image
