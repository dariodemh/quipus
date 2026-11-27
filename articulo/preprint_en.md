# Computational Structure, Three-Level Accounting, and Out-of-Sample Testing Across the Digital Andean Khipu Corpus

**Author:** Dario (`dariodemh`), with AI research agents (Claude Opus/Sonnet and DeepSeek Flash)  
**Repository & Live Tools:** https://github.com/dariodemh/quipus · Interactive Essay & Browser Reader: https://dariodemh.github.io/quipus/articulo/  
**Status:** Open preprint for specialist review (not yet peer-reviewed). All statistics, controls, and reading sheets are deterministically reproducible from the public repository.

---

## Abstract

We present a reproducible statistical audit of the digitized Andean khipu corpus, integrating the Khipu Field Guide (651 khipus, 57,818 cords; 650 unique objects after removing duplicate `UR044`), the Open Khipu Repository (`khipu.db`, 619 khipus, 54,403 cords), 19 unintegrated OKR spreadsheets (`776` cords), 11 newly transcribed handwritten recording sheets from Huacones-Vilcahuasi (`JC024`–`JC034`, `KH0653`–`KH0663`, `101` cords), and Harvard thesis khipu `JS01` (`KH0676`, `138` cords), for a combined evaluation corpus of **682 khipus**. Using within-khipu permutation nulls, multiple-testing corrections (Holm and Benjamini-Hochberg FDR), positive controls (reproducing the Puruchuco hierarchy and `KH0049`), blind testing on anonymized data, and preregistered out-of-sample predictions, we report three main findings:

1. **Three-level accounting architecture at Inkawasi:** Building on Urton and Chu (2015, 2018), the Sector A peanut pile exhibits a verifiable consolidation chain in which `pendant + first subsidiary` of `UR270` reproduces cell by cell the 9-column table of `UR278` (5 of 12 comparable groups with 6–9/9 exact matches; `p = 0.0002`; recovered independently by a blind agent), whose row totals reappear in order as headers of `UR266` (11/18 exact, `Holm = 1.6e-9`) and `UR275` (7 exact, `Holm = 2.8e-4`). A tied pair `UR273A + UR273B` reaches 8 of 18 ledger headers by summing parts (`p = 0.015` under 58,782-test red-team correction). Quantitative maximum-parsimony bootstrap (10,000 replicates) gives **99.8%** support for a lost intermediate ledger `α` (`UR278 → α → {UR266, UR275}`) carrying shared unit-level errors (`±1`).
2. **Methodological refinement and negative controls:** While Medrano and Khosla (2024) showed that 74.15% (`482/650`) of khipus exhibit Ascher-type relationships, within-khipu permutation nulls reveal that 93–100% of simple internal sums occur by chance in long khipus (detector power ~24%); only 14 khipus (9 from Inkawasi) survive two distinct shuffles. Color acts locally as a formatting/column key (`167/403` vs ~20 expected) with no detectable cross-site lexicon (`p = 0.34, 0.79`). Empty decimal bands in `726` zero-containing cords span ~1 decimal band (`median = 0.96`; `1.89×` adjacent spacing in 201 cords), bearing on non-positional hypotheses (Florio & Overmann, 2025).
3. **Out-of-sample test and refutation of Prediction #13:** On the 30 unintegrated/virgin OKR khipus (`11 Huacones` + `19 OKR-extra`), preregistered Prediction #13 (that Huacones Quipus 8 and 9 would match Inkawasi's flat 9-column profile) is **refuted** (`JC024` has 8 pendants `[119, 29, 29, 19, 10, 19, 5, 4]`, `CV = 1.283`; `JC031` has 9 pendants with 4 blanks and `CV = 1.227`). However, 4 of 10 knotted Huacones khipus (`40%`) exhibit non-decimal additive knot grammar (`2L+9L`, `1E+1E`), and a calibrated Bayesian error-tolerant scanner detects zero cross-site links (`q_bh < 0.05`) between Huacones/OKR-extra/unread Inkawasi (`UR272, 276, 277, 279`) and the Sector A chain.

