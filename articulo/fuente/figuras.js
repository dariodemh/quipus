(function(){
'use strict';
const NS = 'http://www.w3.org/2000/svg';
const D = DATOS;
// textos de las figuras: tl('español', 'English') según el idioma de la página
const EN = document.documentElement.lang === 'en';
const tl = (es, en) => EN ? en : es;
// niveles de evidencia tal como vienen en los datos
const NIVEL = s => EN ? s.replace('bien apoyado', 'well supported').replace('apoyado', 'supported').replace('propuesto', 'proposed').replace('entre museos', 'across museums') : s;
const REDUCIR = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function el(tag, a, parent){
  const e = document.createElementNS(NS, tag);
  if (a) for (const k in a){ if (k === 'style') e.setAttribute('style', a[k]); else e.setAttribute(k, a[k]); }
  if (parent) parent.appendChild(e);
  return e;
}
function tx(parent, x, y, s, a){ const t = el('text', Object.assign({x, y}, a || {}), parent); t.textContent = s; return t; }
function limpiar(svg){ while (svg.firstChild) svg.removeChild(svg.firstChild); }
const $ = id => document.getElementById(id);
const fmt = n => (n === null || n === undefined || Number.isNaN(n)) ? '·' : String(n);
function espera(ms){ return new Promise(r => setTimeout(r, REDUCIR ? 0 : ms)); }

// colores de cuerda según el código del transcriptor
const CC = {W:'#f4f0e6',AB:'#b58d5c',MB:'#7d5636',DB:'#4b3220',LB:'#cdab7d',YB:'#c9a54e',NB:'#a07c58',KB:'#3a2a20',
  RL:'#c4574f',RB:'#8e3b2f',R:'#b33a2e',PK:'#e3a6b6',B:'#3c4f9e',G:'#4f7d4f',Y:'#d9b43a',GR:'#8d8a84',BS:'#5f6a8a',HB:'#8a6d4b',FR:'#a66a50',SR:'#b9502f'};
function colorCuerda(code){ const c = String(code || '').split(':')[0].split('-')[0]; return CC[c] || '#9a7b5a'; }

// dibuja una cuerda colgante con sus nudos a escala; devuelve los nudos con su posición
function cuerda(g, x, y0, c, sc, op){
  op = op || {};
  const pos = c.k.map(k => k[2]).filter(p => p !== null);
  const paso = op.paso || 4.6, r = op.r || 2.3, er = op.r ? op.r + .6 : 2.8;
  const alto = (n, t) => t === 'S' ? (n - 1) * paso + 2 * r : t === 'L' ? 4 + n * (op.vuelta || 3.1) : 4 * er;
  // cada nudo va en su posición, pero nunca encima del anterior ni de la cuerda principal
  let fondo = y0 + 2;
  const ys = c.k.map(([n, t, p]) => {
    if (p === null) return null;
    const h = alto(n, t), arriba = Math.max(y0 + p * sc - h / 2, fondo + 2);
    fondo = arriba + h;
    return arriba + h / 2;
  });
  const largo = Math.max((c.l || (Math.max(0, ...pos) + 8)) * sc, fondo - y0 + 6);
  const col = colorCuerda(c.col);
  el('line', {x1:x, y1:y0, x2:x, y2:y0 + largo, style:'stroke:var(--regla);stroke-width:' + ((op.w || 3) + 2) + ';stroke-linecap:round'}, g);
  el('line', {x1:x, y1:y0, x2:x, y2:y0 + largo, style:'stroke:' + col + ';stroke-width:' + (op.w || 3) + ';stroke-linecap:round'}, g);
  const out = [];
  c.k.forEach((k, j) => {
    const [n, t, p, v] = k; if (p === null) return;
    const y = ys[j], kg = el('g', null, g);
    const tinta = 'fill:var(--tinta)';
    if (t === 'S'){
      for (let i = 0; i < n; i++) el('circle', {cx:x, cy:y + (i - (n - 1) / 2) * paso, r, style:tinta}, kg);
    } else if (t === 'L'){
      const h = 4 + n * (op.vuelta || 3.1), w = op.lw || 8;
      el('rect', {x:x - w / 2, y:y - h / 2, width:w, height:h, rx:w / 2, style:tinta}, kg);
      for (let i = 1; i < n; i++){ const yy = y - h / 2 + i * h / n; el('line', {x1:x - w / 2 + 1, y1:yy - 1.5, x2:x + w / 2 - 1, y2:yy + 1.5, style:'stroke:var(--tarjeta);stroke-width:1.1'}, kg); }
    } else if (t === 'E'){
      el('circle', {cx:x, cy:y - er, r:er, style:'fill:none;stroke:var(--tinta);stroke-width:1.8'}, kg);
      el('circle', {cx:x, cy:y + er, r:er, style:'fill:none;stroke:var(--tinta);stroke-width:1.8'}, kg);
    }
    out.push({y, n, t, v, g:kg});
  });
  return {largo, nudos:out};
}

/* ---------- índice de tarjetas ---------- */
(function indice(){
  const H = [
    [1,tl('Una contabilidad en tres niveles', 'Accounts on three levels'),'d','Inkawasi','niveles'],[2,tl('Un segundo camino al mismo libro', 'A second route to the same ledger'),'a','Inkawasi','dos'],
    [3,tl('Nueve columnas fijas', 'Nine fixed columns'),'d','Inkawasi','nueve'],[4,tl('Los errores de los contadores', 'The accountants\' mistakes'),'a','Inkawasi','nudo'],
    [5,tl('Cuánto se guardaba', 'How much was stored'),'p','Inkawasi','escala'],[6,tl('Copias de un museo a otro', 'Copies from one museum to another'),'d','Corpus','red'],
    [7,tl('Una tabla de tres niveles en la costa sur', 'A three-level table on the south coast'),'a','Corpus','bloques'],[8,tl('Tablas escritas con dos colores alternados', 'Tables written in two alternating colours'),'d','Corpus','alterna'],
    [9,tl('Cada quipu tiene su propia clave de colores', 'Each khipu has its own colour key'),'a','Corpus','colores'],[10,tl('Maneras recurrentes de armar una tabla', 'Recurring ways to build a table'),'d','Corpus','tabla'],
    [11,tl('Un formulario con reparto fijo', 'A form with a fixed split'),'a','Corpus','reparto'],[12,tl('Los quipus como sistema de registros', 'Khipus as a system of records'),'a','Corpus','mosaico']];
  const NOM = {d:tl('Bien apoyado', 'Well supported'), a:tl('Apoyado', 'Supported'), p:tl('Propuesto', 'Proposed')};
  const cont = $('indice');
  let grupo = '';
  H.forEach(([n, t, ev, gr, ic]) => {
    if (gr !== grupo){ grupo = gr; const d = document.createElement('div'); d.className = 'grupo'; d.textContent = gr === 'Inkawasi' ? tl('En Inkawasi', 'At Inkawasi') : tl('En todo el corpus', 'Across the corpus'); cont.appendChild(d); }
    const a = document.createElement('a'); a.className = 'tarjeta' + (n === 1 ? ' grande' : ''); a.href = '#h' + n;
    const svg = el('svg', {viewBox:'0 0 200 46', 'aria-hidden':'true'}); a.appendChild(svg); glifo(svg, ic);
    const s1 = document.createElement('span'); s1.className = 'n'; s1.textContent = tl('Hallazgo ', 'Finding ') + n; a.appendChild(s1);
    const s2 = document.createElement('span'); s2.className = 't'; s2.textContent = t; a.appendChild(s2);
    const s3 = document.createElement('span'); s3.className = 'ev ev-' + ev; s3.textContent = NOM[ev]; s3.style.alignSelf = 'flex-start'; a.appendChild(s3);
    cont.appendChild(a);
  });
  function glifo(s, ic){
    const L = 'stroke:var(--fibra);stroke-width:2;stroke-linecap:round', I = 'fill:var(--indigo)', F = 'fill:var(--fibra)';
    const linea = (x1,y1,x2,y2,st) => el('line', {x1,y1,x2,y2,style:st || L}, s);
    if (ic === 'niveles'){ [[10,36,70],[70,22,130],[130,8,190]].forEach(([a,y,b],i) => { el('rect',{x:a,y,width:b-a-10,height:8,rx:4,style:i===2?I:F},s); }); linea(55,36,95,26); linea(115,22,155,12); }
    else if (ic === 'dos'){ el('rect',{x:10,y:30,width:50,height:8,rx:4,style:F},s); el('rect',{x:10,y:8,width:50,height:8,rx:4,style:F},s); el('rect',{x:140,y:19,width:50,height:8,rx:4,style:I},s); linea(62,12,138,22); linea(62,34,138,24); }
    else if (ic === 'nueve'){ [44,42,34,36,36,40,36,30,32].forEach((h,i) => el('rect',{x:12+i*20,y:44-h*.9,width:12,height:h*.9,rx:2,style:i===0?I:F},s)); }
    else if (ic === 'nudo'){ linea(20,23,180,23); [60,70,80].forEach(x=>el('circle',{cx:x,cy:23,r:4,style:F},s)); el('rect',{x:110,y:17,width:30,height:12,rx:6,style:'fill:var(--cochinilla)'},s); }
    else if (ic === 'escala'){ linea(10,30,190,30); el('rect',{x:92,y:18,width:50,height:12,style:'fill:var(--indigo);opacity:.35'},s); [10,55,100,145,190].forEach(x=>linea(x,26,x,34)); }
    else if (ic === 'red'){ const P=[[30,12],[30,34],[100,23],[170,10],[170,36]]; [[0,2],[1,2],[2,3],[2,4],[3,4]].forEach(([a,b])=>linea(P[a][0],P[a][1],P[b][0],P[b][1],'stroke:var(--indigo);stroke-width:1.6')); P.forEach(p=>el('circle',{cx:p[0],cy:p[1],r:5,style:F},s)); }
    else if (ic === 'bloques'){ for (let r=0;r<3;r++) for (let c=0;c<9;c++) el('rect',{x:10+c*20,y:4+r*14,width:16,height:10,rx:2,style:(r===0&&c%3!==2)?I:F+';opacity:'+(r===0?1:.45)},s); }
    else if (ic === 'alterna'){ for (let i=0;i<14;i++) el('line',{x1:14+i*13,y1:4,x2:14+i*13,y2:42,style:'stroke:'+(i%2?CC.AB:'var(--regla)')+';stroke-width:5;stroke-linecap:round'},s); }
    else if (ic === 'colores'){ [[CC.W,CC.AB,CC.RL],[CC.RL,CC.W,CC.AB],[CC.AB,CC.RL,CC.W]].forEach((cs,i)=>cs.forEach((c,j)=>el('circle',{cx:30+i*70+j*14,cy:23,r:6,style:'fill:'+c+';stroke:var(--regla)'},s))); }
    else if (ic === 'tabla'){ [20,26,14,22].forEach((h,i)=>el('rect',{x:20+i*18,y:42-h,width:10,height:h,rx:2,style:F},s)); el('rect',{x:100,y:4,width:10,height:38,rx:2,style:I},s); [30,18,22].forEach((h,i)=>el('rect',{x:135+i*18,y:42-h,width:10,height:h,rx:2,style:i===0?I:F},s)); }
    else if (ic === 'reparto'){ for (let r=0;r<3;r++){ let x=10; [[.64,'var(--regla)'],[.19,CC.RL],[.17,CC.AB]].forEach(([f,c])=>{ el('rect',{x,y:4+r*14,width:f*180,height:10,style:'fill:'+c},s); x+=f*180; }); } }
    else if (ic === 'mosaico'){ const cs=['var(--indigo)','var(--fibra)','#2c7a6b','#b07a1e','var(--regla)']; for (let r=0;r<4;r++) for (let c=0;c<18;c++) el('rect',{x:10+c*10.2,y:3+r*10.5,width:8.5,height:8.5,rx:1.5,style:'fill:'+cs[(c*7+r*3)%5]},s); }
  }
})();

/* ---------- figura 1: la cuerda ---------- */
(function figCuerda(){
  const svg = $('svg-cuerda'), c = D.ej415, sc = 6, x = 170, y0 = 40;
  el('line', {x1:40, y1:y0, x2:300, y2:y0, style:'stroke:var(--fibra);stroke-width:6;stroke-linecap:round'}, svg);
  tx(svg, 40, 26, tl('cuerda principal', 'primary cord'), {class:'g', 'font-size':12});
  const r = cuerda(svg, x, y0, c, sc, {w:4, paso:6, r:3, vuelta:4, lw:11});
  const nombres = {1000:tl('millares', 'thousands'), 100:tl('centenas', 'hundreds'), 10:tl('decenas', 'tens'), 1:tl('unidades', 'units')};
  const filas = [];
  r.nudos.forEach((k, i) => {
    const lugar = k.v >= 100 ? 100 : k.v >= 10 ? 10 : 1;
    const desc = k.t === 'S' ? (k.n + (k.n > 1 ? tl(' nudos simples', ' single knots') : tl(' nudo simple', ' single knot'))) : k.t === 'L' ? tl('nudo largo de ', 'long knot of ') + k.n + tl(' vueltas', ' turns') : tl('figura de ocho', 'figure-eight knot');
    const gg = el('g', {style:'cursor:pointer', tabindex:0}, svg);
    el('rect', {x:x - 26, y:k.y - 18, width:52, height:36, rx:6, style:'fill:var(--indigo);opacity:0'}, gg);
    el('line', {x1:x + 18, y1:k.y, x2:330, y2:k.y, style:'stroke:var(--regla);stroke-dasharray:3 3'}, gg);
    const t1 = tx(gg, 340, k.y - 3, desc, {'font-size':15});
    const t2 = tx(gg, 340, k.y + 16, nombres[lugar] + ' · vale ' + k.v, {class:'g m', 'font-size':13});
    const t3 = tx(gg, 590, k.y + 6, String(k.v), {'text-anchor':'end', class:'m', 'font-size':24, style:'fill:var(--indigo)'});
    filas.push({gg, t3, k});
    const on = () => { filas.forEach(f => { f.gg.style.opacity = f.gg === gg ? 1 : .35; }); };
    const off = () => filas.forEach(f => f.gg.style.opacity = 1);
    gg.addEventListener('mouseenter', on); gg.addEventListener('focus', on); gg.addEventListener('click', on);
    gg.addEventListener('mouseleave', off); gg.addEventListener('blur', off);
  });
  el('line', {x1:340, y1:288, x2:590, y2:288, style:'stroke:var(--tinta);stroke-width:1'}, svg);
  tx(svg, 340, 314, r.nudos.map(k => k.v).join(' + ') + ' =', {'font-size':17, class:'m'});
  tx(svg, 590, 316, String(c.v), {'text-anchor':'end', class:'m', 'font-size':28, style:'fill:var(--indigo);font-weight:500'});
  tx(svg, x - 14, y0 + r.largo + 18, c.c + ' · color ' + c.col, {'font-size':12, class:'g', 'text-anchor':'middle'});
})();

/* ---------- figura 2: prueba de permutación ---------- */
(function figAzar(){
  const svg = $('svg-azar'), out = $('azar-salida');
  const CASOS = {con:[57,12,20,25,64,30,14,20,33,9,11,13], sin:[14,23,8,31,12,19,27,9,16,22,11,25]};
  let caso = 'con', corriendo = false;
  const cuenta = v => { let n = 0; for (let i = 0; i + 3 < v.length; i++) if (v[i] === v[i+1] + v[i+2] + v[i+3]) n++; return n; };
  function barajar(v){ const a = v.slice(); for (let i = a.length - 1; i > 0; i--){ const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
  let gCuerdas, gHist, hist;
  function base(){
    limpiar(svg); hist = [0,0,0,0,0];
    el('line', {x1:30, y1:20, x2:610, y2:20, style:'stroke:var(--fibra);stroke-width:5;stroke-linecap:round'}, svg);
    gCuerdas = el('g', null, svg); gHist = el('g', null, svg);
    pintar(CASOS[caso], true);
    el('line', {x1:60, y1:330, x2:600, y2:330, style:'stroke:var(--regla)'}, svg);
    for (let k = 0; k <= 4; k++) tx(svg, 110 + k * 110, 348, k + (k === 1 ? tl(' suma', ' sum') : tl(' sumas', ' sums')), {'text-anchor':'middle', 'font-size':12, class:'g'});
    tx(svg, 330, 368, tl('cuántos de los 300 barajados encontraron 0, 1, 2… sumas', 'how many of the 300 shuffles found 0, 1, 2… sums'), {'text-anchor':'middle', 'font-size':11, class:'g'});
    const obs = cuenta(CASOS[caso]); let mayores = 0;
    for (let i = 0; i < 300; i++){ const n = cuenta(barajar(CASOS[caso])); hist[Math.min(4, n)]++; if (n >= obs) mayores++; }
    histo(true);
    out.textContent = tl('Sumas en los datos reales: ', 'Sums in the real data: ') + obs + tl('. Barajados con ', '. Shuffles with ') + obs + tl(' o más: ', ' or more: ') + mayores + tl(' de 300.', ' of 300.');
  }
  function pintar(v, real){
    limpiar(gCuerdas);
    v.forEach((n, i) => {
      const x = 55 + i * 48, h = 18 + n * 1.2;
      el('line', {x1:x, y1:22, x2:x, y2:22 + h, style:'stroke:' + (real ? 'var(--fibra)' : 'var(--gris)') + ';stroke-width:4;stroke-linecap:round'}, gCuerdas);
      tx(gCuerdas, x, 22 + h + 16, String(n), {'text-anchor':'middle', class:'m', 'font-size':13});
    });
    if (real) for (let i = 0; i + 3 < v.length; i++) if (v[i] === v[i+1] + v[i+2] + v[i+3]){
      const x = 55 + i * 48;
      el('path', {d:'M' + x + ' 150 q 72 22 144 0', style:'fill:none;stroke:var(--indigo);stroke-width:2'}, gCuerdas);
      tx(gCuerdas, x + 72, 176, 'total', {'text-anchor':'middle', 'font-size':11, style:'fill:var(--indigo)'});
    }
  }
  function histo(final){
    limpiar(gHist);
    const mx = Math.max(...hist, 1), obs = Math.min(4, cuenta(CASOS[caso]));
    hist.forEach((h, k) => { const alto = h / mx * 80; el('rect', {x:85 + k * 110, y:330 - alto, width:50, height:alto, rx:3, style:'fill:var(--fibra);opacity:.55'}, gHist);
      // si la línea de los datos reales cae en esta barra, el número va a un lado para no taparse
      if (h) tx(gHist, 110 + k * 110 - (final && k === obs ? 14 : 0), 326 - alto, String(h), {'text-anchor':final && k === obs ? 'end' : 'middle', 'font-size':11, class:'g m'}); });
    if (final){
      const x = 110 + obs * 110, izq = obs === 4;
      el('line', {x1:x, y1:206, x2:x, y2:332, style:'stroke:var(--indigo);stroke-width:3'}, gHist);
      tx(gHist, x + (izq ? -8 : 8), 216, tl('datos reales: ', 'real data: ') + cuenta(CASOS[caso]) + (cuenta(CASOS[caso]) === 1 ? tl(' suma', ' sum') : tl(' sumas', ' sums')), {'text-anchor':izq ? 'end' : 'start', 'font-size':12, style:'fill:var(--indigo);font-weight:600'});
    }
  }
  async function jugar(){
    if (corriendo) return; corriendo = true; hist = [0,0,0,0,0];
    const obs = cuenta(CASOS[caso]); let mayores = 0;
    for (let i = 0; i < 300; i++){
      const b = barajar(CASOS[caso]), n = Math.min(4, cuenta(b)); hist[n]++; if (cuenta(b) >= obs) mayores++;
      if (i % 6 === 0){ pintar(b, false); histo(false); out.textContent = tl('Barajado ', 'Shuffle ') + (i + 1) + tl(' de 300', ' of 300'); await espera(16); }
    }
    pintar(CASOS[caso], true); histo(true);
    out.textContent = tl('Sumas en los datos reales: ', 'Sums in the real data: ') + obs + tl('. Barajados con ', '. Shuffles with ') + obs + tl(' o más: ', ' or more: ') + mayores + tl(' de 300.', ' of 300.');
    corriendo = false;
  }
  document.querySelectorAll('#fig-azar [data-caso]').forEach(b => b.addEventListener('click', () => {
    if (corriendo) return; caso = b.dataset.caso;
    document.querySelectorAll('#fig-azar [data-caso]').forEach(x => x.setAttribute('aria-pressed', x === b)); base();
  }));
  $('azar-jugar').addEventListener('click', jugar);
  base();
})();

/* ---------- figura 3: prueba a ciegas ---------- */
(function figCiegas(){
  const svg = $('svg-ciegas'), out = $('ciegas-salida');
  const mal = new Set([3, 11, 17, 22, 30, 36, 41, 47, 52, 58, 61, 66]);  // 12 fallos, 56 aciertos
  const pts = [];
  for (let i = 0; i < 68; i++){
    const x = 28 + (i % 17) * 34, y = 28 + Math.floor(i / 17) * 36;
    pts.push(el('circle', {cx:x, cy:y, r:11, style:'fill:' + (mal.has(i) ? 'var(--mal)' : 'var(--ok)') + ';stroke:none'}, svg));
  }
  out.textContent = tl('56 exactas de 68 (82 %)', '56 exact out of 68 (82%)');
  let corriendo = false;
  $('ciegas-jugar').addEventListener('click', async () => {
    if (corriendo) return; corriendo = true; let ok = 0;
    pts.forEach(p => p.setAttribute('style', 'fill:var(--suave);stroke:var(--regla)'));
    for (let i = 0; i < 68; i++){
      const bien = !mal.has(i); if (bien) ok++;
      pts[i].setAttribute('style', 'fill:' + (bien ? 'var(--ok)' : 'var(--mal)') + ';stroke:none');
      out.textContent = ok + tl(' exactas de ', ' exact out of ') + (i + 1); await espera(35);
    }
    out.textContent = tl('56 exactas de 68 (82 %)', '56 exact out of 68 (82%)'); corriendo = false;
  });
})();

/* ---------- figura 4: mapa ---------- */
(function figMapa(){
  const svg = $('svg-mapa');
  // equirectangular con la misma escala en los dos ejes (a 10° S la diferencia es menor al 2 %)
  const K = 27.5, X = lon => 60 + (lon + 82) * K, Y = lat => 12 + (1 - lat) * K;
  const camino = anillos => anillos.map(a => 'M' + a.map(p => X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join('L') + 'Z').join('');
  el('path', {d:camino(D.vecinos), style:'fill:var(--papel);stroke:var(--regla);stroke-width:1;stroke-linejoin:round'}, svg);
  el('path', {d:camino(D.peru), style:'fill:var(--suave);stroke:var(--fibra);stroke-width:1.4;stroke-linejoin:round'}, svg);
  const rot = (s, lo, la, a) => tx(svg, X(lo), Y(la), s, Object.assign({'text-anchor':'middle', 'font-size':11, 'letter-spacing':'.18em', style:'fill:var(--gris)'}, a || {}));
  rot('ECUADOR', -78.6, -1.4); rot('COLOMBIA', -72.5, 0.2); rot(tl('BRASIL', 'BRAZIL'), -68.2, -8.5); rot('BOLIVIA', -66.8, -15.6); rot('CHILE', -69.4, -18.6);
  rot(tl('PERÚ', 'PERU'), -74.4, -9.6, {'font-size':16, 'letter-spacing':'.3em', style:'fill:var(--fibra);font-weight:600'});
  tx(svg, X(-81.6), Y(-16.6), tl('Océano Pacífico', 'Pacific Ocean'), {'font-size':13, style:'font-style:italic;fill:var(--gris)'});
  // [nombre, lat, lon, dx, dy, anclaje, destacado]
  const S = [
    ['Inkawasi (Lunahuaná, Cañete)', -12.96, -76.12, -10, 22, 'end', 1], ['Lima', -12.05, -77.04, -10, 4, 'end', 0],
    ['Puruchuco', -12.03, -76.93, 10, -6, 'start', 0], ['Pachacamac', -12.26, -76.90, -10, 15, 'end', 0],
    [tl('Valle del Santa', 'Santa Valley'), -8.9, -78.5, -10, 4, 'end', 0], ['Leymebamba', -6.71, -77.80, 10, 4, 'start', 0],
    ['Bambamarca', -6.68, -78.52, -10, 4, 'end', 0], ['Ica', -14.07, -75.73, 10, 4, 'start', 0], ['Nazca', -14.83, -74.94, 10, 4, 'start', 0],
    ['Cusco', -13.53, -71.97, 10, 4, 'start', 0]];
  S.forEach(([n, la, lo, dx, dy, an, fuerte]) => {
    const x = X(lo), y = Y(la);
    el('circle', {cx:x, cy:y, r:fuerte ? 6 : 3.5, style:'fill:' + (fuerte ? 'var(--cochinilla)' : 'var(--tinta)') + ';stroke:var(--tarjeta);stroke-width:1.5'}, svg);
    tx(svg, x + dx, y + dy, n, {'text-anchor':an, 'font-size':fuerte ? 15 : 13, style:'paint-order:stroke;stroke:var(--suave);stroke-width:3px;stroke-linejoin:round;' + (fuerte ? 'font-weight:600;fill:var(--cochinilla)' : 'fill:var(--tinta)')});
  });
})();

/* ---------- figura 5: el archivo ---------- */
(function figArchivo(){
  const svg = $('svg-archivo'), out = $('archivo-salida');
  const N = {
    UR270:[420,400,'UR270',tl('detalle', 'detail'),tl('9 unidades × 2 partes', '9 units × 2 parts')], UR278:[200,250,'UR278',tl('tabla de 9 columnas', '9-column table'),tl('suma por unidad', 'sum by unit')],
    UR273B:[480,250,'UR273B',tl('suma de las partes B', 'sum of the B parts'),tl('copia: UR274B, cuota 17', 'copy: UR274B, quota 17')], UR273A:[700,250,'UR273A',tl('suma de las partes A', 'sum of the A parts'),tl('copia: UR274A, cuota 30', 'copy: UR274A, quota 30')],
    UR275:[340,85,'UR275',tl('libro, copia 1', 'ledger, copy 1'),tl('total, cuota 47, reparto', 'total, quota 47, split')], UR266:[600,85,'UR266',tl('libro, copia 2', 'ledger, copy 2'),tl('total y cuota 47', 'total and quota 47')],
    UR269:[860,85,'UR269',tl('libro lateral', 'side ledger'),''], UR268:[860,160,'UR268',tl('libro lateral', 'side ledger'),tl('cuota 208', 'quota 208')]};
  const grises = ['UR272','UR277','UR276','UR279'];
  const C = {d:'var(--ev-d)', a:'var(--ev-a)', p:'var(--ev-p)', c:'var(--gris)'};
  const E = [
    ['UR270','UR278','d',tl('Si a cada cuerda de UR270 se le suma su subsidiaria, salen las celdas de UR278.', 'Adding each UR270 cord to its subsidiary gives the cells of UR278.')],
    ['UR270','UR273B','d',tl('La suma de los colgantes de un registro de UR270 da la cabecera de UR273B.', 'The sum of the pendants of a UR270 record gives the header of UR273B.')],
    ['UR270','UR273A','a',tl('La suma de las subsidiarias da la cabecera de UR273A, con diferencias de uno.', 'The sum of the subsidiaries gives the header of UR273A, with differences of one.')],
    ['UR278','UR275','d',tl('Los totales de fila de UR278 reaparecen en orden en el libro.', 'The row totals of UR278 reappear in order in the ledger.')],
    ['UR278','UR266','d',tl('Y en la otra copia del libro, UR266, con once coincidencias en orden.', 'And in the other copy of the ledger, UR266, with eleven matches in order.')],
    ['UR273A','UR275','a',tl('UR273A + UR273B, registro a registro, llega a las mismas cabeceras por otro camino.', 'UR273A + UR273B, record by record, reaches the same headers by another route.')],
    ['UR273B','UR275','a',''],
    ['UR275','UR266','c',tl('UR266 y UR275 son copias, como ya habían mostrado Urton y Chu.', 'UR266 and UR275 are copies, as Urton and Chu had already shown.')]];
  const flechas = [];
  const def = el('defs', null, svg);
  Object.entries(C).forEach(([k, c]) => { const m = el('marker', {id:'pt-' + k, viewBox:'0 0 10 10', refX:9, refY:5, markerWidth:7, markerHeight:7, orient:'auto-start-reverse'}, def); el('path', {d:'M0 0L10 5L0 10z', style:'fill:' + c}, m); });
  E.forEach(([a, b, ev, txt]) => {
    const [x1, y1] = N[a], [x2, y2] = N[b];
    const sube = y2 < y1, yy1 = y1 + (sube ? -28 : (y2 > y1 ? 28 : 0)), yy2 = y2 + (sube ? 30 : (y2 > y1 ? -30 : 0));
    const xx1 = y1 === y2 ? x1 + (x2 > x1 ? 80 : -80) : x1, xx2 = y1 === y2 ? x2 + (x2 > x1 ? -80 : 80) : x2;
    const p = el('path', {d:'M' + xx1 + ' ' + yy1 + 'L' + xx2 + ' ' + yy2, style:'fill:none;stroke:' + C[ev] + ';stroke-width:' + (ev === 'c' ? 1.5 : 3) + (ev === 'c' ? ';stroke-dasharray:5 4' : ''), 'marker-end':ev === 'c' ? '' : 'url(#pt-' + ev + ')'}, svg);
    flechas.push({p, txt, ev});
  });
  Object.values(N).forEach(([x, y, n, s, s2]) => {
    const lateral = n === 'UR269' || n === 'UR268';
    el('rect', {x:x - 80, y:y - 28, width:160, height:56, rx:8, style:'fill:var(--tarjeta);stroke:' + (lateral ? 'var(--regla)' : 'var(--fibra)') + ';stroke-width:1.5'}, svg);
    tx(svg, x, y - 8, n, {'text-anchor':'middle', 'font-size':15, class:'m', style:'font-weight:500'});
    tx(svg, x, y + 8, s, {'text-anchor':'middle', 'font-size':11.5});
    if (s2) tx(svg, x, y + 22, s2, {'text-anchor':'middle', 'font-size':10.5, class:'g'});
  });
  grises.forEach((n, i) => { const x = 660 + i * 70, y = 410; el('rect', {x:x - 30, y:y - 14, width:60, height:28, rx:6, style:'fill:var(--suave);stroke:var(--regla)'}, svg); tx(svg, x, y + 5, n, {'text-anchor':'middle', 'font-size':12, class:'g m'}); });
  [[tl('Nivel 2', 'Level 2'), tl('libro', 'ledger'), 85], [tl('Nivel 1', 'Level 1'), tl('resúmenes', 'summaries'), 250], [tl('Nivel 0', 'Level 0'), tl('detalle', 'detail'), 400]].forEach(([t, t2, y]) => { tx(svg, 10, y - 2, t, {'font-size':12, style:'font-weight:600;fill:var(--fibra)'}); tx(svg, 10, y + 14, t2, {'font-size':11.5, class:'g'}); });
  tx(svg, 765, 380, tl('fuera de la cuenta', 'outside the account'), {'text-anchor':'middle', 'font-size':11, class:'g'});
  const ley = [['d',tl('bien apoyado', 'well supported')],['a',tl('apoyado', 'supported')],['c',tl('copia', 'copy')]];
  ley.forEach(([k, t], i) => { const x = 160 + i * 120; el('line', {x1:x, y1:455, x2:x + 26, y2:455, style:'stroke:' + C[k] + ';stroke-width:3' + (k === 'c' ? ';stroke-dasharray:5 4' : '')}, svg); tx(svg, x + 32, 459, t, {'font-size':12}); });
  let corriendo = false;
  $('archivo-jugar').addEventListener('click', async () => {
    if (corriendo) return; corriendo = true;
    flechas.forEach(f => f.p.style.opacity = .12);
    for (const f of flechas){ f.p.style.opacity = 1; if (f.txt) out.textContent = f.txt; await espera(f.txt ? 1500 : 300); }
    out.textContent = tl('Dos caminos llegan al mismo libro.', 'Two routes reach the same ledger.'); corriendo = false;
  });
})();

/* ---------- figura 6: celdas UR270 → UR278 ---------- */
(function figCeldas(){
  const svg = $('svg-celdas'), tabs = $('celdas-tabs');
  const pares = D.ur270.filter(g => g.destino !== null);
  const filas = Object.fromEntries(D.ur278.map(f => [f.g, f]));
  const X = i => 150 + i * 92, sc = 3.1;
  function dibujar(par){
    limpiar(svg);
    const fila = filas[par.destino];
    const cols = [];
    // UR270 arriba
    el('line', {x1:110, y1:26, x2:X(8) + 40, y2:26, style:'stroke:var(--fibra);stroke-width:5;stroke-linecap:round'}, svg);
    tx(svg, 10, 30, 'UR270', {'font-size':15, class:'m', style:'font-weight:500'}); tx(svg, 10, 48, tl('grupo ', 'group ') + par.g, {'font-size':12, class:'g'});
    // UR278 abajo
    el('line', {x1:110, y1:330, x2:X(8) + 40, y2:330, style:'stroke:var(--fibra);stroke-width:5;stroke-linecap:round'}, svg);
    tx(svg, 10, 334, 'UR278', {'font-size':15, class:'m', style:'font-weight:500'}); tx(svg, 10, 352, tl('fila ', 'row ') + fila.g, {'font-size':12, class:'g'});
    const R = [tl('colgante', 'pendant'), tl('subsidiaria', 'subsidiary'), tl('suma', 'sum'), 'UR278'];
    R.forEach((r, i) => tx(svg, 10, 216 + i * 22, r, {'font-size':12, class:'g'}));
    let ok = 0;
    par.cel.forEach((c, i) => {
      const x = X(i), g = el('g', {tabindex:0, style:'cursor:pointer'}, svg);
      const fondo = el('rect', {x:x - 40, y:6, width:80, height:508, rx:8, style:'fill:var(--indigo);opacity:0'}, g);
      cuerda(g, x - 8, 26, c.P, sc, {w:3, paso:3.6, r:1.8, vuelta:2.4, lw:6});
      if (c.S){ el('path', {d:'M' + (x - 8) + ' 34 q 8 2 14 10', style:'fill:none;stroke:' + colorCuerda(c.S.col) + ';stroke-width:2'}, g);
        cuerda(g, x + 6, 44, c.S, sc, {w:2, paso:3.6, r:1.8, vuelta:2.4, lw:6}); }
      const cel = fila.cel[i];
      cuerda(g, x, 330, cel, sc, {w:3, paso:3.6, r:1.8, vuelta:2.4, lw:6});
      const suma = par.suma[i], v = cel.v, dif = (v === null || v === undefined) ? null : v - suma;
      const col = dif === 0 ? 'var(--ok)' : (dif !== null && Math.abs(dif) === 1) ? 'var(--casi)' : 'var(--mal)';
      if (dif === 0) ok++;
      tx(g, x, 216, fmt(c.P.v), {'text-anchor':'middle', class:'m', 'font-size':13});
      tx(g, x, 238, c.S ? '+ ' + fmt(c.S.v) : '·', {'text-anchor':'middle', class:'m', 'font-size':13});
      tx(g, x, 260, '= ' + suma, {'text-anchor':'middle', class:'m', 'font-size':14, style:'font-weight:500'});
      tx(g, x, 282, fmt(v), {'text-anchor':'middle', class:'m', 'font-size':14, style:'font-weight:500;fill:' + col});
      el('circle', {cx:x, cy:300, r:4, style:'fill:' + col}, g);
      cols.push({g, fondo});
      const on = () => cols.forEach(o => { o.fondo.style.opacity = o.g === g ? .08 : 0; o.g.style.opacity = o.g === g ? 1 : .45; });
      const off = () => cols.forEach(o => { o.fondo.style.opacity = 0; o.g.style.opacity = 1; });
      g.addEventListener('mouseenter', on); g.addEventListener('focus', on); g.addEventListener('click', on);
      g.addEventListener('mouseleave', off); g.addEventListener('blur', off);
    });
    tx(svg, 10, 304, ok + tl(' de 9 exactas', ' of 9 exact'), {'font-size':12.5, style:'fill:var(--ok);font-weight:600'});
  }
  pares.forEach((p, i) => {
    const b = document.createElement('button'); b.className = 'boton'; b.textContent = tl('grupo ', 'group ') + p.g + tl(' → fila ', ' → row ') + p.destino;
    b.setAttribute('aria-pressed', i === 0); b.addEventListener('click', () => { tabs.querySelectorAll('.boton').forEach(x => x.setAttribute('aria-pressed', x === b)); dibujar(p); });
    tabs.appendChild(b);
  });
  dibujar(pares[0]);
})();

/* ---------- figura 7: totales al libro ---------- */
(function figCadena(){
  const svg = $('svg-cadena'), out = $('cadena-salida');
  const T = D.totales.slice().sort((a, b) => a.g - b.g);
  const destino = (s, q) => { const m = s.match(new RegExp(q + ' g(\\d+)=(\\d+)(?: \\(([+-]\\d+)\\))?')); return m ? {g:+m[1], v:+m[2], d:m[3] ? +m[3] : 0} : null; };
  const Y = i => 30 + i * 14.6, Y66 = g => 30 + (g - 1) * 15.3, Y75 = g => 50 + (g - 1) * 20;
  tx(svg, 200, 16, tl('UR278, total de fila', 'UR278, row total'), {'text-anchor':'end', 'font-size':12, class:'g'});
  tx(svg, 560, 16, 'UR266', {'text-anchor':'middle', 'font-size':12, class:'g'});
  tx(svg, 840, 16, 'UR275', {'text-anchor':'middle', 'font-size':12, class:'g'});
  const lineas = [], vistos66 = {}, vistos75 = {}, sinDestino = [], FILA = tl('fila ', 'row ');
  T.forEach((t, i) => {
    const y = Y(i), d66 = destino(t.enlace, 'UR266'), d75 = destino(t.enlace, 'UR275');
    tx(svg, 120, y + 4, FILA + t.g, {'text-anchor':'end', 'font-size':11, class:'g'});
    tx(svg, 200, y + 4, String(t.v), {'text-anchor':'end', class:'m', 'font-size':12.5});
    const color = d => !d ? 'var(--regla)' : d.d === 0 ? 'var(--ok)' : Math.abs(d.d) === 1 ? 'var(--casi)' : 'var(--mal)';
    if (d66){
      const y2 = Y66(d66.g);
      const p = el('path', {d:'M208 ' + y + ' C 380 ' + y + ', 380 ' + y2 + ', 515 ' + y2, style:'fill:none;stroke:' + color(d66) + ';stroke-width:2;opacity:0'}, svg);
      lineas.push(p);
      if (!vistos66[d66.g]){ vistos66[d66.g] = 1; tx(svg, 520, y2 + 4, 'g' + d66.g, {'font-size':10.5, class:'g'}); tx(svg, 600, y2 + 4, String(d66.v), {'text-anchor':'end', class:'m', 'font-size':12.5}); }
      if (d75){
        const y3 = Y75(d75.g);
        const p2 = el('path', {d:'M606 ' + y2 + ' C 720 ' + y2 + ', 720 ' + y3 + ', 800 ' + y3, style:'fill:none;stroke:' + color(d75) + ';stroke-width:1.5;stroke-dasharray:4 3;opacity:0'}, svg);
        lineas.push(p2);
        if (!vistos75[d75.g]){ vistos75[d75.g] = 1; tx(svg, 805, y3 + 4, 'g' + d75.g, {'font-size':10.5, class:'g'}); tx(svg, 885, y3 + 4, String(d75.v), {'text-anchor':'end', class:'m', 'font-size':12.5}); }
      }
    } else sinDestino.push(y);
  });
  // al final, para que queden encima de la línea que cruza
  sinDestino.forEach(y => tx(svg, 214, y + 4, tl('sin destino conservado', 'no surviving destination'), {'font-size':10.5, class:'g', style:'fill:var(--gris);font-style:italic;paint-order:stroke;stroke:var(--tarjeta);stroke-width:4px;stroke-linejoin:round'}));
  const mostrar = () => lineas.forEach(l => l.style.opacity = 1);
  let corriendo = false;
  $('cadena-jugar').addEventListener('click', async () => {
    if (corriendo) return; corriendo = true;
    lineas.forEach(l => l.style.opacity = 0);
    for (const l of lineas){ l.style.opacity = 1; await espera(110); }
    out.textContent = tl('11 exactos en orden en UR266, 7 en UR275.', '11 exact and in order in UR266, 7 in UR275.'); corriendo = false;
  });
  if (REDUCIR) mostrar(); else setTimeout(() => { if (!corriendo) mostrar(); }, 50);
})();

/* ---------- figura 8: UR273A + UR273B ---------- */
(function figAB(){
  const tabla = $('tabla-ab'), out = $('ab-salida');
  tabla.innerHTML = '<thead><tr><th class="l">' + tl('registro', 'record') + '</th><th>UR273A</th><th></th><th>UR273B</th><th></th><th>' + tl('suma', 'sum') + '</th><th class="l">' + tl('en el libro', 'in a ledger') + '</th></tr></thead>';
  const tb = document.createElement('tbody'); tabla.appendChild(tb);
  const filas = D.ab.map(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = '<td class="l">g' + r.g + '</td><td>' + r.a + '</td><td>+</td><td>' + r.b + '</td><td>=</td><td class="s">' + r.s + '</td><td class="l x">' + (r.hit ? tl('sí', 'yes') : '') + '</td>';
    tb.appendChild(tr); return {tr, r};
  });
  const final = () => { filas.forEach(f => f.tr.classList.toggle('hit', f.r.hit)); out.textContent = filas.filter(f => f.r.hit).length + tl(' sumas aparecen como cabeceras', ' sums appear as headers'); };
  final();
  let corriendo = false;
  $('ab-jugar').addEventListener('click', async () => {
    if (corriendo) return; corriendo = true;
    filas.forEach(f => { f.tr.classList.remove('hit'); f.tr.querySelector('.s').textContent = '?'; f.tr.querySelector('.x').textContent = ''; });
    let n = 0;
    for (const f of filas){ f.tr.querySelector('.s').textContent = f.r.s; if (f.r.hit){ n++; f.tr.classList.add('hit'); f.tr.querySelector('.x').textContent = tl('sí', 'yes'); } out.textContent = n + tl(' coincidencias', ' matches'); await espera(160); }
    final(); corriendo = false;
  });
})();

/* ---------- figura 9: perfil de columnas ---------- */
(function figPerfil(){
  const svg = $('svg-perfil'), F = D.perfil.filas;
  const medias = [...Array(9).keys()].map(j => F.reduce((s, f) => s + f[j], 0) / F.length);
  const mx = Math.max(...F.flat()) * 1.05;
  const X = j => 80 + j * 62, Y = v => 290 - v / mx * 260;
  for (let v = 0; v <= mx; v += 100){ el('line', {x1:55, y1:Y(v), x2:620, y2:Y(v), style:'stroke:var(--suave)'}, svg); tx(svg, 48, Y(v) + 4, String(v), {'text-anchor':'end', 'font-size':11, class:'g m'}); }
  for (let j = 0; j < 9; j++) tx(svg, X(j), 312, 'col. ' + (j + 1), {'text-anchor':'middle', 'font-size':11.5, class:'g'});
  const barras = medias.map((m, j) => el('rect', {x:X(j) - 18, y:Y(m), width:36, height:290 - Y(m), rx:3, style:'fill:var(--fibra);opacity:.35'}, svg));
  medias.forEach((m, j) => tx(svg, X(j), Y(m) - 6, String(Math.round(m)), {'text-anchor':'middle', 'font-size':11, class:'m'}));
  const lineas = F.map(f => el('polyline', {points:f.map((v, j) => X(j) + ',' + Y(v)).join(' '), style:'fill:none;stroke:var(--indigo);stroke-width:1;opacity:.35'}, svg));
  const mb = D.perfil.bambamarca, k = (medias.reduce((a, b) => a + b) / 9) / (mb.reduce((a, b) => a + b) / 9);
  const bamba = el('g', {style:'opacity:0;transition:opacity .4s'}, svg);
  el('polyline', {points:mb.map((v, j) => X(j) + ',' + Y(v * k)).join(' '), style:'fill:none;stroke:var(--gris);stroke-width:2.5;stroke-dasharray:6 4'}, bamba);
  mb.forEach((v, j) => el('circle', {cx:X(j), cy:Y(v * k), r:4, style:'fill:var(--gris)'}, bamba));
  tx(bamba, 620, Y(mb[8] * k) - 10, 'Bambamarca', {'text-anchor':'end', 'font-size':12, class:'g'});
  let corriendo = false;
  $('perfil-jugar').addEventListener('click', async () => {
    if (corriendo) return; corriendo = true;
    lineas.forEach(l => l.style.opacity = 0); barras.forEach(b => b.style.opacity = 0);
    for (const l of lineas){ l.style.opacity = .35; await espera(70); }
    barras.forEach(b => b.style.opacity = .35); corriendo = false;
  });
  const bb = $('perfil-bamba');
  bb.addEventListener('click', () => { const on = bb.getAttribute('aria-pressed') !== 'true'; bb.setAttribute('aria-pressed', on); bamba.style.opacity = on ? 1 : 0; });
})();

/* ---------- figura 10: la cuerda 180 ---------- */
(function figP180(){
  const svg = $('svg-p180'), base = D.p180;
  function dibujar(v){
    limpiar(svg);
    const c = JSON.parse(JSON.stringify(base));
    c.k.forEach(k => { if (k[1] === 'L'){ k[0] = v; k[3] = v; } });
    const valor = c.k.reduce((s, k) => s + k[3], 0);
    el('line', {x1:40, y1:30, x2:220, y2:30, style:'stroke:var(--fibra);stroke-width:6;stroke-linecap:round'}, svg);
    const r = cuerda(svg, 130, 30, c, 4.8, {w:4, paso:5.5, r:2.8, vuelta:3.8, lw:11});
    r.nudos.forEach(k => { el('line', {x1:150, y1:k.y, x2:230, y2:k.y, style:'stroke:var(--regla);stroke-dasharray:3 3'}, svg); tx(svg, 236, k.y + 4, String(k.v), {class:'m', 'font-size':13, style:k.t === 'L' ? 'fill:var(--cochinilla);font-weight:600' : ''}); });
    const fila = 1654 - 238 + valor;
    const R = [[tl('La celda vale', 'The cell is'), valor, ''], [tl('UR270 da, para esa celda', 'UR270 gives, for that cell'), 237, valor === 237], [tl('La fila 21 suma', 'Row 21 adds up to'), fila, ''], [tl('El libro dice', 'The ledger says'), 1653, fila === 1653]];
    R.forEach(([t, n, ok], i) => {
      const y = 70 + i * 52;
      tx(svg, 320, y, t, {'font-size':14, class:'g'});
      tx(svg, 600, y + 2, String(n), {'text-anchor':'end', class:'m', 'font-size':22, style:'font-weight:500'});
      if (ok !== '') tx(svg, 620, y + 2, ok ? '✓' : '✗', {'text-anchor':'end', 'font-size':18, style:'fill:' + (ok ? 'var(--ok)' : 'var(--mal)')});
    });
    tx(svg, 320, 280, v === 6 ? tl('Con 6 vueltas cierran las dos cuentas.', 'With 6 turns both accounts balance.') : tl('Con 7 vueltas no cierra ninguna.', 'With 7 turns neither balances.'), {'font-size':14, style:'fill:' + (v === 6 ? 'var(--ok)' : 'var(--mal)') + ';font-weight:500'});
  }
  document.querySelectorAll('#fig-p180 [data-v]').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('#fig-p180 [data-v]').forEach(x => x.setAttribute('aria-pressed', x === b)); dibujar(+b.dataset.v);
  }));
  dibujar(7);
})();

/* ---------- figura 11: toneladas ---------- */
(function figTon(){
  const svg = $('svg-ton'), X = t => 40 + t / 2000 * 560;
  el('rect', {x:X(900), y:40, width:X(1400) - X(900), height:40, rx:4, style:'fill:var(--indigo);opacity:.25'}, svg);
  el('line', {x1:X(0), y1:80, x2:X(2000), y2:80, style:'stroke:var(--tinta)'}, svg);
  for (let t = 0; t <= 2000; t += 250){ el('line', {x1:X(t), y1:80, x2:X(t), y2:t % 500 ? 85 : 90, style:'stroke:var(--tinta)'}, svg); if (t % 500 === 0) tx(svg, X(t), 108, t + ' t', {'text-anchor':'middle', 'font-size':12, class:'g m'}); }
  tx(svg, X(1150), 30, tl('900 a 1400 toneladas', '900 to 1,400 tonnes'), {'text-anchor':'middle', 'font-size':14, style:'fill:var(--indigo);font-weight:600'});
  tx(svg, X(1150), 66, tl('carga o fanega', 'carga or fanega'), {'text-anchor':'middle', 'font-size':12, class:'g'});
  tx(svg, X(0), 138, tl('Solo orden de magnitud. La unidad no se puede decidir con estos datos.', 'Order of magnitude only. These data cannot decide the unit.'), {'font-size':12, class:'g'});
})();

/* ---------- figura 12: red de copias ---------- */
(function figCopias(){
  const svg = $('svg-copias'), out = $('copias-salida');
  const lugar = m => { const s = String(m).toLowerCase();
    if (s.includes('berl')) return tl('Berlín', 'Berlin'); if (s.includes('par')) return tl('París', 'Paris'); if (s.includes('gotemb')) return tl('Gotemburgo', 'Gothenburg');
    if (s.includes('basil')) return tl('Basilea', 'Basel'); if (s.includes('dallas')) return 'Dallas'; if (s.includes('miami')) return 'Miami';
    if (s.includes('leymeb')) return 'Leymebamba'; if (s.includes('puruch') || s.includes('desconoc')) return 'Puruchuco';
    if (s.includes('incahuasi')) return 'Inkawasi'; if (s.includes('peabody')) return 'Peabody';
    if (s.includes('lima') || s.includes('bcrp') || s.includes('amano') || s.includes('radicati') || s.includes('mnaahp')) return 'Lima';
    return tl('Otros', 'Other'); };
  const P = D.copias, nodos = {}, grupos = {};
  P.forEach(p => { [[p.a, p.ma], [p.b, p.mb]].forEach(([k, m]) => { if (!nodos[k]){ const L = lugar(m); nodos[k] = {k, L, m}; (grupos[L] = grupos[L] || []).push(k); } }); });
  const orden = Object.keys(grupos).sort((a, b) => grupos[b].length - grupos[a].length);
  const cx = 480, cy = 280, rx = 360, ry = 215;
  // todos los quipus van sobre un mismo óvalo, cada grupo en su tramo: en una curva convexa la línea
  // entre dos quipus nunca pasa por encima de un tercero
  const hueco = 1.6, total = P.length && Object.values(grupos).reduce((s, g) => s + g.length + hueco, 0), paso = 2 * Math.PI / total;
  let ang = -Math.PI / 2 - (grupos[orden[0]].length - 1) / 2 * paso;
  orden.forEach(L => {
    const ks = grupos[L], a0 = ang;
    ks.forEach(k => { Object.assign(nodos[k], {x:cx + rx * Math.cos(ang), y:cy + ry * Math.sin(ang), ca:Math.cos(ang), sa:Math.sin(ang)}); ang += paso; });
    const am = (a0 + ang - paso) / 2, ca = Math.cos(am), sa = Math.sin(am);
    const banda = []; for (let q = a0 - paso * .45; q <= ang - paso * .55; q += paso / 6) banda.push((cx + (rx + 13) * Math.cos(q)).toFixed(1) + ' ' + (cy + (ry + 13) * Math.sin(q)).toFixed(1));
    if (banda.length > 1) el('path', {d:'M' + banda.join('L'), style:'fill:none;stroke:var(--regla);stroke-width:7;stroke-linecap:round'}, svg);
    tx(svg, cx + (rx + 26) * ca, cy + (ry + 22) * sa + 5, L, {'text-anchor':ca > .35 ? 'start' : ca < -.35 ? 'end' : 'middle', 'font-size':14, style:'font-weight:600'});
    ang += hueco * paso;
  });
  const COL = n => n.startsWith('bien apoyado') ? 'var(--ev-d)' : n.startsWith('apoyado') ? 'var(--ev-a)' : 'var(--ev-p)';
  const aristas = [];
  P.forEach(p => {
    const a = nodos[p.a], b = nodos[p.b], mx0 = (a.x + b.x) / 2, my0 = (a.y + b.y) / 2;
    // entre grupos la curva se arquea hacia el centro; dentro de un grupo, hacia afuera
    const mismo = a.L === b.L, h = Math.hypot(a.x - b.x, a.y - b.y);
    const mx = mismo ? mx0 + a.ca * (10 + h * .4) : mx0 + (cx - mx0) * .3, my = mismo ? my0 + a.sa * (10 + h * .4) : my0 + (cy - my0) * .3;
    const d = 'M' + a.x + ' ' + a.y + 'Q' + mx + ' ' + my + ' ' + b.x + ' ' + b.y;
    const vis = el('path', {d, style:'fill:none;stroke:' + COL(p.nivel) + ';stroke-width:' + (1 + p.ex / 22).toFixed(1) + ';opacity:.75'}, svg);
    const hit = el('path', {d, style:'fill:none;stroke:transparent;stroke-width:14;cursor:pointer', tabindex:0}, svg);
    const info = p.a + ' (' + p.ma + tl(') y ', ') and ') + p.b + ' (' + p.mb + ') · ' + p.ex + tl(' de ', ' of ') + p.al + tl(' cuerdas alineadas con el mismo valor · ', ' aligned cords with the same value · ') + NIVEL(p.nivel);
    const on = () => { aristas.forEach(o => o.vis.style.opacity = o.vis === vis ? 1 : .15); marcar([p.a, p.b]); out.textContent = info; };
    const off = () => { aristas.forEach(o => o.vis.style.opacity = .75); marcar([]); };
    hit.addEventListener('mouseenter', on); hit.addEventListener('focus', on); hit.addEventListener('click', on);
    hit.addEventListener('mouseleave', off); hit.addEventListener('blur', off);
    aristas.push({vis});
  });
  Object.values(nodos).forEach(n => { n.c = el('circle', {cx:n.x, cy:n.y, r:5.5, style:'fill:var(--tarjeta);stroke:var(--tinta);stroke-width:1.5'}, svg); });
  function marcar(ks){ Object.values(nodos).forEach(n => { const si = ks.includes(n.k); n.c.style.fill = si ? 'var(--tinta)' : 'var(--tarjeta)'; n.c.setAttribute('r', si ? 7 : 5.5); }); }
  [['var(--ev-d)', 'bien apoyado'], ['var(--ev-a)', 'apoyado'], ['var(--ev-p)', 'propuesto']].forEach(([c, n], i) => { el('line', {x1:20, y1:510 + i * 18, x2:44, y2:510 + i * 18, style:'stroke:' + c + ';stroke-width:3'}, svg); tx(svg, 50, 514 + i * 18, NIVEL(n), {'font-size':12}); });
})();

/* ---------- figura 13: el extracto ---------- */
(function figExtracto(){
  const svg = $('svg-extracto');
  const A = [2007, 2080, 3012, 2247, 2578, null, 3419, 3159, 1407], B = [2007, 2080, 3102, 2247, 2578, 2016, 3419, 3159, 1407];
  const X = i => 108 + i * 61;
  tx(svg, 10, 46, 'UR234', {'font-size':13, class:'m', style:'font-weight:500'}); tx(svg, 10, 146, 'UR1104', {'font-size':13, class:'m', style:'font-weight:500'});
  const caja = (x, y, v, est) => { const g = el('g', null, svg);
    el('rect', {x:x - 28, y:y - 18, width:56, height:30, rx:6, style:'fill:var(--tarjeta);stroke:' + (est === 'rota' ? 'var(--mal)' : est === 'var' ? 'var(--casi)' : 'var(--regla)') + ';stroke-width:1.5' + (est === 'rota' ? ';stroke-dasharray:4 3' : '')}, g);
    tx(g, x, y + 2, v === null ? 'rota' : String(v), {'text-anchor':'middle', class:'m', 'font-size':13, style:v === null ? 'fill:var(--mal)' : ''}); return g; };
  A.forEach((v, i) => caja(X(i), 46, v, v === null ? 'rota' : i === 2 ? 'var' : ''));
  const abajo = B.map((v, i) => { const g = el('g', null, svg);
    el('line', {x1:X(i), y1:62, x2:X(i), y2:124, style:'stroke:' + (i === 5 ? 'var(--mal)' : i === 2 ? 'var(--casi)' : 'var(--ok)') + ';stroke-width:1.5'}, g);
    g.appendChild(caja(X(i), 146, v, i === 5 ? '' : i === 2 ? 'var' : '')); return g; });
  tx(svg, X(5), 180, 'conserva lo perdido', {'text-anchor':'middle', 'font-size':11, style:'fill:var(--mal)'});
  tx(svg, X(2), 180, 'cifras invertidas', {'text-anchor':'middle', 'font-size':11, style:'fill:var(--casi)'});
  let corriendo = false;
  $('extracto-jugar').addEventListener('click', async () => {
    if (corriendo) return; corriendo = true;
    abajo.forEach(g => g.style.opacity = 0);
    for (const g of abajo){ g.style.opacity = 1; await espera(260); }
    corriendo = false;
  });
})();

/* ---------- figura 14: KH0049 ---------- */
(function figKH(){
  const svg = $('svg-kh'), K = D.kh0049, U = D.ur122;
  const X = j => 98 + j * 47, Y = i => 22 + i * 30;
  const celdas = K.map((b, i) => { tx(svg, 10, Y(i) + 4, 'B' + i, {'font-size':13, class:'m', style:'font-weight:500'}); return b.map((v, j) => {
    const r = el('rect', {x:X(j) - 22, y:Y(i) - 13, width:44, height:24, rx:4, style:'fill:var(--suave)'}, svg);
    tx(svg, X(j), Y(i) + 4, fmt(v), {'text-anchor':'middle', class:'m', 'font-size':10.5}); return r; }); });
  const nombresU = ['B1', 'B3', 'B4', 'B5'], filaK = [1, 3, 4, 5];
  const gU = el('g', {style:'opacity:0;transition:opacity .4s'}, svg);
  tx(gU, 10, Y(6) + 8, 'UR122, Gotemburgo', {'font-size':12, class:'g'});
  U.forEach((b, i) => { tx(gU, 10, Y(7 + i) + 4, nombresU[i], {'font-size':13, class:'m'}); b.forEach((v, j) => {
    const kv = K[filaK[i]][j], igual = v === kv, perdida = v === 0 && kv;
    el('rect', {x:X(j) - 22, y:Y(7 + i) - 13, width:44, height:24, rx:4, style:'fill:' + (igual ? 'var(--ok)' : 'var(--suave)') + ';opacity:' + (igual ? .25 : 1) + (perdida ? ';stroke:var(--mal);stroke-dasharray:3 2' : '')}, gU);
    tx(gU, X(j), Y(7 + i) + 4, fmt(v), {'text-anchor':'middle', class:'m', 'font-size':10.5, style:perdida ? 'fill:var(--mal)' : ''}); }); });
  const reglas = [[0, [1, 2]], [1, [3, 4, 5]]];
  function marcar(s){
    celdas.flat().forEach(r => r.setAttribute('style', 'fill:var(--suave)'));
    gU.style.opacity = s === 2 ? 1 : 0;
    svg.setAttribute('viewBox', '0 0 960 ' + (s === 2 ? 340 : 200));
    if (s === 2) return;
    const [t, ps] = reglas[s]; let n = 0;
    for (let j = 0; j < 18; j++){
      const suma = ps.reduce((a, p) => a + (K[p][j] || 0), 0), ok = K[t][j] && suma === K[t][j];
      if (ok){ n++; [t, ...ps].forEach(i => celdas[i][j].setAttribute('style', 'fill:var(--ok);opacity:' + (i === t ? .55 : .25))); }
    }
  }
  marcar(0); document.querySelector('#fig-kh [data-s="0"]').setAttribute('aria-pressed', 'true');
  document.querySelectorAll('#fig-kh [data-s]').forEach(b => b.addEventListener('click', () => {
    document.querySelectorAll('#fig-kh [data-s]').forEach(x => x.setAttribute('aria-pressed', x === b)); marcar(+b.dataset.s);
  }));
})();

/* ---------- figura 15: alternancia en UR040 ---------- */
(function figAlt(){
  const svg = $('svg-alt'), C = D.ur040, b = $('alt-jugar');
  el('line', {x1:20, y1:24, x2:620, y2:24, style:'stroke:var(--fibra);stroke-width:5;stroke-linecap:round'}, svg);
  const items = C.map((c, i) => {
    const g = el('g', {style:'transition:transform .7s ease'}, svg);
    el('line', {x1:0, y1:26, x2:0, y2:170, style:'stroke:var(--regla);stroke-width:8;stroke-linecap:round'}, g);
    el('line', {x1:0, y1:26, x2:0, y2:170, style:'stroke:' + colorCuerda(c.col) + ';stroke-width:6;stroke-linecap:round'}, g);
    tx(g, 0, 190, fmt(c.v), {'text-anchor':'middle', class:'m', 'font-size':11});
    tx(g, 0, 206, c.col, {'text-anchor':'middle', 'font-size':9.5, class:'g'});
    return {g, c, x0:35 + i * 17.5};
  });
  const etq = el('g', {style:'opacity:0;transition:opacity .5s'}, svg);
  tx(etq, 160, 240, 'columna W', {'text-anchor':'middle', 'font-size':13, style:'font-weight:600'}); tx(etq, 480, 240, 'columna AB', {'text-anchor':'middle', 'font-size':13, style:'font-weight:600'});
  function poner(sep){
    let w = 0, a = 0;
    items.forEach(it => { let x = it.x0; if (sep){ if (it.c.col === 'W'){ x = 30 + w * 15; w++; } else { x = 345 + a * 15; a++; } } it.g.setAttribute('transform', 'translate(' + x + ',0)'); });
    etq.style.opacity = sep ? 1 : 0;
  }
  b.addEventListener('click', () => { const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', on); b.textContent = on ? tl('Volver al orden original', 'Back to the original order') : tl('Separar por color', 'Split by colour'); poner(on); });
  poner(false);
})();

/* ---------- figura 16: UR1107 y UR237 ---------- */
(function fig1107(){
  const svg = $('svg-1107'), R = D.ur1107, X = i => 92 + i * 20.8;
  const falta = s => s == null || Number.isNaN(s), etiqueta = s => falta(s) ? '—' : String(s).split(':')[0];
  tx(svg, 10, 52, 'UR1107', {'font-size':12, class:'m', style:'font-weight:500'}); tx(svg, 10, 152, 'UR237', {'font-size':12, class:'m', style:'font-weight:500'});
  tx(svg, 10, 102, tl('valor', 'value'), {'font-size':11, class:'g'});
  R.forEach((r, i) => {
    const x = X(i);
    el('rect', {x:x - 8, y:22, width:16, height:22, rx:3, style:'fill:' + (falta(r.a) ? 'var(--suave)' : colorCuerda(r.a)) + ';stroke:var(--regla)'}, svg);
    tx(svg, x, 58, etiqueta(r.a), {'text-anchor':'middle', 'font-size':8.5, class:'g'});
    const igual = r.va === r.vb && !Number.isNaN(r.va);
    tx(svg, x, 96, fmt(r.va), {'text-anchor':'middle', class:'m', 'font-size':9, style:igual ? 'fill:var(--ok)' : 'fill:var(--mal)'});
    tx(svg, x, 108, igual ? '=' : '≠', {'text-anchor':'middle', 'font-size':10, style:igual ? 'fill:var(--ok)' : 'fill:var(--mal)'});
    el('rect', {x:x - 8, y:122, width:16, height:22, rx:3, style:'fill:' + (falta(r.b) ? 'var(--suave)' : colorCuerda(r.b)) + ';stroke:var(--regla)'}, svg);
    tx(svg, x, 158, etiqueta(r.b), {'text-anchor':'middle', 'font-size':8.5, class:'g'});
  });
  const iguales = R.filter(r => r.va === r.vb && !Number.isNaN(r.va)).length, coloresIg = R.filter(r => r.a === r.b).length;
  tx(svg, 92, 194, iguales + tl(' de ', ' of ') + R.length + tl(' valores iguales · ', ' values equal · ') + coloresIg + tl(' etiquetas de color iguales (— = sin color anotado)', ' colour labels equal (— = no colour recorded)'), {'font-size':13, style:'font-weight:500'});
})();

/* ---------- figura 17: formatos ---------- */
(function figFormatos(){
  const svg = $('svg-formatos');
  const panel = (x0, titulo, cuerdas, total, superior) => {
    titulo.split('|').forEach((l, i) => tx(svg, x0 + 92, 222 + i * 15, l, {'text-anchor':'middle', 'font-size':12, class:'g'}));
    el('line', {x1:x0 + 10, y1:50, x2:x0 + 175, y2:50, style:'stroke:var(--fibra);stroke-width:4;stroke-linecap:round'}, svg);
    cuerdas.forEach(([x, v, esTotal], i) => {
      const xx = x0 + x;
      if (superior && esTotal){ el('line', {x1:xx, y1:48, x2:xx, y2:14, style:'stroke:var(--indigo);stroke-width:3;stroke-linecap:round'}, svg); tx(svg, xx + 6, 22, String(v), {class:'m', 'font-size':12, style:'fill:var(--indigo)'}); return; }
      const h = 26 + v * 1.05;
      el('line', {x1:xx, y1:52, x2:xx, y2:52 + h, style:'stroke:' + (esTotal ? 'var(--indigo)' : 'var(--fibra)') + ';stroke-width:3;stroke-linecap:round'}, svg);
      tx(svg, xx, 68 + h, String(v), {'text-anchor':'middle', class:'m', 'font-size':11.5, style:esTotal ? 'fill:var(--indigo)' : ''});
    });
  };
  panel(10, tl('la cuerda superior|suma el grupo anterior', 'the top cord|sums the group before it'), [[25,12],[45,30],[65,18],[85,26],[92,86,true],[120,15],[140,22],[160,9]], 0, true);
  panel(225, tl('fila y cuerda suelta|con el total', 'a row and a loose cord|with the total'), [[20,14],[38,21],[56,9],[74,30],[92,16],[140,90,true]], 0, false);
  panel(440, tl('la cuerda mayor|abre el grupo', 'the largest cord|opens the group'), [[30,62,true],[55,24],[80,31],[105,18],[130,27],[155,12]], 0, false);
})();

/* ---------- figura 18: UR053 ---------- */
(function fig053(){
  const svg = $('svg-053');
  const R = [['UR053A', .70, .17, .13], ['UR053B', .57, .26, .17], ['UR053C', .61, .23, .16], ['UR053D', .66, .16, .18], ['UR053E', .64, .18, .18]];
  const cs = [CC.W, CC.RL, CC.AB], nom = ['W', 'R', 'AB'];
  R.forEach(([n, ...f], i) => {
    const y = 20 + i * 36; let x = 90;
    tx(svg, 80, y + 17, n, {'text-anchor':'end', class:'m', 'font-size':13});
    f.forEach((v, j) => { const w = v * 520; el('rect', {x, y, width:w - 2, height:26, rx:3, style:'fill:' + cs[j] + ';stroke:var(--regla)'}, svg);
      tx(svg, x + w / 2, y + 18, Math.round(v * 100) + ' %', {'text-anchor':'middle', class:'m', 'font-size':11.5, style:'fill:#1d1b18'}); x += w; });
  });
  nom.forEach((n, j) => { el('rect', {x:90 + j * 90, y:206, width:14, height:14, rx:2, style:'fill:' + cs[j] + ';stroke:var(--regla)'}, svg); tx(svg, 110 + j * 90, 218, n, {'font-size':12}); });
})();

/* ---------- figura 19: atlas ---------- */
(function figAtlas(){
  const svg = $('svg-atlas'), b = $('atlas-orden'), ley = $('atlas-leyenda');
  const G = {ARC:[tl('archivo jerárquico', 'hierarchical archive'),'#2f3f8f'], SUM:[tl('lista con totales', 'list with totals'),'#b07a1e'], FOR:[tl('formulario con reparto', 'form with a split'),'#8a6a4a'], TAB:[tl('tabla de recuento', 'tally table'),'#2c7a6b'],
    PAD:[tl('padrón por persona', 'register by person'),'#a8322d'], ASG:[tl('asignación', 'allocation'),'#7b4f9d'], TAL:[tl('conteo por marcas', 'tally marks'),'#6d7f2f'], NAZ:[tl('ficha de Nazca', 'Nazca card'),'#3f7fb5'],
    CAL:[tl('calendario', 'calendar'),'#c2477d'], NON:[tl('no numérico', 'non-numeric'),'#5f6a7a'], SEG:[tl('lista segmentada', 'segmented list'),'#b9a587'], SIN:[tl('sin tipo reconocible', 'no recognisable type'),'#cfc9bd']};
  const ORD = Object.keys(G);
  const proc = p => { const s = String(p).toLowerCase();
    if (s.includes('incahuasi')) return 'Inkawasi'; if (s.includes('pachacamac')) return 'Pachacamac'; if (s.includes('leymebamba') || s.includes('laguna')) return 'Leymebamba';
    if (s.includes('nazca')) return 'Nazca'; if (s.includes('huaquerones') || s.includes('puruchuco')) return 'Puruchuco'; if (s.includes('santa')) return tl('Valle del Santa', 'Santa Valley');
    if (/(^|[^a-z])ica([^a-z]|$)/.test(s)) return 'Ica'; if (s === 'unknown' || s === 'nan' || s === '' || s === 'peru') return tl('Procedencia desconocida', 'Unknown provenance'); return tl('Otras procedencias', 'Other provenances'); };
  const A = D.atlas.map(a => Object.assign({}, a, {P:proc(a.p), o:ORD.indexOf(a.g), baja:a.c === 'baja'}));
  const cont = {}; A.forEach(a => cont[a.g] = (cont[a.g] || 0) + 1);
  ley.innerHTML = ORD.filter(g => cont[g]).map(g => '<div><span style="display:inline-block;width:11px;height:11px;border-radius:2px;background:' + G[g][1] + ';margin-right:6px;vertical-align:-1px"></span>' + G[g][0] + ' <span class="num">' + cont[g] + '</span></div>').join('');
  const lado = 12, paso = 14.5;
  function dibujar(porSitio){
    limpiar(svg);
    const orden = (x, y) => x.o - y.o || (x.baja - y.baja);
    let y = 10;
    if (!porSitio){
      const L = A.slice().sort(orden), cols = 62;
      L.forEach((a, i) => el('rect', {x:10 + (i % cols) * paso, y:y + Math.floor(i / cols) * paso, width:lado, height:lado, rx:2, style:'fill:' + G[a.g][1] + ';opacity:' + (a.baja ? .38 : 1)}, svg));
      y += Math.ceil(L.length / cols) * paso + 10;
    } else {
      const grupos = {}; A.forEach(a => (grupos[a.P] = grupos[a.P] || []).push(a));
      const nombres = Object.keys(grupos).sort((p, q) => (p.startsWith('Proc') || p.startsWith('Otras')) - (q.startsWith('Proc') || q.startsWith('Otras')) || grupos[q].length - grupos[p].length);
      const cols = 52;
      nombres.forEach(n => {
        const L = grupos[n].sort(orden);
        tx(svg, 10, y + 11, n, {'font-size':12, style:'font-weight:500'}); tx(svg, 10, y + 25, L.length + ' quipus', {'font-size':10.5, class:'g'});
        L.forEach((a, i) => el('rect', {x:200 + (i % cols) * paso, y:y + Math.floor(i / cols) * paso, width:lado, height:lado, rx:2, style:'fill:' + G[a.g][1] + ';opacity:' + (a.baja ? .38 : 1)}, svg));
        y += Math.max(32, Math.ceil(L.length / cols) * paso + 12);
      });
    }
    svg.setAttribute('viewBox', '0 0 960 ' + Math.ceil(y));
  }
  b.addEventListener('click', () => { const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', on); b.textContent = on ? tl('Ver todo el corpus junto', 'Show the whole corpus together') : tl('Agrupar por procedencia', 'Group by provenance'); dibujar(on); });
  dibujar(false);
})();

/* ---------- figura 20: el 74 % ---------- */
(function fig74(){
  const svg = $('svg-74'), X = v => 220 + (v - 7700) / 600 * 390;
  const M = [[tl('barajando dentro de cada quipu', 'shuffling within each khipu'), 8031, 7892, 8167], [tl('barajando dentro de cada nivel', 'shuffling within each level'), 7913, 7790, 8036], [tl('entre valores de magnitud parecida', 'among values of similar size'), 8094, 7975, 8209]];
  M.forEach(([n, e, a, b], i) => {
    const y = 40 + i * 46;
    tx(svg, 210, y + 4, n, {'text-anchor':'end', 'font-size':12.5});
    el('line', {x1:X(a), y1:y, x2:X(b), y2:y, style:'stroke:var(--fibra);stroke-width:10;stroke-linecap:round;opacity:.45'}, svg);
    el('circle', {cx:X(e), cy:y, r:5, style:'fill:var(--fibra)'}, svg);
  });
  el('line', {x1:X(8076), y1:18, x2:X(8076), y2:170, style:'stroke:var(--indigo);stroke-width:2.5'}, svg);
  tx(svg, X(8076) + 6, 24, tl('datos reales: 8076', 'real data: 8076'), {'font-size':12.5, style:'fill:var(--indigo);font-weight:600'});
  el('line', {x1:X(7700), y1:180, x2:X(8300), y2:180, style:'stroke:var(--regla)'}, svg);
  [7700, 7900, 8100, 8300].forEach(v => { el('line', {x1:X(v), y1:180, x2:X(v), y2:186, style:'stroke:var(--regla)'}, svg); tx(svg, X(v), 202, String(v), {'text-anchor':'middle', 'font-size':11, class:'g m'}); });
  tx(svg, 10, 202, tl('sumas encontradas', 'sums found'), {'font-size':11, class:'g'});
})();

/* ---------- figura 21: el cero ---------- */
(function figCero(){
  const svg = $('svg-cero'), c = D.cero, sc = 9, x0 = 40, y = 70;
  const X = p => x0 + p * sc, largo = (c.l || 40) * sc;
  el('line', {x1:x0, y1:y - 30, x2:x0, y2:y + 30, style:'stroke:var(--fibra);stroke-width:6;stroke-linecap:round'}, svg);
  el('line', {x1:x0, y1:y, x2:x0 + largo, y2:y, style:'stroke:var(--regla);stroke-width:6;stroke-linecap:round'}, svg);
  el('line', {x1:x0, y1:y, x2:x0 + largo, y2:y, style:'stroke:' + colorCuerda(c.col) + ';stroke-width:4;stroke-linecap:round'}, svg);
  c.k.forEach(([n, t, p, v]) => {
    const x = X(p);
    if (t === 'S') for (let i = 0; i < n; i++) el('circle', {cx:x + (i - (n - 1) / 2) * 7, cy:y, r:3.4, style:'fill:var(--tinta)'}, svg);
    else if (t === 'L'){ const w = 6 + n * 4.5; el('rect', {x:x - w / 2, y:y - 5.5, width:w, height:11, rx:5.5, style:'fill:var(--tinta)'}, svg); }
    tx(svg, x, y - 18, String(v), {'text-anchor':'middle', class:'m', 'font-size':13});
    tx(svg, x, y + 30, p + ' cm', {'text-anchor':'middle', 'font-size':11, class:'g'});
  });
  const [k1, k2, k3] = c.k;
  const llave = (a, b, yy, t, col) => { el('path', {d:'M' + X(a) + ' ' + (yy - 6) + 'V' + yy + 'H' + X(b) + 'V' + (yy - 6), style:'fill:none;stroke:' + col + ';stroke-width:1.5'}, svg); tx(svg, (X(a) + X(b)) / 2, yy + 18, t, {'text-anchor':'middle', 'font-size':12.5, style:'fill:' + col + ';font-weight:500'}); };
  llave(k1[2], k2[2], 130, (k2[2] - k1[2]) + tl(' cm entre millar y centena', ' cm from thousands to hundreds'), 'var(--fibra)');
  llave(k2[2], k3[2], 170, (k3[2] - k2[2]) + tl(' cm de centena a unidades', ' cm from hundreds to units'), 'var(--indigo)');
  const xm = (X(k2[2]) + X(k3[2])) / 2;
  el('rect', {x:xm - 26, y:y - 14, width:52, height:28, rx:6, style:'fill:none;stroke:var(--cochinilla);stroke-dasharray:4 3;stroke-width:1.5'}, svg);
  tx(svg, xm, y - 20, tl('decenas: 0', 'tens: 0'), {'text-anchor':'middle', 'font-size':12, style:'fill:var(--cochinilla);font-weight:600'});
  tx(svg, 600, 222, c.kfg + tl(', cuerda ', ', cord ') + c.c.replace('p', '') + ' · ' + c.v, {'text-anchor':'end', 'font-size':11, class:'g'});
})();

/* ---------- figura 22: el lector ---------- */
(function figLector(){
  const tabs = $('lector-tabs'), caja = $('lector-ficha');
  const CL = {'BIEN APOYADO':'ev-d', APOYADO:'ev-a', PROPUESTO:'ev-p', 'WELL SUPPORTED':'ev-d', SUPPORTED:'ev-a', PROPOSED:'ev-p'};
  const esc = s => s.replace(/[&<>]/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;'})[c]);
  function mostrar(k){
    const F = (EN ? D.fichas_en : D.fichas)[k], secs = [];
    F.forEach(([s, n, t]) => { let x = secs.find(z => z[0] === s); if (!x){ x = [s, []]; secs.push(x); } x[1].push([n, t]); });
    caja.innerHTML = '<div class="num" style="font-size:15px;margin-bottom:6px">' + tl('Ficha de lectura: ', 'Reading card: ') + k + '</div>' + secs.map((s, i) =>
      '<details' + (i < 2 || s[0].startsWith('Relaciones') || s[0].startsWith('Alternancia') || s[0].startsWith('Totales') ? ' open' : '') + '><summary>' + esc(s[0]) + '</summary><ul>' +
      s[1].map(([n, t]) => '<li><span class="ev ' + (CL[n] || '') + '" style="' + (CL[n] ? '' : 'color:var(--gris)') + '">' + n.toLowerCase() + '</span>' + esc(t) + '</li>').join('') + '</ul></details>').join('');
  }
  Object.keys(D.fichas).forEach((k, i) => {
    const b = document.createElement('button'); b.className = 'boton'; b.textContent = k; b.setAttribute('aria-pressed', i === 0);
    b.addEventListener('click', () => { tabs.querySelectorAll('.boton').forEach(x => x.setAttribute('aria-pressed', x === b)); mostrar(k); });
    tabs.appendChild(b);
  });
  mostrar(Object.keys(D.fichas)[0]);
})();
})();
