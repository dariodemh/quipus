"""Tareas 1 y 2. Inventario de redundancia y leave-one-out (una cuerda oculta por vez, regla ciega).

Para cada cuerda con valor del sistema se oculta SOLO su valor, se aplican todas las reglas (comun19.predecir) y se
compara con el real. Salidas: loo_resultados.csv (una fila por cuerda x via), inventario_redundancia.csv (una fila por
cuerda con >=1 via), loo_resumen.csv. Marca `descubrimiento` = la cuerda aparece en una arista del grafo de 13 o en un
grupo emparejado de UR270/UR278 (relaciones halladas mirando estos mismos valores).
"""
import re
import numpy as np
import pandas as pd
import comun19 as M

grafo = pd.read_csv(M.AQUI.parent / "13_sistema_incahuasi" / "grafo_cuerdas.csv")
pareja = pd.read_csv(M.AQUI.parent / "13_sistema_incahuasi" / "ur270_ur278.csv")
DESC = set()


def marca_grupo(k, g, solo_s1=False, solo_l0=False):
    for x in M.GR[k].get(int(g), []):
        if solo_s1 and not x[1].endswith("s1"):
            continue
        if solo_l0 and M.INFO[x]["nivel"] != 0:
            continue
        DESC.add(x)


for k_, c_ in (("origen", "cuerda_o"), ("destino", "cuerda_d")):
    for k, cu in zip(grafo[k_], grafo[c_]):
        if re.fullmatch(r"p\d+(s\d+)*", str(cu)):
            DESC.add((k, cu))
        else:
            m = re.match(r"g(\d+)", str(cu))
            if m:
                marca_grupo(k, m.group(1), solo_l0=True)
                if "subsid" in str(cu):
                    marca_grupo(k, m.group(1), solo_s1=True)
for _, r in pareja[pareja.aciertos >= 5].iterrows():
    marca_grupo("UR270", r.grupo_UR270)
    marca_grupo("UR278", r.fila_UR278)


def indep(vias):
    """Nº maximo (voraz) de vias con conjuntos de entrada disjuntos entre si."""
    usados, n = set(), 0
    for v in sorted(vias, key=lambda v: len(v["inputs"])):
        s = set(v["inputs"])
        if not (s & usados):
            usados |= s
            n += 1
    return n


filas, inv = [], []
for t in M.presentes():
    real = M.VAL[t]
    P = M.predecir(t)
    for p in P:
        m = M.metricas(p["pred"], real)
        filas.append(dict(quipu=t[0], cuerda=t[1], real=real, pred=p["pred"], regla=p["rule"], via=p["via"],
                          n_inputs=len(p["inputs"]), gap=p["gap"], rol=M.rol(t), descubrimiento=t in DESC, **m))
    if P:
        vals = [p["pred"] for p in P]
        inv.append(dict(quipu=t[0], cuerda=t[1], valor=real, n_vias=len(P), n_vias_indep=indep(P),
                        reglas="+".join(sorted({p["rule"] for p in P})),
                        n_vias_acierto=sum(abs(v - real) == 0 for v in vals),
                        n_vias_acierto_pm1=sum(abs(v - real) <= 1 for v in vals),
                        en_grafo_13=t in DESC))
L = pd.DataFrame(filas)
I = pd.DataFrame(inv)
L.to_csv(M.AQUI / "loo_resultados.csv", index=False)
I.to_csv(M.AQUI / "inventario_redundancia.csv", index=False)

pd.set_option("display.width", 220)
pres = M.presentes()
print(f"cuerdas con valor en el sistema: {len(pres)}; con >=1 via ciega: {len(I)} ({len(I)/len(pres):.1%}); en grafo/descubrimiento: {sum(t in DESC for t in pres)}")
tot = pd.Series([t[0] for t in pres]).value_counts()
print(pd.DataFrame({"cuerdas": tot, "predecibles": I.groupby("quipu").size()}).fillna(0).astype(int).to_string())
print("\nvias por cuerda (n, indep):")
print(pd.crosstab(I.n_vias, I.n_vias_indep).to_string())


def resumen(df, por):
    g = df.groupby(por)
    return pd.DataFrame(dict(n=g.size(), exacta=g.exacta.mean().round(3), d1=g.d1.mean().round(3),
                             tol=g.tol.mean().round(3), r5=g.r5.mean().round(3), rel_mediana=g.rel.median().round(4),
                             rel_media=g.rel.mean().round(3)))


print("\n== por regla (todas las predicciones)")
R1 = resumen(L, "regla")
print(R1.to_string())
print("\n== por regla y descubrimiento")
print(resumen(L, ["regla", "descubrimiento"]).to_string())
print("\n== por regla y quipu")
R2 = resumen(L, ["regla", "quipu"])
print(R2.to_string())
R1.to_csv(M.AQUI / "loo_resumen_regla.csv")
R2.to_csv(M.AQUI / "loo_resumen_regla_quipu.csv")
print("\n== regla de alineacion ciega: hueco 1 (anclas contiguas) frente a hueco >1")
print(resumen(L[L.regla.isin(["copia", "suma_AB", "fila278"])].assign(hueco=lambda d: np.where(d.gap <= 1, "1", ">1")), ["regla", "hueco"]).to_string())
resumen(L, ["regla", "via"]).to_csv(M.AQUI / "loo_resumen_via.csv")

# cobertura por cuerda y tasa de acierto con una vez por cuerda: voto por mayoria (empates: regla de mayor orden)
ORDEN = ["fila278", "suma_AB", "celda270", "copia", "cierre", "cuota"]
cons = []
for (q, cu), x in L.groupby(["quipu", "cuerda"]):
    cnt = x.pred.value_counts()
    top = cnt[cnt == cnt.max()].index
    cand = x[x.pred.isin(top)].copy()
    cand["o"] = cand.regla.map(ORDEN.index)
    p = cand.sort_values("o").iloc[0]
    cons.append(dict(quipu=q, cuerda=cu, real=p.real, pred=p.pred, votos=int(cnt.max()), n_vias=len(x),
                     descubrimiento=p.descubrimiento, **M.metricas(p.pred, p.real)))
C_ = pd.DataFrame(cons)
C_.to_csv(M.AQUI / "loo_consenso.csv", index=False)
print("\n== consenso por cuerda (una prediccion por cuerda)")
print(resumen(C_.assign(todo="todas"), "todo").to_string())
print(resumen(C_, "descubrimiento").to_string())
print(resumen(C_, "quipu").to_string())
print(resumen(C_.assign(v=C_.n_vias.clip(upper=3)), "v").to_string())
print("\nacuerdo entre vias: cuerdas con >=2 vias; las que coinciden entre si (=votos>=2):")
m2 = C_[C_.n_vias >= 2]
print(f"{len(m2)} cuerdas; con voto >=2: {(m2.votos>=2).sum()}; exacta en ese caso: {m2[m2.votos>=2].exacta.mean():.3f}; sin acuerdo: exacta {m2[m2.votos<2].exacta.mean():.3f}")
