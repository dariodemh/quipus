# -*- coding: utf-8 -*-
"""Paso 1. Matriz quipu x rasgo con todos los detectores ya validados del proyecto.

Reutiliza los CSV de cada detector (fuente en la columna `fuentes` de rasgos.md)
y recalcula desde KFG/OKR solo lo que no existe por quipu: fraccion no decimal,
torsion Z, cuerdas rotas, fibra, canutos, marcadoras, particiones de color.
Salida: matriz.csv (una fila por quipu de quipus.csv).
"""
import re, sqlite3
import numpy as np, pandas as pd

A = r"./analisis"
OUT = A + r"\28_atlas_generos"
R = lambda p: pd.read_csv(f"{A}\\{p}")

Q = R(r"datos\quipus.csv")
C = R(r"datos\cuerdas.csv")
M = Q[["kfg", "okr", "procedencia", "museo", "region"]].copy().set_index("kfg")

# ---------- calidad de datos y rasgos recalculados desde KFG ----------
def col_norm(s):
    return re.sub(r"\([^)]*\)", "", s) if isinstance(s, str) else ""

def no_decimal(nudos):
    """True si la cuerda viola la gramatica decimal (lugar repetido o cifra >9 en un lugar)."""
    if not isinstance(nudos, str) or not nudos.strip():
        return None
    lugares = []
    for tok in nudos.split(";"):
        m = re.search(r",\s*(-?\d+)\s*$", tok)
        if not m:
            continue
        v = int(m.group(1))
        if v <= 0:
            continue
        k = int(np.floor(np.log10(v)))
        if v % 10 ** k:            # p. ej. 12 (12L): no es d*10^k
            return True
        lugares.append(k)
    if not lugares:
        return None
    return len(lugares) != len(set(lugares))

C["anudada"] = C.nudos.notna() & (C.nudos.astype(str).str.strip() != "")
C["nodec"] = C.nudos.map(no_decimal)
C["colorn"] = C.color.map(col_norm)
g = C.groupby("kfg")
F = pd.DataFrame({
    "n_cuerdas": g.size(),
    "n_colg": g.apply(lambda d: (d.nivel == 0).sum()),
    "n_grupos": g.grupo.nunique(),
    "frac_anudada": g.anudada.mean(),
    "frac_rota": g.apply(lambda d: (d.terminacion == "B").mean()),
    "frac_nodec": g.apply(lambda d: d.nodec.dropna().astype(float).mean() if d.nodec.notna().any() else np.nan),
    "frac_Z": g.apply(lambda d: (d.torsion == "Z").sum() / max(1, d.torsion.isin(["S", "Z"]).sum())
                      if d.torsion.isin(["S", "Z"]).any() else np.nan),
    "n_colores": g.colorn.nunique(),
    "log_val_med": g.apply(lambda d: np.log10(1 + d.valor[d.valor > 0].median()) if (d.valor > 0).any() else 0),
})

# particion color ~ grupo (invariante al vocabulario del transcriptor): NMI de los colgantes
from sklearn.metrics import normalized_mutual_info_score as nmi
def nmi_grupo(d):
    d = d[d.nivel == 0]
    if len(d) < 8 or d.grupo.nunique() < 2 or d.colorn.nunique() < 2:
        return np.nan
    return nmi(d.colorn, d.grupo)
F["nmi_color_grupo"] = g[["nivel", "grupo", "colorn"]].apply(nmi_grupo)
M = M.join(F)

# ---------- OKR (solo lectura): fibra, canutos, marcadoras, cuerdas superiores, estado ----------
con = sqlite3.connect(r"file:data\external\open-khipu-repository\data\khipu.db?mode=ro", uri=True)
km = pd.read_sql("select KHIPU_ID, OKR_NUM, CONDITIONOFKHIPU from khipu_main", con)
cd = pd.read_sql("select KHIPU_ID, FIBER, CORD_CLASSIFICATION, CANUTO_ID from cord", con)
cd["fib"] = cd.FIBER.fillna("").str.strip()
cg = cd.groupby("KHIPU_ID")
O = pd.DataFrame({
    "okr_frac_camelido": cg[["fib"]].apply(lambda d: d.fib.isin(["CL", "A", "L", "CC", "AH"]).sum() / max(1, (d.fib != "").sum())
                                 if (d.fib != "").any() else np.nan),
    "okr_frac_lana": cg[["fib"]].apply(lambda d: (d.fib == "W").sum() / max(1, (d.fib != "").sum()) if (d.fib != "").any() else np.nan),
    "okr_marcadoras": cg.CORD_CLASSIFICATION.apply(lambda s: (s == "M").sum()),
    "okr_superiores": cg.CORD_CLASSIFICATION.apply(lambda s: (s == "T").sum()),
}).reset_index()
O = O.merge(km, on="KHIPU_ID").rename(columns={"OKR_NUM": "okr"})
M = M.reset_index().merge(O.drop(columns=["KHIPU_ID", "CONDITIONOFKHIPU"]).drop_duplicates("okr"),
                          on="okr", how="left").set_index("kfg")

# Canutos: no se usan. En OKR casi toda cuerda tiene canuto (segmento de color), asi que no discrimina.
# transcriptor (22_formularios) y discrepancia KFG-OKR (t_okr_vs_kfg)
M = M.join(R(r"22_formularios\transcriptor_quipus.csv").set_index("kfg")[["inv"]].rename(columns={"inv": "transcriptor"}))
M = M.join(R(r"ds\t_okr_vs_kfg\salidas\por_quipu_final.csv").set_index("kfg")[["tasa_valor"]]
           .rename(columns={"tasa_valor": "disc_okr"}))

