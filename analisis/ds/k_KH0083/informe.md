# Lectura profunda del quipu KH0083 (UR035 / AS070) — Mollepampa / Playa Miller, Arica

Autor: equipo "k_KH0083". Fecha: 2026-10-17.
Scripts reproducibles en esta misma carpeta: `okr_query.py`, `explorar_estructura.py`, `aritmetica.py`, `patrones.py`, `patrones2.py`, `nudos_raros.py`, `arbol.py`.
Reglas del `analisis/BRIEF.md` cumplidas: unidad = quipu; nulo explícito por permutación (semilla 0, 1000 réplicas); corrección de comparaciones múltiples; se reportan negativos; se etiqueta el nivel de evidencia.

---

## 1. Pregunta

¿Qué es KH0083? Reconstruir su estructura completa, buscar toda la aritmética interna comparándola con un modelo nulo, proponer el tipo de registro (censo, tributo, depósito, calendario u otro) identificando qué serían "filas" y "columnas", y señalar lo que no encaja.

## 2. Datos y método

- Fuente preparada: `analisis/datos/cuerdas.csv`, `grupos.csv`, `quipus.csv`. Metadatos y estructura cruzados con la base OKR (`data/external/open-khipu-repository/data/khipu.db`, `KHIPU_ID=1000279`).
- Identidad del objeto: KH0083 = UR035 = AS070, Museo Chileno de Arte Precolombino, nº 780 ("chilean khipu", lana). Procedencia registrada **Mollepampa**, región/investigador **"Inka, Playa Miller"**. OKR, nota de Brezine (2005): "una de una colección de cuatro quipus de la colección de Percy Dahlsberg, en Arica"; encontrados en el centro administrativo de Mollepampa (~30 km río arriba del Lluta desde Arica), aunque Aldunate cree que procede del sitio Inka de Playa Miller.
- **Advertencia de la propia fuente**: el Museo Chileno reordenó los colgantes a lo largo del cordón principal para la exhibición (se movió el *espaciado*, no el orden ni el largo total). Por eso **no se interpreta el espaciado ni los "grupos" como fronteras físicas fiables**; sí el orden.
- Controles: para cada patrón, estadístico observado vs 1000 permutaciones de los valores (o de las etiquetas de color) **dentro de KH0083**, semilla 0; p empírico = (1+Σ(nulo≥obs))/(1+B); corrección BH-FDR.

## 3. Estructura reconstruida

| Rasgo | KH0083 |
|---|---|
| Cuerdas totales | 585 (KFG) / 588 (OKR); **8.º quipu más grande del corpus KFG** (mediana del corpus = 43) |
| Colgantes (nivel 0) | 88 · Subsidiarias (nivel ≥1) | 497 |
| Profundidad | 5 niveles de subsidiarias (OKR: 6) |
| Torsión | 584 S, 1 U (todo hilado S) |
| Unión al cordón principal | colgantes: 86 **R** (recto), 1 U, 1 ? · subsidiarias: 496 **U**, 1 R · **NO HAY cuerdas superiores (union T)** |
| Terminación | 547 K, 38 U |
| Grupos (`grupos.csv`) | 60: **57 grupos de 1 solo colgante**, uno de 4 (g59), uno de 11 (g0), uno de 16 (g57) |
| Racimos de nudos | S=251, L=221, E=67, EE=12, BL=3, U=2 · direcciones S=484, Z=69, U=3 |
| Cuerdas con nudos | 351 (valor>0) · **sin nudos: 234 (40 %)**: no son ceros reales (BRIEF regla 6) |
| Valores distintos (>0) | 93; más frecuentes 10 (n=33), 1 (31), 2 (24), 5 (20), 4 (18), 3 (18) |
| Largo de cuerda | mediana 40 cm, máx 76 cm |

**Estructura dominante**: una jerarquía profunda en la que el número casi nunca está en el colgante (sólo 32 de 88 colgantes tienen nudos) sino en las **subsidiarias hoja**. Ejemplo (p48=130):

