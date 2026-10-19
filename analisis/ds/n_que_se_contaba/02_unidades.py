"""02. Unidades decimales incas: ¿se 'llenan' las unidades de 10/100/500/1000/10000?

Totales de grupo y de quipu a partir de cuerdas de nivel 0 (sin cuerdas
superiores, para no duplicar). Nulo: KDE gaussiana sobre log10(total), con
ancho fijo (0,05 decadas; sensibilidad 0,03 y 0,08). Se compara el numero
observado en cada ventana +-10 % con el esperado integrando la KDE.

Ademas:
  - fraccion de totales multiplos de 10/100/1000 (redondeo exacto);
  - uniformidad de log10(total) mod 1 (KS);
  - nulo estructural: barajar valores entre grupos del mismo quipu (conserva
    tamano de grupo, total del quipu y distribucion de valores).
"""
import numpy as np
import pandas as pd
from scipy.stats import ks_1samp, chi2
import comun as C

rng = np.random.default_rng(C.SEED)
B = 5000
c = C.cargar()
b = c[(c.nivel == 0) & (c.union != "T")]

g = b.groupby(["kfg", "grupo"]).v.sum(min_count=1)
g = g[g > 0]
q = b.groupby("kfg").v.sum(min_count=1)
q = q[q > 0]

UNIDADES = [10, 50, 100, 500, 1000, 5000, 10000]
FACTOR = 1.10


def ventanas(tot, unidades=UNIDADES, factor=FACTOR):
    tot = np.asarray(tot, float)
    return {u: (tot >= u / factor) & (tot <= u * factor) for u in unidades}


def kde_log(tot, bw):
    """KDE gaussiana sobre log10(tot); devuelve funcion de densidad."""
    x = np.log10(np.asarray(tot, float))
    n = len(x)

    def dens(y):
        y = np.atleast_1d(np.asarray(y, float))
        z = (y[:, None] - x[None, :]) / bw
        return np.exp(-0.5 * z ** 2).sum(1) / (n * bw * np.sqrt(2 * np.pi))
    return dens


def esperado_ventana(dens, u, factor, ngrid=4000):
    lo, hi = np.log10(u / factor), np.log10(u * factor)
    xs = np.linspace(lo, hi, ngrid)
    return np.trapezoid(dens(xs), xs)


def analizar(tot, nombre, bw=0.05):
    tot = np.asarray(tot, float)
    tot = tot[tot >= 30]          # por debajo, log no es interpretable
    n = len(tot)
    dens = kde_log(tot, bw)
    print(f"\n--- {nombre}: n={n} (totales >=30), mediana {np.median(tot):.0f} ---")
    print("unidad   obs   esp(KDE)   ratio   p_Poisson(una cola)")
    filas = []
    for u in UNIDADES:
        m = (tot >= u / FACTOR) & (tot <= u * FACTOR)
        obs = int(m.sum())
        esp = n * esperado_ventana(dens, u, FACTOR)
        # p Poisson exacto de observar >= obs con media esp
        from scipy.stats import poisson
        p = poisson.sf(obs - 1, esp) if esp > 0 else np.nan
        print(f"{u:6d} {obs:5d} {esp:9.1f} {obs/esp if esp else np.nan:7.2f}   {p:.4f}")
        filas.append(dict(conjunto=nombre, unidad=u, obs=obs, esp=esp,
                          ratio=obs / esp if esp else np.nan, p=p))
    return filas


filas = []
filas += analizar(g.to_numpy(), "grupos")
filas += analizar(q.to_numpy(), "quipus")
D = pd.DataFrame(filas)
D["q"] = C.bh(D.p.to_numpy())
print("\nBH sobre las 14 pruebas:")
print(D[["conjunto", "unidad", "obs", "esp", "ratio", "p", "q"]].round(4).to_string(index=False))
print("pruebas con exceso significativo (q<0.05 y ratio>1):",
      int(((D.q < .05) & (D.ratio > 1)).sum()))

# sensibilidad del ancho de banda
print("\n=== Sensibilidad al ancho de banda (ratio obs/esp) ===")
for bw in (0.03, 0.05, 0.08):
    dg = kde_log(g[g >= 30].to_numpy(), bw)
    dq = kde_log(q[q >= 30].to_numpy(), bw)
    rg = [((g >= u / FACTOR) & (g <= u * FACTOR)).sum() / (len(g[g >= 30]) * esperado_ventana(dg, u, FACTOR)) for u in UNIDADES]
    rq = [((q >= u / FACTOR) & (q <= u * FACTOR)).sum() / (len(q[q >= 30]) * esperado_ventana(dq, u, FACTOR)) for u in UNIDADES]
    print("bw=%.2f grupos %s | quipus %s" % (bw, np.round(rg, 2).tolist(), np.round(rq, 2).tolist()))

