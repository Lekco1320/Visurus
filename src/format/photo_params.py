import watermark
import resources

from util import *
from util import menu
from util import ansi
from util import output
from util import workspace

from format import shadow

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL.ExifTags import Base

from config import Config

#region 变量

targets: list[image] = []
out: list[outimage]  = []
size                 = wrapper(Config['photo_params.size'])
enshadow             = wrapper(Config['photo_params.enshadow'])
enwatermark          = wrapper(Config['photo_params.enwatermark'])
typeset              = wrapper(Config['photo_params.typeset'])
bottom_side          = wrapper(Config['photo_params.bottom_side'])
bottom_center        = wrapper(Config['photo_params.bottom_center'])
back_blur            = wrapper(Config['photo_params.back_blur'])
width                = { '1080P' : 1920, '2K' : 2560, '4K' : 3840 }
info                 = None

#endregion

#region 主函数

@errhandler
def main():
    global targets, out
    targets.clear()
    out.clear()
    targets = workspace.c_main()
    if len(targets) == 0:
        raise ValueError('目标图像为空.')
    for image in targets:
        single_main(image)
    if len(out) > 0:
        output.main(out)

def single_main(image: image):
    global info
    info = image.exif
    
    m = menu.menu('Lekco Visurus - 拍摄参数', 'X')
    m.add(menu.display(lambda: display(image)))
    m.add(menu.splitter('- 拍摄参数 -'))
    m.add(menu.option('M', '相机制造商', set_make,          get_make))
    m.add(menu.option('D', '相机型号',   set_model,         get_model))
    m.add(menu.option('B', '镜头型号',   set_lens_model,    get_lens_model))
    m.add(menu.option('L', '焦距',       set_focal_len,     get_focal_len))
    m.add(menu.option('E', '曝光时间',   set_exposure_time, get_exposure_time))
    m.add(menu.option('F', '光圈值',     set_fnumber,       get_fnumber))
    m.add(menu.option('I', 'ISO值',      set_iso,           get_iso))
    m.add(menu.option('T', '拍摄时间',   set_datetime,      get_datetime))
    m.add(menu.splitter('- 排版设置 -'))
    m.add(menu.option('P', '排版样式',   lambda: p_main(typeset),                   lambda: p_value(typeset)))
    m.add(menu.option('C', '排版参数…',  lambda: bottom_side_main(bottom_side),     enfunc=lambda: typeset.data == '底部双侧标注'))
    m.add(menu.option('C', '排版参数…',  lambda: bottom_center_main(bottom_center), enfunc=lambda: typeset.data == '底部中央标注'))
    m.add(menu.option('C', '排版参数…',  lambda: blur_main(back_blur),              enfunc=lambda: typeset.data == '背景模糊标注'))
    m.add(menu.option('S', '图像尺寸',   lambda: s_main(size),                      lambda: s_value(size)))
    m.add(menu.option('N', '图像阴影',   lambda: n_main(enshadow),                  lambda: n_value(enshadow)))
    m.add(menu.option('H', '阴影效果…',  shadow.style_main,                         enfunc=h_enable))
    m.add(menu.option('W', '图像水印',   lambda: w_main(enwatermark),               lambda: w_value(enwatermark)))
    m.add(menu.option('A', '水印样式…',  watermark.style.main,                      enfunc=lambda: enwatermark.data))
    m.add(menu.splitter('- 导出 -'))
    m.add(menu.option('O', '完成设置',   lambda: process(image, m)))
    m.add(menu.option('X', '跳过'))
    m.run()

def display(image: image):
    print_left('当前图像: ' + image.formated_name())
    print_spliter()

#endregion

#region 拍摄参数

def set_make():
    print_output('请输入相机制造商:')
    info[Base.Make] = get_input()

def get_make() -> str:
    return info[Base.Make]

def set_model():
    print_output('请输入相机型号:')
    info[Base.Model] = get_input()

def get_model() -> str:
    return info[Base.Model]

def set_lens_model():
    print_output('请输入镜头型号:')
    info[Base.LensModel] = get_input()

def get_lens_model() -> str:
    return info[Base.LensModel]

def set_focal_len():
    print_output('请输入焦距:')
    info[Base.FocalLength] = get_input()

