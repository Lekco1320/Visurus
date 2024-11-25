from util import menu
from . import species_label
from . import photo_params
from . import shadow
from . import round_corner
from . import mounting

def main():
    m = menu.menu('Lekco Visurus - 图像格式化', 'Q')
    m.add(menu.option('F', '物种标注…', species_label.main))
    m.add(menu.option('P', '拍摄参数…', photo_params.main))
    m.add(menu.option('S', '添加阴影…', shadow.main))
    m.add(menu.option('R', '添加圆角…', round_corner.main))
    m.add(menu.option('M', '图像装裱…', mounting.main))
    m.add(menu.option('Q', '返回'))
    m.run()
