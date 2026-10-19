"""Ver diseno_previo.md. Semilla fija. Uso: python pruebas.py (desde la raiz del repo)."""
import csv, re, collections, random, math, json
import numpy as np
rng = np.random.default_rng(20261018); random.seed(20261018)
D = 'analisis/datos/'
C = list(csv.DictReader(open(D+'cuerdas.csv', encoding='utf-8')))
Q = {r['kfg']: r['procedencia'] for r in csv.DictReader(open(D+'quipus.csv', encoding='utf-8'))}
G = {r['kfg']: r['genero'] for r in csv.DictReader(open('analisis/28_atlas_generos/atlas.csv', encoding='utf-8'))}
NR = 5000
grp = collections.defaultdict(lambda: collections.defaultdict(list))  # q -> grupo -> valores nivel0
for x in C:
    if x['nivel'] == '0':
        grp[x['kfg']][int(x['grupo'])].append(int(float(x['valor'] or 0)))
P = {}

# ---- P1 chi2 de homogeneidad del digito de unidades
def chi2(labels, digs):
    cats = sorted(set(labels)); tab = np.zeros((len(cats), 10)); ix = {c: i for i, c in enumerate(cats)}
    for l, d in zip(labels, digs): tab[ix[l]] += d
    e = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
    return ((tab - e) ** 2 / np.where(e == 0, 1, e)).sum()
def p1(lab, name):
    dig = {q: np.bincount([v % 10 for g in grp[q].values() for v in g if v > 0], minlength=10) for q in grp}
    byl = collections.defaultdict(list)
    for q in grp:
        if q in lab and dig[q].sum(): byl[lab[q]].append(q)
    keep = [l for l, qs in byl.items() if len(qs) >= 5 and sum(dig[q].sum() for q in qs) >= 300]
    qs = [q for l in keep for q in byl[l]]; ls = [lab[q] for q in qs]
    obs = chi2(ls, [dig[q] for q in qs]); n = 0
    for _ in range(NR):
        n += chi2(list(rng.permutation(ls)), [dig[q] for q in qs]) >= obs
    P[name] = ((n + 1) / (NR + 1), f'chi2={obs:.0f}; niveles={len(keep)}; quipus={len(qs)}')
    tot = {l: sum(dig[q] for q in byl[l]) for l in keep}
    print(name, P[name]); [print('  ', l, (tot[l] / tot[l].sum()).round(3)) for l in keep]
p1(Q, 'P1a_archivo'); p1(G, 'P1b_genero')

# ---- P2 totales
tot = []  # (q, n, pos)
for q, gs in grp.items():
    for g, v in gs.items():
        w = [a for a in v if a > 0]
        if len(w) >= 3:
            for i, a in enumerate(w):
                if a == sum(w) - a: tot.append((q, len(w), i)); break
def pos_counts(t): return sum(p == 0 for _, n, p in t), sum(p == n - 1 for _, n, p in t)
f0, l0 = pos_counts(tot)
nf = nl = 0
for _ in range(NR):
    s = [(q, n, int(rng.integers(n))) for q, n, _ in tot]
    a, b = pos_counts(s); nf += a >= f0; nl += b >= l0
P['P2a_total_primero'] = ((nf + 1) / (NR + 1), f'{f0}/{len(tot)} (esperado {sum(1/n for _,n,_ in tot):.1f})')
P['P2b_total_ultimo'] = ((nl + 1) / (NR + 1), f'{l0}/{len(tot)} (esperado {sum(1/n for _,n,_ in tot):.1f})')
byq = collections.defaultdict(list)
for t in tot: byq[t[0]].append(t)
def dif(qs):
    t = [x for q in qs for x in byq[q]]
    if not t: return 0
    a, b = pos_counts(t); return (a - b) / len(t)
qq = list(byq); isum = [G.get(q) == 'SUM' for q in qq]
def d2(m):
    a = [q for q, k in zip(qq, m) if k]; b = [q for q, k in zip(qq, m) if not k]
    return dif(a) - dif(b)
