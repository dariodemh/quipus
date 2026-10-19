# -*- coding: utf-8 -*-
"""Catalogo empirico de errores de lectura/transcripcion.

Fuente principal: KFG vs OKR, comparando racimo a racimo (223 discrepancias de
valor sobre 35 884 cuerdas con nudos). Fuente secundaria: KFG vs Databook.

Salida: catalogo_cuerdas.csv (una fila por discrepancia) y catalogo_resumen.csv.
"""
import os, re, sqlite3, difflib
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "n_casi_aciertos")
RE = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")

# ---------- cadenas KFG -> racimos ----------
def kfg_clusters(s):
    out = []
    if not isinstance(s, str):
        return out
    for m in RE.finditer(s):
        n, tipo, pos, d, val = int(m.group(1)), m.group(2), float(m.group(3)), m.group(4), float(m.group(5))
        out.append(dict(tipo=tipo, n=n, val=val, pos=pos))
    return out

# ---------- OKR: nudos -> racimos ----------
con = sqlite3.connect(os.path.join(ROOT, "data", "external", "open-khipu-repository", "data", "khipu.db"))
kn = pd.read_sql("SELECT CORD_ID,TYPE_CODE,DIRECTION,knot_value_type,CLUSTER_ID,KNOT_ORDINAL,"
                 "CLUSTER_ORDINAL,NUM_TURNS FROM knot", con)
con.close()
kn["val"] = kn.knot_value_type.astype(float)
# largos sin valor recuperable: usar vueltas
m = (kn.val == 0) & (kn.TYPE_CODE.isin(["L", "LL"])) & (kn.NUM_TURNS > 0)
kn.loc[m, "val"] = kn.loc[m, "NUM_TURNS"]

def okr_clusters(cid):
    x = kn[kn.CORD_ID == cid].sort_values(["CLUSTER_ORDINAL", "KNOT_ORDINAL"])
    out = []
    for cl, g in x.groupby("CLUSTER_ID", sort=False):
        tipo = "".join(sorted(set(g.TYPE_CODE.astype(str))))
        out.append(dict(tipo=tipo, n=len(g), val=float(g.val.sum()),
                        turns=float(g.NUM_TURNS.max())))
    return out

