"""04 · Fuera de muestra: las cinco pruebas (i)-(v) del diseño §4 de 18_equipo_rojo.

R1 congelada: cab(A_i) + cab(B_i) ∈ unión de cabeceras de UR266/UR275/UR269.
Registro = grupo de colgantes no separador (los grupos PK sin nudos separan);
cabecera = primer colgante anudado; un registro sin colgante anudado sigue ocupando
su posición (no se comprimen los huecos), como en lib18.registros.
La alineación es por posición ordinal de registro, que en UR273A/UR273B coincide con
el número de grupo (ambos tienen la misma lista de grupos) y en UR274A es la única que
cuadra (sus separadores están en otra posición).
Semilla 1804. ≥10 000 réplicas de permutación por prueba; donde el espacio de
permutaciones es pequeño (9 registros, 4 candidatos) se enumera exacto.

Salida: salida_04_fuera_muestra.txt.
"""
import itertools
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import poisson, fisher_exact

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "analisis/18_equipo_rojo"))
sys.path.insert(0, str(RAIZ / "analisis/13_sistema_incahuasi"))
import lib18 as L          # noqa: E402
import comun13 as C13      # noqa: E402  (bh; no se modifica nada de 13)

SEED = 1804
NREP = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
rng = np.random.default_rng(SEED)
c, q = L.cargar()
S = L.diana(c, L.RES, solo_cab=True)      # R1 congelada (cabeceras)
S_all = L.diana(c, L.RES)                 # definición original de 13 (todas las cuerdas)
S269c = L.diana(c, ["UR269"], solo_cab=True)

AQUI = Path(__file__).resolve().parent
out = open(AQUI / "salida_04_fuera_muestra.txt", "w", encoding="utf-8")


def pr(*a):
    print(*a)
    print(*a, file=out)


def serie(k):
    r = L.registros(c, k)
    return r.grupo.to_numpy(), r.x.to_numpy()


def alinear(qa, qb):
    """Series completas alineadas por posición ordinal de registro (huecos conservados)."""
    ga, A = serie(qa)
    gb, B = serie(qb)
    n = min(len(A), len(B))
    return ga[:n], A[:n], gb[:n], B[:n]


def pares(qa, qb):
    ga, A, gb, B = alinear(qa, qb)
    ok = ~np.isnan(A) & ~np.isnan(B)
    return ga[ok], A[ok].astype(np.int64), gb[ok], B[ok].astype(np.int64)


def p_exacto(a, b, D):
    """p exacto enumerando TODAS las permutaciones de b (solo n <= 9)."""
    D = set(np.asarray(D).tolist())
    obs = int(np.isin(a + b, list(D)).sum())
    cnt = 0
    tot = 0
    for pb in itertools.permutations(b.tolist()):
        tot += 1
        if np.isin(a + np.asarray(pb), list(D)).sum() >= obs:
            cnt += 1
    return obs, cnt / tot


def perm_dentro(a, b, D, reps=NREP):
    """Nulo: barajar b entre los registros de la misma mitad."""
    Dl = np.asarray(D)
    obs = int(np.isin(a + b, Dl).sum())
    nul = np.empty(reps, dtype=int)
    for r in range(reps):
        nul[r] = int(np.isin(a + rng.permutation(b), Dl).sum())
    E = L.esperado_perm(a, b, Dl)
    return obs, E, nul, L.p_emp(nul, obs)


def imprime_prueba(nom, obs, E, p, extra=""):
    pr(f"  {nom}: obs={obs}, E_nula={E:.3f}, p={p:.4f}{('; ' + extra) if extra else ''}")


# ---------------------------------------------------------------- (i) mitades 273
pr("=" * 78)
pr("(i) R1 por mitades de registros: UR273A+UR273B -> cabeceras UR266/275/269")
g, a, gb, b = pares("UR273A", "UR273B")
h = np.isin(a + b, S)
pr(f"  n válidos={len(a)}; aciertos={h.sum()}; E exacta={L.esperado_perm(a, b, S):.3f} "
   f"(con S=todas las cuerdas E={L.esperado_perm(a, b, S_all):.3f})")
