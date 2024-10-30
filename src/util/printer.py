import time
import unicodedata

from util import ansi
from typing import overload, Union

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
def text_width(text: ansi.ansi_str) -> int:
    ...

@overload
def text_width(text: ansi.ansi_stream) -> int:
    ...

def text_width(text: Union[str, ansi.ansi_str, ansi.ansi_stream]) -> int:
    width = 0
    for c in text:
        width += FULL_CHAR_WIDTH if is_full_width_char(c) else 1
    return width

@overload
def wrap_text(text: str, width: int) -> str:
    ...

@overload
def wrap_text(text: ansi.ansi_str, width: int) -> ansi.ansi_str:
    ...

@overload
def wrap_text(text: ansi.ansi_stream, width: int) -> ansi.ansi_stream:
    ...

def wrap_text(text: Union[str, ansi.ansi_str, ansi.ansi_stream], width: int) \
    -> Union[str, ansi.ansi_str, ansi.ansi_stream]:
    if width <= 0:
        raise ValueError("Width must be greater than 0.")
    
    if isinstance(text, str):
        return _wrap_text_str(text, width)
    if isinstance(text, ansi.ansi_str):
        text = text.copy()
        text.str = _wrap_text_str(text.str, width)
        return text
    if isinstance(text, ansi.ansi_stream):
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

def _wrap_text_ansi_stream(stream: ansi.ansi_stream, width: int) -> ansi.ansi_stream:
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

    return ansi.ansi_stream(astrs)

def print_wrap(text: Union[str, ansi.ansi_str, ansi.ansi_stream]):
    print(wrap_text(text, SPLITER_LENGTH))

@overload
def center(text: str, width: int) -> str:
    ...

@overload
def center(text: ansi.ansi_str, width: int) -> ansi.ansi_str:
    ...

def center(text: str | ansi.ansi_str, width: int):
    length = text_width(text)
    left   = int((width - 2 - length) / 2)
    right  = width - 2 - length - left
    return '*' + ' ' * left + text + ' ' * right + '*'

def print_center(text: str | ansi.ansi_str):
    print(center(text, SPLITER_LENGTH))

SPLITER_LENGTH = 47

def print_spliter():
    print('*' * SPLITER_LENGTH)

def clear_line():
    print(f'{ansi.ansi_format.CONTROL_CODE}2K', end='')
    print(f'{ansi.ansi_format.format.CONTROL_CODE}H',  end='')

def clear_screen():
    print(f'{ansi.ansi_format.CONTROL_CODE}2J',   end='')
    print(f'{ansi.ansi_format.CONTROL_CODE}1;1H', end='')

def up_line():
    print('\033[1A', end='')

def left(text: str | ansi.ansi_str | ansi.ansi_stream):
    length = text_width(text)
    right  = SPLITER_LENGTH - 3 - length
    return '* ' + text + ' ' * right + '*'

def print_left(text: str | ansi.ansi_str | ansi.ansi_stream):
    print(left(text))

def print_subtitle(text: str | ansi.ansi_str | ansi.ansi_stream):
    print_spliter()
    print_center(ansi.ansi_str(text, ansi.FORMAT_TITLE))

def print_title(text: str | ansi.ansi_str | ansi.ansi_stream):
    print_subtitle(text)
    print_spliter()

def kv(key: str, value: str = None):
    fstr = ansi.ansi_str('', ansi.FORMAT_VALUE)
    main = f'{key}'
    if value != None:
        main += ': '
        fstr.str = value
    return main + fstr

def print_kv(key: str, value: str = None):
    return print_left(kv(key, value))

def print_option(key: str | ansi.ansi_str, text: str | ansi.ansi_str, value: str = None):
    kv_str = kv(text, value)
    print_left(ansi.ansi_str(f'{key}', ansi.FORMAT_OPTION) + ' | ' + kv_str)

def get_input(text: str | ansi.ansi_str = '') -> str:
    return input(f'< {text}')

def print_output(text: str | ansi.ansi_str):
    print(f'> {text}')

def print_ps(text: str):
    print_output(ansi.ansi_str(text, ansi.FORMAT_PS))

def wait(t: float = 1.5):
    time.sleep(t)

def print_error(ex: str):
    print_output(ansi.ansi_str('[错误] ' + ex, ansi.FORMAT_ERROR))
    wait()

def print_success(text: str):
    print_output(ansi.ansi_str(text, ansi.FORMAT_SUCCESS))
    wait(1.0)
