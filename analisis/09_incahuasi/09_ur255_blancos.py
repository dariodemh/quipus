"""UR255: ¿la cuerda 'neta' queda en blanco en la primera mitad? Registro = grupo con x (primera presente) y una cuerda 15. Neto presente si hay otra cuerda presente distinta de x y 15.
Test exacto de Fisher (grupos < 16 vs >= 16) y largo de las cuerdas en blanco intermedias."""
import pandas as pd
from scipy.stats import fisher_exact
from comun import *
c, q = cargar()
for k, cc in (("UR255", 15), ("UR267A", 15)):
    d = c[(c.kfg == k) & (c.nivel == 0)]; rows = []
    for g, gg in d.groupby("grupo", sort=False):
        p = gg[gg.pres & (gg.valor > 0)]; v = p.valor.tolist()
        if len(v) >= 2 and cc in v and v[0] != cc:
            neto = [w for w in v if w not in (v[0], cc)]
            ncords_blank = int((~(gg.pres & (gg.valor > 0))).sum())
            rows.append(dict(g=g, x=v[0], neto=bool(neto), blancas=ncords_blank))
    R = pd.DataFrame(rows); R["mitad"] = (R.g >= 16).map({False: "g<16", True: "g>=16"})
    t = pd.crosstab(R.mitad, R.neto); print(k, "registros", len(R)); print(t)
    if t.shape == (2, 2): print("Fisher p =", fisher_exact(t.values)[1])
bl = c[(c.kfg == "UR255") & (c.nivel == 0) & (c.valor == 0) & (c.nudos == "")]
print("UR255 cuerdas sin nudos:", len(bl), "largo mediana", pd.to_numeric(bl.largo, errors="coerce").median(), "| con largo>=20:", int((pd.to_numeric(bl.largo, errors="coerce") >= 20).sum()))
