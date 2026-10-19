"""Localización del hueco de un cero: banda del mismo exponente en el quipu y en el grupo."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import pandas as pd
from explorar import load


def main():
    d = load()
    rows = []
    for (k, g), gg in d[(d.nivel == 0) & (d.nap >= 2)].groupby(["kfg", "grupo"]):
        cords = {}
        for _, r in gg.iterrows():
            es = [e for e, v, p in r.ap]
            if len(es) != len(set(es)):
                continue
            cords[r.cuerda] = sorted(r.ap, key=lambda t: t[2])
        if len(cords) < 2:
            continue
        # posiciones por exponente en el grupo (otras cuerdas)
        for c, a in cords.items():
            es = [e for e, v, p in a]
            for i in range(len(es) - 1):
                ehi, elo = es[i], es[i + 1]
                for em in range(elo + 1, ehi):
                    phat = a[i][2] + (a[i + 1][2] - a[i][2]) * (ehi - em) / (ehi - elo)
                    pos_g = [x[2] for c2, a2 in cords.items() if c2 != c
                             for x in a2 if x[0] == em]
                    if pos_g:
                        rows.append(dict(kfg=k, grupo=g, cuerda=c, em=em,
                                         phat=phat, med_g=float(np.median(pos_g)),
                                         n=len(pos_g)))
    Z = pd.DataFrame(rows)
    Z["d"] = (Z.phat - Z.med_g).abs()
    Z.to_csv(os.path.join(os.path.dirname(__file__), "ceros_grupo.csv"), index=False)
    print("huecos con banda en su grupo", len(Z), "quipus", Z.kfg.nunique(),
          "grupos", Z.groupby(["kfg", "grupo"]).ngroups)
    print(Z.d.describe(percentiles=[.5, .75, .9]).round(2).to_string())
    print("d<=1", (Z.d <= 1).mean(), "d<=1.5", (Z.d <= 1.5).mean())

    # distancia a la banda del quipu completo (solo para comparar)
    rows2 = []
    for k, gg in d[(d.nivel == 0) & (d.nap >= 2)].groupby("kfg"):
        cords = {}
        for _, r in gg.iterrows():
            es = [e for e, v, p in r.ap]
            if len(es) != len(set(es)):
                continue
            cords[r.cuerda] = sorted(r.ap, key=lambda t: t[2])
        if len(cords) < 2:
            continue
        allpos = {}
        for c, a in cords.items():
            for e, v, p in a:
                allpos.setdefault(e, []).append((c, p))
        for c, a in cords.items():
            es = [e for e, v, p in a]
            for i in range(len(es) - 1):
                ehi, elo = es[i], es[i + 1]
                for em in range(elo + 1, ehi):
                    phat = a[i][2] + (a[i + 1][2] - a[i][2]) * (ehi - em) / (ehi - elo)
                    pos = [p for c2, p in allpos.get(em, []) if c2 != c]
                    if len(pos) >= 1:
                        rows2.append(dict(kfg=k, cuerda=c, em=em, phat=phat,
                                          med_q=float(np.median(pos))))
    Q = pd.DataFrame(rows2)
    Q["d_q"] = (Q.phat - Q.med_q).abs()
    Q.to_csv(os.path.join(os.path.dirname(__file__), "ceros_localizacion.csv"), index=False)
    print("huecos con banda en el quipu", len(Q), "d mediana", round(Q.d_q.median(), 2),
          "<=1", round((Q.d_q <= 1).mean(), 3))


if __name__ == "__main__":
    main()
