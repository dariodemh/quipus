# -*- coding: utf-8 -*-
"""Construye la aplicacion web del Lector de Quipus 100% en navegador (cero servidor):
  - articulo/lector.html     (ingles)
  - articulo/lector.es.html  (espanol)

Embebe los 682 quipus del corpus ampliado (651 KFG + 19 OKR extra + 11 Huacones virgenes + 1 JS01)
y ejecuta en JavaScript en <200 ms: resumen fisico, gramatica decimal/aditiva, sumas vs
nulo de permutacion, clave de color, alternancia de dos colores, regla P5c, medicion de
hueco de cero, escaneo bayesiano tolerante a errores (+-1, x10, transposiciones) y carga
de CSV propio por arrastrar y soltar.

Uso: python articulo/fuente/construir_lector.py [carpeta_destino]
"""
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

S = Path(__file__).resolve().parent
RAIZ = S.parents[1]
DEST = Path(sys.argv[1]) if len(sys.argv) > 1 else S.parent

GENRE_MAP = {
    "ARC": ("Archivo jerárquico", "Hierarchical archive"),
    "SUM": ("Lista con totales", "List with totals"),
    "FOR": ("Formulario con reparto", "Form with a split"),
    "TAB": ("Tabla de recuento", "Tally table"),
    "PAD": ("Padrón por persona", "Register by person"),
    "ASG": ("Asignación", "Allocation"),
    "TAL": ("Conteo por marcas", "Tally marks"),
    "NAZ": ("Ficha de Nazca", "Nazca card"),
    "CAL": ("Calendario", "Calendar"),
    "NON": ("No numérico", "Non-numeric"),
    "SEG": ("Lista segmentada", "Segmented list"),
    "SIN": ("Sin tipo reconocible", "No recognizable type"),
}


def compact_knots(s):
    if not isinstance(s, str) or not s.strip():
        return ""
    out = []
    for m in re.finditer(r"(\d+)([SLE])\(([\d.]+|nan)?,?([SZU]?)\),(\d+)", s):
        n, t, pos, dr, v = m.groups()
        p = "" if not pos or pos == "nan" else str(round(float(pos), 1)).rstrip("0").rstrip(".")
        out.append(f"{n}{t}@{p}={v}")
    return ";".join(out)


def load_all_khipus():
    c_kfg = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False)
    q_meta = pd.read_csv(RAIZ / "analisis/datos/quipus.csv").set_index("kfg")
    atlas = pd.read_csv(RAIZ / "analisis/28_atlas_generos/atlas.csv").set_index("kfg")
    enm = pd.read_csv(RAIZ / "analisis/28_atlas_generos/enmiendas.csv").set_index("kfg")
    c_ext = pd.read_csv(RAIZ / "analisis/17_okr_pendientes/cuerdas_extra.csv", low_memory=False)
    c_hua = pd.read_csv(RAIZ / "analisis/35_huacones_virgenes/cuerdas_huacones.csv", low_memory=False)
    q_hua = pd.read_csv(RAIZ / "analisis/35_huacones_virgenes/quipus_huacones.csv").set_index("kfg")
    c_js1 = pd.read_csv(RAIZ / "analisis/37_vision_y_extra/cuerdas_js01.csv", low_memory=False)
    oos_res = pd.read_csv(RAIZ / "analisis/35_huacones_virgenes/resultados_lector_oos.csv").set_index("kfg")

    items = []

    def pack_df(df, src_label):
        for k, grp in df.groupby("kfg", sort=False):
            grp = grp.sort_values("orden")
            if k in q_meta.index:
                qm = q_meta.loc[k]
                prov = "" if pd.isna(qm.procedencia) else str(qm.procedencia)
                mus = "" if pd.isna(qm.museo) else str(qm.museo)
            elif k in q_hua.index:
                prov = "Huacones-Vilcahuasi (Bajo Cañete)"
                mus = "PIA El Huarco-Huacones (OKR)"
            elif k == "JS01":
                prov = "Ancón (KH0676)"
                mus = "Brooklyn Museum 36.718"
            else:
                prov = "OKR pendiente"
                mus = "OKR"
            if k in enm.index:
                gen = str(enm.loc[k, "genero_nuevo"])
                conf = str(enm.loc[k, "confianza"])
            elif k in atlas.index:
                gen = str(atlas.loc[k, "genero"])
                conf = str(atlas.loc[k, "confianza"])
            elif k in oos_res.index:
                gen = str(oos_res.loc[k, "genero"])
                conf = str(oos_res.loc[k, "confianza"])
            elif k == "JS01":
                gen, conf = "TAL", "media"
            else:
                gen, conf = "SIN", "baja"

            cords = []
            for r in grp.itertuples():
                col = "" if pd.isna(r.color) else re.sub(r"\([^)]*\)", "", str(r.color)).strip()
                val = 0 if pd.isna(r.valor) else int(round(float(r.valor)))
                largo = None if pd.isna(r.largo) else round(float(r.largo), 1)
                kn = compact_knots(r.nudos)
                uni = "" if pd.isna(r.union) else str(r.union)
                if uni in ("Unknown", "nan"):
                    uni = ""
                cords.append([
                    str(r.cuerda),
                    int(r.nivel) if pd.notna(r.nivel) else 0,
                    int(r.grupo) if pd.notna(r.grupo) else 0,
                    val,
                    col,
                    largo,
                    kn,
                    uni,
                ])
            items.append(dict(k=str(k), s=src_label, p=prov, m=mus, g=gen, c=conf, cords=cords))

    pack_df(c_kfg, "KFG")
    pack_df(c_ext, "OKR-extra")
    pack_df(c_hua, "Huacones-OKR")
    pack_df(c_js1, "OKR-JS01")
    return items