pr(f"  n.º de grupo de los aciertos: {g[h].tolist()}")
corte = len(a) // 2
res_i = {}
pex_i = {}
for sl, nom in ((slice(0, corte), "1.ª mitad"), (slice(corte, None), "2.ª mitad")):
    obs, E, nul, p = perm_dentro(a[sl], b[sl], S)
    res_i[nom] = (obs, len(a[sl]), E, p)
    imprime_prueba(nom, f"{obs}/{len(a[sl])}", E, p)
    pe = p_exacto(a[sl], b[sl], S)[1]
    pex_i[nom] = pe
    pr(f"      p exacto por enumeración (9! = 362 880) = {pe:.5f}")
tab = [[int(h[:corte].sum()), int((~h[:corte]).sum())],
       [int(h[corte:].sum()), int((~h[corte:]).sum())]]
pr(f"  tabla 2x2 (acierto/no) = {tab}; Fisher bilateral p={fisher_exact(tab)[1]:.3f}")
p_i = max(pex_i.values())
pr(f"  prueba de conjunción (ambas mitades): p_IUT = max(p1,p2) = {p_i:.4f}")
for sl, nom in ((slice(0, corte), "1.ª"), (slice(corte, None), "2.ª")):
    obs, E, nul, p = perm_dentro(a[sl], b[sl], S_all)
    pr(f"  [sens. S=todas las cuerdas] {nom} mitad: obs={obs}/{len(a[sl])}, E={E:.3f}, p={p:.4f}")

# ---------------------------------------------------------------- (ii) 273A sin cabecera
pr("\n" + "=" * 78)
pr("(ii) Registros con UR273A sin cabecera: UR274A_i + UR273B_i")
ga, A, gb, B = alinear("UR273A", "UR273B")     # series completas (huecos incluidos)
g274, A274 = serie("UR274A")
if len(A274) < len(A):
    A274 = np.pad(A274, (0, len(A) - len(A274)), constant_values=np.nan)
Bpres = ~np.isnan(B)
# "sin cabecera" = ningún colgante anudado con valor >= 100 (solo cuota/resto)
sin_cab = np.array([
    not (c[(c.kfg == "UR273A") & (c.grupo == gg) & (c.nivel == 0) & c.pres].valor >= 100).any()
    for gg in ga])
cand = np.where(sin_cab & Bpres & ~np.isnan(A274[:len(A)]))[0]
pr(f"  registros totales alineados={len(A)}; con 273B presente={Bpres.sum()}; "
   f"con 273A sin cabecera={sin_cab.sum()}; candidatos (273B y 274A presentes)={len(cand)}")
ac = A274[cand].astype(np.int64)
bc = B[cand].astype(np.int64)
sumas = ac + bc
hit_c = np.isin(sumas, S)
hit_all = np.isin(sumas, S_all)
for i in range(len(cand)):
    pr(f"    pos {cand[i]} (grupo {int(ga[cand[i]])}): 274A={ac[i]:>4} + 273B={bc[i]:>4} = "
       f"{sumas[i]:>4}  en S_cab={bool(hit_c[i])}  en S_todas={bool(hit_all[i])}")
obs_ii = int(hit_c.sum())
# nulo exacto: asignar 4 valores de B distintos (de los 21 con B presente) a las 4 posiciones
pool = B[Bpres].astype(np.int64)
E_ii = sum(np.isin(x + pool, S).sum() / len(pool) for x in ac)
obs_cnt = 0
tot = 0
for pb in itertools.permutations(pool.tolist(), len(ac)):
    tot += 1
    if int(np.isin(ac + np.asarray(pb), S).sum()) >= obs_ii:
        obs_cnt += 1
