# Lectura profunda de un quipu: UR019 (KH0255 / CMA-480)

Equipo: `analisis/ds/k_UR019/`. Fecha: 2026-10-17. Scripts: `estructura.py`,
`analisis.py`, `saez_test.py`, `patrones.py`, `controles_finales.py`.

## 0. Pregunta

¿Qué es UR019 y qué registra? En concreto: (1) reconstruir su estructura completa;
(2) buscar toda la aritmética interna (colgante = suma de subsidiarias, superior =
suma de grupo, grupo = suma de grupos, valores repetidos, razones constantes,
periodicidad de color) y comparar cada patrón con un nulo (barajar valores dentro
del quipu, 1000×, semilla 0); (3) proponer la lectura más probable y su nivel de
evidencia; (4) señalar anomalías y si podría haber información no numérica.

## 1. Estructura reconstruida

**Identificación.** KFG `UR019` = OKR `KH0255` = CMA-480/LC1-109.3, museo Centro
Mallqui (Leymebamba, Amazonas). Procedencia declarada: Leymebamba, región
Chachapoyas. Cordón principal: algodón blanco (W), 26,0 cm, estructura P.
(Fuente primaria citada por la ficha 2014: Urton 2003, pp. 130/145/180-181.)

**Tamaño.** 18 cuerdas = **13 colgantes + 5 subsidiarias** (nivel 2), en **4 grupos**.
No hay cuerdas superiores: `union` no contiene ninguna T (reparto V=8, R=4, U=6).
Todas las cuerdas tienen torsión S. Longitud de los colgantes: 16–49,5 cm.

| grupo | pos. (cm) | cuerdas | colgantes | subsidiarias | espacio |
|---|---|---|---|---|---|
| 0 | 0,5 | p1–p3 | 3 | p3s1 | 1,0 cm |
| 1 | 2,5 | p4–p7 | 4 | p6s1, p7s1 | 1,0 cm |
| 2 | 4,5 | p8–p12 | 5 | p9s1, p10s1 | 2,0 cm |
| 3 | 7,5 | p13 | 1 | — | — |

**Cuerda por cuerda** (valor KFG; `nudos` de arriba→abajo; color Ascher;
`union`: V=verso, R=recto, U=desconocida):

| cda | grupo | valor | nudos | color | union | largo | term. | notas |
|---|---|---|---|---|---|---|---|---|
| p1 | 0 | 0 | — (sin nudos) | AB | U | 0,5 | B | |
| p2 | 0 | 0 | — | AB | V | 16,0 | B | |
| p3 | 0 | **18** | 1S(10,5,Z)=10 ; 8L(20,0,Z)=8 | AB | V | 32,0 | K | |
| p3s1 | 0 | **9** | 9L(13,5,Z)=9 | W:KB | U | 31,0 | U | |
| p4 | 1 | **1** | 1E(20,0,**S**)=1 | MB | V | 39,5 | U | |
| p5 | 1 | 0 | — | AB | R | 21,0 | B | |
| p6 | 1 | **10** | 1S(9,5,Z)=10 | KB | U | 31,0 | U | doblado en cordón princ. |
| p6s1 | 1 | 0 | — | W | U | 32,0 | U | "nudo desanudado" |
| p7 | 1 | **1** | 1E(12,0,Z)=1 | MB | R | 18,5 | U | |
| p7s1 | 1 | **2** | 2L(8,0,Z)=2 | KB | R | 13,0 | U | |
| p8 | 2 | 0 | — | MB | V | 40,0 | K | |
| p9 | 2 | **28** | 2S(9,0,Z)=20 ; 8L(17,0,Z)=8 | W:KB | V | 24,0 | U | |
| p9s1 | 2 | **3** | 3L(11,5,Z)=3 | W | U | 17,0 | K | |
| p10 | 2 | **20** | 2S(9,0,Z)=20 | MB:KB | V | 33,0 | K | |
| p10s1 | 2 | **8** | 8L(15,5,Z)=8 | W:KB | U | 35,0 | U | |
| p11 | 2 | 0 | — | W | V | 49,5 | K | |
| p12 | 2 | 0 | — | BL | V | 29,0 | K | |
| p13 | 3 | 0 | — | BL | R | 36,0 | U | |

