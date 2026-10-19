"""Tarea 3 (detalle): (1) orden de c/n por quipu; (2) unión R/V en las parejas (y en el resto de pares significativos del corpus);
(3) descomposición completa de los registros emparejados: x = c + suma de un subconjunto del resto, usando A, B o A∪B, con nulo de registro desajustado."""
import numpy as np, pandas as pd, itertools
from collections import Counter
from comun import *
c, q = cargar(); qi = q.set_index("kfg")
D = pd.read_csv(OUT/"trios_detalle.csv"); D = D[(D.exacto == 1) & (D.patron == "S1")]
print("(1) orden en hits S1 exactos con partes distintas: c (parte menor) en pos 2 vs pos 3")
for k in ["UR255", "UR256", "UR267A", "UR267B", "UR269", "UR275"]:
    d = D[(D.kfg == k) & (D.v2 != D.v3) & (D.v1 >= 30)]; print(k, "pos2<pos3 (c segunda):", int((d.v2 < d.v3).sum()), "| c tercera:", int((d.v2 > d.v3).sum()))
# (2) unión
P = pd.read_csv(OUT/"pares_corpus.csv"); P = P[P.p_bonf < .05]
def uni(k):
    d = c[(c.kfg == k) & c.pres & (c.nivel == 0) & c.union.isin(["R", "V"])]; u = Counter(d.union); tot = sum(u.values())
    if tot < 10: return "?", 0.0
    m, n = u.most_common(1)[0]; return m, n/tot
allu = [uni(k) for k in qi.index]
uni_unif = [m for m, f in allu if f >= .85 and m in ("R", "V")]; pR = uni_unif.count("R")/len(uni_unif)
print("\n(2) quipus con union uniforme (>=85%% R o V) entre %d quipus (>=10 cuerdas L0 con R/V): %d ; R=%.2f V=%.2f ; P(dos al azar difieren)=%.2f" % (len(allu), len(uni_unif), pR, 1-pR, 2*pR*(1-pR)))
rows = []
for _, r in P.iterrows():
    a, b = uni(r.a), uni(r.b); rows.append(dict(a=r.a, b=r.b, ua=a[0], fa=round(a[1], 2), ub=b[0], fb=round(b[1], 2), opuestas=(a[0] != b[0]) and a[1] >= .85 and b[1] >= .85, uniformes=(a[1] >= .85 and b[1] >= .85)))
Pu = pd.DataFrame(rows); print(Pu.to_string()); Pu.to_csv(OUT/"pares_union.csv", index=False)
# (3) descomposición
F = pd.read_csv(OUT/"alineacion_pares.csv")
def recs(k):
    d = c[(c.kfg == k) & (c.nivel == 0) & c.pres & (c.valor > 0)]; return {g: gg.valor.tolist() for g, gg in d.groupby("grupo")}
def solve(x, cc, pool, kmax=3):
    t = x-cc; pool = sorted(set(v for v in pool if v < t and v != x))
    if t == 0: return True
    for r in range(1, kmax+1):
        for s in itertools.combinations(pool, r):
            if sum(s) == t: return True
    return False
rng = np.random.default_rng(3); out = []
for (A_, B_, cc) in [("UR255", "UR267A", 15), ("UR256", "UR267B", 10), ("UR266", "UR275", 47)]:
    RA, RB = recs(A_), recs(B_); f = F[(F.par == f"{A_}-{B_}") & F.valA.notna() & F.valB.notna() & (F.valA == F.valB) & (F.valA > cc*2)]
    pares = sorted(set((int(r.grupoA), int(r.grupoB), int(r.valA)) for _, r in f.iterrows()))
    sa = sb = su = 0; null_su = []; n = 0
    for ga, gb, x in pares:
        ra, rb = RA[ga], RB[gb]; n += 1
        sa += solve(x, cc, [v for v in ra if v != cc]); sb += solve(x, cc, [v for v in rb if v != cc]); su += solve(x, cc, [v for v in ra+rb if v != cc])
    for _ in range(200):
        s = 0
        for ga, gb, x in pares:
            gb2 = rng.choice(list(RB.keys())); s += solve(x, cc, [v for v in RA[ga]+RB[gb2] if v != cc])
        null_su.append(s)
    out.append(dict(par=f"{A_}-{B_}", registros_con_mismo_x=n, resueltos_solo_A=sa, resueltos_solo_B=sb, resueltos_A_union_B=su, nulo_union_media=np.mean(null_su), nulo_union_max=max(null_su), p_union=(1+(np.array(null_su) >= su).sum())/201))
O = pd.DataFrame(out); print("\n(3) x = c + subconjunto (<=3 cuerdas) del resto del registro\n", O.round(2).to_string()); O.to_csv(OUT/"pares_descomposicion.csv", index=False)
