# Lectura profunda del quipu UR003 (KH0239) — Leymebamba

**Autor:** equipo `k_UR003`. **Fecha:** 2026-10-17.
**Entrega:** `analisis/ds/k_UR003/informe.md`. Scripts: `01_estructura.py`, `02_aritmetica.py`,
`03_patrones.py`, `04_nulos.py`, `05_color.py`, `06_tendencia.py` (+ volcados `*_out.txt`).

---

## 1. Pregunta

*¿Qué tipo de registro es UR003 y cómo está organizada su información?* Concretamente:
(1) reconstruir su estructura; (2) buscar toda la aritmética interna y contrastarla con un nulo;
(3) proponer la lectura más probable y su nivel de evidencia; (4) señalar lo que no encaja.

## 2. Datos y método

- **Identificación:** UR003 = **KH0239** = CMA-419/LC1-048 TEQ, *Centro Mallqui, Leymebamba*,
  procedencia **Leymebamba (Laguna de los Cóndores), region Chachapoyas** (`quipus.csv`).
- **Fuentes:** `analisis/datos/cuerdas.csv` (758 cuerdas de UR003), `grupos.csv`, el resumen y las
  relaciones de suma automáticas del KFG (`data-science-khipu-article`), y el OKR (`khipu.db`,
  khipu_id 1000020, 769 cuerdas). Nunca se imprimieron ficheros completos.
- **Método:** toda relación aritmética se contrastó con un **nulo explícito**: barajar el vector de
  valores entre las 758 cuerdas (preservando la estructura de árbol madre/hija), 1000 iteraciones,
  **semilla 0**; p-valor empírico de una cola `p = (1+#{nulo≥obs})/(N+1)`. Corrección de
  comparaciones múltiples por **Holm**. Las pruebas a nivel de estructura **no numérica** (color,
  attachment) usan el mismo esquema de permutación dentro del quipu. La unidad es el **quipu**, no
  la cuerda.

## 3. Resultados

### 3.1 Estructura reconstruida

| Nivel | cuerdas |
|---|---|
| 0 (colgantes) | **281** |
| 1 (subsidiarias) | 392 |
| 2 | 77 |
| 3 | 7 |
| 4 | 1 |
| **Total** | **758** |

- **15 grupos** (`grupo` 0–14). Colgantes por grupo:
  `g0=1 · g1=4 · g2=40 · g3=21 · g4=40 · g5=10 · g6=26 · g7=1 · g8=60 · g9=21 · g10=18 · g11=17 · g12=20 · g13=1 · g14=1`.
  Nº total de cuerdas por grupo: `1,4,104,63,93,33,59,1,178,61,45,39,66,1,10`.
- **Subsidiarias:** 477 en total (1,7 por colgante de media); casi todas cuelgan en un solo nivel
  (392 en nivel 1). Sólo 85 cuerdas alcanzan nivel ≥2.
- **Cuerdas superiores (union T): NO hay ninguna.** Confirmado en KFG (`union` ∈ {U,V,R,?}) y en
  OKR (attachments ∈ {R,U,V}). El KFG también da `num_top_cords = 0`
  (`num_top_cord_sum_clusters = 0`, `double_sum_top_cords = 0`). Por tanto **no cabe la
  comprobación "cuerda superior = suma de grupo"**: no existe(n) la(s) cuerda(s) superior(es).
- **Attachment de los colgantes:** **V = 219**, **R = 55**, U = 5, ? = 2. Las subsidiarias son
  casi siempre U (390 en nivel 1; sólo 1 V). Torsión: S = 749, ~Z, 1 U. Terminación: K 567, B 87,
  U/desconocida 77, R 21.
- **Nudos:** 496 nudos-cúmulo (uno por grupo de nudos); **figura-ocho (E) 301, largo (L) 189,
  simple (S) ¡sólo 2!**. Direcciones: Z 365, S 120, U 7. OKR confirma: E 304, L 190, S 2.
  Es decir, **el quipu usa casi exclusivamente nudos de unidades**; toda la aritmética decimal
  (decenas/centenas, que se escriben con nudos simples) está prácticamente ausente.