def get_focal_len() -> str:
    return info[Base.FocalLength]

def set_exposure_time():
    print_output('请输入曝光时间:')
    info[Base.ExposureTime] = get_input()

def get_exposure_time() -> str:
    return info[Base.ExposureTime]

def set_fnumber():
    print_output('请输入光圈值:')
    info[Base.FNumber] = get_input()

def get_fnumber() -> str:
    return info[Base.FNumber]

def set_iso():
    print_output('请输入ISO值:')
    info[Base.ISOSpeedRatings] = get_input()

def get_iso() -> str:
    return info[Base.ISOSpeedRatings]

def set_datetime():
    print_output('请输入拍摄时间:')
    info[Base.DateTimeOriginal] = get_input()

def get_datetime() -> str:
    return info[Base.DateTimeOriginal]

#endregion

#region 图像尺寸

def s_main(size: wrapper):
    m = menu.menu('Lekco Visurus - 图像尺寸')
    m.add(menu.option('1', '1080P', lambda: s_1080P(size)))
    m.add(menu.option('2', '2K',    lambda: s_2K(size)))
    m.add(menu.option('3', '4K',    lambda: s_4K(size)))
    m.add(menu.option('4', '自适应', lambda: s_fit(size)))
    m.add(menu.option('Q', '退出'))
    m.run()

def s_1080P(size: wrapper):
    size.data = '1080P'

def s_2K(size: wrapper):
    size.data = '2K'

def s_4K(size: wrapper):
    size.data = '4K'

def s_fit(size: wrapper):
    size.data = '自适应'

def s_value(size: wrapper) -> str:
    return size.data

#endregion

#region 图像阴影

def n_main(enshadow: wrapper):
    m = menu.menu('Lekco Visurus - 图像阴影')
    m.add(menu.option('E', '启用', lambda: e_enable(enshadow)))
    m.add(menu.option('D', '关闭', lambda: e_disable(enshadow)))
    m.run()

def e_enable(enshadow: wrapper):
    enshadow.data = True

def e_disable(enshadow: wrapper):
    enshadow.data = False

def n_value(enshadow: wrapper) -> str:
    return '启用' if enshadow.data else '关闭'

def h_enable():
    return enshadow.data

#endregion

#region 图像水印

def w_main(enwatermark: wrapper):
    m = menu.menu('Lekco Visurus - 图像水印')
    m.add(menu.option('E', '启用', lambda: w_enable(enwatermark)))
    m.add(menu.option('D', '关闭', lambda: w_disable(enwatermark)))
    m.run()

def w_enable(enwatermark: wrapper):
    enwatermark.data = True

def w_disable(enwatermark: wrapper):
    enwatermark.data = False

def w_value(enwatermark: wrapper) -> str:
    return '启用' if enwatermark.data else '关闭'

#endregion

#region 排版模式

def p_main(typeset: wrapper):
    m = menu.menu('Lekco Visurus - 排版样式')
    m.add(menu.option('S', '底部两侧标注', lambda: p_bottom_side(typeset)))
    m.add(menu.option('C', '底部中央标注', lambda: p_bottom_center(typeset)))
    m.add(menu.option('B', '背景模糊标注', lambda: p_blur(typeset)))
    m.add(menu.option('Q', '返回'))
    m.run()

def p_bottom_side(typeset: wrapper):
    typeset.data = '底部双侧标注'

def p_bottom_center(typeset: wrapper):
    typeset.data = '底部中央标注'

def p_blur(typeset: wrapper):
    typeset.data = '背景模糊标注'

def p_value(typeset: wrapper) -> str:
    return typeset.data

#endregion

#region 排版参数

def param_display():
    print_left('下列参数以给定占位符表示:')
    colored = lambda c: ansi.ansi_str(c, ansi.FORMAT_VALUE)
    print_left(colored('{M}') + ' | 相机制造商')
    print_left(colored('{D}') + ' | 相机型号')
    print_left(colored('{B}') + ' | 镜头型号')
    print_left(colored('{L}') + ' | 焦距')
    print_left(colored('{E}') + ' | 曝光时间')
    print_left(colored('{F}') + ' | 光圈值')
    print_left(colored('{I}') + ' | ISO值')
    print_left(colored('{T}') + ' | 拍摄时间')
    print_spliter()

