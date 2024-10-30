import os
import sys
import ast
import shutil
import platform
import resources

from util import *
from util import menu
from pathlib import Path

from .info import info

CONFIG_FILE: Path = None

infos: list[info] = []
has_inited: bool  = False
Config: dict[str, wrapper] = {}

def main():
    init()
    
    m = menu.menu('Lekco Visurus - 首选项', 'Q')
    m.add(menu.splitter('- 类别 -'))
    category, char = None, 65
    for info in infos:
        if info.category != category:
            category = info.category
            m.add(menu.option(chr(char), f'{category}…', lambda _=category: category_main(_)))
            char += 1
    m.add(menu.splitter('- 常规 -'))
    m.add(menu.option('R', '恢复默认值', reset))
    m.add(menu.option('Q', '返回'))
    m.run()

def reset():
    default()
    print_success('首选项已恢复至默认值.')

def category_main(category: str):
    m = menu.menu(f'Lekco Visurus - {category}', 'Q')
    m.add(menu.splitter('- 默认值 -'))
    all = [i for i in infos if i.category == category]
    for info in all:
        m.add(menu.option(info.menukey, info.name, info.set, info.get))
    m.add(menu.splitter('- 常规 -'))
    m.add(menu.option('Q', '返回'))
    m.run()
    save()

def init():
    global has_inited, infos
    if has_inited:
        return
    
    from util import output
    from util import stitching
    from format import species_label
    from format import photo_params
    from format import shadow
    from format import round_corner
    from watermark import style as watermark
    
    infos = [
        info('导出设置', '导出路径',        'output.ddir', 'A1', output.d_main, output.d_value),
        info('导出设置', '导出格式',        'output.fformat', 'A2', output.f_main, output.f_value),
        info('物种标注', '图像尺寸',        'species_label.size', 'B1', species_label.s_main, species_label.s_value),
        info('物种标注', '图像阴影',        'species_label.enshadow', 'B2', species_label.e_main, species_label.e_value),
        info('物种标注', '图像圆角',        'species_label.encorner', 'B3', species_label.r_main, species_label.r_value),
        info('物种标注', '图像水印',        'species_label.enwatermark', 'B4', species_label.a_main, species_label.a_value),
        info('拍摄参数', '图像尺寸',        'photo_params.size', 'C1', photo_params.s_main, photo_params.s_value),
        info('拍摄参数', '图像阴影',        'photo_params.enshadow', 'C2', photo_params.n_main, photo_params.n_value),
        info('拍摄参数', '图像水印',        'photo_params.enwatermark', 'C3', photo_params.w_main, photo_params.w_value),
        info('拍摄参数', '排版样式',        'photo_params.typeset', 'C4', photo_params.p_main, photo_params.p_value),
        info('拍摄参数', '底部双侧标注参数', 'photo_params.bottom_side', 'C5', photo_params.bottom_side_main),
        info('拍摄参数', '底部中央标注参数', 'photo_params.bottom_center', 'C6', photo_params.bottom_center_main),
        info('拍摄参数', '背景模糊标注参数', 'photo_params.back_blur', 'C7', photo_params.blur_main),
        info('阴影效果', '阴影颜色',        'shadow.color', 'D1', shadow.set_color, shadow.get_color),
        info('阴影效果', '阴影偏移',        'shadow.offset', 'D2', shadow.set_offset, shadow.get_offset),
        info('阴影效果', '模糊程度',        'shadow.blur', 'D3', shadow.set_blur, shadow.get_blur),
        info('阴影效果', '范围限制',        'shadow.limit', 'D4', shadow.set_limit, shadow.get_limit),
        info('圆角效果', '圆角半径',        'round_corner.radius', 'E', round_corner.set_radius, round_corner.get_radius),
        info('图像拼接', '拼接方向',        'stitching.direction', 'F1', stitching.d_main, stitching.d_value),
        info('图像拼接', '裁切模式',        'stitching.clip', 'F2', stitching.l_main, stitching.l_value),
        info('图像拼接', '垂直方向对齐模式', 'stitching.halign', 'F3', stitching.ah_main, stitching.a_value),
        info('图像拼接', '水平方向对齐模式', 'stitching.valign', 'F4', stitching.av_main, stitching.a_value),
        info('图像拼接', '水平方向对齐模式', 'stitching.spacing', 'F5', stitching.set_spacing, stitching.get_spacing),
        info('图像拼接', '背景颜色',        'stitching.background', 'F6', stitching.set_background, stitching.get_background),
        info('水印样式', '水印内容',        'watermark.content', 'G1', watermark.w_main, watermark.w_value),
        info('水印样式', '水印字体',        'watermark.font', 'G2', watermark.f_main, watermark.f_value),
        info('水印样式', '字体颜色',        'watermark.color', 'G3', watermark.set_color, watermark.get_color),
        info('水印样式', '文字内容',        'watermark.text', 'G4', watermark.set_text, watermark.get_text),
        info('水印样式', '图片源',          'watermark.psource', 'G5', watermark.set_psource, watermark.get_psource),
        info('水印样式', '不透明度',        'watermark.opacity', 'G6', watermark.set_opacity, watermark.get_opacity),
        info('水印样式', '对齐方式',        'watermark.aligns', 'G7', watermark.a_main, watermark.a_value),
        info('水印样式', '缩放方式',        'watermark.scale', 'G8', watermark.z_main, watermark.z_value),
        info('水印样式', '水印位置',        'watermark.position', 'G9', watermark.p_main, watermark.p_value),
        info('水印样式', '位置偏移',        'watermark.offset', 'GA', watermark.set_offset, watermark.get_offset),
    ]
    
    has_inited = True

def check_current_config(current_folder: str):
    global CONFIG_FILE
    current_config = Path(current_folder) / 'config.ini'
    if not os.path.isfile(current_config):
        if CONFIG_FILE == None:
            config.default()
            config.save()
        return
    app_config = CONFIG_FILE
    CONFIG_FILE = current_config
    if not app_config.exists():
        shutil.copy(CONFIG_FILE, app_config)

def check_app_config():
    global CONFIG_FILE
    system = platform.system()
    if system == "Windows":
        app_config = Path(os.getenv('APPDATA')) / "Lekco" / "visurus" / 'config.ini'
    elif system in ["Linux", "Darwin"]:
        app_config = Path.home() / ".config" / "Lekco" / "visurus" / 'config.ini'
    CONFIG_FILE = app_config

def check():
    check_app_config()
    check_current_config(os.path.dirname(sys.argv[0]))

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
        'watermark.font'             : wrapper(resources.font.TIMES_REGULAR),
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

def eval(line: str) -> tuple | None:
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
    global Config
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        for line in file:
            ret = eval(line)
            if ret != None:
                Config[ret[0]] = wrapper(ret[1])

def to_str(pair: tuple) -> str:
    value = f'R\'{pair[1].data}\'' if isinstance(pair[1].data, str) else pair[1].data
    return f'{pair[0]} = {value}\n'

def save():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        for pair in Config.items():
            file.write(to_str(pair))

check()
default()
read()
