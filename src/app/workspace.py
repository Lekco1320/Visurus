import util
import os
import tkinter as tk

from PIL import Image
from PIL import ImageTk

SUPPORTED = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.ico', '.psd', '.webp', '.tif', '.tiff']

images: list[util.InImage] = []

def main():
    m = util.Menu('Lekco Visurus - 工作区', 'Q')
    m.add(util.Display(display))
    m.add(util.Option('I', '导入图像', input_main))
    m.add(util.Option('R', '移除图像', remove_main))
    m.add(util.Option('S', '显示图像', show_main))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_left(f'已导入 {len(images)} 张图像:')
    for i in range(len(images)):
        util.print_left(f'{i + 1}. ' + images[i].formated_name())
    util.print_splitter()

def check_space() -> bool:
    ret = len(images) > 0
    if not ret:
        util.print_error('工作区为空.')
    return ret

@util.errhandler
def choose() -> list[int]:
    if not check_space():
        return
    
    util.print_output('请选择目标图像:')
    util.print_ps('请用空格隔开多个索引')
    util.print_ps('空输入默认全选')
    ans = list(map(int, util.get_input().split()))
    if len(ans) == 0:
        util.up_line()
        util.print_output(' '.join([str(i) for i in range(1, len(images) + 1)]))
        return [i for i in range(1, len(images) + 1)]
    for i in ans:
        if i <= 0 or i > len(images):
            raise IndexError(f'\'{i}\' 超出索引范围.')
    return ans

def input_main():
    m = util.Menu('Lekco Visurus - 导入图像')
    m.add(util.Option('F', '输入文件路径', input_files))
    m.add(util.Option('P', '输入目录路径', input_folders))
    m.add(util.Option('D', '对话框选择',   input_dialog))
    m.add(util.Option('Q', '返回'))
    m.run()

def access_check(path: str) -> bool:
    if '$RECYCLE.BIN' in path:
        return False
    try:
        with open(path, 'r'):   
            return True
    except:
        return False  

@util.errhandler
def input_files():
    util.print_output('请输入图像文件路径:')
    path = util.get_input()
    input_file(path)

@util.errhandler
def input_folders():
    util.print_output('请输入图像目录路径:')
    path = util.get_input()
    input_folder(path)

@util.errhandler
def input_file(path: str):
    path = path.replace('"', '').strip()
    _, extension = os.path.splitext(path)
    if extension.lower() in SUPPORTED:
        if access_check(path):
            images.append(util.InImage(path))

@util.errhandler
def input_folder(path: str):
    path = path.replace('"', '').strip()
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            input_file(file_path)

@util.errhandler
def input_file_or_folder(path: str):
    path = path.replace('"', '').strip()
    if   os.path.isdir(path):
        input_folder(path)
    elif os.path.isfile(path):
        input_file(path)

@util.errhandler
def input_dialog():
    util.print_output('已启动文件选择器.')
    from tkinter import filedialog
    filetypes = [('图像文件', ';'.join('*' + ext for ext in SUPPORTED))]
    filenames = filedialog.askopenfilenames(title='导入图像', initialdir='/', filetypes=filetypes)
    for file in filenames:
        if file not in images:
            images.append(util.InImage(file))

def remove_main():
    if not check_space():
        return
    
    to_remove = choose()
    to_remove.sort(reverse=True)
    for id in to_remove:
        del images[id - 1]

def image_window(img: Image.Image, name: str):
    root = tk.Tk()
    root.title(name)
    swidth  = root.winfo_screenwidth()  * 0.8
    sheight = root.winfo_screenheight() * 0.8
    pwidth  = img.width
    pheight = img.height
    zoom    = 1.0
    if pwidth > swidth or pheight > sheight:
        wzoom  = swidth  / pwidth
        hzoom  = sheight / pheight
        zoom   = min(wzoom, hzoom)
    newimg = img.resize((int(pwidth * zoom), int(pheight * zoom)))
    photo  = ImageTk.PhotoImage(newimg)
    label  = tk.Label(root, image=photo)
    label.pack()
    root.mainloop()

def show_main():
    if not check_space():
        return
    
    for id in choose():
        with Image.open(images[id - 1].path) as img:
            image_window(img, images[id - 1].name)

chosen: list[util.InImage] = []

def c_init():
    global chosen
    chosen.clear()

def c_display():
    util.print_left(f'已选择 {len(chosen)} 张图像:')
    for i in range(len(chosen)):
        util.print_left(f'{i + 1}. ' + chosen[i].formated_name())
    util.print_splitter()

def c_main() -> list[util.InImage]:
    c_init()
    
    m = util.Menu('Lekco Visurus - 工作区', 'Q')
    m.add(util.Display(display))
    m.add(util.Display(c_display))
    m.add(util.Option('I', '导入图像', input_main))
    m.add(util.Option('C', '选择图像', choose_main))
    m.add(util.Option('R', '移除图像', remove_main))
    m.add(util.Option('S', '显示图像', show_main))
    m.add(util.Option('Q', '返回'))
    m.run()
    return chosen

def choose_main():
    if not check_space():
        return
    
    global chosen
    chosen.clear()
    for id in choose():
        chosen.append(images[id - 1])
