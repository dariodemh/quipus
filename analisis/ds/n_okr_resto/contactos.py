"""Hojas de contacto (grids de miniaturas con numero de pagina) para revisar los escaneos."""
import glob
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
for kh in ["KH0674", "KH0675", "KH0676"]:
    files = sorted(glob.glob(os.path.join(HERE, "png", kh, "thumb", "p*.png")))
    if not files:
        continue
    cols, rows = 4, 4
    per = cols * rows
    for s in range(0, len(files), per):
        chunk = files[s:s + per]
        ims = [Image.open(f) for f in chunk]
        w = max(i.width for i in ims)
        h = max(i.height for i in ims)
        sheet = Image.new("RGB", (cols * w, rows * h), "white")
        dr = ImageDraw.Draw(sheet)
        for k, (f, im) in enumerate(zip(chunk, ims)):
            x, y = (k % cols) * w, (k // cols) * h
            sheet.paste(im, (x, y))
            dr.rectangle([x, y, x + w - 1, y + h - 1], outline="red", width=3)
            dr.text((x + 8, y + 8), os.path.basename(f)[:-4], fill="red")
        out = os.path.join(HERE, "png", kh, "contacto_%02d.png" % (s // per + 1))
        sheet.save(out)
        print(out, sheet.size)
