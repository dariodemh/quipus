# -*- coding: utf-8 -*-
"""Desciframiento por tanteo controlado de quipus no numericos.

Para cada (quipu, alfabeto):
  1. secuencia de signos (cuerdas de nivel 0 en orden)
  2. optimo de verosimilitud bigrama por recocido simulado (4 reinicios)
  3. nulo: 60 barajados de la MISMA secuencia, mismo esfuerzo de busqueda
  4. calibracion: 20 replicas de TEXTO QUECHUA REAL comprimido a V clases
     (mismo n y V) -> distribucion de z bajo la hipotesis "es lengua"
  5. estadisticos sin asignacion: H condicional, Zipf, repeticion
Controles explicitos: quipus numericos de Incahuasi, secuencias aleatorias,
texto real con cifrado biyectivo (positivo).
"""
import re, os, sys, json, math, time
import numpy as np
import pandas as pd
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D
from lm_utils import CORP, silabas

BASE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261018
N_NULL = 60
N_PC = 20
REST_OBS = 4
REST_CTRL = 2
ITERS = 2500

# ------------------------------------------------------------------ datos
df = pd.read_csv(r"./analisis/datos/cuerdas.csv")
df = df.drop_duplicates(subset=["kfg", "cuerda"], keep="first")

KNOT = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\)(?:,([\d.]+))?")
def parse_nudos(s):
    if not isinstance(s, str) or not s.strip():
        return []
    return [(int(m.group(1)), m.group(2), float(m.group(3)), m.group(4))
            for m in KNOT.finditer(s)]

def col_base(c):
    """Color canonico: componentes basicos ordenados (sin rangos ni posiciones)."""
    if not isinstance(c, str):
        return "?"
    c = re.sub(r"\([^)]*\)", "", c)          # quitar rangos de posicion
    parts = re.split(r"[:/\-]", c)
    parts = sorted({p.strip().upper() for p in parts if p.strip()})
    return "+".join(parts) if parts else "?"

def sig_color(r): return str(r["color"]).strip() if pd.notna(r["color"]) else "?"
def sig_color2(r): return col_base(r["color"])
def sig_color_tor(r): return sig_color2(r) + "|" + (str(r["torsion"]).strip() if pd.notna(r["torsion"]) else "?")
def sig_color_uni(r): return sig_color2(r) + "|" + (str(r["union"]).strip() if pd.notna(r["union"]) else "?")
def sig_color_fib(r):
    notas = str(r["notas"]).lower() if pd.notna(r["notas"]) else ""
    canuto = "K" if "canut" in notas else "-"
    term = str(r["terminacion"]).strip() if pd.notna(r["terminacion"]) else "?"
    return sig_color2(r) + "|" + canuto + term
def sig_nudo(r):
    ks = parse_nudos(r["nudos"])
    if not ks:
        return "_"
    return f"{len(ks)}" + "".join(k[1] for k in ks)
def sig_color_nudo(r): return sig_color2(r) + "|" + sig_nudo(r)

SIGS = {"A1_color": sig_color2, "A2_color_tor": sig_color_tor,
        "A3_color_union": sig_color_uni, "A4_color_fibra": sig_color_fib,
        "A5_nudo": sig_nudo, "A6_color_nudo": sig_color_nudo}

CAND = ["UR179", "UR180", "UR178", "UR050", "UR054", "UR052", "AS076", "JC012",
        "UR203", "UR215"]
NUM = ["UR278", "UR266"]

def secuencia(kfg, fn):
    s = df[(df.kfg == kfg) & (df.nivel == 0)].sort_values("orden")
    return [fn(r) for _, r in s.iterrows()]

def micro(kfg):
    seq = []
    s = df[(df.kfg == kfg) & (df.nivel == 0)].sort_values("orden")
    for _, r in s.iterrows():
        ks = parse_nudos(r["nudos"])
        if not ks:
            seq.append("_")
        for (n, t, p, d) in ks:
            seq.append(f"{t}{min(n, 9)}{d}")
        seq.append("|")
    return seq

# ------------------------------------------------------------------ LM
LM_NAME = os.environ.get("LM", "quechua")
uni, bi = D.load_stream_lm(LM_NAME)
L, TOP = D.build_L(uni, bi, 120)
K = len(TOP)
TXT_FILE = {"quechua": "quechua.txt", "aymara": "aymara_limpio.txt",
            "quechua_wiki": "quechua_wiki.txt"}[LM_NAME]
