# UR1032 — Lectura profunda de un quipu nazca (541 cuerdas)

**Investigador:** slot `ds`, carpeta `analisis/ds/k_UR1032/`
**Datos:** `analisis/datos/cuerdas.csv`, `grupos.csv`, `quipus.csv` (KFG) + OKR
`data/external/open-khipu-repository/data/khipu.db` + `khipu_summary.csv`. No regenerados.
**Identidad:** UR1032 = **KH0034 = AS032**, Peabody Museum 42.28.30/4532, `procedencia=Nazca`,
`region=Unknown` (KFG/OKR). Cordón principal blanco (W), estructura P.
**Scripts:** `01_estructura.py` … `14_posicional.py` (reproducibles, semilla 0).

---

## 1. Pregunta

¿Qué registro es UR1032 (Nazca, 541 cuerdas)? ¿Tiene estructura aritmética interna
verificable (colgante = Σ subsidiarias, grupo = Σ grupos, valores repetidos,
periodicidad de color) y qué tipo de registro explica mejor su forma? ¿Qué cuerdas
no encajan y podrían ser información no numérica?

## 2. Método

- Reconstrucción por jerarquía (`cuerda`/`nivel`/`padre`/`grupo`) con pandas.
- Aritmética: colgante vs Σ subsidiarias; grupo vs grupos (posición a posición, patrón
  documentado en otro quipu nazca, AS215); pares de grupos adyacentes; igualdades escalares.
- **Nulo explícito (BRIEF §2):** para cada patrón se permutan los valores **dentro de
  UR1032** (respetando la estructura de grupos cuando aplica), 1000–5000 veces, **semilla 0**;
  p-valor empírico de una cola (el lado de la hipótesis).
- Corrección múltiple **Holm** sobre el banco de 7 pruebas. Niveles:
  bien apoyado / apoyado con datos / propuesto / especulativo.

---

## 3. Estructura reconstruida (cifras)

**Conteos.** 541 = **415 colgantes (nivel 0)** + **126 subsidiarias (nivel 1)**.
**108 grupos** de colgantes. Máximo nivel jerárquico = 1 (no hay sub-sub-cuerdas).

**Sin cuerda superior.** `union`: **V = 403, U = 130 (casi todas subsidiarias), R = 8;
ninguna T** (cuerda superior). Es un quipu de colgantes "simples", sin sumario superior.
`torsion`: **S = 540, 1 desconocida** (monótona). `tipo`: todas `p`.

**Colores (colgantes):** **LB = 260**, **W = 153**, B = 1, ? = 1. Sólo dos colores reales.
KFG registra `num_ascher_colors = 12`, pero casi todo es LB (azul claro) y W (blanco).

**El color está determinado por el tamaño del grupo:**
- 50 grupos de **5 cuerdas → todas LB (azul)**.
- 51 grupos de **3 cuerdas → todas W (blanco)**.
- 6 grupos de **1 cuerda** + 1 grupo de **6 cuerdas** (LB).
- Excepciones: 2 cuerdas (una "B" dentro del grupo LB g3; un color "?" dentro del grupo
  blanco g76). Es decir, **color = tamaño de grupo, salvo 2/415 cuerdas**.
KFG marca estos grupos como **`num_banded_clusters = 107/108`** (patrón de bandas de color),
lo que confirma que la alternancia cromática es una propiedad reconocida del objeto.

**Plantilla de módulo.** Los grupos alternan **5-azul, 3-blanco, 5-azul, 3-blanco…**
Un "módulo" = 8 colgantes = 5 azules + 3 blancos (existen 94 módulos bien formados).
La alternancia se invierte en un punto del quipu (a partir del grupo 54 pasa a 3-5).

