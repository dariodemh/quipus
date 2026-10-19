"""Figura resumen: bandas decimales y distribución del ratio de huecos."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from explorar import load
from alineacion import quipu_points

OUT = os.path.join(os.path.dirname(__file__), "fig_alineacion.png")


def panel(ax, d, k, titulo):
    r = quipu_points(d, k, unique=True)
    P, C, E, L = r
    # jitter vertical mínimo para visibilidad
    rng = np.random.default_rng(0)
    y = E + rng.uniform(-0.08, 0.08, len(E))
    ax.scatter(P, y, s=8, alpha=.45, c="#31688e", edgecolors="none")
    for e in sorted(set(E)):
        p = P[E == e]
        if len(p) >= 3:
            med = np.median(p)
            ax.plot([med, med], [e - .28, e + .28], color="#c0392b", lw=2)
    ax.set_yticks(sorted(set(E)))
    ax.set_yticklabels([f"10^{e}" for e in sorted(set(E))])
    ax.set_xlabel("posición desde el cordón principal (cm)")
    ax.set_ylabel("orden decimal")
    ax.set_title(titulo, fontsize=10)
    ax.grid(alpha=.2)
    ax.set_xlim(0, min(45, P.max() + 3))


def main():
    d = load()
    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5))
    panel(axes[0, 0], d, "UR1120", "A. UR1120: escalera decimal compartida")
    panel(axes[0, 1], d, "AS008", "B. AS008: bandas globales anchas")
    panel(axes[1, 0], d, "UR1095", "C. UR1095: bandas desordenadas")
    # D: histograma del ratio
    ax = axes[1, 1]
    B = pd.read_csv(os.path.join(os.path.dirname(__file__), "bandas_quipu2.csv"))
    # reconstruir ratios de huecos a nivel 0
    reg = d[(d.nivel == 0) & (d.nap >= 2)].copy()
    rows = []
    for _, r in reg.iterrows():
        a = sorted(r.ap, key=lambda t: t[2])
        es = [e for e, v, p in a]
        if len(es) != len(set(es)):
            continue
        if any(es[i] < es[i + 1] for i in range(len(es) - 1)):
            continue
        for i in range(len(a) - 1):
            rows.append((r.kfg, es[i] - es[i + 1], a[i + 1][2] - a[i][2]))
    G = pd.DataFrame(rows, columns=["kfg", "de", "dp"])
    w = G[G.de == 1].groupby("kfg").dp.median()
    G["w"] = G.kfg.map(w)
    G["ratio"] = G.dp / (G.de * G.w)
    z = G[(G.de >= 2) & G.ratio.notna() & (G.ratio < 3)]
    ax.hist(z.ratio, bins=np.arange(0, 3.01, .1), color="#31688e", alpha=.8)
    ax.axvline(1, color="#c0392b", lw=2, label="una banda por lugar")
    ax.axvline(z.ratio.median(), color="k", ls="--", lw=1.5,
               label=f"mediana = {z.ratio.median():.2f}")
    ax.set_xlabel("Δposición / (Δexponente × ancho de banda)")
    ax.set_ylabel("n.º de huecos")
    ax.set_title("D. Tamaño del hueco de un cero", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=.2)
    fig.tight_layout()
    fig.savefig(OUT, dpi=180)
    print("guardado", OUT, "n ratio", len(z))


if __name__ == "__main__":
    main()
