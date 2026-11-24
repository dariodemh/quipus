# -*- coding: utf-8 -*-
"""Fotogrametria calibrada en color (CIELAB) y escala sobre la foto de campo de SH001 (KH0631):
  data/external/open-khipu-repository/data/KH0631_0632/SH 001 upper half with ruler & greyscale.jpeg

1. Mide los 15 parches de la carta de grises (0..14) para verificar linealidad de exposicion
   y obtener balance de blancos neutral sobre el gris medio (parche 7).
2. Mide las cuerdas de los 4 grupos visibles debajo de la cuerda principal y las convierte a
   espacio CIELAB (D65/sRGB) de forma vectorizada para calcular la separacion perceptual Delta-E.

Uso: python analisis/37_vision_y_extra/medir_sh001_foto.py
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent


def srgb_to_lab_batch(rgb):
    """Convierte arreglo (..., 3) RGB [0..255] a CIELAB (D65) vectorizado."""
    arr = np.clip(np.asarray(rgb, float) / 255.0, 0.0, 1.0)
    lin = np.where(arr <= 0.04045, arr / 12.92, ((arr + 0.055) / 1.055) ** 2.4)
    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])
    xyz = lin @ M.T
    ref = np.array([0.95047, 1.00000, 1.08883])
    t = xyz / ref
    f = np.where(t > 0.008856, np.cbrt(t), 7.787 * t + 16.0 / 116.0)
    L = 116.0 * f[..., 1] - 16.0
    a = 500.0 * (f[..., 0] - f[..., 1])
    b = 200.0 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], axis=-1)


def delta_e(lab1, lab2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(lab1, lab2)))


def main():
    img_path = RAIZ / "data/external/open-khipu-repository/data/KH0631_0632/SH 001 upper half with ruler & greyscale.jpeg"
    im = np.array(Image.open(img_path).convert("RGB"))

    x0, x1 = 925, 3385
    w_patch = (x1 - x0) / 15.0
    parches = []
    for k in range(15):
        px0 = int(x0 + (k + 0.25) * w_patch)
        px1 = int(x0 + (k + 0.75) * w_patch)
        med = np.median(im[900:1060, px0:px1], axis=(0, 1))
        parches.append((k, med))

    mid_rgb = parches[7][1]
    wb_gain = mid_rgb.mean() / mid_rgb
    print("SH001 carta gris parche 7 RGB crudo:", [round(x, 1) for x in mid_rgb], "gains:", [round(x, 4) for x in wb_gain])

    rows = []
    for k, rgb in parches:
        c_rgb = np.clip(rgb * wb_gain, 0, 255)
        L, a, b = srgb_to_lab_batch(c_rgb)
        rows.append(dict(clase="carta_gris", etiqueta=f"parche_{k}", x=int(x0 + (k + 0.5) * w_patch), y=980,
                         R=round(float(c_rgb[0]), 1), G=round(float(c_rgb[1]), 1), B=round(float(c_rgb[2]), 1),
                         L_star=round(float(L), 2), a_star=round(float(a), 2), b_star=round(float(b), 2),
                         n_pixeles=0))

    # Submuestreo espacial 4x4 en el ROI para rapidez y exactitud
    roi = im[1600:2800:4, 400:4900:4].astype(float) * wb_gain
    lum = roi.mean(axis=2)
    sat = roi.max(axis=2) - roi.min(axis=2)
    mask_cord = (lum < 122) | (sat > 22)
    lab_roi = srgb_to_lab_batch(roi)

    bandas = [
        ("g0_oscuro_WLK", 550, 1450, lambda L, a, b: L < 22),
        ("g0_marron_MB", 550, 1450, lambda L, a, b: (L >= 22) & (L <= 45) & (a > 6)),
        ("g0_claro_YB", 550, 1450, lambda L, a, b: L > 48),
        ("g1_marron_MB", 1850, 2750, lambda L, a, b: (L >= 22) & (L <= 45) & (a > 6)),
        ("g1_claro_YB", 1850, 2750, lambda L, a, b: L > 48),
        ("g2_oscuro_WLK", 2950, 3550, lambda L, a, b: L < 22),
        ("g2_claro_YB", 2950, 3550, lambda L, a, b: L > 48),
        ("g3_claro_AB", 3750, 4800, lambda L, a, b: L > 48),
    ]

    grupos_lab = {}
    for etq, bx0, bx1, pred in bandas:
        cx0 = (bx0 - 400) // 4
        cx1 = (bx1 - 400) // 4
        m = mask_cord[:, cx0:cx1]
        pts_rgb = roi[:, cx0:cx1][m]
        pts_lab = lab_roi[:, cx0:cx1][m]
        sel_m = pred(pts_lab[:, 0], pts_lab[:, 1], pts_lab[:, 2])
        if np.any(sel_m):
            med_rgb = np.median(pts_rgb[sel_m], axis=0)
            med_lab = np.median(pts_lab[sel_m], axis=0)
            grupos_lab[etq] = (float(med_lab[0]), float(med_lab[1]), float(med_lab[2]))
            rows.append(dict(
                clase="cuerda_sh001", etiqueta=etq, x=int((bx0 + bx1) / 2), y=2200,
                R=round(float(med_rgb[0]), 1), G=round(float(med_rgb[1]), 1), B=round(float(med_rgb[2]), 1),
                L_star=round(float(med_lab[0]), 2), a_star=round(float(med_lab[1]), 2), b_star=round(float(med_lab[2]), 2),
                n_pixeles=int(np.sum(sel_m)),
            ))

    pd.DataFrame(rows).to_csv(DIR / "sh001_fotogrametria.csv", index=False)

    pares_de = {}
    for k1, k2 in [("g0_oscuro_WLK", "g0_marron_MB"), ("g0_marron_MB", "g0_claro_YB"),
                   ("g0_oscuro_WLK", "g0_claro_YB"), ("g1_claro_YB", "g3_claro_AB"),
                   ("g0_marron_MB", "g1_marron_MB"), ("g0_oscuro_WLK", "g2_oscuro_WLK")]:
        if k1 in grupos_lab and k2 in grupos_lab:
            pares_de[f"{k1} vs {k2}"] = round(delta_e(grupos_lab[k1], grupos_lab[k2]), 2)

    print("SH001 CIELAB por grupo:", {k: [round(x, 1) for x in v] for k, v in grupos_lab.items()})
    print("SH001 Delta-E:", pares_de)
    (DIR / "sh001_delta_e.json").write_text(json.dumps(dict(lab=grupos_lab, delta_e=pares_de), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