HTML_HEAD = """<!doctype html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23f7f6f2'/%3E%3Cpath d='M4 8h24' stroke='%238a6a4a' stroke-width='3' stroke-linecap='round'/%3E%3Cpath d='M10 9v15M16 9v18M22 9v12' stroke='%238a6a4a' stroke-width='2.2' stroke-linecap='round'/%3E%3Ccircle cx='10' cy='16' r='2.2' fill='%232f3f8f'/%3E%3Ccircle cx='16' cy='14' r='2.2' fill='%232f3f8f'/%3E%3Ccircle cx='16' cy='21' r='2.2' fill='%232f3f8f'/%3E%3Ccircle cx='22' cy='16' r='2.2' fill='%232f3f8f'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{
  --papel:#f7f6f2; --tarjeta:#fffdf8; --tinta:#1d1b18; --gris:#6b655c; --regla:#dcd8cf; --suave:#efece5;
  --indigo:#2f3f8f; --cochinilla:#a8322d; --fibra:#8a6a4a;
  --ev-d:#2f3f8f; --ev-a:#2c7a6b; --ev-p:#a8701a; --ok:#2c7a6b; --casi:#b07a1e; --mal:#a8322d;
  --serif:"Newsreader",Georgia,"Times New Roman",serif;
  --sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,"Cascadia Mono",Consolas,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --papel:#17150f; --tarjeta:#1f1c16; --tinta:#ece7dd; --gris:#a69e90; --regla:#3a352d; --suave:#25221b;
  --indigo:#a3b0ff; --cochinilla:#f08177; --fibra:#c9a27e;
  --ev-d:#a3b0ff; --ev-a:#6cc3b0; --ev-p:#e2b25a; --ok:#6cc3b0; --casi:#e2b25a; --mal:#f08177; color-scheme:dark}}
:root[data-theme="dark"]{
  --papel:#17150f; --tarjeta:#1f1c16; --tinta:#ece7dd; --gris:#a69e90; --regla:#3a352d; --suave:#25221b;
  --indigo:#a3b0ff; --cochinilla:#f08177; --fibra:#c9a27e;
  --ev-d:#a3b0ff; --ev-a:#6cc3b0; --ev-p:#e2b25a; --ok:#6cc3b0; --casi:#e2b25a; --mal:#f08177; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--papel);color:var(--tinta);font-family:var(--sans);font-size:15px;line-height:1.55;margin:0;padding:20px 16px 64px}
.wrap{max-width:1160px;margin-inline:auto}
a{color:var(--indigo);text-underline-offset:2px}
header{border-bottom:1px solid var(--regla);padding-bottom:16px;margin-bottom:22px}
.kicker{font-size:12px;letter-spacing:.09em;text-transform:uppercase;color:var(--gris);margin-bottom:6px}
h1{font-family:var(--serif);font-weight:500;font-size:clamp(30px,4.5vw,44px);line-height:1.1;margin:0 0 8px}
.sub{font-family:var(--serif);font-style:italic;color:var(--gris);font-size:19px;margin:0 0 12px}
.meta{font-size:13.5px;color:var(--gris);display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}
.tema-btn{font:inherit;color:var(--indigo);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline;text-underline-offset:2px}
.grid{display:grid;grid-template-columns:340px 1fr;gap:20px;align-items:start}
@media (max-width:860px){.grid{grid-template-columns:1fr}}
.panel{background:var(--tarjeta);border:1px solid var(--regla);border-radius:12px;padding:16px}
.panel h2{font-family:var(--serif);font-size:21px;font-weight:500;margin:0 0 12px}
.tabs{display:flex;gap:6px;margin-bottom:12px}
.tab{flex:1;font-size:13px;font-weight:500;padding:7px 10px;border-radius:8px;border:1px solid var(--regla);background:var(--papel);color:var(--tinta);cursor:pointer}
.tab[aria-selected="true"]{background:var(--tinta);color:var(--papel);border-color:var(--tinta)}
input[type="search"],select,textarea{width:100%;font-family:var(--sans);font-size:14px;padding:8px 10px;border-radius:8px;border:1px solid var(--regla);background:var(--papel);color:var(--tinta);margin-bottom:8px}
textarea{font-family:var(--mono);font-size:12px;min-height:130px;resize:vertical}
.lista{max-height:290px;overflow-y:auto;border:1px solid var(--regla);border-radius:8px;background:var(--papel)}
.item{display:flex;justify-content:space-between;align-items:center;gap:8px;width:100%;text-align:left;padding:7px 10px;border:0;border-bottom:1px solid var(--suave);background:none;color:var(--tinta);cursor:pointer;font-size:13px}
.item:hover{background:var(--suave)}
.item.act{background:color-mix(in srgb,var(--indigo) 14%,transparent);font-weight:600}
.item .kid{font-family:var(--mono);font-weight:600}
.item .subt{font-size:11.5px;color:var(--gris);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:165px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 12px}
.chip{font-family:var(--mono);font-size:12px;padding:4px 9px;border-radius:99px;border:1px solid var(--regla);background:var(--papel);color:var(--tinta);cursor:pointer}
.chip:hover{border-color:var(--fibra)}
.drop{border:2px dashed var(--regla);border-radius:10px;padding:14px;text-align:center;color:var(--gris);font-size:13px;margin-bottom:10px;cursor:pointer;background:var(--papel)}
.drop.over{border-color:var(--indigo);color:var(--indigo)}
.btn{font-size:13px;font-weight:500;padding:7px 12px;border-radius:99px;border:1px solid var(--regla);background:var(--papel);color:var(--tinta);cursor:pointer}
.btn.pri{background:var(--indigo);color:#fff;border-color:var(--indigo)}
.btn:hover{opacity:.9}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:14px}
.kpi{background:var(--suave);border-radius:8px;padding:10px 12px}
.kpi .v{font-family:var(--mono);font-size:20px;font-weight:600}
.kpi .l{font-size:12px;color:var(--gris)}
.ev{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:2px 7px;border-radius:99px;border:1px solid currentColor;margin-right:6px;white-space:nowrap}
.ev-d{color:var(--ev-d)} .ev-a{color:var(--ev-a)} .ev-p{color:var(--ev-p)} .ev-n{color:var(--gris)}
.sec{border-top:1px solid var(--regla);padding:12px 0}
.sec h3{font-family:var(--serif);font-size:18px;font-weight:500;margin:0 0 8px}
.sec ul{margin:0;padding:0;list-style:none}
.sec li{margin:6px 0}
.svgbox{overflow-x:auto;background:var(--papel);border:1px solid var(--regla);border-radius:10px;padding:10px;margin-bottom:14px}
.svgbox svg{display:block;height:auto}
.tip{font-family:var(--mono);font-size:12.5px;color:var(--gris);min-height:1.5em;margin-top:6px}
.matches{width:100%;border-collapse:collapse;font-size:13px}
.matches th{text-align:left;font-size:11.5px;color:var(--gris);border-bottom:1px solid var(--regla);padding:5px 6px}
.matches td{padding:5px 6px;border-bottom:1px solid var(--suave)}
.matches td.m{font-family:var(--mono)}
.oculto{display:none}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="kicker">__KICKER__</div>
  <h1>__TITLE__</h1>
  <p class="sub">__DESC__</p>
  <div class="meta">
    <a href="__ESSAY__">__BACK_ESSAY__</a>
    <a href="__OTHER_HTML__">__OTHER_LANG__</a>
    <button type="button" class="tema-btn" id="tema-btn" aria-pressed="false">__DARK_LBL__</button>
    <span><strong id="corpus-count">682</strong> __CORPUS_LBL__</span>
  </div>
</header>

<div class="grid">
  <aside class="panel">
    <div class="tabs" role="tablist">
      <button type="button" class="tab" id="tab-corpus" aria-selected="true">__TAB_CORPUS__</button>
      <button type="button" class="tab" id="tab-custom" aria-selected="false">__TAB_CUSTOM__</button>
    </div>

    <div id="pane-corpus">
      <input type="search" id="buscar" placeholder="__SEARCH_PH__">
      <select id="filtro-fuente">
        <option value="">__ALL_SRC__</option>
        <option value="KFG">KFG (651)</option>
        <option value="OKR-extra">OKR extra (19)</option>
        <option value="Huacones-OKR">Huacones OKR (11)</option>
        <option value="OKR-JS01">OKR JS01 (1)</option>
      </select>
      <div class="chips" id="rapidos"></div>
      <div class="lista" id="lista-quipus"></div>
    </div>

    <div id="pane-custom" class="oculto">
      <div class="drop" id="dropzone">__DROP_TXT__<input type="file" id="archivo-csv" accept=".csv,.txt" style="display:none"></div>
      <textarea id="csv-texto" placeholder="__PASTE_PH__"></textarea>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button type="button" class="btn pri" id="btn-analizar">__ANALYZE_BTN__</button>
        <button type="button" class="btn" id="btn-ejemplo">__SAMPLE_BTN__</button>
      </div>
    </div>
  </aside>

  <main class="panel" id="salida">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;margin-bottom:12px">
      <div>
        <h2 id="q-titulo" style="margin:0">—</h2>
        <div id="q-meta" style="font-size:13px;color:var(--gris)"></div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button type="button" class="btn" id="btn-copiar-md">__COPY_MD__</button>
        <button type="button" class="btn" id="btn-dl-json">__DL_JSON__</button>
      </div>
    </div>

    <div class="kpis" id="kpis"></div>

    <div class="svgbox">
      <svg id="svg-quipu" viewBox="0 0 900 260" width="900" height="260" role="img" aria-label="Diagrama del quipu"></svg>
      <div class="tip" id="cord-tip">__HOVER_TIP__</div>
    </div>

    <div id="ficha-secciones"></div>
  </main>
</div>
</div>

<script>
const CORPUS = __CORPUS__;
const GENRES = __GENRES__;
__JS__
</script>
</body>
</html>
"""

