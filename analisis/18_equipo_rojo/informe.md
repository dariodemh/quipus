# 18 · Equipo rojo contra el sistema de Incahuasi (equipo 13)

Carpeta: `analisis/18_equipo_rojo/`. Scripts: `lib18.py` (definiciones de 13 congeladas: registro = grupo no separador rosa; cabecera = primer colgante anudado), `01_jardin.py`, `02_nulos_duros.py`, `03_aburridas.py`. Salidas: `salida_01_jardin.txt`, `salida_02_nulos_duros.txt`, `salida_03_aburridas.txt`. Semilla 18. Las p de Poisson usan la esperanza exacta del nulo de 13 (barajar B): E = (1/n) Σ_i Σ_j 1[a_i + b_j ∈ C].

**Pendiente:** el ataque 4 (fuera de muestra, `04_fuera_muestra.py`) no llegó a escribirse ni a ejecutarse porque se rechazó la escritura del script. Su diseño está en §4 y se dan las cifras que ya se podían leer de los datos sin script nuevo.

## Veredicto por afirmación

| # | Afirmación de 13 | Veredicto | Cifra que lo justifica |
|---|---|---|---|
| 1a | cab(UR273A_i) + cab(UR273B_i) = cabecera de UR266/UR275/UR269 (8/18) | **Sobrevive** (con un p más modesto) | Corregido por la búsqueda completa (58 782 pruebas): p = 0,015 (13 decía 1·10⁻⁴). Desfase k≠0: media 1,0, máx 2 en 16 desfases, frente a 8 en k=0. 59 pares de quipus ajenos con magnitudes parecidas: 0 con p ≤ 10⁻³. |
| 1b | cab(UR267A_i) + cab(UR267B_i) = cabecera de UR269 | **Se debilita** | 5/26 (E = 0,69; p = 7·10⁻⁴) solo si el destino son las *cabeceras* de UR269. Con todas las cuerdas: 6 frente a 2,6, Holm 0,33 en el propio 13. Corregido por la búsqueda completa: **p = 0,32**. Sí resiste los nulos de desfase (5 frente a ≤1) y de dígitos (p = 0,005). |
| 2 | Celda de UR278 = colgante + 1.ª subsidiaria de UR270, columna a columna | **Sobrevive** | 5 de 12 grupos con 6–9/9 columnas frente a 0,003 esperados. Son secuencias de 9 cifras de 3 dígitos casi sin redondos (237 295 138 198 201 153 106 138 187). Sin notas ni alt, KFG = OKR, ninguna huella física compartida. No le apliqué un nulo nuevo: el margen es tan grande que ninguna corrección razonable lo alcanza. Es un argumento, no una cifra calculada. |
| 3 | Totales de fila de UR278 = cabeceras de UR266, en orden | **Sobrevive** (no lo ataqué con cálculo nuevo) | Heredado de 04: q = 1·10⁻⁸ sobre 311 150 pares, con 3 nulos. 16 lo reproduce con 11 pares exactos y τ = 1. Lo único nuevo es la advertencia de procedencia de UR266 (§3a). |
| 4a | 30 + 17 = 47 y 15 + 10 = 25 (las cuotas se suman) | **Se debilita** | El 17 casi no está atestiguado. En UR273B, la propia parte B, aparece en 3 de 27 registros (p = 0,88, según 16). En UR274B, en 12 de 33 (p = 0,06). Además, KFG **omite 32 subsidiarias de UR274B** que sí están en OKR, entre ellas los valores 10, 15, 46 y 47. Que los registros sumados "lleven 47" no es independiente de 1a: todo UR266/UR275 lleva 47. La numerología, sin corregir, da p = 0,01–0,04. |
| 4b | UR269 en bloques de 5 flujos, con la suma 273 en la fila 1 y la suma 267 en la fila 5 | **La estructura interna sobrevive como descripción; la prueba de posición cae** | La P = 1·10⁻³ / 5·10⁻⁵ supone que cualquier fila es igual de probable. Pero las filas se separan por magnitud. La fila 1 tiene cabeceras de 1130 a 1890 (1505–1890 casi todas), las filas 2–4 de 2100 a 2850 y la fila 5 de 392 a 828. Las sumas 267A+B (392–828) solo pueden caer en la fila 5, y las sumas 273A+B (1506–1827) casi solo en la fila 1. Con la magnitud, la posición no añade evidencia. |

