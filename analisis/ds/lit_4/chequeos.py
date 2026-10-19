"""Chequeos de afirmaciones de la literatura sobre quipus (lit_4).

Lee analisis/datos/{cuerdas,quipus,grupos}.csv y comprueba, con modelo nulo
explícito cuando corresponde:
  V1 Hyland (2024): prevalencia de "nudos inferiores" (nether knots) > 20 %.
  V2 Medrano & Khosla (2024): formulas de Ascher en >= 74 % de los quipus.
  V3 Contreras (2026): replicacion del patron recto/verso del valle del Santa.
  V4 Thompson (2025): correcciones numericas concretas (AS010, AS044, AS115, AS128).
  V5 Medrano & Khosla (2024): cuerdas blancas como marcadores de limite de grupo.
  V6 Thompson (2024)/FitzPatrick (2026): quipu mas grande y posible par de Arica.

No modifica nada fuera de analisis/ds/lit_4/. Semilla fija.
"""
import json
import re
import numpy as np
import pandas as pd

SEM = 20261017
NPERM = 2000
BASE = "analisis/datos"


def cargar():
    c = pd.read_csv(f"{BASE}/cuerdas.csv", dtype=str)
    q = pd.read_csv(f"{BASE}/quipus.csv", dtype=str)
    g = pd.read_csv(f"{BASE}/grupos.csv", dtype=str)
    c["v"] = pd.to_numeric(c["valor"], errors="coerce")
    c["orden"] = pd.to_numeric(c["orden"], errors="coerce")
    c["grupo"] = c["grupo"].astype(int)
    c["nivel"] = c["nivel"].astype(int)
    g["grupo"] = g["grupo"].astype(int)
    c["pn"] = c["cuerda"].str.extract(r"^p(\d+)")[0].astype(float)
    return c, q, g


CLUST = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([^)]*)\),(-?[\d.]+)")


def clusters(s):
    """[(tipo, pos_cm, valor_aportado), ...] en el orden del registro (arriba->abajo)."""
    if not isinstance(s, str):
        return []
    return [(m.group(2), float(m.group(3)), float(m.group(5)))
            for m in CLUST.finditer(s)]


# ---------------------------------------------------------------- V1 nether
def es_nether(cl, modo="dos_ultimos"):
    if modo == "dos_ultimos":
        return len(cl) >= 2 and 1 <= cl[-1][2] <= 9 and 1 <= cl[-2][2] <= 9
    if modo == "ultimo_tras_unidad":
        # el ultimo cluster es de unidades y hay otro cluster de unidades antes
        return (len(cl) >= 2 and 1 <= cl[-1][2] <= 9
                and any(1 <= x[2] <= 9 for x in cl[:-1]))
    raise ValueError(modo)


def v1(c):
    c = c.copy()
    c["cl"] = c["nudos"].map(clusters)
    res = {}
    nq = c["kfg"].nunique()
    rng = np.random.default_rng(SEM)
    for modo in ["dos_ultimos", "ultimo_tras_unidad"]:
        c["net"] = c["cl"].map(lambda x: es_nether(x, modo))
        porq = c.groupby("kfg")["net"].any()
        # Nulo: permutacion uniforme del orden de clusters dentro de cada cuerda.
        # La probabilidad del evento se calcula de forma analitica por cuerda y
        # luego se simula el "al menos uno" por quipu (cuerdas independientes).
        p_any = {}
        for k, x in c.groupby("kfg"):
            probs = []
            for cl in x["cl"]:
                kk = len(cl)
                if kk < 2:
                    continue
                u = sum(1 for t in cl if 1 <= t[2] <= 9)
                if modo == "dos_ultimos":
                    p = u * (u - 1) / (kk * (kk - 1))
                else:
                    if kk == 2:
                        p = (u / kk) * ((u - 1) / (kk - 1))
                    else:
                        from math import comb
                        p = (u / kk) * (1 - comb(kk - u, 2) / comb(kk - 1, 2))
                probs.append(p)
            if probs:
                p_any[k] = 1 - np.prod([1 - p for p in probs])
        pa = np.array(list(p_any.values()))
        perm_counts = (rng.random((NPERM, len(pa))) < pa).sum(axis=1)
        obs_n = int(porq.sum())
        pval = (1 + (perm_counts >= obs_n).sum()) / (NPERM + 1)
        res[modo] = dict(cuerdas=int(c["net"].sum()), quipus=obs_n,
                         n_quipus=int(nq), pct=round(100 * obs_n / nq, 1),
                         nulo_media=round(float(perm_counts.mean()), 1),
                         nulo_pct=round(100 * float(perm_counts.mean()) / nq, 1),
                         p_empirico=float(pval))
    return res


