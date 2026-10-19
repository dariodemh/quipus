"""Genera recortes de las fotos de fichas para lectura visual.

Uso: python recortar.py JC024 [x0 y0 x1 y1] [escala]
Sin caja: genera 'full' (imagen completa reducida) y 'tabla' (mitad derecha).
Las coordenadas se dan en fracciones 0-1 de la imagen original.
"""
import sys, os
from PIL import Image

SRC = os.path.join(os.path.dirname(__file__), '..', '..', '..',
                   'data', 'external', 'open-khipu-repository', 'data',
                   'KH0653_0663')
OUT = os.path.join(os.path.dirname(__file__), 'recortes')
os.makedirs(OUT, exist_ok=True)


def crop(name, box=None, width=1700, suffix=''):
    p = os.path.join(SRC, name + '_record.jpg')
    im = Image.open(p)
    W, H = im.size
    if box:
        x0, y0, x1, y1 = box
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    w, h = im.size
    if w > width:
        im = im.resize((width, int(h * width / w)), Image.LANCZOS)
    out = os.path.join(OUT, f'{name}{suffix}.jpg')
    im.save(out, quality=92)
    print(out, im.size)


if __name__ == '__main__':
    name = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] != 'auto':
        box = [float(x) for x in sys.argv[2:6]]
        suf = sys.argv[6] if len(sys.argv) > 6 else '_crop'
        crop(name, box, suffix=suf)
    else:
        crop(name, None, 1400, '_full')
        crop(name, (0.42, 0.12, 1.0, 0.68), 1700, '_tabla')
