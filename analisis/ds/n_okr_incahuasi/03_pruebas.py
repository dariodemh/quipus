"""03 - Pruebas centrales de Incahuasi repetidas con OKR (mismas definiciones que 13 y 18).

T1  UR273A + UR273B -> cabeceras/cuerdas de UR266+UR275 (+UR269)   [13/04, 1a]
T2  UR274A + UR273B -> idem (control de la copia que rellena huecos)
T3  UR270 (P + primera subsidiaria) -> filas de UR278, columna a columna [13/07]
T4  totales de grupo de UR278 -> cuerdas de UR266 (y UR275)          [13/02, 04]
T5  UR267A + UR267B -> UR269: (a) todas las cuerdas, (b) solo cabeceras, (c) registros con cuota 25
T6  cuota 17 en UR273B / UR274B (neto x-17 y 17 explicito tras la cabecera) [13/03]
Nulos: los mismos de 13/18. Semilla fija. 10 000 replicas (5 000 en T3/T6). Holm sobre la familia principal.

Salida: pruebas_okr.csv, detalle_t1.csv, detalle_t3.csv.
"""
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
import sys
import lib_okr as L

FUENTE = sys.argv[1] if len(sys.argv) > 1 else "okr"
SEED = 4218
rng = np.random.default_rng(SEED)
N1 = 10000
N2 = 5000
c = L.cargar(FUENTE)
P = []          # pruebas
FIL = []


def add(nombre, obs, nul, n=None, familia="principal", nota=""):
    nul = np.asarray(nul)
    P.append(dict(prueba=nombre, n=n, obs=int(obs), nulo_media=float(nul.mean()),
                  nulo_max=int(nul.max()), p=float((np.sum(nul >= obs) + 1) / (len(nul) + 1)),
                  familia=familia, nota=nota))


# ---------------- T1 / T2 : sumas A+B ----------------
def test_ab(qa, qb, destinos, familia="principal"):
    a, b, ga, gb = L.pares(c, qa, qb)
    S = L.conjunto(c, destinos)
    obs = int(L.hallados(a + b, S).sum())
    nul = np.array([L.hallados(a + rng.permutation(b), S).sum() for _ in range(N1)])
    add(f"{qa}+{qb} -> {'+'.join(destinos)}", obs, nul, n=len(a), familia=familia)
    # detalle
    for x, y, gx, gy in zip(a, b, ga, gb):
        d = c[c.pres & c.kfg.isin(destinos) & (c.valor == x + y)]
        FIL.append(dict(fuente=f"{qa}+{qb}", grupo_A=gx, grupo_B=gy, A=x, B=y, suma=x + y,
                        destino=" ".join(f"{r.kfg}:g{r.grupo}:{r.cuerda}:{r.valor}" for r in d.itertuples())))
    return obs, len(a), a, b


print("== T1/T2 sumas A+B")
o1, n1, a1, b1 = test_ab("UR273A", "UR273B", ["UR266", "UR275"])
print(f"  UR273A+B -> UR266+UR275: {o1}/{n1}")
o1b, _, _, _ = test_ab("UR273A", "UR273B", ["UR266", "UR275", "UR269"], familia="secundaria")
print(f"  UR273A+B -> UR266+UR275+UR269: {o1b}/{n1}")
o2, n2, a2, b2 = test_ab("UR274A", "UR273B", ["UR266", "UR275"], familia="secundaria")
print(f"  UR274A+UR273B -> UR266+UR275: {o2}/{n2}")
o3, n3, a3, b3 = test_ab("UR274A", "UR274B", ["UR266", "UR275"], familia="secundaria")
print(f"  UR274A+UR274B -> UR266+UR275: {o3}/{n3}")

# ---------------- T3 : UR270 -> UR278 ----------------
print("\n== T3 UR270 -> UR278 (celdas)")
u = c[c.kfg == "UR270"]
G = {}
for g, x in u.groupby("grupo"):
    x0 = x[x.nivel == 0]
    if x0.pres.sum() < 7:
        continue
    filas = []
    for _, p in x0.iterrows():
        s1 = x[(x.cuerda == p.cuerda + "s1") & (x.nivel == 1)]
        sv = int(s1.valor.iloc[0]) if len(s1) and bool(s1.pres.iloc[0]) else 0
        filas.append((int(p.valor) if p.pres else -10**6, sv))
    G[g] = np.array(filas)
t = c[(c.kfg == "UR278") & (c.nivel == 0)]
H = {}
for h, x in t.groupby("grupo"):
    x0 = x[x.nivel == 0]
    if x0.pres.sum() >= 7:
        H[h] = np.where(x0.pres, x0.valor, -10**6).astype(int)