p_ii = (obs_cnt + 1) / (tot + 1)
pr(f"  resultado: {obs_ii}/{len(ac)}; E exacta={E_ii:.3f}; nulo exacto (21P4={tot:,}) p={p_ii:.5f} "
   f"({obs_cnt} permutaciones con ≥{obs_ii}); p Poisson={poisson.sf(obs_ii - 1, E_ii):.4f}")
pr(f"  18 §4 anunciaba 3/3; con el criterio completo son {obs_ii}/{len(ac)}: falla el registro de "
   f"grupo 2 (3084).")
# criterio estricto: TODAS las cuerdas de 273A sin nudos (no solo sin cabecera)
estricto = np.array([
    not c[(c.kfg == "UR273A") & (c.grupo == gg) & (c.nivel == 0)].pres.any() for gg in ga])
cand_e = np.where(estricto & Bpres & ~np.isnan(A274[:len(A)]))[0]
if len(cand_e):
    se = A274[cand_e].astype(np.int64) + B[cand_e].astype(np.int64)
    pr(f"  [criterio estricto: 273A totalmente en blanco] {int(np.isin(se, S).sum())}/{len(cand_e)}: "
       + ", ".join(str(int(x)) for x in se))
# ¿es especial UR274A? otros quipus del archivo en las mismas posiciones
ARCH = sorted(q[q.procedencia == "Incahuasi"].kfg)
fam = []
for k in ARCH:
    if k in ("UR273A", "UR274A"):
        continue
    _, X = serie(k)
    if len(X) < cand.max() + 1:
        continue
    xx = X[cand]
    m = ~np.isnan(xx)
    if m.sum() < 3:
        continue
    fam.append((k, int(np.isin(xx[m].astype(np.int64) + bc[m], S).sum()), int(m.sum())))
fam.sort(key=lambda t: (-t[1], t[0]))
pr(f"  control de familia: {len(fam)} quipus del archivo con ≥3 posiciones utilizables; "
   f"274A (excluido del control) da {obs_ii}/{len(ac)}")
pr("    mejores: " + "; ".join(f"{k} {hh}/{nn}" for k, hh, nn in fam[:6]))
pr(f"    quipus distintos de 274A con ≥3/4: {sum(1 for _, hh, _ in fam if hh >= 3)}; "
   f"con ≥2/4: {sum(1 for _, hh, _ in fam if hh >= 2)}")

# ---------------------------------------------------------------- (iii) mitades 267
pr("\n" + "=" * 78)
pr("(iii) R1 por mitades: UR267A+UR267B -> cabeceras UR269")
g3, a3, gb3, b3 = pares("UR267A", "UR267B")
h3 = np.isin(a3 + b3, S269c)
pr(f"  n válidos={len(a3)}; aciertos={h3.sum()}; E exacta={L.esperado_perm(a3, b3, S269c):.3f}")
pr(f"  n.º de grupo de los aciertos: {g3[h3].tolist()}")
corte3 = len(a3) // 2
res_iii = {}
for sl, nom in ((slice(0, corte3), "1.ª mitad"), (slice(corte3, None), "2.ª mitad")):
    obs, E, nul, p = perm_dentro(a3[sl], b3[sl], S269c)
    res_iii[nom] = (obs, len(a3[sl]), E, p)
    imprime_prueba(nom, f"{obs}/{len(a3[sl])}", E, p)
tab3 = [[int(h3[:corte3].sum()), int((~h3[:corte3]).sum())],
        [int(h3[corte3:].sum()), int((~h3[corte3:]).sum())]]
pr(f"  tabla 2x2 = {tab3}; Fisher bilateral p={fisher_exact(tab3)[1]:.3f}")
p_iii = max(res_iii["1.ª mitad"][3], res_iii["2.ª mitad"][3])
pr(f"  prueba de conjunción (ambas mitades): p_IUT = max(p1,p2) = {p_iii:.4f}")

