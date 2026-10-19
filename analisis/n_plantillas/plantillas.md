# Biblioteca de plantillas (CONGELADA antes del barrido)

**Equipo:** `n_plantillas` · **Fecha de congelación:** 18-10-2026, antes de ejecutar `02_puntuar.py` sobre el corpus.
**Semilla:** 20261018 (partición en mitades y permutaciones).
**Unidad de análisis:** el quipu. Toda cifra que se mide se mide sobre cuerdas de **nivel 0** (colgantes) en el orden de `cuerdas.csv`. La excepción es P8a, que cuenta las subsidiarias. Una cuerda es *anudada* si `nudos` no está vacío; si no, su valor está **ausente**, aunque `valor = 0` (regla del BRIEF).

## 0. Lo que ya vi antes de congelar (para corregir los senderos bifurcados)

Leí los informes previos y miré la estructura de algunos quipus:

- **Controles positivos:** UR006 (grupos de ~21 más una cuerda de lazo con 9 subsidiarias), UR053B/UR053C, UR087 y UR089 (grupos de 6), UR278 (grupos de 9), UR029 (7 × 5), Puruchuco (UR063, UR067, UR068, UR064, UR066 y UR073).
- **Quipus no numéricos:** UR050 (164 colgantes, todos en grupos de 1), UR054 (115), UR055 (180), UR052 (24 grupos de 4) y UR178 (14).

Al leer estas cifras noté dos coincidencias **antes de congelar**:

- 164 ≈ 328/2, la mitad de las wakas de los ceques.
- 164 + 180 = 344, dentro del intervalo «328–350» de Urton.

Además, los 24 grupos de UR052 recuerdan los 24 «meses» de UR006. **Todas estas coincidencias son post hoc.** Ningún acierto de P9b ni de P8 en UR050, UR052, UR054 o UR055 cuenta como evidencia de la plantilla. Solo vale como evidencia una **predicción con datos no usados**, en el paso 5.

## 1. Fuentes y plantillas

Las referencias de línea son a `analisis/fuentes_txt/`. «U17» = `Urton2017_InkaHistoryInKnots.txt`; «R» = `Rostworowski_CostaPeruana.txt`; «MU18» = `TowardtheDeciphermentofaSetofMid.txt` (Medrano y Urton 2018); «P04» = `Parssinen2004_TextosAndinos_parcial.txt`; «C13» = `Curatola2013_ContarConcertando.txt`; «M24» = Murra 2024, a través de `ds/n_murra_wanka/informe.md`.

Notación:

- `V` = secuencia de valores de los colgantes anudados, en orden.
- `G` = grupos KFG de colgantes.
- Ventana = tramo de cuerdas anudadas **consecutivas** de `V`.

Cada plantilla tiene una o varias **variantes**, y cada variante es un estadístico. **Hay 30 variantes en total**, y todas entran en la corrección múltiple.

### P1. Censo decimal por «calles» de edad (Murúa / Guaman Poma)

- **Fuente:** U17 l. 2438–2439 (p. 179). El tucuyricuc «organized them into ten rows ["streets"] for the men and another ten for the women… seated by ages… every five years»; Murúa nombra las diez clases.
- **Nombres y edades:** vienen de Guaman Poma [1615], ff. 195–236, citados **de memoria**. No están en el repo; hay que verificarlos.
- **Perfil esperado (calles de varones en el orden de Guaman Poma):**

| Calle | Nombre | Edades |
|---:|---|---|
| 1 | auca camayoc | 25–50 |
| 2 | puric macho | 50–80 |
| 3 | rocto macho | 80+ |
| 4 | uncoc runa | impedidos, 3 % del total |
| 5 | sayapayac | 18–25 |
| 6 | macta | 12–18 |
| 7 | tocllacoc | 9–12 |
| 8 | pucllacoc | 5–9 |
| 9 | lluccllacoc | 1–5 |
| 10 | quiraupi | 0–1 |

  El efectivo esperado de cada calle son los años-persona de una población estacionaria con mortalidad pre-industrial (lx aproximada Coale–Demeny Oeste, e0 ≈ 30; está en el código). El mismo perfil vale para las mujeres.