```
p48 v=130 K  W
  p48s1   v=0  (W)  -> p48s1s1 v=0 (W-HB) -> p48s1s1s1 v=25 (HB)
  p48s2   v=0  (W:MB) -> p48s2s1 v=10 (HB)
  p48s3   v=0  (W-DB) -> p48s3s1 v=4  (HB)
  p48s4   v=10 (W-DB)
  p48s5   v=511 KZ (HB)
```

## 4. Aritmética interna y controles

| Prueba (KH0083) | Observado | Media nula | p empírico |
|---|---|---|---|
| R1: padre = Σ hijas, padre>0 (todas, ≥1 hija) | 2 | 2.50 | 0.710 |
| R1b: igual pero ≥2 hijas | 1 | 1.18 | 0.686 |
| R2: nº de valores repetidos | 42 | 42.0 | 1.000 (**test inválido**, ver abajo) |
| R3: razón entera padre ≥2×hija, hija≥2 | 11 | 3.54 | **0.0010** |
| R4: periodicidad de color SR (escaneo de m=2..44) | 7 (m=11) | 4.64 | **0.0150** |
| R5: cambios de color en la secuencia de 88 colgantes | 36 | 51.2 | **0.0010** (cola baja) |
| R6: corr(nº descendientes, valor) | −0.078 | — | — (nulo) |

**BH-FDR (α=0.05) sobre {0.71, 0.69, 0.001, 0.015, 0.001}**: siguen significativas R3 (q=0.005), R5 (q=0.005) y R4 (q=0.025); R1/R1b quedan no significativas. **Corroboración independiente**: el análisis previo del equipo en `analisis/01_aritmetica/` da para KH0083 `obs_R1 = 0` (colgante = suma de subsidiarias) y `cierre_intragrupo obs = 0, p = 1.0`, y `tieneT = 0, ausentes = 0.40`.

Comentarios críticos (evitar la explicación "interesante" antes de la aburrida):
- **R3 es débil**: los 11 pares con razón entera se explican en gran parte porque muchos valores son enteros "redondos" y varios hijos valen 2, 4, 5 o 10; ningún colgante "totaliza" a sus hijas. Se etiqueta **apoyado con datos, pero con explicación aburrida no descartada**.
- **R2 es un test degenerado**: barrer los valores entre cuerdas preserva el multiconjunto de valores, y el número de valores repetidos sólo depende de ese multiconjunto → p=1.0 por construcción. Lo reporto como **control mal planteado** (lección metodológica), no como resultado.

## 5. Patrón de color (el hallazgo más robusto)

- Los colgantes son mayoritariamente **W blanco (50)** y **AB marrón claro (26)**; sólo 7 son **SR**, 3 PK, 1 GA.
- Los 7 colgantes **SR** ("strong red", rojo **verdadero teñido**, raro en el corpus: `analisis/02_color/informe.md` señala que sólo hay 8 quipus evaluables con rojos reales) están, en el orden izquierda→derecha, en las **posiciones 1, 12, 23, 34, 45, 56 y 67** — una progresión aritmética de **paso exacto 11** (gaps: 11,11,11,11,11,11).
- Dato decisivo: esas 7 cuerdas SR **no llevan ningún nudo** (valor 0). Son **marcadores puros, sin número**.
- 88 colgantes = **8 × 11**: la lectura natural es **8 bloques de 11 colgantes**, cada uno abierto por una cuerda roja. El bloque 8 (posiciones 78–88) **no** tiene su marcador rojo (p78 es blanca, con el valor más alto, 748) → anomalía (§7).
- Control: escaneo honesto de periodos m=2..44 (evita el sesgo post-hoc de fijar 11) → p = 0.015. Los colores están además fuertemente **agrupados** por bloques (R5, p=0.001): dentro de un bloque los colgantes tienden al mismo color.
- Lectura aburrida parcial: parte del "patrón" es que el rojo es rarísimo y cualquier concentración llama la atención; pero una periodicidad **exacta** de periodo 11 en 7/7 es difícilmente accidental (p=0.015 tras corregir por escaneo).

