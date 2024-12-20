import util
import os
import sys
import shutil
import platform

from . import appdir

from enum            import Enum
from pathlib         import Path
from fontTools.ttLib import TTFont

RESOURCE_FOLDER: Path = None

_FONT_ANNOTATIONS = {
    'PUHUI_LIGHT'   : '阿里巴巴普惠体 Light',
    'PUHUI_REGULAR' : '阿里巴巴普惠体 Regular',
    'PUHUI_BOLD'    : '阿里巴巴普惠体 Bold',
    'SONGTI_BOLD'   : '思源宋体 Bold',
    'TIMES_REGULAR' : 'Times New Roman',
    'TIMES_BOLD'    : 'Times New Roman Bold',
    'TIMES_ITALIC'  : 'Times New Roman Italic',
    'TIMES_BITALIC' : 'Times New Roman Bold Italic',
}

class Font(Enum):
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

class Icon(Enum):
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

def get(key: Font | Icon | Path) -> str:
    if isinstance(key, Font) or isinstance(key, Icon):
        return str(Path.joinpath(RESOURCE_FOLDER, key.value))
    return str(key)

def font_name(key: Font | Path) -> str:
    if isinstance(key, Font):
        return str(key)
    basename = os.path.basename(key)
    return _get_font_name(key, basename)

def font_main(origin: Font | Path) -> Font | Path:
    ret = util.Wrapper(origin)
    m = util.Menu('Lekco Visurus - 字体设置')
    m.add(util.Option('I', '选择内置字体…', lambda: select_internal_font(ret)))
    m.add(util.Option('S', '选择系统字体…', lambda: select_system_font(ret)))
    m.add(util.Option('D', '选择字体文件…', lambda: select_font(ret)))
    m.add(util.Option('Q', '返回'))
    m.run()
    return ret.data

def select_internal_font(value: util.Wrapper):
    m = util.Menu('Lekco Visurus - 选择字体')
    m.add(util.Option('A', '阿里巴巴普惠体 Light',         lambda: value.set(Font.PUHUI_LIGHT)))
    m.add(util.Option('B', '阿里巴巴普惠体 Regular',       lambda: value.set(Font.PUHUI_REGULAR)))
    m.add(util.Option('C', '阿里巴巴普惠体 Bold',          lambda: value.set(Font.PUHUI_BOLD)))
    m.add(util.Option('D', '思源宋体 Bold',               lambda: value.set(Font.SONGTI_BOLD)))
    m.add(util.Option('E', 'Times New Roman',             lambda: value.set(Font.TIMES_REGULAR)))
    m.add(util.Option('F', 'Times New Roman Bold',        lambda: value.set(Font.TIMES_BOLD)))
    m.add(util.Option('G', 'Times New Roman Italic',      lambda: value.set(Font.TIMES_ITALIC)))
    m.add(util.Option('H', 'Times New Roman Bold Italic', lambda: value.set(Font.TIMES_BITALIC)))
    m.run()

@util.errhandler
def select_font(value: util.Wrapper):
    util.print_output('已启动文件选择器.')
    from tkinter import filedialog
    fonttypes = [('字体文件', '*.otf;*.ttf')]
    fontfile  = filedialog.askopenfilename(title='选择字体', initialdir='/', filetypes=fonttypes)
    ret = Path(fontfile)
    if not ret.exists():
        raise ValueError('字体文件不存在.')
    value.data = ret

if   platform.system() == 'Windows':
    system_font_path = os.path.join(os.environ['WINDIR'], 'Fonts')
    user_font_path   = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Fonts')
    SYSTEM_FONT_PATH = [system_font_path, user_font_path]
elif platform.system() == 'Linux':
    SYSTEM_FONT_PATH = [
        '/usr/share/fonts',
        '/usr/local/share/fonts',
        '/etc/fonts',
    ]
elif platform.system() == 'Darwin':
    SYSTEM_FONT_PATH = [
        '/Library/Fonts',
        '/System/Library/Fonts',
        str(os.path.expanduser('~/Library/Fonts')),
    ]
else:
    SYSTEM_FONT_PATH = []

def _get_font_name(path: str, basename: str) -> str:
    try:
        font = TTFont(path)
        for r in font['name'].names:
            if r.nameID == 4:
                return r.toUnicode()
    except:
        pass
    return basename

def get_system_fonts() -> dict[str, str]:
    font_dict = {}
    for path in SYSTEM_FONT_PATH:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith('.otf') or file.lower().endswith('.ttf'):
                    path = os.path.join(root, file)
                    name = _get_font_name(path, file)
                    font_dict[name] = path
    return font_dict

def _select_system_font_menu_display(count: int):
    util.print_left(f'共发现 {count} 个系统字体.')
    util.print_splitter()

def select_system_font(value: util.Wrapper):
    util.print_output('读取系统字体中…')
    fonts = get_system_fonts()
    keys  = list(fonts.keys())
    vals  = list(fonts.values())
    
    m = util.Menu('Lekco Visurus - 选择字体', pagesize=13)
    m.add(util.Display(lambda: _select_system_font_menu_display(len(fonts))))
    m.add(util.FixedOption('Q', '返回'))
    
    for i in range(len(fonts)):
        key = chr(65 + i % 12)
        m.add(util.Option(key, keys[i], lambda _i=i: value.set(vals[_i])))
    m.run()

check()
