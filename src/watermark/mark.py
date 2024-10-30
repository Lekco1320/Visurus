from abc import ABC
from abc import abstractmethod
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from watermark import anchor
from watermark import scaler

class markbase(ABC):
    def __init__(self, anchor: anchor, scaler: scaler) -> None:
        super().__init__()
        
        self._anchor = anchor
        self._scaler = scaler
    
    @property
    def anchor(self):
        return self._anchor
    
    @property
    def scaler(self):
        return self._scaler
    
    @property
    @abstractmethod
    def size(self):
        pass
    
    @abstractmethod
    def mark(self, image: Image.Image) -> Image.Image:
        pass

class image_mark(markbase):
    def __init__(self, anchor: anchor, scaler: scaler, image: str, opacity: float) -> None:
        super().__init__(anchor, scaler)
        
        self._image   = image
        self._size    = None
        self._opacity = opacity
        self._initialize()
    
    def _initialize(self):
        width, height = self._scaler.size
        iwdith = 0
        iheight = 0
        with Image.open(self._image) as image:
            iwdith  = image.width
            iheight = image.height
        if   (width, height) == (None, None):
            self._size = (iwdith, iheight)
        elif width == None:
            width = int(height / iheight * iwdith)
            self._size = (width, height)
        else:
            height = int(width / iwdith * iheight)
            self._size = (width, height)
    
    @property
    def image(self):
        return self.image
    
    @property
    def size(self):
        return self._size
    
    @property
    def opacity(self):
        return self._opacity
    
    def mark(self, image: Image.Image) -> Image.Image:
        position = self._anchor.real_position(self._size)
        with Image.open(self._image).convert('RGBA') as img:
            nimg = img.resize(self._size)
            pale = Image.new('RGBA', nimg.size, (0, 0, 0, 0))
            aimg = Image.blend(pale, nimg, self._opacity / 100.0)
            image.paste(aimg, position, aimg)
            return image

class label_mark(markbase):
    def __init__(self, anchor: anchor, scaler: scaler, font: str, color: tuple, text: str) -> None:
        super().__init__(anchor, scaler)
        
        self._font      = font
        self._color     = color
        self._text      = text
        self._size      = None
        self._font_size = None
        self._initialize()
    
    def _initialize(self):
        width, height = self._scaler.size
        if (width, height) == (None, None):
            raise ValueError('文字水印的尺寸大小不得为长宽自适应.')
        if width == None:
            self._font_size = height
            font  = ImageFont.truetype(self._font, height)
            width = font.getlength(self._text)
            self._size = (width, height)
        else:
            size   = 0
            length = 0
            while length < width:
                size  += 1
                font   = ImageFont.truetype(self._font, size)
                length = font.getlength(self._text)
            self._size = (length, size)
            self._font_size = size
    
    @property
    def font(self):
        return self._font
    
    @property
    def text(self):
        return self._text
    
    @property
    def color(self):
        return self._color
    
    @property
    def size(self):
        return self._size
    
    def mark(self, image: Image.Image) -> Image.Image:
        position = self._anchor.real_position(self._size)
        font = ImageFont.truetype(self._font, self._font_size)
        text = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text)
        draw.text(position, self._text, self._color, font)
        return Image.alpha_composite(image, text)
