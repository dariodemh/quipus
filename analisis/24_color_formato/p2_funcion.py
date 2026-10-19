"""P2: ¿el color marca la función de la cuerda? (diseno.md §3)

Tipos: T1 total de grupo, T2 total de subsidiarias, T3 cabecera-máximo, T4 en blanco (KFG);
T5 marcadora, T6 cuerda superior (OKR); T7 subsidiaria frente a su padre (KFG).
D (distinción) = 1 - fracción de las otras cuerdas de su grupo/vecindad con el mismo color
(D_moda = color distinto del modal se guarda también; ver desviación 1 del informe).
Nulos: NG (cuerda no-tipo al azar del mismo grupo/vecindad), NP (no-tipo de otro grupo en la misma
posición relativa; T1 y T3). Preferencia de color entre quipus con nulo de etiqueta dentro de grupo.
Salidas: p2_instancias.csv, p2_quipu.csv, p2_global.csv, p2_preferido.csv
"""
from collections import Counter

import numpy as np
import pandas as pd

import comun24 as C

rng = np.random.default_rng(C.SEED)
NG_REP, Q_REP = 9999, 1999
c = C.cargar().sort_values(["kfg", "orden"])
c0 = c[(c.nivel == 0) & (c.col != "")].copy()
c0["pos"] = c0.groupby(["kfg", "grupo"]).cumcount()
c0["k"] = c0.groupby(["kfg", "grupo"]).pos.transform("size")
c0["poscl"] = np.where(c0.pos == 0, "primera", np.where(c0.pos == c0.k - 1, "ultima", "interior"))

# ---------------------------------------------------------------- tipos KFG
subs = c[(c.nivel == 1) & c.pres].groupby(["kfg", "padre"]).valor.agg(["sum", "size"])
subs = subs[subs["size"] >= 2]
tipo = {}
for (k, g), x in c0.groupby(["kfg", "grupo"], sort=False):
    v = x.valor.values
    pres = x.pres.values
    idx = x.index.values
    tot = v.sum()
    t1 = set()
    for i in range(len(x)):
        resto = tot - v[i]
        if v[i] > 0 and v[i] == resto and ((v > 0).sum() - 1) >= 2:
            tipo[idx[i]] = "T1"
            t1.add(i)
    pp = np.where(pres)[0]
    if len(x) >= 3 and len(pp) and pp[0] not in t1:
        i = pp[0]
        if v[i] > 0 and (v[i] > np.delete(v, i)).all():
            tipo.setdefault(idx[i], "T3")
    if pres.sum() >= 2:
        for i in np.where(~pres)[0]:
            if x.terminacion.values[i] != "B":
                tipo.setdefault(idx[i], "T4")
for i, r in c0.iterrows():
    if (r.kfg, r.cuerda) in subs.index and i not in tipo:
        s = subs.loc[(r.kfg, r.cuerda)]
        if r.valor > 0 and r.valor == s["sum"]:
            tipo[i] = "T2"
c0["tipo"] = pd.Series(tipo).reindex(c0.index).fillna("")


def D_de(color, otros):
    if len(otros) == 0:
        return np.nan, np.nan
    cnt = Counter(otros)
    return 1 - cnt[color] / len(otros), float(color != cnt.most_common(1)[0][0])


# instancias con NG (mismo grupo) y NP (misma posición, otro grupo)
grupos = {kg: x for kg, x in c0.groupby(["kfg", "grupo"], sort=False)}
# D propio de cada cuerda no-tipo frente a su grupo (para NP)
Dprop = {}
for kg, x in grupos.items():
    cols = list(x.col)
    for j, i in enumerate(x.index):
        Dprop[i] = D_de(cols[j], cols[:j] + cols[j + 1:])[0]
c0["Dprop"] = pd.Series(Dprop)
nt = c0[(c0.tipo == "") & (c0.k >= 3)]
np_pool = {kp: x for kp, x in nt.groupby(["kfg", "poscl"])}

