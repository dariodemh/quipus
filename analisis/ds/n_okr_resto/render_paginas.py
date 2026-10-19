"""Renderiza a PNG (300 dpi) las paginas de los PDF escaneados de KH0674, KH0675 y KH0676.
Tambien genera miniaturas a 80 dpi para inspeccion visual rapida.
Salida: analisis/ds/n_okr_resto/png/<doc>/p###.png y png/<doc>/thumb/p###.png
"""
import os
import fitz  # pymupdf

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BASE = os.path.join(RAIZ, "data", "external", "open-khipu-repository", "data")
OUT = os.path.join(os.path.dirname(__file__), "png")

DOCS = {
    "KH0674": ("KH0674_0675", "PC.WBC.2016.072.pdf"),
    "KH0675": ("KH0674_0675", "PC.WBC.2016.071.pdf"),
    "KH0676": ("KH0676", "Struass_Original_Notes.pdf"),
}

for kh, (carpeta, fn) in DOCS.items():
    dst = os.path.join(OUT, kh)
    os.makedirs(os.path.join(dst, "thumb"), exist_ok=True)
    doc = fitz.open(os.path.join(BASE, carpeta, fn))
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        pix.save(os.path.join(dst, "p%03d.png" % (i + 1)))
        th = page.get_pixmap(dpi=80)
        th.save(os.path.join(dst, "thumb", "p%03d.png" % (i + 1)))
    print(kh, doc.page_count, "paginas ->", dst)
