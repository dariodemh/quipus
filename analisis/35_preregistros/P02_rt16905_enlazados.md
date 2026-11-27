# Preregistro P02 — Validación física vs. aritmética en los 15 Quipus Enlazados RT-16905 (`KH0638–KH0652`) (v1.1 post-equipo-rojo)

- **ID:** `P02`
- **Fecha de congelación:** 2026-11-27 (revisión pre-hash tras auditoría adversarial con Claude Opus 5.5 Medium)
- **Semilla fija:** `20261127`
- **Objeto:** Conjunto RT-16905 (MNAAHP, Lima; registrado por Chirinos, Ghezzi y Álvarez, sept. 2023), 15 quipus (`K01`–`K15`, códigos `KH0638`–`KH0652`) físicamente atados entre sí (`Croquis KhipusEnlazadosEnglish.jpg` y `Description RT 16905 MNAAHP.docx`).

## 1. Topología física congelada (extraída exclusivamente del croquis y descripción, ANTES de mirar los números)

Grafo físico $G_{\text{fis}} = (V, E)$ sobre los 14 quipus con colgantes (`K01`–`K14`; `K15` = 19 hilos envueltos sobre `K01`):
- **Hub C:** `{K10, K11, K12}`
- **Hub A (y Manojo H):** `{K11, K12, K13, K14}`
- **Hub B:** `{K01, K13, K14}`
- **Hub D (sobre cordón primario de K01):** `{K01, K02, K03}`
- **Hub E (unión K01–K04):** `{K01, K04}`
- **Zona F (sobre cordón primario de K04):** `{K04, K05, K06, K07}`
- **Hub G (sobre cordón primario de K04):** `{K04, K08, K09}`
- **Ramas macro:** Inferior (eje C–A–B) = `{K11, K12, K13, K14}`; Superior = `{K01–K10}` (+ `K15` sobre `K01`).

Adyacencia física: $A_{ij} = 1$ si comparten al menos un Hub/Zona; $d_{\text{fis}}(i,j)$ = distancia de camino mínimo en $G_{\text{fis}}$.

## 2. Familia confirmatoria congelada (Holm exacto sobre `m = 4` pruebas)

| Test ID | Hipótesis | Estadístico exacto (normalizado por tamaño para evitar confusión de hubs grandes) | Nulo emparejado | Criterio binario |
|---|---|---|---|---|
| **P02.1** | **Sumas jerárquicas sobre ejes físicos (`K01`, `K04`, `K11–K14`):** los totales de quipu o de grupo (estrictamente **≥ 10**, excluyendo 1–9 para evitar coincidencias triviales) de los nodos hoja reaparecen en sus vecinos físicos ($A_{ij}=1$) por encima de lo esperado dado el tamaño de ambos quipus. | Para cada par dirigido $(i,j)$, exceso normalizado $Z_{ij} = (\text{obs}_{ij} - \mu^{\text{tam}}_{ij}) / \max(\sigma^{\text{tam}}_{ij}, 1)$, donde $(\mu^{\text{tam}}_{ij}, \sigma^{\text{tam}}_{ij})$ se obtiene barajando los valores ≥ 10 de $j$ contra el pool del conjunto manteniendo $|j|$ (200 réplicas internas). Estadístico global: media de $Z_{ij}$ en pares adyacentes ($A_{ij}=1$) menos no adyacentes ($A_{ij}=0$). | QAP sobre $G_{\text{fis}}$ (10 000 permutaciones de etiquetas de quipu sobre la matriz $Z_{ij}$, que ya está estandarizada por tamaño). | Diferencia > 0 y `p_Holm < 0,05`. |
| **P02.2** | **Acoplamiento numérico/copias correlaciona con proximidad física:** pares adyacentes ($A_{ij}=1$) comparten más valores ≥ 10 (similitud Jaccard ponderada por IDF y score Smith-Waterman **estandarizado por tamaño** $Z^{\text{SW}}_{ij}$ frente a nulo de rachas del par) que pares distantes ($d_{\text{fis}} \ge 2$). | Correlación de Mantel (Spearman) entre $Z^{\text{SW}}_{ij}$ (normalizado por tamaño de ambos quipus) y $-d_{\text{fis}}(i,j)$. | QAP (10 000 permutaciones simultáneas de filas y columnas de $d_{\text{fis}}$). | $\rho_{\text{Mantel}} > 0$ y `p_Holm < 0,05`. |
| **P02.3** | **Coherencia de formato textil por vecindad física:** los quipus unidos al mismo hub comparten perfil físico-textil (proporción torsión S/Z, proporción unión R/V, fibra dominante, longitud mediana de colgantes, paleta de color — excluyendo el tamaño total para no confundir con el grado del hub). | Correlación de Mantel entre similitud física-textil (1 − distancia de Gower) y $-d_{\text{fis}}(i,j)$. | QAP (10 000 permutaciones de filas/columnas). | $\rho_{\text{Mantel}} > 0$ y `p_Holm < 0,05`. |
| **P02.4** | **Alineación cromática de `K15` (19 hilos envueltos) con `K01`:** la secuencia de colores de `W1–W19` en las 4 secciones de `K15` se alinea con la paleta/orden de colores de los grupos de `K01` mejor que el azar. | Máxima puntuación de coincidencia de secuencia de color normalizada (o NMI entre sección de `K15` y grupo de `K01`). | Permutación de la secuencia de colores de `K15` preservando rachas de color idéntico (5 000 réplicas). | `p_Holm < 0,05`. |

## 3. Análisis descriptivos complementarios (FUERA de la familia Holm `m = 4`)
- **D02.5 (contabilidad interna individual):** ejecutar los detectores estándar de suma interna (`R1`, `F`, `A`, `TA`, permutación intra-quipu por nivel con 5 000 réplicas y `q_BH < 0,05`) en cada uno de los 14 quipus `K01–K14` y reportar la tasa de quipus con contabilidad interna verificable frente al 3 % del corpus.
- **D02.6 (descripción estructural de `Tie Cord 04` y cuentas de `K15`):** documentar los valores y posiciones de `Tie Cord 04` (`3L+1S`) y la relación de conteos entre `K15` (19 hilos, 4 secciones) y `K01` (etiquetado como `descriptivo` / `propuesto`).
- **Honestidad ante negativos:** si `P02.1`–`P02.4` son negativos, se registrará explícitamente que el enlace físico de RT-16905 (decomiso) no muestra jerarquía aritmética ni acoplamiento detectable con estos datos.
