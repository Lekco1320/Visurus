import watermark
import resources

from util import *
from util import menu
from util import lstr
from util import output
from util import workspace

from format import shadow
from format import round_corner

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from config import Config

#region 变量

targets       = []
species_name  = lstr.lstr()
size          = wrapper(Config['species_label.size'])
enshadow      = wrapper(Config['species_label.enshadow'])
encorner      = wrapper(Config['species_label.encorner'])
enwatermark   = wrapper(Config['species_label.enwatermark'])
latin_name    = ''
gender        = '未知'
location      = ''
date          = ''
width         = { '1080P' : 1920, '2K' : 2560, '4K' : 3840 }

def default():
    global targets, species_name, latin_name, gender, location, date
    targets       = []
    species_name  = lstr.lstr()
    latin_name    = ''
    gender        = '未知'
    location      = ''
    date          = ''

#endregion

#region 主函数

def main():
    default()
    
    m = menu.menu('Lekco Visurus - 物种标注', 'Q')
    m.add(menu.display(display))
    m.add(menu.splitter('- 标注参数 -'))
    m.add(menu.option('N', '物种名',       set_species_name, get_species_name))
    m.add(menu.option('L', '拉丁学名',     set_latin_name,   get_latin_name))
    m.add(menu.option('G', '性别',         g_main,           g_value))
    m.add(menu.option('D', '日期',         set_date,         get_date))
    m.add(menu.option('T', '地点',         set_location,     get_location))
    m.add(menu.splitter('- 图像样式 -'))
    m.add(menu.option('S', '图像尺寸',     lambda: s_main(size),        lambda: s_value(size)))
    m.add(menu.option('E', '图像阴影',     lambda: e_main(enshadow),    lambda: e_value(enshadow)))
    m.add(menu.option('H', '阴影效果…',    shadow.style_main,           enfunc=h_enable))
    m.add(menu.option('A', '图像水印',     lambda: a_main(enwatermark), lambda: a_value(enwatermark)))
    m.add(menu.option('W', '水印样式…',    watermark.style.main,        enfunc=lambda: enwatermark.data))
    m.add(menu.option('R', '图像圆角',     lambda: r_main(encorner),    lambda: r_value(encorner)))
    m.add(menu.option('Y', '圆角半径',     round_corner.radius_main,    round_corner.radius_value, enfunc=y_enable))
    m.add(menu.splitter('- 导入与导出 -'))
    m.add(menu.option('C', '选择目标图像…', choose_targets))
    m.add(menu.option('O', '执行导出…',    execute))
    m.add(menu.option('Q', '返回'))
    m.run()

def display():
    print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        print_left(f'{i + 1}. ' + targets[i].formated_name())
    print_spliter()

#endregion

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

#region 物种名

def set_species_name():
    print_output('请输入物种名:')
    print_ps('用半角括号括住拼音')
    global species_name
    species_name = lstr.lstr(get_input())

def get_species_name() -> str:
    return species_name.__str__()

#endregion

#region 拉丁学名

def set_latin_name():
    print_output('请输入拉丁学名:')
    global latin_name
    latin_name = get_input()

def get_latin_name():
    return latin_name

#endregion

#region 性别

def g_main():
    m = menu.menu('Lekco Visurus - 性别')
    m.add(menu.option('M', '雄性', g_male))
    m.add(menu.option('F', '雌性', g_female))
    m.add(menu.option('N', '未知', g_unknown))
    m.add(menu.option('Q', '退出'))
    m.run()

def g_male():
    global gender
    gender = '雄性'

def g_female():
    global gender
    gender = '雌性'

def g_unknown():
    global gender
    gender = '未知'

def g_value() -> str:
    return gender

#endregion

#region 日期
def set_date():
    print_output('请输入日期:')
    global date
    date = get_input()

def get_date() -> str:
    return date

#endregion

#region 地点

def set_location():
    print_output('请输入地点:')
    global location
    location = get_input()