**Direcciones de nudo (OKR y cadena KFG coinciden).** Todos los nudos son **Z**
salvo el único nudo figura-de-ocho de p4, que es **S**: reparto S=1, Z=11.

**Valores.** Colgantes: `[0,0,18,1,0,10,1,0,28,20,0,0,0]` → **Σ = 78**. Subsidiarias:
`[9,0,2,3,8]` → **Σ = 22**. **Σ total = 100.** Solo 6 de 13 colgantes llevan nudo
(p3, p4, p6, p7, p9, p10). Los 7 colgantes sin nudo (p1, p2, p5, p8, p11, p12, p13)
son **ausencia** (regla del brief), no ceros reales. Sumas de grupo (colgantes):
**G0=18, G1=12, G2=48, G3=0**.

## 2. Método y controles

- Unidad de análisis: el quipu (UR019). Las pruebas internas usan **permutación
  de los 18 valores dentro del quipu** (nulo que preserva el multiset de valores y
  la estructura de madres/hijas pero rompe la asignación), 1000 iteraciones,
  semilla 0, p empírico `(≥obs + 1)/(N+1)`. Los indicadores estructurales
  (tiene-nudo, color) se contrastan además permutando el propio indicador.
- Corrección por comparaciones múltiples: **Holm y BH-FDR** sobre el conjunto de
  tests. Se reportan también los negativos.
- Control externo independiente: las características de suma precomputadas del
  *data-science-khipu-article* (`ascher_sum_relations/*.csv`) para UR019.

## 3. Resultados con cifras

### 3.1 Jerarquía aritmética (colgante ⇄ subsidiarias ⇄ grupos)

- **Colgante = suma de sus subsidiarias:** 0 de 5 madres lo cumplen. Nulo:
  media 0,95, máximo 4; p = 1,00. **Negativo.**
- **Cuerda superior = suma de grupo:** no aplica; **UR019 no tiene cuerdas
  superiores** (0 de 18 con `union = T`).
- **Grupo = suma de otros grupos / razón entre sumas:** las sumas no nulas de
  grupo son {18, 12, 48}; hay 1 razón entera (48 = 4 × 12). Nulo: media 0,57,
  máximo 5; p = 0,41. **Negativo.**

### 3.2 Valores repetidos, razones y ternas aditivas

- **Valores repetidos:** solo un par igual (p4 = p7 = 1). Es un artefacto trivial
  del multiset (nulo: siempre 1). **No informativo.**
- **Razones enteras (2..10) entre valores ≠ 0:** 18 pares (p. ej. 18=2·9, 20=2·10,
  10=10·1). El recuento es **invariante a la permutación** (propiedad del multiset,
  media nula = 18): no es un test.
- **Ternas a + b = c** (cuerdas distintas): 10 ternas, p. ej. p6+p10s1 = 10+8 = 18
  = p3; p10+p10s1 = 20+8 = 28 = p9; p3s1+p7 = 9+1 = 10 = p6; p4+p7 = 1+1 = 2 =
  p7s1. Nulo: media 9,47, máximo 15; **p = 0,51**. Es lo esperable por azar con
  números pequeños. **Negativo** (salvo la relación 3.3).
- **Tipos con algún acierto:** 4 de 5; nulo media 4,12; p = 0,82. **Negativo.**

### 3.3 El "descubrimiento" de Saez-Rodriguez (2014) bajo control

Saez ([ficha 2014](2014-Saez-Rodriguez-khipu-UR19)) sostiene que
Σ(colgante × subsidiaria) = 40,9 y que 40,9 ÷ 13 = π; que "S-knots" = 24,6 y
"Z-knots" = 16,3; y que 24,6 ≈ distancia Tierra–Luna ÷ 10.000.

- Con los datos KFG/OKR, Σ(colgante × subsidiaria) = 408 → 408/10 = 40,8 →
  **/10/13 = 3,138** (π = 3,1416; se desvía 0,11 %).
