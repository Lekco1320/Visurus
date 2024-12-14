# Lekco Visurus
# Lukaß Zhang, 2024/05/23

import util
import sys
import formatter
import watermark

from app import about
from app import settings
from app import stitcher
from app import workspace

@util.errhandler
def main():
    m = util.Menu('Lekco Visurus', 'Q')
    m.add(util.Option('F', '图像格式化…', formatter.main))
    m.add(util.Option('S', '图像拼接…',   stitcher.main))
    m.add(util.Option('T', '添加水印…',   watermark.main_menu))
    m.add(util.Option('W', '工作区…',     workspace.main))
    m.add(util.Option('O', '设置…',       settings.main))
    m.add(util.Option('A', '关于',        about.main))
    m.add(util.Option('Q', '退出'))
    m.run()

def parse_args():
    for arg in sys.argv[1:]:
        workspace.input_file_or_folder(arg)

if __name__ == '__main__':
    parse_args()
    main()
