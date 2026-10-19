"""05_corpus.py — Busca en el corpus KFG quipus con la forma que predice el registro wanka.
Predicción: 12 grupos (categorías), ~19 cuerdas por grupo (eventos), 200-450 cuerdas,
mayoría numéricas, grupos cromáticamente homogéneos (color = categoría).
Salida: candidatos.csv, salida_05.txt
"""
import os, json
import numpy as np, pandas as pd
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(20261018)

c = pd.read_csv("../../datos/cuerdas.csv", low_memory=False)
q = pd.read_csv("../../datos/quipus.csv", low_memory=False).set_index("kfg")

# ---- features por quipu ----------------------------------------------------
def color_base(x):
    if pd.isna(x):
        return "?"
    return str(x).split(":")[0].split("-")[0].split("/")[0].strip()

c["cb"] = c.color.map(color_base)
c["numerica"] = (c.valor.fillna(0) > 0) & c.nudos.notna()

rows = []
for k, s in c.groupby("kfg"):
    pend = s[s.nivel == 0]
    g = pend.groupby("grupo").size()
    num = s.numerica.mean()
    # homogeneidad cromática de los grupos (solo grupos con >=3 cuerdas)
    hom, ng = [], 0
    for gr, sub in s.groupby("grupo"):
        if len(sub) < 3:
            continue
        ng += 1
        moda = sub.cb.value_counts(normalize=True).iloc[0]
        hom.append(moda)
    rows.append(dict(kfg=k, ncord=len(s), n_grupos=s.grupo.nunique(),
                     n_pend=len(pend), med_grupo=g.median(), max_grupo=g.max(),
                     frac_num=num, hom_color=np.mean(hom) if hom else np.nan,
                     nivel_max=s.nivel.max(),
                     n_sub=(s.nivel > 0).sum(),
                     ratio_sub=(s.nivel > 0).mean(),
                     n_colores=s.cb.nunique()))
F = pd.DataFrame(rows).set_index("kfg").join(q[["procedencia", "museo"]])
F.to_csv("features_corpus.csv")

pred = dict(n_grupos=(10, 14), ncord=(180, 500), med_grupo=(12, 26), frac_num=(0.55, 1.0))
sel = F[(F.n_grupos.between(*pred["n_grupos"])) &
        (F.ncord.between(*pred["ncord"])) &
        (F.med_grupo.between(*pred["med_grupo"])) &
        (F.frac_num.between(*pred["frac_num"]))]
print("Quipus compatibles con la forma wanka predicha:", len(sel), "de", len(F),
      f"({100*len(sel)/len(F):.1f} %)")
print(sel.sort_values(["hom_color", "ncord"], ascending=False)
       [["ncord","n_grupos","med_grupo","max_grupo","frac_num","hom_color","n_colores","procedencia"]]
       .head(15).to_string())

# ---- ¿cuán raro es? base rates y nulo -------------------------------------
print("\nBase rates:")
for k, (a, b) in pred.items():
    print(f"  {k:10s} en [{a},{b}]: {100*F[k].between(a,b).mean():.1f} %")
# nulo: emparejar cada feature por separado (independencia) -> esperado
pe = np.prod([F[k].between(a, b).mean() for k, (a, b) in pred.items()])
print(f"Esperado por independencia: {pe*len(F):.1f} quipus; observado {len(sel)}; "
      f"razón {len(sel)/(pe*len(F)+1e-9):.2f}")

# ---- los 12 grupos mejor alineados (aunque no cumplan todo) ---------------
print("\nQuipus con 11-13 grupos y >=150 cuerdas (candidatos a arquitectura de 12 categorías):")
cand = F[(F.n_grupos.between(11, 13)) & (F.ncord >= 150)].sort_values("ncord", ascending=False)
print(cand[["ncord","n_grupos","med_grupo","max_grupo","frac_num","hom_color","n_colores","procedencia"]]
      .to_string())
cand.to_csv("candidatos.csv")

# ---- ¿hay algún quipu de procedencia Mantaro/Jauja? -----------------------
proc = F.procedencia.astype(str)
print("\nProcedencias que mencionan Mantaro/Jauja/Xauxa/Huanca:",
      proc[proc.str.contains("Mantaro|Jauja|Xauxa|Huanca", case=False)].unique().tolist())
print("Quipus con procedencia desconocida:", int((proc == "Unknown").sum()))
