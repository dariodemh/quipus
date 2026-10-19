"""Tarea 5: catalogo de quipus con anomalias 'estructuradas'.
Familias (a nivel de cuerda con nudos): inf (L/E con racimo debajo; incluye series L/E), banda (fuera de banda), L10 (L>=10 vueltas),
tiporaro (EE,LL,BL,SP,TF,U), raras (>9 simples, L1, E multiple, S no n*10^k, valor!=suma).
Para cada (quipu, familia) con >=5 cuerdas anomalas y >=10 con nudos, 3 estadisticos con nulo = permutar la etiqueta anomala entre las cuerdas con nudos del mismo quipu:
  contiguidad (pares anomalos adyacentes en el orden del quipu), concentracion en grupos de colgantes (suma de cuadrados de cuotas por grupo),
  concentracion de color (cuota del color modal). La firma (secuencia de tipos) se reporta solo descriptivamente (con 'lift' frente al resto del quipu):
  usarla como estadistico seria circular porque varias familias se definen por la secuencia de tipos. Combinacion Westfall-Young (min-p) por prueba; BH sobre todas las pruebas.
Si >80% de las cuerdas con nudos son anomalas, la familia es 'sistematica' (convencion de todo el quipu; no se puede permutar).
"""
import numpy as np, pandas as pd
from util import *

rng = np.random.default_rng(SEED)
cf = pd.read_csv(AQUI / "cuerdas_flags2.csv", keep_default_na=False, low_memory=False)
c = pd.read_csv(AQUI / "racimos.csv", keep_default_na=False)
qm = pd.read_csv(AQUI.parents[0] / "datos/quipus.csv", keep_default_na=False).set_index("kfg")
for x in cf.columns:
    if x.startswith("v_") or x in ("nether", "dir_mixta", "con_nudos", "roto", "nota_dano"): cf[x] = cf[x].astype(bool)
k = cf[cf.con_nudos].copy()
k["i"] = k.index
k["grp"] = pd.read_csv(AQUI.parents[0] / "datos/cuerdas.csv", keep_default_na=False, low_memory=False).grupo.reindex(k.index).astype(str).values
k["sig"] = c.sort_values(["i", "j"]).groupby("i").tipo.apply("-".join).reindex(k.index).fillna("")
k["col"] = k.color.str.extract(r"^([A-Za-z]+)")[0].fillna("")
k["raras"] = k[["v_over9", "v_L1", "v_Emulti", "v_Spot", "v_valor_dist"]].any(axis=1)
FAM = {"inf": k.nether | k.v_serie_LE, "banda": k.v_banda, "L10": k.v_L10, "tiporaro": k.v_tiporaro, "raras": k.raras}
k = k.sort_values(["kfg", "orden"])
FAM = {f: v.reindex(k.index).values for f, v in FAM.items()}
B = 999

def modal_share(codes, mask, nmax):
    return np.bincount(codes[mask], minlength=nmax).max() / mask.sum()
def conc(codes, mask, nmax):
    p_ = np.bincount(codes[mask], minlength=nmax) / mask.sum(); return (p_ ** 2).sum()

rows = []
for kf, g in k.groupby("kfg"):
    if len(g) < 10: continue
    pos = k.index.get_indexer(g.index)
    sg = pd.factorize(g.grp)[0]; cl = pd.factorize(g.col)[0]; ns, nc = sg.max() + 1, cl.max() + 1
    for f, arr in FAM.items():
        a = arr[pos]; na = int(a.sum())
        if na < 5: continue
        base = dict(kfg=kf, familia=f, n_con_nudos=len(g), n_anom=na, frac=na / len(g))
        sigs = g.sig[a].value_counts(); cols = g.col[a].value_counts()
        resto = g.sig[~a]; base.update(firma_modal=sigs.index[0], cuota_firma=sigs.iloc[0] / na, cuota_firma_resto=(resto == sigs.index[0]).mean() if len(resto) else np.nan, color_modal=cols.index[0], cuota_color=cols.iloc[0] / na)
        if na / len(g) > .8:
            base.update(sistematica=True, p=np.nan); rows.append(base); continue
        def stats_(m):
            return (np.sum(m[1:] & m[:-1]), conc(sg, m, ns), modal_share(cl, m, nc))
        obs = np.array(stats_(a)); S = np.array([stats_(rng.permutation(a)) for _ in range(B)])
        pk = np.array([(1 + (S[:, j] >= obs[j]).sum()) / (B + 1) for j in range(3)])
        # min-p (Westfall-Young): p de cada permutacion respecto del resto de permutaciones
        ranks = np.column_stack([(1 + B - np.searchsorted(np.sort(S[:, j]), S[:, j], side="left")) / (B + 1) for j in range(3)])
        minp_perm = ranks.min(axis=1); minp_obs = pk.min()
        base.update(sistematica=False, p_contig=pk[0], p_grupo=pk[1], p_color=pk[2], pares_adj=int(obs[0]), pares_esp=S[:, 0].mean(),
                    p=(1 + (minp_perm <= minp_obs).sum()) / (B + 1))
        rows.append(base)
