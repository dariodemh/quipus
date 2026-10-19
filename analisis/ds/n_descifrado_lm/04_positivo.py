# -*- coding: utf-8 -*-
"""Control POSITIVO y curva de potencia del metodo.

(a) Cifrado biyectivo de texto quechua real: cada silaba -> un signo, clave
    aleatoria. Se mide si el metodo recupera la clave (precision por token y NMI).
(b) Cifrado many-to-one: texto real -> V clases (cifrado de sustitucion no
    inyectivo). Mide si el metodo detecta estructura de lengua con V simbolos.
Se corre con el MISMO esfuerzo de busqueda que los quipus.
"""
import os, sys, re, time, json
import numpy as np
import pandas as pd
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D
from lm_utils import CORP, silabas

BASE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261018
N_NULL, N_REP, REST_OBS, REST_CTRL, ITERS = 40, 12, 4, 2, 2500

uni, bi = D.load_stream_lm("quechua")
L, TOP = D.build_L(uni, bi, 120)
txt = open(os.path.join(CORP, "quechua.txt"), encoding="utf-8").read()
STREAM = []
for line in txt.lower().split("\n"):
    for w in re.findall(r"[a-zA-ZñÑ]+", line):
        STREAM.extend(silabas(w))
STREAM = np.array(STREAM)

def zsc(obs, null):
    return (obs - null.mean()) / (null.std() + 1e-9)

def nmi(a, b):
    a = np.asarray(a); b = np.asarray(b)
    n = len(a)
    pa = Counter(a); pb = Counter(b); pab = Counter(zip(a, b))
    Ha = -sum(v / n * np.log2(v / n) for v in pa.values())
    Hb = -sum(v / n * np.log2(v / n) for v in pb.values())
    I = 0.0
    for (x, y), v in pab.items():
        I += v / n * np.log2((v / n) / ((pa[x] / n) * (pb[y] / n)))
    return I / max(1e-9, (Ha + Hb) / 2)

def eval_seq(seq, true_tokens=None):
    C, st, inv = D.counts_seq(seq)
    V = len(inv); n = len(seq)
    f, v = D.anneal(C[None], st[None], L, restarts=REST_OBS, iters=ITERS, seed=SEED)
    seqs = [list(np.random.default_rng(SEED + 1 + i).permutation(seq)) for i in range(N_NULL)]
    Cs, sts = [], []
    for s in seqs:
        cc, ss, _ = D.counts_seq(s); Cs.append(cc); sts.append(ss)
    _, vn = D.anneal(np.array(Cs), np.array(sts), L, restarts=REST_CTRL, iters=ITERS, seed=SEED + 7)
    out = dict(logL= v[0] / n, null=vn.mean() / n, z=zsc(v[0], vn),
               p=float((vn >= v[0]).mean()), V=V, n=n)
    if true_tokens is not None:
        # signo -> silaba recuperada; comparar con la clase verdadera
        asg = {inv[i]: TOP[f[0][i]] for i in range(V)}
        rec = [asg[s] for s in seq]
        out["nmi"] = nmi(true_tokens, rec)
        out["acc"] = float(np.mean([rec[i] == true_tokens[i] for i in range(n)]))
    return out

rows = []
rng = np.random.default_rng(SEED)
# ---------- (a) biyectivo, V = tipos distintos de la ventana
print("== cifrado biyectivo")
for n in [30, 60, 100, 164, 298]:
    for rep in range(N_REP):
        r = np.random.default_rng(SEED + rep)
        start = r.integers(0, len(STREAM) - n)
        plain = list(STREAM[start:start + n])
        tipos = sorted(set(plain))
        if len(tipos) > 120:
            continue
        perm = r.permutation(len(tipos))
        clave = {t: "s%d" % perm[i] for i, t in enumerate(tipos)}
        seq = [clave[x] for x in plain]
        o = eval_seq(seq, true_tokens=plain)
        o.update(tipo="biyectivo", rep=rep)
        rows.append(o)
        print(f"  n={n} V={o['V']} logL/s={o['logL']:.2f} z={o['z']:.2f} "
              f"p={o['p']:.3f} acc={o['acc']:.2f} nmi={o['nmi']:.2f}")

# ---------- (b) many-to-one, V clases balanceadas
print("== cifrado many-to-one")
for n in [30, 100, 164, 298]:
    for V in [4, 8, 16, 30, 60]:
        for rep in range(6):
            r = np.random.default_rng(SEED + 100 + rep)
            start = r.integers(0, len(STREAM) - n)
            plain = list(STREAM[start:start + n])
            tipos = sorted(set(plain))
            tab = {t: "s%d" % r.integers(0, V) for t in tipos}
            seq = [tab[x] for x in plain]
            if len(set(seq)) < 2:
                continue
            o = eval_seq(seq, true_tokens=plain)
            o.update(tipo="many2one", rep=rep, V_obj=V)
            rows.append(o)
            print(f"  n={n} V={o['V']} logL/s={o['logL']:.2f} z={o['z']:.2f} "
                  f"p={o['p']:.3f} nmi={o['nmi']:.2f}")

t = pd.DataFrame(rows)
t.to_csv(os.path.join(BASE, "control_positivo.csv"), index=False)
print(t.groupby(["tipo", "n"])[["logL", "z", "p", "nmi"]].agg(["mean", "max"]).round(2).to_string())