# ---------------------------------------------------------------- redondeo exacto
print("\n=== Redondeo exacto (multiplos) ===")
for nombre, s in [("grupos", g), ("quipus", q)]:
    for m in (10, 100, 1000):
        frac = float((s % m == 0).mean())
        # esperado bajo continuo local: 1/m; bajo la distribucion observada de residues
        # nulo: barajar el ultimo digito no tiene sentido; usamos 1/m y un chi2 de uniformidad
        print("%-7s multiplos de %4d: %.3f (esperado continuo %.3f)" % (nombre, m, frac, 1 / m))
    # chi2 de uniformidad de t mod 100 para t>=100
    s2 = s[s >= 100].to_numpy()
    cnt = np.bincount((s2 % 100).astype(int), minlength=100)
    st = chi2.sf(((cnt - cnt.mean()) ** 2 / cnt.mean()).sum(), 99)
    print("   chi2 uniformidad mod 100 (n=%d): p=%.2e; residuo 0 = %d (esp %.1f)" %
          (len(s2), st, cnt[0], len(s2) / 100))

# control: ¿el redondeo viene de las cuerdas o se añade al total?
print("\n=== Control: ¿los multiplos de 10 se heredan de las cuerdas? ===")
base = b[["kfg", "grupo", "v"]].dropna().copy()
base["dec"] = (base.v // 10) * 10
base["ud"] = (base.v % 10).astype(int)
obs10 = float((base.groupby(["kfg", "grupo"]).v.sum() % 10 == 0).mean())
sim10 = []
for _ in range(500):
    ud = rng.permutation(base.ud.to_numpy())
    gv = (base.dec + ud).groupby([base.kfg, base.grupo]).sum()
    sim10.append(float((gv % 10 == 0).mean()))
print("observado %.4f ; nulo (barajar digito de unidades entre cuerdas) %.4f [%.4f,%.4f]" %
      (obs10, np.mean(sim10), *np.percentile(sim10, [2.5, 97.5])))
print("(si el total se redondeara ademas de las cuerdas, el observado superaria el nulo)")

# ---------------------------------------------------------------- log-uniformidad
print("\n=== log10(total) mod 1: ¿hay escala preferida? ===")
for nombre, s in [("grupos", g), ("quipus", q)]:
    x = np.log10(s[s >= 30].to_numpy()) % 1
    st = ks_1samp(x, lambda z: z)
    print("%-7s KS vs U(0,1): D=%.3f p=%.2e  (n=%d)" % (nombre, st.statistic, st.pvalue, len(x)))
    # masa cerca de 0 (potencias de 10) y de log10(5)=0.699
    print("        masa [0,0.05) = %.3f (esp 0.05); [0.65,0.75) = %.3f (esp 0.10)" %
          ((x < .05).mean(), ((x >= .65) & (x < .75)).mean()))

# ---------------------------------------------------------------- nulo estructural
print("\n=== Nulo estructural: barajar valores entre grupos del mismo quipu ===")
# observado: fraccion de grupos en ventanas
mask_obs = {u: ((g >= u / FACTOR) & (g <= u * FACTOR)) for u in UNIDADES}
obs_frac = {u: float(mask_obs[u].mean()) for u in UNIDADES}
# simular: dentro de cada quipu, permutar los valores de nivel 0 entre las cuerdas
base = b[["kfg", "grupo", "v"]].dropna().copy()
sim_frac = {u: [] for u in UNIDADES}
for _ in range(1000):
    vals = base.groupby("kfg").v.transform(lambda s: rng.permutation(s.to_numpy()))
    gg = base.assign(v=vals).groupby(["kfg", "grupo"]).v.sum(min_count=1)
    gg = gg[gg > 0]
    for u in UNIDADES:
        sim_frac[u].append(float(((gg >= u / FACTOR) & (gg <= u * FACTOR)).mean()))
print("unidad  obs_frac  nulo_medio  p(obs>=nulo)")
for u in UNIDADES:
    sim = np.array(sim_frac[u])
    print("%6d  %.4f    %.4f      %.4f" %
          (u, obs_frac[u], sim.mean(), (sim >= obs_frac[u]).mean()))

D.to_csv(C.OUT / "unidades_decimales.csv", index=False)
print("\nguardado unidades_decimales.csv")