- **Colores (base, 758 cuerdas):** W 271, AB 185, MB 153, RL 48, KB 32, GG 19, LC 13, RM 11, más
  colores mixtos (`:` barber-pole), compuestos (`-`,`/`) y de rango (p.ej. `MB(0.0-19.0)/RL(...)`).
  **Los colgantes son W/AB/MB** (131/86/52); las **subsidiarias añaden colores cálidos y claros**
  (RL 41, GG 16, KB 15, LC 12, RM 11) que apenas aparecen entre colgantes.
- **Valores:** máx **11**, media 1.18. Distribución (todas las cuerdas): `0:292, 1:276, 2:95, 3:34,
  4:26, 5:14, 6:11, 7:4, 8:1, 9:2, 10:2, 11:1`. **289 cuerdas sin nudos** (142 colgantes = 50.5 %).
  Suma total = 893 (colgantes 263).

### 3.2 Aritmética interna (con controles nulos) — **resultado negativo**

Se implementaron de forma genérica las relaciones que el KFG detecta automáticamente y las que
pide la tarea. Observado vs. nulo (N=1000, semilla 0):

| Prueba | Observado | Nulo (media) | p (una cola) | Holm |
|---|---|---|---|---|
| A) madre = suma de sus hijas directas | 37 / 206 | 43.7 | 0.912 | 1.0 |
| A2) colgante = suma de todos sus descendientes | 15 | 19.1 | 0.904 | 1.0 |
| B) cluster con mitad equilibrada (prefijo = sufijo) | 3 | 2.8 | 0.555 | 1.0 |
| C) par de clusters con suma total igual (>0) | 1 | 1.0 | 0.653 | 1.0 |
| D) colgante = suma de ≥2 cuerdas homólogas de otros clusters | 26 | 36.1 | 0.964 | 1.0 |
| E) subsecuencia de valores idéntica entre clusters | 10 | 8.6 | 0.179 | ~1.0 |

**Ninguna** supera el azar (tras Holm, todos p ≈ 1). Peor aún: en A, A2 y D el observado es
**menor** que el nulo — es decir, hay *menos* coincidencias aritméticas de las esperadas por azar
(porque las cuerdas madre tienden a tener valores pequeños/cero, no sumas de sus hijas).

Coincidencia con el KFG: sus detectores hallan exactamente lo mismo que el azar predice —
`num_pendant_pendant_sum = 1` (p129 = 6+1+0+0+1+0+0+0+2+1 = 11), `num_indexed_pendant_sum = 1`
(p56 = 3+2+1 = 6), `num_cluster_cluster_sum = 1` (g5 y g10 ambas suman 51 incluidas subsidiarias),
`num_cluster_sum_bands = 2`. Son casos aislados, todos dentro del rango nulo. **No hay sistema
aritmético.**

### 3.3 Lo que SÍ tiene estructura: color y attachment (no numérico)

| Prueba | Observado | Nulo | p | Holm |
|---|---|---|---|---|
| Cambios de R/V a lo largo del quipu | 28 | 51.4 | **0.001** | 0.003 |
| Nº de "bloques" de color en los colgantes | 88 | 164.0 | **0.001** | 0.003 |
| Asociación V ↔ blanco (colgantes) | 112 | 103.2 | **0.005** | 0.005 |
| Correlación posición ↔ R (Spearman) | ρ = 0.516 | — | <1e-4 | — |
| Correlación posición ↔ W | ρ = 0.120 | — | 0.044 | — |
| Correlación posición ↔ valor | ρ = −0.132 | — | 0.027 | — |

Interpretación: **hay ~la mitad de cambios de attachment y de color de los esperados por azar.**
El quipu está ordenado en **bloques**: attachment **V** domina la mitad izquierda (grupos 1–8) y
**R** la derecha (grupos 9–12); análogamente la mitad izquierda es más blanca y la derecha
introduce marrones (MB/RL). Rho(orden, R) = 0.52 confirma un gradiente izquierda→derecha. **78
colgantes llevan color (no blancos) y NO tienen nudo alguno**: el color porta información
independiente del valor.

### 3.4 Contexto comparado: UR003 dentro de Leymebamba