def aciertos(v, w):
    n = min(len(v), len(w))
    ok = (v[:n] > 0) & (w[:n] > 0)
    return int(np.sum(ok & (np.abs(v[:n] - w[:n]) <= 1)))


def mejor(cols):
    return {g: max((aciertos(v, w), h) for h, w in H.items()) for g, v in cols.items()}


def estad(cols):
    m = mejor(cols)
    return sum(a >= 6 for a, _ in m.values()), sum(a for a, _ in m.values())


PS = {g: np.where(a[:, 0] > 0, a[:, 0] + a[:, 1], -10**6) for g, a in G.items()}
PSm = {g: np.where(a[:, 0] > 0, a[:, 0] + a[:, 1], -10**6) for g, a in G.items()}
onlyP = {g: a[:, 0] for g, a in G.items()}
o6, osum = estad(PS)
n1n = np.array([estad({g: rng.permutation(v) for g, v in PS.items()}) for _ in range(N2)])
add("UR270 P+S1 -> UR278: grupos con >=6 columnas", o6, n1n[:, 0], n=len(PS))
add("UR270 P+S1 -> UR278: total de aciertos", osum, n1n[:, 1], n=len(PS), familia="secundaria")
n2n = []
for _ in range(N2):
    cc = {g: np.where(a[:, 0] > 0, a[:, 0] + rng.permutation(a[:, 1]), -10**6) for g, a in G.items()}
    n2n.append(estad(cc))
n2n = np.array(n2n)
add("UR270 P+S1 -> UR278: nulo 2 (barajar S entre colgantes)", o6, n2n[:, 0], n=len(PS), familia="secundaria")
c6, csum = estad(onlyP)
add("UR270 solo P -> UR278 (control)", c6, np.zeros(N2, int), n=len(onlyP), familia="control",
    nota=f"control negativo: {c6} grupos con >=6; sin nulo, el maximo posible bajo P sola no se simula")
print(f"  P+S1: {o6} grupos con >=6 columnas, {osum} aciertos; nulo1 {n1n[:,0].mean():.2f}/{n1n[:,1].mean():.1f}; nulo2 {n2n[:,0].mean():.2f}")
print(f"  solo P (control): {c6} grupos, {csum} aciertos")
det = []
for g, (a_, h) in sorted(mejor(PS).items()):
    det.append(dict(grupo_UR270=g, fila_UR278=h, aciertos=a_,
                    P=" ".join(map(str, G[g][:, 0])), S1=" ".join(map(str, G[g][:, 1])),
                    P_mas_S1=" ".join(str(x) if x > 0 else "·" for x in PS[g]),
                    UR278=" ".join(str(x) if x > 0 else "·" for x in H[h])))
pd.DataFrame(det).to_csv(L.AQUI / f"detalle_t3_{FUENTE}.csv", index=False)

# ---------------- T4 : UR278 -> UR266 / UR275 ----------------
print("\n== T4 UR278 totales de grupo -> UR266 / UR275")
lv0 = c[(c.kfg == "UR278") & (c.nivel == 0)].copy()
g278 = lv0[lv0.pres].groupby("grupo").valor.agg(["sum", "size"])
g278 = g278[g278["size"] >= 2]
tot = g278["sum"].to_numpy()
v0 = lv0.valor.to_numpy()


def totales(vals):
    s = lv0.assign(v=vals)
    g = s[s.pres].groupby("grupo").v.agg(["sum", "size"])
    return g[g["size"] >= 2]["sum"].to_numpy()


for dest in ["UR266", "UR275"]:
    S = L.conjunto(c, [dest])
    obs = int(np.isin(tot, S).sum())
    nul = np.array([np.isin(totales(rng.permutation(v0)), S).sum() for _ in range(N1)])
    add(f"UR278 totales de grupo -> {dest}", obs, nul, n=len(tot))
    print(f"  -> {dest}: {obs} exactas de {len(tot)} filas; nulo {nul.mean():.1f} (max {nul.max()}); p={(np.sum(nul>=obs)+1)/(N1+1):.4g}")
    # orden (tau) de los aciertos con las cabeceras del destino
    hdr = pd.read_csv(L.AQUI / "cuerdas_okr.csv", keep_default_na=False)
    hdr = hdr[(hdr.kfg == dest) & (hdr.pres.astype(str).str.lower() == "true") & (hdr.nivel == 0)]
    hdr = hdr.sort_values("orden").groupby("grupo").valor.first().to_numpy()
    pares = [(i, int(np.where(hdr == v)[0][0])) for i, v in enumerate(tot) if v in hdr]
    if len(pares) >= 3:
        tau = kendalltau([p[0] for p in pares], [p[1] for p in pares]).statistic
        print(f"     tau de orden con cabeceras de {dest}: {tau:.2f} ({len(pares)} pares)")

