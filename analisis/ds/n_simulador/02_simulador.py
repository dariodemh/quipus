# -*- coding: utf-8 -*-
"""Simulador generativo del archivo de Incahuasi.

Estructura
----------
Un "flujo" tiene R registros. Cada registro se reparte en J=9 unidades con pesos
estables w_j (las 9 columnas de UR278). Cada unidad se parte en dos componentes:
B (colgante, ~76 %) y A (subsidiaria, ~24 %). Niveles:
  unidad (9)  ->  componentes A/B  ->  libro del flujo (A+B, cuota 47)
  UR270 (detalle)  ->  UR278 (tabla derivada: celda = B_j + A_j)
                   ->  UR273A/B (componentes independientes) -> UR266/275/269

Dos tipos de enlace, con presupuestos de error distintos:
  DERIVADO     destino = suma de cuerdas que ya existen (solo error de transcripcion)
  INDEPENDIENTE destino atado aparte desde el mismo hecho (error de racimo en origen)

Parametros explicitos en PARAMS. Semilla fija.
"""
import json
import numpy as np
import pandas as pd

RAIZ = r"."
OUT = RAIZ + r"\analisis\ds\n_simulador"
SEMILLA = 20261018
rng = np.random.default_rng(SEMILLA)

# pesos de las 9 columnas (medias reales de UR278, normalizadas)
BASE9 = np.array([290, 299, 209, 239, 255, 284, 246, 184, 195], float)
W9 = BASE9 / BASE9.sum()

PARAMS = dict(
    med=2015.0,        # mediana del total bruto de un registro (real: 2015)
    sig_row=0.36,      # dispersion del tamano de registro (CV real: 0.364)
    sig_idio=0.24,     # ruido idiosincratico de cada unidad
    a_mean=0.24,       # fraccion media de la parte A (real: 0.24)
    a_conc=30.0,       # concentracion Beta de la parte A
    q_rac=0.050,       # error de UN racimo (nudo) en un componente, por racimo
    q_trans=0.0022,    # error de transcripcion moderna por cuerda (KFG vs OKR)
    p_factor10=0.20,   # fraccion de errores de transcripcion que son x10
    s_blank=0.02,      # componente en blanco / perdido (estructural)
    f_dest=15 / 18,    # probabilidad de que el libro destino se conserve
    p_link=5 / 12,     # fraccion de grupos UR270 que son el mismo registro que UR278
    n_rac=3.4,         # racimos por cuerda (real: 3.39 en A/B)
)

OBS = dict(exact18=8 / 18, exact15=8 / 15, le1=10 / 18, le10=13 / 18,
           le1000=15 / 18, pot=7 / 7, ac=[9, 9, 7, 8, 6, 5, 2, 1, 1, 1, 1, 1],
           cv_col=0.163, cv_row=0.287, corr=0.70)


# ---------------------------------------------------------------- errores
def error_racimo(V, q, nrac=None, rng=rng):
    """Un racimo mal contado: +-1 en una posicion decimal elegida al azar.

    Devuelve (valor, hubo_error). q es por racimo; se aplica a cada racimo de la
    cuerda, de modo que P(error en la cuerda) = 1-(1-q)^nrac.
    """
    V = np.asarray(V, float)
    nrac = PARAMS["n_rac"] if nrac is None else nrac
    hubo = np.zeros(V.shape, bool)
    out = V.copy()
    # numero de racimos con error ~ Binomial(nrac, q)
    nerr = rng.binomial(int(round(nrac)), q, size=V.shape)
    for _ in range(int(nerr.max()) if nerr.size else 0):
        m = nerr > 0
        if not m.any():
            break
        k = rng.integers(0, 4, size=V.shape)   # unidades, decenas, centenas, millares
        d = rng.choice([-1, 1], size=V.shape)
        out = np.where(m & ~hubo, out + d * (10.0 ** k), out)
        hubo |= m
        nerr = np.where(m, nerr - 1, nerr)
    return out, hubo


def error_transcripcion(V, q, rng=rng):
    """Error moderno por cuerda: 20 % factor 10, 80 % errata pequena."""
    V = np.asarray(V, float)
    m = rng.random(V.shape) < q
    out = V.copy()
    if not m.any():
        return out, np.zeros(V.shape, bool)
    u = rng.random(V.shape)
    f10 = m & (u < PARAMS["p_factor10"])
    out = np.where(f10, V * rng.choice([10.0, 0.1], size=V.shape), out)
    pequena = m & ~f10
    out = np.where(pequena, V + rng.choice([-4, -3, -2, -1, 1, 2, 3, 4], size=V.shape), out)
    return out, m


