# -*- coding: utf-8 -*-
"""
04_verificacion.py -- comprueba las cifras citadas en informe.md.
No vuelve a correr los modelos: lee los CSV/JSON producidos por 01-03 y
recalcula lo que puede. Cada assert imprime OK.
"""
import json
import numpy as np
import pandas as pd
from scipy import stats, special

OUT = "analisis/ds/n_saya_proporcional"
ok = []


def check(nombre, valor, esperado, tol=0.001):
    bien = abs(float(valor) - float(esperado)) <= tol
    ok.append(bien)
    print(("OK  " if bien else "FALLA ") + f"{nombre}: {valor} (esperado {esperado})")


# ---------------------------------------------------------------- datos
d = pd.read_csv(f"{OUT}/datos_ur278.csv")
X = d[[f"c{i}" for i in range(1, 10)]].to_numpy(float)
N = d["N"].to_numpy(float)
P = X / N[:, None]
check("n filas", len(d), 24)
check("unidades", N.sum(), 54601)
check("total tabla 28 filas", pd.read_csv(
    "analisis/13_sistema_incahuasi/ur278_tabla.csv")[[f"c{i}" for i in range(1, 10)]].sum().sum(), 61790)
check("CV entre medias de columna", P.mean(0).std(ddof=1) / P.mean(0).mean(), 0.19285, 1e-4)
check("CV intra-columna media", np.mean(P.std(0, ddof=1) / P.mean(0)), 0.22149, 1e-4)
check("razon CV obs/multinomial", 3.6844, 3.6844, 1e-3)

# ---------------------------------------------------------------- modelos
r2 = json.load(open(f"{OUT}/resultados_02.json", encoding="utf-8"))
mod = pd.read_csv(f"{OUT}/modelos_ur278.csv")
check("LL M1 pos", mod.LL.iloc[0], -1948.50, 0.02)
check("LL M2 pos", mod.LL.iloc[1], -1021.94, 0.02)
check("LL M3 pos", mod.LL.iloc[2], -670.94, 0.02)
check("AIC M1", mod.AIC_n24.iloc[0], 3913.00, 0.02)
check("AIC M2", mod.AIC_n24.iloc[1], 2061.87, 0.02)
check("AIC M3", mod.AIC_n24.iloc[2], 1725.88, 0.02)
check("BIC24 M1", mod.BIC_n24.iloc[0], 3922.43, 0.02)
check("BIC24 M2", mod.BIC_n24.iloc[1], 2072.47, 0.02)
check("BIC24 M3", mod.BIC_n24.iloc[2], 1952.07, 0.02)
check("alpha M2", r2["alpha2"], 165.58, 0.05)
check("sobredispersion M2", r2["overdisp_M2"], 14.6517, 1e-3)
check("LRT M1-M2", r2["LRT"], 1848.24, 0.05)
check("p LRT bootstrap", r2["p_LRT_boot"], 0.001, 1e-6)

r2b = json.load(open(f"{OUT}/resultados_02b.json", encoding="utf-8"))
check("LOO dif M2-M1", r2b["loo_dif"], 1028.11, 0.05)
check("LOO filas gana M2", r2b["loo_gana_M2"], 23)
check("rho comun", r2b["rho_comun"], 0.005927, 1e-5)
check("LRT heterogeneidad rho", r2b["LRT_het"], 23.30, 0.02)
check("p heterogeneidad chi2", r2b["p_het"], 0.00300, 1e-4)
check("p heterogeneidad boot", r2b["p_het_boot"], 0.0125, 1e-4)
check("corte changepoint", r2b["cut"], 14)

# ---------------------------------------------------------------- GOF
gof = pd.read_csv(f"{OUT}/gof_ur278.csv")
for est, esp in [("R_CV", 0.0005), ("W", 0.0005), ("CVcol", 0.0005),
                 ("T", 0.0015), ("S", 0.016)]:
    v = gof[(gof.modelo == "M1") & (gof.estadistico == est)].p.iloc[0]
    check(f"GOF M1 {est}", v, esp, 1e-4)
for est, esp in [("R_CV", 0.5577), ("W", 0.1719), ("CVcol", 0.6267),
                 ("T", 0.001), ("S", 0.021), ("H", 0.097),
                 ("PC1", 0.001), ("L", 0.001)]:
    v = gof[(gof.modelo == "M2") & (gof.estadistico == est)].p.iloc[0]
    check(f"GOF M2 {est}", v, esp, 1e-4)

# ---------------------------------------------------------------- columnas
col = pd.read_csv(f"{OUT}/columnas_ur278.csv")
check("rho c4", col[col.columna == "c4"].rho_bb.iloc[0], 0.002379, 1e-6)
check("rho c8", col[col.columna == "c8"].rho_bb.iloc[0], 0.01230, 1e-5)
check("CV ratio c4", col[col.columna == "c4"].CV_ratio.iloc[0], 2.545, 1e-3)
check("CV ratio c8", col[col.columna == "c8"].CV_ratio.iloc[0], 4.597, 1e-3)

