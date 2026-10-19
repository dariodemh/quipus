"""T3b. Detalle de las cuerdas fuera de tabla que coinciden con totales de columna o de fila (quipus con q<0,05 en T3)."""
import numpy as np
import pandas as pd
import comun as C

M, c, s = C.matrices()
d = pd.read_csv(C.OUT / "t3_por_quipu.csv")
filas = []
for t in ("fuera_col", "fuera_fila"):
    for k in d[d["q_" + t] < .05].kfg:
        m = M[k]
        V = np.nan_to_num(m["V"])
        cq = c[(c.kfg == k) & (c.nivel == 0)]
        en = set(m["O"].ravel())
        g0, g1 = m["grupos"].min(), m["grupos"].max()
        tc = V.sum(0)
        tf = V.sum(1)
        for r in cq[~cq.orden.isin(en) & (cq.v > 0)].itertuples():
            js = np.where(np.isclose(tc, r.v))[0] if t == "fuera_col" else np.where(np.isclose(tf, r.v) & ((~np.isnan(m["V"])).sum(1) >= 2))[0]
            if len(js):
                lugar = "antes" if r.grupo < g0 else ("después" if r.grupo > g1 else "intercalado")
                filas.append({"prueba": t, "kfg": k, "cuerda": r.cuerda, "grupo": r.grupo, "lugar": lugar, "union": r.union,
                              "color": r.ckey, "valor": r.v, "coincide_con": ("col " if t == "fuera_col" else "fila ") + ",".join(map(str, js)),
                              "R": m["R"], "K": m["K"]})
x = pd.DataFrame(filas)
x.to_csv(C.OUT / "t3b_cuerdas_resumen.csv", index=False)
print(x.to_string(index=False))
print(x.groupby("prueba").lugar.value_counts())


# ---------------------------------------------------------------- formato "fila + cuerda-total"
# Para cada fila de la tabla, la cuerda de un grupo unitario inmediatamente anterior y posterior.
# ¿= suma de la fila (exacta / a <=2 %)? Nulo: barajar los valores de las cuerdas unitarias del quipu entre sí (B=999).
def adyacentes(cq, m):
    sz = cq.groupby("grupo").size()
    uni = cq[cq.grupo.map(sz) == 1].set_index("grupo").v
    ant = np.array([uni.get(g - 1, np.nan) for g in m["grupos"]], float)
    pos = np.array([uni.get(g + 1, np.nan) for g in m["grupos"]], float)
    return ant, pos, uni


def aciertos(ts, x, tol):
    ok = ~np.isnan(x) & (ts > 0)
    return (ok & (np.abs(x - ts) <= tol * ts)).sum()


out = []
for i, k in enumerate(sorted(M)):
    m = M[k]
    cq = c[(c.kfg == k) & (c.nivel == 0) & (c.union != "T")]
    ant, pos, uni = adyacentes(cq, m)
    if np.isnan(ant).all() and np.isnan(pos).all():
        continue
    ts = np.where((~np.isnan(m["V"])).sum(1) >= 2, np.nansum(m["V"], 1), np.nan)
    rng = np.random.default_rng([C.SEED, 31, i])
    o = {"kfg": k, "R": m["R"], "K": m["K"], "n_unitarias": len(uni)}
    for lado, x in (("ant", ant), ("pos", pos)):
        o[lado + "_n"] = int((~np.isnan(x) & ~np.isnan(ts)).sum())
        for tol, nom in ((0, "exacta"), (.02, "2pc")):
            obs = aciertos(ts, x, tol)
            u = uni.dropna().to_numpy()
            nul = []
            for _ in range(999):
                # reasignar valores de cuerdas unitarias al azar conservando qué filas tienen vecina unitaria
                y = x.copy()
                y[~np.isnan(x)] = rng.choice(u, (~np.isnan(x)).sum(), replace=True) if len(u) else np.nan
                nul.append(aciertos(ts, y, tol))
            o[f"{lado}_{nom}"], o[f"e_{lado}_{nom}"] = obs, np.mean(nul)
            o[f"p_{lado}_{nom}"] = C.pemp(obs, nul) if obs > 0 else np.nan
    out.append(o)
f = pd.DataFrame(out)
for col in [x for x in f.columns if x.startswith("p_")]:
    f["q" + col[1:]] = C.bh(f[col])
f.to_csv(C.OUT / "t3b_fila_total.csv", index=False)
qs = [x for x in f.columns if x.startswith("q_")]
sig = f[(f[qs] < .05).any(axis=1)]
print(f"\nFormato fila + cuerda-total (grupo unitario adyacente): {len(f)} tablas con unitarias adyacentes; "
      f"{len(sig)} con q<0,05 en alguna variante")
print(sig[["kfg", "R", "K", "ant_n", "ant_exacta", "ant_2pc", "e_ant_2pc", "pos_n", "pos_exacta", "pos_2pc", "e_pos_2pc"] + qs].round(3).to_string(index=False))
