# Estructura computacional, contabilidad en tres niveles y pruebas fuera de muestra en el corpus digital de quipus andinos (v2.0)

**Autor:** Dario (`dariodemh`), con agentes de IA (Gemini de Google, Claude Opus/Sonnet de Anthropic y DeepSeek Flash)  
**Repositorio y herramientas:** https://github.com/dariodemh/quipus · Ensayo, Resumen Visual y Lector en navegador: https://dariodemh.github.io/quipus/articulo/index.es.html  
**Estado:** Preprint v2 abierto a revisión especializada (sin revisión de pares todavía). Todos los estadísticos, controles y fichas son reproducibles de forma determinista desde el repositorio público.

---

## Resumen

Presentamos una auditoría estadística reproducible del corpus digital de quipus andinos. Sobre la base inicial del *Khipu Field Guide* (651 hojas, 57,818 cuerdas; 650 objetos únicos tras descontar el duplicado `UR044`), construimos un **Corpus Maestro Unificado de 689 quipus con colgantes y 60,969 cuerdas** (más `KH0652` con 19 hilos enrollados, 690 objetos en total), integrando el *Open Khipu Repository* (`khipu.db` v2.1.0), el *Databook* de los Ascher, las 222 correcciones estructuradas de Karen M. Thompson (2025), 11 fichas fotográficas transcritas de Huacones-Vilcahuasi (`JC024`–`JC034`) y el conjunto físicamente atado `RT-16905` del Museo Nacional en Lima (Chirinos, Ghezzi y Álvarez, 2023). El corpus separa los 650 quipus base de **39 quipus puros fuera de muestra (`held-out`, 2,414 cuerdas)**. Mediante nulos por permutación dentro de cada quipu, corrección por multiplicidad (Holm y Benjamini-Hochberg), controles positivos (Puruchuco y `KH0049`), prueba ciega sobre datos anonimizados y seis protocolos locales congelados con SHA-256 (`P01`–`P06`, integrados en un registro público de 98 pruebas), reportamos cuatro resultados principales:

1. **Contabilidad en tres niveles en Inkawasi:** Ampliando Urton y Chu (2015, 2018), el montón del maní del sector A muestra una cadena verificable donde `colgante + 1.ª subsidiaria` de `UR270` reproduce celda a celda la tabla de 9 columnas de `UR278` (5/12 grupos comparables con 6–9/9 coincidencias; `p = 0.0002`; recuperada también en prueba ciega), cuyos totales de fila reaparecen en orden como cabeceras de `UR266` (11/18 exactas, `Holm = 1.6×10⁻⁹`) y `UR275` (7 exactas, `Holm = 2.8×10⁻⁴`). La pareja atada `UR273A + UR273B` alcanza 8/18 cabeceras por una segunda vía (`p = 0.015` bajo 58,782 pruebas del equipo rojo). El bootstrap de máxima parsimonia (10,000 réplicas) da 99.8 % de soporte a un libro intermedio perdido `α` (`UR278 → α → {UR266, UR275}`) portador de los desajustes compartidos (`±1`). Usando la carga andina precolombina (~28 L, ~8 kg de maní en vaina), las ~59,000 unidades de `UR278` corresponden al orden de **~470 toneladas** (con una cota superior colonial de ~950 t bajo la fanega castellana de ~16 kg).
2. **Confirmaciones fuera de muestra y dos nuevos casos aritméticos (`P01`, `P03.4`, `E03.6`):** En los 39 quipus fuera de muestra (Holm estricto `m = 6`) se confirman "la cuerda mayor abre el grupo" (29/104 = 27.9 % frente a 17.0 %, `p_Holm = 0.0168`) y la alternancia `A/B/A/B` (5/16 frente a 0.16, `p_Holm < 10⁻⁴`). Además, 53/174 cuerdas superiores rescatadas de OKR (30.5 % frente a 7.0 %) suman exactamente el grupo anterior (`p_Holm = 0.0010`), el quipu fuera de muestra `KH0674` (Dumbarton Oaks) exhibe 8/41 grupos con cuerda-resumen exacta (`p_Holm = 0.002`), y una auditoría post hoc en `QU005` (Dallas) descubre una tercera tabla de sumas por columna (`B2 = B0 + B1` en 12/19 posiciones exactas y 13/19 con `±1`, `p_corr = 0.0001`).
3. **Propiedades físicas independientes de etiquetas humanas (`P04`):** Al proyectar el color al espacio perceptual CIE `L*a*b*` (96.8 % de las cuerdas), los tonos más luminosos llevan valores algo mayores dentro de cada grupo incluso excluyendo el blanco `W` (`n = 225`, `med_rho = +0.0529`, `p_Holm = 0.012`). Cortar grupos únicamente por huecos físicos en centímetros (`k = 2.0`, sin etiquetas humanas) replica tendencias ordenadas en 9/35 quipus (`p_Holm = 0.00017`). Sin embargo, el análisis PERMANOVA sobre geometría 2D (`n = 148`) advierte que el capturista (`R² = 0.087`) explica tanta varianza como el sitio arqueológico (`R² = 0.085`, museo `R² = 0.272`).
4. **Auditoría metodológica y negativos informativos (`P02`, `P03`, `P05`, `P06`):** Al aplicar nulos quipu por quipu, entre el 93 % y el 100 % de las sumas simples contadas por la cifra publicada del 74 % aparece por azar (potencia ~24 %; solo 14 quipus resisten dos barajados). En 726 cuerdas con ceros internos (727 huecos), el espacio vacío mide 0.96 bandas decimales (1.89× entre bandas contiguas en 201 cuerdas, replicado en `UR-298` con 1.909×). En `RT-16905` (15 quipus atados) las cuatro pruebas de jerarquía aritmética y similitud numérica cierran negativas (`p_Holm = 0.25–0.81`). En 1,190 ítems coloniales (38 tablas), un clasificador de géneros fiscales cae de `LODO = 38.2 %` (`p = 0.0085`) a `LOSO = 5.0 %` (`p = 0.9925`) con 53.7 % de falsos positivos sintéticos. Finalmente, al auditar cuatro trabajos computacionales de 2026 con nulos estrictos, las señales de entropía R/V (0/39 bajo nulo por rachas, `p_Holm = 0.587`), torsión imperial (`F1: 0.241 → 0.048` en CV por sitio; OKR 100 % idéntico a `collca.db` en el Santa), color global (`R² = 1.06 %` frente a clave local `16.0 %`) y similitud padre-hijo en grafos (`z: 6.76 → 1.82`, `p_Holm = 0.126` al controlar grupo y escala) dependen de supuestos nulos permisivos, mientras que la igualdad agregada entre colgante y suma de sus subsidiarias sí supera el nulo (`4.30 %` frente a `2.75 %`, `p_Holm = 0.003`).