# ---------------------------------------------------------------- registros
def simular_registros(nsim, R, p, rng=rng):
    """Genera R registros y devuelve A, B, C observados y el perfil de diferencias."""
    X = rng.lognormal(np.log(p["med"]), p["sig_row"], (nsim, R))
    E = rng.lognormal(-0.5 * p["sig_idio"] ** 2, p["sig_idio"], (nsim, R, 9))
    U = X[:, :, None] * W9[None, None, :] * E
    a = rng.beta(p["a_mean"] * p["a_conc"], (1 - p["a_mean"]) * p["a_conc"], (nsim, R, 9))
    Au = np.rint(U * a)
    Bu = np.rint(U - Au)
    A = Au.sum(2)
    B = Bu.sum(2)
    C = A + B

    # --- errores de origen: racimo mal contado en A, B o C (independientes)
    A1, eA = error_racimo(A, p["q_rac"], p["n_rac"], rng)
    B1, eB = error_racimo(B, p["q_rac"], p["n_rac"], rng)
    C1, eC = error_racimo(C, p["q_rac"], p["n_rac"], rng)
    err_org = eA | eB | eC

    # --- componente en blanco (estructural)
    blankA = rng.random((nsim, R)) < p["s_blank"]
    blankB = rng.random((nsim, R)) < p["s_blank"]
    A1 = np.where(blankA, np.nan, A1)
    B1 = np.where(blankB, np.nan, B1)

    # --- transcripcion moderna
    A2, _ = error_transcripcion(A1, p["q_trans"], rng)
    B2, _ = error_transcripcion(B1, p["q_trans"], rng)
    C2, _ = error_transcripcion(C1, p["q_trans"], rng)

    # --- registro destino conservado
    presente = rng.random((nsim, R)) < p["f_dest"]
    dif = np.abs(A2 + B2 - C2)
    valido = presente & ~np.isnan(dif)
    exacto = valido & (dif == 0)
    return dict(exacto=exacto, valido=valido, dif=dif, err_org=err_org,
                A=A1, B=B1, C=C1)


def stats_ab(sim):
    d = sim["dif"]
    v = sim["valido"]
    ex = sim["exacto"]
    # se cuentan los 18: destino ausente = no exacto
    exact18 = ex.sum(1) / d.shape[1]
    exact15 = np.where(v.sum(1) > 0, ex.sum(1) / np.maximum(v.sum(1), 1), np.nan)
    le1 = (v & (d <= 1)).sum(1) / d.shape[1]
    le10 = (v & (d <= 10)).sum(1) / d.shape[1]
    le1000 = (v & (d <= 1000)).sum(1) / d.shape[1]
    pot = np.where(v & (d > 0),
                   np.isclose(np.log10(np.maximum(d, 1)), np.round(np.log10(np.maximum(d, 1)))), False)
    pot_frac = np.where((v & (d > 0)).sum(1) > 0,
                        pot.sum(1) / np.maximum((v & (d > 0)).sum(1), 1), np.nan)
    return dict(exact18=exact18, exact15=exact15, le1=le1, le10=le10,
                le1000=le1000, pot=pot_frac)


# ---------------------------------------------------------------- tabla UR278
def simular_tabla(nsim, p, rng=rng):
    """12 grupos: p_link son el mismo registro (enlace derivado), el resto no.

    En el enlace derivado la celda de UR278 se ata como suma de las dos cuerdas
    de UR270: solo hay error de transcripcion (q_trans). En los no enlazados se
    compara con la fila de otro registro y se cuentan coincidencias por azar.
    """
    R = 12
    X = rng.lognormal(np.log(p["med"]), p["sig_row"], (nsim, R))
    E = rng.lognormal(-0.5 * p["sig_idio"] ** 2, p["sig_idio"], (nsim, R, 9))
    U = X[:, :, None] * W9[None, None, :] * E
    a = rng.beta(p["a_mean"] * p["a_conc"], (1 - p["a_mean"]) * p["a_conc"], (nsim, R, 9))
    S = np.rint(U * a)          # parte A (subsidiaria)
    P = np.rint(U - S)          # parte B (colgante)
    celda = P + S
    enlazado = rng.random((nsim, R)) < p["p_link"]
    # errores de transcripcion en las tres cuerdas
    S2, _ = error_transcripcion(S, p["q_trans"], rng)
    P2, _ = error_transcripcion(P, p["q_trans"], rng)
    C2, _ = error_transcripcion(celda, p["q_trans"], rng)
    obs = P2 + S2
    # celda ausente (no copiada) en un 5 % de las celdas
    falta = rng.random(celda.shape) < p.get("p_miss_cell", 0.05)
    # fila de comparacion: si no enlazado, otro registro al azar
    perm = rng.permutation(R)
    Ccmp = np.where(enlazado[:, :, None], C2, C2[:, perm, :])
    aciertos = ((np.abs(obs - Ccmp) <= 1) & ~falta).sum(2)
    return aciertos, enlazado


