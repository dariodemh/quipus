"""Diagnostico rapido: instancias, cobertura de via y acierto exacto por regla (sin nulo)."""
import time
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
from motor import construir, REGLAS

t0 = time.time()
Q, c, q = construir()
print("construido en %.1f s, quipus %d" % (time.time() - t0, len(Q)))

rows = []
for k, o in Q.items():
    via, hit = o.evaluar(o.val)
    m = o.pres
    rows.append(dict(kfg=k, n=o.n, nval=int(m.sum()), inst=o.ni, via=int((via[m] > 0).sum()),
                     hit=int((hit[m] > 0).sum())))
R = pd.DataFrame(rows)
print("cuerdas con valor:", R.nval.sum(), " con via:", R.via.sum(), " con acierto:", R.hit.sum())
print("tasa acierto bruta sobre cuerdas con valor: %.3f" % (R.hit.sum() / R.nval.sum()))

# por regla: cuantas instancias y cuantas aciertan
tot = Counter(); ok = Counter()
for k, o in Q.items():
    if o.ni == 0:
        continue
    pred = np.bincount(o.fin, weights=o.fc * o.val[o.fi], minlength=o.ni)
    h = np.abs(pred - o.val[o.tgt]) < 0.5
    for r in np.unique(o.rule):
        sel = o.rule == r
        tot[REGLAS[r]] += int(sel.sum()); ok[REGLAS[r]] += int(h[sel].sum())
print("\nregla            instancias  aciertan  tasa")
for r in REGLAS:
    if tot[r]:
        print("%-14s %8d %9d  %.3f" % (r, tot[r], ok[r], ok[r] / tot[r]))

print("\nquipus con >=1 instancia:", int((R.inst > 0).sum()))
print("R.hit/nval describe:")
print((R.hit / R.nval.replace(0, np.nan)).describe().round(3))
print("\ntop 10 quipus por acierto bruto (>=20 cuerdas):")
R["tasa"] = R.hit / R.nval.replace(0, np.nan)
print(R[R.nval >= 20].sort_values("tasa", ascending=False).head(10).to_string(index=False))
print("\n%s" % ("OK" if True else ""))
