# Computational Structure, Three-Level Accounting, and Out-of-Sample Testing Across the Digital Andean Khipu Corpus (v2.0)

**Author:** Dario (`dariodemh`), with AI research agents (Gemini from Google, Claude Opus/Sonnet from Anthropic, and DeepSeek Flash)  
**Repository & Live Tools:** https://github.com/dariodemh/quipus · Interactive Essay, Visual Overview & Browser Reader: https://dariodemh.github.io/quipus/articulo/  
**Status:** Open preprint v2 for specialist review (not yet peer-reviewed). All statistics, controls, and reading sheets are deterministically reproducible from the public repository.

---

## Abstract

We present a reproducible statistical audit of the digitized Andean khipu corpus. Building on the Khipu Field Guide base (651 spreadsheets, 57,818 cords; 650 unique objects after removing duplicate `UR044`), we assemble a **Unified Master Corpus of 689 pendant khipus and 60,969 cords** (plus `KH0652` with 19 wrapped threads, 690 objects total), reconciling the Open Khipu Repository (`khipu.db` v2.1.0), the Ascher *Databook*, Karen M. Thompson's (2025) 222 structured corrections, 11 newly transcribed photographic recording sheets from Huacones-Vilcahuasi (`JC024`–`JC034`), and the physically tied `RT-16905` assemblage at the National Museum in Lima (Chirinos, Ghezzi & Álvarez, 2023). The corpus cleanly separates the 650 base khipus from **39 pure out-of-sample (`held-out`) khipus (2,414 cords)**. Using within-khipu permutation nulls, multiple-testing corrections (Holm and Benjamini-Hochberg), positive controls (Puruchuco and `KH0049`), blind testing on anonymized data, and six locally SHA-256-sealed protocols (`P01`–`P06`, consolidated into a public 98-test register), we report four main results:

1. **Three-level accounting architecture at Inkawasi:** Extending Urton and Chu (2015, 2018), the Sector A peanut pile shows a verifiable chain in which `pendant + first subsidiary` of `UR270` reproduces cell by cell the 9-column table of `UR278` (5/12 comparable groups with 6–9/9 exact matches; `p = 0.0002`; independently recovered in a blind run), whose row totals reappear in order as headers of `UR266` (11/18 exact, `Holm = 1.6×10⁻⁹`) and `UR275` (7 exact, `Holm = 2.8×10⁻⁴`). The tied pair `UR273A + UR273B` reaches 8/18 ledger headers by a second route (`p = 0.015` across 58,782 red-team combinations). Maximum-parsimony bootstrap (10,000 replicates) yields 99.8% support for a lost intermediate ledger `α` (`UR278 → α → {UR266, UR275}`) carrying shared unit-level errors (`±1`). Using the pre-Columbian Andean *carga* (~28 L, ~8 kg peanuts in the shell), `UR278`'s ~59,000 units correspond to roughly **~470 tonnes** (with the colonial Castilian *fanega* of ~16 kg serving only as a ~950-tonne upper-bound reference).
2. **Out-of-sample confirmations and two new internal-arithmetic cases (`P01`, `P03.4`, `E03.6`):** Across the 39 held-out khipus (strict Holm `m = 6`), both "largest cord opens group" (29/104 = 27.9% vs. 17.0%, `p_Holm = 0.0168`) and `A/B/A/B` alternation (5/16 vs. 0.16, `p_Holm < 10⁻⁴`) replicate. In addition, 53/174 OKR-rescued top cords (30.5% vs. 7.0%) exactly sum the preceding group (`p_Holm = 0.0010`), held-out khipu `KH0674` (Dumbarton Oaks) contains 8/41 groups with an exact summary cord (`p_Holm = 0.002`), and a post-hoc audit of `QU005` (Dallas) uncovers a third hierarchical column-sum table (`B2 = B0 + B1` in 12/19 exact positions and 13/19 within `±1`, `p_corr = 0.0001`).
3. **Label-free physical signals (`P04`):** Projecting color codes into continuous perceptual CIE `L*a*b*` space (96.8% of cords), lighter shades carry slightly larger values within each group even after excluding white `W` (`n = 225`, `med_rho = +0.0529`, `p_Holm = 0.012`). Segmenting groups purely by physical spacing gaps in centimeters (`k = 2.0`, without human group labels) replicates ordered intra-group trends in 9/35 khipus (`p_Holm = 0.00017`). However, PERMANOVA on 2D OKR geometry (`n = 148`) warns that recorder identity (`R² = 0.087`) accounts for as much variance as archaeological site (`R² = 0.085`; museum `R² = 0.272`).
4. **Methodological auditing and informative negatives (`P02`, `P03`, `P05`, `P06`):** Under within-khipu permutation nulls, 93–100% of simple sums counted by the published 74% figure arise by chance (detector power ~24%; only 14 khipus survive two shuffles). Across 726 zero-containing cords (727 gaps), the empty space spans 0.96 decimal bands (1.89× adjacent spacing in 201 cords, replicated out-of-sample in `UR-298` at 1.909×). Across `RT-16905` (15 physically tied khipus), all four tests of arithmetic hierarchy and numerical similarity are negative (`p_Holm = 0.25–0.81`). Across 1,190 colonial fiscal items (38 tables), a generative genre classifier collapses from `LODO = 38.2%` (`p = 0.0085`) to `LOSO = 5.0%` (`p = 0.9925`) with 53.7% synthetic false positives. Finally, auditing four 2026 computational studies under matched nulls shows that R/V entropy (0/39 under run-preserving nulls, `p_Holm = 0.587`), imperial twist classification (`F1: 0.241 → 0.048` under site-grouped CV; OKR 100% identical to `collca.db` in Santa), global color effects (`R² = 1.06%` vs. local key `16.0%`), and graph parent-child similarity (`z: 6.76 → 1.82`, `p_Holm = 0.126` when controlling group and scale) depend on permissive null assumptions, whereas aggregate pendant equality with the sum of its subsidiaries clears the null (`4.30%` vs. `2.75%`, `p_Holm = 0.003`).