**Marcadores (M).** OKR clasifica **5 cuerdas con `CORD_CLASSIFICATION='M' = marker`**:
`p58, p131, p204, p277, p342` (con `INVESTIGATOR_CORD_NUM = 1,2,3,4,5` → **M1–M5**).
Son **cuerdas sin nudos** (valor 0), LB. Coincide con la nota de Thompson (2026):
"el M1 se ubica entre p57–p58" para KH0034. **Los marcadores dividen el quipu en 6
secciones** (la 1.ª también empieza con una cuerda suelta, p1, blanca, sin nudos):

| sección | colgantes | n | composición | Σ valores |
|---|---|---|---|---|
| 1 | p1–p57 | 57 | 7 módulos (35 azul + 21 blanco) + p1 | 51 |
| 2 | p58–M1 … p130 | 73 | M1 + 9 módulos (45+27) | 31 |
| 3 | p131–p203 | 73 | M2 + 9 módulos (45+27) | 43 |
| 4 | p204–p276 | 73 | M3 + 9 módulos (45+27) | 46 |
| 5 | p277–p341 | 65 | M4 + 8 módulos (40+24) | 44 |
| 6 | p342–p415 | 74 | M5 + 8 módulos + 3 blancas extra + grupo de 6 | 42 |

Cada sección = **número entero de módulos de 8** (7, 9, 9, 9, 8, 8). Esto es demasiado
regular para ser azar y encaja con "secciones separadas por marcadores" (cuerdas vacías
como separadores: patrón ya observado por Sivan 2026 en otros khipus).

**Valores.** Media 0.62 en colgantes; máx 11. Distribución: 0×266, 1×91, 2×39, 3×9, 4×6,
6×1, 10×2, 11×1. **303 cuerdas con valor 0 y sin nudos = ausencias** (no ceros; BRIEF §6):
**266 de 415 colgantes (64 %) están vacíos**, sólo 149 (36 %) llevan nudo.
Los nudos son casi todos de **figura-de-ocho** (E → valor 1) o **largos** (L → 2-9):
en 238 cuerdas con nudo, primer tipo **E = 169, L = 66, S = 2**. Dirección de nudo:
**S = 104, Z = 131, U = 5**. Casi no hay nudos simples de decena (sólo 3 cuerdas con "1S": p48, p303, p345),
así que **no hay estructura decimal multinivel**.

**Patrón posicional dentro del grupo (bien apoyado).** Dentro de cada grupo, el valor
se concentra en el **centro** y los **bordes** quedan vacíos: en grupos de 5, fracción con
nudo por posición = [0.20, 0.44, 0.54, 0.50, 0.30]; en grupos de 3 = [0.28, 0.43, 0.26].
Prueba de permutación dentro de cada grupo: centro-bordes obs 110, **p < 0.0001** (g5);
obs 14, **p = 0.0014** (g3).

---

## 4. Aritmética interna — casi toda NEGATIVA

| prueba | estadístico | p empírico | p Holm |
|---|---|---|---|
| T1 color ~ tamaño de grupo (5=LB, 3=W) | 1.989 (de 2.0) | 0.000 | **0.000** |
| T2 valor medio: grupos de 5 > grupos de 3 | 0.265 | 0.012 | 0.060 |
| T3 colgante = Σ subsidiarias | 36/114 = 31.6 % | 0.981 | 1.000 |
| T4 Σ grupo de 5 = Σ grupo de 3 adyacente | 14/94 = 14.9 % | 0.581 | 1.000 |
| T5 autocorrelación lag-8 (periodicidad) | −0.019 | 0.696 | 1.000 |
| T6 Σ grupo = Σ a 2 grupos de distancia (mismo color) | 26.1 % | 0.027 | 0.108 |
| T7 tasa de subsidiaria: grupos de 3 > grupos de 5 | 0.255 (0.47 vs 0.22) | 0.000 | **0.000** |

**Confirmado tras Holm:** T1 (color = tamaño) y T7 (los grupos blancos de 3 llevan más
subsidiarias). **T2** queda en el borde (Holm = 0.06): apoyado, no bien apoyado.

