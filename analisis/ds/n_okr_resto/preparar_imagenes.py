"""Orienta las paginas con tesseract OSD y guarda recortes legibles para transcripcion visual.

- png/<kh>/rot/p###.png : pagina entera rotada, ancho 2000 px
- png/<kh>/left/p###.png: mitad izquierda (cord, spin, knots) ancho 1600 px
- png/<kh>/right/p###.png: mitad derecha (length, color, value, subsidiaries) ancho 1400 px
"""
import glob
import os
import re
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def osd_rotate(path):
    try:
        out = subprocess.run([TESS, path, "-", "--psm", "0"], capture_output=True,
                             text=True, timeout=120).stdout
        m = re.search(r"Rotate: (\d+)", out)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


for kh in ["KH0674", "KH0675"]:
    for sub in ("rot", "left", "right"):
        os.makedirs(os.path.join(HERE, "png", kh, sub), exist_ok=True)
    for p in sorted(glob.glob(os.path.join(HERE, "png", kh, "p*.png"))):
        base = os.path.basename(p)
        rot = osd_rotate(p)
        im = Image.open(p)
        if rot:
            im = im.rotate(-rot, expand=True)
        w, h = im.size
        full = im.resize((2000, int(h * 2000 / w)))
        full.save(os.path.join(HERE, "png", kh, "rot", base))
        izq = im.crop((0, 0, int(w * 0.56), h))
        izq = izq.resize((1600, int(izq.height * 1600 / izq.width)))
        izq.save(os.path.join(HERE, "png", kh, "left", base))
        der = im.crop((int(w * 0.50), 0, w, h))
        der = der.resize((1400, int(der.height * 1400 / der.width)))
        der.save(os.path.join(HERE, "png", kh, "right", base))
        print(kh, base, "rot", rot, im.size)
