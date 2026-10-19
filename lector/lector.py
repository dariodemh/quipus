# -*- coding: utf-8 -*-
"""Lector reproducible de quipus: ficha de lectura con el nivel de evidencia de cada afirmación.

Uso (desde cualquier carpeta):
  python lector/lector.py UR278             # id KFG
  python lector/lector.py KH0517            # id OKR (se traduce a KFG; o se lee de 17_okr_pendientes)
  python lector/lector.py mi_quipu.csv      # CSV con el esquema de analisis/datos/cuerdas.csv
  python lector/lector.py UR278 --json
  python lector/lector.py --todos [--json]  # corpus completo: una línea por quipu y recuento de errores
"""
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import detectores as D  # noqa: E402

DETECTORES = [D.fisico, D.gramatica, D.sumas, D.formato, D.ficha_nazca, D.formulario, D.relaciones]


def resolver(ident, ctx):
    """Devuelve una lista de DataFrames (uno por quipu) a partir de un id KFG/OKR o de un CSV."""
    if ident.lower().endswith(".csv"):
        c = pd.read_csv(ident, low_memory=False, keep_default_na=False)
        if "kfg" not in c or (c["kfg"] == "").all():
            c["kfg"] = Path(ident).stem
        falta = {"orden", "cuerda", "nivel", "padre", "grupo", "valor", "nudos", "color"} - set(c.columns)
        if falta:
            raise SystemExit(f"Al CSV le faltan columnas: {sorted(falta)}")
        c = D.preparar(c)
        return [x for _, x in c.groupby("kfg", sort=False)]
    if ident in ctx.por_quipu:
        return [ctx.por_quipu[ident]]
    okr = ctx.Q.index[ctx.Q.okr == ident]
    if len(okr):
        return [ctx.por_quipu[okr[0]]]
    x = ctx.extra[ctx.extra.kfg == ident]
    if len(x):
        return [x]
    raise SystemExit(f"No encuentro el quipu {ident!r} (ni en KFG, ni como OKR, ni en 17_okr_pendientes).")


def leer(d, ctx):
    fichas = []
    for f in DETECTORES + D.DETECTORES_EXTRA:
        try:
            fichas.append(f(d, ctx))
        except Exception as e:  # un detector que falla no tumba la ficha; queda registrado
            fichas.append(dict(titulo=f.__name__, datos={}, afirmaciones=[], error=f"{type(e).__name__}: {e}"))
    fichas.append(D.genero(d, ctx, fichas))
    return dict(quipu=d.kfg.iloc[0], secciones=fichas)


def markdown(L):
    out = [f"# Ficha de lectura: {L['quipu']}", ""]
    for s in L["secciones"]:
        out += [f"## {s['titulo']}", ""]
        if s.get("error"):
            out += [f"**Error del detector:** {s['error']}", ""]
        for a in s["afirmaciones"]:
            out.append(f"- [{a['nivel'].upper()}] {a['texto']}  \n  _fuente: {a['fuente']}_")
        if s["datos"]:
            out += ["", "<details><summary>datos</summary>", "", "```", json.dumps(s["datos"], ensure_ascii=False,
                                                                                  indent=1, default=_js), "```",
                    "</details>"]
        out.append("")
    return "\n".join(out)


def _js(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (tuple, set, np.ndarray)):
        return list(o)
    return str(o)


# ---------------------------------------------------------------- corpus completo
_CTX = None


def _uno(k):
    global _CTX
    if _CTX is None:
        _CTX = D.Contexto()
    t = time.time()
    try:
        L = leer(_CTX.por_quipu[k], _CTX)
        err = [s["titulo"] + ": " + s["error"] for s in L["secciones"] if s.get("error")]
        g = L["secciones"][-1]["datos"]
        rel = [h for s in L["secciones"] if s["titulo"].startswith("Relaciones") for h in s["datos"].get("detectadas", [])]
        enm = g.get("enmienda")
        return dict(quipu=k, genero=g.get("genero"), confianza=g.get("confianza"),
                    enmienda=f"{enm['genero']} ({enm['confianza']})" if enm else None, relaciones=len(rel),
                    con=sorted({h["con"] for h in rel}), errores=err, segundos=round(time.time() - t, 1))
    except Exception:
        return dict(quipu=k, errores=[traceback.format_exc(limit=3)], segundos=round(time.time() - t, 1))


def todos(como_json):
    from multiprocessing import Pool, cpu_count
    t = time.time()
    ctx = D.Contexto()
    ks = [k for k in ctx.Q.index if k in ctx.por_quipu]
    with Pool(max(1, cpu_count() - 2)) as P:
        R = P.map(_uno, ks, chunksize=4)
    for r in R:
        if como_json:
            print(json.dumps(r, ensure_ascii=False, default=_js))
        else:
            print(f"{r['quipu']:10s} {str(r.get('genero')):4s} {str(r.get('confianza')):10s} "
                  + (f"enmienda={r['enmienda']} " if r.get("enmienda") else "")
                  + f"rel={r.get('relaciones', '-')} {' '.join(r.get('con', []))}"
                  + (f"  ERROR: {r['errores']}" if r["errores"] else ""))
    n_err = sum(bool(r["errores"]) for r in R)
    print(f"\n{len(R)} quipus en {time.time() - t:.0f} s; con error: {n_err}", file=sys.stderr)
    return R


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    como_json = "--json" in sys.argv
    if "--todos" in sys.argv:
        todos(como_json)
    elif args:
        ctx = D.Contexto()
        for d in resolver(args[0], ctx):
            L = leer(d, ctx)
            print(json.dumps(L, ensure_ascii=False, indent=1, default=_js) if como_json else markdown(L))
    else:
        print(__doc__)
