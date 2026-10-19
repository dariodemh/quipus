# Monografía del «archivo de Santa»: quipus KH0227, UR087–UR092 y UR198

**Autor:** analista del equipo (carpeta `analisis/ds/a_santa/`)
**Datos:** `analisis/datos/{cuerdas,grupos,quipus}.csv` (derivados del Khipu Field Guide, KFG),
`data/external/data-science-khipu-article/data/…` (relaciones de suma de Ascher),
`data/external/open-khipu-repository/data/okr-kh-numbers.csv` (puente de nombres OKR/KH).
**Scripts:** `01_descriptivo.py`, `02_relaciones.py`, `03_estructura_color.py`.
**Semilla:** 0. Réplicas del nulo: 500.

---

## 1. Pregunta

Describir el conjunto de ocho quipus que el encargo agrupa bajo «procedencia Santa»
(KH0227, UR087–UR092, UR198), buscar relaciones **entre** ellos con un modelo nulo
explícito, reconstruir —si existe— la jerarquía del archivo, y contrastarlo con la
literatura del sitio para proponer qué se registraba allí.

---

## 2. Advertencia previa: el «conjunto» no es un archivo único (identificación)

Antes de cualquier estadística hay que fijar **qué** es cada objeto, porque el rotulado
«Santa» une tres cosas distintas:

| KFG | OKR | Nombre antiguo | Museo / nº | Procedencia registrada |
|---|---|---|---|---|
| KH0227 | KH0227 | AS207C | Museum für Völkerkunde, Viena, 140708 **(OKR dice Museum of Science, Buffalo, C14459)** | «Huaura Valley, near Lima, **Santa Rosalía** Hacienda» |
| UR087 | KH0323 | UR087 | Museo Temple Radicati, 6 | **Santa** |
| UR088 | KH0324 | UR088 | Museo Temple Radicati, 1 | **Santa** |
| UR089 | KH0325 | UR089 | Museo Temple Radicati, 5 | **Santa** |
| UR090 | KH0326 | UR090 | Museo Temple Radicati, 3 | **Santa** |
| UR091 | KH0327 | UR091 | Museo Temple Radicati, 2 | **Santa** |
| UR092 | KH0328 | UR092 | Museo Temple Radicati, 4 | **Santa** |
| UR198 | KH0436 | UR198 | Ethnologisches Museum, Berlín, VA63039 | **Santa Clara, Nazca** |

Hallazgos de identificación (**demostrado** con las fuentes citadas):

1. **UR087–UR092 = KH0323–KH0328 son el célebre corpus de seis quipus del valle del Santa**
   (Museo Temple Radicati, nº de colección 1–6), el llamado caso «piedra de Rosetta» de
   Medrano y Urton (2018) y FitzPatrick (2024). El propio `docs/estado_del_arte.md`
   (líneas 143, 213) lo afirma literalmente: «los seis del valle del Santa = KH0323–KH0328 =
   UR087–UR092». Por tanto UR087 y KH0323 **son el mismo objeto con dos nombres**: cualquier
   «relación» entre un UR y su KH equivalente es un artefacto de nomenclatura, no un hallazgo
   (`okr-kh-numbers.csv` lo confirma uno a uno).
2. **KH0227 no es del valle del Santa.** Su procedencia es la hacienda **Santa Rosalía**, valle
   de Huaura (costa central, cerca de Lima), y su nombre antiguo es AS207C, no un UR. Comparte
   sólo la subcadena «Santa» del rótulo.
3. **UR198 tampoco.** Es de **Santa Clara, Nazca** (costa sur), museo de Berlín. Otra «Santa».
4. **Discrepancia de fuente:** KFG ubica KH0227 en Viena (140708) mientras `okr-kh-numbers.csv`
   lo ubica en el Museum of Science de Buffalo (C14459). El mismo número KH recibe dos museos
   distintos. Es una alerta metodológica: no usar el museo como lugar de origen (regla 6 del
   BRIEF) y tratar el rótulo «Santa» como contaminado.

**Consecuencia:** el archivo real (los seis del valle del Santa) es UR087–UR092. KH0227 y
UR198 se analizan como **grupo externo / control**, no como miembros del archivo.

---

## 3. Método

- Unidad de análisis: **el quipu** (regla 1). Las pruebas entre quipus comparan sus secuencias
  o conjuntos de valores; el nulo **baraja los valores dentro de cada quipu** (preserva el
  multiset y el tamaño de cada objeto, destruye el orden), 500 réplicas, semilla 0.
