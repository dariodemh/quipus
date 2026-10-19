# -*- coding: utf-8 -*-
"""Muestras usadas para la auditoria manual de precision de la taxonomia.

Imprime 12 notas distintas por categoria (semilla 11). La adjudicacion manual
se reporta en informe.md: rota 12/12, reparacion 11/12, envoltura 12/12,
nudo_extra 9/12, objeto 2/3 (el resto son montajes de museo, no objetos
originales).
"""
import os, pandas as pd
AQUI = os.path.dirname(os.path.abspath(__file__))
an = pd.read_csv(os.path.join(AQUI, 'rasgos.csv'))
for c in ['rota', 'reparacion', 'envoltura', 'nudo_extra', 'objeto']:
    d = an.loc[an[c], 'notas'].drop_duplicates()
    print('##', c, len(d))
    for x in d.sample(min(12, len(d)), random_state=11):
        print('  |', str(x)[:105].replace('\n', ' '))
