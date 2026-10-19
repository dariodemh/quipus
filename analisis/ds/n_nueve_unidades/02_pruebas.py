"""02. Pruebas pre-registradas para las tres hipótesis sobre las 9 columnas.

Dos familias de nulo, porque las preguntas son distintas:

  NULO L (etiquetas de columna, MISMA permutación en todas las filas; 9! = 362 880 exacto).
      Pregunta: ¿el ORDEN FÍSICO observado de las 9 columnas es especial frente a otros órdenes?
      Conserva el perfil de medias por columna, el efecto de fila y toda la distribución conjunta
      salvo la asignación de posiciones. Es el nulo correcto para (A) tiempo/adyacencia y para
      cualquier predicción sobre el orden.

  NULO C (permutación independiente de cada columna entre filas; 20 000 réplicas).
      Pregunta: ¿hay ASOCIACIÓN entre columnas más allá de sus marginales?
      Destruye la covariación entre columnas conservando la distribución de cada una. Es el nulo
      correcto para (B/C) emparejamientos y mitades, y para "una columna distinta".
      OJO: los estadísticos de "mejor de 945 emparejamientos" son INVARIANTES a permutar etiquetas,
      así que el nulo L les daría p=1 por construcción; por eso se calibran con el nulo C.

Estadísticos (definidos antes de mirar los resultados):
  L1 adj_abs      suma |p_j - p_{j+1}| del perfil (cola baja = columnas vecinas parecidas)
  L2 adj_corr     correlación media entre columnas físicamente adyacentes (cola alta)
  L3 trend        |Spearman(perfil, posición)| (dos colas)
  L4 extrema      nº de extremos locales del perfil (cola baja = curva suave/estacional)
  L5 season       R2 de perfil ~ 1 + cos(2pi j/9) + sin(2pi j/9) (cola alta)
  L6 pair_corr    r media del emparejamiento a priori (1-2)(3-4)(5-6)(7-8) (cola alta)
  L7 pair_prof    suma |p_i - p_j| de ese mismo emparejamiento (cola baja)
  L8 mit44_prof   |media(p1..p4) - media(p5..p8)| (cola alta)
  L9 adj_ties     nº de celdas con |x_ij - x_i,j+1| <= 1 (cola alta)
  C0 friedman     chi2 de Friedman sobre rangos dentro de fila (cola alta: hay efecto de columna)
  C1 best_pair    máximo sobre los 945 emparejamientos de la r media intra-par (cola alta)
  C2 best_44      máximo sobre las 126 biparticiones 4+4(+1) de (r intra - r entre) (cola alta)
  C3 best_ties    máximo sobre 945 emparejamientos de igualdades intra-par (cola alta)
  C1b best_pair_abs  igual que C1 pero con |r| (relación de cualquier signo)
  C5 gap          mayor hueco del perfil ordenado / rango (cola alta = una columna aparte)
  (C4, CV de sumas de par, se descartó: el nulo de columnas independientes destruye el efecto de
   fila común y hace que CUALQUIER par parezca estable; ver 03_diagnosticos.py y el informe.)

Salidas: pruebas.csv (hipotesis, estadistico, observado, nulo_media, p, q) y salida_02.txt.
"""
import itertools
import json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.stats import rankdata, friedmanchisquare

AQUI = Path(__file__).resolve().parent
SEED = 20261018
rng = np.random.default_rng(SEED)
NPERM_C = 20000
COLS = [f"c{i}" for i in range(1, 10)]


# ---------------------------------------------------------------- datos
def matrices():
    T = pd.read_csv(AQUI / "ur278_24.csv")
    X = T[COLS].to_numpy(float)
    U = pd.read_csv(AQUI / "ur270_9.csv")
    X270 = U[COLS].to_numpy(float)
    return T, X, X270


def clr(X):
    Y = np.log(X)
    return Y - Y.mean(1, keepdims=True)


# ---------------------------------------------------------------- estadísticos
def perfil(Z):
    return Z.mean(0)


def n_extremos(p):
    d = np.diff(p)
    s = np.sign(d)
    s = s[s != 0]
    return int(np.sum(s[1:] != s[:-1]))


def r2_estacional(p):
    j = np.arange(9)
    D = np.column_stack([np.ones(9), np.cos(2 * np.pi * j / 9), np.sin(2 * np.pi * j / 9)])
    beta, *_ = np.linalg.lstsq(D, p, rcond=None)
    res = p - D @ beta
    return 1 - (res @ res) / ((p - p.mean()) @ (p - p.mean()))


