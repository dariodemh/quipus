"""Diagnostico: (1) la senal A se debe a enteros pequenos comunes?
(2) secuencias de los pares top; (3) pares que son el MISMO objeto (RN compartido)."""
import pandas as pd, numpy as np
from itertools import combinations

RAIZ = "../../../"
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
HP = [f"HP{i:03d}" for i in range(1, 33)]
hp = c[c.kfg.isin(HP)].copy()
hp["v"] = pd.to_numeric(hp.valor, errors="coerce")
seqs = {k: hp[hp.kfg == k].sort_values("orden")["v"].to_numpy(float) for k in HP}
pairs = list(combinations(HP, 2))

def am(seqA, seqB, minv=2):
    n = min(len(seqA), len(seqB)); a, b = seqA[:n], seqB[:n]
    m = ~np.isnan(a) & ~np.isnan(b) & (a == b) & (a >= minv)
    return int(m.sum())

for minv in (2, 10, 50, 100):
    obs = sum(am(seqs[a], seqs[b], minv) for a, b in pairs)
    # raro: cuantas cuerdas en rango total
    tot = sum(int((~np.isnan(seqs[k]) & (seqs[k] >= minv)).sum()) for k in HP)
    print(f"val>={minv}: matches={obs} cuerdas_candidatas={tot}")

# frecuencia de valores: cuantos pares comparten por valor
allv = pd.concat([pd.Series(seqs[k]) for k in HP]).dropna()
print("\ntop valores repetidos globalmente:")
print(allv.astype(int).value_counts().head(10).to_string())

# pares mismo objeto (RN compartido)
kh = pd.read_csv(RAIZ + "data/external/open-khipu-repository/data/okr-kh-numbers.csv")
kh["okr"] = kh["OKR Number"].str.strip()
hpkh = kh[kh["OKR Number"].str.startswith("KH05") & kh["Other Names"].notna()]
hpkh = hpkh[hpkh["Other Names"].str.contains("HP0", na=False)].copy()
hpkh["rn"] = hpkh["Collection Number"].astype(str).str.extract(r"RN\s*(\d+)")
hpkh["hp"] = hpkh["Other Names"].str.extract(r"(HP\d{3}[_A-Z]*)")
sub = hpkh[hpkh["hp"].isin(HP)]
dup = sub.groupby("rn")["hp"].apply(list)
print("\nRN compartido entre quipus HP001-HP032:")
print(dup[dup.map(len) > 1].to_string())

# secuencias de pares interesantes
for (a, b) in [("HP014", "HP031"), ("HP017", "HP031"), ("HP001", "HP002"), ("HP029", "HP030")]:
    print(f"\n--- {a} ---"); print(np.nan_to_num(seqs[a], nan=-1).astype(int)[:40])
    print(f"--- {b} ---"); print(np.nan_to_num(seqs[b], nan=-1).astype(int)[:40])
