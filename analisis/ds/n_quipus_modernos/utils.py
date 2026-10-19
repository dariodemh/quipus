# -*- coding: utf-8 -*-
"""Utilidades comunes: carga, nulos por permutacion, Holm, entropia/MI."""
import numpy as np
import pandas as pd

SEMILLA = 20261018


def load():
    c = pd.read_csv("cuerdas_merged.csv")
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce")
    c["nudos"] = c["nudos"].fillna("")
    return c


def holm(pvals, names=None):
    """Holm-Bonferroni. Devuelve q (mismo orden) y rechazos."""
    p = np.asarray(pvals, float)
    m = len(p)
    order = np.argsort(p)
    q = np.empty(m)
    prev = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * p[i]
        val = max(val, prev)
        q[i] = min(val, 1.0)
        prev = q[i]
    return q


def perm_p(obs, null, side="greater"):
    """p empirico con correccion +1."""
    null = np.asarray(null, float)
    if side == "greater":
        k = np.sum(null >= obs)
    elif side == "less":
        k = np.sum(null <= obs)
    else:
        k = np.sum(np.abs(null - np.mean(null)) >= abs(obs - np.mean(null)))
    return (1.0 + k) / (1.0 + len(null))


def mi(x, y):
    """Mutual information en bits entre dos categoricas (listas/Series)."""
    x = pd.Series(list(x)).astype(str)
    y = pd.Series(list(y)).astype(str)
    n = len(x)
    if n == 0:
        return 0.0
    ct = pd.crosstab(x, y).values.astype(float)
    px = ct.sum(1) / n
    py = ct.sum(0) / n
    pxy = ct / n
    nz = pxy > 0
    return float(np.sum(pxy[nz] * np.log2(pxy[nz] / np.outer(px, py)[nz])))


def weighted_mean(vals, w):
    vals = np.asarray(vals, float)
    w = np.asarray(w, float)
    ok = np.isfinite(vals) & np.isfinite(w) & (w > 0)
    if ok.sum() == 0:
        return np.nan
    return float(np.sum(vals[ok] * w[ok]) / np.sum(w[ok]))


def zscore_effect(obs, null):
    null = np.asarray(null, float)
    sd = np.std(null, ddof=1)
    if sd == 0:
        return np.nan
    return (obs - np.mean(null)) / sd


def describe(obs, null, side):
    return dict(obs=float(obs), null_mean=float(np.mean(null)),
                null_sd=float(np.std(null, ddof=1)),
                efecto_z=zscore_effect(obs, null),
                p=perm_p(obs, null, side))
