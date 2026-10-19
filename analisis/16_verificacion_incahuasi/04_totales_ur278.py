"""Afirmacion 5: suma de cuerdas por grupo de UR278 vs cabeceras de UR266 (mismo orden).
Estadistico: para cada cabecera de UR266 (registros sep A, con valor) se buscan los grupos de UR278 cuya suma coincide
(exacta, o +-1). Se toman solo cabeceras con UNA coincidencia (unicidad) y se mide tau de Kendall entre el indice de
cabecera y el indice de grupo. Evitamos el emparejamiento greedy (que fuerza tau=1 por construccion).
Nulo: permutar las sumas de UR278 entre grupos (10 000 replicas, semilla 16): distribucion de (n_pares, tau).
p_cuenta = P(n >= obs); p_mono = P(n >= obs y tau = 1) en el nulo."""
import numpy as np
from scipy.stats import kendalltau
from lib import load, registros, SEED

c = load()
N_REP = 10000
rng = np.random.default_rng(SEED)

q = c[c.kfg == "UR278"].sort_values("orden")
sums_all = np.array([gg.valor_n.fillna(0).sum() for _, gg in q.groupby("grupo", sort=False)], dtype=float)
sums_col = np.array([gg[gg.nivel == 0].valor_n.fillna(0).sum() for _, gg in q.groupby("grupo", sort=False)], dtype=float)
cab266 = [r["cab"] for r in registros(c, "UR266", "A")]
cab_idx = [i for i, x in enumerate(cab266) if x == x]


def matches(sums, tol):
    """Pares (i, k) unicos: cabecera i con exactamente un grupo k que iguala (+-tol)."""
    out = []
    for i in cab_idx:
        ks = [k for k, s in enumerate(sums) if abs(s - cab266[i]) <= tol]
        if len(ks) == 1:
            out.append((i, ks[0]))
    return out


def stat(sums, tol):
    p = matches(sums, tol)
    if len(p) < 2:
        return len(p), np.nan
    tau = kendalltau([a for a, _ in p], [b for _, b in p])[0]
    return len(p), tau


for label, sums in [("todas las cuerdas", sums_all), ("solo colgantes", sums_col)]:
    for tol in (0, 1):
        n_obs, tau_obs = stat(sums, tol)
        pl = matches(sums, tol)
        print(f"== {label}, tol=+-{tol}: pares unicos={n_obs}, tau={tau_obs:.3f}")
        print("   pares (cab_i, grupo_k, cab, suma):", [(i, k, int(cab266[i]), int(sums[k])) for i, k in pl])
        # nulo: cada grupo de UR278 se sustituye por la suma de su mismo numero de cuerdas, extraidas al azar
        # del conjunto de valores de todas las cuerdas de UR278 (conserva n cuerdas y magnitudes; rompe la identidad)
        cords_pool = q.valor_n.dropna().values
        sizes = [int(gg.valor_n.notna().sum()) for _, gg in q.groupby("grupo", sort=False)]
        null_n = np.empty(N_REP)
        null_mono = np.empty(N_REP, dtype=bool)
        for r in range(N_REP):
            fake = np.array([rng.choice(cords_pool, size=s, replace=False).sum() if s > 0 else 0.0 for s in sizes])
            n, t = stat(fake, tol)
            null_n[r] = n
            null_mono[r] = (n >= n_obs) and (not np.isnan(t)) and t >= 0.999999
        p_cnt = (np.sum(null_n >= n_obs) + 1) / (N_REP + 1)
        p_mono = (np.sum(null_mono) + 1) / (N_REP + 1)
        print(f"   nulo (sumas aleatorias de n cuerdas): n medio={null_n.mean():.2f}; p(n>=obs)={p_cnt:.4f}; p(n>=obs y tau=1)={p_mono:.4f}")
