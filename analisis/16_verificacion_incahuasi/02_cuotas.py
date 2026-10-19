"""Afirmacion 3: valor 'cuota' presente en casi todos los registros de cada quipu.
k_any = registros (grupos no separadores, sep A) con >=1 cuerda (colgante o subsidiaria del grupo) de valor exacto X.
Nulo: permutar los valores de todas las cuerdas no ausentes dentro del mismo quipu (conserva distribucion de valores
y estructura grupo/nivel), 10 000 replicas, semilla 16. Look-elsewhere: maximo de k_any sobre todos los valores del quipu."""
import numpy as np
from collections import Counter
from lib import load, registros, SEED

c = load()
N_REP = 10000
rng = np.random.default_rng(SEED)
CASOS = [("UR274A", 30), ("UR274B", 17), ("UR273B", 17), ("UR266", 47), ("UR275", 47),
         ("UR267A", 15), ("UR255", 15), ("UR267B", 10), ("UR256", 10)]


def k_any_fn(cords_by_rec, x):
    return sum(any(v == x for v in vals) for vals in cords_by_rec)


for kfg, x in CASOS:
    q = c[c.kfg == kfg].sort_values("orden")
    recs = registros(c, kfg, "A")
    rec_groups = [r["grupo"] for r in recs]
    cords_by_rec = []  # valores de todas las cuerdas del grupo (colgante + subsidiarias)
    col_by_rec = []    # solo colgantes
    after_by_rec = []  # cuerdas posteriores a la cabecera
    for g in rec_groups:
        gg = q[q.grupo == g]
        cords_by_rec.append(gg.valor_n.tolist())
        col_by_rec.append(gg[gg.nivel == 0].valor_n.tolist())
        con = gg[(gg.nivel == 0) & gg.tiene_nudos]
        if len(con):
            h = con.orden.iloc[0]
            after_by_rec.append(gg[gg.orden > h].valor_n.tolist())
        else:
            after_by_rec.append([])
    n = len(recs)
    obs_any = k_any_fn(cords_by_rec, x)
    obs_col = k_any_fn(col_by_rec, x)
    obs_after = k_any_fn(after_by_rec, x)
    # nulo: permutar valores no ausentes dentro del quipu
    present = q[~((q.valor_n == 0) & (~q.tiene_nudos))]
    idx = present.index.values
    vals = present.valor_n.values.copy()
    # mapa de posicion -> (registro) para reconstruir k_any sin pandas en el bucle
    pos_rec = {}
    for ri, g in enumerate(rec_groups):
        for ix in q[q.grupo == g].index:
            pos_rec.setdefault(ix, ri)
    rec_of = np.array([pos_rec.get(i, -1) for i in idx])
    null = np.empty(N_REP)
    for r in range(N_REP):
        p = rng.permutation(vals)
        hit = np.zeros(n, dtype=bool)
        m = (p == x) & (rec_of >= 0)
        hit[rec_of[m]] = True
        null[r] = hit.sum()
    p_null = (np.sum(null >= obs_any) + 1) / (N_REP + 1)
    # nulo de maximo: max_v k_any(v) bajo permutacion, comparado con k_any(x) observado
    uv, inv = np.unique(vals, return_inverse=True)
    mask = rec_of >= 0
    rec_m, inv_m = rec_of[mask], inv[mask]
    null_max = np.empty(N_REP)
    for r in range(N_REP):
        perm = rng.permutation(inv_m)
        key = np.unique(rec_m * len(uv) + perm)
        cnts = np.bincount(key % len(uv), minlength=len(uv))
        null_max[r] = cnts.max()
    p_max = (np.sum(null_max >= obs_any) + 1) / (N_REP + 1)
    # look-elsewhere: conteo por valor
    cnt = Counter()
    for vals_r in cords_by_rec:
        for v in set(vals_r):
            if v == v and v != 0:
                cnt[v] += 1
    top = cnt.most_common(5)
    rank = sorted(cnt.values(), reverse=True).index(cnt[x]) + 1 if x in cnt else None
    print(f"{kfg} x={x}: registros={n} | any={obs_any} ({obs_any/n:.0%}) col={obs_col} after_cab={obs_after} | "
          f"nulo valor fijo media={null.mean():.2f} p={p_null:.4f} | nulo max media={null_max.mean():.1f} p_max={p_max:.4f} | rango del valor={rank} de {len(cnt)} | top5={top}")
