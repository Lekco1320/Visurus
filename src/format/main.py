from util import menu

from . import species_label
from . import photo_params
from . import mounting
from . import effect

def main_menu():
    m = menu.menu('Lekco Visurus - 图像格式化', 'Q')
    m.add(menu.option('F', '物种标注…', species_label.main))
    m.add(menu.option('P', '拍摄参数…', photo_params.main))
    m.add(menu.option('M', '图像装裱…', mounting.main))
    m.add(menu.option('E', '图像效果…', effect.main))
    m.add(menu.option('Q', '返回'))
    m.run()
