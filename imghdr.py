
# imghdr.py - Polyfill for Python 3.13 support
# Based on Python 3.12 standard library source
# https://github.com/python/cpython/blob/3.12/Lib/imghdr.py

__all__ = ["what"]

def what(file, h=None):
    f = None
    try:
        if h is None:
            if isinstance(file, str):
                f = open(file, 'rb')
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
                
        for tf in tests:
            res = tf(h, f)
            if res:
                return res
    finally:
        if f: f.close()
    return None

tests = []

def test_jpeg(h, f):
    """JPEG data in JFIF or Exif format"""
    if h[6:10] in (b'JFIF', b'Exif'):
        return 'jpeg'

def test_png(h, f):
    if h.startswith(b'\211PNG\r\n\032\n'):
        return 'png'

def test_gif(h, f):
    """GIF ('87 and '89 variants)"""
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'

def test_tiff(h, f):
    """TIFF (can be in Motorola or Intel byte order)"""
    if h[:2] in (b'MM', b'II'):
        return 'tiff'

def test_rgb(h, f):
    """SGI image library"""
    if h.startswith(b'\001\332'):
        return 'rgb'

def test_pbm(h, f):
    """PBM (portable bitmap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in (b'1', b'4') and h[2] in (b' ', b'\t', b'\n', b'\r'):
        return 'pbm'

def test_pgm(h, f):
    """PGM (portable graymap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in (b'2', b'5') and h[2] in (b' ', b'\t', b'\n', b'\r'):
        return 'pgm'

def test_ppm(h, f):
    """PPM (portable pixmap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in (b'3', b'6') and h[2] in (b' ', b'\t', b'\n', b'\r'):
        return 'ppm'

def test_rast(h, f):
    """Sun raster file"""
    if h.startswith(b'\x59\xA6\x6A\x95'):
        return 'rast'

def test_xbm(h, f):
    """X bitmap (X10 or X11)"""
    s = b'#define '
    if h.startswith(s):
        return 'xbm'

def test_bmp(h, f):
    if h.startswith(b'BM'):
        return 'bmp'

def test_webp(h, f):
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'

def test_exr(h, f):
    if h.startswith(b'\x76\x2f\x31\x01'):
        return 'exr'

tests.append(test_jpeg)
tests.append(test_png)
tests.append(test_gif)
tests.append(test_tiff)
tests.append(test_rgb)
tests.append(test_pbm)
tests.append(test_pgm)
tests.append(test_ppm)
tests.append(test_rast)
tests.append(test_xbm)
tests.append(test_bmp)
tests.append(test_webp)
tests.append(test_exr)
