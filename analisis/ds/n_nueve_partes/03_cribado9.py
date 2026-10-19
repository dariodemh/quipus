"""Cribado de grupos de exactamente 9 cuerdas en todo el corpus y
comprobacion de los totales UR278 -> UR266/UR275.
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(r"./analisis")
sys.path.insert(0, str(RAIZ / "ds" / "n_que_se_contaba"))
from comun import cargar  # noqa: E402

OUT = RAIZ / "ds" / "n_nueve_partes"


def main():
    c = cargar()
    base = c[(c.nivel == 0)]
    filas = []
    for k, q in base.groupby("kfg"):
        for g, s in q.groupby("grupo"):
            v = s.sort_values("orden").v.dropna().values
            if len(v) == 9:
                cv = v.std(ddof=1) / v.mean() if v.mean() > 0 else np.nan
                filas.append(dict(kfg=k, grupo=g, total=v.sum(), cv=cv,
                                  maxmin=v.max() / v.min() if v.min() > 0 else np.nan))
    F = pd.DataFrame(filas)
    F.to_csv(OUT / "grupos9_corpus.csv", index=False)
    print(f"Grupos de exactamente 9 cuerdas presentes: {len(F)} en {F.kfg.nunique()} quipus")
    porq = F.groupby("kfg").agg(n=("grupo", "size"), cv=("cv", "mean"),
                                tot=("total", "sum")).sort_values("cv")
    print("\nQuipus con >=2 grupos de 9 (ordenados por CV medio):")
    print(porq[porq.n >= 2].head(15).to_string())
    print(f"\nUR278: {int((F.kfg=='UR278').sum())} grupos de 9; CV medio "
          f"{F[F.kfg=='UR278'].cv.mean():.3f}")
    print(f"Percentil de UR278 entre todos los grupos de 9: "
          f"{100*(F.cv < F[F.kfg=='UR278'].cv.mean()).mean():.0f}%")
    # control por magnitud: solo grupos con total > 500 y > 1000
    for umbral in [100, 500, 1000]:
        sub = F[F.total > umbral]
        u = F[(F.kfg == "UR278") & (F.total > umbral)].cv.mean()
        print(f"   grupos de 9 con total > {umbral}: n={len(sub)}; "
              f"CV mediana {sub.cv.median():.3f}; UR278 CV {u:.3f}; "
              f"percentil {100*(sub.cv < u).mean():.0f}%")
    # cuantos grupos de 9 tienen CV < 0.20 y total > 500
    print(f"Grupos de 9 con CV < 0.20 y total > 500: "
          f"{int(((F.cv < 0.20) & (F.total > 500)).sum())} de {len(F)}")
    print("  quipus:", F[(F.cv < 0.20) & (F.total > 500)].kfg.value_counts().to_dict())

    # prueba a nivel de quipu: 24 grupos de UR278 frente a 24 grupos al azar
    rng = np.random.default_rng(20261018)
    obs = F[F.kfg == "UR278"].cv.mean()
    n = int((F.kfg == "UR278").sum())
    null = np.array([rng.choice(F.cv.values, n, replace=False).mean()
                     for _ in range(20000)])
    print(f"   nulo a nivel de quipu (24 grupos al azar de 238): CV medio "
          f"{null.mean():.3f} [{np.percentile(null,2.5):.3f};"
          f"{np.percentile(null,97.5):.3f}]; observado {obs:.3f}; "
          f"p={((null<=obs).sum()+1)/20001:.4f}")
    # nulo emparejado por magnitud: grupos con total 1000-5000
    sub = F[(F.total >= 1000) & (F.total <= 5000)]
    obs2 = F[(F.kfg == "UR278") & (F.total >= 1000) & (F.total <= 5000)].cv.mean()
    n2 = int(((F.kfg == "UR278") & (F.total >= 1000) & (F.total <= 5000)).sum())
    null2 = np.array([rng.choice(sub.cv.values, n2, replace=False).mean()
                      for _ in range(20000)])
    print(f"   nulo emparejado por magnitud (total 1000-5000, n={len(sub)}): "
          f"CV medio {null2.mean():.3f}; observado {obs2:.3f} (n={n2}); "
          f"p={((null2<=obs2).sum()+1)/20001:.4f}")
    # cuantos grupos de 9 tienen CV < 0.20
    print(f"Grupos de 9 con CV < 0.20: {int((F.cv < 0.20).sum())} de {len(F)} "
          f"({100*(F.cv<0.20).mean():.0f}%)")
    print("Quipus de esos grupos:", F[F.cv < 0.20].kfg.value_counts().head(10).to_dict())

    # UR278 -> UR266/UR275: comparar totales de fila con cabeceras
    print("\n== Totales de UR278 y cabeceras de UR266/UR275")
    V = {}
    for k in ["UR278", "UR266", "UR275"]:
        q = c[(c.kfg == k) & (c.nivel == 0)]
        V[k] = q.groupby("grupo").apply(lambda s: np.nansum(s.v), include_groups=False)
    t278 = sorted(V["UR278"].values)
    for k in ["UR266", "UR275"]:
        # las cabeceras son la primera cuerda de cada grupo
        q = c[(c.kfg == k) & (c.nivel == 0)].sort_values(["grupo", "orden"])
        cab = q.groupby("grupo").first().v.dropna().values
        cab = np.sort(cab)
        matches = 0
        for x in cab:
            if np.any(np.abs(t278 - x) <= 1):
                matches += 1
        print(f"   {k}: {len(cab)} cabeceras; {matches} coinciden (+-1) con algun "
              f"total de grupo de UR278; rango {cab.min():.0f}-{cab.max():.0f}")
    print(f"   UR278: {len(t278)} grupos; total {np.nansum(t278):.0f}; "
          f"mediana {np.median(t278):.0f}; rango {np.min(t278):.0f}-{np.max(t278):.0f}")


if __name__ == "__main__":
    main()
