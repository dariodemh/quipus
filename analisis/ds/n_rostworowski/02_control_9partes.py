# -*- coding: utf-8 -*-
"""
Controles cuantitativos para el informe Rostworowski.

Dos pruebas de permutación sobre la tabla de 9 columnas de UR278
(analisis/13_sistema_incahuasi/ur278_tabla.csv):

  T1. "Las 9 partes están equilibradas": CV dentro de fila observado
      frente a un nulo de reparto aleatorio del total de cada fila en
      9 partes (Dirichlet(1,...,1)).
  T2. "Las 9 columnas tienen identidad estable": correlación media
      entre perfiles de fila observada frente a un nulo que permuta
      los 9 valores dentro de cada fila (preserva total y CV de fila).

Además: la cuota 47 como proporción del total de cada registro, y
comparación con la estabilidad de las cuotas por tributario de las
tasas de 1577/1590.

Semilla fija: 20261018.
"""
import os
import sys
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
TABLA = os.path.join(REPO, "analisis", "13_sistema_incahuasi", "ur278_tabla.csv")
CUERDAS = os.path.join(REPO, "analisis", "datos", "cuerdas.csv")

RNG = np.random.default_rng(20261018)
NPERM = 20000
COLS = [f"c{i}" for i in range(1, 10)]


def cv_rows(X):
    return (X.std(1, ddof=0) / X.mean(1)).mean()


def mean_profile_r(X):
    C = np.corrcoef(X)
    iu = np.triu_indices(len(X), 1)
    return C[iu].mean()


