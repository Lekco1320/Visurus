import os
import sys
import shutil

from enum import Enum
from pathlib import Path
from util import appdir

RESOURCE_FOLDER: Path = None

class font(Enum):
    PUHUI_LIGHT   = 'font/AlibabaPuHuiTi-3-45-Light.otf'
    PUHUI_REGULAR = 'font/AlibabaPuHuiTi-3-55-Regular.otf'
    PUHUI_BOLD    = 'font/AlibabaPuHuiTi-3-85-Bold.otf'
    SONGTI_BOLD   = 'font/SourceHanSerifCN-Bold.otf'
    TIMES_REGULAR = 'font/times.ttf'
    TIMES_BOLD    = 'font/timesbd.ttf'
    TIMES_ITALIC  = 'font/timesi.ttf'
    TIMES_BITALIC = 'font/timesbi.ttf'

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

def get_font(font: font) -> str:
    return str(Path.joinpath(RESOURCE_FOLDER, font.value))

def get_icon(icon: icon) -> str:
    return str(Path.joinpath(RESOURCE_FOLDER, icon.value))
