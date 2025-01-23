import util
import watermark

from app import input
from app import output
from app import workspace
from app import appconfig
from app import resources
from app import console

from formatter import shadow
from formatter import round_corner

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from datetime import datetime

#region 变量

CONFIG = appconfig.get('species_label', [
    util.Field('size',      '2K'),
    util.Field('shadow',    False),
    util.Field('sstyle',    shadow.Style.DEFAULT,       shadow.Style.self_validate),
    util.Field('round',     False),
    util.Field('rstyle',    round_corner.Style.DEFAULT, round_corner.Style.self_validate),
    util.Field('order',     ('阴影', '圆角', '水印', '物种标注')),
    util.Field('watermark', False),
    util.Field('wstyle',    watermark.Style.DEFAULT,    watermark.Style.self_validate),
])

targets       = []
species_name  = util.AnnotatedStr()
latin_name    = ''
gender        = '未知'
location      = ''
date          = ''
width         = { '1080P' : 1920, '2K' : 2560, '4K' : 3840 }

def default():
    global targets, species_name, latin_name, gender, location, date
    targets       = []
    species_name  = util.AnnotatedStr()
    latin_name    = ''
    gender        = '未知'
    location      = ''
    today         = datetime.today()
    date          = f'{today.year}.{today.month}.{today.day}'

#endregion

#region 主函数

def main():
    default()
    
    m = util.Menu('Lekco Visurus - 物种标注', 'Q')
    m.add(util.Display(display))
    m.add(util.Splitter('- 标注参数 -'))
    m.add(util.Option('N', '物种名',       set_species_name, get_species_name))
    m.add(util.Option('L', '拉丁学名',     set_latin_name,   get_latin_name))
    m.add(util.Option('G', '性别',         g_main,           g_value))
    m.add(util.Option('D', '日期',         set_date,         get_date))
    m.add(util.Option('T', '地点',         set_location,     get_location))
    m.add(util.Splitter('- 样式设置 -'))
    m.add(util.Option('S', '图像尺寸',     s_main, s_value))
    m.add(util.Option('E', '图像阴影',     e_main, e_value))
    m.add(util.Option('H', '阴影效果…',    CONFIG.sstyle.set, enfunc=lambda: CONFIG.shadow))
    m.add(util.Option('A', '图像水印',     a_main, a_value))
    m.add(util.Option('W', '水印样式…',    CONFIG.wstyle.set, enfunc=lambda: CONFIG.watermark))
    m.add(util.Option('R', '图像圆角',     r_main, r_value))
    m.add(util.Option('P', '圆角参数',     CONFIG.rstyle.set, enfunc=lambda: CONFIG.round))
    m.add(util.Option('B', '效果顺序',     set_order, get_order))
    m.add(util.Option('Y', '保存当前设置', lambda: appconfig.save(CONFIG)))
    m.add(util.Splitter('- 导入与导出 -'))
    m.add(util.Option('C', '选择目标图像…', choose_targets))
    m.add(util.Option('O', '执行导出…',    execute))
    m.add(util.Option('Q', '返回'))
    m.run()

def display():
    util.print_left(f'已选择 {len(targets)} 张目标图像:')
    for i in range(len(targets)):
        util.print_left(f'{i + 1}. ' + targets[i].info())
    util.print_splitter()

#endregion

# 选择图片对象
def choose_targets():
    global targets
    targets = workspace.c_main()

#region 物种名

@console.history('species_label.species_name')
def set_species_name():
    util.print_output('请输入物种名:')
    util.print_ps('用半角括号括住拼音')
    global species_name
    species_name = util.AnnotatedStr(util.get_input())

def get_species_name() -> str:
    return species_name.__str__()

#endregion

#region 拉丁学名

@console.history('species_label.latin_name')
def set_latin_name():
    util.print_output('请输入拉丁学名:')
    global latin_name
    latin_name = util.get_input()

def get_latin_name():
    return latin_name

#endregion

#region 性别

def g_main():
    m = util.Menu('Lekco Visurus - 性别')
    m.add(util.Option('M', '雄性', g_male))
    m.add(util.Option('F', '雌性', g_female))
    m.add(util.Option('N', '未知', g_unknown))
    m.add(util.Option('Q', '退出'))
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
    util.print_output('请输入日期:')
    global date
    date = util.get_input()

def get_date() -> str:
    return date

#endregion

#region 地点

@console.history('species_label.location')
def set_location():
    util.print_output('请输入地点:')
    global location
    location = util.get_input()

def get_location() -> str:
    return location

#endregion

#region 图像尺寸

def s_main():
    m = util.Menu('Lekco Visurus - 图像尺寸')
    m.add(util.Option('1', '1080P', s_1080P))
    m.add(util.Option('2', '2K',    s_2K))
    m.add(util.Option('3', '4K',    s_4K))
    m.add(util.Option('4', '自适应', s_fit))
    m.add(util.Option('Q', '退出'))
    m.run()

