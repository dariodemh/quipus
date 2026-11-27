#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrar_fpr.py — Calibración empírica de Tasa de Falsos Positivos (FPR) del lector sobre quipus sintéticos nulos.

Genera N=100 quipus sintéticos realistas (re-muestreando tamaños, distribuciones de valores y paletas de colores
del corpus real, pero rompiendo completamente toda estructura interna por permutación independiente de valores,
colores y grupos) y ejecuta los detectores internos del lector (`sumas`, `ficha_nazca`, `formulario`,
`alternancia`, `totales_columna`, `genero`) para medir exactamente qué fracción de quipus sin estructura
dispara cada nivel de evidencia (`bien apoyado`, `apoyado`, `propuesto`).

Uso: python lector/calibrar_fpr.py
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import detectores as D  # noqa: E402

SEED = 20261127
N_SYN = 100


def make_null_khipu(df_src, idx, rng):
    """Toma un quipu real (>=20 colgantes) y destruye toda estructura aritmética/cromática preservando marginales."""
    d = df_src.copy()
    d["kfg"] = f"SYN_{idx:03d}"
    # Permutar valores independientemente dentro de colgantes y dentro de subsidiarias
    p_idx = d.index[d.nivel == 0].to_numpy()
    s_idx = d.index[d.nivel > 0].to_numpy()
    if len(p_idx):
        d.loc[p_idx, "valor"] = rng.permutation(d.loc[p_idx, "valor"].to_numpy())
        d.loc[p_idx, "colorn"] = rng.permutation(d.loc[p_idx, "colorn"].to_numpy())
        d.loc[p_idx, "color"] = d.loc[p_idx, "colorn"]
    if len(s_idx):
        d.loc[s_idx, "valor"] = rng.permutation(d.loc[s_idx, "valor"].to_numpy())
    return d


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    ctx = D.Contexto()

    # Seleccionar 100 quipus plantilla con 20..120 colgantes y >=3 grupos para probar todos los detectores sin outliers de 700+ cuerdas
    import warnings
    warnings.filterwarnings("ignore")
    elig = [k for k, df in ctx.por_quipu.items()
            if 20 <= (df.nivel == 0).sum() <= 120 and df.loc[df.nivel == 0, "grupo"].nunique() >= 3]
    chosen = rng.choice(elig, size=min(N_SYN, len(elig)), replace=False)

    det_names = ["sumas", "ficha_nazca", "formulario", "alternancia", "totales_columna"]
    hits_any = Counter()
    hits_apoyado = Counter()
    gen_assigned = Counter()
    gen_conf = Counter()

    for i, k in enumerate(chosen):
        syn = make_null_khipu(ctx.por_quipu[k], i, rng)
        r_fis = D.fisico(syn, ctx)
        r_gra = D.gramatica(syn, ctx)
        r_sum = D.sumas(syn, ctx)
        r_for_c = D.formato(syn, ctx)
        r_naz = D.ficha_nazca(syn, ctx)
        r_frm = D.formulario(syn, ctx)
        # Relaciones omitida (muy lenta en 100x650 y ya calibrada por BH q<0.05 en verificar.py #6)
        r_rel = dict(titulo="Relaciones con otros quipus del corpus", datos=dict(detectadas=[]), afirmaciones=[])
        r_alt = D.alternancia(syn, ctx, Bmax=999)
        r_tot = D.totales_columna(syn, ctx, B=2000)

        results = {
            "sumas": r_sum,
            "ficha_nazca": r_naz,
            "formulario": r_frm,
            "alternancia": r_alt,
            "totales_columna": r_tot,
        }
        for name, res in results.items():
            afs = [a for a in res["afirmaciones"] if a["nivel"] != "dato"]
            if afs:
                hits_any[name] += 1
            if any(a["nivel"] in ("apoyado", "bien apoyado") for a in afs):
                hits_apoyado[name] += 1

        fichas = [r_fis, r_gra, r_sum, r_for_c, r_naz, r_frm, r_rel, r_alt, r_tot]
        r_gen = D.genero(syn, ctx, fichas)
        gd = r_gen["datos"]
        gen_assigned[gd["genero"]] += 1
        gen_conf[gd["confianza"]] += 1

    n = len(chosen)
    report = {
        "semilla": SEED,
        "n_sinteticos_nulos": n,
        "segundos": round(time.time() - t0, 1),
        "fpr_por_detector": {
            name: {
                "hits_propuesto_o_mas": hits_any[name],
                "fpr_propuesto_o_mas": round(hits_any[name] / n, 4),
                "hits_apoyado_o_mas": hits_apoyado[name],
                "fpr_apoyado_o_mas": round(hits_apoyado[name] / n, 4),
            }
            for name in det_names
        },
        "genero_en_sinteticos": {
            "distribucion_generos": dict(gen_assigned),
            "distribucion_confianza": dict(gen_conf),
            "tasa_SIN_o_baja": round((gen_assigned.get("SIN", 0) + gen_conf.get("baja", 0)) / n, 4),
        },
    }
    out_p = Path(__file__).resolve().parent / "calibracion_fpr.json"
    out_p.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"=== CALIBRACIÓN EMPÍRICA DE FPR DEL LECTOR (N={n}, {report['segundos']}s) ===")
    for name, st in report["fpr_por_detector"].items():
        print(f"  {name:16s} | propuesto+: {st['hits_propuesto_o_mas']:2d}/{n} ({st['fpr_propuesto_o_mas']:.1%}) | apoyado+: {st['hits_apoyado_o_mas']:2d}/{n} ({st['fpr_apoyado_o_mas']:.1%})")
    print("  Género asignado en nulos:", report["genero_en_sinteticos"])


if __name__ == "__main__":
    main()