**Keywords:** Andean khipus, Inkawasi, Huacones-Vilcahuasi, permutation nulls, quantitative stemmatology, computational archaeology, open data.

---

## 1. Master Corpus, Database Errata, and Virgin Transcriptions

- **Primary sources:** KFG v2.1.0 (edited and maintained by Ashok Khosla; 651 sheets, 57,818 cords; 650 unique objects excluding duplicate `UR044`), OKR v2.1.0 (`khipu.db`, 619 khipus, 54,403 cords), *Databook* (Ascher & Ascher, 1978), 222 structured corrections by Karen M. Thompson (2025, stored in parallel column `valor_thompson` without overwriting raw values), 11 Huacones-Vilcahuasi recording sheets (`JC024`–`JC034`, 101 cords), and `RT-16905` (14 pendant khipus + `KH0652` with 19 wrapped threads).
- **Reconciliation and errata (`C26`, `D01.6`):** KFG and OKR agree on 99.33% of comparable values (>99.8% at Inkawasi, reflecting one shared transcription); the three independent double-readings (`UR1107=UR237`, `KH0033=UR044`, `AS125=UR247`) set an empirical reading-noise floor of 0–12%. The Master Corpus restores 111 missing Inkawasi cords (including `UR274B = 133` cords), 248 top cords (`T`), and 447 marker cords (`M`), repairs four shifted spreadsheets (`KH0197`, `KH0227`, `KH0267`, `KH0350`), and resolves `AS↔UR1xxx` alias collisions (`UR1180`, `MM1086`), closing at **689 pendant khipus (60,969 cords)** with **39 pure held-out khipus (2,414 cords)**.

---

## 2. Methods, Sealed Protocols, and Empirical Calibration

All detectors apply within-khipu permutation nulls (preserving group, run-length, provenance, or magnitude strata), Holm or Benjamini-Hochberg correction, positive controls (`Puruchuco`, `KH0049`), shuffled negative controls, blind testing on 52 anonymized Inkawasi khipus, and six locally SHA-256-sealed protocols (`analisis/35_preregistros/MANIFEST_SHA256.csv`), reviewed before and after execution by Claude Opus with every deviation declared in `analisis/paquete_revision/paquete_zenodo_y_revista.md`. The five fast internal detectors of Reader v2 were calibrated on 100 shuffled synthetic khipus, yielding 0–1/100 false positives at the indication tier (95% CI upper bound 3.6–5.4%).

---

## 3. Additional Results and Measured Boundaries

- **Corpus formats and copies:** `KH0049` (`AS38`, hierarchy described by Ascher & Ascher 1978, partial copy `UR122` identified by Chirinos 2010; null test `p < 0.0001` and shared `15652/15649` discrepancy), `A/B/A/B` alternating tables (`UR040`, `UR167`), copying as an archival practice (`OR = 17.9`, `p = 10⁻⁷`, including `HP055 ≈ UR1084` and the `UR1104 → UR234` extract preserving `2016`), and the `UR053A–E` fixed-split form (with `P03.2` negative for direct `UR053E → B/C` sums, `p_Holm = 0.70`).
- **Huacones-Vilcahuasi, Bayesian stemmatology, and Prediction #17:** Prediction #13 is refuted (`JC024` has `CV = 1.283`, `JC031` mixes blanks with non-decimal additive knots; 4/10 knotted Huacones khipus and 99.27% of `JS01` use additive knot ordering). The error-tolerant Bayesian `LLR` scanner finds zero `q_bh < 0.05` links between the 4 unread Inkawasi khipus (`UR272`, `UR276`, `UR277`, `UR279`, `P03.3` negative) or held-out pieces and Sector A. Across 8 colonial demographic lists excluding Bambamarca (`P06.4`), median `ρ = -0.294` satisfies the conservative branch of the binary rule (`< -0.30`; 6/8 negative, `p_Holm = 0.004`), yet 0/8 match `UR278`'s slope (`-0.73`) or flatness (`CV = 0.173`).

