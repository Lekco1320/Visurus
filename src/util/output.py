from util import *
from util import menu
from util import workspace

import os

from config import Config

images: list[outimage] = []
chosen: list[int]      = []

ddir    = wrapper(Config['output.ddir'])
fformat = wrapper(Config['output.fformat'])

def init(imgs: list[outimage]):
    global images, chosen
    images = imgs
    chosen = list(range(1, len(images) + 1))

def main(imgs: list[outimage]):
    init(imgs)
    
    m = menu.menu('Lekco Visurus - 导出设置', 'Q')
    m.add(menu.option('V', '预览图像',   preview))
    m.add(menu.option('P', '导出内容',   p_main,                  p_value))
    m.add(menu.option('D', '导出路径',   lambda: d_main(ddir),    lambda: d_value(ddir)))
    m.add(menu.option('F', '导出格式',   lambda: f_main(fformat), lambda: f_value(fformat)))
    m.add(menu.option('O', '确认并导出', output))
    m.add(menu.option('Q', '返回'))
    m.add(menu.display(display))
    m.run()

def display():
    print_left(f'导出源含有 {len(images)} 张图像:')
    for i in range(len(images)):
        print_left(f'{i + 1}. ' + images[i].formated_name())
    print_spliter()

def check_space() -> bool:
    ret = len(images) > 0
    if not ret:
        print_error('[错误] 导出源为空.')
    return ret

@errhandler
def choose() -> list[int]:
    if not check_space():
        return
    
    while True:
        print_output('请选择目标图像:')
        print_ps('请用空格隔开多个索引')
        print_ps('空输入默认全选')
        ans = list(map(int, get_input().split()))
        if len(ans) == 0:
            up_line()
            print_output(' '.join([str(i) for i in range(1, len(images) + 1)]))
            return [i for i in range(1, len(images) + 1)]
        else:
            for i in ans:
                if i < 0 or i > len(images):
                    raise IndexError(f'\'{i}\' 超出索引范围.')
            return ans

def preview():
    if not check_space():
        return
    
    for id in choose():
        workspace.image_window(images[id - 1].img, images[id - 1].name)

def p_main():
    global chosen
    chosen = choose()

def p_value() -> str:
    return chosen.__str__()

def d_main(ddir: wrapper):
    m = menu.menu('Lekco Visurus - 导出内容')
    m.add(menu.option('O', '导出至源路径', lambda: dsource(ddir)))
    m.add(menu.option('D', '导出至硬盘',   lambda: ddisk(ddir)))
    m.add(menu.option('W', '暂存至工作区', lambda: dworkplace(ddir)))
    m.add(menu.option('Q', '返回'))
    m.run()

def ddisk(ddir: wrapper):
    from tkinter import filedialog
    print_output('请选择目标路径:')
    ddir.data = filedialog.askdirectory()

def dsource(ddir: wrapper):
    ddir.data = '源路径'

def dworkplace(ddir: wrapper):
    ddir.data = '工作区'

def d_value(ddir: wrapper) -> str:
    return ddir.data

def f_main(fformat: wrapper):
    m = menu.menu('Lekco Visurus - 导出格式')
    m.add(menu.option('J', '*.JPG', lambda: fjpg(fformat)))
    m.add(menu.option('P', '*.PNG', lambda: fpng(fformat)))
    m.add(menu.option('B', '*.BMP', lambda: fbmp(fformat)))
    m.add(menu.option('G', '*.GIF', lambda: fgif(fformat)))
    m.add(menu.option('Q', '返回'))
    m.run()

def fjpg(fformat: wrapper):
    fformat.data = '*.JPG'

def fpng(fformat: wrapper):
    fformat.data = '*.PNG'

def fbmp(ffmort: wrapper):
    fformat.data = '*.BMP'

def fgif(fformat: wrapper):
    fformat.data = '*.GIF'

def f_value(fformat: wrapper) -> str:
    return fformat.data

def output():
    print_output('正在导出图像...')
    extension = fformat.data[1:].lower()
    for i in chosen:
        dir  = ddir.data
        if   dir == '工作区':
            dir = workspace.dir
        elif dir == '源路径':
            dir = images[i - 1].dir
        path = os.path.join(dir, os.path.splitext(images[i - 1].name)[0] + extension)
        if extension == '.jpg' and images[i - 1].img.mode == 'RGBA':
            images[i - 1].convert('RGB')
        images[i - 1].img.save(path)
        print_success(f'{images[i - 1].name} 导出成功.')
    wait()