JS_APP = r"""(function(){
'use strict';
const EN = document.documentElement.lang === 'en';
const tl = (es, en) => EN ? en : es;
const $ = id => document.getElementById(id);

const CC = {W:'#f4f0e6',AB:'#b58d5c',MB:'#7d5636',DB:'#4b3220',LB:'#cdab7d',YB:'#c9a54e',NB:'#a07c58',KB:'#3a2a20',
  RL:'#c4574f',RB:'#8e3b2f',R:'#b33a2e',RO:'#c44536',PK:'#e3a6b6',B:'#3c4f9e',G:'#4f7d4f',Y:'#d9b43a',GR:'#8d8a84',
  BS:'#5f6a8a',HB:'#8a6d4b',FR:'#a66a50',SR:'#b9502f',LC:'#a68b67'};
function colorCuerda(code){ const c = String(code || '').split(':')[0].split('/')[0].split('-')[0].trim(); return CC[c] || '#9a7b5a'; }

// PRNG determinista (Mulberry32) para nulos reproducibles
function makeRng(seed){
  let a = seed >>> 0;
  return function(){ a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
function shuffle(arr, rng){
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(rng() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

// Precomputar frecuencias globales en el corpus para busqueda bayesiana rapida
const FREQ = new Map();
let TOT_NZ = 0;
CORPUS.forEach(q => q.cords.forEach(c => { if (c[3] > 0){ FREQ.set(c[3], (FREQ.get(c[3]) || 0) + 1); TOT_NZ++; } }));
const CORP_NZ = CORPUS.map(q => ({
  k: q.k, s: q.s, p: q.p,
  vals: q.cords.filter(c => c[3] > 0).map(c => c[3]),
  set10: new Set(q.cords.filter(c => c[3] >= 10).map(c => c[3]))
}));

function parseKnots(kstr){
  if (!kstr) return [];
  const out = [];
  String(kstr).split(';').forEach(tok => {
    const m = tok.match(/^(\d+)([SLE])@([\d.]*)=(\d+)$/);
    if (m) out.push({n:+m[1], t:m[2], pos:m[3] === '' ? null : +m[3], v:+m[4]});
    else {
      const m2 = tok.match(/(\d+)([SLE])\(([\d.]+|nan)?,?[SZU]?\),(\d+)/);
      if (m2) out.push({n:+m2[1], t:m2[2], pos:(m2[3] && m2[3] !== 'nan') ? +m2[3] : null, v:+m2[4]});
    }
  });
  return out;
}

function isNonDecimal(kstr){
  const ks = parseKnots(kstr).filter(x => x.v > 0);
  if (!ks.length) return null;
  const ords = [];
  for (const x of ks){
    const d = Math.floor(Math.log10(x.v));
    if (x.v % Math.pow(10, d) !== 0) return true;
    ords.push(d);
  }
  return new Set(ords).size !== ords.length;
}

function analyzeKhipu(q){
  const rng = makeRng(20261123);
  const cords = q.cords;
  const p0 = cords.filter(c => c[1] === 0);
  const subs = cords.filter(c => c[1] > 0);
  const knotted = cords.filter(c => c[3] > 0 || c[6]);
  const broken = cords.filter(c => c[3] === 0 && !c[6]).length;
  const colors = [...new Set(cords.map(c => c[4]).filter(Boolean))];
  const groups = [...new Set(p0.map(c => c[2]))];
  const totVal = cords.reduce((s, c) => s + (c[3] || 0), 0);

  // 1. Gramatica
  let nonDec = 0, evalDec = 0, additive = 0;
  cords.forEach(c => {
    const nd = isNonDecimal(c[6]);
    if (nd !== null){ evalDec++; if (nd) nonDec++; }
    const ks = parseKnots(c[6]).filter(x => (x.t === 'L' || x.t === 'E') && x.v < 10);
    if (ks.length >= 2 && ks.reduce((s, x) => s + x.v, 0) > 9) additive++;
  });

  // 2. Sumas internas (extremo de grupo = suma del resto; consecutivo 2..3) vs nulo (500 barajas)
  const byGrp = new Map();
  p0.forEach(c => { if (!byGrp.has(c[2])) byGrp.set(c[2], []); byGrp.get(c[2]).push(c[3]); });
  const countGroupSums = valsArr => {
    let idx = 0, hits = 0;
    for (const g of byGrp.values()){
      const sub = valsArr.slice(idx, idx + g.length); idx += g.length;
      const nz = sub.filter(v => v > 0);
      if (nz.length >= 3){
        const tot = sub.reduce((a, b) => a + b, 0);
        if (sub[0] >= 10 && sub[0] === tot - sub[0]) hits++;
        else if (sub[sub.length - 1] >= 10 && sub[sub.length - 1] === tot - sub[sub.length - 1]) hits++;
      }
    }
    return hits;
  };
  const p0Vals = p0.map(c => c[3]);
  const obsGrpSums = countGroupSums(p0Vals);
  let geGrp = 0;
  const B = 500;
  for (let b = 0; b < B; b++){ if (countGroupSums(shuffle(p0Vals, rng)) >= obsGrpSums) geGrp++; }
  const pSum = obsGrpSums > 0 ? (1 + geGrp) / (1 + B) : 1;

  // Ejemplos concretos de suma en grupos
  const sumExamples = [];
  for (const [gid, vals] of byGrp.entries()){
    if (vals.filter(v => v > 0).length < 3) continue;
    const tot = vals.reduce((a, b) => a + b, 0);
    if (vals[0] >= 10 && vals[0] === tot - vals[0]) sumExamples.push(tl('grupo ', 'group ') + gid + tl(': primera = ', ': first = ') + vals[0]);
    else if (vals[vals.length - 1] >= 10 && vals[vals.length - 1] === tot - vals[vals.length - 1]) sumExamples.push(tl('grupo ', 'group ') + gid + tl(': última = ', ': last = ') + vals[vals.length - 1]);
  }

  // 3. Alternancia de dos colores (desfase 2: A-B-A)
  const cols0 = p0.map(c => c[4]);
  const countAlt = arr => { let n = 0; for (let i = 0; i + 2 < arr.length; i++) if (arr[i] && arr[i] === arr[i+2] && arr[i] !== arr[i+1]) n++; return n; };
  const obsAlt = countAlt(cols0);
  let geAlt = 0;
  for (let b = 0; b < B; b++){ if (countAlt(shuffle(cols0, rng)) >= obsAlt) geAlt++; }
  const pAlt = obsAlt > 0 ? (1 + geAlt) / (1 + B) : 1;

  // 4. Regla P5c: mayor abre grupo
  let p5Hits = 0, p5Tot = 0, p5Exp = 0;
  for (const vals of byGrp.values()){
    const nz = vals.filter(v => v > 0);
    if (nz.length >= 3){
      p5Tot++;
      const mx = Math.max(...nz);
      if (vals[0] === mx) p5Hits++;
      p5Exp += 1 / nz.length;
    }
  }

  // 5. Huecos de cero (cuerdas con >=2 racimos donde falta una banda decimal)
  const zeroGaps = [];
  cords.forEach(c => {
    const ks = parseKnots(c[6]).filter(x => x.pos !== null && x.v > 0).sort((a, b) => a.pos - b.pos);
    for (let i = 0; i + 1 < ks.length; i++){
      const d1 = Math.floor(Math.log10(ks[i].v)), d2 = Math.floor(Math.log10(ks[i+1].v));
      if (d1 - d2 === 2){
        const gap = ks[i+1].pos - ks[i].pos;
        const adj = i > 0 ? ks[i].pos - ks[i-1].pos : (i + 2 < ks.length ? ks[i+2].pos - ks[i+1].pos : null);
        if (adj && adj > 0) zeroGaps.push({cord:c[0], val:c[3], ratio: +(gap / adj).toFixed(2)});
      }
    }
  });

  // 6. Busqueda bayesiana tolerante a errores contra 682 quipus
  const myNz = cords.filter(c => c[3] > 0).map(c => c[3]);
  const my10 = new Set(myNz.filter(v => v >= 10));
  const matches = [];
  if (my10.size >= 3){
    CORP_NZ.forEach(other => {
      if (other.k === q.k || other.vals.length < 4) return;
      let llr = 0, nEx = 0, nPm1 = 0, n10 = 0, nTr = 0;
      const seen = new Set();
      for (const v of my10){
        if (other.set10.has(v)){
          const pr = Math.max((FREQ.get(v) || 1) / TOT_NZ, 1 / TOT_NZ);
          llr += Math.min(7, Math.log(0.85 / pr));
          nEx++; seen.add(v);
        } else if (other.set10.has(v + 1) || other.set10.has(v - 1)){
          llr += 1.4; nPm1++;
        } else if (other.set10.has(v * 10) || (v % 10 === 0 && other.set10.has(v / 10))){
          llr += 1.1; n10++;
        } else {
          const sv = String(v).split('').sort().join('');
          for (const ov of other.set10){
            if (String(ov).length === sv.length && String(ov).split('').sort().join('') === sv){ llr += 1.6; nTr++; break; }
          }
        }
      }
      if (nEx >= 3 && llr >= 10){
        matches.push({k:other.k, s:other.s, p:other.p, llr:+llr.toFixed(1), nEx, nPm1, n10, nTr});
      }
    });
    matches.sort((a, b) => b.llr - a.llr);
  }

  return {
    nCords: cords.length, nP0: p0.length, nSubs: subs.length, nKnotted: knotted.length, nBroken: broken,
    nGroups: groups.length, colors, totVal,
    evalDec, nonDec, additive,
    obsGrpSums, pSum, sumExamples,
    obsAlt, pAlt,
    p5Hits, p5Tot, p5Exp:+p5Exp.toFixed(1),
    zeroGaps, matches: matches.slice(0, 10)
  };
}

function drawSVG(q){
  const svg = $('svg-quipu'), tip = $('cord-tip');
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  const NS = 'http://www.w3.org/2000/svg';
  const el = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
  const p0 = q.cords.filter(c => c[1] === 0);
  const maxShow = Math.min(p0.length, 90);
  const W = Math.max(900, 70 + maxShow * 18);
  svg.setAttribute('viewBox', `0 0 ${W} 260`);
  svg.setAttribute('width', W);
  el('line', {x1:20, y1:28, x2:W - 20, y2:28, style:'stroke:var(--fibra);stroke-width:5;stroke-linecap:round'}, svg);

  let prevG = null, x = 40;
  const maxL = Math.max(40, ...p0.slice(0, maxShow).map(c => c[5] || 35));
  p0.slice(0, maxShow).forEach((c, i) => {
    if (prevG !== null && c[2] !== prevG) x += 10;
    prevG = c[2];
    const len = ((c[5] || 30) / maxL) * 165 + 25;
    const g = el('g', {style:'cursor:pointer'}, svg);
    el('line', {x1:x, y1:28, x2:x, y2:28 + len, style:`stroke:var(--regla);stroke-width:6;stroke-linecap:round`}, g);
    el('line', {x1:x, y1:28, x2:x, y2:28 + len, style:`stroke:${colorCuerda(c[4])};stroke-width:4;stroke-linecap:round`}, g);
    const ks = parseKnots(c[6]);
    ks.forEach((k, j) => {
      const ky = k.pos !== null ? 28 + Math.min(len - 8, (k.pos / maxL) * 165 + 8) : 45 + j * 18;
      el('circle', {cx:x, cy:ky, r:k.t === 'L' ? 3.8 : 2.6, style:`fill:${k.t === 'E' ? 'var(--cochinilla)' : 'var(--tinta)'}`}, g);
    });
    if (c[3] > 0 && maxShow <= 55){
      const tx = el('text', {x, y:45 + len, 'text-anchor':'middle', style:'font-family:var(--mono);font-size:10px;fill:var(--tinta)'}, g);
      tx.textContent = c[3];
    }
    const info = `${c[0]} (${tl('grupo', 'group')} ${c[2]}) · ${tl('valor', 'value')}=${c[3]} · ${tl('color', 'color')}=${c[4] || '—'} · ${tl('largo', 'length')}=${c[5] ?? '—'} cm${c[6] ? ' · ' + c[6] : ''}`;
    g.addEventListener('mouseenter', () => { tip.textContent = info; });
    g.addEventListener('click', () => { tip.textContent = info; });
    x += 16;
  });
  if (p0.length > maxShow){
    const tx = el('text', {x:24, y:248, style:'font-family:var(--sans);font-size:11.5px;fill:var(--gris)'}, svg);
    tx.textContent = tl(`Mostrando primeros ${maxShow} de ${p0.length} colgantes.`, `Showing first ${maxShow} of ${p0.length} pendants.`);
  }
}

let CURRENT = null, LAST_RES = null;

function render(q){
  CURRENT = q;
  const R = analyzeKhipu(q);
  LAST_RES = R;
  $('q-titulo').textContent = q.k;
  const gInfo = GENRES[q.g] ? (EN ? GENRES[q.g][1] : GENRES[q.g][0]) : q.g;
  $('q-meta').textContent = `${q.s} · ${q.p || tl('Procedencia desconocida', 'Unknown provenance')} · ${q.m || '—'} · ${tl('Género atlas:', 'Atlas genre:')} ${q.g} (${gInfo}, ${q.c})`;

  $('kpis').innerHTML = [
    [R.nCords, tl('Cuerdas totales', 'Total cords')],
    [R.nP0, tl('Colgantes', 'Pendants')],
    [R.nKnotted, tl('Anudadas', 'Knotted')],
    [R.totVal.toLocaleString(), tl('Suma total', 'Total sum')],
    [R.colors.length, tl('Colores', 'Colors')],
    [R.nGroups, tl('Grupos', 'Groups')],
  ].map(([v, l]) => `<div class="kpi"><div class="v">${v}</div><div class="l">${l}</div></div>`).join('');

  drawSVG(q);

  const badge = (lvl, txt) => {
    const cls = lvl === 'd' ? 'ev-d' : lvl === 'a' ? 'ev-a' : lvl === 'p' ? 'ev-p' : 'ev-n';
    const lbl = lvl === 'd' ? tl('dato', 'data') : lvl === 'a' ? tl('indicio', 'indication') : lvl === 'p' ? tl('conjetura', 'conjecture') : tl('negativo', 'negative');
    return `<li><span class="ev ${cls}">${lbl}</span>${txt}</li>`;
  };

  let html = '';
  html += `<div class="sec"><h3>${tl('1. Resumen físico y gramática numérica', '1. Physical summary & number grammar')}</h3><ul>`;
  html += badge('d', tl(`${R.nP0} colgantes, ${R.nSubs} subsidiarias, ${R.nBroken} sin nudos (rotas o vacías).`, `${R.nP0} pendants, ${R.nSubs} subsidiaries, ${R.nBroken} unknotted (broken or blank).`));
  if (R.evalDec){
    const pct = Math.round(100 * R.nonDec / R.evalDec);
    html += badge(R.nonDec ? 'a' : 'd', tl(`Gramática decimal: ${R.nonDec}/${R.evalDec} cuerdas anudadas (${pct} %) con estructura no decimal estándar; ${R.additive} cuerdas con notación aditiva multiunidad.`, `Decimal grammar: ${R.nonDec}/${R.evalDec} knotted cords (${pct}%) deviate from standard decimal places; ${R.additive} cords use additive multi-unit notation.`));
  }
  if (R.zeroGaps.length){
    const ex = R.zeroGaps.slice(0, 3).map(z => `${z.cord}=${z.val} (${z.ratio}×)`).join(', ');
    html += badge('d', tl(`Ceros posicionales medidos en ${R.zeroGaps.length} cuerda(s): ${ex}.`, `Positional zero gaps measured on ${R.zeroGaps.length} cord(s): ${ex}.`));
  }
  html += `</ul></div>`;

  html += `<div class="sec"><h3>${tl('2. Pruebas estadísticas internas (500 permutaciones)', '2. Internal statistical tests (500 permutations)')}</h3><ul>`;
  html += badge(R.pSum < 0.05 ? 'a' : 'n', tl(`Sumas de extremo de grupo: ${R.obsGrpSums} detectadas (p = ${R.pSum.toFixed(3)}). ${R.sumExamples.slice(0, 3).join('; ')}`, `Group-edge sums: ${R.obsGrpSums} detected (p = ${R.pSum.toFixed(3)}). ${R.sumExamples.slice(0, 3).join('; ')}`));
  html += badge(R.pAlt < 0.05 ? 'a' : 'n', tl(`Alternancia de dos colores (tríos A-B-A): ${R.obsAlt} (p = ${R.pAlt.toFixed(3)}).`, `Two-color alternation (A-B-A trios): ${R.obsAlt} (p = ${R.pAlt.toFixed(3)}).`));
  if (R.p5Tot){
    html += badge(R.p5Hits > R.p5Exp * 1.6 ? 'a' : 'd', tl(`Regla P5c («mayor abre grupo»): ${R.p5Hits} de ${R.p5Tot} grupos (esperado por azar: ${R.p5Exp}).`, `Rule P5c (“largest opens group”): ${R.p5Hits} of ${R.p5Tot} groups (expected by chance: ${R.p5Exp}).`));
  }
  html += `</ul></div>`;

  html += `<div class="sec"><h3>${tl(`3. Coincidencias bayesianas tolerantes a errores en ${CORPUS.length} quipus`, `3. Error-tolerant Bayesian matches across ${CORPUS.length} khipus`)}</h3>`;
  if (!R.matches.length){
    html += `<ul>${badge('n', tl('Sin coincidencias fuertes (LLR ≥ 10 con ≥ 3 valores ≥ 10) en el corpus.', 'No strong matches (LLR ≥ 10 with ≥ 3 values ≥ 10) across the corpus.'))}</ul>`;
  } else {
    html += `<table class="matches"><thead><tr><th>${tl('Quipu', 'Khipu')}</th><th>${tl('Procedencia', 'Provenance')}</th><th>LLR</th><th>${tl('Exactas', 'Exact')}</th><th>±1</th><th>×10</th><th>${tl('Transp.', 'Transp.')}</th></tr></thead><tbody>`;
    R.matches.forEach(m => {
      html += `<tr><td><button type="button" class="chip jump-q" data-k="${m.k}">${m.k}</button></td><td>${m.p || m.s}</td><td class="m">${m.llr}</td><td class="m">${m.nEx}</td><td class="m">${m.nPm1}</td><td class="m">${m.n10}</td><td class="m">${m.nTr}</td></tr>`;
    });
    html += `</tbody></table>`;
  }
  html += `</div>`;

  $('ficha-secciones').innerHTML = html;
  $('ficha-secciones').querySelectorAll('.jump-q').forEach(b => b.addEventListener('click', () => {
    const found = CORPUS.find(x => x.k === b.dataset.k);
    if (found){ render(found); highlightList(found.k); }
  }));
}

function highlightList(k){
  $('lista-quipus').querySelectorAll('.item').forEach(el => el.classList.toggle('act', el.dataset.k === k));
}

function renderList(){
  const q = $('buscar').value.trim().toLowerCase();
  const src = $('filtro-fuente').value;
  const cont = $('lista-quipus');
  const filt = CORPUS.filter(x => (!src || x.s === src) && (!q || x.k.toLowerCase().includes(q) || x.p.toLowerCase().includes(q) || x.g.toLowerCase().includes(q)));
  cont.innerHTML = filt.slice(0, 150).map(x => `<button type="button" class="item${CURRENT && CURRENT.k === x.k ? ' act' : ''}" data-k="${x.k}"><span class="kid">${x.k}</span><span class="subt">${x.g} · ${x.p || x.s}</span></button>`).join('');
  cont.querySelectorAll('.item').forEach(b => b.addEventListener('click', () => {
    const obj = CORPUS.find(x => x.k === b.dataset.k);
    if (obj){ render(obj); highlightList(obj.k); }
  }));
}

// Quipus rapidos
['UR278', 'UR270', 'KH0049', 'UR040', 'UR1104', 'UR053A', 'JC024', 'JC028', 'JC031', 'JS01'].forEach(k => {
  const b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.textContent = k;
  b.addEventListener('click', () => { const obj = CORPUS.find(x => x.k === k); if (obj){ render(obj); highlightList(obj.k); } });
  $('rapidos').appendChild(b);
});

// Tabs Corpus vs Custom
function setTab(custom){
  $('tab-corpus').setAttribute('aria-selected', String(!custom));
  $('tab-custom').setAttribute('aria-selected', String(custom));
  $('pane-corpus').classList.toggle('oculto', custom);
  $('pane-custom').classList.toggle('oculto', !custom);
}
$('tab-corpus').addEventListener('click', () => setTab(false));
$('tab-custom').addEventListener('click', () => setTab(true));

// Parse CSV propio (soporta esquema completo de cuerdas.csv o simple: cuerda,color,valor)
function parseCSV(txt, name){
  const lines = txt.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return null;
  const sep = lines[0].includes(';') && !lines[0].includes(',') ? ';' : ',';
  const hdr = lines[0].split(sep).map(s => s.trim().toLowerCase());
  const idx = n => hdr.indexOf(n);
  const iC = idx('cuerda') >= 0 ? idx('cuerda') : idx('cord');
  const iV = idx('valor') >= 0 ? idx('valor') : idx('value');
  const iCol = idx('color');
  const iGrp = idx('grupo') >= 0 ? idx('grupo') : idx('group');
  const iLvl = idx('nivel') >= 0 ? idx('nivel') : idx('level');
  const iLen = idx('largo') >= 0 ? idx('largo') : idx('length');
  const iKn = idx('nudos') >= 0 ? idx('nudos') : idx('knots');
  const cords = [];
  for (let i = 1; i < lines.length; i++){
    const cols = lines[i].split(sep).map(s => s.trim().replace(/^"|"$/g, ''));
    const val = iV >= 0 ? (parseInt(cols[iV], 10) || 0) : 0;
    cords.push([
      iC >= 0 ? cols[iC] : ('p' + i),
      iLvl >= 0 ? (parseInt(cols[iLvl], 10) || 0) : 0,
      iGrp >= 0 ? (parseInt(cols[iGrp], 10) || 0) : 0,
      val,
      iCol >= 0 ? cols[iCol] : 'W',
      iLen >= 0 && cols[iLen] ? parseFloat(cols[iLen]) : null,
      iKn >= 0 ? cols[iKn] : '',
      ''
    ]);
  }
  return {k: name || tl('MI_QUIPU', 'MY_KHIPU'), s: tl('Archivo local', 'Local CSV'), p: '—', m: '—', g: 'SIN', c: '—', cords};
}

$('btn-ejemplo').addEventListener('click', () => {
  $('csv-texto').value = 'cuerda,grupo,color,valor\np1,0,W,120\np2,0,AB,45\np3,0,AB,50\np4,0,AB,25\np5,1,W,80\np6,1,AB,30\np7,1,AB,50';
});
$('btn-analizar').addEventListener('click', () => {
  const q = parseCSV($('csv-texto').value);
  if (q) render(q);
});
const dz = $('dropzone'), fi = $('archivo-csv');
dz.addEventListener('click', () => fi.click());
dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('over'); });
dz.addEventListener('dragleave', () => dz.classList.remove('over'));
dz.addEventListener('drop', e => {
  e.preventDefault(); dz.classList.remove('over');
  const f = e.dataTransfer.files[0]; if (!f) return;
  f.text().then(t => { $('csv-texto').value = t; const q = parseCSV(t, f.name.replace(/\.[^.]+$/, '')); if (q) render(q); });
});
fi.addEventListener('change', () => {
  const f = fi.files[0]; if (!f) return;
  f.text().then(t => { $('csv-texto').value = t; const q = parseCSV(t, f.name.replace(/\.[^.]+$/, '')); if (q) render(q); });
});

$('btn-copiar-md').addEventListener('click', () => {
  if (!CURRENT || !LAST_RES) return;
  const md = `# ${CURRENT.k}\n- Source: ${CURRENT.s} | Provenance: ${CURRENT.p}\n- Cords: ${LAST_RES.nCords} (${LAST_RES.nKnotted} knotted), Total: ${LAST_RES.totVal}\n- Group-edge sums: ${LAST_RES.obsGrpSums} (p=${LAST_RES.pSum.toFixed(3)})\n- Two-color alt: ${LAST_RES.obsAlt} (p=${LAST_RES.pAlt.toFixed(3)})`;
  navigator.clipboard && navigator.clipboard.writeText(md);
});
$('btn-dl-json').addEventListener('click', () => {
  if (!CURRENT || !LAST_RES) return;
  const blob = new Blob([JSON.stringify({khipu:CURRENT, analysis:LAST_RES}, null, 2)], {type:'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = CURRENT.k + '_ficha.json'; a.click();
});

// Tema claro / oscuro compartido con el ensayo
(function tema(){
  const btn = $('tema-btn'), root = document.documentElement;
  const mq = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
  let g = null; try { g = localStorage.getItem('quipus-tema'); } catch (_) {}
  if (g === 'dark' || g === 'light') root.setAttribute('data-theme', g);
  const actual = () => root.getAttribute('data-theme') || (mq && mq.matches ? 'dark' : 'light');
  function pintar(){ const osc = actual() === 'dark'; btn.textContent = osc ? tl('Tema claro', 'Light theme') : tl('Tema oscuro', 'Dark theme'); btn.setAttribute('aria-pressed', String(osc)); }
  btn.addEventListener('click', () => { const n = actual() === 'dark' ? 'light' : 'dark'; root.setAttribute('data-theme', n); try { localStorage.setItem('quipus-tema', n); } catch (_) {} pintar(); });
  pintar();
})();

$('buscar').addEventListener('input', renderList);
$('filtro-fuente').addEventListener('change', renderList);
$('corpus-count').textContent = CORPUS.length;
renderList();
render(CORPUS.find(x => x.k === 'UR278') || CORPUS[0]);
})();
"""


