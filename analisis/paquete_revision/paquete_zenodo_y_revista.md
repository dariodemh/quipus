# Paquete de Depósito Zenodo v2.0.2 y Propuesta de Artículo Científico

**Proyecto:** *Lo que suman los quipus / What the Khipus Add Up To* (v2.0.2)  
**Repositorio fuente:** `github.com/dariodemh/quipus`  
**Fecha de cierre de análisis:** 27 de noviembre de 2026  
**Respuesta directa a la recomendación editorial de Manuel Medrano:** *"El análisis que compara la frecuencia de las sumas internas en los quipus con lo que cabría esperar por azar es bastante interesante, y contribuye al debate en curso sobre cómo los investigadores deberían abordar la evaluación de los patrones y propiedades numéricas en el corpus. Para una evaluación más exhaustiva, te recomendaría que consideres enviar tus hallazgos a una revista científica, de modo que un(a) especialista pueda evaluarlos más detalladamente."*

---

## 1. Arquitectura para Depósito Zenodo v2.0.2 (con DOI citable)

Siguiendo un estándar de reproducibilidad transparente (protocolos locales sellados con SHA-256, registro completo de pruebas positivas y negativas, código determinista con semilla fija `20261127` y calibración empírica de FPR), el paquete Zenodo v2.0.2 congela cinco artefactos trazables:

| Componente | Ruta en el repositorio | Descripción y verificación |
|---|---|---|
| **1. Manifiesto de protocolos congelados (SHA-256)** | `analisis/35_preregistros/MANIFEST_SHA256.csv` y `P01`–`P06` | 6 protocolos congelados localmente con SHA-256 *antes* de correr código (tras revisión adversarial con Claude Opus; no equivale a revisión por pares humana). El sello temporal externo queda fijado al depositar en Zenodo. |
| **2. Corpus Maestro Unificado v2 (689 quipus + KH0652 = 690 objetos)** | `analisis/36_corpus_maestro/maestro_quipus.csv`, `maestro_cuerdas.csv`, `thompson_2025_correcciones.csv` | 650 base KFG (excl. `UR044`, reparando los 4 desfases `KH0197/0227/0267/0350` y los alias `UR1180`/`MM1086`) + **39 quipus held-out puros con colgantes** (2,414 cuerdas; incluyen los 14 de RT-16905 y los 11 de Huacones-Vilcahuasi) + `KH0652` (19 hilos enrollados = 690 objetos) + 222 correcciones de Karen Thompson (2025) en columna paralela + CIE $L^*a^*b^*$ (96.8 %) + geometría 2D OKR (65.1 %). |
| **3. Registro Unificado de Pruebas (98 pruebas)** | `analisis/registro_pruebas/test_register.html`, `.json`, `.csv` | Buscador sin conexión con las 62 pruebas históricas (Rondas 1–19) + las 36 pruebas v2 (todos los ítems `P01`–`P06`, `E03.6`–`E03.7`, `D03.8`–`D04.5` ejecutados y cerrados), con igual prominencia para positivos, negativos y sin potencia. |
| **4. Lector de Quipus v2 + Calibración FPR** | `lector/lector.py`, `lector/detectores.py`, `lector/verificar.py`, `lector/calibrar_fpr.py` | 21 comprobaciones automatizadas + soporte de Corpus Maestro (689 quipus con colgantes) + calibración empírica de tasa de falsos positivos de los 5 detectores internos rápidos sobre 100 sintéticos (`calibracion_fpr.json`: 0–1/100 en "apoyado+", límite superior IC 95 % ≤ 3.6 %–5.4 %). |
| **5. Ensayo interactivo bilingüe y Resumen Visual** | `articulo/index.html`, `articulo/index.es.html`, `articulo/overview.html`, `articulo/overview.es.html` | Ensayo verificado (`comprobar.py`) + presentación visual de 18 láminas lista para exportar a PDF + lector interactivo en navegador (`articulo/lector.es.html`, 682 quipus indexados). |

