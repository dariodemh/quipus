# 31. Frontera del atlas: perfiles estadísticos y géneros por semejanza

Scripts: `perfiles.py` (-> `perfiles.csv`, 651 quipus × 28 columnas), `analisis.py` (-> `asignacion_frontera.csv`, `salida_analisis.txt`). Frontera = los 180 quipus SIN con evidencia «decimal sin estructura detectada». Rasgos: ver `perfiles.csv` (valores: mediana/log-rango, ceros, vacíos, red10, red5, Benford, var/media, dígitos; estructura: cuerdas, grupos, tamaño y CV de grupo, subsidiarias/colgante, n.º de colores, colores por grupo, NMI color~grupo, Z, largo; contexto: procedencia y museo). Colores normalizados con `re.sub`; solo se usan conteos y particiones, no etiquetas. Faltantes imputados por la mediana (45 quipus de la frontera no tienen 3 valores ≥ 10, red10 vacío).

## 1. ¿Uno o varios géneros? (180 quipus, 19 rasgos estandarizados)

- k-means; silueta frente a un nulo gaussiano con la misma covarianza (100 réplicas), que representa «un solo género continuo» (el nulo de columnas barajadas es demasiado fácil de superar y daba una conclusión opuesta en k=2).
- Silueta observada 0,19 (k=2), 0,17 (k=3), 0,14 (k=4). Todas superan el nulo (p=0,01; nulo p95 0,15 para k=2), pero **ninguna llega a 0,25**, el umbral convencional de estructura sustancial. Hay estructura real pero débil: un gradiente más que géneros separados.
- Estabilidad bootstrap (ARI): k=2 0,77 [0,03; 0,99], k=3 0,66, k=4 0,42, k=5 0,52. El IC de k=2 es muy ancho (en algunas réplicas el corte cae en otro eje).
- La partición k=2 (estable, 170 de 180 con acuerdo ≥ 0,7) es de **escala**:
  - grupo 0 (122): mediana de 18 cuerdas, valores pequeños (log10 mediana 0,74, es decir ~5), var/media 7,6, 4 colores, 3 grupos, subsidiarias 0,43/colgante;
  - grupo 1 (58): 30 cuerdas, valores ~100 (log 2,0), var/media 738, 12 colores, 5 grupos, subsidiarias 0,25.
- Procedencia: ambos grupos mezclan Unknown, Pachacamac, Ica e Incahuasi (no hay separación geográfica evidente).
- **Lectura:** la frontera no es un solo bloque homogéneo, pero tampoco son varios géneros bien definidos. Es una dispersión de listas cortas, con un eje «cifras pequeñas/pocos colores» frente a «cifras grandes/muchos colores/más grupos».

## 2. Clasificador sobre géneros de confianza alta y media

- Entrenamiento: 198 quipus no frontera (FOR 70, TAB 34, ASG 28, ARC 21, TAL 19, SUM 14, NAZ 6, PAD 6; NON y CAL descartados por n<6). Random forest balanceado, mismos 19 rasgos.
- **Validación cruzada 5 pliegues: exactitud 0,60; exactitud balanceada 0,46**; base mayoritaria 0,35; etiquetas barajadas 0,125 (p95 0,16). Recall: FOR 0,76, TAL 0,74, ASG 0,68, ARC 0,62, SUM 0,57, TAB 0,35, NAZ 0 y PAD 0 (n=6). Solo el 4 % de los casos de validación llega a prob ≥ 0,7 (precisión 1,0).
- Caveat de circularidad: los géneros se definieron con detectores, algunos usan los mismos rasgos (redondez para ASG, Z para TAL); la exactitud es optimista como medida de «verdad» y es una medida de cuánto de la etiqueta se refleja en un perfil.
- **Aplicado a los 180:** el modelo es de mundo cerrado (no tiene clase «ninguno»), así que reparte los quipus entre FOR 65, TAL 48, ASG 29, TAB 26, SUM 5, PAD 4, ARC 3 por argmax. Probabilidad máxima ≥ 0,5 solo en 14, ≥ 0,6 en 4, máximo 0,74. TAL y FOR no son sorprendentes: por construcción los TAL (Z) tienen perfil de listas cortas.
- Por grupo: ambos mejor-clase promedio 0,34 (grupo 0, «TAL») y 0,36 (grupo 1, «FOR»). Es decir, el grupo de cifras grandes se parece al formulario sin clave detectada (FOR) y el de cifras pequeñas a tally/lista corta, pero con probabilidad baja.

