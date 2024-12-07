import os
import time
import unicodedata

from .ansi  import *
from typing import overload

FULL_CHAR_WIDTH = 2

def set_full_char_width(width: int) -> None:
    global FULL_CHAR_WIDTH
    FULL_CHAR_WIDTH = width

def is_full_width_char(char: str) -> bool:
    if len(char) != 1:
        raise ValueError("Input must be a single character.")
    width = unicodedata.east_asian_width(char)
    return width in ('F', 'W')

@overload
def text_width(text: str) -> int:
    ...

@overload
def text_width(text: ansi_str) -> int:
    ...

@overload
def text_width(text: ansi_stream) -> int:
    ...

def text_width(text: strOrStream) -> int:
    width = 0
    for c in text:
        width += FULL_CHAR_WIDTH if is_full_width_char(c) else 1
    return width

@overload
def wrap_text(text: str, width: int) -> str:
    ...

@overload
def wrap_text(text: ansi_str, width: int) -> ansi_str:
    ...

@overload
def wrap_text(text: ansi_stream, width: int) -> ansi_stream:
    ...

def wrap_text(text: strOrStream, width: int) -> strOrStream:
    if width <= 0:
        raise ValueError("Width must be greater than 0.")
    
    if isinstance(text, str):
        return _wrap_text_str(text, width)
    if isinstance(text, ansi_str):
        text = text.copy()
        text.str = _wrap_text_str(text.str, width)
        return text
    if isinstance(text, ansi_stream):
        return _wrap_text_ansi_stream(text, width)

def _wrap_cannot_break(char: str) -> bool:
    return char.islower() or char.isupper() or char in \
           [',', '.', '?', '!', ':', ';', '\'', '"', '(', ')',
            '，', '。', '？', '！', '：', '；', '‘', '’', '_',
            '“', '”', '（', '）']

def _wrap_end_index(text: str, width: int) -> int:
    w = 0
    for i in range(len(text)):
        w += FULL_CHAR_WIDTH if is_full_width_char(text[i]) else 1
        if w > width:
            return i
    return width

def _wrap_text_str(text: str, width: int, offset: int = 0) -> str:
    lines  = []
    rwidth = width - offset
    while text_width(text) > rwidth:
        canContinue = False
        for i in range(len(text[:rwidth])):
            if text[i] == '\n':
                lines.append(text[:i].rstrip())
                text        = text[i:].lstrip()
                rwidth      = width
                canContinue = True
                break
        if canContinue:
            continue
        
        break_index = index = _wrap_end_index(text, rwidth)
        if _wrap_cannot_break(text[index]) or text_width(text[:index]) > rwidth:
            while break_index > 1 and _wrap_cannot_break(text[break_index - 1]):
                break_index -= 1
        if break_index == 0 and text_width(text) > width:
            break_index = index
        lines.append(text[:break_index].rstrip())
        text   = text[break_index:].lstrip()
        rwidth = width
    
    lines.append(text)
    return '\n'.join(lines)

def _wrap_text_ansi_stream(stream: ansi_stream, width: int) -> ansi_stream:
    astrs  = []
    offset = 0
    for astr in stream._astrs:
        astr = astr.copy()
        astr.str = _wrap_text_str(astr.str, width, offset)
        astrs.append(astr)
        
        offset  = 0
        for char in reversed(''.join(s.str for s in astrs)):
            if char == '\n':
                break
            offset += 1

    return ansi_stream(astrs)

def print_wrap(text: strOrStream):
    print(wrap_text(text, SPLITER_LENGTH))

@overload
def center(text: str, width: int) -> str:
    ...

@overload
def center(text: ansi_str, width: int) -> ansi_str:
    ...

def center(text: strLike, width: int):
    length = text_width(text)
    left   = int((width - 2 - length) / 2)
    right  = width - 2 - length - left
    return '*' + ' ' * left + text + ' ' * right + '*'

def print_center(text: strLike):
    print(center(text, SPLITER_LENGTH))

SPLITER_LENGTH = 47

def print_spliter():
    print('*' * SPLITER_LENGTH)

def clear_line():
    print(f'{ansi_format.CONTROL_CODE}2K', end='')
    print(f'{ansi_format.format.CONTROL_CODE}H',  end='')

def clear_screen():
    print(f'{ansi_format.CONTROL_CODE}2J',   end='')
    print(f'{ansi_format.CONTROL_CODE}1;1H', end='')

def true_clear_screen(): 
    if os.name == 'posix':
        os.system('clear')
    else: 
        os.system('cls')

def up_line():
    print('\033[1A', end='')

def left(text: strOrStream):
    length = text_width(text)
    right  = SPLITER_LENGTH - 3 - length
    return '* ' + text + ' ' * right + '*'

def print_left(text: strOrStream):
    print(left(text))

def print_subtitle(text: strOrStream):
    print_spliter()
    print_center(ansi_str(text, FORMAT_TITLE))

def print_title(text: strOrStream):
    print_subtitle(text)
    print_spliter()

def kv(key: str, value: str = None):
    fstr = ansi_str('', FORMAT_VALUE)
    main = f'{key}'
    if value != None:
        main += ': '
        fstr.str = value
    return main + fstr

def print_kv(key: str, value: str = None):
    return print_left(kv(key, value))

def print_option(key: strLike, text: strLike, value: str = None):
    kv_str = kv(text, value)
    print_left(ansi_str(f'{key}', FORMAT_OPTION) + ' | ' + kv_str)

def get_input(text: strLike = '') -> str:
    return input(f'< {text}')

def print_output(text: strLike):
    print(f'> {text}')

def print_ps(text: str):
    print_output(ansi_str('* ' + text, FORMAT_PS))

def wait(t: float = 1.5):
    time.sleep(t)

def print_error(ex: str):
    print_output(ansi_str('[错误] ' + ex, FORMAT_ERROR))
    wait()

def print_success(text: str):
    print_output(ansi_str(text, FORMAT_SUCCESS))
    wait(1.0)

def compress_path(path: str, length: int) -> str:
    path = os.path.normpath(path)
    if text_width(path) <= length:
        return path
    
    parts = path.split(os.sep)
    ret   = path
    
    if len(parts) == 0:
        return path
    if len(parts) > 2: 
        ret = os.path.join(parts[0], os.sep, '...', parts[-1])
    if len(parts) == 2 or text_width(ret) > length:
        ret = os.path.join('...', parts[-1])
    if text_width(ret) <= length:
        return ret
    if len(parts[-1]) <= 3:
        return f'...{ret}'
    
    ret = parts[-1][3:]
    while text_width(ret) + 3 > length: 
        ret = ret[1:]
    return f'...{ret}'

def auto_compress_path(format_str: str, path: str) -> str:
    count       = format_str.count('{}')
    placeholder = format_str.replace('{}', '')
    length      = (SPLITER_LENGTH - text_width(placeholder)) / (count if count > 0 else count == 1)
    return compress_path(path, length)
