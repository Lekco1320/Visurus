from util import *
from util import menu
from util import output
from util import workspace

from PIL import Image
from PIL import ImageDraw

from config import Config

targets = []
radius  = wrapper(Config['round_corner.radius'])

def main():
    targets.clear()
    
    m = menu.menu('Lekco Visurus - 圆角效果', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('R', '圆角半径', lambda: set_radius(radius), lambda: get_radius(radius)))
    m.add(menu.option('O', '执行导出…', execute))
    m.add(menu.option('Q', '返回'))
    m.run()

def radius_main():
    set_radius(radius)

def radius_value() -> str:
    return get_radius(radius)

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
def set_radius(radius: wrapper):
    print_output('请输入圆角半径:')
    value = int(get_input())
    if value < 0:
        raise ValueError(f'非法的圆角半径值 {value}')
    radius.data = value

def get_radius(radius: wrapper) -> str:
    return f'{radius.data}px'

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

# https://www.pyget.cn/p/185266
def process(image: Image.Image) -> Image.Image: 
    radii = radius.data
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
