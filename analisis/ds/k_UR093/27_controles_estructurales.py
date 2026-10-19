# -*- coding: utf-8 -*-
"""UR093: controles estructurales (modulo 8, color 6/7) con nulos explicitos."""
import pandas as pd, numpy as np, re
C = pd.read_csv('analisis/datos/cuerdas.csv', low_memory=False)
u = C[C.kfg == 'UR093'].copy().sort_values('orden').reset_index(drop=True)
u['valor'] = u.valor.fillna(0).astype(int)
l1 = u[u.nivel == 1].copy(); l1['pos'] = l1.groupby('padre').cumcount() + 1
l0 = u[u.nivel == 0]
mods = l1.groupby('padre').size()
print('colgantes con subs', len(mods), '| distribucion', mods.value_counts().sort_index().to_dict())

rng = np.random.default_rng(0)
# Nulo A: repartir 956 subsidiarias entre 121 colgantes al azar (multinomial)
tot = int(mods.sum()); k = len(mods); n8_obs = int((mods == 8).sum())
sim = []
for _ in range(1000):
    # composicion uniforme de tot en k partes
    cuts = np.sort(rng.choice(np.arange(1, tot), k - 1, replace=False))
    parts = np.diff(np.concatenate([[0], cuts, [tot]]))
    sim.append((parts == 8).sum())
sim = np.array(sim)
print(f'Nulo A (reparto aleatorio): obs={n8_obs}/121 con 8; nulo media={sim.mean():.2f}, max={sim.max()}, p={(1+(sim>=n8_obs).sum())/1001:.4f}')

# Nulo B: colores de subsidiarias permutados entre todas las subsidiarias
def base(c): return str(c).split('(')[0] if pd.notna(c) else 'NA'
def fam(c):
    c = base(c); c = re.split(r'[:/\-]', c)[0]
    return 'verde' if c in ('BG','VB','GG','LG','TG','VG','YG','GL','LC','BL','PB','0G') else c
l1['fam'] = l1.color.map(fam)
# pos6 verde en 111/114
fam_all = l1.fam.values; pos_all = l1.pos.values
m6 = pos_all == 6; m7 = pos_all == 7
obs6 = int((fam_all[m6] == 'verde').sum()); n6 = int(m6.sum())
print(f'pos6 verde: {obs6}/{n6}; tasa global verde en subsidiarias: {(l1.fam=="verde").mean():.3f}')
sim6 = []
for _ in range(1000):
    f = rng.permutation(fam_all)
    sim6.append(int((f[m6] == 'verde').sum()))
sim6 = np.array(sim6)
print(f'  nulo B: media={sim6.mean():.1f}, max={sim6.max()}, p={(1+(sim6>=obs6).sum())/1001:.4f}')
# pos7 barber pole (contiene ':')
bar_all = l1.color.astype(str).str.contains(':').values
obs7 = int(bar_all[m7].sum()); n7 = int(m7.sum())
print(f'pos7 barber pole: {obs7}/{n7}; tasa global: {bar_all.mean():.3f}')
sim7 = []
for _ in range(1000):
    f = rng.permutation(bar_all)
    sim7.append(int(f[m7].sum()))
sim7 = np.array(sim7)
print(f'  nulo B: media={sim7.mean():.1f}, max={sim7.max()}, p={(1+(sim7>=obs7).sum())/1001:.4f}')

# Nulo C: el maximo del grupo cae en las 3 primeras posiciones (8/12)
groups = {g: grp.cuerda.tolist() for g, grp in l0.groupby('grupo')}
V = dict(zip(u.cuerda, u.valor))
obs = sum(1 for cs in groups.values() if int(np.argmax([V[c] for c in cs])) < 3)
simc = []
for _ in range(1000):
    gs = []
    for cs in groups.values():
        vv = rng.permutation([V[c] for c in cs])
        gs.append(int(np.argmax(vv)) < 3)
    simc.append(sum(gs))
simc = np.array(simc)
print(f'max en top-3 por grupo: obs={obs}/12; nulo media={simc.mean():.2f}, max={simc.max()}, p={(1+(simc>=obs).sum())/1001:.4f}')

# Nulo D: color de colgante y valor (asociacion)
ct = pd.crosstab(l0.color.map(lambda c: re.split(r'[:/\-]', base(c))[0]), l0.valor > 0)
print('\ncolgantes: color primario x tiene valor>0 (frecuencias)')
print(ct.to_string())
