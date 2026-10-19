"""Preparación de datos para el análisis de información física (espaciado, nudos, largo).

Salidas (en derived/):
  clusters.parquet  (o pickle)  una fila por racimo de nudos
  cuerdas.pkl                   cuerdas con columnas derivadas
  grupos.pkl                    grupos con gaps
"""
import os, re, pickle
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..', '..', '..'))
DAT = os.path.join(ROOT, 'analisis', 'datos')
OUT = os.path.join(BASE, 'derived')
os.makedirs(OUT, exist_ok=True)

# nTIPO(pos,dir),valor  -- el valor y la coma pueden faltar en algunas celdas
PAT = re.compile(r'^(\d+)([A-Z]+)\(([0-9]+(?:\.[0-9]+)?),([SZU])\)(?:,(-?[0-9.]+))?$')


def parse_nudos(s):
    """Devuelve lista de dicts por racimo."""
    out = []
    if not isinstance(s, str) or not s.strip():
        return out
    for k, part in enumerate(s.split(';')):
        part = part.strip()
        if not part:
            continue
        m = PAT.match(part)
        if not m:
            continue
        n, tipo, pos, direc, val = m.groups()
        out.append(dict(orden_racimo=k, n=int(n), tipo=tipo,
                        pos=float(pos), direccion=direc,
                        valor_racimo=float(val) if val is not None else np.nan))
    return out


def main():
    c = pd.read_csv(os.path.join(DAT, 'cuerdas.csv'))
    g = pd.read_csv(os.path.join(DAT, 'grupos.csv'))

    # ---- cuerdas derivadas ----
    c['n_clusters'] = c.nudos.map(lambda s: len(parse_nudos(s)))
    c['n_nudos_tot'] = c.nudos.map(lambda s: sum(x['n'] for x in parse_nudos(s)))
    c['pos_min'] = c.nudos.map(lambda s: min([x['pos'] for x in parse_nudos(s)], default=np.nan))
    c['pos_max'] = c.nudos.map(lambda s: max([x['pos'] for x in parse_nudos(s)], default=np.nan))
    c['pos_top'] = c.pos_min
    c['cola'] = c.largo - c.pos_max
    c['lead'] = c.pos_min
    c['tiene_nudos'] = c.nudos.notna() & (c.nudos.fillna('').str.strip() != '')
    # color simple / mixto
    def colbase(x):
        if not isinstance(x, str):
            return np.nan
        x = x.strip()
        if any(ch in x for ch in ':-/'):
            return 'MIX'
        return x
    c['color_simple'] = c.color.map(colbase)
    c['logvalor'] = np.log1p(c.valor)

    # ---- clusters ----
    rows = []
    for r in c.itertuples(index=False):
        for x in parse_nudos(r.nudos):
            x.update(kfg=r.kfg, cuerda=r.cuerda, orden=r.orden, nivel=r.nivel,
                     grupo=r.grupo, largo=r.largo, color=r.color)
            rows.append(x)
    cl = pd.DataFrame(rows)

    # ---- grupos con gaps ----
    g = g.sort_values(['kfg', 'grupo']).reset_index(drop=True)
    g['n_pend'] = g.hasta - g.desde + 1
    g['pos_next'] = g.groupby('kfg').pos_cm.shift(-1)
    g['dpos'] = g.pos_next - g.pos_cm          # ancho del grupo + espacio
    g['ultimo'] = g.groupby('kfg').grupo.transform('max') == g.grupo
    # gap: espacio anotado (grupos con >=2 colgantes); para grupos de 1 colgante
    # el ancho es ~0, así que dpos aproxima el hueco
    g['gap'] = np.where(g.n_pend >= 2, g.espacio_cm, g.dpos)
    g['gap'] = g.gap.where(~g.ultimo)
    g['gap_dpos'] = g.dpos.where(~g.ultimo)

    # ---- features por grupo ----
    def agg_grupo(df):
        d = df[df.tiene_nudos]
        return pd.Series(dict(
            n_cuerdas=len(df),
            n_con_nudos=len(d),
            v_sum=d.valor.sum(),
            v_mean=d.valor.mean(),
            logv_mean=d.logvalor.mean(),
            logv_max=d.logvalor.max(),
            ncl_mean=d.n_clusters.mean(),
            ndig_max=d.n_clusters.max(),
            largo_mean=df.largo.mean(),
            color_ent=(-(df.color_simple.value_counts(normalize=True) *
                         np.log(df.color_simple.value_counts(normalize=True))).sum()),
            frac_blanco=(df.color_simple == 'W').mean(),
        ))
    gf = c.groupby(['kfg', 'grupo']).apply(agg_grupo, include_groups=False).reset_index()
    g = g.merge(gf, on=['kfg', 'grupo'], how='left')

    c.to_pickle(os.path.join(OUT, 'cuerdas.pkl'))
    cl.to_pickle(os.path.join(OUT, 'clusters.pkl'))
    g.to_pickle(os.path.join(OUT, 'grupos.pkl'))
    print('cuerdas', c.shape, 'clusters', cl.shape, 'grupos', g.shape)
    print('clusters sin valor', cl.valor_racimo.isna().sum())
    print(cl.tipo.value_counts().head(10).to_dict())


if __name__ == '__main__':
    main()
