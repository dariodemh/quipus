# -*- coding: utf-8 -*-
"""Registro de hipotesis ANTES de probarlas contra explore/confirmar.
Cada fila: id, enunciado, regla exacta, prediccion, n_variantes.
"""
import pandas as pd
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

H = [
 ('H01','H-a dinamica: UR273B es un saldo que se mueve con UR273A',
  'A_i=max(grupo i de UR273A), B_i=max(grupo i de UR273B); para i consecutivos en la misma mitad: B_{i+1}=B_i-A_i-17, B_i+A_i+17, B_i-A_i, B_i+A_i, y las 4 con el signo de la cuota invertido; tolerancia exacta',
  'Si B es saldo y A movimiento, >=3 de ~15 transiciones exactas; si no, ~0',8),
 ('H02','H-a dinamica: UR274B es un saldo que se mueve con UR274A',
  'A_i=max(grupo i de UR274A), B_i=max(grupo i de UR274B); mismas 8 formulas de H01 (cuota 30+17)',
  '>=3 transiciones exactas',8),
 ('H03','H-a libro: las cabeceras de UR275 son un saldo acumulado',
  'H_i=cord 1 del grupo i; N_i=suma(resto)-47; para i consecutivos en la misma mitad: H_{i+1}=H_i+N_i, H_i-N_i, H_i+suma(resto), H_i-suma(resto)',
  '>=5 de ~12 transiciones exactas',4),
 ('H04','H-a libro: las cabeceras de UR269 son un saldo acumulado',
  'Misma regla que H03 sobre grupos consecutivos de UR269 (cuota modal por registro)',
  '>=10 de ~50 transiciones exactas',4),
 ('H05','H-b impuesto: la cuota es proporcional a la cabecera (2 %)',
  'cuota_i (47 en UR275, 208 en UR268, cuota modal 47/46/44/40/25 en UR269) frente a cabecera_i; r de Pearson y r de rangos',
  'Proporcional: r>0,7. Fija: r~0',3),
 ('H06','H-b reparto: cabecera = cuota + resto (el registro es un deposito repartido)',
  'Por registro: cabecera == suma(cuerdas no cabecera), exacto y +-1; UR275, UR266, UR269, UR268',
  'Muchos mas aciertos que el nulo de cabeceras barajadas',8),
 ('H07','H-c las 9 partes son proporciones fijas del total (perfil estable)',
  'Perfil P_j = cuota media de la columna j en las filas de exploracion de UR278 (y UR270); predecir celdas de confirmacion = total_i*P_j; MAE. Comparar con (a) novenos iguales y (b) columnas barajadas',
  'MAE observado menor que el 95 % del nulo de columnas barajadas y que novenos iguales',4),
 ('H08','H-c el orden de magnitud de las 9 columnas se conserva entre mitades',
  'Spearman entre el perfil medio de columnas en exploracion y en confirmacion (UR278, UR270)',
  'rho>0,7; nulo: columnas barajadas en confirmacion',2),
 ('H09','H-d la escalera de copias va UR269 -> UR278 -> UR266/UR275',
  'Triple conocido 2433 (UR269), 2533 (UR278), 2633 (UR266/UR275): cada paso suma 100. Nulo: probabilidad de que 3 valores al azar (uno de cada quipu) formen progresion aritmetica de paso 100',
  'Los 2 pasos exactos; n=1 triple -> solo especulativo',1),
 ('H10','H-e UR277: el cordon grande de cada grupo es la suma de los pequenos (leva/jornales)',
  'Por grupo de UR277 (>=3 colgantes): primer cordon == suma de los demas; exacto y +-1 %',
  '>=8 de ~10 grupos exactos',2),
 ('H11','H-e UR272: el primer cordon de cada grupo es la suma del resto',
  'Por grupo de UR272 (>=3 colgantes): primer cordon == suma de los demas; exacto y +-1 %',
  '>=8 de ~10 grupos exactos',2),
 ('H12','H-e UR276: el colgante es la suma de sus dos subsidiarias',
  'Por registro de UR276: parent == s1+s2 (5 registros)',
  '5 de 5 exactos',1),
 ('H13','H-e UR279: sus 12 colgantes son totales de grupos de otro quipu del monton',
  'Cada valor de colgante de UR279 se busca como suma de grupo (o cabecera) exacta en los otros 13 quipus; contar coincidencias frente a valores barajados',
  '>=3 coincidencias exactas',1),
 ('H14','Control positivo: la celda de UR278 = colgante + subsidiaria de UR270',
  'Para cada grupo de UR270: 9 sumas (colgante+subsidiarias) en orden; buscar la fila de UR278 con >=6/9 celdas +-1; contar grupos con match frente a filas barajadas',
  '>=4 grupos con match (ya publicado: 5)',1),
 ('H15','Control positivo: UR270 y UR278 comparten el mismo perfil de 9 columnas',
  'Correlacion de Spearman entre los perfiles medios de columnas de UR270 y UR278 (todas las filas)',
  'rho>0,7',1),
 ('H16','H-b reparto tolerante: cabecera = cuota + destinos salvo error de transcripcion <5 %',
  'Por registro: |cabecera-(cuota+suma(destinos))|/cabecera < 0,05; UR275, UR266, UR269. Nulo: barajar los valores de destino entre registros del mismo quipu',
  'Fraccion observada mucho mayor que el nulo',3),
]
df = pd.DataFrame(H, columns=['id','enunciado','regla_exacta','predice','n_variantes'])
df['registrada_antes_de_confirmar'] = True
df['momento'] = ['inicial'] * 15 + ['ampliacion']
df.to_csv('ds/n_tanteo/hipotesis.csv', index=False)
print(df[['id','n_variantes','enunciado']].to_string(index=False))
print('TOTAL hipotesis registradas:', len(df), '| variantes:', df.n_variantes.sum())
