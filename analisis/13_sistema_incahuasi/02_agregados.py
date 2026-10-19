"""Tarea 1b. ¿Qué cuerda de qué quipu es un TOTAL de cuerdas de otro (o del mismo)? Búsqueda exhaustiva.

Para cada quipu A se calculan agregados candidatos (solo valores >=100):
  G   total de colgantes anudados de cada grupo (>=2 anudados)
  GS  total de grupo incluyendo subsidiarias (grupos con alguna subsidiaria anudada)
  GSUB total de las subsidiarias del grupo (>=2)
  PS  colgante + sus subsidiarias (con >=1 subsidiaria anudada);  S  suma de las subsidiarias de un colgante (>=2)
  COL total de cada columna (posición dentro del grupo) en quipus con >=4 grupos del tamaño modal
  CG  total por color dentro de un grupo (>=2 cuerdas de ese color y >=2 colores en el grupo)
  CQ  total por color en todo el quipu;  BLK total de bloque (grupos entre grupos vacíos);  TOT total de colgantes
Cada agregado se busca en las cuerdas anudadas de cada quipu B del archivo (incluido B = A, «interno»: un total
no puede igualar exactamente a una de sus partes, todas >0, así que no hace falta excluirlas en la versión exacta).
Estadístico: nº de agregados distintos hallados en B, exacto y con tolerancia ±1 dígito.
Nulo: permutar los valores de A dentro de cada nivel (colgantes entre posiciones de colgante, subsidiarias entre
posiciones de subsidiaria) y recalcular (conserva magnitudes, tamaños de grupo y huecos). B fijo. 1000 réplicas.
Solo reciben nulo las pruebas con >=2 coincidencias; el resto entra con p = 1 en el BH-FDR (m = todas las pruebas).
Refinamiento adaptativo: las pruebas con p <= 0,005 reciben 20 000 réplicas más (con 1000 el p mínimo, 0,001,
no puede sobrevivir a un BH con m ~ 13 500).
Salidas: agregados_pruebas.csv, agregados_hallazgos.csv
"""
import sys
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13002
NPERM = 1000
NPERM2 = 20000
TOLS = np.array([0, 1, 10, 100, 1000, 10000])
TIPOS = ["G", "GS", "GSUB", "PS", "S", "COL", "CG", "CQ", "BLK", "TOT"]

c, q = C.archivo()
c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
c["cprinc"] = c.color.str.split(r"[(\s]", regex=True).str[0]
c["pend"] = c.cuerda.str.extract(r"^(p\d+)")[0]


def indices(s):
    """Para un quipu, lista de (tipo, array de etiquetas por cuerda o -1, nº mínimo de partes)."""
    n = len(s)
    lv0 = (s.nivel == 0).to_numpy()
    sub = ~lv0
    out = []
    gid = pd.factorize(s.grupo)[0]
    out.append(("G", np.where(lv0, gid, -1), 2))
    out.append(("GS", gid.copy(), 2))
    out.append(("GSUB", np.where(sub, gid, -1), 2))
    pid = pd.factorize(s.pend)[0]
    out.append(("PS", pid.copy(), 2))
    out.append(("S", np.where(sub, pid, -1), 2))
    tam = s[lv0].groupby("grupo").size()
    lab = -np.ones(n, int)
    if len(tam):
        k = tam.mode().iloc[0]
        gk = set(tam[tam == k].index)
        if k >= 2 and len(gk) >= 4:
            pos = s[lv0].groupby("grupo").cumcount()
            m = lv0 & s.grupo.isin(gk).to_numpy()
            lab[m] = pos.reindex(s.index)[m].to_numpy()
    out.append(("COL", lab, 2))
    ncol = s[lv0].groupby("grupo").cprinc.nunique()
    multi = s.grupo.isin(ncol[ncol >= 2].index).to_numpy()
    out.append(("CG", np.where(lv0 & multi, pd.factorize(s.grupo.astype(str) + "|" + s.cprinc)[0], -1), 2))
    out.append(("CQ", np.where(lv0, pd.factorize(s.cprinc)[0], -1), 2))
    vac = s.groupby("grupo").pres.sum()
    blk, b, prev_vacio = {}, 0, False
    for g, v in vac.items():
        if v == 0:
            prev_vacio = True
            continue
        if prev_vacio:
            b += 1
        prev_vacio = False
        blk[g] = b
    lab = np.where(lv0, s.grupo.map(blk).fillna(-1).astype(int), -1)
    out.append(("BLK", lab if b >= 1 else -np.ones(n, int), 2))
    out.append(("TOT", np.where(lv0, 0, -1), 2))
    return out


def agregados(val, idx, s):
    """val: valores (0 = ausente). Devuelve dict tipo -> array de totales >=100 (con >=2 partes anudadas)."""
    pres = val > 0
    res = {}
    for t, lab, mn in idx:
        m = lab >= 0
        if not m.any():
            res[t] = np.array([], int)
            continue
        L = lab[m]
        tot = np.bincount(L, weights=val[m]).astype(int)
        cnt = np.bincount(L, weights=pres[m])
        sel = (cnt >= mn) & (tot >= 100)
        if t == "PS":  # exige al menos una subsidiaria anudada además del colgante
            nsub = np.bincount(L, weights=(pres & (s.nivel.to_numpy() > 0))[m], minlength=len(cnt))
            sel &= nsub >= 1
        res[t] = np.unique(tot[sel])
    return res


