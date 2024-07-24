import util.ansi as ansi
import util.menu as menu
import util.printer as prt

def main():
    m = menu.menu('Lekco Visurus - 关于', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    logo   = lambda text: ansi.fstr(text, ansi.format(foreground=ansi.color.WHITE, background=ansi.color.GREEN))
    glow   = lambda text: ansi.fstr(text, ansi.format(foreground=ansi.color.GREEN))
    italic = lambda text: ansi.fstr(text, ansi.format(ansi.style.ITALIC | ansi.style.BOLD, foreground=ansi.color.WHITE))
    prt.left('')
    prt.center(logo("Lekco") + glow("  _                          "))
    prt.center(glow(R"__   ___)___ _   _ _ __ _   _ ___ "))
    prt.center(glow(R"\ \ / / / __| | | | '__| | | / __|"))
    prt.center(glow(R" \ V /| \__ \ |_| | |  | |_| \__ \ "))
    prt.center(glow(R"  \_/ |_|___/\__,_|_|   \__,_|___/"))
    prt.left('')
    prt.left(italic('Visurus') + ' is the future participle form of')
    prt.left('the Latin verb ' + italic('videō') + ' (to see).')
    prt.split()
    prt.pkv('版本', '1.0.0.62')
    prt.pkv('作者', 'Lukas Zhang')
    prt.pkv('邮箱', 'Lekco_1320@qq.com')
    prt.pkv('仓库', 'https://github.com/Lekco1320/visurus')
    prt.center('Available under the Apache-2.0 License.')
    prt.split()