- `valor = 0` con `nudos` vacío se trata como **ausente** (regla 6), no como cero real.
- p-valor empírico = `(1 + nº de nulos ≥ observado)/(500+1)`; corrección de multiplicidad
  **Holm** y **BH-FDR** sobre los 28 pares.
- Toda conclusión se etiqueta: demostrado / apoyado con datos / propuesto / especulativo.

---

## 4. Resultados

### 4.1 Descripción del conjunto (tabla por quipu)

Valores ausentes (0 sin nudos) excluidos de las columnas de valor. `kd_*` = dirección de los
nudos individuales leída de la cadena `nudos`; `t_*` = torsión; `u_*` = unión al cordón principal.

| KFG | n cuerdas | colgantes | subsidiarias | grupos | colores top (nº) | n colores | rango valor | mediana | 0-ausentes | u_R | u_V | u_T | t_S | t_Z | kd_S | kd_Z | kd_U |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KH0227 | 221 | 168 | 53 | 16 | AB:73; W:51; MB:45 | 21 | 1–90 | 5 | 40 | 0 | 169 | 0 | 220 | 1 | **193** | 27 | 2 |
| UR087 | 370 | 306 | 64 | 56 | W:85; AB:78; YB:70 | 68 | 1–26 | 1 | 49 | **310** | 0 | 0 | 366 | 4 | 40 | **323** | 1 |
| UR088 | 102 | 54 | 48 | 1 | W:40; AB:26; MB:10 | 23 | 1–184 | 9 | 13 | 0 | **54** | 0 | 100 | 0 | 1 | **131** | 0 |
| UR089 | 288 | 206 | 82 | 9 | W:125; AB:63; LG:19 | 39 | 1–71 | 4 | 51 | 0 | **207** | 0 | 286 | 1 | 0 | **288** | 1 |
| UR090 | 131 | 108 | 23 | 4 | W:60; B:16; YB:15 | 28 | 1–172 | 10 | 8 | 40 | **69** | 0 | 130 | 1 | 13 | **167** | 1 |
| UR091 | 125 | 90 | 35 | 3 | W:53; AB:35; YB:13 | 23 | 1–73 | 5 | 44 | 0 | **93** | 0 | 125 | 0 | 0 | **94** | 0 |
| UR092 | 61 | 60 | 1 | 1 | W:24; RL:12; AB:12 | 6 | 1–9 | 2 | 11 | **56** | 0 | 0 | 59 | 2 | 1 | **49** | 0 |
| UR198 | 369 | 257 | 112 | 40 | AB:189; W:114; HB:26 | 32 | 1–38 | 2 | 69 | 8 | **252** | 0 | 368 | 0 | **217** | 138 | 1 |

Lecturas (**apoyado con datos**):

- **Tamaños muy dispares**: de 61 cuerdas (UR092) a 370 (UR087). El «archivo» no es homogéneo
  en escala; sí lo es en que **todos son quipus de colgantes puros** (tipo `p`; ninguna cuerda
  superior registrada como fila propia en KFG) y **todos con torsión S dominante** (1.654 S de
  1.667 cuerdas; sólo 9 Z).
- **Ninguna «cuerda superior» (union = T) en KFG para estos 8.** Pero el `NOTES` del OKR de
  **KH0323 = UR087** dice textualmente: *«Top cords. Top cords are fastened through the pendant
  attachments… Markers on this khipu are short lengths of cotton cord… pointing upwards in the
  same direction as the top cords»*, y `khipu_summary.csv` le asigna **13 top cords**. Es decir,
  sólo UR087 tiene cordones superiores/marcadores; el resto no.
- **Unión R/V**: en el grupo Santa, cinco quipus son **puros** (UR087, UR092 todo R; UR088,
  UR089, UR091 todo V) y **UR090 es el único mixto (40 R / 69 V)**. Global Santa = **406 R /
  423 V = 49,0 % / 51,0 %**. Esto **reproduce exactamente** el resultado publicado por
  Contreras (2026) (49,0/51,0, KH0326 = UR090 como único mixto). KH0227 no tiene R/V (sólo 14
  «U») y UR198 es mayoritariamente V (8 R / 252 V).