**Keywords:** Andean khipus, Inkawasi, Huacones-Vilcahuasi, permutation tests, quantitative stemmatology, computational archaeology, open data.

---

## 1. Introduction

Andean knotted-string khipus remain one of the most thoroughly digitized yet incompletely understood administrative technologies of the ancient Americas. Since Locke (1912) demonstrated decimal positional notation via summing top cords, research has documented internal arithmetic relationships (Ascher & Ascher, 1978), multi-khipu accounting hierarchies at Puruchuco (Urton & Brezine, 2005), duplicate accounts (Urton, 2005; Chirinos, 2010), and the Inkawasi Sector A storehouse archive (Urton & Chu, 2015, 2018; Urton, 2017). Recent data-science and linguistic proposals have ranged from corpus-wide prevalence estimates of internal sums (Medrano & Khosla, 2024) and unsupervised structural clustering (Contreras, 2026) to non-positional interpretations of Inka numeracy (Florio & Overmann, 2025) and syllabic decipherments (Sivan, 2026).

Because a corpus of nearly 58,000 cords generates abundant coincidences by sheer combinatorics, claims about khipu structure require explicit null models that preserve cord-count, value-magnitude, and grouping structure within each object, coupled with multiple-comparison correction and out-of-sample tests. Here we synthesize a full computational audit of the public digital corpus, integrate 30 previously unanalyzed OKR objects—including 11 virgin Huacones recording sheets transcribed from archival photographs—and release both a formal five-knot museum verification protocol and a zero-server browser Khipu Reader.

---

## 2. Corpus, Data Audits, and Virgin Transcriptions

### 2.1 Primary Digital Sources and Database Errata
We draw on two open repositories without physical examination of any artifact:
- **Khipu Field Guide (KFG v2.1.0):** companion snapshot to Medrano and Khosla (2024), comprising `651` Excel sheets (`57,818` cords) and `650` summary rows (`UR044` is an incomplete duplicate of `AS031/KH0033`).
- **Open Khipu Repository (OKR v2.1.0):** `khipu.db` (`619` khipus, `54,403` cords) plus `okr-kh-numbers.csv` (`702` assigned KH numbers across `761` physical lines due to embedded newlines).

Cross-reconciliation revealed systematic database discrepancies (`C26`; full technical report in `analisis/paquete_revision/en/errata_report_okr_kfg.md`):
1. **Shared transcription at Inkawasi:** KFG and OKR agree on `99.33%` of comparable knotted cords (`>99.8%` at Inkawasi), indicating they are two encodings of the same underlying transcription rather than independent physical readings. Independent double-readings exist only for three objects (`UR1107 = UR237` read in reverse, `23/26` exact values, cord-length `r = 0.99`, `0/23` matching color labels; `KH0033 = UR044`, `23/23`; `AS125 = UR247`, `14/15`), yielding an empirical reading noise floor of `0–12%` (`3–7%` on aligned families).
2. **Omissions in KFG:** KFG omits `111` Inkawasi cords present in OKR (including `58` in `UR256` and `32` subsidiaries in `UR274B`), `92 of 95` level-1 top cords, and `502 of 502` marker cords.
3. **KH collisions & discrepancies:** Four KFG spreadsheets (`KH0197`, `KH0227`, `KH0267`, `KH0350`) collide with other KH records; `86%` of KFG–OKR numeric discrepancies cluster in five khipus (`UR090, UR144, UR235, UR193, UR190`), half being factor-of-10 shifts; `AS001–AS009` sit in `AS1-AS9.db` outside `khipu.db`; and `KH0676` collides with `KH0700` on inventory `80.1012 aka 2708`.

