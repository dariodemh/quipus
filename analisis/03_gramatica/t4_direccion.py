"""Tarea 4: dirección de nudos (S/Z) y torsión de la cuerda: ¿marcadores con función o ruido?
Unidad = quipu. Colgantes (nivel 0) de quipus MIXTOS (ambas etiquetas, minoría >=3, >=10 cuerdas).
Etiquetas por cuerda (para no mezclar tipos de nudo, que tienen direcciones distintas):
  dirLE = dirección del racimo largo/ocho (unidades); dirS = dirección mayoritaria de los racimos simples;
  tor   = torsión de la cuerda.
1 = etiqueta minoritaria del quipu ("marcada").
Hipótesis y nulos (permutaciones dentro del quipu, P=2000, misma semilla; para dirLE todas las
permutaciones son además dentro del tipo de racimo de unidades, L o E, salvo 'mitad|grupos'):
  inicio        exceso de la etiqueta minoritaria en la 1.ª cuerda de cada grupo (una cola). Nulo: libre.
  bloques       menos corridas de lo esperado (etiqueta en bloques). Nulo: libre.
  grupo         I(etiqueta; grupo). Nulo: libre.
  mitad         I(etiqueta; mitad del quipu). Nulo: libre.
  mitad|grupos  ídem, pero el nulo baraja el ORDEN de los grupos (conserva la homogeneidad intragrupo):
                ¿hay oposición de mitades más allá de que los grupos sean homogéneos?
  color, union, magn       I(etiqueta; covariable). Nulo: libre.
  color|grupo, magn|grupo  ídem con nulo que permuta solo DENTRO de cada grupo: ¿la dirección sigue al
                color/magnitud de la cuerda o solo al grupo (sesión de anudado/lote)?
Agregado de corpus: suma de z por quipu con permutaciones conjuntas -> p_corpus; Holm sobre todas las
filas de la tabla; por quipu: BH.
"""
import numpy as np
import pandas as pd
from scipy import stats

import comun as C

P = 2000


def preparar(c):
    d = c[c["nivel"] == 0].copy()
    le, s_, tle = [], [], []
    for txt in d["nudos"]:
        cl = C.parse_nudos(txt)
        a = [dr for _, t, _, dr, _ in cl if t in ("L", "E", "EE", "LL") and dr in ("S", "Z")]
        b = [dr for _, t, _, dr, _ in cl if t == "S" and dr in ("S", "Z")]
        le.append(a[-1] if a else None)
        tl = [t for _, t, _, dr, _ in cl if t in ("L", "E", "EE", "LL") and dr in ("S", "Z")]
        tle.append(tl[-1] if tl else "-")
        s_.append(None if not b or b.count("S") == b.count("Z") else ("S" if b.count("S") > b.count("Z") else "Z"))
    d["dirLE"], d["dirS"], d["tipoLE"] = le, s_, tle
    d["tor"] = d["torsion"].where(d["torsion"].isin(["S", "Z"]))
    d["pos"] = d.groupby("kfg").cumcount()
    d["inicio"] = (d["grupo"] != d.groupby("kfg")["grupo"].shift()).astype(int)
    return d


def perm_dentro(lab, bloques, rng):
    L = np.tile(lab, (P + 1, 1))
    for b in np.unique(bloques):
        m = bloques == b
        if m.sum() > 1:
            L[1:, m] = rng.permuted(L[1:, m], axis=1)
    return L


def analizar(d, et, rng):
    res = []
    for k, g in d.groupby("kfg"):
        g = g[g[et].notna()]
        if len(g) < 10:
            continue
        vc = g[et].value_counts()
        if len(vc) < 2 or vc.min() < 3:
            continue
        lab = (g[et] == vc.idxmin()).to_numpy().astype(np.int64)
        n = len(lab)
        grp = C.codificar(g["grupo"].to_numpy())
        mitad = (np.arange(n) >= n / 2).astype(np.int64)
        # para dirLE se estratifica por tipo del racimo de unidades (L vs E), que tienen direcciones distintas
        est = C.codificar(g["tipoLE"].to_numpy()) if et == "dirLE" else np.zeros(n, dtype=np.int64)
        Llib = perm_dentro(lab, est, rng)
        Lgr = perm_dentro(lab, grp * (est.max() + 1) + est, rng)
        Lord = np.vstack([lab[None, :], C.barajar_grupos(lab, grp, P, rng)])
        covs = {cv: C.codificar(g[cv].fillna("U").astype(str).to_numpy())
                for cv in ("tok_color", "union_n", "magn")}
        st = {}
        ini = g["inicio"].to_numpy()
        if 0 < ini.sum() < n:
            st["inicio"] = Llib[:, ini == 1].mean(1) - Llib[:, ini == 0].mean(1)
        st["bloques"] = -(1 + (Llib[:, 1:] != Llib[:, :-1]).sum(1)).astype(float)
        if grp.max() > 0:
            st["grupo"] = C.mi_etiqueta(Llib, grp, 2, grp.max() + 1)
            st["mitad|grupos"] = C.mi_etiqueta(Lord, mitad, 2, 2)
        st["mitad"] = C.mi_etiqueta(Llib, mitad, 2, 2)
        for cv, x in covs.items():
            if x.max() > 0:
                st[cv] = C.mi_etiqueta(Llib, x, 2, x.max() + 1)
                if grp.max() > 0 and cv != "union_n":
                    st[f"{cv}|grupo"] = C.mi_etiqueta(Lgr, x, 2, x.max() + 1)
        fila = {"kfg": k, "n": n, "minoritaria": vc.idxmin(), "frac_min": lab.mean()}
        for h, s in st.items():
            if s[1:].std() < 1e-12:
                continue
            sd = s[1:].std()
            fila[f"z_{h}"] = (s[0] - s[1:].mean()) / sd
            fila[f"p_{h}"] = (1 + (s[1:] >= s[0]).sum()) / (P + 1)
            fila[f"_null_{h}"] = (s[1:] - s[1:].mean()) / sd
        res.append(fila)
    return res