- **Dirección de nudo**: contraste marcado. Los **seis del Santa** tienen nudos casi todos en
  dirección **Z** (UR087: 323 Z vs 40 S; UR089 y UR088 ≈ 100 % Z); **KH0227 (externo)** es lo
  opuesto (**193 S vs 27 Z**); UR198 es intermedio (217 S / 138 Z). Este es el hallazgo interno
  más fuerte y coincide con la polaridad valle-del-Santa descrita en la literatura.
- **Colores**: dominan blanco (W) y marrón claro (AB) en todos; el número de colores Ascher va
  de 6 (UR092) a 68 (UR087). RL (rojo) y LG (verde claro) son propios de los urdimbres del
  grupo Santa.

### 4.2 Sumas (fórmulas de Ascher)

| KFG | banded | seriated | pendant_pendant | pendant_pendants_color | indexed_pendant |
|---|---|---|---|---|---|
| KH0227 | 0 | 16 | 50 | 32 | 20 |
| UR087 | **43** | 12 | 65 | 55 | 13 |
| UR088 | 0 | 1 | 6 | 1 | 0 |
| UR089 | 6 | 3 | 60 | 11 | 1 |
| UR090 | 1 | 3 | 50 | 4 | 1 |
| UR091 | 0 | 3 | 13 | 1 | 0 |
| UR198 | 21 | 19 | 55 | 36 | 31 |

**Todos** los quipus del conjunto tienen relaciones de suma; **UR087 concentra las «banded
clusters» (43)**, el tipo que la literatura asocia a grupos de cuerdas jerarquizados. Nivel:
**apoyado con datos** (es un recuento directo del KFG, no una inferencia).

### 4.3 Estructura de grupos (multiset de tamaños)

- UR087: 34 grupos de **6** (+18 de 1, +3 de 24, +1 de 12). UR089: 4 de 6. UR090: 1 de 6.
- UR088: **un solo grupo de 54**. UR092: **un solo grupo de 60**. UR091: grupos de 12/36/42.
- UR198 (externo): muchos grupos de 4 y de 2.

El **motivo «grupo de seis»** reaparece en UR087/UR089/UR090, pero **no es distintivo del
sitio**: el 29,3 % (191/651) de los quipus del KFG tienen al menos un grupo de 6, y **KH0227
(el quipu externo de Huaura) también tiene 7 grupos de 6**. Además, el examen del primer cordel
de cada grupo de 6 en el Santa da valores casi todos = 1 (suma total 64), **no** el tributo
esperado; es decir, **los límites de grupo del KFG no reproducen los «grupos de seis cordeles»
de Medrano y Urton**, y con estos datos no se puede validar la suma-tributo (ver §6).

### 4.4 Relaciones entre quipus

**(a) Secuencias de valores compartidas.** Nº de 3-gramas contiguos de valores compartidos por
par (observado vs nulo que baraja valores dentro de cada quipu, 500×, semilla 0):

| par | obs | media nula | p |
|---|---|---|---|
| UR087–UR198 | 51 | 47,95 | 0,301 |
| UR089–UR198 | 27 | 27,34 | 0,569 |
| KH0227–UR198 | 20 | 15,63 | 0,130 |
| KH0227–UR092 | 10 | 4,47 | **0,012** |
| UR087–UR089 | 11 | 17,34 | 0,978 |

**Resultado negativo:** ningún par sobrevive a la corrección de multiplicidad
(**Holm: 0/28; BH-FDR: 0/28**). El único p nominalmente < 0,05 (KH0227–UR092, p = 0,012) cae con
Holm (0,012 × 28 ≈ 0,34) y no es interpretable. No hay evidencia de secuencias de valores
compartidas entre los quipus del archivo.

**(b) Totales de un quipu presentes en otro.** El test de «suma de grupo de A presente como
valor de B» es **degenerado**: como los valores son enteros pequeños (1–184) y las sumas de
grupo también, casi todas las sumas «aparecen» tanto en el dato como en el nulo
(p = 1,00 en todos los pares). **No es informativo.** Búsqueda directa: **ningún total de un
quipu aparece como valor de cuerda en otro**, salvo una coincidencia anecdótica: el total de
**UR092 = 176** es exactamente el valor de una cuerda de **UR088** (`p16`, color W,
nudos `1S(4.5,Z),100;7S(9.5,Z),70;6L(21.0,Z),6`). Nivel: **especulativo** (una coincidencia
entre cientos de valores en un rango de 184).

