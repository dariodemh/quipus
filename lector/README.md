# Khipu reader

*Spanish version: [LEEME.md](LEEME.md).*

Gives the **reading sheet** (ficha de lectura) of a khipu: a KFG or OKR id, or a CSV with the cord schema. Each claim carries its evidence level and the path in the repo where it comes from.

The reader adds no new methods. It packages the methods the project has already validated (work log: `analisis/SINTESIS.md`) and reuses their code; where it copies code, a comment says so.

## Usage

```bash
python lector/lector.py UR278            # id KFG
python lector/lector.py KH0517           # id OKR (se traduce a KFG; los 19 OKR sin KFG salen de 17_okr_pendientes)
python lector/lector.py mi_quipu.csv     # CSV con las columnas de analisis/datos/cuerdas.csv
python lector/lector.py UR278 --json     # salida JSON
python lector/lector.py --todos          # todo el corpus: una línea por quipu y, al final, el recuento de errores
python lector/verificar.py               # resultados conocidos; falla si algo se rompe
```

**Requirements.** Python ≥ 3.10 with pandas, numpy, scipy, numba and scikit-learn (the same ones `analisis/` already uses). The reader does not use the network.

**Timing.** The first run compiles numba (~1 min); the cache is kept in `lector/__pycache__/`. After that, each sheet takes between 4 and 20 s.

**Input CSV.** Required columns: `orden, cuerda, nivel, padre, grupo, valor, nudos, color`. Optional: `kfg, torsion, union, terminacion`. If the CSV contains several `kfg` values, each khipu is read separately.

**Conventions:**
- A cord with value 0 and no knots is treated as absent, not as a zero.
- The color is normalised with `re.sub(r'\([^)]*\)', '', s)`.
- In `nudos`, the number that precedes the type is the VALUE, not the number of turns: `200L` is a long knot of 2 turns in the hundreds.

## What the reading sheet contains

**Evidence levels:**
- `dato` (data as transcribed): what the transcription says.
- `demostrado` (demonstrated), `apoyado` (supported), `propuesto` (proposed): the same levels as in `analisis/SINTESIS.md`.
- `negativa` (negative), `especulativo` (speculative): only for documented relations that the repo has already evaluated and either discarded or left open (e.g. the candidates UR004→UR091 and UR1034~UR1145). If the reader recalculates them, the recalculated line flags this.

Relations marked `[documentada]` (documented) come from the work log, with their level. Those the reader recalculates appear as `propuesto` (proposed): the BH correction covers only the khipus compared in that query, not the ~210,000 pairs in the corpus. They are candidates to confirm.

| Section (as printed) | What it does | Source (method and validation) |
|---|---|---|
| Resumen físico (physical summary) | Cords, levels, groups, normalised colors, ply, values, broken or knotless cords, OKR marker cords | `analisis/datos/`, `28_atlas_generos/matriz.csv` |
| Gramática numérica (numerical grammar) | Non-decimal fraction, additive notation (several units summing to more than 9), knots of ≥ 10 turns (`NUM_TURNS` in OKR) and Z-ply | `28_atlas_generos/01_matriz.py`, `ds/n_nudos_imposibles/`, `27_familia_z/` |
| Sumas internas (internal sums) | Pendant cord = Σ subsidiary cords (R1), pendant cord = Σ neighbours (F), adjacent group total (A), top cord (TA), with permutation null within level; concrete examples; q from the corpus | `01_aritmetica/nucleo.py`, `08_auditoria_sumas/refinado.csv`, `14_copias/fila_total_por_quipu.csv` |
| Encabezados y color (headers and color) | First or last pendant cord as the group maximum; NMI color–group and color–position against a null; color of each column | `10_tablas/`, `24_color_formato/p3_transcriptor.py`, `ds/n_color_posicion/` |
| Formato Nazca/Berlín (Nazca/Berlin format) | Records of n fields + 2 marker cords, frozen orientation, rule "field 1 is the maximum" | `ds/n_ficha_nazca/lib.py` and `p4_barrido.py`, `ds/n_ur1140_nazca/` |
| Formulario (form) | Distribution key. In the corpus the published result is read (BH and Holm over 651 khipus); in a new CSV it is recalculated | `22_formularios/detector.py` |
| Relaciones (relations) | Copies and inversions (Smith-Waterman log-odds), group totals that reappear in order (order null and magnitude null), cell = pendant cord + 1st subsidiary cord. BH over the ~640 khipus compared. Documented: work log, `14_copias` and `33_estematica/pares_copia.csv` (if the level rises or the pair is new) | `04_concordancias/concordancias.py`, `ds/n_cuota_entrega/03_relaciones.py`, `13_sistema_incahuasi/`, `33_estematica/` |
| Alternancia de dos colores (two-color alternation) | A/B/A/B between pendant cords (offset 2); dominant column within the pair | `30_frontera_estructura/06_alternancia.py`, `04_diagnosticos.py` |
| Totales por columna (column totals) | A block = sum of 2 or 3 consecutive blocks, position by position (hierarchical table) | `30_frontera_estructura/07_ur122_kh0049.py` |
| Género (genre) | In the corpus, the published atlas (the rules are reapplied to verify it) and, if there is one, its amendment with the source. In a CSV, atlas rules applied to the recalculated traits | `28_atlas_generos/reglas.py`, `atlas.csv`, `enmiendas.csv` |

