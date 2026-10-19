# -*- coding: utf-8 -*-
"""Define alfabetos de signo-por-cuerda y extrae las secuencias de signos.

Alfabetos (a priori, declarados antes de mirar la verosimilitud):
  A1 color          : codigo de color exacto tal como lo registra el KFG
  A2 color+tor      : color exacto + torsion (S/Z/U)
  A3 color+union    : color exacto + tipo de union al cordon (R/V/T/U)
  A4 color+fibra    : color exacto + material/fibra (canuto / terminacion como prox.)
  A5 nudo           : tipologia de nudos de la cuerda (nº y patron de tipos), '_' si vacia
  A6 micro          : secuencia de nudos dentro de la cuerda como signos (tipo+direccion)

Unidad de secuencia: cuerdas de nivel 0 en orden `orden` (variante: todas las cuerdas).
"""
import re, json, os, sys
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
D = r"./analisis/datos/cuerdas.csv"

CAND = ["UR179", "UR180", "UR178", "UR050", "UR054", "UR052", "AS076", "JC012",
        "UR203", "UR215"]
NUM = ["UR278", "UR266"]

df = pd.read_csv(D)
# dedup como en n_no_numericos
df = df.drop_duplicates(subset=["kfg", "cuerda"], keep="first")

KNOT = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\)(?:,([\d.]+))?")

def parse_nudos(s):
    """Devuelve lista de (n, tipo, pos, dir, valor)."""
    if not isinstance(s, str) or not s.strip():
        return []
    out = []
    for m in KNOT.finditer(s):
        out.append((int(m.group(1)), m.group(2), float(m.group(3)), m.group(4),
                    float(m.group(5)) if m.group(5) else None))
    return out

def sig_color(r):
    return str(r["color"]).strip() if pd.notna(r["color"]) else "?"

def sig_color_tor(r):
    return sig_color(r) + "|" + (str(r["torsion"]).strip() if pd.notna(r["torsion"]) else "?")

def sig_color_uni(r):
    return sig_color(r) + "|" + (str(r["union"]).strip() if pd.notna(r["union"]) else "?")

def sig_color_fib(r):
    # no hay fibra en cuerdas.csv: usamos terminacion + presencia de canuto en notas
    notas = str(r["notas"]).lower() if pd.notna(r["notas"]) else ""
    canuto = "K" if ("canuto" in notas or "canut" in notas) else "-"
    term = str(r["terminacion"]).strip() if pd.notna(r["terminacion"]) else "?"
    return sig_color(r) + "|" + canuto + term

def sig_nudo(r):
    ks = parse_nudos(r["nudos"])
    if not ks:
        return "_"
    tipos = "".join(k[1] for k in ks)
    return f"{len(ks)}{tipos}"

def sig_color_nudo(r):
    return sig_color(r) + "|" + sig_nudo(r)

SIGS = {"A1_color": sig_color, "A2_color_tor": sig_color_tor,
        "A3_color_union": sig_color_uni, "A4_color_fibra": sig_color_fib,
        "A5_nudo": sig_nudo, "A6_color_nudo": sig_color_nudo}

def secuencia(kfg, col, nivel0=True):
    s = df[df.kfg == kfg]
    if nivel0:
        s = s[s.nivel == 0]
    s = s.sort_values("orden")
    return [SIGS[col](r) for _, r in s.iterrows()], s

def micro_secuencia(kfg, nivel0=True):
    """A6b: cada nudo es un signo; las cuerdas se separan con '|'."""
    seq = []
    s = df[df.kfg == kfg]
    if nivel0:
        s = s[s.nivel == 0]
    for _, r in s.sort_values("orden").iterrows():
        ks = parse_nudos(r["nudos"])
        if not ks:
            seq.append("_")
        for (n, t, p, d, v) in ks:
            # signo = tipo + nº de vueltas (1-9) ; direccion aparte
            seq.append(f"{t}{min(n,9)}{d}")
        seq.append("|")
    return seq

if __name__ == "__main__":
    rows = []
    for k in CAND + NUM:
        for name in SIGS:
            seq, s = secuencia(k, name)
            inv = sorted(set(seq))
            rows.append(dict(quipu=k, alfabeto=name, n=len(seq), n_signos=len(inv),
                             tipos=len(inv), inv=" ".join(inv)[:200]))
        seq = micro_secuencia(k)
        rows.append(dict(quipu=k, alfabeto="A6_micro", n=len(seq), n_signos=len(set(seq)),
                         tipos=len(set(seq)), inv=" ".join(sorted(set(seq)))[:200]))
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(BASE, "alfabetos.csv"), index=False)
    print(t.pivot(index="quipu", columns="alfabeto", values="n_signos").to_string())
    print()
    print(t.pivot(index="quipu", columns="alfabeto", values="n").to_string())
    print()
    print(t[t.alfabeto.isin(["A1_color", "A5_nudo"])][["quipu", "alfabeto", "n", "inv"]].to_string())
