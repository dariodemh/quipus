"""Potencia complementaria de r3: lista de 11 pueblos de m40 SIN los totales 823/260, y lista de 9 servicios de m4,
insertadas con 2 errores de ±1 dígito en 100 quipus al azar (>= 40 cuerdas)."""
import numpy as np
from r3_rosetta import cargar, consultas, pesos, sw, p_adapt, SEED

c, seqs = cargar()
todos = c.valor.to_numpy(float)
Q = consultas()
rng = np.random.default_rng(SEED + 7)
ks = [k for k, s in seqs.items() if len(s) >= 40]
thr = 0.05 / 10208
lines = []
for nom, q in (("m40 sin totales (11 pueblos)", Q["m40_aldana_aullagas"][2:]), ("m4 (9 servicios)", Q["m4_chupaychos_inca"])):
    w, _ = pesos(q, todos)
    ps = []
    for t in range(100):
        s = seqs[ks[rng.integers(len(ks))]].copy()
        ins = q.copy()
        for j in rng.choice(len(ins), 2, replace=False):
            ins[j] += rng.choice([-1, 1]) * (10 if ins[j] >= 10 else 1)
        i0 = rng.integers(0, len(s) - len(ins))
        s[i0:i0 + len(ins)] = ins
        ps.append(p_adapt(s, q, w, sw(s, q, w), SEED + 20_000 + t)[0])
    ps = np.array(ps)
    lines.append(f"{nom}: info máx {w.sum():.1f}; p mediana {np.median(ps):.1e}; detectada a p <= {thr:.1e} en {(ps <= thr).mean():.0%}; p<0,001 en {(ps < .001).mean():.0%}")
open("r3b_resumen.txt", "w", encoding="utf8").write("\n".join(lines))
print("\n".join(lines))
