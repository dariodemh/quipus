# Preregistro P01 — Validación confirmatoria en quipus *held-out* del Corpus Maestro Unificado (v1.1 post-equipo-rojo)

- **ID:** `P01`
- **Fecha de congelación:** 2026-11-27 (revisión pre-hash tras auditoría adversarial independiente con Claude Opus 5.5 Medium)
- **Semilla fija:** `20261127`
- **Principio:** Ninguna prueba de esta familia se ha corrido sobre los quipus recién integrados (`held_out == True`).

## 1. Definición de la cohorte *held-out* y exclusión NO circular de duplicados
- Un quipu entra en `held_out` si su identificador canónico `KH####` (o `AS###` sin `KH`) **no** corresponde a ninguno de los 650 quipus distintos de `analisis/datos/cuerdas.csv` (excluyendo el duplicado conocido `UR044 = KH0033`).
- **Regla anti-circularidad para duplicados físicos:** solo se excluyen pares cuyo **mismo objeto físico** conste por criterios **estrictamente no numéricos** (mismo museo y mismo número de inventario normalizado, o los tres duplicados físicos ya publicados/verificados antes de este preregistro: `UR044=KH0033`, `UR1107=UR237`, `AS125=UR247`). **Nunca** se excluye un par por similitud numérica.

## 2. Familia confirmatoria congelada (Holm exacto sobre `m = 6` pruebas)

| Test ID | Pregunta / Afirmación previa (`quipus`) | Estadístico exacto | Nulo emparejado | Criterio binario de confirmación |
|---|---|---|---|---|
| **P01.1** | **«La cuerda mayor abre el grupo» (`K08`)** en `held_out`. | Proporción de grupos (≥ 3 cuerdas con valor > 0, sin empates en el máximo y sin suma exacta interna) cuya primera cuerda es el máximo estricto. | Permutación de valores dentro de cada grupo (5 000 réplicas). | Exceso > 0 y `p_Holm < 0,05` (mínimo `n ≥ 15` grupos elegibles; si `< 15`, `SIN_POTENCIA`). |
| **P01.2** | **Ceros posicionales = hueco de una banda decimal (`C09`)** en `held_out`. | En cuerdas `held_out` con ≥ 3 racimos y un cero interno (salto de 2 órdenes decimales) con `START_POS` en OKR/`collca.db`: mediana de `hueco_cero / ancho_banda_contigua`. | Wilcoxon pareado del hueco del cero frente al ancho mediano entre bandas contiguas dentro de la misma cuerda. | Mediana en `[1,4; 2,5]` y `p_Holm < 0,05` (mínimo `n ≥ 10` cuerdas; si `< 10`, `SIN_POTENCIA`). |
| **P01.3a** | **Cuerda superior = suma del grupo anterior (`C03`) — Estrato puro `held_out`.** | Fracción de cuerdas superiores (`union='T'` o `CORD_CLASSIFICATION='T'`) en quipus `held_out` cuyo valor iguala exactamente la suma del grupo contiguo anterior. | Permutación de asignaciones cuerda superior ↔ grupo dentro del mismo quipu (5 000 réplicas). | Exceso > 0 y `p_Holm < 0,05` (mínimo `n ≥ 10` cuerdas superiores; si `< 10`, `SIN_POTENCIA`). |
| **P01.3b** | **Cuerda superior = suma del grupo anterior (`C03`) — Estrato separado de las cuerdas superiores recuperadas de OKR en quipus base** (que KFG omitía). | Mismo estadístico que P01.3a, restringido exclusivamente a cuerdas superiores presentes en OKR y ausentes en `cuerdas.csv` de quipus base (no contamina `held_out`). | Permutación de asignaciones cuerda superior ↔ grupo dentro del mismo quipu (5 000 réplicas). | Exceso > 0 y `p_Holm < 0,05`. |
| **P01.4** | **Alternancia cromática de desfase 2 (`K02`)** en `held_out`. | Fracción de quipus `held_out` (≥ 10 colgantes, ≥ 2 colores) que pasan el detector de alternancia desfase 2 con `p_bloque < 0,01`. | Nulo que conserva longitudes de racha de color por quipu (2 000 réplicas); contraste binomial unilateral contra tasa nula 0,01. | Exceso > 0 y `p_Holm < 0,05` (mínimo `n ≥ 15` quipus elegibles). |
| **P01.5** | **Copias hacia/dentro de `held_out` como rasgo de archivo (`K05`).** | Barrido Smith-Waterman log-odds (directo e inverso, tol ±1 nudo) con **nulo por rachas** (hasta 9 999 réplicas secuenciales) sobre todos los pares con al menos un miembro en `held_out`; contraste de `OR` (mismo sitio/museo vs distinto) entre los pares con `q_BH < 0,05` y ≥ 4 valores distintos. | Test exacto de Fisher unilateral (`OR > 1`) sobre los pares confirmados con `q_BH < 0,05`. | `OR > 1` y `p_Holm < 0,05` (si hay `< 3` copias nuevas confirmadas con metadato de sitio/museo, reportar pares y marcar `OR` como `SIN_POTENCIA`). |

## 3. Comprobación descriptiva de robustez (FUERA de la familia Holm `m = 6`)
- **D01.6 (control determinista de robustez, sin p-valor):** Recálculo de las 15 comprobaciones de `paquete_revision/verificar.py` tras aplicar los parches deterministas de Thompson (2025a) y las 111 cuerdas faltantes de Inkawasi en OKR. Regla: **ROBUSTO** si 15/15 comprobaciones conservan dirección y significación; cualquier cambio concreto se documenta en `test_register`.
