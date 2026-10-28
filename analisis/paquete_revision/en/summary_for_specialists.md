# Computational analysis of the khipu corpus: summary for specialist review

*Open to specialist review, 18-10-2026. Not yet peer reviewed; corrections are welcome as [issues](https://github.com/dariodemh/quipus/issues). Spanish original: [`../resumen_para_especialista.md`](../resumen_para_especialista.md).*

## 0. One-page overview

We ran the entire digital khipu corpus (about 650 objects, 57,818 cords) through statistical tests using permutation nulls and multiple-comparison correction. The main result concerns the archive of Inkawasi (Incahuasi, Cañete):

- **Well supported.** In the heap of fourteen peanut-covered (maní) khipus from the kallanka (great hall) of sector A, there is a **three-level consolidation**:
  - the pendant cord plus the first subsidiary cord of UR270 give, column by column, the cells of the 9-column table of UR278;
  - the row totals of UR278 reappear, in the same order, as the headers of the books UR275 and UR266.

  Neither of these two relations is published. Both were recovered in a blind test on anonymized data.
- **Supported, not well supported.** The tied pair UR273A/UR273B, summed record by record, reaches the same headers by a second route.
- **Already published, replicated here only:** the fixed quotas 10, 15, 47 and 208, and the copies UR255≈UR267A, UR256≈UR267B and UR266≈UR275 (Urton and Chu 2015, 2018; Urton 2017).

Outside Inkawasi, the results are mostly negative or methodological:

- the figure of 74% of khipus with sums is not informative;
- there is no shared color lexicon;
- there is no trace of syllabic text;
- the colonial genre templates do not exceed chance.

Some archival formats also appear, such as the tied set UR053A–E with a stable W/R/AB allocation, and a list of errata in the databases.

**Why we are writing to you.** What we cannot do from the data is examine the objects and the documents. KFG and OKR, for Inkawasi, are two encodings of **the same reading**, made by the same transcriber. We attach frozen predictions that only someone with access to museums, photographs or archives can test (`verifiable_predictions.md`).

## 1. Data

- **KFG** (Khipu Field Guide, data from the article by Medrano and Khosla 2024; Zenodo v2.1.0): 651 khipus and 57,818 cords. We use 650, because UR044 is a duplicate of AS031/KH0033. Each cord records its knot chain, value, color, ply/twist direction, attachment (R/V), length and termination. In 57,789 cords the value is exactly the sum of the knots' contributions.
- **OKR** (Open Khipu Repository, Zenodo v2.1.0; `khipu.db` with 619 khipus and 702 KH numbers). We use it to cross-check KFG and, for Inkawasi, as the preferred base: KFG loses 111 cords from that archive, among them 58 of UR256 and 32 subsidiary cords of UR274B. We also recovered 19 khipus from xlsx/PDF sheets that are not in the databases (776 cords).
- **KFG–OKR agreement:** 99.33% of values identical. 86% of the discrepancies are concentrated in five khipus (UR090, UR144, UR235, UR193 and UR190), and half of them are factor-of-10 errors.
- **Textual sources checked** (full text unless otherwise indicated):
  - Urton and Chu 2015 with its supplement, Urton and Chu 2018 (English and Spanish), Urton 2017 (ch. 9 and appendix) and Urton and Brezine 2005;
  - Medrano 2019 (thesis) and Medrano and Khosla 2024;
  - Pärssinen 1992 and the introduction of Pärssinen and Kiviharju 2004;
  - Rostworowski, *Costa peruana prehispánica*, and Espinoza Soriano 1963 (the *visita* (colonial inspection and census) of Martínez Rengifo, 1571);
  - Hyslop 1985, LeVine (ed.) 1992, Salomon 2004, *Narrative Threads* 2002, Hyland 2017 and Curatola and de la Puente 2013;
  - FitzPatrick 2024 and Chu 2015–2018.
- **Limits of the data.** The `alt` column is empty. KFG loses almost all level-1 top cords (92 of 95) and all marker cords (502 of 502), so the analyses of top and marker cords were carried out with OKR. We have not examined any object.

## 2. Methods

1. **Permutation nulls adapted to each question.** Values are shuffled within the level, the group or the magnitude class, depending on what is being tested. We learned this from an error of our own: a null that "substitutes a value from the corpus" inflates any sum, and one that shuffles across khipus leaves copies intact.
2. **Multiple-comparison correction.** Holm or Benjamini–Hochberg over the full family of tests. When a rule was chosen by looking at the data (how to align, which pair to test), we count all the possible variants ("garden of forking paths"). The red team recalculated the A+B relation this way over 58,782 tests.
3. **Exploration and confirmation halves,** and cross-validation by blocks of records.
4. **Blind test.**
   - 52 khipus from Inkawasi were anonymized (Q01–Q52), 15% of the knotted cords (597) were hidden, and language models with no access to the literature were asked to predict values and look for relations.
   - Afterwards, in targeted tests, the rule, the null and the correction were fixed in writing before the data were opened.
   - The answers were scored without giving feedback to the model.
5. **Positive controls.** Every detector was first tested on known relations, to measure its power:
   - the Puruchuco hierarchy of Urton and Brezine (2005), which the method reproduces literally, including the discrepancies 2904/2908 and 161/162;
   - the copies published by Urton (2005);
   - UR006/UR009/UR021;
   - the Santa *padrón* (census roll);
   - artificially inserted lists.

   Several negatives are interpreted as "not detectable with this power" and not as "does not exist".
6. **Preregistered predictions** before looking at the data that test them. For example, the ceque hypothesis (ceques: the radiating lines of Cusco) for UR050 + UR055 was registered beforehand and failed its three predictions.
7. **Evidence scale.**
   - **Well supported:** survives the null and the correction, and was replicated by an independent route (another script, another agent or a blind test).
   - **Supported:** significant with correction, but without an independent replication, or fragile to the choice of rule.
   - **Proposed:** compatible with the data, with no test that distinguishes it from alternatives.
   - **Speculative:** no test.

## 3. Findings by level of evidence

Bracketed identifiers refer to `findings_table.csv`.

### 3.1 Well supported

**Inkawasi, sector A, peanut heap (U.A. 4, U.E. 11–22).**

- **[I01] UR270 → UR278, cell by cell.** The pendant cord plus the first subsidiary cord of UR270 match the cells of one row of UR278, in the same column order.
  - Five of twelve groups have 6–9/9 matches, and two match 9/9: group g0 of UR270 with g21 of UR278 (237, 295, 138, 198, 201, 153, 106, 138, 187) and g4 with g25.
  - With the pendant cords alone, no group reaches 6/9 (p = 0.0002).
  - It was replicated by an independent script and by manual review. A blind model, without knowledge of the identity of the khipus or of our rule, found the same relation with the same rule (p ≈ 3·10⁻¹⁰).
- **[I02] UR278 → UR275 → UR266.** The row totals of the 9-cord rows of UR278 reappear, in the same order, as headers.
  - In the white pendant cords of UR266: 11 exact matches against 0.4–0.5 expected (Holm 1.6·10⁻⁹; ρ = 1).
  - In the group totals of UR275: 7 against 0.5 (Holm 2.8·10⁻⁴).
  - Examples: 3618 (= 415 + 415 + 353 + 415 + 415 + 415 + 414 + 413 + 363), 1506, 1384, 2919, 2089, 2950, 1278.
  - The relation was confirmed in a targeted blind test, with the rule frozen in advance.
- **[I09–I10] The 9 columns are 9 units with fixed identity.**
  - They are the same 9, in the same order, in UR270 and UR278: the identity is the best of the 9! permutations across the 5 comparable records.
  - Their flatness is exceptional in the corpus. The CV between column means is 0.17–0.19 depending on the definition, and 7 of the 8 groups of 9 cords with CV < 0.2 in the whole corpus belong to UR278.
- **[I06, I18] We replicate what was published:**
  - the fixed quotas 10, 15, 47 and 208, with the formula "total = fixed + remainder";
  - the copies UR255≈UR267A, UR256≈UR267B and UR266≈UR275.

**Rest of the corpus.**

- **[C03] Top cord = sum of the immediately preceding group:** 23 of 72 against 2.4 expected (Holm 0.0035). The phenomenon has been known since Locke. What is new is that the sum corresponds to the preceding group and not to an arbitrary one.
- **[C04] "Row + loose total cord" format:** 51 hits against 14.9 (p = 0.0005), with seven significant khipus (AS044, AS066, AS199, UR1096, UR118, UR119 and UR166).
- **[C06] Color works as a category with a local key.**
  - It predicts magnitude within the khipu in 167 of 403 (about 20 expected), and in 103 even when color is shuffled within each group.
  - There is no shared lexicon between khipus or between sites (p = 0.34 and 0.79).
- **[C24, C26] Data.**
  - Copies between museums not noted in the literature we reviewed; for example, HP055 (Lima) ≈ UR1084/AS084 (Paris), with 121 of 142 cords exact.
  - Specific errata in the databases. Four KFG files (KH0197, KH0227, KH0267 and KH0350) actually contain the following khipu. KH0676 is Brooklyn 36.718, not 80.1012. UR1107 and UR237 are the same object recorded in reverse.

### 3.2 Supported

- **[I03] Tied pair UR273A + UR273B.** Aligned by group number (the pink separators fall in the same groups), their sums give 8 of 18 exact headers of UR266, UR275 and UR269 (2950, 1653, 1737, 1827, 1780, 2247, 1765 and 1506; 1.27 expected).
  - It survives correction for the choice of rule (p = 0.015) and the split into halves (5/9 and 3/9; Holm 0.016).
  - In the targeted blind test over 132,600 triads, the pair ranks among the top five, but does not pass the Holm correction (0.93).
  - **Level: supported, not well supported.** It converges with [I02]: the sums A+B and the rows of UR278 fall on the same totals.
  - **[I04]** When UR273A is blank, UR274A takes its place in 3 of 4 records (p = 0.00013).
- **[I11–I14] Profile of the 9 columns.**
  - It is unequal and ordered from largest to smallest (Spearman −0.73; p = 0.025).
  - It does not behave like demography or like time: the CV is too low for a pyramid, and there is no seasonality.
  - Its proportions predict unseen rows (Holm 0.002).
  - Of the nine colonial lists of 9 units that we compared, the only one that declines like UR278 is that of the **9 pachacas (decimal subunits of a guaranga) of the guaranga (a unit of about 1,000 tributaries) of Bambamarca** (*visita* of González de Cuenca, 1567, according to table 2 of Pärssinen 1992): ρ = −0.87 (Holm 0.005). Bambamarca is more unequal: CV 0.39 versus 0.19.
- **[I15] Pairing according to the curacas (local lords) of Guancayo (Chillón, 1571).** The order of the curacas (2+1+2+2+2 pachacas) predicts pairs of columns with 11 exact equalities against 4 (p = 0.0003). There is no covariation (r = 0.09), and if the 945 possible pairings are counted, p rises to 0.086. **Supported, fragile.**
- **[I08] The quota is absolute, not proportional.** 47 represents between 1.1% and 4.2% of the record; the "~2%" of Urton and Chu 2018 is an average.
- **[I16–I17] Blind prediction.**
  - Leaving out one cord at a time, the model predicts exactly 58.8% of the predictable cords, against 20.5% for the best baseline.
  - In the cords that did not take part in the discovery, the advantage almost disappears: 17.5% against 15.1%.
  - In the blind test, a model predicted 68 hidden cords with 82% exact matches, and it was well calibrated.
  - Honest reading: **we read the arithmetic of the chain, not the whole file or its content.**
- **[C07] Tied set UR053A–E** (Banco Central de Reserva). The five khipus distribute the three cords W / R / AB in similar proportions, close to 4:1:1 (W between 0.57 and 0.70), although their totals range from 1,200 to 36,800. W is the largest of the triad in 13 of 14 triads (UR053A) and in 23 of 23 (UR053D). It is not a sum. It is a second case, independent of Inkawasi, of "archive form with a stable allocation key".
- **[C09] Positional zeros.** In 726 cords with an internal zero, the gap measures one decimal band (median 0.96; 1.89 times the band width within the same cord; p = 6·10⁻³³). It is evidence against the non-positional thesis of Florio and Overmann (2025), with one caveat: the assignment of value to the knots is partly circular.
- **[C10] The cord wrappings/sleeves are the attachment system.** 97.6% of the cords lie within a cord wrapping/sleeve, with about 4 pendant cords per wrapping/sleeve. In UR052, 23 of 24 group boundaries coincide with wrapping/sleeve boundaries (p = 5·10⁻⁵), but this is a single object.
- **[C01–C02] The 74% of khipus with sums (Medrano and Khosla) is not informative.**
  - Between 93% and 100% of the KFG relations are expected by chance.
  - The metric has only 24% power.
  - Only about 20 khipus (3%) have verifiable internal accounting.
- **[C12, C13, C14, C18, C19, C23] Well-supported negatives.**
  - There are no mirror halves.
  - Only 100 is overrepresented as a value.
  - The pairing of the 1670 Santa *padrón* does not survive a correct null (p = 0.24). In addition, FitzPatrick's p = 0.03 is the best of 20 alignments.
  - Cords do not behave like text, and Sivan's syllabary fails its own predictions.
  - Non-numerical khipus have alphabets of 5 to 19 colors, far from the 60–120 signs of a syllabary.
  - No ancient khipu reaches Collata's sign inventory.

### 3.3 Proposed or speculative

- **[I07] Quotas that add up in the consolidation:** 30 + 17 = 47, and 15 + 10 = 25. The 17 is explicit in UR274B (with OKR, p = 0.004) but barely appears in UR273B. The relation UR267A + UR267B → UR269, which underpinned the 25, **did not** pass out-of-sample tests.
- **[I20] Attachment R/V opposed in the two halves of each tied pair.** It holds in the three Inkawasi pairs, but in the corpus only in 6 of 14 A/B pairs (p = 0.16). It is a proposed archive convention.
- **What the 9 columns are.** We propose 9 pachacas or subunits of a guaranga, ordered by rank or size. No 9 is documented in Lunahuaná or Guarco. "P = quota, S1 = delivery" in UR270 is under test.
- **Unit.** Open, with two hypotheses that the data do not separate: **carga** (load, an Andean unit; ~80 L, ~23 kg; slightly preferred, proposed) and **fanega** (Castilian unit of dry measure; ~56 L, ~16 kg). The capacity of the storerooms only excludes very small units. The total would be **~900–1,400 t**, an order of magnitude only (10²–10³ t). We give no firm figure: it depends on the unit.
- **UR050** would be a table of 163 rows × 3 zones at fixed relative heights, compatible with subtype B1-b of Mackey.
- **UR1140** (Berlin, Nazca) would be a card with 7 fields.

### 3.4 Findings from rounds 17–18 (outside Inkawasi, except the mismatches)

**A hierarchical table on the south coast: KH0049.** *Supported (post hoc).*

- KH0049 (AS038/HP036, Museo Nacional, Lima, MNAAHP3550, south coast) is a **three-level table in blocks of 18 cords**: B0 = B1 + B2 at 14 of 18 exact positions, and B1 = B3 + B4 + B5 at 7 of 18 (the null gives at most 6 and 4; p = 5·10⁻⁵).
- UR122 (Göteborg, 1938.45.0228) is a partial copy: the subtotal section, with 58% of the cords broken or at 0.
- The discrepancy **15652 versus 15649** is present in both copies; it comes from the original.
- **Publication.** Partial: the Khipu Field Guide lists 15 indexed sums of KH0049 as automatic output, without describing the hierarchy or UR122 (`analisis/30_frontera_estructura/novedad_kh0049.md`). We have not been able to read Ascher and Ascher 1978 or Pereyra Sánchez 2011.
- It is a second case of "column total" outside Inkawasi.

**Two-color alternation.** *Well supported in UR040 and UR167 (Holm 0.025); supported in UR1033F (q 0.010).*

- Pairs of two-colored cords interleaved (A/B/A/B), the only structure of the 180-khipu frontier set that was replicated in the confirmation half (q 0.003). It is read as a two-column table written in interleaved form.
- There are 19 such khipus in the corpus; 15 were already TAB/FOR. In UR040 and UR167 the values are almost all 0 or 1: the format is secure, the content is not.
- Of the 180 khipus in the frontier set, only 3 cease to belong to it (4 with KH0049). **The rest are decimal lists with no structure recoverable with these data.**

**New copy: UR1104 → UR234, a "one-field extract".** *Supported (post hoc); the strength is that of well supported.*

- UR1104 (AS104, Berlin, Pachacamac) reproduces in order the headers of nine records of UR234: 7 exact, one variant (3102 versus 3012) and the broken header of UR234 (2016). It is a summary that moves up a level, taking the major field of the Nazca/Berlin format.
- UR108 → UR231 is similar (5 of 6; proposed).

**Copying as an archival trait.** *Supported.* Within a site there are 10 pairs in 6,820; between sites, 6 in 72,980 (OR 17.9; p = 10⁻⁷). In nearly complete archives, 14–20% of khipus have a copy (5.5% in the corpus; a lower bound). Types: duplicate, partial copy, alternative breakdown and one-field extract. The direction is undecidable in almost all pairs.

**A lost intermediate book α between UR278 and UR266/UR275.** *Proposed.* The ±1 values shared by the two copies of the book indicate an intermediate step, not preserved, between the detail and the book (conjunctive error). Together with KH0049/UR122, it is one of the two firm points on copy direction.

**The UR278 mismatches are turn-counting errors.** *Supported (small n).* Of 18 rows with a destination, 11 are exact and 7 are not (39%). The mismatches (book − detail) are +6, +100, +1, −1, +1, −1, −1: no consistent direction (4+/3−). 6 of 7 fall on the units (p = 0.007; approximate null), the signature of a miscounted long knot, not of a convention (which would give a constant sign or magnitude). The two copies of the book agree on all of them: the difference arises in the detail → book step.

**"The largest cord opens the group" (P5c).** *Supported, new.* Outside Inkawasi, the largest value comes first in 25.9% of groups against 15.2% expected (Holm 0.002). In UR278 the columns are decreasing (tau −0.41; well supported).

**Balancing by two routes.** *Proposed, with a weak analogy.* It is not documented in Uruk or Pilos (Nissen, Damerow and Englund 1993). We treat it as a feature specific to Inkawasi. There is a documented parallel in the document hierarchy, the fixed format by type, and the copies.

**KFG and OKR are the same reading** (99.9% agreement in the UR khipus). The only independent readings are three duplicates of a single object, and they give a reading noise of 3–12%. This is an estimate based on few data.

## 4. What is new and what was already published

| New, unpublished (according to our review) | Already published and only replicated |
|---|---|
| UR270 → UR278 cell by cell; totals of UR278 → UR275/UR266; UR273A+B → books; UR274A substitutes for UR273A | Tied pairs with similar values; UR255/UR267A and UR256/UR267B; UR266≈UR275 (Urton and Chu 2015; Urton 2017) |
| Identity, flatness and ordered profile of the 9 columns; resemblance to Bambamarca; Guancayo pairs | UR278 "organized in sets of 9 cords" (2015 supplement) |
| The quota as an absolute value; quota 46; 30 + 17 = 47 as a sum | Fixed quotas 10, 15, 47 and 208; 17 and 30 considered and rejected (Urton and Chu 2018) |
| "Row + loose total" format; orientation of the top cord to the preceding group | Summing top cords (Locke 1927; Ascher and Ascher) |
| Stable W/R/AB allocation in the five khipus of UR053 | W/RL/AB pattern in all five and the UR53B/C pair with a different format and opposed R/V (Urton 2017, ch. 8) |
| KH0049 as a hierarchical table and UR122 as its copy; A/B/A/B alternation; UR1104 → UR234 (one-field extract); copying as an archival trait; "the largest cord opens the group" | Summing top cords and Ascher sums (Locke 1927; Ascher and Ascher 1981); in KFG, the automatic list of 15 sums of KH0049 |
| Zero = empty band; cord wrapping/sleeve = fixing; correct null for the Santa; errata in the databases; copies between museums | Color seriation in the Santa (FitzPatrick 2024); structure of UR006 (Urton 2017, ch. 4); Puruchuco hierarchy (Urton and Brezine 2005) |

**What we do not claim:**

- that there are accounting chains between khipus, published in Puruchuco and UR006;
- that the Inkawasi system is "exclusive": what is new is its **concrete architecture**;
- the fiscal interpretation of the quotas, which belongs to Urton and Chu.

The sources closest to each finding, and why they do not contain it, are in `prior_work.md`.

## 5. Corrections made along the way

1. **"74% is not distinguishable from chance" became "is not informative".** With power of ~24%, the metric neither proves nor refutes accounting.
2. **UR006.** We first said it did not reproduce Urton's structure. Counting the loop cords, it does: 24 pairs, 729 cords and 45 of 48 sums. The calendrical reading remains proposed.
3. **UR278 → UR266.** "16 of 33 in order" fell to 15 and then to 11, the figure replicated by the independent script and the blind test. Nor was it true that it was "the only relation between khipus in the corpus": the method reproduces Puruchuco.
4. **UR273A+B (H1)** fell from well supported to supported. **UR267A+B → UR269** fell to not well supported. **30 + 17 = 47** fell to proposed. The "position in the UR269 block" was withdrawn: it was explained by magnitude.
5. **UR270 → UR278 (H2)** rose from supported to well supported after the blind test.
6. **R/V attachment.** It went from "well supported code" to **proposed archive convention** (6 of 14 in the corpus).
7. **UR054/UR055 compensation, withdrawn.** Zones in centimeters gave p = 0.0002, but with heights relative to cord length, p rises to 0.76 and 0.44. Of that family, only UR050 is sustained.
8. **UR053B ≈ UR053C** is a copy already known, published by Urton (2017, ch. 8) and recorded in our critique of copies. An intermediate task said "they are not copies" because it compared by position.
9. **Santa.**
   - Our p = 0.0056 was circular; with the correct null it is 0.24.
   - The color seriation of the Santa khipus was already published by FitzPatrick 2024, so we withdraw it as a novelty.
   - KH0227 (Huaura) and UR198 (Nazca) had been wrongly assigned to the Santa by name.
10. **Copies and quotas already published.** We treated the Inkawasi copies and the quotas 10, 15, 47 and 208 as our own until we read Urton and Chu 2015 and 2018.
11. **Transcription error model.**
    - That a discrepancy can be repaired with a single knot change does not prove it is a transcription error: this occurs 31 times out of 35, against 28.3 expected.
    - The "copy ladder" 2433 → 2533 → 2633 loses strength, because 2633 also appears in UR269.
    - **Correction in this package:** the four "10" quotas of UR274B are not exactly the four shortest cords. They are among the five shortest: one measures 25.0 cm, and the shortest cord of the 17 quota measures 24.5 cm. The chance probability rises from 5.5·10⁻⁴ to about 3·10⁻³.
12. **Unit and tonnage of Incahuasi.** We had written "~1,390 t" and "82 L" with too much precision. The figure came from an 82 L *bulto* (load) that was only proposed (derived from the storeroom capacity, which gives 5,090 or 8,300–13,000 m³ depending on the calculation). The unit is undecidable between carga (~23 kg) and fanega (~56 L); the total is ~900–1,400 t, an order of magnitude only.
13. **"54% failures" of UR278 → book.** These were 13 of 24. There are 26 rows, 8 without destination; of the 18 with destination, 11 are exact and 7 are mismatches (39%).
14. **KH0049 and the novelty.** The question "is it published?" gives "partially": KFG lists its sums, but neither the hierarchy nor the copy. We keep "supported" because it is post hoc.
15. **Guancayo.** The 1571 visit concerns the Chillón valley, not the Wanka of Huancayo. Espinoza 1963 has numerical errors, and his list of "9 products" is an editorial selection, not a native template.
16. **Wooden rods (correction in this package).** One task presented as new that AS124, AS136 and AS140 were tied to carved wooden rods. Urton (2017, ch. 7) already describes between 12 and 15 khipus on rods of this kind, so we do not claim it.

## 6. What we ask of you

1. **Archaeological judgment.** Is it plausible that a heap of fourteen peanut-covered khipus contains three levels of one and the same flow, plus a book (UR269) organized by periods?
2. **Ethnohistorical judgment.** Is it reasonable to read the 9 columns as pachacas of a guaranga ordered by rank? Do you know lists of pachacas from Lunahuaná or Guarco?
3. **Physical or documentary checks** from `verifiable_predictions.md`. The cheapest:
   - UR278 p180: does the last long knot have 6 or 7 turns?
   - UR275 p51 and the four ends of UR274B: is the terminal 7L missing?
   - The order of the Bambamarca pachacas in the 1567 manuscript.

## 7. Verified figures for this package

We recalculated the following figures from `analisis/datos/cuerdas.csv` (KFG), without using the scripts of the tasks. The script is `analisis/paquete_revision/verificar.py` (15/15 correct).

| # | Figure | Result |
|---|---|---|
| 1 | R/V attachment | UR273A 83 V / 0 R; UR273B 113 R / 1 V; UR267A 82 V; UR267B 103 R |
| 2 | UR273A + UR273B by group number | 18 comparable records; 8 exact sums in the headers of UR266/UR275/UR269: 2950, 1653, 1737, 1827, 1780, 2247, 1765, 1506 |
| 3 | UR270 g0 (P+S1) versus UR278 g21 | 8 exact; the first cell differs by +1 (238 versus 237) |
| 4 | Row totals of UR278 in the pendant cords of UR266 | 11 exact in the same order (LCS); row g0 = 3618 |
| 5 | Quotas of UR274B | 12 cords of 17 and 4 of 10. Those of 10 measure 20.5, 22.5, 24.0 and 25.0 cm; the shortest cord of 17, 24.5 cm. Corrects the "exactly the 4 shortest" of `n_casi_aciertos`. |
| 6 | UR275 p51 | Value 40; there are 24 cords of value 47 |
| 7 | CV between column means of UR278 | 0.173 (24 complete rows; max./min. 1.64). The reports give 0.17–0.19 depending on the definition. |
| 8 | Bambamarca (104, 75, 78, 68, 49, 75, 67, 30, 27) | ρ = −0.870; CV = 0.385 |
| 9 | W/R/AB allocation in UR053A–E | A 0.67/0.18/0.15; B 0.57/0.26/0.17; C 0.61/0.23/0.16; D 0.66/0.16/0.18; E 0.64/0.18/0.18. The work log (SINTESIS.md, Spanish only) gives two values for A: 0.65/0.19/0.16 and 0.70/0.17/0.13. |
| 10 | KH0049, blocks of 18 | B0 = B1 + B2: 14/18; B1 = B3 + B4 + B5: 7/18 |
| 11 | 15652/15649 | KH0049 B1[1] = UR122 B0[1] = 15652; B3 + B4 + B5 = 15649 = B0 − B2 |
| 12 | UR122 at 0 where KH0049 has a value (p19–p36) | 12 positions; p21–p23 = 487, 281, 661 |
| 13 | UR1104 versus UR234 g0–g8 | 7 exact, 3102/3012, broken header 2016 |
| 14 | UR278 → book mismatches | 18 with destination, 11 exact, 7 mismatches (+6, +100, +1, −1, +1, −1, −1); 6/7 on units, p = 0.0069 |
| 15 | UR278 g29 | mismatch −1 (1507 versus 1506) |

**Checked against the source text** (Urton 2017, lines 1266–1491 of our text copy, which is not distributed): Urton already describes the UR53B/C pair, the change of format and the opposed R/V attachment. We treat it as published.
