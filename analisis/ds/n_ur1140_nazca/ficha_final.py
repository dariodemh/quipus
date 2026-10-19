"""Genera ficha7.csv (ficha canonica de UR1140) y resumen_pruebas.csv."""
import re, numpy as np, pandas as pd
from pathlib import Path
from collections import Counter
from scipy.stats import binomtest

OUT = Path(__file__).resolve().parent
DAT = OUT.parents[1] / 'datos'
c = pd.read_csv(DAT / 'cuerdas.csv', low_memory=False).drop_duplicates(['kfg', 'cuerda'])
c['v'] = np.where(c.nudos.notna() & (c.nudos.astype(str).str.strip() != ''), c.valor, np.nan)
c['col'] = c.color.fillna('?').astype(str).map(lambda s: re.sub(r'\([^)]*\)', '', s).strip())


def recs(k):
    d = c[(c.kfg == k) & (c.nivel == 0)].sort_values('orden')
    out = []
    for g, dd in d.groupby('grupo', sort=False):
        if len(dd) != 9:
            continue
        cols = list(dd.col); cnt = Counter(cols); maj, nmaj = cnt.most_common(1)[0]
        mix = tuple(i + 1 for i, x in enumerate(cols) if x != maj)
        if nmaj != 7:
            continue
        out.append(dict(g=int(g), mix=mix, v=dd.v.to_numpy(float)[np.array(cols) == maj]))
    return out


def canon(k):
    M = []
    for x in recs(k):
        if np.isnan(x['v']).any():
            continue
        M.append(x['v'] if x['mix'][-1] < 5 else x['v'][::-1])
    return np.array(M)


def prof(M):
    P = []
    for r in M:
        x = np.log10(r + 1)
        P.append((x - x.mean()) / x.std(ddof=0) if np.ptp(x) > 0 else x * 0)
    return np.mean(P, 0)


M = canon('UR1140')
f = prof(M)
raw = M.mean(0)
med = np.median(M, 0)
# sub-fichas directas (sin canonicalizar)
R = recs('UR1140')
t34 = np.array([x['v'] for x in R if x['mix'] == (3, 4) and not np.isnan(x['v']).any()])
t67 = np.array([x['v'] for x in R if x['mix'] == (6, 7) and not np.isnan(x['v']).any()])

nota = {
    1: 'maximo en 44/45 registros de 4 quipus; adyacente al par marcador',
    2: 'minimo en 33/45; profundo en UR1140/UR1136, no en UR223/HP056',
    3: 'sin perfil compartido entre quipus (campos 3-7)',
    4: 'sin perfil compartido entre quipus (campos 3-7)',
    5: 'sin perfil compartido entre quipus (campos 3-7)',
    6: 'sin perfil compartido entre quipus (campos 3-7)',
    7: 'sin perfil compartido entre quipus (campos 3-7)',
}
comp = {1: 'si', 2: 'parcial', 3: 'no', 4: 'no', 5: 'no', 6: 'no', 7: 'no'}
F = pd.DataFrame({'posicion': np.arange(1, 8), 'perfil_canonico_z': np.round(f, 3),
                  'media_aritmetica': np.round(raw, 1), 'mediana': med.astype(int),
                  'perfil_tipo_34_z': np.round(prof(t34), 3),
                  'perfil_tipo_67_z': np.round(prof(t67), 3),
                  'compartido_con_UR1136': [comp[i] for i in range(1, 8)],
                  'nota': [nota[i] for i in range(1, 8)]})
F.to_csv(OUT / 'ficha7.csv', index=False)
print(F.to_string(index=False))

# resumen de pruebas clave
mx = M.argmax(1) + 1
S = pd.DataFrame([
    dict(prueba='UR1140 15 rachas de 7: eta2', valor=0.4236, p=0.0001, nota='reproduce n_plantillas 0.42'),
    dict(prueba='UR1140 15 rachas de 7: rho medio', valor=0.412, p=0.0001, nota='nulo: permutar dentro de racha'),
    dict(prueba='UR1140 grupos de 9, 7 campos: eta2', valor=0.274, p=0.0001, nota='unidad fisica'),
    dict(prueba='UR1140 canonico: max en campo 1', valor=len(M), p=binomtest(int((mx == 1).sum()), len(M), 1 / 7, alternative='greater').pvalue,
         nota=f'{int((mx == 1).sum())}/{len(M)}; binomial anti-conservador por clustering'),
    dict(prueba='4 quipus: max en campo 1', valor=44, p=4.2e-4, nota='44/45; 4/4 quipus (1/7)^4'),
    dict(prueba='UR1136 perfil canonico total', valor=0.960, p=0.0003, nota='Holm 5=0.0009; Holm 651=0.195'),
    dict(prueba='UR1136 campos 3-7', valor=-0.319, p=0.697, nota='no comparte el medio de la ficha'),
    dict(prueba='UR223 perfil canonico total', valor=0.883, p=0.0057, nota='Holm 5=0.011; Holm 651=1.0'),
    dict(prueba='HP056 perfil canonico total', valor=0.796, p=0.0186, nota='held-out; Holm 651=1.0'),
    dict(prueba='Santa control positivo', valor=5 / 6, p=0.0005, nota='5/6 con p<=0.0005; 6 campos, no 7'),
])
S.to_csv(OUT / 'resumen_pruebas.csv', index=False)
print('\nescritos ficha7.csv y resumen_pruebas.csv')