## 3. Firmas documentales coloniales (`11_rosetta/transcripciones_numeros.csv`, ítems)

| Clase documental | n | % redondas (≥10) | log10 mediana | distancia Benford |
|---|---|---|---|---|
| padrón/recuento (Santa 1670, encomienda, elicit) | 22 | 0,17 | 1,31 | 0,33 |
| otros recuentos | 6 | 0,60 | 1,74 | 0,61 |
| servicio/asignación (Chupaychos Inca) | 9 | 1,00 | 2,18 | 0,72 |
| tributo (serie Chachapoyas) | 8 | 0,38 | 3,88 | 0,58 |

Frontera: grupo 0 red10 0,25, log mediana 0,74, Benford 0,74; grupo 1 red10 0,34, log mediana 2,0, Benford 0,48.

- Redondez: ambos grupos están entre recuento puro (0,10 esperado; padrón 0,17) y asignación (1,0); coincide con la tasa conjunta del corpus (0,29, informe 11). No son listas de asignación (100 %) ni recuentos puros. Mezcla de recuento con redondeo parcial.
- Escala: grupo 1 (~100) es comparable a asignaciones/inventarios medianos (log 1,7-2,2); grupo 0 (~5) es más pequeño que cualquier clase documental (el más bajo: padrón 1,31), típico de conteos unitarios por cuerda o precios/cantidades pequeñas (m16, mediana 4,5).
- Benford no discrimina: con medianas bajas el primer dígito está truncado, y n documental es 5-22. **Las firmas documentales son demasiado pequeñas (n=45 ítems) para decidir recuento de población vs inventario vs tributo.** Lo único firme es que no son asignaciones de 100 % redondas. Tributo (log 3,9) no se parece a ningún grupo.

## 4. Cuántos de los 180 se asignan con probabilidad ≥ 0,7

- A un género existente: **1** (clasificador; ASG). Con umbral 0,5: 14.
- A un género nuevo bien definido: **0**: ningún grupo cumple silueta ≥ 0,25 más estabilidad, y p_mejor medio < 0,5.
- Total **1 de 180** (0,6 %). `asignacion_frontera.csv` da p_<género> para cada quipu, cluster, estabilidad y mejor género.

## Limitaciones

Imputación por mediana; nulo gaussiano (no captura distribuciones sesgadas); k-means asume grupos esféricos; la mediana de 21 cuerdas por quipu da perfiles ruidosos; rosetta con n pequeño; el clasificador es circular con las reglas del atlas.

## Para el coordinador

- **Estructura de la frontera (evidencia moderada):** los 180 se separan en 2 grupos de escala (122 y 58), silueta 0,19 > nulo gaussiano 0,15 (p=0,01), estables en bootstrap (170/180 con acuerdo ≥ 0,7). Pero la silueta es < 0,25 y el IC de ARI es [0,03; 0,99]: es un gradiente, no géneros nítidos.
- **Un género nuevo (evidencia: negativa):** ningún grupo cumple silueta ≥ 0,25 con k=2…7. 0 de 180 asignables a un género nuevo bien definido.
- **Parecido a géneros conocidos (evidencia baja):** el clasificador (CV 5 pliegues exactitud 0,60, balanceada 0,46, base 0,35) los reparte FOR 65, TAL 48, ASG 29, TAB 26 por argmax, pero solo 14 superan prob 0,5 y 1 supera 0,7 (ASG). El modelo no tiene clase «ninguno» y estima mal NAZ y PAD (n=6).
- **Asignables ≥ 0,7:** 1 de 180 (0,6 %). La frontera sigue siendo frontera con perfiles estadísticos; cualquier asignación más allá de eso requiere nuevas pruebas, no más perfil.
- **Firma documental (evidencia baja):** red10 0,25-0,34 en ambos grupos: ni asignación (1,00) ni recuento puro (0,10-0,17). El grupo de ~100 (58 quipus, 12 colores) tiene escala de inventario/asignación mediana; el de ~5 (122) es más pequeño que todo el material documental. Con 45 ítems y Benford truncado no se puede distinguir padrón de inventario ni tributo.
- **Qué falta:** transcripciones con cifras de inventarios/pueblos pequeños (n documentales); una clase «ninguno» abierta en el clasificador; el otro agente (30) cubre relaciones aritméticas.