**Aritmética específica (el patrón de AS215, otro quipu nazca del Peabody con suma
posición-a-posición "grupo 3 = grupos 7+9+11+13+15"):** en UR1032 se probó
"grupo = Σ de 3 ó 5 grupos del mismo color, posición a posición" y "grupo = Σ de k grupos"
→ **0/40, 0/44, 1/45 (p = 0.70), ventanas 0/45** etc. **No hay ninguna relación de suma.**
Consistente con KFG, que reporta para UR1032 **`num_top_cord_sum_clusters = 0` y
`num_top_cord_double_sum_clusters = 0`**.

**Valores repetidos / módulos repetidos.** Hay módulos idénticos (p. ej. azul (0,0,0,0,1)
aparece 16 veces; vector blanco (0,0,1) aparece 32 veces), pero es la **tasa base** de
valores enteros pequeños (0-3) en vectores cortos: el nulo de permutación reproduce
esos recuentos (T4, T6 no significativos). No es evidencia de estructura repetida.

---

## 5. Lectura más probable

**Lo que está bien apoyado:** UR1032 es un quipu **estructurado por color y separadores,
sin aritmética**. Su esqueleto es un patrón de bandas (5 azul + 3 blanco = módulo de 8),
cortado por **5 marcadores físicos** (M1–M5, cuerdas vacías) en **6 secciones** de 7–9 módulos;
los valores son diminutos y **64 % de los colgantes están en blanco**. El color no codifica
cantidades sino la **plantilla** (5 vs 3). Dentro de cada grupo el valor ocupa el centro,
no los bordes.

**Interpretación (propuesta):** un **registro de tipo lista/tally administrativo de bajo
nivel** ("de trabajo" en el sentido de Medrano y Khosla 2024) más que una cuenta aritmética.
El sistema de módulos de 8 y las 6 secciones sugieren una clasificación **categórica**
(p. ej. 6 unidades/parcialidades, cada una con 7–9 sub-registros), con la dicotomía
azul/blanco marcando dos tipos dentro de cada módulo. **No es un libro de tributo ni de
depósito** (esos muestran sumas; aquí no hay ninguna) ni un censo numérico completo
(no hay magnitudes). Un **calendario** es **especulativo**: 6 secciones y módulos de 8 no
mapean de forma natural sobre meses/semanas, y no hay periodicidad de valores (T5).

**Filas y columnas (propuesta):** filas = las **unidades de las 6 secciones** o los
**módulos (8 colgantes)**; columnas = las **3-5 cuerdas de cada grupo**, tipadas por color.
El "valor" sólo codifica presencia/ausencia o una marca 0-4, no una magnitud.

**Nivel de evidencia:** forma y color **bien apoyados** (T1, T7); ausencia de aritmética
**bien apoyada** (varias pruebas nulas concordantes + KFG); lectura como registro
administrativo de bajo nivel **propuesta**; censo/calendario específicos **especulativos**.

## 6. Lo que no encaja / información no numérica

- **Grupo de 6 cuerdas (g100, p335–p340):** rompe la plantilla 5/3. Tres blancas "de más"
  al final de la sección 6. Posible error de transcripción o tramo de cierre.
- **Inversión del patrón** (5-3 → 3-5) a partir del grupo 54 (M3). Cambio de convención a
  mitad del registro.
- **Excepciones de color:** 1 cuerda "B" en un grupo azul (g3) y 1 color "?" en un grupo
  blanco (g76).
- **Cuerdas sin nudos = marcadores** (M1–M5) y el inicio p1: información **no numérica**
  (separadores). Son el 1.2 % de las cuerdas pero definen toda la macroestructura.
- **8 cuerdas unión R (recto)** frente a 403 V — sin patrón claro de posición (no marcan
  frontera de grupo de forma consistente).
- **Notas de campo / anomalías registradas:** p45s1 rota (2000); p72s1 y p275s1 con nudo
  cambiado por Urton (1E→2L); p141s1, p267s1, p270s1 con fibra distinta ("¿camélido?"; en
  el género *Camelidae*); p278 "porción remendada, 5 colgantes excluidos" (Ascher);
  p282 reparación incorrecta; p328s2 nudo suelto; p390s1 rota. Indican **daño y reparación**,
  no datos.