### Metadatos recomendados para Zenodo
- **Título:** *What the Khipus Add Up To (v2.0): Null-Model Auditing, 689-Khipu Master Corpus, Frozen Protocols, and 2026 Literature Audit*
- **Tipo de recurso:** Software & Dataset / Working Paper
- **Licencias:** Textos y figuras bajo **CC BY 4.0**; código y tablas derivadas bajo **MIT** (las bases originales KFG, OKR y Databook conservan sus licencias respectivas y se citan por DOI; ningún PDF con derechos de autor se incluye en el depósito).
- **Fuentes primarias citadas con atribución estricta:**
  - **Ashok Khosla** (editor y mantenedor del *Khipu Field Guide*, KFG; Manuel Medrano citado como afiliado y coautor de Medrano & Khosla 2024).
  - **Andrés Chirinos Rivera** (2010, *Quipus del Tahuantinsuyo*, atribución explícita de las copias Lima-París `AS084/HP055` y Lima-Gotemburgo `AS038/UR122`, la proporcionalidad numérica, el registro de RT-16905 junto a Ghezzi y Álvarez 2023, y la entrada de 2026 sobre `UR053A–E`).
  - **Marcia y Robert Ascher** (1978, *Code of the Quipu Databook*, atribución explícita de la jerarquía de 3 niveles de `AS038/KH0049`).
  - **Gary Urton, Alejandro Chu, Carrie Brezine, Jon Clindaniel, Sabine Hyland, Martti Pärssinen, Marco Curatola & José Carlos de la Puente, Karen M. Thompson (2025)** (222 correcciones estructuradas al *Databook*, DOI `10.26188/30526775`).

---

## 2. Propuesta de Manuscrito para Revista Científica Revisada por Pares

### Revistas objetivo (en orden de encaje)
1. ***Latin American Antiquity* (Cambridge University Press, prioridad 1):** allí se publicaron Urton & Chu (2015, 2018) y Medrano & Khosla (2024). El manuscrito responde directamente al debate metodológico abierto allí, con respeto explícito por las bases de datos y el trabajo previo.
2. ***Journal of Archaeological Science* (Elsevier, alternativa técnica):** encaje natural si se prioriza el marco metodológico general (modelos nulos quipu por quipu, auditoría unificada de 4 estudios computacionales de 2026, geometría 2D, CIELAB y calibración empírica de FPR).

### Título sugerido del manuscrito
> **Separating Accounting Structure from Chance in Andean Khipus: Null-Model Auditing, Out-of-Sample Replication, and a Unified Evaluation of Recent Computational Claims**

### Estructura recomendada (8 secciones, ~7,500–8,500 palabras)
1. **Introducción. El problema del "jardín de senderos que se bifurcan" en el corpus de quipus:** Por qué un corpus de ~650–689 objetos heterogéneos genera coincidencias aritméticas, cromáticas y de clasificación por azar si no se calibran modelos nulos que preserven la estructura interna (tamaño de grupo, rachas, procedencia y capturista).
2. **Corpus Maestro Unificado v2 (689 quipus con colgantes + `KH0652` = 690 objetos, 60,969 cuerdas) y reconciliación de bases:** Integración sin duplicados de KFG, OKR v2.1.0, *Databook* (reconciliando las colisiones `AS↔UR1xxx`), 222 correcciones de Karen Thompson (2025), RT-16905 y Huacones-Vilcahuasi; partición estricta en **650 base** y **39 held-out puros** (2,414 cuerdas, que incluyen los 14 de RT-16905 y los 11 de Huacones). Auditoría PERMANOVA de geometría 2D OKR (`D04.5`): capturista (`CREATED_BY`, `R² = 0.087`) y sitio (`R² = 0.085`) explican varianzas comparables, ambas por debajo del museo (`R² = 0.272`).
3. **Evaluación con modelos nulos quipu por quipu de las sumas internas (`C01–C04`, `P01.3b`, `P03.4`, `E03.6`):**
   - Precisión metodológica sobre la cifra publicada del 74 %: no separa señal de azar quipu por quipu (93–100 % reproducible bajo barajado, potencia ~24 %); la prevalencia verificable robusta es ~3 % (cota central 4–7 %), concentrada en archivos contables específicos.
   - Réplica confirmatoria sobre cuerdas superiores rescatadas de OKR (`P01.3b`: `53/174` exactas = `30.5 %` vs `7.0 %` / `12.2` esperadas, `p_Holm(m=6) = 0.0010`).
   - **Dos hallazgos estructurales adicionales:** `KH0674` (Dumbarton Oaks, held-out `P03.4`: `8/41` grupos con cuerda-resumen exacta vs `0.31`, `p_Holm = 0.002`) y `QU005` (Dallas, post hoc auditada `E03.6`: `B2 = B0 + B1` en `12/19` posiciones exactas vs `0.10` máx nulo, `p_corr = 0.0001`; barrido de copias en los 689 quipus: 0 copias confirmadas). Además, `D03.8` reproduce directamente sobre OKR `khipu.db` las 3 zonas relativas de `UR050` (`[0.211, 0.428, 0.761]`, `ΔBIC = 243.1`), y `E03.7` cierra en negativo los 4 quipus del British Museum (`0/4` sumas o copias).