@errhandler
def param_set(param: wrapper, id: int):
    print_output('请输入参数对应的占位符:')
    print_ps('请按顺序连续拼接一个或多个参数.')
    param.data[id] = get_input()

def bottom_side_main(param: wrapper):
    m = menu.menu('Lekco Visurus - 排版参数', 'Q')
    m.add(menu.display(param_display))
    m.add(menu.option('A', '左第一行', lambda: param_set(param, 0), lambda: param.data[0]))
    m.add(menu.option('B', '左第二行', lambda: param_set(param, 1), lambda: param.data[1]))
    m.add(menu.option('C', '右第一行', lambda: param_set(param, 2), lambda: param.data[2]))
    m.add(menu.option('D', '右第二行', lambda: param_set(param, 3), lambda: param.data[3]))
    m.add(menu.option('Q', '返回'))
    m.run()

def bottom_center_main(param: wrapper):
    m = menu.menu('Lekco Visurus - 排版参数', 'Q')
    m.add(menu.display(param_display))
    m.add(menu.option('A', '第一行黑字', lambda: param_set(param, 0), lambda: param.data[0]))
    m.add(menu.option('B', '第一行红字', lambda: param_set(param, 1), lambda: param.data[1]))
    m.add(menu.option('C', '第一行粗字', lambda: param_set(param, 2), lambda: param.data[2]))
    m.add(menu.option('D', '第二行',     lambda: param_set(param, 3), lambda: param.data[3]))
    m.add(menu.option('Q', '返回'))
    m.run()

def blur_main(param: wrapper):
    m = menu.menu('Lekco Visurus - 排版参数', 'Q')
    m.add(menu.display(param_display))
    m.add(menu.option('A', '第一行文本',   lambda: param_set(param, 0),    lambda: param.data[0]))
    m.add(menu.option('B', '第二行文本',   lambda: param_set(param, 1),    lambda: param.data[1]))
    m.add(menu.option('R', '背景模糊程度', lambda: blur_set_blur(param),   lambda: param.data[2].__str__()))
    m.add(menu.option('I', '背景亮度',     lambda: blur_set_brightness(param),   lambda: f'{param.data[3] * 100}%'))
    m.add(menu.option('Q', '返回'))
    m.run()

@errhandler
def blur_set_blur(param: wrapper):
    print_output('请输入模糊半径:')
    param.data[2] = int(get_input())

@errhandler
def blur_set_brightness(param: wrapper):
    print_output('请输入亮度(%):')
    ans = int(get_input())
    if ans < 0 or ans > 100:
        raise ValueError(f'非法的亮度值 \'{ans}\'')
    param.data[3] = ans / 100

#endregion

#region 图像处理

params_map = {
    'M' : Base.Make,
    'D' : Base.Model,
    'B' : Base.LensModel,
    'L' : Base.FocalLength,
    'E' : Base.ExposureTime,
    'F' : Base.FNumber,
    'I' : Base.ISOSpeedRatings,
    'T' : Base.DateTimeOriginal
}

def param_to_str(params: wrapper, id: int) -> str:
    return params.data[id].format_map({key : info[params_map[key]] for key in params_map.keys()})

def process(image: image, menu: menu.menu):
    img = resize(image.image)
    if enshadow.data:
        img = shadow.process(img)
    if   typeset.data == '底部双侧标注':
        img = process_bottom_side(img)
    elif typeset.data == '底部中央标注':
        img = process_bottom_center(img)
    elif typeset.data == '背景模糊标注':
        img = process_blur(img)
    if enwatermark.data:
        img = watermark.main.process(img)
    out.append(output.outimage(img, image))
    menu.exit()

def resize(image: Image.Image) -> Image.Image:
    if size.data == '自适应':
        return image
    newheight = round(image.height * width[size.data] / image.width)
    return image.resize((width[size.data], newheight))