o = d2(isum); n = 0
for _ in range(NR): n += abs(d2(list(rng.permutation(isum)))) >= abs(o) - 1e-12
P['P2c_genero_SUM_vs_resto'] = ((n + 1) / (NR + 1), f'dif={o:.2f}; SUM {sum(isum)} quipus, resto {len(qq)-sum(isum)}; SUM(prim-ult)={dif([q for q,k in zip(qq,isum) if k]):.2f} resto={dif([q for q,k in zip(qq,isum) if not k]):.2f}')
print('totales', len(tot), 'quipus', len(qq))
# por genero descriptivo
for gname in sorted(set(G.get(q) for q in qq)):
    t = [x for x in tot if G.get(x[0]) == gname]
    if t: a, b = pos_counts(t); print('  genero', gname, 'tot', len(t), 'primero', a, 'ultimo', b)

# ---- P3 UR278 -> UR266
rows = [g for g in grp['UR278'].values() if sum(a > 0 for a in g) >= 8]
cells = np.array([[a for a in g if a > 0][:9] for g in rows if sum(a > 0 for a in g) == 9])
H = np.array([[a for a in g if a > 0][0] for g in grp['UR266'].values() if any(a > 0 for a in g) and [a for a in g if a > 0][0] >= 100])
def stat(cm):
    s = cm.sum(1); ex = si = 0
    for v in s:
        d = v - H[np.argmin(abs(H - v))]
        if d == 0: ex += 1
        elif re.fullmatch(r'[1-9]0*', str(abs(int(d)))): si += 1
    return ex, si
ex, si = stat(cells); N = len(cells)
nulo = []
for _ in range(NR):
    c2 = np.column_stack([rng.permutation(cells[:, j]) for j in range(9)]); nulo.append(stat(c2))
nulo = np.array(nulo); k = ex + si
p = ((nulo.sum(1) >= k).sum() + 1) / (NR + 1)
lo = (ex/N + 1.96**2/(2*N) - 1.96*math.sqrt(ex/N*(1-ex/N)/N + 1.96**2/(4*N*N))) / (1 + 1.96**2/N)
P['P3_discrepancias_UR278'] = (p, f'filas={N}; exactas={ex}; un-digito={si}; fallo={1-ex/N:.2f}; nulo exactas={nulo[:,0].mean():.2f}, un-digito={nulo[:,1].mean():.2f}')
print('P3', P['P3_discrepancias_UR278'])

# ---- P4 o-pe-ro
inc = [q for q in grp if Q.get(q) == 'Incahuasi']
def count_c(gs, c):
    n = 0
    for v in gs:
        w = [a for a in v if a > 0 and a != c]
        if any(c == a + b for i, a in enumerate(w) for b in w[i+1:]): n += 1
    return n
obs = 0; nl = np.zeros(NR); used = []
for q in inc:
    gs = list(grp[q].values()); cnt = collections.Counter(v for g in gs for v in set(g) if v >= 10)
    if not cnt: continue
    c, m = cnt.most_common(1)[0]
    if m < 8: continue
    o = count_c(gs, c); obs += o; used.append((q, c, m, o))
    rest = [[a for a in g if a != c] for g in gs]; flat = np.array([a for g in rest for a in g]); sz = [len(g) for g in rest]
    for r in range(NR):
        f = rng.permutation(flat); i = 0; sh = []
        for s in sz: sh.append(list(f[i:i+s])); i += s
        nl[r] += count_c(sh, c)
P['P4_cuota_suma_de_dos'] = (((nl >= obs).sum() + 1) / (NR + 1), f'obs={obs}; nulo media={nl.mean():.2f}; quipus={used}')
print('P4', P['P4_cuota_suma_de_dos'])

# ---- Holm
it = sorted(P.items(), key=lambda kv: kv[1][0]); m = len(it); run = 0; out = []
for i, (k, (p, d)) in enumerate(it):
    run = max(run, min(1, (m - i) * p)); out.append((k, p, run, d))
with open('analisis/34_comparada/resultados_pruebas.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['prueba', 'p', 'p_holm', 'detalle']); w.writerows(out)
for r in out: print(r)
