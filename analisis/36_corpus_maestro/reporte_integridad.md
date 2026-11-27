# Reporte de Integridad — Corpus Maestro Unificado de Quipus (`KH####`)

- **Quipus totales unificados:** **689** (+ `KH0652` / `MNAAHP.15` con 19 hilos envueltos en `rt16905_k15_wrapped.csv`)
  - Base KFG distintos (sin duplicado `UR044`): **650**
  - **Cohorte `held_out` (nunca analizada en `quipus` v1):** **39 quipus (2414 cuerdas)**
    - OKR `khipu.db` ausentes de KFG: 3
    - Adjuntos OKR xlsx (`cuerdas_extra`: RT-16905 `KH0638–0651`, `SH001`, British Museum `KH0633–0635`, `KH0702`): 19
    - Adjuntos OKR transcritos de PDF/xlsx (`KH0674`, `KH0675`, `KH0676`): 3
    - Huacones-Vilcahuasi (`KH0653–KH0663`, fichas JPG): 11
    - Databook de Ascher genuinamente ausentes de KFG y OKR (tras resolver alias `UR1xxx` vía `puente.csv`): 3
- **Cuerdas totales unificadas:** **60969**
  - Con coordenadas perceptuales CIE $L^*a^*b^*$ (`ascher_color_dc`): **59033** (96.8 %)
  - Con geometría física 2D de OKR (posición de clúster o nudo en cm): **39676** (65.1 %)
  - Cuerdas superiores (`T`) rescatadas de OKR en quipus base: **248**
  - Cuerdas marcadoras (`M`) rescatadas de OKR en quipus base: **447**
  - Quipus base reemplazados por OKR preferente (4 desplazados + Inkawasi UR): **33**
  - Parches deterministas de valor de Thompson (2025a) aplicados en columna `valor_thompson` (sin sobrescribir `valor`): **19** (222 notas en 108 quipus AS en `thompson_2025_correcciones.csv`)
- **Hallazgo de conciliación Databook / `collca.db`:**
  - Los "80 quipus del Databook ausentes de KFG" de `ds/n_databook` eran en su mayoría colisiones de alias (`AS###` registrado como `UR1xxx` en KFG). Al resolver por `puente.csv` (`KH####`), los genuinamente ausentes de KFG y OKR son **3** (más los presentes solo en `khipu.db` como `AS086`, `AS130B`, `AS181`, `AS190`, `AS208`).
  - Entradas en `collca.db` sin cruce directo por alias simple (14): `AB001, AS090/N2, AS101 - Part 1, AS101 - Part 2, AS130 B, HP046 A, HP046 B, HP051 A, HP051 B, LL01, MA029 (1), MA29 (2), TEST4, UR1124 Detail 1` (en su mayoría variantes de nombre o sin fila en OKR).