- **P1a:** ρ de Spearman máximo entre una ventana de 10 cuerdas de `V` y el perfil Guaman Poma.
- **P1b:** pirámide ordenada por edad, con las 9 bandas sin impedidos. Es el máximo, sobre ventanas de 9, de max(ρ, ρ invertido).
- **P1c:** varones más mujeres. Es el máximo, sobre ventanas de 20, de min(ρ(primeras 10, GP), ρ(últimas 10, GP)).
- **P1d:** ρ máximo entre 10 **sumas de grupo** consecutivas y el perfil Guaman Poma.
- **Puerta:** ≥ 10 cuerdas anudadas (P1c, ≥ 20; P1d, ≥ 10 grupos con valor).

### P2. Censo toledano en 4 categorías (Lunahuaná)

- **Fuente:** R l. 762. La visita de 1577 dio 740 tributarios, 89 viejos, 601 muchachos y 1846 mujeres (= 3276). La revisita de 1590 dio 474, 96, 372 y 973.
- **P2:** −(distancia L1 mínima) entre las proporciones de una ventana de 4 cuerdas positivas y cualquiera de los dos vectores. Opcionalmente sigue una 5.ª cuerda con el total, pero no puntúa.
- **Control positivo:** ninguno.

### P3. Padrón de unidades domésticas (Urton, cap. 10)

- **Fuente:** U17 l. 2485, p. 187: «sequences of numbers in roughly the one to seven range… higher occurrence… 1–4». Urton propone análogos con χ² no significativo en l. 2492: UR029, UR091, AS026A, AS157 y UR023.
- **Distribución esperada H** sobre {0, 1, …, 7, 8–10, ≥11}: 0,03; 0,15; 0,19; 0,18; 0,15; 0,11; 0,08; 0,05; 0,05; 0,01.
- **P3:** log-razón de verosimilitud media por cuerda anudada, H frente a la distribución del corpus en las mismas clases. Es un estadístico de **composición**: la permutación interna no lo cambia, así que solo hay nulo de corpus.

### P4. Padrón de personas nombradas (Santa 1670)

- **Fuente:**
  - MU18 l. 38: 130 tributarios con nombre (132 contados), cada uno con un tributo de 2 pesos 7 reales 3 cuartillos.
  - MU18 l. 48: «one group of six cords of one color is followed by another six cords of a different color».
  - U17, cap. 12.
- **Firma:** un formulario fijo por persona. Son grupos de igual tamaño k (4 ≤ k ≤ 12), monocromos, y cada grupo de color distinto del anterior; los valores son pequeños.
- **Puerta:**
  - ≥ 6 grupos del tamaño modal k (sin contar los grupos de 1), que cubran ≥ 50 % de los colgantes que no están en grupos de 1;
  - mediana de valores ≤ 30.
- **P4:** (homogeneidad cromática media dentro de los grupos modales) + (fracción de pares de grupos modales consecutivos con color modal distinto). El nulo permuta los colores entre colgantes.

### P5. Libro de almacén (Incahuasi)

- **Fuente:**
  - U17, cap. 9;
  - SINTESIS: «UR275 depósito repartido, cabecera = cuota + destinos»; «las 9 partes de UR278 son proporciones estables»; cuotas 47, 15, 10, 30 y 17; tríos `[x, c, x−c]`.
- **P5a, tabla de partes estables:**
  - Puerta: ≥ 4 grupos de tamaño modal m ∈ {8, 9, 10} y mediana de valores ≥ 20.
  - Estadístico: −mediana sobre columnas del coeficiente de variación de la cuota de la columna dentro de cada fila. Solo cuentan las filas completas.
  - Nulo: permutar los valores entre las celdas de esas filas.
- **P5b, cabecera = cuota + destinos:**
  - Para cada grupo con ≥ 3 cuerdas anudadas, d = (primera) − (suma del resto).
  - Estadístico: el máximo, sobre c ∈ [1, 300], del número de grupos con d = c.
  - Nulo: permutar los valores entre las cuerdas de esos grupos.
- **P5c, trío con cuota:** el máximo, sobre c ≥ 2, del número de tríos consecutivos dentro de un grupo con v1 = c + v3 y v2 = c. Mismo nulo.

### P6. Consolidación jerárquica (Puruchuco)

