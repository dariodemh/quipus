"""Tarea 5: los quipus que más se apartan del comportamiento tabular/numérico.
Puntuación de "textualidad" (rango percentil medio, solo quipus con >=30 colgantes y >=50 % anudados):
  + fracción de cuerdas anudadas no conformes con la notación decimal (anom_dec)
  + fracción de la dependencia secuencial que está en el desfase 1 y no en desfases >1 (tokens de patrón; t1)
  - auto-repetición (bandeado) del color (t1)
  - tamaño del efecto de columnas (t2, máximo de color/magnitud, periodo implícito o grupos)
  - relaciones de suma de Ascher por cuerda (KFG)
  + riqueza de patrones (V/n de patrón de nudos)
Puntuación final = residuo respecto de log(n) (la versión bruta favorecía quipus pequeños).
Controles de daño/transcripción: fracción de cuerdas rotas (terminación B), fracción de rasgos
desconocidos (U), nº de colgantes; correlación de Spearman entre puntuación y daño.
Además: prueba directa del "canal silábico" (Sivan 2026) en cuerdas con >=2 racimos largo/ocho:
¿el orden de los racimos dentro de la cuerda importa (como el de las sílabas en una palabra)?
Salidas: resultados/t5_puntuacion.csv, t5_top20.csv, t5_resumen.txt
"""

import numpy as np
import pandas as pd
from scipy import stats

import comun as C

KFG = C.RAIZ / "data" / "external" / "data-science-khipu-article" / "data"


def sumas():
    a = pd.read_csv(KFG / "ascher_sum_relations" / "ascher_sum_relationships.csv")
    a["kfg"] = a["name"].str.extract(r">([^<]+)<")[0]
    cols = [c for c in a.columns if c.startswith("num_") and c not in ("num_banded_clusters",
                                                                         "num_seriated_clusters")]
    a["sumas"] = a[cols].fillna(0).sum(1)
    return a.set_index("kfg")[["sumas"]]


def pos_rank(s, asc=True):
    return s.rank(pct=True, ascending=asc)


def _v(tok):
    """nº de vueltas de un token 'L3' / 'EE1'."""
    return int(tok.lstrip("ELU"))


def canal_silabico(c, rng, P=2000):
    """Cuerdas con >=2 racimos L/E: secuencia de 'sílabas' = tipo+vueltas de cada racimo L/E, arriba->abajo.
    Estadístico: I(token; posición en la cuerda) (inicio/medio/final). Nulo: barajar el orden de los
    racimos dentro de cada cuerda (conserva la composición de cada 'palabra').
    Referencia: el mismo estadístico en palabras quechuas (sílabas) con barajado dentro de palabra."""
    pal = []
    for kfg, s in c[["kfg", "nudos"]].dropna().itertuples(index=False):
        cl = [f"{t}{n}" for n, t, _, _, _ in C.parse_nudos(s) if t in ("L", "E", "EE", "LL")]
        if len(cl) >= 2:
            pal.append((kfg, cl))
    tt, tg = C.texto_referencia("Quechua")
    qpal = [list(tt[tg == g]) for g in np.unique(tg)]
    qpal = [p for p in qpal if len(p) >= 2]

    def prueba(palabras):
        toks = np.concatenate([np.array(p) for p in palabras])
        x = C.codificar(toks)
        lens = np.array([len(p) for p in palabras])
        posl = np.concatenate([np.r_[0, np.ones(L - 2, int), 2] for L in lens])  # inicio/medio/final
        V = int(x.max()) + 1
        obs = C.mi_etiqueta(x[None, :], posl, V, 3)[0]
        cortes = np.cumsum(lens)[:-1]
        nul = np.empty(P)
        for i in range(P):
            xs = np.concatenate([rng.permutation(b) for b in np.split(x, cortes)])
            nul[i] = C.mi_etiqueta(xs[None, :], posl, V, 3)[0]
        H0 = C.entropia(x)
        return {"palabras": len(palabras), "tokens": len(x), "V": V, "MI_pos": obs,
                "MI_pos_nulo": nul.mean(), "exceso_rel": (obs - nul.mean()) / H0,
                "p": (1 + (nul >= obs).sum()) / (P + 1)}

    r_q = prueba([p for _, p in pal])
    r_t = prueba(qpal)
    # ¿son las 'palabras' de nudos reutilizadas como léxico? tipos/ocurrencias y Zipf
    w = pd.Series([" ".join(p) for _, p in pal])
    wq = pd.Series([" ".join(p) for p in qpal])
    lex = {"quipu_tipos/ocurr": w.nunique() / len(w), "quechua_tipos/ocurr": wq.nunique() / len(wq),
           "quipu_zipf": C.zipf_exponente(w.to_numpy()), "quechua_zipf": C.zipf_exponente(wq.to_numpy()),
           "quipu_monotona_desc": float(np.mean([all(_v(a) >= _v(b) for a, b in zip(p, p[1:]))
                                                  for _, p in pal])),
           "quipus_con_string": len({k for k, _ in pal})}
    # monotonía esperada si se barajan los racimos de cada cuerda
    mono_nul = np.mean([np.mean([all(_v(a) >= _v(b) for a, b in zip(q_, q_[1:]))
                                 for q_ in (rng.permutation(p) for _, p in pal)]) for _ in range(50)])
    lex["quipu_monotona_desc_nulo"] = float(mono_nul)
    return r_q, r_t, lex


