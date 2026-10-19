"""Ataque 2. Nulos más duros para "cab(A_i) + cab(B_i) ∈ C".

(a) Nulo de desfase: A_i + B_{i+k}, k ≠ 0. Conserva magnitudes, autocorrelación y orden de ambas series;
    solo rompe la alineación. Si el efecto fuera de "magnitud parecida", aparecería también en k ≠ 0.
(b) Nulo de dígitos: se barajan entre registros solo las unidades (o unidades+decenas) de B. Conserva
    magnitud, millares y centenas, y por tanto la autocorrelación casi entera.
(c) Trasplante: pares (A', B') de quipus de OTROS archivos (Pachacamac, Ica, Leymebamba, Huaquerones, Nazca,
    Armatambo, Lima...) con cabeceras de magnitud parecida a UR273A (mediana ~450) y UR273B (~1300),
    alineados registro a registro igual (registro = grupo), y sus sumas buscadas en la unión UR266/275/269.
(d) Control negativo por archivo: la búsqueda completa de 01 (todos los pares, cabecera = primer anudado,
    destino = cada quipu del archivo + unión greedy de 3) dentro de cada archivo grande. ¿Cuántas
    "A+B = C" con p ≤ p_afirmación aparecen entre quipus que no tienen nada que ver?
Semilla 18. Salida: salida_02_nulos_duros.txt
"""
import itertools
import numpy as np
from scipy.stats import poisson
import lib18 as L

rng = np.random.default_rng(L.SEED + 2)
c, q = L.cargar()
out = open(L.AQUI / "salida_02_nulos_duros.txt", "w", encoding="utf-8")


def pr(*a):
    print(*a)
    print(*a, file=out)


S = L.diana(c, L.RES)
S269c = L.diana(c, ["UR269"], solo_cab=True)
CASOS = [("UR273A", "UR273B", S, "unión 266/275/269"), ("UR274A", "UR273B", S, "unión 266/275/269"),
         ("UR267A", "UR267B", S269c, "cabeceras UR269")]

pr("(a) Nulo de desfase k (aciertos exactos)")
for qa, qb, D, nom in CASOS:
    fila = {}
    for k in range(-8, 9):
        a, b = L.pares_ab(c, qa, qb, lag=k)
        fila[k] = (np.isin(a + b, D).sum(), len(a))
    otros = np.array([fila[k][0] for k in fila if k != 0])
    pr(f"  {qa}+{qb} → {nom}: k=0: {fila[0][0]}/{fila[0][1]}; k≠0 (16 desfases): media {otros.mean():.2f}, "
       f"máx {otros.max()}; P(k≠0 ≥ k=0) = {np.mean(otros >= fila[0][0]):.3f}")
    pr("     " + " ".join(f"{k}:{v[0]}" for k, v in fila.items()))

pr("\n(b) Nulo de dígitos (10 000 réplicas): barajar entre registros las últimas cifras de B")
for qa, qb, D, nom in CASOS:
    a, b = L.pares_ab(c, qa, qb)
    obs = np.isin(a + b, D).sum()
    for mod in (10, 100):
        nul = np.array([np.isin(a + (b - b % mod + rng.permutation(b % mod)), D).sum() for _ in range(10000)])
        pr(f"  {qa}+{qb} → {nom}, b mod {mod}: obs {obs}, nulo media {nul.mean():.2f} máx {nul.max()}, "
           f"p = {L.p_emp(nul, obs):.4f}")

# (c) Trasplante con magnitud emparejada
pr("\n(c) Trasplante: pares de quipus de otros archivos con magnitudes como UR273A/B, sumas buscadas en la unión")
inca = set(q[q.procedencia == "Incahuasi"].kfg)
otros_k = [k for k in q.kfg if k not in inca]
cab = {}
for k in otros_k:
    x = L.registros(c, k).x.to_numpy()
    if np.sum(~np.isnan(x)) >= 10:
        cab[k] = x
