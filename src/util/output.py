import os

from util import *
from util import config
from util import ansi
from util import menu
from util import workspace

from tkinter  import filedialog
from datetime import datetime

images: list[outimage] = []
chosen: list[int]      = []

FORMAT_MAP = {
    '*.JPG': 'JPEG',
    '*.PNG': 'PNG',
    '*.BMP': 'BMP',
    '*.GIF': 'GIF',
}

CONFIG = config.get('output', [
    config.field('dir',      '桌面'),
    config.field('format',   '*.JPG'),
    config.field('filename', 'o_{N}{E}'),
])

def init(imgs: list[outimage]):
    global images, chosen
    images = imgs
    chosen = list(range(1, len(images) + 1))

def main(imgs: list[outimage]):
    init(imgs)
    
    m = menu.menu('Lekco Visurus - 导出设置', 'Q')
    m.add(menu.display(display))
    m.add(menu.splitter('参数'))
    m.add(menu.option('P', '导出内容',   p_main, p_value))
    m.add(menu.option('D', '导出路径',   d_main, d_value))
    m.add(menu.option('F', '导出格式',   f_main, f_value))
    m.add(menu.option('S', '文件名格式', n_main, n_value))
    m.add(menu.splitter('导出'))
    m.add(menu.option('V', '预览图像',   preview))
    m.add(menu.option('Y', '保存当前设置', lambda: config.save(CONFIG)))
    m.add(menu.option('O', '确认并导出', output))
    m.add(menu.option('Q', '返回'))
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

def d_main():
    m = menu.menu('Lekco Visurus - 导出内容')
    m.add(menu.option('O', '导出至源路径', d_source))
    m.add(menu.option('D', '导出至桌面',   d_desktop))
    m.add(menu.option('F', '选择指定目录', d_disk))
    m.add(menu.option('Q', '返回'))
    m.run()

def d_source(): 
    CONFIG.dir = '源路径'

def d_desktop(): 
    CONFIG.dir = '桌面'

def d_disk():
    print_output('请选择目标路径:')
    CONFIG.dir = filedialog.askdirectory()

def d_value() -> str:
    return fomit_path('* D | 导出路径: {} *', CONFIG.dir)

def f_main():
    m = menu.menu('Lekco Visurus - 导出格式')
    m.add(menu.option('J', '*.JPG', f_jpg))
    m.add(menu.option('P', '*.PNG', f_png))
    m.add(menu.option('B', '*.BMP', f_bmp))
    m.add(menu.option('G', '*.GIF', f_gif))
    m.add(menu.option('Q', '返回'))
    m.run()

def f_jpg():
    CONFIG.format = '*.JPG'

def f_png():
    CONFIG.format = '*.PNG'

def f_bmp():
    CONFIG.format = '*.BMP'

def f_gif():
    CONFIG.format = '*.GIF'

def f_value() -> str:
    return CONFIG.format

def n_display(): 
    true_clear_screen()
    print_left('下列参数以给定占位符表示:')
    colored = lambda c: ansi.ansi_str(c, ansi.FORMAT_VALUE)
    print_left(colored('{N}') + ' | 源文件名')
    print_left(colored('{E}') + ' | 导出格式拓展名')
    print_left(colored('{Y}') + ' | 导出时间:年')
    print_left(colored('{M}') + ' | 导出时间:月')
    print_left(colored('{D}') + ' | 导出时间:日')
    print_left(colored('{H}') + ' | 导出时间:时')
    print_left(colored('{m}') + ' | 导出时间:分')
    print_left(colored('{S}') + ' | 导出时间:秒')
    print_spliter()

@errhandler
def n_main(): 
    print_title('Lekco Visurus - 文件名格式')
    n_display()
    print_output('请输入参数对应的占位符:')
    print_ps('请按顺序连续拼接一个或多个参数.')
    CONFIG.filename = get_input()

def n_value(): 
    return CONFIG.filename

def validate_filename(name: str) -> bool: 
    if os.name == 'posix': 
        invalid_chars = ''
    else:
        invalid_chars = '<>:"/\\|?*'    
    return not any(char in name for char in invalid_chars)

def generate_filename(path: str) -> str: 
    name      = os.path.splitext(os.path.basename(path))[0]
    extension = CONFIG.format[1:].lower()
    time      = datetime.now()
    info      = {
        'N': name,
        'E': extension,
        'Y': time.year,
        'M': time.month,
        'D': time.day,
        'H': time.hour,
        'm': time.minute,
        'S': time.second
    }
    return CONFIG.filename.format_map({key : info[key] for key in info.keys()})

def output():
    print_output('正在导出图像...')
    format = FORMAT_MAP[CONFIG.format]
    for i in chosen:
        dir = CONFIG.dir
        if dir == '桌面':
            if os.name == 'posix':
                dir = os.path.join(os.path.expanduser('~'), 'Desktop')
            else: 
                dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        elif dir == '源路径':
            dir = images[i - 1].dir
        
        name = generate_filename(images[i - 1].name)
        if not validate_filename(name): 
            raise ValueError(f'文件名\"{name}\"中含有非法字符.')
        
        path = os.path.join(dir, name)
        if format in ['JPEG', 'BMP'] and images[i - 1].img.mode == 'RGBA':
            images[i - 1].convert('RGB')
        images[i - 1].img.save(path, format)
        print_success(f'{name} 导出成功.')
    wait()