4. **Arquitectura contable de doble vía en Inkawasi (`I01–I22`):** Cadena verificada `UR270 (P+S1) → UR278 (tabla 9 cols) → UR266/UR275` y segunda vía `UR273A+B` (escala de almacenamiento ~470 t bajo la carga precolombina de ~8 kg de maní en vaina, con cota superior colonial de ~950 t en fanegas), cierre negativo de los 4 quipus no leídos `UR272/276/277/279` (`P03.3`, `p_Holm = 1.0`), prueba de Huacones-Vilcahuasi (`P03.1`: `JC024` baja con `rho = -0.952`, pero `CV = 1.28`, no plano) y prueba sin Bambamarca de Predicción #17 (`P06.4`: bajo la regla binaria congelada `< -0.30`, la mediana observada `-0.2939` confirma formalmente la Predicción #17; a la vez, 6/8 listas son negativas con `p_Holm = 0.004`, pero `0/8` igualan la planitud `CV = 0.173` o la pendiente `-0.73` de `UR278`).
5. **Validación fuera de muestra y propiedades físicas independientes (`P01`, `P04`):**
   - En los 39 quipus held-out (Holm estricto `m = 6`): se confirman "la cuerda mayor abre el grupo" (`P01.1`: `29/104 = 27.9 %` vs `17.0 %`, `p_Holm(m=6) = 0.0168`) y la alternancia `A/B/A/B` (`P01.4`: `5/16` vs `0.16`, `p_Holm(m=6) < 10⁻⁴`).
   - Color perceptual continuo CIE $L^*$: señal pequeña pero significativa de luminancia × magnitud intra-grupo incluso excluyendo el blanco `W` (`P04.2`: `n = 225`, `med_rho = +0.0529`, `p_Holm = 0.012`; efecto muy pequeño en `AS = +0.0083`, mayor en `UR = +0.0595`).
   - Segmentación puramente física por huecos en cm (`k = 2.0`, sin etiquetas humanas de grupo): replica tendencias monótonas intra-grupo en `9/35` quipus (`P04.3`, `p_Holm = 0.00017`).
6. **Pruebas negativas de alto valor informativo (`P02`, `P03.2`, `P03.5`, `P06.1–P06.3`):**
   - **RT-16905 (`P02`, 15 quipus físicamente atados):** 4/4 pruebas negativas (`p_Holm = 0.25–0.81`). Estar atados físicamente no implica automáticamente jerarquía aritmética ni copia numérica.
   - **`UR053E → B/C` (`P03.2`)** y **bases mixtas tipo Damerow-Englund (`P03.5`):** negativos limpios (`p_Holm = 0.70` y `1.0`).
   - **Torneo generativo colonial (`P06.1–P06.3`, 1,190 ítems en 38 tablas):** demuestra cuantitativamente el espejismo `LODO` vs `LOSO` (`LODO bAcc = 0.382, p = 0.0085` colapsa a `LOSO bAcc = 0.050, p = 0.9925`), controles no circulares en `37.0 %` (`p = 0.261`), y fracasa bajo el criterio de `P06.3` al mostrar una tasa empírica de falsos positivos de **`53.7 %`** en 1,000 sintéticos (`45/148 = 30.4 %` en frontera, `p = 1.0`, muy por encima del límite `< 5 %`).
7. **Auditoría unificada de la literatura computacional de 2026 (`P05`):**
   - `khipu-rv-reproducibility` (`P05.1`, `FRAGIL_A_RACHAS`): de `17/39` significativos bajo Fisher-Yates a **`0/39`** bajo un nulo que preserva rachas (`p_Holm = 0.587`).
   - `Khipu-ML` (`P05.2`, `INFLADO_POR_SESGO_U_O_FUGA`; `P05.3`, `NO_INDEPENDIENTE_MISMA_FUENTE`): al excluir quipus con `>50 % U`, la torsión `S` es menor en sitios imperiales (`77.8 %` vs `93.4 %`), el F1 colapsa de `0.241` a `0.048` en CV agrupada por sitio, y OKR coincide al **100.0 %** con `collca.db` en el Valle del Santa.
   - `K-CAT` (`P05.4`, `PSEUDORREPLICACION_Y_CLAVE_LOCAL`; `P05.5`, `SENAL_REAL`): el contraste crudo de color × magnitud (`H = 1,076`, `p = 4.3×10⁻²⁰⁷` en 28,411 cuerdas) se explica por clave local (`R² = 16.0 %`) frente a léxico global (`R² = 1.06 %`); en cambio, `padre = Σ hijos` sí muestra señal agregada real (`4.30 %` vs `2.75 %`, `p_Holm = 0.003`), aunque `0` quipus individuales pasan BH.
   - Análisis de complejidad en grafos (`P05.6`, `EXPLICADO_POR_ESCALA_LOCAL`, arXiv:2610.08861): replicamos `AUC = 0.861` y `z = 6.76` (`p = 0.002`) bajo re-cableado `(quipu, fibra, torsión)`, pero al controlar `(quipu, grupo, magnitud)` cae a `z = 1.82` (`p_Holm = 0.126`), aislando el escalado decimal local como mecanismo.