a0, b0 = L.pares_ab(c, "UR273A", "UR273B")
ma, mb = np.median(a0), np.median(b0)
candA = [k for k, x in cab.items() if 0.5 * ma <= np.nanmedian(x) <= 2 * ma]
candB = [k for k, x in cab.items() if 0.5 * mb <= np.nanmedian(x) <= 2 * mb]
res = []
for ka in candA:
    for kb in candB:
        if ka == kb:
            continue
        A, B = cab[ka], cab[kb]
        n = min(len(A), len(B))
        ok = ~np.isnan(A[:n]) & ~np.isnan(B[:n])
        a, b = A[:n][ok].astype(np.int64), B[:n][ok].astype(np.int64)
        if len(a) < 8:
            continue
        h = np.isin(a + b, S).sum()
        E = L.esperado_perm(a, b, S)
        res.append((poisson.sf(h - 1, E), h, len(a), E, ka, kb))
res.sort()
pr(f"  candidatos A (mediana {ma:.0f}±×2): {len(candA)}; B (mediana {mb:.0f}±×2): {len(candB)}; pares con ≥8 registros: {len(res)}")
if res:
    hs = np.array([r[1] / r[2] for r in res])
    pr(f"  fracción de aciertos: media {hs.mean():.3f} (UR273A+B: {8 / 18:.3f}); máx {hs.max():.3f}")
    pr(f"  pares con p ≤ 5.7e-5: {sum(r[0] <= 5.7e-5 for r in res)}; con p ≤ 1e-3: {sum(r[0] <= 1e-3 for r in res)}; "
       f"con ≥8 aciertos: {sum(r[1] >= 8 for r in res)}")
    for r in res[:5]:
        pr(f"   p={r[0]:.2e} h={r[1]}/{r[2]} E={r[3]:.2f} {r[4]}+{r[5]}")

# (d) Búsqueda completa dentro de otros archivos
pr("\n(d) Búsqueda completa dentro de cada archivo (todos los pares × destinos de su archivo + unión greedy de 3)")
ARCHIVOS = ["Incahuasi", "Pachacamac", "Ica", "Leymebamba", "Huaquerones", "Nazca", "Armatambo, Huaca San Pedro"]
lima = ["near Lima", "Armatambo, Huaca San Pedro"]
for arch in ARCHIVOS:
    ks = sorted(q[q.procedencia == arch].kfg)
    reg = {k: L.registros(c, k).x.to_numpy() for k in ks}
    dst = {k: L.diana(c, [k]) for k in ks}
    ps, ntest = [], 0
    for qa, qb in itertools.combinations(ks, 2):
        A, B = reg[qa], reg[qb]
        n = min(len(A), len(B))
        ok = ~np.isnan(A[:n]) & ~np.isnan(B[:n])
        a, b = A[:n][ok].astype(np.int64), B[:n][ok].astype(np.int64)
        if len(a) < 8:
            continue
        Ssum = a[:, None] + b[None, :]
        dk = [k for k in ks if k not in (qa, qb)]
        mem = np.stack([np.isin(Ssum, dst[k]) for k in dk])
        E = mem.sum((1, 2)) / len(a)
        H = mem[:, np.arange(len(a)), np.arange(len(a))].sum(1)
        p = poisson.sf(H - 1, np.maximum(E, 1e-9))
        top = np.argsort(-H)[:3]
        mu = mem[top].any(0)
        pu = poisson.sf(mu[np.arange(len(a)), np.arange(len(a))].sum() - 1, max(mu.sum() / len(a), 1e-9))
        ntest += len(dk) + 1
        ps.append((min(p.min(), pu), qa, qb, int(H.max())))
    ps.sort()
    if not ps:
        pr(f"  {arch}: sin pares con ≥8 registros alineados")
        continue
    pr(f"  {arch}: {len(ks)} quipus, {len(ps)} pares con ≥8 registros, {ntest} pruebas; min p = {ps[0][0]:.2e} "
       f"({ps[0][1]}+{ps[0][2]}, {ps[0][3]} aciertos); pares con p ≤ 5.7e-5: {sum(x[0] <= 5.7e-5 for x in ps)}; "
       f"p ≤ 1e-3: {sum(x[0] <= 1e-3 for x in ps)}")
out.close()
