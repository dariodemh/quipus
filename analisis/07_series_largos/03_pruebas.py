"""Paso 2b-3: "palabras" de vueltas en las cuerdas de series de largos, nulos y pruebas de interpretacion.

Unidad = quipu (9 quipus foco). Cada estadistico se calcula por quipu y se combina como media de z entre quipus;
el p combinado sale de las mismas permutaciones (media de z por permutacion). Semilla fija. B = 2000.
Nulos: (a) barajar racimos entre cuerdas serie del quipu manteniendo k por cuerda; (b) vueltas iid de la marginal del quipu;
(d) permutar el orden de los racimos dentro de cada cuerda; (c) referencia: cuerdas decimales limpias de otros quipus
(misma estadistica, distribucion entre quipus).
Salidas: 03_salida.txt, tabla_pruebas.csv, tabla_descriptiva.csv, tabla_vs_decimal.csv
"""
import sys
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "06_nudos"))
from util import holm, bh, pemp, SEED  # reutiliza utilidades del equipo de nudos

B = 2000
rng = np.random.default_rng(SEED)
STR = {c: str for c in ["vueltas", "pos", "niv", "tipos", "dirs"]}
T = pd.read_csv(AQUI / "cuerdas_foco.csv", dtype=STR)
D = pd.read_csv(AQUI / "cuerdas_decimal.csv", dtype=STR)
F = sorted(T.kfg.unique())
f = open(AQUI / "03_salida.txt", "w", encoding="utf-8")
def P(*a):
    print(*a); print(*a, file=f)

lst = lambda s: [np.nan if x == "?" else float(x) for x in s.split(";")]
T["w"] = T.vueltas.map(lst); T["p"] = T.pos.map(lst)
D["w"] = D.vueltas.map(lst); D["p"] = D.pos.map(lst)
S = T[T.serie].copy()

# ---------------- estadisticos sobre una lista de palabras ----------------
def mi_bigram(ws):
    pares = [(a, b) for w in ws for a, b in zip(w, w[1:])]
    if len(pares) < 5: return np.nan
    n = len(pares); cxy = Counter(pares); cx = Counter(a for a, _ in pares); cy = Counter(b for _, b in pares)
    return sum(v / n * np.log2(v * n / (cx[a] * cy[b])) for (a, b), v in cxy.items())

def zipf(ws):
    fr = np.sort(np.array(list(Counter(map(tuple, ws)).values())))[::-1]
    if len(fr) < 5: return np.nan
    r = np.arange(1, len(fr) + 1)
    return np.polyfit(np.log(r), np.log(fr), 1)[0]

def stats(ws):
    adj = [(a, b) for w in ws for a, b in zip(w, w[1:])]
    c = Counter(map(tuple, ws))
    return dict(
        eqadj=np.mean([a == b for a, b in adj]),                    # pares contiguos iguales
        madj=np.mean([abs(a - b) for a, b in adj]),                 # |diferencia| contigua
        sdin=np.mean([np.std(w) for w in ws]),                      # dispersion dentro de cuerda
        rep=np.mean([c[tuple(w)] > 1 for w in ws]),                 # cuerdas cuya palabra se repite en el quipu
        dist=len(c) / len(ws),                                      # tipos / ocurrencias
        trend=np.mean([w[-1] - w[0] for w in ws]),                  # ultimo - primero
        mi=mi_bigram(ws), zipf=zipf(ws))
NOMBRES = ["eqadj", "madj", "sdin", "rep", "dist", "trend", "mi", "zipf"]

def nulo_a(ws, rng):
    flat = np.concatenate(ws); rng.shuffle(flat); out, i = [], 0
    for w in ws: out.append(list(flat[i:i + len(w)])); i += len(w)
    return out
def nulo_b(ws, rng):
    flat = np.concatenate(ws); return [list(rng.choice(flat, len(w))) for w in ws]
def nulo_d(ws, rng):
    return [list(rng.permutation(w)) for w in ws]

