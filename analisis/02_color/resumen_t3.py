"""Resumen de T3: un color/resultado es 'robusto' si sobrevive BH<0.05 en los tres nulos (Nq, Ng, Nc),
con el mismo signo en los tres y prueba de signo entre quipus p<0.05. Salida: resultados_t3_robustos.csv"""
import pandas as pd
import comun as m

pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 140)
M = pd.read_csv(m.OUT + "/resultados_t3_meta.csv")
k = ["clase", "outcome", "color", "fondo"]
w = M.pivot_table(index=k, columns="nulo", values=["q_bh", "z_stouffer"])
w.columns = [a + "_" + b for a, b in w.columns]
b = M[M.nulo == "Nq"].set_index(k)[["n", "eff_med", "frac_pos", "p_signo", "frac_p05", "por_coleccion"]]
t = b.join(w)
zs = t[["z_stouffer_Nq", "z_stouffer_Ng", "z_stouffer_Nc"]]
mismo = (zs > 0).all(axis=1) | (zs < 0).all(axis=1)
t["robusto"] = (t.q_bh_Nq < .05) & (t.q_bh_Ng < .05) & (t.q_bh_Nc < .05) & (t.p_signo < .05) & mismo
t.round(4).to_csv(m.OUT + "/resultados_t3_robustos.csv")
if __name__ == "__main__":
    print("robustos:", t.robusto.sum(), "de", len(t))
    cols = ["n", "eff_med", "frac_pos", "p_signo", "z_stouffer_Nq", "z_stouffer_Ng", "z_stouffer_Nc", "por_coleccion"]
    print(t[t.robusto].sort_values("z_stouffer_Ng", key=abs, ascending=False)[cols].round(3).to_string())
    print("NO robustos con q<.05 en algun nulo:")
    print(t[~t.robusto & ((t.q_bh_Nq < .05) | (t.q_bh_Ng < .05) | (t.q_bh_Nc < .05))][cols[:4] + ["q_bh_Nq", "q_bh_Ng", "q_bh_Nc"]].round(3).to_string())