- **Fuente:**
  - U17, cap. 5 (l. 6231: «four-cord color-seriated groupings that make up the Puruchuco accounting hierarchy»);
  - `ds/n_puruchuco_pacha` §3: las secciones de 20 de UR068 suman, columna a columna, los 20 datos de UR067; las de UR063 suman el centro de UR068.
- **P6a, sumas internas:** (n.º de grupos en los que una cuerda = suma de las demás cuerdas anudadas del grupo, con suma ≥ 10) + (n.º de totales de grupo ≥ 10 que reaparecen como valor de una cuerda de otro grupo). El nulo permuta los valores.
- **P6b, suma de secciones en otro quipu de la misma procedencia (conocida):**
  - Para k, se prueban los periodos L = m·t (m = tamaño modal de grupo ≥ 3; t = 1…6; 4 ≤ L ≤ 40) y los inicios en un comienzo de grupo.
  - Las secciones son bloques consecutivos de L colgantes (incluidas las cuerdas sin nudos, que valen 0), en tramos de 2, 3 o todos los bloques posibles.
  - El vector S es la suma columna a columna. Se compara con cada ventana de L colgantes del quipu j, contando las posiciones con S_i ≥ 1 y S_i = w_i.
  - Estadístico: el máximo, sobre (L, inicio, tramo, ventana), de esas coincidencias para el mejor j.
  - Nulo: permutar los valores de k (j fijo), con Bonferroni por el número de compañeros j.

### P7. Lista de tributo en orden constante (wanka; tasa de Lunahuaná)

- **Fuente:**
  - M24: 12 categorías en orden constante × 19 eventos (`ds/n_murra_wanka` §3.1).
  - R l. 762: tasa de 1577 = 1196 pesos, 366 piezas de ropa, 500 fanegas de maíz y 758 aves.
  - R l. 806–809: retasa de 1590 = 1392 pesos, 234,5 piezas, 641 fanegas y 483,5 aves.
- **P7a, formulario de categorías heterogéneas:**
  - Puerta: ≥ 4 grupos del mismo tamaño m ∈ [3, 20].
  - Estadístico: η² de la posición sobre log10(v+1) en las celdas con valor.
  - Nulo: permutar los valores entre las celdas.
- **P7b, doce categorías como grupos:**
  - Puerta: 11–13 grupos con ≥ 3 cuerdas anudadas cada uno.
  - Estadístico: η² del grupo sobre log10(v+1).
  - Nulo: permutar los valores.
- **P7c, tasa de 4 especies:** −(L1 mínima) entre una ventana de 4 cuerdas positivas y las proporciones de 1577 o de 1590.

### P8. Calendario

- **Fuente:**
  - U17 l. 711–717 y 750: UR006 tiene 24 conjuntos pareados de [20–22 colgantes] + [8–10 de lazo] ≈ 30; total 730 = 362 + 368.
  - `ds/n_rostworowski` (R 914–916): año de 9 meses × 40 días (+5).
- **P8a, unidades de ~30 cuerdas:**
  - Una unidad es un grupo más los grupos de 1 que lo siguen. Se cuentan todas las cuerdas del subárbol.
  - Estadístico: la racha más larga de unidades consecutivas con tamaño en [27, 33].
  - Nulo: cortar al azar la misma secuencia de subárboles en el mismo número de unidades.
- **P8b, días como valores (12 × 30):** el máximo, sobre ventanas de 12, de #valores en [28, 32]. El nulo permuta los valores.
- **P8c, 9 × 40:** el máximo, sobre ventanas de 9, de #valores en [38, 42]. El nulo permuta los valores.

### P9. Sistema de ceques

- **Fuente:**
  - U17 l. 1258: 328–350 wakas en 41 ceques.
  - U17 l. 1263: tres suyus de 9 ceques (3 tríos collana/payan/cayao) y Cuntisuyu con 14; mitades hanan y hurin.
  - U17 l. 1266–1280 (tabla 8.1): UR053C/UR053B, con colores AB W RB repetidos en tríos y fijación V/R opuesta.
  - U17 l. 1518–1524: un par de quipus, uno por mitad.