- Test de la operación **fija** (×hijas, ÷10, ÷13) contra el nulo de permutación:
  p = 0,001. Pero **la operación es post hoc**.
- **Control de multiplicidad:** con una rejilla de divisores (1..30, ×10, ×100,
  ×1000, ×10000) frente a 15 "constantes famosas" y tolerancia 0,5 %, la suma 408
  produce **4 aciertos** (π, e, 24 y 27,2). El nulo da media 0,85, máximo 5;
  **p = 0,02**, pero al corregir por las otras pruebas queda **Holm = 0,12,
  BH = 0,05**: **no es robusto**. El alto puntaje está además confundido con la
  magnitud de la suma (408 es un valor atípicamente grande, en la cola del nulo),
  no con la "estructura significativa".
- **Partición S/Z no reproducible:** el dato real solo tiene **1 nudo S** (p4) y
  11 Z. La división 24,6/16,3 en que se basa la tesis **no existe** en UR019.
  Nivel de la tesis astronómica: **especulativo** (igual que la ficha).

### 3.4 Color

- Familias (colgantes): p1–p3 marrón (AB); p4–p7 marrón/AB/KB; p8 MB, p9 y p10
  mixto (W:KB, MB:KB), p11 blanco, p12 y p13 azul (BL).
- **Adyacencias de color** (misma familia entre colgantes consecutivos): obs = 9;
  nulo global media 4,65, **p = 0,001 → Holm 0,007, BH 0,007 (sobrevive)**. Pero
  el color está confundido con los grupos: con un nulo que permuta colores **dentro
  de cada grupo**, p = 0,032 (Holm 0,13): **no sobrevive**. Conclusión: el color
  forma bloques ~alineados con los grupos, no una periodicidad adicional fiable.
- **Periodicidad** del indicador tiene-nudo: el patrón visible `0 0 1 1 0 | 1 1 0 |
  1 1 0 | 0 0` (bloques (1,1,0) de p3 a p11) es tentador, pero lag-3 da 7/10
  coincidencias con p = 0,13; los pares (1,1) adyacentes p = 0,41. **Negativo**
  (con n = 13 hay poca potencia).
- **Subsidiarias vs colgantes:** 4 de 5 subsidiarias son de base blanca
  (W o W:KB) frente a 2 de 13 colgantes; Fisher p = 0,022, pero **Holm = 0,12**.
  Sugerente (convención "subsidiaria = marca secundaria"), no robusto.
- `union`: los colgantes son mayoritariamente V (8), y **el grupo 2 es 100 % V**
  (p8–p12); las subsidiarias son mayoritariamente U (4/5). Descriptivo.

### 3.5 Tabla de controles (Holm/BH)

| test | obs | p | Holm | BH |
|---|---|---|---|---|
| color adyacente (global) | 9 | 0,0010 | **0,0070** | **0,0070** |
| Saez π (multiplicidad) | 4 | 0,0200 | 0,1199 | 0,0507 |
| subsidiaria blanca (Fisher) | — | 0,0217 | 0,1199 | 0,0507 |
| color adyacente (intragrupo) | 9 | 0,0320 | 0,1279 | 0,0559 |
| tiene-nudo lag-3 | 7 | 0,1299 | 0,3896 | 0,1818 |
| tiene-nudo pares | 3 | 0,4056 | 0,8112 | 0,4732 |
| madre = suma(hijas) | 0 | 1,0000 | 1,0000 | 1,0000 |

(m = 7 tests; solo el **bloque de color global** sobrevive; y desaparece al
controlar por grupo.)

### 3.6 Control externo (KFG, `ascher_sum_relations`)

Para UR019 (id 1000000) las características precomputadas dan: sumas
colgante–colgante = 0; sumas de clúster = 0; cuerdas superiores = 0; clústeres
decrecientes = 0; bandas de suma = 0 de 4 clústeres. **La única relación de suma
detectada** es un *pendant–sub neighbor*: `p10 (20) + p10s1 (8) = p9 (28)`. Esto
**confirma de forma independiente** (i) que UR019 es aritméticamente casi vacío y
(ii) la única igualdad "de diseño" de mi análisis.

