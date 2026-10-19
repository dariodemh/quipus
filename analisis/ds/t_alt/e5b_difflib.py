"""Alinea las secuencias de valores KFG vs OKR con difflib (permite inserciones y
borrados) para separar:
  - desacuerdo ESTRUCTURAL: una cuerda presente en una transcripcion y no en la otra,
    o en otra posicion del arbol (aparece como insercion/borrado en el alineamiento).
  - desacuerdo de VALOR: cuerdas alineadas 1-a-1 cuyo valor difiere.
"""
import difflib
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
P = pd.read_csv(AQUI/"kfg_vs_okr_cuerdas.csv").sort_values(["kfg", "oidx"])
P["v_okr"] = P.v.fillna(0)

tot_eq = tot_sub = tot_indel = 0
pares = []
det = []
for kfg, g in P.groupby("kfg"):
    a = g.v_kfg.tolist(); b = g.v_okr.tolist()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    eq = sub = indel = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            eq += i2 - i1
        elif op == "replace":
            n = min(i2-i1, j2-j1)
            sub += n
            indel += abs((i2-i1) - (j2-j1))
            if (i2-i1) == (j2-j1):
                for d in range(n):
                    r = g.iloc[i1+d]
                    pares.append(dict(kfg=kfg, cuerda=r.cuerda, v_kfg=r.v_kfg,
                                      v_okr=g.v_okr.iloc[j1+d]))
        else:
            indel += (i2-i1) + (j2-j1)
    det.append(dict(kfg=kfg, n=len(a), iguales=eq, sustituidas=sub, indels=indel))
    tot_eq += eq; tot_sub += sub; tot_indel += indel
D = pd.DataFrame(det)
D["frac_sub"] = D.sustituidas / D.n
print("cuerdas totales:", tot_eq + tot_sub + tot_indel)
print("alineadas iguales:", tot_eq, f"({100*tot_eq/(tot_eq+tot_sub+tot_indel):.2f}%)")
print("alineadas con valor distinto:", tot_sub, f"({100*tot_sub/(tot_eq+tot_sub+tot_indel):.2f}%)")
print("inserciones/borrados (estructural):", tot_indel, f"({100*tot_indel/(tot_eq+tot_sub+tot_indel):.2f}%)")
print("\nquipus con sustituciones de valor:", (D.sustituidas > 0).sum(), "de", len(D))
print("quipus con indels:", (D.indels > 0).sum())
print(D[D.sustituidas > 0].sort_values("frac_sub", ascending=False).head(12).to_string(index=False))
D.to_csv(AQUI/"alineamiento_difflib.csv", index=False)
W = pd.DataFrame(pares)
W.to_csv(AQUI/"desacuerdos_alineados.csv", index=False)
print("\npares alineados con valor distinto:", len(W))
