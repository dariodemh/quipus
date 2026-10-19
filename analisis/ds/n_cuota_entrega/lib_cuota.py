"""Biblioteca común: celdas P (colgante) / S1 (primera subsidiaria) en quipus KFG.

Reglas del brief:
- valor 0 con nudos vacío = cuerda ausente (no es un cero).
- unidad de análisis = quipu; los tests globales usan nulo de intercambio P<->S1
  dentro de cada celda y, además, un test a nivel de quipu (signos / Wilcoxon).
- semilla 20261018.
"""
from pathlib import Path
import re

import numpy as np
import pandas as pd
from scipy import stats

RAIZ = Path(__file__).resolve().parents[3]
DATOS = RAIZ / "analisis" / "datos"
SEED = 20261018


def cargar():
    c = pd.read_csv(DATOS / "cuerdas.csv", low_memory=False, keep_default_na=False)
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce").fillna(0).round().astype(int)
    c["pres"] = (c["nudos"] != "") | (c["valor"] > 0)
    # limpiar rangos de cm del color: "W (12-15)" -> "W"
    c["color_limpio"] = c["color"].map(lambda s: re.sub(r"\([^)]*\)", "", str(s)).strip())
    q = pd.read_csv(DATOS / "quipus.csv", keep_default_na=False)
    return c, q


def incahuasi(q):
    """Sistema Incahuasi según 13/16: quipus UR255-UR279 (28 quipus).

    Ojo: el metadato `procedencia` marca además los JC001-JC023 (Sector B) y
    UR280. La tarea define el sistema como UR255-UR279; los JC se usan como
    control separado.
    """
    out = []
    for k in q.kfg:
        mm = re.match(r"^(UR)(\d{3})[AB]?$", k)
        if mm and 255 <= int(mm.group(2)) <= 279:
            out.append(k)
    return out


def celdas(c, kfg):
    """Devuelve una fila por colgante con su S1 (si existe).

    j = posición del colgante dentro de su grupo (1..n), contando también los
    colgantes ausentes, para alinear columnas sin saltar huecos.
    """
    d = c[c.kfg == kfg].sort_values("orden").copy()
    p = d[d.nivel == 0].copy()
    p["j"] = p.groupby("grupo").cumcount() + 1
    s1 = d[(d.nivel == 1) & d.cuerda.str.endswith("s1")][["padre", "valor", "pres"]].copy()
    s1.columns = ["cuerda", "S1", "presS1"]
    m = p.merge(s1, on="cuerda", how="left")
    m["tiene_s1"] = m["S1"].notna()
    m["S1"] = m["S1"].fillna(0).astype(int)
    m["presS1"] = m["presS1"].map(lambda x: bool(x) if pd.notna(x) else False)
    m = m.rename(columns={"valor": "P", "pres": "presP"})
    return m[["kfg", "grupo", "j", "cuerda", "P", "presP", "S1", "presS1",
              "tiene_s1", "color_limpio"]]


def decada(v):
    v = abs(int(v))
    if v == 0:
        return 0
    return int(np.floor(np.log10(v)))


def _round(v, base):
    return int(v > 0 and v % base == 0)


def _cv(x):
    x = np.asarray(x, dtype=float)
    if len(x) < 2 or x.mean() == 0:
        return np.nan
    return float(x.std(ddof=1) / x.mean())


def metricas(m, solo_obs=True):
    """Métricas de un quipu a partir de sus celdas (versión directa, sin réplicas)."""
    d = m[m.tiene_s1].copy()
    if solo_obs:
        d = d[(d.presP) & (d.P > 0) & (d.presS1) & (d.S1 > 0)].reset_index(drop=True)
    if len(d) == 0:
        return dict(n_celdas=int(len(m[m.tiene_s1])), n_obs=0, n_grupos=0,
                    medP=np.nan, medS1=np.nan,
                    **{k: np.nan for k in ["r10P", "r10S1", "dr10", "r50P", "r50S1",
                                           "dr50", "r100P", "r100S1", "dr100", "pares",
                                           "eqP", "eqS1", "deq", "n_grupos_cv", "cvP",
                                           "cvS1", "dcv"]})
    grupos = [g.index.to_numpy() for _, g in d.groupby("grupo")]
    r = metricas_mat(d.P.to_numpy()[None, :], d.S1.to_numpy()[None, :], grupos)
    out = {k: (float(v[0]) if isinstance(v, np.ndarray) else v) for k, v in r.items()}
    out.update(n_celdas=int(len(m[m.tiene_s1])), n_obs=int(len(d)),
               n_grupos=int(d.grupo.nunique()),
               medP=float(d.P.median()), medS1=float(d.S1.median()))
    return out


