"""Multiplicidad, exploracion/confirmacion, niveles y salida (diseno.md). Uso: python 03_decision.py [--nulo R]"""
import sys, glob
import numpy as np, pandas as pd
from scipy.stats import binomtest
from comun import *

FAMILIAS = ["T1_periodo_valor", "T2_periodo_color", "T3_repeticion", "T4_tendencia", "T5_subsidiaria",
            "T6_suma_salteada", "T7_pares_suma", "I1_copia", "I2_invertida", "I3_diferencia", "I4_razon",
            "I5_grupos_permutados", "I6_suma_bloque_F_en_otro", "I7_suma_bloque_otro_en_F",
            "I8_total_grupo_F_en_sitio", "I9_total_grupo_sitio_en_F"]

GENERO = {
    "T1_periodo_valor": "FOR/TAB (formulario repetido por bloques)",
    "T2_periodo_color": "FOR cromatico (clave de color ciclica)",
    "T3_repeticion": "copia interna (duplicado de tramo; archivo)",
    "T4_tendencia": "nuevo: lista ordenada por magnitud (ranking)",
    "T5_subsidiaria": "ASG/ARC (ajuste o cuota sobre la partida)",
    "T6_suma_salteada": "SUM/TAB (total de columna no contigua)",
    "T7_pares_suma": "ARC (pares complementarios x, c-x)",
    "I1_copia": "copia entre quipus (archivo)",
    "I2_invertida": "copia invertida (lectura en sentido opuesto)",
    "I3_diferencia": "nuevo: version desplazada (actualizacion por diferencia)",
    "I4_razon": "nuevo: version escalada (cambio de unidad o cuota)",
    "I5_grupos_permutados": "copia con grupos reordenados (archivo)",
    "I6_suma_bloque_F_en_otro": "ARC debil (F es detalle de otro)",
    "I7_suma_bloque_otro_en_F": "ARC debil (F resume a otro)",
    "I8_total_grupo_F_en_sitio": "ARC debil (totales de F pasan a otro quipu del sitio)",
    "I9_total_grupo_sitio_en_F": "ARC debil (F recoge totales de otro quipu del sitio)",
}


EXTRA = {  # precisiones tras los diagnosticos (04, 07); no cambian niveles
    ("UR122", "T6_suma_salteada"): "UR122 copia la seccion subtotal de KH0049 (B1 = B3+B4+B5; 07_ur122_kh0049.py): p2 = 457+951+875, p9 = 447+855+972. Las cuerdas en 0 de UR122 donde KH0049 tiene valor (p21-p23: 487, 281, 661) deben estar rotas o sueltas en el objeto; 15652 (frente a 15649) esta en ambas copias: error del original.",
    ("QU017", "I3_diferencia"): "No especifico: QU017 puntua casi igual con UR016, AS093, QU002 y UR056A; es propiedad de QU017, no vinculo. Prediccion: ningun companero concreto reproducira el tramo al releerlo.",
    ("UR016", "T5_subsidiaria"): "Las subsidiarias de UR016 escalan con su colgante (rho 0,38; subsidiaria menor en 90 %, razon mediana 0,20), sin razon fija: colgantes releidos mayores tendran subsidiarias mayores, pero no una fraccion constante.",
}


