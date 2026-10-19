# Brief común para los equipos de análisis

Objetivo general: averiguar qué significan los quipus, con evidencia que sobreviva a controles estadísticos.

## Datos (ya preparados, úsalos; no los regeneres)

Raíz del repo: `` (en Bash: `/c/Users/D/Documents/GitHub/quipu`).

- `analisis/datos/cuerdas.csv` — una fila por cuerda (57 818), de los 651 xlsx del Khipu Field Guide (KFG).
  - `kfg`: id del quipu (AS###, UR###, HP###, JC###, QU###, CM###...). `orden`: orden de la cuerda en el quipu (izquierda→derecha, subsidiarias justo después de su madre).
  - `cuerda`: nombre jerárquico (`p12` = colgante 12; `p12s2` = 2.ª subsidiaria de p12; `p12s2s1` ...). `nivel` = 0 colgante, 1 subsidiaria, ... `padre` = nombre de la cuerda madre.
  - `grupo`: índice del grupo de colgantes (los quipus agrupan colgantes con espacios entre grupos); detalle en `grupos.csv`.
  - `valor`: valor decimal decodificado por KFG. **0 con `nudos` vacío = cuerda sin nudos (no es un cero real)**. `alt`: valor alternativo.
  - `nudos`: cadena de racimos de nudos, de arriba (junto al cordón principal) hacia abajo, separados por `;`. Formato `nTIPO(posición_cm,dirección),valor_aportado`. Tipos: S simple, L largo, E figura de ocho, EE, LL... Dirección S/Z/U(desconocida). Ej.: `3S(7.5,U),30;9L(9.0,U),9` = 3 simples en decenas + largo de 9 vueltas en unidades = 39.
  - `color`: código Ascher (W blanco, AB marrón claro, MB marrón medio, KB marrón oscuro, YB, B, LB, NB, GG, RL...). `:` = hilos mezclados (barber pole/moteado), `-` y `/` = otras combinaciones. Puede traer rangos.
  - `torsion` S/Z/U, `union` (fijación al cordón principal: R recto, V verso, T cuerda superior, U/Unknown/? desconocida), `largo` (cm), `terminacion`, `notas`.
- `analisis/datos/quipus.csv` — metadatos por quipu: `procedencia`, `region`, `museo`, `pc_*` (cordón principal), `okr` (número KH).
- `analisis/datos/grupos.csv` — grupos de colgantes: posición en cm sobre el cordón principal, rango de cuerdas, espacio.
- Fuentes crudas si las necesitas: `data/external/open-khipu-repository/data/khipu.db` (SQLite OKR, 619 quipus; tablas `khipu_main`, `cord`, `knot`, `knot_cluster`, `ascher_cord_color`), `data/external/data-science-khipu-article/data/` (KFG: `khipu_summary.csv`, `ascher_sum_relations/*.csv`), `data/external/khipu-computational-toolkit/data/processed/*.csv`.
- Literatura: `docs/estado_del_arte.md` (síntesis crítica, léela por secciones con grep) y `docs/fichas/*.md` (una ficha por paper). PDFs en `papers/`.

## Reglas de método (obligatorias)

1. La unidad de análisis es el **quipu**, no la cuerda (evita la pseudorreplicación). Si pruebas a nivel de cuerda, usa permutaciones *dentro* de cada quipu o agrega por quipu.
2. Todo efecto lleva **modelo nulo explícito** (permutación que preserve lo que podría explicar el efecto por sí solo) y p-valor empírico. Semilla fija.
3. Corrige por comparaciones múltiples (Holm o BH-FDR) y dilo.
4. Reporta también los **resultados negativos**.
5. Etiqueta cada conclusión: **demostrado / apoyado con datos / propuesto / especulativo**.
6. No uses procedencia de museo como lugar de origen. Valores 0 sin nudos = ausentes.
7. Sé escéptico de tus propios hallazgos: busca la explicación aburrida antes de la interesante.

## Entorno y entrega

- Python 3.13 con pandas, numpy, scipy, scikit-learn. Usa la herramienta Bash. Si necesitas otro paquete, `pip install` está permitido.
- Escribe **solo** dentro de tu carpeta `analisis/<tu_carpeta>/`: scripts `.py` reproducibles y un `informe.md` en español (método, resultados con cifras, controles, negativos, nivel de evidencia, ideas para la siguiente ronda). No hagas commits. No toques otras carpetas.
- Tu respuesta final al coordinador: resumen de 300–500 palabras con los hallazgos numéricos clave, su nivel de evidencia y qué recomiendas investigar después. Lo que no está en esa respuesta no le llega al coordinador.