## 6. Nudos "raros" y candidatos a información no numérica

- **BL** (valor 9 en los tres casos): sólo 3 cuerdas, y las tres **agrupadas** al final del quipu (p83, p84, p84s4s1). Tipo de nudo poco común → posible marcador o transcripción peculiar.
- **"Nudo bajo las unidades" (patrón de Hyland)**: 9 cuerdas (10 apariciones; una repetida) tienen una figura de ocho (E/EE) **antes** del último racimo, p.ej. `p17s2s2 = 10 + 1 + 2`, `p21s1s2s1 = 20 + 1 + 2`, `p87 = 1 + 10 + 8`. Es el mismo tipo de rasgo que el "nether" que `analisis/06_nudos/informe.md` marca para KH0083 (22 cuerdas, q=0.022; definición algo distinta). **Propuesto**: marcador adicional por cuerda, no parte del valor decimal.
- **Dirección Z**: los 69 racimos Z de KH0083 son **figuras de ocho** (E/EE). A escala de corpus, E/EE se transcriben mayoritariamente con dirección Z (5 592 Z vs 2 069 S) ⇒ **es convención de transcripción, no señal del quipu**. Descartado como información.
- **38 terminaciones U** (desconocidas) y 1 colgante con unión desconocida: ruido de catalogación, no patrones.
- Las cuerdas **sin nudos (40 %)** no son "ceros": son posiciones a las que no se les colgó valor.

## 7. Anomalías

1. El **bloque 8** (colgantes 78–88) rompe el patrón: sin marcador rojo, y concentra los valores grandes (748, 624, 641, 117, 203, 109) junto con PK en los extremos. Sugiere que la parte final del quipu es de **naturaleza distinta** (o que el marcador se perdió/trasladó en el reordenamiento museístico).
2. Los tres nudos **BL** aparecen juntos y al final (p83/p84) → artefacto localizado.
3. p14s1 (nivel 1) es la **única subsidiaria con unión R**; y un colgante tiene unión desconocida: micro-inconsistencias de catalogación.
4. Recordatorio de fuente: el **espaciado entre colgantes no es interpretable** (reordenamiento del museo); los "60 grupos" de `grupos.csv` son en su mayoría falsos positivos de espaciado (57 de tamaño 1). El marcador rojo da la partición real (11 × 8).

## 8. Lectura más probable (hipótesis y nivel de evidencia)

**Hipótesis (propuesta / especulativa)**: KH0083 es un **registro administrativo jerárquico no sumatorio** — un *padrón* o listado organizativo (p. ej. censo/reparto/registro de unidades) —, NO un quipu de cálculo.

- **"Filas"**: los **88 colgantes** = entidades individuales (personas, familias, unidades de tributarios, o categorías), agrupadas en **8 bloques de 11** delimitados por cuerdas **rojas SR sin nudos** (probables "cabeceras de sección"/marcadores de frontera; cf. Medrano y Khosla 2024 sobre cordeles claros como marcadores de límite, y la tradición de "firmas de color" en el caso Santa).
- **"Columnas"**: los **niveles de la jerarquía de subsidiarias** (0–5). El valor numérico vive casi siempre en las **hojas**; cabeceras y tallos intermedios van sin nudos. Esto es un **árbol de desagregación**, no una suma: la coincidencia colgante=Σsubsidiarias es **cero** (obs_R1 del equipo) y no hay cuerdas superiores (T).
- **Ubicación cultural**: Arica (Playa Miller / Mollepampa), *chilean khipu* de lana; `UR35/AS70` figura entre las muestras datadas por **Cherkinsky y Urton (2014): 365 ± 29 BP → cal 1559–1579 d. C.**, es decir, **horizonte tardío / contacto colonial**, coherente con un registro administrativo.

