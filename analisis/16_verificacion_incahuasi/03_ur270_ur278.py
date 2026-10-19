"""Afirmacion 4: UR270 vs UR278 por columnas.
Por grupo g de UR270: S_j = valor(colgante_j) + valor(primera subsidiaria s1 de colgante_j), j=1..9 (orden).
Control: solo colgantes. Por cada grupo de UR270 se busca el grupo de UR278 con mas columnas iguales (+-1, misma posicion j).
Nulo: permutar las 9 sumas dentro de cada grupo de UR270 (10 000 replicas, semilla 16); p por grupo = P(max_null >= obs).
Tambien se reporta el numero de grupos con >=6 de 9 (contado tras el nulo global)."""
import numpy as np
from lib import load, SEED

c = load()
N_REP = 10000
rng = np.random.default_rng(SEED)


def grupos_vectores(kfg, con_sub=True):
    q = c[c.kfg == kfg].sort_values("orden")
    out = {}
    for g, gg in q.groupby("grupo", sort=False):
        col = gg[gg.nivel == 0].sort_values("orden")
        if len(col) < 9:
            continue
        col = col.iloc[:9]
        vec = []
        for _, r in col.iterrows():
            v = r.valor_n if r.valor_n == r.valor_n else 0.0
            if con_sub:
                s1 = gg[gg.cuerda == r.cuerda + "s1"]
                if len(s1):
                    v += s1.valor_n.iloc[0]
            vec.append(v)
        out[g] = np.array(vec)
    return out


def ur278_vectores():
    q = c[c.kfg == "UR278"].sort_values("orden")
    out = {}
    for g, gg in q.groupby("grupo", sort=False):
        col = gg[gg.nivel == 0].sort_values("orden")
        if len(col) >= 9:
            out[g] = col.iloc[:9].valor_n.fillna(0).values
    return out


def best_match(v, targets, tol=1):
    best, bg = -1, None
    for tg, tv in targets.items():
        m = int(np.sum(np.abs(v - tv) <= tol))
        if m > best:
            best, bg = m, tg
    return best, bg


T = ur278_vectores()
for con_sub, label in [(True, "colgante+s1"), (False, "control solo colgantes")]:
    U = grupos_vectores("UR270", con_sub)
    obs = {g: best_match(v, T) for g, v in U.items()}
    print(f"== {label}: grupos UR270 con >=9 colgantes = {len(U)}; UR278 grupos = {len(T)}")
    n6 = sum(1 for m, _ in obs.values() if m >= 6)
    print("   mejor (matches, grupo UR278) por grupo UR270:", {g: obs[g] for g in obs})
    print(f"   grupos con >=6/9: {n6}")
    if con_sub:
        # nulo: permutar las 9 sumas dentro de cada grupo
        nulls = np.zeros((N_REP, len(U)))
        keys = list(U.keys())
        for r in range(N_REP):
            for i, g in enumerate(keys):
                nulls[r, i] = best_match(rng.permutation(U[g]), T)[0]
        for i, g in enumerate(keys):
            m = obs[g][0]
            p = (np.sum(nulls[:, i] >= m) + 1) / (N_REP + 1)
            print(f"   g{g}: obs={m}/9 -> {obs[g][1]}  nulo media={nulls[:, i].mean():.2f}  p={p:.4f}")
        null_n6 = (nulls >= 6).sum(axis=1)
        print(f"   nulo: numero de grupos >=6/9 medio={null_n6.mean():.2f}, P(>= {n6})={(np.sum(null_n6 >= n6)+1)/(N_REP+1):.4f}")
        print("   vector g0:", U[keys[0]].astype(int).tolist() if keys else None)
    # ejemplo pedido
    if con_sub and 0 in U:
        print("   ejemplo UR270 g0:", U[0].astype(int).tolist(), "UR278 g21:", T[21].astype(int).tolist() if 21 in T else None)
