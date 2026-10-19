"""Tarea 3: proporciones fijas. F1: (colgante o subsidiaria, suma de sus subsidiarias directas) con razón hijos/padre = p/q exacta.
F2: pares ordenados de grupos (totales de colgantes >=10) con razón total_i/total_j = p/q exacta.
Nulo N2 (permutar valores presentes dentro de cada nivel del quipu, B=1000); BH-FDR sobre quipu x razón; nulo agregado de corpus."""
import numpy as np, pandas as pd
from multiprocessing import Pool
from pathlib import Path
from nucleo import *
B = 1000
QS = None
def init():
    global QS
    QS, _ = cargar()
def tarea(a):
    i, k = a
    Q = QS[k]; nf = len(FP)
    obs = np.zeros(2 * nf, np.int64); stats_ratio(Q["v"], Q["par"], Q["L0"], Q["gs"], FP, FQ, obs)
    p, s = estratos(Q, 1)
    R = run_null_ratio(Q["v"], Q["par"], Q["L0"], Q["gs"], p, s, B, 4242 + i, FP, FQ)
    return k, obs, R.mean(0), (1 + (R >= obs).sum(0)) / (B + 1), R.sum(0) * 0 + R.std(0), R.astype(np.int32)
if __name__ == "__main__":
    Qs, q = cargar(); ks = list(Qs); nf = len(FP)
    with Pool(12, initializer=init) as P: res = P.map(tarea, list(enumerate(ks)), chunksize=2)
    names = [f"{a}/{b}" for a, b in FRAC]
    rows = []
    for k, o, e, p, sd, _ in res:
        for f in range(nf):
            rows.append(dict(kfg=k, fam="F1_cuerda_subs", razon=names[f], obs=o[f], E=e[f], sd=sd[f], p=p[f]))
            rows.append(dict(kfg=k, fam="F2_grupos", razon=names[f], obs=o[nf + f], E=e[nf + f], sd=sd[nf + f], p=p[nf + f]))
    d = pd.DataFrame(rows)
    d["q"] = 1.0
    for fam, e in d.groupby("fam"):
        t = e.index[e.sd > 0]; d.loc[t, "q"] = bh(d.loc[t, "p"].values)
    d.to_csv(Path(__file__).parent / "proporciones_por_quipu.csv", index=False)
    tot = sum(r[5].astype(np.int64) for r in res)
    out = []
    for f in range(nf):
        for fam, off in (("F1_cuerda_subs", 0), ("F2_grupos", nf)):
            o = sum(r[1][off + f] for r in res); nl = tot[:, off + f]
            e = d[(d.fam == fam) & (d.razon == names[f])]
            out.append(dict(familia=fam, razon=names[f], obs=int(o), E=round(nl.mean(), 1), sd=round(nl.std(), 1), p_corpus=(1 + (nl >= o).sum()) / (B + 1),
                            quipus_obs_ge1=int((e.obs > 0).sum()), quipus_p05=int((e.p < .05).sum()), esperados_p05=round(0.05 * (e.sd > 0).sum(), 1), quipus_q05=int((e.q < .05).sum())))
    T = pd.DataFrame(out); pd.set_option("display.width", 250); print(T.to_string())
    T.to_csv(Path(__file__).parent / "proporciones_resumen.csv", index=False)
    print(d[d.q < .05].sort_values("q").head(40).merge(q[["kfg", "procedencia"]], on="kfg").to_string())
