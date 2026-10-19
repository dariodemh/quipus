# Quipus: análisis computacional del corpus digital

*English version: [README.md](README.md).*

**Borrador para revisión especializada.** Nada de lo que hay aquí ha pasado por revisión de pares.

**Idiomas.** Los informes de cada carpeta y la bitácora están en español. El paquete de revisión tiene versión en inglés en [`analisis/paquete_revision/en/`](analisis/paquete_revision/en/), y la guía del lector, en [`lector/README.md`](lector/README.md).

## Qué es

Este repositorio reúne los análisis, los datos derivados y un **lector** reproducible que da la ficha de lectura de cualquier quipu del corpus. Cada afirmación de la ficha lleva su nivel de evidencia y la ruta del código que la sostiene.

**Por dónde empezar:**

1. [`analisis/paquete_revision/resumen_para_especialista.md`](analisis/paquete_revision/resumen_para_especialista.md): resumen de datos, métodos y hallazgos, por nivel de evidencia.
2. [`analisis/paquete_revision/tabla_hallazgos.csv`](analisis/paquete_revision/tabla_hallazgos.csv): cada hallazgo con su estadístico, su p o q, su archivo fuente, si es nuevo o ya estaba publicado, y si se corrigió.
3. [`analisis/paquete_revision/predicciones_verificables.md`](analisis/paquete_revision/predicciones_verificables.md): predicciones congeladas para comprobar en museos y archivos.
4. [`analisis/paquete_revision/antecedentes.md`](analisis/paquete_revision/antecedentes.md): qué estaba publicado antes.
5. [`lector/LEEME.md`](lector/LEEME.md): uso del lector.

## Cómo se hizo: asistencia de IA

El análisis lo hicieron agentes de IA (Claude, de Anthropic, en Claude Code; además, algunas tareas de extracción con DeepSeek). Los coordinó y dirigió una persona. Los agentes:

- escribieron y corrieron los scripts;
- se revisaron entre sí, con un «equipo rojo» que intentaba romper cada resultado.

Por eso el repositorio insiste en lo que se puede verificar sin confiar en nosotros: cada número sale de un script que se puede volver a correr, y los dos verificadores de abajo fallan si un resultado clave cambia. Los errores que encontramos y corregimos quedan anotados en la columna `corregido_si_no` de la tabla de hallazgos y en los informes de cada carpeta.

**Ningún agente vio los objetos.** Todo sale de las transcripciones publicadas y de la literatura citada.

## Hallazgos principales

| Id | Hallazgo | Nivel |
|---|---|---|
| I01 | UR270 → UR278: colgante + 1.ª subsidiaria = celdas de la tabla de 9 columnas | demostrado |
| I02 | Totales de fila de UR278 = cabeceras de UR266 y totales de UR275, en orden | demostrado |
| I03 | UR273A + UR273B = las mismas cabeceras por una segunda vía | apoyado |
| I09–I10 | Las 9 columnas son las mismas 9 unidades en UR270 y UR278, con una planitud excepcional | demostrado |
| C01 | El 74 % de quipus con sumas no es informativo frente a un nulo correcto | apoyado |
| C06, C18 | El color es una clave local, sin léxico compartido; los quipus son registros de datos, no texto | demostrado / apoyado (negativos) |
| C24, K05 | Copias entre museos; la copia es un rasgo de archivo (OR 17,9) | demostrado / apoyado |
| C27 | El método reproduce la jerarquía publicada de Puruchuco (control positivo) | demostrado |
| K01 | KH0049 es una tabla de tres niveles con totales por columna; UR122 es su copia parcial | apoyado (post hoc) |
| K02 | Tablas de dos columnas en alternancia de colores (UR040, UR167) | demostrado |
| K03 | UR1104 extrae las cabeceras de 9 registros de UR234 y conserva una cabecera rota | apoyado |
| K11 | Unidad de Incahuasi: carga (~23 kg) o fanega; total del orden de 900–1 400 t | propuesto |

La lista completa (I01–I22, C01–C29, K01–K11) está en la tabla de hallazgos.

**Escala de evidencia:**
- **Demostrado:** sobrevive al nulo y a la corrección, y se replicó por una vía independiente.
- **Apoyado:** significativo con corrección, pero sin réplica independiente.
- **Propuesto:** compatible con los datos, sin prueba que lo distinga de las alternativas.
- **Especulativo:** sin prueba.

## Reproducir

