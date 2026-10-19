"""Tarea 1c. Componentes A/B: ¿las cabeceras de UR266/UR275/UR269 son la suma de dos partes registradas aparte?

Prueba 1 (componente A + componente B, registro a registro): registro = grupo que no es separador rosa (PK);
se suman las cabeceras del registro i de A y de B. Combinaciones: UR267A/UR255 (c=15) con UR267B/UR256 (c=10);
UR273A/UR274A (c=30) con UR273B/UR274B (c=17). Estadístico: nº de registros cuya suma aparece entre las cuerdas
anudadas de UR266 ∪ UR275 ∪ UR269 (principal; también cada uno por separado, descriptivo) y de los demás
quipus del archivo salvo la propia familia de componentes y copias (control), exacto y ±1 dígito.
Nulo: barajar las cabeceras de B entre registros completos (conserva ambos marginales, rompe solo el emparejamiento).
Prueba 2 (UR270): por grupo, P = suma de colgantes (blancos), S = suma de las primeras subsidiarias (s1) de cada
colgante (variante: todas las subsidiarias de nivel 1). P se busca en UR273B ∪ UR274B, S en UR273A ∪ UR274A y P+S en
UR266 ∪ UR275 ∪ UR269.
Nulos: P y S, permutar valores entre posiciones del mismo nivel dentro de UR270 (conserva tamaños de grupo);
P+S, barajar S entre grupos (rompe solo el emparejamiento P-S).
Control negativo: las mismas pruebas buscando en quipus del archivo que no son resúmenes (todos los demás).
10 000 réplicas, semilla fija. Holm sobre las pruebas principales.
Salidas: componentes_pruebas.csv, componentes_filas.csv
"""
import numpy as np
import pandas as pd
import comun13 as C

SEED = 13004
NPERM = 10000
TOLS = [0, 1, 10, 100, 1000, 10000]
RES = ["UR266", "UR275", "UR269"]
c, q = C.archivo()
c = c.sort_values(["kfg", "orden"])
pres = c[c.pres]


def conjunto(ks):
    return np.unique(pres[pres.kfg.isin(ks)].valor.to_numpy())


def hallados(v, S, tol):
    v = np.asarray(v)
    if tol:
        return np.isin(np.abs(v[:, None] - S[None, :]), TOLS).any(1)
    return np.isin(v, S)


def cab(k):
    s = pres[(pres.kfg == k) & (pres.nivel == 0)]
    return s.groupby("grupo").valor.first()


rng = np.random.default_rng(SEED)
filas, pruebas = [], []
OTROS = [k for k in C.ARCHIVO if k not in RES + ["UR273A", "UR273B", "UR274A", "UR274B", "UR270"]]

def registros_cab(k):
    """Cabecera (primer colgante anudado; NaN si no hay) de cada registro = grupo que no es separador rosa (PK)."""
    s = c[c.kfg == k]
    out = []
    for g, x in s.groupby("grupo"):
        x0 = x[x.nivel == 0]
        if (x0.color.str.startswith("PK")).all() and not x0.pres.any():
            continue
        p0 = x0[x0.pres]
        out.append((g, p0.valor.iloc[0] if len(p0) else np.nan))
    return pd.DataFrame(out, columns=["grupo", "x"])


PAREJAS_AB = [("UR267A", "UR267B"), ("UR255", "UR256"), ("UR267A", "UR256"), ("UR255", "UR267B"),
              ("UR273A", "UR273B"), ("UR274A", "UR274B"), ("UR273A", "UR274B"), ("UR274A", "UR273B")]
