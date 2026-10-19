"""Tarea 1 (b): ¿dónde caen los quipus? Clasificador entrenado SOLO con secuencias de referencia
(texto silabeado/letras, tabla sintética, bandeado sintético, azar = quipu barajado), con rasgos que no
dependen del vocabulario, y aplicado a los quipus reales en cada nivel de token.
Requiere resultados/t1_metricas.csv (t1_entropia.py). Salidas: t1b_clasificacion.csv, t1b_resumen.txt
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import comun as C
from t1_entropia import NIVELES, metricas

# principal: sin auto-repetición (inestable cuando V ~ n: el texto casi nunca repite token contiguo y un quipu
# con vocabulario enorme tampoco, por puro tamaño de vocabulario). Sensibilidad: con auto-repetición y Heaps.
RASGOS_SENS = ["D1_a", "D2_a", "Iexc1_rel", "Iexcmax_rel", "log_auto_rep", "heaps_ratio", "frac_z1"]
RASGOS = ["D1_a", "D2_a", "Iexc1_rel", "Iexcmax_rel", "frac_z1"]


def rasgos(df):
    df = df.copy()
    df["log_auto_rep"] = np.log(df["auto_rep"].clip(lower=0.05))
    # parte de la estructura secuencial que está en el desfase 1 (texto/bandeado) frente a desfases >1
    a, b = df["z1"].clip(lower=0), df["zmax_d>1"].clip(lower=0)
    df["frac_z1"] = np.where(a + b > 0, a / (a + b + 1e-9), 0.5)
    return df


def main():
    rng = np.random.default_rng(C.SEMILLA + 11)
    m = pd.read_csv(C.RES / "t1_metricas.csv")
    c, _ = C.cargar()
    # referencia adicional: bandeado sintético (corridas de longitud geométrica, media 4), mismas longitudes
    # y frecuencias de color que cada quipu
    ban = []
    for k, (tok, grp) in C.secuencias(c, "tok_color", 10).items():
        _, frec = np.unique(tok, return_counts=True)
        n = len(tok)
        x = np.repeat(rng.choice(len(frec), size=n, p=frec / frec.sum()), rng.geometric(0.25, size=n))[:n]
        if len(np.unique(x)) > 1:
            ban.append({"doc": f"banda_{k}", "clase": "bandeado", "nivel": "color", **metricas(x, grp, rng)})
    m = pd.concat([m, pd.DataFrame(ban)], ignore_index=True)
    m = rasgos(m).dropna(subset=RASGOS_SENS)
    m["clase_ref"] = m["clase"].str.replace(r"texto_.*", "texto", regex=True)
    ref = m[m["clase_ref"] != "quipu"]
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
    cv = cross_val_score(clf, ref[RASGOS], ref["clase_ref"], cv=5)
    clf.fit(ref[RASGOS], ref["clase_ref"])
    lin = [f"referencias: {ref['clase_ref'].value_counts().to_dict()}; exactitud CV-5 = {cv.mean():.3f}"]
    qu = m[m["clase_ref"] == "quipu"].copy()
    pr = pd.DataFrame(clf.predict_proba(qu[RASGOS]), columns=[f"P_{c}" for c in clf.classes_], index=qu.index)
    qu = qu.join(pr)
    qu["pred"] = clf.predict(qu[RASGOS])
    qu[["doc", "nivel", "n", "V", "pred"] + list(pr.columns) + RASGOS].to_csv(C.RES / "t1b_clasificacion.csv",
                                                                               index=False)
    for nv in NIVELES:
        d = qu[qu["nivel"] == nv]
        lin.append(f"[{nv}] quipus={len(d)}: " + ", ".join(f"{k}={v:.1%}" for k, v in
                                                          d["pred"].value_counts(normalize=True).items()))
        for n0 in (30, 100):
            dd = d[d["n"] >= n0]
            lin.append(f"     n>={n0} ({len(dd)}): " + ", ".join(f"{k}={v:.1%}" for k, v in
                                                               dd["pred"].value_counts(normalize=True).items()))
    clf2 = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(ref[RASGOS_SENS], ref["clase_ref"])
    qu["pred_sens"] = clf2.predict(qu[RASGOS_SENS])
    for nv in NIVELES:
        d = qu[qu["nivel"] == nv]
        lin.append(f"[sensibilidad con auto-repetición y Heaps, {nv}]: " + ", ".join(
            f"{k}={v:.1%}" for k, v in d["pred_sens"].value_counts(normalize=True).items()))
    med = m.groupby(["clase_ref", "nivel"])[RASGOS_SENS + ["H0_norm", "zipf", "heaps_beta"]].median().round(3)
    lin.append("medianas de rasgos por clase y nivel:\n" + med.to_string())
    # probabilidad de texto: los quipus más 'textuales' por este criterio (nivel patrón y tupla)
    top = qu[qu["nivel"].isin(["patron", "tupla"])].sort_values("P_texto", ascending=False)
    lin.append("quipus con mayor P(texto):\n" + top.head(20)[["doc", "nivel", "n", "P_texto", "P_tabla", "P_bandeado",
                                                           "P_azar"]].round(3).to_string(index=False))
    txt = "\n".join(lin)
    (C.RES / "t1b_resumen.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