# ---------------- descriptivo ----------------
desc = []
for q in F:
    t = T[(T.kfg == q) & T.soloL]; s = S[S.kfg == q]
    allw = np.concatenate(t.w.values)
    c = Counter(tuple(map(int, w)) for w in s.w)
    desc.append(dict(quipu=q, cuerdas_nudo=int((T.kfg == q).sum()), soloL=len(t), serie=len(s),
                     k_moda=int(s.k.mode()[0]), vueltas_media=allw.mean().round(2), vueltas_moda=int(Counter(allw).most_common(1)[0][0]),
                     frac_4a6=np.mean((allw >= 4) & (allw <= 6)).round(2), dirS=round(np.mean([ch == "S" for d in t.dirs for ch in d]), 3),
                     palabras_distintas=len(c), top=", ".join(f"{'-'.join(map(str, k))}x{v}" for k, v in c.most_common(4)),
                     total_vueltas=int(allw.sum()), total_racimos=len(allw)))
desc = pd.DataFrame(desc); desc.to_csv(AQUI / "tabla_descriptiva.csv", index=False)
P("=== Descriptivo (cuerdas solo-L; serie = k>=2)"); P(desc.to_string(index=False))

# distribucion de vueltas: foco vs L de unidades en cuerdas decimales limpias
uL = np.array([w[-1] for w, t in zip(D.w, D.tipos) if t[-1] == "L"])
fL = np.concatenate(T[T.soloL].w.values)
P("\nVueltas L foco (frac):", {int(k): round(v / len(fL), 3) for k, v in sorted(Counter(fL).items()) if v / len(fL) > .004})
P("Vueltas L de unidades en cuerdas decimales (frac):", {int(k): round(v / len(uL), 3) for k, v in sorted(Counter(uL).items()) if v / len(uL) > .004})
# por quipu decimal: moda de vueltas L de unidades
dm = {q: Counter(int(w[-1]) for w in g.w) for q, g in D[D.tipos.str[-1] == "L"].groupby("kfg")}
modas = Counter(c.most_common(1)[0][0] for c in dm.values() if sum(c.values()) >= 20)
P("Moda de vueltas L-unidades en quipus decimales (>=20 L):", dict(sorted(modas.items())))

# ---------------- pruebas con nulos a/b/d ----------------
filas = []
Z = {nm: {} for nm in "abd"}
for nm, fn in [("a", nulo_a), ("b", nulo_b), ("d", nulo_d)]:
    zs_obs, zs_null = [], []
    for q in F:
        ws = [list(w) for w in S[S.kfg == q].w]
        obs = stats(ws)
        nul = pd.DataFrame([stats(fn(ws, rng)) for _ in range(B)])
        for st in NOMBRES:
            if np.isnan(obs[st]) or nul[st].std() == 0: continue
            filas.append(dict(nulo=nm, quipu=q, estad=st, obs=obs[st], media_nulo=nul[st].mean(), sd_nulo=nul[st].std(),
                              z=(obs[st] - nul[st].mean()) / nul[st].std(), p=pemp(obs[st], nul[st].values, "dos")))
        Z[nm][q] = (obs, nul)
    # combinado: media de z entre quipus
    for st in NOMBRES:
        zo, zn = [], []
        for q, (obs, nul) in Z[nm].items():
            if np.isnan(obs[st]) or nul[st].std() == 0: continue
            m, sd = nul[st].mean(), nul[st].std()
            zo.append((obs[st] - m) / sd); zn.append(((nul[st] - m) / sd).values)
        if zo:
            zo = np.mean(zo); zn = np.nanmean(np.vstack(zn), axis=0)
            filas.append(dict(nulo=nm, quipu="COMBINADO", estad=st, obs=np.nan, z=zo, p=pemp(zo, zn, "dos")))
R = pd.DataFrame(filas)

# ---------------- (c) referencia decimal ----------------
ref = []
for q, g in D.groupby("kfg"):
    if len(g) < 20: continue
    st = stats([list(w) for w in g.w]); st["quipu"] = q; ref.append(st)
ref = pd.DataFrame(ref)
vs = []
for q in F:
    obs = Z["a"][q][0]
    vs.append({"quipu": q, **{st: f"{obs[st]:.2f} (pct {100 * np.mean(ref[st] < obs[st]):.0f})" for st in NOMBRES}})
vs.append({"quipu": f"decimal mediana (n={len(ref)})", **{st: f"{ref[st].median():.2f}" for st in NOMBRES}})
vs = pd.DataFrame(vs); vs.to_csv(AQUI / "tabla_vs_decimal.csv", index=False)
P("\n=== (c) Foco vs cuerdas decimales limpias (valor y percentil entre", len(ref), "quipus decimales con >=20 cuerdas k>=2)")
P(vs.to_string(index=False))

