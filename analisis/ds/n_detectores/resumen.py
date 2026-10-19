"""Resumen y ensamblado de enlaces_nuevos.csv.

Anade a D2/D3 un q dirigido: BH dentro de la familia (procedencia/museo) restringida a los quipus
con contenido numerico (>=3 cabeceras/totales >=100), que es la unidad de la leccion Incahuasi.
Luego reune D1-D4 en un solo CSV.
"""
import numpy as np
import pandas as pd
import comun as C

AQUI = C.AQUI


def q_dirigida(D, big):
    D = D.copy()
    D["q_dir"] = np.nan
    sub = D[D.A.isin(big) & D.B.isin(big)]
    for fam, idx in sub.groupby("familia").groups.items():
        D.loc[idx, "q_dir"] = C.bh(sub.loc[idx, "p"])
    return D


def main():
    c, q = C.cargar()
    R = C.todos_los_registros(c)
    X = C.cabeceras(R)
    big = {k for k, v in X.items() if (np.asarray(v) >= 100).sum() >= 3}

    D2full = pd.read_csv(AQUI / "d2_observado.csv")
    D2full = q_dirigida(D2full, big)
    D2full.to_csv(AQUI / "d2_observado.csv", index=False, float_format="%.4g")
    D2 = pd.read_csv(AQUI / "enlaces_d2.csv")
    D2 = D2.merge(D2full[["A", "B", "q_dir"]], on=["A", "B"], how="left")
    D3full = pd.read_csv(AQUI / "d3_cadenas.csv")
    D3full = q_dirigida(D3full, big)
    D3full.to_csv(AQUI / "d3_cadenas.csv", index=False, float_format="%.4g")
    D3 = pd.read_csv(AQUI / "enlaces_d3.csv")
    D3 = D3.merge(D3full[["A", "B", "q_dir"]], on=["A", "B"], how="left")
    D4 = pd.read_csv(AQUI / "d4_celdas.csv")
    D4["q_dir"] = D4["q_familia"]
    D4.to_csv(AQUI / "d4_celdas.csv", index=False, float_format="%.4g")
    D1 = pd.read_csv(AQUI / "d1_cuotas.csv")

    filas = []
    for r in D1.itertuples():
        if (r.q_max < 0.05) or (r.q_pos < 0.05) or (r.q_expl < 0.05):
            cif = f"nrec={r.nrec}; c*={r.c_estrella}; apoyo={r.apoyo}; expl={r.cuota_explicita}; pos={r.pos_j}:{r.pos_valor}x{r.pos_conteo}"
            p = min(r.p_max, r.p_pos, r.p_expl)
            qq = min(r.q_max, r.q_pos, r.q_expl)
            filas.append(dict(detector="D1", A=r.kfg, B="", C="", cifras=cif, p=p, q=qq,
                              q_dir=qq, familia=r.familia,
                              nota="cuota por diferencia" if r.q_max < 0.05 else "",
                              enlace=""))
    for r in D2.itertuples():
        if (r.p <= 0.05):
            cif = f"n={r.n}; obs={r.obs}; exacto={r.obs_exacto}; nC={getattr(r, 'nC', '')}; tau={getattr(r, 'tau', '')}; top3={getattr(r, 'top3_nombres', '')}"
            filas.append(dict(detector="D2", A=r.A, B=r.B, C=getattr(r, "C", ""), cifras=cif, p=r.p,
                              q=r.q_global, q_dir=r.q_dir if np.isfinite(r.q_dir) else r.q_familia,
                              familia=r.familia, nota=f"exceso={r.exceso:.2f}", enlace=""))
    for r in D3.itertuples():
        if (r.p <= 0.05):
            cif = f"nA={r.nA}; nB={r.nB}; lcs={r.lcs}; tau_nulo={r.nulo_media:.2f}"
            filas.append(dict(detector="D3", A=r.A, B=r.B, C="", cifras=cif, p=r.p, q=r.q,
                              q_dir=r.q_dir if np.isfinite(r.q_dir) else r.q_familia,
                              familia=r.familia, nota=f"exceso={r.exceso:.2f}", enlace=""))
    for r in D4.itertuples():
        if r.p <= 0.05:
            cif = f"nA={r.nA}; nB={r.nB}; grupos={r.obs}; columnas={r.columnas}; B_grupo={r.B_grupo}; tau={r.tau}"
            filas.append(dict(detector="D4", A=r.A, B=r.B, C="", cifras=cif, p=r.p, q=r.q,
                              q_dir=r.q_dir, familia=r.familia, nota="celda colgante+s1",
                              enlace=""))
    E = pd.DataFrame(filas)
    # marcar controles
    ctrl = {("D2", "UR273A", "UR273B"), ("D2", "UR273B", "UR274A"), ("D3", "UR278", "UR266"),
            ("D3", "UR278", "UR275"), ("D4", "UR270", "UR278"), ("D1", "UR267A", ""),
            ("D1", "UR275", ""), ("D1", "UR268", "")}
    E["control"] = [int((r.detector, r.A, r.B) in ctrl) for r in E.itertuples()]
    E = E.sort_values(["control", "q_dir", "p"], ascending=[False, True, True])
    E.to_csv(AQUI / "enlaces_nuevos.csv", index=False, float_format="%.4g")
    print(f"filas en enlaces_nuevos.csv: {len(E)}")
    print(E.head(40).to_string(index=False))
    print("\nResumen por detector y familia (q_dir<0.05):")
    print(E[E.q_dir < 0.05].groupby(["detector", "familia"]).size().to_string())
    print("\nPares con q_dir<0.05 fuera de Incahuasi:")
    print(E[(E.q_dir < 0.05) & (~E.familia.str.contains("Incahuasi"))].to_string(index=False))


if __name__ == "__main__":
    main()