for qa, qb in PAREJAS_AB:
    A, B = registros_cab(qa), registros_cab(qb)
    n = min(len(A), len(B))
    ok = (A.x[:n].notna() & B.x[:n].notna()).to_numpy()
    a, b = A.x[:n].to_numpy()[ok].astype(int), B.x[:n].to_numpy()[ok].astype(int)
    familia = {"UR267A", "UR267B", "UR255", "UR256"} if "267" in qa + qb or "255" in qa + qb else         {"UR273A", "UR273B", "UR274A", "UR274B", "UR270"}
    control = [k for k in C.ARCHIVO if k not in set(RES) | familia]
    for destino in ["UR266+UR275+UR269"] + RES + ["control"]:
        S = conjunto(control) if destino == "control" else conjunto(destino.split("+"))
        for tol in (False, True):
            obs = hallados(a + b, S, tol).sum()
            nul = np.array([hallados(a + rng.permutation(b), S, tol).sum() for _ in range(NPERM)])
            pruebas.append(dict(prueba=f"{qa}+{qb} registro a registro", destino=destino, tolerancia=tol, n=len(a),
                                obs=int(obs), nulo_media=nul.mean(), nulo_max=int(nul.max()),
                                p=(np.sum(nul >= obs) + 1) / (NPERM + 1)))
    for i in np.flatnonzero(ok):
        x, y = int(A.x[i]), int(B.x[i])
        dest = pres[pres.kfg.isin(RES) & pres.valor.sub(x + y).abs().isin(TOLS)]
        filas.append(dict(fuente=f"{qa}+{qb}", grupo=f"{A.grupo[i]}/{B.grupo[i]}", registro=i, parte_A=x, parte_B=y,
                          suma=x + y, en_resumen=" ".join(f"{r.kfg}:g{r.grupo}:{r.valor}{'' if r.valor == x + y else '~'}"
                                                         for r in dest.itertuples())))

# Prueba 1b (dirigida): registros de UR269 cuya cuota (cuerda explícita o x - neto) es 25 = 15 + 10, o 47 = 30 + 17.
# ¿Su cabecera es la suma de un registro de UR267A + UR267B (25) o de UR273A + UR273B (47)? Nulo: barajar B.
u = c[(c.kfg == "UR269") & c.pres]
rec269 = []
for g, x in u.groupby("grupo"):
    p0 = x[x.nivel == 0]
    if len(p0) and p0.valor.iloc[0] >= 100:
        xv = int(p0.valor.iloc[0]); otros_v = x.valor.iloc[1:].to_numpy()
        for cc in (25, 47):
            if (otros_v == cc).any() or (otros_v == xv - cc).any():
                rec269.append((g, xv, cc))
for (qa, qb, cc) in [("UR267A", "UR267B", 25), ("UR273A", "UR273B", 47)]:
    objetivo = np.array([xv for g, xv, k in rec269 if k == cc])
    A, B = registros_cab(qa), registros_cab(qb)
    n = min(len(A), len(B))
    ok = (A.x[:n].notna() & B.x[:n].notna()).to_numpy()
    a, b = A.x[:n].to_numpy()[ok].astype(int), B.x[:n].to_numpy()[ok].astype(int)
    for tol in (False, True):
        f = (lambda sums: hallados(objetivo, np.unique(sums), tol).sum())
        obs = f(a + b)
        nul = np.array([f(a + rng.permutation(b)) for _ in range(NPERM)])
        pruebas.append(dict(prueba=f"UR269 registros con cuota {cc}: cabecera = {qa}+{qb}", destino="UR269",
                            tolerancia=tol, n=len(objetivo), obs=int(obs), nulo_media=nul.mean(), nulo_max=int(nul.max()),
                            p=(np.sum(nul >= obs) + 1) / (NPERM + 1)))
print("UR269, registros con cuota 25:", [(g, x) for g, x, k in rec269 if k == 25])
print("UR269, registros con cuota 47:", [(g, x) for g, x, k in rec269 if k == 47])

# UR270
s = c[c.kfg == "UR270"].copy()
s["v"] = s.valor.where(s.pres, 0)
s["pend"] = s.cuerda.str.extract(r"^(p\d+)")[0]
s["subsec"] = s.cuerda.str.extract(r"^p\d+(s\d+)")[0]
cprinc = s.color.str.split(r"[(\s]", regex=True).str[0]


def comp(v, solo_s1=True):
    t = s.assign(v=v)
    P = t[t.nivel == 0].groupby("grupo").v.sum()
    m = (t.nivel == 1)
    if solo_s1:
        m &= (t.subsec == "s1")  # solo la primera subsidiaria de cada colgante
    Sg = t[m].groupby("grupo").v.sum().reindex(P.index, fill_value=0)
    ok = (P > 0) & (Sg > 0)
    return P[ok].to_numpy(), Sg[ok].to_numpy(), P[ok].index.to_numpy()