**Detectors from 30_frontera_estructura (rounds 17–18).** They are hooked into `detectores.DETECTORES_EXTRA`. They are generic: they do not name khipus.
- **Two-color alternation** (`alternancia`). Statistic T2 from `30_frontera_estructura/01_internas.py`: maximum prominence of the autocorrelation of color matches. Null: permute the colors of the pendant cords (in batches of 1,000, up to 9,999 replicates or 10 exceedances); it is only run if the offset with the greatest prominence is 2. In the corpus, the level comes from the published BH q over 515 khipus (`alternancia_corpus.csv`): `apoyado` (supported) if q < 0.05; in a CSV, `propuesto` (proposed) if p < 0.05. Reading it as an interleaved two-column table (unit = pair, column = color) is always `propuesto` (proposed). In the corpus it gives 19 of 06 as apoyado and 5 more as propuesto. Level in the source: UR040 and UR167 demostrado (Holm 0.025 at the boundary), UR1033F apoyado.
- **Column totals** (`totales_columna`). Pendant cords are cut into consecutive blocks of the modal group size. Each candidate is a total block and a run of 2 or 3 consecutive blocks that sum to it position by position (exact and > 0). Null of 07: permute the positions of the last addend (20,000 replicates). BH over all candidates of the khipu; those that do not reach 3 hits count with p = 1. Level `propuesto` (proposed). In the corpus it lights up in KH0049 (B0 = B1+B2 in 14/18, B1 = B3+B4+B5 in 7/18, as in 07; supported post hoc in the source), UR1120 (summary row already seen in 10_tablas) and QU005 (B2 = B0+B1 in 12/19, undocumented).

**Amendments to the atlas.** `analisis/28_atlas_generos/atlas.csv` is frozen. The outputs of 30 go into `enmiendas.csv` (kfg, genero_nuevo, confianza, evidencia, fuente, fecha): UR040 → TAB low, UR167 and UR1033F → TAB medium, KH0049 → SUM medium (previously FOR) and UR122 → SUM low. The sheet shows the genre from the atlas and, below it, the amendment with its source; `--todos` adds it to the khipu's line. `verificar.py` prints the coverage (high or medium confidence) before and after the amendments.

**New documented relations (rounds 17–18).** UR234 → UR1104, extract of the headers (apoyado, post hoc). UR231 → UR108, cord 9 of the sections (propuesto). KH0049 → UR122, subtotals section (apoyado). UR278 → book: of 18 rows with a destination, 11 exact and 7 mismatches, 6 of 7 in the units and without direction; this is a turn-counting error, not a convention (`34_comparada/desajustes.py`). Reader candidates: UR004 → UR091, negativa (negative); UR1034 ~ UR1145, especulativo (speculative).

**How to add a detector.** Just add a function `f(d, ctx) -> dict(titulo, datos, afirmaciones)` to `detectores.DETECTORES_EXTRA`.