def main():
    t = pd.read_csv(TABLA)
    X = t[COLS].to_numpy(float)
    completas = ~np.isnan(X).any(1)
    Xc = X[completas]
    out = []
    out.append("CONTROLES UR278 (9 columnas)")
    out.append("=" * 62)
    out.append(f"filas totales: {len(X)}; filas completas (9 columnas): {len(Xc)}")
    out.append(f"suma de las 9 columnas (28 filas): {np.nansum(X):.0f}")
    out.append(f"suma de totales de fila (28 filas): {t.total.sum():.0f}")
    out.append("")

    # T1 -----------------------------------------------------------------
    cv_obs = cv_rows(Xc)
    null1 = np.empty(NPERM)
    for b in range(NPERM):
        S = RNG.dirichlet(np.ones(9), size=len(Xc)) * Xc.sum(1, keepdims=True)
        null1[b] = cv_rows(S)
    p1 = (np.sum(null1 <= cv_obs) + 1) / (NPERM + 1)
    out.append("T1. Equilibrio de las 9 partes (CV dentro de fila)")
    out.append(f"  CV observado (media de {len(Xc)} filas): {cv_obs:.4f}")
    out.append(f"  nulo Dirichlet(1) media: {null1.mean():.4f} (sd {null1.std():.4f})")
    out.append(f"  p unilateral (nulo <= obs): {p1:.2e}")
    out.append(f"  CV por fila: mínimo {cv_obs and (Xc.std(1,ddof=0)/Xc.mean(1)).min():.3f}, "
               f"máximo {(Xc.std(1,ddof=0)/Xc.mean(1)).max():.3f}")
    out.append("")

    # T2 -----------------------------------------------------------------
    r_obs = mean_profile_r(Xc)
    null2 = np.empty(NPERM)
    for b in range(NPERM):
        Y = np.array([RNG.permutation(r) for r in Xc])
        null2[b] = mean_profile_r(Y)
    p2 = (np.sum(null2 >= r_obs) + 1) / (NPERM + 1)
    out.append("T2. Identidad estable de las 9 columnas (correlación de perfiles)")
    out.append(f"  r media observada ({len(Xc)*(len(Xc)-1)//2} pares): {r_obs:.4f}")
    out.append(f"  nulo (permutar dentro de fila) media: {null2.mean():.4f} "
               f"(sd {null2.std():.4f})")
    out.append(f"  p unilateral (nulo >= obs): {p2:.2e}")
    out.append("")

    # Holm sobre las dos pruebas
    ps = [p1, p2]
    orden = np.argsort(ps)
    holm = np.empty(2)
    m = 2
    prev = 0.0
    for rank, idx in enumerate(orden):
        val = min(1.0, (m - rank) * ps[idx])
        prev = max(prev, val)
        holm[idx] = prev
    out.append("Corrección de Holm (2 pruebas)")
    out.append(f"  T1 p={p1:.2e} -> p_Holm={holm[0]:.2e}")
    out.append(f"  T2 p={p2:.2e} -> p_Holm={holm[1]:.2e}")
    out.append("")

    # Perfil de columnas
    tot_col = Xc.sum(0)
    share = tot_col / tot_col.sum()
    out.append("Perfil de las 9 columnas (filas completas)")
    out.append("  totales: " + ", ".join(f"{v:.0f}" for v in tot_col))
    out.append("  cuotas:  " + ", ".join(f"{100*v:.1f}%" for v in share))
    out.append(f"  mayor/menor = {share.max()/share.min():.2f}")
    out.append("")

    # Cuota 47 -----------------------------------------------------------
    out.append("CUOTA 47 COMO PROPORCIÓN DEL REGISTRO (UR278, 28 filas)")
    out.append("=" * 62)
    r = 47 / t.total.astype(float)
    out.append(f"  rango: {100*r.min():.2f}% - {100*r.max():.2f}%")
    out.append(f"  media: {100*r.mean():.2f}%; CV: {r.std()/r.mean():.2f}")
    out.append(f"  filas dentro de ±10% de 2%: {int(((r>0.018)&(r<0.022)).sum())} de {len(r)}")
    out.append(f"  totales de registro: mínimo {t.total.min():.0f}, "
               f"máximo {t.total.max():.0f}, mediana {t.total.median():.0f}")
    out.append("  Lectura: 47 es una cuota ABSOLUTA fija; su proporción varía 3,8x.")
    out.append("")

    # Grupos KFG de otras cuotas
    c = pd.read_csv(CUERDAS)
    out.append("CUOTAS EN OTROS QUIPUS (grupos de cuerdas nivel 0, KFG)")
    out.append("=" * 62)
    for k, q in [("UR275", 47), ("UR268", 208), ("UR266", 47)]:
        d = c[(c.kfg == k) & (c.nivel == 0) & (c.valor > 0)]
        g = d.groupby("grupo").valor.sum()
        rr = q / g
        out.append(f"  {k}: cuota {q}, {len(g)} grupos, proporción "
                   f"{100*rr.min():.2f}%-{100*rr.max():.2f}%, "
                   f"media {100*rr.mean():.2f}%, CV {rr.std()/rr.mean():.2f}")
    out.append("  (KFG; no son los valores publicados por Urton & Chu 2018)")
    out.append("")

    # Estabilidad de las tasas históricas -------------------------------
    out.append("ESTABILIDAD DE LAS CUOTAS POR TRIBUTARIO (1577 vs 1590)")
    out.append("=" * 62)
    pares = [("ropa", 366/732, 234.5/469),
             ("aves", 758/732, 483.5/469),
             ("plata", 2196/732, 1392.34375/469),
             ("total", 3660/732, 2330.28125/469)]
    for nombre, a, b in pares:
        out.append(f"  {nombre:6s}: 1577={a:.4f}  1590={b:.4f}  "
                   f"cambio={100*(b-a)/a:+.2f}%")
    out.append("  Lectura: la tasa colonial es una plantilla POR CABEZA;")
    out.append("  al caer la población 36%, el total baja pero la cuota unitaria casi no cambia.")
    out.append("")

    # El 9 en las fuentes -------------------------------------------------
    out.append("EL NÚMERO 9 EN LAS UNIDADES DOCUMENTADAS (exploratorio)")
    out.append("=" * 62)
    unidades = [("Lunahuaná guarangas", 4), ("Lunahuaná curacas", 8),
                ("Lunahuaná barrios/ayllus", 16), ("Collique pachacas", 10),
                ("Guancayos pachacas", 9), ("Chincha pachacas", 30)]
    for nombre, n in unidades:
        out.append(f"  {nombre:28s} {n}")
    p9 = 1 - (28/29)**len(unidades)
    out.append(f"  P(≥1 nueve) si los conteos fueran uniformes en 2..30: {p9:.3f}")
    out.append("  -> con 6 conteos, un solo 9 no es estadísticamente especial;")
    out.append("     el 9 de Guancayos es un ancla textual, no una prueba.")
    out.append("")

    # Declive demográfico ------------------------------------------------
    out.append("DECLIVE DEMOGRÁFICO (cifras del texto)")
    out.append("=" * 62)
    out.append(f"  tributarios 1577->1590: 740 -> 474 = {100*(474-740)/740:+.1f}%")
    out.append(f"  personas 1577->1590:   3276 -> 1915 = {100*(1915-3276)/3276:+.1f}%")
    out.append("  1590 compara además con 590 tributarios de la cuenta anterior:")
    out.append(f"  590 -> 469 = {100*(469-590)/590:+.1f}% (faltan 121, línea 805).")
    out.append("")

    txt = "\n".join(out)
    with open(os.path.join(BASE, "resultados_control.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