INST = []
for i in c0.index[c0.tipo != ""]:
    r = c0.loc[i]
    x = grupos[(r.kfg, r.grupo)]
    otros = x.drop(i)
    if len(otros) < 2:
        continue
    d, dm = D_de(r.col, list(otros.col))
    cand = otros[otros.tipo == ""]
    ng = []
    for j in cand.index:
        oo = list(otros.drop(j).col)
        if oo:
            ng.append(D_de(c0.at[j, "col"], oo)[0])
    pool = np_pool.get((r.kfg, r.poscl))
    npv = pool[pool.grupo != r.grupo].Dprop.dropna().values if pool is not None else np.array([])
    INST.append(dict(idx=i, kfg=r.kfg, reg=r.reg, grupo=r.grupo, tipo=r.tipo, col=r.col, poscl=r.poscl,
                     D=d, D_moda=dm, ng=np.array(ng), npv=npv))

# ---------------------------------------------------------------- T7 subsidiaria vs padre
par = c[(c.nivel == 1) & (c.col != "")][["kfg", "padre", "col"]].merge(
    c[["kfg", "cuerda", "col"]].rename(columns={"cuerda": "padre", "col": "col_padre"}), on=["kfg", "padre"])
par = par[par.col_padre != ""]

# ---------------------------------------------------------------- T5/T6 OKR
con = C.okr()
oc = pd.read_sql("select KHIPU_ID, CORD_ID, CORD_ORDINAL, CORD_LEVEL, CORD_CLASSIFICATION cls from cord", con)
col = pd.read_sql("select CORD_ID, FULL_COLOR, color_id from ascher_cord_color where PCORD_FLAG=0 order by color_id", con)
km = pd.read_sql("select KHIPU_ID, INVESTIGATOR_NUM from khipu_main", con)
con.close()
col = col.drop_duplicates("CORD_ID")
oc = oc.merge(col[["CORD_ID", "FULL_COLOR"]], on="CORD_ID")
oc["col"] = oc.FULL_COLOR.map(C.norm)
oc = oc[oc.col != ""]
oc["cls"] = oc.cls.fillna("").str.strip()
oc = oc.merge(km, on="KHIPU_ID")
oc["kfg"] = oc.INVESTIGATOR_NUM.astype(str)
oc["reg"] = oc.kfg.map(lambda s: C.registrador(s) if len(s) >= 5 else "?")
oc = oc.sort_values(["KHIPU_ID", "CORD_LEVEL", "CORD_ORDINAL"])
for t, code in (("T5", "M"), ("T6", "T")):
    for kid, x in oc.groupby(["KHIPU_ID", "CORD_LEVEL"]):
        tt = x[x.cls == code]
        if len(tt) == 0:
            continue
        no = x[x.cls != code]
        for _, r in tt.iterrows():
            vec = no.iloc[np.argsort(np.abs(no.CORD_ORDINAL.values - r.CORD_ORDINAL), kind="stable")[:6]]
            if len(vec) < 3:
                continue
            d, dm = D_de(r.col, list(vec.col))
            vc = list(vec.col)
            ng = [D_de(vc[j], vc[:j] + vc[j + 1:])[0] for j in range(len(vc))]
            INST.append(dict(idx=r.CORD_ID, kfg=r.kfg, reg=r.reg, grupo=-1, tipo=t, col=r.col, poscl="",
                             D=d, D_moda=dm, ng=np.array(ng), npv=np.array([])))

I = pd.DataFrame(INST)
I = I[I.ng.map(len) > 0].reset_index(drop=True)


def sim_sum(arrs, nrep):
    """suma de un sustituto al azar por instancia, nrep réplicas"""
    tot = np.zeros(nrep)
    for a in arrs:
        tot += a[rng.integers(0, len(a), nrep)]
    return tot


# ---------------------------------------------------------------- global
G = []
for t in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    for reg in ["todos", "UR", "AS"]:
        x = I[(I.tipo == t) & ((I.reg == reg) if reg != "todos" else True)]
        if len(x) < 10:
            continue
        obs = x.D.sum()
        nul = sim_sum(list(x.ng), NG_REP)
        row = dict(tipo=t, reg=reg, n=len(x), n_quipus=x.kfg.nunique(), D_media=round(x.D.mean(), 3),
                   NG_media=round(nul.mean() / len(x), 3), p_NG=C.p_emp(obs, nul),
                   D_moda_media=round(x.D_moda.mean(), 3))
        y = x[x.npv.map(len) > 0]
        if t in ("T1", "T3") and len(y) >= 10:
            nul2 = sim_sum(list(y.npv), NG_REP)
            row.update(n_NP=len(y), D_NP_obs=round(y.D.mean(), 3), NP_media=round(nul2.mean() / len(y), 3),
                       p_NP=C.p_emp(y.D.sum(), nul2))
        G.append(row)

