import util
import platform

from . import appconfig
from . import resources
from . import console

def main():
    m = util.Menu('Lekco Visurus - 设置', 'Q')
    m.add(util.Display(display))
    m.add(util.Option('R', '恢复默认设置', restore_config))
    m.add(util.Option('C', '清除输入记录', clear_input_history))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_kv('操作系统', util.fomit_str('* 操作系统: {} *', platform.platform()))
    util.print_kv('资源路径', util.fomit_path('* 资源目录: {} *', str(resources.RESOURCE_FOLDER)))
    util.print_splitter()

@util.errhandler
def restore_config():
    appconfig.clear()
    util.print_success('已恢复至默认设置，重启程序以生效.')
    exit()

@util.errhandler
def clear_input_history():
    console.clear_history()
    util.print_success('输入记录已清除完毕.')