Requiere Python 3.10 o superior; se probó con 3.13.

```bash
git clone --recurse-submodules https://github.com/dariodemh/quipus.git
cd quipus
pip install -r requirements.txt

python analisis/paquete_revision/verificar.py   # cifras del paquete de revisión
python lector/verificar.py                      # resultados conocidos del lector
python lector/lector.py UR278                   # ficha de lectura de un quipu
python lector/lector.py --todos                 # todo el corpus (~3 min)
```

**Primera ejecución.** Compila numba (~1 min); después cada ficha tarda entre 4 y 20 s.

**Cómo se abre OKR.** Su base se abre siempre en solo lectura, desde el submódulo: `data/external/open-khipu-repository/data/khipu.db`.

**Scripts de `analisis/`.** Se corren desde la raíz del repo (`python analisis/NN_tema/script.py`): las rutas son relativas a ella. Algunos scripts de `analisis/` escriben archivos intermedios (`.pkl`, imágenes) que no se suben porque se regeneran al correrlos. Si un script lee uno de esos intermedios, hay que correr antes el script que lo genera, en el orden de numeración de las carpetas.

## Estructura

```
analisis/            un directorio por pregunta, numerado en el orden en que se abordó
  datos/             cuerdas.csv: tabla única de cuerdas derivada de KFG
  paquete_revision/  resumen, tabla de hallazgos, predicciones, antecedentes y verificador
  ds/                rondas de agentes (cada carpeta con su informe.md)
  NN_tema/           informe.md + scripts de cada análisis
lector/              lector reproducible (lector.py, detectores.py, verificar.py)
docs/fichas/         fichas de lectura de la literatura
scripts/             construcción de la tabla de cuerdas
data/external/       submódulos: Open Khipu Repository y datos de Medrano y Khosla 2024
```

## Qué no está y por qué

- **Textos y PDFs con derechos de autor.** Cotejamos libros y artículos publicados. Aquí solo quedan las citas breves y las referencias, no los textos.
- **Imágenes y fotografías.** Algunas fuentes prohíben reproducirlas. Ninguna imagen se incluye.
- **Fuentes locales.** Algunos scripts e informes citan rutas de `analisis/fuentes_txt/` (extractos de texto de las publicaciones citadas, usados para cotejar) o de `encontrado/` (archivos fuente, como PDFs y hojas de cálculo). Esas carpetas no se distribuyen; las publicaciones están citadas en los informes.
- **Archivos intermedios regenerables y los scripts de lanzamiento de agentes.** La bitácora de trabajo (`analisis/SINTESIS.md`) sí está, sin notas administrativas. Las entradas que se corrigieron después llevan una nota que remite a la corrección.

## Datos y licencias

- **Open Khipu Repository (OKR)**, v2.1.0. DOI [10.5281/zenodo.18025748](https://doi.org/10.5281/zenodo.18025748). Licencia MIT.
- **Khipu Field Guide (KFG)**: datos de Medrano, M. y Khosla, A. (2024), *How can data science contribute to understanding the khipu code?*, *Latin American Antiquity*. Repositorio v2.1.0, DOI [10.5281/zenodo.10472429](https://doi.org/10.5281/zenodo.10472429). Licencia MIT.

`analisis/datos/cuerdas.csv` se deriva de KFG. Las erratas que encontramos en ambas bases se describen en el hallazgo C26.

**Licencia de este repositorio.** El código y los datos derivados van bajo MIT ([`LICENSE`](LICENSE)), y los textos bajo CC BY 4.0 ([`LICENSE-texts.md`](LICENSE-texts.md)).

## Limitaciones

- **No hemos visto ningún objeto.** En Inkawasi, KFG y OKR son dos codificaciones de la misma lectura (hallazgo K10), así que no contamos con una relectura independiente.
- **Varios hallazgos son post hoc:** K01, K03 y K04. Están marcados como tales y necesitan confirmación con datos nuevos.
- **Los negativos tienen potencia limitada.** Se leen como «no detectable con esta potencia», no como «no existe».
- **La búsqueda de antecedentes es incompleta** en varios hallazgos marcados como «nuevo»; la columna `nuevo_o_publicado` lo indica.

## Cómo citar

> dariodemh (2026). *Quipus: análisis computacional del corpus digital* [repositorio de código y datos, borrador]. https://github.com/dariodemh/quipus

Si usan los datos, citen también OKR y Medrano y Khosla (2024).
