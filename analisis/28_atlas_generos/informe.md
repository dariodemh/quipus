# 28. Atlas de géneros: el corpus KFG clasificado por tipo de registro

**Pregunta.** Si juntamos todos los detectores validados del proyecto, ¿qué tipo de registro es, con más probabilidad, cada uno de los 651 quipus de KFG? ¿Con qué confianza? ¿Qué fracción del corpus entendemos estructuralmente?

**Entregables:**

- `atlas.csv`: una fila por quipu con estas columnas: kfg, okr, procedencia, museo, genero, genero_nombre, confianza, evidencia, prediccion, lineas, secundarios, estabilidad.
- `generos.md`: una ficha por género.
- Scripts, en este orden de ejecución: `01_matriz.py`, `03_controles.py`, `02_atlas.py`. Las reglas están en `reglas.py`; ejecutarlo comprueba los 8 controles positivos.
- Salidas intermedias: `matriz.csv`, `cobertura.csv`, `resumen_generos.csv`, `contraste_cluster.csv`, `control_barajado.csv`, `estabilidad.csv` y `salida_0*.txt`.

## 1. Matriz quipu × rasgo (`01_matriz.py`, `matriz.csv`: 651 × 56)

**Rasgos reutilizados** de los CSV de cada detector:

| Rasgo | Origen |
|---|---|
| Sumas locales robustas a M1 y M2 | 08; replica exactamente la lista de 14 |
| Cuerdas superiores y cierre | 01 |
| Fila + total suelto | 14 |
| Relaciones entre quipus | 13/09/04 y n_puruchuco_pacha; listas verificadas |
| Copias | 14 |
| Formulario: tipo, Holm, BH y nivel del archivo | 22 |
| Ficha Nazca | n_ficha_nazca |
| Plantillas P4r (Santa), P8ar (calendario), P11a (bloques) | n_plantillas |
| Tablas: R × K, 1.ª columna mayor, ρ entre columnas | 10 |
| Redondeo y cuotas repetidas | 11 |
| Clase no numérica | n_no_numericos |
| Vueltas ≥ 10 | n_nudos_imposibles |
| Partición color ~ grupo | 24 |
| Discrepancia KFG–OKR | t_okr_vs_kfg |
| Transcriptor | 22 |

**Rasgos recalculados:**

- Desde KFG:
  - fracción de cuerdas no decimales: el valor de la contribución de cada racimo con un lugar repetido o una cifra mayor que 9; por la convención KFG, el número antes del tipo es el VALOR;
  - torsión Z sobre S + Z;
  - cuerdas rotas (terminación B) y fracción anudada;
  - número de colores (normalizado con `re.sub(r'\([^)]*\)','',s)`);
  - NMI color ~ grupo, que es una partición y no depende de las etiquetas.
- Desde OKR (solo lectura): fibra camélida o de lana, marcadoras (`CORD_CLASSIFICATION='M'`) y cuerdas superiores.

**Faltantes y calidad:**

- OKR falta en 9 % de los quipus (fibra en el 52 %).
- La torsión falta (toda U) en el 21 %.
- Las tablas solo están en 177 quipus. La plantilla P4r solo se evaluó en 275, porque tiene puerta de entrada.
- 55 quipus tienen más del 50 % de cuerdas rotas, y 76 tienen menos de 10 cuerdas.
- Transcriptores: UR 294, AS 220, HP 56, JC 23, MM 22, QU 22, KH 14.
- Descartados con razón:
  - `CANUTO_ID` de OKR: está lleno en casi todas las cuerdas, porque es el segmento de color, así que no discrimina.
  - `CONDITIONOFKHIPU = Fragmentary`: solo afecta a 11 quipus OKR que no están en KFG.

## 2. Clasificación transparente

**Reglas** (`reglas.py`): 11 géneros más «sin género».

