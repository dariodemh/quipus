"""Tarea 1f. Papel de las cuerdas jaspeadas (color con ':') y del blanco en los registros con cuota.

Roles por registro (aristas internas de grafo_cuerdas.csv): x = cabecera, c = cuerda cuota, n = neto (x - c, o
x = c + deducciones + n). Resto = las demás cuerdas anudadas del registro (deducciones/partidas).
Estadístico por rol: fracción de cuerdas jaspeadas y fracción blancas (W puro).
Nulo: permutar los colores entre las cuerdas anudadas de cada registro (conserva la composición de colores de cada
registro y rompe solo la asignación color-rol). 5000 réplicas, agregado sobre todos los registros y por quipu.
"""
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13010
rng = np.random.default_rng(SEED)
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"])
P = c[c.pres]
E = pd.read_csv(C.AQUI / "grafo_cuerdas.csv")
I = E[(E.origen == E.destino) & E.tipo.isin(["cuota", "neto"])]
recs = []
for (k, cab), x in I.groupby(["origen", "cuerda_o"]):
    d = P[P.kfg == k]
    g = d[d.cuerda == cab].grupo.iloc[0]
    r = d[d.grupo == g]
    rol = {cu: "resto" for cu in r.cuerda}
    rol[cab] = "x"
    for t in x.itertuples():
        rol[t.cuerda_d] = "c" if t.tipo == "cuota" else "n"
    col = r.color.str.split(r"[(\s]", regex=True).str[0].tolist()
    recs.append((k, [rol[cu] for cu in r.cuerda], col))


def frac(recs_, colores=None):
    out = {}
    for rol in ["x", "c", "n", "resto"]:
        jas = bla = tot = 0
        for i, (k, roles, col) in enumerate(recs_):
            cc = colores[i] if colores is not None else col
            for ro, co in zip(roles, cc):
                if ro == rol:
                    tot += 1
                    jas += ":" in co
                    bla += co == "W"
        out[rol] = (jas / max(tot, 1), bla / max(tot, 1), tot)
    return out


def prueba(rs, etiqueta):
    obs = frac(rs)
    nul = [frac(rs, [rng.permutation(col) for _, _, col in rs]) for _ in range(5000)]
    print(f"\n{etiqueta}: {len(rs)} registros")
    for rol in ["x", "c", "n", "resto"]:
        nj = np.array([z[rol][0] for z in nul])
        nb = np.array([z[rol][1] for z in nul])
        j, b, t = obs[rol]
        print(f"  {rol:5s} n={t:3d}  jaspeadas {j:.2f} (nulo {nj.mean():.2f}; p_mayor={(np.sum(nj >= j)+1)/5001:.4f})"
              f"  blancas {b:.2f} (nulo {nb.mean():.2f}; p_mayor={(np.sum(nb >= b)+1)/5001:.4f})")


prueba(recs, "Todos los quipus con cuota")
for k in sorted({r[0] for r in recs}):
    rs = [r for r in recs if r[0] == k]
    if len(rs) >= 5:
        prueba(rs, k)