### 2.2 Out-of-Sample Corpus Integration (30 OOS Khipus + `JS01`)
From the `83` KH numbers absent from `khipu.db`, we integrated:
- **19 OKR spreadsheets (`776` cords)** (`analisis/17_okr_pendientes/cuerdas_extra.csv`): `KH0631` (`SH001`), `KH0633–KH0635`, `KH0638–KH0651` (linked khipus `RT-16905`), and `KH0702` (`R4303`).
- **11 virgin Huacones-Vilcahuasi recording sheets (`101` cords)** (`analisis/35_huacones_virgenes/cuerdas_huacones.csv`): transcribed directly from handwritten field photographs `JC024_record.jpg`–`JC034_record.jpg` (`KH0653–KH0663`, Sector F, Unit 8, Element 11, Lot 97, RAE 1/12/2017). Every cord's transcribed value matches its parsed knot sum except `JC028 p5` (`4L+2L+2L+5L = 13` vs handwritten value `12`), documented as a primary-sheet erratum.
- **Harvard senior thesis khipu `JS01` (`KH0676`, `138` cords)** (`analisis/37_vision_y_extra/cuerdas_js01.csv`): Brooklyn Museum `36.718` parsed to up to level-4 subsidiaries, plus out-of-sample PDF/photogrammetry measurements on `UR-298` (`KH0675`) and `SH001` (`KH0631`).

---

## 3. Statistical Methodology and Evidence Scale

