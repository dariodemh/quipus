# Lector de quipus

Da la **ficha de lectura** de un quipu: un id KFG u OKR, o un CSV con el esquema de cuerdas. Cada afirmación lleva su nivel de evidencia y la ruta de donde sale en el repo.

El lector no aporta métodos nuevos. Empaqueta los que el proyecto ya validó (bitácora: `analisis/SINTESIS.md`) y reutiliza su código; donde lo copia, lo indica en un comentario.

## Uso

```bash
python lector/lector.py UR278            # id KFG
python lector/lector.py KH0517           # id OKR (se traduce a KFG; los 19 OKR sin KFG salen de 17_okr_pendientes)
python lector/lector.py mi_quipu.csv     # CSV con las columnas de analisis/datos/cuerdas.csv
python lector/lector.py UR278 --json     # salida JSON
python lector/lector.py --todos          # todo el corpus: una línea por quipu y, al final, el recuento de errores
python lector/verificar.py               # resultados conocidos; falla si algo se rompe
```

**Requisitos.** Python ≥ 3.10 con pandas, numpy, scipy, numba y scikit-learn (los mismos que ya usa `analisis/`). El lector no usa la red.

**Tiempos.** La primera ejecución compila numba (~1 min); la caché queda en `lector/__pycache__/`. Después, cada ficha tarda entre 4 y 20 s.

**CSV de entrada.** Columnas obligatorias: `orden, cuerda, nivel, padre, grupo, valor, nudos, color`. Opcionales: `kfg, torsion, union, terminacion`. Si el CSV trae varios `kfg`, se lee cada quipu por separado.

**Convenciones:**
- Una cuerda con valor 0 y sin nudos se toma como ausente, no como un cero.
- El color se normaliza con `re.sub(r'\([^)]*\)', '', s)`.
- En `nudos`, el número que precede al tipo es el VALOR, no el número de vueltas: `200L` es un nudo largo de 2 vueltas en las centenas.

## Qué contiene la ficha

**Niveles de evidencia:**
- `dato`: lo que dice la transcripción.
- `demostrado`, `apoyado`, `propuesto`: los mismos niveles de `analisis/SINTESIS.md`.
- `negativa`, `especulativo`: solo en relaciones documentadas que el repo ya evaluó y descartó o dejó en el aire (p. ej. las candidatas UR004→UR091 y UR1034~UR1145). Si el lector las recalcula, la línea recalculada lo avisa.

Las relaciones marcadas como `[documentada]` vienen de la bitácora, con su nivel. Las que recalcula el lector salen como `propuesto`: la corrección BH cubre solo los quipus comparados en esa consulta, no las ~210 000 parejas del corpus. Son candidatas a confirmar.

| Sección | Qué hace | Fuente (método y validación) |
|---|---|---|
| Resumen físico | Cuerdas, niveles, grupos, colores normalizados, torsión, valores, cuerdas rotas o sin nudos, marcadoras de OKR | `analisis/datos/`, `28_atlas_generos/matriz.csv` |
| Gramática numérica | Fracción no decimal, notación aditiva (varias unidades que suman más de 9), nudos de ≥ 10 vueltas (`NUM_TURNS` de OKR) y torsión Z | `28_atlas_generos/01_matriz.py`, `ds/n_nudos_imposibles/`, `27_familia_z/` |
| Sumas internas | Colgante = Σ subsidiarias (R1), colgante = Σ vecinos (F), total de grupo adyacente (A), cuerda superior (TA), con nulo de permutación dentro de nivel; ejemplos concretos; q del corpus | `01_aritmetica/nucleo.py`, `08_auditoria_sumas/refinado.csv`, `14_copias/fila_total_por_quipu.csv` |
| Encabezados y color | Primer o último colgante como máximo del grupo; NMI color–grupo y color–posición frente a un nulo; color de cada columna | `10_tablas/`, `24_color_formato/p3_transcriptor.py`, `ds/n_color_posicion/` |
| Formato Nazca/Berlín | Registros de n campos + 2 marcadoras, orientación congelada, regla «el campo 1 es el máximo» | `ds/n_ficha_nazca/lib.py` y `p4_barrido.py`, `ds/n_ur1140_nazca/` |
| Formulario | Clave de reparto. En el corpus se lee el resultado publicado (BH y Holm sobre 651 quipus); en un CSV nuevo se recalcula | `22_formularios/detector.py` |
| Relaciones | Copias e inversiones (Smith-Waterman log-odds), totales de grupo que reaparecen en orden (nulo de orden y nulo de magnitud), celda = colgante + 1.ª subsidiaria. BH sobre los ~640 quipus comparados. Documentadas: bitácora, `14_copias` y `33_estematica/pares_copia.csv` (si sube el nivel o el par es nuevo) | `04_concordancias/concordancias.py`, `ds/n_cuota_entrega/03_relaciones.py`, `13_sistema_incahuasi/`, `33_estematica/` |
| Alternancia de dos colores | A/B/A/B entre colgantes (desfase 2); columna dominante dentro del par | `30_frontera_estructura/06_alternancia.py`, `04_diagnosticos.py` |
| Totales por columna | Un bloque = suma de 2 o 3 bloques consecutivos, posición a posición (tabla jerárquica) | `30_frontera_estructura/07_ur122_kh0049.py` |
| Género | En el corpus, atlas publicado (las reglas se reaplican para comprobarlo) y, si la hay, su enmienda con la fuente. En un CSV, reglas del atlas sobre los rasgos recalculados | `28_atlas_generos/reglas.py`, `atlas.csv`, `enmiendas.csv` |

