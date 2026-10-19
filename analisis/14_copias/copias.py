"""14_copias · Tarea 1: crítica de copias, cuerda a cuerda, sobre los 25 pares de 04_concordancias.
Lee (sin modificar) 04_concordancias/resultados/alineamientos.txt y pares_significativos.csv, y datos/cuerdas.csv.
Salidas en esta carpeta: filas_alineadas.csv, pares_resumen.csv, copias_salida.txt, tests_sistematicos.csv.
`python copias.py --demo` corre la autocomprobación de la clasificación de valores.
"""
import re, sys, math
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from sklearn.metrics import normalized_mutual_info_score as nmi

RAIZ = Path(__file__).resolve().parents[2]
A4 = RAIZ / "analisis/04_concordancias/resultados"
OUT = Path(__file__).resolve().parent
SEED = 20261017
NPERM = 2000
rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ clasificación de valores
def clase_valor(a, b):
    a, b = int(a), int(b)
    if a == b:
        return "exacta"
    if abs(a - b) in (1, 10, 100, 1000):
        return "pm1_nudo"                      # |a-b| = 10^k: un nudo de más o de menos en alguna posición
    sa, sb = str(a), str(b)
    if sa.replace("0", "") == sb.replace("0", ""):
        return "misma_cifra_otra_posicion"     # p. ej. 187 vs 1087: cero insertado
    n = max(len(sa), len(sb))
    da, db = sa.zfill(n), sb.zfill(n)
    dif = [i for i in range(n) if da[i] != db[i]]
    if len(dif) == 2 and sorted(da) == sorted(db):
        return "transposicion"
    if len(dif) == 1:
        return "un_digito_otro"               # una sola cifra distinta, salto >= 2
    return "varias_cifras"


def _demo():
    assert clase_valor(40, 40) == "exacta"
    assert clase_valor(65, 55) == "pm1_nudo"
    assert clase_valor(99, 100) == "pm1_nudo"
    assert clase_valor(187, 1087) == "misma_cifra_otra_posicion"
    assert clase_valor(54, 45) == "transposicion"
    assert clase_valor(30, 32) == "un_digito_otro"
    assert clase_valor(120, 345) == "varias_cifras"
    print("demo ok")


if "--demo" in sys.argv:
    _demo()
    sys.exit()

# ------------------------------------------------------------------ datos
C = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv")
Q = pd.read_csv(RAIZ / "analisis/datos/quipus.csv").set_index("kfg")
IDX = {(r.kfg, r.cuerda): r for r in C.itertuples()}
NSUB = C[C.nivel == 1].groupby(["kfg", "padre"]).size().to_dict()
RX = re.compile(r"(\d+)([A-Za-z]+)\(([\d.]+),([SZU])\)")


def clusters(nud):
    return [(int(n), t, float(p), d) for n, t, p, d in RX.findall(nud)] if isinstance(nud, str) else []


def dir_tipo(nud, tipo):
    ds = [d for n, t, p, d in clusters(nud) if t == tipo and d != "U"]
    return max(set(ds), key=ds.count) if ds else None


def color_tokens(c):
    if not isinstance(c, str):
        return frozenset()
    return frozenset(t for t in re.split(r"[^A-Za-z]+", re.sub(r"\([^)]*\)", "", c)) if t)


def color_etiqueta(c):
    return re.sub(r"\([^)]*\)", "", c) if isinstance(c, str) else None