UR003 es, con 758 cuerdas, **el quipu más grande de los 22 de Leymebamba**… y a la vez el de
**menores valores**: suma total 893 y máximo 11, frente a 1 500–261 000 y máximos de 90–15 746 en
el resto (p.ej. UR011 suma 261 452, máx 15 746; UR006 —el "calendario/censo" de Urton— 3 037,
máx 521). **UR003 no es un registro decimal de magnitudes como el resto de la colección.**

### 3.5 Anomalías y ruido

- **Grupos g0, g7, g13**: una sola cuerda, sin nudos (posibles separadores/marcadores).
- **Grupo g14**: un único colgante (p281) con **9 subsidiarias todas sin nudos** (un "abanico").
- 5 uniones `?`, 5 colores `MIX`, 2 colores con rango; 11 cuerdas de OKR no están en KFG (758 vs 769).
- **Nota de campo del OKR (decisiva):** *"interrupción por descomposición del cordón principal;
  descartamos cantidad de pendientes (con subsidiarias) por su fragilidad; empezamos de nuevo en un
  punto artificial con hilo sintético (verde-caña) amanado al cordón principal"*. El tramo final
  (grupos 13–14, a 112 cm, tras un hueco de ~37 cm) es **posterior a un empalme artificial**: los
  datos están **incompletos** y el "quipu" reconstruido no es íntegro.
- Valor máximo 11 (p129); sólo 2 nudos simples en todo el quipu.

## 4. Lectura más probable y nivel de evidencia

**Propuesta.** UR003 **no es un quipu aritmético/decimal**. Es un registro **categórico**:
cada **colgante** ≈ una unidad de registro (persona/ítem) y cada **grupo** ≈ una categoría o
subconjunto; la información principal va en el **color** y en el **attachment recto/verso**
(bloques izquierda→derecha), con el **valor** como conteo pequeño (0–11, mayoritariamente 0/1) y la
**jerarquía** (subsidiarias, casi siempre sin valor) como detalle/desglose. La mitad de los
colgantes no tiene nudo: el color solo ya distingue.

- **Nivel: apoyado con datos** — *que UR003 carece de aritmética interna y usa sólo nudos de
  unidades* (máx 11, 2 nudos simples; KFG y OKR coinciden; todos los p-valores ≈ 1). **Bien apoyado**.
- **Nivel: apoyado con datos** — *que porta estructura no numérica en color y attachment R/V*
  (permutaciones p = 0.001/0.001/0.005, que sobreviven Holm y replican el hallazgo publicado de
  KH0239 con p = 0 en el test de attachment binario R/V, `repo-rv-repro`).
- **Nivel: propuesto** — *que el género sea una lista/censo con color como categoría*. Encaja con
  el nicho: la colección de la Laguna de los Cóndores es de **contexto funerario** y Urton
  (2001, 2005) interpreta UR6 (misma colección) como **calendario bienal + censo de
  contribuyentes**; pero **UR003 NO replica la estructura de UR6** (UR6 = 24 conjuntos de 29–31
  cuerdas; UR003 = 15 grupos de tamaños irregulares 1–60 y valores mínimos). No hay evidencia de
  periodicidad calendárica ni de totales demográficos.
- **Nivel: especulativo** — asignar un referente concreto (qué colores = qué categorías, qué
  grupos = qué ayllus/parcialidades). Sin clave externa no es decidible.

**Contraste con la literatura (grep en `docs/fichas/`).** Clindaniel (2019) clasifica los khipus
en *banded* vs *seriated* según **patrones de color** (no numéricos) y encuentra que los de
**magnitud alta** tienden a *seriated*; UR003, de magnitud ~1 (máx 11), cae del lado *banded*, que
es justo lo que observamos (bloques de color, `num_banded_clusters = 4`, y nuestro test de runs
p = 0.001). Esto **refuerza** la lectura de que UR003 es un khipu "de patrón de color", no de
cuentas. La advertencia metodológica del estado del arte (Saez-Rodríguez, UR19) manda no forzar
lecturas numerológicas con n=1; aquí la disciplina es: **no afirmamos desciframiento, sólo
estructura y ausencia de aritmética.**

## 5. Resultados negativos (explícitos)