**Detectores de 30_frontera_estructura (rondas 17–18).** Van enganchados en `detectores.DETECTORES_EXTRA`. Son genéricos: no nombran quipus.
- **Alternancia de dos colores** (`alternancia`). Estadístico T2 de `30_frontera_estructura/01_internas.py`: prominencia máxima de la autocorrelación de coincidencias de color. Nulo: permutar los colores de los colgantes (en tandas de 1 000, hasta 9 999 réplicas o 10 excedencias); solo se corre si el desfase con más prominencia es 2. En el corpus, el nivel sale de la q BH publicada sobre 515 quipus (`alternancia_corpus.csv`): `apoyado` si q < 0,05; en un CSV, `propuesto` si p < 0,05. La lectura como tabla de dos columnas intercalada (unidad = par, columna = color) es siempre `propuesto`. En el corpus da los 19 de 06 como apoyados y 5 más como propuestos. Nivel en la fuente: UR040 y UR167 demostrado (Holm 0,025 en la frontera), UR1033F apoyado.
- **Totales por columna** (`totales_columna`). Los colgantes se cortan en bloques consecutivos del tamaño de grupo modal. Cada candidato es un bloque total y un tramo de 2 o 3 bloques consecutivos que lo suman posición a posición (exacto y > 0). Nulo de 07: permutar las posiciones del último sumando (20 000 réplicas). BH sobre todos los candidatos del quipu; los que no llegan a 3 aciertos cuentan con p = 1. Nivel `propuesto`. En el corpus enciende en KH0049 (B0 = B1+B2 en 14/18, B1 = B3+B4+B5 en 7/18, como en 07; apoyado post hoc en la fuente), UR1120 (fila resumen ya vista en 10_tablas) y QU005 (B2 = B0+B1 en 12/19, sin documentar).

**Enmiendas del atlas.** `analisis/28_atlas_generos/atlas.csv` queda congelado. Las salidas de 30 van en `enmiendas.csv` (kfg, genero_nuevo, confianza, evidencia, fuente, fecha): UR040 → TAB baja, UR167 y UR1033F → TAB media, KH0049 → SUM media (antes FOR) y UR122 → SUM baja. La ficha muestra el género del atlas y, debajo, la enmienda con su fuente; `--todos` la añade a la línea del quipu. `verificar.py` imprime la cobertura (confianza alta o media) antes y después de las enmiendas.

**Relaciones documentadas nuevas (rondas 17–18).** UR234 → UR1104, extracto de las cabeceras (apoyado, post hoc). UR231 → UR108, cuerda 9 de las secciones (propuesto). KH0049 → UR122, sección de subtotales (apoyado). UR278 → libro: de 18 filas con destino, 11 exactas y 7 desajustes, 6 de 7 en las unidades y sin dirección; es un error de conteo de vueltas, no una convención (`34_comparada/desajustes.py`). Candidatas del lector: UR004 → UR091, negativa; UR1034 ~ UR1145, especulativa.

