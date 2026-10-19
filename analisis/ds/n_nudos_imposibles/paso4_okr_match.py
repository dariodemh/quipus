# -*- coding: utf-8 -*-
"""Paso 4: emparejar cuerdas KFG con OKR y comparar 'n' de KFG con NUM_TURNS real.
Solo quipus con cuerdas imposibles (para velocidad).
"""
import re, sqlite3, pandas as pd, numpy as np
BASE = r"."
df = pd.read_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\cuerdas_lecturas.pkl")
qp = pd.read_csv(BASE + r"\analisis\datos\quipus.csv", dtype=str, keep_default_na=False)
con = sqlite3.connect("file:" + BASE.replace("\\","/") + "/data/external/open-khipu-repository/data/khipu.db?mode=ro", uri=True)

def path_of(nombre):
    m = re.match(r"^p(\d+)((?:s\d+)*)$", nombre)
    if not m: return None
    return tuple([int(m.group(1))] + [int(x) for x in re.findall(r"s(\d+)", m.group(2))])

okr_map = {r[0]: r[1] for r in con.execute("select OKR_NUM,KHIPU_ID from khipu_main where OKR_NUM!=''")}
qp["kid"] = qp.okr.map(okr_map)
flag_kfg = set(df[df.imposible].kfg)
kids = qp[qp.kid.notna() & qp.kfg.isin(flag_kfg)][["kfg","kid"]].drop_duplicates()
print("quipus flag con match OKR:", len(kids))

rows=[]
for _,qr in kids.iterrows():
    kfg, kid = qr.kfg, int(float(qr.kid))
    cords = con.execute("select CORD_ID,CORD_ORDINAL,PENDANT_FROM,CORD_LEVEL,CORD_NOTES from cord where KHIPU_ID=?",(kid,)).fetchall()
    byid = {c[0]: c for c in cords}
    paths={}
    for cid, ordinal, parent, level, notes in cords:
        chain=[ordinal]; p=parent; guard=0
        while p in byid and byid[p][3]>=1 and guard<10:
            chain.append(byid[p][1]); p=byid[p][2]; guard+=1
        paths[tuple(reversed(chain))]=cid
    # todos los nudos del quipu de una vez
    kn = con.execute('''select c.CORD_ID,k.TYPE_CODE,k.NUM_TURNS,k.knot_value_type,k.KNOT_ORDINAL,
                               c.NUM_KNOTS,c.START_POS,c.NOTES
                        from knot k join knot_cluster c on k.CLUSTER_ID=c.CLUSTER_ID
                        join cord d on c.CORD_ID=d.CORD_ID where d.KHIPU_ID=?''',(kid,)).fetchall()
    bycord={}
    for x in kn: bycord.setdefault(x[0],[]).append(x)
    sub = df[df.kfg==kfg]
    for _,r in sub.iterrows():
        cid=paths.get(path_of(r.cuerda))
        if cid is None: continue
        ks=sorted(bycord.get(cid,[]), key=lambda x:(x[4] if x[4] is not None else 9999))
        cl=[]
        for x in ks:
            if not cl or abs(cl[-1]["pos"]-x[6])>1e-6:
                cl.append(dict(pos=x[6], tipos=[x[1]], turns=[x[2]], kvt=[x[3]], nk=x[5], notes=x[7]))
            else:
                cl[-1]["tipos"].append(x[1]); cl[-1]["turns"].append(x[2]); cl[-1]["kvt"].append(x[3])
        rows.append(dict(kfg=kfg, cuerda=r.cuerda, n_rac_kfg=r.n_rac, n_rac_okr=len(cl),
                         kfg_n=[k["n"] for k in r.knots], kfg_tipos=[k["tipo"] for k in r.knots],
                         okr_tipos=[c["tipos"][0] for c in cl],
                         okr_turns=[max([t for t in c["turns"] if t is not None], default=None) for c in cl],
                         okr_kvt=[max([t for t in c["kvt"] if t is not None], default=None) for c in cl],
                         okr_nk=[c["nk"] for c in cl],
                         okr_notes=[c["notes"] for c in cl if c["notes"]],
                         imposible=r.imposible, L10=r.L10))
m = pd.DataFrame(rows)
print("cuerdas KFG emparejadas con OKR:", len(m), "de", len(df[df.kfg.isin(flag_kfg)]))
print("de las L>=10, emparejadas:", m[m.L10].shape[0], "de", int(df.L10.sum()))
m.to_pickle(BASE + r"\analisis\ds\n_nudos_imposibles\match_okr.pkl")

sub=m[m.L10].copy()
sub["kfg_max"]=sub.kfg_n.map(lambda x:max(x) if len(x) else None)
sub["turns_max"]=sub.okr_turns.map(lambda x:max([t for t in x if t is not None],default=None))
sub["kvt_max"]=sub.okr_kvt.map(lambda x:max([t for t in x if t is not None],default=None))
print("\nL10 emparejadas:",len(sub))
print("turns_max>=10 (vueltas reales):", int((sub.turns_max>=10).sum()))
print("turns_max 2-9 y kvt_max>=10 (valor de posicion):", int(((sub.turns_max<10)&(sub.kvt_max>=10)).sum()))
print("sin dato turns:", int(sub.turns_max.isna().sum()))
print("\nejemplos turns>=10:")
print(sub[sub.turns_max>=10][["kfg","cuerda","kfg_n","okr_turns","okr_kvt","okr_tipos"]].head(12).to_string())
print("\nejemplos turns<10 kvt>=10:")
print(sub[(sub.turns_max<10)&(sub.kvt_max>=10)][["kfg","cuerda","kfg_n","okr_turns","okr_kvt","okr_tipos"]].head(12).to_string())
