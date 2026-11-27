# Errata Report for OKR (v2.1.0) and KFG (v2.1.0)

Technical summary of verified inconsistencies, duplicate records, and encoding discrepancies across the two open khipu databases, ready to file as upstream issues.

---

## 1. KH Number Collisions and Shifted Files in KFG (`KFG_DB_Excel/`)

| ID / File | Verified issue | Evidence |
|---|---|---|
| `KH0197.xlsx` | Spreadsheet holds a different khipu record; collides with `UR1180` | `analisis/17_okr_pendientes/informe.md` §1.4; `findings_table.csv` (`C26`) |
| `KH0227.xlsx` | KH collision: assigned to both `KH0227` (221 cords, Huaura) and `AS207C` (14 cords, `C14459`) | `17_okr_pendientes/puente.csv`; `summary_for_specialists.md` §5.9 |
| `KH0267.xlsx` | KH collision: `KH0267` (22 cords) and `UR034` (188 cords) share the same KH number | `17_okr_pendientes/informe.md` §1.4 |
| `KH0350.xlsx` | KH collision: `KH0350` (55 cords) and `UR114` (260 cords) share the same KH number | `17_okr_pendientes/informe.md` §1.4 |
| `UR044.xlsx` | Incomplete duplicate of `AS031 / KH0033` (66 cords, flagged duplicate in OKR) | `khipu_summary.csv` has 650 rows (excluding `UR044`) vs 651 `.xlsx` files |
| `KFG_DB.SQL` vs CSV/XLSX | `khipu_main` in SQL has **685** rows, `KFG_DB_Excel/` has **651** `.xlsx`, `khipu_summary.csv` has **650** | Exact 650 + 35 reconciliation in `17_okr_pendientes/informe.md` §1.5 |

## 2. Unflagged Physical Duplicates and Museum-ID Collisions

* **`UR1107` (`KH0121`, Berlin `VA24370(B)`) = `UR237` (`KH0473`, Berlin `VA66834`):** match on **23 of 26** knotted cords in reverse order (cord-length correlation `r = 0.99`), while **0 of 23** color labels match (`analisis/14_copias/verificacion_UR1107_UR237.csv`). They represent two independent readings of the same physical khipu from opposite ends; the museum inventory recorded on `KH0473` (`VA66834`) conflicts with `VA24370`.
* **`KH0676` (`JS01`, Brooklyn `36.718`) vs `KH0700` (`SB001`):** inventory number `80.1012 aka 2708` appears assigned to both `KH0676` and `KH0700` (`17_okr_pendientes/informe.md` §1.6).

## 3. Systematic Cords Omitted in KFG Relative to OKR (`khipu.db`)

* **Missing Inkawasi cords:** KFG omits **111 cords** present in OKR at Inkawasi, including **58 cords of `UR256`** and **32 subsidiaries of `UR274B`**.
* **Top cords and markers:** KFG omits **92 of 95** level-1 top cords and **502 of 502** marker cords; any analysis of top-cord (`T`) or marker structure must query `khipu.db`.
* **Value discrepancies:** KFG and OKR agree on **99.33%** of comparable knotted cords, but **86%** of discrepancies cluster in five khipus (`UR090`, `UR144`, `UR235`, `UR193`, `UR190`), half of them factor-of-10 decimal shifts.

## 4. Internal Inconsistencies in OKR (`data/khipu.db` and Pending Folders)

* **`AS001–AS009` outside `khipu.db`:** those nine khipus sit exclusively in `KH0002_0010/AS1-AS9.db` (`681` cords, `1,872` knots) and are absent from `khipu.db` (`619` khipus).
* **Unintegrated records:** `83` KH numbers in `okr-kh-numbers.csv` (`702` actual rows) are absent from `khipu.db`; `19` exist as convertible `.xlsx` spreadsheets (`cuerdas_extra.csv`, `776` cords) and `11` (`KH0653–KH0663`, Huacones `JC024–JC034`) only as JPG recording sheets (`analisis/35_huacones_virgenes/`).
* **Broken UTF-8 in `okr-kh-numbers.csv`:** contains `U+FFFD` replacement characters and embedded newlines inside quoted fields (`761` physical lines for `702` rows).
* **Arithmetic erratum on `JC028_record.jpg` (`KH0657`, cord `p5`):** additive knots `4L + 2L + 2L + 5L` sum to **13**, while the handwritten `value` column records **12**.
