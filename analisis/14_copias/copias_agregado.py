"""14_copias · agregados entre pares (lee filas_alineadas.csv y pares_resumen.csv de copias.py).
Salida: agregado_salida.txt (y se imprime). Semilla fija 20261017.
"""
import re, sys
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats

OUT = Path(__file__).resolve().parent
RAIZ = OUT.parents[1]
SEED = 20261017
rng = np.random.default_rng(SEED)
F = pd.read_csv(OUT / "filas_alineadas.csv")
R = pd.read_csv(OUT / "pares_resumen.csv")
C = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv")
sys.path.insert(0, str(OUT))

REP = [("HP055", "UR1084"), ("UR1175", "UR233"), ("KH0049", "UR122"), ("UR053B", "UR053C"), ("UR006", "UR009"), ("UR064", "UR068"),
       ("UR1114", "UR1123"), ("UR066", "UR067"), ("UR1118", "UR218"), ("QU002", "UR137"), ("AS159", "AS173"), ("UR255", "UR267A"), ("MM016", "UR212")]
rep = R[[(a, b) in REP for a, b in zip(R.A, R.B)]].copy()
cop = R[R.tipo == "copia"]
obj = R[R.tipo == "mismo_objeto"]


def pr(*a):
    print(*a)


pr("=== 1. Composición de la muestra")
pr(f"pares {len(R)}: copia {len(cop)}, mismo_objeto {len(obj)}, debil {(R.tipo=='debil').sum()}; familias representativas (copias): {len(rep)}")

# ---------------------------------------------------------------- 2. nivel: colgantes vs subsidiarias
pr("\n=== 2. Valor conservado por nivel (filas alineadas; sesgo de selección: el alineamiento premia las coincidencias)")
for nom, d in (("copias", rep), ("mismo_objeto", obj)):
    pr(f"{nom}: colgantes exactas {int(d.col_exacta.sum())}/{int(d.col_n.sum())} = {d.col_exacta.sum()/d.col_n.sum():.3f}; "
       f"subsidiarias exactas {int(d.sub_exacta.sum())}/{int(d.sub_n.sum())} = {d.sub_exacta.sum()/max(d.sub_n.sum(),1):.3f}")
a, b = int(rep.col_exacta.sum()), int(rep.col_n.sum())
c, dd = int(obj.col_exacta.sum()), int(obj.col_n.sum())
pr(f"Fisher colgantes copias ({a}/{b}) vs mismo objeto ({c}/{dd}): p={stats.fisher_exact([[a,b-a],[c,dd-c]])[1]:.3f}")
pr("Por par (representantes): colgantes exactas / n ; subsidiarias exactas / n ; solo_A ; solo_B ; subsidiarias sin pareja")
for r in rep.itertuples():
    pr(f"  {r.A}~{r.B}: col {r.col_exacta}/{r.col_n}  sub {r.sub_exacta}/{r.sub_n}  soloA {r.solo_A} soloB {r.solo_B}  gaps_sub {r.gaps_subsidiarias} gaps_colg {r.gaps_colgantes}  vacía_otro {r.gaps_con_vacia_en_otro}")

# ---- 2b. ¿qué capa cambia: colgantes o subsidiarias? cuerdas con y sin pareja por nivel, Cochran-Mantel-Haenszel entre pares
pr("\n=== 2b. Cuerdas sin pareja por nivel (cada cuerda de cada lado cuenta una vez)")
TT = {}
for a_, b_ in REP:
    g = F[(F.A == a_) & (F.B == b_)]
    x = []
    for lado in "AB":
        pres = g[g["valor_" + lado].notna()]
        x.append(pd.DataFrame({"nivel": pres["nivel_" + lado].astype(int), "sin": (g.clase == "solo_" + lado)[pres.index].astype(int)}))
    x = pd.concat(x)
    TT[f"{a_}~{b_}"] = [[int(((x.nivel == 0) & (x.sin == 0)).sum()), int(((x.nivel == 0) & (x.sin == 1)).sum())],
                        [int(((x.nivel >= 1) & (x.sin == 0)).sum()), int(((x.nivel >= 1) & (x.sin == 1)).sum())]]
    pr(f"  {a_}~{b_}: colgantes con/sin pareja {TT[f'{a_}~{b_}'][0]}  subsidiarias con/sin pareja {TT[f'{a_}~{b_}'][1]}")