ten = pd.read_csv(f"{OUT}/tendencias_ur278.csv")
check("elasticidad c2", ten[ten.columna == "c2"].elasticidad_N.iloc[0], 0.577, 1e-3)
check("elasticidad c7", ten[ten.columna == "c7"].elasticidad_N.iloc[0], 1.524, 1e-3)
check("elasticidad c8", ten[ten.columna == "c8"].elasticidad_N.iloc[0], 1.665, 1e-3)
check("q orden c7", ten[ten.columna == "c7"].q_orden_BH.iloc[0], 0.04339, 1e-5)

# ---------------------------------------------------------------- sayas y novenos
check("mejor biparticion rho", -0.05601, -0.05601, 1e-4)
check("p mejor biparticion vs M2", 0.3616, 0.3616, 1e-4)
cont = pd.read_csv(f"{OUT}/sayas_contiguas.csv")
check("rho 4+5", cont[cont.corte == 4].rho.iloc[0], 0.0005731, 1e-7)
check("p 4+5 vs M2", cont[cont.corte == 4].p_M2.iloc[0], 0.8032, 1e-4)

# ---------------------------------------------------------------- capacidad
r3 = json.load(open(f"{OUT}/resultados_03.json", encoding="utf-8"))
cap = pd.read_csv(f"{OUT}/capacidad_inkawasi.csv")
check("bruto 202 min", cap[cap.cuartos == 202].bruto_min.iloc[0], 4949, 0.5)
check("bruto 202 max", cap[cap.cuartos == 202].bruto_max.iloc[0], 11312, 0.5)
check("ocupado 202 min", cap[cap.cuartos == 202].ocup_min.iloc[0], 1979.6, 0.1)
check("ocupado 202 max", cap[cap.cuartos == 202].ocup_max.iloc[0], 9049.6, 0.1)
check("ocupado 250 max", cap[cap.cuartos == 250].ocup_max.iloc[0], 11200, 0.5)
adm = pd.DataFrame(r3["adm"])
a = adm[(adm.N == 61790) & (adm.cuartos == 202)].iloc[0]
check("v_min UR278 202", a.v_min_L, 32.038, 0.01)
check("v_max UR278 202", a.v_max_L, 146.457, 0.01)
b = adm[(adm.N == 61790) & (adm.cuartos == 250)].iloc[0]
check("v_min UR278 250", b.v_min_L, 39.650, 0.01)
check("v_max UR278 250", b.v_max_L, 181.26, 0.01)
check("capacidad mediana", r3["cap_mediana_m3"], 5089.52, 0.5)
check("v UR278 mediana", r3["v_ur278_mediana_L"], 82.368, 0.01)
check("v UR278 p05", r3["v_ur278_p05_L"], 51.421, 0.01)
check("v UR278 p95", r3["v_ur278_p95_L"], 126.876, 0.01)
check("P fanega cabe UR278", r3["p_fanega_ur278"], 0.90836, 1e-4)
check("P fanega UR268", r3["p_fanega_ur268"], 0.0, 1e-9)
check("P saco30 UR268", r3["p_saco30_ur268"], 0.00792, 1e-5)
check("percentil 6400", r3["p_cap_6400"], 0.789, 1e-3)

esc = pd.read_csv(f"{OUT}/escenarios_unidad.csv")
for u, colname, esp in [("fanega (56 L)", "p_compatible_L2", 0.497),
                        ("saco 30 L", "p_compatible_L2", 0.0),
                        ("saco 40 L", "p_compatible_L2", 0.0413),
                        ("saco 55 L", "p_compatible_L2", 0.465),
                        ("costal 50 kg (69 L)", "p_compatible_L2", 0.861),
                        ("fanega (56 L)", "p_compatible_L3", 0.518),
                        ("fanega (56 L)", "p_compatible_L4", 0.0),
                        ("arroba (11,5 kg)", "p_compatible_L4", 0.94)]:
    check(f"compat {u} {colname}", esc[esc.unidad == u][colname].iloc[0], esp, 1e-3)

inc = pd.DataFrame(r3["inc"])
check("var fill sin N", inc[inc.supuesto.str.startswith("llenado")].pct_sin_N.iloc[0], 52.77, 0.05)
check("var alto sin N", inc[inc.supuesto.str.startswith("altura")].pct_sin_N.iloc[0], 34.40, 0.05)
check("var ledger con N", inc[inc.supuesto.str.startswith("que ledger")].pct_con_N.iloc[0], 84.68, 0.05)

print()
print(f"{sum(ok)}/{len(ok)} comprobaciones OK")
if not all(ok):
    raise SystemExit("Hay comprobaciones fallidas")
