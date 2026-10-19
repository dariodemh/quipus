"""Genera un prompt por tarea en tareas/<id>.md para los agentes DeepSeek (opencode)."""
from pathlib import Path

AQUI = Path(__file__).parent

COMUN = """Eres un investigador de un equipo que intenta descubrir qué significan los quipus andinos. Trabajas en el repo actual (raíz ``).

PRIMERO lee `analisis/BRIEF.md` (datos, reglas de método). Cúmplelo.

LÍMITE DE CONTEXTO (crítico, tienes 200k tokens y no puedes pasarte):
- NUNCA leas ni imprimas archivos grandes completos: ni `analisis/datos/*.csv`, ni PDFs, ni `docs/estado_del_arte.md`, ni `khipu.db`. Consulta siempre con python/pandas o grep e imprime como máximo ~40 líneas por comando.
- Para la literatura usa `grep -n` y lee solo fragmentos; como mucho 4 fichas de `docs/fichas/` completas (salvo que tu tarea diga otra cosa).
- Escribe tus resultados en tu `informe.md` a medida que avanzas, no al final, para no perderlos.
- Escribe SOLO dentro de `{carpeta}/`. No toques nada más. No hagas commits.

ENTREGA: `{carpeta}/informe.md` en español con: pregunta, método, resultados con cifras, controles (nulo, p-valor, corrección múltiple si aplica), resultados negativos, nivel de evidencia (demostrado / apoyado con datos / propuesto / especulativo) y una sección final "Para el coordinador" de 5–10 viñetas con lo más importante. Guarda tus scripts .py en la misma carpeta.

TU TAREA:
"""

KHIPU = """Lectura profunda de un solo quipu: {k}. {extra}
1. Reconstruye su estructura completa: grupos (`grupo`, `analisis/datos/grupos.csv`), cuerdas por grupo, subsidiarias, colores, valores, cuerdas superiores (union T), unión R/V, direcciones de nudo.
2. Busca toda la aritmética interna: colgante = suma de subsidiarias, cuerda superior = suma de grupo, grupo = suma de grupos, valores repetidos, razones constantes, patrones periódicos de color. Compara cada patrón con un nulo (barajar valores dentro del quipu, 1000 veces, semilla 0).
3. Propón la lectura más probable: ¿qué tipo de registro es (censo, tributo, depósito, calendario, otro)? ¿Qué serían las filas y columnas? Justifica con la literatura (grep en `docs/fichas/` por el id {k} y por la procedencia) y marca el nivel de evidencia.
4. Señala lo que no encaja (anomalías, nudos raros, cuerdas sin nudos) y si podría ser información no numérica."""

ARCHIVO = """Monografía del archivo de {p}: quipus {ks}.
1. Describe el conjunto: tamaños, estructuras, colores dominantes, rangos de valores, presencia de sumas, cuerdas superiores, unión R/V, torsión, direcciones de nudo. Tabla por quipu.
2. Busca relaciones ENTRE estos quipus: secuencias de valores compartidas, totales de un quipu que aparecen en otro, estructuras de grupos idénticas (mismo número de cuerdas por grupo), mismos patrones de color. Nulo: barajar valores dentro de cada quipu (500 veces, semilla 0). Ojo: dos nombres del mismo objeto no son un hallazgo (mira `data/external/open-khipu-repository/data/okr-kh-numbers.csv`).
3. Reconstruye, si existe, la jerarquía del archivo (quipus de detalle y de resumen).
4. Contrasta con lo que dice la literatura de este sitio (grep en `docs/fichas/` y `docs/estado_del_arte.md`) y propone qué se registraba aquí."""

LIT = """Extracción de afirmaciones comprobables de la literatura. Lee estas fichas (son cortas): {fs}.
Para cada afirmación concreta sobre el significado o la estructura de quipus que se pueda contrastar con datos (ids de quipus, cifras, patrones de color, sumas, alineaciones con documentos), crea una fila en `{carpeta}/afirmaciones.csv` con columnas: fuente, afirmacion, quipus_implicados, cifras, como_comprobarla, comprobable_con_datos_del_repo (si/no/parcial).
Después COMPRUEBA tú mismo con `analisis/datos/*.csv` las 3–5 afirmaciones más importantes que sean comprobables, y reporta si se sostienen."""

