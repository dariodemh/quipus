"""Generalización de R7: grupo 'cierra' si su PRIMERA cuerda presente = suma del resto de cuerdas de nivel 0 del grupo (>=3 presentes)
(variante con subsidiarias: + valores de subsidiarias, y variante 'resta encadenada': existe a=b+c entre tres cuerdas cualesquiera del grupo).
Tol 0/1/2. Nulo N1: barajar valores presentes de L0 entre posiciones del quipu (grupos fijos). B=2000. Incahuasi (JC, UR255-280) + resto del corpus
(se reportan solo q<.05). BH sobre quipus testables."""
import numpy as np, pandas as pd, itertools
from comun import *
B = 2000
c, q = cargar(); qi = q.set_index("kfg")
def bh(p):
    p = np.asarray(p); n = len(p); o = np.argsort(p); r = np.empty(n); r[o] = np.arange(1, n+1)
    qs = np.minimum.accumulate((p*n/r)[o][::-1])[::-1]; out = np.empty(n); out[o] = np.minimum(qs, 1); return out
rows = []
for i, (k, d) in enumerate(c[c.nivel == 0].groupby("kfg", sort=False)):
    d = d.sort_values("orden"); d = d[d.pres & (d.valor > 0)]
    v = d.valor.values.astype(np.int64); g = d.grupo.values
    if len(v) < 6: continue
    starts = np.r_[0, np.where(np.diff(g) != 0)[0]+1, len(v)]; sizes = np.diff(starts); el = np.where(sizes >= 3)[0]
    if len(el) == 0: continue
    S = starts[el]; E_ = starts[el+1]
    def stat(v, tol):
        n = 0
        for s, e in zip(S, E_):
            seg = v[s:e]
            if abs(seg[0]-seg[1:].sum()) <= tol: n += 1
        return n
    def stat_any(v, tol=0):
        n = 0
        for s, e in zip(S, E_):
            seg = v[s:e]
            if len(seg) > 12: continue
            ok = False
            for a_, b_, c_ in itertools.combinations(range(len(seg)), 3):
                x = seg[[a_, b_, c_]]; m = x.max(); 
                if m == x.sum()-m and m > 0: ok = True; break
            n += ok
        return n
    rng = np.random.default_rng(2000+i); res = dict(kfg=k, procedencia=qi.loc[k, "procedencia"], grupos_elegibles=len(el))
    for tol in (0, 1, 2):
        ob = stat(v, tol); N = np.array([stat(rng.permutation(v), tol) for _ in range(B)])
        res[f"primera_t{tol}"] = ob; res[f"E_t{tol}"] = N.mean(); res[f"p_t{tol}"] = (1+(N >= ob).sum())/(B+1); res[f"sd_t{tol}"] = N.std()
    ob = stat_any(v); N = np.array([stat_any(rng.permutation(v)) for _ in range(300)])
    res["any3"] = ob; res["E_any3"] = N.mean(); res["p_any3"] = (1+(N >= ob).sum())/301
    rows.append(res)
R = pd.DataFrame(rows)
for tol in (0, 1, 2):
    t = R[f"sd_t{tol}"] > 0; R[f"q_t{tol}"] = 1.0; R.loc[t, f"q_t{tol}"] = bh(R.loc[t, f"p_t{tol}"])
R.to_csv(OUT/"cierre_primera_por_quipu.csv", index=False)
pd.set_option("display.width", 250)
for tol in (0, 1, 2):
    t = R[f"sd_t{tol}"] > 0; s = R[R[f"q_t{tol}"] < .05]
    print(f"tol {tol}: testables {t.sum()} p<.05 {(R[f'p_t{tol}']<.05).sum()} (esp {.05*t.sum():.1f}) q<.05 {len(s)} ; no Incahuasi: {list(s[s.procedencia!='Incahuasi'].kfg)}")
print(R[R.procedencia == "Incahuasi"][["kfg", "grupos_elegibles", "primera_t0", "E_t0", "q_t0", "primera_t1", "q_t1", "primera_t2", "E_t2", "q_t2", "any3", "E_any3", "p_any3"]].round(3).to_string())