1. **Quipu-level permutation nulls:** Values, colors, or runs are permuted *within* each khipu (or within level/group/magnitude strata) so marginal distributions remain invariant.
2. **Multiple-testing control:** Holm step-down or Benjamini-Hochberg FDR across entire test families. When alignments or pairings were selected after inspecting data (e.g., `UR273A + UR273B`), the red team re-evaluated all `58,782` possible combinations.
3. **Positive & negative controls:** Every detector was calibrated on published hierarchies (Puruchuco: `UR063 → UR068 → UR067` with known discrepancies `2904/2908` and `161/162`; `KH0049`) and shuffled negative controls (`AS010`, `UR001`, `AS006`, shuffled `UR278`, shuffled `KH0049`).
4. **Blind test & preregistration:** 52 Inkawasi khipus were anonymized (`Q01–Q52`) with 15% of knotted cords (`597`) masked; an LLM agent predicted `68` hidden cords (`56/68 = 82%` exact vs `40%` majority-value baseline on those 68 and `14.4%` on all 597) and discovered `UR270 → UR278` unprompted (with the caveat that the model's pretraining corpus may include published khipu literature).
5. **Evidence scale:** **Strong indication** (survives null + correction + separate second analysis on the same data), **Indication** (significant after correction without separate second analysis), **Conjecture** (compatible with data, not uniquely separated from alternatives).

---

## 4. Results

### 4.1 Inkawasi Three-Level Accounting Consolidation (Sector A Peanut Pile)
- **Level 0 → Level 1 (`UR270 → UR278`, *Strong indication*):** Summing `pendant + first subsidiary` in `UR270` reproduces the 9-column rows of `UR278` cell by cell (`5/12` comparable groups with `6–9/9` exact matches, including `8/9` in `UR270 g0` vs `UR278 g21`, differing only by `+1` on `p180`; `p = 0.0002` vs `0/12` with pendants alone; independently recovered in the blind run).
- **Level 1 → Level 2 (`UR278 → UR266 / UR275`, *Strong indication*):** Row totals of `UR278` (`g0 = 3618`) reappear in the exact same order as headers of `UR266` (`11/18` exact matches among rows with preserved ledger counterparts; `Holm = 1.6e-9`) and `UR275` (`7` exact; `Holm = 2.8e-4`).
- **Second route (`UR273A + UR273B`, *Indication*):** Aligned by group number (pink spacers matching), summing `UR273A + UR273B` yields `8/18` exact ledger headers (`2950, 1653, 1737, 1827, 1780, 2247, 1765, 1506`; `1.27` expected; `p = 0.015` under 58,782 red-team combinations; top-5 of 132,600 triples in directed blind search without passing Holm). When `UR273A` is blank, `UR274A` substitutes in `3/4` records (`p = 0.00013`).
- **Accountant errors (`p180` & unit-place mismatches, *Indication*):** Seven of 18 linked rows differ between `UR278` and the ledgers (`+6, +100, +1, -1, +1, -1, -1`), `6/7` in the units place (`p = 0.0069`). On `UR278 p180` (`238` vs `237`), changing the terminal `7L` to `6L` simultaneously resolves `UR270 g0` and `UR278 g21` (`1654 → 1653`).
- **Nine-column profile & storage scale (*Indication* / *Conjecture*):** Column proportions across the `24` complete nine-cord rows of `UR278` are exceptionally flat (`CV = 0.173`; `7 of 8` nine-cord groups with `CV < 0.2` in the entire corpus belong to `UR278`). Their ordering shows superficial similarity (`rho = +0.64`, `p = 0.07`) to the 9 *pachakas* of Bambamarca (Pärssinen, 1992, `CV = 0.385`), remaining a **conjecture**. Across all `26` nine-cord rows (`~59,166` units), using documented colonial `carga` (`~28 L`, ~8 kg peanuts in shell) and `fanega` (`~56 L`, ~16 kg) bounds (LeVine, 1992; Platt, 2002; Shukla et al., 2019) yields an order-of-magnitude volume of **500–950 tonnes**.

### 4.2 Audit of Corpus-Wide Claims
- **The "74% with internal sums" figure (*Indication*):** In KFG, `482/650` (`74.15%`) carry Ascher relations (`69%` cord sums). Under within-khipu permutation nulls, `93–100%` of simple sums arise by chance (real corpus `8,076` vs shuffled 95% intervals `[7892, 8167]`, `[7790, 8036]`, `[7975, 8209]`; simulated detection power `~24%`). We reproduce Medrano and Khosla's lateral asymmetry (`53.9%`, `p < 0.002`), half explained by large-value placement. Only `14` khipus (`2%`, `9` from Inkawasi) survive two distinct shuffles.
- **Positional zeros:** Across `726` khipus/cords with internal zeros (`727` gaps), the empty band spans `0.96` decimal bands (median) and `1.89×` adjacent knot spacing (`201` cords; `p = 6e-33`), demonstrating spatial reservation of decimal places—with the caveat that transcription partially relies on knot spacing.
- **Color as local key, no syllabic signal:** Color predicts value magnitude within `167/403` khipus (`103` within groups) but shows `3.1%` vs `3.0%` chance overlap across unrelated archives (`p = 0.34, 0.79`). Non-numeric khipus hold `5–19` colors (`≤39` ungrouped shades), far below logosyllabic inventories (`80–800`), and color Heaps exponent (`0.44`) resembles tabular records rather than syllable-segmented Quechua text (`0.90`).

### 4.3 Corpus Formats, Copies, and Control Cases
- **Three-level table `KH0049` (`AS38`) and copy `UR122` (*Indication* for null test):** Blocks of 18 cords satisfy `B0 = B1 + B2` in `14/18` positions and `B1 = B3 + B4 + B5` in `7/18` (`p < 0.0001`, 20,000 permutations), recovering the structure already described in the Aschers' *Databook* (1978, pp. 217–218) and partial copy `UR122` (Chirinos, 2010), while adding that both objects share the `15652` vs `15649` discrepancy.
- **Alternating two-color tables (*Indication*):** `UR040` (`26/31` A-B-A trios) and `UR167` (`30/35`) replicate across split-half confirmation (`Holm = 0.025`).
- **Archive copying (`OR = 17.9`) and extracts (*Indication*):** `25+` copy pairs cluster within sites (`10/6,820` vs `6/72,980` across sites, `p = 1e-7`), including cross-museum pairs (`HP055` Lima ≈ `UR1084` Paris, `121/142`) and a field extract (`UR1104` Berlin extracting `g0–g8` headers of `UR234` Berlin: `7` exact, digit transposition `3102/3012`, and `2016` preserved where `UR234` is broken).
- **Fixed-split form `UR053A–E` (*Indication*):** White (`W`), red (`R`), and light-brown (`AB`) shares remain near `4:1:1` (`W = 0.57–0.70`) across totals from `1,200` to `36,800` (developing Urton, 2017 and Chirinos, 2026).

### 4.4 Out-of-Sample Test on 30 Unintegrated OKR Khipus (Huacones & OKR-Extra)
- **Refutation of Prediction #13:** On the 11 newly transcribed Huacones sheets (`JC024–JC034`), Quipu 8 (`JC024`) has `8` pendants (`[119, 29, 29, 19, 10, 19, 5, 4]`, `rho = -0.952`, `CV = 1.283`) and Quipu 9 (`JC031`) has `9` pendants (`[11, 1, 4, 8, 0, 0, 0, 0, 9]`, `rho = -0.400`, `CV = 1.227`), refuting the hypothesis that they mirror `UR278`'s flat 9-column accounting profile (`CV ~ 0.2`).
- **Additive grammar prevalence in Huacones & `JS01`:** `4 of 10` knotted Huacones khipus (`40%`: `JC028, JC031, JC032, JC034`) employ stacked non-decimal units (`2L+9L`, `2L+6L`, `1E+1E`), alongside shared loop-closed primary cords (`6/11`), red pigment bands (`9/11`), `Z`-direction knots, and `S`-final ply. Likewise, `JS01` (`KH0676`, `138` cords, up to level-4 subsidiaries) exhibits `99.27%` (`136/137`) non-decimal/additive knot ordering (`analisis/37_vision_y_extra/informe.md`).
- **Out-of-sample zero-gap, `RT-16905` link graph, and `SH001` CIELAB photogrammetry:** On Dumbarton Oaks `UR-298` (`KH0675`, `PC.WBC.2016.071.pdf`), `13` internal-zero intervals (median `10.5 cm`) vs `45` adjacent intervals (`5.5 cm`) give a ratio of **`1.909`** (Mann-Whitney `U = 585.0`, `p = 1.94e-8`), independently replicating the `1.89` KFG ratio. On `RT-16905` (`KH0638–KH0651`), physically linked khipus share cord-length scale (`6.78` vs `10.55 cm`, `p = 0.009`) without sharing numeric values (`p = 0.101`). Greyscale-calibrated CIELAB photogrammetry on `SH001` (`KH0631`) shows coarse categories separate strongly (`ΔE = 16.1–54.2`) whereas fine shades (`YB` vs `AB`, `ΔE = 2.45`) sit at the perceptual noise floor.
- **Reader evaluation (`30` OOS khipus):** `6/30` receive an atlas genre (`TAL`, `ASG`, `FOR`, `SEG`), `24/30` remain `SIN`, and none exhibit cross-corpus copies or Inkawasi links.

### 4.5 Quantitative Stemmatology & Bayesian Error-Channel Model
Using empirical noise rates calibrated across the `3` double readings (`N = 64`: `60` exact, `2` `×10` shifts, `2` other) and `225` aligned copy variants (`38` exact, `15` `±1`, `108` omissions, `64` other), we ran a Numba-accelerated Bayesian log-likelihood-ratio (`LLR`) local alignment scanner (`500` permutations + BH-FDR) on: (a) the `4` unread Inkawasi khipus (`UR272, UR276, UR277, UR279`), and (b) all `30` out-of-sample khipus. Of `210` prefiltered candidate pairs (`LLR >= 8.0`), **0** survived `q_bh < 0.05` (minimum `q_bh = 0.2096`), establishing a bounded negative result even when `±1`, `×10`, and digit-transposition errors are explicitly rewarded.

In 10,000-replicate maximum-parsimony bootstrap tests across multi-witness families:
- **Inkawasi (`UR278, UR266, UR275`):** Across `12` rows present in both ledgers, `5` shared synapomorphies (`UR266 == UR275 != UR278`) yield **99.8%** bootstrap support for a lost intermediate ancestor `α` over independent derivation.
- **Leymebamba `F02` (`UR006, UR009, UR021`):** Across `4` informative variant sites, `UR009 = UR021` receives only **14.3%** bootstrap support (vs `49.8%` `{6,21}` and `15.0%` `{6,9}`), quantitatively confirming an unresolved star topology.
- **Costa Sur `F08` (`KH0049, UR122`):** **100.0%** support for the shared `15652/15649` conjunctive discrepancy alongside `12` missing/zeroed cords in `UR122`.

---

## 5. Limitations & Falsifiable Physical Predictions

All findings rest on published transcriptions and archival recording sheets without physical access to the textiles. At Inkawasi, KFG and OKR reflect one shared reading. To enable rapid physical falsification, we condense the highest-leverage checks into a 15-minute museum protocol (`analisis/paquete_revision/en/museum_protocol_5_knots.md`):
1. `UR278 p180` (`KH0517`): predict `6L` (`237`) rather than `7L` (`238`).
2. `UR266 p104` (`KH0502`): predict `7L` (`1737`, matching OKR) rather than `2L` (`1732`, Urton 2017).
3. `UR275 p51` (`KH0514`): predict broken tip or missing `7L` after `4S = 40`.
4. `UR234 p41` (`VA66837`): predict broken stump / traces consistent with `2016` preserved in `UR1104`.
5. `KH0049 p19` (`MNAAHP 3550`): confirm `15652` (`2L`) on the object, matching `UR122`.

---

## 6. Data, Code, and Browser Tool Availability

All scripts, CSVs, verification suites (`analisis/paquete_revision/verificar.py`, `19/19`; `lector/verificar.py`, `21/21`; `articulo/fuente/comprobar.py`), the interactive essay (`articulo/index.html`), and the standalone **682-khipu browser Khipu Reader** (`articulo/lector.html`, zero server required, supporting custom CSV drag-and-drop) are openly available at `https://github.com/dariodemh/quipus` (code/data under MIT; texts under CC BY 4.0).

---

## References

- Ascher, M., & Ascher, R. (1978). *Code of the Quipu Databook*. University Microfilms.
- Chirinos Rivera, A. (2010). *Quipus del Tahuantinsuyo*. Editorial Commentarios.
- Chirinos, A. (2026). The “Waterfall” Khipu Set and Indigenous Political Organization in the 16th Century. *The Khipu Field Guide Blog*.
- Contreras, M. (2026). Structural Pattern Mining in Inka Khipus. arXiv:2607.00185.
- FitzPatrick, M. (2024). New Insights on Cord Attachment and Social Hierarchy in Six Khipus from the Santa Valley, Peru. *Ethnohistory*, 71(4), 443–469.
- Florio, C., & Overmann, K. A. (2025). Inka numbers, khipu, and yupana: a reanalysis. *Journal of Cognition and Culture*, 25(1–2), 128–158.
- Hyland, S. (2017). Writing with Twisted Cords: The Inscriptive Capacity of Andean Khipus. *Current Anthropology*, 58(3), 412–419.
- LeVine, T. Y. (Ed.). (1992). *Inka Storage Systems*. University of Oklahoma Press.
- Locke, L. L. (1912). The ancient quipu, a Peruvian knot record. *American Anthropologist*, 14(2), 325–332.
- Medrano, M., & Khosla, A. (2024). How can data science contribute to understanding the khipu code? *Latin American Antiquity*, 36(2), 497–516.
- Pärssinen, M. (1992). *Tawantinsuyu: The Inca State and Its Political Organization*. Societas Historica Finlandiae.
- Platt, T. (2002). “Without Deceit or Lies”: Variable Chinu Readings during a Sixteenth-Century Tribute-Restitution Trial. In *Narrative Threads*, Univ. of Texas Press.
- Shukla, Makwana, & Gupta (2019). Determination of Some Engineering Properties of Groundnut Pod. *Int. J. Curr. Microbiol. Appl. Sci.*, 8(2), 3025–3030.
- Sivan, J. (2026). Reading the Inca Spreadsheet. Zenodo:19184002.
- Urton, G. (2005). Khipu Archives: Duplicate Accounts and Identity Labels. *Latin American Antiquity*, 16(2), 147–167.
- Urton, G. (2017). *Inka History in Knots: Reading Khipus as Primary Sources*. University of Texas Press.
- Urton, G., & Brezine, C. J. (2005). Khipu accounting in ancient Peru. *Science*, 309(5737), 1065–1067.
- Urton, G., & Chu, A. (2015). Accounting in the King's Storehouse: The Inkawasi Khipu Archive. *Latin American Antiquity*, 26(4), 512–529.
- Urton, G., & Chu, A. (2018). The Invention of Taxation in the Inka Empire. *Latin American Antiquity*, 30(1), 1–16.