# ---------------- posiciones (cm) ----------------
def bandas_foco(g):
    k = g.k.mode()[0]; h = g[g.k == k]
    if len(h) < 5: return np.nan
    return np.mean([np.std([p[j] for p in h.p]) for j in range(k)])
def bandas_dec(g):
    sds = []
    for nv in range(0, 4):
        x = [p for ps, ns in zip(g.p, g.niv) for p, n in zip(ps, lst(ns)) if n == nv]
        if len(x) >= 5: sds.append(np.std(x))
    return np.mean(sds) if sds else np.nan
def gapcv(g):
    v = [np.std(np.diff(p)) / np.mean(np.diff(p)) for p in g.p if len(p) >= 3 and np.mean(np.diff(p)) > 0]
    return np.mean(v) if len(v) >= 5 else np.nan
def gapmed(g):
    return np.median([x for p in g.p for x in np.diff(p)])
posf = pd.DataFrame([dict(quipu=q, sd_banda=bandas_foco(S[S.kfg == q]), cv_hueco=gapcv(S[S.kfg == q]), hueco_mediano=gapmed(S[S.kfg == q]),
                          pos_rel_primero=np.median([p[0] / l for p, l in zip(S[S.kfg == q].p, S[S.kfg == q].largo) if l > 0]))
                     for q in F])
posd = pd.DataFrame([dict(quipu=q, sd_banda=bandas_dec(g), cv_hueco=gapcv(g), hueco_mediano=gapmed(g)) for q, g in D.groupby("kfg") if len(g) >= 20])
P("\n=== Posiciones de los racimos (cm)")
P(posf.round(2).to_string(index=False))
P("Decimal (quipus con >=20 cuerdas limpias): sd por nivel decimal mediana", round(posd.sd_banda.median(), 2),
  "[p10-p90", posd.sd_banda.quantile(.1).round(2), "-", posd.sd_banda.quantile(.9).round(2), "]; cv hueco mediana",
  round(posd.cv_hueco.median(), 2), "[", posd.cv_hueco.quantile(.1).round(2), "-", posd.cv_hueco.quantile(.9).round(2), "]; hueco mediano",
  round(posd.hueco_mediano.median(), 1))
for st in ["sd_banda", "cv_hueco"]:
    P(f"  percentil de cada foco en {st} decimal:", {q: int(100 * np.mean(posd[st].dropna() < v)) for q, v in zip(posf.quipu, posf[st]) if v == v})
# vueltas ~ posicion absoluta (dentro de cuerda): rho de Spearman, nulo d
from scipy.stats import spearmanr
P("  rho(vueltas, posicion cm) por quipu:", {q: round(spearmanr(np.concatenate(S[S.kfg == q].p.values), np.concatenate(S[S.kfg == q].w.values))[0], 2) for q in F})

# ---------------- interpretacion (i): sumas ----------------
def valores(w, modo):
    if modo == "suma": return sum(w)
    if modo == "pos10": return sum(int(x) * 10 ** (len(w) - 1 - j) for j, x in enumerate(w))
    if modo == "k": return len(w)
def hits_canuto(vals, ci, grandes):
    tot = np.bincount(ci, vals)
    h = np.bincount(ci, (2 * vals == tot[ci]).astype(float), minlength=len(tot)) > 0
    return int((h & grandes).sum())
def hits_contiguos(vals):
    c = np.concatenate([[0], np.cumsum(vals)]); n = len(vals); hit = np.zeros(n, bool); i = np.arange(n)
    for L in range(2, 7):
        ok = i + L < n; hit[ok] |= vals[ok] == c[i[ok] + 1 + L] - c[i[ok] + 1]
        ok = i - L >= 0; hit[ok] |= vals[ok] == c[i[ok]] - c[i[ok] - L]
    return int(hit.sum())