**Genre codes** (from `analisis/28_atlas_generos/reglas.py`):

| Code | Genre |
|---|---|
| CAL | Calendar (UR006 type) |
| NAZ | Record with header and marker pair (Nazca/Berlin) |
| ARC | Hierarchical archive with relations between khipus (Inkawasi, Puruchuco) |
| PAD | Census by person (Santa 1670 type) |
| FOR | Form with an allocation key |
| NON | Non-numeric (no knots, or knots off the decimal axis) |
| TAL | Additive record / tally (Z ply) |
| SUM | Decimal accounting with internal totals |
| ASG | Assignment list (round figures, quotas) |
| TAB | Count table (units × categories) |
| SEG | Segmented list (format only: colour by group, marker cords) |
| SIN | No genre assigned |

## Verification

`verificar.py` reproduces these results:
- UR270 → UR278 (cell = P + S1, with only P giving 0 groups);
- UR278 → UR266 and UR278 → UR275 (totals in order);
- the copy UR275 ~ UR266, given as documented (13, at record level). The cord-by-cord alignment does not recover it, as in 04 (q = 0.20), and the test requires that this remains so;
- the cell UR270 g0 = UR278 g21;
- the sheet of UR1140 (19/19) and of UR1131 (11/12);
- the genre of UR053A (FOR, high confidence) and the match of the rules with `atlas.csv` across the 651 khipus;
- the 32 cords of ≥ 10 turns in UR1095;
- the W/AB alternation of UR040 (26/33 positions, offset 2, p ≤ 1e-3);
- the hierarchical table of KH0049 (B0 = B1+B2 in ≥ 12/18; B1 = B3+B4+B5);
- UR1104 → UR234: ≥ 8 headers in order and the 6th, broken in UR234, present in UR1104 (2016);
- the amendment of KH0049 (FOR in the atlas, SUM in the amendment).

It also runs five negative controls (AS010, UR001 and UR278 with shuffled values; AS006 without alternation; KH0049 with shuffled values) and one CSV input.

**Result (18-10-2026):** 19/19 checks passed. `lector.py --todos`: 651 khipus, 0 errors.

## Limitations

- **The p-values are per khipu.** Relations are corrected with BH over the khipus compared, but the sheet does not correct over the ~640 possible queries in the corpus. The corpus q, where it exists, comes from the published tables: 04, 08, 14, 22 and 28.
- **The first sheet with numba is slow.** The reader uses a fixed seed (20261018), but the number of permutations changes with the candidates, so the p-values may vary in the last digit between corpus versions.
- **Relations start from exact values (±1 in cells).** They do not detect block rearrangements, scales or single-field extracts (UR1104/UR234 appears only as documented). `30_frontera_estructura` is already closed: scales, periodicity and non-contiguous sums gave negative or only speculative results, so there is no detector for them.
- **The new detectors have known limits.** Alternation depends on color, and color depends on the transcriber (UR distinguishes more colors than AS). Column totals only see blocks aligned to the modal group size from the first cord; a shifted table or one with blocks of different sizes will not be detected.
- **A new CSV does not have all the atlas traits.** Santa templates, calendar and blocks, the table of 10, the fibre and the OKR marker cords, and the non-numeric class are missing. The recalculated genre is capped at "medium" confidence and is always `propuesto` (proposed).
- **Colors depend on the transcriber.** Color comparisons between khipus from different transcribers are not reliable (24_color_formato).
- **KFG and OKR are the same reading**, made by the same transcriber at Incahuasi. Matching OKR is not an independent verification.
- **The reader does not interpret content.** The Incahuasi readings are in `analisis/29_lectura_incahuasi/lectura.md`.

## How to cite

Cite the repository (quipu, folder `lector/`, with the commit used) and the data sources:
- OKR Team (2025). *The Open Khipu Repository* (v2.1.0). Zenodo. https://doi.org/10.5281/zenodo.18025748
- Medrano, M. and Khosla, A. (2024). *How Can Data Science Contribute to Understanding the Khipu Code? (Companion Data and Code)* (v2.1.0). Zenodo. https://doi.org/10.5281/zenodo.10472429

For a specific finding, also cite the source path given in the sheet (`analisis/...`).
