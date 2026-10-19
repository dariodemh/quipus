# -*- coding: utf-8 -*-
"""Estadisticos de lengua SIN asignacion de signos (paso 5).

Para cada secuencia de signos: entropia condicional H(next|prev) con correccion
de Miller-Madow, entropia normalizada, pendiente de Zipf y tasa de repeticion.
Se comparan con:
  - barajados de la misma secuencia (misma distribucion, sin orden)
  - texto quechua real comprimido a V clases con la misma marginal (calibracion)
  - secuencias rigidas (periodicas y de runs)
"""
import os, sys, re, json
import numpy as np
import pandas as pd
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decipher as D
from lm_utils import CORP, silabas

BASE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261018
NREF = 200

txt = open(os.path.join(CORP, "quechua.txt"), encoding="utf-8").read()
STREAM = []
for line in txt.lower().split("\n"):
    for w in re.findall(r"[a-zA-ZñÑ]+", line):
        STREAM.extend(silabas(w))
STREAM = np.array(STREAM)

def stats(seq):
    seq = list(seq); n = len(seq); V = len(set(seq))
    c = Counter(seq)
    p = np.array(list(c.values()), float) / n
    H1 = -(p * np.log2(p)).sum()
    bi = Counter(zip(seq[:-1], seq[1:]))
    H2 = -sum((k / (n - 1)) * np.log2(k / c[a]) for (a, b), k in bi.items())
    H2c = H2 + (len(bi) - 1) / (2 * (n - 1) * np.log(2)) if n > 2 else np.nan
    return dict(H_cond=H2c, H_norm=H2c / max(1e-9, np.log2(max(V, 2))),
                H1=H1, zipf=D.zipf_slope(seq), rep=D.rep_rate(seq),
                bigram_tipos=len(bi), V=V, n=n)

def pc_seq(seq, rng):
    """Texto real comprimido a V clases con la MISMA marginal que seq."""
    n = len(seq); V = len(set(seq))
    freqs = np.array(sorted(Counter(seq).values(), reverse=True))
    start = rng.integers(0, len(STREAM) - n)
    plain = STREAM[start:start + n]
    tipos, cuentas = np.unique(plain, return_counts=True)
    orden = np.argsort(-cuentas)
    etiquetas = np.repeat(np.arange(V), freqs)[:n]
    mp = {}; pos = 0
    for ti in orden:
        mp[tipos[ti]] = int(etiquetas[min(pos, n - 1)]); pos += cuentas[ti]
    return [mp[x] for x in plain]

df = pd.read_csv(r"./analisis/datos/cuerdas.csv")
df = df.drop_duplicates(subset=["kfg", "cuerda"], keep="first")
KNOT = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\)")
def parse(s):
    return [(int(m.group(1)), m.group(2)) for m in KNOT.finditer(s)] if isinstance(s, str) else []
def col_base(c):
    if not isinstance(c, str): return "?"
    c = re.sub(r"\([^)]*\)", "", c)
    return "+".join(sorted({p.strip().upper() for p in re.split(r"[:/\-]", c) if p.strip()})) or "?"
def sig_color(r): return col_base(r["color"])
def sig_ctor(r): return col_base(r["color"]) + "|" + str(r["torsion"])
def sig_cuni(r): return col_base(r["color"]) + "|" + str(r["union"])
def sig_cfib(r):
    notas = str(r["notas"]).lower() if pd.notna(r["notas"]) else ""
    return col_base(r["color"]) + "|" + ("K" if "canut" in notas else "-") + str(r["terminacion"])
def sig_nudo(r):
    ks = parse(r["nudos"])
    return "_" if not ks else f"{len(ks)}" + "".join(k[1] for k in ks)
def sig_cnud(r): return col_base(r["color"]) + "|" + sig_nudo(r)
SIGS = {"A1_color": sig_color, "A2_color_tor": sig_ctor, "A3_color_union": sig_cuni,
        "A4_color_fibra": sig_cfib, "A5_nudo": sig_nudo, "A6_color_nudo": sig_cnud}

def seqs(k):
    s = df[(df.kfg == k) & (df.nivel == 0)].sort_values("orden")
    out = {n: [f(r) for _, r in s.iterrows()] for n, f in SIGS.items()}
    m = []
    for _, r in s.iterrows():
        ks = parse(r["nudos"])
        if not ks: m.append("_")
        for (nn, t) in ks: m.append(f"{t}{min(nn,9)}")
        m.append("|")
    out["A6_micro"] = m
    return out

CAND = ["UR179", "UR180", "UR178", "UR050", "UR054", "UR052", "AS076", "JC012",
        "UR203", "UR215", "UR278", "UR266"]
rows = []
for k in CAND:
    for name, seq in seqs(k).items():
        if len(seq) < 8: continue
        s = stats(seq)
        rng = np.random.default_rng(SEED)
        sh = [stats(list(rng.permutation(seq))) for _ in range(NREF)]
        pcr = [stats(pc_seq(seq, rng)) for _ in range(NREF)]
        Hs = np.array([x["H_cond"] for x in sh])
        Hp = np.array([x["H_cond"] for x in pcr])
        rows.append(dict(quipu=k, alfabeto=name, **s,
                         H_cond_shuffle=Hs.mean(), H_cond_pc=Hp.mean(),
                         z_H_shuffle=(s["H_cond"] - Hs.mean()) / (Hs.std() + 1e-9),
                         pct_H_pc=float((Hp <= s["H_cond"]).mean()),
                         zipf_pc=np.mean([x["zipf"] for x in pcr]),
                         rep_pc=np.mean([x["rep"] for x in pcr])))
        print(k, name, "H=%.2f" % s["H_cond"], "shuf=%.2f" % Hs.mean(),
              "pc=%.2f" % Hp.mean(), "z=%.2f" % rows[-1]["z_H_shuffle"],
              "pct_pc=%.2f" % rows[-1]["pct_H_pc"])

t = pd.DataFrame(rows)
t.to_csv(os.path.join(BASE, "langstats.csv"), index=False)
print(t.groupby("alfabeto")[["H_cond", "H_cond_pc", "z_H_shuffle", "pct_H_pc"]].mean().round(2).to_string())