- **P9a, ciclo cromático de periodo 3:** A3 − max(A1, A2), con Aℓ = fracción de colgantes con color(i) = color(i+ℓ). El nulo permuta los colores.
- **P9b, conteos.** Son comparaciones de base, no pruebas; p = tasa base en el corpus.
  - (i) 40–42 colgantes;
  - (ii) 326–352 cuerdas en total;
  - (iii) 161–167 colgantes (mitad de 328);
  - (iv) cuatro grupos consecutivos con multiconjunto de tamaños {9, 9, 9, 14} (±1 en cada uno).

### P10. Lista dinástica o genealógica

- **Fuente:** listas reales de los cronistas, 11–13 incas, Hurin (5) y Hanan (6–8). **No hay** cifras de reinado en el repo, así que es una plantilla débil y no hay control.
- **P10:** en ventanas de 11–13 colgantes con valor positivo, el contraste de color entre los 5 primeros y el resto: (homogeneidad del bloque 1 + homogeneidad del bloque 2)/2 × [color modal distinto]. Se toma el máximo. El nulo permuta los colores.

### P11. (Segunda fuente del coordinador, incluida ANTES de congelar) Registro segmentado por eventos

- **Fuente:**
  - P04 l. 318: la «Memoria» de Guacrapaucar (1558) «está organizada en series de categorías, así que cada nueva serie comienza después de presentar una información histórica estereotipada».
  - P04 l. 300–310: la cuerda suplementaria es el «tercer objeto en la categoría».
  - P04 l. 373–380: listas de mit'a (Chupaychu 1549, Canta, Hatun Xauxa 1561), con categorías en orden fijo.
  - El registro wanka (12 × 19 eventos) es el caso documentado.
- **P11a, bloques con la misma secuencia de categorías:**
  - Entre los grupos con ≥ 3 colgantes, para cada tamaño L se busca la tupla de colores modal.
  - Estadístico: el máximo n.º de grupos de tamaño L cuya tupla coincide en ≥ 80 % de posiciones con la modal. Se excluyen las tuplas monocromas: un grupo de un solo color no es una «secuencia de categorías».
  - Nulo: permutar los colores entre colgantes.
  - Condición descriptiva: los valores **varían** entre bloques, con < 50 % de celdas idénticas (si no, sería una copia).
- **P11b, con marcador de evento:** igual que P11a, pero solo cuentan los bloques precedidos inmediatamente por un marcador. El marcador es un grupo de 1 o un grupo de tamaño ≠ L cuyo color modal no aparece en la tupla.
- **P11c, lista de conquistas o itinerario:**
  - Fuentes: P04 l. 570–578 («Memoria de las provincias», Sarmiento cap. 44: provincias, fortalezas y reyes en orden); P04 l. 318 (Calancha: «Cada pueblo cabeza de provincia tenía su cifra»).
  - Firma: ≥ 8 grupos, cada uno abierto por una «cifra» de lugar distinta de las demás y seguido de conteos.
  - Estadístico: fracción de primeras cuerdas de grupo con valor único en el quipu, menos la fracción en el resto de las cuerdas.
  - Nulo: permutar los valores.

### P12. (Segunda fuente) Cuenta monetaria colonial (Lucanas 1581)

- **Fuente:**
  - C13 l. 18–19 y 96–124: cuentas de cajas de comunidad en pesos y reales; el quipu no dice la unidad (n. 20).
  - MU18 l. 38: tributo de 2 pesos, 7 reales y 3 cuartillos.
- **Firma:** colgante = pesos y primera subsidiaria = reales (0–7), un sistema mixto.
- **P12:** fracción de primeras subsidiarias anudadas con valor ≤ 7 (y ≥ 1) cuando el colgante es ≥ 8. Es de composición, así que solo hay nulo de corpus. Puerta: ≥ 8 pares colgante–subsidiaria.

## 2. Inferencia (congelada)

