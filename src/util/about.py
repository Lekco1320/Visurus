from util import ansi
from util import menu
from util import *

def main():
    m = menu.menu('Lekco Visurus - 关于', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    logo   = lambda text: ansi.ansi_str(text, ansi.ansi_format(foreground=ansi.color.WHITE, background=ansi.color.GREEN))
    glow   = lambda text: ansi.ansi_str(text, ansi.ansi_format(foreground=ansi.color.GREEN))
    italic = lambda text: ansi.ansi_str(text, ansi.ansi_format(ansi.style.ITALIC | ansi.style.BOLD, foreground=ansi.color.WHITE))
    print_left('')
    print_center(logo("Lekco") + glow("  _                          "))
    print_center(glow(R"__   ___)___ _   _ _ __ _   _ ___ "))
    print_center(glow(R"\ \ / / / __| | | | '__| | | / __|"))
    print_center(glow(R" \ V /| \__ \ |_| | |  | |_| \__ \ "))
    print_center(glow(R"  \_/ |_|___/\__,_|_|   \__,_|___/"))
    print_left('')
    print_left(italic('Visurus') + ' is the future participle form of')
    print_left('the Latin verb ' + italic('videō') + ' (to see).')
    print_spliter()
    print_kv('版本', '1.0.1.158')
    print_kv('作者', 'Lukas Zhang')
    print_kv('邮箱', 'Lekco_1320@qq.com')
    print_kv('仓库', 'https://github.com/Lekco1320/visurus')
    print_center('Available under the Apache-2.0 License.')
    print_spliter()
