# Verificación del ensayo, noviembre de 2026

Entre el 9 y el 10 de noviembre de 2026 se revisó el ensayo `articulo/` afirmación por afirmación. La regla fue: el ensayo solo dice lo que se puede probar con los datos del repositorio o con una fuente que tenemos a la mano. Lo demás se quitó o se reescribió para decir solo lo probado.

La revisión la hicieron agentes de IA (Claude), dirigidos por una persona. Ningún agente vio los objetos.

## Cómo se hizo

Cada afirmación recibió un veredicto con su prueba:

- **RECOMPUTED:** se recalculó desde `analisis/datos/cuerdas.csv`, `khipu.db` o los datos del Khipu Field Guide.
- **STORED:** la cifra está en la salida guardada de un script del repositorio. Después se volvieron a correr esos scripts (ver «Recálculo»).
- **SOURCE:** la afirmación sobre una publicación se encontró en el texto de esa publicación, con página y cita.
- **INFORME-ONLY, UNVERIFIED, WRONG, IMPRECISE:** sin respaldo suficiente, falsa o dicha de más. Todas se corrigieron o se quitaron.

Una frase que solo aparece en un informe, en la bitácora o en una ficha de lectura no contó como prueba.

## Archivos

| Archivo | Qué cubre |
|---|---|
| `v1.md` | Introducción, datos, método y prueba a ciegas |
| `v2.md` | Inkawasi, hallazgos 1 y 2 |
| `v3.md` | Hallazgos 3 a 5 |
| `v4.md` | Hallazgos 6 a 8 |
| `v5.md` | Hallazgos 9 a 12 |
| `v6.md` | Propuestas que los datos no apoyan, correcciones, lector, cómo se hizo |
| `v7.md` | Referencias, créditos de imágenes y citas de datos |
| `c1.md` | Auditoría de las correcciones aplicadas y secciones que la primera pasada no cubrió |
| `fuentes.md` | Lo que dicen las fuentes que se releyeron (Urton 2005, Florio y Overmann 2025, Databook de los Ascher, carga y fanega, densidad del maní) |
| `aplicado.md` | Qué se cambió en el ensayo, fila por fila |

Los números de línea de estas tablas son los de `articulo/fuente/plantilla.html` en el momento de la revisión; el texto cambió después, así que sirven para ubicar la sección, no la línea exacta. Las rutas que empiezan por `quipu/` son del repositorio de trabajo, que no es público, y `(temporal)/` es una carpeta de trabajo que no se conserva.

## Qué cambió en el ensayo

- **Atribuciones.** El Khipu Field Guide lo edita y mantiene Ashok Khosla. Las copias AS38 ≈ UR122 y AS84 ≈ copia de Lima están en Chirinos (2010). La jerarquía de tres niveles de AS38 (KH0049) está en el Databook de los Ascher (1978). Los tríos de color del conjunto UR053 y sus proporciones aproximadas están en Chirinos (2026).
- **Hallazgo 7** pasó a ser un caso publicado que el método recupera.
- **Hallazgo 5.** La carga de 23 kg no tenía fuente. Con las unidades que sí la tienen (fanega de unos 56 litros; carga de media fanega en las transcripciones de Charcas), el orden de magnitud para la tabla UR278 es de 500 a 950 toneladas.
- **Prueba a ciegas.** El agente encontró por su cuenta la primera etapa de la cadena (UR270 a UR278). El paso al libro salió en una prueba dirigida. La línea base acierta el 14,4 % de las 597 cuerdas escondidas y el 40 % de las 68 que el agente eligió predecir.
- **Bambamarca.** El −0,87 era la tendencia de Bambamarca con la posición, no su parecido con UR278. Entre los dos perfiles la correlación es +0,64 (p = 0,07). Queda como conjetura.
- **Niveles de evidencia.** Los hallazgos 3, 6, 8 y 10 bajaron de «indicio fuerte» a «indicio» porque no tenían un segundo análisis separado.
- **Cifras corregidas.** UR040 (26 de 31) y UR167 (30 de 35); UR053D (24 de 24); ruido de lectura (0 % a 12 %); la descripción de FitzPatrick (2024); la cita de Locke.
- **Quitado por falta de respaldo.** Los títulos de trabajos no leídos, las obras que no tenemos (Ascher y Ascher 1981, Pereyra Sánchez 2011), «entre el 14 % y el 20 % tiene copia», «un silabario necesita 60 a 120 signos» y varias afirmaciones sobre el orden en que se hizo el trabajo.

## Recálculo

Se volvieron a correr, en una copia fuera del repositorio, los scripts que producen los valores p y los barridos que cita el ensayo: unos 120 scripts de las carpetas 05, 08, 13, 14, 16, 18, 19, 20, 23, 26, 28, 30, 33 y 34, y de `ds/` (`n_color_posicion`, `n_fuera_muestra`, `n_parssinen`, `n_puruchuco_pacha`, `n_santa_padron`, `t_cuerdas_superiores`), además de `lector/lector.py --todos`.

- Las salidas recalculadas coinciden con las guardadas. Las únicas diferencias son tiempos de ejecución, espacios, orden de filas y un valor auxiliar que cambia en el cuarto decimal; ninguna toca una cifra del ensayo.
- La batería de calendarios (4 000 simulaciones) reproduce 5 de 111 pruebas con p < 0,05 y ninguna tras Holm o Benjamini-Hochberg.
- El barrido entre quipus de `30_frontera_estructura/02_entre.py` tarda cerca de una hora y reproduce sus salidas.
- `ds/n_color_posicion/agregados.csv` estaba desactualizado respecto de su script; se reemplazó por el recalculado. No lo usa ninguna cifra del ensayo.

Dos scripts de `23_sivan_ur193/` (`control.py` y `control_ur039_ur112.py`) necesitan fuentes que no se distribuyen. Se corrieron con ellas en local y reproducen sus resultados; en el repositorio público se detienen con un mensaje que lo explica. `control_exacto.py` sí corre con lo publicado.

## Arreglos de reproducibilidad hechos en esta revisión

- `05_etnohistoria/calendario.py` y `calendario_holm_total.py` buscaban sus archivos en la carpeta de trabajo y fallaban al correrse desde la raíz; ahora los buscan junto al script.
- Faltaba `analisis/n_plantillas/puntuaciones.csv`, que necesita `28_atlas_generos/01_matriz.py`; se añadió.

## Lo que esta revisión no resuelve

- Todo descansa en las transcripciones publicadas. En Inkawasi, las dos bases vienen de la misma lectura.
- La búsqueda de antecedentes cubre lo que leímos. «Nuevo» quiere decir que no aparece ahí.
- Las posiciones del mapa del ensayo son aproximadas; no tenemos una fuente de coordenadas.
