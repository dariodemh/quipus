"""UR1032 — pares (5 azul / 3 blanco), igualdades de suma, nulo, direcciones de nudo."""
import pandas as pd, numpy as np, re
C = pd.read_csv('analisis/datos/cuerdas.csv')
s = C[C.kfg == 'UR1032'].copy().sort_values('orden').reset_index(drop=True)
col = s[s.nivel == 0].copy()

def ab(c):
    if pd.isna(c): return '?'
    for tok in re.split(r'[^A-Za-z]+', str(c)):
        if tok: return tok[:3]
    return '?'
col['cab'] = col.color.map(ab)
col['size'] = col.groupby('grupo')['grupo'].transform('size')
gsum = col.groupby('grupo').valor.sum()
gsize = col.groupby('grupo').size()

# --- pares (grupo de 5 azul seguido de grupo de 3 blanco) ---
pairs = []
for gid in range(107):
    a, b = gsum[gid], gsum[gid+1]
    sa, sb = gsize[gid], gsize[gid+1]
    if {sa, sb} == {5, 3}:
        pairs.append((gid, gid+1, sa, sb, a, b))
P = pd.DataFrame(pairs, columns=['ga','gb','sa','sb','suma_a','suma_b'])
print('== pares (5,3) adyacentes:', len(P), '==')
eq = (P.suma_a == P.suma_b)
print('sumas iguales:', int(eq.sum()), f'({100*eq.mean():.1f}%)')
print(P.head(40).to_string())

# nulo: barajar valores de colgantes dentro del quipu, 1000x (semilla 0)
rng = np.random.default_rng(0)
vals = col.sort_values('orden').valor.values
obs = eq.sum()
N = 1000
cnt = 0
ga = P.ga.values; gb = P.gb.values; sa = P.sa.values; sb = P.sb.values
order = col.sort_values('orden').grupo.values; sizes = col.groupby('grupo').size().values
for _ in range(N):
    pv = rng.permutation(vals)
    dfp = pd.DataFrame({'grupo': order, 'v': pv})
    gs = dfp.groupby('grupo').v.sum().values
    e = np.sum(gs[ga] == gs[gb])
    if e >= obs: cnt += 1
print(f'\nNULO par-sum-equal: obs={obs}/{len(P)}  p_emp={cnt/N:.3f}')

# --- direcciones de nudo S/Z desde nudos ---
def dirs(nudos):
    if pd.isna(nudos): return []
    return re.findall(r'[SZU]\)', str(nudos))
S = s.nudos.dropna().map(lambda n: str(n).count('S)'))
Z = s.nudos.dropna().map(lambda n: str(n).count('Z)'))
U = s.nudos.dropna().map(lambda n: str(n).count('U)'))
print('\n== direccion de nudo (conteo total) ==')
print('S:', int(S.sum()), 'Z:', int(Z.sum()), 'U:', int(U.sum()))

# nudos: tipos
tipos = s.nudos.dropna().str.findall(r'\d([SL]|EE|LL|E)').map(lambda x: x[0] if x else '?')
print('tipos nudo:', tipos.value_counts().to_dict())

# cuerdas SIN nudos
sin = s[s.nudos.isna()]
print('\ncuerdas sin nudos:', len(sin), '| de ellas valor!=0:', int((sin.valor!=0).sum()))
print('sin nudos por nivel:', sin.nivel.value_counts().to_dict())
