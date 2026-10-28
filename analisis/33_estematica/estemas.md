# 33 · Estemas del corpus de quipus

Notación:
- `A → B`: B deriva de A. Solo se escribe si hay dos criterios independientes (diseño §8); con uno solo se escribe `A ⇢ B (1 criterio)`.
- `A — B`: copia sin dirección.
- `A = B`: el mismo objeto leído dos veces.
- `α`, `β`: testigo perdido, inferido por errores conjuntivos o por fragmentos.
- `···>`: contaminación (contenido tomado de un segundo modelo).

Nivel de cada arista entre corchetes. La salida automática completa (variantes, separativos, conjuntivos, distancias) está en `estemas_auto.md`. Las columnas leídas una a una, en `variantes.csv` y `celdas_alineadas_todo.csv`.

**Advertencia general.** Casi todas las familias tienen 2 testigos. Con dos testigos, el método de Lachmann no puede orientar la arista sin un criterio externo: no hay errores conjuntivos que separar. Solo Leymebamba y el grupo UR1175 tienen 3 testigos, y en el segundo no se solapan. La dirección es casi siempre indecidible, y lo digo así en vez de forzarla.

---

## 1. Incahuasi (sector A y corredor). Un archivo con cuatro clases de relación

```
                UR270 (detalle por 9 columnas)
                  │  celda = colgante + 1.ª subsidiaria            [bien apoyado, 13/18/ciego]
                  ▼
                UR278 (filas de 9)
                  │  totales de fila → cabeceras, en orden          [bien apoyado, 13/ciego]
                  ▼
                  α  (libro perdido: ya contiene los ±1 de unidades)
                 ╱ ╲
            UR266 — UR275    misma lista de cabeceras, desglose distinto;
                             25 valores ≥100 compartidos, los 25 en orden  [apoyado (post hoc); publicado: Urton 2017 cap. 9]

   UR273A + UR273B ──suma──► cabeceras de UR266/UR275                      [apoyado, 13/18]
   UR273B — UR274B   7 valores ≥100 compartidos, en orden                  [propuesto (post hoc); ya en el proyecto (13)]

   UR267A (canasta, sector A) — UR255 (corredor)   27/28 exactas; UR267A añade 12 cuerdas AB:MB
                                                                            [apoyado; publicado: Urton y Chu 2015]
   UR267B (canasta, sector A) — UR256 (corredor)   25 valores ≥100 compartidos, 18 en orden
                                                                            [apoyado (post hoc); publicado: Urton y Chu 2015]
```

- **Error conjuntivo (lo aporta 13/ds y lo confirma el coordinador).** Los desajustes de UR278 frente al libro son de ±1 en las unidades. UR266 y UR275 coinciden entre sí en todos ellos. Eso obliga a un ancestro común `α`, posterior a UR278, del que derivan los dos libros. El error nace en el paso detalle → libro. Es el único error conjuntivo del corpus que da un nudo de estema por encima de un par, y es lo que la crítica de Lachmann exige para afirmarlo.
- **Pares A/B y sus duplicados.** UR255 y UR256 son copias de UR267A y UR267B, guardadas en otro edificio (el corredor, sector C, frente a la canasta del sector A). Se publicaron como «pares cercanos» (Urton y Chu 2015).
  - Corrección dentro del par: UR267B tiene 152 − 10 = 143, y UR256 tiene 153, que cierra la regla [x, c, x − c] (SINTESIS, 2018).
  - Por el criterio 1 (aritmética), UR256 tiene la lectura correcta. Las dos lecturas posibles son que UR256 sea copia corregida o que UR267B sea copia con error. Con un solo criterio, la arista queda **sin dirección**.
- **Lo que el barrido no ve.** UR256/UR267B y UR266/UR275 comparten cabeceras, no tramos: cada fragmento común mide 2 cuerdas, por debajo de τ = 20 bits. La prueba sin orden (05, post hoc) sí los recupera, con q ≤ 1e-7.

## 2. Puruchuco (Huaquerones). Jerarquía con copias del mismo nivel

```
   nivel I     UR063 ──suma──► UR068 (sección central)          [bien apoyado, publicado: Urton y Brezine 2005]
   nivel II    UR064 — UR068          41/47 exactas, 8 variantes  [bien apoyado; publicado]
                         │ suma (2904/2908, 161/162)
   nivel III   UR066 — UR067          20/21 exactas, enrollados juntos  [bien apoyado; publicado: «identical numerical values»]
```

- **UR064/UR068:** 6 diferencias de valor (4 de ±1 nudo) y 1 por daño. Ningún criterio orienta la arista.
- **UR066/UR067:** 1 sola variante. Es el par más fiel del corpus fuera del mismo objeto.
- La arista hacia arriba UR068 → UR067 es de resumen, no de copia (14, n_puruchuco_pacha). Las mismas dos divergencias aparecen frente a UR066 y frente a UR067: son errores conjuntivos de la pareja de nivel III. Eso apoya que UR066 y UR067 salgan de un mismo cálculo, no uno de otro.

