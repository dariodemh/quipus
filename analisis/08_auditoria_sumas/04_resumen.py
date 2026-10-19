"""Resume nulos_por_quipu.csv / nulos_corpus.npz: fracción esperable por azar de las relaciones KFG, prevalencia >=1
observada vs nula, y quipus significativos (BH-FDR por estadístico y nulo)."""
import numpy as np, pandas as pd
from kfg import NOMBRES, bh
d = pd.read_csv("nulos_por_quipu.csv"); z = np.load("nulos_corpus.npz")
MODOS = ["M0_quipu", "M1_nivel", "M2_magnitud"]
N = NOMBRES + ["any4"]
n = len(d)
L = [f"quipus: {n}"]
L.append("\n## Corpus: total observado vs esperado (media nula, IC 95 %) y fracción atribuible al azar")
for j, s in enumerate(N[:-1]):
    o = d[f"obs_{s}"].sum()
    parts = []
    for m in MODOS:
        x = z[f"{m}_sum"][:, j]
        parts.append(f"{m}: E={x.mean():.1f} [{np.percentile(x,2.5):.0f}-{np.percentile(x,97.5):.0f}] azar={x.mean()/max(o,1e-9):.2f} p={(1+(x>=o).sum())/(len(x)+1):.4f}")
    L.append(f"{s}: obs={o:.1f} | " + " | ".join(parts))
L.append("\n## Quipus con >=1 relación: observado vs nulo (media e IC 95 % del nº de quipus)")
for j, s in enumerate(N):
    if s in ("PPS_sumlog_local",): continue
    o = (d[f"obs_{s}"] > 0).sum()
    parts = []
    for m in MODOS:
        x = z[f"{m}_ind"][:, j]
        parts.append(f"{m}: {x.mean():.1f} [{np.percentile(x,2.5):.0f}-{np.percentile(x,97.5):.0f}] p={(1+(x>=o).sum())/(len(x)+1):.4f}")
    L.append(f"{s}: obs={o} ({o/n:.1%}) | " + " | ".join(parts))
L.append("\n## Por quipu: testables (sd nula>0), p<0,05 (esperado 5 %), q<0,05 (BH dentro de cada estadístico x nulo)")
sig = {}
for s in ["PPS", "COL", "IDX", "SUB", "PPS_ady", "PPS_100", "PPS_ady100", "PPS_cadena", "PPS_cara01", "PPS_sumlog_local"]:
    parts = []
    for m in MODOS:
        t = d[f"sd_{m}_{s}"] > 0
        q = pd.Series(1.0, index=d.index); q[t] = bh(d.loc[t, f"p_{m}_{s}"])
        d[f"q_{m}_{s}"] = q
        p = d.loc[t, f"p_{m}_{s}"]
        pi0 = min(1, (p > .5).mean() / .5) if t.sum() else 1
        parts.append(f"{m}: test={t.sum()} p<.05={(p<.05).sum()} (esp {0.05*t.sum():.0f}) q<.05={(q<.05).sum()} 1-pi0={1-pi0:.2f}")
        sig[(s, m)] = set(d.kfg[q < .05])
    L.append(f"{s}: " + " | ".join(parts))
u = sig[("PPS_sumlog_local", "M2_magnitud")] | sig[("PPS_ady", "M2_magnitud")] | sig[("PPS_ady100", "M2_magnitud")]
L.append(f"\nunión M2 (ady, ady100, sumlog_local) q<.05: {len(u)} quipus: {sorted(u)}")
u1 = sig[("PPS_sumlog_local", "M1_nivel")] | sig[("PPS_ady", "M1_nivel")] | sig[("PPS_ady100", "M1_nivel")]
L.append(f"unión M1 (ady, ady100, sumlog_local) q<.05: {len(u1)} quipus; en ambos M1 y M2: {len(u & u1)}")
uk = set()
for s in ["PPS", "COL", "IDX", "SUB", "PPS_100", "PPS_cadena"]:
    uk |= sig[(s, "M2_magnitud")]
L.append(f"definición KFG sin localidad (PPS, COL, IDX, SUB, PPS_100, cadena) q<.05 en M2: {len(uk)} quipus: {sorted(uk)}")
uk1 = set()
for s in ["PPS", "COL", "IDX", "SUB", "PPS_100", "PPS_cadena"]:
    uk1 |= sig[(s, "M1_nivel")]
L.append(f"ídem en M1: {len(uk1)}: {sorted(uk1)}")
d.to_csv("nulos_por_quipu_q.csv", index=False)
print("\n".join(L))
open("salida_04_resumen.txt", "w", encoding="utf8").write("\n".join(L) + "\n")