def get_location() -> str:
    return location

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

def e_main(enshadow: wrapper):
    m = menu.menu('Lekco Visurus - 图像阴影')
    m.add(menu.option('E', '启用', lambda: e_enable(enshadow)))
    m.add(menu.option('D', '关闭', lambda: e_disable(enshadow)))
    m.run()

def e_enable(enshadow: wrapper):
    enshadow.data = True

def e_disable(enshadow: wrapper):
    enshadow.data = False

def e_value(enshadow: wrapper) -> str:
    return '启用' if enshadow.data else '关闭'

def h_enable():
    return enshadow.data

#endregion

#region 图像圆角

def r_main(encorner: wrapper):
    m = menu.menu('Lekco Visurus - 图像圆角')
    m.add(menu.option('E', '启用', lambda: r_enable(encorner)))
    m.add(menu.option('D', '关闭', lambda: r_disable(encorner)))
    m.run()

def r_enable(encorner: wrapper):
    encorner.data = True

def r_disable(encorner: wrapper):
    encorner.data = False

def r_value(encorner: wrapper) -> str:
    return '启用' if encorner.data else '关闭'

def y_enable():
    return encorner.data

#endregion

#region 图像水印

def a_main(enwatermark: wrapper):
    m = menu.menu('Lekco Visurus - 图像水印')
    m.add(menu.option('E', '启用', lambda: a_enable(enwatermark)))
    m.add(menu.option('D', '关闭', lambda: a_disable(enwatermark)))
    m.run()

def a_enable(enwatermark: wrapper):
    enwatermark.data = True

def a_disable(enwatermark: wrapper):
    enwatermark.data = False

def a_value(enwatermark: wrapper) -> str:
    return '启用' if enwatermark.data else '关闭'

#endregion

#region 图像处理

def get_params(size: tuple[int, int]) -> dict[str, int]:
    if size[0] >= size[1]:
        return get_params_w(size[0])
    return get_params_h(size[0])

def get_params_w(width: int) -> dict[str, int]:
    ret = {}
    ratio = 1 + (width - 2560) / 2560
    
    ret['pic_width']       = width
    ret['pic_margin']      = round(ratio * 70)
    ret['pic_bottom']      = round(ratio * 210)
    ret['gender_size']     = round(ratio * 52)
    ret['name_fsize']      = round(ratio * 18 * 300 / 72)
    ret['ps_fsize']        = round(ratio * 7 * 300 / 72)
    ret['latin_fsize']     = round(ratio * 10.5 * 300 / 72)
    ret['other_fsize']     = round(ratio * 10 * 300 / 72)
    ret['ps_offset']       = round(ratio * 4)
    ret['name_offset']     = ret['ps_offset'] + ret['ps_fsize'] * 0.8
    ret['latin_offset']    = round(ratio * 23)
    ret['location_offset'] = round(ratio * -18)
    ret['location_margin'] = round(ratio * 20)
    ret['date_offset']     = round(ratio * -18)
    
    return ret

def get_params_h(width: int) -> dict[str, int]:
    ret = {}
    ratio = 1 + (width - 2560) / 2560
    
    ret['pic_width']       = width
    ret['pic_margin']      = round(ratio * 100)
    ret['pic_bottom']      = round(ratio * 280)
    ret['gender_size']     = round(ratio * 57)
    ret['name_fsize']      = round(ratio * 23 * 300 / 72)
    ret['ps_fsize']        = round(ratio * 11.5 * 300 / 72)
    ret['latin_fsize']     = round(ratio * 15.5 * 300 / 72)
    ret['other_fsize']     = round(ratio * 15 * 300 / 72)
    ret['ps_offset']       = round(ratio * 6)
    ret['name_offset']     = ret['ps_offset'] + ret['ps_fsize'] * 0.8
    ret['latin_offset']    = round(ratio * 28)
    ret['location_offset'] = round(ratio * -23)
    ret['location_margin'] = round(ratio * 25)
    ret['date_offset']     = round(ratio * -23)
    
    return ret

@errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        print_output(f'正在处理 {srcimg.name}...')
        processed = process(srcimg.image)
        out.append(output.outimage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)

def center_of(target_w: float, border_w: float) -> float:
    return (border_w - target_w) / 2

@errhandler
def process(img: Image.Image) -> Image.Image:
    twidth = width[size.data] if size.data != '自适应' else img.width
    if img.width != twidth:
        ratio = img.height / img.width
        img   = img.resize((twidth, round(twidth * ratio)))
    
    if encorner.data:
        img = round_corner.process(img)
    
    if enshadow.data:
        img = shadow.process(img)
    
    params = get_params(img.size)
    final = Image.new('RGBA', (img.width + params['pic_margin'] * 2, img.height + params['pic_margin'] + params['pic_bottom']), 'white')
    final.paste(img, (params['pic_margin'], params['pic_margin']), img)
    draw    = ImageDraw.Draw(final)
    fname   = ImageFont.truetype(resources.get_font(resources.font.SONGTI_BOLD),   params['name_fsize'])
    fps     = ImageFont.truetype(resources.get_font(resources.font.SONGTI_BOLD),   params['ps_fsize'])
    flatin  = ImageFont.truetype(resources.get_font(resources.font.TIMES_BITALIC), params['latin_fsize'])
    fgender = ImageFont.truetype(resources.get_font(resources.font.TIMES_BOLD),    params['latin_fsize'])
    fother  = ImageFont.truetype(resources.get_font(resources.font.SONGTI_BOLD),   params['other_fsize'])
    
    bottom = params['pic_margin'] + img.height
    draw.text((params['pic_margin'], bottom + params['name_offset']), species_name.raw, 'black', fname)
    y    = bottom + params['name_offset'] + params['name_fsize'] + params['latin_offset']
    draw.text((params['pic_margin'], y), latin_name, 'black', flatin)
    if gender != '未知':
        w = draw.textlength(latin_name, flatin)
        x = params['pic_margin'] + w
        draw.text((x, y), ' (m.)' if gender == '雄性' else ' (f.)', 'black', fgender)
    y   += params['location_offset']
    w    = draw.textlength(location, fother)
    x    = params['pic_margin'] + params['pic_width'] - w
    draw.text((x, y), location, 'black', fother)
    x   -= params['location_margin'] + params['other_fsize']
    limg = Image.open(resources.get_icon(resources.icon.LOCATION)).resize((params['other_fsize'] + 4, params['other_fsize'] + 4))
    final.paste(limg, (int(x), int(y + params['other_fsize'] * 0.35)), limg)
    y   += params['date_offset'] - params['other_fsize']
    w    = draw.textlength(date, fother)
    x    = params['pic_margin'] + params['pic_width'] - w
    draw.text((x, y), date, 'black', fother)
    
    x = params['pic_margin']
    y = bottom + params['ps_offset']
    for pair in species_name:
        bw = draw.textlength(pair[0], fname)
        if pair[1] != None:
            pw = draw.textlength(pair[1], fps)
            tx = x + center_of(pw, bw)
            draw.text((tx, y), pair[1], 'black', fps)
        x += bw
    
    x += 10
    y  = bottom + params['name_offset'] + params['name_fsize'] - params['gender_size'] / 2
    gimg: Image.Image
    if   gender == '雄性':
        gimg = Image.open(resources.get_icon(resources.icon.MALE))
    elif gender == '雌性':
        gimg = Image.open(resources.get_icon(resources.icon.FEMALE))
    if   gender != '未知':
        gimg = gimg.resize((params['gender_size'], params['gender_size']))
        final.paste(gimg, (int(x), int(y)), gimg)
    
    if enwatermark.data:
        final = watermark.process(final)
    
    return final

#endregion
