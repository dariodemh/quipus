"""05: controles de especificidad de la jerarquia de Puruchuco.

Se comparan las sumas de columnas (P1: UR068 -> nivel III; P2: UR063 -> nivel II)
con TODOS los quipus de Puruchuco, para ver si el ajuste es especifico del padre
o aparece en cualquier quipu del archivo (explicacion aburrida: densidad).
"""
import numpy as np
import pandas as pd
import comun_np as L

c, q = L.cargar_kfg()
ks = sorted(q[q.region == "Puruchuco"].kfg)
OUT = []


def pr(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUT.append(s)


def V(k):
    return [int(v) for v in c[c.kfg == k].sort_values("orden").valor]


V68, V67, V63 = V("UR068"), V("UR067"), V("UR063")
SEC68 = [V68[13:33], V68[33:53], V68[53:73]]
sumas68 = [sum(x) for x in zip(*SEC68)]
d67 = V67[12:32]
d67 = d67[:17] + d67[18:]          # sin la cuerda rota (cuerda 30)


def matches(a, b, tol=False):
    return sum(L.coincide(x, y, tol) for x, y in zip(a, b))


pr("P1: sumas de UR068 (20 columnas) frente a los 20 primeros valores de datos")
pr("    de cada quipu de Puruchuco (cuerdas 13-32; UR067: 13-33 sin la rota):")
filas = []
for k in ks:
    v = V(k)
    if k == "UR067":
        # misma definicion que P1: cuerdas 13-33 sin la cuerda rota (30)
        v = v[12:33]
        v = v[:17] + v[18:]
    else:
        v = v[12:32]
    n = min(len(v), 20)
    filas.append(dict(kfg=k, n=n, exactas=matches(sumas68[:n], v[:n]),
                      toler=matches(sumas68[:n], v[:n], tol=True)))
t1 = pd.DataFrame(filas).sort_values("exactas", ascending=False)
pr(t1.to_string(index=False))

# P2: sumas de UR063 -> seccion central de UR068; comparar con todos
cortes = [0, 20, 41, 56, 76, 96, 111]
SEC63 = [V63[a:b] for a, b in zip(cortes[:-1], cortes[1:])]
cols = list(c[c.kfg == "UR063"].sort_values("orden").col3)

# se reutiliza la construccion de 01 (misma definicion)
def quads_de(cols, vals):
    idx = [i for i, col in enumerate(cols) if col.startswith("W") and ":" not in col]
    out = []
    for j, i in enumerate(idx):
        fin = idx[j + 1] if j + 1 < len(idx) else len(cols)
        out.append((i, fin))
    if out and out[-1][1] - out[-1][0] < 4 and sum(vals[out[-1][0]:out[-1][1]]) == 0:
        out.pop()
    return out


def vec_por_color(qq):
    v = [0, 0, 0, 0]
    for val, col in qq:
        if ":" in col:
            k = 3
        elif col.startswith("W"):
            k = 0
        elif "AB" in col or "MB" in col or "KB" in col:
            k = 1
        elif "GG" in col:
            k = 2
        else:
            k = 3
        v[k] += val
    return v


Q = []
for a, b in zip(cortes[:-1], cortes[1:]):
    cc = cols[a:b]
    Q.append([vec_por_color(list(zip(V63[a + i:a + j], cc[i:j]))) for i, j in quads_de(cc, V63[a:b])])


def sumas_alineadas(secs):
    M = np.zeros((5, 4), dtype=int)
    for vecs in secs:
        take = vecs[-5:] if len(vecs) >= 5 else vecs
        for k, v in enumerate(take):
            M[5 - len(take) + k] += v
    return M.ravel().tolist()


sumas63 = sumas_alineadas(Q)
central = SEC68[1]
pr("\nP2b: sumas de UR063 frente a TODAS las ventanas contiguas de 20 cuerdas")
pr("     de cada quipu de Puruchuco (se informa el maximo de cada quipu):")
filas = []
for k in ks:
    v = V(k)
    if len(v) < 20:
        continue
    vals = [matches(sumas63, v[i:i + 20]) for i in range(len(v) - 19)]
    filas.append(dict(kfg=k, n_ventanas=len(vals), max_exactas=max(vals),
                      ventana=int(np.argmax(vals)) + 1,
                      exactas_en_central=(matches(sumas63, v[33:53]) if len(v) >= 53 and k == "UR068" else np.nan)))
t2 = pd.DataFrame(filas).sort_values("max_exactas", ascending=False)
pr(t2.to_string(index=False))
# ventana concreta de UR068 (seccion central)
pr(f"\nUR068 seccion central (cuerdas 34-53): {matches(sumas63, central)}/20 exactas, "
   f"{matches(sumas63, central, tol=True)}/20 con tolerancia")
pr(f"nulo de la mejor ventana entre los 22 quipus: media={t2.max_exactas.mean():.2f}, "
   f"max={t2.max_exactas.max()}")
p_vent = (1 + (t2.max_exactas >= matches(sumas63, central)).sum()) / (len(t2) + 1)
pr(f"p empirico (mejor ventana >= observado, sin corregir por ventanas): {p_vent:.4f}")

t1.to_csv(L.AQUI / "control_p1.csv", index=False)
t2.to_csv(L.AQUI / "control_p2.csv", index=False)
with open(L.AQUI / "salida_05_controles.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
