"""Elige la orientacion correcta de cada pagina probando 4 rotaciones con tesseract
y puntuando palabras clave de la ficha. Guarda png/<kh>/full/p###.png (2200 px de ancho).
"""
import glob
import os
import re
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
KEYS = ["cord", "knots", "length", "value", "khipu", "subsidiaries", "spin"]


def score(img, tmp):
    img.save(tmp)
    out = subprocess.run([TESS, tmp, "stdout", "-l", "eng", "--psm", "6"],
                         capture_output=True).stdout.decode("utf-8", "ignore").lower()
    return sum(out.count(k) for k in KEYS)


for kh in ["KH0674", "KH0675"]:
    os.makedirs(os.path.join(HERE, "png", kh, "full"), exist_ok=True)
    tmp = r"~\AppData\Local\Temp\opencode\_osd.png"
    for p in sorted(glob.glob(os.path.join(HERE, "png", kh, "p*.png"))):
        base = os.path.basename(p)
        dst = os.path.join(HERE, "png", kh, "full", base)
        if os.path.exists(dst):
            continue
        im = Image.open(p)
        small = im.resize((im.width // 2, im.height // 2))
        best, bs = 0, -1
        for ang in (0, 90, 180, 270):
            s = score(small.rotate(ang, expand=True), tmp)
            if s > bs:
                best, bs = ang, s
        im2 = im.rotate(best, expand=True)
        w, h = im2.size
        im2.resize((2200, int(h * 2200 / w))).save(dst)
        print(kh, base, "rot", best, "score", bs)