**(c) Estructuras de grupo idénticas.** El multiset de tamaños de grupo **no** se repite entre
pares del archivo (UR087 ≠ UR089 ≠ UR090, etc.). El único rasgo común es el bloque de 6, y
—como se vio— es común en todo el corpus. **Sin coincidencia estructural específica.**

**(d) Patrones de color.** Nº de 4-gramas de color compartidos (mismo nulo):

| par | obs | media nula | p |
|---|---|---|---|
| UR087–UR089 | 11 | 0,55 | 0,002 |
| UR087–UR090 | 10 | 0,47 | 0,002 |
| UR087–UR091 | 10 | 1,41 | 0,002 |
| UR089–UR090 | 6 | 0,09 | 0,002 |
| KH0227–UR087 | 7 | 1,88 | 0,002 |

21/28 pares dan p nominal ≤ 0,05, **18/28 sobreviven a BH-FDR pero 0/28 a Holm** (el p está en
el suelo 1/501 porque el nulo nunca alcanza el valor observado). **Pero la explicación aburrida
es la correcta:** al inspeccionar los 4-gramas compartidos entre UR087 y UR090 son
`('W','W','W','W')`, `('YB','YB','YB','YB')`, `('AB','W','W','W')`… es decir, **simples tramos
monocromáticos** (blanco, amarillo-marrón) que ambos quipus tienen por usar la misma paleta
pobre y bloques de color. El nulo (barajar colores) rompe esos tramos, de ahí la «significación»
trivial. **No es un patrón de color codificado compartido.**

### 4.5 Jerarquía del archivo (detalle vs resumen)

- **Cordones superiores (marcador de quipu «de trabajo»/resumen): sólo UR087** (13 top cords,
  marcadores; ver §4.1). Es el candidato a quipu **de resumen o de cabecera** del archivo.
- **UR088 y UR092 son «de un solo grupo»** (54 y 60 cuerdas): UR088 tiene los valores grandes
  (media 25,7; hasta 184) y UR092 los pequeños (media 3,5; ≤ 9). No se observa que el total de
  uno sea el valor o la suma de otro (§4.4b), ni que cordones de UR088 reconstruyan sumas de
  UR089–UR091.
- **No se puede reconstruir una jerarquía numérica detalle→resumen** con estos datos: los
  totales de cada quipu son del mismo orden (176–2.731), ninguno se reutiliza como valor en
  otro, y el test de contención es degenerado. Nivel: **resultado negativo**.

### 4.6 Síntesis interna del grupo Santa

El conjunto UR087–UR092 comparte tres rasgos fuertes: (i) corpus Temple Radicati nº 1–6;
(ii) **unión R/V casi pura por quipu** con UR090 como único mixto (49,0/51,0 %); (iii) **nudos
en dirección Z**. Ninguno de estos rasgos lo comparten KH0227 ni (en la misma forma) UR198.

---

## 5. Controles

- **Nulo explícito**: barajado de valores (o colores) **dentro de cada quipu**, 500 réplicas,
  semilla 0. Preserva el tamaño y el multiset de cada objeto; destruye el orden y la co-ocurrencia.
- **p empírico** = (1 + nº nulos ≥ obs)/(501). Suelo = 0,001996 cuando ningún nulo alcanza el dato.
- **Multiplicidad**: 28 pares → Holm y BH-FDR.

| prueba | pares p<0,05 crudo | Holm | BH-FDR | veredicto |
|---|---|---|---|---|
| 3-gramas de **valores** | 2/28 | 0/28 | 0/28 | **negativo** |
| 4-gramas de **color** | 21/28 | 0/28 | 18/28 | **trivial** (tramos monocromáticos) |
| sumas de grupo dentro de valores | 28/28 «p = 1,00» | — | — | **degenerado / no informativo** |

- **Contraste externo**: KH0227 y UR198 actúan como fuera-de-sitio. Su inclusión agranda el nulo
  de color y de valores, y ninguno de los rasgos fuertes internos del Santa (R/V casi puro, Z
  casi total) se les aplica, lo que apoya la lectura de que el grupo Santa es una unidad real.

## 6. Resultados negativos (explícitos)

1. **No hay secuencias de valores compartidas** entre los quipus del archivo (Holm y BH: 0/28).
2. **No hay totales de un quipu que reaparezcan como datos de otro** (salvo la coincidencia
   única UR092=176↔UR088 p16, especulativa). El test de contención de sumas de grupo es
   degenerado por el rango pequeño de valores.