T = pd.DataFrame(rows)
m = T.p.notna(); T["q_bh"] = np.nan; T.loc[m, "q_bh"] = bh(T.p[m])
T["estructurada"] = T.sistematica | (T.q_bh < .05)
T = T.sort_values(["estructurada", "n_anom"], ascending=False); T.to_csv(AQUI / "tabla_estructura_anomalias.csv", index=False)
print("pruebas (quipu x familia):", len(T), " permutables:", int(m.sum()), " estructuradas por permutacion (q<.05):", int((T.q_bh < .05).sum()), " sistematicas:", int(T.sistematica.sum()))
print(T.groupby("familia").agg(n=("kfg", "size"), estr=("estructurada", "sum"), sist=("sistematica", "sum")))
# directions blocks
R4 = pd.read_csv(AQUI / "tabla_dir_bloques.csv"); dirq = set(R4[R4.q_bh < .05].kfg)
# catalogo: score = cuerdas anomalas en familias estructuradas (sin contar L10, artefacto de codificacion)
E = T[T.estructurada & T.familia.isin(["inf", "tiporaro", "raras"])]  # banda y L10 se reportan aparte (banda = ruido de valla; L10 = n codifica valor)
sc = E.groupby("kfg").agg(score=("n_anom", "sum"), familias=("familia", lambda s: ",".join(s)))
cat = sc.join(qm[["procedencia", "museo"]]).join(k.groupby("kfg").size().rename("n_cuerdas_nudos"))
cat["dir_bloques"] = cat.index.isin(dirq)
Bd = T[T.estructurada & (T.familia == "banda")].set_index("kfg").n_anom; cat["n_banda_estructurada"] = Bd.reindex(cat.index).fillna(0).astype(int)
def nota(kf):
    e = E[E.kfg == kf]; n = []
    for r in e.itertuples():
        if r.familia == "inf" and (r.firma_modal.startswith("L-L") or r.firma_modal.startswith("E-E")): n.append("serie L/E: valor=suma de vueltas, sin pesos decimales")
        elif r.familia == "inf": n.append("L/E con racimo debajo (nudo inferior en sentido de Hyland?)")
        if r.familia == "tiporaro": n.append("tipo de nudo fuera de S/L/E (TF,U,EE,LL,SP...) sin glosa en KFG")
        if r.familia == "raras": n.append("violacion puntual (>9 simples, L1, E multiple, aporte no n*10^k, valor!=suma)")
    return " | ".join(dict.fromkeys(n))
cat["lectura_aburrida"] = [nota(x) for x in cat.index]
def det(kf):
    e = E[E.kfg == kf]; return "; ".join(f"{r.familia}:{r.n_anom}({100*r.frac:.0f}%) firma {r.firma_modal} {100*r.cuota_firma:.0f}% (resto {100*r.cuota_firma_resto:.0f}%)" + (" SIST" if r.sistematica else f" q={r.q_bh:.3g}") for r in e.itertuples())
cat["detalle"] = [det(x) for x in cat.index]
cat = cat.sort_values("score", ascending=False)
cat.to_csv(AQUI / "catalogo_completo.csv")
cat.head(30).to_csv(AQUI / "catalogo_top30.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(cat.head(30)[["procedencia", "n_cuerdas_nudos", "score", "dir_bloques", "detalle"]].to_string())
print("quipus con alguna familia estructurada (sin L10):", len(cat), "de", k.kfg.nunique())
