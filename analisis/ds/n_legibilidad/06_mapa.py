"""Mapa de legibilidad: une reglas intra y entre quipus, LOO + nulo con la MISMA permutacion.

Salidas:
  cuerdas_legibles.csv   una fila por cuerda con valor: vias, aciertos, reglas, prob. nula
  quipus_legibles.csv    indice por quipu (bruto, nulo, neto, p, q BH, cobertura, acierto)
  nulo_resumen.npz       distribuciones nulas agregadas (corpus y por quipu)
"""
import pickle, time
import numpy as np
import pandas as pd
from pathlib import Path
from motor import cargar, construir, REGLAS

AQUI = Path(__file__).resolve().parent
SEED = 20261018
NPERM = 1000

c, q = cargar()
Q, _, _ = construir(c)
with open(AQUI / "inter_estructura.pkl", "rb") as f:
    E = pickle.load(f)
# INDICE PRINCIPAL: solo reglas que pasan el control fuera de muestra.
# copia_grupo y suma_dos se evaluan aparte (ver 11_fuera_muestra.py): su acierto cae a ~35 %
# y ~24 % cuando el offset se estima sin las posiciones que luego se evaluan.
P_all = E["P"]
cop = P_all[P_all.regla == "copia_quipu"].reset_index(drop=True)
sum2 = E["S2"].iloc[0:0]
sum2_ev = []
proc = q.set_index("kfg").procedencia.fillna("Unknown").to_dict()

# indices de las cuerdas de nivel 0 dentro de cada quipu (mismo orden que seq)
l0idx = {k: np.where(o.nivel == 0)[0] for k, o in Q.items()}
for k in Q:
    assert len(l0idx[k]) == len(E["seq"][k]), k

# ------------------------------------------------------------------ observado
via_i, hit_i, ihit_i = {}, {}, {}
for k, o in Q.items():
    via_i[k], hit_i[k] = o.evaluar(o.val)
    ihit_i[k] = o.inst_hits(o.val)
O = pd.read_csv(AQUI / "inter_pred.csv")
O = O[O.regla == "copia_quipu"].reset_index(drop=True)  # indice principal
# i de inter_pred es la POSICION en la secuencia de colgantes: pasar a indice local
mapa = {k: {s: int(v) for s, v in enumerate(l0idx[k])} for k in Q}
O["i_local"] = [mapa[k][i] for k, i in zip(O.kfg, O.i)]
pd.DataFrame([(k, s, int(v)) for k in Q for s, v in mapa[k].items()],
             columns=["kfg", "seq", "i_local"]).to_csv(AQUI / "mapa_l0.csv", index=False)
hi = {k: np.zeros(Q[k].n, bool) for k in Q}
vi = {k: np.zeros(Q[k].n, bool) for k in Q}
for r in O.itertuples():
    vi[r.kfg][r.i_local] = True
    if r.hit:
        hi[r.kfg][r.i_local] = True

# posiciones de las predicciones inter agrupadas por quipu
def por_quipu(df, col_i):
    d = {}
    for t, (k, i) in enumerate(zip(df.kfg.to_numpy(), df[col_i].to_numpy())):
        d.setdefault(k, []).append((t, int(i)))
    return {k: (np.array([a for a, _ in v]), np.array([b for _, b in v])) for k, v in d.items()}
_cl = pd.DataFrame(dict(kfg=cop.kfg.to_numpy(), i=[mapa[k][i] for k, i in zip(cop.kfg, cop.i)]))
_sl = pd.DataFrame(dict(kfg=sum2.kfg.to_numpy(), i=[mapa[k][i] for k, i in zip(sum2.kfg, sum2.i)]))
cop_k = por_quipu(_cl, "i")
si_k = por_quipu(_sl, "i")
cop_a = cop[["kfg", "i", "otro", "j"]].to_numpy(object)
si = np.array([(r.kfg, r.i, r.A, r.ja, r.B, r.jb) for r in sum2.itertuples()], object) if len(sum2) else np.zeros((0,6), object)

