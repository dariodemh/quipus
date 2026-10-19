"""R7 'cierre intra-grupo' (sin posición): un grupo cumple si una cuerda = suma del resto del grupo (total == 2*max, >=3 cuerdas no nulas).
Nulo N2: barajar los valores de las cuerdas presentes de nivel 0 de todo el quipu (tamaños de grupo fijos). BH-FDR entre quipus.
También: en grupos de 3 cuerdas con cierre, constancia del sumando menor (patrón 'x, 15, x-15' de Incahuasi)."""
import numpy as np, pandas as pd
from collections import Counter
from pathlib import Path
from nucleo import cargar, bh
B = 2000
Qs, q = cargar(); q = q.set_index("kfg")
rows = []; glob_obs = 0; glob_null = np.zeros(B)
for i, (k, Q) in enumerate(Qs.items()):
    rng = np.random.default_rng(500 + i)
    a = Q["v"][Q["L0"]].copy(); pres = Q["pres"][Q["L0"]]; gs = Q["gs"]
    st = gs[:-1]
    def cuenta(a):
        tot = np.add.reduceat(a, st); mx = np.maximum.reduceat(a, st); nz = np.add.reduceat((a > 0).astype(int), st)
        return int(((tot == 2 * mx) & (nz >= 3)).sum())
    obs = cuenta(a)
    pi = np.where(pres)[0]; N = np.empty(B)
    for b in range(B):
        x = a.copy(); x[pi] = rng.permutation(a[pi]); N[b] = cuenta(x)
    glob_obs += obs; glob_null += N
    # constancia del sumando menor en cierres de 3 cuerdas
    menores = []
    for g in range(len(gs) - 1):
        s = np.sort(a[gs[g]:gs[g + 1]])
        if len(s) == 3 and s[0] > 0 and s[0] + s[1] == s[2]: menores.append(int(s[0]))
    c = Counter(menores).most_common(1)
    rows.append(dict(kfg=k, procedencia=q.loc[k, "procedencia"], n_grupos=len(gs) - 1, obs=obs, E=N.mean(), sd=N.std(),
                     p=(1 + (N >= obs).sum()) / (B + 1), cierres3=len(menores), menor_modal=c[0][0] if c else np.nan, menor_modal_n=c[0][1] if c else 0))
d = pd.DataFrame(rows); t = d.sd > 0
d["q"] = 1.0; d.loc[t, "q"] = bh(d.loc[t, "p"])
d.to_csv(Path(__file__).parent / "cierre_intragrupo.csv", index=False)
print("global obs", glob_obs, "E", glob_null.mean(), "sd", glob_null.std(), "p", (1 + (glob_null >= glob_obs).sum()) / (B + 1))
print("testables", t.sum(), "p<.05", (d.p < .05).sum(), "esperados", round(.05 * t.sum(), 1), "q<.05", (d.q < .05).sum(), " >=1 crudo", (d.obs > 0).sum(), "esperado nulo >=1 ~", round((d.E.clip(upper=1)).sum(), 0))
print(d[d.q < .05].sort_values("q")[["kfg", "procedencia", "n_grupos", "obs", "E", "q", "cierres3", "menor_modal", "menor_modal_n"]].to_string())
print(d[d.q < .05].procedencia.value_counts())
