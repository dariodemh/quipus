"""02 - Inventario de diferencias KFG vs OKR en los 52 quipus de Incahuasi.

Emparejamiento por clave = (nº de colgante por 'orden' KFG / CORD_ORDINAL OKR) + camino de subsidiarias.
  KFG: p12s3 -> (12,'s3');  OKR: p12s3 -> (12,'s3').
Las diferencias de nombre por jerarquia aplanada en OKR aparecen como pares solo_kfg/solo_okr; se separan
las que son el mismo colgante con distinto nivel.

Salidas: inventario_incahuasi.csv, detalle_nuevas.csv, detalle_solo_kfg.csv.
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
AQUI = Path(__file__).resolve().parent
INC = ([f"JC{i:03d}" for i in range(1, 24)]
       + [f"UR{i}" for i in range(255, 281) if i not in (267, 273, 274)]
       + ["UR267A", "UR267B", "UR273A", "UR273B", "UR274A", "UR274B"])


def clave_kfg(c):
    c = c.sort_values(["kfg", "orden"]).copy()
    c["rank"] = np.nan
    for k, s in c.groupby("kfg"):
        r0 = s[s.nivel == 0].sort_values("orden")
        m = {cu: i + 1 for i, cu in enumerate(r0.cuerda)}
        c.loc[s.index, "rank"] = s.cuerda.map(lambda x: m.get(x.split("s")[0], np.nan))
    c["rank"] = c["rank"].astype("Int64")
    c["sub"] = c.cuerda.str.extract(r"^p\d+(s.*)?$")[0].fillna("")
    c["clave"] = c["rank"].astype(str) + c["sub"]
    return c.drop_duplicates(["kfg", "clave"])


def clave_okr(o):
    o = o.copy()
    o["rank"] = o.cuerda.str.extract(r"^p(\d+)")[0].astype("Int64")
    o["sub"] = o.cuerda.str.extract(r"^p\d+(s.*)?$")[0].fillna("")
    o["clave"] = o["rank"].astype(str) + o["sub"]
    return o.drop_duplicates(["kfg", "clave"])


def main():
    k = pd.read_csv(RAIZ / "analisis/datos/cuerdas.csv", low_memory=False, keep_default_na=False)
    k = k[k.kfg.isin(INC)].copy()
    k["valor"] = pd.to_numeric(k.valor, errors="coerce").fillna(0).round().astype(int)
    k["pres"] = (k.nudos != "") | (k.valor > 0)
    o = pd.read_csv(AQUI / "cuerdas_okr.csv", keep_default_na=False)
    o = o[o.kfg.isin(INC)].copy()
    o["pres"] = o.pres.astype(str).str.lower().isin(["true", "1"])
    K, O = clave_kfg(k), clave_okr(o)

    filas, nuevas, viejas = [], [], []
    for q in INC:
        a, b = K[K.kfg == q], O[O.kfg == q]
        sa, sb = set(a.clave), set(b.clave)
        dk = a[~a.clave.isin(sb)]
        do = b[~b.clave.isin(sa)]
        com = a[a.clave.isin(sb)].set_index("clave")
        comb = b[b.clave.isin(sa)].set_index("clave")
        dv = [(c_, int(com.loc[c_, "valor"]), int(comb.loc[c_, "valor"])) for c_ in com.index
              if com.loc[c_, "valor"] != comb.loc[c_, "valor"]]
        filas.append(dict(kfg=q, n_kfg=len(a), n_okr=len(b),
                          n0_kfg=int((a.nivel == 0).sum()), n0_okr=int((b.nivel == 0).sum()),
                          nsub_kfg=int((a.nivel > 0).sum()), nsub_okr=int((b.nivel > 0).sum()),
                          suma_kfg=int(a.valor.sum()), suma_okr=int(b.valor.sum()),
                          grupos_kfg=a.grupo.nunique(), grupos_okr=b.grupo.nunique(),
                          marcadoras_okr=int(b.sep.sum()), superiores_okr=int((b.clas == "T").sum()),
                          n_solo_kfg=len(dk), n_solo_okr=len(do), val_distintos=len(dv),
                          solo_kfg=";".join(f"{r.clave}={r.valor}" for r in dk.itertuples()),
                          solo_okr=";".join(f"{r.clave}={r.valor}" for r in do.itertuples()),
                          ej_val=";".join(f"{c_}:{x}->{y}" for c_, x, y in dv[:5])))
        for r in do.itertuples():
            nuevas.append(dict(kfg=q, clave=r.clave, nivel=r.nivel, grupo=r.grupo, valor=r.valor,
                               color=r.color, padre=r.padre, clas=r.clas))
        for r in dk.itertuples():
            viejas.append(dict(kfg=q, clave=r.clave, nivel=r.nivel, grupo=r.grupo, valor=r.valor,
                               color=r.color, padre=r.padre))
    D = pd.DataFrame(filas)
    D.to_csv(AQUI / "inventario_incahuasi.csv", index=False)
    pd.DataFrame(nuevas).to_csv(AQUI / "detalle_nuevas.csv", index=False)
    pd.DataFrame(viejas).to_csv(AQUI / "detalle_solo_kfg.csv", index=False)
    pd.set_option("display.width", 250)
    cols = ["kfg", "n_kfg", "n_okr", "n0_kfg", "n0_okr", "nsub_kfg", "nsub_okr", "suma_kfg", "suma_okr",
            "grupos_kfg", "grupos_okr", "marcadoras_okr", "superiores_okr", "n_solo_kfg", "n_solo_okr", "val_distintos"]
    print(D[cols].to_string(index=False))
    print("\nTOTALES:", D[cols[1:]].sum().to_dict())
    print("\nQuipus con cuerdas OKR que no estan en KFG (por clave):")
    print(D[D.n_solo_okr > 0][["kfg", "n_solo_okr", "solo_okr"]].to_string(index=False))
    print("\nQuipus con cuerdas KFG que no estan en OKR:")
    print(D[D.n_solo_kfg > 0][["kfg", "n_solo_kfg", "solo_kfg"]].head(12).to_string(index=False))
    print("\nValores distintos:", D[D.val_distintos > 0][["kfg", "val_distintos", "ej_val"]].to_string(index=False))


if __name__ == "__main__":
    main()