# ------------------------------------------------------------------ nulo
rng = np.random.default_rng(SEED)
nh_int = {k: np.zeros(Q[k].n, np.int16) for k in Q}
nh_i = {k: np.zeros(Q[k].n, np.int16) for k in Q}
nh_any = {k: np.zeros(Q[k].n, np.int16) for k in Q}
nh_q = {k: np.zeros(NPERM, np.int32) for k in Q}
nh_cop = np.zeros(NPERM, np.int32)
nh_sum = np.zeros(NPERM, np.int32)
regn = {r: 0 for r in REGLAS}       # cuerdas cubiertas por la regla (obs)
regh = {r: 0 for r in REGLAS}       # de ellas, acertadas (obs)
regnull = {r: 0.0 for r in REGLAS}  # de ellas, acertadas con valores barajados (media)
regq = {r: set() for r in REGLAS}
nh_reg = {r: {k: np.zeros(Q[k].n, np.int16) for k in Q} for r in REGLAS}
cub = {r: {k: np.zeros(Q[k].n, bool) for k in Q} for r in REGLAS}
for k, o in Q.items():
    for r in np.unique(o.rule):
        nm = REGLAS[r]
        sel = o.rule == r
        tg = np.unique(o.tgt[sel])
        cub[nm][k][tg] = True
        regn[nm] += len(tg); regq[nm].add(k)
        tgok = np.unique(o.tgt[sel & ihit_i[k]])
        regh[nm] += len(tgok)
t0 = time.time()
for p in range(NPERM):
    vp = {}
    for k, o in Q.items():
        v = o.val.copy()
        idx = np.where(o.pres)[0]
        v[idx] = rng.permutation(v[idx])
        vp[k] = v
    hc = np.zeros(len(cop_a), bool)
    for t, (k, i, otro, j) in enumerate(cop_a):
        hc[t] = abs(vp[k][i] - vp[otro][j]) < 0.5
    hs = np.zeros(len(si), bool)
    for t, (k, i, A, ja, B, jb) in enumerate(si):
        kk = sum2_ev[t]
        dA, dB = ja - i, jb - i
        ok = 0
        for x in kk:
            ok += abs(vp[k][x] - (vp[A][x + dA] + vp[B][x + dB])) <= 1
        if ok >= 2 and ok / len(kk) >= 0.6 and abs(vp[k][i] - (vp[A][ja] + vp[B][jb])) < 0.5:
            hs[t] = True
    nh_cop[p] = hc.sum(); nh_sum[p] = hs.sum()
    for k, o in Q.items():
        via, hit = o.evaluar(vp[k])
        h = hit > 0
        ip = np.zeros(o.n, bool)
        for dic, arr in ((cop_k, hc), (si_k, hs)):
            if k in dic:
                ids, locs = dic[k]
                m = arr[ids]
                if m.any():
                    ip[locs[m]] = True
        u = h | ip
        if o.ni:
            ih = o.inst_hits(vp[k])
            for r in np.unique(o.rule):
                nm = REGLAS[r]
                tg = np.unique(o.tgt[(o.rule == r) & ih])
                regnull[nm] += len(tg)
                nh_reg[nm][k][tg] += 1
        nh_int[k] += h; nh_i[k] += ip; nh_any[k] += u
        nh_q[k][p] = int(u.sum())
print("nulo %d perms en %.1f s" % (NPERM, time.time() - t0))

# ------------------------------------------------------------------ tabla por cuerda
filas = []
for k, o in Q.items():
    for i in np.where(o.pres)[0]:
        filas.append(dict(kfg=k, i=int(i), cuerda=o.nombre[i], nivel=int(o.nivel[i]),
                          grupo=int(o.grupo[i]), valor=float(o.val[i]),
                          via_intra=int(via_i[k][i] > 0), hit_intra=int(hit_i[k][i] > 0),
                          via_inter=int(vi[k][i]),
                          hit_inter=int(hi[k][i]),
                          reglas=";".join(REGLAS[x] for x in sorted(o.regla_de[i])),
                          reglas_hit=";".join(sorted({REGLAS[int(o.rule[t])] for t in np.where(ihit_i[k])[0]
                                                      if o.tgt[t] == i})),
                          p_null_intra=nh_int[k][i] / NPERM,
                          p_null_inter=nh_i[k][i] / NPERM,
                          p_null=nh_any[k][i] / NPERM))
B = pd.DataFrame(filas)
B["hit"] = (B.hit_intra | B.hit_inter).astype(int)
B["via"] = (B.via_intra | B.via_inter).astype(int)
B["procedencia"] = B.kfg.map(proc)
B.to_csv(AQUI / "cuerdas_legibles.csv", index=False)
print("cuerdas con valor:", len(B), " aciertos:", B.hit.sum(), " (%.3f)" % B.hit.mean(),
      " p_null medio %.3f" % B.p_null.mean())

