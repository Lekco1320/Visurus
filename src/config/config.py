import os
import ast
import resource.main as main

from util.wrapper import wrapper

Config : dict[str, wrapper] = {}

def default():
    global Config
    Config = {
        'output.ddir'                : wrapper(os.path.join(os.path.expanduser('~'), 'Desktop')),
        'output.fformat'             : wrapper('*.PNG'),
        'species_label.size'         : wrapper('2K'),
        'species_label.enshadow'     : wrapper(False),
        'species_label.encorner'     : wrapper(False),
        'species_label.enwatermark'  : wrapper(False),
        'shadow.color'               : wrapper('#0000007F'),
        'shadow.offset'              : wrapper((10, 10)),
        'shadow.blur'                : wrapper(5),
        'shadow.limit'               : wrapper((8, 8)),
        'watermark.content'          : wrapper('文字'),
        'watermark.font'             : wrapper(main.font.TIMES_REGULAR),
        'watermark.color'            : wrapper('#0000007F'),
        'watermark.text'             : wrapper('Lekco'),
        'watermark.psource'          : wrapper('无'),
        'watermark.opacity'          : wrapper(100),
        'watermark.aligns'           : wrapper(['居中对齐', '底部对齐']),
        'watermark.scale'            : wrapper(['固定尺寸', ('*', '*')]),
        'watermark.position'         : wrapper('图像下中央'),
        'watermark.offset'           : wrapper((0, 0)),
        'photo_params.size'          : wrapper('2K'),
        'photo_params.enshadow'      : wrapper(False),
        'photo_params.enwatermark'   : wrapper(False),
        'photo_params.typeset'       : wrapper('底部双侧标注'),
        'photo_params.bottom_side'   : wrapper(['{B}', '{D}', '{L} {F} {E} {I}', '{T}']),
        'photo_params.bottom_center' : wrapper(['Shot on ', '{D} ', '{M} ', '{L} {F} {E} {I}']),
        'photo_params.back_blur'     : wrapper(['{D}', '{L} {F} {E} {I}', 50, 0.45]),
        'round_corner.radius'        : wrapper(10),
        'stitching.direction'        : wrapper('垂直方向'),
        'stitching.clip'             : wrapper('扩展至最长边'),
        'stitching.halign'           : wrapper('左对齐'),
        'stitching.valign'           : wrapper('顶部对齐'),
        'stitching.spacing'          : wrapper(0),
        'stitching.background'       : wrapper('#FFFFFFFF'),
    }

def eval(line : str) -> tuple | None:
    key = ''
    value = ''
    meet_equal = False
    for c in line:
        if c == '=':
            meet_equal = True
        elif not meet_equal:
            key += c
        else:
            value += c
    value = value.strip()
    if meet_equal:
        return (key.strip(), ast.literal_eval(value))

def read():
    if not os.path.exists('./config.ini'):
        save()
        return
    
    global Config
    with open('./config.ini', 'r', encoding='utf-8') as file:
        for line in file:
            ret = eval(line)
            if ret != None:
                Config[ret[0]] = wrapper(ret[1])

def to_str(pair : tuple) -> str:
    value = f'R\'{pair[1].data}\'' if isinstance(pair[1].data, str) else pair[1].data
    return f'{pair[0]} = {value}\n'

def save():
    with open('./config.ini', 'w', encoding='utf-8') as file:
        for pair in Config.items():
            file.write(to_str(pair))

default()
read()