txt = open(os.path.join(CORP, TXT_FILE), encoding="utf-8").read()
STREAM = []
for line in txt.lower().split("\n"):
    for w in re.findall(r"[a-zA-ZñÑ]+", line):
        STREAM.extend(silabas(w))
STREAM = np.array(STREAM)
TYPES, CODES = np.unique(STREAM, return_inverse=True)
print("stream quechua", len(STREAM), "silabas; K =", K, "; tipos", len(TYPES))

rng_global = np.random.default_rng(SEED)

def zscore(obs, null):
    return (obs - null.mean()) / (null.std() + 1e-9)

def run_config(seq, label):
    C, st, inv = D.counts_seq(seq)
    V = len(inv); n = len(seq)
    C1 = C[None]; st1 = st[None]
    t0 = time.time()
    f, v = D.anneal(C1, st1, L, restarts=REST_OBS, iters=ITERS, seed=SEED)
    obs = v[0]
    # ---- nulo: barajados
    seqs = [list(np.random.default_rng(SEED + 1 + i).permutation(seq)) for i in range(N_NULL)]
    Cs, sts = [], []
    for s in seqs:
        cc, ss, _ = D.counts_seq(s); Cs.append(cc); sts.append(ss)
    _, vn = D.anneal(np.array(Cs), np.array(sts), L, restarts=REST_CTRL,
                     iters=ITERS, seed=SEED + 7)
    # ---- calibracion: lengua real comprimida a V clases CON LA MISMA
    # distribucion marginal de signos que el quipu (control pareado)
    freqs = np.array(sorted(Counter(seq).values(), reverse=True))
    pcs = []
    for i in range(N_PC):
        r = np.random.default_rng(SEED + 1000 + i)
        start = r.integers(0, len(STREAM) - n)
        plain = STREAM[start:start + n]
        tipos, cuentas = np.unique(plain, return_counts=True)
        orden = np.argsort(-cuentas)
        etiquetas = np.repeat(np.arange(V), freqs)[:n]
        mp = {}
        pos = 0
        for ti in orden:
            mp[tipos[ti]] = int(etiquetas[min(pos, n - 1)])
            pos += cuentas[ti]
        cls = [mp[x] for x in plain]
        cc = np.zeros((V, V)); ss = np.zeros(V)
        for t, x in enumerate(cls):
            if t == 0: ss[x] += 1
            else: cc[cls[t - 1], x] += 1
        pcs.append((cc, ss))
    Cs2 = np.array([x[0] for x in pcs]); sts2 = np.array([x[1] for x in pcs])
    _, vpc = D.anneal(Cs2, sts2, L, restarts=REST_CTRL, iters=ITERS, seed=SEED + 11)
    # ---- estadisticos sin asignacion
    hc, hn = D.hcond(seq, V)
    zs = D.zipf_slope(seq); rr = D.rep_rate(seq)
    out = dict(quipu=label[0], alfabeto=label[1], n=n, n_signos=V,
               inventario=" ".join(inv)[:300],
               logL_obs=obs / n, logL_null_mean=vn.mean() / n,
               logL_null_sd=vn.std() / n,
               logL_pc_mean=vpc.mean() / n, logL_pc_sd=vpc.std() / n,
               z_obs=zscore(obs, vn), z_pc_mean=zscore(vpc.mean(), vn),
               p_vs_barajado=float((vn >= obs).mean()),
               p_calibrado=float((vpc >= obs).mean()),
               entropia_cond=hc, entropia_norm=hn,
               zipf=zs, repeticion=rr,
               seg=time.time() - t0)
    return out

rows = []
configs = []
for k in CAND + NUM:
    for name, fn in SIGS.items():
        seq = secuencia(k, fn)
        if len(seq) >= 8:
            configs.append((seq, (k, name)))
    configs.append((micro(k), (k, "A6_micro")))

outpath = os.path.join(BASE, "resultados.csv" if LM_NAME == "quechua" else f"resultados_{LM_NAME}.csv")
for i, (seq, lab) in enumerate(configs):
    try:
        r = run_config(seq, lab)
        rows.append(r)
        pd.DataFrame(rows).to_csv(outpath, index=False)
        print(f"{i+1}/{len(configs)} {lab} n={r['n']} V={r['n_signos']} "
              f"logL/s={r['logL_obs']:.2f} null={r['logL_null_mean']:.2f} "
              f"pc={r['logL_pc_mean']:.2f} p={r['p_vs_barajado']:.3f} "
              f"pcal={r['p_calibrado']:.3f} ({r['seg']:.1f}s)")
    except Exception as e:
        print("ERROR", lab, e)
print("listo", len(rows))