# ---------------- T5 : UR267A+B -> UR269 ----------------
print("\n== T5 UR267A+UR267B -> UR269")
a, b, ga, gb = L.pares(c, "UR267A", "UR267B")
S_all = L.conjunto(c, ["UR269"])
obs = int(L.hallados(a + b, S_all).sum())
nul = np.array([L.hallados(a + rng.permutation(b), S_all).sum() for _ in range(N1)])
add("UR267A+B -> UR269 (todas las cuerdas)", obs, nul, n=len(a))
print(f"  todas las cuerdas: {obs}/{len(a)}; nulo {nul.mean():.2f}; p={(np.sum(nul>=obs)+1)/(N1+1):.4g}")
hdr269 = L.registros(c, "UR269").x.dropna().to_numpy().astype(int)
obs = int(L.hallados(a + b, hdr269).sum())
nul = np.array([L.hallados(a + rng.permutation(b), hdr269).sum() for _ in range(N1)])
add("UR267A+B -> cabeceras de UR269", obs, nul, n=len(a))
print(f"  solo cabeceras: {obs}/{len(a)}; nulo {nul.mean():.2f}; p={(np.sum(nul>=obs)+1)/(N1+1):.4g}")

# dirigido: registros de UR269 con cuota 25
u = c[(c.kfg == "UR269") & c.pres]
objetivo = []
for g, x in u.groupby("grupo"):
    x0 = x[x.nivel == 0]
    if len(x0) and x0.valor.iloc[0] >= 100:
        xv = int(x0.valor.iloc[0])
        otros = x.valor.iloc[1:].to_numpy()
        if (otros == 25).any() or (otros == xv - 25).any():
            objetivo.append(xv)
objetivo = np.array(objetivo)
obs = int(L.hallados(objetivo, np.unique(a + b)).sum())
nul = np.array([L.hallados(objetivo, np.unique(a + rng.permutation(b))).sum() for _ in range(N1)])
add("UR269 cuota 25: cabecera = UR267A+B", obs, nul, n=len(objetivo))
print(f"  UR269 cuota 25: {obs}/{len(objetivo)} cabeceras son suma A+B; nulo {nul.mean():.2f}; p={(np.sum(nul>=obs)+1)/(N1+1):.4g}")

# ---------------- T6 : cuota 17 ----------------
print("\n== T6 cuota 17")


def regs17(s):
    R = []
    for g, x in s[s.pres].groupby("grupo"):
        x0 = x[x.nivel == 0]
        if len(x0) == 0 or len(x) < 2:
            continue
        cab = x0.index[0]
        xv = int(x0.valor.iloc[0])
        if xv < 100:
            continue
        resto = x.drop(cab)
        R.append((xv, resto.valor.to_numpy(int)))
    return R


def apoyo(X, rest, d):
    return sum(int(np.any(r == x - d)) for x, r in zip(X, rest))


def explicito(rest, d):
    return sum(int(np.any(r[:2] == d)) for r in rest)


for k in ["UR273B", "UR274B", "UR273A", "UR274A"]:
    R = regs17(c[c.kfg == k])
    if len(R) < 4:
        print(f"  {k}: solo {len(R)} registros, sin prueba")
        continue
    X = [x for x, _ in R]
    rest = [r for _, r in R]
    sizes = np.cumsum([len(r) for r in rest])[:-1]
    flat = np.concatenate(rest)
    oa, oe = apoyo(X, rest, 17), explicito(rest, 17)
    na, ne = [], []
    for _ in range(N2):
        rp = np.split(rng.permutation(flat), sizes)
        na.append(apoyo(X, rp, 17))
        ne.append(explicito(rp, 17))
    add(f"{k}: registros con neto x-17", oa, na, n=len(R), familia="cuota17")
    add(f"{k}: registros con 17 explicito tras la cabecera", oe, ne, n=len(R), familia="cuota17")
    print(f"  {k}: {len(R)} registros; neto x-17 {oa} (nulo {np.mean(na):.2f}, p={(np.sum(np.array(na)>=oa)+1)/(N2+1):.4g}); "
          f"17 explicito {oe} (nulo {np.mean(ne):.2f}, p={(np.sum(np.array(ne)>=oe)+1)/(N2+1):.4g})")

T = pd.DataFrame(P)
T["p_holm"] = np.nan
m = T.familia == "principal"
T.loc[m, "p_holm"] = L.holm(T.loc[m, "p"].to_numpy())
T.to_csv(L.AQUI / f"pruebas_{FUENTE}.csv", index=False, float_format="%.4g")
pd.DataFrame(FIL).to_csv(L.AQUI / f"detalle_t1_{FUENTE}.csv", index=False)
pd.set_option("display.width", 220)
print("\n== TABLA")
print(T[["prueba", "n", "obs", "nulo_media", "nulo_max", "p", "p_holm"]].to_string(index=False))