# T7
for reg in ["todos", "UR", "AS"]:
    x = par if reg == "todos" else par[par.kfg.map(C.registrador) == reg]
    obs = (x.col == x.col_padre).sum()
    nul = np.zeros(NG_REP)
    grp = [g for _, g in x.groupby("kfg")]
    for g in grp:
        cs, cp = g.col.values, g.col_padre.values
        # nulo: colores de subsidiaria permutados dentro del quipu
        perm = np.array([rng.permutation(cs) for _ in range(NG_REP)])
        nul += (perm == cp).sum(1)
    G.append(dict(tipo="T7", reg=reg, n=len(x), n_quipus=x.kfg.nunique(),
                  D_media=round(1 - obs / len(x), 3), NG_media=round(1 - nul.mean() / len(x), 3),
                  p_NG=C.p_emp(-obs, -nul), p_igual_mayor=C.p_emp(obs, nul),
                  igual_obs=round(obs / len(x), 3), igual_nulo=round(nul.mean() / len(x), 3)))
GG = pd.DataFrame(G)
GG.to_csv(C.AQUI / "p2_global.csv", index=False)

# ---------------------------------------------------------------- por quipu
Q = []
for (k, t), x in I.groupby(["kfg", "tipo"]):
    if len(x) < 3:
        continue
    nul = sim_sum(list(x.ng), Q_REP)
    Q.append(dict(kfg=k, reg=x.reg.iloc[0], tipo=t, n=len(x), D=round(x.D.mean(), 3),
                  NG=round(nul.mean() / len(x), 3), p=C.p_emp(x.D.sum(), nul),
                  modal=Counter(x.col).most_common(1)[0][0],
                  modal_share=round(Counter(x.col).most_common(1)[0][1] / len(x), 3)))
QQ = pd.DataFrame(Q)
QQ["q"] = QQ.groupby("tipo").p.transform(lambda s: C.bh(s.values))
QQ.to_csv(C.AQUI / "p2_quipu.csv", index=False)

# ---------------------------------------------------------------- color preferido entre quipus
# nulo: la etiqueta de tipo pasa a una cuerda al azar del mismo grupo (KFG) o del mismo khipu/nivel (OKR)
pool_grupo = {kg: list(x.col) for kg, x in grupos.items()}
pool_okr = {k: list(x.col) for k, x in oc.groupby("kfg")}
P = []
for t in ["T1", "T2", "T3", "T4", "T5", "T6"]:
    x = I[I.tipo == t]
    qs = [(k, y) for k, y in x.groupby("kfg") if len(y) >= 3]
    if len(qs) < 5:
        continue
    obs_modal = [Counter(y.col).most_common(1)[0][0] for _, y in qs]
    obsW = sum(m == "W" for m in obs_modal)
    pools = []
    for k, y in qs:
        if t in ("T5", "T6"):
            pools.append([pool_okr[k]] * len(y))
        else:
            pools.append([pool_grupo[(k, g)] for g in y.grupo])
    nulW = np.zeros(Q_REP)
    nultop = np.zeros(Q_REP)
    for b in range(Q_REP):
        mods = []
        for pl in pools:
            ch = [p[rng.integers(len(p))] for p in pl]
            mods.append(Counter(ch).most_common(1)[0][0])
        nulW[b] = sum(m == "W" for m in mods)
        nultop[b] = Counter(mods).most_common(1)[0][1]
    top = Counter(obs_modal).most_common(3)
    P.append(dict(tipo=t, n_quipus=len(qs), modal_W=obsW, nulo_W=round(nulW.mean(), 2), p_W=C.p_emp(obsW, nulW),
                  top_obs=", ".join(f"{a}:{b}" for a, b in top), top_n=top[0][1],
                  nulo_top=round(nultop.mean(), 2), p_top=C.p_emp(top[0][1], nultop),
                  frac_W=round(obsW / len(qs), 3)))
PP = pd.DataFrame(P)
PP.to_csv(C.AQUI / "p2_preferido.csv", index=False)

I.drop(columns=["ng", "npv"]).to_csv(C.AQUI / "p2_instancias.csv", index=False)
pd.set_option("display.width", 250)
print(GG.to_string())
print(PP.to_string())
s = QQ.groupby("tipo").agg(n_quipus=("kfg", "size"), sig=("q", lambda q: int((q < 0.05).sum())))
print(s)