- Cada regla devuelve un nivel (alta, media o baja), el número de líneas de evidencia y un texto con las cifras.
- Asignación: gana el nivel máximo; si hay empate, el género más específico.
- Si los datos son pobres, los géneros suaves bajan un nivel.
- Los umbrales son perillas explícitas en `U`.
- **Controles positivos** (assert): UR006 → CAL, UR1140 → NAZ, UR278 y UR068 → ARC, UR087 → PAD, UR053A → FOR, UR193 → TAL, UR118 → SUM. Pasan los 8.

**Resultado:**

| Género | n | Alta | Media | Baja | Procedencia dominante |
|---|---|---|---|---|---|
| CAL calendario | 3 | 1 | 2 | 0 | Leymebamba 3 |
| NAZ ficha encabezado + par marcador | 6 | 3 | 3 | 0 | Berlín 5 (Nazca, Ica, Pachacamac) |
| ARC archivo jerárquico | 21 | 18 | 3 | 0 | Incahuasi 14, Puruchuco 7 |
| PAD padrón por persona | 9 | 6 | 0 | 3 | Santa 6 |
| FOR formulario con clave de reparto | 101 | 9 | 61 | 31 | desconocida 34, Pachacamac 18, Ica 9 |
| NON no numérico | 17 | 0 | 5 | 12 | Pachacamac, Huaquerones, Cajamarquilla |
| TAL aditivo/tally (Z) | 28 | 12 | 7 | 9 | variada (circula) |
| SUM decimal con totales internos | 14 | 8 | 6 | 0 | desconocida 9, Paracas 2 |
| ASG asignación (redondas/cuotas) | 28 | 4 | 24 | 0 | Pachacamac 10 |
| TAB tabla de recuento | 55 | 0 | 34 | 21 | desconocida 30, Pachacamac 7 |
| SEG lista segmentada (solo formato) | 76 | 0 | 0 | 76 | variada |
| SIN sin género | 293 | – | – | – | 113 por datos insuficientes, 180 decimales sin estructura |

**Solapes:** 198 de los 358 quipus asignados tienen al menos un género secundario. Lo más frecuente es FOR, TAB o SEG debajo de un género más específico. El atlas los conserva en la columna `secundarios`: el género asignado es el más probable, no el único compatible.

**Contraste no supervisado** (`03_controles.py` A): Ward con k = 12 sobre 25 rasgos estandarizados, los mismos que usan las reglas.

- Concordancia con las reglas: **ARI 0,244 y NMI 0,392**. Solo con asignados: 0,250 y 0,398. Con k = 4–6, ARI ≈ 0,39–0,40.
- **Lo que el agrupamiento recupera solo:**
  - NAZ: los 6 en un cluster de pureza 1,00;
  - PAD: 8 de 9 en un cluster de pureza 1,00;
  - TAL: un núcleo de 10 de 28 en un cluster de pureza 0,71;
  - ARC: 8 de 21 en un cluster propio.
- **Lo que no recupera:**
  - SUM, FOR, TAB, ASG y CAL caen en un gran cluster mixto (cluster 0) o en el de «sin señal».
  - Son géneros definidos por UNA prueba estadística (una suma, un reparto), no por un perfil de muchos rasgos. La distancia euclídea los diluye.
- Estabilidad bootstrap de Ward: ARI medio 0,54 [0,35; 0,70], bastante menor que la de las reglas (sección 5).
- **Conclusión:** el agrupamiento confirma los géneros «de perfil» (Nazca, Santa, tally) y no sirve para los géneros «de prueba». Por eso el atlas se basa en las reglas.

## 3. Fichas por género

Están en `generos.md`. Cada una da n, procedencias, rasgos diagnósticos, analogía documental o etnográfica con su fuente (líneas de `fuentes_txt`) y una predicción comprobable para un quipu típico. En el atlas, cada quipu lleva además su propia predicción con sus cifras (R × K, cifra modal, ejemplo de suma, clave de reparto, fibra y torsión esperadas).

Las analogías se dividen en dos grupos:

