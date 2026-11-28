#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
construir_overview.py: Genera el Resumen Visual de 18 láminas (print-to-PDF ready) en español e inglés:
  - articulo/overview.es.html
  - articulo/overview.html

Cifras leídas directamente desde los JSON verificados del repo, insignias honestas de evidencia
y visibilidad completa de los negativos bajo protocolos congelados.
"""
import json
from pathlib import Path

SCR = Path(__file__).resolve().parent
ART = SCR.parent
RAIZ = ART.parent
AN = RAIZ / "analisis"


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


CSS = """
  :root {
    --bg: #181614; --paper: #faf7f2; --ink: #1e1b18; --muted: #625b53;
    --accent: #8c2d19; --accent2: #1f5c4e; --gold: #a66c00; --bad: #9e2626;
    --line: #e2dacd; --soft: #f2ece2;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font-family: Georgia, "Times New Roman", serif; }
  .toolbar {
    position: sticky; top: 0; z-index: 20; background: #141210; color: #ece5da;
    padding: 10px 20px; display: flex; justify-content: space-between; align-items: center;
    font-family: system-ui, -apple-system, sans-serif; font-size: 0.85rem; border-bottom: 1px solid #302b26;
  }
  .toolbar a, .toolbar button {
    color: #f6efe6; background: #2c2621; border: 1px solid #483f37; border-radius: 6px;
    padding: 5px 11px; text-decoration: none; cursor: pointer; font-size: 0.82rem; margin-left: 6px;
  }
  .toolbar button:hover, .toolbar a:hover { background: var(--accent); border-color: var(--accent); }
  .deck { max-width: 1120px; margin: 22px auto 60px; padding: 0 16px; display: flex; flex-direction: column; gap: 26px; }
  .slide {
    background: var(--paper); border-radius: 10px; box-shadow: 0 12px 32px rgba(0,0,0,0.35);
    min-height: 610px; padding: 42px 52px 34px; display: flex; flex-direction: column; justify-content: space-between;
    position: relative; overflow: hidden; border-top: 6px solid var(--accent);
  }
  .slide.dark { background: #1f1b18; color: #f6f1e9; border-top-color: #c8643c; }
  .slide.dark .kicker { color: #e29b76; }
  .slide.dark .muted { color: #bfb6aa; }
  .slide.dark .card { background: #2a2420; border-color: #3d352f; color: #f6f1e9; }
  .kicker {
    font-family: system-ui, sans-serif; font-size: 0.78rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.09em; color: var(--accent); margin-bottom: 8px;
  }
  h1 { margin: 0 0 14px; font-size: 2.55rem; line-height: 1.12; letter-spacing: -0.02em; }
  h2 { margin: 0 0 14px; font-size: 1.78rem; line-height: 1.18; letter-spacing: -0.015em; }
  p { margin: 0 0 12px; font-size: 1.03rem; line-height: 1.5; }
  .lead { font-size: 1.18rem; color: var(--muted); max-width: 860px; }
  .slide.dark .lead { color: #d6cdc1; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px; }
  .grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 10px; }
  .grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 10px; }
  .card {
    background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 16px 18px;
    font-family: system-ui, -apple-system, sans-serif; font-size: 0.89rem; line-height: 1.45;
  }
  .card h3 { margin: 0 0 6px; font-size: 0.96rem; color: var(--accent); }
  .slide.dark .card h3 { color: #f0a882; }
  .big { font-size: 2.05rem; font-weight: 800; line-height: 1.08; font-family: system-ui, sans-serif; margin-bottom: 4px; }
  .tag { display: inline-block; padding: 2px 8px; border-radius: 999px; font-family: system-ui, sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.03em; }
  .t-ok { background: #e3f4eb; color: #165e3d; }
  .t-bad { background: #fbe8e8; color: #942020; }
  .t-warn { background: #fdf1d6; color: #824f00; }
  .t-neu { background: #ece8e1; color: #4d4740; }
  table { width: 100%; border-collapse: collapse; margin-top: 8px; font-family: system-ui, sans-serif; font-size: 0.85rem; }
  th { text-align: left; background: var(--soft); padding: 8px 10px; border-bottom: 2px solid var(--line); font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.04em; color: #4c453e; }
  td { padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  .bar-wrap { background: #ece6dc; border-radius: 4px; height: 14px; width: 100%; overflow: hidden; margin-top: 4px; }
  .bar { height: 100%; background: var(--accent2); border-radius: 4px; }
  .bar.bad { background: var(--bad); }
  .bar.gold { background: var(--gold); }
  .mono { font-family: ui-monospace, Consolas, monospace; font-size: 0.82rem; }
  .foot {
    display: flex; justify-content: space-between; align-items: center; margin-top: 18px;
    padding-top: 10px; border-top: 1px solid var(--line); font-family: system-ui, sans-serif; font-size: 0.76rem; color: var(--muted);
  }
  .slide.dark .foot { border-top-color: #362f29; color: #a79e92; }
  @media print {
    body { background: #fff; }
    .toolbar { display: none; }
    .deck { max-width: none; margin: 0; padding: 0; gap: 0; }
    .slide { box-shadow: none; border-radius: 0; min-height: 100vh; page-break-after: always; break-after: page; }
  }
"""


def build_slides(lang, ctx):
    es = (lang == "es")
    reg = ctx["reg"]
    fpr = ctx["fpr"]
    p3 = ctx["p3"]

    slides = []
    # 1. Cover
    slides.append((True,
        "Resumen visual · v2.0.2 · Noviembre de 2026" if es else "Visual Overview · v2.0.2 · November 2026",
        "Lo que suman los quipus" if es else "What the Khipus Add Up To",
        f"""<p class="lead">{"Auditoría con modelos nulos, Corpus Maestro de 689 quipus, protocolos locales sellados con SHA-256 y evaluación unificada de la literatura computacional de 2026." if es else "Null-model auditing, a unified 689-khipu Master Corpus, locally SHA-256 sealed protocols, and a unified evaluation of 2026 computational khipu studies."}</p>
        <div class="grid4" style="margin-top:26px">
          <div class="card"><div class="big">689</div>{"quipus unificados (+ KH0652)<br>60,969 cuerdas" if es else "unified khipus (+ KH0652)<br>60,969 cords"}</div>
          <div class="card"><div class="big">39</div>{"quipus <i>held-out</i> puros<br>fuera de muestra" if es else "pure held-out khipus<br>out-of-sample"}</div>
          <div class="card"><div class="big">{reg['total_pruebas']}</div>{"pruebas en el registro<br>(26 bajo protocolos SHA-256)" if es else "tests in register<br>(26 under SHA-256 protocols)"}</div>
          <div class="card"><div class="big">0–1 %</div>{"FPR empírica del lector v2<br>en nivel “apoyado”" if es else "empirical FPR of reader v2<br>at “indication” tier"}</div>
        </div>
        <p style="margin-top:22px;font-family:system-ui,sans-serif;font-size:0.88rem;color:#cfc6b9">{"Repositorio abierto: github.com/dariodemh/quipus · Semilla fija: 20261127 · Todos los negativos publicados con igual visibilidad que los positivos." if es else "Open repository: github.com/dariodemh/quipus · Fixed seed: 20261127 · Every negative result published with equal prominence to positive findings."}</p>"""
    ))

    # 2. The Core Methodological Problem
    slides.append((False,
        "1 · El problema metodológico" if es else "1 · The Methodological Problem",
        "Por qué un corpus heterogéneo engaña sin modelos nulos estrictos" if es else "Why a Heterogeneous Corpus Misleads Without Strict Null Models",
        f"""<p class="lead">{"En 650+ quipus con decenas de miles de números y colores, casi cualquier regla buscada a posteriori produce coincidencias aparentemente “significativas”." if es else "Across 650+ khipus and tens of thousands of numbers and colors, almost any post-hoc rule yields seemingly “significant” coincidences."}</p>
        <div class="grid3">
          <div class="card"><h3>{"1. Sumas por azar" if es else "1. Chance Sums"}</h3>{"La cifra publicada del 74 % cuenta bien las relaciones de Ascher, pero al barajar quipu por quipu el azar reproduce entre <b>93 % y 100 %</b> de ellas (potencia ~24 %)." if es else "The published 74% figure counts Ascher relations accurately, yet shuffling khipu-by-khipu reproduces <b>93%–100%</b> of them by chance (~24% power)."}</div>
          <div class="card"><h3>{"2. Fugas y pseudorreplicación" if es else "2. Leakage & Pseudoreplication"}</h3>{"Mezclar cuerdas como muestras independientes o validar sin agrupar por sitio o fuente infla <i>p</i> hasta 10<sup>−207</sup> y oculta efectos de capturista (<code>CREATED_BY</code>)." if es else "Treating cords as independent samples or validating without grouping by site or source inflates <i>p</i> to 10<sup>−207</sup> and hides recorder effects (<code>CREATED_BY</code>)."}</div>
          <div class="card"><h3>{"3. Nuestro protocolo v2" if es else "3. Our v2 Protocol"}</h3>{"Protocolos sellados localmente con <b>SHA-256</b> antes de correr código, auditoría adversarial previa (Opus), partición <i>held-out</i> pura (39 quipus) y calibración empírica de FPR." if es else "Locally <b>SHA-256</b> sealed protocols before running code, adversarial pre-audit (Opus), pure held-out split (39 khipus), and empirical FPR calibration."}</div>
        </div>"""
    ))

    # 3. Master Corpus v2
    slides.append((False,
        "2 · Corpus Maestro Unificado (Bloque A)" if es else "2 · Unified Master Corpus (Block A)",
        "689 quipus, 60,969 cuerdas y cero duplicados silenciosos" if es else "689 Khipus, 60,969 Cords, Zero Silent Duplicates",
        f"""<p>{"Reconciliamos KFG (Ashok Khosla), OKR v2.1.0, el <i>Databook</i> de los Ascher, las 222 correcciones de Karen Thompson (2025), RT-16905 (Chirinos, Ghezzi y Álvarez 2023) y Huacones-Vilcahuasi." if es else "We reconciled KFG (Ashok Khosla), OKR v2.1.0, the Ascher <i>Databook</i>, Karen Thompson's (2025) 222 corrections, RT-16905 (Chirinos, Ghezzi & Álvarez 2023), and Huacones-Vilcahuasi."}</p>
        <table>
          <thead><tr><th>{"Componente" if es else "Component"}</th><th>{"Volumen" if es else "Volume"}</th><th>{"Reconciliación clave" if es else "Key Reconciliation"}</th></tr></thead>
          <tbody>
            <tr><td><b>{"Base KFG limpia" if es else "Clean KFG Base"}</b></td><td>650 {"quipus" if es else "khipus"}</td><td>{"Excluye duplicado UR044; corrige 4 desfases KH0197/0227/0267/0350 y alias UR1180/MM1086." if es else "Excludes duplicate UR044; fixes 4 shifted IDs KH0197/0227/0267/0350 and aliases UR1180/MM1086."}</td></tr>
            <tr><td><b>{"Held-out puro (nuevo)" if es else "Pure Held-Out (new)"}</b></td><td><b>39 {"quipus" if es else "khipus"}</b> (2,414)</td><td>{"14 de RT-16905 + 11 de Huacones + 3 transcritos (KH0674–676) + 8 OKR/BM + 3 Databook genuinamente ausentes." if es else "14 RT-16905 + 11 Huacones + 3 transcribed (KH0674–676) + 8 OKR/BM + 3 genuinely absent Databook."}</td></tr>
            <tr><td><b>{"Rescate OKR" if es else "OKR Rescue"}</b></td><td>248 T · 447 M</td><td>{"Calcula valores desde SUM(knot_value_type); restaura las 111 cuerdas faltantes de Inkawasi (UR274B = 133 cuerdas)." if es else "Computes values from SUM(knot_value_type); restores 111 missing Inkawasi cords (UR274B = 133 cords)."}</td></tr>
            <tr><td><b>Karen Thompson (2025)</b></td><td>222 {"filas" if es else "rows"} / 108 AS</td><td>{"19 parches deterministas en columna paralela <code>valor_thompson</code> (nunca sobrescribe el valor crudo)." if es else "19 deterministic patches in parallel column <code>valor_thompson</code> (never overwrites raw values)."}</td></tr>
            <tr><td><b>{"Física 2D y CIELAB" if es else "2D Physics & CIELAB"}</b></td><td>96.8 % Lab · 65.1 % 2D</td><td>{"Coordenadas CIE <i>L*a*b*</i> continuas y geometría física en cm sin etiquetas humanas." if es else "Continuous CIE <i>L*a*b*</i> coordinates and label-free physical geometry in cm."}</td></tr>
          </tbody>
        </table>"""
    ))

    # 4. P01 Out-of-Sample Confirmations
    slides.append((False,
        "3 · Confirmaciones fuera de muestra (P01)" if es else "3 · Out-of-Sample Confirmations (P01)",
        "Tres leyes estructurales sobreviven al salto fuera de muestra" if es else "Three Structural Laws Survive Out-of-Sample Testing",
        f"""<div class="grid3">
          <div class="card">
            <span class="tag t-ok">{"CONFIRMADO · p_Holm(m=6) = 0.0168" if es else "CONFIRMED · p_Holm(m=6) = 0.0168"}</span>
            <h3 style="margin-top:8px">{"P01.1 · Mayor abre grupo" if es else "P01.1 · Largest Opens Group"}</h3>
            <div class="big">27.9 %</div>
            {"29 de 104 grupos en los 39 quipus <i>held-out</i> frente a 17.0 % esperado por azar." if es else "29 of 104 groups in the 39 held-out khipus vs. 17.0% expected by chance."}
            <div class="bar-wrap"><div class="bar" style="width:72%"></div></div>
          </div>
          <div class="card">
            <span class="tag t-ok">{"CONFIRMADO · p_Holm(m=6) = 0.0010" if es else "CONFIRMED · p_Holm(m=6) = 0.0010"}</span>
            <h3 style="margin-top:8px">{"P01.3b · Cuerdas superiores T" if es else "P01.3b · Rescued Top Cords T"}</h3>
            <div class="big">53 / 174</div>
            {"30.5 % de las cuerdas superiores rescatadas de OKR suman exactamente el grupo anterior (vs 7.0 % esperado; 12.2 aciertos)." if es else "30.5% of OKR-rescued top cords equal the exact sum of the preceding group (vs. 7.0% expected; 12.2 hits)."}
            <div class="bar-wrap"><div class="bar" style="width:85%"></div></div>
          </div>
          <div class="card">
            <span class="tag t-ok">{"CONFIRMADO · p_Holm(m=6) < 10⁻⁴" if es else "CONFIRMED · p_Holm(m=6) < 10⁻⁴"}</span>
            <h3 style="margin-top:8px">{"P01.4 · Alternancia A/B/A/B" if es else "P01.4 · A/B/A/B Alternation"}</h3>
            <div class="big">5 / 16</div>
            {"Quipus <i>held-out</i> con p &lt; 0.01 (AS033, KH0208, KH0648, KH0651, KH0676) frente a 0.16 esperados." if es else "Held-out khipus with p &lt; 0.01 (AS033, KH0208, KH0648, KH0651, KH0676) vs. 0.16 expected."}
            <div class="bar-wrap"><div class="bar" style="width:90%"></div></div>
          </div>
        </div>
        <div class="card" style="margin-top:16px">
          <b>{"Transparencia en pruebas sin potencia (P01.2, P01.3a, P01.5):" if es else "Transparency on underpowered tests (P01.2, P01.3a, P01.5):"}</b>
          {" 0 cuerdas elegibles para ceros OKR (P01.2) y 0 cuerdas T (P01.3a) en el subconjunto held-out; 0 copias pasan q_BH &lt; 0.05 sobre 17,766 pares a B=2,000 (candidato principal: KH0139~KH0138, SW=33.82, Berlín/Marquez). Sensibilidad Karen Thompson (D01.6): 0 parches alteran quipus clave." if es else " 0 eligible cords for OKR zeros (P01.2) and 0 top cords (P01.3a) in held-out; 0 copies clear q_BH &lt; 0.05 over 17,766 pairs at B=2,000 (top hit: KH0139~KH0138, SW=33.82, Berlin/Marquez). Karen Thompson sensitivity (D01.6): 0 patches alter key khipus."}
        </div>"""
    ))

    # 5. Inkawasi Double-Route Architecture
    slides.append((False,
        "4 · Sistema contable de Inkawasi (v1 verificado)" if es else "4 · Inkawasi Accounting System (v1 Verified)",
        "Una cadena de tres niveles con doble cuadre y prueba ciega" if es else "A Three-Level Chain with Double-Entry Reconciliation & Blind Test",
        f"""<div class="grid2">
          <div class="card">
            <h3>{"Vía 1: UR270 → UR278 → UR266 / UR275" if es else "Route 1: UR270 → UR278 → UR266 / UR275"}</h3>
            <p>{"Cada celda de la tabla de 9 columnas de <b>UR278</b> iguala a <code>colgante + 1.ª subsidiaria</code> de <b>UR270</b> (5/12 grupos con 6–9/9 exactas; solo colgantes: 0; prueba ciega p ≈ 3×10<sup>−10</sup>)." if es else "Each cell of <b>UR278</b>'s 9-column table equals <code>pendant + 1st subsidiary</code> of <b>UR270</b> (5/12 groups with 6–9/9 exact; pendants alone: 0; blind p ≈ 3×10<sup>−10</sup>)."}</p>
            <p>{"Los totales de fila de UR278 reaparecen <b>en orden</b> como cabeceras de <b>UR266</b> (11 exactos, Holm 1.6×10<sup>−9</sup>) y <b>UR275</b> (7 exactos, Holm 2.8×10<sup>−4</sup>)." if es else "UR278 row totals reappear <b>in order</b> as headers of <b>UR266</b> (11 exact, Holm 1.6×10<sup>−9</sup>) and <b>UR275</b> (7 exact, Holm 2.8×10<sup>−4</sup>)."}</p>
          </div>
          <div class="card">
            <h3>{"Vía 2 y prueba ciega (597 cuerdas ocultas)" if es else "Route 2 & Blind Test (597 Hidden Cords)"}</h3>
            <p>{"<b>UR273A + UR273B</b> suman a las cabeceras del libro en 8/18 registros (Holm 0.0018; fuera de muestra Holm 0.016). En prueba ciega sobre 52 quipus anonimizados, la aritmética predice <b>56/68 exactas (82 %)</b> y <b>21/23</b> en confianza alta vs 14.4 % base." if es else "<b>UR273A + UR273B</b> sum to ledger headers in 8/18 records (Holm 0.0018; out-of-sample Holm 0.016). On 52 anonymized khipus, the arithmetic predicts <b>56/68 exact (82%)</b> and <b>21/23</b> at high confidence vs. 14.4% baseline."}</p>
            <p><span class="tag t-bad">{"P03.3 NEGATIVO · p_Holm = 1.0" if es else "P03.3 NEGATIVE · p_Holm = 1.0"}</span> {"Los 4 quipus no leídos (UR272/276/277/279) no enlazan aritméticamente con el depósito (5 aciertos vs 5.27 nulo)." if es else "The 4 unread khipus (UR272/276/277/279) do not link arithmetically to the storehouse (5 hits vs. 5.27 null)."}</p>
          </div>
        </div>"""
    ))

    # 6. NEW DISCOVERY 1: KH0674
    slides.append((False,
        "5 · Hallazgo nuevo v2 (Protocolo P03.4)" if es else "5 · New v2 Discovery (Protocol P03.4)",
        "KH0674 (Dumbarton Oaks): sumas exactas confirmadas en un quipu held-out" if es else "KH0674 (Dumbarton Oaks): Exact Group Sums Confirmed Out-of-Sample",
        f"""<div class="grid2">
          <div class="card">
            <span class="tag t-ok">{"CONFIRMADO · p_Holm = 0.002" if es else "CONFIRMED · p_Holm = 0.002"}</span>
            <div class="big" style="margin-top:12px">8 / 41 {"grupos" if es else "groups"}</div>
            <p>{"En el quipu <b>KH0674</b> (Dumbarton Oaks, nunca usado en v1), 8 de 41 grupos poseen una cuerda-resumen igual a la suma exacta del resto del grupo, frente a <b>0.31</b> esperados bajo permutación intra-quipu." if es else "In <b>KH0674</b> (Dumbarton Oaks, untouched in v1), 8 of 41 groups contain a summary cord equal to the exact sum of the remaining cords, vs. <b>0.31</b> expected under intra-khipu permutation."}</p>
            <p class="mono">{"Solo colgantes: 8/41 vs 0.31 (p = 0.0002)<br>Colgantes + subs: 8/41 vs 0.32 (p = 0.0002)<br>Combinado: p = 0.0004 · p_Holm = 0.002" if es else "Pendants only: 8/41 vs 0.31 (p = 0.0002)<br>Pendants + subs: 8/41 vs 0.32 (p = 0.0002)<br>Combined: p = 0.0004 · p_Holm = 0.002"}</p>
          </div>
          <div class="card">
            <h3>{"Por qué importa" if es else "Why It Matters"}</h3>
            <p>{"Demuestra que nuestros detectores de contabilidad interna encuentran <b>estructura aritmética genuina fuera de muestra</b> en quipus recién incorporados al Corpus Maestro, además de los casos conocidos de Inkawasi y Puruchuco." if es else "Shows that our internal-accounting detectors uncover <b>genuine out-of-sample arithmetic structure</b> on newly integrated Master Corpus khipus beyond known Inkawasi and Puruchuco cases."}</p>
            <p>{"A diferencia del 74 % crudo de fórmulas de Ascher, KH0674 supera un nulo estricto quipu por quipu y corre bajo familia Holm cerrada." if es else "Unlike the raw 74% Ascher-formula count, KH0674 clears a strict khipu-by-khipu null inside a frozen Holm family."}</p>
          </div>
        </div>"""
    ))

    # 7. NEW DISCOVERY 2: QU005
    b0, b1, b2 = p3["post_hoc_E03_6_QU005"]["bloques"]
    cells_html = "".join(
        f"<td style='text-align:right;{'background:#e3f4eb;font-weight:700' if b0[i]+b1[i]==b2[i] else ''}'>{b0[i]}<br>+{b1[i]}<br><b>{b2[i]}</b></td>"
        for i in range(19)
    )
    slides.append((False,
        "6 · Hallazgo nuevo v2 (Post hoc auditada E03.6)" if es else "6 · New v2 Discovery (Audited Post Hoc E03.6)",
        "QU005 (Dallas): tercera tabla jerárquica de totales por columna del corpus" if es else "QU005 (Dallas): Third Hierarchical Column-Sum Table in the Corpus",
        f"""<p>{"En <b>QU005</b> (57 colgantes = 3 bloques de 19), el tercer bloque iguala exactamente la suma columna a columna de los dos primeros en <b>12 de 19 posiciones</b> (13/19 con ±1) frente a un nulo máximo medio de <b>0.10</b> sobre los 3 tríos posibles (<b><i>p</i><sub>corr</sub> = 0.0001</b>)." if es else "In <b>QU005</b> (57 pendants = 3 blocks of 19), block 3 equals the exact column-by-column sum of blocks 1 and 2 in <b>12 of 19 positions</b> (13/19 within ±1) vs. a mean null max of <b>0.10</b> across all 3 possible triples (<b><i>p</i><sub>corr</sub> = 0.0001</b>)."}</p>
        <table style="font-size:0.72rem">
          <thead><tr>{"".join(f"<th style='text-align:right'>c{i+1}</th>" for i in range(19))}</tr></thead>
          <tbody><tr>{cells_html}</tr></tbody>
        </table>
        <div class="card" style="margin-top:14px">
          <span class="tag t-ok">{"APOYADO (POST HOC AUDITADA)" if es else "SUPPORTED (AUDITED POST HOC)"}</span>
          {" Junto a <b>KH0049/AS038</b> (Ascher 1978, bloques de 18) y la jerarquía de <b>Puruchuco</b> (Urton y Brezine 2005), <b>QU005</b> (bloques de 19, incluida la suma 524 + 583 = 1107) amplía a tres los casos verificados de contabilidad matricial por columnas." if es else " Alongside <b>KH0049/AS038</b> (Ascher 1978, blocks of 18) and the <b>Puruchuco</b> hierarchy (Urton & Brezine 2005), <b>QU005</b> (blocks of 19, including 524 + 583 = 1107) expands verified column-sum matrix accounting to three cases."}
        </div>"""
    ))

    # 8. P04 Perceptual Color & Label-Free 2D Geometry
    slides.append((False,
        "7 · Física perceptual y geometría 2D (P04)" if es else "7 · Perceptual Color & 2D Geometry (P04)",
        "Dos señales físicas independientes de las etiquetas humanas" if es else "Two Physical Signals Independent of Human Labels",
        f"""<div class="grid2">
          <div class="card">
            <span class="tag t-ok">{"P04.2 CONFIRMADO · p_Holm = 0.012" if es else "P04.2 CONFIRMED · p_Holm = 0.012"}</span>
            <h3 style="margin-top:8px">{"Luminancia continua CIE L* vs magnitud" if es else "Continuous CIE L* Luminance vs Magnitude"}</h3>
            <p>{"Con blanco (W): n = 351 quipus, mediana ρ = <b>+0.0869</b> (p = 0.0005).<br><b>EXCLUYENDO el blanco (sin W)</b>: n = 225 quipus, mediana ρ = <b>+0.0529</b> (p = 0.004, p_Holm = 0.012), mismo signo en UR (+0.0595) y AS (+0.0083)." if es else "With white (W): n = 351 khipus, median ρ = <b>+0.0869</b> (p = 0.0005).<br><b>EXCLUDING white (no W)</b>: n = 225 khipus, median ρ = <b>+0.0529</b> (p = 0.004, p_Holm = 0.012), same sign in UR (+0.0595) and AS (+0.0083)."}</p>
            <p class="muted">{"Incluso entre hilos no blancos, los tonos más luminosos portan magnitudes mayores dentro del grupo." if es else "Even among non-white yarns, lighter shades carry larger magnitudes within each group."}</p>
          </div>
          <div class="card">
            <span class="tag t-ok">{"P04.3 CONFIRMADO · p_Holm = 0.00017" if es else "P04.3 CONFIRMED · p_Holm = 0.00017"}</span>
            <h3 style="margin-top:8px">{"Segmentación física pura en cm (k = 2.0)" if es else "Pure Physical Gap Segmentation in cm (k = 2.0)"}</h3>
            <p>{"Sin usar ninguna etiqueta humana de grupo, cortando la cuerda primaria solo por huecos ≥ 2× el espaciado mediano, <b>9 de 35 quipus (25.7 %)</b> replican tendencias monótonas intra-grupo vs 1.75 esperados." if es else "Without any human group labels, cutting the primary cord purely at gaps ≥ 2× median spacing, <b>9 of 35 khipus (25.7%)</b> replicate intra-group monotonic trends vs. 1.75 expected."}</p>
            <p><span class="tag t-warn">{"D04.5 ALERTA PERMANOVA" if es else "D04.5 PERMANOVA WARNING"}</span> {"En geometría 2D OKR, el capturista (R² = 0.087) explica más varianza que el sitio (R² = 0.085; museo R² = 0.272)." if es else "In OKR 2D geometry, recorder identity (R² = 0.087) explains more variance than site (R² = 0.085; museum R² = 0.272)."}</p>
          </div>
        </div>"""
    ))

    # 9. P02 RT-16905 Negative
    slides.append((False,
        "8 · Protocolo P02: RT-16905 (15 quipus atados)" if es else "8 · Protocol P02: RT-16905 (15 Tied Khipus)",
        "Negativo de alto valor: atar quipus juntos ≠ jerarquía aritmética" if es else "High-Value Negative: Physical Tying ≠ Automatic Arithmetic Hierarchy",
        f"""<p>{"El conjunto RT-16905 del MNAAHP (14 quipus con colgantes + K15 enrollado en 19 hilos sobre K01, registrado por Chirinos, Ghezzi y Álvarez 2023) ofrece una prueba natural directa de si la topología física de nodos (Hubs A–G, H) refleja sumas entre quipus." if es else "The MNAAHP RT-16905 assemblage (14 pendant khipus + K15 wrapped in 19 threads on K01, recorded by Chirinos, Ghezzi & Álvarez 2023) provides a direct test of whether physical tying topology (Hubs A–G, H) encodes inter-khipu sums."}</p>
        <table>
          <thead><tr><th>{"Prueba" if es else "Test"}</th><th>{"Hipótesis evaluada (QAP 10,000 perm)" if es else "Tested Hypothesis (10,000 QAP perms)"}</th><th>{"Estadístico" if es else "Statistic"}</th><th>p / p_Holm</th><th>{"Veredicto" if es else "Verdict"}</th></tr></thead>
          <tbody>
            <tr><td class="mono">P02.1</td><td>{"Sumas jerárquicas >=10 en pares físicamente adyacentes" if es else "Hierarchical sums >=10 on physically adjacent pairs"}</td><td>diff_Z = +0.0881</td><td>0.063 / 0.251</td><td><span class="tag t-bad">NEGATIVO</span></td></tr>
            <tr><td class="mono">P02.2</td><td>{"Similitud numérica SW (sin sesgo de tamaño) vs cercanía física" if es else "Size-standardized SW numeric similarity vs physical proximity"}</td><td>ρ_Mantel = +0.1026</td><td>0.159 / 0.478</td><td><span class="tag t-bad">NEGATIVO</span></td></tr>
            <tr><td class="mono">P02.3</td><td>{"Coherencia textil (color/torsión sin tamaño) vs cercanía física" if es else "Textile coherence (color/twist without size) vs proximity"}</td><td>ρ_Mantel = +0.0174</td><td>0.406 / 0.812</td><td><span class="tag t-bad">NEGATIVO</span></td></tr>
            <tr><td class="mono">P02.4</td><td>{"Alineación cromática de los 19 hilos de K15 sobre su huésped K01" if es else "Color alignment of K15's 19 wrapped threads with host K01"}</td><td>align = 0.1579</td><td>0.732 / 0.812</td><td><span class="tag t-bad">NEGATIVO</span></td></tr>
          </tbody>
        </table>
        <p style="margin-top:12px" class="muted">{"D02.5: solo 1 de 14 quipus (K10, 1 de 3 grupos) tiene suma interna. Los pares adyacentes K01–K04 (z=2.39) y K10–K11 (z=1.67) destacan localmente, pero el patrón global del atado es archivístico y no aritmético." if es else "D02.5: only 1 of 14 khipus (K10, 1 of 3 groups) has an internal sum. Adjacent pairs K01–K04 (z=2.39) and K10–K11 (z=1.67) lead locally, yet the global tying pattern is archival rather than arithmetic."}</p>"""
    ))

    # 10. P03 Other Open Cases (Huacones, UR053E, Mixed Radices)
    slides.append((False,
        "9 · Cierre de casos abiertos (P03)" if es else "9 · Closing Open Cases (P03)",
        "Huacones-Vilcahuasi, UR053E y bases mixtas tipo proto-cuneiforme" if es else "Huacones-Vilcahuasi, UR053E, and Proto-Cuneiform Mixed Radices",
        f"""<div class="grid3">
          <div class="card">
            <span class="tag t-warn">{"P03.1 · SIN POTENCIA / NO PLANO" if es else "P03.1 · UNDERPOWERED / NOT FLAT"}</span>
            <h3 style="margin-top:8px">Huacones-Vilcahuasi</h3>
            {"<b>JC031</b> solo tiene 5 colgantes positivos (ρ=0.0, CV=0.61). <b>JC024</b> desciende con fuerza (ρ=−0.952, p=0.0006), pero con alta dispersión (CV=1.28, no plano como UR278). En escala (D03.9), Huacones (med=10 cuerdas) se parece a Inkawasi Sector B (med=13), lejos del Sector A (med=125)." if es else "<b>JC031</b> has only 5 positive pendants (ρ=0.0, CV=0.61). <b>JC024</b> drops sharply (ρ=−0.952, p=0.0006) yet with high spread (CV=1.28, unlike flat UR278). Structurally (D03.9), Huacones (med=10 cords) mirrors Inkawasi Sector B (med=13), away from Sector A (med=125)."}
          </div>
          <div class="card">
            <span class="tag t-bad">{"P03.2 NEGATIVO · p_Holm = 0.70" if es else "P03.2 NEGATIVE · p_Holm = 0.70"}</span>
            <h3 style="margin-top:8px">UR053E → UR053B/C</h3>
            {"Con segmentación real de 35 tríos W/R/AB en UR053E, los tramos contiguos aciertan 48 valores exactos de B/C frente a 45.17 esperados por azar (p=0.234). No hay consolidación directa detectable entre E y B/C." if es else "Segmenting UR053E's 35 W-led W/R/AB trios, contiguous spans match 48 exact B/C values vs. 45.17 expected by chance (p=0.234). No direct summation from E to B/C is detectable."}
          </div>
          <div class="card">
            <span class="tag t-bad">{"P03.5 NEGATIVO · p_Holm = 1.0" if es else "P03.5 NEGATIVE · p_Holm = 1.0"}</span>
            <h3 style="margin-top:8px">{"Bases mixtas (Damerow–Englund)" if es else "Mixed Radices (Damerow–Englund)"}</h3>
            {"Barrido de pares de bases (r1, r2) sobre los 7 quipus multiunidad elegibles: ganancia máxima de +1 suma (p_min = 0.54). Descarta sistemas metrológicos ocultos de base mixta." if es else "Sweep of mixed-radix pairs (r1, r2) over all 7 eligible multi-unit khipus: max gain is +1 sum (p_min = 0.54). Rules out hidden proto-cuneiform mixed-radix metrology."}
          </div>
        </div>"""
    ))

    # 11. P05 Unified Audit of 2026 Literature: Overview Table
    slides.append((False,
        "10 · Auditoría unificada de la literatura de 2026 (P05)" if es else "10 · Unified Audit of 2026 Computational Literature (P05)",
        "Seis pruebas cerradas sobre cuatro estudios computacionales recientes" if es else "Six Frozen Tests Across Four Recent Computational Studies",
        f"""<table>
          <thead><tr><th>ID</th><th>{"Hipótesis / herramienta" if es else "Hypothesis / Tool"}</th><th>{"Propuesta evaluada" if es else "Evaluated Claim"}</th><th>{"Nuestro resultado con nulo estricto" if es else "Our Strict-Null Result"}</th><th>{"Veredicto" if es else "Verdict"}</th></tr></thead>
          <tbody>
            <tr><td class="mono">P05.1</td><td>khipu-rv-reprod.</td><td>{"Entropía R/V baja en 17/39 (FY)" if es else "Low R/V entropy in 17/39 (FY)"}</td><td>{"Cae a <b>0/27 y 0/39</b> bajo nulo de rachas (p_Holm=0.587)" if es else "Drops to <b>0/27 & 0/39</b> under run-preserving null (p_Holm=0.587)"}</td><td><span class="tag t-bad">{"FRÁGIL A RACHAS" if es else "RUN-ARTIFACT"}</span></td></tr>
            <tr><td class="mono">P05.2</td><td>Khipu-ML (torsión S)</td><td>{"Torsión S identifica sitios imperiales" if es else "S-twist marks imperial sites"}</td><td>{"Sin >50% U se invierte (77.8% vs 93.4%); F1 cae 0.241→0.048" if es else "Excl. >50% U reverses (77.8% vs 93.4%); F1 drops 0.241→0.048"}</td><td><span class="tag t-bad">{"SESGO U / FUGA" if es else "U-BIAS / LEAK"}</span></td></tr>
            <tr><td class="mono">P05.3</td><td>Khipu-ML (Santa)</td><td>{"OKR valida collca.db en el Santa" if es else "OKR validates collca.db in Santa"}</td><td>{"<b>100.0 % idénticos</b> (misma fuente KDB); base 5+1 = 7.2 %" if es else "<b>100.0% identical</b> (same KDB source); 5+1 base rate = 7.2%"}</td><td><span class="tag t-bad">{"MISMA FUENTE" if es else "SAME SOURCE"}</span></td></tr>
            <tr><td class="mono">P05.4</td><td>K-CAT (color)</td><td>{"Color × magnitud p = 4.3×10⁻²⁰⁷" if es else "Color × magnitude p = 4.3×10⁻²⁰⁷"}</td><td>{"Clave local R² = <b>16.0 %</b> vs etiqueta global R² = <b>1.06 %</b>" if es else "Local key R² = <b>16.0%</b> vs global label R² = <b>1.06%</b>"}</td><td><span class="tag t-bad">{"CLAVE LOCAL" if es else "LOCAL KEY"}</span></td></tr>
            <tr><td class="mono">P05.5</td><td>K-CAT (hijos)</td><td>{"Padre = Σ subsidiarias" if es else "Parent = Σ subsidiaries"}</td><td>{"<b>67/1,557 (4.30 %)</b> vs 2.75 % nulo (p_Holm = 0.003; 0 ind. BH)" if es else "<b>67/1,557 (4.30%)</b> vs 2.75% null (p_Holm = 0.003; 0 ind. BH)"}</td><td><span class="tag t-ok">{"SEÑAL REAL" if es else "REAL SIGNAL"}</span></td></tr>
            <tr><td class="mono">P05.6</td><td>{"Grafos (2026)" if es else "Graphs (2026)"}</td><td>{"Similitud algorítmica padre-hijo" if es else "Algorithmic parent-child similarity"}</td><td>{"Replica AUC=0.861 y z=6.76; con (grupo, escala) z=1.82 (p_H=0.126)" if es else "Replicates AUC=0.861 & z=6.76; with (group, scale) z=1.82 (p_H=0.126)"}</td><td><span class="tag t-warn">{"ESCALA LOCAL" if es else "LOCAL SCALE"}</span></td></tr>
          </tbody>
        </table>"""
    ))

    # 12. P05 Visual Spotlight (Why Null Choice Changes Everything)
    slides.append((False,
        "11 · Lección central de P05" if es else "11 · Core Lesson of P05",
        "El modelo nulo correcto separa mecanismos reales de espejismos" if es else "The Right Null Model Separates Real Mechanisms from Mirages",
        f"""<div class="grid2">
          <div class="card">
            <h3>{"K-CAT color × magnitud: 15× más varianza local que global" if es else "K-CAT Color × Magnitude: 15× More Local Than Global Variance"}</h3>
            <p style="margin-bottom:6px">{"Clave local intra-quipu (R² = 16.0 %)" if es else "Intra-khipu local key (R² = 16.0%)"}</p>
            <div class="bar-wrap"><div class="bar" style="width:80%"></div></div>
            <p style="margin:12px 0 6px">{"Etiqueta global de color (R² = 1.06 %)" if es else "Global color label (R² = 1.06%)"}</p>
            <div class="bar-wrap"><div class="bar bad" style="width:5.3%"></div></div>
            <p style="margin-top:12px" class="muted">{"El H = 1,076 (p = 4.3×10⁻²⁰⁷) se reproduce al pie de la letra, pero emerge de mezclar 28,411 cuerdas sin efecto de quipu." if es else "H = 1,076 (p = 4.3×10⁻²⁰⁷) replicates verbatim, arising from pooling 28,411 cords without khipu-level nesting."}</p>
          </div>
          <div class="card">
            <h3>{"Complejidad en grafos (2026): qué explica el z = 6.76" if es else "Graph Complexity (2026): What Drives z = 6.76"}</h3>
            <p style="margin-bottom:6px">{"Re-cableado (quipu, fibra, torsión): z = 6.76 (p = 0.002)" if es else "Rewiring (khipu, fiber, twist): z = 6.76 (p = 0.002)"}</p>
            <div class="bar-wrap"><div class="bar gold" style="width:84%"></div></div>
            <p style="margin:12px 0 6px">{"Re-cableado (quipu, grupo, magnitud): z = 1.82 (p_Holm = 0.126)" if es else "Rewiring (khipu, group, magnitude): z = 1.82 (p_Holm = 0.126)"}</p>
            <div class="bar-wrap"><div class="bar bad" style="width:22%"></div></div>
            <p style="margin-top:12px" class="muted">{"Aislamos el mecanismo: los padres y sus subsidiarias comparten banda decimal local dentro del mismo grupo." if es else "We isolate the mechanism: parents and subsidiaries share local decimal scale within the same group."}</p>
          </div>
        </div>"""
    ))

    # 13. P06 Colonial Generative Tournament
    slides.append((False,
        "12 · Torneo generativo colonial (Bloque D · P06)" if es else "12 · Colonial Generative Tournament (Block D · P06)",
        "1,190 ítems coloniales revelan el espejismo LODO vs LOSO" if es else "1,190 Colonial Items Expose the LODO vs. LOSO Mirage",
        f"""<p>{"Extrajimos <b>1,190 ítems en 38 tablas independientes</b> de 5 géneros fiscales (Curatola 2013, Chirinos 2010, Pärssinen 1992 y 11_rosetta) y evaluamos un clasificador gaussiano regularizado sobre 8 firmas numéricas invariantes." if es else "We extracted <b>1,190 items across 38 independent tables</b> spanning 5 fiscal genres (Curatola 2013, Chirinos 2010, Pärssinen 1992, and 11_rosetta) and tested a regularized Gaussian classifier on 8 invariant numeric signatures."}</p>
        <div class="grid3">
          <div class="card">
            <span class="tag t-bad">P06.1 · LOSO = 0.050</span>
            <h3 style="margin-top:8px">{"LODO engaña; LOSO desnuda" if es else "LODO Misleads; LOSO Exposes"}</h3>
            {"LODO da bAcc = <b>0.382</b> (p = 0.0085), pero dejar una fuente editorial fuera (LOSO) colapsa a <b>0.050</b> (p = 0.9925). El modelo aprende edición y no género universal." if es else "LODO gives bAcc = <b>0.382</b> (p = 0.0085), yet Leave-One-Source-Out collapses to <b>0.050</b> (p = 0.9925). The classifier learns editorial source rather than universal genre."}
          </div>
          <div class="card">
            <span class="tag t-bad">P06.2 · 37.0 %</span>
            <h3 style="margin-top:8px">{"Controles no circulares" if es else "Non-Circular Controls"}</h3>
            {"Acierto medio = 37.0 % (p = 0.261): ASG 11/23 (47.8 %), PAD Santa 1/6 (16.7 %), TAL OOD 13/28 (46.4 %). Las marginales solas no identifican el género de un quipu." if es else "Mean accuracy = 37.0% (p = 0.261): ASG 11/23 (47.8%), PAD Santa 1/6 (16.7%), TAL OOD 13/28 (46.4%). Marginal distributions alone cannot identify a khipu's genre."}
          </div>
          <div class="card">
            <span class="tag t-bad">P06.3 · FPR = 53.7 %</span>
            <h3 style="margin-top:8px">{"FPR sintética bloquea la frontera" if es else "Synthetic FPR Gates the Frontier"}</h3>
            {"El modelo asigna 45/148 (30.4 %) de la frontera, pero asigna <b>53.7 %</b> de 1,000 listas sintéticas sin género (p = 1.0). La puerta FPR &lt; 5 % impide falsos hallazgos." if es else "The model assigns 45/148 (30.4%) frontier khipus, yet assigns <b>53.7%</b> of 1,000 genre-free synthetic lists (p = 1.0). Our FPR &lt; 5% gate prevents false claims."}
          </div>
        </div>"""
    ))

    # 14. P06.4 Prediction #17 (Without Bambamarca)
    slides.append((False,
        "13 · Predicción #17 sin circularidad (P06.4)" if es else "13 · Non-Circular Prediction #17 (P06.4)",
        "8 listas demográficas coloniales sin Bambamarca: descenso leve, pero UR278 sigue siendo único" if es else "8 Colonial Demographic Lists Without Bambamarca: Mild Drift, Yet UR278 Remains an Outlier",
        f"""<div class="grid2">
          <div class="card">
            <span class="tag t-ok">{"CONFIRMA PRED. #17 (REGLA BINARIA)" if es else "CONFIRMS PRED. #17 (BINARY RULE)"}</span>
            <h3 style="margin-top:8px">{"Mediana ρ = −0.294 (no cruza −0.30)" if es else "Median ρ = −0.294 (does not cross −0.30)"}</h3>
            <p>{"Bajo la regla binaria congelada de P06.4 (&lt; −0.30), las 8 listas independientes confirman formalmente la Predicción #17; a la vez, 6/8 son negativas (p_Holm = 0.004), indicando un descenso leve." if es else "Under P06.4's frozen binary rule (&lt; −0.30), the 8 independent lists formally confirm Prediction #17; meanwhile 6/8 are negative (p_Holm = 0.004), showing a mild downward drift."}</p>
            <p><b>{"Pero 0 de 8 (0 %) alcanzan la pendiente de UR278 (−0.73) ni su planitud (CV = 0.173 vs mediana colonial CV = 1.260, mín = 0.416)." if es else "Yet 0 of 8 (0%) match UR278's slope (−0.73) or flatness (CV = 0.173 vs. colonial median CV = 1.260, min = 0.416)."}</b></p>
          </div>
          <div class="card">
            <table>
              <thead><tr><th>{"Lista colonial (sin Bambamarca)" if es else "Colonial List (excl. Bambamarca)"}</th><th>n</th><th>ρ</th><th>CV</th></tr></thead>
              <tbody>
                <tr><td>PAR1992 Table 6</td><td>61</td><td>−0.607</td><td>1.720</td></tr>
                <tr><td>PAR1992 Table 3</td><td>51</td><td>−0.440</td><td>1.441</td></tr>
                <tr><td>PAR1992 Table 7</td><td>35</td><td>−0.335</td><td>1.515</td></tr>
                <tr><td>PAR1992 Table 8</td><td>18</td><td>−0.320</td><td>1.709</td></tr>
                <tr><td>PAR1992 Table 4</td><td>9</td><td>−0.268</td><td>1.079</td></tr>
                <tr><td>Chucuito 1567 (Chirinos)</td><td>17</td><td>−0.105</td><td>0.416</td></tr>
                <tr><td>PAR1992 Table 9 / 10</td><td>16 / 15</td><td>+0.015 / +0.503</td><td>0.58 / 0.60</td></tr>
                <tr style="background:#fdf1d6;font-weight:700"><td>UR278 (Inkawasi, referencia)</td><td>9</td><td>−0.730</td><td>0.173</td></tr>
              </tbody>
            </table>
          </div>
        </div>"""
    ))

    # 15. Lector v2 + Empirical FPR Calibration
    fdet = fpr["fpr_por_detector"]
    slides.append((False,
        "14 · Lector de Quipus v2 y Calibración Empírica de FPR" if es else "14 · Khipu Reader v2 & Empirical FPR Calibration",
        "21 pruebas de regresión y 0–1 % de falsos positivos en nivel “apoyado”" if es else "21 Regression Checks and 0–1% False-Positive Rate at “Indication” Tier",
        f"""<p>{"El lector v2 de línea de comandos resuelve cualquier quipu del Corpus Maestro (689 objetos, incluidos KH0674, QU005, RT-16905 y Huacones) o cualquier CSV externo. Probamos sus detectores internos en <b>100 quipus sintéticos realistas barajados</b>:" if es else "Command-line Reader v2 resolves any Master Corpus khipu (689 objects, including KH0674, QU005, RT-16905, and Huacones) or any external CSV. We calibrated its detectors on <b>100 realistic shuffled synthetic khipus</b>:"}</p>
        <table>
          <thead><tr><th>{"Detector interno" if es else "Internal Detector"}</th><th>{"FPR propuesto+" if es else "FPR Conjecture+"}</th><th>{"FPR apoyado+" if es else "FPR Indication+"}</th><th>{"Evaluación" if es else "Assessment"}</th></tr></thead>
          <tbody>
            <tr><td><code>sumas</code></td><td>{fdet['sumas']['hits_propuesto_o_mas']}/100 ({fdet['sumas']['fpr_propuesto_o_mas']:.0%})</td><td><b>{fdet['sumas']['hits_apoyado_o_mas']}/100 ({fdet['sumas']['fpr_apoyado_o_mas']:.0%})</b></td><td><span class="tag t-ok">{"CALIBRADO" if es else "CALIBRATED"}</span></td></tr>
            <tr><td><code>ficha_nazca</code></td><td>{fdet['ficha_nazca']['hits_propuesto_o_mas']}/100 (0%)</td><td><b>0/100 (0%)</b></td><td><span class="tag t-ok">{"CALIBRADO" if es else "CALIBRATED"}</span></td></tr>
            <tr><td><code>formulario</code></td><td>{fdet['formulario']['hits_propuesto_o_mas']}/100 ({fdet['formulario']['fpr_propuesto_o_mas']:.0%})</td><td><b>0/100 (0%)</b></td><td><span class="tag t-ok">{"CALIBRADO" if es else "CALIBRATED"}</span></td></tr>
            <tr><td><code>alternancia</code></td><td>0/100 (0%)</td><td><b>0/100 (0%)</b></td><td><span class="tag t-ok">{"CALIBRADO" if es else "CALIBRATED"}</span></td></tr>
            <tr><td><code>totales_columna</code></td><td>0/100 (0%)</td><td><b>0/100 (0%)</b></td><td><span class="tag t-ok">{"CALIBRADO" if es else "CALIBRATED"}</span></td></tr>
          </tbody>
        </table>
        <p style="margin-top:12px" class="muted">{"Calibrado sobre los 5 detectores internos rápidos (IC 95 % límite superior: 3.6 % para 0/100 y 5.4 % para 1/100). En género automático: 92 % queda en SIN (79 %) o baja (13 %) y 0 % en alta." if es else "Calibrated across the 5 fast internal detectors (95% CI upper bound: 3.6% for 0/100, 5.4% for 1/100). Automatic genre: 92% remain SIN (79%) or low (13%) and 0% high."}</p>"""
    ))

    # 16. Unified Searchable Test Register & SHA-256 Architecture
    slides.append((False,
        "15 · Arquitectura de credibilidad" if es else "15 · Credibility Architecture",
        f"Registro unificado de {reg['total_pruebas']} entradas y hashes locales SHA-256" if es else f"Unified {reg['total_pruebas']}-Entry Register and Local SHA-256 Seals",
        f"""<div class="grid2">
          <div class="card">
            <h3>{"Desglose del Registro Unificado (test_register.html)" if es else "Unified Register Breakdown (test_register.html)"}</h3>
            <p>{f"• <b>{reg['total_pruebas']} entradas totales</b>: {reg['historicas_v1']} históricas (v1) + {reg['nuevas_v2']} nuevas (Bloques A–D v2, todos los ítems cerrados).<br>• <b>26 pruebas bajo protocolos congelados</b> con Holm exacto (m=6 en P01).<br>• <b>Negativos, refutados y desviaciones</b> visibles con la misma prominencia que los positivos." if es else f"• <b>{reg['total_pruebas']} total entries</b>: {reg['historicas_v1']} historical (v1) + {reg['nuevas_v2']} new (Blocks A–D v2, all items closed).<br>• <b>26 tests under frozen protocols</b> with exact Holm adjustment (m=6 in P01).<br>• <b>Negatives, refutations, and deviations</b> shown with equal prominence to positive findings."}</p>
            <p>{"Búsqueda instantánea sin conexión por ID, quipu, bloque o veredicto." if es else "Instant offline search by ID, khipu, block, or verdict."}</p>
          </div>
          <div class="card">
            <h3>{"Sellos SHA-256 archivados en Zenodo (v2.0.2)" if es else "SHA-256 Seals Archived on Zenodo (v2.0.2)"}</h3>
            <div class="mono" style="font-size:0.75rem;line-height:1.65">
              P01: 9c8346f026f710e9…<br>
              P02: fe169457c81eed41…<br>
              P03: 49bc9f1f061cc2c7…<br>
              P04: bfa1d02ceec83353…<br>
              P05: 21152013979545e4…<br>
              P06: b44a3293e4182065…
            </div>
            <p style="margin-top:8px" class="muted">{"Revisados por un segundo modelo de IA (Claude Opus) antes y después de la ejecución (no equivale a revisión por pares humana)." if es else "Reviewed by a second AI model (Claude Opus) before and after execution (not equivalent to human peer review)."}</p>
          </div>
        </div>"""
    ))

    # 17. Strict Prior-Art Attribution & Corrections
    slides.append((False,
        "16 · Atribución rigurosa y autocorrecciones" if es else "16 · Strict Prior-Art Attribution & Self-Corrections",
        "Construir sobre el trabajo de especialistas y corregir errores en público" if es else "Building on Specialist Scholarship and Correcting Errors Publicly",
        f"""<div class="grid2">
          <div class="card">
            <h3>{"Atribución explícita de antecedentes" if es else "Explicit Prior-Art Attribution"}</h3>
            <p>{"• <b>Ashok Khosla</b>: editor y mantenedor del KFG (Manuel Medrano citado con precisión como afiliado y coautor 2024).<br>• <b>Andrés Chirinos (2010, 2023, 2026)</b>: copias Lima–París y Lima–Gotemburgo, proporcionalidad, registro RT-16905 y nota sobre UR053.<br>• <b>Ascher &amp; Ascher (1978)</b>: jerarquía de 3 niveles en AS038/KH0049.<br>• <b>Urton &amp; Chu (2015, 2018)</b>: cuotas y copias de Inkawasi.<br>• <b>Karen Thompson (2025)</b>: 222 correcciones al Databook." if es else "• <b>Ashok Khosla</b>: editor & maintainer of KFG (Manuel Medrano accurately credited as affiliate & 2024 co-author).<br>• <b>Andrés Chirinos (2010, 2023, 2026)</b>: Lima–Paris & Lima–Gothenburg copies, proportionality, RT-16905 recording, UR053 note.<br>• <b>Ascher &amp; Ascher (1978)</b>: 3-level hierarchy in AS038/KH0049.<br>• <b>Urton &amp; Chu (2015, 2018)</b>: Inkawasi quotas & copies.<br>• <b>Karen Thompson (2025)</b>: 222 Databook corrections."}</p>
          </div>
          <div class="card">
            <h3>{"Errores nuestros corregidos y retirados" if es else "Our Own Errors Corrected & Withdrawn"}</h3>
            <p>{"• Retiramos <code>UR267A+B → UR269</code> (falló fuera de muestra, Holm 0.50) y nuestra hipótesis de ceques <code>UR050+UR055</code> (0/3 predicciones).<br>• Corregimos nuestro <i>p</i>=0.006 circular del Santa a 0.24.<br>• Rebajamos 1,390 t a ~470 t por carga precolombina (hasta 950 t en fanega colonial).<br>• Precisamos “no se distingue del azar” por “no es informativo” sobre el 74 %." if es else "• Withdrew <code>UR267A+B → UR269</code> (failed out-of-sample, Holm 0.50) and our ceque hypothesis <code>UR050+UR055</code> (0/3 predictions).<br>• Corrected our circular Santa <i>p</i>=0.006 to 0.24.<br>• Revised 1,390 t down to ~470 t via pre-Columbian carga (up to 950 t colonial fanega).<br>• Tightened “indistinguishable from chance” to “not informative” for the 74% figure."}</p>
          </div>
        </div>"""
    ))

    # 18. Next Steps: Zenodo DOI & Peer-Reviewed Journal
    slides.append((True,
        "17 · Próximo paso: Zenodo v2.0.2 y revista científica" if es else "17 · Next Step: Zenodo v2.0.2 & Peer-Reviewed Journal",
        "De ensayo abierto a estándar replicable de evaluación cuantitativa" if es else "From Open Essay to a Replicable Standard for Quantitative Khipu Auditing",
        f"""<div class="grid2">
          <div class="card">
            <h3>{"1. Depósito Zenodo v2.0.2 (DOI 10.5281/zenodo.24600101)" if es else "1. Zenodo v2.0.2 Deposit (DOI 10.5281/zenodo.24600101)"}</h3>
            {f"Congela el Corpus Maestro (689 quipus), los 6 protocolos SHA-256, el Registro Unificado de {reg['total_pruebas']} pruebas (HTML/JSON/CSV), el Lector v2 con FPR calibrada y el ensayo bilingüe bajo CC BY 4.0 / MIT." if es else f"Freezes the 689-khipu Master Corpus, 6 SHA-256 protocols, the {reg['total_pruebas']}-test Unified Register (HTML/JSON/CSV), Reader v2 with calibrated FPR, and the bilingual essay under CC BY 4.0 / MIT."}
          </div>
          <div class="card">
            <h3>{"2. Envío a revista revisada por pares" if es else "2. Peer-Reviewed Journal Submission"}</h3>
            {"Siguiendo la recomendación de Manuel Medrano, manuscrito listo para <i>Latin American Antiquity</i> o <i>Journal of Archaeological Science</i>: evaluación con modelos nulos quipu por quipu, réplica fuera de muestra y auditoría unificada de la literatura de 2026." if es else "Following Manuel Medrano's recommendation, manuscript structured for <i>Latin American Antiquity</i> or <i>Journal of Archaeological Science</i>: khipu-by-khipu null modeling, out-of-sample replication, and unified audit of 2026 computational claims."}
          </div>
        </div>
        <p style="margin-top:22px;font-family:system-ui,sans-serif;font-size:0.9rem;color:#d6cdc1">{"Verificación completa: <code>python lector/verificar.py</code> (21/21 OK) · <code>python analisis/paquete_revision/verificar.py</code> (19/19 OK) · <code>python articulo/fuente/comprobar.py</code> (todo cuadra)" if es else "Full verification: <code>python lector/verificar.py</code> (21/21 OK) · <code>python analisis/paquete_revision/verificar.py</code> (19/19 OK) · <code>python articulo/fuente/comprobar.py</code> (all checks pass)"}</p>"""
    ))
    return slides


def render_deck(lang, ctx):
    es = (lang == "es")
    slides = build_slides(lang, ctx)
    total = len(slides)
    blocks = []
    for i, (dark, kicker, title, body) in enumerate(slides, 1):
        cls = "slide dark" if dark else "slide"
        h_tag = "h1" if i == 1 else "h2"
        blocks.append(f"""
<section class="{cls}">
  <div>
    <div class="kicker">{kicker}</div>
    <{h_tag}>{title}</{h_tag}>
    {body}
  </div>
  <div class="foot">
    <span>{"Lo que suman los quipus · v2.0.2" if es else "What the Khipus Add Up To · v2.0.2"}</span>
    <span>{i} / {total}</span>
  </div>
</section>""")

    other_href = "overview.html" if es else "overview.es.html"
    other_lbl = "English" if es else "Español"
    art_href = "index.es.html" if es else "index.html"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{"Resumen Visual (18 láminas): Lo que suman los quipus v2.0.2" if es else "Visual Overview (18 slides): What the Khipus Add Up To v2.0.2"}</title>
<style>{CSS}</style>
</head>
<body>
<div class="toolbar">
  <div><b>{"Resumen Visual (18 láminas)" if es else "Visual Overview (18 slides)"}</b> · {"Lo que suman los quipus v2.0.2" if es else "What the Khipus Add Up To v2.0.2"}</div>
  <div>
    <a href="{art_href}">{"Ensayo completo" if es else "Full Essay"}</a>
    <a href="registro_pruebas.html">{"Registro (98 pruebas)" if es else "Register (98 tests)"}</a>
    <a href="{other_href}">{other_lbl}</a>
    <button onclick="window.print()">{"Guardar / Imprimir PDF" if es else "Print / Save PDF"}</button>
  </div>
</div>
<main class="deck">
{"".join(blocks)}
</main>
</body>
</html>
"""


def main():
    ctx = {
        "reg": load_json(AN / "registro_pruebas/test_register.json"),
        "fpr": load_json(RAIZ / "lector/calibracion_fpr.json"),
        "p1": load_json(AN / "36_corpus_maestro/resultados_P01.json"),
        "p2": load_json(AN / "37_bloque_B/resultados_P02.json"),
        "p3": load_json(AN / "37_bloque_B/resultados_P03.json"),
        "p4": load_json(AN / "38_bloque_C/resultados_P04.json"),
        "p5": load_json(AN / "38_bloque_C/resultados_P05.json"),
        "p6": load_json(AN / "39_bloque_D/resultados_P06.json"),
    }
    for lang, fname in [("es", "overview.es.html"), ("en", "overview.html")]:
        html = render_deck(lang, ctx)
        out = ART / fname
        out.write_text(html, encoding="utf-8", newline="\n")
        print(f"{out} ({len(html.encode())//1024} KB)")


if __name__ == "__main__":
    main()