**Cómo añadir un detector.** Basta con una función `f(d, ctx) -> dict(titulo, datos, afirmaciones)` añadida a `detectores.DETECTORES_EXTRA`.

## Verificación

`verificar.py` reproduce estos resultados:
- UR270 → UR278 (celda = P + S1, con solo P 0 grupos);
- UR278 → UR266 y UR278 → UR275 (totales en orden);
- la copia UR275 ~ UR266, que se da como documentada (13, a nivel de registro). El alineamiento cuerda a cuerda no la recupera, igual que en 04 (q = 0,20), y la prueba exige que siga siendo así;
- la celda UR270 g0 = UR278 g21;
- la ficha de UR1140 (19/19) y de UR1131 (11/12);
- el género de UR053A (FOR, confianza alta) y la coincidencia de las reglas con `atlas.csv` en los 651 quipus;
- las 32 cuerdas de ≥ 10 vueltas de UR1095;
- la alternancia W/AB de UR040 (26/33 posiciones, desfase 2, p ≤ 1e-3);
- la tabla jerárquica de KH0049 (B0 = B1+B2 en ≥ 12/18; B1 = B3+B4+B5);
- UR1104 → UR234: ≥ 8 cabeceras en orden y la 6.ª, rota en UR234, presente en UR1104 (2016);
- la enmienda de KH0049 (FOR en el atlas, SUM en la enmienda).

También corre cinco controles negativos (AS010, UR001 y UR278 con los valores barajados; AS006 sin alternancia; KH0049 con los valores barajados) y una entrada CSV.

**Resultado (18-10-2026):** 19/19 comprobaciones correctas. `lector.py --todos`: 651 quipus, 0 errores.

## Limitaciones

- **Las p son por quipu.** Las relaciones se corrigen con BH sobre los quipus comparados, pero la ficha no corrige sobre las ~640 consultas posibles del corpus. La q de corpus, cuando existe, viene de las tablas publicadas: 04, 08, 14, 22 y 28.
- **La primera ficha con numba es lenta.** El lector usa semilla fija (20261018), pero el número de permutaciones cambia según los candidatos, así que las p pueden variar en el último dígito entre versiones del corpus.
- **Las relaciones parten de valores exactos (±1 en celdas).** No detectan reordenamientos de bloques, escalas ni extractos de un campo (UR1104/UR234 sale solo como documentada). `30_frontera_estructura` ya cerró: escalas, periodicidad y sumas no contiguas dieron negativo o solo especulativo, así que no hay detector para ellos.
- **Los detectores nuevos tienen límites conocidos.** La alternancia depende del color, y el color depende del transcriptor (UR distingue más colores que AS). Los totales por columna solo ven bloques alineados al tamaño de grupo modal desde la primera cuerda: una tabla desplazada o con bloques de tamaños distintos no sale.
- **Un CSV nuevo no tiene todos los rasgos del atlas.** Faltan plantillas Santa, calendario y bloques, la tabla de 10, la fibra y las marcadoras de OKR, y la clase no numérica. El género recalculado queda con confianza «media» como máximo y siempre en `propuesto`.
- **Los colores dependen del transcriptor.** Las comparaciones de color entre quipus de transcriptores distintos no son fiables (24_color_formato).
- **KFG y OKR son la misma lectura**, hecha por la misma transcriptora en Incahuasi. Coincidir con OKR no equivale a una verificación independiente.
- **El lector no interpreta el contenido.** Las lecturas de Incahuasi están en `analisis/29_lectura_incahuasi/lectura.md`.

## Cómo citar

Cita el repositorio (quipu, carpeta `lector/`, con el commit usado) y las fuentes de datos:
- OKR Team (2025). *The Open Khipu Repository* (v2.1.0). Zenodo. https://doi.org/10.5281/zenodo.18025748
- Medrano, M. y Khosla, A. (2024). *How Can Data Science Contribute to Understanding the Khipu Code? (Companion Data and Code)* (v2.1.0). Zenodo. https://doi.org/10.5281/zenodo.10472429

Para un hallazgo concreto, cita además la ruta de la fuente que da la ficha (`analisis/...`).
