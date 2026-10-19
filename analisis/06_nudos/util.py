import numpy as np
from pathlib import Path
AQUI = Path(__file__).resolve().parent
SEED = 20261017

def holm(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    adj = np.empty(n); run = 0
    for r, i in enumerate(o):
        run = max(run, (n - r) * p[i]); adj[i] = min(1, run)
    return adj

def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)[::-1]
    adj = np.empty(n); run = 1
    for r, i in enumerate(o):
        k = n - r; run = min(run, p[i] * n / k); adj[i] = run
    return adj

def pemp(obs, null, lado="mayor"):
    null = np.asarray(null)
    if lado == "mayor": return (1 + (null >= obs).sum()) / (1 + len(null))
    if lado == "menor": return (1 + (null <= obs).sum()) / (1 + len(null))
    return (1 + (np.abs(null - np.mean(null)) >= abs(obs - np.mean(null))).sum()) / (1 + len(null))

def wilson(k, n, z=1.96):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); w = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - w) / d, (c + w) / d)
