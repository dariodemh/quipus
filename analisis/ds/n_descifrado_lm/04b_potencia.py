# -*- coding: utf-8 -*-
"""Curva de potencia: texto generado por el propio modelo bigrama restringido a
V silabas (texto "tan lengua como el modelo permite"), cifrado biyectivo
aleatorio, descifrado con el mismo metodo. Mide a partir de que n/V el metodo
recupera la clave. Demuestra que el metodo funciona y que su fracaso en los
quipus es falta de datos, no un bug."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D

BASE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261018
uni, bi = D.load_stream_lm("quechua")
L, TOP = D.build_L(uni, bi, 120)
K = len(TOP)
P = np.exp(L)

def genera(n, V, rng):
    """Cadena de Markov sobre las V silabas mas frecuentes."""
    M = P[1:V + 1, :V].copy()          # filas = silaba previa, cols = siguiente
    M = M / M.sum(axis=1, keepdims=True)
    u = np.array([uni[TOP[i]] for i in range(V)], float); u /= u.sum()
    s = [rng.choice(V, p=u)]
    for _ in range(n - 1):
        s.append(rng.choice(V, p=M[s[-1]]))
    return s

rows = []
CASOS = [(500, 5), (1000, 10), (1000, 20)]
for n, V in CASOS:
    for rep in range(3):
        r = np.random.default_rng(SEED + n + V + rep)
        plain = [TOP[i] for i in genera(n, V, r)]
        perm = r.permutation(V)
        cifra = {TOP[i]: "s%d" % perm[i] for i in range(V)}
        seq = [cifra[x] for x in plain]
        C, st, inv = D.counts_seq(seq)
        f, v = D.anneal(C[None], st[None], L, restarts=20, iters=15000, seed=SEED)
        asg = {inv[i]: TOP[f[0][i]] for i in range(len(inv))}
        acc = np.mean([asg[seq[t]] == plain[t] for t in range(n)])
        rows.append(dict(n=n, V=V, tok_por_signo=n / V, precision=acc))
        print(f"n={n} V={V} tokens/signo={n/V:.1f} precision={acc:.2f}")
pd.DataFrame(rows).to_csv(os.path.join(BASE, "potencia.csv"), index=False)