# ------------------------------------------------------------------ indice por quipu
R = []
for k, o in Q.items():
    d = B[B.kfg == k]
    nv = len(d)
    hoc = int(d.hit.sum()); hnu = float(d.p_null.sum())
    R.append(dict(kfg=k, n=o.n, nval=nv,
                  via=int(d.via.sum()), hit=hoc, hit_null=hnu,
                  hit_intra=int(d.hit_intra.sum()), hit_inter=int(d.hit_inter.sum()),
                  via_intra=int(d.via_intra.sum()), via_inter=int(d.via_inter.sum()),
                  tasa=hoc / nv if nv else np.nan,
                  tasa_neta=(hoc - hnu) / nv if nv else np.nan,
                  cobertura=d.via.mean() if nv else np.nan,
                  acierto_si_via=hoc / d.via.sum() if nv and d.via.sum() else np.nan,
                  p=(1 + int((nh_q[k] >= hoc).sum())) / (NPERM + 1) if nv else np.nan,
                  nulo_sd=float(nh_q[k].std()),
                  nT=len(o.tunits), nsub=int((o.nivel > 0).sum()), ngrupos=len(o.grupos),
                  maxv=float(np.max(o.val[o.pres])) if nv else np.nan,
                  div=float(len(np.unique(o.val[o.pres])) / nv) if nv else np.nan,
                  media_grupo=float(o.n / max(1, len(o.grupos)))))
R = pd.DataFrame(R)
R["procedencia"] = R.kfg.map(proc)
qq = q.set_index("kfg")
R["region"] = R.kfg.map(qq.region.to_dict())
R["museo"] = R.kfg.map(qq.museo.to_dict())

# BH-FDR sobre los quipus con valor
def bh(p):
    p = np.asarray(p, float)
    ok = ~np.isnan(p)
    qv = np.full(len(p), np.nan)
    idx = np.where(ok)[0]
    o = np.argsort(p[idx])
    m = len(idx)
    r = np.empty(m)
    prev = 1.0
    for t in range(m - 1, -1, -1):
        val = p[idx][o[t]] * m / (t + 1)
        prev = min(prev, val)
        r[t] = prev
    qv[idx[o]] = np.minimum(r, 1)
    return qv
R["q"] = bh(R.p.to_numpy())
R["sig"] = R.q < 0.05
R.to_csv(AQUI / "quipus_legibles.csv", index=False)
print(R[["tasa", "tasa_neta", "cobertura", "acierto_si_via"]].describe().round(3).to_string())
print("quipus con q<0.05:", int(R.sig.sum()), "de", int(R.nval.gt(0).sum()))

# ------------------------------------------------------------------ nulos agregados
tot_p = np.array([sum(nh_q[k][p] for k in Q) for p in range(NPERM)])
RR = pd.DataFrame([dict(regla=r, quipus=len(regq[r]), cuerdas=regn[r], aciertos=regh[r],
                        tasa=regh[r] / regn[r] if regn[r] else np.nan,
                        nulo=regnull[r] / NPERM,
                        tasa_nula=regnull[r] / NPERM / regn[r] if regn[r] else np.nan)
                   for r in REGLAS if regn[r]])
RR["exceso"] = RR.tasa - RR.tasa_nula
RR.to_csv(AQUI / "reglas_resumen.csv", index=False)
print("\n" + RR.round(3).to_string(index=False))
np.savez(AQUI / "nulo_resumen.npz", tot=tot_p, cop=nh_cop, sum2=nh_sum,
         obs_tot=int(B.hit.sum()), obs_cop=int(O.hit.sum()),
         obs_sum2=int(O[O.regla == "suma_dos"].hit.sum()),
         por_quipu=np.array([nh_q[k] for k in sorted(Q)]))
print("\nagregado: obs %d  nulo media %.1f sd %.1f max %d  p=%.4f"
      % (B.hit.sum(), tot_p.mean(), tot_p.std(), tot_p.max(),
         (1 + int((tot_p >= B.hit.sum()).sum())) / (NPERM + 1)))
print("copia: obs %d  nulo medio %.1f" % (O.hit.sum(), nh_cop.mean()))
print("suma_dos: obs %d  nulo medio %.1f" % (O[O.regla == "suma_dos"].hit.sum(), nh_sum.mean()))
