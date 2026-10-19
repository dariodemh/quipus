"""Tarea 1: tríos [x,c,x-c] y variantes en TODO el corpus (651 quipus), con tolerancia 0 y ±1.
Ventana = 3 cuerdas L0 presentes (valor>0) consecutivas dentro de un grupo. Tres posiciones de la suma:
  S1: v1 = v2+v3  ([x,c,x-c] y [x,x-c,c])   S2: v2 = v1+v3  ([c,x,x-c])   S3: v3 = v1+v2  ([c,x-c,x])
Nulos (semilla fija; la unidad es el quipu):
  N1 = barajar los valores presentes de L0 del quipu entre sus posiciones (conserva grupos y multiconjunto, incluida c repetida)
  N2 = (solo grupos de exactamente 3 cuerdas presentes) barajar cada COLUMNA (posición 1,2,3) entre los grupos: conserva el
       marginal de x, de c y de x-c, y rompe solo el emparejamiento por fila (el más estricto).
BH-FDR entre quipus testables (nulo con varianza>0), por tolerancia y nulo."""
import numpy as np, pandas as pd
from collections import Counter
from comun import *
B = 2000
c, q = cargar(); qi = q.set_index("kfg")
def bh(p):
    p = np.asarray(p); n = len(p); o = np.argsort(p); r = np.empty(n); r[o] = np.arange(1, n+1)
    qv = p*n/r; qs = np.minimum.accumulate(qv[o][::-1])[::-1]; out = np.empty(n); out[o] = np.minimum(qs, 1); return out
def hits(v, W, tol):
    a, b, d = v[W[:,0]], v[W[:,1]], v[W[:,2]]
    s1 = np.abs(a-(b+d)) <= tol; s2 = np.abs(b-(a+d)) <= tol; s3 = np.abs(d-(a+b)) <= tol
    return s1, s2, s3
rows = []; det = []
for i, (k, d) in enumerate(c[(c.nivel == 0)].groupby("kfg", sort=False)):
    d = d.sort_values("orden"); d = d[d.pres & (d.valor > 0)]
    v = d.valor.values.astype(np.int64); g = d.grupo.values; n = len(v)
    W = []
    for j in range(n-2):
        if g[j] == g[j+2]: W.append((j, j+1, j+2))
    W = np.array(W, dtype=int).reshape(-1, 3)
    # grupos de exactamente 3
    gs = [np.where(g == x)[0] for x in np.unique(g)]; T3 = np.array([x for x in gs if len(x) == 3], dtype=int).reshape(-1, 3)
    rng = np.random.default_rng(1000+i)
    res = dict(kfg=k, procedencia=qi.loc[k, "procedencia"], n_cuerdas=n, n_ventanas=len(W), n_trios3=len(T3))
    for tol in (0, 1):
        if len(W):
            s = hits(v, W, tol); res[f"obs_t{tol}"] = int(sum(x.sum() for x in s)); res[f"S1_t{tol}"], res[f"S2_t{tol}"], res[f"S3_t{tol}"] = [int(x.sum()) for x in s]
            N = np.empty(B)
            for b in range(B):
                vv = rng.permutation(v); N[b] = sum(x.sum() for x in hits(vv, W, tol))
            res[f"E1_t{tol}"] = N.mean(); res[f"sd1_t{tol}"] = N.std(); res[f"p1_t{tol}"] = (1+(N >= res[f"obs_t{tol}"]).sum())/(B+1)
        else:
            res[f"obs_t{tol}"] = 0; res[f"p1_t{tol}"] = 1.0; res[f"sd1_t{tol}"] = 0.0; res[f"E1_t{tol}"] = 0
        # N2 sobre los grupos de 3
        if len(T3) >= 4:
            M = v[T3]; W3 = np.array([[0, 1, 2]]*len(T3))
            ob = sum(x.sum() for x in hits(M.reshape(-1), np.arange(3*len(T3)).reshape(-1, 3), tol))
            N = np.empty(B)
            for b in range(B):
                M2 = np.stack([rng.permutation(M[:, j]) for j in range(3)], 1)
                N[b] = sum(x.sum() for x in hits(M2.reshape(-1), np.arange(3*len(T3)).reshape(-1, 3), tol))
            res[f"obs3_t{tol}"] = int(ob); res[f"E2_t{tol}"] = N.mean(); res[f"sd2_t{tol}"] = N.std(); res[f"p2_t{tol}"] = (1+(N >= ob).sum())/(B+1)
        else:
            res[f"obs3_t{tol}"] = 0; res[f"p2_t{tol}"] = 1.0; res[f"sd2_t{tol}"] = 0.0; res[f"E2_t{tol}"] = 0
    # detalle de los hits (tol 1) para tabla
    if len(W):
        s1, s2, s3 = hits(v, W, 1)
        for w, a1, a2, a3 in zip(W, s1, s2, s3):
            for pat, f in (("S1", a1), ("S2", a2), ("S3", a3)):
                if f:
                    x = v[w]; tot = x[{"S1": 0, "S2": 1, "S3": 2}[pat]]; part = sorted(np.delete(x, {"S1": 0, "S2": 1, "S3": 2}[pat]))
                    det.append(dict(kfg=k, patron=pat, i0=int(w[0]), v1=int(x[0]), v2=int(x[1]), v3=int(x[2]), exacto=int(abs(tot-sum(part)) == 0), menor=int(part[0]), grupo=int(g[w[0]])))
    rows.append(res)
R = pd.DataFrame(rows)
for tol in (0, 1):
    for nl in ("1", "2"):
        t = R[f"sd{nl}_t{tol}"] > 0; R[f"q{nl}_t{tol}"] = 1.0; R.loc[t, f"q{nl}_t{tol}"] = bh(R.loc[t, f"p{nl}_t{tol}"])
R.to_csv(OUT/"trios_por_quipu.csv", index=False); pd.DataFrame(det).to_csv(OUT/"trios_detalle.csv", index=False)
for tol in (0, 1):
    for nl in ("1", "2"):
        t = R[f"sd{nl}_t{tol}"] > 0
        print(f"tol{tol} N{nl}: testables {t.sum()} p<.05 {(R[f'p{nl}_t{tol}']<.05).sum()} (esp {0.05*t.sum():.1f}) q<.05 {(R[f'q{nl}_t{tol}']<.05).sum()}")
        s = R[(R[f"q{nl}_t{tol}"] < .05)]
        print("   ", dict(Counter(s.procedencia)), list(s.kfg))
