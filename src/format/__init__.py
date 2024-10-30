from util   import menu
from format import species_label
from format import photo_params
from format import shadow
from format import round_corner

def main():
    m = menu.menu('Lekco Visurus - 图像格式化', 'Q')
    m.add(menu.option('F', '物种标注…', species_label.main))
    m.add(menu.option('P', '拍摄参数…', photo_params.main))
    m.add(menu.option('S', '添加阴影…', shadow.main))
    m.add(menu.option('R', '添加圆角…', round_corner.main))
    m.add(menu.option('Q', '返回'))
    m.run()
