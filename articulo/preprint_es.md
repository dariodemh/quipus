# Estructura computacional, contabilidad en tres niveles y pruebas fuera de muestra en el corpus digital de quipus andinos

**Autor:** Dario (`dariodemh`), con agentes de IA (Claude Opus/Sonnet y DeepSeek Flash)  
**Repositorio y herramientas:** https://github.com/dariodemh/quipus · Ensayo y Lector en navegador: https://dariodemh.github.io/quipus/articulo/index.es.html  
**Estado:** Preprint abierto a revisión especializada (sin revisión de pares todavía). Todos los estadísticos, controles y fichas son reproducibles de forma determinista desde el repositorio público.

---

## Resumen

Presentamos una auditoría estadística reproducible del corpus digital de quipus andinos, integrando el *Khipu Field Guide* (`651` quipus, `57 818` cuerdas; `650` objetos únicos tras descontar el duplicado `UR044`), el *Open Khipu Repository* (`khipu.db`, `619` quipus, `54 403` cuerdas), `19` hojas de OKR sin integrar (`776` cuerdas), `11` fichas manuscritas recién transcritas de Huacones-Vilcahuasi (`JC024`–`JC034`, `KH0653`–`KH0663`, `101` cuerdas) y el quipu `JS01` (`KH0676`, `138` cuerdas), conformando un corpus ampliado de **682 quipus**. Mediante nulos por permutación dentro de cada quipu, corrección múltiple (Holm y Benjamini-Hochberg), controles positivos (Puruchuco y `KH0049`), prueba ciega sobre datos anonimizados y predicciones prerregistradas fuera de muestra, reportamos tres conclusiones principales:

1. **Contabilidad en tres niveles en Inkawasi:** Ampliando Urton y Chu (2015, 2018), el montón del maní del sector A muestra una cadena verificable donde `colgante + 1.ª subsidiaria` de `UR270` reproduce celda a celda la tabla de 9 columnas de `UR278` (`5/12` grupos comparables con `6–9/9` coincidencias; `p = 0,0002`; recuperada también en prueba ciega), cuyos totales de fila reaparecen en orden como cabeceras de `UR266` (`11/18` exactas, `Holm = 1,6·10⁻⁹`) y `UR275` (`7` exactas, `Holm = 2,8·10⁻⁴`). La pareja atada `UR273A + UR273B` alcanza `8/18` cabeceras por una segunda vía (`p = 0,015` bajo `58 782` pruebas del equipo rojo). El bootstrap de máxima parsimonia (`10 000` réplicas) otorga **99,8 %** de soporte a un libro intermedio perdido `α` (`UR278 → α → {UR266, UR275}`) portador de los desajustes compartidos (`±1`).
2. **Precisión metodológica y resultados negativos:** Aunque Medrano y Khosla (2024) hallaron relaciones tipo Ascher en el `74,15 %` (`482/650`) de los quipus, los nulos por permutación quipu por quipu muestran que el `93–100 %` de las sumas simples aparecen por azar (potencia ~`24 %`); solo `14` quipus (`9` de Inkawasi) resisten dos barajados distintos. El color opera como clave local (`167/403` frente a ~20 esperados) sin léxico compartido entre archivos (`p = 0,34` y `0,79`). En `726` cuerdas con ceros internos (`727` huecos), el espacio vacío mide `0,96` bandas decimales (`1,89×` entre bandas contiguas en `201` cuerdas), pesando contra tesis no posicionales (Florio y Overmann, 2025).
3. **Prueba fuera de muestra y refutación de la Predicción #13:** Sobre los `30` quipus fuera de muestra (`11 Huacones` + `19 OKR extra`), la Predicción #13 (que los quipus 8 y 9 de Huacones tendrían perfil plano de 9 columnas como `UR278`) queda **refutada** (`JC024` tiene `8` colgantes `[119, 29, 29, 19, 10, 19, 5, 4]`, `CV = 1,283`; `JC031` tiene `9` colgantes con `4` vacías, `CV = 1,227`). Sin embargo, `4 de 10` quipus anudados de Huacones (`40 %`) usan gramática **aditiva no decimal** (`2L+9L`, `1E+1E`), y un escáner bayesiano calibrado tolerante a errores no halla enlaces significativos (`q_bh < 0,05`) entre Huacones/OKR-extra/`UR272, 276, 277, 279` y la cadena de Inkawasi.

---

## 1. Corpus, auditoría de bases y transcripciones vírgenes

* **Fuentes principales:** KFG v2.1.0 (`651` Excel, `57 818` cuerdas; `650` objetos únicos) y OKR v2.1.0 (`khipu.db`: `619` quipus, `54 403` cuerdas; `okr-kh-numbers.csv`: `702` filas reales).
* **Erratas documentadas (`C26`; detalle en [`reporte_erratas_okr_kfg.md`](../analisis/paquete_revision/reporte_erratas_okr_kfg.md)):** En Inkawasi, KFG y OKR comparten `>99,8 %` de valores porque derivan de la misma lectura; las únicas tres dobles lecturas independientes (`UR1107=UR237`, `KH0033=UR044`, `AS125=UR247`) fijan un ruido basal de `0–12 %`. KFG pierde `111` cuerdas de Inkawasi presentes en OKR, `92/95` cuerdas superiores de nivel 1 y `502/502` marcadoras; cuatro `.xlsx` (`KH0197, KH0227, KH0267, KH0350`) colisionan; y el `86 %` de las discrepancias KFG–OKR se concentra en cinco quipus (`UR090, UR144, UR235, UR193, UR190`).
* **Corpus fuera de muestra (`30` quipus OOS + `JS01`):** `19` hojas `.xlsx` sin integrar (`776` cuerdas, `analisis/17_okr_pendientes/cuerdas_extra.csv`) + `11` fichas fotográficas inéditas de Huacones-Vilcahuasi (`JC024`–`JC034` / `KH0653`–`KH0663`, `101` cuerdas, `analisis/35_huacones_virgenes/`), donde detectamos además una errata aritmética en la hoja original de `JC028 p5` (`4L+2L+2L+5L = 13` frente a `12` manuscrito), junto con `JS01` (`KH0676`, `138` cuerdas, `analisis/37_vision_y_extra/cuerdas_js01.csv`).