**Nivel de evidencia**:
- **Apoyado con datos**: la estructura jerárquica; la ausencia de sumas y de cuerdas superiores; la partición 8×11 marcada por rojos sin nudos (p=0.015); el agrupamiento de colores (p=0.001).
- **Propuesto**: que los bloques de 11 sean secciones administrativas (ayllus/unidades) y las rojas sus cabeceras; que KH0083 sea un padrón/registro y no un quipu de cálculo.
- **Especulativo**: la semántica concreta (¿censo de tribute t? ¿reparto? ¿qué representan las "filas" y "columnas" en términos de personas/bienes?).

## 9. Resultados negativos (relevantes)

- **No hay aritmética de sumas**: colgante = Σ subsidiarias ⇒ obs 2 vs nulo 2.5 (p=0.71); con ≥2 hijas, obs 1 (p=0.69); obs_R1 del equipo = 0. **No hay "cuadre" interno.**
- **No hay cuerdas superiores** (union T ausente; `tieneT = 0`): no hay nivel de totales.
- **No hay cierre intragrupo** (obs 0, p=1.0).
- **No hay razón constante** en cadenas de hijo único (25 cadenas; sólo 1 igualdad 5=5; razones dispersas).
- **No hay relación estructura–magnitud**: corr(nº descendientes, valor) = −0.078 (todas: 0.000).
- **No hay grupo = suma de grupos**: sin estructura de totales entre bloques (sumas por bloque 65, 32, 59, 3, 1284, 85, 10, 2587; ninguna coincide ni suma a un total redondo; Σ colgantes = 4 125).

## 10. Para el coordinador

- **KH0083 = UR035 = AS070**, Museo Chileno nº 780, Arica (Mollepampa/Playa Miller); datado ~1559–1579 d. C. (Cherkinsky y Urton 2014). 585 cuerdas, 88 colgantes, 497 subsidiarias, hasta 5 niveles; **8.º quipu más grande** del corpus KFG (mediana 43).
- **No es un quipu de cálculo**: no hay sumas (colgante = Σ subsidiarias ⇒ obs 0–2, p≈0.7), **no hay cuerdas superiores** (T ausente) y no hay cierre intragrupo (p=1.0). Corrobora el análisis previo del equipo (`01_aritmetica`).
- **Hallazgo más fuerte (apoyado con datos)**: **88 = 8 × 11**, y los 7 colgantes **rojos SR** (rojo verdadero, raro) caen en las posiciones 1, 12, 23, 34, 45, 56, 67 — **periodo exacto 11** (p=0.015 tras escaneo honesto de periodos). Esas cuerdas rojas **no llevan nudos**: son marcadores puros.
- **Colores agrupados** por bloques (menos cambios que el azar, p=0.001). El rojo delimita secciones; el blanco/marrón llena el interior.
- **Interpretación propuesta**: registro administrativo **jerárquico no sumatorio** tipo *padrón*/listado; "filas" = 88 colgantes en 8 bloques de 11; "columnas" = niveles de subsidiarias (el número queda en las hojas). Semántica (censo vs reparto vs otro) = **especulativa**.
- **Anomalías**: el bloque 8 pierde su marcador rojo y concentra los valores grandes (748, 624, 641…); 3 nudos **BL** juntos al final; 10 cuerdas con "nudo bajo las unidades" (patrón Hyland); 40 % de cuerdas sin nudos (no son ceros).
- **Ruin descartado como señal**: la dirección Z de KH0083 son todas figuras de ocho ⇒ es **convención de transcripción** (corpus: 5 592 Z vs 2 069 S en E/EE), no información.
- **Advertencia de fuente**: el museo reordenó el espaciado; **no usar `grupos.csv`** (57 "grupos" de tamaño 1 son falsos). La partición fiable es la roja (11 × 8).
- **Recomendación**: (a) verificar con imágenes del Museo Chileno si el bloque 8 tiene un marcador rojo movido/perdido; (b) buscar el "par" de KH0083 entre los otros tres quipus de la colección Dahlsberg (Thompson 2024 describe una relación numérica entre dos quipus de Arica); (c) contrastar el patrón 8×11 con otros quipus grandes del corpus para ver si "bloques de 11 con cabecera roja" es un género.
