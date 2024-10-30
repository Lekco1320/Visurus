# Lekco Visurus. 2024.5.23.

import sys
import format
import watermark
import config

from util import *
from util import menu
from util import about
from util import stitching
from util import workspace

@errhandler
def main():
    m = menu.menu('Lekco Visurus', 'Q')
    m.add(menu.option('F', '图像格式化…', format.main))
    m.add(menu.option('S', '图像拼接…',   stitching.main))
    m.add(menu.option('T', '添加水印…',   watermark.main))
    m.add(menu.option('W', '工作区…',     workspace.main))
    m.add(menu.option('O', '首选项…',     config.main))
    m.add(menu.option('A', '关于',        about.main))
    m.add(menu.option('Q', '退出'))
    m.run()

def parse_args():
    for arg in sys.argv[1:]:
        workspace.input_file_or_folder(arg)

if __name__ == '__main__':
    parse_args()
    main()
