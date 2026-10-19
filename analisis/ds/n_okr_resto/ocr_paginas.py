"""OCR con Tesseract de las paginas renderizadas. Guarda txt por pagina en ocr/.
Uso: python ocr_paginas.py [KH0674 KH0675 ...]
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OUT = os.path.join(HERE, "ocr")
os.makedirs(OUT, exist_ok=True)

khs = sys.argv[1:] or ["KH0674", "KH0675", "KH0676"]
for kh in khs:
    dst = os.path.join(OUT, kh)
    os.makedirs(dst, exist_ok=True)
    for png in sorted(glob.glob(os.path.join(HERE, "png", kh, "p*.png"))):
        base = os.path.splitext(os.path.basename(png))[0]
        txt = os.path.join(dst, base)
        if os.path.exists(txt + ".txt"):
            continue
        subprocess.run([TESS, png, txt, "-l", "eng", "--psm", "3"],
                       check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(kh, "ok", len(glob.glob(os.path.join(dst, "*.txt"))), "paginas")
