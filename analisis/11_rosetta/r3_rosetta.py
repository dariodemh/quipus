"""Búsqueda 'Rosetta': secuencias numéricas de transcripciones coloniales contra los 651 quipus.

Alineamiento local (Smith-Waterman) entre la secuencia de la transcripción q_1..q_m y los valores no vacíos
de cada quipu en orden de cuerda (colgantes y subsidiarias, KFG `orden`):
  - acierto si |v - q| = 0 o = 10^k <= max(q,1) (un nudo de más/menos en una posición decimal = "±1 dígito");
  - puntuación del acierto w_j = -log10 f_j, con f_j = frecuencia en el corpus de valores que aciertan q_j
    (penaliza valores comunes: 10, 20, 100 valen poco; 823 vale mucho);
  - saltar una cuerda del quipu: -0,25 (la transcripción puede omitir cuerdas de detalle);
    saltar una cifra de la transcripción: -1.
Nulo: permutación de los valores no vacíos DENTRO del quipu (conserva su distribución de valores, destruye el orden).
p adaptativo: 1 000 permutaciones; si p <= 0,005, 100 000; si sigue en el piso, cola Gumbel ajustada a las 100 000.
BH-FDR sobre todas las pruebas (secuencia x sentido x quipu).
Controles positivos: (a) totales de grupo de UR278 -> UR266/UR275 (04_concordancias); (b) tramo de AS159 -> AS173;
(c) potencia: la secuencia m40 con 2 errores de ±1 dígito insertada en quipus al azar.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from numba import njit
from scipy.stats import gumbel_r, false_discovery_control

RAIZ = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
SEED = 20261017
GQ, GT = 0.25, 1.0


@njit(cache=True)
def acierta(v, q):
    d = abs(v - q)
    if d == 0:
        return True
    lim = max(q, 1.0)
    p = 1.0
    while p <= lim:
        if d == p:
            return True
        p *= 10.0
    return False


@njit(cache=True)
def sw(seq, q, w):
    n, m = len(seq), len(q)
    prev = np.zeros(m + 1)
    best = 0.0
    for i in range(1, n + 1):
        cur = np.zeros(m + 1)
        for j in range(1, m + 1):
            s = prev[j - 1] + (w[j - 1] if acierta(seq[i - 1], q[j - 1]) else -(GQ + GT))
            s = max(s, prev[j] - GQ, cur[j - 1] - GT, 0.0)
            cur[j] = s
            if s > best:
                best = s
        prev = cur
    return best


@njit(cache=True)
def nulo(seq, q, w, B, seed):
    np.random.seed(seed)
    x = seq.copy()
    out = np.empty(B)
    for b in range(B):
        for i in range(len(x) - 1, 0, -1):
            j = np.random.randint(0, i + 1)
            x[i], x[j] = x[j], x[i]
        out[b] = sw(x, q, w)
    return out


def traza(seq, q, w):
    """reconstruye el alineamiento óptimo (python, solo para informar)."""
    n, m = len(seq), len(q)
    H = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = H[i - 1, j - 1] + (w[j - 1] if acierta(seq[i - 1], q[j - 1]) else -(GQ + GT))
            H[i, j] = max(s, H[i - 1, j] - GQ, H[i, j - 1] - GT, 0.0)
    i, j = np.unravel_index(H.argmax(), H.shape)
    pares = []
    while i > 0 and j > 0 and H[i, j] > 0:
        if acierta(seq[i - 1], q[j - 1]) and np.isclose(H[i, j], H[i - 1, j - 1] + w[j - 1]):
            pares.append((int(i - 1), int(q[j - 1]), int(seq[i - 1])))
            i, j = i - 1, j - 1
        elif np.isclose(H[i, j], H[i - 1, j] - GQ):
            i -= 1
        elif np.isclose(H[i, j], H[i, j - 1] - GT):
            j -= 1
        else:
            i, j = i - 1, j - 1
    return pares[::-1]


def pesos(q, todos):
    f = np.array([np.mean([acierta(v, x) for v in todos]) if x < 50 else
                  np.mean(np.isin(todos, [x] + [x + s * 10 ** k for k in range(6) if 10 ** k <= x for s in (-1, 1)]))
                  for x in q])
    return -np.log10(np.maximum(f, 1e-5)), f


def p_adapt(seq, q, w, obs, seed):
    nb = nulo(seq, q, w, 1000, seed)
    k = (nb >= obs - 1e-9).sum()
    p, pg, B = (k + 1) / 1001, np.nan, 1000
    if p <= 0.005:
        nb = nulo(seq, q, w, 100_000, seed + 1)
        k = (nb >= obs - 1e-9).sum()
        p, B = (k + 1) / 100_001, 100_000
        loc, sc = gumbel_r.fit(nb)
        pg = gumbel_r.sf(obs, loc, sc)
        if k == 0:
            p = max(pg, 1e-12)
    return p, pg, B


def cargar():
    c = pd.read_csv(RAIZ / "datos" / "cuerdas.csv", low_memory=False).sort_values(["kfg", "orden"])
    c = c[c.nudos.notna()]
    seqs = {k: g.valor.to_numpy(float) for k, g in c.groupby("kfg")}
    return c, seqs


def consultas():
    t = pd.read_csv(OUT / "transcripciones_numeros.csv")
    Q = {}
    for sid, g in t.groupby("secuencia", sort=False):
        v = g[g.papel != "precio"].valor.to_numpy(float)
        if len(v) >= 3:
            Q[sid] = v
    return Q


def buscar(Q, seqs, todos, excluir=(), etiqueta=""):
    rows = []
    for sid, q in Q.items():
        for sentido, qq in (("directo", q), ("inverso", q[::-1].copy())):
            w, f = pesos(qq, todos)
            for n, (kfg, s) in enumerate(seqs.items()):
                if kfg in excluir or len(s) < 2:
                    continue
                obs = sw(s, qq, w)
                p, pg, B = p_adapt(s, qq, w, obs, SEED + n)
                rows.append(dict(control=etiqueta, secuencia=sid, sentido=sentido, kfg=kfg, n=len(s), score=obs,
                                 score_max=w.sum(), p=p, p_gumbel=pg, B=B))
    return pd.DataFrame(rows)


def describe(df, Q, seqs, todos, top=5):
    lines = []
    for _, r in df.sort_values("p").head(top).iterrows():
        q = Q[r.secuencia] if r.sentido == "directo" else Q[r.secuencia][::-1]
        w, _ = pesos(q, todos)
        pares = traza(seqs[r.kfg], q, w)
        lines.append(f"    {r.secuencia} {r.sentido} {r.kfg}: score {r.score:.2f}/{r.score_max:.2f} p={r.p:.2e} q={r.get('q', np.nan):.3g}"
                     f"  aciertos (pos, transcr->quipu): {pares}")
    return lines


if __name__ == "__main__":
    c, seqs = cargar()
    todos = c.valor.to_numpy(float)
    out = []
    Q = consultas()
    out.append("Pesos (w = -log10 f) por cifra:")
    for sid, q in Q.items():
        w, f = pesos(q, todos)
        out.append(f"  {sid}: " + ", ".join(f"{int(x)}:{y:.2f}" for x, y in zip(q, w)) + f"  (máx. posible {w.sum():.1f})")

    # ---------- controles positivos ----------
    p = c[(c.kfg == "UR278") & (c.nivel == 0)]
    tot = p.groupby("grupo").valor.sum().to_numpy(float)[:12]
    ctrl = {"ctrl_UR278_totales": tot}
    a159 = seqs["AS159"]
    ctrl["ctrl_AS159_tramo"] = a159[0:12].copy()  # contiene el tramo de 8 compartido con AS173 (Urton 2005)
    cpos = buscar(ctrl, seqs, todos, excluir=("UR278", "AS159"), etiqueta="control")
    cpos["q"] = false_discovery_control(cpos.p.clip(upper=1))
    out.append("\nControles positivos (BH dentro de los controles, 2 x 2 x 649 pruebas):")
    out.append(f"  UR278 totales de grupo (12): {tot.astype(int).tolist()}")
    out.append(f"  AS159 cuerdas 0-11: {ctrl['ctrl_AS159_tramo'].astype(int).tolist()}")
    out += describe(cpos, ctrl, seqs, todos, top=6)

    # ---------- búsqueda principal ----------
    res = buscar(Q, seqs, todos, etiqueta="rosetta")
    res["q"] = false_discovery_control(res.p.clip(upper=1))
    res["procedencia"] = pd.read_csv(RAIZ / "datos" / "quipus.csv").set_index("kfg").procedencia.reindex(res.kfg).to_numpy()
    res.sort_values("p").to_csv(OUT / "rosetta_resultados.csv", index=False)
    out.append(f"\nBúsqueda Rosetta: {len(res)} pruebas ({len(Q)} secuencias x 2 sentidos x quipus). "
               f"q<0,05: {(res.q < .05).sum()}; q<0,25: {(res.q < .25).sum()}; p<0,001: {(res.p < .001).sum()} "
               f"(esperadas por azar {len(res) * .001:.1f}); p<0,01: {(res.p < .01).sum()} (esperadas {len(res) * .01:.1f})")
    for sid in Q:
        r = res[res.secuencia == sid]
        out.append(f"  {sid}: mejor p = {r.p.min():.2e} (q = {r.q.min():.2f}); p<0,01 en {(r.p < .01).sum()} de {len(r)}")
    out.append("  Mejores alineamientos:")
    out += describe(res, Q, seqs, todos, top=12)

    # ---------- potencia: m40 plantada con 2 errores de ±1 dígito ----------
    rng = np.random.default_rng(SEED)
    q40 = Q["m40_aldana_aullagas"]
    w40, _ = pesos(q40, todos)
    ks = [k for k, s in seqs.items() if len(s) >= 40]
    det = []
    for t in range(100):
        k = ks[rng.integers(len(ks))]
        s = seqs[k].copy()
        ins = q40.copy()
        for j in rng.choice(len(ins), 2, replace=False):
            ins[j] = ins[j] + rng.choice([-1, 1]) * (10 if ins[j] >= 10 else 1)
        i0 = rng.integers(0, len(s) - len(ins))
        s[i0:i0 + len(ins)] = ins
        obs = sw(s, q40, w40)
        p, pg, B = p_adapt(s, q40, w40, obs, SEED + 10_000 + t)
        det.append(p)
    det = np.array(det)
    thr = 0.05 / len(res)
    out.append(f"\nPotencia (m40 insertada con 2 errores, 100 ensayos): p mediana {np.median(det):.1e}; "
               f"detectada a p <= {thr:.1e} (umbral BH de un único hallazgo) en {(det <= thr).mean():.0%}; a p<0,001 en {(det < .001).mean():.0%}")
    txt = "\n".join(out)
    (OUT / "r3_resumen.txt").write_text(txt, encoding="utf8")
    print(txt)