# ---------------------------------------------------------------- V2 Ascher
def relaciones_grupo(c, g):
    """Devuelve por quipu si existe alguna de estas relaciones de suma:
    B) en un grupo de >=3 colgantes, el primero vale la suma de los demas;
    B2) en un grupo de >=3, algun colgante vale la suma de los demas;
    C) un grupo de 1 colgante vale la suma del grupo anterior.
    Solo colgantes nivel 0 con nudos (valor no ausente).
    """
    out = {}
    pend = c[(c["nivel"] == 0) & c["nudos"].notna() & c["v"].notna()]
    for k, d in pend.groupby("kfg"):
        gg = g[g["kfg"] == k].sort_values("grupo")
        vals = {int(gr): list(x["v"]) for gr, x in d.groupby("grupo")}
        b = b2 = cc = False
        totales = {}
        for gr, vv in vals.items():
            if len(vv) >= 2:
                total = sum(vv)
                totales[gr] = total
                if len(vv) >= 3:
                    if abs(vv[0] - (total - vv[0])) < 1e-6:
                        b = True
                    if any(abs(x - (total - x)) < 1e-6 for x in vv):
                        b2 = True
        for gr in sorted(vals):
            vv = vals[gr]
            if len(vv) == 1:
                prev = [x for x in vals if x < gr]
                if prev:
                    pg = max(prev)
                    if pg in totales and abs(vv[0] - totales[pg]) < 1e-6:
                        cc = True
        out[k] = dict(B=b, B2=b2, C=cc, cualquiera=(b or b2 or cc))
    return pd.DataFrame(out).T


def v2(c, g):
    obs = relaciones_grupo(c, g)
    pend = c[(c["nivel"] == 0) & c["nudos"].notna() & c["v"].notna()]
    rng = np.random.default_rng(SEM)
    nq = obs.shape[0]
    keys = ["B", "B2", "C", "cualquiera"]
    obs_rate = {k: round(100 * obs[k].astype(bool).mean(), 1) for k in keys}
    # estructuras precalculadas: por quipu, valores y fronteras de grupo
    est = {}
    for k, d in pend.groupby("kfg"):
        d = d.sort_values("grupo")
        vals = d["v"].values.astype(float)
        gr = d["grupo"].values
        cortes = []
        i = 0
        while i < len(gr):
            j = i
            while j + 1 < len(gr) and gr[j + 1] == gr[i]:
                j += 1
            cortes.append((i, j + 1))
            i = j + 1
        est[k] = (vals, cortes)
    perm = {k: np.empty(NPERM) for k in keys}
    for it in range(NPERM):
        nb = nb2 = nc = nany = 0
        for k, (vals, cortes) in est.items():
            v = rng.permutation(vals)
            tot = {}
            b = b2 = cc = False
            for (i, j) in cortes:
                vv = v[i:j]
                if len(vv) >= 2:
                    s = vv.sum()
                    tot[(i, j)] = s
                    if len(vv) >= 3:
                        if abs(vv[0] - (s - vv[0])) < 1e-6:
                            b = True
                        if np.any(np.abs(vv - (s - vv)) < 1e-6):
                            b2 = True
            for idx, (i, j) in enumerate(cortes):
                if j - i == 1 and idx > 0:
                    pg = cortes[idx - 1]
                    if pg in tot and abs(v[i] - tot[pg]) < 1e-6:
                        cc = True
            nb += b; nb2 += b2; nc += cc; nany += (b or b2 or cc)
        perm["B"][it] = 100 * nb / nq
        perm["B2"][it] = 100 * nb2 / nq
        perm["C"][it] = 100 * nc / nq
        perm["cualquiera"][it] = 100 * nany / nq
    pvals = {}
    for k in keys:
        pvals[k] = float((1 + (perm[k] >= obs_rate[k]).sum()) / (NPERM + 1))
    return dict(n_quipus=int(nq), obs=obs_rate,
                nulo={k: round(float(perm[k].mean()), 2) for k in keys},
                p_empirico=pvals,
                detalle=obs.astype(bool).sum().to_dict())