def spearman_abs(p):
    return abs(np.corrcoef(rankdata(p), np.arange(1, 10))[0, 1])


# 945 emparejamientos de 8 columnas dejando una fuera
def emparejamientos():
    out = []
    for fuera in range(9):
        idx = [i for i in range(9) if i != fuera]
        for a in itertools.combinations(idx, 2):
            r1 = [i for i in idx if i not in a]
            for b in itertools.combinations(r1, 2):
                r2 = [i for i in r1 if i not in b]
                for c in itertools.combinations(r2, 2):
                    d = tuple(i for i in r2 if i not in c)
                    out.append((a, b, c, d))
    assert len({tuple(sorted(m)) for m in out}) == 945
    return out


EMP = emparejamientos()
E0 = np.array([[m[k][0] for m in EMP] for k in range(4)]).T   # (945,4)
E1 = np.array([[m[k][1] for m in EMP] for k in range(4)]).T
PAIRS = [(i, j) for i in range(9) for j in range(i + 1, 9)]
PI = np.array([p[0] for p in PAIRS])
PJ = np.array([p[1] for p in PAIRS])


def biparticiones():
    """126 formas de elegir 4 columnas; el complemento son 4 y sobra 1. Cada bipartición 2 veces."""
    out = []
    for S in itertools.combinations(range(9), 4):
        C = tuple(i for i in range(9) if i not in S)
        out.append((S, C))
    return out


BIP = biparticiones()
# índices de pares intra y entre para cada bipartición
INTRA = []
ENTRE = []
for S, C in BIP:
    intra = [(i, j) for i in S for j in S if i < j] + [(i, j) for i in C for j in C if i < j]
    entre = [(min(i, j), max(i, j)) for i in S for j in C]
    INTRA.append([PAIRS.index(p) for p in intra])
    ENTRE.append([PAIRS.index(p) for p in entre])
INTRA = np.array(INTRA)   # (126,12)
ENTRE = np.array(ENTRE)   # (126,16)


def stats_asociacion(R):
    """Estadísticos C a partir de la matriz de correlaciones 9x9."""
    q = R[E0, E1]                                   # (945,4)
    best_pair = float(q.mean(1).max())
    best_abs = float(np.abs(q).mean(1).max())
    wi = R[PI, PJ]
    intra_b = wi[INTRA].mean(1)
    entre_b = wi[ENTRE].mean(1)
    best_44 = float((intra_b - entre_b).max())
    return best_pair, best_44, best_abs


PIDX = np.array([[PAIRS.index(p) for p in m] for m in EMP])   # (945,4) índices en PAIRS


def suma_pares(X):
    """CV (entre filas) de la suma de cada par como fracción del total de la fila; mín. sobre 945."""
    S = X / X.sum(1, keepdims=True)
    PS = S[:, PI] + S[:, PJ]                 # (n,36)
    S4 = PS[:, PIDX]                         # (n,945,4)
    cv = (S4.std(0) / S4.mean(0)).mean(1)    # (945,)
    return cv.min()


def gap_outlier(p, B=20000):
    """Mayor hueco entre valores ordenados / rango. Nulo: 9 valores iid N(0,1) con el mismo rango."""
    ps = np.sort(p)
    obs = np.diff(ps).max() / (ps[-1] - ps[0])
    sim = rng.normal(size=(B, 9))
    sim = np.sort(sim, axis=1)
    nul = np.diff(sim, axis=1).max(1) / (sim[:, -1] - sim[:, 0])
    return obs, nul