8. **Conclusión y protocolo abierto para futuros quipus:** Uso de `lector/` v2 con FPR calibrada y depósito externo con sello temporal para protocolos futuros.

---

## 2b. Tabla de desviaciones declaradas respecto a los protocolos congelados P01–P06

*(Toda desviación respecto a los archivos sellados en `MANIFEST_SHA256.csv` se declara de forma transparente sin alterar los documentos originales congelados.)*

| Prueba | Protocolo congelado (`P01`–`P06`) | Ejecución real / corrección aplicada | Impacto en el veredicto |
|---|---|---|---|
| **Sello temporal** | Prerregistro con SHA-256 local | Los 6 archivos se congelaron localmente antes de ejecutar código, pero carecen de sello temporal externo previo y se ejecutaron sobre un corpus base ya conocido (solo los 39 held-out eran no vistos). | Se describe como **protocolo congelado localmente** hasta depositar en OSF/Zenodo. |
| **`P01` Holm** | Familia `m = 6` | El script inicial guardó `p_holm` sobre `m = 3` evaluables; el registro v2 y el ensayo reportan **`m = 6` estricto** (`P01.1: 0.0168`, `P01.3b: 0.0010`, `P01.4: < 10⁻⁴`). | Ninguno: las 3 pruebas siguen siendo significativas con `p_Holm < 0.02`. |
| **`P01.5`** | Hasta `B = 9,999` permutaciones | Se ejecutó con `B = 2,000` (piso `p = 5×10⁻⁴`, insuficiente para `q_BH < 0.05` sobre 17,766 pares). | Marcado explícitamente como `SIN POTENCIA (DESVIACIÓN B=2000)`. |
| **`P04.1`** | Mínimo 10 pares inter-transcriptor | Tras limpieza de alias quedaron 8 pares elegibles (con 8 pares intra-transcriptor de control). | Negativo global (`p_Holm = 0.456`); se reportan los 8 pares con detalle. |
| **`P04.3`** | Concordancia ARI + réplica T4 | Se ejecutó la prueba confirmatoria de réplica T4 (`9/35`, `p_Holm = 0.00017`); el estadístico auxiliar ARI queda pendiente. | No afecta al criterio confirmatorio principal de `P04.3`. |
| **`P06.2–P06.3`** | 28 `ASG` y 180 frontera | El filtro de `≥ 10` valores positivos deja `23/28` `ASG` y `148/180` quipus de frontera. | Ambos son negativos contundentes (`37.0 %`; `FPR = 53.7 %`). |
| **`E03.6` / `E03.7` / `D03.8`** | Barrido de copias `QU005`, British Museum (`E03.7`) y `UR050` OKR (`D03.8`) | Todos ejecutados y cerrados en `03_cerrar_flecos_P03.py` (`QU005` sin copias, BM `0/4` negativo, `UR050` OKR reproduce zonas `[0.211, 0.428, 0.761]`, `ΔBIC=243.1`). | Sin omisiones ni sesgo de reporte. |

---

## 3. Lista de verificación pre-envío (Checklist editorial)
- [x] Todos los protocolos `P01–P06` sellados en `MANIFEST_SHA256.csv` antes de ejecución.
- [x] Atribución exacta a Ashok Khosla (editor KFG), Manuel Medrano (afiliado KFG / coautor 2024), Andrés Chirinos (2010, 2023, 2026), Marcia y Robert Ascher (1978) y Karen M. Thompson (2025).
- [x] Todos los negativos, retiros y pruebas sin potencia publicados con idéntica visibilidad en `test_register.html`.
- [x] Declaración transparente de autoría asistida por IA (Gemini, Claude Opus/Sonnet y DeepSeek Flash, auditoría adversarial independiente y responsabilidad humana sobre preguntas, diseño y decisiones editoriales).
- [ ] Subir el release etiquetado `v2.0.2` a Zenodo para acuñar el DOI definitivo antes de enviar a *Latin American Antiquity*.
