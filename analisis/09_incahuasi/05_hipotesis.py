"""Tareas 3-4: predicciones distintas de cada hipótesis y su comprobación.
H_fija (tara/cuota fija por registro)   -> c no depende de x dentro del quipu (CV(c)=0, c/x varía mucho).
H_prop (diezmo, merma %, impuesto proporcional) -> c/x constante: c crece con x.
H_saldo (entrada-salida-saldo encadenado) -> n_i reaparece como x_(i+1) (saldo arrastrado).
H_resultado (color 'resultado') -> cuerdas jaspeadas ':' sobrerrepresentadas al final del registro.
H_doble_entrada (pares) -> mismos x en ambos quipus, c/n intercambiados; descomposición completa solo al unir ambos.
"""
import numpy as np, pandas as pd, itertools
from scipy.stats import spearmanr
from collections import Counter
from comun import *
c, q = cargar(); qi = q.set_index("kfg")
K6 = ["UR255", "UR256", "UR267A", "UR267B", "UR269", "UR275"]
D = pd.read_csv(OUT/"trios_detalle.csv"); D = D[D.exacto == 1]
def part(r):
    x = [r.v1, r.v2, r.v3]; i = {"S1": 0, "S2": 1, "S3": 2}[r.patron]; p = sorted(x[:i]+x[i+1:]); return pd.Series(dict(x=x[i], c=p[0], n=p[1]))
D = D.join(D.apply(part, axis=1)); D = D[(D.c != D.n) & (D.x >= 30) & (D.c >= 5)]
# ---- tabla por quipu
T = []
for k in K6:
    d = D[D.kfg == k]; r = c[(c.kfg == k)]; g3 = pd.read_csv(OUT/"trios_por_quipu.csv").set_index("kfg").loc[k]
    T.append(dict(kfg=k, tríos_exactos=len(d), grupos_de_3=int(g3.n_trios3), c_valores=dict(Counter(d.c)), x_min=int(d.x.min()), x_max=int(d.x.max()), c_sobre_x_min=round(d.c.min()/d.x.max(), 4), c_sobre_x_max=round(d.c.max()/d.x.min(), 3),
                  cv_c=round(d.c.std()/d.c.mean(), 3), cv_x=round(d.x.std()/d.x.mean(), 3), corr_spearman_cx=(round(spearmanr(d.c, d.x)[0], 2) if d.c.nunique() > 1 else np.nan), x_lista=sorted(d.x.tolist())))