P("\n=== (i) Relaciones de suma (cuerdas solo-L, k>=1); nulo: barajar valores entre cuerdas del quipu")
for modo in ["suma", "pos10", "k"]:
    o1 = o2 = 0; n1 = np.zeros(B); n2 = np.zeros(B)
    for q in F:
        t = T[(T.kfg == q) & T.soloL & T.CANUTO_ID.notna()].sort_values("orden")
        vals = np.array([valores(w, modo) for w in t.w], float)
        ci = pd.factorize(t.CANUTO_ID)[0]; grandes = np.bincount(ci) >= 3
        o1 += hits_canuto(vals, ci, grandes); o2 += hits_contiguos(vals)
        for b in range(B):
            pv = rng.permutation(vals)
            n1[b] += hits_canuto(pv, ci, grandes); n2[b] += hits_contiguos(pv)
    for nm, o, n in [("canuto: una = suma del resto", o1, n1), ("contigua: = suma de 2-6 vecinas", o2, n2)]:
        p = pemp(o, n, "mayor"); filas.append(dict(nulo="perm_cuerdas", quipu="TODOS", estad=f"suma_{modo}_{nm[:6]}", obs=o, media_nulo=n.mean(), p=p))
        P(f"  {modo:5s} {nm}: obs {o}, nulo {n.mean():.1f} (sd {n.std():.1f}), p(mayor) {p:.3f}")

# ---------------- (ii) unidades no decimales / radix mixto: techo de los racimos inferiores ----------------
P("\n=== (ii) Vueltas por posicion ordinal j (cuerdas serie); radix mixto predice techo en j>=1 y valores bajos frecuentes")
for q in F:
    s = S[S.kfg == q]; by = {}
    for w in s.w:
        for j, x in enumerate(w): by.setdefault(min(j, 3), []).append(x)
    P(f"  {q}: " + " | ".join(f"j{j}{'+' if j == 3 else ''}: media {np.mean(v):.2f} max {max(v):g} frac<=3 {np.mean(np.array(v) <= 3):.2f}" for j, v in sorted(by.items())))

# ---------------- (iii) calendario ----------------
P("\n=== (iii) Calendario: cuerdas con suma 29/30, canutos con suma 29/30, totales por quipu (nulo b: vueltas iid de la marginal)")
o_c = o_k = 0; n_c = np.zeros(B); n_k = np.zeros(B)
for q in F:
    t = T[(T.kfg == q) & T.soloL]; ws = [list(w) for w in t.w]; can = t.CANUTO_ID.fillna(-1).values
    sums = lambda ws: np.array([sum(w) for w in ws])
    def canut(sv): return sum(1 for c in np.unique(can) if c >= 0 and (sv[can == c].sum() in (29, 30)))
    sv = sums(ws); o_c += np.isin(sv, [29, 30]).sum(); o_k += canut(sv)
    for b in range(B):
        nv = sums(nulo_b(ws, rng)); n_c[b] += np.isin(nv, [29, 30]).sum(); n_k[b] += canut(nv)
for nm, o, n in [("cuerdas suma 29/30", o_c, n_c), ("canutos suma 29/30", o_k, n_k)]:
    p = pemp(o, n, "mayor"); filas.append(dict(nulo="b", quipu="TODOS", estad=nm, obs=o, media_nulo=n.mean(), p=p))
    P(f"  {nm}: obs {o}, nulo {n.mean():.1f}, p(mayor) {p:.3f}")
P("  totales de vueltas por quipu:", dict(zip(desc.quipu, desc.total_vueltas)), "| racimos:", dict(zip(desc.quipu, desc.total_racimos)))

# ---------------- (iv) codigos: posiciones homologas en canutos, color; (v) lotes: similitud dentro de canuto ----------------
P("\n=== (iv)/(v) Similitud entre cuerdas: posicion homologa en canuto, color, mismo canuto, vecinas (+ = mas parecidas)")
def sim_pairs(M, rel, valid):
    """M = (|dif media vueltas|, misma palabra, mismo k) por par; rel/valid matrices booleanas (triangulo superior)"""
    a, b = rel & valid, ~rel & valid
    if a.sum() < 5 or b.sum() < 5: return None
    return np.array([M[0][b].mean() - M[0][a].mean(), M[1][a].mean() - M[1][b].mean(), M[2][a].mean() - M[2][b].mean()])
def relacion(cual, d):
    eq = lambda x: x[:, None] == x[None, :]
    U = np.triu(np.ones((len(d), len(d)), bool), 1)
    if cual == "homologa_canuto": return eq(d.CANUTO_ORDINAL.values), U & ~eq(d.CANUTO_ID.values)
    if cual == "mismo_color": return eq(d.color.values), U
    if cual == "mismo_canuto": return eq(d.CANUTO_ID.values), U
    if cual == "vecinas": o = d.orden.values; return np.abs(o[:, None] - o[None, :]) <= 2, U