def s_1080P():
    CONFIG.size = '1080P'

def s_2K():
    CONFIG.size = '2K'

def s_4K():
    CONFIG.size = '4K'

def s_fit():
    CONFIG.size = '自适应'

def s_value() -> str:
    return CONFIG.size

#endregion

#region 图像阴影

def e_main():
    m = util.Menu('Lekco Visurus - 图像阴影')
    m.add(util.Option('E', '启用', e_enable))
    m.add(util.Option('D', '关闭', e_disable))
    m.run()

def e_enable():
    CONFIG.shadow = True

def e_disable():
    CONFIG.shadow = False

def e_value() -> str:
    return '启用' if CONFIG.shadow else '关闭'

#endregion

#region 图像圆角

def r_main():
    m = util.Menu('Lekco Visurus - 图像圆角')
    m.add(util.Option('E', '启用', r_enable))
    m.add(util.Option('D', '关闭', r_disable))
    m.run()

def r_enable():
    CONFIG.round = True

def r_disable():
    CONFIG.round = False

def r_value() -> str:
    return '启用' if CONFIG.round else '关闭'

#endregion

#region 效果顺序

@util.errhandler
def set_order():
    util.print_output('请输入效果顺序:')
    util.print_ps('例: 阴影 圆角 水印 物种标注')
    CONFIG.order = input.input_valid_sequence(['阴影', '圆角', '水印', '物种标注'])

def get_order() -> str:
    return '→'.join(CONFIG.order)

#endregion

#region 图像水印

def a_main():
    m = util.Menu('Lekco Visurus - 图像水印')
    m.add(util.Option('E', '启用', a_enable))
    m.add(util.Option('D', '关闭', a_disable))
    m.run()

def a_enable():
    CONFIG.watermark = True

def a_disable():
    CONFIG.watermark = False

def a_value() -> str:
    return '启用' if CONFIG.watermark else '关闭'

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

@util.errhandler
def execute():
    if len(targets) <= 0:
        raise ValueError('目标图像为空.')
    
    out = []
    for srcimg in targets:
        util.print_output(f'正在处理 {srcimg.name}...')
        processed = process(srcimg.image)
        out.append(util.OutImage(processed, srcimg))
    
    if len(out) > 0:
        output.main(out)

def center_of(target_w: float, border_w: float) -> float:
    return (border_w - target_w) / 2

def apply_shadow(image: Image.Image) -> Image.Image:
    return shadow.process(CONFIG.sstyle, image) if CONFIG.shadow else image

def apply_round(image: Image.Image) -> Image.Image:
    return round_corner.process(CONFIG.rstyle, image) if CONFIG.round else image

def apply_watermark(image: Image.Image) -> Image.Image:
    return watermark.process(CONFIG.wstyle, image) if CONFIG.watermark else image

def apply_label(img: Image.Image) -> Image.Image:
    twidth = width[CONFIG.size] if CONFIG.size != '自适应' else img.width
    if img.width != twidth:
        ratio = img.height / img.width
        img   = img.resize((twidth, round(twidth * ratio)))
    
    params = get_params(img.size)
    final = Image.new('RGBA', (img.width + params['pic_margin'] * 2, img.height + params['pic_margin'] + params['pic_bottom']), 'white')
    final.paste(img, (params['pic_margin'], params['pic_margin']), img)
    draw    = ImageDraw.Draw(final)
    fname   = ImageFont.truetype(resources.get(resources.Font.SONGTI_BOLD),   params['name_fsize'])
    fps     = ImageFont.truetype(resources.get(resources.Font.SONGTI_BOLD),   params['ps_fsize'])
    flatin  = ImageFont.truetype(resources.get(resources.Font.TIMES_BITALIC), params['latin_fsize'])
    fgender = ImageFont.truetype(resources.get(resources.Font.TIMES_BOLD),    params['latin_fsize'])
    fother  = ImageFont.truetype(resources.get(resources.Font.SONGTI_BOLD),   params['other_fsize'])
    
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
    limg = Image.open(resources.get(resources.Icon.LOCATION)).resize((params['other_fsize'] + 4, params['other_fsize'] + 4))
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
        gimg = Image.open(resources.get(resources.Icon.MALE))
    elif gender == '雌性':
        gimg = Image.open(resources.get(resources.Icon.FEMALE))
    if   gender != '未知':
        gimg = gimg.resize((params['gender_size'], params['gender_size']))
        final.paste(gimg, (int(x), int(y)), gimg)
    
    return final

def process(image: Image.Image):
    for effect in CONFIG.order:
        if   effect == '阴影':
            image = apply_shadow(image)
        elif effect == '圆角':
            image = apply_round(image)
        elif effect == '水印':
            image = apply_watermark(image)
        elif effect == '物种标注':
            image = apply_label(image)
    return image

#endregion
