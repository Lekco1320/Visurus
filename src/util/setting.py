from .        import menu
from .        import config
from .        import errhandler
from .printer import *
from .history import clear_history

def main():
    m = menu.menu('Lekco Visurus - 设置', 'Q')
    m.add(menu.option('R', '恢复默认设置', restore_config))
    m.add(menu.option('C', '清除输入记录', clear_input_history))
    m.add(menu.option('Q', '返回'))
    m.run()

@errhandler
def restore_config():
    config.clear()
    print_success('已恢复至默认设置，重启程序以生效.')
    exit()

@errhandler
def clear_input_history():
    clear_history()
    print_success('输入记录已清除完毕.')
    wait()
