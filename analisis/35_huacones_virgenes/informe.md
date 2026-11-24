# 35 · Quipus vírgenes fuera de muestra: Huacones-Vilcahuasi (Bajo Cañete) y prueba de la Predicción #13

Fecha: 2026-11-23. Semilla del lector: `20261018`.

## 0. Qué hicimos y por qué importa

Para salir de los datos ya digeridos de KFG y `khipu.db`, transcribimos íntegramente las **11 fichas de registro manuscritas** inéditas en las bases del Open Khipu Repository (`data/external/open-khipu-repository/data/KH0653_0663/JC024_record.jpg`–`JC034_record.jpg`, excavación PIA El Huarco–Huacones, Sector F, Unidad 8, Elemento 11, Lote 97, Registro RAE 1/12/2017): **101 cuerdas** en 11 quipus (`JC024`–`JC034`, `KH0653`–`KH0663`).

Luego pasamos los **30 quipus fuera de muestra** del repositorio (**11 Huacones recién transcritos + 19 quipus de `analisis/17_okr_pendientes/cuerdas_extra.csv`**) por el Lector de Quipus completo y evaluamos la **Predicción #13** de `analisis/paquete_revision/predicciones_verificables.md`.

---

## 1. Veredicto sobre la Predicción #13 (Huacones Quipus 8 y 9)

La Predicción #13 (fijada el 18-10-2026 antes de mirar las fichas) planteaba:
> *«Si los quipus 8 y 9, con 9 colgantes cada uno, registran las mismas 9 unidades [que UR278 de Inkawasi], sus valores descenderán con la posición (ρ < −0,5) y tendrán un CV cercano a 0,2.»*

**Resultado: REFUTADA como tablas de 9 unidades tipo Inkawasi.**

| Quipu | Ficha | Colgantes | Anudadas | Valores de colgantes | ρ (Spearman) | CV | Veredicto |
|---|---|---:|---:|---|---:|---:|---|
| **JC024** | Quipu 8 | 8 | 8 | `[119, 29, 29, 19, 10, 19, 5, 4]` | -0.952 | 1.283 | **No es tabla de 9** (son 8 colgantes: grupo 0 de cabecera `119` + grupo 1 de 7 colgantes `[29, 29, 19, 10, 19, 5, 4]`, suma = 115). |
| **JC031** | Quipu 9 | 9 | 5 | `[11, 1, 4, 8, 0, 0, 0, 0, 9]` | -0.4 | 1.227 | **No es tabla de 9** (4 cuerdas sin nudos, CV = 1.227 ≫ 0,2, y 4 de sus 7 cuerdas anudadas usan gramática **aditiva no decimal** `2L+9L=11`, `2L+6L=8`, `2L+1E=3`, `4L+5L=9`). |

Aunque `JC024` desciende fuerte con la posición (ρ = -0.952), su desigualdad extrema (CV = 1.283 frente a 0,17–0,19 en UR278) y su estructura de 1+7 cuerdas no corresponden al perfil plano de 9 unidades de Inkawasi.

---

## 2. Hallazgos propios de la muestra virgen de Huacones (`JC024`–`JC034`)

1. **Prevalencia alta de gramática aditiva (no posicional decimal estándar):** **4 de 10 quipus anudados (40 %)** tienen cuerdas con múltiples nudos largos o figuras de ocho en la misma cuerda (`JC028` p1/p4/p5/p6, `JC031` p1/p4/p4s1/p9, `JC032` p2/p4, `JC034` p2). En el corpus KFG completo (651 quipus), esta notación aditiva es rara y se concentra en pocos casos como `UR1095`.
2. **Arquitectura física compartida en el lote:** **6 de 11 quipus** cierran la cuerda principal formando un bucle anudado (`JC024, JC025, JC026, JC028, JC030, JC034`); **9 de 11** presentan pigmento rojo (`RO`) aplicado en bandas o recubrimiento completo (`JC034`); y casi todos los racimos reportados llevan dirección **Z** (salvo `JC032 p1s1s1` y `JC033 p5`, en `S`), con torsión final **S**.
3. **Errata detectada en ficha original:** en `JC028 p5`, la transcripción anota `4L(5.0,Z), 2L(10.0,Z), 2L(14.0,Z), 5L(18.0,Z)` (4 + 2 + 2 + 5 = **13**), pero el transcriptor escribió `12` en la columna `value`. En `JC032 p1`, el dígito final de `138` está sobreescrito (`138/139`; los nudos `1S+3S+8L` suman `138`).
4. **Regla P5c («la cuerda mayor abre el grupo»):** en `JC027` (12 colgantes), la primera cuerda vale **259** (4,3× la segunda mayor, 60) y en `JC024` la cabecera `119` abre el quipu (`119` frente a grupo 1 que suma `115`).