- **Documentadas en la fuente:** PAD (padrón del Santa 1670, MU18), ARC (Urton y Chu; Urton y Brezine), CAL (U17 cap. 4), TAL (Mackey 1970; Uhle 1897 en NT), NON (Hyland 2017; Salomon 2004), SUM (encomienda de Aldana 1540 en Medrano 2019), ASG (tasa de Lunahuaná 1577/1590, R).
- **Propuestas:** NAZ (Guacrapaucar, P04) y SEG (registro wanka, Murra 2024).

## 4. Cobertura: cuánto del corpus entendemos

| Confianza | Quipus | % de quipus | % de cuerdas |
|---|---|---|---|
| Alta | 61 | **9,4 %** | 15,5 % |
| Media | 145 | **22,3 %** | 36,9 % |
| Baja | 152 | **23,3 %** | 28,6 % |
| Sin género | 293 | **45,0 %** | 18,9 % |

- Con confianza alta o media entendemos estructuralmente **un tercio de los quipus (31,6 %) y la mitad de las cuerdas (52,4 %)**. Los quipus entendidos son los grandes.
- El 45 % sin género se divide así:
  - 17 % del corpus (113 quipus) por datos insuficientes;
  - 28 % (180 quipus) son «decimal sin estructura detectada». Esa es la frontera real del conocimiento: listas decimales cortas donde los detectores tienen poca potencia.
- La confianza baja la llena sobre todo SEG (76), que solo nos dice cómo está segmentado el quipu, no qué cuenta.

## 5. Controles

**B. Barajado de rasgos entre quipus.** Cada detector se permuta como bloque, independiente de los demás; 200 réplicas (`control_barajado.csv`).

| Métrica | Observado | Barajado (media [IC 95 %]) | p |
|---|---|---|---|
| Asignación igual al atlas (ARI) | 1 | −0,001 [−0,017; 0,017] | 0,005 |
| NMI género ~ procedencia (asignados con procedencia conocida) | **0,355** | 0,220 [0,195; 0,241] | 0,005 |
| NMI género ~ museo | **0,301** | 0,179 [0,162; 0,199] | 0,005 |
| Fracción alta | 0,094 | 0,084 [0,078; 0,089] | 0,010 |
| Fracción sin género | 0,450 | 0,322 | – |
| Quipus asignados con ≥ 2 líneas de evidencia | 0,399 | 0,391 | 0,29 |

- **La validez externa se degrada claramente.** Los géneros del atlas se concentran por sitio y museo mucho más que los de rasgos barajados.
- La fracción de confianza alta baja muy poco, porque los marginales se conservan.
- Al barajar hay MÁS quipus con algún género, porque las señales se reparten en vez de acumularse en los mismos objetos. Las señales reales se **concentran**: el 45 % sin género es real, no un artefacto de umbrales.
- **Negativo honesto:** la «convergencia» (≥ 2 líneas) no supera al barajado (p = 0,29). Las líneas que cuento son casi todas internas a un mismo detector, así que no prueban independencia.
- La silueta de Ward no discrimina (0,12 observada frente a 0,15 barajada), otro motivo para no usar el agrupamiento como árbitro.

**C. Estabilidad** (`estabilidad.csv`; columna `estabilidad` del atlas). Hay tres escenarios, de 200 réplicas cada uno:

- bootstrap de cuerdas dentro de cada quipu, recalculando no decimales, Z, rotas, anudadas y redondeo con su BH;
- umbrales movidos ±25 %;
- ambas cosas a la vez.

El recálculo sin remuestreo reproduce el 99,7 % del atlas.

| Escenario | Mediana | Quipus con estabilidad ≥ 0,8 |
|---|---|---|
| Cuerdas | 1,00 | 93,1 % |
| Umbrales | 1,00 | 95,7 % |
| Ambos | 1,00 | **90,9 %** |

