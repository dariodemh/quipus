# -*- coding: utf-8 -*-
"""
07_materiales.py -- fibra, grosor, canutos: cobertura y sesgo de registro.
Y prueba clave: ¿la firma identica es mas comun de lo que predicen las marginales?
"""
import os, json, sqlite3
import numpy as np, pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
f = pd.read_csv(os.path.join(AQUI, 'firma_quipu.csv'))
o = pd.read_csv(os.path.join(AQUI, 'cuerdas_okr.csv'))
res = {}

# ---------- fibra ----------
print('== FIBRA (OKR, 612 quipus con cuerdas) ==')
print('cuerdas: CN %d, CL %d, otros %d, sin dato %d' % (
    (o.FIBER == 'CN').sum(), (o.FIBER == 'CL').sum(),
    o.FIBER.isin(['W','H','CC','V','AH']).sum(), o.FIBER.isna().sum()))
qcov = o.groupby('kfg').FIBER.apply(lambda s: s.notna().mean())
print('cobertura de fibra por quipu: %.0f%% con 0%%, %.0f%% con 100%%' % (
    100*(qcov == 0).mean(), 100*(qcov == 1).mean()))
print('distribucion de la cobertura (deciles):', np.round(np.percentile(qcov, [0,25,50,75,90,100]), 2))
print('\ncobertura por transcriptor (fraccion de cuerdas con fibra):')
print(o.groupby('CREATED_BY').FIBER.apply(lambda s: s.notna().mean()).round(3).to_string())
res['fibra'] = dict(cn=int((o.FIBER=='CN').sum()), cl=int((o.FIBER=='CL').sum()),
                    sin=int(o.FIBER.isna().sum()),
                    q0=float((qcov==0).mean()), q1=float((qcov==1).mean()))

# ---------- grosor ----------
print('\n== GROSOR (OKR) ==')
print('cuerdas con grosor exactamente 0: %d de %d (%.1f%%)' % (
    (o.THICKNESS == 0).sum(), len(o), 100*(o.THICKNESS == 0).mean()))
nz = o[o.THICKNESS > 0].THICKNESS
print('no-cero: n=%d media %.3f mediana %.3f p95 %.3f max %.2f' % (
    len(nz), nz.mean(), nz.median(), nz.quantile(.95), nz.max()))
print('dentro de quipu (solo quipus con >=5 no-cero): variacion del grosor')
g = o[o.THICKNESS > 0].groupby('kfg').THICKNESS
cv = (g.std()/g.mean()).dropna()
print('  CV mediano = %.3f; %% de quipus con CV<0.15 = %.0f%% (n=%d)' % (
    cv.median(), 100*(cv < .15).mean(), len(cv)))
res['grosor'] = dict(frac_cero=float((o.THICKNESS == 0).mean()), cv_med=float(cv.median()))

# ---------- firma identica vs marginales ----------
print('\n== FIRMA IDENTICA: observado vs esperado por marginales independientes ==')
CAT = ['eje_tors','eje_ndS','eje_union','eje_term']
d = f.dropna(subset=CAT)
p_id = 0.0
for c in CAT:
    p = d[c].value_counts(normalize=True).values
    p_id += 0  # placeholder
    print('  %-10s %s  sum p^2 = %.3f' % (c, d[c].value_counts(normalize=True).round(3).to_dict(), (p**2).sum()))
p_id = np.prod([ (d[c].value_counts(normalize=True).values**2).sum() for c in CAT])
obs = (d.groupby(CAT).size().pow(2).sum() - len(d)) / (len(d)*(len(d)-1))
print('  P(par con firma identica): observado %.3f | esperado si los ejes son independientes %.3f' % (obs, p_id))
res['firma_identica'] = dict(obs=float(obs), esperado=float(p_id), n=int(len(d)))

# ---------- copias: firma identica ----------
pares = pd.read_csv(os.path.join(RAIZ, 'analisis', '14_copias', 'pares_resumen.csv'))
fx = f.set_index('kfg')
cop = pares[pares.tipo == 'copia']
ident = 0; n = 0
for _, r in cop.iterrows():
    if r.A in fx.index and r.B in fx.index:
        a, b = fx.loc[r.A], fx.loc[r.B]
        if all(pd.notna(a[c]) and pd.notna(b[c]) for c in CAT):
            n += 1
            ident += int(all(a[c] == b[c] for c in CAT))
print('\n  copias con firma identica en los 4 ejes: %d/%d (%.0f%%) vs %.0f%% del corpus' % (
    ident, n, 100*ident/max(n,1), 100*obs))
res['copias_identicas'] = dict(id=ident, n=n)

# ---------- canutos ----------
print('\n== CANUTOS ==')
print('quipus con canutos (OKR): %d; con >=1 cuerda envuelta: %d' % (
    int(f.canuto_frac.notna().sum()), int((f.canuto_frac > 0).sum())))
print(f[f.canuto_frac > 0].groupby('pref').size().to_string())
json.dump(res, open(os.path.join(AQUI, 'res_07.json'), 'w'), indent=1)
