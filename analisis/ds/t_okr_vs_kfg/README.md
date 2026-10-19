# README — auditoría KFG vs OKR

Carpeta: `analisis/ds/t_okr_vs_kfg/`

## Orden de ejecución

Los scripts se ejecutan en este orden (todos desde esta carpeta). Escriben en `salidas/`.

1. `01_mapeo.py` — enlaza quipus KFG ↔ OKR (`quipus.csv.okr` / `INVESTIGATOR_NUM`) y genera nombres jerárquicos de cuerdas.
2. `02_join.py` — reconstruye el valor OKR (suma de `knot.knot_value_type`, con recuperación de vueltas en nudos largos) y une cuerda a cuerda por nombre.
3. `04_descriptivo.py` — categorías de cobertura y concordancia.
4. `05_por_quipu.py` — tasas por quipu (definición amplia).
5. `06_discrepancias.py` — caracterización de las discrepancias de valor.
6. `07_atribucion.py` — comparación racimo a racimo KFG vs OKR.
7. `08_por_quipu_final.py` — separa discrepancia de valor (largo coincide) de desalineación estructural.
8. `09_controles.py` — binomial + BH, permutación de prefijos, sensibilidad.
9. `10_extras.py` — cobertura, defectos internos, multiset, nulo del umbral 5 %.
10. `11_final.py` — cifras finales con/sin exclusiones.
11. `12_tabla_entrega.py` — tabla de quipus >5 % con causa y correcciones de metadatos.

`03_sensibilidad_mapeo_largo.py` es una exploración descartada: emparejar cuerdas por largo
dentro de cada grupo de hermanos falla cuando muchas cuerdas comparten largos casi iguales
(baja la concordancia de 98 % a 82 %). Se conserva como evidencia de que el mapeo por
nombre jerárquico es superior. **No se usa para las cifras finales.**

## Salidas principales

- `salidas/join_cuerdas.csv` — una fila por cuerda KFG emparejada por nombre.
- `salidas/por_quipu.csv`, `salidas/por_quipu_final.csv` — tasas por quipu.
- `salidas/quipus_mas_5pct.csv` — tabla de entrega (23 quipus + notas).
- `salidas/correcciones_kfg.csv` — 4 registros KH con número desplazado.
- `salidas/discrepancias_valor.csv`, `salidas/atribucion.csv` — detalle.

## Requisitos

Python 3.13, pandas, numpy, scipy. Semilla fija `20261018`.