def permuta(d, cual, rng):
    d = d.copy()
    if cual == "homologa_canuto":
        d["CANUTO_ORDINAL"] = d.groupby("CANUTO_ID").CANUTO_ORDINAL.transform(lambda s: rng.permutation(s.values))
    elif cual == "mismo_color": d["color"] = rng.permutation(d.color.values)
    elif cual == "mismo_canuto": d["CANUTO_ID"] = rng.permutation(d.CANUTO_ID.values)
    elif cual == "vecinas": d["orden"] = rng.permutation(d.orden.values)
    return d
BS = 1000
for cual in ["homologa_canuto", "mismo_color", "mismo_canuto", "vecinas"]:
    zo, zn, usados = [], [], []
    for q in F:
        d = T[(T.kfg == q) & T.soloL & T.CANUTO_ID.notna()].reset_index(drop=True)
        if cual == "mismo_color":
            vc = d.color.value_counts(); d = d[d.color.isin(vc[vc >= 5].index)].reset_index(drop=True)
            if d.color.nunique() < 2: continue
        m = np.array([np.mean(w) for w in d.w]); wid = pd.factorize(d.vueltas)[0]; k = d.k.values
        M = (np.abs(m[:, None] - m[None, :]), (wid[:, None] == wid[None, :]).astype(float), (k[:, None] == k[None, :]).astype(float))
        obs = sim_pairs(M, *relacion(cual, d))
        if obs is None: continue
        nul = np.array([sim_pairs(M, *relacion(cual, permuta(d, cual, rng))) for _ in range(BS)])
        m, sd = nul.mean(0), nul.std(0); sd[sd == 0] = np.nan
        for e, nmst in enumerate(["dmedia", "mismapalabra", "mismok"]):
            filas.append(dict(nulo="perm_" + cual, quipu=q, estad=nmst, obs=obs[e], media_nulo=m[e], sd_nulo=sd[e],
                              z=(obs[e] - m[e]) / sd[e], p=pemp(obs[e], nul[:, e], "dos")))
        zo.append((obs - m) / sd); zn.append((nul - m) / sd); usados.append(q)
    zo = np.nanmean(zo, 0); zn = np.nanmean(np.stack(zn), 0)
    for e, nmst in enumerate(["dmedia", "mismapalabra", "mismok"]):
        filas.append(dict(nulo="perm_" + cual, quipu="COMBINADO", estad=nmst, obs=np.nan, z=zo[e], p=pemp(zo[e], zn[:, e], "dos")))
    P(f"  {cual} ({len(usados)} quipus): z combinado dmedia {zo[0]:.2f}, misma palabra {zo[1]:.2f}, mismo k {zo[2]:.2f}")

R = pd.DataFrame(filas)
R["p_BH"] = bh(R.p.values); R["p_Holm"] = holm(R.p.values)
R.to_csv(AQUI / "tabla_pruebas.csv", index=False)
P(f"\n=== Pruebas ({len(R)}; BH y Holm sobre todas). Combinados y globales:")
P(R[R.quipu.isin(["COMBINADO", "TODOS"])][["nulo", "estad", "obs", "media_nulo", "z", "p", "p_BH", "p_Holm"]].round(4).to_string(index=False))
P("\nPor quipu (nulo a/d), estadisticos clave:")
for st in ["eqadj", "sdin", "rep", "mi", "zipf", "trend"]:
    for nm in "ad":
        x = R[(R.nulo == nm) & (R.estad == st) & (R.quipu != "COMBINADO")]
        P(f"  {st} nulo {nm}: " + "; ".join(f"{r.quipu} {r.obs:.2f} vs {r.media_nulo:.2f} (q{r.p_BH:.3f})" for r in x.itertuples()))
for cual in ["homologa_canuto", "mismo_color", "mismo_canuto", "vecinas"]:
    x = R[(R.nulo == "perm_" + cual) & (R.quipu != "COMBINADO") & (R.estad == "dmedia")]
    P(f"  {cual} dmedia: " + "; ".join(f"{r.quipu} {r.obs:.2f} vs {r.media_nulo:.2f} (q{r.p_BH:.3f})" for r in x.itertuples()))
f.close()