def main():
    rng = np.random.default_rng(C.SEMILLA + 5)
    c, q = C.cargar()
    p0 = c[c["nivel"] == 0]
    base = p0.groupby("kfg").agg(n=("orden", "size"), frac_anudada=("anudada", "mean"),
                                 frac_rota=("rota", "mean"),
                                 frac_torU=("torsion", lambda s: (s == "U").mean()),
                                 frac_unionU=("union_n", lambda s: (s == "U").mean()),
                                 V_patron=("tok_patron", "nunique"))
    an = c[c["anudada"]].groupby("kfg").agg(frac_anom=("anom_dec", "mean"), n_anom=("anom_dec", "sum"))
    dirs = c.groupby("kfg").apply(lambda g: (g["nudos"].fillna("").str.count(r",U\)")).sum()
                                  / max(1, g["n_racimos"].sum()), include_groups=False).rename("frac_dirU")
    t1 = pd.read_csv(C.RES / "t1_metricas.csv")
    t1q = t1[t1["clase"] == "quipu"]
    pat = t1q[t1q["nivel"] == "patron"].set_index("doc")
    col = t1q[t1q["nivel"] == "color"].set_index("doc")
    a_, b_ = pat["z1"].clip(lower=0), pat["zmax_d>1"].clip(lower=0)
    seq = pd.DataFrame({"lag1_no_periodico": np.where(a_ + b_ > 0, a_ / (a_ + b_ + 1e-9), 0.5),
                        "auto_rep_color": col["auto_rep"], "z1_patron": pat["z1"]}, index=pat.index)
    t2 = pd.read_csv(C.RES / "t2_por_quipu.csv")
    t2 = t2[t2["clase"] == "quipu"]
    # tamaño del efecto de columnas (no su p, que depende de n): máximo entre color/magnitud y pruebas
    t2["efecto"] = t2[["exc_col", "g_exc"]].max(axis=1)
    tab = t2.groupby("kfg")["efecto"].max().rename("tabular_efecto")
    df = base.join([an, dirs, seq, tab, sumas()], how="left")
    df["sumas_por_cuerda"] = df["sumas"].fillna(0) / df["n"]
    df["riqueza_patron"] = df["V_patron"] / df["n"]
    df["frac_anom"] = df["frac_anom"].fillna(0)
    df = df.join(q.set_index("kfg")[["sitio", "procedencia", "museo"]])
    el = df[(df["n"] >= 30) & (df["frac_anudada"] >= 0.5)].dropna(subset=["lag1_no_periodico", "tabular_efecto"])
    comp = pd.DataFrame({
        "r_anom": pos_rank(el["frac_anom"]),
        "r_seq": pos_rank(el["lag1_no_periodico"]),
        "r_noband": pos_rank(el["auto_rep_color"], asc=False),
        "r_notab": pos_rank(el["tabular_efecto"], asc=False),
        "r_nosum": pos_rank(el["sumas_por_cuerda"], asc=False),
        "r_riq": pos_rank(el["riqueza_patron"]),
    })
    el = el.join(comp)
    el["textualidad_bruta"] = comp.mean(1)
    # quitar la dependencia residual del tamaño: residuo de la regresión sobre log(n)
    b = np.polyfit(np.log(el["n"]), el["textualidad_bruta"], 1)
    el["textualidad"] = el["textualidad_bruta"] - np.polyval(b, np.log(el["n"]))
    el = el.sort_values("textualidad", ascending=False)
    el.to_csv(C.RES / "t5_puntuacion.csv")
    lin = [f"quipus puntuados: {len(el)}"]
    for dmg in ("frac_rota", "frac_torU", "frac_unionU", "frac_dirU", "n"):
        r = stats.spearmanr(el["textualidad"], el[dmg], nan_policy="omit")
        lin.append(f"Spearman(textualidad, {dmg}) = {r.statistic:.3f} (p={r.pvalue:.2g})")
    top = el.head(20).copy()
    p75 = el["frac_rota"].quantile(.75)
    top["alerta_dano"] = np.where(top["frac_rota"] > p75, "rotas>P75", "")
    top["alerta_dano"] += np.where(top["frac_dirU"] > 0.5, " dirU>50%", "")
    cols = ["n", "sitio", "textualidad", "frac_anom", "lag1_no_periodico", "auto_rep_color", "tabular_efecto",
            "sumas_por_cuerda", "riqueza_patron", "frac_rota", "frac_dirU", "alerta_dano"]
    top[cols].round(3).to_csv(C.RES / "t5_top20.csv")
    lin.append(f"P75 de cuerdas rotas en el corpus puntuado: {p75:.3f}")
    lin.append(top[cols].round(3).to_string())
    # ¿la textualidad es solo 'anomalía decimal'? correlación entre componentes
    lin.append("correlaciones de Spearman entre componentes:\n" + comp.corr("spearman").round(2).to_string())
    r_q, r_t, lex = canal_silabico(c, rng)
    lin.append(f"canal silábico, cuerdas con >=2 largos/ocho: {r_q}")
    lin.append(f"referencia quechua (palabras >=2 sílabas): {r_t}")
    lin.append(f"léxico: {lex}")
    txt = "\n".join(str(x) for x in lin)
    (C.RES / "t5_resumen.txt").write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