def process_bottom_side(image: Image.Image) -> Image.Image:
    width, height = image.size
    margin = round(width * 200 / 8250)
    bottom = round(height * 650 / 5500)
    bmar1  = round(bottom * 135 / 660)
    bmar2  = round(bottom * 55  / 660)
    font   = round(bottom * 140 / 660)
    offy   = margin + height + bmar1
    
    final  = Image.new('RGBA', (width + margin * 2, height + margin + bottom), (255, 255, 255))
    final.paste(image, (margin, margin), image)
    
    light = ImageFont.truetype(resources.get_font(resources.font.PUHUI_LIGHT), font)
    bold  = ImageFont.truetype(resources.get_font(resources.font.PUHUI_BOLD), font)
    draw  = ImageDraw.Draw(final)
    sget  = lambda id: param_to_str(bottom_side, id)
    
    draw.text((margin, offy), sget(0), (0, 0, 0), bold)
    draw.text((margin, offy + font + bmar2), sget(1), (50, 50, 50), light)
    length = draw.textlength(sget(2), bold)
    draw.text((width + margin - length, offy), sget(2), (0, 0, 0), bold)
    length = draw.textlength(sget(3), light)
    draw.text((width + margin - length, offy + font + bmar2), sget(3), (50, 50, 50), light)
    
    return final

def process_bottom_center(image: Image.Image) -> Image.Image:
    width, height = image.size
    margin = round(width * 200 / 8250)
    bottom = round(height * 650 / 5500)
    bmar1  = round(bottom * 125 / 660)
    bmar2  = round(bottom * 55  / 660)
    font1  = round(bottom * 160 / 660)
    font2  = round(bottom * 135 / 660)
    offy   = margin + height + bmar1
    
    final  = Image.new('RGBA', (width + margin * 2, height + margin + bottom), (255, 255, 255))
    final.paste(image, (margin, margin), image)
    sget  = lambda id: param_to_str(bottom_center, id)
    
    light   = ImageFont.truetype(resources.get_font(resources.font.PUHUI_LIGHT), font2)
    regular = ImageFont.truetype(resources.get_font(resources.font.PUHUI_REGULAR), font1)
    bold    = ImageFont.truetype(resources.get_font(resources.font.PUHUI_BOLD), font1)
    draw    = ImageDraw.Draw(final)
    
    len0 = draw.textlength(sget(0), regular)
    len1 = draw.textlength(sget(1), bold)
    len2 = draw.textlength(sget(2), bold)
    left = round((image.width + 2 * margin - len0 - len1 - len2) / 2)
    draw.text((left, offy), sget(0), (0, 0, 0), regular)
    draw.text((left + len0, offy), sget(1), (227, 39, 39), bold)
    draw.text((left + len0 + len1, offy), sget(2), (0, 0, 0), bold)
    
    len3  = draw.textlength(sget(3), light)
    left  = round((image.width + 2 * margin - len3) / 2)
    draw.text((left, offy + font1 + bmar2), sget(3), (50, 50, 50), light)
    
    return final

def process_blur(image: Image.Image) -> Image.Image:
    width, height = image.size
    margin = round(width * 400 / 8250)
    bottom = round(height * 650 / 5500)
    bmar1  = round(bottom * 125 / 660)
    bmar2  = round(bottom * 55  / 660)
    font1  = round(bottom * 160 / 660)
    font2  = round(bottom * 135 / 660)
    offy   = margin + height + bmar1
    
    bwidth  = round(width + 2 * margin)
    bheight = round(height + margin + bottom)
    final   = ImageEnhance.Brightness(image.copy() \
                                           .resize((bwidth, bheight)) \
                                           .filter(ImageFilter.GaussianBlur(back_blur.data[2]))) \
                                           .enhance(back_blur.data[3])
    final.paste(image, (margin, margin), image)
    sget = lambda id: param_to_str(back_blur, id)
    
    bold    = ImageFont.truetype(resources.get_font(resources.font.PUHUI_BOLD), font1)
    regular = ImageFont.truetype(resources.get_font(resources.font.PUHUI_REGULAR), font2)
    draw    = ImageDraw.Draw(final)
    
    len0 = draw.textlength(sget(0), bold)
    left = round((bwidth - len0) / 2)
    draw.text((left, offy), sget(0), (255, 255, 255), bold)
    len1 = draw.textlength(sget(1), regular)
    left = round((bwidth - len1) / 2)
    draw.text((left, offy + font1 + bmar2), sget(1), (255, 255, 255), regular)
    
    return final

#endregion
