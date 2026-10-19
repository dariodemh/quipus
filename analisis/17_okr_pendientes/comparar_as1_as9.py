"""Parte B1: compara AS1-AS9.db (KH0002_0010) con las cuerdas KFG de AS001-AS009.

Solo lectura. Compara n.o de cuerdas por quipu y el multiconjunto de valores por quipu
(valor de cuerda = suma de TOTAL_VALUE de sus knot_cluster, la misma regla que el KFG).
Uso: python -I analisis/17_okr_pendientes/comparar_as1_as9.py
"""
import csv, sqlite3, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DB = RAIZ / "data/external/open-khipu-repository/data/KH0002_0010/AS1-AS9.db"
CUERDAS = RAIZ / "analisis/datos/cuerdas.csv"
QUIPUS = RAIZ / "analisis/datos/quipus.csv"

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
# valor por cuerda (suma de clusters de nudos); cuerdas sin nudos quedan en None
valor_cord = {cid: (tot if tot is not None else None) for cid, tot in con.execute(
    "select CORD_ID, sum(TOTAL_VALUE) from knot_cluster group by CORD_ID")}
nudos_cord = collections.Counter(cid for (cid,) in con.execute("select CORD_ID from knot"))
quip_db = {}
for kid, mnum, inv in con.execute("select KHIPU_ID, MUSEUM_NUM, INVESTIGATOR_NUM from khipu_main"):
    quip_db[kid] = (inv, mnum)
filas_db = collections.defaultdict(list)
niveles = collections.Counter()
for kid, cid, lvl, pend, att in con.execute(
        "select KHIPU_ID, CORD_ID, CORD_LEVEL, PENDANT_FROM, ATTACHED_TO from cord"):
    filas_db[kid].append((cid, lvl))
    niveles[lvl] += 1

kfg = list(csv.DictReader(open(CUERDAS, encoding="utf-8")))
kfg_as = [r for r in kfg if r["kfg"].startswith("AS00") and r["kfg"] in
          {f"AS00{i}" for i in range(1, 10)}]
por_q = collections.defaultdict(list)
for r in kfg_as:
    por_q[r["kfg"]].append(r)

print("cord por nivel en DB (CORD_LEVEL):", dict(sorted(niveles.items())))
print("quipu | KHIPU_ID | cuerdas | con nudos | suma de valores | multiconjunto de valores")
for kid in sorted(filas_db, key=lambda k: quip_db[k][0]):
    inv, mnum = quip_db[kid]
    cs = filas_db[kid]
    vals_db = [valor_cord.get(cid) for cid, _ in cs]
    con_nud = sum(1 for cid, _ in cs if nudos_cord.get(cid))
    kf = por_q.get(inv, [])
    kf_vals = [int(float(r["valor"])) if r["valor"] not in ("", None) else None for r in kf]
    kf_sin = sum(1 for r in kf if not r["nudos"])
    db_norm = sorted(v or 0 for v in vals_db)   # cuerda sin nudos = 0 (no hay valor que comparar)
    kf_norm = sorted(v or 0 for v in kf_vals)
    igual = db_norm == kf_norm
    print(f"{inv} | {kid} | cuerdas DB {len(cs)} / KFG {len(kf)} | con nudos DB {con_nud} / KFG {len(kf) - kf_sin} | "
          f"suma valores DB {sum(db_norm)} / KFG {sum(kf_norm)} | multiconjunto igual: {'si' if igual else 'no'}")
