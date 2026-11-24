# Protocolo de verificación en museo: 5 nudos en 15 minutos

Este protocolo resume las **cinco comprobaciones físicas más baratas y decisivas** de todo el proyecto (`analisis/paquete_revision/predicciones_verificables.md`). Todas son preguntas binarias de lupa sobre objetos específicos que confirman o refutan el núcleo del modelo sin necesidad de transcribir un quipu entero.

---

## 1. UR278, cuerda `p180` (Inkawasi, Sector A · `KH0517`)
* **Qué mirar:** el último racimo largo de la cuerda `p180` (grupo `g21`, columna 1, cuerda blanca `W`, 50 cm).
* **Lectura actual (KFG/OKR):** `2S (4 cm) ; 3S (10 cm) ; 7L (19 cm) ; 1E (24 cm)` = **238**.
* **Pregunta:** ¿el nudo largo a ~19 cm tiene **6 vueltas (`6L`)** o **7 vueltas (`7L`)**?
* **Por qué importa:** cambiar una sola vuelta (`238 → 237`) resuelve **a la vez** dos desajustes independientes de +1:
  1. `UR270 g0` (`178 + 59 = 237`);
  2. el total de la fila `g21` en los libros `UR266/UR275` (`1654 → 1653`).
* **Confirma:** `6L`. **Refuta (error de transcripción):** `7L` claro e intacto (en ese caso, el desajuste ya existía en el registro original).

## 2. UR266, cuerda `p104` (Inkawasi, Sector A · `KH0502`)
* **Qué mirar:** la posición de las unidades de la cuerda `p104`.
* **Lectura divergente:** Urton (2017) publicó **1732** (`2L`); el reimport OKR (2020) y KFG registran **1737** (`7L`).
* **Pregunta:** ¿el nudo largo terminal tiene **7 vueltas (`7L`)** o **2 vueltas (`2L`)**?
* **Por qué importa:** **1737** es una de las 8 sumas exactas que vinculan a la pareja atada `UR273A + UR273B` (`448 + 1289 = 1737`, Hallazgo 2) con el libro `UR266`.
* **Confirma:** `7L` (`1737`). **Refuta esa coincidencia:** `2L` (`1732`).

## 3. UR275, cuerda `p51` (Inkawasi, Sector A · `KH0514`)
* **Qué mirar:** la punta distal de la cuerda `p51` (cuota del registro `g10`), inmediatamente después del racimo de 4 nudos simples (`40`).
* **Lectura actual:** `4S` = **40**, largo **26,5 cm** (frente a una mediana de **41,8 cm** en las otras 24 cuotas de este quipu, todas de valor **47**).
* **Pregunta:** ¿la punta está rota justo después de `4S`, o conserva restos de un `7L`?
* **Confirma:** punta rota o `7L` presente. **Refuta:** punta intacta sin nudo de unidades (sería una cuota real de 40).

## 4. UR234, cabecera del grupo `g5` / cuerda `p41` (Berlín, `VA66837` · `KH0471`)
* **Qué mirar:** el muñón o resto de cuerda `p41` (transcrito con **6,5 cm**, valor `0`, roto).
* **Pregunta:** ¿conserva rastros de nudos o documentación previa que permita reconstruir **2016**?
* **Por qué importa:** `UR1104` (`VA42527`, Berlín) reproduce en orden las cabeceras de `g0–g8` de `UR234` y en esa sexta posición registra **2016**.
* **Confirma:** trazas compatibles con `2016` (o confirmación de rotura compatible con pérdida de nudos). **Refuta:** cuerda intacta sin nudos o valor distinto.

## 5. KH0049 (`AS038`/`HP036`), cuerda `p19` / `B1[1]` (MNAAHP, Lima `3550`)
* **Qué mirar:** la cuerda `p19` (primera cuerda del segundo bloque de 18).
* **Lectura actual:** **15652** (idéntica a la copia parcial de Gotemburgo `UR122`, `1938.45.0228`), mientras que la suma `B3 + B4 + B5` y `B0 − B2` dan **15649**.
* **Pregunta:** ¿`p19` vale efectivamente **15652** (nudo final `2L`) o **15649** (`9L`)?
* **Confirma la transmisión con error conjuntivo:** `15652` en ambos objetos (`KH0049` y `UR122`).

---

## Hoja de respuesta rápida (para enviar por issue o correo)

```text
Objeto / Cuerda       | Foto tomada (S/N) | Observación física exacta        | Estado
----------------------|-------------------|-----------------------------------|------------------
UR278 p180 (KH0517)   |                   | 6L / 7L / ilegible / roto         |
UR266 p104 (KH0502)   |                   | 7L / 2L / ilegible / roto         |
UR275 p51  (KH0514)   |                   | punta rota / 7L / punta intacta   |
UR234 p41  (VA66837)  |                   | muñón roto / trazas / intacta     |
KH0049 p19 (MNAAHP)   |                   | 15652 (2L) / 15649 (9L) / otro    |
```

Las fotos con escala métrica (regla junto a los nudos) y cualquier corrección pueden subirse como issue en `https://github.com/dariodemh/quipus/issues`.
