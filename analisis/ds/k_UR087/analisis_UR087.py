#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analisis estructural y aritmetico de UR087 (Santa) + controles nulos.
Semilla fija 0, 1000 permutaciones. Salida a stdout (<= ~40 lineas por bloque)."""
import pandas as pd, numpy as np
from collections import defaultdict
rng = np.random.default_rng(0)

c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg == 'UR087'].copy()
d['valor'] = pd.to_numeric(d.valor, errors='coerce').fillna(0)

p = d[d.nivel == 0].sort_values('orden').reset_index(drop=True)   # 306 colgantes
vals = p.valor.values.astype(int)
N = len(vals)

# ---------- helpers ----------
def count_sixsum(v, N):
    """n de posiciones i>=6 con v[i] == suma de los 6 anteriores."""
    n = 0; idx = []
    for i in range(6, N):
        if v[i] == v[i-6:i].sum():
            n += 1; idx.append(i)
    return n, idx

def count_anysum(v, N):
    """n de posiciones i con v[i] == suma de algun bloque contiguo anterior (2..8 cords)."""
    n = 0
    for i in range(N):
        for L in range(2, 9):
            if i-L >= 0 and v[i] == v[i-L:i].sum() and v[i] > 0:
                n += 1; break
    return n

def count_dups(v):
    from collections import Counter
    cnt = Counter(v)
    # pares repetidos (sin contar el 0 ausente), ponderado por combinaciones
    return sum(k*(k-1)//2 for x, k in cnt.items() if x > 0)

def ratio_const(v):
    """num de tripletas consecutivas a,b,c con a=b=c o a/b constante... usa diferencias."""
    n = 0
    for i in range(len(v)-2):
        a, b, cc = v[i], v[i+1], v[i+2]
        if a > 0 and b > 0 and cc > 0 and abs(a-b) == abs(b-cc):
            n += 1
    return n

# ---------- estructura ----------
def color_run_dirs():
    def cc(x): return str(x).split('/')[0].split(':')[0].split('(')[0].strip()
    cols = p.color.map(cc).values
    runs = []; cur = None; start = 0
    for i in range(N):
        if cols[i] != cur:
            if cur is not None: runs.append((cur, start, i-1))
            cur = cols[i]; start = i
    runs.append((cur, start, N-1))
    return runs

runs = color_run_dirs()
size6 = [r for r in runs if r[2]-r[1]+1 == 6]

print("=== ESTRUCTURA UR087 ===")
print(f"cuerdas totales {len(d)}, colgantes {N}, subsidiarias {(d.nivel>0).sum()}")
print(f"runs de color {len(runs)}; runs de tamano 6: {len(size6)}")
print(f"colores: {p.color.map(lambda x: str(x).split('/')[0].split(':')[0].split('(')[0]).value_counts().to_dict()}")
print(f"union: {d.union.value_counts().to_dict()}; torsion: {d.torsion.value_counts().to_dict()}")
print(f"terminacion: {d.terminacion.value_counts().to_dict()}")
print(f"cuerdas sin nudos: {(d.nudos.isna()).sum()}; valor>0 sin nudos: {((d.nudos.isna())&(d.valor>0)).sum()}")
print(f"colores de las sin-nudos: {d[d.nudos.isna()].color.value_counts().to_dict()}")

# ---------- T1 colgante = suma subsidiarias ----------
sub = d[d.nivel > 0]
t1_hit = 0; t1_tot = 0
for _, r in d[(d.nivel == 0)].iterrows():
    ch = sub[sub.padre == r.cuerda]
    if len(ch) > 0:
        t1_tot += 1
        if r.valor == ch.valor.sum():
            t1_hit += 1
print(f"\n=== T1 colgante==suma(subsidiarias) === hits {t1_hit}/{t1_tot}")

# null T1: barajar valores de subsidiarias entre madres
paren_vals = {r.cuerda: r.valor for _, r in d[d.nivel == 0].iterrows()}
groups = [sub[sub.padre == k].valor.values for k in paren_vals if (sub.padre == k).any()]
allsub = np.concatenate(groups); sizes = [len(g) for g in groups]
null_hits = []
for _ in range(1000):
    rng.shuffle(allsub)
    pos = 0; h = 0
    for k in [k for k in paren_vals if (sub.padre == k).any()]:
        g = allsub[pos:pos+len(sub[sub.padre == k])]; pos += len(g)
        if paren_vals[k] == g.sum(): h += 1
    null_hits.append(h)
null_hits = np.array(null_hits)
p1 = (np.sum(null_hits >= t1_hit)+1)/(1000+1)
print(f"nulo T1: media {null_hits.mean():.2f}, max {null_hits.max()}, p={p1:.3f}")

# ---------- T2 sum cord = suma bloque previo de 6 ----------
h2, idx2 = count_sixsum(vals, N)
nh2 = []
for _ in range(1000):
    v = vals.copy(); rng.shuffle(v)
    nh2.append(count_sixsum(v, N)[0])
nh2 = np.array(nh2)
p2 = (np.sum(nh2 >= h2)+1)/(1000+1)
print(f"\n=== T2 cord==suma 6 colgantes previos === real {h2}, nulo media {nh2.mean():.2f} max {nh2.max()}, p={p2:.4f}")
print(f"  posiciones: {[int(p.iloc[i].orden) for i in idx2]} (nombres: {[p.iloc[i].cuerda for i in idx2]})")

# T2b: cualquier bloque 2..8
h2b = count_anysum(vals, N)
nh2b = []
for _ in range(1000):
    v = vals.copy(); rng.shuffle(v)
    nh2b.append(count_anysum(v, N))
nh2b = np.array(nh2b)
p2b = (np.sum(nh2b >= h2b)+1)/(1000+1)
print(f"T2b cord==suma de algun bloque contiguo (2..8) previo: real {h2b}, nulo {nh2b.mean():.1f}+-{nh2b.std():.1f}, p={p2b:.4f}")

# ---------- T3 valores repetidos ----------
h3 = count_dups(vals)
nh3 = []
for _ in range(1000):
    v = vals.copy(); rng.shuffle(v)
    nh3.append(count_dups(v))
nh3 = np.array(nh3)
p3 = (np.sum(nh3 <= h3)+1)/(1000+1)   # menor repeticion = mas estructura? dos colas
print(f"\n=== T3 valores repetidos (pares) === real {h3}, nulo {nh3.mean():.1f}+-{nh3.std():.1f}, p(<=)={p3:.3f}")

# ---------- T4 progresion aritmetica local ----------
h4 = ratio_const(vals)
nh4 = []
for _ in range(1000):
    v = vals.copy(); rng.shuffle(v)
    nh4.append(ratio_const(v))
nh4 = np.array(nh4)
p4 = (np.sum(nh4 >= h4)+1)/(1000+1)
print(f"=== T4 tripletas con diferencias iguales === real {h4}, nulo {nh4.mean():.1f}+-{nh4.std():.1f}, p={p4:.3f}")

# ---------- T5 periodicidad de color ----------
def col_period(cols, period):
    return sum(1 for i in range(len(cols)-period) if cols[i] == cols[i+period])
cols = p.color.map(lambda x: str(x).split('/')[0].split(':')[0].split('(')[0]).values
print("\n=== T5 periodos de color (aciertos color[i]==color[i+p]) ===")
for per in [1, 2, 3, 5, 6, 7, 12, 18]:
    real = col_period(cols, per)
    nh = []
    for _ in range(1000):
        v = cols.copy(); rng.shuffle(v)
        nh.append(col_period(v, per))
    nh = np.array(nh)
    pv = (np.sum(nh >= real)+1)/(1000+1)
    print(f"  p={per:2d}: real {real:3d}, esperado {nh.mean():.1f}, p={pv:.4f}")

# ---------- union R vs U por posicion en el grupo ----------
d['col1'] = d.color.map(lambda x: str(x).split('/')[0].split(':')[0].split('(')[0])
sub_col = d.set_index('cuerda')
print("\n=== union segun posicion en run de 6 ===")
pos_union = defaultdict(list)
for col, s, e in size6:
    for j in range(6):
        pos_union[j].append(d[(d.orden == p.iloc[s+j].orden)].union.values[0])
for j in range(6):
    from collections import Counter
    print(f"  pos{j}: {dict(Counter(pos_union[j]))}")
