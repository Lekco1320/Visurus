# Lekco Visurus. 2024.5.23.

import sys
import util.menu as menu
import util.about as about
import util.stitching as stitching
import util.workspace as workspace
import format.main as format
import config.main as config
import watermark.main as watermark

from util.errhandler import errhandler

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