---

## 2. Métodos y escala de evidencia

Todos los detectores aplican nulos por permutación dentro de cada quipu, corrección por Holm o Benjamini-Hochberg, controles positivos (`Puruchuco`, `KH0049`), controles negativos barajados (`AS010`, `UR001`, `AS006`), prueba ciega sobre `52` quipus anonimizados de Inkawasi y predicciones prerregistradas. Distinguimos **indicio fuerte** (nulo + corrección + segundo análisis separado), **indicio** (significativo tras corrección) y **conjetura** (compatible sin prueba excluyente).

---

## 3. Resultados principales

1. **Cadena de Inkawasi (`UR270 → UR278 → α → {UR266, UR275}` y `UR273A + UR273B`):** Véase el detalle cuantitativo en el ensayo ([`index.es.html`](index.es.html)) y en [`resumen_para_especialista.md`](../analisis/paquete_revision/resumen_para_especialista.md). Las `24` filas completas de `UR278` tienen `CV = 0,173`; sus `26` filas de nueve suman `~59 166` unidades (`500–950 t` bajo equivalencias coloniales de `carga` y `fanega`).
2. **Auditoría del `74 %`, ceros posicionales y color:** La medida de Ascher detecta el `74,15 %` (`482/650`), pero entre el `93 %` y el `100 %` se reproduce tras barajar cada quipu (potencia `~24 %`). El color opera como formato local y no léxico imperial (`p = 0,34; 0,79`); su exponente de Heaps (`0,44`) coincide con tablas de datos y no con texto quechua silábico (`0,90`).
3. **Formatos y copias en el corpus:** `KH0049` (`14/18` y `7/18`, `p < 0,0001`) + copia `UR122` compartiendo `15652/15649`; alternancia `A/B/A/B` en `UR040` (`26/31`) y `UR167` (`30/35`); copias como rasgo de archivo (`OR = 17,9`, `p = 10⁻⁷`), incluyendo `HP055 ≈ UR1084` (`121/142`) y el extracto `UR1104 → UR234` (`7/9` exactas, `3102/3012` y `2016` conservado).
4. **Prueba fuera de muestra en Huacones (`JC024–JC034`), `OKR-extra`, `JS01`, `RT-16905`, `UR-298` y `SH001`:** Refutada la Predicción #13; alta prevalencia en Huacones de gramática aditiva no decimal (`4/10` quipus anudados = `40 %`), bucle anudado en cuerda principal (`6/11`), pigmento rojo `RO` (`9/11`) y nudos `Z`, y en `JS01` (`KH0676`, `138` cuerdas) un `99,27 %` (`136/137`) de orden no decimal/aditivo. Fuera de muestra en `UR-298` (`KH0675`), `13` huecos con cero (`10,5 cm`) frente a `45` adyacentes (`5,5 cm`) replican la razón **`1,909`** (`p = 1,94·10⁻⁸`). En `RT-16905` (`KH0638–KH0651`), los quipus enlazados a un mismo hub comparten largo mediano (`p = 0,009`) sin compartir valores (`p = 0,101`). La fotogrametría CIELAB calibrada en `SH001` separa categorías gruesas (`ΔE = 16,1–54,2`) frente a tonos finos `YB`/`AB` (`ΔE = 2,45`). En el lector (`30` quipus), `6/30` reciben género y `24/30` quedan en `SIN`.
5. **Estemática bayesiana y bootstrap (`10 000` réplicas):** Calibrado el canal de error sobre `64` pares de doble lectura y `225` variantes de copia, el escáner `LLR` tolerante a `±1`, `×10` y transposiciones sobre `UR272, 276, 277, 279` y los `30` quipus fuera de muestra arroja **0 pares con `q_bh < 0,05`** (`210` candidatos prefiltrados, mínimo `q_bh = 0,2096`). El bootstrap da **99,8 %** de soporte al nodo perdido `α` en Inkawasi, **14,3 %** en Leymebamba `F02` (estrella no resuelta) y **100,0 %** a la transmisión conjunta `15652/15649` en `KH0049/UR122`.

---

## 4. Protocolo de 5 nudos en museo y disponibilidad

Las cinco comprobaciones físicas decisivas (`UR278 p180`, `UR266 p104`, `UR275 p51`, `UR234 p41` y `KH0049 p19`) están listas en [`protocolo_museo_5_nudos.md`](../analisis/paquete_revision/protocolo_museo_5_nudos.md). Todo el código, datos y el **Lector de Quipus en navegador** (`682` quipus, sin servidor, con carga de CSV propio) están disponibles en `https://github.com/dariodemh/quipus` (MIT / CC BY 4.0).