## 4. Resultados negativos (resumen)

- No hay jerarquía de sumas: colgante ≠ Σsubs; no hay superiores; no hay
  relación entre sumas de grupo.
- Las ternas a+b=c, razones y valores repetidos son **indistinguibles del azar**.
- La "periodicidad" de color/nudos **no supera el azar** ni la corrección.
- La partición S/Z y las interpretaciones astronómicas de Saez **no se reproducen**.
- La asociación subsidiaria–blanca y el bloque de color desaparecen al controlar
  por grupo / corregir.

## 5. Anomalías e información no numérica

- **p1**: solo 0,5 cm, sin nudos, `union = U`. Es un abdomen/fragmento o un
  marcador, no una cuerda de datos. p2 y p5 también son cortas/sin nudos con
  terminación **B (rota)**. Las 3 cuerdas con terminación B son justamente p1, p2,
  p5 (todas vacías) → posible pérdida física de información.
- **p6 "doblado en cordón principal"** y **p6s1 "nudo desanudado"**: dos marcas
  físicas raras; la segunda implica un valor 0 que podría no ser numérico.
- **p4** porta el único nudo **S** (figura de ocho); el resto son Z. Una sola
  oposición S/Z no sostiene ninguna bipartición.
- **7 de 13 colgantes vacíos** y 2 de 5 subsidiarias vacías: el "contenido" ocupa
  ~1/3 de las cuerdas. Compatible con un registro breve, no con un censo.
- **Colores mixtos** (W:KB, MB:KB, W:KB en p9, p10, p10s1): hilos barber-pole.
  Son el mejor candidato a **información no numérica** (categoría/material) junto
  con `union` R/V, la dirección y las terminaciones. La convención
  "subsidiarias de base blanca" refuerza que el color codifica **nivel/rol**, no
  cantidad.
- Color = eje semántico: los bloques de color por grupo recuerdan la función
  **categorial** del color documentada en el archivo (Urton 2003, 2019; ver
  `estado_del_arte.md` § sobre UR28: "la organización por color AB/MB").

## 6. Lectura más probable (con literatura) y nivel de evidencia

**Contexto documental.** UR019 es uno de los 32 khipus chachapoyas de la Laguna
de los Cóndores/Leymebamba ([ficha 2014] menciona Urton 2001). En ese mismo
archivo, Urton ([ficha 2001](2001-Urton-calendrical-tomb-text),
[ficha 2005](2005-Urton-khipu-archives)) interpreta **UR6** (762 colgantes) como
**calendario bienal + censo**, y describe conjuntos de tres términos como posibles
**"etiquetas"** de identidad. La [ficha 2026-Sivan](2026-Sivan_inca-spreadsheet)
clasifica cuerdas no decimales como STRING. El [estado del arte](estado_del_arte.md)
usa a Saez-Rodriguez como **contraejemplo metodológico** (n = 1, divisores post hoc).

**Escala.** UR019 es minúsculo dentro de su archivo: 18 cuerdas (percentil 4,5 %;
mediana Chachapoyas = 124) y Σvalor = 100 (mediana = 2.981). **No es** un censo ni
un gran libro de tributo como UR6.

**Hipótesis más probable (propuesto, evidencia débil):** un **registro
administrativo breve** (una cuenta/tally pequeña, tipo depósito o anotación de
unos pocos renglones), donde:
- las **columnas/categorías** = los 4 grupos y su color (marrón, mixto, blanco,
  azul); el color y `union` marcan la categoría/rol;
- las **filas/entradas** = los colgantes con nudo (p3, p4, p6, p7, p9, p10);
- las **subsidiarias** = sub-partidas o restos (p10s1 = 8 se suma a p10 = 20 para
  dar p9 = 28; p3s1 = 9 y p7s1 = 2 son otros sub-valores). La única suma interna
  "de diseño" (p9 = p10 + p10s1) sugiere que en el grupo 2 un colgante es el
  **subtotal** de otro más su subsidiaria.

