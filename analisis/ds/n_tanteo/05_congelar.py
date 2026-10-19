# -*- coding: utf-8 -*-
"""Congela las reglas que pasaron exploracion. Se escribe ANTES de tocar confirmacion."""
import pandas as pd
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

P278 = [13.5, 13.6, 8.7, 10.7, 11.6, 12.5, 12.4, 8.7, 8.3]  # % medios por columna, 17 filas explore UR278

rows = [
 dict(id='H06', variante='UR275', congelada=True,
      regla='registro = cabecera == suma(cuerdas no cabecera), exacto; mitad confirmar',
      parametros='cuota=47; exacto',
      criterio='p_perm<0,05 con cabeceras barajadas'),
 dict(id='H06', variante='UR269', congelada=True,
      regla='registro = cabecera == suma(cuerdas no cabecera), exacto; mitad confirmar',
      parametros='cuota modal; exacto',
      criterio='p_perm<0,05 con cabeceras barajadas'),
 dict(id='H07', variante='UR278', congelada=True,
      regla='celda_ij = total_i * P_j / 100, P congelado de exploracion; MAE por celda en confirmar',
      parametros='P=' + str(P278),
      criterio='MAE < novenos iguales y p_perm<0,05 con columnas barajadas por fila'),
 dict(id='H16', variante='UR275', congelada=True,
      regla='|cabecera - suma(resto)|/cabecera < 0,05; mitad confirmar',
      parametros='umbral=0,05; cuota=47',
      criterio='p_perm<0,05 con destinos barajados entre registros'),
 dict(id='H16', variante='UR269', congelada=True,
      regla='|cabecera - suma(resto)|/cabecera < 0,05; mitad confirmar',
      parametros='umbral=0,05',
      criterio='p_perm<0,05 con destinos barajados entre registros'),
 dict(id='H09', variante='escalera', congelada=False,
      regla='triple 2433->2533->2633, paso +100',
      parametros='un solo triple',
      criterio='no confirmable con n=1; queda especulativo'),
 dict(id='H08', variante='UR278', congelada=False,
      regla='rho perfil explore vs confirm',
      parametros='se elimina: habria usado confirmacion para explorar',
      criterio='no cuenta como confirmacion'),
]
pd.DataFrame(rows).to_csv('ds/n_tanteo/congeladas.csv', index=False)
print(pd.DataFrame(rows)[['id','variante','congelada']].to_string(index=False))
