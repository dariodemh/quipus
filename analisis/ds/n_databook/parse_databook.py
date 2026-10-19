#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser del Code of the Quipu Databook (Ascher & Ascher 1988), OCR Tesseract.
Extrae filas de la tabla: cuerda | nudos | largo | color | valor | subsidiarias.
Escribe databook_rows.csv y databook_observaciones_raw.csv.
"""
import re, glob, os
import pandas as pd
from decoder import decode

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '..', '..', 'fuentes_txt', 'databook')

def clean_line(s: str) -> str:
    s = s.replace('\u00a2', ' ')          # centavo = fin de largo
    s = s.replace('\u00b0', ' ')
    s = s.replace('\u2014', '-').replace('\u2013', '-')
    s = s.replace('|', ' ')
    s = s.replace('\u2018', "'").replace('\u2019', "'")
    return s

# ---------------- etiqueta de cuerda ----------------
LABEL_RE = re.compile(r'^\s*((?:T[0-9lIi]|[0-9]{1,3})(?:[a-zA-Z0-9]{0,6}))\s+(?=\S)')

def norm_cord(label: str):
    """T1->t1, 3->p3, 1s1/1sl/1si->p1s1, 4us1->p4s1, T2sl->t2s1."""
    lab = label.strip()
    m = re.match(r'^(T[0-9lIi])(.*)$', lab)
    if m:
        base = 't' + ('1' if m.group(1)[-1] in 'lIi' else m.group(1)[-1])
        rest = m.group(2)
    else:
        m = re.match(r'^([0-9]{1,3})(.*)$', lab)
        if not m:
            return None, True
        base = 'p' + str(int(m.group(1)))
        rest = m.group(2)
    amb = False
    # normalizar confusiones l/i -> 1, quitar ruido u/h/k, minusculas
    rest = rest.lower().replace('l', '1').replace('i', '1')
    rest = re.sub(r'[uhk]', '', rest)
    # tokens: 's' + digito
    toks = re.findall(r's(\d+)', rest)
    leftover = re.sub(r's\d+', '', rest)
    if leftover.strip('.'):
        amb = True
    for t in toks:
        base += 's' + str(int(t[0]))
    return base, amb

# ---------------- nudos ----------------
def clean_knots(seg: str) -> str:
    s = seg
    s = s.replace('Tl', 'T1')
    s = re.sub(r'(?<![0-9])([1-9])5\s*\(', r'\1s(', s)     # 35(3.5) = 3s
    s = re.sub(r'(?<![0-9])([1-9])5\s*;', r'\1s;', s)
    s = re.sub(r'(?<![0-9])([1-9])8\s*\(', r'\1s(', s)     # 38(3.0) = 3s
    s = re.sub(r'[^0-9sSlLeE;,.,()\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    # separar clusters pegados por ruido: ")34L(" -> ");3L(" aprox.
    s = re.sub(r'\)\s*\d\s*(?=\d*[sSlLeE]\s*\()', ');', s)
    s = re.sub(r'([0-9])\s*[sS]\s*\(', r'\1s(', s)
    s = re.sub(r'([0-9])\s*[lL]\s*\(', r'\1L(', s)
    s = re.sub(r'([0-9])\s*[eE]\s*\(', r'\1E(', s)
    s = re.sub(r'\s*;\s*', ';', s)
    # quitar punto y coma final
    s = s.strip('; ')
    return s

CLUST_RE = re.compile(r'(\d{1,2})\s*([sLeE])')

def value_from_knots(kn: str):
    if kn is None or kn.strip() in ('', '-', '--', '---'):
        return 0
    parts = [p.strip() for p in kn.split(';') if p.strip()]
    if not parts:
        return 0
    vals = []
    for i, p in enumerate(parts):
        m = CLUST_RE.search(p)
        if not m:
            return None
        n = int(m.group(1)); t = m.group(2)
        if t == 's':
            v = n * 10 if n > 1 else (10 if i < len(parts) - 1 else 1)
        elif t == 'L':
            v = n
        else:
            v = n
        vals.append(v)
    return sum(vals)

# ---------------- color ----------------
_CV = None
def color_vocab():
    global _CV
    if _CV is None:
        _CV = set()
        try:
            kk = pd.read_csv(os.path.join(BASE, '..', '..', 'datos', 'cuerdas.csv')).color.dropna().astype(str)
            for v in kk:
                for p in re.split(r'[:/\-]', re.sub(r'\([^)]*\)', '', v.upper())):
                    if p.strip(): _CV.add(p.strip())
        except Exception:
            pass
        _CV |= {'W','B','AB','MB','LB','DB','KB','YB','BB','BS','GB','GG','GY','PK','RB','SB','SR','SY','VB','BG','FB','LC','NB','OD','RM','GR','GO','BL'}
    return _CV

def clean_color(tok: str) -> str:
    if not tok:
        return ''
    t = tok.strip().strip('.,;')
    t = re.sub(r'\s+', '', t)
    t = t.replace('=', '').replace('|', '').replace('*', ':').replace('$', '')
    t = t.upper()
    t = re.sub(r'(?<=[A-Z])0', 'O', t)
    t = re.sub(r'0(?=[A-Z])', 'O', t)
    t = t.replace('8', 'B') if re.fullmatch(r'[A-Z8]{1,3}', t) else t
    t = re.sub(r':+', ':', t).strip(':')
    if not re.fullmatch(r'[A-Z]{1,4}([:/\-][A-Z]{1,4})*', t):
        return ''
    parts = re.split(r'[:/\-]', t)
    V = color_vocab()
    if all(p in V for p in parts):
        return t
    return ''

SUB_RE = re.compile(r'(\d{1,2}\s*:\s*\d{1,3}(?:[.,]\d)?|missing)\s*[.\s|:;,]*$', re.I)
DEC_RE = re.compile(r'(?<![\d.])(\d{1,3})\s*[.,]\s*(\d)(?![\d])')

def parse_row(line: str):
    """Devuelve dict o None. Estrategia derecha->izquierda."""
    s = line.rstrip()
    # 1) subsidiarias al final
    subs = ''
    m = SUB_RE.search(s)
    if m:
        subs = m.group(1).replace(' ', '')
        s = s[:m.start()].rstrip()
    # 2) valor = expresion final: "4", "4+4", "16+T", "12(?)"
    mv = re.search(r"(?<![\d.])(\d{1,3}(?:\s*\+\s*\d{1,3})*)\s*([A-Za-z?()*.,;:'\"\-]*)\s*$", s)
    if mv:
        expr, marca = mv.group(1), mv.group(2)
        valor = sum(int(x) for x in re.findall(r'\d+', expr))
        valor_marca = marca
        valor_expr = expr
        dudoso = '?' in marca
        pre_val = s[:mv.start()].rstrip()
    else:
        # fila sin columna de valor (p.ej. AS87, AS95, AS104): se conserva
        valor = float('nan'); valor_marca = 'SIN_VALOR'; valor_expr = 'SIN_VALOR'; dudoso = False
        pre_val = s
    # 3) color = ultima palabra antes del valor (si tiene letras)
    color = ''
    pre_len = pre_val
    for mt in reversed(list(re.finditer(r'\S+', pre_val))):
        tok = mt.group(0)
        c = clean_color(tok)
        if c:
            color = c
            pre_len = pre_val[:mt.start()].rstrip()
            break
        if re.search(r'\d', tok):
            break
    # 4) largo = ultimo decimal del prefijo restante
    decs = list(DEC_RE.finditer(pre_len))
    if not decs:
        return None
    lm = decs[-1]
    largo = float(lm.group(1)) + float(lm.group(2)) / 10
    if pd.isna(valor):
        for tok in pre_len[lm.end():].split():
            c = clean_color(tok)
            if c:
                color = c
                break
    pre = pre_len[:lm.start()].rstrip()
    # descartar si "largo" esta dentro de parentesis (posicion de nudo)
    if pre.count('(') > pre.count(')'):
        return None
    # 5) etiqueta + nudos
    lm2 = LABEL_RE.match(pre)
    if not lm2:
        return None
    label = lm2.group(1)
    cord, amb = norm_cord(label)
    if cord is None:
        return None
    knots_raw = pre[lm2.end():].strip()
    # limpiar ruido de inicio / final
    knots_raw = re.sub(r'^[-–—:.\s]+', '', knots_raw)
    knots_raw = re.sub(r'[\s:.\-]+$', '', knots_raw)
    # si quedan letras sueltas tipo "missing"
    if re.search(r'[A-Za-z]', re.sub(r'[sLeE]', '', knots_raw)):
        return None
    kn = clean_knots(knots_raw)
    return dict(cord_databook=cord, label_ocr=label, label_ambiguo=amb,
                knots_raw=knots_raw, knots_norm=kn,
                largo=largo, color=color, valor=valor, valor_dudoso=dudoso,
                valor_marca=valor_marca, valor_expr=valor_expr,
                valor_knots=decode(kn, largo)[0], knots_ambiguo=decode(kn, largo)[1],
                subs_raw=subs)

KFG_IDS = set(pd.read_csv(os.path.join(BASE, '..', '..', 'datos', 'cuerdas.csv')).kfg.unique())

def resolve_header(h):
    """Convierte 'AS207 A', 'AS101--PART II', 'AS61/MA36'... en id KFG."""
    h = h.upper()
    n = re.search(r'AS\s*([0-9]{1,3})', h)
    if not n:
        return None
    num = int(n.group(1))
    if 'PART' in h:
        part = 2 if re.search(r'PART\s*(II|2)', h) else 1
        cand = 'AS%03d_Part_%d' % (num, part)
        if cand in KFG_IDS: return cand
    if 'MA' in h:
        mm = re.search(r'MA\s*([0-9]+)', h)
        if mm:
            cand = 'AS%03d_MA%03d' % (num, int(mm.group(1)))
            if cand in KFG_IDS: return cand
    if '/N' in h:
        mm = re.search(r'/\s*N\s*([0-9]+)', h)
        if mm:
            cand = 'AS%03d_N%d' % (num, int(mm.group(1)))
            if cand in KFG_IDS: return cand
    suf = re.search(r'AS\s*[0-9]{1,3}\s*([A-F])\b', h)
    for cand in (('AS%03d%s' % (num, suf.group(1)) if suf else None),
                 ('AS%d%s' % (num, suf.group(1)) if suf else None),
                 'AS%03d' % num):
        if cand and cand in KFG_IDS:
            return cand
    return 'AS%03d' % num

def header_id(path):
    txt = open(path, encoding='utf8', errors='replace').read()[:800]
    m = re.search(r'QUIPU\s+([^\n]+)', txt)
    return resolve_header(m.group(1)) if m else None

def parse_file(path):
    fallback = 'AS%03d' % int(re.search(r'as(\d+)\.txt$', os.path.basename(path)).group(1))
    quipu = header_id(path) or fallback
    rows, obs = [], []
    in_obs = False
    for raw in open(path, encoding='utf8', errors='replace'):
        line = clean_line(raw.rstrip('\n'))
        # cambio de quipu dentro del mismo archivo (AS33A-G, AS35A-D, AS101 I/II...)
        mh = re.match(r'^\s*QUIPU\s+(.+)$', line)
        if mh:
            quipu = resolve_header(mh.group(1)) or quipu
            in_obs = False
            continue
        if re.match(r'^\s*Observations?\s*$', line, re.I):
            in_obs = True
            continue
        if in_obs:
            t = line.strip()
            if t and not re.match(r'^===', t) and not re.match(r'^\s*\d{1,4}\s*$', t):
                obs.append((quipu, t))
            continue
        if not line.strip() or re.search(r'Cord\s+Knots', line):
            continue
        r = parse_row(line)
        if r:
            r.update(quipu=quipu, page_file=os.path.basename(path))
            rows.append(r)
    return rows, obs

def main():
    all_rows, all_obs = [], []
    files = sorted(glob.glob(os.path.join(SRC, 'as[0-9]*.txt')),
                   key=lambda x: int(re.search(r'as(\d+)\.txt', x).group(1)))
    for f in files:
        rows, obs = parse_file(f)
        all_rows += rows
        for i, (qo, o) in enumerate(obs):
            all_obs.append(dict(quipu=qo, orden=i, texto=o))
    df = pd.DataFrame(all_rows)
    df.to_csv(os.path.join(BASE, 'databook_rows.csv'), index=False, encoding='utf-8')
    pd.DataFrame(all_obs).to_csv(os.path.join(BASE, 'databook_observaciones_raw.csv'),
                                 index=False, encoding='utf-8')
    print('filas', len(df), '| quipus con filas', df.quipu.nunique(), '| obs', len(all_obs))
    print('valor == valor(nudos)', (df.valor == df.valor_knots).mean().round(4),
          '| valor_knots nulo', df.valor_knots.isna().sum())
    print('color vacio', (df.color == '').mean().round(3),
          '| label ambiguo', df.label_ambiguo.mean().round(3))
    print('niveles:', df.cord_databook.str.count('s').value_counts().to_dict())
    print(df.head(10).to_string(max_colwidth=22))

if __name__ == '__main__':
    main()