TT = pd.DataFrame(T); TT.to_csv(OUT/"tabla_por_quipu.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
print(TT.drop(columns="x_lista").to_string())
# ---- H_prop: simulación de lo que daría un tributo proporcional
rng = np.random.default_rng(11)
print("\n[H_prop] SD esperado de c si c=round(r*x) con r=media(c/x) y x observadas, frente a SD observada")
for k in K6:
    d = D[D.kfg == k]; r_ = (d.c/d.x).mean(); sd_pred = (np.round(r_*d.x)).std(); print(k, "r=%.3f" % r_, "sd_c_pred=%.2f" % sd_pred, "sd_c_obs=%.2f" % d.c.std())
# ---- UR269 por fila del bloque (5 filas entre separadores vacíos)
d = c[(c.kfg == "UR269") & (c.nivel == 0)]; row = 0; rec = []
for g, gd in d.groupby("grupo", sort=False):
    v = gd[gd.pres & (gd.valor > 0)].valor.tolist()
    if not v: row = 0; continue
    row += 1; cc = [x for x in v[1:3] if 20 <= x <= 50]
    imp = v[0]-v[1] if len(v) > 1 and 20 <= v[0]-v[1] <= 50 else None
    cv = cc[0] if cc else imp
    if cv is not None and v[0] >= 400: rec.append(dict(g=g, fila=min(row, 5), x=v[0], c=cv))
U = pd.DataFrame(rec); U.to_csv(OUT/"ur269_filas.csv", index=False)
print("\n[UR269] registros con x y c:", len(U)); print(U.groupby("fila").agg(n=("c", "size"), c_media=("c", "mean"), c_sd=("c", "std"), c_mod=("c", lambda s: s.mode()[0]), x_media=("x", "mean"), x_sd=("x", "std")).round(2))
B = 10000; ob_r2 = 1-U.groupby("fila").c.transform(lambda s: s-s.mean()).pow(2).sum()/((U.c-U.c.mean())**2).sum()
N = np.empty(B)
for b in range(B):
    cs = rng.permutation(U.c.values); t = pd.Series(cs); N[b] = 1-t.groupby(U.fila.values).transform(lambda s: s-s.mean()).pow(2).sum()/((t-t.mean())**2).sum()
print("R2 de c explicado por la fila: %.3f ; nulo medio %.3f ; p=%.4f" % (ob_r2, N.mean(), (1+(N >= ob_r2).sum())/(B+1)))
# correlación intra-fila c~x (permutando c dentro de fila)
def within(Ud, cs):
    r = []
    for f, gg in Ud.groupby("fila"):
        if len(gg) >= 5 and gg.c.nunique() > 1: r.append(spearmanr(cs[gg.index], gg.x)[0])
    return np.nanmean(r) if r else np.nan
ob = within(U, U.c.values); Nn = []
for b in range(2000):
    cs = U.c.values.copy()
    for f, gg in U.groupby("fila"): cs[gg.index] = rng.permutation(cs[gg.index])
    Nn.append(within(U, cs))
Nn = np.array(Nn); print("Spearman medio c~x dentro de fila: %.3f ; nulo %.3f ; p(>=)=%.3f" % (ob, np.nanmean(Nn), (1+(Nn >= ob).sum())/2001))
fm = U.groupby("fila").apply(lambda g: pd.Series(dict(k=g.c.mean()/g.x.mean(), sd_pred=(g.c.mean()/g.x.mean()*g.x).std(), sd_obs=g.c.std())))
print("tributo proporcional dentro de fila: SD(c) predicha vs observada\n", fm.round(2))
# ---- H_saldo: encadenamiento n_i == x_(i+1), por quipu (registros en orden)
print("\n[H_saldo] encadenamiento n_i = x_(i+1)")
for k in K6:
    d = D[D.kfg == k].sort_values("i0"); n_, x_ = d.n.values, d.x.values
    ob = int((n_[:-1] == x_[1:]).sum()); ob_any = sum(int(a in set(x_)) for a in n_)
    N = np.array([int((n_[:-1] == rng.permutation(x_)[1:]).sum()) for _ in range(1000)])
    print(k, "adyacente obs", ob, "nulo", N.mean(), "| n que aparecen como x en el quipu:", ob_any, "de", len(n_))
# ---- H_resultado: jaspeadas al final del registro (grupos >=3, 8 quipus Incahuasi)
print("\n[H_resultado] cuerda jaspeada (':' en color) en última posición del grupo vs nulo N1 (barajar colores entre cuerdas L0 presentes)")
res = []
for i, k in enumerate(["UR255", "UR256", "UR266", "UR267A", "UR267B", "UR269", "UR274B", "UR275"]):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values("orden"); d = d[d.pres & (d.valor > 0)]
    col = d.color.values; g = d.grupo.values; moth = np.array([":" in x for x in col])
    st = np.r_[0, np.where(np.diff(g) != 0)[0]+1, len(g)]; ends = [e-1 for s, e in zip(st[:-1], st[1:]) if e-s >= 3]; firsts = [s for s, e in zip(st[:-1], st[1:]) if e-s >= 3]
    ob = moth[ends].sum(); N = np.array([np.random.default_rng(i*1000+b).permutation(moth)[ends].sum() for b in range(2000)])
    res.append(dict(kfg=k, grupos=len(ends), jaspeadas_al_final=int(ob), esperadas=N.mean(), p=(1+(N >= ob).sum())/2001, jaspeadas_total=int(moth.sum()), n_cuerdas=len(moth)))
print(pd.DataFrame(res).round(3).to_string()); pd.DataFrame(res).to_csv(OUT/"resultado_jaspeadas.csv", index=False)
# ---- unión R/V por quipu
print("\nunión R/V/T/U por quipu (todas las cuerdas L0 presentes)")
for k in ["UR255", "UR267A", "UR256", "UR267B", "UR266", "UR275", "UR269"]:
    d = c[(c.kfg == k) & (c.nivel == 0) & c.pres]; print(k, dict(Counter(d.union)), "pc_color", qi.loc[k, "pc_color"])
