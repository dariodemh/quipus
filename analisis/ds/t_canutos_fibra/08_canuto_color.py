"""
Los canutos llevan una SECUENCIA de color (bandas de ~3 cm). Que codifica?

 (1) estructura de las secuencias: repeticion y corrimiento ("sliding window")
 (2) coinciden con el color de las cuerdas que envuelven? (nulo: permutar
     secuencias de canuto dentro del quipu)
 (3) coinciden con los limites de grupo / de cluster?
"""
import os, sqlite3
import numpy as np
import pandas as pd
from scipy import stats

BASE = r"."
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20241018)
con = sqlite3.connect(os.path.join(BASE, "data", "external", "open-khipu-repository",
                                   "data", "khipu.db"))
q = pd.read_csv(os.path.join(OUT, "quipus.csv"))
cord = pd.read_csv(os.path.join(OUT, "cuerdas_okr.csv"), low_memory=False)

a = pd.read_sql("select * from ascher_canuto_color", con)
a = a.sort_values(["CANUTO_ID", "COLOR_RANGE"])
# secuencia = colores de banda (se colapsan duplicados consecutivos)
seqs = {}
for cid, g in a.groupby("CANUTO_ID"):
    cols = g.COLOR_CD_1.tolist()
    ded = [c for i, c in enumerate(cols) if i == 0 or c != cols[i - 1]]
    seqs[cid] = tuple(ded)
can = pd.read_sql("select * from canuto", con).sort_values(["KHIPU_ID", "CTO_ORDINAL"])
can["seq"] = can.CANUTO_ID.map(seqs)

print("=" * 72)
print("(1) ESTRUCTURA DE LAS SECUENCIAS DE COLOR DEL CANUTO")
print("canutos con color: %d de %d" % (can.seq.notna().sum(), len(can)))
print("n de bandas por canuto:")
print(can.seq.dropna().apply(len).value_counts().sort_index().to_string())
print("\ncanutos por quipu, secuencias distintas y runs:")
rows = []
for kid, g in can.groupby("KHIPU_ID"):
    s = g.seq.tolist()
    seqs_nc = [x for x in s if isinstance(x, tuple)]
    if not seqs_nc:
        continue
    runs = 1 + sum(1 for i in range(1, len(seqs_nc)) if seqs_nc[i] != seqs_nc[i - 1])
    # transiciones que son "corrimiento": comparten >=2 bandas y difieren en 1
    shift = 0
    tot = 0
    for i in range(1, len(seqs_nc)):
        A, B = set(seqs_nc[i - 1]), set(seqs_nc[i])
        if A != B:
            tot += 1
            if len(A & B) >= max(1, min(len(A), len(B)) - 1):
                shift += 1
    rows.append(dict(quipu=int(kid), n_can=len(seqs_nc), n_seq=len(set(seqs_nc)),
                     runs=runs, transiciones=tot, corrimientos=shift,
                     frac_corr=(shift / tot) if tot else np.nan))
S = pd.DataFrame(rows)
print(S.to_string(index=False))
print("\ncanutos por run (mediana): %.1f" % np.median(
    can.groupby(["KHIPU_ID", (can.seq != can.groupby("KHIPU_ID").seq.shift()).cumsum()]).size()))
print("total transiciones: %d, de ellas 'corrimiento' (comparten >=2 bandas): %d (%.0f%%)"
      % (S.transiciones.sum(), S.corrimientos.sum(),
         100 * S.corrimientos.sum() / max(1, S.transiciones.sum())))
# linea base: pares de secuencias distintas elegidos al azar dentro del mismo quipu
base_share, base_n = 0, 0
for kid, g in can.groupby("KHIPU_ID"):
    lst = [x for x in g.seq if isinstance(x, tuple)]
    if len(lst) < 3:
        continue
    for _ in range(400):
        i, j = rng.choice(len(lst), 2, replace=False)
        if lst[i] != lst[j]:
            base_n += 1
            if len(set(lst[i]) & set(lst[j])) >= 2:
                base_share += 1
print("azar: pares de secuencias distintas que comparten >=2 bandas = %.0f%% (n=%d pares)"
      % (100 * base_share / max(1, base_n), base_n))

print("\n" + "=" * 72)
print("(2) COINCIDEN CON EL COLOR DE LAS CUERDAS QUE ENVUELVEN?")
res = []
for kid, g in can.groupby("KHIPU_ID"):
    c1 = cord[(cord.KHIPU_ID == kid) & (cord.CORD_LEVEL >= 1)].copy()
    c1 = c1.sort_values(["CORD_LEVEL", "CORD_ORDINAL"])
    # ordenar las cuerdas de nivel 1 como lo hace el canuto (CTO_BEG_CORD)
    g1 = cord[(cord.KHIPU_ID == kid) & (cord.CORD_LEVEL == 1)].sort_values("CORD_ORDINAL")
    if len(g1) < 10:
        continue
    col = g1.color.fillna("NA").astype(str).str.split(":").str[0].str.split("-").str[0].values
    obs_hit, obs_n = 0, 0
    mapa = []
    for _, r in g.iterrows():
        b, e = int(r.CTO_BEG_CORD), int(r.CTO_END_CORD)
        if not isinstance(r.seq, tuple) or e > len(col):
            continue
        cc = col[b - 1:e]
        # se compara el conjunto de colores del canuto con el de sus cuerdas
        hit = len(set(r.seq) & set(cc)) / len(set(r.seq))
        obs_hit += hit
        obs_n += 1
        mapa.append(hit)
    if obs_n == 0:
        continue
    obs = np.mean(mapa)
    # nulo: reasignar las secuencias de canuto a otras posiciones del mismo quipu
    seqs_k = [r.seq for _, r in g.iterrows()]
    lims = [(int(r.CTO_BEG_CORD), int(r.CTO_END_CORD)) for _, r in g.iterrows()]
    cnt = 0
    for _ in range(5000):
        lst = [s for s in seqs_k if isinstance(s, tuple)]
        perm = [lst[i] for i in rng.permutation(len(lst))]
        j = 0
        vals = []
        for (b, e) in lims:
            if e > len(col) or j >= len(perm):
                continue
            cc = set(col[b - 1:e])
            vals.append(len(set(perm[j]) & cc) / len(set(perm[j])))
            j += 1
        if np.mean(vals) >= obs:
            cnt += 1
    res.append(dict(quipu=int(kid), n_can=obs_n, solape=obs,
                    n_colores_cuerda=len(set(col)),
                    p=(cnt + 1) / 5001))
R = pd.DataFrame(res)
print(R.round(3).to_string(index=False))
print("\nNota: con 2-4 colores de cuerda el solape por azar ya es alto;")
print("el p-valor es lo informativo, no el nivel absoluto.")

print("\n" + "=" * 72)
print("(3) SECUENCIA DE KH0280 (UR050), el caso completo")
g = can[can.KHIPU_ID == 1000363]
print(g[["CTO_ORDINAL", "CTO_BEG_CORD", "CTO_END_CORD", "NUM_CORDS", "seq"]]
      .assign(seq=g.seq.apply(lambda s: "-".join(s) if isinstance(s, tuple) else None)).to_string(index=False))
R.to_csv(os.path.join(OUT, "canuto_color.csv"), index=False)
S.to_csv(os.path.join(OUT, "canuto_secuencias.csv"), index=False)