v0 = s.v.to_numpy()
niv = s.nivel.to_numpy()
for solo in (True, False):
    P, Sg, gg = comp(v0, solo)
    etiqueta = "S = s1" if solo else "S = todas las subsid. nivel 1"
    for nombre, val, destino_ks in [("P en UR273B+UR274B", P, ["UR273B", "UR274B"]),
                                    ("S en UR273A+UR274A", Sg, ["UR273A", "UR274A"]),
                                    ("P+S en UR266+UR275+UR269", P + Sg, RES)]:
        for destino, Sset in [("+".join(destino_ks), conjunto(destino_ks)), ("otros 42 quipus", conjunto(OTROS))]:
            for tol in (False, True):
                obs = hallados(val, Sset, tol).sum()
                nul = []
                for _ in range(NPERM if nombre.startswith("P+S") else 2000):
                    if nombre.startswith("P+S"):
                        nul.append(hallados(P + rng.permutation(Sg), Sset, tol).sum())
                    else:
                        vp = v0.copy()
                        for lv in (0, 1):
                            mm = niv == lv
                            vp[mm] = rng.permutation(vp[mm])
                        Pp, Sp, _ = comp(vp, solo)
                        nul.append(hallados(Pp if nombre.startswith("P ") else Sp, Sset, tol).sum())
                nul = np.array(nul)
                pruebas.append(dict(prueba=f"UR270 {nombre} ({etiqueta})", destino=destino, tolerancia=tol, n=len(val),
                                    obs=int(obs), nulo_media=nul.mean(), nulo_max=int(nul.max()),
                                    p=(np.sum(nul >= obs) + 1) / (len(nul) + 1)))
    # prueba conjunta: misma fila i de UR273A/B con B_i = P_g (exacto) y A_i = S_g (±1 dígito)
    A3, B3 = cab("UR273A"), cab("UR273B")
    filas3 = [(A3[g], B3[g]) for g in sorted(set(A3.index) & set(B3.index))]

    def conjunta(P_, S_):
        return sum(any(b == p and abs(a - s_) in TOLS for a, b in filas3) for p, s_ in zip(P_, S_))
    obs = conjunta(P, Sg)
    nul = np.array([conjunta(P, rng.permutation(Sg)) for _ in range(NPERM)])
    pruebas.append(dict(prueba=f"UR270 (P,S) = fila (B,A) de UR273 ({etiqueta})", destino="UR273A/B", tolerancia=True,
                        n=len(P), obs=int(obs), nulo_media=nul.mean(), nulo_max=int(nul.max()),
                        p=(np.sum(nul >= obs) + 1) / (NPERM + 1)))
    if solo:
        for gi, x, y in zip(gg, P, Sg):
            def donde(v, ks):
                return " ".join(f"{r.kfg}:g{r.grupo}:{r.valor}" for r in
                                pres[pres.kfg.isin(ks) & pres.valor.sub(v).abs().isin(TOLS)].itertuples())
            filas.append(dict(fuente="UR270", grupo=gi, parte_A=y, parte_B=x, suma=x + y,
                              en_resumen=donde(x + y, RES), parte_B_en=donde(x, ["UR273B", "UR274B"]),
                              parte_A_en=donde(y, ["UR273A", "UR274A"])))

T = pd.DataFrame(pruebas)
principal = (~T.destino.isin(["otros 42 quipus", "control", "UR266", "UR275", "UR269"]) | T.prueba.str.startswith("UR269 registros")) & ((~T.tolerancia) | T.prueba.str.contains(r"fila \(B,A\)"))
T["p_holm_principal"] = np.nan
from scipy.stats import false_discovery_control  # noqa: E402,F401
pp = T.loc[principal, "p"].to_numpy()
o = np.argsort(pp)
holm = np.minimum(1, np.maximum.accumulate((len(pp) - np.arange(len(pp))) * pp[o]))
T.loc[T.index[principal][o], "p_holm_principal"] = holm
T.to_csv(C.AQUI / "componentes_pruebas.csv", index=False, float_format="%.4g")
F = pd.DataFrame(filas)
F.to_csv(C.AQUI / "componentes_filas.csv", index=False)
pd.set_option("display.width", 250)
T["prueba"] = T.prueba.str.slice(0, 70)
print(T.drop(columns=["n"]).to_string(index=False))
print()
for col in ["en_resumen", "parte_B_en", "parte_A_en"]:
    if col in F:
        F[col] = F[col].fillna("").astype(str).str.slice(0, 70)
print(F.fillna("").to_string(index=False))