def cmh(T):
    obs = ev = var = 0
    for t in T.values():
        a, b = t[0]; c, d = t[1]; n = a + b + c + d
        if min(a + b, c + d) == 0 or min(a + c, b + d) == 0:
            continue
        obs += d; ev += (c + d) * (b + d) / n; var += (a + b) * (c + d) * (b + d) * (a + c) / (n * n * (n - 1))
    z = (obs - ev) / np.sqrt(var)
    return obs, round(ev, 1), round(z, 2), 2 * stats.norm.sf(abs(z))
pr("CMH (subsidiarias sin pareja: observadas, esperadas, z, p):", cmh(TT))
pr("CMH sin UR1175~UR233:", cmh({k: v for k, v in TT.items() if k != "UR1175~UR233"}))

# ---------------------------------------------------------------- 3. tipos de discordancia
pr("\n=== 3. Clases de discordancia entre colgantes alineados (ambos nivel 0), pares representantes")
amb = F[F.valor_A.notna() & F.valor_B.notna() & (F.nivel_A == 0) & (F.nivel_B == 0)]
amb = amb[[(a, b) in REP for a, b in zip(amb.A, amb.B)]]
pr(amb.clase.value_counts().to_string())
pm = amb[amb.clase == "pm1_nudo"].copy()
pm["k"] = (pm.valor_B - pm.valor_A).abs()
pr("pm1: |Δ| =", pm.k.value_counts().sort_index().to_dict(), "(1=unidades, 10=decenas, 100=centenas)")
# expectativa: reparto de |Δ| si el error cayera en una posición decimal al azar proporcional al nº de cuerdas con esa cifra no nula
dig = {1: 0, 10: 0, 100: 0}
tot = amb[amb.clase == "exacta"].valor_A.astype(int)
for v in tot:
    for k, nm in ((1, v % 10), (10, v // 10 % 10), (100, v // 100 % 10)):
        dig[k] += nm > 0
s = sum(dig.values())
pr("cifras no nulas en filas exactas por posición:", {k: round(v / s, 3) for k, v in dig.items()}, "-> esperado si el error fuese uniforme sobre cifras no nulas")
obs = np.array([(pm.k == k).sum() for k in (1, 10, 100)])
pr("chi2 de bondad vs esperado:", stats.chisquare(obs, np.array([dig[k] for k in (1, 10, 100)]) / s * obs.sum()))
pr("Signo (B>A) por par, discordantes colgante-colgante:")
for (a_, b_), g in amb[amb.clase != "exacta"].groupby(["A", "B"]):
    up = int((g.valor_B > g.valor_A).sum()); n = len(g)
    pr(f"  {a_}~{b_}: B>A {up}/{n}  p_binom={stats.binomtest(up, n, .5).pvalue:.3f}")

# ---------------------------------------------------------------- 4. ¿daño físico? McNemar sobre cuerda rota
pr("\n=== 4. Daño físico: entre discordancias colgante-colgante (|valor|≠), ¿la cuerda de menor valor está rota (terminación B) más a menudo que la de mayor valor?")
def mcnemar(F_):
    d = F_[(F_.clase != "exacta") & F_.valor_A.notna() & F_.valor_B.notna() & (F_.nivel_A == 0) & (F_.nivel_B == 0) & (F_.valor_A != F_.valor_B)].copy()
    lo = np.where(d.valor_A < d.valor_B, d.term_A, d.term_B); hi = np.where(d.valor_A < d.valor_B, d.term_B, d.term_A)
    b = int(((lo == "B") & (hi != "B")).sum()); c = int(((lo != "B") & (hi == "B")).sum())
    return len(d), b, c, stats.binomtest(b, b + c, .5, alternative="greater").pvalue if b + c else np.nan
cpf = F[[(a, b) in REP for a, b in zip(F.A, F.B)]]
pr("copias (representantes): n_disc, solo menor rota, solo mayor rota, p_unilateral =", mcnemar(cpf))
pr("mismo_objeto:", mcnemar(F[[(a, b) in [("KH0033", "UR044"), ("UR1107", "UR237"), ("AS125", "UR247")] for a, b in zip(F.A, F.B)]]))
for k in REP:
    r = mcnemar(F[(F.A == k[0]) & (F.B == k[1])])
    if r[0]:
        pr(f"  {k}: {r}")

# ---------------------------------------------------------------- 5. sustituciones repetidas y omisiones concentradas (Holm sobre pares)
pr("\n=== 5. Edición sistemática: sustitución repetida a->b y omisión concentrada por valor")
x = R[R.sust_rep_p.notna()][["A", "B", "tipo", "n_discordantes", "sust_rep_max", "sust_rep_nulo", "sust_rep_p", "sust_rep_top"]].copy()
m = len(x)
x["p_holm"] = np.minimum(1, x.sust_rep_p * m)
pr(x.sort_values("sust_rep_p").head(6).round(4).to_string(index=False), f"\n(Holm sobre {m} pares)")
S = pd.read_csv(OUT / "tests_sistematicos.csv")
S["p_holm_pares"] = np.minimum(1, S.p_holm_valores * len(S))
pr(S.sort_values("p_hiper").head(5).round(5).to_string(index=False), f"\n(Holm por valores dentro de cada par, y por {len(S)} pruebas)")

# ---- 5b. coherencia aditiva/multiplicativa de las discordancias (¿actualización?): modo de delta=b-a y del cociente redondeado vs nulo (barajar b entre filas discordantes)
pr("\n=== 5b. Coherencia de las discordancias colgante-colgante (pares con >=8 discordancias)")
amb_all = F[F.valor_A.notna() & F.valor_B.notna() & (F.nivel_A == 0) & (F.nivel_B == 0) & (F.valor_A != F.valor_B)]
for (a_, b_), g in amb_all.groupby(["A", "B"]):
    if len(g) < 8 or (a_, b_) not in REP:
        continue
    va, vb = g.valor_A.to_numpy(float), g.valor_B.to_numpy(float)
    def modo(x, y):
        d = pd.Series(y - x).value_counts(); r_ = pd.Series(np.round(y / x, 1)).value_counts()
        return d.iloc[0], d.index[0], r_.iloc[0], r_.index[0]
    o_ = modo(va, vb)
    nd, nr = [], []
    for _ in range(2000):
        m_ = modo(va, rng.permutation(vb)); nd.append(m_[0]); nr.append(m_[2])
    pr(f"  {a_}~{b_}: n={len(g)}  delta modal {o_[1]:+.0f} x{o_[0]} (nulo {np.mean(nd):.2f}, p={(1+(np.array(nd)>=o_[0]).sum())/2001:.3f}); cociente modal {o_[3]} x{o_[2]} (nulo {np.mean(nr):.2f}, p={(1+(np.array(nr)>=o_[2]).sum())/2001:.3f})")

# ---------------------------------------------------------------- 6. forma: color (mismo registrador) y dirección / unión
pr("\n=== 6. Forma: color, dirección y unión")
sr = R[(R.mismo_registrador) & (R.tipo == "copia") & R.color_exacto.notna()]
pr("color, pares del mismo registrador (copias): exacto observado vs nulo (barajado simple) | exacto estratificado por valor | NMI estratificado")
for r in sr.itertuples():
    pr(f"  {r.A}~{r.B}  n={int(r.color_n)}  exacto {r.color_exacto:.2f} vs {r.color_exacto_nulo:.2f} p={r.color_exacto_p:.3f} | "
       f"estrat. {r.colorE_exacto:.2f} vs {r.colorE_exacto_nulo:.2f} p={r.colorE_exacto_p:.3f} | NMI {r.colorE_nmi:.2f} vs {r.colorE_nmi_nulo:.2f} p={r.colorE_nmi_p:.3f}")
def fisher(ps):
    ps = [p for p in ps if p == p]
    return stats.combine_pvalues(ps, method="fisher")[1], len(ps)
fam1 = sr[[(a, b) in REP for a, b in zip(sr.A, sr.B)]]
pr("Fisher combinado (un par por familia) color exacto simple:", fisher(fam1.color_exacto_p), " estratificado:", fisher(fam1.colorE_exacto_p), " NMI estratificado:", fisher(fam1.colorE_nmi_p))
cr = R[(~R.mismo_registrador) & (R.tipo == "copia") & R.colorE_nmi.notna()]
cr = cr[[(a, b) in REP for a, b in zip(cr.A, cr.B)]]
pr("color entre registradores distintos (NMI estratificado, invariante a la convención):")
for r in cr.itertuples():
    pr(f"  {r.A}~{r.B}  NMI {r.colorE_nmi:.2f} vs {r.colorE_nmi_nulo:.2f} p={r.colorE_nmi_p:.3f}  (exacto {r.color_exacto:.2f}, p={r.color_exacto_p:.3f})")
pr("Fisher combinado NMI estratificado (distintos registradores):", fisher(cr.colorE_nmi_p))

# línea base de dominantes (por quipu, todas las cuerdas)
from copias import dir_tipo, dominante, registrador  # noqa
Cq = C.copy()
Cq["dS"] = Cq.nudos.map(lambda s: dir_tipo(s, "S")); Cq["dL"] = Cq.nudos.map(lambda s: dir_tipo(s, "L"))
base = []
for k, g in Cq.groupby("kfg"):
    base.append({"kfg": k, "reg": registrador(k), "dirS": dominante(g.dS), "dirL": dominante(g.dL), "union": dominante(g.union)})
base = pd.DataFrame(base)
pr("\nLínea base (quipus del corpus, dominante >=80 % de las cuerdas con dato):")
for c_ in ("dirS", "dirL", "union"):
    pr(f"  {c_}:", base[c_].value_counts(dropna=True).to_dict())

def agreement(campo_A, campo_B, col_base):
    """para cada par: ¿coincide el dominante? esperado = sum_c P_gA(c) P_gB(c), nulo MC Bernoulli por par."""
    rows = []
    for r in rep.itertuples():
        a_, b_ = getattr(r, campo_A), getattr(r, campo_B)
        if not isinstance(a_, str) or not isinstance(b_, str) or "mixto" in (a_, b_):
            continue
        ga, gb = r.registradores.split("/")
        pa = base[(base.reg == ga) & base[col_base].isin(["S", "Z", "R", "V"])][col_base].value_counts(normalize=True)
        pb = base[(base.reg == gb) & base[col_base].isin(["S", "Z", "R", "V"])][col_base].value_counts(normalize=True)
        pe = float(sum(pa.get(c, 0) * pb.get(c, 0) for c in set(pa.index) | set(pb.index)))
        rows.append((r.A, r.B, a_, b_, a_ == b_, pe))
    return rows
for campo, col_base, nom in (("dom_dirL", "dirL", "dirección nudos largos"), ("dom_dirS", "dirS", "dirección nudos simples"), ("dom_union", "union", "unión R/V")):
    ca = [f"{campo}_A", f"{campo}_B"]
    rows = agreement(*ca, col_base)
    obs = sum(r[4] for r in rows)
    pe = np.array([r[5] for r in rows])
    sim = (rng.random((20000, len(pe))) < pe).sum(1)
    pr(f"{nom}: {len(rows)} familias comparables; coinciden {obs}; esperado por azar entre quipus al azar de las mismas series {pe.sum():.1f}; "
       f"p(>=obs)={((sim>=obs).mean()):.4f} ; p(<=obs)={((sim<=obs).mean()):.4f}")
    for r in rows:
        pr(f"    {r[0]}~{r[1]}: {r[2]} vs {r[3]}  esperado {r[5]:.2f}")

# largo
pr("\nLargo de cuerda entre pares (rho Spearman por par; copias representantes):")
pr(rep[["A", "B", "largo_rho", "largo_p"]].round(3).to_string(index=False))
pr("mediana rho copias:", round(rep.largo_rho.median(), 3), " mismo objeto:", obj.largo_rho.round(3).tolist())
sub = rep[rep.subs_p.notna()]
pr("Subsidiarias: acuerdo en nº de subsidiarias por colgante alineado (obs vs nulo):")
pr(sub[["A", "B", "subs_n", "subs_acuerdo", "subs_nulo", "subs_p", "subs_totA", "subs_totB"]].round(3).to_string(index=False))