# ---------------------------------------------------------------- bloques de UR269
u = c[(c.kfg == "UR269") & (c.nivel == 0)].sort_values("orden")
reg269 = {}
bb_, ff_ = 0, 0
for gg, x in u.groupby("grupo", sort=True):
    if x.color.str.startswith("PK").all() and not x.pres.any():
        bb_, ff_ = bb_ + 1, 0
        continue
    if not x.pres.any():
        continue
    ff_ += 1
    reg269[int(gg)] = dict(grupo=int(gg), b=bb_, f=ff_, cab=int(x[x.pres].valor.iloc[0]))
tam = {}
for d in reg269.values():
    tam[d["b"]] = max(tam.get(d["b"], 0), d["f"])
for d in reg269.values():
    d["t"] = tam[d["b"]]


def diana_pos(v, tol=0):
    return [d for d in reg269.values() if abs(d["cab"] - v) <= tol]


def prob_cond(hits, objetivo, tol=0.15, regs=None):
    """p del estadístico 'obs aciertos en la fila objetivo' con nulo condicionado a la magnitud.
    Para cada acierto, filas elegibles = cabeceras del bloque dentro de ±tol de la cabecera
    observada; se elige una al azar (uniforme). Réplicas Monte Carlo + producto exacto."""
    regs = reg269 if regs is None else regs
    el = []
    for d in hits:
        vals = [e["f"] for e in regs.values() if e["b"] == d["b"]
                and abs(e["cab"] - d["cab"]) <= tol * d["cab"]]
        el.append(tuple(sorted(set(vals))))
    fila_obj = (lambda d, e: max(e)) if objetivo == "ultima" else (lambda d, e: 1)
    obs = sum(d["f"] == fila_obj(d, el[i]) for i, d in enumerate(hits))
    prod = float(np.prod([1 / len(e) for e in el]))
    cnt = np.empty(NREP, dtype=int)
    for r in range(NREP):
        c_ = 0
        for i, d in enumerate(hits):
            e = el[i]
            ff = e[rng.integers(len(e))]
            c_ += (ff == fila_obj(d, e))
        cnt[r] = c_
    p = L.p_emp(cnt, obs)
    naive = float(np.prod([1 / d["t"] for d in hits]))
    return obs, len(hits), el, prod, naive, p


def imprime_iv(nom, hits, objetivo, tol=0.15, regs=None):
    if not hits:
        pr(f"  {nom}: sin aciertos")
        return None
    obs, n, el, prod, naive, p = prob_cond(hits, objetivo, tol, regs)
    pr(f"  {nom}: {obs}/{n} en la fila {'última' if objetivo == 'ultima' else '1.ª'}; "
       f"elegibles={el}; P(las n en la fila)= {prod:.3f}; P_nula_uniforme={naive:.4f}; p_MC={p:.4f}")
    return p


pr("\n" + "=" * 78)
pr("(iv) Posición en el bloque de UR269 con nulo condicionado a la magnitud (±15 %)")
sumas273 = a + b
hits273 = []
for s in sumas273[h]:
    hits273 += diana_pos(int(s), 0)
hits273 = list({d["grupo"]: d for d in hits273}.values())
hits273.sort(key=lambda d: d["grupo"])
pr("  273A+B exactos en UR269: " + ", ".join(
    f"g{d['grupo']} (bloque {d['b']}, fila {d['f']}/{d['t']}, {d['cab']})" for d in hits273))
p_iv = imprime_iv("273A+B exactos, fila 1.ª", hits273, "primera")
hits273b = []
for s in sumas273:
    hits273b += diana_pos(int(s), 1)
hits273b = list({d["grupo"]: d for d in hits273b}.values())
hits273b.sort(key=lambda d: d["grupo"])
pr("  273A+B ±1 en UR269: " + ", ".join(
    f"g{d['grupo']} (b{d['b']}, f{d['f']}/{d['t']}, {d['cab']})" for d in hits273b))
