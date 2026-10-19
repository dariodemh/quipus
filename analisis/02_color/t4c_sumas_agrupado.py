"""Tarea 4 (sumas): pocas sumas por quipu (<8 quipus por prueba), asi que se hace una prueba estratificada por quipu:
T = numero de cuerdas 'suma' con atributo de color; nulo = permutar el atributo DENTRO de cada quipu (entre candidatos);
p empirico, B=2000; nulos Nq (permuta dentro del quipu) y Nv (permuta dentro de terciles de valor dentro del quipu), semilla fija. No sustituye al analisis por quipu: el resultado depende de pocos quipus (se informa cuantos).
Tambien valida la deteccion de sumas contra las relaciones de suma de Ascher calculadas por el KFG."""
import numpy as np, pandas as pd
import comun as m
from t4_especiales import banderas_suma

B = 2000
c, q = m.cargar(); rng = np.random.default_rng([m.SEED, 8])
glob = c.ckey.value_counts(normalize=True)
strata = {"colgante_suma_de_subs": [], "borde_de_grupo_suma_del_resto": []}
for kfg, d in c.groupby("kfg"):
    d = d.sort_values("orden").reset_index(drop=True)
    F = banderas_suma(d, rng, bs=1)
    ok = d.ckey.notna().values
    if ok.sum() < 5: continue
    nat = (d.nd == "nat").values
    att = {"blanca": (d.ckey == "W").values, "mixta": (d.ctipo.fillna("simple") != "simple").values,
           "rara_global": (d.ckey.map(glob).fillna(1) < .005).values, "tinte": (d.nd == "tinte").values}
    for nm, pop, sp in (("colgante_suma_de_subs", F["cand"], F["sp"]), ("borde_de_grupo_suma_del_resto", F["first"] | F["last"], F["edge"])):
        pm = pop & ok
        if sp[pm].sum() >= 1 and (~sp[pm]).sum() >= 1:
            vv = d.val.values[pm]; vb = np.full(pm.sum(), -1); ii = np.where(~np.isnan(vv))[0]
            if len(ii) >= 3: vb[ii] = (3 * (pd.Series(vv[ii]).rank(method="first").values - 1) / len(ii)).astype(int)
            strata[nm].append(dict(kfg=kfg, sp=sp[pm], nat=nat[pm], vb=vb, **{k: v[pm] for k, v in att.items()}))
rows = []
for nm, L in strata.items():
    for an in ("blanca", "mixta", "rara_global", "tinte"):
        for fondo in ("todos", "natural"):
            if an == "tinte" and fondo == "natural": continue
            for nulo in ("Nq", "Nv"):
                S = []
                for s in L:
                    k = s["nat"] if fondo == "natural" else np.ones(len(s["sp"]), bool)
                    sp = s["sp"][k]; a = s[an][k].astype(float); vb = s["vb"][k]
                    if sp.sum() >= 1 and (~sp).sum() >= 1: S.append((sp, a, vb))
                if not S: continue
                T = sum(a[sp].sum() for sp, a, vb in S); N = sum(sp.sum() for sp, a, vb in S)
                def una(sp, a, vb):
                    if nulo == "Nq": return a[rng.permutation(len(a))][sp].sum()
                    ap = a.copy()
                    for g in np.unique(vb):
                        ix = np.where(vb == g)[0]; ap[ix] = a[rng.permutation(ix)]
                    return ap[sp].sum()
                nul = np.zeros(B)
                for b in range(B):
                    nul[b] = sum(una(sp, a, vb) for sp, a, vb in S)
                exp = nul.mean()
                p = min(1, 2 * min((1 + (nul >= T).sum()) / (B + 1), (1 + (nul <= T).sum()) / (B + 1)))
                rows.append(dict(especial=nm, atributo=an, fondo=fondo, nulo=nulo, n_quipus=len(S), n_sumas=int(N), con_atributo=T, esperado_azar=exp, prop_obs=T / N, prop_esp=exp / N, p_perm=p))
R = pd.DataFrame(rows); R["q_bh"] = m.bh(R.p_perm.values); R.to_csv(m.OUT + "/resultados_t4_sumas_agrupado.csv", index=False)
pd.set_option("display.width", 250); print(R.round(4).to_string())
# validacion contra KFG
S = pd.read_csv(m.OUT + "/resultados_t4_sumas_quipu.csv")
a = pd.read_csv(m.RAIZ + r"\data\external\data-science-khipu-article\data\ascher_sum_relations\ascher_sum_relationships.csv")
a["kfg"] = a.name.str.extract(r">([A-Z]+\d+)<")[0]
X = S.merge(a[["kfg", "num_subsidiary_pendant_sum", "num_pendant_pendant_sum"]], on="kfg")
print("quipus emparejados:", len(X), "| con suma colgante=subs (mia):", (X.n_sp > 0).sum(), "| KFG num_subsidiary_pendant_sum>0:", (X.num_subsidiary_pendant_sum > 0).sum(),
      "| ambos:", ((X.n_sp > 0) & (X.num_subsidiary_pendant_sum > 0)).sum())
print("KFG pendant_pendant_sum>0:", (X.num_pendant_pendant_sum > 0).sum(), "| mi borde-suma>0:", (X.n_edge > 0).sum(), "| ambos:", ((X.n_edge > 0) & (X.num_pendant_pendant_sum > 0)).sum())