1. No hay cuerdas superiores (union T): la comprobación "superior = suma de grupo" es inaplicable.
2. Ninguna relación aritmética interna supera el azar (A, A2, B, C, D: p = 0.56–0.96; Holm = 1).
3. No hay sumas de colgante = subsidiarias (de hecho hay menos que por azar).
4. No hay grupos que sumen igual salvo el par trivial g5 = g10 = 51 (1 par, p = 0.65).
5. No hay subsecuencias de valor repetidas entre grupos (p = 0.18).
6. No hay razones constantes entre grupos; las sumas de grupos son todas distintas (salvo grupos
   vacíos = 0).
7. El "seriado" del KFG (11 clusters, 73 %) es un **patrón de color** (Clindaniel), no una
   progresión numérica: nuestra prueba de monotonía de valores da 1 cluster (≤ azar).

---

## 6. Para el coordinador

- **UR003 (KH0239) NO es un quipu decimal/aritmético.** Máximo valor **11**, media 1.18, **sólo 2
  nudos simples** en todo el quipu (496 nudos: 301 fig-ocho + 189 largos + 2 simples); KFG y OKR
  coinciden. La codificación decimal (decenas/centenas) no se usa.
- **No hay ninguna aritmética interna.** madre = Σ hijas (37/206, p = 0.91), colgante = Σ
  descendientes (p = 0.90), mitades equilibradas (p = 0.56), clusters de igual suma (p = 0.65),
  sumas homólogas cruzadas (p = 0.96), subsecuencias repetidas (p = 0.18). **Todos Holm ≈ 1.** En
  tres pruebas hay *menos* coincidencias que por azar. Las "sumas" que detecta el KFG (p129, p56,
  g5 = g10 = 51) son casos aislados dentro del rango nulo, no un sistema.
- **No hay cuerdas superiores (union T).** La comprobación "superior = Σ grupo" es inaplicable.
- **Lo que SÍ es estructura es lo no numérico:** attachment y color están **bloqueados** muy por
  encima del azar (cambios de R/V: 28 vs 51.4, p = 0.001; bloques de color: 88 vs 164, p = 0.001;
  V↔blanco p = 0.005; Holm ≤ 0.005). ρ(orden, R) = 0.52: mitad izquierda **V/blanca**, mitad
  derecha **R/marrón**.
- **Replicamos un resultado publicado:** `repo-rv-repro` da **p = 0 para KH0239** en su test de
  attachment binario R/V; nuestro test independiente (semilla 0) da **p = 0.001**. Es la señal más
  sólida del quipu y es **apoyada con datos**.
- **UR003 es el mayor de los 22 quipus de Leymebamba (758 cuerdas) y el de mínima magnitud
  (Σ = 893, máx 11)**, frente a 1 500–261 000 del resto. No es del mismo género contable que
  UR006/UR011. **No replica** la estructura calendárica de UR6 (24 conjuntos de 29–31). No hay
  censo/calendario detectable.
- **Lectura propuesta (nivel "propuesto"):** registro **categórico** — colgante ≈ ítem/persona,
  grupo ≈ categoría, color y attachment = código, valor = conteo pequeño (0–11), y **78 colgantes
  con color y sin ningún nudo** ⇒ el color porta información por sí solo. Encaja con el nicho de
  Leymebamba (contexto funerario, Urton 2001/2005) y con Clindaniel 2019 (khipus de baja magnitud
  = *banded*, patrón de color). El referente concreto es **especulativo**.
- **Advertencia de integridad:** la nota de campo del OKR dice que el **cordón principal estaba
  descompuesto**, se **descartaron pendientes** y se reinició la anotación en un **punto artificial
  con hilo sintético verde**; los grupos 13–14 (a 112 cm, tras un hueco de 37 cm) son
  **posteriores al empalme**. Los datos de UR003 están **incompletos**; conviene usar cualquier
  lectura con cautela.
- **Recomendación siguiente:** (a) tratar UR003 como caso testigo de "quipu no numérico" y
  contrastar su patrón **color+attachment** con los otros UR/Leymebamba; (b) no gastar esfuerzo en
  buscar sumas en UR003 (quedó refutado); (c) la vía productiva es decodificar el **código de
  color y la dicotomía V/R** (¿dos mitades hanan/hurin?, ¿dos registradores?), no los valores.
