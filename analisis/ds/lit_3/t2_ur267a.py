"""T2. Clindaniel (2019, cap. 4): la aritmetica de colores de UR267A.

Afirmacion: en UR267A, blanco (W) = suma/credito, marron claro (AB) =
resta/debito, moteado AB:MB = resultado; el ejemplo es 106 - 15 = 91.
UR255 invertiria los roles (AB claro = suma).

Prueba: (a) reproducir el triple citado; (b) ver si la relacion
primer - segundo = tercero se cumple en todos los grupos del mismo quipu;
(c) test de permutacion del tercer valor (nulo que rompe el emparejamiento
dentro del quipu); (d) comprobar si el color del tercer cordel predice el
acierto (AB:MB = "resultado" vs AB solido).
"""
import numpy as np
import pandas as pd
from comun import cargar, RNG

c, _, _ = cargar()


def analizar(kfg):
    d = c[(c.kfg == kfg) & (c.nivel == 0)].sort_values("orden")
    filas = []
    for gr, g in d.groupby("grupo"):
        v = list(g.valor.astype(float))
        col = list(g.color.astype(str))
        filas.append((gr, v, col))
    return filas


for kfg in ["UR267A", "UR255"]:
    print("=" * 70)
    print(kfg)
    grupos = analizar(kfg)
    triples = [x for x in grupos if len(x[1]) == 3]
    a = np.array([x[1][0] for x in triples])
    b = np.array([x[1][1] for x in triples])
    d3 = np.array([x[1][2] for x in triples])
    c3 = [x[2][2] for x in triples]
    ok = np.isclose(a - b, d3)
    print("triples completos:", len(triples), "| a-b=c exacto:", ok.sum())

    # Descartar terceros ausentes (0 sin nudos) para el test principal
    tiene = d3 > 0
    ok_t = ok[tiene]
    print("triples con tercer valor >0:", tiene.sum(),
          "| exactos:", ok_t.sum(), f"({ok_t.mean():.0%})")

    # Permutacion: romper el emparejamiento del tercer valor
    B = 20000
    obs = int(ok_t.sum())
    n = int(tiene.sum())
    aa, bb, dd = a[tiene], b[tiene], d3[tiene]
    cnt = 0
    for _ in range(B):
        perm = RNG.permutation(dd)
        if int(np.isclose(aa - bb, perm).sum()) >= obs:
            cnt += 1
    p = (cnt + 1) / (B + 1)
    print(f"permutacion del tercer valor: p = {p:.5f} (B={B})")

    # Color del tercer cordel
    cc = np.array(c3)[tiene]
    for color in sorted(set(cc)):
        m = cc == color
        print(f"  tercer cordel {color:8s}: n={m.sum():2d} exactos={ok_t[m].sum():2d}")

    print("Detalle (a, b, c, color_c, a-b-c):")
    for (gr, v, col), o in zip(triples, ok):
        print(f"  g{gr:02d} {int(v[0]):4d} - {int(v[1]):3d} = {int(v[0]-v[1]):4d}"
              f" | c={int(v[2]):4d} {col[2]:7s} {'OK' if o else 'NO'}")
