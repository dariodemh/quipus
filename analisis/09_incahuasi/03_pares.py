"""Tarea 3: (a) búsqueda en TODO el corpus de pares de quipus que comparten valores grandes (>=50) más allá de lo esperado;
(b) alineación cuerda a cuerda de las parejas Incahuasi (UR255-UR267A, UR256-UR267B, UR266-UR275) con nulo de alineación.
(a) Esperado bajo independencia: E = sum_{v en A} min(1, nB * p(v)), p(v)=frecuencia por cuerda de v en el corpus (valores>=50); cola de Poisson; BH sobre pares."""
import numpy as np, pandas as pd, itertools
from scipy.stats import poisson
from collections import Counter
from comun import *
c, q = cargar(); qi = q.set_index("kfg")
big = c[c.pres & (c.valor >= 50)]
S = {k: set(g.valor) for k, g in big.groupby("kfg")}; cnt = {k: Counter(g.valor) for k, g in big.groupby("kfg")}
tot = sum(sum(x.values()) for x in cnt.values()); pv = Counter(); [pv.update(x) for x in cnt.values()]
nB = {k: len(s) for k, s in S.items()}
ks = [k for k in S if len(S[k]) >= 8]; rows = []
for a, b in itertools.combinations(ks, 2):
    inter = S[a] & S[b]
    if len(inter) < 5: continue
    E = sum(min(1, nB[b]*pv[v]/tot) for v in S[a]); 
    rows.append(dict(a=a, b=b, comp=len(inter), nA=nB[a], nB=nB[b], E=E, p=poisson.sf(len(inter)-1, max(E, 1e-9))))
P = pd.DataFrame(rows)
m = len(ks)*(len(ks)-1)//2; P["p_bonf"] = (P.p*m).clip(upper=1)
P["procA"] = P.a.map(qi.procedencia); P["procB"] = P.b.map(qi.procedencia)
P = P.sort_values("p"); P.to_csv(OUT/"pares_corpus.csv", index=False)
print("pares probados", m, "con >=5 comunes", len(P), "Bonferroni<.05:", (P.p_bonf < .05).sum())
print(P[P.p_bonf < .05].head(40)[["a", "b", "comp", "nA", "nB", "E", "p_bonf", "procA", "procB"]].round(4).to_string())
# (b) alineación global
def align(a, b, tol=1):
    n, m = len(a), len(b); M = np.zeros((n+1, m+1)); T = np.zeros((n+1, m+1), int)
    M[:, 0] = -np.arange(n+1); M[0, :] = -np.arange(m+1); T[1:, 0] = 1; T[0, 1:] = 2
    for i in range(1, n+1):
        for j in range(1, m+1):
            d = abs(a[i-1]-b[j-1]); s = 3 if d == 0 else (1 if d <= tol else -1)
            o = (M[i-1, j-1]+s, M[i-1, j]-1, M[i, j-1]-1); t = int(np.argmax(o)); M[i, j] = o[t]; T[i, j] = t
    i, j, out = n, m, []
    while i > 0 or j > 0:
        t = T[i, j]
        if i > 0 and j > 0 and t == 0: out.append((i-1, j-1)); i -= 1; j -= 1
        elif i > 0 and (t == 1 or j == 0): out.append((i-1, None)); i -= 1
        else: out.append((None, j-1)); j -= 1
    return out[::-1], M[n, m]
def seq(k):
    d = c[(c.kfg == k) & (c.nivel == 0) & c.pres & (c.valor > 0)].sort_values("orden").reset_index(drop=True); return d
resum = []; filas = []
for A_, B_, cc in [("UR255", "UR267A", 15), ("UR256", "UR267B", 10), ("UR266", "UR275", 47)]:
    a, b = seq(A_), seq(B_); al, sc = align(a.valor.values, b.valor.values)
    ex = sum(1 for i, j in al if i is not None and j is not None and a.valor[i] == b.valor[j] and a.valor[i] != cc)
    pm = sum(1 for i, j in al if i is not None and j is not None and abs(a.valor[i]-b.valor[j]) <= 1 and a.valor[i] != cc and a.valor[i] >= 30)
    rng = np.random.default_rng(5); N = []
    for _ in range(300):
        bb = b.valor.values.copy(); rng.shuffle(bb); al2, _s = align(a.valor.values, bb)
        N.append(sum(1 for i, j in al2 if i is not None and j is not None and abs(a.valor[i]-bb[j]) <= 1 and a.valor[i] != cc and a.valor[i] >= 30))
    p = (1+(np.array(N) >= pm).sum())/301
    nx_a = int(((a.valor != cc) & (a.valor >= 30)).sum()); nx_b = int(((b.valor != cc) & (b.valor >= 30)).sum())
    resum.append(dict(par=f"{A_}-{B_}", c=cc, cuerdas_A=len(a), cuerdas_B=len(b), n_valores_ge30_A=nx_a, n_valores_ge30_B=nx_b, alineados_exactos=ex, alineados_pm1=pm, nulo_media=np.mean(N), nulo_max=max(N), p=p))
    for i, j in al:
        filas.append(dict(par=f"{A_}-{B_}", ordenA=None if i is None else int(a.orden[i]), cuerdaA=None if i is None else a.cuerda[i], grupoA=None if i is None else int(a.grupo[i]), valA=None if i is None else int(a.valor[i]), colA=None if i is None else a.color[i],
                          ordenB=None if j is None else int(b.orden[j]), cuerdaB=None if j is None else b.cuerda[j], grupoB=None if j is None else int(b.grupo[j]), valB=None if j is None else int(b.valor[j]), colB=None if j is None else b.color[j]))
F = pd.DataFrame(filas); F.to_csv(OUT/"alineacion_pares.csv", index=False)
R = pd.DataFrame(resum); R.to_csv(OUT/"alineacion_resumen.csv", index=False); print(R.round(4).to_string())
