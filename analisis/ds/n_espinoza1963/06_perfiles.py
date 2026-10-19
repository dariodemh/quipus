# -*- coding: utf-8 -*-
"""Compara los perfiles que la Visita documenta para las 9 pachacas de
Guancayo con la firma de 9 columnas de UR278.

Perfiles:
  - tasa por pachaca: 9 valores iguales (la Visita dice que cada pachaca daba
    la misma lista)
  - productos: [5,26,2,3,4,20,10,3,1] y totales x9
  - supervivencia en 1571: 2 pachacas con gente, 7 extinguidas
  - chacras comunales: 9 chacras, solo 3 de maiz (3 fanegas cada una)
  - mitas: 8 indios repartidos 2/3/2 entre Maca, Guarauni y Guancayo
Salida: perfiles.csv, perfiles_pruebas.csv
"""
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import pearsonr

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
SEED = 20261018
rng = np.random.default_rng(SEED)

d = pd.read_csv(RAIZ / "analisis/13_sistema_incahuasi/ur278_tabla.csv")
C = [f"c{i}" for i in range(1, 10)]
X = d.dropna(subset=C)[C].astype(float).values
perfil = (X / X.sum(1, keepdims=True)).mean(0)
print("Perfil UR278 (cuota por columna):", np.round(perfil, 4))
print("  CV entre columnas: %.4f; max/min: %.3f" % (perfil.std() / perfil.mean(), perfil.max() / perfil.min()))

T = np.array([5, 26, 2, 3, 4, 20, 10, 3, 1], float)
T9 = T * 9
surv = np.array([100, 100, 0, 0, 0, 0, 0, 0, 0], float)  # 2 pachacas de Mongoy vivas
chacras = np.array([3, 3, 3, 0, 0, 0, 0, 0, 0], float)  # 3 chacras de maiz, 3 fanegas
tasa = np.ones(9)


def cv(v):
    return v.std() / v.mean() if v.mean() else np.nan


P = []
P.append(dict(perfil="tasa por pachaca (9 iguales)", media=tasa.mean(), cv=cv(tasa),
              max_min=tasa.max() / tasa.min(), nota="la Visita: misma lista en cada pachaca"))
P.append(dict(perfil="productos (9 rubros)", media=T.mean(), cv=cv(T),
              max_min=T.max() / T.min(), nota="5,26,2,3,4,20,10,3,1"))
P.append(dict(perfil="productos x9", media=T9.mean(), cv=cv(T9),
              max_min=T9.max() / T9.min(), nota="45,234,18,27,36,180,90,27,9"))
P.append(dict(perfil="supervivencia 1571", media=surv.mean(), cv=cv(surv),
              max_min=np.inf, nota="2 vivas / 7 extintas"))
P.append(dict(perfil="chacras de maiz", media=chacras.mean(), cv=cv(chacras),
              max_min=np.inf, nota="3 chacras x 3 fanegas"))
P.append(dict(perfil="UR278 (columnas)", media=perfil.mean(), cv=cv(perfil),
              max_min=perfil.max() / perfil.min(), nota="firma observada"))
P = pd.DataFrame(P)
print("\nPerfiles:")
print(P.to_string(index=False))

# --- correlaciones y pruebas de colocacion ---
res = []
for nombre, v in [("productos", T), ("supervivencia", surv), ("chacras", chacras)]:
    r = pearsonr(v, perfil)[0] if v.std() > 0 else np.nan
    # nulo: permutar el perfil del visitante sobre las 9 columnas
    perm = np.array([pearsonr(v, rng.permutation(perfil))[0] for _ in range(50000)])
    p = (1 + np.sum(perm >= r)) / 50001
    res.append(dict(perfil=nombre, r_orden_documentado=r, p_permutacion=p,
                    r_medio_nulo=perm.mean()))
    print(f"\n{nombre}: r con el orden documentado = {r:.3f}; p (permutar columnas) = {p:.4f}")

# mejor asignacion posible del vector de productos a las 9 columnas (post hoc)
best = (-9, None)
for _ in range(200000):
    q = rng.permutation(T)
    r = pearsonr(q, perfil)[0]
    if r > best[0]:
        best = (r, q)
print("\nMejor asignacion post hoc de los 9 productos a las columnas: r = %.3f (vector %s)" %
      (best[0], best[1].astype(int).tolist()))
print("  (el null de 200000 permutaciones da una idea de lo facil que es encontrar r alto)")

# --- prueba dirigida del bloque de curacas 2+1+2+2+2 ---
L = np.log(X)
Z = L - L.mean(1, keepdims=True)
R = np.corrcoef(Z.T)


def rintra(mm):
    return np.mean([R[i, j] for i, j in mm])


def matchings(items):
    if not items:
        yield []
    else:
        a = items[0]
        for k in range(1, len(items)):
            b = items[k]
            for mm in matchings(items[1:k] + items[k + 1:]):
                yield [(a, b)] + mm


ALL = []
for sing in range(9):
    for mm in matchings([i for i in range(9) if i != sing]):
        ALL.append((sing, mm))
target = [(0, 1), (3, 4), (5, 6), (7, 8)]
vals = np.array([rintra(m) for s, m in ALL])
r = rintra(target)
print("\nBloque de curacas 2+1+2+2+2 (Mongoy 2, Cancay 1, Chuquitanga 2, Chumbillan 2, Antachumbi 2):")
print("  r intra-par = %.3f; rank %d/945; p = %.4f" % (r, 1 + np.sum(vals > r), (1 + np.sum(vals > r)) / len(vals)))

# --- prueba de igualdades del bloque de curacas ---
def ties(M, mm):
    return sum(int(np.sum(M[:, i] == M[:, j])) for i, j in mm)


t = ties(X, target)
tv = np.array([ties(X, m) for s, m in ALL])
cnt = np.empty(20000)
for b in range(20000):
    P_ = np.array([rng.permutation(row) for row in X])
    cnt[b] = ties(P_, target)
print("  igualdades exactas = %d; rank %d/945; p = %.4f; nulo dentro de fila p = %.4f" %
      (t, 1 + np.sum(tv > t), (1 + np.sum(tv > t)) / len(tv), (1 + np.sum(cnt >= t)) / 20001))
print("  media esperada dentro de fila = %.2f" % cnt.mean())

perfiles = pd.DataFrame(res)
perfiles.to_csv(AQUI / "perfiles_pruebas.csv", index=False)
P.to_csv(AQUI / "perfiles.csv", index=False)
