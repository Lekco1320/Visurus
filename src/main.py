# Lekco Visurus
# Lukaß Zhang, 2024/05/23

import sys
import formatter
import watermark

from util import *
from util import menu
from app import about
from app import settings
from app import stitcher
from app import workspace

@errhandler
def main():
    m = menu.menu('Lekco Visurus', 'Q')
    m.add(menu.option('F', '图像格式化…', formatter.main_menu))
    m.add(menu.option('S', '图像拼接…',   stitcher.main))
    m.add(menu.option('T', '添加水印…',   watermark.main_menu))
    m.add(menu.option('W', '工作区…',     workspace.main))
    m.add(menu.option('O', '设置…',       settings.main))
    m.add(menu.option('A', '关于',        about.main))
    m.add(menu.option('Q', '退出'))
    m.run()

def parse_args():
    for arg in sys.argv[1:]:
        workspace.input_file_or_folder(arg)

if __name__ == '__main__':
    parse_args()
    main()
