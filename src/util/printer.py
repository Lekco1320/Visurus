import builtins
import util.ansi as ansi
import time

SPLITER_LENGTH = 47

def clrl():
    ansi.clear_line()

def clrs():
    ansi.clear_all()

def split():
    print('*' * SPLITER_LENGTH)

def chinese_count(text : str | ansi.fstr | ansi.fstrs):
    count = 0
    for char in text:
        if '\u4e00' <= char <= '\u9fa5':
            count += 1
    return count

def left(text : str | ansi.fstr | ansi.fstrs):
    length = len(text) + chinese_count(text)
    right  = SPLITER_LENGTH - 3 - length
    print('* ' + text + ' ' * right + '*')

def center(text : str | ansi.fstr | ansi.fstrs):
    length = len(text) + chinese_count(text)
    left   = int((SPLITER_LENGTH - 2 - length) / 2)
    right  = SPLITER_LENGTH - 2 - length - left
    print('*' + ' ' * left + text + ' ' * right + '*')

def title(text : str | ansi.fstr | ansi.fstrs):
    split()
    center(ansi.fstr(text, ansi.format(ansi.style.BOLD, ansi.color.WHITE)))

def stitle(text : str | ansi.fstr | ansi.fstrs):
    title(text)
    split()

def kv(key: str, value : str = None):
    fstr = ansi.fstr('', ansi.format(foreground=ansi.color.CYAN))
    main = f'{key}'
    if value != None:
        main += ': '
        fstr._text = value
    return main + fstr

def pkv(key: str, value : str = None):
    left(kv(key, value))

def option(key : str | ansi.fstr, text : str | ansi.fstr, value : str = None):
    kv_str = kv(text, value)
    left(ansi.fstr(f'{key}', ansi.format(foreground=ansi.color.YELLOW)) + ' | ' + kv_str)

def input(text : str | ansi.fstr = '') -> str:
    return builtins.input(f'< {text}')

def output(text : str | ansi.fstr):
    print(f'> {text}')

def ps(text : str):
    output(ansi.fstr(text, ansi.format(style=ansi.style.FAINT)))

def wait(t : float = 1.5):
    time.sleep(t)

def error(ex : str):
    output(ansi.fstr('[错误] ' + ex, ansi.format(foreground=ansi.color.RED)))
    wait()

def success(text : str):
    output(ansi.fstr(text, ansi.format(foreground=ansi.color.GREEN)))
    wait(1.0)

def change_length(value : int):
    global SPLITER_LENGTH
    SPLITER_LENGTH = value