**Lo que NO apoyo:** lectura calendárica/astronómica (π, distancia lunar) es
**especulativa**; no hay periodicidad ni razones que superen el nulo; la partición
S/Z no existe. El calificativo "portador de etiquetas" **no proviene** de la ficha
de UR019 (que es astronómica); la ficha de "knot labels" (2013) trata otro quipu
(VA 42527). Se deja constancia de la discrepancia.

**Nivel de evidencia global:**
- Estructura (18 cuerdas, 4 grupos, valores, direcciones, ausencia de superiores):
  **demostrado** (coinciden KFG y OKR).
- Ausencia de aritmética interna y fracaso de la lectura π/S-Z tras control:
  **apoyado con datos**.
- Clasificación categorial del color y convención subsidiaria–blanca:
  **apoyado con datos** (color) / **propuesto** (subsidiarias).
- Tipo de registro = tally administrativo breve: **propuesto** (no demostrado).
- Lectura astronómica: **especulativo** (refutada en su base S/Z).

## 7. Qué sigue (para la siguiente ronda)

- Replicar el test de multiplicidad "divisores × constantes" sobre **todos** los
  khipus chachapoyas para estimar la tasa base de coincidencias numéricas (¿cuántos
  "hallan" π por azar?).
- Comparar la convención color/grupo y subsidiaria–blanca en los 21 khipus
  chachapoyas restantes (¿es UR019 típico o atípico?).
- Buscar pares/tríos de "tres términos" (tipo UR6) en UR019–UR020.

## 8. Para el coordinador

- **UR019 es minúsculo y casi vacío:** 18 cuerdas, 4 grupos, 13 colgantes + 5
  subsidiarias; solo **6 de 13 colgantes** llevan nudos; **Σ = 100** (78 en
  colgantes + 22 en subsidiarias). No tiene **cuerdas superiores** (0 con union T).
- **Aritmética interna prácticamente nula:** colgante = Σsubs falla 0/5 (p=1,0);
  ternas a+b=c (10) no superan el azar (p=0,51); razones de grupo p=0,41. El único
  rasgo "de diseño" —confirmado de forma independiente por el toolkit KFG— es
  **p9 = p10 + p10s1** (28 = 20 + 8).
- **La tesis astronómica de Saez-Rodriguez no resiste:** Σ(colgante×subs)/10/13 =
  3,138 ≈ π, pero es post hoc; con rejilla de divisores la significación cae a
  Holm = 0,12/BH = 0,05 (no robusta). Su **partición S/Z (24,6/16,3) no existe**:
  hay 1 nudo S y 11 Z. Nivel: **especulativo**.
- **Único patrón que sobrevive la corrección:** el **color forma bloques** a lo
  largo de las cuerdas (p=0,001; Holm 0,007), pero se explica por la pertenencia a
  grupo (intragrupo p=0,03, no sobrevive). El color es **categorial**, no cantidad.
- **Mucha información probablemente no numérica:** colores mixtos (W:KB, MB:KB),
  unión R/V (grupo 2 = 100 % verso), dirección, terminaciones; 4/5 subsidiarias de
  base blanca (Fisher p=0,02, Holm 0,12 → sugerente).
- **Anomalías claras:** p1 = 0,5 cm sin nudos (fragmento); p2 y p5 rotas (B);
  p6 "doblado en el cordón principal"; **p6s1 "nudo desanudado"** (un cero que
  podría no ser numérico); p4 porta el único nudo S.
- **Lectura propuesta (evidencia débil):** un **registro administrativo breve**
  (tally/depósito), columnas = grupos/color, filas = los 6 colgantes con nudo,
  subsidiarias = sub-partidas. **No** es censo/tributo grande (percentil 4,5 % del
  archivo) **ni** calendario (sin periodicidad significativa).
- **Nivel de evidencia:** estructura = **demostrado**; ausencia de aritmética y
  refutación de π/S-Z = **apoyado con datos**; color categorial = **apoyado**;
  tipo de registro = **propuesto**; astronomía = **especulativo**.
- **Recomendación:** usar UR019 como caso de control (contraejemplo) y extender el
  test de multiplicidad a todo el archivo chachapoyas antes de aceptar cualquier
  coincidencia numérica.