def main():
    items = load_all_khipus()
    corpus_js = json.dumps(items, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    genres_js = json.dumps(GENRE_MAP, ensure_ascii=False, separators=(",", ":"))
    DEST.mkdir(parents=True, exist_ok=True)

    configs = [
        ("en", "lector.html", "Khipu Reader · Browser Edition",
         "Client-side statistical reader, knot-grammar auditor, and Bayesian corpus matcher across 682 khipus.",
         "Interactive tool · open to specialist review · zero server",
         "index.html", "← Back to essay", "lector.es.html", "Leer en español", "Dark theme",
         "khipus indexed", "Corpus (682)", "Your CSV", "Search ID, site, genre…", "All sources",
         "Drop a CSV file here or click to load", "cord,group,color,value\np1,0,W,120\n...",
         "Analyze CSV", "Load sample", "Copy Markdown", "Download JSON",
         "Hover or click any cord to inspect its transcription."),
        ("es", "lector.es.html", "Lector de Quipus · Edición en navegador",
         "Lector estadístico en el navegador, auditor de gramática de nudos y buscador bayesiano en 682 quipus.",
         "Herramienta interactiva · abierta a revisión especializada · sin servidor",
         "index.es.html", "← Volver al ensayo", "lector.html", "Read in English", "Tema oscuro",
         "quipus indexados", "Corpus (682)", "Tu CSV", "Buscar ID, sitio, género…", "Todas las fuentes",
         "Arrastra un archivo CSV aquí o haz clic para cargar", "cuerda,grupo,color,valor\np1,0,W,120\n...",
         "Analizar CSV", "Cargar ejemplo", "Copiar Markdown", "Descargar JSON",
         "Pasa el cursor o haz clic en cualquier cuerda para ver su transcripción."),
    ]
    for (lang, fname, title, desc, kicker, essay, back, other, other_l, dark_l,
         corp_l, tab_c, tab_u, s_ph, all_s, drop_t, p_ph, ana_b, smp_b, cp_m, dl_j, h_tip) in configs:
        html = (HTML_HEAD
                .replace("__LANG__", lang)
                .replace("__TITLE__", title)
                .replace("__DESC__", desc)
                .replace("__KICKER__", kicker)
                .replace("__ESSAY__", essay)
                .replace("__BACK_ESSAY__", back)
                .replace("__OTHER_HTML__", other)
                .replace("__OTHER_LANG__", other_l)
                .replace("__DARK_LBL__", dark_l)
                .replace("__CORPUS_LBL__", corp_l)
                .replace("__TAB_CORPUS__", tab_c)
                .replace("__TAB_CUSTOM__", tab_u)
                .replace("__SEARCH_PH__", s_ph)
                .replace("__ALL_SRC__", all_s)
                .replace("__DROP_TXT__", drop_t)
                .replace("__PASTE_PH__", p_ph)
                .replace("__ANALYZE_BTN__", ana_b)
                .replace("__SAMPLE_BTN__", smp_b)
                .replace("__COPY_MD__", cp_m)
                .replace("__DL_JSON__", dl_j)
                .replace("__HOVER_TIP__", h_tip)
                .replace("__CORPUS__", corpus_js)
                .replace("__GENRES__", genres_js)
                .replace("__JS__", JS_APP))
        out = DEST / fname
        out.write_text(html, encoding="utf-8", newline="\n")
        print(f"{out} {round(len(html.encode('utf-8')) / 1024)} KB ({len(items)} quipus)")


if __name__ == "__main__":
    main()
