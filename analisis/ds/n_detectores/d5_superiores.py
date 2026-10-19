"""D5. Cuantas cuerdas superiores (T) y marcadoras (M) de OKR se pierden en KFG.

Cruce:
  analisis/datos/cuerdas.csv  <->  khipu.db (tabla cord) via analisis/17_okr_pendientes/puente.csv
  (kfg -> KHIPU_ID).
  OKR CORD_LEVEL=1 con CORD_ORDINAL=n  <->  n-esimo colgante (nivel 0) de KFG por 'orden'.
  (comprobado en UR087: CORD_ORDINAL 7,14,21,... = p7,p14,p21,...)

'Perdida' = OKR clasifica la cuerda como T (cuerda superior) o M (marcador) y KFG no la marca
como union='T'. KFG no tiene campo de marcador, de modo que todo M es una perdida de codificacion.
Se cuenta ademas el caso especifico union='U' (el que documenta k_UR087).

Salida: superiores_perdidas.csv (por quipu) + resumen por consola.
"""
import sqlite3
import numpy as np
import pandas as pd
import comun as C

DB = C.RAIZ / "data/external/open-khipu-repository/data/khipu.db"
PUENTE = C.RAIZ / "analisis/17_okr_pendientes/puente.csv"


def main():
    c, q = C.cargar()
    p = pd.read_csv(PUENTE)
    p = p[p.khipu_id.notna()][["kfg", "khipu_id"]].copy()
    p["khipu_id"] = p.khipu_id.astype(int)
    con = sqlite3.connect(DB)
    ids = tuple(p.khipu_id.unique().tolist())
    marks = ",".join("?" * len(ids))
    cord = pd.read_sql(f"""select KHIPU_ID,CORD_ID,CORD_ORDINAL,CORD_LEVEL,CORD_CLASSIFICATION,
                                  ATTACHMENT_TYPE,INVESTIGATOR_CORD_NUM
                           from cord where KHIPU_ID in ({marks})""", con, params=ids)
    cord["CORD_LEVEL"] = pd.to_numeric(cord.CORD_LEVEL, errors="coerce")
    cord["CORD_ORDINAL"] = pd.to_numeric(cord.CORD_ORDINAL, errors="coerce")
    cls = cord.CORD_CLASSIFICATION.fillna("")
    oks = cord[(cord.CORD_LEVEL == 1) & cls.isin(["T", "M"])].copy()
    print(f"quipus puente con id: {len(p)}; cuerdas OKR nivel 1: {(cord.CORD_LEVEL == 1).sum()}; T: {(cls == 'T').sum()}; M: {(cls == 'M').sum()}")

    # rangos KFG
    k0 = c[c.nivel == 0].sort_values(["kfg", "orden"]).copy()
    k0["rank"] = k0.groupby("kfg").cumcount() + 1
    mapa = {(r.kfg, int(r["rank"])): (r.cuerda, r.union, r.valor) for _, r in k0.iterrows()}

    filas = []
    for r in p.itertuples():
        kk = r.kfg
        sub = oks[oks.KHIPU_ID == r.khipu_id]
        nk = int((k0.kfg == kk).sum())
        t = sub[sub.CORD_CLASSIFICATION == "T"]
        m = sub[sub.CORD_CLASSIFICATION == "M"]
        t_info = [mapa.get((kk, int(o))) for o in t.CORD_ORDINAL]
        m_info = [mapa.get((kk, int(o))) for o in m.CORD_ORDINAL]
        t_perd = sum(1 for v in t_info if v is None or v[1] != "T")
        t_u = sum(1 for v in t_info if v is not None and v[1] == "U")
        t_rv = sum(1 for v in t_info if v is not None and v[1] in ("R", "V"))
        t_otro = sum(1 for v in t_info if v is not None and v[1] not in ("T", "U", "R", "V"))
        t_sin = sum(1 for v in t_info if v is None)
        # marcadores: KFG no tiene clase M; se cuentan como perdidos salvo que por azar lleve union T
        m_perd = sum(1 for v in m_info if v is None or v[1] != "T")
        # falsos positivos: KFG dice T y OKR no
        kfg_t = set(k0[(k0.kfg == kk) & (k0.union == "T")].cuerda)
        okr_t = {v[0] for v in t_info if v is not None}
        fp = len(kfg_t - okr_t)
        if len(t) or len(m) or kfg_t:
            filas.append(dict(kfg=kk, khipu_id=int(r.khipu_id), nivel0_kfg=nk,
                              n_T_okr=len(t), n_T_kfg=len(kfg_t), n_T_perdidas=t_perd,
                              T_como_U=t_u, T_como_RV=t_rv, T_otro=t_otro, T_sin_mapear=t_sin,
                              n_M_okr=len(m), n_M_perdidas=m_perd, T_kfg_no_okr=fp))
    D = pd.DataFrame(filas).sort_values(["n_T_perdidas", "n_M_perdidas"], ascending=False)
    D.to_csv(C.AQUI / "superiores_perdidas.csv", index=False)
    tot = D[["n_T_okr", "n_T_kfg", "n_T_perdidas", "T_como_U", "T_como_RV", "T_otro",
             "T_sin_mapear", "n_M_okr", "n_M_perdidas", "T_kfg_no_okr"]].sum()
    print("TOTALES en quipus cruzados:")
    print(tot.to_string())
    print(f"  (T okr en cruzados: {int(tot['n_T_okr'])}; T perdidas: {int(tot['n_T_perdidas'])} = "
          f"{100*tot['n_T_perdidas']/max(1,tot['n_T_okr']):.1f}%; M perdidas: {int(tot['n_M_perdidas'])}/{int(tot['n_M_okr'])})")
    print(f"\nquipus con T o M: {len(D)}; con T: {(D.n_T_okr > 0).sum()}; con M: {(D.n_M_okr > 0).sum()}")
    print("\nTop 20 por T perdidas:")
    print(D.head(20).to_string(index=False))
    print("\nUR087:")
    print(D[D.kfg == "UR087"].to_string(index=False))
    # cobertura global
    print(f"\nKFG union=T en todo cuerdas.csv: {(c.union == 'T').sum()} cuerdas, "
          f"{(c[c.union == 'T'].kfg.nunique())} quipus")
    con2 = sqlite3.connect(DB)
    allc = pd.read_sql("select KHIPU_ID,CORD_LEVEL,CORD_CLASSIFICATION from cord", con2)
    allc["CORD_LEVEL"] = pd.to_numeric(allc.CORD_LEVEL, errors="coerce")
    allc["CORD_CLASSIFICATION"] = allc.CORD_CLASSIFICATION.fillna("")
    t_all = allc[(allc.CORD_LEVEL == 1) & (allc.CORD_CLASSIFICATION == "T")]
    m_all = allc[(allc.CORD_LEVEL == 1) & (allc.CORD_CLASSIFICATION == "M")]
    map_ids = set(p.khipu_id)
    t_map = t_all[t_all.KHIPU_ID.isin(map_ids)]
    print(f"OKR T nivel1 en khipu.db: {len(t_all)} en {t_all.KHIPU_ID.nunique()} quipus; "
          f"de ellos cruzables por puente: {len(t_map)} en {t_map.KHIPU_ID.nunique()} quipus "
          f"({len(t_all)-len(t_map)} T en quipus sin cruce)")
    print(f"OKR M nivel1: {len(m_all)} en {m_all.KHIPU_ID.nunique()} quipus; cruzables: "
          f"{len(m_all[m_all.KHIPU_ID.isin(map_ids)])} en {m_all[m_all.KHIPU_ID.isin(map_ids)].KHIPU_ID.nunique()}")
    sinmap = c[(c.union == "T") & (~c.kfg.isin(p.kfg))]
    print(f"KFG union=T sin fila en puente: {len(sinmap)} cuerdas en {sinmap.kfg.nunique()} quipus")


if __name__ == "__main__":
    main()
