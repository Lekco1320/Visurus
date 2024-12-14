import util
import os
import sys
import shutil

from . import appdir

from enum    import Enum
from pathlib import Path

RESOURCE_FOLDER: Path = None

_FONT_ANNOTATIONS = {
    'PUHUI_LIGHT'   : '阿里巴巴普惠体-Light',
    'PUHUI_REGULAR' : '阿里巴巴普惠体-Regular',
    'PUHUI_BOLD'    : '阿里巴巴普惠体-Bold',
    'SONGTI_BOLD'   : '思源宋体-Bold',
    'TIMES_REGULAR' : 'Times New Roman',
    'TIMES_BOLD'    : 'Times New Roman-Bold',
    'TIMES_ITALIC'  : 'Times New Roman-Italic',
    'TIMES_BITALIC' : 'Times New Roman-Bold Italic',
}

class font(Enum):
    PUHUI_LIGHT   = 'font/AlibabaPuHuiTi-3-45-Light.otf'
    PUHUI_REGULAR = 'font/AlibabaPuHuiTi-3-55-Regular.otf'
    PUHUI_BOLD    = 'font/AlibabaPuHuiTi-3-85-Bold.otf'
    SONGTI_BOLD   = 'font/SourceHanSerifCN-Bold.otf'
    TIMES_REGULAR = 'font/times.ttf'
    TIMES_BOLD    = 'font/timesbd.ttf'
    TIMES_ITALIC  = 'font/timesi.ttf'
    TIMES_BITALIC = 'font/timesbi.ttf'
    
    def __str__(self) -> str:
        return _FONT_ANNOTATIONS[self.name]

class icon(Enum):
    LOCATION = 'icon/location.png'
    MALE     = 'icon/male.png'
    FEMALE   = 'icon/female.png'

def check_app_resource():
    global RESOURCE_FOLDER
    RESOURCE_FOLDER = appdir.APPDIR / 'resources'

def check_current_resource(current_folder: str):
    global RESOURCE_FOLDER
    current_resource = Path(current_folder) / 'resources'
    if not os.path.isdir(current_resource):
        if RESOURCE_FOLDER == None:
            raise RuntimeError('找不到应用程序资源。')
        return
    app_resource = RESOURCE_FOLDER
    RESOURCE_FOLDER = current_resource
    if not app_resource.exists():
        shutil.copytree(RESOURCE_FOLDER, app_resource, ignore=ignore_files)

def ignore_files(src, names):
    ignore_dirs = { '__pycache__' }
    ignore_suffixes = { '.py', '.pyc' }
    ignored = set()
    
    for name in names:
        full_path = os.path.join(src, name)
        if os.path.isdir(full_path) and name in ignore_dirs:
            ignored.add(name)
        elif os.path.isfile(full_path) and os.path.splitext(name)[1] in ignore_suffixes:
            ignored.add(name)
    
    return ignored

def check():
    check_app_resource()
    check_current_resource(os.path.dirname(sys.argv[0]))

def get(key: font | icon | Path) -> str:
    if isinstance(key, font) or isinstance(key, icon):
        return str(Path.joinpath(RESOURCE_FOLDER, key.value))
    if isinstance(key, Path):
        return str(key)
    raise ValueError(f'Unsupported resource type \'{type(key)}\'')

def font_main(origin: font | Path) -> font | Path:
    ret = util.Wrapper(origin)
    m = util.Menu('Lekco Visurus - 字体设置')
    m.add(util.Option('I', '选择内置字体…', lambda: select_internal_font(ret)))
    m.add(util.Option('D', '选择字体文件…', lambda: select_font(ret)))
    m.run()
    return ret.data

def select_internal_font(value: util.Wrapper):
    m = util.Menu('Lekco Visurus - 选择字体')
    m.add(util.Option('A', '阿里巴巴普惠体-Light',         lambda: value.set(font.PUHUI_LIGHT)))
    m.add(util.Option('B', '阿里巴巴普惠体-Regular',       lambda: value.set(font.PUHUI_REGULAR)))
    m.add(util.Option('C', '阿里巴巴普惠体-Bold',          lambda: value.set(font.PUHUI_BOLD)))
    m.add(util.Option('D', '思源宋体-Bold',               lambda: value.set(font.SONGTI_BOLD)))
    m.add(util.Option('E', 'Times New Roman',             lambda: value.set(font.TIMES_REGULAR)))
    m.add(util.Option('F', 'Times New Roman-Bold',        lambda: value.set(font.TIMES_BOLD)))
    m.add(util.Option('G', 'Times New Roman-Italic',      lambda: value.set(font.TIMES_ITALIC)))
    m.add(util.Option('H', 'Times New Roman-Bold Italic', lambda: value.set(font.TIMES_BITALIC)))
    m.run()

@util.errhandler
def select_font(value: util.Wrapper):
    util.print_output('已启动文件选择器.')
    from tkinter import filedialog
    fonttypes = [('字体文件', '*.otf;*.ttf')]
    fontfile  = filedialog.askopenfilename(title='选择字体', initialdir='/', filetypes=fonttypes)
    ret = Path(fontfile)
    if not ret.exists():
        raise ValueError('非法的字体文件.')
    value.data = ret

check()
