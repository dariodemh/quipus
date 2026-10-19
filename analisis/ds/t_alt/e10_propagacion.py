"""Validacion del intervalo alternativo y propagacion del ruido de transcripcion a sumas.

(1) ?El intervalo [vmin,vmax] captura el valor de la OTRA transcripcion (OKR)
    en las cuerdas donde discrepan?
(2) Propagacion a sumas de k cuerdas de un grupo real:
    M1 empirico: cada cuerda se corrompe con prob p = tasa KFG vs OKR y el error es
       multiplicativo, con razon muestreada (simetrizada) de los desacuerdos observados.
    M2 intervalo: cada cuerda pasa a su valor minimo o maximo alternativo.
"""
from pathlib import Path
import pandas as pd, numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
V = pd.read_csv(AQUI/"intervalos_cuerdas.csv").set_index(["kfg", "cuerda"])
P = pd.read_csv(AQUI/"kfg_vs_okr_cuerdas.csv")
P["v_okr"] = P.v.fillna(0); P["dif"] = P.v_okr - P.v_kfg
P = P.set_index(["kfg", "cuerda"])
J = P.join(V[["v0", "vmin", "vmax"]], how="inner")
des = J[J.dif != 0]
print("== (1) validacion del intervalo ==")
print("cuerdas con desacuerdo KFG-OKR y con intervalo:", len(des))
dentro = (des.v_okr >= des.vmin - 1e-9) & (des.v_okr <= des.vmax + 1e-9)
print("v_okr dentro del intervalo:", dentro.sum(), f"({100*dentro.mean():.1f}%)")
print("de ellas, intervalo NO trivial:", (dentro & (des.vmin != des.vmax)).sum())
print(des[["v_kfg", "v_okr", "vmin", "vmax"]].head(10).to_string())

print("\n== (2) propagacion a sumas ==")
d = pd.read_csv(RAIZ/"analisis/datos/cuerdas.csv", dtype=str, keep_default_na=False)
d["v"] = pd.to_numeric(d.valor, errors="coerce").fillna(0)
g = pd.read_csv(RAIZ/"analisis/datos/grupos.csv", dtype=str, keep_default_na=False)
g["desde"] = pd.to_numeric(g.desde, errors="coerce"); g["hasta"] = pd.to_numeric(g.hasta, errors="coerce")
d["pnum"] = d.cuerda.str.extract(r"^p(\d+)$")[0]
raiz = d[d.pnum.notna()].copy(); raiz["pnum"] = raiz.pnum.astype(int)
Vq = {k: {int(i): float(x) for i, x in zip(gr.pnum, gr.v)} for k, gr in raiz.groupby("kfg")}
grupos = []
for _, r in g.iterrows():
    vals = Vq.get(r.kfg, {})
    idx = [i for i in range(int(r.desde), int(r.hasta)+1) if i in vals]
    if len(idx) >= 2:
        grupos.append(np.array([vals[i] for i in idx]))
print("grupos con >=2 cuerdas:", len(grupos))
print("suma de grupo: mediana", np.median([x.sum() for x in grupos]),
      " p25", np.percentile([x.sum() for x in grupos], 25),
      " p75", np.percentile([x.sum() for x in grupos], 75))

rng = np.random.default_rng(20261018)
W = pd.read_csv(AQUI/"desacuerdos_alineados.csv")
print("pares alineados 1-a-1 con valor distinto:", len(W))
rat = (W.v_okr / W.v_kfg.replace(0, np.nan)).dropna()
rat = rat[(rat > 0) & np.isfinite(rat)]
logr = np.concatenate([np.log(rat.values), -np.log(rat.values)])
p_err = len(W)/48465
print("p (desacuerdo por cuerda) =", round(p_err, 5), "  n razones =", len(rat))

print("\nM1 (empirico, p=%.4f)" % p_err)
print("k  P(cambia)   mediana_reldif  p90     p99")
res_all = {}
for k in [2, 3, 5, 8, 10]:
    out = []
    for _ in range(20000):
        gr = grupos[rng.integers(len(grupos))]
        if len(gr) < k:
            continue
        pick = rng.choice(len(gr), k, replace=False)
        vals = gr[pick].astype(float)
        s0 = vals.sum()
        if s0 <= 0:
            continue
        m = rng.random(k) < p_err
        vals2 = vals * np.where(m, np.exp(rng.choice(logr, k)), 1.0)
        out.append((abs(vals2.sum()-s0)/s0, m.any(), m.sum()))
    out = np.array(out)
    q = np.percentile(out[:, 0], [50, 90, 99])
    res_all[k] = out
    print(f"{k:<3} {100*out[:,1].mean():7.2f}%   {100*q[0]:10.2f}    {100*q[1]:7.2f} {100*q[2]:7.2f}")

print("\nM2 (cambio de convencion tipo-por-posicion: factor 10 en nudos L/E no finales)")
print("k  P(cambia)   mediana_reldif  p90     p99")
for k in [2, 3, 5, 8, 10]:
    out = []
    for _ in range(20000):
        gr = grupos[rng.integers(len(grupos))]
        if len(gr) < k:
            continue
        pick = rng.choice(len(gr), k, replace=False)
        vals = gr[pick].astype(float)
        s0 = vals.sum()
        if s0 <= 0:
            continue
        m = rng.random(k) < 0.08      # 7,94 % de cuerdas con lectura alternativa
        vals2 = vals * np.where(m, 10.0, 1.0)
        out.append((abs(vals2.sum()-s0)/s0, m.any()))
    out = np.array(out)
    q = np.percentile(out[:, 0], [50, 90, 99])
    print(f"{k:<3} {100*out[:,1].mean():7.2f}%   {100*q[0]:10.2f}    {100*q[1]:7.2f} {100*q[2]:7.2f}")
