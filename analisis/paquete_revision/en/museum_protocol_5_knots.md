# Museum Verification Protocol: 5 Knots in 15 Minutes

This protocol distills the **five cheapest, highest-leverage physical checks** from `analisis/paquete_revision/en/verifiable_predictions.md`. Each is a binary magnifier check on a specific cord that tests the core claims of the study without needing to re-transcribe an entire khipu.

---

## 1. UR278, cord `p180` (Inkawasi, Sector A · `KH0517`)
* **Where to look:** the terminal long knot on cord `p180` (group `g21`, column 1, white cord `W`, 50 cm).
* **Current reading (KFG/OKR):** `2S (4 cm) ; 3S (10 cm) ; 7L (19 cm) ; 1E (24 cm)` = **238**.
* **Question:** Does the long knot at ~19 cm have **6 turns (`6L`)** or **7 turns (`7L`)**?
* **Why it matters:** A single-turn change (`238 → 237`) resolves **two independent +1 discrepancies at once**:
  1. `UR270 g0` (`178 + 59 = 237`);
  2. row `g21`'s sum in the ledgers `UR266/UR275` (`1654 → 1653`).
* **Confirms transcription error:** `6L`. **Refutes (original difference):** clear, intact `7L`.

## 2. UR266, cord `p104` (Inkawasi, Sector A · `KH0502`)
* **Where to look:** the units cluster on cord `p104`.
* **Divergent readings:** Urton (2017) published **1732** (`2L`); the 2020 OKR re-import and KFG record **1737** (`7L`).
* **Question:** Does the terminal long knot have **7 turns (`7L`)** or **2 turns (`2L`)**?
* **Why it matters:** **1737** is one of the 8 exact sums linking the tied pair `UR273A + UR273B` (`448 + 1289 = 1737`, Finding 2) to the ledger `UR266`.
* **Confirms:** `7L` (`1737`). **Refutes that match:** `2L` (`1732`).

## 3. UR275, cord `p51` (Inkawasi, Sector A · `KH0514`)
* **Where to look:** the distal tip of cord `p51` (quota of record `g10`), right below the tens cluster (`4S = 40`).
* **Current reading:** `4S` = **40**, length **26.5 cm** (vs median **41.8 cm** across the other 24 quotas on this khipu, all equal to **47**).
* **Question:** Is the tip broken right below `4S`, or are remnants of a `7L` visible?
* **Confirms:** broken tip or `7L`. **Refutes:** intact tip with no units knot (genuine quota of 40).

## 4. UR234, `g5` header / cord `p41` (Berlin, `VA66837` · `KH0471`)
* **Where to look:** cord `p41` (recorded at **6.5 cm**, value `0`, broken).
* **Question:** Are any knot traces or archival notes consistent with **2016**?
* **Why it matters:** `UR1104` (`VA42527`, Berlin) extracts the `g0–g8` headers of `UR234` in order and records **2016** in that 6th slot.
* **Confirms:** broken stump compatible with missing knots / traces of `2016`. **Refutes:** intact unknotted cord or another value.

## 5. KH0049 (`AS038`/`HP036`), cord `p19` / `B1[1]` (MNAAHP, Lima `3550`)
* **Where to look:** cord `p19` (first cord of the second 18-cord block).
* **Current reading:** **15652** (identical to the Gothenburg partial copy `UR122`, `1938.45.0228`), while `B3 + B4 + B5` and `B0 − B2` both equal **15649**.
* **Question:** Does `p19` physically read **15652** (final `2L`) or **15649** (`9L`)?
* **Confirms shared conjunctive error:** `15652` on both physical khipus (`KH0049` and `UR122`).

---

## Quick Response Sheet

```text
Object / Cord         | Scale photo (Y/N) | Exact physical observation        | Verdict
----------------------|-------------------|-----------------------------------|------------------
UR278 p180 (KH0517)   |                   | 6L / 7L / unreadable / broken     |
UR266 p104 (KH0502)   |                   | 7L / 2L / unreadable / broken     |
UR275 p51  (KH0514)   |                   | broken tip / 7L / intact unknotted|
UR234 p41  (VA66837)  |                   | broken stump / traces / intact    |
KH0049 p19 (MNAAHP)   |                   | 15652 (2L) / 15649 (9L) / other   |
```

Scale photographs and results can be submitted as an issue at `https://github.com/dariodemh/quipus/issues`.