imprime_iv("273A+B ±1, fila 1.ª", hits273b, "primera")
for tol in (0.10, 0.20):
    imprime_iv(f"273A+B exactos, ±{int(tol * 100)} %", hits273, "primera", tol)
hits267 = []
for s in (a3 + b3)[h3]:
    hits267 += diana_pos(int(s), 0)
hits267 = list({d["grupo"]: d for d in hits267}.values())
hits267.sort(key=lambda d: d["grupo"])
pr("  267A+B exactos en UR269: " + ", ".join(
    f"g{d['grupo']} (b{d['b']}, f{d['f']}/{d['t']}, {d['cab']})" for d in hits267))
p_iv267 = imprime_iv("267A+B exactos, fila última", hits267, "ultima")
pr("    (4/5: p_MC es P(≥4/5); P(5/5)=P_exacta=0,25. La 5.ª, g41, cae en la fila 4 de un bloque de 9.)")
# sensibilidad: el bloque 5 (9 filas) se parte en dos tras la fila 4 (g41), como sugiere 13
split = {}
for d in reg269.values():
    e = dict(d)
    if d["b"] == 5 and d["f"] > 4:
        e["b"], e["f"] = 51, d["f"] - 4
    elif d["b"] == 5:
        e["b"] = 50
    split[d["grupo"]] = e
for b_ in (50, 51):
    hh = [e for e in split.values() if e["b"] == b_]
    t_ = max(x["f"] for x in hh)
    for x in hh:
        x["t"] = t_
hits267s = [split[d["grupo"]] for d in hits267]
imprime_iv("267 exactos, bloque 5 partido 4+5 (g41 última de la 1.ª parte)", hits267s, "ultima", regs=split)
for par in (0, 1):
    hh = [d for d in hits273 if d["b"] % 2 == par]
    imprime_iv(f"273 exactos, bloques {'pares' if par == 0 else 'impares'}", hh, "primera")

# ---------------------------------------------------------------- (v) cuotas por fila
pr("\n" + "=" * 78)
pr("(v) Cuota por fila: bloques pares frente a impares (solo bloques canónicos de 5 filas)")


def cuota_de(d):
    x = c[(c.kfg == "UR269") & (c.grupo == d["grupo"]) & (c.nivel == 0) & c.pres].sort_values("orden")
    vals = [int(v) for v in x.valor.tolist()[1:]]
    expl = [v for v in vals if 15 <= v <= 50]
    imp = [d["cab"] - v for v in vals if 15 <= d["cab"] - v <= 50]
    if expl:
        return expl[0]
    if imp:
        return imp[0]
    return None


for d in reg269.values():
    d["cuota"] = cuota_de(d)
F = pd.DataFrame([d for d in reg269.values() if d["t"] == 5])
CANON = {1: 47, 2: 46, 3: 46, 4: 44, 5: 25}


def patron(df):
    return {r: (int(s.mode().iloc[0]) if len(s.dropna()) else None) for r, s in df.groupby("f").cuota}


def aciertos(df, pat):
    return int(sum(1 for r in df.itertuples() if r.cuota is not None and pat.get(r.f) is not None
                   and r.cuota == pat[r.f]))


def perm_bloques(df, pat, reps=NREP):
    """Nulo: barajar las cuotas entre las filas de cada bloque (conserva bloque, tamaño y cuotas)."""
    obs = aciertos(df, pat)
    cnt = np.empty(reps, dtype=int)
    for rr in range(reps):
        tot = 0
        for _, x in df.groupby("b"):
            vals = x.cuota.dropna().tolist()
            idx = x.index[x.cuota.notna()]
            for i, v in zip(idx, rng.permutation(vals)):
                f_ = int(df.loc[i, "f"])
                tot += (pat.get(f_) is not None and v == pat[f_])
        cnt[rr] = tot
    return obs, len(df), cnt, L.p_emp(cnt, obs)