def metricas_mat(P, S1, grupos):
    """Estadísticos para B réplicas a la vez. P, S1: arrays (B, n)."""
    P = np.asarray(P)
    S1 = np.asarray(S1)
    if P.ndim == 1:
        P = P[None, :]
        S1 = S1[None, :]
    B = P.shape[0]
    out = {}
    for base, nom in [(10, "r10"), (50, "r50"), (100, "r100")]:
        rp = ((P % base == 0) & (P > 0))
        rs = ((S1 % base == 0) & (S1 > 0))
        out[nom + "P"] = rp.mean(axis=1)
        out[nom + "S1"] = rs.mean(axis=1)
        out["d" + nom] = out[nom + "P"] - out[nom + "S1"]
    eqP = np.zeros(B)
    eqS = np.zeros(B)
    npar = 0
    cvP, cvS, ng = [], [], 0
    for idx in grupos:
        m = len(idx)
        if m < 2:
            continue
        VP = P[:, idx]
        VS = S1[:, idx]
        iu = np.triu_indices(m, 1)
        eqP += (VP[:, iu[0]] == VP[:, iu[1]]).sum(axis=1)
        eqS += (VS[:, iu[0]] == VS[:, iu[1]]).sum(axis=1)
        npar += len(iu[0])
        if m >= 3:
            ng += 1
            with np.errstate(invalid="ignore", divide="ignore"):
                cvP.append(VP.std(axis=1, ddof=1) / VP.mean(axis=1))
                cvS.append(VS.std(axis=1, ddof=1) / VS.mean(axis=1))
    out["eqP"] = eqP
    out["eqS1"] = eqS
    out["pares"] = npar
    out["deq"] = (eqP - eqS) / npar if npar else np.zeros(B)
    out["n_grupos_cv"] = ng
    if ng:
        out["cvP"] = np.nanmean(np.vstack(cvP), axis=0)
        out["cvS1"] = np.nanmean(np.vstack(cvS), axis=0)
        out["dcv"] = out["cvS1"] - out["cvP"]
    else:
        out["cvP"] = out["cvS1"] = out["dcv"] = np.full(B, np.nan)
    return out


def _swap_mat(P, S1, rng, B):
    """B matrices de intercambio: devuelve P', S' con P/S1 permutados por celda."""
    n = len(P)
    sw = rng.random((B, n)) < 0.5
    return np.where(sw, S1[None, :], P[None, :]), np.where(sw, P[None, :], S1[None, :])


def test_quipu(m, nperm=20000, rng=None, lote=2000):
    """p de permutación por quipu para d10, d50, d100, deq, dcv (una cola, dirección P)."""
    rng = rng or np.random.default_rng(SEED)
    d = m[m.tiene_s1]
    d = d[(d.presP) & (d.P > 0) & (d.presS1) & (d.S1 > 0)].reset_index(drop=True)
    obs_met = metricas(m)
    keys = [("dr10", "p_r10"), ("dr50", "p_r50"), ("dr100", "p_r100"),
            ("deq", "p_eq"), ("dcv", "p_cv")]
    obs = {"dr10": obs_met["dr10"], "dr50": obs_met["dr50"],
           "dr100": obs_met["dr100"], "deq": obs_met["deq"], "dcv": obs_met["dcv"]}
    if len(d) < 2:
        obs_met.update({pk: np.nan for _, pk in keys})
        return obs_met, {pk: np.nan for _, pk in keys}
    P = d.P.to_numpy()
    S1 = d.S1.to_numpy()
    grupos = [g.index.to_numpy() for _, g in d.groupby("grupo")]
    # mapas posición -> índice local
    pos = {ix: i for i, ix in enumerate(d.index)}
    gidx = [np.array([pos[i] for i in ix]) for ix in grupos]
    null = {k: [] for k, _ in keys}
    hechos = 0
    while hechos < nperm:
        b = min(lote, nperm - hechos)
        Pp, Ss = _swap_mat(P, S1, rng, b)
        met = metricas_mat(Pp, Ss, gidx)
        for k, _ in keys:
            null[k].append(met[k])
        hechos += b
    ps = {}
    for k, pk in keys:
        arr = np.concatenate(null[k])
        o = obs[k]
        ps[pk] = float((np.sum(arr >= o) + 1) / (nperm + 1))
    obs_met.update(ps)
    return obs_met, ps


def holm(pvals):
    """Holm ajustado; devuelve array en el orden de entrada."""
    p = np.asarray(pvals, dtype=float)
    ok = ~np.isnan(p)
    idx = np.where(ok)[0]
    orden = idx[np.argsort(p[idx])]
    m = len(orden)
    adj = np.full(len(p), np.nan)
    prev = 0.0
    for i, j in enumerate(orden):
        val = min(1.0, (m - i) * p[j])
        prev = max(prev, val)
        adj[j] = prev
    return adj


def perm_global(celdas_df, stat_fn, nperm=20000, rng=None):
    """Nulo de intercambio P<->S1 dentro de celda, agregado sobre todos los quipus.

    Devuelve (observado, p, media_nula, sd_nula).
    """
    rng = rng or np.random.default_rng(SEED)
    obs = stat_fn(celdas_df)
    null = np.empty(nperm)
    for i in range(nperm):
        null[i] = stat_fn(_swap_metricas(celdas_df, rng))
    p = float((np.sum(null >= obs) + 1) / (nperm + 1))
    return obs, p, float(null.mean()), float(null.std(ddof=1))