def resumir(res, nombre):
    df = pd.DataFrame([{k: v for k, v in r.items() if not k.startswith("_null")} for r in res])
    filas = []
    for h in [c[2:] for c in df.columns if c.startswith("z_")]:
        rs = [r for r in res if f"_null_{h}" in r]
        T = sum(r[f"z_{h}"] for r in rs)
        Tn = np.vstack([r[f"_null_{h}"] for r in rs]).sum(0)
        pq = df[f"p_{h}"].dropna().to_numpy()
        filas.append({"etiqueta": nombre, "hipotesis": h, "quipus": len(rs), "Z_suma": T,
                      "p_corpus": (1 + (Tn >= T).sum()) / (P + 1),
                      "quipus_q<0.05": int((C.bh(pq) < 0.05).sum()),
                      "frac_p<0.05": float((pq < 0.05).mean())})
    df.to_csv(C.RES / f"t4_por_quipu_{nombre}.csv", index=False)
    return pd.DataFrame(filas)


def main():
    rng = np.random.default_rng(C.SEMILLA + 4)
    c, q = C.cargar()
    d = preparar(c)
    lin = []
    for et in ("dirLE", "dirS", "tor"):
        x = d[d[et].notna()]
        cnt = x.groupby("kfg").size()
        mn = x.groupby("kfg")[et].agg(lambda s: s.value_counts(normalize=True).min() if s.nunique() > 1 else 0.0)
        mn = mn[cnt >= 10]
        lin.append(f"{et}: quipus con >=10 cuerdas etiquetadas={len(mn)}; uniformes={(mn == 0).mean():.1%}; "
                   f"minoría >=10%={(mn >= .1).mean():.1%}; S global={(x[et] == 'S').mean():.1%}")
    # contraste de tipos de nudo, unidad = quipu
    both = d.dropna(subset=["dirLE", "dirS"])
    pq = both.groupby("kfg").agg(n=("dirLE", "size"), le=("dirLE", lambda s: (s == "S").mean()),
                                 s=("dirS", lambda s: (s == "S").mean()))
    pq = pq[pq.n >= 5]
    dif = pq["le"] - pq["s"]
    w = stats.wilcoxon(dif[dif != 0])
    lin.append(f"misma cuerda, P(S) del largo/ocho menos P(S) de los simples, por quipu (n={len(pq)}): "
               f"media={dif.mean():.3f}; LE más S en {int((dif > 0).sum())}, menos en {int((dif < 0).sum())}; "
               f"Wilcoxon p={w.pvalue:.2e}; cuerdas con LE y S en direcciones distintas="
               f"{(both.dirLE != both.dirS).mean():.1%}")
    # ¿dirección determinada por la torsión? (física del anudado) — quipus con torsión mixta y dirección
    tz = d.dropna(subset=["dirLE", "tor"])
    ct = pd.crosstab(tz["tor"], tz["dirLE"])
    lin.append(f"torsión x dirección del largo/ocho (todas las cuerdas; descriptivo):\n{ct}")
    out = pd.concat([resumir(analizar(d, et, rng), et) for et in ("dirLE", "dirS", "tor")])
    out["p_holm"] = C.holm(out["p_corpus"].to_numpy())
    out.to_csv(C.RES / "t4_hipotesis.csv", index=False)
    txt = "\n".join(lin) + "\n\n" + out.round(4).to_string(index=False)
    (C.RES / "t4_resumen.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