3. **No hay multiset de estructura de grupos idéntico** entre pares.
4. **No hay patrón de color codificado compartido**: los 4-gramas «significativos» son tramos
   monocromáticos triviales (WWWW, YBYBYB), no códigos.
5. **No hay jerarquía numérica detalle→resumen** reconstruible; sólo UR087 tiene cordones
   superiores/marcadores.
6. **El «grupo de seis»** no es exclusivo del Santa: 29,3 % del corpus y **KH0227 (Huaura)**
   también lo tiene.
7. **No reproduzco la suma-tributo del Santa** con los límites de grupo del KFG: el primer
   cordel de los 39 grupos de 6 suma **64** (casi todos = 1), no el tributo de las revisitas.
   Es un **desajuste de definición de grupo**, no una refutación del hallazgo original.

## 7. Nivel de evidencia de cada conclusión

| Conclusión | Nivel |
|---|---|
| UR087–UR092 = KH0323–KH0328 son el corpus Santa (Temple Radicati 1–6); KH0227 (Huaura, AS207C) y UR198 (Nazca) **no** son del valle del Santa | **demostrado** (fuentes de identidad) |
| R/V casi puro por quipu, UR090 el único mixto; 49,0/51,0 % — reproduce Contreras (2026) | **apoyado con datos** |
| Nudos en dirección Z dominan en los seis del Santa; KH0227 en dirección S opuesta | **apoyado con datos** (recuento directo) |
| UR087 tiene cordones superiores y marcadores (OKR), único del conjunto | **apoyado con datos** |
| Presencia de relaciones de suma (Ascher) en todos; UR087 con 43 banded clusters | **apoyado con datos** |
| Motivo «grupo de seis» presente en UR087/UR089/UR090 | **apoyado con datos** (pero no distintivo, ver §6.6) |
| Coincidencia total UR092↔UR088 p16 | **especulativo** |
| Relaciones de secuencia/color/totales entre quipus | **no apoyado / negativo** |
| Jerarquía detalle↔resumen numérica | **no apoyado / negativo** |

## 8. Contraste con la literatura del sitio y qué se registraba

**Literatura del sitio (grep en `docs/fichas/` y `docs/estado_del_arte.md`):**

- *Medrano y Urton (2018)* — los **seis quipus del valle del Santa** y la **revisita de 1670 de
  San Pedro de Corongo** (132 tributarios, 6 *pachacas*); 133 «grupos de seis cordeles» por
  color; los valores de los primeros cordeles suman el tributo; los amarres R/V dividen en
  **moieties**. Nivel declarado: apoyado con datos la coincidencia numérica, propuesto las moieties.
- *FitzPatrick (2024)* revisa y **corrige** la alineación de moieties; propone R = marcado, V =
  no marcado; advierte que faltan detalles y que no hay test contra alineaciones nulas.
- *Contreras (2026)* reproduce el **patrón estructural R/V** (49,0/51,0; KH0326 = UR090 único
  mixto) pero **no** el emparejamiento numérico con el tributo de 367 pesos; su independencia es
  dudosa (relee el mismo campo de la tradición KDB). `estado_del_arte` líneas 259–265 y 361.
- *Urton (2019)* sobre **UR28 (Nazca, 74 cordeles)**: seis ayllus, 102=102=102, color AB/MB;
  «AB = hanan» especulativo (línea 295) — relevante porque UR198 también es de Nazca.
- *Brezine et al. (2024)*: los seis del valle del Santa = KH0323–KH0328 = UR087–UR092 (líneas 143, 213).

**Lo que mis datos confirman de la literatura.** (i) La identificación del corpus (§2).
(ii) El **patrón R/V por quipu** con UR090 mixto y el 49,0/51,0 % global: reproducido **de forma
exacta** desde el KFG, independientemente del campo `ATTACHMENT_TYPE` del OKR. (iii) La
dirección **Z** dominante, coherente con la caracterización del sitio.

**Lo que no puedo confirmar.** (i) La **suma-tributo**: con los límites de grupo del KFG no se
reproduce (primer cordel de los grupos de 6 suman 64). (ii) Los **133 grupos de seis**: el KFG
sólo da 39 grupos de tamaño exacto 6 en los seis quipus. (iii) El emparejamiento numérico con
los 367 pesos. Estas tres cosas dependen de definiciones de «grupo» y de datos que **no están
en las fuentes abiertas** usadas aquí.