## 3. Leymebamba (Centro Mallqui). La única familia con 3 testigos solapados

```
                 UR006 (calendario, 24 pares de conjuntos)
                ╱                         ╲
   UR009 copia p276–p365 de UR006       UR021 copia 3 tramos de p279–p386
   (2 bloques, reordenados, sentido      (directo; 40/44 exactas)
    inverso; 68/74 exactas)               [bien apoyado; publicado: Urton 2005]
   [bien apoyado; publicado: Urton 2005]
                \_________ UR009 — UR021 (21 cuerdas, sentido opuesto; 18/21) _________/
```

- Columnas con lectura numérica en los tres testigos: solo 4 con variante.
  - UR009 es singular 2 veces. Una de ellas es una transposición: 3/1 en p292s5 y p292s5s1.
  - UR021 es singular 1 vez.
  - UR009 = UR021 ≠ UR006 1 vez: p283, 8 frente a 9.
- Particiones incompatibles: 0.
- **Árbol: estrella sin resolver**, con UR006 en el centro.
  - El único conjuntivo posible (p283) es de ±1 nudo. Puede ser coincidencia.
  - No decide entre las dos lecturas: «UR009 y UR021 reportan a UR006» (Urton 2005, consolidación) y «UR009 y UR021 extraen de UR006».
- Las orientaciones opuestas (UR009 invertido frente a UR006 y frente a UR021) indican que el tramo se leyó, o se anudó, en sentido contrario.
- **Nivel:** familia bien apoyada; estema especulativo.
- Falla del equipo rojo: los valores son casi todos menores que 10. Al quitar los 10 valores más comunes del corpus no queda señal (p = 0,31). Esto no rebaja el nivel, porque el par está publicado (§7). Sí avisa de que una copia de valores pequeños **no publicada** quedaría como «propuesta».

## 4. Berlín: UR1175 (Ascher) y UR233 + UR232 (Urton). Una copia en dos piezas

```
   UR1175 (Pachacamac; 268 cuerdas, con capa de subsidiarias)
     ├─ p1–p104   ⇢  UR233  (93 alineadas, 77 exactas; omite 42 de 51 subsidiarias; 100→110 ×4)   [bien apoyado]
     └─ p160–p223 ⇢  UR232  (50 alineadas, 38 exactas; omite 11 de 16 subsidiarias)              [bien apoyado]
   UR233 y UR232 comparten el inventario VA63038 (comentario OKR de KH0469): dos partes de un mismo testigo β.
```

- UR232 y UR233 no se solapan: 0 columnas comunes. No hay conjuntivos que separar.
- Dirección: un criterio, la omisión de una capa entera (lectio brevior). Más la sustitución sistemática 100 → 110. Queda en **`UR1175 ⇢ β` (1 criterio)**. Que β sea una versión sin desglose de UR1175 o que UR1175 sea un desarrollo de β no se puede decidir sin aritmética.
- La procedencia declarada difiere: Pachacamac frente a Huacho. Es el único cruce de sitio que no se explica por la etiqueta.

## 5. Basilea (Museum der Kulturen) y Berlín: UR212 copiado en fragmentos, con contaminación

```
   UR212 (Berlín, 162 cuerdas)
     ├─ p6–p14    → MM008  directo, 8/8      [propuesto: q = 0,007, Holm 0,16]
     ├─ p140–p153 → MM016  INVERSO, 11/13    [bien apoyado]
     └─ p182–p194 → MM015  INVERSO, 13/13    [bien apoyado]
   UR1131 p35–p39 ···> MM016 p15–p19  (5/5 cuerdas W)   [propuesto: q = 0,006, Holm 0,14]
   MM008/MM015/MM016 = IVc.366.03 (14): fragmentos de un mismo testigo β de Basilea.
```

- Los tres fragmentos cubren tramos **disjuntos** de UR212. Es una copia, hoy fragmentada, de varias secciones de UR212.
- Dos fragmentos están en sentido inverso. Las lecturas posibles son que el transcriptor de Basilea numerara desde el otro extremo o que el copista anudara al revés.
- MM016 contiene además 5 cuerdas idénticas a UR1131 (Berlín). Si se confirmara, β sería una **compilación de dos modelos**: la única red con contaminación del corpus. Nivel: **propuesto**.

## 6. Pares de dos testigos sin dirección

