"""Control de 02: el nulo de 02 permuta los valores de A, y eso no conserva la distribución de magnitud de los totales
cuando A tiene aritmética interna (en UR255 el total del grupo es x + 15, siempre en la franja 100-250). Aquí se
repiten las pruebas de cabeza de 02 (p_e <= 0,005) con un nulo del lado de B: cada valor anudado de B se sustituye por
uno de los 40 valores más cercanos en escala log del resto del archivo (sin A ni B), como en 01. Los agregados de A
quedan fijos. 5000 réplicas. Salida: agregados_control_magnitud.csv
"""
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13021
NPERM = 5000
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
c["cprinc"] = c.color.str.split(r"[(\s]", regex=True).str[0]
c["pend"] = c.cuerda.str.extract(r"^(p\d+)")[0]
# reutiliza indices() y agregados() de 02 sin ejecutar su búsqueda: se copian por texto
src = open(C.AQUI / "02_agregados.py", encoding="utf-8").read()
ns = {"np": np, "pd": pd, "C": C, "c": c}
exec(src[src.index("def indices"):src.index("def cuenta")], ns)

D = pd.read_csv(C.AQUI / "agregados_pruebas.csv")
top = D[(D.p_e <= 0.005) & (D.exactos >= 2)].copy()
rng = np.random.default_rng(SEED)
P = c[c.pres]
pool_all = {k: np.unique(P[P.kfg == k].valor.to_numpy()) for k in C.ARCHIVO}
filas = []
for r in top.itertuples():
    s = c[c.kfg == r.A]
    ag = ns["agregados"](s.valor.where(s.pres, 0).to_numpy(), ns["indices"](s), s)[r.tipo]
    vb = P[P.kfg == r.B].valor.to_numpy()
    obs = int(np.isin(ag, vb).sum())
    pool = np.concatenate([pool_all[k] for k in C.ARCHIVO if k not in (r.A, r.B)])
    pool = pool[pool > 0]
    f = C.vecinos_magnitud(pool, rng)
    nul = np.array([np.isin(ag, f(vb)).sum() for _ in range(NPERM)])
    filas.append(dict(A=r.A, tipo=r.tipo, B=r.B, exactos=obs, p_nulo_A=r.p_e, nulo_B_media=nul.mean(),
                      p_nulo_B=(np.sum(nul >= obs) + 1) / (NPERM + 1)))
F = pd.DataFrame(filas)
F["q_nulo_B"] = C.bh(F.p_nulo_B)
F["p_max_ambos"] = F[["p_nulo_A", "p_nulo_B"]].max(axis=1)
F = F.sort_values("p_max_ambos")
F.to_csv(C.AQUI / "agregados_control_magnitud.csv", index=False, float_format="%.4g")
pd.set_option("display.width", 200)
print(F.to_string(index=False))