def parse_alineamientos():
    pares, cur = {}, None
    for ln in (A4 / "alineamientos.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"=== (\S+) vs (\S+)\s+score=([\d.]+) bits\s+sentido=(\w+)", ln)
        if m:
            cur = (m[1], m[2])
            pares[cur] = {"sentido": m[4], "filas": []}
            continue
        if cur is None or " | " not in ln:
            continue
        izq, der = ln.split(" | ", 1)
        na = izq.split()[0] if izq.strip() != "-" and izq.split() and izq.split()[0] != "-" else None
        nb = der.split()[0] if der.split() and der.split()[0] != "-" else None
        pares[cur]["filas"].append((na, nb))
    return pares


def fila(k, name):
    return IDX[(k, name)] if name else None


# ------------------------------------------------------------------ categorías de pareja
FAMILIA = {("HP055", "UR1084"): "HP055~UR1084", ("UR1175", "UR233"): "UR1175~UR233/232", ("UR1175", "UR232"): "UR1175~UR233/232",
           ("KH0049", "UR122"): "KH0049~UR122", ("UR053B", "UR053C"): "UR053B~C", ("UR006", "UR009"): "UR006/009/021",
           ("UR009", "UR021"): "UR006/009/021", ("UR006", "UR021"): "UR006/009/021", ("UR064", "UR068"): "UR064~UR068",
           ("KH0033", "UR044"): "KH0033=UR044", ("UR1107", "UR237"): "UR1107=UR237", ("AS128", "QU013"): "AS128~QU013",
           ("MM015", "UR212"): "Basilea~UR212", ("MM016", "UR212"): "Basilea~UR212", ("MM008", "UR212"): "Basilea~UR212",
           ("MM016", "UR1131"): "Basilea~UR212", ("UR1114", "UR1123"): "UR1114~UR1123", ("UR066", "UR067"): "UR066~UR067",
           ("AS125", "UR247"): "AS125=UR247", ("UR113", "UR271"): "UR113~UR271", ("UR1118", "UR218"): "UR1118~UR218",
           ("QU002", "UR137"): "QU002~UR137", ("AS159", "AS173"): "AS159~AS173", ("UR255", "UR267A"): "UR255~UR267A",
           ("MM019", "UR131C"): "MM019~UR131C"}
TIPO = {k: "mismo_objeto" for k in [("KH0033", "UR044"), ("UR1107", "UR237"), ("AS125", "UR247")]}
TIPO.update({k: "debil" for k in [("AS128", "QU013"), ("UR113", "UR271"), ("MM019", "UR131C")]})
pref = lambda k: re.match(r"[A-Z]+", k)[0]


def registrador(k):
    """Serie de registro. UR1xxx son registros de Ascher (AS) volcados en la serie UR (04: UR1084=AS084, UR1175=AS175, UR1107=AS107)."""
    p, n = pref(k), int(re.search(r"\d+", k)[0])
    return "AS" if p == "AS" or (p == "UR" and n >= 1000) else p


def dominante(vals, umbral=.8):
    v = [x for x in vals if isinstance(x, str) and x not in ("U", "Unknown", "?")]
    if len(v) < 4:
        return None
    c = pd.Series(v).value_counts(normalize=True)
    return c.index[0] if c.iloc[0] >= umbral else "mixto"


def perm_p(obs, nul, mayor=True):
    nul = np.asarray(nul)
    return (1 + (nul >= obs - 1e-12).sum()) / (1 + len(nul)) if mayor else (1 + (nul <= obs + 1e-12).sum()) / (1 + len(nul))


def acuerdo_cat(x, y, r):
    """fracción de coincidencia y nulo por barajado de y (los valores None no cuentan)."""
    ok = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(ok) < 4:
        return None
    a = np.array([o[0] for o in ok], object); b = np.array([o[1] for o in ok], object)
    obs = np.mean(a == b)
    nul = [np.mean(a == r.permutation(b)) for _ in range(NPERM)]
    return len(ok), obs, float(np.mean(nul)), perm_p(obs, nul)


def main():
    pares = parse_alineamientos()
    sig = pd.read_csv(A4 / "pares_significativos.csv").set_index(["A", "B"])
    filas, resumen, sistem = [], [], []
    for (A, B), info in pares.items():
        r = np.random.default_rng([SEED, len(filas)])
        rows = []
        for na, nb in info["filas"]:
            ra, rb = fila(A, na), fila(B, nb)
            d = {"A": A, "B": B, "cuerda_A": na, "cuerda_B": nb}
            if ra is not None and rb is not None:
                d["clase"] = clase_valor(ra.valor, rb.valor)
            else:
                x = ra if ra is not None else rb
                d["clase"] = "solo_A" if ra is not None else "solo_B"
                d["nivel_solitaria"] = int(x.nivel)
            for lado, x in (("A", ra), ("B", rb)):
                if x is not None:
                    d.update({f"valor_{lado}": int(x.valor), f"color_{lado}": x.color, f"largo_{lado}": x.largo, f"term_{lado}": x.terminacion,
                              f"nivel_{lado}": int(x.nivel), f"torsion_{lado}": x.torsion, f"union_{lado}": x.union, f"nudos_{lado}": x.nudos})
            rows.append(d)
        F = pd.DataFrame(rows)
        # vacías en el otro lado: cuerdas sin nudos en el intervalo del otro quipu entre vecinas alineadas
        ordA = {(A, rr.cuerda): rr.orden for rr in C[C.kfg == A].itertuples()}
        ordB = {(B, rr.cuerda): rr.orden for rr in C[C.kfg == B].itertuples()}
        vacias = []
        for i, d in F.iterrows():
            if d.clase not in ("solo_A", "solo_B"):
                vacias.append(np.nan); continue
            lado_otro, o_otro, k_otro = ("B", ordB, B) if d.clase == "solo_A" else ("A", ordA, A)
            col_otro = "cuerda_" + lado_otro
            prev = F.iloc[:i][F.iloc[:i].clase.isin(["exacta", "pm1_nudo", "un_digito_otro", "varias_cifras", "transposicion", "misma_cifra_otra_posicion"])]
            nxt = F.iloc[i + 1:][F.iloc[i + 1:].clase.isin(["exacta", "pm1_nudo", "un_digito_otro", "varias_cifras", "transposicion", "misma_cifra_otra_posicion"])]
            if len(prev) == 0 or len(nxt) == 0:
                vacias.append(np.nan); continue
            lo, hi = sorted([o_otro[(k_otro, prev.iloc[-1][col_otro])], o_otro[(k_otro, nxt.iloc[0][col_otro])]])
            z = C[(C.kfg == k_otro) & (C.orden > lo) & (C.orden < hi) & (C.valor == 0) & C.nudos.isna()]
            vacias.append(len(z))
        F["vacias_otro_lado"] = vacias
        F["gap_en_borde"] = F.apply(lambda d: d.clase in ("solo_A", "solo_B") and (pd.isna(d.vacias_otro_lado)), axis=1)
        F["sentido"] = info["sentido"]
        filas.append(F)

        ambos = F[F.valor_A.notna() & F.valor_B.notna()]
        n = len(ambos)
        cl = ambos.clase.value_counts()
        o = {"A": A, "B": B, "tipo": TIPO.get((A, B), "copia"), "familia": FAMILIA[(A, B)], "mismo_prefijo": pref(A) == pref(B), "mismo_registrador": registrador(A) == registrador(B), "registradores": f"{registrador(A)}/{registrador(B)}",
             "prefijos": f"{pref(A)}/{pref(B)}", "n_alineadas": n, "solo_A": int((F.clase == "solo_A").sum()), "solo_B": int((F.clase == "solo_B").sum()),
             "q_04": sig.loc[(A, B), "q"]}
        for c_ in ["exacta", "pm1_nudo", "misma_cifra_otra_posicion", "transposicion", "un_digito_otro", "varias_cifras"]:
            o["n_" + c_] = int(cl.get(c_, 0))
        o["pct_exacta"] = o["n_exacta"] / n
        o["n_discordantes"] = n - o["n_exacta"]
        # sub-colgantes
        sol = F[F.clase.isin(["solo_A", "solo_B"])]
        o["gaps_subsidiarias"] = int((sol.nivel_solitaria >= 1).sum()) if len(sol) else 0
        o["gaps_colgantes"] = int((sol.nivel_solitaria == 0).sum()) if len(sol) else 0
        o["gaps_con_vacia_en_otro"] = int((sol.vacias_otro_lado > 0).sum()) if len(sol) else 0
        o["gaps_en_borde"] = int(sol.gap_en_borde.sum()) if len(sol) else 0

        # ---- forma: color, dirección, torsión, unión, largo, subsidiarias
        ca = [color_etiqueta(x) if isinstance(x, str) else None for x in ambos.color_A]
        cb = [color_etiqueta(x) if isinstance(x, str) else None for x in ambos.color_B]
        res = acuerdo_cat(ca, cb, r)
        o["color_n"], o["color_exacto"], o["color_exacto_nulo"], o["color_exacto_p"] = res if res else (np.nan,) * 4
        ta = [color_tokens(x) for x in ambos.color_A]; tb = [color_tokens(x) for x in ambos.color_B]
        ok = [i for i in range(n) if ta[i] and tb[i]]
        if len(ok) >= 4:
            obs = np.mean([bool(ta[i] & tb[i]) for i in ok])
            nul = []
            for _ in range(NPERM):
                pi = r.permutation(ok)
                nul.append(np.mean([bool(ta[i] & tb[j]) for i, j in zip(ok, pi)]))
            o["color_compartido"], o["color_compartido_nulo"], o["color_compartido_p"] = obs, float(np.mean(nul)), perm_p(obs, nul)
            la = [ca[i] for i in ok]; lb = [cb[i] for i in ok]
            obs = nmi(la, lb)
            nul = [nmi(la, list(r.permutation(lb))) for _ in range(500)]
            o["color_nmi"], o["color_nmi_nulo"], o["color_nmi_p"] = obs, float(np.mean(nul)), perm_p(obs, nul)
        for tipo in ("S", "L"):
            da = [dir_tipo(x, tipo) for x in ambos.nudos_A]; db = [dir_tipo(x, tipo) for x in ambos.nudos_B]
            res = acuerdo_cat(da, db, r)
            o[f"dir{tipo}_n"], o[f"dir{tipo}_acuerdo"], o[f"dir{tipo}_nulo"], o[f"dir{tipo}_p"] = res if res else (np.nan,) * 4
        for campo in ("torsion", "union"):
            va = [x if isinstance(x, str) and x not in ("U", "Unknown", "?") else None for x in ambos[f"{campo}_A"]]
            vb = [x if isinstance(x, str) and x not in ("U", "Unknown", "?") else None for x in ambos[f"{campo}_B"]]
            res = acuerdo_cat(va, vb, r)
            o[f"{campo}_n"], o[f"{campo}_acuerdo"], o[f"{campo}_nulo"], o[f"{campo}_p"] = res if res else (np.nan,) * 4
        m = ambos[(ambos.largo_A > 0) & (ambos.largo_B > 0)]
        if len(m) >= 5:
            rho = stats.spearmanr(m.largo_A, m.largo_B)[0]
            nul = [stats.spearmanr(m.largo_A, r.permutation(m.largo_B.to_numpy()))[0] for _ in range(1000)]
            o["largo_rho"], o["largo_p"] = rho, perm_p(rho, nul)
            o["largo_cociente_med"] = float(np.median(m.largo_B / m.largo_A))
        # subsidiarias: n de subsidiarias directas de colgantes alineados
        c0 = ambos[(ambos.nivel_A == 0) & (ambos.nivel_B == 0)]
        sa = [NSUB.get((A, x), 0) for x in c0.cuerda_A]; sb = [NSUB.get((B, x), 0) for x in c0.cuerda_B]
        if len(c0) >= 4 and (sum(sa) + sum(sb)) > 0:
            obs = np.mean(np.array(sa) == np.array(sb))
            nul = [np.mean(np.array(sa) == r.permutation(sb)) for _ in range(NPERM)]
            o["subs_n"], o["subs_acuerdo"], o["subs_nulo"], o["subs_p"] = len(c0), obs, float(np.mean(nul)), perm_p(obs, nul)
            o["subs_totA"], o["subs_totB"] = sum(sa), sum(sb)

        # ---- control: el color condicionado al valor (nulo estratificado: barajar color de B dentro de filas con el mismo valor)
        ex = ambos[(ambos.clase == "exacta") & ambos.color_A.notna() & ambos.color_B.notna()]
        if len(ex) >= 6:
            la = np.array([color_etiqueta(x) for x in ex.color_A], object); lb = np.array([color_etiqueta(x) for x in ex.color_B], object)
            grp = [np.where(ex.valor_A.to_numpy() == v)[0] for v in ex.valor_A.unique()]
            grp = [g for g in grp if len(g) >= 2]
            if grp:
                def barajar_estrato(y):
                    y = y.copy()
                    for g in grp:
                        y[g] = y[r.permutation(g)]
                    return y
                obs_e, obs_n = np.mean(la == lb), nmi(la, lb)
                ne, nn = [], []
                for _ in range(1000):
                    y = barajar_estrato(lb)
                    ne.append(np.mean(la == y)); nn.append(nmi(la, y))
                o["colorE_n"], o["colorE_exacto"], o["colorE_exacto_nulo"], o["colorE_exacto_p"] = len(ex), obs_e, float(np.mean(ne)), perm_p(obs_e, ne)
                o["colorE_nmi"], o["colorE_nmi_nulo"], o["colorE_nmi_p"] = obs_n, float(np.mean(nn)), perm_p(obs_n, nn)
        # ---- por nivel (colgantes vs subsidiarias)
        c00 = ambos[(ambos.nivel_A == 0) & (ambos.nivel_B == 0)]
        css = ambos[(ambos.nivel_A >= 1) | (ambos.nivel_B >= 1)]
        o["col_n"], o["col_exacta"] = len(c00), int((c00.clase == "exacta").sum())
        o["sub_n"], o["sub_exacta"] = len(css), int((css.clase == "exacta").sum())
        # ---- formato de quipu entero: dominantes de dirección y de unión en el tramo alineado
        for tipo in ("S", "L"):
            o[f"dom_dir{tipo}_A"] = dominante([dir_tipo(x, tipo) for x in ambos.nudos_A]); o[f"dom_dir{tipo}_B"] = dominante([dir_tipo(x, tipo) for x in ambos.nudos_B])
        o["dom_union_A"] = dominante(ambos.union_A); o["dom_union_B"] = dominante(ambos.union_B)

        # ---- ¿ruido o edición? discordantes
        dis = ambos[ambos.clase != "exacta"].copy()
        if len(dis):
            dis["delta"] = dis.valor_B - dis.valor_A
            up = int((dis.delta > 0).sum()); dn = int((dis.delta < 0).sum())
            o["disc_B_mayor"], o["disc_A_mayor"] = up, dn
            o["disc_signo_p"] = stats.binomtest(up, up + dn, .5).pvalue if up + dn else np.nan
            pm = dis[dis.clase == "pm1_nudo"]
            o["pm1_B_mayor"], o["pm1_A_mayor"] = int((pm.delta > 0).sum()), int((pm.delta < 0).sum())
            # repetición de la misma sustitución (a->b): máximo de multiplicidad frente a nulo
            pr = list(zip(dis.valor_A, dis.valor_B))
            mult = max(pd.Series(pr).value_counts()) if pr else 0
            nul = []
            for _ in range(NPERM):
                pb = r.permutation(dis.valor_B.to_numpy())
                nul.append(max(pd.Series(list(zip(dis.valor_A, pb))).value_counts()))
            o["sust_rep_max"], o["sust_rep_nulo"], o["sust_rep_p"] = mult, float(np.mean(nul)), perm_p(mult, nul)
            o["sust_rep_top"] = str(pd.Series(pr).value_counts().index[0])
            # daño físico: la cuerda de menor valor ¿está rota (terminacion B) más que las cuerdas alineadas en general?
            bajo_term = [d.term_A if d.delta > 0 else d.term_B for d in dis.itertuples()]
            todos_term = list(ambos.term_A) + list(ambos.term_B)
            o["disc_bajo_rota"] = int(sum(t == "B" for t in bajo_term)); o["disc_n"] = len(dis)
            o["base_rota"] = float(np.mean([t == "B" for t in todos_term]))
            o["disc_bajo_rota_p"] = stats.binomtest(o["disc_bajo_rota"], len(dis), max(o["base_rota"], 1e-3), alternative="greater").pvalue
        resumen.append(o)

        # ---- omisiones concentradas por valor (cuerdas sin pareja)
        for lado in ("A", "B"):
            sol_l = F[F.clase == "solo_" + lado]
            if len(sol_l) >= 4:
                span = F[F["valor_" + lado].notna()]
                vals = span["valor_" + lado].astype(int)
                N, M = len(vals), len(sol_l)
                pv = {}
                for v, k in sol_l["valor_" + lado].astype(int).value_counts().items():
                    tot = int((vals == v).sum())
                    if tot >= 3:
                        pv[v] = (k, tot, stats.hypergeom.sf(k - 1, N, tot, M))
                if pv:
                    best = min(pv.items(), key=lambda kv: kv[1][2])
                    holm = min(1, best[1][2] * len(pv))
                    sistem.append({"A": A, "B": B, "lado": lado, "n_solitarias": M, "de_span": N, "valor_mas_concentrado": best[0],
                                   "solitarias_de_ese_valor": best[1][0], "total_ese_valor_en_span": best[1][1], "p_hiper": best[1][2], "p_holm_valores": holm})
    Fa = pd.concat(filas, ignore_index=True)
    Fa.to_csv(OUT / "filas_alineadas.csv", index=False)
    R = pd.DataFrame(resumen)
    R.to_csv(OUT / "pares_resumen.csv", index=False)
    S = pd.DataFrame(sistem)
    S.to_csv(OUT / "tests_sistematicos.csv", index=False)
    return R, Fa, S


if __name__ == "__main__":
    R, Fa, S = main()
    pd.set_option("display.width", 250, "display.max_columns", 60)
    print(R[["A", "B", "tipo", "prefijos", "n_alineadas", "solo_A", "solo_B", "pct_exacta", "n_pm1_nudo", "n_misma_cifra_otra_posicion", "n_transposicion", "n_un_digito_otro", "n_varias_cifras"]].round(2).to_string())
    print(S.round(4).to_string())
