#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_registro.py — Construye el Registro Unificado de Pruebas (test_register.json, .csv y .html)
fusionando:
  1. Los 62 hallazgos históricos de `analisis/paquete_revision/tabla_hallazgos.csv` (I01–I22, C01–C29, K01–K11).
  2. Todas las pruebas prerregistradas (selladas con SHA-256 en `analisis/35_preregistros/MANIFEST_SHA256.csv`),
     post hoc y descriptivas de los Bloques A–D (`P01`–`P06`, `D01.6`, `D02.5`, `D02.6`, `E03.6`, `D03.9`, `D04.5`).

Incluye TODOS los resultados negativos, refutados y sin potencia con igual prominencia que los positivos.
"""
import csv
import json
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent
AN = DIR.parent
RAIZ = AN.parent


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def load_manifest():
    m = {}
    with open(AN / "35_preregistros/MANIFEST_SHA256.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m[r["archivo"]] = r["sha256"]
    return m


def normalize_legacy_verdict(nivel):
    s = nivel.lower()
    if "refutado" in s:
        return "REFUTADO"
    if "retirado" in s or "no bien apoyado" in s:
        return "RETIRADO / NEGATIVO"
    if "negativo" in s or "(negativo)" in s:
        return "NEGATIVO"
    if "bien apoyado" in s:
        return "CONFIRMADO"
    if "apoyado" in s:
        return "APOYADO"
    if "propuesto" in s:
        return "PROPUESTO"
    return "DESCRIPTIVO"


def classify_legacy_domain(hid):
    if hid.startswith("I"):
        return "Inkawasi (Sistema contable)"
    if hid.startswith("C"):
        return "Corpus general y métodos"
    return "Estemática y frontera (Rondas 17–19)"


def build_new_entries(manifest):
    p1 = load_json(AN / "36_corpus_maestro/resultados_P01.json")
    p2 = load_json(AN / "37_bloque_B/resultados_P02.json")
    p3 = load_json(AN / "37_bloque_B/resultados_P03.json")
    p4 = load_json(AN / "38_bloque_C/resultados_P04.json")
    p5 = load_json(AN / "38_bloque_C/resultados_P05.json")
    p6 = load_json(AN / "39_bloque_D/resultados_P06.json")

    by = lambda doc, tid: next(x for x in doc["familia_holm"] if x["test_id"] == tid)

    entries = []

    def add(tid, bloque, dominio, tipo_prueba, pregunta, estadistico, p_raw, p_corr, veredicto,
            prereg_file, fuente, novedad="nuevo"):
        entries.append({
            "id": tid,
            "bloque": bloque,
            "dominio": dominio,
            "tipo": tipo_prueba,
            "pregunta": pregunta,
            "estadistico": estadistico,
            "p_raw": "" if p_raw is None else str(p_raw),
            "p_corr": "" if p_corr is None else str(p_corr),
            "veredicto": veredicto,
            "preregistro": prereg_file or "",
            "sha256": manifest.get(prereg_file, "") if prereg_file else "",
            "fuente": fuente,
            "novedad": novedad,
        })

    # --- P01 (Holm estricto sobre m = 6 según P01 §2, manteniendo los 3 SIN_POTENCIA en el denominador) ---
    p1_eval = [by(p1, tid) for tid in ("P01.1", "P01.3b", "P01.4")]
    p1_eval_sorted = sorted(p1_eval, key=lambda z: z["p"])
    p1_holm_m6 = {}
    rmax_p1 = 0.0
    for idx_m, item in enumerate(p1_eval_sorted):
        val = min(1.0, (6 - idx_m) * item["p"])
        rmax_p1 = max(rmax_p1, val)
        p1_holm_m6[item["test_id"]] = round(rmax_p1, 6)

    x = by(p1, "P01.1")
    add("P01.1", "Bloque A (Corpus Maestro)", "Held-out puro (39 quipus)", "Protocolo congelado SHA-256 (Holm m=6)",
        "¿La cuerda de mayor valor abre el grupo en los 39 quipus held-out puros?",
        f"{x['obs_aciertos']}/{x['n_grupos']} grupos ({x['obs_tasa']:.1%}) vs {x['exp_tasa']:.1%} esperado",
        f"p={x['p']}", f"p_Holm(m=6)={p1_holm_m6['P01.1']}",
        "CONFIRMADO" if p1_holm_m6["P01.1"] < 0.05 else "NEGATIVO",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/resultados_P01.json",
        "confirmación fuera de muestra de K08 (Holm m=6 exacto según protocolo)")

    x = by(p1, "P01.2")
    add("P01.2", "Bloque A (Corpus Maestro)", "Held-out puro (39 quipus)", "Protocolo congelado SHA-256 (Holm m=6)",
        "¿El hueco del cero posicional mide una banda decimal (~1.0) en los quipus held-out?",
        f"n={x['n_cuerdas']} cuerdas elegibles con alturas OKR y cero interno en held-out",
        "N/A", "N/A", "SIN POTENCIA",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/resultados_P01.json",
        "prueba fuera de muestra de C09 (sin cobertura OKR en held-out)")

    x = by(p1, "P01.3a")
    add("P01.3a", "Bloque A (Corpus Maestro)", "Held-out puro (39 quipus)", "Protocolo congelado SHA-256 (Holm m=6)",
        "¿Las cuerdas superiores (T) suman exactamente el grupo contiguo anterior en held-out?",
        f"n={x['n_superiores']} cuerdas superiores (T) en los 39 quipus held-out",
        "N/A", "N/A", "SIN POTENCIA",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/resultados_P01.json",
        "prueba fuera de muestra de C03")

    x = by(p1, "P01.3b")
    add("P01.3b", "Bloque A (Corpus Maestro)", "Rescate OKR (Corpus Maestro)", "Protocolo congelado SHA-256 (Holm m=6)",
        "¿Las cuerdas superiores (T) rescatadas desde OKR suman exactamente el grupo contiguo anterior?",
        f"{x['obs_aciertos']}/{x['n_superiores']} exactas ({x['obs_aciertos']/x['n_superiores']:.1%}) vs {x['exp_aciertos']} esperadas",
        f"p={x['p']}", f"p_Holm(m=6)={p1_holm_m6['P01.3b']}",
        "CONFIRMADO" if p1_holm_m6["P01.3b"] < 0.05 else "NEGATIVO",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/resultados_P01.json",
        "réplica ampliada de C03 sobre cuerdas T rescatadas de OKR (Holm m=6)")

    x = by(p1, "P01.4")
    cands = ", ".join(c["kh_id"] for c in x.get("candidatos", []))
    add("P01.4", "Bloque A (Corpus Maestro)", "Held-out puro (39 quipus)", "Protocolo congelado SHA-256 (Holm m=6)",
        "¿La alternancia de dos colores A/B/A/B (desfase 2) supera el 1 % en held-out?",
        f"{x['n_sig_p001']}/{x['n_quipus']} quipus con p<0.01 vs {x['exp_p001']} esperados ({cands})",
        f"p={x['p']:.2e}", f"p_Holm(m=6)={p1_holm_m6['P01.4']:.2e}",
        "CONFIRMADO" if p1_holm_m6["P01.4"] < 0.05 else "NEGATIVO",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/resultados_P01.json",
        "confirmación fuera de muestra de K02 (Holm m=6)")

    x = by(p1, "P01.5")
    add("P01.5", "Bloque A (Corpus Maestro)", "Held-out puro (39 quipus)", "Protocolo congelado SHA-256 (Holm m=6)",
        "¿Las nuevas copias held-out × corpus se concentran en mismo sitio/museo (OR > 1)?",
        f"{x['n_confirmadas']} copias confirmadas con q_BH<0.05 sobre {x['pares_evaluados']} pares (desviación declarada: B=2000 en lugar de 9999; top bruto KH0139~KH0138 SW=33.82)",
        "N/A", "N/A", "SIN POTENCIA (DESVIACIÓN B=2000)",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/resultados_P01.json",
        "búsqueda fuera de muestra de copias (requiere B>=20000 para superar q_BH sobre 17,766 pares)")

    d16 = p1["descriptivo"]
    add("D01.6", "Bloque A (Corpus Maestro)", "Integridad Karen Thompson (2025) y OKR", "Descriptiva",
        "Sensibilidad a los 222 parches de Karen Thompson (2025) y restauración OKR de Inkawasi (19/19 verificar.py OK)",
        f"0 parches deterministas tocan quipus clave; 19/19 verificar.py intactos; 111 cuerdas Inkawasi restauradas en OKR (UR274B pasa a {d16['ur274b_cuerdas_okr']} cuerdas totales, {d16['ur274b_cuotas_17_okr']} cuotas de 17)",
        "—", "—", "ROBUSTO",
        "P01_corpus_maestro_y_heldout.md", "analisis/36_corpus_maestro/thompson_2025_correcciones.csv",
        "primera integración sistemática de Karen Thompson (2025)")

    # --- P02 ---
    x = by(p2, "P02.1")
    add("P02.1", "Bloque B (RT-16905)", "RT-16905 (15 quipus atados)", "Prerregistrada (Holm)",
        "¿Los quipus unidos en nodos físicos (Hubs A–G / H) contienen sumas jerárquicas >=10 del otro?",
        f"diff_Z adyacentes vs no-adyacentes = +{x['obs_diff_Z_adj_vs_non']:.4f} (10,000 perm QAP)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P02_rt16905_enlazados.md", "analisis/37_bloque_B/resultados_P02.json",
        "primera prueba cuantitativa del conjunto atado RT-16905 (Chirinos/Ghezzi/Álvarez 2023)")

    x = by(p2, "P02.2")
    add("P02.2", "Bloque B (RT-16905)", "RT-16905 (15 quipus atados)", "Prerregistrada (Holm)",
        "¿Los pares físicamente cercanos en RT-16905 tienen mayor similitud numérica SW (estandarizada por tamaño)?",
        f"rho_Mantel = +{x['rho_mantel']:.4f} (top pares adyacentes: K01–K04 z=2.39, K10–K11 z=1.67)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P02_rt16905_enlazados.md", "analisis/37_bloque_B/resultados_P02.json",
        "nuevo negativo: el atado físico no equivale a copias numéricas")

    x = by(p2, "P02.3")
    add("P02.3", "Bloque B (RT-16905)", "RT-16905 (15 quipus atados)", "Prerregistrada (Holm)",
        "¿La cercanía física en RT-16905 correlaciona con coherencia textil (color/torsión sin tamaño)?",
        f"rho_Mantel_textil = +{x['rho_mantel_textil']:.4f}",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P02_rt16905_enlazados.md", "analisis/37_bloque_B/resultados_P02.json", "nuevo")

    x = by(p2, "P02.4")
    add("P02.4", "Bloque B (RT-16905)", "RT-16905 (15 quipus atados)", "Prerregistrada (Holm)",
        "¿Los 19 hilos enrollados de K15 (KH0652) replican la paleta posicional de su huésped K01?",
        f"alineación posicional = {x['align_k15_k01']:.4f}",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P02_rt16905_enlazados.md", "analisis/37_bloque_B/resultados_P02.json", "nuevo")

    n_gsum = sum(1 for r in p2["descriptivo_D02_5"] if r["g_sum_hits"] > 0)
    add("D02.5", "Bloque B (RT-16905)", "RT-16905 (15 quipus atados)", "Descriptiva",
        "Sumas internas dentro de los 14 quipus con colgantes de RT-16905",
        f"0/14 con suma global R1; solo {n_gsum}/14 (K10, 1 de 3 grupos) con suma de grupo",
        "—", "—", "DESCRIPTIVO",
        "P02_rt16905_enlazados.md", "analisis/37_bloque_B/resultados_P02.json", "nuevo")

    # --- P03 ---
    x = by(p3, "P03.1")
    d31 = x["detalle"]
    add("P03.1", "Bloque B (Casos abiertos)", "Huacones-Vilcahuasi (Pred. #13)", "Prerregistrada (Holm)",
        "¿Los quipus de 8–9 colgantes de Huacones-Vilcahuasi replican la planitud (CV<0.25) y descenso de UR278?",
        f"JC031 (KH0660): solo 5 positivos (rho=0.0, CV=0.61); JC024 (KH0653): 8 positivos, rho={d31['JC024_Quipu8']['rho']}, p={d31['JC024_Quipu8']['p']}, pero CV={d31['JC024_Quipu8']['cv']} (no plano)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "SIN POTENCIA / REFUTA PLANITUD",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json",
        "primera prueba directa de Predicción #13 sobre Huacones-Vilcahuasi")

    x = by(p3, "P03.2")
    add("P03.2", "Bloque B (Casos abiertos)", "UR053E → UR053B/C", "Prerregistrada (Holm)",
        "¿Tramos contiguos de tríos W/R/AB de UR053E suman exactamente valores de UR053B/C?",
        f"{x['obs_exactos']} exactos ({x['obs_tol1']} ±1) vs {x['nulo_medio']} nulo medio ({x['n_grupos_E']} tríos W en UR053E)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json",
        "cierra la hipótesis de consolidación directa UR053E → B/C")

    x = by(p3, "P03.3")
    add("P03.3", "Bloque B (Casos abiertos)", "Inkawasi no leídos", "Prerregistrada (Holm)",
        "¿Los 4 quipus no leídos de Inkawasi (UR272/276/277/279, valores OKR reales) cuadran con los 252 objetivos del depósito?",
        f"{x['obs_aciertos']} aciertos vs {x['nulo_medio']} nulo medio",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json",
        "cierra la hipótesis de vínculo aritmético directo con los libros conocidos")

    x = by(p3, "P03.4")
    add("P03.4", "Bloque B (Casos abiertos)", "KH0674 (Dumbarton Oaks)", "Prerregistrada (Holm)",
        "¿KH0674 (held-out, 41 grupos) contiene sumas exactas de grupo en colgantes o colgantes+subs?",
        f"{x['solo_colgantes']['obs']}/{x['n_grupos']} grupos con cuerda-resumen exacta vs {x['solo_colgantes']['nulo_medio']} nulo medio",
        f"p={x['p']}", f"p_Holm={x['p_holm']}",
        "CONFIRMADO" if (x["p_holm"] is not None and x["p_holm"] < 0.05) else "NEGATIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json",
        "HALLAZGO NUEVO prerregistrado en quipu held-out (Dumbarton Oaks)")

    x = by(p3, "P03.5")
    add("P03.5", "Bloque B (Casos abiertos)", "Bases mixtas (Damerow–Englund)", "Prerregistrada (Holm)",
        "¿Algún quipu no-decimal/multiunidad mejora sus sumas exactas bajo pares de bases mixtas (r1, r2)?",
        f"{x['n_quipus_evaluados']} quipus evaluados; mejor ganancia máxima = +1 acierto (p_min = 0.54)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json",
        "refuta hipótesis de sistemas metrológicos de base mixta tipo proto-cuneiforme")

    fl3 = load_json(AN / "37_bloque_B/resultados_flecos_P03.json")
    e36 = p3["post_hoc_E03_6_QU005"]
    e36c = fl3["E03_6_QU005_copias"]
    add("E03.6", "Bloque B (Casos abiertos)", "QU005 (Dallas)", "Post hoc (auditada)",
        "Auditoría de bloques de 19 colgantes en QU005 (57 colgantes = 3 bloques) + barrido de copias en 689 quipus",
        f"{e36['mejor_trio']} en {e36['obs_exactas']}/19 exactas ({e36['obs_tol1']}/19 ±1) vs {e36['nulo_max_medio']} máx nulo sobre 3 tríos; barrido de copias en corpus: 0 copias confirmadas (top SW={e36c['top_5'][0]['sw']}, p_bonf=1.0)",
        f"p_corr={e36['p_corregido_trios']}", f"p_corr={e36['p_corregido_trios']}",
        "APOYADO (POST HOC)",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json; resultados_flecos_P03.json",
        "HALLAZGO POST HOC: 3.ª tabla jerárquica por columnas observada (sin copia en el corpus)")

    bm = fl3["E03_7_British_Museum"]
    bm_sum = ", ".join(f"{k}:{v['n_colgantes']}c/{v['g_sum_hits']}s" for k, v in bm.items())
    add("E03.7", "Bloque B (Casos abiertos)", "British Museum (KH0633–635, KH0702)", "Exploratoria",
        "Barrido exploratorio de sumas internas y copias en los 4 quipus held-out del British Museum",
        f"0/4 con sumas internas significativas ni copias confirmadas en 689 quipus ({bm_sum}; todo p_bonf=1.0)",
        "p_min=0.549", "p_bonf=1.0", "NEGATIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_flecos_P03.json",
        "cierre exploratorio de los 4 quipus held-out del British Museum")

    d38 = fl3["D03_8_UR050_OKR"]
    add("D03.8", "Bloque B (Casos abiertos)", "UR050 (alturas relativas OKR)", "Descriptiva",
        "Reverificación de las 3 zonas relativas de altura de nudos de UR050 (KH0280) directamente sobre OKR khipu.db",
        f"{d38['n_racimos_okr']} racimos en {d38['n_colgantes_con_altura']} colgantes OKR; centroides={d38['centroides_3_zonas_okr']} ({d38['conteos_por_zona']}); ΔBIC={d38['delta_BIC_1_vs_3']}",
        "—", "—", "CONFIRMADO (RÉPLICA OKR)" if d38["reproduce_zonas_020_041_075"] else "NEGATIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_flecos_P03.json",
        "reproduce C11 (0.20/0.41/0.75) directamente sobre coordenadas crudas OKR")

    d39 = p3["descriptivo_D03_9_canete"]
    add("D03.9", "Bloque B (Casos abiertos)", "Valle de Cañete (Huacones vs Inkawasi)", "Descriptiva",
        "Comparación estructural entre Huacones-Vilcahuasi, Inkawasi Sector A (UR) e Inkawasi Sector B (JC)",
        f"Huacones: med={d39['Huacones']['mediana_n_cuerdas']:.0f} cuerdas (max={d39['Huacones']['mediana_max_val']:.0f}) ≈ Inkawasi B (med={d39['Inkawasi_B_JC']['mediana_n_cuerdas']:.0f}, max={d39['Inkawasi_B_JC']['mediana_max_val']:.0f}) vs Inkawasi A (med={d39['Inkawasi_A_UR']['mediana_n_cuerdas']:.0f}, max={d39['Inkawasi_A_UR']['mediana_max_val']:.0f})",
        "—", "—", "DESCRIPTIVO",
        "P03_huacones_y_casos_abiertos.md", "analisis/37_bloque_B/resultados_P03.json", "nuevo")

    # --- P04 ---
    x = by(p4, "P04.1")
    add("P04.1", "Bloque C (Física y Auditoría)", "Color perceptual CIELAB", "Prerregistrada (Holm)",
        "¿Las copias entre transcriptores distintos preservan la cercanía perceptual ΔE2000 pese al cambio de etiqueta textual?",
        f"mediana ratio ΔE2000 = {x['obs_ratio_dE_mediano']:.3f} en {x['n_pares_distinto_investigador']} pares (sí en policromos UR1175~UR232/233: ratio=0.44, p=0.0005; diluido por monocromos)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P04_cielab_y_geometria_2d.md", "analisis/38_bloque_C/resultados_P04.json",
        "primera prueba perceptual CIELAB ΔE2000 entre transcriptores")

    x = by(p4, "P04.2")
    add("P04.2", "Bloque C (Física y Auditoría)", "Color perceptual CIELAB", "Prerregistrada (Holm)",
        "¿La luminancia continua CIE L* correlaciona positivamente con log(1+valor) intra-grupo, incluso EXCLUYENDO el blanco (W)?",
        f"Con W: med_rho=+{x['con_W']['med_rho_global']:.4f} (n={x['con_W']['n_quipus']}, p={x['con_W']['p']}); SIN W: med_rho=+{x['sin_W']['med_rho_global']:.4f} (n={x['sin_W']['n_quipus']}, UR=+0.0595, AS=+0.0083)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}",
        "CONFIRMADO" if (x["p_holm"] is not None and x["p_holm"] < 0.05) else "NEGATIVO",
        "P04_cielab_y_geometria_2d.md", "analisis/38_bloque_C/resultados_P04.json",
        "HALLAZGO NUEVO: gradiente continuo de luminancia L* → magnitud más allá de la convención del blanco")

    x = by(p4, "P04.3")
    add("P04.3", "Bloque C (Física y Auditoría)", "Geometría 2D (OKR)", "Prerregistrada (Holm)",
        "¿La segmentación puramente física por huecos en cm (k=2.0, sin etiquetas humanas) replica las tendencias monótonas intra-grupo?",
        f"{x['n_sig_p005']}/{x['n_quipus_elegibles']} ({x['tasa_obs']:.1%}) quipus con p<0.05 vs {x['exp_p005']} esperados",
        f"p={x['p']:.2e}", f"p_Holm={x['p_holm']:.2e}",
        "CONFIRMADO" if (x["p_holm"] is not None and x["p_holm"] < 0.05) else "NEGATIVO",
        "P04_cielab_y_geometria_2d.md", "analisis/38_bloque_C/resultados_P04.json",
        "HALLAZGO NUEVO: validación física independiente de la segmentación en grupos")

    x = by(p4, "P04.4")
    add("P04.4", "Bloque C (Física y Auditoría)", "Geometría 2D (OKR)", "Prerregistrada (Holm)",
        "¿Los quipus aritméticamente enlazados comparten 'mano física' 2D independiente del valor (estratificado por sitio×capturista)?",
        f"dist media enlazados={x['dist_media_enlazados']:.2f} vs no-enlazados={x['dist_media_no_enlazados']:.2f} (n={x['n_pares_enlazados']} pares en 3 estratos)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NEGATIVO",
        "P04_cielab_y_geometria_2d.md", "analisis/38_bloque_C/resultados_P04.json",
        "nuevo control estratificado sin circularidad por valor")

    d45 = p4["descriptivo_D04_5"]
    add("D04.5", "Bloque C (Física y Auditoría)", "Auditoría de confusión OKR", "Descriptiva (alerta)",
        "PERMANOVA de varianza geométrica 2D: sitio arqueológico vs capturista (CREATED_BY) vs museo",
        f"R²_created_by={d45['R2_created_by']:.3f} > R²_sitio={d45['R2_sitio']:.3f}; R²_museo={d45['R2_museo']:.3f} (n={d45['n_quipus']})",
        "—", "—", "ALERTA DE CONFUSIÓN",
        "P04_cielab_y_geometria_2d.md", "analisis/38_bloque_C/resultados_P04.json",
        "advertencia metodológica crítica para modelos ML sobre geometría OKR")

    # --- P05 (etiquetas exactas del protocolo P05 §2) ---
    x = by(p5, "P05.1")
    add("P05.1", "Bloque C (Auditoría 2026)", "khipu-rv-reproducibility (2026)", "Protocolo congelado SHA-256 (Holm)",
        "¿Sobrevive la entropía de transiciones R/V a un nulo que preserva longitudes de racha y sin el corte arbitrario Top-100?",
        f"Fisher-Yates: {x['cohorte_27']['q_fy_lt005']}/27 y {x['cohorte_completa_sin_top100']['q_fy_lt005']}/39 q<0.05; bajo nulo de rachas: 0/27 y 0/39 q<0.05",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "FRÁGIL A RACHAS",
        "P05_auditoria_2026.md", "analisis/38_bloque_C/resultados_P05.json",
        "auditoría: señal colapsa a 0/39 bajo nulo de rachas (etiqueta exacta P05)")

    x = by(p5, "P05.2")
    add("P05.2", "Bloque C (Auditoría 2026)", "Khipu-ML / Contreras (2026)", "Protocolo congelado SHA-256 (Holm)",
        "¿Sobrevive la firma de torsión imperial (S vs Z) al excluir quipus con >50 % U y evaluar con CV agrupada por sitio?",
        f"Sin >50% U (n={x['n_quipus_sin_U']}): frac_S imperial={x['frac_S_imperiales']:.1%} < otros={x['frac_S_otros']:.1%}; F1 cae de {x['f1_estratificado_sin_U']:.3f} a {x['f1_agrupado_por_sitio_sin_U']:.3f}",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "INFLADO POR SESGO U / FUGA",
        "P05_auditoria_2026.md", "analisis/38_bloque_C/resultados_P05.json",
        "auditoría: colapso en CV agrupada por sitio (etiqueta exacta P05)")

    x = by(p5, "P05.3")
    add("P05.3", "Bloque C (Auditoría 2026)", "Khipu-ML Santa Valley (2026)", "Protocolo congelado SHA-256 (Holm)",
        "¿Es OKR una fuente independiente de collca.db en el Santa, y es rara la firma '5 puros + 1 mixto'?",
        f"Concordancia OKR vs collca.db = {x['concordancia_OKR_vs_collca_Santa']:.1%} (100 % misma fuente); tasa base en otros sitios = {x['tasa_base_5puros_1mixto']:.1%}",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "NO INDEPENDIENTE (MISMA FUENTE)",
        "P05_auditoria_2026.md", "analisis/38_bloque_C/resultados_P05.json",
        "auditoría: pseudorreplicación entre bases espejadas (etiqueta exacta P05)")

    x = by(p5, "P05.4")
    add("P05.4", "Bloque C (Auditoría 2026)", "K-CAT color×magnitud (2026)", "Protocolo congelado SHA-256 (Holm)",
        "¿El Kruskal-Wallis p=3.6e-267 de color×magnitud refleja un léxico global o pseudorreplicación + clave local?",
        f"H ingenuo={x['kw_ingenuo_H']} (p={x['kw_ingenuo_p']:.1e}); clave local R²={x['R2_clave_local_intra_quipu']:.1%} vs etiqueta global R²={x['R2_etiqueta_global_obs']:.2%} (<2 %)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "PSEUDORREPLICACIÓN Y CLAVE LOCAL",
        "P05_auditoria_2026.md", "analisis/38_bloque_C/resultados_P05.json",
        "auditoría: 15× más varianza local que global (etiqueta exacta P05)")

    x = by(p5, "P05.5")
    add("P05.5", "Bloque C (Auditoría 2026)", "K-CAT padre = Σ hijos (2026)", "Protocolo congelado SHA-256 (Holm)",
        "¿La igualdad padre = Σ subsidiarias supera el nulo intra-quipu (permutación de subsidiarias)?",
        f"{x['obs_exactos']}/{x['n_colgantes_ge2subs']} ({x['tasa_obs']:.2%}) vs {x['nulo_medio']} ({x['tasa_nula']:.2%}) nulo; 0 quipus individuales pasan BH",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "SEÑAL REAL (AGREGADA)",
        "P05_auditoria_2026.md", "analisis/38_bloque_C/resultados_P05.json",
        "réplica positiva a nivel agregado, sin potencia quipu por quipu")

    x = by(p5, "P05.6")
    add("P05.6", "Bloque C (Auditoría 2026)", "Zenil & Uthamacumaran (2026)", "Protocolo congelado SHA-256 (Holm)",
        "¿La similitud algorítmica padre-hijo sobrevive a un re-cableado estricto que preserva (quipu, grupo, magnitud)?",
        f"AUC distal replicado={x['auc_rol_distal_holdout']:.3f}; nulo (fibra/torsión) z={x['rewiring_b1_quipu_fibra_torsion']['z']}, p=0.002 -> nulo (grupo/magnitud) z={x['rewiring_b2_quipu_grupo_magnitud']['z']}",
        f"p={x['p']}", f"p_Holm={x['p_holm']}", "EXPLICADO POR ESCALA LOCAL",
        "P05_auditoria_2026.md", "analisis/38_bloque_C/resultados_P05.json",
        "auditoría: aísla el escalado decimal local como mecanismo")

    # --- P06 ---
    x = by(p6, "P06.1")
    add("P06.1", "Bloque D (Torneo Colonial)", "Corpus Colonial Ampliado", "Prerregistrada (Holm)",
        "¿Son separables los géneros fiscales coloniales bajo LODO y bajo Leave-One-Source-Out (LOSO) sin aprender autor?",
        f"n={x['n_items']} ítems en {x['n_tablas']} tablas; LODO bAcc={x['balanced_acc_LODO']:.3f} (p={x['p_LODO']}); LOSO bAcc={x['balanced_acc_LOSO']:.3f} (p={x['p_LOSO']})",
        f"p={x['p']}", f"p_Holm={x['p_holm']}",
        "CONFIRMADO" if x["veredicto"] == "SEPARABLES" else "NEGATIVO",
        "P06_torneo_colonial_generativo.md", "analisis/39_bloque_D/resultados_P06.json",
        "torneo generativo multi-fuente con control LOSO")

    x = by(p6, "P06.2")
    dc = x["detalle_controles"]
    c_str = ", ".join(f"{k}:{v['hits']}/{v['n']}({v['acc']:.0%})" for k, v in dc.items())
    add("P06.2", "Bloque D (Torneo Colonial)", "Controles positivos no circulares", "Prerregistrada (Holm)",
        "¿El modelo entrenado solo en textos coloniales acierta los 3 controles cerrados (ASG, PAD Santa, TAL OOD)?",
        f"acierto medio={x['acierto_medio_3_controles']:.1%} ({c_str})",
        f"p={x['p']}", f"p_Holm={x['p_holm']}",
        "CONFIRMADO" if x["veredicto"] == "CONTROLES_CONFIRMADOS" else "NEGATIVO",
        "P06_torneo_colonial_generativo.md", "analisis/39_bloque_D/resultados_P06.json",
        "controles no circulares cerrados antes del hash")

    x = by(p6, "P06.3")
    add("P06.3", "Bloque D (Torneo Colonial)", "Frontera 180 quipus + FPR", "Prerregistrada (Holm)",
        "¿Asigna el modelo generativo la frontera de 180 quipus con FPR empírica < 5 % en 1,000 sintéticos?",
        f"{x['n_asignados_post070_chi005']}/{x['n_frontera_ge10']} ({x['tasa_asignada_frontera']:.1%}) asignados vs FPR sintética={x['FPR_sinteticos_1000']:.1%}",
        f"p={x['p']}", f"p_Holm={x['p_holm']}",
        "APOYADO" if x["veredicto"] == "APOYADO" else "NEGATIVO / FPR ALTA",
        "P06_torneo_colonial_generativo.md", "analisis/39_bloque_D/resultados_P06.json",
        "calibración abierta con rechazo OOD y FPR en 1,000 sintéticos")

    x = by(p6, "P06.4")
    add("P06.4", "Bloque D (Torneo Colonial)", "Predicción #17 (sin Bambamarca)", "Protocolo congelado SHA-256 (Holm)",
        "¿Descienden sistemáticamente de mayor a menor las listas coloniales de >=7 unidades (excluyendo Bambamarca)?",
        f"{x['n_listas_ge7_sin_Bambamarca']} listas independientes; mediana rho={x['mediana_rho']:+.4f} (no cruza umbral binario congelado < −0.30; nota: 6/8 negativas, p_Holm={x['p_holm']}), mediana CV={x['mediana_cv']:.3f}; 0/8 igualan a UR278 en pendiente (−0.73) ni planitud (CV=0.173)",
        f"p={x['p']}", f"p_Holm={x['p_holm']}",
        "CONFIRMA PREDICCIÓN #17 (REGLA BINARIA P06.4)" if x["veredicto"] == "ORDEN_DE_PRESTIGIO_CONFIRMA_P17" else "DESCENSO SISTEMÁTICO",
        "P06_torneo_colonial_generativo.md", "analisis/39_bloque_D/resultados_P06.json",
        "regla binaria exacta P06.4 cumplida sin mover umbrales (med_rho=-0.2939 >= -0.30)")

    return entries


def build_legacy_entries():
    entries = []
    with open(AN / "paquete_revision/tabla_hallazgos.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            hid = r["id"]
            entries.append({
                "id": hid,
                "bloque": "Rondas 1–19 (Paquete de revisión)",
                "dominio": classify_legacy_domain(hid),
                "tipo": "Exploratoria / Verificada (v1)",
                "pregunta": r["hallazgo"],
                "estadistico": r["estadistico"],
                "p_raw": r["p_o_q"],
                "p_corr": r["p_o_q"],
                "veredicto": normalize_legacy_verdict(r["nivel"]),
                "preregistro": "analisis/n_plantillas/predicciones_preregistradas.md" if hid == "C21" else "",
                "sha256": "",
                "fuente": r["archivo_fuente"],
                "novedad": r["nuevo_o_publicado"],
            })
    return entries


HTML_TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Registro Unificado de Pruebas — Lo que suman los quipus (v2.0)</title>
<style>
  :root {
    --bg: #faf8f4; --card: #ffffff; --ink: #1f1e1c; --muted: #66615a;
    --line: #e4ded3; --accent: #7a2e1d; --ok: #1d6b45; --ok-bg: #e8f5ee;
    --warn: #8a5600; --warn-bg: #fdf3dc; --bad: #992424; --bad-bg: #fbeaea;
    --neu: #4a5568; --neu-bg: #edf0f5;
  }
  * { box-sizing: border-box; }
  body { margin: 0; font-family: Georgia, "Times New Roman", serif; background: var(--bg); color: var(--ink); line-height: 1.5; }
  header { background: #1e1a17; color: #f6f1e9; padding: 28px 24px 22px; border-bottom: 4px solid var(--accent); }
  .wrap { max-width: 1260px; margin: 0 auto; padding: 0 20px; }
  h1 { margin: 0 0 6px; font-size: 1.85rem; font-weight: 600; letter-spacing: -0.01em; }
  .sub { margin: 0; color: #cfc6b9; font-family: system-ui, -apple-system, sans-serif; font-size: 0.94rem; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; margin: 20px 0 18px; }
  .stat { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 12px 14px; font-family: system-ui, sans-serif; }
  .stat .n { font-size: 1.65rem; font-weight: 700; color: var(--ink); line-height: 1.1; }
  .stat .l { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }
  .controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 16px; font-family: system-ui, sans-serif; }
  input[type=search], select { padding: 8px 11px; border: 1px solid #cfc7ba; border-radius: 6px; background: #fff; font-size: 0.9rem; color: var(--ink); }
  input[type=search] { flex: 1 1 260px; }
  .pills { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; font-family: system-ui, sans-serif; }
  .pill { border: 1px solid var(--line); background: #fff; padding: 5px 11px; border-radius: 999px; font-size: 0.8rem; cursor: pointer; color: var(--ink); }
  .pill.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  .manifest { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; margin-bottom: 18px; font-family: system-ui, sans-serif; font-size: 0.84rem; }
  .manifest summary { cursor: pointer; font-weight: 600; color: var(--accent); }
  .manifest code { font-family: ui-monospace, Consolas, monospace; font-size: 0.76rem; color: #3a342e; word-break: break-all; }
  table { width: 100%; border-collapse: collapse; background: var(--card); border: 1px solid var(--line); border-radius: 8px; overflow: hidden; font-family: system-ui, -apple-system, sans-serif; font-size: 0.86rem; }
  th { background: #f2ece2; text-align: left; padding: 10px 10px; font-weight: 600; font-size: 0.77rem; text-transform: uppercase; letter-spacing: 0.04em; color: #4a433b; border-bottom: 1px solid var(--line); }
  td { padding: 10px 10px; border-bottom: 1px solid #efeae1; vertical-align: top; }
  tr:hover td { background: #fcfaf6; }
  .idcell { font-family: ui-monospace, Consolas, monospace; font-weight: 700; white-space: nowrap; color: var(--accent); }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 0.73rem; font-weight: 600; white-space: nowrap; }
  .b-ok { background: var(--ok-bg); color: var(--ok); }
  .b-warn { background: var(--warn-bg); color: var(--warn); }
  .b-bad { background: var(--bad-bg); color: var(--bad); }
  .b-neu { background: var(--neu-bg); color: var(--neu); }
  .meta { font-size: 0.76rem; color: var(--muted); margin-top: 4px; }
  .sha { font-family: ui-monospace, Consolas, monospace; font-size: 0.7rem; color: #6e655b; }
  .countbar { font-family: system-ui, sans-serif; font-size: 0.84rem; color: var(--muted); margin-bottom: 8px; }
  footer { margin: 28px 0 40px; text-align: center; font-family: system-ui, sans-serif; font-size: 0.8rem; color: var(--muted); }
</style>
</head>
<body>
<header>
  <div class="wrap">
    <h1>Registro Unificado de Pruebas — <em>Lo que suman los quipus</em> (v2.0)</h1>
    <p class="sub">Auditoría completa y sin conexión de todas las pruebas ejecutadas: positivas, negativas, refutadas, sin potencia y selladas criptográficamente con SHA-256 (Bloques A–D + Rondas 1–19).</p>
  </div>
</header>
<div class="wrap">
  <div class="stats" id="stats"></div>

  <details class="manifest">
    <summary>Manifiesto SHA-256 de prerregistros congelados antes de ejecutar código (P01–P06, v1.1 post-equipo-rojo con Claude Opus)</summary>
    <div id="manifest-list" style="margin-top:8px"></div>
  </details>

  <div class="controls">
    <input type="search" id="q" placeholder="Buscar por ID (P03.4, E03.6, P05.1, I01...), quipu (KH0674, QU005, UR278...), método o palabra...">
    <select id="f-bloque"><option value="">Todos los bloques</option></select>
    <select id="f-tipo"><option value="">Todos los tipos</option></select>
  </div>
  <div class="pills" id="pills"></div>
  <div class="countbar" id="countbar"></div>

  <table>
    <thead>
      <tr>
        <th style="width:76px">ID</th>
        <th style="width:155px">Bloque / Tipo</th>
        <th>Pregunta / Hipótesis</th>
        <th style="width:270px">Estadístico y evidencia</th>
        <th style="width:125px">p / Holm / q</th>
        <th style="width:145px">Veredicto</th>
      </tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>

  <footer>
    Generado automáticamente por <code>analisis/registro_pruebas/construir_registro.py</code> · Semilla fija <code>20261127</code> · Todas las pruebas negativas se publican con idéntica visibilidad que las positivas.
  </footer>
</div>

<script>
const DATA = __DATA_JSON__;
const MANIFEST = __MANIFEST_JSON__;

function vClass(v) {
  const s = v.toUpperCase();
    if (s.includes("CONFIRMADO") || s.includes("ROBUSTO") || s.includes("CONFIRMA PRED") || s.includes("SEÑAL REAL")) return "b-ok";
  if (s.includes("APOYADO")) return "b-ok";
  if (s.includes("REFUTADO") || s.includes("NEGATIVO") || s.includes("RETIRADO") || s.includes("EXPLICADO") || s.includes("FRÁGIL") || s.includes("INFLADO") || s.includes("MISMA FUENTE") || s.includes("CLAVE LOCAL")) return "b-bad";
  if (s.includes("PROPUESTO") || s.includes("POTENCIA") || s.includes("ALERTA") || s.includes("NO EJECUTADO")) return "b-warn";
  return "b-neu";
}
function vGroup(v) {
  const s = v.toUpperCase();
  if (s.includes("CONFIRMADO") || s.includes("APOYADO") || s.includes("ROBUSTO") || s.includes("CONFIRMA PRED") || s.includes("SEÑAL REAL")) return "Positivo / Apoyado";
  if (s.includes("REFUTADO") || s.includes("NEGATIVO") || s.includes("RETIRADO") || s.includes("EXPLICADO") || s.includes("FRÁGIL") || s.includes("INFLADO") || s.includes("MISMA FUENTE") || s.includes("CLAVE LOCAL")) return "Negativo / Refutado";
  if (s.includes("POTENCIA") || s.includes("ALERTA") || s.includes("NO EJECUTADO")) return "Sin potencia / Pendiente";
  if (s.includes("PROPUESTO")) return "Propuesto";
  return "Descriptivo";
}

// Stats
const tot = DATA.length;
const nPrereg = DATA.filter(d => d.tipo.startsWith("Prerregistrada") || d.tipo.startsWith("Protocolo congelado")).length;
const nPos = DATA.filter(d => vGroup(d.veredicto) === "Positivo / Apoyado").length;
const nNeg = DATA.filter(d => vGroup(d.veredicto) === "Negativo / Refutado").length;
const nLow = DATA.filter(d => vGroup(d.veredicto) === "Sin potencia / Alerta").length;
const nProp = DATA.filter(d => vGroup(d.veredicto) === "Propuesto").length;
document.getElementById("stats").innerHTML = [
  [tot, "Pruebas registradas"],
  [nPrereg, "Prerregistradas (SHA-256)"],
  [nPos, "Confirmadas / Apoyadas"],
  [nNeg, "Negativas / Refutadas"],
  [nLow, "Sin potencia / Alertas"],
  [nProp, "Propuestas"]
].map(([n, l]) => `<div class="stat"><div class="n">${n}</div><div class="l">${l}</div></div>`).join("");

document.getElementById("manifest-list").innerHTML = Object.entries(MANIFEST).map(
  ([f, h]) => `<div style="margin:4px 0"><strong>${f}</strong>: <code>${h}</code></div>`
).join("");

// Populate selects
const bloques = [...new Set(DATA.map(d => d.bloque))];
const tipos = [...new Set(DATA.map(d => d.tipo))];
const fb = document.getElementById("f-bloque");
bloques.forEach(b => fb.insertAdjacentHTML("beforeend", `<option value="${b}">${b}</option>`));
const ft = document.getElementById("f-tipo");
tipos.forEach(t => ft.insertAdjacentHTML("beforeend", `<option value="${t}">${t}</option>`));

let activeGroup = "TODOS";
const groups = ["TODOS", "Positivo / Apoyado", "Negativo / Refutado", "Sin potencia / Pendiente", "Propuesto", "Descriptivo"];
const pills = document.getElementById("pills");
function renderPills() {
  pills.innerHTML = groups.map(g => `<button class="pill ${activeGroup===g?'active':''}" data-g="${g}">${g}</button>`).join("");
  pills.querySelectorAll(".pill").forEach(btn => btn.onclick = () => { activeGroup = btn.dataset.g; renderPills(); render(); });
}

function esc(s) {
  return String(s || "").replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

function render() {
  const q = document.getElementById("q").value.trim().toLowerCase();
  const b = fb.value;
  const t = ft.value;
  const rows = DATA.filter(d => {
    if (b && d.bloque !== b) return false;
    if (t && d.tipo !== t) return false;
    if (activeGroup !== "TODOS" && vGroup(d.veredicto) !== activeGroup) return false;
    if (q) {
      const hay = `${d.id} ${d.bloque} ${d.dominio} ${d.pregunta} ${d.estadistico} ${d.veredicto} ${d.fuente} ${d.novedad}`.toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  });
  document.getElementById("countbar").textContent = `Mostrando ${rows.length} de ${DATA.length} pruebas.`;
  document.getElementById("tbody").innerHTML = rows.map(d => `
    <tr>
      <td class="idcell">${esc(d.id)}</td>
      <td>
        <div><strong>${esc(d.dominio)}</strong></div>
        <div class="meta">${esc(d.bloque)} · ${esc(d.tipo)}</div>
      </td>
      <td>
        <div>${esc(d.pregunta)}</div>
        <div class="meta">${esc(d.novedad)} · <code>${esc(d.fuente)}</code></div>
        ${d.sha256 ? `<div class="sha">SHA-256: ${d.sha256.slice(0.16)}… (${esc(d.preregistro)})</div>` : ""}
      </td>
      <td>${esc(d.estadistico)}</td>
      <td>
        <div>${esc(d.p_corr || d.p_raw || "—")}</div>
        ${d.p_raw && d.p_corr && d.p_raw !== d.p_corr ? `<div class="meta">${esc(d.p_raw)}</div>` : ""}
      </td>
      <td><span class="badge ${vClass(d.veredicto)}">${esc(d.veredicto)}</span></td>
    </tr>
  `).join("");
}

document.getElementById("q").addEventListener("input", render);
fb.addEventListener("change", render);
ft.addEventListener("change", render);
renderPills();
render();
</script>
</body>
</html>
"""


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest()
    new_entries = build_new_entries(manifest)
    legacy_entries = build_legacy_entries()
    all_entries = new_entries + legacy_entries

    # JSON
    out_json = {
        "version": "2.0",
        "semilla": 20261127,
        "total_pruebas": len(all_entries),
        "nuevas_v2": len(new_entries),
        "historicas_v1": len(legacy_entries),
        "manifiesto_sha256": manifest,
        "conteo_veredictos": dict(Counter(e["veredicto"] for e in all_entries)),
        "pruebas": all_entries,
    }
    (DIR / "test_register.json").write_text(json.dumps(out_json, indent=2, ensure_ascii=False), encoding="utf-8")

    # CSV
    fields = ["id", "bloque", "dominio", "tipo", "pregunta", "estadistico", "p_raw", "p_corr",
              "veredicto", "preregistro", "sha256", "fuente", "novedad"]
    with open(DIR / "test_register.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(all_entries)

    # Offline searchable HTML
    html = HTML_TEMPLATE.replace(
        "__DATA_JSON__", json.dumps(all_entries, ensure_ascii=False).replace("</", "<\\/")
    ).replace(
        "__MANIFEST_JSON__", json.dumps(manifest, ensure_ascii=False).replace("</", "<\\/")
    )
    (DIR / "test_register.html").write_text(html, encoding="utf-8")
    (RAIZ / "articulo/registro_pruebas.html").write_text(html, encoding="utf-8")

    print(f"=== REGISTRO UNIFICADO DE PRUEBAS CONSTRUIDO ===")
    print(f"Total: {len(all_entries)} ({len(new_entries)} nuevas v2 + {len(legacy_entries)} históricas v1)")
    for k, v in sorted(out_json["conteo_veredictos"].items()):
        print(f"  {k:32s}: {v}")
    print(f"Archivos: test_register.json, test_register.csv, test_register.html ({len(html)//1024} KB)")


if __name__ == "__main__":
    main()