def prediccion(r):
    if (r.kfg, r.estructura) in EXTRA: return EXTRA[(r.kfg, r.estructura)]
    d = str(r.detalle); f = r.estructura
    comp = d.split("companero=")[1].split(";")[0] if "companero=" in d else (d.split("companeros=")[1].split("|")[0] if "companeros=" in d else "")
    if f == "T1_periodo_valor": return f"Releyendo {r.kfg}, los valores deben repetirse con desfase {d.split('=')[-1]} (rangos/iguales); los grupos fisicos (espaciado) deben tener ese tamano o un multiplo."
    if f == "T2_periodo_color":
        from collections import Counter
        q = quipu(r.kfg); c, v = q.col, q.v; top = [x for x, _ in Counter(c).most_common(2)]
        pares = [(v[i], v[i + 1]) if c[i] == top[0] else (v[i + 1], v[i]) for i in range(len(c) - 1) if {c[i], c[i + 1]} == set(top)]
        nz = [(a, b) for a, b in pares if a != b]; k2 = sum(b > a for a, b in nz)
        return (f"{r.kfg} es una lista de pares intercalados {top[0]}/{top[1]} (ciclo de {d.split('lag=')[1].split(';')[0]}); hoy {top[1]} > {top[0]} en {k2} de {len(nz)} pares distintos. "
                f"En foto, el ciclo de color se conserva con otro transcriptor; si es una tabla de 2 columnas intercaladas, el color que domina seguira dominando en los pares que se relean.")
    if f == "T3_repeticion": return f"Un tramo de {r.kfg} duplica otro (tolerancia de un nudo); en el objeto, ambos tramos deben tener nudos en las mismas posiciones relativas."
    if f == "T4_tendencia": return f"Dentro de cada grupo de {r.kfg} los valores estan ordenados ({d}); un quipu hermano del mismo sitio con igual formato tendra tambien grupos ordenados."
    if f == "T5_subsidiaria": return f"Las subsidiarias de {r.kfg} guardan una relacion fija con su colgante ({d.split(';')[0]}); colgantes nuevos leidos en el objeto deben cumplir la misma razon/diferencia."
    if f == "T6_suma_salteada": return f"En {r.kfg} hay cuerdas que totalizan la misma posicion de varios grupos o un paso fijo ({d.split(';')[0]}); corregir un nudo dudoso con esa suma debe dar el valor del objeto."
    if f == "T7_pares_suma": return f"En {r.kfg} pares de cuerdas ({d}) suman la misma cantidad; el par que falte o este roto debe completar esa suma."
    if f in ("I1_copia", "I2_invertida", "I5_grupos_permutados"): return f"{r.kfg} y {comp} registran la misma lista ({f.split('_',1)[1]}); medir ambos: largos de cuerda no correlacionados (objetos distintos) y discrepancias de un nudo."
    if f == "I3_diferencia": return f"{r.kfg} y {comp} difieren en una constante ({d.split(';')[-1]}) en un tramo; el resto del tramo, si se relee, mantiene la diferencia."
    if f == "I4_razon": return f"{r.kfg} y {comp} son proporcionales en un tramo ({d.split(';')[-1]}); el resto del tramo, si se relee, mantiene la razon."
    if f.startswith("I6") or f.startswith("I8"): return f"Sumas de bloques/grupos de {r.kfg} reaparecen en {comp}; nuevas lecturas de {comp} deben conservar esos valores (archivo jerarquico del sitio)."
    if f.startswith("I7") or f.startswith("I9"): return f"Totales de bloques/grupos de {comp} aparecen como cuerdas de {r.kfg}; {r.kfg} seria un resumen de nivel superior."
    return ""


def cargar(nulo):
    suf = f"_nulo{nulo}" if nulo is not None else ""
    I = pd.read_csv(AQUI / f"internas{suf}.csv")
    partes = [x for x in sorted(glob.glob(str(AQUI / f"entre{suf}_*_*.csv"))) if nulo is not None or "nulo" not in Path(x).name]
    if (AQUI / f"entre{suf}.csv").exists(): E = pd.read_csv(AQUI / f"entre{suf}.csv")
    else: E = pd.concat([pd.read_csv(x) for x in partes])
    E = E[E.kfg.isin(FRONTERA)]
    df = pd.concat([I, E], ignore_index=True).rename(columns={"prueba": "estructura"})
    assert set(df.estructura) <= set(FAMILIAS)
    assert df.groupby("kfg").size().eq(16).all(), df.groupby("kfg").size().value_counts()
    df["p_congelado"] = df.p; df["p_bloque"] = np.nan
    sens = AQUI / f"sensibilidad{suf}.csv"
    if "--sin_enmienda3" not in sys.argv and sens.exists():
        S = pd.read_csv(sens).rename(columns={"prueba": "estructura"})
        df = df.drop(columns="p_bloque").merge(S[["kfg", "estructura", "p_bloque"]], on=["kfg", "estructura"], how="left")
        df["p"] = np.fmax(df.p_congelado, df.p_bloque).where(df.p_congelado.notna())
    return df