TAREAS = {}
for k, extra in [
    ("AS069", "Es el quipu más grande del corpus (1831 cuerdas), valle de Lluta, Chile."),
    ("UR093", "1227 cuerdas, procedencia desconocida."),
    ("UR231", "954 cuerdas, Ica/Pisco, casi todas cuerdas verso."),
    ("UR006", "Leymebamba; Urton lo propuso como calendario (ver ficha 2001-Urton-calendrical-tomb-text)."),
    ("UR113", "Nazca, 866 cuerdas."),
    ("UR003", "Leymebamba, 758 cuerdas."),
    ("UR1057", "589 cuerdas, procedencia desconocida."),
    ("KH0083", "Mollepampa, 585 cuerdas."),
    ("UR1032", "Nazca, 541 cuerdas."),
    ("UR262", "Incahuasi/Inkawasi, 490 cuerdas; almacén inca de productos (ficha 2015-Urton_inkawasi)."),
    ("UR087", "Valle del Santa, 370 cuerdas; asociado a la revisita de 1670 (fichas 2018-Medrano y 2024-FitzPatrick)."),
    ("UR019", "Leymebamba; estudiado por Saez-Rodríguez como portador de etiquetas (ficha 2014-Saez-Rodriguez-khipu-UR19)."),
    ("CM009", "Región Puruchuco; la contabilidad jerárquica de Puruchuco la estudió Urton (ficha 2005-Urton_puruchuco)."),
    ("UR001", "Leymebamba, 572 cuerdas."),
    ("UR004", "Leymebamba, 573 cuerdas."),
]:
    TAREAS[f"k_{k}"] = KHIPU.format(k=k, extra=extra)

for tid, p, ks in [
    ("a_incahuasi", "Incahuasi (Inkawasi)", "JC001–JC023 y UR255–UR280 (procedencia Incahuasi en quipus.csv)"),
    ("a_leymebamba", "Leymebamba (Laguna de los Cóndores)", "UR001–UR022"),
    ("a_pachacamac_hp", "Pachacamac, serie HP", "HP001–HP032"),
    ("a_pachacamac_asur", "Pachacamac, series AS y UR", "los quipus AS y UR con procedencia Pachacamac"),
    ("a_santa", "Santa", "KH0227, UR087–UR092, UR198 (procedencia Santa)"),
    ("a_ica", "Ica y alrededores", "procedencias que contengan Ica, Ocucaje, Callango, Ullujalla, Pisco"),
    ("a_nazca", "Nazca y Atarco", "procedencias Nazca y Atarco"),
    ("a_lima", "costa central de Lima", "procedencias Armatambo, Huaquerones, near Lima, Chancay, Huacho, Chuquitanta, Marquez"),
    ("a_chile", "norte de Chile", "procedencias Lluta Valley, Arica, Playa Miller"),
]:
    TAREAS[tid] = ARCHIVO.format(p=p, ks=ks)

fichas = sorted(p.name for p in (AQUI / "../../docs/fichas").glob("*.md"))
for i in range(0, len(fichas), 12):
    TAREAS[f"lit_{i // 12 + 1}"] = LIT.format(fs=", ".join(f"`docs/fichas/{f}`" for f in fichas[i:i + 12]), carpeta="{carpeta}")