# ---------------------------------------------------------------- V3 Santa
def v3(c):
    ks = ["UR087", "UR088", "UR089", "UR090", "UR091", "UR092"]
    d = c[c["kfg"].isin(ks)]
    filas = []
    for k in ks:
        x = d[d["kfg"] == k]
        rv = x[x["union"].isin(["R", "V"])]
        filas.append(dict(kfg=k, cuerdas=len(x),
                          R=int((rv["union"] == "R").sum()),
                          V=int((rv["union"] == "V").sum()),
                          U=int((x["union"] == "U").sum()),
                          pct_R=round(100 * (rv["union"] == "R").mean(), 1)))
    rv = d[d["union"].isin(["R", "V"])]
    agg = dict(n=int(len(rv)), R=int((rv["union"] == "R").sum()),
               V=int((rv["union"] == "V").sum()),
               pct_R=round(100 * (rv["union"] == "R").mean(), 1))
    puros = sum(1 for f in filas if f["pct_R"] in (0.0, 100.0))
    mixto = [f for f in filas if f["pct_R"] not in (0.0, 100.0)]
    return dict(filas=filas, agregado=agg, puros=puros, mixto=mixto)


# ---------------------------------------------------------------- V4 Thompson
def v4(c):
    c = c.copy()
    out = {}
    # AS128: p170 + p170s1 = 75 ; suma p177..p198 = 72
    d = c[c["kfg"] == "AS128"]
    v170 = d.loc[d["cuerda"] == "p170", "v"]
    v170s1 = d.loc[d["cuerda"] == "p170s1", "v"]
    sub = d[d["cuerda"].str.match(r"^p(17[7-9]|18[0-9]|19[0-8])$")]
    out["AS128"] = dict(p170=float(v170.iloc[0]) if len(v170) else None,
                        p170s1=float(v170s1.iloc[0]) if len(v170s1) else None,
                        suma_170=float(v170.sum() + v170s1.sum()),
                        n_p177_198=int(len(sub)),
                        suma_p177_198=float(sub["v"].sum()))
    # AS115: 188+205+213 y 266+225+245
    d = c[c["kfg"] == "AS115"]
    vals = set(d["v"].dropna())
    out["AS115"] = dict(tripleta1=[188, 205, 213], suma1=606,
                        tiene1=all(v in vals for v in [188, 205, 213]),
                        tripleta2=[266, 225, 245], suma2=736,
                        tiene2=all(v in vals for v in [266, 225, 245]))
    # AS044: grupo 10 = 248 (Thompson: 248 vs 228)
    d = c[(c["kfg"] == "AS044") & (c["nivel"] == 0)]
    out["AS044"] = dict(suma_grupo10=float(d[d["grupo"] == 10]["v"].sum()),
                        grupos={int(k): float(x["v"].sum()) for k, x in d.groupby("grupo")})
    # AS010: p1 + p1s1 (= primeras cuerdas) y primeros 7 colgantes
    d = c[c["kfg"] == "AS010"]
    out["AS010"] = dict(p1=float(d.loc[d["cuerda"] == "p1", "v"].sum()),
                        p1s1=float(d.loc[d["cuerda"] == "p1s1", "v"].sum()),
                        primeros7_por_orden=float(
                            d[(d["nivel"] == 0)].sort_values("orden")["v"].head(7).sum()),
                        primeros7_por_pn=float(
                            d[d["nivel"] == 0].sort_values("pn")["v"].head(7).sum()))
    # AS014 y AS021: notacion de nudos corregida
    out["AS014_p20"] = c[(c["kfg"] == "AS014") & (c["nudos"].str.contains("20", na=False))][
        ["cuerda", "nudos"]].head(3).to_dict("records")
    out["AS021_p3"] = c[(c["kfg"] == "AS021")][["cuerda", "nudos"]].head(3).to_dict("records")
    return out


