"""Ataque 1. Jardín de senderos: corrección por todo el espacio de búsqueda de "cab(A_i) + cab(B_i) ∈ C".

Para cada configuración (par de quipus A<B del archivo de Incahuasi, definición de cabecera, quipu destino C)
se calcula el nº de aciertos exactos h y su esperanza EXACTA bajo el nulo de 13 (barajar B entre registros):
E = (1/n) Σ_i Σ_j 1[a_i + b_j ∈ C]. Puntuación = p de Poisson P(X ≥ h | E).
Familias:
  F13   = lo que 13 probó de verdad (8 parejas de 04_componentes × destinos {unión 266+275+269, 266, 275, 269}).
  Famplia = todos los pares (A,B) con ≥8 registros alineados × 3 definiciones de cabecera (primer anudado, máximo,
          suma de colgantes) × destino = cada quipu del archivo (todas sus cuerdas, o solo cabeceras) + la unión
          de los 3 destinos con más aciertos (elección a posteriori, como hizo 13 al unir 266+275+269).
Corrección: se repite TODA la búsqueda con B barajado en cada configuración (1000 réplicas) y se toma el mínimo p
de la familia; p corregido = P_nulo(min p ≤ p observado de la afirmación). Semilla 18.
Salida: salida_01_jardin.txt
"""
import itertools
import time
import numpy as np
from scipy.stats import poisson
import lib18 as L

import sys
NREP = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
rng = np.random.default_rng(L.SEED + 1)
c, q = L.cargar()
ARCH = sorted(q[q.procedencia == "Incahuasi"].kfg)
DEFS = ["primero", "max", "suma"]

# destinos: todas las cuerdas y solo cabeceras
dest_all = {k: L.diana(c, [k]) for k in ARCH}
dest_cab = {k: L.diana(c, [k], solo_cab=True) for k in ARCH}
UNION = L.diana(c, L.RES)
regs = {(k, d): L.registros(c, k, d).x.to_numpy() for k in ARCH for d in DEFS}


def prep(qa, qb, d, dests):
    A, B = regs[(qa, d)], regs[(qb, d)]
    n = min(len(A), len(B))
    a, b = A[:n], B[:n]
    ok = ~np.isnan(a) & ~np.isnan(b)
    a, b = a[ok].astype(np.int64), b[ok].astype(np.int64)
    if len(a) < 8:
        return None
    Ssum = a[:, None] + b[None, :]
    mem = np.stack([np.isin(Ssum, S) for S in dests])          # (ndest, n, n)
    E = mem.sum((1, 2)) / len(a)
    return mem, E, len(a)


def score(mem, E, n, perm, greedy_k):
    """p mínimo sobre destinos (y unión greedy de los greedy_k primeros destinos de 'todas las cuerdas')."""
    ar = np.arange(n)
    H = mem[:, ar, perm].sum(1)
    p = poisson.sf(H - 1, np.maximum(E, 1e-9))
    p[E == 0] = np.where(H[E == 0] > 0, 0.0, 1.0)  # no ocurre con E=0 salvo fuera del soporte
    best = p.min()
    if greedy_k:
        top = np.argsort(-H[:greedy_k])[:3]
        mu = mem[top].any(0)
        hu, eu = mu[ar, perm].sum(), mu.sum() / n
        best = min(best, poisson.sf(hu - 1, eu))
    return best


out = open(L.AQUI / "salida_01_jardin.txt", "w", encoding="utf-8")


def pr(*a):
    print(*a)
    print(*a, file=out)


# --- afirmación tal como está escrita
mem, E, n = prep("UR273A", "UR273B", "primero", [UNION])
h0 = mem[0, np.arange(n), np.arange(n)].sum()
p_claim = poisson.sf(h0 - 1, E[0])
pr(f"Afirmación: UR273A+UR273B → unión 266/275/269: h={h0} de n={n}, E_perm={E[0]:.3f}, p_Poisson={p_claim:.2e}")
mem, E, n = prep("UR267A", "UR267B", "primero", [dest_cab["UR269"], L.diana(c, ["UR269"])])
h = mem[:, np.arange(n), np.arange(n)].sum(1)
p267 = poisson.sf(h - 1, E)
pr(f"UR267A+UR267B → UR269 cabeceras: h={h[0]}, E={E[0]:.2f}, p={p267[0]:.2e};  → UR269 todas las cuerdas: h={h[1]}, E={E[1]:.2f}, p={p267[1]:.2e}")

# --- F13: lo que 13 probó
F13 = [("UR267A", "UR267B"), ("UR255", "UR256"), ("UR267A", "UR256"), ("UR255", "UR267B"),
       ("UR273A", "UR273B"), ("UR274A", "UR274B"), ("UR273A", "UR274B"), ("UR274A", "UR273B")]
d13 = [UNION] + [L.diana(c, [k]) for k in L.RES]
conf13 = [x for x in (prep(a, b, "primero", d13) for a, b in F13) if x is not None]
obs13 = min(score(m, e, n, np.arange(n), 0) for m, e, n in conf13)
nul13 = np.array([min(score(m, e, n, rng.permutation(n), 0) for m, e, n in conf13) for _ in range(NREP)])
pr(f"\nF13 ({len(conf13)} pares × {len(d13)} destinos = {len(conf13) * len(d13)} pruebas): min p obs={obs13:.2e}; "
   f"P_nulo(min p ≤ p_afirmación) = {L.p_emp(-nul13, -p_claim):.4f}")

# --- Familia amplia
t0 = time.time()
conf = []
for qa, qb in itertools.combinations(ARCH, 2):
    dk = [k for k in ARCH if k not in (qa, qb)]
    dests = [dest_all[k] for k in dk] + [dest_cab[k] for k in dk]
    for d in DEFS:
        x = prep(qa, qb, d, dests)
        if x is not None:
            conf.append((qa, qb, d, len(dk)) + x)
pr(f"\nFamilia amplia: {len(conf)} configuraciones (par×definición) × ~{2 * (len(ARCH) - 2)} destinos + unión greedy "
   f"= {sum(2 * g + 1 for _, _, _, g, *_ in conf)} pruebas; preparación {time.time() - t0:.0f}s")
obs = [(score(m, e, n, np.arange(n), g), a, b, d) for a, b, d, g, m, e, n in conf]
obs.sort()
pr("10 mejores configuraciones en los datos reales (p mínimo sobre destinos):")
for p, a, b, d in obs[:10]:
    pr(f"   {a}+{b} [{d}]  p={p:.2e}")
nul = []
for r in range(NREP):
    nul.append(min(score(m, e, n, rng.permutation(n), g) for a, b, d, g, m, e, n in conf))
nul = np.array(nul)
pr(f"Nulo de la familia amplia ({NREP} réplicas): mediana min p={np.median(nul):.2e}, 5 %={np.quantile(nul, .05):.2e}")
pr(f"p corregido de la afirmación (UR273A+B, p={p_claim:.2e}) = P_nulo(min p ≤ p) = {L.p_emp(-nul, -p_claim):.4f}")
pr(f"p corregido de UR267A+B → cabeceras UR269 (p={p267[0]:.2e}) = {L.p_emp(-nul, -p267[0]):.4f}")
pr(f"Configuraciones reales con p ≤ p_afirmación: {sum(p <= p_claim for p, *_ in obs)}; "
   f"con p ≤ 1e-3: {sum(p <= 1e-3 for p, *_ in obs)} (esperadas bajo el nulo ≈ ver nulo)")
out.close()
