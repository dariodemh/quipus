import pandas as pd, numpy as np
rng = np.random.default_rng(0)
c = pd.read_csv('analisis/datos/cuerdas.csv')
d = c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
val = d.valor.to_numpy(dtype=float)
pos = np.where(val>0)[0]
w = val[pos]
N = len(w)
print("N nonzero cords:", N)

def matched(w):
    A = np.concatenate([[0.0], np.cumsum(w)])
    # sums[i,j] = A[j]-A[i], elements i..j-1, length j-i>=2
    sums = A[np.newaxis,:] - A[:,np.newaxis]   # sums[i,j]
    n = len(w)
    ii, jj = np.tril_indices(n+1, k=-2)  # j-i>=2 -> row i, col j with j-i>=2
    # careful orientation: sums[i,j] with j>i corresponds to elements i..j-1
    run_sums = sums[ii, jj]
    run_sums = run_sums[run_sums>0]
    us = np.unique(run_sums)
    return np.isin(w, us).sum()

obs = matched(w)
print("OBSERVED matched cords (value = sum of >=2 consecutive nonzero cords):", obs, f"({100*obs/N:.1f}%)")
nulls = np.empty(1000)
for t in range(1000):
    ws = rng.permutation(w)
    nulls[t] = matched(ws)
p = (1 + (nulls>=obs).sum())/(1+1000)
print("null mean", nulls.mean(), "sd", nulls.std(), "max", nulls.max(), "min", nulls.min())
print("p-value empirico:", p)
np.save('analisis/ds/k_AS069/null_runs.npy', nulls)