## 1. Jardín de senderos (`01_jardin.py`)

**Lo que se exploró de verdad antes de llegar a 1a/1b** (leído de los scripts):
- 04: sumas cuerda a cuerda en ventanas (A1 + A2 = B) sobre todos los tripletes del archivo. **Negativo**: ninguna p_FWER < 0,6.
- 13/01: LCS sobre 378 pares.
- 13/02: 13 260 pruebas de agregados. Ninguna sobrevive al FDR.
- 13/04: 8 parejas A+B × 5 destinos (unión, UR266, UR275, UR269, control) × 2 tolerancias, más 2 pruebas dirigidas a UR269 y 26 pruebas con UR270. En total, 110 pruebas, de las que solo 18 entran en el Holm "principal".
- 16: 3 definiciones de separador. No cambian nada.
- Las pruebas dirigidas (UR269 con cuota 25 o 47) y la unión de los 3 destinos se eligieron después de ver dónde caían las coincidencias.

**Corrección.** Se repitió la búsqueda entera sobre datos nulos (B barajado en cada configuración, 1000 réplicas) y se tomó el mínimo p de la familia.

| Familia | Pruebas | p de la afirmación 1a (5,7·10⁻⁵ sin corregir) | p de 1b (7,5·10⁻⁴) |
|---|---|---|---|
| F13: lo que 13 probó (8 parejas × 4 destinos) | 32 | **0,001** | — |
| Amplia: 194 pares del archivo con ≥8 registros × 3 definiciones de cabecera (primero, máx, suma) × cada quipu destino (todas las cuerdas o solo cabeceras) + unión greedy de los 3 mejores destinos | 58 782 | **0,015** | **0,32** |

En los datos reales, las 4 mejores configuraciones de toda la familia amplia son 273A+273B y 274A+273B (p ≈ 5,7–5,9·10⁻⁵). La 5.ª, UR263+UR272 [suma], está 4 veces peor. Cuidado: las réplicas barajan cada configuración por separado, y eso hace la corrección algo conservadora.

## 2. Nulos más duros (`02_nulos_duros.py`)

- **Desfase** (conserva magnitudes, orden y autocorrelación; solo rompe la alineación):
  - 273A+B: aciertos por desfase de −8 a +8 = 1 1 0 1 0 1 2 2 **8** 1 2 2 1 0 0 0 2.
  - 274A+273B: **7** frente a un máximo de 4.
  - 267A+B → cabeceras de UR269: **5** frente a un máximo de 1.

  El efecto es de alineación registro a registro, no de "magnitudes parecidas".
- **Dígitos** (barajar entre registros solo las unidades de B, o unidades y decenas):
  - 273A+B: 8 frente a 2,7 (p = 0,0012) con unidades, y frente a 1,6 (p = 10⁻⁴) con unidades y decenas.
  - 267A+B: 5 frente a 1,3 (p = 0,005).

  Es el nulo más duro, porque conserva casi toda la cifra, y aun así el efecto lo resiste.
- **Trasplante** (control negativo): pares de quipus de otros archivos con medianas de cabecera dentro de ×2 de UR273A (450) y de UR273B (1328). Son 59 pares con ≥8 registros, y sus sumas se buscan en la misma unión de destino. Fracción media de aciertos 0,05 (máx 0,31, frente a 0,44). Ningún par llega a p ≤ 10⁻³ ni a 8 aciertos.
- **Búsqueda completa dentro de otros archivos.** Mínimo p de cada archivo:

