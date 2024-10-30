import os

from util import ansi
from PIL import Image
from PIL.ExifTags import Base
from datetime import datetime

class image:
    def __init__(self, path: str) -> None:
        self._path = path
        self._dir  = os.path.dirname(path)
        self._name = os.path.basename(path)
        self._size = os.path.getsize(path)
        with Image.open(path) as img:
            self._width  = img.width
            self._height = img.height
    
    @property
    def path(self):
        return self._path
    
    @property
    def dir(self):
        return self._dir
    
    @property
    def name(self):
        return self._name
    
    @property
    def size(self):
        return self._size
    
    @property
    def image(self) -> Image.Image:
        try:
            return Image.open(self._path).convert('RGBA')
        except Exception as ex:
            raise ex
    
    @property
    def raw(self) -> Image.Image:
        return Image.open(self._path)
    
    @property
    def exif(self):
        data = None
        with Image.open(self._path) as raw:
            data = raw._getexif()
        return {
            Base.Make             : image._exif_format(data, Base.Make, lambda val: val, 'Unknown'),
            Base.Model            : image._exif_format(data, Base.Model, lambda val: val, 'Unknown'),
            Base.LensModel        : image._exif_format(data, Base.LensModel, lambda val: val, 'Unknown'),
            Base.FocalLength      : image._exif_format(data, Base.FocalLength, lambda val: f'{image._to_int(val)}mm', '-mm'),
            Base.ExposureTime     : image._exif_format(data, Base.ExposureTime, lambda val: f'{val if val >= 1 else val.real.__str__()}s', '1/-s'),
            Base.FNumber          : image._exif_format(data, Base.FNumber, lambda val: f'f/{image._to_int(val)}', 'f/-'),
            Base.ISOSpeedRatings  : image._exif_format(data, Base.ISOSpeedRatings, lambda val: f'ISO{val}', 'ISO-'),
            Base.DateTimeOriginal : image._exif_format(data, Base.DateTimeOriginal, lambda val: datetime.strptime(val, "%Y:%m:%d %H:%M:%S").__str__(), '-/-/- -:-:-'),
        }
    
    @staticmethod
    def _to_int(value):
        if value.denominator == 1:
            return value.numerator
        return value
    
    @staticmethod
    def _exif_format(data, key, formatfunc, default):
        if data == None:
            return default
        value = data.get(key, None)
        return formatfunc(value) if value != None else default
    
    def formated_name(self):
        return self._name + ansi.ansi_str(f' @{self._width}x{self._height}', ansi.FORMAT_ANNO)

class outimage:
    def __init__(self, new: Image.Image, src: image = None):
        self._img    = new
        self._width  = new.width
        self._height = new.height
        self._dir    = None
        self._name   = None
        if isinstance(src, image):
            self._dir  = src._dir
            self._name = src._name
    
    @property
    def img(self):
        return self._img
    
    @property
    def dir(self):
        return self._dir
    
    @property
    def name(self):
        return self._name
    
    def convert(self, mode: str):
        self._img = self._img.convert(mode)
    
    def formated_name(self):
        return self._name + ansi.ansi_str(f' @{self._width}x{self._height}', ansi.FORMAT_ANNO)