---

## 1. Corpus Maestro, erratas y transcripciones vírgenes

- **Fuentes primarias:** KFG v2.1.0 (editado y mantenido por Ashok Khosla; 651 hojas, 57,818 cuerdas; 650 objetos únicos sin el duplicado `UR044`), OKR v2.1.0 (`khipu.db`, 619 quipus, 54,403 cuerdas), *Databook* (Ascher y Ascher, 1978), 222 correcciones estructuradas de Karen M. Thompson (2025, aplicadas en columna paralela `valor_thompson` sin sobrescribir datos crudos), 11 fichas de Huacones-Vilcahuasi (`JC024`–`JC034`, 101 cuerdas) y `RT-16905` (14 quipus con colgantes + `KH0652` con 19 hilos enrollados).
- **Reconciliación y erratas (`C26`, `D01.6`):** KFG y OKR comparten 99.33 % de valores (>99.8 % en Inkawasi por provenir de la misma lectura); las tres dobles lecturas independientes (`UR1107=UR237`, `KH0033=UR044`, `AS125=UR247`) fijan un ruido basal de 0–12 %. El Corpus Maestro rescata 111 cuerdas faltantes de Inkawasi (incluido `UR274B = 133` cuerdas), 248 cuerdas superiores (`T`) y 447 marcadoras (`M`), repara cuatro archivos desplazados (`KH0197`, `KH0227`, `KH0267`, `KH0350`) y resuelve los alias `AS↔UR1xxx` (`UR1180`, `MM1086`), cerrando en **689 quipus (60,969 cuerdas)**, de los cuales **39 (2,414 cuerdas)** forman la cohorte `held-out`.

---

## 2. Métodos, protocolos sellados y calibración

Todos los detectores aplican nulos por permutación dentro de cada quipu (o preservando grupo, racha, procedencia y magnitud), corrección de Holm o Benjamini-Hochberg, controles positivos (`Puruchuco`, `KH0049`), controles negativos barajados, prueba ciega sobre 52 quipus anonimizados de Inkawasi y seis protocolos locales congelados con SHA-256 (`analisis/35_preregistros/MANIFEST_SHA256.csv`), auditados por Claude Opus antes y después de la ejecución con todas las desviaciones declaradas en `analisis/paquete_revision/paquete_zenodo_y_revista.md`. Los cinco detectores internos rápidos del Lector v2 se calibraron en 100 quipus sintéticos barajados, arrojando 0–1/100 falsos positivos en nivel de indicio (cota superior IC 95 % entre 3.6 % y 5.4 %).

---

## 3. Resultados adicionales y límites medidos

- **Formatos y copias del corpus:** `KH0049` (`AS38`, jerarquía descrita por Ascher y Ascher 1978, copia parcial `UR122` identificada por Chirinos 2010; prueba nula `p < 0.0001` y error compartido `15652/15649`), alternancia `A/B/A/B` (`UR040`, `UR167`), copia como rasgo de archivo (`OR = 17.9`, `p = 10⁻⁷`, incluidas `HP055 ≈ UR1084` y el extracto `UR1104 → UR234` que conserva `2016`), reparto fijo `UR053A–E` (con `P03.2` negativo en sumas directas `UR053E → B/C`, `p_Holm = 0.70`).
- **Huacones-Vilcahuasi, estemática bayesiana y Predicción #17:** Queda refutada la Predicción #13 sobre Huacones (`JC024` tiene `CV = 1.283`, `JC031` mezcla vacíos y nudos aditivos no decimales; 4/10 quipus anudados de Huacones y 99.27 % de `JS01` usan gramática aditiva). El escáner bayesiano `LLR` tolerante a errores no halla enlaces con `q_bh < 0.05` entre los 4 quipus no leídos de Inkawasi (`UR272`, `UR276`, `UR277`, `UR279`, `P03.3` negativo) o los quipus fuera de muestra y el sector A. En 8 listas demográficas coloniales sin Bambamarca (`P06.4`), la mediana `ρ = -0.294` cumple la rama conservadora de la regla binaria (`< -0.30`; 6/8 negativas, `p_Holm = 0.004`), pero 0/8 igualan la pendiente (`-0.73`) o la planitud (`CV = 0.173`) de `UR278`.