| Archivo | Pruebas | Mínimo p |
|---|---|---|
| Pachacamac | 41 385 | 7,9·10⁻⁴ |
| Ica | 2990 | 1·10⁻² |
| Leymebamba | 1113 | 2·10⁻² |
| Huaquerones | 162 | 0,23 |
| Nazca | 288 | 0,11 |
| Armatambo | 10 | 0,36 |
| **Incahuasi** | 9894 | **5,7·10⁻⁵** |

Ninguna relación "A+B = C" de otro archivo se acerca a la de Incahuasi. En cambio, 1b (7,5·10⁻⁴) queda **al nivel del mejor resultado de Pachacamac**, que se toma por ruido.

## 3. Explicaciones aburridas (`03_aburridas.py`)

**(a) ¿Correcciones del transcriptor?**
- Ninguna de las cuerdas que cuadran (8 de UR273A, 11 de UR273B, 3 de UR274A, 11 de UR267A/B, 26 de los destinos, 84 de UR278 g21–29 y 114 de UR270) lleva notas ni valor alt.
- KFG y OKR son idénticos en valores y número de cuerdas en 45 de los 52 quipus, incluidos todos los implicados salvo UR274B. Esto **no** prueba independencia: ambas bases vienen de la misma hoja de Urton/Chu.
- **Discrepancias KFG–OKR:**
  - UR256: KFG tiene 118 cuerdas y OKR 176.
  - UR274B: 101 frente a 133. Son 32 subsidiarias ausentes en KFG, con valores 1080, 867, 483, 46, 47, 15, 10...
  - UR265: 14 frente a 25.
  - UR255, UR264, UR280 y JC005: diferencias menores.
  - Afecta a las pruebas de cuota y de copia de 13 con UR274B y UR256.
- **Banderas sobre UR266:**
  - Urton (*gurton*) reimportó UR266 entero en OKR el 26-03-2020, después del libro de 2017.
  - De los 12 valores de UR266 que cita Urton 2017 (pp. 166–167), 11 siguen en los datos. **1,732 ya no está**. En su lugar, UR266 g26 dice 1737, que es justo un acierto A+B (448 + 1289) y coincide exactamente con UR275.
  - Hoy hay 20 valores >1000 comunes entre UR266 y UR275. Urton contaba 18 coincidencias exactas, por posición, así que las cifras no son del todo comparables.
  - No cambia el recuento de 1a, porque 1737 también está en UR275 y en UR269. Pero muestra que UR266 se tocó después de conocerse la relación UR266–UR275. Hay que revisar en el objeto UR266 p104.
- La tabla 9.2 de Urton 2017 (UR275) coincide con los datos actuales en los 15 valores comprobables.

**(b) ¿El mismo objeto registrado varias veces?**
- Entre UR273A/B, UR274A/B, UR270, UR278, UR266 y UR275 hay 0 cuerdas anudadas con huella idéntica (nudos + posiciones + largo + color).
- La única cuerda compartida es la de atadura nº 1 de UR273A/B, sin nudos. La nota de campo lo dice expresamente: "Cord 1 and its subsidiaries is the same for both khipus".
- UR270 y UR278 no son el mismo objeto: los largos son distintos, y UR278 g25 es AB entero mientras que UR270 g4 es W.

**(c) ¿Valores frecuentes o redondos?**
- De las 10 sumas acertadas del flujo 47, 3 son múltiplos de 10 y ninguna de 100.
- Fuera de Incahuasi aparecen de media 0,50 veces, frente a 0,53 para cualquier valor de la diana en 1000–3000.
- La diana tiene una densidad del 6,4 % en 1000–3000.
- No hay concentración en valores frecuentes.

## 4. Fuera de muestra (no ejecutado: diseño y lectura directa)