# ---------------------------------------------------------------- nulo L exacto
def nulo_L(X):
    Y = np.log(X)
    Z = clr(X)
    p = perfil(Z)
    R = np.corrcoef(Z.T)
    n = len(X)
    perms = np.array(list(itertools.permutations(range(9))), dtype=np.int8)
    B = len(perms)
    Xc = X.astype(float)
    obs = {}
    obs["L1_adj_abs"] = np.abs(np.diff(p)).sum()
    obs["L2_adj_corr"] = np.mean([R[i, i + 1] for i in range(8)])
    obs["L3_trend"] = spearman_abs(p)
    obs["L4_extrema"] = n_extremos(p)
    obs["L5_season"] = r2_estacional(p)
    obs["L6_pair_corr"] = np.mean([R[0, 1], R[2, 3], R[4, 5], R[6, 7]])
    obs["L7_pair_prof"] = np.abs(p[0] - p[1]) + np.abs(p[2] - p[3]) + np.abs(p[4] - p[5]) + np.abs(p[6] - p[7])
    obs["L8_mit44_prof"] = abs(p[:4].mean() - p[4:8].mean())
    obs["L9_adj_ties"] = np.sum(np.abs(np.diff(X, axis=1)) <= 1)

    nul = {k: np.empty(B) for k in obs}
    CH = 20000
    for s in range(0, B, CH):
        Q = perms[s:s + CH]
        pq = p[Q]                                        # (b,9)
        nul["L1_adj_abs"][s:s + CH] = np.abs(np.diff(pq, axis=1)).sum(1)
        nul["L2_adj_corr"][s:s + CH] = R[Q[:, :-1], Q[:, 1:]].mean(1)
        nul["L3_trend"][s:s + CH] = np.array([spearman_abs(v) for v in pq]) if len(Q) < 50 else _spear_vec(pq)
        nul["L4_extrema"][s:s + CH] = _extr_vec(pq)
        nul["L5_season"][s:s + CH] = _r2_vec(pq)
        nul["L6_pair_corr"][s:s + CH] = (R[Q[:, 0], Q[:, 1]] + R[Q[:, 2], Q[:, 3]]
                                         + R[Q[:, 4], Q[:, 5]] + R[Q[:, 6], Q[:, 7]]) / 4
        nul["L7_pair_prof"][s:s + CH] = (np.abs(pq[:, 0] - pq[:, 1]) + np.abs(pq[:, 2] - pq[:, 3])
                                         + np.abs(pq[:, 4] - pq[:, 5]) + np.abs(pq[:, 6] - pq[:, 7]))
        nul["L8_mit44_prof"][s:s + CH] = np.abs(pq[:, :4].mean(1) - pq[:, 4:8].mean(1))
        Xq = Xc[:, Q]                                    # (n,b,9)
        nul["L9_adj_ties"][s:s + CH] = (np.abs(np.diff(Xq, axis=2)) <= 1).sum(axis=(0, 2))
    return obs, nul


def _spear_vec(P):
    n = P.shape[1]
    rp = rankdata(P, axis=1)
    rj = rankdata(np.arange(1, n + 1))
    rp = rp - rp.mean(1, keepdims=True)
    rj = rj - rj.mean()
    num = rp @ rj
    den = np.sqrt((rp ** 2).sum(1) * (rj ** 2).sum())
    return np.abs(num / den)


def _extr_vec(P):
    S = np.sign(np.diff(P, axis=1))
    return (S[:, 1:] != S[:, :-1]).sum(1)


def _r2_vec(P):
    j = np.arange(9)
    D = np.column_stack([np.ones(9), np.cos(2 * np.pi * j / 9), np.sin(2 * np.pi * j / 9)])
    H = D @ np.linalg.pinv(D)
    Pc = P - P.mean(1, keepdims=True)
    num = ((Pc @ H) ** 2).sum(1)
    den = (Pc ** 2).sum(1)
    return num / den


# ---------------------------------------------------------------- nulo C
def nulo_C(X, nperm=NPERM_C, nperm_r2=5000):
    Y = np.log(X)
    Z = clr(X)
    R = np.corrcoef(Z.T)
    obs = {}
    obs["C0_friedman"] = None
    bp, b44, babs = stats_asociacion(R)
    obs["C1_best_pair"] = bp
    obs["C1b_best_pair_abs"] = babs
    obs["C2_best_44"] = b44
    T = (np.abs(X[:, :, None] - X[:, None, :]) <= 1).sum(0).astype(float)
    obs["C3_best_ties"] = max((T[E0, E1].sum(1)).max(), 0)  # suma de 4 pares (no media)
    obs["C5_gap"] = gap_outlier(perfil(Z))[0]

    nul = {k: np.empty(nperm) for k in ["C1_best_pair", "C1b_best_pair_abs", "C2_best_44", "C3_best_ties"]}
    for b in range(nperm):
        Yp = np.column_stack([rng.permutation(Y[:, j]) for j in range(9)])
        Zp = Yp - Yp.mean(1, keepdims=True)
        Rp = np.corrcoef(Zp.T)
        bp, b44, babs = stats_asociacion(Rp)
        nul["C1_best_pair"][b] = bp
        nul["C1b_best_pair_abs"][b] = babs
        nul["C2_best_44"][b] = b44
        Xp = np.exp(Yp)
        # nulo de empates que conserva la "planitud" de cada fila: permutar dentro de cada fila
        Xr = np.array([rng.permutation(r) for r in X])
        Tr = (np.abs(Xr[:, :, None] - Xr[:, None, :]) <= 1).sum(0).astype(float)
        nul["C3_best_ties"][b] = Tr[E0, E1].sum(1).max()
    nul["C5_gap"] = gap_outlier(perfil(Z))[1]
    return obs, nul