def stats_tabla(ac, enl):
    # media de aciertos (0-9) de las filas enlazadas y no enlazadas
    ml = np.where(enl, ac, np.nan)
    mu = np.where(~enl, ac, np.nan)
    return (np.nanmean(ml, axis=1), np.nanmean(mu, axis=1),
            (ac >= 6).sum(1), (ac <= 2).sum(1))


# ---------------------------------------------------------------- rejilla
def correr(verbose=True):
    filas = []
    for q_rac in [0.0, 0.02, 0.035, 0.05, 0.065, 0.08, 0.11]:
        for s_blank in [0.0, 0.02, 0.05, 0.10]:
            for q_tr in [0.00047, 0.0022, 0.01, 0.05, 0.10, 0.24]:
                p = dict(PARAMS, q_rac=q_rac, s_blank=s_blank, q_trans=q_tr)
                s = stats_ab(simular_registros(1500, 18, p))
                ac, enl = simular_tabla(400, p)
                ml, mu, n6, n2 = stats_tabla(ac, enl)
                filas.append(dict(q_rac=q_rac, s_blank=s_blank, q_trans=q_tr,
                                  exact18=np.nanmean(s["exact18"]),
                                  exact15=np.nanmean(s["exact15"]),
                                  le1=np.nanmean(s["le1"]), le10=np.nanmean(s["le10"]),
                                  le1000=np.nanmean(s["le1000"]), pot=np.nanmean(s["pot"]),
                                  ac_link=np.nanmean(ml), ac_unlink=np.nanmean(mu),
                                  n_ge6=np.nanmean(n6), n_le2=np.nanmean(n2)))
    df = pd.DataFrame(filas)
    # distancia a los objetivos (todos en la misma escala 0-1)
    df["dist"] = (np.abs(df.exact18 - OBS["exact18"]) +
                  np.abs(df.le1 - OBS["le1"]) +
                  np.abs(df.le10 - OBS["le10"]) +
                  np.abs(df.le1000 - OBS["le1000"]) +
                  np.abs(np.nan_to_num(df.pot) - 1.0) +
                  np.abs(df.ac_link / 9 - 7.8 / 9) +
                  np.abs(df.ac_unlink / 9 - 8 / 63) +
                  np.abs(df.n_ge6 - 5) / 12 + np.abs(df.n_le2 - 6) / 12)
    df.to_csv(OUT + r"\rejilla_ajuste.csv", index=False)
    if verbose:
        print("== 10 mejores combinaciones (dist = suma de |sim-obs|) ==")
        print(df.sort_values("dist").head(10).to_string(index=False))
        print("\n== perfil con q_rac=0, s_blank=0 (solo transcripcion moderna) ==")
        print(df[(df.q_rac == 0) & (df.s_blank == 0)][
            ["q_trans", "exact18", "le1", "le10", "pot", "ac_link"]].to_string(index=False))
        print("\n== perfil con q_trans=0.0022, s_blank=0.05 (solo error de racimo) ==")
        print(df[(df.q_trans == 0.0022) & (df.s_blank == 0.05)][
            ["q_rac", "exact18", "le1", "le10", "le1000", "pot", "ac_link"]].to_string(index=False))
    return df


# ---------------------------------------------------------------- valores y vacias
def simular_valores(nsim, p, rng=rng):
    """Distribucion de valores de las cuerdas de detalle (UR278) y de cabeceras."""
    X = rng.lognormal(np.log(p["med"]), p["sig_row"], nsim)
    E = rng.lognormal(-0.5 * p["sig_idio"] ** 2, p["sig_idio"], (nsim, 9))
    U = X[:, None] * W9[None, :] * E
    a = rng.beta(p["a_mean"] * p["a_conc"], (1 - p["a_mean"]) * p["a_conc"], (nsim, 9))
    A = np.rint(U * a)
    B = np.rint(U - A)
    return (U.ravel(), (A + B).sum(1), A.sum(1), B.sum(1))


if __name__ == "__main__":
    df = correr()
    json.dump({k: (float(v) if np.isscalar(v) else v) for k, v in PARAMS.items()},
              open(OUT + r"\parametros.json", "w"), indent=1)