pr(f"  patrón canónico de 13 (filas 1-5): {[CANON[i] for i in range(1, 6)]}")
even = F[F.b % 2 == 0]
odd = F[F.b % 2 == 1]
pe, po = patron(even), patron(odd)
pr(f"  bloques canónicos: pares={sorted(even.b.unique().tolist())} ({len(even)} registros), "
   f"impares={sorted(odd.b.unique().tolist())} ({len(odd)} registros)")
pr(f"  patrón modal en pares: {[pe.get(i) for i in range(1, 6)]}")
pr(f"  patrón modal en impares: {[po.get(i) for i in range(1, 6)]}")
obs_all, n_all, cnt_all, p_all = perm_bloques(F, CANON)
pr(f"  ajuste al patrón canónico en los 10 bloques: {obs_all}/{n_all}; nulo media={cnt_all.mean():.2f}; p={p_all:.4f}")
obs_e2o, n_e2o, cnt_e2o, p_e2o = perm_bloques(odd, pe)
pr(f"  [fuera de muestra] patrón de pares -> impares: {obs_e2o}/{n_e2o}; nulo media={cnt_e2o.mean():.2f}; p={p_e2o:.4f}")
obs_o2e, n_o2e, cnt_o2e, p_o2e = perm_bloques(even, po)
pr(f"  [fuera de muestra] patrón de impares -> pares: {obs_o2e}/{n_o2e}; nulo media={cnt_o2e.mean():.2f}; p={p_o2e:.4f}")
p_v = p_e2o
for r in range(1, 6):
    pr(f"    fila {r}: pares={sorted(even[even.f == r].cuota.dropna().tolist())}, "
       f"impares={sorted(odd[odd.f == r].cuota.dropna().tolist())}")
# sensibilidad exploratoria: corte temporal 5+5 bloques (elegido después de ver la paridad)
A1 = F[F.b <= 6]
A2 = F[F.b >= 7]
p1_, p2_ = patron(A1), patron(A2)
pr(f"  [sens. temporal, post hoc] bloques 0-6: patrón {[p1_.get(i) for i in range(1, 6)]}; "
   f"bloques 7-14: patrón {[p2_.get(i) for i in range(1, 6)]}")
obs_12, n_12, cnt_12, p_12 = perm_bloques(A2, p1_)
pr(f"    patrón de 0-6 -> 7-14: {obs_12}/{n_12}; nulo media={cnt_12.mean():.2f}; p={p_12:.4f}")
obs_21, n_21, cnt_21, p_21 = perm_bloques(A1, p2_)
pr(f"    patrón de 7-14 -> 0-6: {obs_21}/{n_21}; nulo media={cnt_21.mean():.2f}; p={p_21:.4f}")

# ---------------------------------------------------------------- corrección múltiple
pr("\n" + "=" * 78)
P = {"(i) 273 mitades": p_i, "(ii) 274A rellena 273A": p_ii, "(iii) 267 mitades": p_iii,
     "(iv) posición UR269": p_iv, "(v) cuota par/impar": p_v}
nombres = list(P)
pv = np.array([P[k] for k in nombres], dtype=float)
orden = np.argsort(pv)
m = len(pv)
holm = np.empty(m)
mx = 0.0
for rank, idx in enumerate(orden):
    mx = max(mx, (m - rank) * pv[idx])
    holm[idx] = min(1.0, mx)
pr("Corrección de Holm sobre las 5 pruebas (p primarios):")
for k, p, h in zip(nombres, pv, holm):
    pr(f"  {k:<32} p={p:.4f}  Holm={h:.4f}")
pr("BH-FDR (por comparación): " + ", ".join(f"{k}={v:.4f}" for k, v in zip(nombres, C13.bh(pv))))
out.close()