| familia | relación | nota estemática | nivel |
|---|---|---|---|
| HP055 (Lima) — UR1084 (París) | 121/142 exactas | UR1084 omite 8 de 14 cuerdas «222» (Holm 3e-4, 14). Salto +10 ×5. 7 diferencias son daño en HP055. Un criterio (omisión): `HP055 ⇢ UR1084 (1 criterio)` | bien apoyado; nuevo frente a la literatura (ya en 04/14) |
| KH0049 (Lima) — UR122 (Gotemburgo) | 68/90 | **Error conjuntivo 15652/15649 en las dos** (30_frontera). Hay fuente común con ese error, o una copia de la otra. UR122 conserva solo la sección de subtotales (extracto); KH0049 tiene 22 cuerdas más en el tramo. Propuesto: `KH0049 ⇢ UR122`, o `α → KH0049, UR122` | bien apoyado; nuevo frente a la literatura |
| UR053B — UR053C | 35/48 | Hermanos del conjunto atado ATE 3517. Uniones R/V opuestas. Diferencias sin signo común (14) | bien apoyado; publicado (Urton 2017, cap. 8) |
| UR1114 — UR1123 (AS114/AS123) | 10/10 | Tramo de 10 cuerdas | bien apoyado; publicado (Urton 2005) |
| UR1118 — UR218 | 7/8 | Tramo corto | bien apoyado; nuevo frente a la literatura |
| QU002 (Dallas) — UR137 (Miami) | 10/11 | Tramo corto | bien apoyado; nuevo frente a la literatura |
| AS159 — AS173 | 8/8 | Tramo corto | apoyado; publicado (Urton 2005) |
| AS128 — QU013 | 43/43 | Solo 9 valores distintos, 2 de ellos ≥ 10. Falla la diversidad | propuesto |

## 7. Extractos de un campo: nuevos (post hoc)

```
   UR234 (Berlín VA66837; ficha NAZ de registros de 8)
     cabeceras de los registros g0–g8: 2007 2080 3012 2247 2578 [rota] 3419 3159 1407
                                        │    │    ≈    │    │     ?     │    │    │
   UR1104 (Berlín VA42527, Pachacamac; Ascher) p8–p16:
                                       2007 2080 3102 2247 2578  2016  3419 3159 1407
   [apoyado (post hoc): 8 valores ≥ 100 compartidos y los 8 en orden; q_comb = 1,9e-6]
```

- La única variante, 3012 frente a 3102, es el **mismo nudo simple leído en posición de decenas o de centenas**: 1S a 21,5 cm en UR234 y a 17,5 cm en UR1104.
- UR234 tiene rota la cabecera de g5 (p41, 6,5 cm). UR1104 conserva ese valor: 2016.
- Ningún otro quipu del corpus contiene más de 1 de esos 9 valores.
- Son objetos distintos: los largos difieren y la dirección de nudo también (UR234 todo Z; UR1104 con los largos en S). Los registraron investigadores distintos: Ascher y Urton.
- Dirección propuesta: `UR234 ⇢ UR1104`. El extracto de un campo es un resumen que sube de nivel. Es especulativa: no hay ningún criterio de §8 que la sostenga.
- 09 ya había marcado el par por valores compartidos, pero no lo analizó. 30 tampoco lo detecta.

```
   UR231 (Berlín VA16135a + b, Ica/Pisco; 954 cuerdas): 6 secciones grandes de 12 cuerdas
     (grupos 3, 16, 28 | 42, 56, 70). Cuerda 9 de cada una:   582  275  286  270  278  390
   UR108 (Lima, Museo Temple Radicati n.º 23; 7 cuerdas):     582  275  286  270  278  370  + 2 (marcadora LG:AB)
   [propuesto (post hoc): K = 5, p_comb = 7e-8, q_comb = 2e-5; el orden solo da 1/60]
```

- Solo UR231 comparte más de 2 de esos valores.
- Son objetos y manos distintas: nudos S en UR108 y Z en UR231; colores AB frente a B, AB y YB.
- **Consecuencia de lado.** Las seis secciones caen a los dos lados de la unión de los fragmentos VA16135a y VA16135b, que KFG reconstruye tras el clúster 39. Si UR108 es un extracto de UR231, apoya esa reconstrucción con un dato externo.

## 8. El mismo objeto leído dos veces (no son copias)

- UR1107 (Ascher) = UR237 (Urton): invertido, 23/26 exactas, r de largos 0,99.
- KH0033 = UR044: 23/23.
- AS125 = UR247: 14/15.

Son el control de «ruido de lectura»: 3 a 7 % de lecturas distintas.

## 9. Descartados por el equipo rojo o negativos

- **UR004 ~ UR037** (escala ×0,5, reordenado; 37/38 exactas). Solo hay 2 valores distintos, ninguno ≥ 10. Son rachas de valores pequeños: **artefacto**.
- **UR113 ~ UR260** (escala ×10). Hay 3 valores distintos, y sin los valores comunes p = 0,6. **Artefacto**.
- **UR004 → UR091** (candidata del lector, «totales en orden»).
  - Exactos: 3 totales aparecen, frente a 2,3 esperados.
  - Con ±1 nudo: 10 frente a 9,6 (p = 0,51).
  - Orden: p = 0,45.
  - Barrido: p = 0,7. **Negativa**.
- **UR1034 → UR1145** (candidata del lector).
  - 5 totales de grupo exactos de UR1034 aparecen en UR1145, en orden (p = 4e-4, nominal y post hoc). Con ±1 nudo: p = 0,10.
  - Cuatro de los cinco totales son 10, 12, 18 y 19. Solo 150 es informativo.
  - En 04 (311 150 pares ordenados) quedaba con q = 0,15.
  - **Especulativa.**