def cuenta(vals, bset_e, bset_t):
    return int(np.isin(vals, bset_e).sum()), int(np.isin(vals, bset_t).sum())


rng = np.random.default_rng(SEED)
quipus = {k: c[c.kfg == k] for k in C.ARCHIVO}
BS = {}
for k, s in quipus.items():
    v = np.unique(s[s.pres].valor.to_numpy())
    BS[k] = (v, np.unique((v[:, None] + np.concatenate([TOLS, -TOLS])[None, :]).ravel()))
filas, hall = [], []
for a, s in quipus.items():
    if s.pres.sum() < 3:
        continue
    idx = indices(s)
    val = s.valor.where(s.pres, 0).to_numpy()
    obs = agregados(val, idx, s)
    tipos = [t for t in TIPOS if len(obs[t])]
    oc = {(t, b): cuenta(obs[t], *BS[b]) for t in tipos for b in C.ARCHIVO}
    vivos = [k for k, (e, tl) in oc.items() if max(e, tl) >= 2]
    N = {k: np.zeros((NPERM, 2), int) for k in vivos}
    fino = []
    if vivos:
        niv = s.nivel.to_numpy()
        masks = [niv == lv for lv in np.unique(niv)]
        for r in range(NPERM):
            vp = val.copy()
            for m in masks:
                vp[m] = rng.permutation(vp[m])
            ag = agregados(vp, idx, s)
            for k in vivos:
                N[k][r] = cuenta(ag[k[0]], *BS[k[1]])
    # refinamiento adaptativo
    fino = [k for k in vivos if (np.sum(N[k][:, 0] >= oc[k][0]) + 1) / (NPERM + 1) <= 0.005
            or (np.sum(N[k][:, 1] >= oc[k][1]) + 1) / (NPERM + 1) <= 0.005]
    if fino:
        extra = {k: np.zeros((NPERM2, 2), int) for k in fino}
        for r in range(NPERM2):
            vp = val.copy()
            for m in masks:
                vp[m] = rng.permutation(vp[m])
            ag = agregados(vp, idx, s)
            for k in fino:
                extra[k][r] = cuenta(ag[k[0]], *BS[k[1]])
        for k in fino:
            N[k] = np.vstack([N[k], extra[k]])
    for (t, b), (e, tl) in oc.items():
        f = dict(A=a, tipo=t, B=b, n_agregados=len(obs[t]), exactos=e, tolerantes=tl)
        if (t, b) in N and len(N[(t, b)]):
            M = N[(t, b)]
            nn = len(M)
            f.update(nulo_e=M[:, 0].mean(), nulo_t=M[:, 1].mean(), p_e=(np.sum(M[:, 0] >= e) + 1) / (nn + 1),
                     p_t=(np.sum(M[:, 1] >= tl) + 1) / (nn + 1), replicas=nn)
        else:
            f.update(nulo_e=np.nan, nulo_t=np.nan, p_e=1.0, p_t=1.0)
        filas.append(f)
    print(a, "tipos:", tipos, "pruebas con nulo:", len(vivos), "refinadas:", len(fino) if vivos else 0,
          flush=True, file=sys.stderr)

df = pd.DataFrame(filas)
df["q_e"] = C.bh(df.p_e)
df["q_t"] = C.bh(df.p_t)
df = df.sort_values(["p_e", "p_t"])
df.to_csv(C.AQUI / "agregados_pruebas.csv", index=False, float_format="%.4g")
sig = df[(df.q_e < 0.05) | (df.q_t < 0.05)]
pd.set_option("display.width", 220)
print(f"pruebas: {len(df)}; con nulo: {df.nulo_e.notna().sum()}; q_e<0,05: {(df.q_e < 0.05).sum()}; "
      f"q_t<0,05: {(df.q_t < 0.05).sum()}")
print(sig.to_string(index=False))

# lista de coincidencias concretas (exactas) de las pruebas significativas o con p_e <= 0,002
top = df[(df.q_e < 0.05) | (df.q_t < 0.05) | (df.p_e <= 0.002)]
for _, r in top.iterrows():
    s = quipus[r.A]
    idx = indices(s)
    val = s.valor.where(s.pres, 0).to_numpy()
    for t, lab, mn in idx:
        if t != r.tipo:
            continue
        for L in np.unique(lab[lab >= 0]):
            m = (lab == L) & (val > 0)
            v = int(val[m].sum())
            if m.sum() < 2 or v < 100:
                continue
            sb = quipus[r.B][quipus[r.B].pres]
            for cb in sb[sb.valor == v].itertuples():
                hall.append(dict(A=r.A, tipo=r.tipo, total=v, partes=" + ".join(map(str, val[m])),
                                 cuerdas_A=",".join(s.cuerda.to_numpy()[m][:4]) + ("..." if m.sum() > 4 else ""),
                                 B=r.B, cuerda_B=cb.cuerda, grupo_B=cb.grupo, color_B=cb.color))
pd.DataFrame(hall).to_csv(C.AQUI / "agregados_hallazgos.csv", index=False)
print(f"coincidencias exactas listadas: {len(hall)}")
