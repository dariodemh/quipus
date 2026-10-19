# -*- coding: utf-8 -*-
"""UR001. Aritmetica interna + controles nulos (permutacion de valores, 1000x, semilla 0).
Unidad = quipu unico; los tests a nivel de cuerda usan permutacion dentro del quipu."""
import pandas as pd, numpy as np, json

D = 'analisis/datos/'
d = pd.read_csv(D+'cuerdas.csv')
r = d[d.kfg=='UR001'].copy().sort_values('orden').reset_index(drop=True)
rng = np.random.default_rng(0)
NPERM = 1000

# --- jerarquia: madre directa e hijos ---
val = dict(zip(r.cuerda, r.valor))
has_knot = dict(zip(r.cuerda, r.nudos.notna()))
padre = dict(zip(r.cuerda, r.padre))

# hijos directos
children = {}
for c,p in padre.items():
    if isinstance(p,str):
        children.setdefault(p, []).append(c)

def desc_all(name):
    out=[]; stack=list(children.get(name,[]))
    while stack:
        x=stack.pop(); out.append(x); stack+=children.get(x,[])
    return out

# ============ TEST 1: madre = suma de hijas directas ============
def test_mother_sum(use_all=False):
    hits=0; ev=0; details=[]
    for c in r.cuerda:
        ch = desc_all(c) if use_all else children.get(c,[])
        if not ch: continue
        if not has_knot.get(c, False):  # madre sin nudos -> no evaluable
            continue
        # solo evaluable si TODAS las hijas tienen nudos (si no, suma incompleta)
        if not all(has_knot.get(x,False) for x in ch): continue
        ev+=1
        s=sum(val[x] for x in ch)
        if s==val[c]:
            hits+=1; details.append((c,val[c],s))
    return hits, ev, details

for use_all in (False, True):
    h,e,det=test_mother_sum(use_all)
    print(f'TEST1 madre=suma(hijas {"TODAS" if use_all else "directas"}): {h}/{e} exactas ({100*h/max(e,1):.1f}%)')
    if det: print('   aciertos:', det[:10])

# ============ TEST 2: alguna cuerda = suma de su grupo ============
roups = r[r.nivel==0].groupby('grupo')['valor'].sum() if False else None
grp_pendants = r[r.nivel==0].groupby('grupo')['cuerda'].apply(list)
grp_sum = r[r.nivel==0].groupby('grupo')['valor'].sum()
# existe una cuerda (de cualquier nivel) cuyo valor == suma de un grupo de colgantes?
allvals = set(r.valor.tolist())
matches = [(gg, int(s)) for gg,s in grp_sum.items() if s in allvals and s>0]
print(f'\nTEST2 sumas de grupo ({len(grp_sum)} grupos) que coinciden con algun valor del quipu: {len(matches)}')
print('   ejemplos:', matches[:8])

# ============ TEST 3: valores repetidos ============
vc = r[r.valor>0].valor.value_counts()
rep = vc[vc>1]
print(f'\nTEST3 valores repetidos: {rep.sum()} cuerdas en {len(rep)} valores distintos')
print('   top:', rep.head(8).to_dict())

# ============ TEST 4: proporciones constantes entre cuerdas de un grupo ============
# para cada madre con >=2 hijas con valor>0, razones entre primera y siguientes
ratios=[]
for c,ch in children.items():
    vs=[val[x] for x in ch if has_knot.get(x,False) and val[x]>0]
    if len(vs)>=2:
        base=vs[0]
        for v in vs[1:]:
            if v>0: ratios.append(base/v)
ratios=np.array(ratios)
if len(ratios):
    frac=(ratios==1).mean()
    print(f'\nTEST4 razones hija1/hijaK (n={len(ratios)}): fraccion ==1: {frac:.2f}; mediana {np.median(ratios):.2f}')

# ============ TEST 5: patrones de color ============
def color_runs(seq):
    runs=0
    for i in range(1,len(seq)):
        if seq[i]!=seq[i-1]: runs+=1
    return runs
pend = r[r.nivel==0].sort_values('orden')
cols = pend.color.tolist()
obs_runs = color_runs(cols)
# nulo: barajar colores de colgantes
null_runs=[]
arr=np.array(cols)
for _ in range(NPERM):
    null_runs.append(color_runs(rng.permutation(arr)))
null_runs=np.array(null_runs)
p_col = (np.sum(null_runs<=obs_runs)+1)/(NPERM+1)
print(f'\nTEST5 runs de color en colgantes: obs={obs_runs}, nulo media={null_runs.mean():.0f}, p(<=obs)={p_col:.3f}')

# ============ TEST 6: alternancia grupo grande vs color/serie ============
# ? ya cubierto

# ============ TEST 7: nulo global de la "aritmetica de hijas" ============
# barajar valores entre TODAS las cuerdas del quipu y recontar TEST1
obs_h, obs_e, _ = test_mother_sum(False)
vals_all = r.valor.values.copy()
nullhits=[]
for _ in range(NPERM):
    perm = rng.permutation(vals_all)
    vmap = dict(zip(r.cuerda, perm))
    h=0;e=0
    for c in r.cuerda:
        ch=children.get(c,[])
        if not ch or not has_knot.get(c,False): continue
        if not all(has_knot.get(x,False) for x in ch): continue
        e+=1
        if sum(vmap[x] for x in ch)==vmap[c]: h+=1
    nullhits.append(h)
nullhits=np.array(nullhits)
p_m = (np.sum(nullhits>=obs_h)+1)/(NPERM+1)
print(f'\nTEST7 nulo madre=suma(hijas): obs={obs_h} (de {obs_e}); nulo max={nullhits.max()} media={nullhits.mean():.2f}; p={p_m:.3f}')

res=dict(test1_directas=[int(obs_h),int(obs_e)], test1_todas=None,
         test2_grupos_coinciden=len(matches), test3_repetidos=int(rep.sum()),
         test5_color_runs=dict(obs=int(obs_runs),null=float(null_runs.mean()),p=float(p_col)),
         test7_p=float(p_m))
json.dump(res, open('analisis/ds/k_UR001/resultados_aritmetica.json','w'), indent=1)
print('\n[guardado resultados_aritmetica.json]')