def decidir(df):
    m = division(); df["mitad"] = df.kfg.map(m)
    ok = df.p.notna()
    df["q"] = bh(df.p.where(ok)); df["holm"] = holm(df.p.where(ok))
    A = df[df.mitad == "A"].copy(); A["qA"] = bh(A.p)
    fam = []
    for f in FAMILIAS:
        a = A[(A.estructura == f) & A.p.notna()]
        k = int((a.p < 0.05).sum()); n = len(a)
        pb = binomtest(k, n, 0.05, "greater").pvalue if n else 1.0
        prom = bool((a.qA < 0.10).any() or pb < 0.05)
        fam.append(dict(familia=f, nA=n, kA=k, binomA=pb, minqA=a.qA.min() if n else np.nan, promovida=prom))
    fam = pd.DataFrame(fam).set_index("familia")
    B = df[(df.mitad == "B") & df.estructura.isin(fam.index[fam.promovida]) & df.p.notna()].copy()
    B["qconf"] = bh(B.p)
    df["qconf"] = np.nan; df.loc[B.index, "qconf"] = B.qconf
    pbB = {}
    for f in fam.index[fam.promovida]:
        b = B[B.estructura == f]; k = int((b.p < 0.05).sum()); n = len(b)
        pbB[f] = binomtest(k, n, 0.05, "greater").pvalue if n else 1.0
        fam.loc[f, "nB"] = n; fam.loc[f, "kB"] = k; fam.loc[f, "binomB"] = pbB[f]
        fam.loc[f, "minqconf"] = b.qconf.min() if n else np.nan
    if pbB:
        hb = holm(list(pbB.values()))
        for f, h in zip(pbB, hb): fam.loc[f, "binomB_holm"] = h
    fam["replica"] = False
    for f in pbB:
        fam.loc[f, "replica"] = bool(fam.loc[f, "binomB_holm"] < 0.05 or fam.loc[f, "minqconf"] < 0.05)
    rep = df.estructura.map(fam.replica)
    niv = np.full(len(df), "ninguno", object)
    niv[(df.p < 0.01).to_numpy()] = "especulativo"
    prop = ((df.q < 0.05) & ~rep) | ((df.mitad == "B") & (df.qconf < 0.05) & (df.q >= 0.05))
    niv[prop.to_numpy()] = "propuesto"
    niv[((df.q < 0.05) & rep).to_numpy()] = "apoyado"
    niv[((df.holm < 0.05) & rep).to_numpy()] = "bien apoyado"
    df["nivel"] = niv
    return df, fam


CONOCIDOS = None
def conocido(r):
    global CONOCIDOS
    if CONOCIDOS is None:
        P = pd.read_csv(RAIZ / "analisis/04_concordancias/resultados/pares_significativos.csv")
        CONOCIDOS = {frozenset((a, b)) for a, b in zip(P.A, P.B)}
    d = str(r.detalle)
    if "companero=" not in d: return False
    c = d.split("companero=")[1].split(";")[0]
    return frozenset((r.kfg, c)) in CONOCIDOS


if __name__ == "__main__":
    nulo = int(sys.argv[sys.argv.index("--nulo") + 1]) if "--nulo" in sys.argv else None
    df, fam = decidir(cargar(nulo))
    df["conocido_04"] = df.apply(conocido, axis=1)
    sale = df[df.nivel.isin(["bien apoyado", "apoyado"])]
    nuevos = sale[~sale.conocido_04]
    print("familias:\n", fam.round(4).to_string())
    print("\nniveles:", df.nivel.value_counts().to_dict())
    print("filas que sacan de la frontera por familia:", sale.estructura.value_counts().to_dict())
    print("quipus que dejan la frontera:", sale.kfg.nunique(), "| solo por relacion nueva (no 04):", nuevos.kfg.nunique())
    print("propuestos (quipus):", df[df.nivel == "propuesto"].kfg.nunique())
    print("suma de q en filas que sacan:", round(sale.q.sum(), 3))
    if nulo is None and "--sin_enmienda3" in sys.argv:
        df.to_csv(AQUI / "frontera_estructura_sin_enmienda3.csv", index=False)
    elif nulo is None:
        df["genero_cercano"] = df.estructura.map(GENERO)
        df["prediccion"] = [prediccion(r) if r.nivel in ("bien apoyado", "apoyado", "propuesto") else "" for r in df.itertuples()]
        cols = ["kfg", "estructura", "estadistico", "p", "q", "mitad", "nivel", "prediccion", "holm", "qconf", "N", "detalle", "conocido_04", "genero_cercano", "p_congelado", "p_bloque"]
        df[cols].sort_values(["nivel", "q", "kfg"], key=lambda s: s.map({"bien apoyado": 0, "apoyado": 1, "propuesto": 2, "especulativo": 3, "ninguno": 4}) if s.name == "nivel" else s).to_csv(AQUI / "frontera_estructura.csv", index=False)
        fam.to_csv(AQUI / "familias.csv")
        print("\nfilas bien apoyado/apoyado/propuesto:")
        print(df[df.nivel.isin(["bien apoyado", "apoyado", "propuesto"])][["kfg", "estructura", "estadistico", "p", "q", "mitad", "nivel", "conocido_04", "detalle"]].sort_values("q").to_string())
    else:
        fam.to_csv(AQUI / f"familias_nulo{nulo}.csv")
