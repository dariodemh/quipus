"""Rasgos de contenido: seriacion de valores y banding de color, con nulo
(barajar dentro de cada quipu, 500 veces, semilla 0)."""
import pandas as pd, numpy as np

RAIZ = "../../../"
c = pd.read_csv(RAIZ + "analisis/datos/cuerdas.csv")
HP = [f"HP{i:03d}" for i in range(1, 33)]
hp = c[c.kfg.isin(HP)].copy()
hp["v"] = pd.to_numeric(hp.valor, errors="coerce")

def monotonic_frac(k):
    d = hp[hp.kfg == k].sort_values("orden")
    tot = 0; mono = 0
    for _, g in d.groupby("grupo"):
        v = g["v"].dropna().to_numpy(float)
        if len(v) < 3: continue
        for i in range(len(v) - 1):
            tot += 1
            if (i > 0):
                pass
        # monotona si las diferencias no cambian de signo
        dv = np.diff(v)
        nz = dv[dv != 0]
        if len(nz) >= 1 and (np.all(nz > 0) or np.all(nz < 0)):
            mono += 1
        tot -= (len(v) - 1)
    return mono, sum(len(g["v"].dropna()) >= 3 for _, g in d.groupby("grupo"))

def band_frac(k):
    d = hp[hp.kfg == k].sort_values("orden")
    col = d["color"].fillna("").astype(str).to_numpy()
    if len(col) < 2: return 0, 0
    same = sum(1 for i in range(len(col) - 1) if col[i] != "" and col[i] == col[i+1])
    return same, len(col) - 1

obs_mono = sum(monotonic_frac(k)[0] for k in HP)
n_mono_groups = sum(monotonic_frac(k)[1] for k in HP)
obs_same = sum(band_frac(k)[0] for k in HP)
n_adj = sum(band_frac(k)[1] for k in HP)
print(f"seriacion: {obs_mono} grupos monotonos de {n_mono_groups} grupos(>=3)  ({obs_mono/max(n_mono_groups,1):.2f})")
print(f"banding color: {obs_same} adyacentes iguales de {n_adj}  ({obs_same/max(n_adj,1):.2f})")

rng = np.random.default_rng(0)
seqs = {k: hp[hp.kfg == k].sort_values("orden")["v"].to_numpy(float) for k in HP}
cols = {k: hp[hp.kfg == k].sort_values("orden")["color"].fillna("").astype(str).to_numpy() for k in HP}
null_mono, null_same = [], []
for _ in range(500):
    tot_m = 0; tot_s = 0
    for k in HP:
        vv = seqs[k].copy(); rng.shuffle(vv)
        d = hp[hp.kfg == k].sort_values("orden")
        gsz = d.groupby("grupo").size().to_numpy()
        idx = 0; m = 0; ng = 0
        for s in gsz:
            v = vv[idx:idx+s]; idx += s
            v = v[~np.isnan(v)]
            if len(v) >= 3:
                ng += 1
                dv = np.diff(v); nz = dv[dv != 0]
                if len(nz) >= 1 and (np.all(nz > 0) or np.all(nz < 0)): m += 1
        tot_m += m
        cc = cols[k].copy(); rng.shuffle(cc)
        tot_s += sum(1 for i in range(len(cc)-1) if cc[i] != "" and cc[i] == cc[i+1])
    null_mono.append(tot_m); null_same.append(tot_s)
null_mono = np.array(null_mono); null_same = np.array(null_same)
p_mono = (np.sum(null_mono >= obs_mono)+1)/(len(null_mono)+1)
p_same = (np.sum(null_same >= obs_same)+1)/(len(null_same)+1)
print(f"nulo seriacion: media={null_mono.mean():.1f} sd={null_mono.std():.1f} p={p_mono:.4f}")
print(f"nulo banding:   media={null_same.mean():.1f} sd={null_same.std():.1f} p={p_same:.4f}")

# escala de valores por quipu: mediana
print("\n== escala (mediana de valores) por quipu ==")
med = {k: float(np.nanmedian(seqs[k][~np.isnan(seqs[k])])) if (~np.isnan(seqs[k])).any() else np.nan for k in HP}
for k in HP:
    print(f"  {k}: mediana={med[k]:.0f}")
