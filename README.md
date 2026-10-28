# Khipus: a computational analysis of the digital corpus

*Versión en español: [README.es.md](README.es.md).*

**Open to specialist review.** Nothing here has been through peer review yet, and we invite specialists in khipus, Andean history and statistics to check it. Objections, corrections and new readings of the objects are welcome as [issues](https://github.com/dariodemh/quipus/issues).

**Languages.** The review package is available in English in [`analisis/paquete_revision/en/`](analisis/paquete_revision/en/), and the reader's guide in [`lector/README.md`](lector/README.md). The per-folder reports and the work log (`analisis/SINTESIS.md`) are in Spanish only.

## Summary

We ran the whole digital khipu corpus (Khipu Field Guide and Open Khipu Repository: ~650 khipus, 57,818 cords) through a series of tests:

- permutation tests with multiple-comparison correction;
- positive controls;
- a blind test on anonymised data;
- pre-registered predictions.

**Main result.** The Inkawasi (Incahuasi, Cañete) archive contains a three-level consolidation chain:

- pendant + first subsidiary of UR270 reproduce, cell by cell, the 9-column table of UR278;
- the row totals of UR278 reappear, in order, as headers of UR275 and UR266.

A second route (UR273A + UR273B) is supported but not well supported.

**Outside Inkawasi,** the results are mostly negative or methodological:

- the widely cited figure that 74% of khipus contain sums is not informative against a proper null;
- there is no shared colour lexicon and no detectable syllabic text;
- copying is an archive-level practice (OR 17.9).

**New candidates:**

- a three-level table with column totals in KH0049, with UR122 as its partial copy;
- two-colour alternating tables (UR040, UR167).

Every claim carries an evidence level and points to the script that produces it. The [verifiable predictions](analisis/paquete_revision/en/verifiable_predictions.md) are frozen, and only someone with access to the objects, photographs or archives can check them.

## Where to start

0. [`articulo/index.html`](articulo/index.html): the essay *What the khipus add up to*, for a general reader, with interactive figures. It opens in English and links to the Spanish version, [`articulo/index.es.html`](articulo/index.es.html).
1. [`analisis/paquete_revision/en/summary_for_specialists.md`](analisis/paquete_revision/en/summary_for_specialists.md): data, methods and findings, grouped by evidence level.
2. [`analisis/paquete_revision/en/findings_table.csv`](analisis/paquete_revision/en/findings_table.csv): one row per finding, with:
   - its statistic and p or q value;
   - the source file;
   - whether it is new or already published;
   - whether it was corrected.
3. [`analisis/paquete_revision/en/verifiable_predictions.md`](analisis/paquete_revision/en/verifiable_predictions.md): frozen predictions to check in museums and archives.
4. [`analisis/paquete_revision/en/prior_work.md`](analisis/paquete_revision/en/prior_work.md): what was already published.
5. [`lector/README.md`](lector/README.md): the reproducible **reader**. It produces a reading sheet for any khipu in the corpus; every statement on the sheet carries its evidence level and the path of the code behind it.

## How this was done: AI assistance

The analysis was carried out by AI agents: Claude (Anthropic), running in Claude Code, plus DeepSeek for some extraction tasks. One person coordinated and directed them. The agents:

- wrote and ran the scripts;
- reviewed each other's work, including a "red team" that tried to break every result.

For this reason the repository puts weight on what can be checked without trusting us:

- every number comes from a script that can be rerun;
- the two verifiers below fail if a key result changes.

The errors we found and corrected are recorded in the `corrected` column of the findings table and in each folder's report.

**No agent examined the objects.** Everything comes from the published transcriptions and the literature cited.

## Main findings

| Id | Finding | Level |
|---|---|---|
| I01 | UR270 → UR278: pendant + first subsidiary = cells of the 9-column table | well supported |
| I02 | Row totals of UR278 = headers of UR266 and totals of UR275, in order | well supported |
| I03 | UR273A + UR273B = the same headers by a second route | supported |
| I09–I10 | The 9 columns are the same 9 units in UR270 and UR278, with exceptional flatness | well supported |
| C01 | The "74% of khipus with sums" figure is not informative against a proper null | supported |
| C06, C18 | Colour is a local key with no shared lexicon; khipus are data records, not text | well supported / supported (negative) |
| C24, K05 | Copies across museums; copying is an archive-level practice (OR 17.9) | well supported / supported |
| C27 | The method reproduces the published Puruchuco hierarchy (positive control) | well supported |
| K01 | KH0049 is a three-level table with column totals; UR122 is its partial copy | supported (post hoc) |
| K02 | Two-column tables with alternating colours (UR040, UR167) | well supported |
| K03 | UR1104 extracts the headers of 9 records of UR234 and preserves a broken header | supported |
| K11 | Inkawasi unit: *carga* (load, ~23 kg) or *fanega*; total of the order of 900–1,400 t | proposed |

The full list (I01–I22, C01–C29, K01–K11) is in the findings table.

**Evidence scale:**

- **Well supported:** survives the null and the correction, and was replicated by an independent route.
- **Supported:** significant after correction, but without independent replication.
- **Proposed:** consistent with the data, with no test that separates it from the alternatives.
- **Speculative:** untested.

## Reproduce

Requires Python 3.10 or later; tested with 3.13.

```bash
git clone --recurse-submodules https://github.com/dariodemh/quipus.git
cd quipus
pip install -r requirements.txt

python analisis/paquete_revision/verificar.py   # figures in the review package
python lector/verificar.py                      # known results of the reader
python lector/lector.py UR278                   # reading sheet for one khipu
python lector/lector.py --todos                 # the whole corpus (~3 min)

python articulo/fuente/extraer.py . articulo/fuente/datos.json   # data for the essay's figures
python articulo/fuente/construir.py             # articulo/index.html (English) and index.es.html (Spanish)
python articulo/fuente/comprobar.py             # what the text says about each figure matches its data
python articulo/fuente/comprobar_idioma.py articulo/index.html en   # no Spanish left on the English page (needs playwright)
```

- **Run time.** The first run compiles numba, which takes about 1 minute. After that, each sheet takes 4–20 s.
- **OKR database.** It is always opened read-only, from the submodule: `data/external/open-khipu-repository/data/khipu.db`.
- **Scripts in `analisis/`.** Run them from the repository root (`python analisis/NN_tema/script.py`), since paths are relative to it. Some scripts write intermediate files (`.pkl`, images) that are not committed, because rerunning regenerates them. If a script needs one of these files, first run the script that produces it, following the folder numbering.

## Layout

```
analisis/            one folder per question, numbered in the order it was addressed
  datos/             cuerdas.csv: the single cord table, derived from KFG
  paquete_revision/  review package (Spanish) and en/ (English)
  ds/                agent rounds (each folder with its informe.md)
  NN_tema/           informe.md + scripts for each analysis
  SINTESIS.md        work log, in chronological order (Spanish)
lector/              reproducible reader (lector.py, detectores.py, verificar.py)
articulo/            the essay: index.html (English), index.es.html (Spanish)
  fuente/            templates (plantilla.en.html, plantilla.html), figuras.js, datos.json and the build scripts
docs/fichas/         reading notes on the literature
scripts/             construction of the cord table
data/external/       submodules: Open Khipu Repository and Medrano & Khosla 2024 data
```

## What is not included, and why

- **Copyrighted texts and PDFs.** We collated published books and articles; only short quotations and references remain here.
- **Images and photographs.** Some sources forbid their reproduction, so no image is included.
- **Local sources.** Some scripts and reports cite paths under `analisis/fuentes_txt/` (text extracts of the cited publications, used for collation) or `encontrado/` (source files such as PDFs and spreadsheets). These folders are not distributed; the publications are listed in the reports.
- **Intermediate files and agent launch scripts.** Intermediate files can be regenerated by rerunning the scripts.

The work log (`analisis/SINTESIS.md`) is included without administrative notes. Entries that were later corrected carry a note that points to the correction.

## Data and licences

- **Open Khipu Repository (OKR)**, v2.1.0. DOI [10.5281/zenodo.18025748](https://doi.org/10.5281/zenodo.18025748). MIT licence.
- **Khipu Field Guide (KFG)**, from Medrano, M. & Khosla, A. (2024), *How can data science contribute to understanding the khipu code?*, *Latin American Antiquity*. Repository v2.1.0, DOI [10.5281/zenodo.10472429](https://doi.org/10.5281/zenodo.10472429). MIT licence.

`analisis/datos/cuerdas.csv` is derived from KFG. Finding C26 lists the errata we found in both databases.

The essay's map uses country outlines from **Natural Earth** (1:50m, public domain), via the `world-atlas` package (v2.0.2). The images in the essay are public domain (Cleveland Museum of Art, CC0; Locke 1912; Guaman Poma, c. 1615).

**This repository:**

- code and derived data: MIT ([`LICENSE`](LICENSE));
- texts: CC BY 4.0 ([`LICENSE-texts.md`](LICENSE-texts.md)).

## Limitations

- **We have not examined any object.** At Inkawasi, KFG and OKR are two encodings of the same reading (finding K10), so there is no independent re-reading.
- **Several findings are post hoc** (K01, K03, K04). They are marked as such and need confirmation on new data.
- **Negative results have limited power.** Read them as "not detectable with this power", not as "does not exist".
- **The search for prior work is incomplete** for several findings marked as new; the `new_or_published` column says so.

## How to cite

> dariodemh (2026). *Khipus: a computational analysis of the digital corpus* [code and data repository]. https://github.com/dariodemh/quipus

If you use the data, please also cite OKR and Medrano & Khosla (2024).
