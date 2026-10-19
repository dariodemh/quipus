# ¿Está publicado lo de KH0049?

Veredicto: **parcialmente**. Las sumas elementales de KH0049 están publicadas por el Khipu Field Guide como lista algorítmica. No encontramos descripción de la tabla jerárquica de 3 niveles en bloques de 18, de su copia parcial UR122, ni de la discrepancia 15652/15649.

## (a) Qué es KH0049

- OKR (`khipu_main`): KHIPU_ID 1000565, `OKR_NUM` KH0049, investigador **AS038/HP036** (`orig_inv_num` HP036), museo Museo Nacional de Arqueología, Antropología e Historia del Perú (Lima), **MNAAHP3550**, procedencia «Costa Sur». Nota OKR: Ascher y Ascher la describieron en 1978 como AS038 y el registro se acordó con la base. Colección Museo Histórico, 1929. En `quipus.csv` figura como KFG = OKR = KH0049.
- Es decir, no es un número UR: la transcripción es de Ascher (AS038) y de Hyland (HP036). «Nazca» es la lectura de la base: la procedencia registrada es Costa Sur.
- KFG (catálogo KH0049): 7 grupos, 367 cuerdas (108 colgantes, 259 subsidiarias); 21 sumas de Ascher (5 pps, 15 ips, 1 cps); bibliografía Pereyra Sánchez 2011.
- UR122 = KH0362 en OKR: Museum of World Culture, Gotemburgo, 1938.45.0228, procedencia Nazca, transcriptor Urton. KFG le da 3 sumas (1 pps, 2 ips).

## (b) Búsqueda en el repositorio

- `analisis/fuentes_txt/`: ninguna mención de KH0049, UR122, AS038, HP036 ni MNAAHP3550. «Göteborg/Goteborg» aparece solo en la tabla de museos de Urton 2017 (líneas 1136-1138 y 1233-1235; lista de museos), en Nissen et al. 1993 (créditos de Friberg) y en la ficha de Milillo 2023 (otros quipus, 1932.08.0001-2). Ninguna trata 1938.45.0228.
- `docs/fichas/`, `docs/estado_del_arte.md`, `docs/fuentes_sin_datos_abiertos.md`: nada sobre KH0049 ni UR122 (solo recuentos de MNAAHP).
- `papers/` (txt de `papers/web/chu/`): nada.
- Dentro del proyecto solo consta `SINTESIS.md` (línea 54) como «copia entre museos no publicada».

## (c) Búsqueda web

- `khipufieldguide.com/catalog/KH0049.html` y `catalog/KH0362.html`: listan cada uno al otro como «Similar Khipu» (vecinos del catálogo), sin decir que sea copia ni mencionar Gotemburgo, AS038 o HP036. No dan 15652 ni la discrepancia.
- `notebook/fieldmarks/indexed_pendant_sum/html/KH0049.html`: KFG publica **15 sumas indexadas** de KH0049 (valores 1535-27475). Siete son sumas en g1 (g1p1 = g4p1+g5p1+g6p1+g7p1 = 27475; g1p2 = g3p2+g4p2 = 3417; etc.) y ocho en g3 (suman cuerdas de g5, g6, g7). Esto es la tabla jerárquica vista como lista de sumas, sin texto interpretativo, sin descripción en niveles ni en bloques de 18 y sin alusión a UR122. Es salida automática del método de Ascher, no un análisis.
- Pereyra Sánchez 2011 (*Descripción de una muestra de quipus del MNAAHP*, CONCYTEC) es la bibliografía de KFG para los MNAAHP; no pudimos leerlo ni confirmar si cubre MNAAHP3550. Es la fuente publicada más probable.
- Búsquedas sobre «MNAAHP3550», «AS038», «HP036», «1938.45.0228» y «hierarchical khipu column totals Nazca»: sin resultados que mencionen estos objetos. Resultados cercanos, de otros quipus: KH0263/UR028 (Múnich, Nazca; p1 = suma de p2-p4, con off-by-one), KH0235/AS215 (Hood Museum, Nazca; cuerda superior = suma de 6 colgantes), KH0142/UR1127. Es decir, las sumas jerárquicas en quipus nazcas son conocidas en general (Ascher y Ascher; Urton y Brezine para Puruchuco), pero no para este objeto.
- No se consultó Ascher 1978 / *Code of the Quipu* directamente (no accesible); la nota OKR dice que AS038 fue descrito en 1978, así que AS038 puede aparecer en el libro de Ascher y Ascher con sus sumas. Queda por revisar.

## Qué queda como nuevo (según lo encontrado)

1. Que KH0049 es una tabla de **tres niveles en bloques de 18** (B0 = B1+B2 en 14/18; B1 = B3+B4+B5 en 7/18) y su contraste con nulos.
2. Que UR122 (Gotemburgo) es copia parcial (sección del subtotal) con 58 % de cuerdas rotas.
3. Que la discrepancia 15652/15649 está en ambas copias.

## Qué no podemos reclamar

- Las sumas posición a posición en sí: KFG las lista (15 ips). Nuestro aporte es la lectura como tabla jerárquica y la copia.
- Que no haya algo en Ascher y Ascher 1978/1981 o Pereyra Sánchez 2011, no revisados.

Fuentes: <https://www.khipufieldguide.com/catalog/KH0049.html>, <https://www.khipufieldguide.com/catalog/KH0362.html>, <https://www.khipufieldguide.com/notebook/fieldmarks/indexed_pendant_sum/html/KH0049.html>, OKR `khipu.db`.