---

## 4. Museum 5-Knot Protocol and Availability

The five decisive physical checks (`UR278 p180`, `UR266 p104`, `UR275 p51`, `UR234 p41`, `KH0049 p19`) are packaged in [`museum_protocol_5_knots.md`](../analisis/paquete_revision/en/museum_protocol_5_knots.md). All code, the 689-khipu Master Corpus, the 98-test register (`articulo/registro_pruebas.html`), the 18-slide visual overview (`articulo/overview.html`), the command-line Reader v2 (689 khipus), and the zero-server Browser Khipu Reader (`articulo/lector.html`, 682 indexed khipus) are openly available at `https://github.com/dariodemh/quipus` (MIT / CC BY 4.0).

---

## References

- Ascher, M., & Ascher, R. (1978). *Code of the Quipu Databook*. Ann Arbor: University Microfilms.
- Chirinos Rivera, A. (2010). *Quipus del Tahuantinsuyo*. Lima: Editorial Commentarios.
- Chirinos, A., Ghezzi, I., & Álvarez, F. (2023). *Description of RT 16905 MNAAHP (KH0638–KH0652)*. OKR / MNAAHP.
- Chirinos, A. (2026). The “Waterfall” Khipu Set and Indigenous Political Organization in the 16th Century. *The Khipu Field Guide Blog*.
- Contreras, M. (2026). Structural Pattern Mining in Inka Khipus. arXiv:2607.00185.
- Curatola Petrocchi, M., & de la Puente Luna, J. C. (Eds.) (2013). *El quipu colonial*. PUCP.
- Da Fieno Delucchi, A. (2025). *Khipu Computational Analysis Toolkit (K-CAT)*. GitHub.
- FitzPatrick, M. (2024). New Insights on Cord Attachment and Social Hierarchy in Six Khipus from the Santa Valley, Peru. *Ethnohistory*, 71(4), 443–469.
- Florio, C., & Overmann, K. A. (2025). Inka numbers, khipu, and yupana: a reanalysis. *Journal of Cognition and Culture*, 25(1–2), 128–158.
- Hyland, S. (2017). Writing with Twisted Cords. *Current Anthropology*, 58(3), 412–419.
- *khipu-rv-reproducibility* (2026). *Corpus-Scale Analysis of Binary Attachment Encoding in Inka Khipus: Reproducibility Package*.
- LeVine, T. Y. (Ed.) (1992). *Inka Storage Systems*. University of Oklahoma Press.
- Locke, L. L. (1912). The ancient quipu, a Peruvian knot record. *American Anthropologist*, 14(2), 325–332.
- Medrano, M., & Khosla, A. (2024). How can data science contribute to understanding the khipu code? *Latin American Antiquity*, 36(2), 497–516.
- Medrano, M., & Urton, G. (2018). Toward the Decipherment of a Set of Mid-Colonial Khipus from the Santa Valley. *Ethnohistory*, 65(1), 1–23.
- Pärssinen, M. (1992). *Tawantinsuyu*. Societas Historica Finlandiae.
- Platt, T. (2002). “Without Deceit or Lies”. In *Narrative Threads*, Univ. of Texas Press.
- Shukla, Makwana, & Gupta (2019). Determination of Some Engineering Properties of Groundnut Pod. *Int. J. Curr. Microbiol. Appl. Sci.*, 8(2), 3025–3030.
- Sivan, J. (2026). Reading the Inca Spreadsheet. Zenodo:19184002.
- Thompson, K. M. (2025). *Notes and Corrections to Aschers' Published Khipu Data*. University of Melbourne (figshare). DOI: 10.26188/30526775.
- Urton, G. (2005). Khipu Archives. *Latin American Antiquity*, 16(2), 147–167.
- Urton, G. (2017). *Inka History in Knots*. University of Texas Press.
- Urton, G., & Brezine, C. J. (2005). Khipu accounting in ancient Peru. *Science*, 309(5737), 1065–1067.
- Urton, G., & Chu, A. (2015, 2018). *Latin American Antiquity*, 26(4), 512–529; 30(1), 1–16.
- Zenil, H., & Uthamacumaran, A. (2026). Reconstruction of Geometric and Structural Aspects of Undeciphered Messages by Information-theoretic Methods. arXiv:2610.08861.
