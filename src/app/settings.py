from .        import appconfig
from .        import resources
from .console import clear_history

from util         import menu
from util         import errhandler
from util.printer import *

def main():
    m = menu.menu('Lekco Visurus - 设置', 'Q')
    m.add(menu.display(display))
    m.add(menu.option('R', '恢复默认设置', restore_config))
    m.add(menu.option('C', '清除输入记录', clear_input_history))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    print_kv('资源路径', fomit_path('* 资源目录: {} *', str(resources.RESOURCE_FOLDER)))
    print_spliter()

@errhandler
def restore_config():
    appconfig.clear()
    print_success('已恢复至默认设置，重启程序以生效.')
    exit()

@errhandler
def clear_input_history():
    clear_history()
    print_success('输入记录已清除完毕.')
    wait()