Diseño de `04_fuera_muestra.py`, con R1 congelada (A_i + B_i ∈ unión):
- (i) R1 por mitades de registros.
- (ii) Registros donde UR273A está en blanco y UR274A presente.
- (iii) R1 por mitades en la pareja 267.
- (iv) Fila del bloque de UR269 con un nulo condicionado a la magnitud (±15 %).
- (v) Cuota por fila en los bloques pares frente a los impares.

Lo que se lee sin el script (`salida_01/02` y la tabla de 16):
- Los aciertos de 273A+B están en los registros 3, 9, 11, 12, 13, 17, 18 y 19, es decir, **casi todos en la segunda mitad**.
- Los de 267A+B están en los registros 11, 14, 15, 18 y 21 (con 26 válidos): **ninguno en los registros 0–10**.
- Es compatible con que UR269/UR266 cubran solo una ventana de tiempo, pero esa explicación es post hoc. Una regla derivada en la primera mitad no se habría formulado.
- La predicción (ii) sí funciona: en los 3 registros con UR273A en blanco, UR274A + UR273B da 1278, 2020 y 2106, los 3 exactos en la unión. La esperanza es ≈ 0,2 (13/16 dan ≈ 1,3/18 por registro).

**Para la siguiente ronda:** ejecutar 04 tal como está diseñado, sobre todo (iv) y (v).

## 5. Ataque más dañino

1. **La afirmación 1b (UR267A+B) no sobrevive a la corrección honesta: p = 0,32.** Además depende de dos elecciones hechas a posteriori: solo cabeceras y solo UR269. Su p sin corregir es igual al mejor ruido de Pachacamac.
2. **La prueba de posición en los bloques de UR269 (p hasta 5·10⁻⁵) es, en gran parte, un artefacto de magnitud.**

Lo central, 1a y 2, resiste todos los nulos que probé. 1a baja de p = 10⁻⁴ a p = 0,015 en el peor caso de familia.

## 6. Niveles de evidencia, revisados

- **Bien apoyado:** 2 (UR270 → UR278) y 3 (UR278 → UR266).
- **Apoyado con datos:** 1a, p corregido 0,015, robusto al desfase, a los dígitos y al trasplante.
- **Propuesto:**
  - 1b.
  - 30 + 17 = 47: el 17 es débil y faltan cuerdas de UR274B en KFG.
  - UR269 como libro de 5 flujos: la estructura interna se ve, pero el enlace por posición no es independiente de la magnitud.
- **Especulativo:** UR268 = Σ bloques, sin cambios.

## Para el coordinador

- **Sobreviven:** UR270 → UR278 (P + S1 por columna) y UR278 → UR266 (totales de fila). Son el núcleo del hallazgo. 273A+B también sobrevive (8/18; p corregido por 58 782 pruebas = 0,015; 8 aciertos frente a ≤2 en cualquier desfase; 0 de 59 pares ajenos emparejados por magnitud).
- **Se debilitan:** 267A+B → UR269 (p corregido = 0,32) y la aritmética de cuotas 30 + 17 = 47 (el 17 casi no está en UR273B; KFG omite 32 subsidiarias de UR274B que sí están en OKR).
- **Cae como evidencia independiente:** la "posición en el bloque" de UR269, porque las filas se separan por magnitud.
- **Bandera de datos:** UR266 fue reimportado por Urton en 2020. El valor 1,732 citado en 2017 hoy es 1737, que es un acierto A+B. No cambia el recuento, pero obliga a revisar el objeto.
- **Lo que lo haría irrefutable:**
  - Fotos o relectura independiente de UR273A/B, UR266 p104, UR270 y UR278.
  - Las subsidiarias de UR274B y UR256 que faltan en KFG.
  - Encontrar entre los 5 quipus de Inkawasi no publicados una pareja A/B cuyas sumas den las filas 2–4 de UR269. Esa sería una predicción genuinamente fuera de muestra.
  - Ejecutar `04_fuera_muestra.py`.
