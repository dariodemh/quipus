"""Exploración inicial: estructura de racimos, saltos posicionales y bandas."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from parse_quipus import add_parsed, clasifica_aportes


def load():
    d = add_parsed(pd.read_csv("analisis/datos/cuerdas.csv", dtype={"nudos": str}))
    d["ap"] = d.cl.map(clasifica_aportes)
    d["nap"] = d.ap.map(len)
    return d


if __name__ == "__main__":
    d = load()
    x = d[d.nap > 0]
    print("cuerdas totales", len(d), "con >=1 racimo con valor", len(x))
    print("quipus con >=1", x.kfg.nunique())
    print("distribucion nap")
    print(x.nap.value_counts().sort_index().head(12).to_string())

    # saltos posicionales
    def saltos(ap):
        es = sorted({e for e, v, p in ap})
        if len(es) < 2:
            return []
        return [e for e in range(min(es), max(es) + 1) if e not in es]

    x = x.copy()
    x["saltos"] = x.ap.map(saltos)
    x["nsal"] = x.saltos.map(len)
    y = x[x.nap >= 2]
    print("\ncuerdas con >=2 racimos:", len(y), "quipus:", y.kfg.nunique())
    print("con >=1 salto intermedio:", (y.nsal > 0).sum(), f"({(y.nsal>0).mean():.1%})")
    print("saltos por cuerda:", y.nsal.value_counts().sort_index().to_dict())
    print("quipus con >=1 cuerda con salto:", y[y.nsal > 0].kfg.nunique())
    print("\nejemplos de saltos:")
    print(y[y.nsal > 0][["kfg", "cuerda", "valor", "largo", "nudos"]].head(8).to_string())
