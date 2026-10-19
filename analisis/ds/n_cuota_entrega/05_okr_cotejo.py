"""Paso 5 (control de fuente): cotejo de la jerarquía P/S1 de KFG con OKR, solo lectura.

Reconstruye el valor de cada cuerda en OKR como suma de nudos
(L/LL: nº de vueltas x valor de posición; S/E: valor de posición).
- Nivel 0: compara valor a valor los colgantes en orden.
- Nivel 1: compara, colgante a colgante, el conjunto ordenado de sus subsidiarias
  (PENDANT_FROM en OKR) con el de KFG (s1, s2, ...).
También imprime el vector P y S1 del grupo 6 de UR270 desde KFG (ya cotejado en OKR).
Salida: salida_05.txt, okr_cotejo.csv
"""
import sqlite3
import numpy as np
import pandas as pd

import lib_cuota as L

DB = L.RAIZ / "data/external/open-khipu-repository/data/khipu.db"
con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)

c, q = L.cargar()
qidx = q.set_index("kfg")

ctrl = pd.read_csv("p_vs_s1.csv")
ctrl = ctrl.loc[ctrl.sistema == "Control", "kfg"].tolist()
ks = L.incahuasi(q) + ctrl

SQL = """
select c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, c.PENDANT_FROM,
       sum(case when k.TYPE_CODE in ('L','LL')
                then coalesce(k.NUM_TURNS,1)*k.knot_value_type
                else k.knot_value_type end) val,
       count(k.KNOT_ID) nudos
from cord c left join knot k on k.CORD_ID = c.CORD_ID
where c.KHIPU_ID = ?
group by c.CORD_ID
"""

filas = []
for k in ks:
    okr = qidx.loc[k, "okr"]
    row = con.execute("select KHIPU_ID from khipu_main where OKR_NUM=?", (okr,)).fetchone()
    if not row:
        filas.append(dict(kfg=k, okr=okr, nivel=0, estado="sin OKR"))
        continue
    kid = row[0]
    d = pd.read_sql(SQL, con, params=(kid,))
    d["val"] = d["val"].where(d["nudos"] > 0)
    kfg = c[c.kfg == k]
    # nivel 0: valor a valor en orden
    a = kfg[kfg.nivel == 0].sort_values("orden").valor.to_numpy(float)
    p_okr = d[d.CORD_LEVEL == 1].sort_values("CORD_ORDINAL")
    b = p_okr.val.to_numpy(float)
    n = min(len(a), len(b))
    ok = (~np.isnan(a[:n])) & (~np.isnan(b[:n]))
    filas.append(dict(kfg=k, okr=okr, nivel=0, n_kfg=len(a), n_okr=len(b),
                      comparables=int(ok.sum()), exactos=int(np.sum(a[:n][ok] == b[:n][ok])),
                      med_kfg=float(np.nanmedian(a)) if len(a) else np.nan,
                      med_okr=float(np.nanmedian(b)) if len(b) else np.nan))
    # nivel 1: conjuntos de subsidiarias por colgante
    comp = exact = 0
    for i, (_, pk) in enumerate(p_okr.iterrows()):
        if i >= len(kfg[kfg.nivel == 0].sort_values("orden")):
            break
        nombre = kfg[kfg.nivel == 0].sort_values("orden").cuerda.iloc[i]
        hijos_kfg = kfg[kfg.padre == nombre].sort_values("orden")
        vk = sorted(int(x) for x in hijos_kfg.valor if x > 0)
        hijos_okr = d[d.PENDANT_FROM == pk.CORD_ID].sort_values("CORD_ORDINAL")
        vo = sorted(int(x) for x in hijos_okr.val if not np.isnan(x))
        if vk and vo:
            comp += 1
            exact += int(vk == vo)
    filas.append(dict(kfg=k, okr=okr, nivel=1, n_kfg=len(kfg[kfg.nivel == 1]),
                      n_okr=len(d[d.CORD_LEVEL == 2]), comparables=comp, exactos=exact,
                      med_kfg=np.nan, med_okr=np.nan))

R = pd.DataFrame(filas)
R.to_csv("okr_cotejo.csv", index=False)

# grupo 6 de UR270
u = c[(c.kfg == "UR270") & (c.nivel == 0) & (c.grupo == 6)].sort_values("orden")
det = []
for _, r in u.iterrows():
    s1 = c[(c.kfg == "UR270") & (c.cuerda == r.cuerda + "s1")]
    det.append(dict(cuerda=r.cuerda, P=int(r.valor), S1=int(s1.valor.iloc[0]) if len(s1) else None))

with open("salida_05.txt", "w", encoding="utf-8") as f:
    f.write("== cotejo KFG vs OKR ==\n")
    f.write(R.to_string(index=False) + "\n\n")
    for niv in [0, 1]:
        x = R[R.nivel == niv]
        if "estado" in x.columns:
            x = x[x["estado"].isna()]
        f.write(f"nivel {niv}: quipus {len(x)}; comparables {int(x.comparables.sum())}; "
                f"exactos {int(x.exactos.sum())} "
                f"({x.exactos.sum()/max(1,x.comparables.sum()):.3f})\n")
    f.write("\nUR270 grupo 6 (KFG):\n" + pd.DataFrame(det).to_string(index=False) + "\n")

print(R.groupby("nivel")[["comparables", "exactos", "n_kfg", "n_okr"]].sum().to_string())
print("tasa exacta:", (R.groupby("nivel").exactos.sum() /
                        R.groupby("nivel").comparables.sum()).round(3).to_dict())
print(pd.DataFrame(det).to_string(index=False))