TAREAS.update({
    "t_okr_vs_kfg": "Calidad de datos: compara cuerda a cuerda los valores de KFG (`analisis/datos/cuerdas.csv`) con los del OKR (`data/external/open-khipu-repository/data/khipu.db`: tablas cord, knot_cluster, knot; une por número KH, columna `okr` de `quipus.csv`). Reconstruye el valor de cada cuerda OKR a partir de sus nudos. Cuantifica discrepancias por quipu y por investigador (prefijo AS/UR/HP/JC). Lista los quipus con más del 5 % de discrepancias: los análisis de los demás equipos deberían saberlo.",
    "t_cuerdas_superiores": "Cuerdas superiores (union T) y cordón principal: lista todos los quipus con cuerdas superiores; para cada una, ¿es la suma de qué cuerdas exactamente (grupo contiguo, cuerdas de un color, cuerdas alternas)? Busca exhaustivamente sumas de subconjuntos contiguos y de subconjuntos por color. Nulo: barajar valores. ¿Qué nos dicen sobre cómo se organizaban las categorías?",
    "t_subsidiarias_profundas": "Árboles de subsidiarias profundos (nivel >= 3, hasta 15): ¿en qué quipus aparecen? ¿Son sumas jerárquicas, listas de detalle, o algo distinto (genealogías, desgloses)? Compara la forma de los árboles con nulos de ramificación aleatoria. Describe los 10 casos más extremos cuerda por cuerda.",
    "t_espaciado": "Información física: ¿el espaciado entre grupos (`grupos.csv`: pos_cm, espacio_cm), la posición de los racimos de nudos (cm, en la columna nudos) y el largo de las cuerdas llevan información? P. ej. ¿grupos separados por espacios mayores marcan secciones con aritmética distinta? ¿El largo de las cuerdas se relaciona con el valor o con el color dentro del quipu (permutación dentro de quipu)?",
    "t_cuerdas_vacias": "El 30 % de las cuerdas no tiene nudos. ¿Qué son? ¿Rotas (terminacion, notas), marcadores de posición, ceros, separadores, etiquetas por color? Analiza su posición en el grupo (primera/última), su color, su unión y su largo frente a las cuerdas con nudos, con permutación dentro de quipu. Distingue cuerdas cortadas de cuerdas completas sin nudos.",
    "t_ceros": "Ceros posicionales: detecta en la columna `nudos` las cuerdas donde falta una posición decimal intermedia (p. ej. 305: centenas y unidades sin decenas), usando la distancia en cm entre racimos frente a las bandas posicionales del quipu. ¿Los quipucamayoc alineaban las posiciones decimales entre cuerdas (como columnas)? ¿Qué tan consistente es la alineación por quipu? ¿Hay quipus sin alineación (posible otro tipo de registro)?",
    "t_notas": "Mina la columna `notas` de `analisis/datos/cuerdas.csv` y las notas de khipu_main/primary_cord en `khipu.db`: clasifica las observaciones cualitativas de los investigadores (cuerdas cortadas, reparaciones, objetos atados, nudos raros, plumas, pelo, colores especiales, cuerdas superiores). Haz un catálogo de rasgos no numéricos con frecuencias por quipu y procedencia. Imprime solo muestras, nunca todas las notas.",
    "t_canutos_fibra": "En `khipu.db`: tablas canuto, canutito, canuto_cluster y la columna FIBER de cord/primary_cord. ¿Qué quipus tienen canutos (envolturas) y qué marcan? ¿La fibra (algodón vs camélido) se asocia a valor, color, posición o procedencia? Unidad = quipu.",
    "t_alt": "Ambigüedades de lectura: compara `valor` con `alt` en `cuerdas.csv` y los valores dudosos (nudos con dirección U, racimos rotos). ¿Cuánta incertidumbre de transcripción hay y dónde? Estima cuánto cambia una suma típica por esa incertidumbre: esto calibra la tolerancia que deberían usar los equipos que buscan sumas.",
    "t_valores_frecuentes": "Vocabulario numérico: ¿qué valores concretos se repiten más de lo esperado en todo el corpus (p. ej. 1, 2, 5, 10, 12, 15, 30, 40, 100) dados la distribución log-uniforme/Benford? Haz el análisis por quipu (cuántos quipus sobrerrepresentan cada valor, nulo por permutación entre quipus). ¿Algunos valores funcionan como códigos (no cantidades)? ¿Se concentran por procedencia o por color?",
    "t_mitades": "Dualidad andina (hanan/hurin, mitades): ¿los quipus se dividen en dos mitades con valores o estructuras espejo (mismo número de cuerdas, misma secuencia de colores, sumas iguales o en razón fija)? Busca simetrías en todo el corpus (primera mitad vs segunda, R vs V, S vs Z) con nulo. Revisa la ficha de Urton sobre binariedad (grep 'binari' en docs/fichas).",
})

(AQUI / "tareas").mkdir(exist_ok=True)
for tid, texto in TAREAS.items():
    carpeta = f"analisis/ds/{tid}"
    (AQUI / "tareas" / f"{tid}.md").write_text(COMUN.format(carpeta=carpeta) + texto.replace("{carpeta}", carpeta), encoding="utf-8")
print(len(TAREAS))