# ---------- detectores existentes ----------
# 08 auditoria de sumas: estadisticos locales, q<.05 en M1 y M2 (replica la lista de 14)
r = R(r"08_auditoria_sumas\refinado.csv").set_index("kfg")
loc = ["PPS_ady", "PPS_ady100", "PPS_cara01", "PPS_sumlog_local"]
q1 = r[[f"qr_M1_nivel_{s}" for s in loc]].min(axis=1)
q2 = r[[f"qr_M2_magnitud_{s}" for s in loc]].min(axis=1)
M["sumas_q"] = np.maximum(q1, q2)          # robusto a ambos nulos
M["sumas_q_M1"] = q1
# 01: cuerdas superiores que suman (TA) y cierre R7 (lista del 08 sec. 6)
M["sumas_01"] = M.index.isin(["AS001", "AS007", "QU009", "QU015", "QU016", "UR1152"])
# 14: fila + total suelto
ft = R(r"14_copias\fila_total_por_quipu.csv").set_index("kfg")
M["filatotal_q"] = ft.q_tol0

# relaciones entre quipus (13, 09, 04, n_puruchuco_pacha) y copias (14)
INCA = ["UR255", "UR256", "UR266", "UR267A", "UR267B", "UR269", "UR270", "UR273A", "UR273B",
        "UR274A", "UR274B", "UR275", "UR278"]
PURU = ["UR063", "UR064", "UR066", "UR067", "UR068"]
M["rel_archivo"] = np.select([M.index.isin(INCA + PURU), M.index.isin(["UR268", "UR073", "UR078"])],
                             ["demostrada", "propuesta"], "")
pr = R(r"14_copias\pares_resumen.csv")
cop = {}
for _, x in pr.iterrows():
    for a, b in ((x.A, x.B), (x.B, x.A)):
        cop.setdefault(a, []).append(f"{x.tipo}:{b}")
M["copias"] = pd.Series({k: " ".join(v) for k, v in cop.items()})
M["trio_xcx"] = M.index.isin(["UR255", "UR256", "UR266", "UR267A", "UR267B", "UR269", "UR274B", "UR275"])

# 22 formularios
fd = R(r"22_formularios\quipus_detector.csv").set_index("kfg")
M["form_Q"] = fd.Q
M["form_holm"] = fd.holm
M["form_qbh"] = fd.q_bh
fo = R(r"22_formularios\formularios.csv")
niv = {}
rank = {"demostrado-local": 3, "apoyado-indeterminado": 2, "no confirmado": 1, "no confirmable": 0}
for _, x in fo.iterrows():
    for col in ("quipus_E", "quipus_C"):
        for k in str(x[col]).split():
            if k != "nan" and rank.get(x.nivel, 0) > rank.get(niv.get(k, ""), -1):
                niv[k] = x.nivel
M["form_archivo"] = pd.Series(niv)

# n_ficha_nazca
fn = R(r"ds\n_ficha_nazca\barrido_corpus.csv").set_index("khipu")
M["nazca_p"] = fn.p_bin_holm
# n_plantillas: padron Santa (P4r), calendario (P8ar), libro segmentado (P11a)
pt = R(r"n_plantillas\puntuaciones.csv")
for t, nm in (("P4r", "santa"), ("P8ar", "calend"), ("P11a", "segm")):
    s = pt[pt.plantilla == t].set_index("khipu")
    M[f"{nm}_q"] = s.q
    M[f"{nm}_pcorpus"] = s.p_corpus
# 10 tablas
t1 = R(r"10_tablas\t1_por_quipu.csv").set_index("kfg")
M["tabla_R"] = t1.R
M["tabla_K"] = t1.K
M["tabla_q_orden"] = t1.q_orden
M["tabla_rho"] = t1["corr"]
# 11 rosetta: redondeo (asignacion) y cuotas repetidas
fa = R(r"11_rosetta\fA_redondeo_por_quipu.csv").set_index("kfg")
M["red_n"] = fa.n
M["red_frac"] = fa.frac
M["red_q"] = fa.q
M["cuotas_rep_q"] = R(r"11_rosetta\fBCF_por_quipu.csv").set_index("kfg").q_iguales
# no numericos y nudos de >=10 vueltas
nn = R(r"ds\n_no_numericos\quipus_clase.csv").set_index("kfg")
M["nonum_clase"] = nn.clase_limpia
M["nonum_subtipo"] = nn.subtipo.where(nn.clase_limpia)
M["frac_sin_nudo"] = nn.frac_sin_nudo
M["pure_tally"] = nn.pure_tally
l10 = R(r"ds\n_nudos_imposibles\quipus_L10_clase.csv").set_index("kfg")
M["vueltas10"] = l10.vueltas_reales
M["vueltas10"] = M.vueltas10.fillna(0)
# 24 color: particion color~grupo sobre el nulo
nm_ = R(r"24_color_formato\p3_nmi_grupo.csv").set_index("kfg")
M["color_grupo_p"] = nm_.p

M.index.name = "kfg"
M.to_csv(OUT + r"\matriz.csv")

# faltantes por rasgo
falt = M.isna().mean().sort_values(ascending=False)
print("quipus:", len(M))
print("fraccion faltante por rasgo:\n" + falt.round(3).to_string())
print("transcriptor:", M.transcriptor.value_counts(dropna=False).to_dict())
print("con cuerdas en KFG:", M.n_cuerdas.notna().sum())
print("frac_rota>0.5:", int((M.frac_rota > .5).sum()), " n_cuerdas<10:", int((M.n_cuerdas < 10).sum()))