- **Mitades:** permutación de los 651 quipus con `default_rng(20261018)`. La primera mitad (326) es de **exploración** y la segunda de **confirmación**. La partición se hace antes de puntuar.
- **p de permutación (p_perm):**
  - Hay 999 réplicas. Si p ≤ 0,01, se pasa a 9999; si p ≤ 0,001, a 99 999.
  - p = (1 + #≥)/(1 + B).
  - Para P3 y P12 no hay permutación posible, y p = p_corpus.
- **p de corpus (p_corpus):** percentil superior del estadístico entre los quipus del corpus completo con un número de colgantes entre n/1,5 y 1,5n (excluido el propio quipu).
- **Corrección:** BH y Holm sobre **todas** las pruebas quipu × variante de **cada mitad**. Entran P1–P12, incluida P9b. P6b y P11 llevan su propia corrección interna, ya descrita.
- **Coincidencia declarada:** q_BH(p) < 0,05 **y** p_corpus ≤ 0,05 (la firma debe ser rara entre quipus de tamaño parecido, no solo «tener estructura»).
- **Detalle del Monte Carlo** (fijado antes del barrido; precisa la regla «999 réplicas»):
  - Las réplicas son secuenciales: 199 → 1999 → 19 999 → 99 999. Se pasa al siguiente escalón mientras p ≤ 10/B.
  - Los estadísticos con bucle en Python (P4r, P5b, P5c, P6a, P10, P11a–c y P8ar) tienen un tope de 19 999 (p mínimo 5·10⁻⁵).
  - P6b usa 199 → 1999 (p mínimo 5·10⁻⁴).
- **p_corpus:** si hay < 20 quipus de referencia con el estadístico definido, se usan todos los que lo tienen definido.
- **Validación con controles:** una plantilla queda **validada** si al menos la mitad de sus controles positivos dan p < 0,05 y p_corpus ≤ 0,10, sin corrección (los controles se eligieron a priori). Si no, se revisa **una vez**, la revisión queda documentada y cuenta como variante; si sigue fallando, se descarta.

## 3. Revisiones tras los controles positivos (una por plantilla; antes del barrido)

Los controles se corrieron **antes** de puntuar el corpus (`controles_antes_revision.csv`, `obs_perm_prueba.csv`). Hubo tres cambios. Cada uno cuenta como variante adicional para los senderos bifurcados: **30 + 2 = 32 estadísticos probados**, más un cambio de clave de datos.

1. **P4 → P4r** (padrón).
   - **Por qué falló:** los grupos KFG no recogen las bandas de 6 del Santa. UR088 y UR092 son *un solo* grupo KFG, y UR089, UR090 y UR091 tienen grupos de 36–66. La puerta solo se cumplía en UR087, que sí reconoció (p < 10⁻⁴).
   - **Revisión:** registro = **banda de color**, es decir, una racha de colgantes contiguos del mismo color (MU18 l. 48 los describe así: «six-cord color-coded groups»).
   - **Estadístico P4r:**
     - Se toma el largo modal k ∈ [4, 12] de las bandas. Si hay ≥ 6 bandas de ese largo, el estadístico es k·(n.º de bandas de largo k)/n.º de colgantes; si no, vale 0.
     - Puerta: ≥ 24 colgantes y mediana de valores ≤ 30.
     - Nulo: permutar los colores.
2. **P8a → P8ar** (calendario).
   - **Por qué falló:** con «grupo + grupos de 1 *siguientes*» y la racha en [27, 33], UR006 daba p = 0,24. En KFG, la cuerda de lazo (1 colgante + 9 subsidiarias) **precede** a su grupo de ~21.
   - **Revisión:** unidad = racha de grupos de 1 + el grupo siguiente.
   - **Estadístico P8ar:** n.º de unidades con 26–36 cuerdas, es decir, 30 ± 20 %; Urton, por su parte, cuenta 20–22 + 8–10. Nulo: cortes al azar.
3. **P6b, clave de hallazgo.** UR063 y UR068 tienen `procedencia = Unknown` y `region = Puruchuco`. Por eso «mismo hallazgo» pasa a ser «misma procedencia conocida **o** misma región conocida». El cambio se hizo antes de correr P6b sobre ningún quipu.

**Plantillas sin control positivo en el corpus:** P1 (calles), P2 (censo toledano), P7 (wanka y tasa: el quipu wanka no está en el corpus, véase `ds/n_murra_wanka`), P8b/P8c, P10, P11a–c y P12. Sus coincidencias **no** pueden pasar de «propuesto»: la plantilla no está validada.