---

## 3. Corrida fuera de muestra del Lector de Quipus (30 quipus: 11 Huacones + 19 OKR extra)

Archivo completo: [`resultados_lector_oos.csv`](resultados_lector_oos.csv).

- **Géneros asignados:** 6 de 30 quipus reciben un género del atlas; **24** quedan sin tipo reconocible (`SIN`).
- **Sumas internas frente a nulo por permutación:** ninguno supera el umbral estricto tras corrección (`p_sum_min` más bajo en muestra pequeña: revisar tabla).
- **Relaciones detectadas contra el corpus de 651 quipus:** ninguno de los 30 quipus muestra copia ni enlace aritmético con la cadena de Inkawasi (confirmando también la **Predicción #12** sobre la desconexión entre lotes costeros del Bajo Cañete fuera de Inkawasi Sector A y la cadena del maní).

| Lote | Quipu | Cuerdas | Anudadas | Suma | Aditivas | Género (conf.) | p sumas | p color | p alt. |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| Huacones-OKR | JC024 | 16 | 10 | 273 | 0 | SIN (sin genero) | 0.318 | — | — |
| Huacones-OKR | JC025 | 10 | 10 | 192 | 0 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC026 | 2 | 0 | 0 | 0 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC027 | 12 | 12 | 593 | 0 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC028 | 12 | 12 | 359 | 4 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC029 | 10 | 8 | 291 | 0 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC030 | 5 | 5 | 27 | 0 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC031 | 11 | 7 | 37 | 4 | TAL (baja) | 1.0 | — | — |
| Huacones-OKR | JC032 | 8 | 8 | 558 | 2 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC033 | 8 | 4 | 23 | 0 | SIN (sin genero) | 1.0 | — | — |
| Huacones-OKR | JC034 | 7 | 6 | 51 | 1 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0631 | 22 | 13 | 5108 | 7 | TAL (media) | 1.0 | — | — |
| OKR-extra | KH0633 | 67 | 56 | 414 | 0 | SEG (baja) | 0.326 | — | — |
| OKR-extra | KH0634 | 42 | 38 | 489 | 0 | SIN (sin genero) | 0.09 | — | 1.0 |
| OKR-extra | KH0635 | 166 | 98 | 1328 | 0 | FOR (baja) | 0.057 | — | — |
| OKR-extra | KH0638 | 16 | 15 | 354 | 0 | SIN (sin genero) | 0.37 | — | — |
| OKR-extra | KH0639 | 12 | 11 | 26 | 0 | SIN (sin genero) | 0.504 | — | — |
| OKR-extra | KH0640 | 8 | 5 | 2487 | 0 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0641 | 8 | 6 | 133 | 0 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0642 | 15 | 10 | 1438 | 0 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0643 | 5 | 5 | 63 | 0 | SIN (sin genero) | 0.376 | — | — |
| OKR-extra | KH0644 | 9 | 3 | 55 | 1 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0645 | 7 | 7 | 9 | 0 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0646 | 10 | 8 | 15 | 0 | SIN (sin genero) | 1.0 | — | — |
| OKR-extra | KH0647 | 42 | 23 | 540 | 0 | SIN (sin genero) | 0.06 | — | 0.959 |
| OKR-extra | KH0648 | 58 | 53 | 632 | 0 | SIN (sin genero) | 0.293 | — | — |
| OKR-extra | KH0649 | 30 | 14 | 220 | 2 | FOR (baja) | 0.58 | — | — |
| OKR-extra | KH0650 | 26 | 23 | 80 | 2 | SIN (sin genero) | 0.295 | — | — |
| OKR-extra | KH0651 | 86 | 80 | 697 | 0 | SIN (sin genero) | 0.795 | — | — |
| OKR-extra | KH0702 | 147 | 101 | 277 | 36 | ASG (media) | 0.04 | — | — |