# ---------------------------------------------------------------- V5 blanco
def v5(c, g):
    d = c[(c["nivel"] == 0) & c["pn"].notna()].copy()
    d["blanco"] = d["color"].fillna("").eq("W")
    d["blanco_amp"] = d["color"].fillna("").str.contains("W")
    filas = []
    for k, x in d.groupby("kfg"):
        gg = g[g["kfg"] == k]
        bound, interior = [], []
        for _, row in gg.iterrows():
            gr = x[(x["pn"] >= float(row["desde"])) & (x["pn"] <= float(row["hasta"]))]
            if len(gr) < 2:
                continue
            gr = gr.sort_values("pn")
            bound += [gr.iloc[0], gr.iloc[-1]]
            interior += [r for _, r in gr.iloc[1:-1].iterrows()]
        if not bound or not interior:
            continue
        filas.append(dict(kfg=k,
                          n_b=len(bound), n_i=len(interior),
                          b=sum(r["blanco"] for r in bound),
                          i=sum(r["blanco"] for r in interior),
                          b_amp=sum(r["blanco_amp"] for r in bound),
                          i_amp=sum(r["blanco_amp"] for r in interior)))
    f = pd.DataFrame(filas)
    f["d"] = 100 * (f["b"] / f["n_b"] - f["i"] / f["n_i"])
    obs_b, obs_i = f["b"].sum() / f["n_b"].sum(), f["i"].sum() / f["n_i"].sum()
    obs_diff = float(f["d"].mean())
    # nulo: permutar colores entre colgantes dentro de cada quipu
    rng = np.random.default_rng(SEM)
    cols = {}
    pos = {}
    for k, x0 in d.groupby("kfg"):
        x = x0.sort_values("pn")
        cols[k] = x["color"].fillna("").eq("W").values
        idx = {int(p): i for i, p in enumerate(x["pn"].values)}
        gg = g[g["kfg"] == k]
        b, it = [], []
        for _, row in gg.iterrows():
            ps = [p for p in x["pn"].values if float(row["desde"]) <= p <= float(row["hasta"])]
            ps = sorted(ps)
            if len(ps) < 2:
                continue
            b += [idx[int(ps[0])], idx[int(ps[-1])]]
            it += [idx[int(p)] for p in ps[1:-1]]
        if b and it:
            pos[k] = (np.array(b), np.array(it))
    stats = []
    for _ in range(NPERM):
        ds = []
        for k, (b, it) in pos.items():
            arr = rng.permutation(cols[k])
            ds.append(100 * (arr[b].mean() - arr[it].mean()))
        stats.append(np.mean(ds))
    p = (1 + (np.array(stats) >= obs_diff).sum()) / (NPERM + 1)
    return dict(n_quipus=int(len(f)), n_frontera=int(f["n_b"].sum()),
                n_interior=int(f["n_i"].sum()),
                pct_blanco_frontera=round(100 * obs_b, 1),
                pct_blanco_interior=round(100 * obs_i, 1),
                dif_media_pp=round(obs_diff, 1),
                media_nulo_pp=round(float(np.mean(stats)), 2),
                p_empirico=float(p),
                amp_frontera=round(100 * f["b_amp"].sum() / f["n_b"].sum(), 1),
                amp_interior=round(100 * f["i_amp"].sum() / f["n_i"].sum(), 1))


# ---------------------------------------------------------------- V6 grande
def v6(c, q):
    n = c.groupby("kfg").size().sort_values(ascending=False)
    top = n.head(5)
    info = q.set_index("kfg").loc[top.index, ["okr", "procedencia", "region", "museo"]]
    # pares de Arica/Lluta: comparar total de AS069 con totales de UR131A-C
    tot = c.groupby("kfg")["v"].sum()
    cand = ["UR131A", "UR131B", "UR131C", "KH0083", "KH0267", "UR084", "UR130", "UR132"]
    comp = {k: round(float(tot.get(k, np.nan)), 1) for k in cand}
    return dict(top={k: int(v) for k, v in top.items()},
                info=info.to_dict("index"),
                total_AS069=round(float(tot["AS069"]), 1),
                totales_candidatos=comp)


if __name__ == "__main__":
    c, q, g = cargar()
    res = {}
    res["V1_nether"] = v1(c)
    print("V1", json.dumps(res["V1_nether"], ensure_ascii=False))
    res["V2_ascher"] = v2(c, g)
    print("V2", json.dumps(res["V2_ascher"], ensure_ascii=False))
    res["V3_santa"] = v3(c)
    print("V3", json.dumps(res["V3_santa"], ensure_ascii=False))
    res["V4_thompson"] = v4(c)
    print("V4", json.dumps(res["V4_thompson"], ensure_ascii=False)[:1200])
    res["V5_blanco"] = v5(c, g)
    print("V5", json.dumps(res["V5_blanco"], ensure_ascii=False))
    res["V6_grande"] = v6(c, q)
    print("V6", json.dumps(res["V6_grande"], ensure_ascii=False))
    with open("analisis/ds/lit_4/resultados.json", "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