- Por confianza (ambos): alta 97 %, media 83 %, baja 86 %.
- Por género:
  - ARC, CAL, NAZ, PAD y SUM: 100 %;
  - FOR: 96 %;
  - SEG: 93 %;
  - TAB: 80 %;
  - NON: 76 %;
  - **TAL: 68 %;**
  - **ASG: 46 %, el género más frágil.** El umbral del 80 % de cifras redondas en quipus con 8–20 cuerdas elegibles decide la asignación.

## 6. Limitaciones

- Las listas de membresía de ARC, CAL y NAZ son resultados ya verificados que se usan como entrada. No se re-derivan aquí, y la estabilidad bootstrap no los somete a prueba.
- Los géneros por color (FOR cromático, PAD, SEG) dependen de particiones, no de etiquetas. Aun así, el transcriptor fija cuántos colores se distinguen: Ascher ~6, Urton 9,7, Clindaniel 14,9. Un quipu de Ascher tiene menos probabilidad de mostrar partición.
- TAB y FOR se solapan mucho: un formulario que se repite en bloques también es una tabla. 64 quipus FOR tienen TAB como secundario, y 20 detecciones de formulario quedan como TAB porque allí tienen más confianza. Cambiar el orden cambia la etiqueta, no la lectura.
- Las predicciones son comprobables en el objeto (foto, fibra, torsión, conteo de cuerdas) o en un documento. Ninguna se ha comprobado aquí.

## Para el coordinador

- **Cobertura:** de 651 quipus, 61 (9,4 %) tienen género con confianza alta, 145 (22,3 %) media, 152 (23,3 %) baja, y 293 (45,0 %) quedan sin género. **Entendemos estructuralmente ~1/3 de los quipus y ~1/2 de las cuerdas** (52,4 % alta o media).
- **Géneros con base sólida (alta):** ARC 18 (Incahuasi 13 y Puruchuco 5), TAL 12, FOR 9 (UR053A–E, UR131A–C, UR149), SUM 8, PAD 6 (Santa), ASG 4, NAZ 3 y CAL 1. Los formatos de archivo (ARC, PAD, FOR, NAZ, CAL) suman 37 de los 61.
- **Tamaños totales:** FOR 101, SEG 76, TAB 55, TAL 28, ASG 28, ARC 21, NON 17, SUM 14, PAD 9, NAZ 6, CAL 3.
- **Sin género:** 293 = 113 por datos insuficientes + 180 «decimales sin estructura». Esos 180 (28 % del corpus) son la frontera: listas cortas donde los detectores no tienen potencia.
- **Contraste no supervisado:** Ward reproduce sin supervisión NAZ (6/6, pureza 1,0), PAD (8/9, pureza 1,0) y el núcleo de TAL (pureza 0,71). No reproduce los géneros definidos por una prueba (SUM, FOR, ASG). Concordancia global: ARI 0,24 y NMI 0,39.
- **Barajado:** sin el barajado, el atlas se concentra por sitio y museo: NMI género ~ procedencia 0,355 frente a 0,220 barajado, y ~ museo 0,301 frente a 0,179 (p = 0,005). Con barajado, la asignación es azar (ARI ≈ 0).
- **Negativo:** la convergencia de ≥ 2 líneas de evidencia no supera al barajado (0,40 frente a 0,39; p = 0,29). No la uses como argumento de independencia.
- **Estabilidad:** el 90,9 % de los quipus conserva su género en al menos el 80 % de las réplicas (bootstrap de cuerdas + umbrales ±25 %); en confianza alta, el 97 %. Los géneros frágiles son ASG (46 %) y TAL (68 %).
- **Solapes:** 198 de los 358 asignados tienen géneros secundarios (sobre todo FOR, TAB o SEG). El atlas da el más probable y conserva los demás.
- **Predicciones más baratas para cerrar géneros:**
  - fotos de UR179/UR180 (NON: ¿hilos atados?);
  - fibra y torsión de UR050/UR054 (TAL: Z + camélido esperados);
  - marcadoras de UR1140 en foto (NAZ);
  - 5 quipus de Inkawasi no estudiados, con cuotas que sumen 46 o 44 (ARC).