def friedman_obs(X):
    return friedmanchisquare(*X.T).statistic


# ---------------------------------------------------------------- p-valores
DIR = {  # cola de rechazo
    "L1_adj_abs": "baja", "L2_adj_corr": "alta", "L3_trend": "alta", "L4_extrema": "baja",
    "L5_season": "alta", "L6_pair_corr": "alta", "L7_pair_prof": "baja", "L8_mit44_prof": "alta",
    "L9_adj_ties": "alta", "C0_friedman": "alta", "C1_best_pair": "alta", "C1b_best_pair_abs": "alta",
    "C2_best_44": "alta", "C3_best_ties": "alta", "C5_gap": "alta",
}
HIP = {"L1_adj_abs": "A", "L2_adj_corr": "A", "L3_trend": "A", "L4_extrema": "A", "L5_season": "A",
       "L6_pair_corr": "B/C", "L7_pair_prof": "B/C", "L8_mit44_prof": "C", "L9_adj_ties": "A",
       "C0_friedman": "B/C", "C1_best_pair": "B/C", "C1b_best_pair_abs": "B/C",
       "C2_best_44": "C", "C3_best_ties": "B/C", "C5_gap": "C"}


def pval(obs, nul, side):
    nul = np.asarray(nul)
    if side == "alta":
        return (np.sum(nul >= obs) + 1) / (len(nul) + 1)
    return (np.sum(nul <= obs) + 1) / (len(nul) + 1)


def bh(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.clip(q, 0, 1)


def holm(p):
    p = np.asarray(p, float)
    n = len(p)
    o = np.argsort(p)
    q = np.empty(n)
    q[o] = np.minimum(1, np.maximum.accumulate(p[o] * (n - np.arange(n))))
    return q


# ---------------------------------------------------------------- main
def main():
    T, X, X270 = matrices()
    print(f"UR278: {X.shape}; UR270: {X270.shape}")

    obsL, nulL = nulo_L(X)
    obsC, nulC = nulo_C(X)

    # Friedman (nulo: permutar dentro de cada fila)
    fo = friedman_obs(X)
    fn = np.array([friedman_obs(np.array([rng.permutation(r) for r in X])) for _ in range(5000)])
    obsC["C0_friedman"] = fo
    nulC["C0_friedman"] = fn

    filas = []
    for k in DIR:
        o = obsL.get(k, obsC.get(k))
        n = nulL.get(k, nulC.get(k))
        p = pval(o, n, DIR[k])
        filas.append({"hipotesis": HIP[k], "estadistico": k, "observado": o,
                      "nulo_media": float(np.mean(n)), "nulo_sd": float(np.std(n)),
                      "nulo_p95": float(np.percentile(n, 95)), "nulo_p05": float(np.percentile(n, 5)),
                      "cola": DIR[k], "p": p, "n_nulo": len(n)})
    P = pd.DataFrame(filas)
    P["q"] = bh(P.p)
    P["q_holm"] = holm(P.p)
    P["q_bh"] = P["q"]
    P = P.sort_values("p").reset_index(drop=True)
    P.to_csv(AQUI / "pruebas.csv", index=False)
    with open(AQUI / "salida_02.txt", "w", encoding="utf-8") as f:
        f.write("UR278, 24 filas x 9 columnas. Nulo L exacto 9!=362880; nulo C 20000 (R2: 5000).\n")
        f.write(P.to_string(index=False, float_format=lambda v: f"{v:.4g}") + "\n")
        f.write(f"\nsemilla {SEED}\n")
    print(P.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    print(f"\nsemilla {SEED}")


if __name__ == "__main__":
    main()
