# 37 · Fuentes vírgenes adicionales, red física RT-16905, ceros en UR-298 y fotogrametría CIELAB en SH001

Fecha: 2026-11-23. Semilla: `20261123`.

Este módulo procesa las cuatro fuentes físicas/manuscritas restantes en `data/external/open-khipu-repository/data/` sin depender de tablas precompiladas de KFG ni `khipu.db`.

---

## 1. Integración de `JS01` (`KH0676`, Brooklyn Museum `36.718`, Ancón)

Archivo fuente: `data/external/open-khipu-repository/data/KH0676/JS01_Strauss_Harvard_Senior_Thesis.xlsx`. Salida normalizada: [`cuerdas_js01.csv`](cuerdas_js01.csv).

- **Conteos:** **138 cuerdas** (`65` colgantes, `73` subsidiarias hasta nivel 4 en `p65`), **137 anudadas**, suma total **4 652** bajo la convención aditiva de la hoja (`s = 10`, `L = n`, `e = 1`), y **6** nudos especiales `SP`.
- **Gramática:** **136 de 137 cuerdas anudadas (99,27 %)** rompen el orden posicional decimal estándar (lugares repetidos o invertidos verticalmente en la cuerda, p. ej. `4L` sobre `5L` sobre `1e` en `p3`, o `3e` sobre `1s` sobre `4L` en `p16`), con torsión final `Z` en la cuerda principal y fibra mixta algodón/camélido (`CN`).

---

## 2. Red física del conjunto enlazado `RT-16905` (`KH0638`–`KH0652`, MNAAHP)

Digitalizamos el grafo de intersecciones físicas del croquis `Croquis KhipusEnlazadosEnglish.jpg` (nodos `1–15` = `KH0638`–`KH0652`; nodos `1–14` con cuerdas en `cuerdas_extra.csv`) sobre los hubs `C={10,11,12}`, `A={11,12,13,14}`, `B={1,13,14,15}`, `D={2,3,4}`, `E={1,4}`, `Zona F={5,6,7}` y `G={4,8,9}`.

Archivo de pares: [`red_rt16905.csv`](red_rt16905.csv) (`91` pares posibles entre `14` quipus, `20` enlazados físicamente por un mismo hub y `71` no enlazados).

| Métrica | Pares enlazados (`n=20`) | Pares no enlazados (`n=71`) | *p* (2 000 permutaciones de grafo) |
|---|---:|---:|---:|
| Jaccard de valores no nulos | 0,1524 | 0,1091 | 0,1009 (no sig.) |
| Diferencia absoluta de largo mediano (cm) | **6,78** | **10,55** | **0,0090** |

**Lectura:** los quipus unidos a un mismo nudo o tramo de encuentro en `RT-16905` comparten escala física de cuerda mucho más de lo esperado al azar (`p = 0,009`), sin compartir secuencias numéricas por encima del azar (`p = 0,101`).

---

## 3. Prueba fuera de muestra de ceros posicionales en `UR-298` (`KH0675`, Dumbarton Oaks `PC.WBC.2016.071.pdf`)

Medimos directamente en las páginas manuscritas `2, 3, 10, 13, 17, 18` de `PC.WBC.2016.071.pdf` **13 intervalos que saltan un cero intermedio** (p. ej. `p188 = 18 067`, `p191 = 2 084`, `p192 = 1 083`, `p72 = 105`, `p80 = 609`) frente a **45 intervalos entre bandas decimales adyacentes** en el mismo quipu.

Archivo: [`ur298_ceros_oos.csv`](ur298_ceros_oos.csv).

- **Mediana de intervalo con cero intermedio:** **10,5 cm** (`n = 13`).
- **Mediana de intervalo adyacente sin cero:** **5,5 cm** (`n = 45`).
- **Razón de medianas:** **1,909** (Mann-Whitney `U = 585,0`, **`p = 1,94 × 10⁻⁸`**).
- **Razón intracuerda** (en `p188`, `p191`, `p192`): `[1,615, 1,294, 1,615]`, mediana **1,615**.

Esta muestra completamente fuera del corpus KFG/OKR (`khipu.db`) reproduce casi exactamente la razón **`1,89`** medida en las 201 cuerdas de KFG contra la tesis no posicional de Florio y Overmann (2025).

---

## 4. Fotogrametría calibrada en CIELAB de `SH001` (`KH0631`)

Medimos la fotografía de campo `SH 001 upper half with ruler & greyscale.jpeg` calibrando el balance de blancos sobre el parche neutro central (parche 7 de la carta de grises: RGB crudo `[54,0, 52,0, 63,0]`, ganancias `[1,0432, 1,0833, 0,8942]`) y convirtiendo los grupos de cuerdas visibles a **CIELAB (D65)**.

Archivo: [`sh001_fotogrametria.csv`](sh001_fotogrametria.csv).

| Grupo / Clase visual | Código `SH001.xlsx` | `L*` | `a*` | `b*` |
|---|---|---:|---:|---:|
| Grupo 0 oscuro (cabello humano) | `W^LK` | 10,8 | 6,0 | 9,8 |
| Grupo 2 oscuro (cabello humano) | `W^LK` | 4,6 | 0,5 | 2,6 |
| Grupo 0 marrón rojizo | `MB` | 24,6 | 9,4 | 17,4 |
| Grupo 1 marrón rojizo | `MB` | 26,3 | 8,5 | 18,7 |
| Grupo 0 claro | `YB` | 63,2 | -7,1 | 13,8 |
| Grupo 1 claro | `YB` | 66,0 | -7,3 | 14,3 |
| Grupo 2 claro | `YB` | 66,4 | -7,3 | 14,1 |
| Grupo 3 claro | `AB` | 63,6 | -7,0 | 13,9 |

* **Separación perceptual `ΔE` entre categorías gruesas:** `W^LK` vs `MB` = **16,12**; `MB` vs `YB` = **42,11**; `W^LK` vs `YB` = **54,16**.
* **Inestabilidad entre tonos finos:** `g1_claro_YB` frente a `g3_claro_AB` da **`ΔE = 2,45`** (prácticamente en el umbral mínimo de discriminación humana, `~2,3`), casi idéntico a la variación del mismo color entre grupos (`g0_MB` vs `g1_MB`: `ΔE = 2,32`). Esto cuantifica ópticamente en una foto calibrada por qué los colores gruesos son fiables y las etiquetas finas (`YB` vs `AB`) son ruidosas entre transcriptores.
