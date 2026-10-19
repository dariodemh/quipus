"""Crea una copia deduplicada de cuerdas.csv (UR196 y MM007_AN002 tienen filas repetidas).
Conserva la fila con nudos no vacios.
"""
import pandas as pd
C=pd.read_csv('analisis/datos/cuerdas.csv',dtype={'nudos':str,'color':str,'notas':str})
print('original',len(C),'duplicadas',C.duplicated(['kfg','cuerda']).sum())
C['_nn']=C.nudos.fillna('').str.strip().ne('')
C=C.sort_values(['kfg','cuerda','_nn']).drop_duplicates(['kfg','cuerda'],keep='last').drop(columns='_nn')
C.to_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv',index=False)
print('dedup',len(C))
