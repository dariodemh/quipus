"""Tarea 2: ¿qué distingue a x (bruto), c (constante) y n (= x-c) en los tríos exactos?
Roles por valor: x = cuerda suma, c = parte menor, n = parte mayor. Atributos: color, unión R/V, torsión, dirección de nudos,
tipo de nudos, largo. Nulo: permutar los roles DENTRO de cada trío (conserva las tres cuerdas, su color y largo; solo destruye
la asignación rol-cuerda). Estadístico categórico = información mutua rol-atributo; continuo = diferencia de medias c-n y x-n.
Se calcula por quipu (unidad) con B=5000 y Holm sobre todas las pruebas."""
import numpy as np, pandas as pd
from itertools import permutations
from collections import Counter
from comun import *
B = 5000
c, q = cargar()
K = ["UR255", "UR256", "UR267A", "UR267B", "UR269", "UR275"]
D = pd.read_csv(OUT/"trios_detalle.csv"); D = D[D.exacto == 1]
def dirs(nudos, tipo):
    if not nudos: return ""
    s = set()
    for t in nudos.split(";"):
        t = t.strip(); m = t.split("(")[0]; ty = m.lstrip("0123456789")
        if tipo(ty): s.add(t.split("(")[1].split(",")[0].split(")")[0].replace("U", "u")[-1] if "(" in t else "")
    return "".join(sorted(s))
def tipos(nudos):
    return "|".join(t.split("(")[0].lstrip("0123456789") for t in nudos.split(";")) if nudos else ""
rows = []
for k in K:
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values("orden"); d = d[d.pres & (d.valor > 0)].reset_index(drop=True)
    for _, h in D[D.kfg == k].iterrows():
        idx = [h.i0, h.i0+1, h.i0+2]; v = [h.v1, h.v2, h.v3]; i = {"S1": 0, "S2": 1, "S3": 2}[h.patron]
        o = [j for j in range(3) if j != i]; o.sort(key=lambda j: v[j])
        if v[o[0]] == v[o[1]] or v[i] < 30: continue
        for rol, j in (("x", i), ("c", o[0]), ("n", o[1])):
            r = d.loc[idx[j]]
            rows.append(dict(kfg=k, trio=f"{k}:{h.i0}", rol=rol, pos=j+1, valor=r.valor, color=r.color, union=r.union, torsion=r.torsion, largo=float(r.largo) if r.largo != "" else np.nan,
                             dir_S=dirs(r.nudos, lambda t: t in ("S", "SP")), dir_L=dirs(r.nudos, lambda t: t in ("L", "E")), tipos=tipos(r.nudos), cuerda=r.cuerda))
A = pd.DataFrame(rows); A.to_csv(OUT/"roles_cuerdas.csv", index=False)
print(A.groupby("kfg").trio.nunique().to_dict())
def mi(lab, att):
    # lab: enteros 0..2 ; att: enteros; informacion mutua con bincount
    na = att.max()+1; ct = np.bincount(lab*na+att, minlength=3*na).reshape(3, na).astype(float); p = ct/ct.sum()
    pr = p.sum(1, keepdims=True); pa = p.sum(0, keepdims=True); nz = p > 0
    return float((p[nz]*np.log(p[nz]/(pr@pa)[nz])).sum())
res = []
for k in K:
    a = A[A.kfg == k]; T = a.trio.unique(); rng = np.random.default_rng(77 + len(k)+ord(k[-1]))
    rolmat = np.array([a[a.trio == t].set_index("rol").loc[["x", "c", "n"]].index.tolist() for t in T])
    for att in ["color", "union", "torsion", "dir_S", "dir_L", "tipos"]:
        M = np.array([a[a.trio == t].set_index("rol").loc[["x", "c", "n"], att].astype(str).tolist() for t in T])  # filas=trio, cols=x,c,n
        if len(set(M.ravel())) == 1: res.append(dict(kfg=k, atributo=att, n_trios=len(T), estad=0.0, p=1.0, nota="constante en todo el quipu (valor %s)" % M[0, 0])); continue
        lab = np.tile(np.arange(3), len(T)); codes = {u: i for i, u in enumerate(sorted(set(M.ravel())))}; Mi = np.vectorize(codes.get)(M)
        ob = mi(lab, Mi.ravel()); N = np.empty(B)
        for b in range(B):
            Mp = rng.permuted(Mi, axis=1); N[b] = mi(lab, Mp.ravel())
        # constancia de c: cuota modal de c
        sh = lambda col: Counter(M[:, col]).most_common(1)[0]
        res.append(dict(kfg=k, atributo=att, n_trios=len(T), estad=ob, p=(1+(N >= ob).sum())/(B+1), E_nulo=N.mean(),
                        nota="modal x=%s(%d) c=%s(%d) n=%s(%d)" % (sh(0)[0], sh(0)[1], sh(1)[0], sh(1)[1], sh(2)[0], sh(2)[1])))
    M = np.array([a[a.trio == t].set_index("rol").loc[["x", "c", "n"], "largo"].astype(float).tolist() for t in T])
    for nm, (u, w) in {"largo c-n": (1, 2), "largo x-n": (0, 2), "largo x-c": (0, 1)}.items():
        ok = ~np.isnan(M).any(1); Mm = M[ok]; ob = (Mm[:, u]-Mm[:, w]).mean(); N = np.empty(B)
        for b in range(B):
            Mp = rng.permuted(Mm, axis=1); N[b] = (Mp[:, u]-Mp[:, w]).mean()
        res.append(dict(kfg=k, atributo=nm, n_trios=int(ok.sum()), estad=ob, p=(1+(np.abs(N) >= abs(ob)).sum())/(B+1), E_nulo=0.0, nota="medias largo x=%.1f c=%.1f n=%.1f cm" % tuple(Mm.mean(0))))
R = pd.DataFrame(res)
# Holm sobre pruebas no constantes
t = ~R.nota.str.startswith("constante"); p = R.loc[t, "p"].values; o = np.argsort(p); m = len(p); h = np.maximum.accumulate((m-np.arange(m))*p[o]); ph = np.empty(m); ph[o] = np.minimum(h, 1)
R["p_holm"] = np.nan; R.loc[t, "p_holm"] = ph
R.to_csv(OUT/"roles_pruebas.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(R.round(4).to_string())
