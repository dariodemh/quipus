"""26_clave_local / estructura: representaciones, conteo de pares y POTENCIA, antes de mirar acuerdos (diseno.md §6).

No calcula distancias entre quipus: solo qué pares comparten patrón (estructura) y simula concordancias.
Uso: python analisis/26_clave_local/estructura.py
Salidas: patrones.csv, quipus26.csv, archivos26.csv, estructura.csv, salida_estructura.txt
"""
import sys, itertools
sys.path.insert(0, 'analisis/26_clave_local')
from comun26 import *  # noqa

L = []
def say(*a):
    s = ' '.join(map(str, a)); print(s); L.append(s)

construir_reps()
REP, R3 = cargar_reps()
q = tabla_quipus()
q[['kfg', 'inv', 'museo', 'procedencia', 'MUSEUM_NUM', 'archivo', 'archivo_sitio']].to_csv(A26 + 'archivos26.csv', index=False)
lab = dict(zip(q.kfg, q.archivo.where(q.archivo.notna(), None)))
invs = dict(zip(q.kfg, q.inv))
EX = pares_excluidos()
rng = np.random.default_rng(SEED)

filas = []
for R in ('R1', 'R2'):
    ks = sorted(k for k in REP[R] if lab.get(k) not in ('UR053', 'Incahuasi') and k in invs)
    say(f'\n== {R}: quipus elegibles (sin UR053 ni Incahuasi) {len(ks)}; por investigador {pd.Series([invs[k] for k in ks]).value_counts().to_dict()}')
    SH = {}
    for a, b in itertools.combinations(ks, 2):
        if frozenset((a, b)) in EX or misma_base(a, b): continue
        SH[frozenset((a, b))] = float(any(t in REP[R][b] for t in REP[R][a]))
    df = pd.DataFrame([dict(a=tuple(p)[0], b=tuple(p)[1], comparte=v) for p, v in SH.items()])
    df['inv'] = np.where(df.a.map(invs) == df.b.map(invs), df.a.map(invs), 'cruzado')
    df['dentro'] = [lab[a] is not None and lab[a] == lab[b] for a, b in zip(df.a, df.b)]
    t = df.groupby(['inv', 'dentro']).comparte.agg(['size', 'sum']).reset_index()
    say(t.to_string())
    for r in t.itertuples():
        filas.append(dict(R=R, inv=r.inv, dentro=r.dentro, n_pares=r.size, n_comparten=int(r.sum)))
    # potencia: S simulada sobre pares que comparten patrón
    for p1, p0 in ((.22, .05), (.15, .05), (.30, .10)):
        hits = []
        for _ in range(200):
            S = {pr: float(v and rng.random() < (p1 if (lab[tuple(pr)[0]] is not None and lab[tuple(pr)[0]] == lab[tuple(pr)[1]]) else p0)) for pr, v in SH.items()}
            hits.append(prueba_perm(ks, S, lab, invs, B=199, rng=rng)['p'] < .05)
        say(f'  potencia {R} (p1={p1}, p0={p0}; alfa .05 nominal, 200 sim, B=199): {np.mean(hits):.2f}')
        filas.append(dict(R=R, inv='POTENCIA', p1=p1, p0=p0, potencia=np.mean(hits)))
pd.DataFrame(filas).to_csv(A26 + 'estructura.csv', index=False)
open(A26 + 'salida_estructura.txt', 'w', encoding='utf-8').write('\n'.join(L))
