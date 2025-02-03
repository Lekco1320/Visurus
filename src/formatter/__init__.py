import util

from . import species_label
from . import photo_params
from . import mounting
from . import effects

def main():
    m = util.Menu('Lekco Visurus - 图像格式化', 'Q')
    m.add(util.Option('F', '物种标注…', species_label.main))
    m.add(util.Option('P', '拍摄参数…', photo_params.main))
    m.add(util.Option('M', '图像装裱…', mounting.main))
    m.add(util.Option('E', '图像效果…', effects.main))
    m.add(util.Option('Q', '返回'))
    m.run()