---

## 4. Protocolo de 5 nudos en museo y disponibilidad

Las cinco comprobaciones físicas decisivas (`UR278 p180`, `UR266 p104`, `UR275 p51`, `UR234 p41` y `KH0049 p19`) figuran en [`protocolo_museo_5_nudos.md`](../analisis/paquete_revision/protocolo_museo_5_nudos.md). El código, el Corpus Maestro (689 quipus), el Registro Unificado de 98 pruebas (`articulo/registro_pruebas.html`), el Resumen Visual de 18 láminas (`articulo/overview.es.html`), el Lector v2 de línea de comandos (689 quipus) y el Lector en navegador (`articulo/lector.es.html`, 682 quipus indexados sin servidor) están en `https://github.com/dariodemh/quipus` (MIT / CC BY 4.0).

---

## Referencias principales

- Ascher, M. y Ascher, R. (1978). *Code of the Quipu Databook*. Ann Arbor: University Microfilms.
- Chirinos Rivera, A. (2010). *Quipus del Tahuantinsuyo*. Lima: Editorial Commentarios.
- Chirinos, A., Ghezzi, I. y Álvarez, F. (2023). *Description of RT 16905 MNAAHP (KH0638–KH0652)*. OKR / MNAAHP.
- Chirinos, A. (2026). The “Waterfall” Khipu Set and Indigenous Political Organization in the 16th Century. *The Khipu Field Guide Blog*.
- Contreras, M. (2026). Structural Pattern Mining in Inka Khipus. arXiv:2607.00185.
- Curatola Petrocchi, M. y de la Puente Luna, J. C. (eds.) (2013). *El quipu colonial*. PUCP.
- Da Fieno Delucchi, A. (2025). *Khipu Computational Analysis Toolkit (K-CAT)*. GitHub.
- FitzPatrick, M. (2024). New Insights on Cord Attachment and Social Hierarchy in Six Khipus from the Santa Valley, Peru. *Ethnohistory*, 71(4), 443–469.
- Florio, C. y Overmann, K. A. (2025). Inka numbers, khipu, and yupana: a reanalysis. *Journal of Cognition and Culture*, 25(1–2), 128–158.
- Hyland, S. (2017). Writing with Twisted Cords. *Current Anthropology*, 58(3), 412–419.
- *khipu-rv-reproducibility* (2026). *Corpus-Scale Analysis of Binary Attachment Encoding in Inka Khipus: Reproducibility Package*.
- LeVine, T. Y. (ed.) (1992). *Inka Storage Systems*. University of Oklahoma Press.
- Locke, L. L. (1912). The ancient quipu, a Peruvian knot record. *American Anthropologist*, 14(2), 325–332.
- Medrano, M. y Khosla, A. (2024). How can data science contribute to understanding the khipu code? *Latin American Antiquity*, 36(2), 497–516.
- Medrano, M. y Urton, G. (2018). Toward the Decipherment of a Set of Mid-Colonial Khipus from the Santa Valley. *Ethnohistory*, 65(1), 1–23.
- Pärssinen, M. (1992). *Tawantinsuyu*. Societas Historica Finlandiae.
- Platt, T. (2002). “Without Deceit or Lies”. En *Narrative Threads*, Univ. of Texas Press.
- Shukla, Makwana y Gupta (2019). Determination of Some Engineering Properties of Groundnut Pod. *Int. J. Curr. Microbiol. Appl. Sci.*, 8(2), 3025–3030.
- Sivan, J. (2026). Reading the Inca Spreadsheet. Zenodo:19184002.
- Thompson, K. M. (2025). *Notes and Corrections to Aschers' Published Khipu Data*. University of Melbourne (figshare). DOI: 10.26188/30526775.
- Urton, G. (2005). Khipu Archives. *Latin American Antiquity*, 16(2), 147–167.
- Urton, G. (2017). *Inka History in Knots*. University of Texas Press.
- Urton, G. y Brezine, C. J. (2005). Khipu accounting in ancient Peru. *Science*, 309(5737), 1065–1067.
- Urton, G. y Chu, A. (2015, 2018). *Latin American Antiquity*, 26(4), 512–529; 30(1), 1–16.
- Zenil, H. y Uthamacumaran, A. (2026). Reconstruction of Geometric and Structural Aspects of Undeciphered Messages by Information-theoretic Methods. arXiv:2610.08861.
