"""Contrastes por pares de roles sobre el color: (i) x vs {c,n} (permutando cuál de las tres es x dentro del trío); (ii) c vs n (permutando solo c/n).
Estadístico: información mutua rol-color. B=5000, semilla fija. Holm sobre las 12 pruebas."""
import numpy as np, pandas as pd
A = pd.read_csv("roles_cuerdas.csv"); B = 5000; rng = np.random.default_rng(99); res = []
def mi(lab, att):
    na = att.max()+1; nl = lab.max()+1; ct = np.bincount(lab*na+att, minlength=nl*na).reshape(nl, na).astype(float); p = ct/ct.sum()
    pr = p.sum(1, keepdims=True); pa = p.sum(0, keepdims=True); nz = p > 0; return float((p[nz]*np.log(p[nz]/(pr@pa)[nz])).sum())
for k, g in A.groupby("kfg"):
    T = g.trio.unique(); M = np.array([g[g.trio == t].set_index("rol").loc[["x", "c", "n"], "color"].tolist() for t in T])
    cod = {u: i for i, u in enumerate(sorted(set(M.ravel())))}; Mi = np.vectorize(cod.get)(M)
    # (i) x vs resto
    lab = np.tile(np.array([0, 1, 1]), len(T)); ob = mi(lab, Mi.ravel()); N = np.empty(B)
    for b in range(B): N[b] = mi(lab, rng.permuted(Mi, axis=1).ravel())
    res.append(dict(kfg=k, contraste="x vs {c,n}", n=len(T), MI=ob, p=(1+(N >= ob).sum())/(B+1)))
    # (ii) c vs n
    Mcn = Mi[:, 1:]; lab = np.tile(np.array([0, 1]), len(T)); ob = mi(lab, Mcn.ravel()); N = np.empty(B)
    for b in range(B): N[b] = mi(lab, rng.permuted(Mcn, axis=1).ravel())
    res.append(dict(kfg=k, contraste="c vs n", n=len(T), MI=ob, p=(1+(N >= ob).sum())/(B+1)))
R = pd.DataFrame(res); p = R.p.values; o = np.argsort(p); m = len(p); h = np.maximum.accumulate((m-np.arange(m))*p[o]); ph = np.empty(m); ph[o] = np.minimum(h, 1); R["p_holm"] = ph
R.to_csv("roles_color_contrastes.csv", index=False); print(R.round(4).to_string())