# ---------- clasificacion de una diferencia entre dos secuencias de racimos ----------
def clasifica(ck, co):
    """Devuelve (tipo, detalle) para una pareja de cadenas alineada."""
    vk = [c["val"] for c in ck]
    vo = [c["val"] for c in co]
    sm = difflib.SequenceMatcher(a=vk, b=vo, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    if len(ops) != 1:
        return "compuesto", f"{len(ops)} operaciones"
    tag, i1, i2, j1, j2 = ops[0]
    a, b = ck[i1:i2], co[j1:j2]
    if tag == "delete":
        return "racimo_omitido_okr", f"KFG {[c['val'] for c in a]} no en OKR"
    if tag == "insert":
        return "racimo_omitido_kfg", f"OKR {[c['val'] for c in b]} no en KFG"
    if len(a) == 1 and len(b) == 1:
        ka, kb = a[0], b[0]
        if ka["tipo"].startswith("L") and kb["tipo"].startswith("L"):
            d = kb["val"] - ka["val"]
            return "vueltas", f"L {ka['val']:.0f}->{kb['val']:.0f} (d={d:+.0f})"
        if ka["tipo"].startswith("L") and kb["tipo"].startswith("E") or \
           ka["tipo"].startswith("E") and kb["tipo"].startswith("L"):
            return "ocho_vs_largo", f"{ka['tipo']}{ka['val']:.0f} vs {kb['tipo']}{kb['val']:.0f}"
        if {ka["tipo"][:1], kb["tipo"][:1]} == {"S", "L"}:
            return "S_vs_L", f"{ka['tipo']}{ka['val']:.0f} vs {kb['tipo']}{kb['val']:.0f}"
        if ka["tipo"].startswith("S") and kb["tipo"].startswith("S"):
            d = (kb["val"] - ka["val"]) / max(ka["val"], 1e-9)
            if abs(ka["val"] - kb["val"]) <= 1.5:
                return "simple_conteo", f"S {ka['val']:.0f}->{kb['val']:.0f}"
            r = kb["val"] / ka["val"] if ka["val"] else np.nan
            if r and (abs(r - 10) < 1e-6 or abs(r - 0.1) < 1e-6):
                return "factor10", f"S {ka['val']:.0f}->{kb['val']:.0f}"
            return "S_otro", f"S {ka['val']:.0f}->{kb['val']:.0f}"
        r = kb["val"] / ka["val"] if ka["val"] else np.nan
        if r and (abs(r - 10) < 1e-6 or abs(r - 0.1) < 1e-6):
            return "factor10", f"{ka['tipo']}{ka['val']:.0f}->{kb['tipo']}{kb['val']:.0f}"
        return "otro", f"{ka['tipo']}{ka['val']:.0f} vs {kb['tipo']}{kb['val']:.0f}"
    return "bloque", f"{len(a)} vs {len(b)} racimos"

# ---------- 1. KFG vs OKR ----------
j = pd.read_csv(os.path.join(ROOT, "analisis", "ds", "t_okr_vs_kfg", "salidas", "join_cuerdas.csv"))
j = j[j.nudos.notna() & (j.dlargo.abs() <= 0.5)]          # comparacion defendible
j = j[j.valor > 0]
j["es_disc"] = (j.valor_okr - j.valor).abs() > 1e-9

# denominadores
n_cuerdas = len(j)
n_con_L = j.nudos.str.contains(r"\d+L\(", regex=True).sum()
n_con_E = j.nudos.str.contains(r"\d+E", regex=True).sum()
filas = []
for _, r in j[j.es_disc].iterrows():
    ck, co = kfg_clusters(r.nudos), okr_clusters(r.CORD_ID)
    tipo, det = clasifica(ck, co)
    filas.append(dict(kfg=r.kfg, cuerda=r.cuerda, valor_kfg=r.valor, valor_okr=r.valor_okr,
                      delta=r.valor_okr - r.valor, tipo_error=tipo, detalle=det,
                      nudos=r.nudos, n_racimos=len(ck), tiene_L=any(c["tipo"].startswith("L") for c in ck),
                      tiene_E=any(c["tipo"].startswith("E") for c in ck), prefijo=r.kfg[:2]))
cat = pd.DataFrame(filas)
cat.to_csv(os.path.join(OUT, "catalogo_cuerdas.csv"), index=False)

print(f"cuerdas comparables (nudos, largo +-0.5): {n_cuerdas}")
print(f"  con nudo largo: {n_con_L}   con figura de ocho: {n_con_E}")
print(f"discrepancias de valor: {len(cat)}  ({len(cat)/n_cuerdas*100:.2f} %)")
print()
res = cat.tipo_error.value_counts().rename("n").to_frame()
res["pct"] = (res.n / len(cat) * 100).round(1)
res["por_1000_cuerdas"] = (res.n / n_cuerdas * 1000).round(2)
print(res.to_string())
print()
print("detalle de los tipos grandes:")
for t in res.index[:8]:
    x = cat[cat.tipo_error == t]
    print(f"  {t:20s} n={len(x):3d}  ejemplo: {x.detalle.iloc[0][:60]}  | {x.kfg.iloc[0]} {x.cuerda.iloc[0]}")
print()
print("delta por tipo (mediana, min, max):")
print(cat.groupby("tipo_error").delta.agg(["count", "median", "min", "max"]).to_string())

# tasas por cuerda (para el modelo de probabilidad)
tasas = {}
for t, g in cat.groupby("tipo_error"):
    tasas[t] = len(g) / n_cuerdas
tasas["cualquier_error"] = len(cat) / n_cuerdas
pd.Series(tasas).to_csv(os.path.join(OUT, "catalogo_tasas.csv"), header=["tasa_por_cuerda"])

# --- tasas del "resto": sin los 5 quipus que concentran el 86 % de las discrepancias ---
OUTL = {"UR090", "UR144", "UR235", "UR193", "UR190"}
jr = j[~j.kfg.isin(OUTL)]
catr = cat[~cat.kfg.isin(OUTL)]
nr, nLr = len(jr), jr.nudos.str.contains(r"\d+L\(", regex=True).sum()
nEr = jr.nudos.str.contains(r"\d+E", regex=True).sum()
print(f"RESTO (sin UR090/144/235/193/190): {len(catr)} discrepancias / {nr} cuerdas = {len(catr)/nr*100:.3f} %")
print("  con L:", nLr, " con E:", nEr)
rr = (catr.tipo_error.value_counts() / nr * 1000).round(4).rename("por_1000_cuerdas").to_frame()
rr["n"] = catr.tipo_error.value_counts()
print(rr.to_string())
pd.DataFrame({"n": catr.tipo_error.value_counts(), "tasa_por_cuerda": catr.tipo_error.value_counts()/nr,
              "n_con_L": nLr, "n_con_E": nEr}).to_csv(os.path.join(OUT, "catalogo_tasas_resto.csv"))
# exposiciones utiles
print("\nVentanas de exposicion (resto):")
print(f"  cuerdas: {nr}; con L: {nLr} ({nLr/nr*100:.1f} %); con E: {nEr} ({nEr/nr*100:.1f} %)")
print(f"  racimos por cuerda (media): {catr.n_racimos.mean():.2f}")

# ---------- 2. KFG vs Databook (fuente secundaria) ----------
db = pd.read_csv(os.path.join(ROOT, "analisis", "ds", "n_databook", "discrepancias.csv"))
print("\nKFG vs Databook (311 discrepancias, 210 quipus AS):")
print(db.clase.value_counts().to_string())
