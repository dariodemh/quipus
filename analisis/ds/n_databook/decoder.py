#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Decodificador Ascher de una cadena de nudos (formato Databook normalizado
o KFG) con reglas posicionales y marca de ambiguedad."""
import re

CL = re.compile(r'(\d{1,2})\s*([sSlL]+|[eE]+)\s*(?:\(\s*([0-9]{0,3}(?:[.,][0-9])?)?\s*\))?')

def clusters(knots):
    out = []
    if not knots or str(knots).strip() in ('', '-', '--', '---', 'nan'):
        return out
    for p in str(knots).split(';'):
        m = CL.search(p)
        if not m:
            continue
        pos = m.group(3)
        pos = float(pos.replace(',', '.')) if pos else None
        t = m.group(2)
        t = 's' if t[0] in 'sS' else ('L' if t[0] in 'lL' else 'E')
        out.append((int(m.group(1)), t, pos))
    return out

def decode(knots, largo=None):
    """Devuelve (valor, ambiguo, n_clusters). None si no hay nudos validos."""
    cl = clusters(knots)
    if not cl:
        return 0, False, 0
    amb = False
    total = 0
    for i, (n, t, pos) in enumerate(cl):
        if t in ('L', 'e', 'E'):
            if n > 13:
                amb = True
            total += n
            continue
        # simple
        below_s = sum(1 for j in range(i + 1, len(cl)) if cl[j][1] == 's')
        below_any = i < len(cl) - 1
        e = below_s + (1 if below_any else 0)
        if e == 0:
            if pos is not None and largo and largo > 0:
                r = pos / largo
                if r < 0.42:
                    e = 1
                elif r < 0.62:
                    amb = True
                    e = 1
            else:
                amb = True
        if n > 9:
            amb = True
        total += n * (10 ** min(e, 2))
    return total, amb, len(cl)
