# Preregistro P06 — Corpus numérico colonial ampliado y torneo de modelos generativos (v1.1 post-equipo-rojo)

- **ID:** `P06`
- **Fecha de congelación:** 2026-11-27 (revisión pre-hash tras auditoría adversarial con Claude Opus 5.5 Medium)
- **Semilla fija:** `20261127`

## 1. Fuentes coloniales congeladas y control de confusión `fuente = género`
Se extraerán tablas numéricas completas con verificación aritmética (`assert suma == total` donde exista total impreso) desde:
1. **Curatola y de la Puente (2013):** Castro de Trelles (Cuadros 2–7, Huamachuco 1611–1631 → `GANADO_INVENTARIO`, *etiquetado explícitamente como fuente única*), Medelius (Cuadros 1–3, Angaraes 1550–1571 → `TRIBUTO_TASA`), Lucanas-Laramati 1580–1581 → `TRIBUTO_TASA`.
2. **Chirinos Rivera (2010):** Cuadros 1.1–1.9, 2.1–2.7, 3.1–3.4, 6.1–6.4, 7.1–7.4 (huancas 1533–1561, Chucuito 1567, Paria 1565/1572, Chupaychu 1562, Aullagas 1548–1551 → `APORTE_INVENTARIO`, `TRIBUTO_TASA`, `PADRON_DEMOGRAFICO`, `SERVICIO_ASIGNACION`).
3. **Pärssinen (1992):** Tablas 2–10 (visitas de Chondal/Pomamarca, Asto Cacas, Coco, Chuquiapo, Caquiaviri, Aullagas/Quillaca, Cavana Conde, Yanque Collagua, Ocona → `PADRON_DEMOGRAFICO`; **Bambamarca queda EXCLUIDA de `P06.4`** por ser la observación que motivó la prueba).
4. **`11_rosetta/transcripciones_numeros.csv`** (deduplicado contra las fuentes anteriores).

**Regla de salvaguarda muestral (congelada antes de correr):**
- Si tras la extracción no se alcanzan **≥ 500 ítems numéricos** y **≥ 25 tablas independientes** cubriendo **≥ 4 géneros** (con ≥ 2 fuentes independientes para al menos 2 géneros), el Bloque `P06.1–P06.3` se degrada automáticamente a `EXPLORATORIO_N_INSUFICIENTE` y no se declara hallazgo confirmatorio.

## 2. Vector de 8 firmas congelado (invariante a color y transcriptor)
Calculado para toda tabla documental y todo quipu con ≥ 10 valores positivos:
`[log10_mediana, iqr_log10, frac_red10, frac_red5, cv_p95, frac_pequenos_le9, frac_repetidos, spearman_pos]`.

## 3. Controles positivos NO circulares congelados (tabla cerrada antes del hash)
*(Se excluye explícitamente `UR278` como control de `PADRON_DEMOGRAFICO` para evitar circularidad con Bambamarca).*
- **Control 1 (`ASG`, 28 quipus de `28_atlas_generos/atlas.csv`):** clase esperada = `SERVICIO_ASIGNACION` o `TRIBUTO_TASA`.
- **Control 2 (`PAD`, 6 quipus del Santa `UR087–UR092`):** clase esperada = `PADRON_DEMOGRAFICO` (evaluando las cifras de tributo/cabecera y colgantes por separado).
- **Control 3 (`TAL`, 28 quipus aditivos/tally de `atlas.csv`):** clase esperada = `FUERA_DE_DISTRIBUCION` (conteos unitarios pequeños fuera de tablas fiscales coloniales).
- **Frontera fija congelada para `P06.3`:** exactamente los **180 quipus** de `analisis/28_atlas_generos/atlas.csv` con `genero == 'SIN'` y `evidencia == 'decimal sin estructura detectada'`.

## 4. Familia confirmatoria congelada (Holm exacto sobre `m = 4` pruebas)

| Test ID | Pregunta | Método | Nulo / Control | Criterio binario |
|---|---|---|---|---|
| **P06.1** | **Separabilidad real entre géneros coloniales sin aprender autor/edición:** | Validación cruzada **Leave-One-Source-Out (LOSO)** en géneros multi-fuente + **Leave-One-Document-Out (LODO)** en el conjunto completo, con modelo generativo gaussiano regularizado (LDA/QDA bayesiano). | Permutación de etiquetas de género a nivel de documento/fuente (2 000 réplicas). | **Separables** solo si `balanced_acc_LODO ≥ 0,55` **y** `balanced_acc_LOSO ≥ 0,50` (en géneros multi-fuente) **y** `p_Holm < 0,05`. |
| **P06.2** | **Controles positivos NO circulares (tabla §3):** aplicar el modelo entrenado **solo en documentos coloniales** a `ASG`, `PAD` y `TAL` (con rechazo OOD si $p_{\chi^2} < 0,01$ de distancia de Mahalanobis). | Tasa de acierto exacta en los 3 controles positivos cerrados de §3 (ponderando igual cada control). | Permutación de etiquetas de género de los documentos de entrenamiento (2 000 réplicas). | Acierto medio ≥ 0,60 **y** `p_Holm < 0,05`. |
| **P06.3** | **Clasificación abierta (con rechazo OOD) de los 180 quipus de frontera:** | Asignación solo si `posterior ≥ 0,70` **y** $p_{\chi^2} \ge 0,05$. Calibrar **FPR** sobre 1 000 listas sintéticas sin género (log-normales y permutadas). | Tasa empírica de falsos positivos (`FPR`) en 1 000 sintéticos; contraste binomial de tasa asignada en los 180 quipus frente a `FPR`. | Reportar asignaciones como apoyadas **solo si** `FPR < 0,05` **y** la fracción asignada en los 180 quipus supera a `FPR` con `p_Holm < 0,05`. |
| **P06.4** | **Prueba ampliada de Predicción #17 (listas de pachacas/ayllus sin Bambamarca):** en todas las listas coloniales de ≥ 7 unidades de Pärssinen (1992) y Chirinos (2010) **excluyendo Bambamarca**, ¿descienden sistemáticamente de mayor a menor ($\rho < 0$)? | Mediana de $\rho(\text{tamaño}, \text{posición})$ y prueba de signos/Wilcoxon contra $\rho = 0$ sobre todas las listas independientes de ≥ 7 unidades (sin Bambamarca), más percentil exacto de `UR278` ($-0,73$; $CV = 0,173$) en esa distribución. | Permutación de posiciones dentro de cada lista (5 000 réplicas). | Si mediana $\rho < -0,30$ y `p_Holm < 0,05`: **«el descenso por tamaño es rasgo sistemático de listas andinas»** (refuta la excepcionalidad de Bambamarca, resolviendo Predicción #17); si no, el orden administrativo es de prestigio y no de tamaño (confirma Predicción #17). |