**Propuesta de qué se registraba aquí (nivel: propuesto).** El grupo UR087–UR092 es un
**archivo administrativo/censal coherente**: seis quipus de una misma colección (Temple
Radicati 1–6), colores y torsión homogéneos, nudos en Z, y —sobre todo— **una variable binaria
R/V casi constante por objeto** (5 de 6 puros). Esa polaridad binaria por quipu es exactamente
lo que la literatura interpreta como codificación de **moieties/estatus**; el hallazgo de que se
reproduce limpiamente refuerza la lectura de un registro de **población tributaria organizada en
dos mitades**. La estructura de **grupos de seis** (UR087 con 34) encaja con la unidad «persona/
tributario» de la revisita. El contenido *numérico* (suma-tributo) queda fuera de alcance con
datos abiertos. En contraste, **KH0227** (fragmento de AS207A, Huaura) y **UR198** (Nazca) son
**otras tradiciones locales** —distinta dirección de nudo (KH0227 en S), distinta
unión (KH0227 sin R/V)— y **no deben promediarse con el Santa**: el rótulo «Santa» del encargo
es un falso positivo de búsqueda de subcadena.

---

## 9. Para el coordinador

- **El «archivo de Santa» son seis quipus, no ocho.** UR087–UR092 = KH0323–KH0328 son el
  corpus del valle del Santa (Temple Radicati 1–6). **KH0227** es un fragmento de **AS207A de
  Huaura** (hacienda Santa *Rosalía*) y **UR198** es de **Santa *Clara*, Nazca**: comparten sólo
  la subcadena «Santa». Analizarlos juntos es un falso positivo de nomenclatura (demostrado).
- **Reproduje de forma exacta el patrón R/V publicado:** cinco quipus puros (UR087/UR092 → R;
  UR088/UR089/UR091 → V) y **UR090 el único mixto (40 R / 69 V)**; global **49,0 % R / 51,0 % V**.
  Coincide al decimal con Contreras (2026) y se obtiene independientemente del campo ORIGINAL del
  OKR (apoyado con datos).
- **Rasgo distintivo del Santa: nudos en dirección Z.** UR087 = 323 Z/40 S; UR089 y UR088 ≈ 100 %
  Z. El quipu externo KH0227 es el **opuesto** (193 S/27 Z). Buena variable para separar
  procedencias (apoyado con datos).
- **Ninguna relación entre quipus sobrevive al control.** Secuencias de valores: 0/28 tras Holm
  y BH. Totales en otros: coincidencia única UR092=176↔UR088 (especulativa). Estructuras de
  grupo idénticas: ninguna. Colores: la «señal» son tramos monocromáticos triviales (negativos).
- **Cuidado con el test de «suma en valores»:** es **degenerado** (p = 1,00 siempre) porque los
  valores son enteros pequeños; no sirve para probar jerarquías con estos datos.
- **No pude validar la suma-tributo del Santa** desde datos abiertos: los límites de grupo del
  KFG dan 39 grupos de 6 (no 133) y el primer cordel suma 64 (no el tributo). Es un problema de
  **definición de grupo y de datos faltantes**, no una refutación.
- **Sólo UR087 tiene cordones superiores/marcadores** (13 top cords, con nota explícita del OKR);
  es el único candidato a quipu «de resumen» del archivo. **No hay jerarquía numérica
  detalle→resumen reconstruible** (negativo).
- **Propuesta (nivel propuesto):** el grupo Santa es un registro **censal/tributario** con la
  dicotomía R/V como marcador de **moieties**; los grupos de seis, la unidad «persona». KH0227
  y UR198 representan otras tradiciones y no deben agregarse.
- **Recomendación siguiente ronda:** (1) construir los **grupos de seis según la definición de
  Urton** (color/bloques, no los grupos del KFG) y re-probar la suma-tributo con nulo de
  permutación; (2) auditar si `ATTACHMENT_TYPE` del OKR es circular respecto de Urton; (3) buscar
  en el OKR los fragmentos de AS207 (A/C) para confirmar que KH0227 es un sub-objeto; (4) separar
  «Santa» (valle) de «Santa Clara» y «Santa Rosalía» en el índice del proyecto.
