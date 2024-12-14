import util

VERSION = util.Version(1, 0, 1, 196)

def main():
    m = util.Menu('Lekco Visurus - 关于', 'Q')
    m.add(util.Display(display))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    logo   = lambda text: util.AnsiStr(text, util.AnsiFormat(foreground=util.AnsiColor.WHITE, background=util.AnsiColor.GREEN))
    glow   = lambda text: util.AnsiStr(text, util.AnsiFormat(foreground=util.AnsiColor.GREEN))
    italic = lambda text: util.AnsiStr(text, util.AnsiFormat(util.AnsiStyle.ITALIC | util.AnsiStyle.BOLD, foreground=util.AnsiColor.WHITE))
    util.print_left('')
    util.print_center(logo("Lekco") + glow("  _                          "))
    util.print_center(glow(R"__   ___)___ _   _ _ __ _   _ ___ "))
    util.print_center(glow(R"\ \ / / / __| | | | '__| | | / __|"))
    util.print_center(glow(R" \ V /| \__ \ |_| | |  | |_| \__ \ "))
    util.print_center(glow(R"  \_/ |_|___/\__,_|_|   \__,_|___/"))
    util.print_left('')
    util.print_left(italic('Visurus') + ' is the future participle form of')
    util.print_left('the Latin verb ' + italic('videō') + ' (to see).')
    util.print_splitter()
    util.print_kv('版本', str(VERSION))
    util.print_kv('作者', 'Lukaß Zhang')
    util.print_kv('邮箱', 'Lekco_1320@qq.com')
    util.print_kv('仓库', 'https://github.com/Lekco1320/Visurus')
    util.print_center('Available under the Apache-2.0 License.')
    util.print_splitter()
