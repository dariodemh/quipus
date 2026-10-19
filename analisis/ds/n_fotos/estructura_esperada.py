# -*- coding: utf-8 -*-
"""Extrae la estructura 'esperada' (KFG + prosa del Databook) para los quipus fotografiados.
Salida compacta por pantalla y estructura_esperada.csv en esta carpeta."""
import os, re, pandas as pd

ROOT = r"."
FOTOS = os.path.join(ROOT, r"encontrado\Databook\Quipus\Images-notreproduce")
DB = os.path.join(ROOT, r"analisis\fuentes_txt\databook")
KFG = pd.read_csv(os.path.join(ROOT, r"analisis\datos\cuerdas.csv"))
ROWS = pd.read_csv(os.path.join(ROOT, r"analisis\ds\n_databook\databook_rows.csv"))

# id de quipu a partir del nombre de foto
def qid(f):
    b = f.upper()
    m = re.match(r"AS0*(\d+)", b)
    if not m:
        return None
    return "AS%03d" % int(m.group(1))

fotos = sorted(os.listdir(FOTOS))
inv = [(f, qid(f)) for f in fotos]
print("fotos:", len(fotos), "ids:", len({q for _, q in inv}))

out = []
for f, q in inv:
    if q is None:
        continue
    s = KFG[KFG.kfg == q]
    # KFG
    n_k = len(s); n0_k = int((s.nivel == 0).sum()); ng_k = int(s.grupo.nunique()) if n_k else 0
    sizes = s[s.nivel == 0].groupby("grupo").size().tolist() if n_k else []
    cols_k = "; ".join(f"{k}:{v}" for k, v in s.color.value_counts().head(6).items()) if n_k else ""
    # Databook
    d = ROWS[ROWS.quipu == q]
    n0_d = int(d.cord_databook.str.match(r"^p\d+$").sum()) if len(d) else 0
    cols_d = "; ".join(f"{k}:{v}" for k, v in d.color.value_counts().head(6).items()) if len(d) else ""
    out.append(dict(foto=f, quipu=q, kfg_n=n_k, kfg_pendants=n0_k, kfg_grupos=ng_k,
                    kfg_tamanos=",".join(map(str, sizes)), kfg_colores=cols_k,
                    db_filas=len(d), db_pendants=n0_d, db_colores=cols_d))

df = pd.DataFrame(out)
df.to_csv(os.path.join(os.path.dirname(__file__), "estructura_esperada.csv"), index=False)
res = df.groupby("quipu").agg(fotos=("foto", "size"), kfg_n=("kfg_n", "first"), kfg_p=("kfg_pendants", "first"),
                              kfg_g=("kfg_grupos", "first"), db_p=("db_pendants", "first"), db_f=("db_filas", "first"))
print(res.to_string())