- **Casi 2/3 de las cuerdas vacías** ⇒ gran parte del contenido es **presencia/ausencia**
  (posible información no numérica o binaria), no un registro de cantidades.

## 7. Resultados negativos (para el registro)

- No hay cuerda superior ni unión T (0 cuerdas); no hay sumas de ningún tipo.
- No hay "colgante = Σ subsidiarias" (p = 0.98).
- No hay relación de suma entre grupos adyacentes ni a distancia (p = 0.58 y 0.11).
- No hay periodicidad de valores (lag-8, p = 0.70).
- La longitud del cordón principal no está en KFG (`pc_largo = 0`); Thompson (2026) la
  corrige a 91.5 cm y pide "dar la vuelta al khipu" ⇒ el orden p1→p415 podría estar invertido.

---

## Para el coordinador

- **UR1032 (=KH0034=AS032, Peabody, Nazca) es un quipu limpio y muy regular pero SIN
  aritmética.** Ninguna relación de suma se sostiene frente al nulo: colgante=Σsubs
  p=0.98; grupo=Σgrupos (patrón AS215, posición a posición) 0/40; pares adyacentes p=0.58.
  Coherente con KFG (`num_top_cord_sum_clusters=0`). **Negativo sólido**, no ruido.
- **Color = tamaño de grupo (bien apoyado):** 50 grupos de 5 = azules (LB), 51 grupos de 3
  = blancos (W), salvo 2/415 cuerdas; KFG lo reconoce (`num_banded_clusters=107`).
  La dicotomía azul/blanco es **plantilla estructural**, no cantidad.
- **OKR identifica 5 cuerdas "M" (marcador)** —M1–M5 = p58, p131, p204, p277, p342— que
  **dividen el quipu en 6 secciones** de 7–9 módulos, cada módulo = 8 colgantes (5 azul + 3
  blanco). M1 coincide con el "M1 entre p57–p58" de Thompson (2026). Esto es el hallazgo
  organizativo más fuerte y es **bien apoyado**.
- **Dentro del grupo, el valor ocupa el centro y los bordes quedan vacíos**
  ([0.20,0.44,0.54,0.50,0.30] en grupos de 5; p<0.0001). Sugiere cuerdas-marco y centro-datos.
- **64 % de los colgantes están vacíos** (303 sin nudos); sólo 149 llevan nudo, casi todos
  figura-de-ocho (=1) o largos (2-9); no hay jerarquía decimal (3 cuerdas con decena). El
  contenido es sobre todo **presencia/ausencia → posible información no numérica/binaria**.
- **Nivel de evidencia:** estructura y color **bien apoyados**; ausencia de aritmética
  **bien apoyada**; lectura como registro administrativo de bajo nivel ("de trabajo")
  **propuesta**; censo o calendario **especulativos** (no superan controles).
- **Anomalías:** grupo de 6 cuerdas (g100) rompiendo el 5/3; inversión 5-3→3-5 tras M3;
  2 cuerdas de color excepcional; varias cuerdas rotas/remendadas (p45s1, p278, p282, p328s2,
  p390s1) y fibras "camélido" (p267s1, p270s1). Ruido de conservación, no datos.
- **Siguiente ronda (recomendado):** (1) tratar UR1032 como **caso de referencia negativo**
  junto a los "nazca" del Peabody/nazca-valle (AS215, AS074, UR28) para aislar **qué distingue
  a un quipu nazca con sumas de uno sin ellas**; (2) verificar la hipótesis "6 secciones =
  6 unidades" replicando el conteo de marcadores 'M' en todo el corpus OKR (¿cuántos quipus
  tienen M1–M5?); (3) probar lectura **invertida** (Thompson: "dar la vuelta") y ver si las
  secciones se igualan; (4) modelar el patrón de presencia/ausencia como matriz binaria
  (¿columnas tipadas por color?) en vez de valores.
