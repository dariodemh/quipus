# -*- coding: utf-8 -*-
"""Motor del test color|posicion (version rapida).

Modelo A:  y ~ posicion(k,pos) + color          (compara grupos en la MISMA posicion)
Modelo B:  y ~ grupo + posicion(k,pos) + color   (anade efectos fijos de grupo)
Modelo C:  B + nrac + log(largo)                 (control de tamano de la cuerda)
Nulo: se permutan los colores DENTRO de cada (quipu,k,pos).
Estadistico: R2 parcial del color; F para el p por quipu.
"""
import numpy as np
import pandas as pd


def onehot(codes, k):
    M = np.zeros((len(codes), k))
    M[np.arange(len(codes)), codes] = 1.0
    return M


def dummies(vals):
    cats = pd.Categorical(vals)
    M = onehot(cats.codes, len(cats.categories))
    if M.shape[1] > 1:
        M = M[:, 1:]
    return M


class QuipuFit:
    def __init__(self, df, modelo="A", extra=None):
        df = df.sort_values(["k", "grupo", "pos"]).reset_index(drop=True)
        self.df = df
        self.y = df.y.values.astype(float)
        self.n = len(df)
        self.strata = [np.where((df.k.values == k) & (df.pos.values == p))[0]
                       for k, p in df[["k", "pos"]].drop_duplicates().values]
        self.strata = [s for s in self.strata if len(s) >= 2]
        P = dummies(df[["k", "pos"]].astype(str).agg("_".join, axis=1))
        if modelo == "A":
            W = np.column_stack([np.ones(self.n), P])
        else:
            G = dummies(df.grupo.astype(str))
            W = np.column_stack([np.ones(self.n), G, P])
        if extra is not None:
            W = np.column_stack([W, extra])
        self.W = W
        U, s, _ = np.linalg.svd(W, full_matrices=False)
        keep = s > 1e-8 * max(1.0, s[0] if len(s) else 1)
        self.Qw = U[:, keep]
        self.q = int(keep.sum())
        self.r0 = self.y - self.Qw @ (self.Qw.T @ self.y)
        self.rss0 = float(self.r0 @ self.r0)
        self.tss = float(((self.y - self.y.mean()) ** 2).sum())
        vc = df.col3.value_counts()
        self.cols = list(vc.index)
        codes = pd.Categorical(df.col3, categories=self.cols).codes
        self.codes = codes.copy()
        self.C = len(self.cols)
        self.M = onehot(self.codes, self.C)
        RZ = self.M - self.Qw @ (self.Qw.T @ self.M)
        G = RZ.T @ RZ
        self.rank = int(np.linalg.matrix_rank(G))

    def stat(self, M=None, full=False):
        if M is None:
            M = self.M
        RZ = M - self.Qw @ (self.Qw.T @ M)
        a = RZ.T @ self.r0
        G = RZ.T @ RZ
        b = np.linalg.pinv(G) @ a
        dss = float(a @ b)
        df1 = int(np.linalg.matrix_rank(G))
        rss1 = max(self.rss0 - dss, 1e-12)
        df2 = self.n - self.q - df1
        F = (dss / max(df1, 1)) / (rss1 / max(df2, 1))
        out = dict(r2=dss / self.rss0 if self.rss0 > 0 else 0.0,
                   F=F, df1=df1, df2=df2)
        if full:
            # efectos de color ajustados por posicion (y grupo en modelo B)
            X = np.column_stack([np.ones(self.n), M[:, 1:]])
            beta, *_ = np.linalg.lstsq(X, self.r0, rcond=None)
            out["efectos"] = np.concatenate([[0.0], beta[1:]])
        return out

    def perm_codes(self, rng):
        c = self.codes.copy()
        for s in self.strata:
            c[s] = rng.permutation(c[s])
        return c


def pvalor(qf, rng, nperm=999, stat="F"):
    obs = qf.stat()[stat]
    cnt = 0
    for _ in range(nperm):
        M = onehot(qf.perm_codes(rng), qf.C)
        if qf.stat(M)[stat] >= obs - 1e-12:
            cnt += 1
    return obs, (cnt + 1) / (nperm + 1)
