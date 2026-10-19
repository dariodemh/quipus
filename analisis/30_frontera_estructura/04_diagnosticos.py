"""Diagnosticos descriptivos de las filas con nivel >= propuesto (no cambian niveles). Uso: python 04_diagnosticos.py"""
import importlib.util
import numpy as np, pandas as pd
from comun import *

def _mod(nombre, archivo):
    s = importlib.util.spec_from_file_location(nombre, AQUI / archivo); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
E = _mod("e2", "02_entre.py"); I1 = _mod("i1", "01_internas.py")

F = pd.read_csv(AQUI / "frontera_estructura.csv")
sel = F[F.nivel.isin(["demostrado", "apoyado", "propuesto"])]
out = []
for r in sel.itertuples():
    q = quipu(r.kfg); v = q.v; d = dict(kfg=r.kfg, estructura=r.estructura, nivel=r.nivel, sitio=ATLAS.loc[r.kfg, "procedencia"], museo=MUSEO[r.kfg])
    if r.estructura == "T2_periodo_color":
        c = q.col; alt = [i for i in range(len(c) - 1) if c[i] != c[i + 1] and i + 2 < len(c) and c[i] == c[i + 2]]
        # pares intercalados: dos colores que alternan; valor de cada color en pares consecutivos
        from collections import Counter
        top = [x for x, _ in Counter(c).most_common(2)]
        pares = [(v[i], v[i + 1]) for i in range(len(c) - 1) if c[i] == top[0] and c[i + 1] == top[1]]
        pares += [(v[i + 1], v[i]) for i in range(len(c) - 1) if c[i] == top[1] and c[i + 1] == top[0]]
        nz = [(a, b) for a, b in pares if a > 0 or b > 0]
        d["texto"] = (f"colores alternos {top[0]}/{top[1]} en {len(alt)} de {len(c)} posiciones; media {top[0]}={v[c == top[0]].mean():.1f}, "
                      f"{top[1]}={v[c == top[1]].mean():.1f}; pares vecinos con algun valor: {len(nz)}, {top[1]}>{top[0]} en {sum(b > a for a, b in nz)}")
    elif r.estructura == "T5_subsidiaria":
        pv = v[q.sub_padre]; m = (pv > 0) & (q.sub_v > 0)
        d["texto"] = f"{m.sum()} pares; subsidiaria < colgante en {np.mean(q.sub_v[m] < pv[m]):.0%}; razon mediana {np.median(q.sub_v[m] / pv[m]):.3f}; {r.detalle}"
    elif r.estructura == "T4_tendencia":
        gs = [list(map(int, v[(q.g == g) & (v > 0)])) for g in np.unique(q.g)]
        d["texto"] = "grupos >=4: " + " | ".join(str(x) for x in gs if len(x) >= 4)[:300]
    elif r.estructura == "T6_suma_salteada":
        gid = pd.factorize(q.g)[0]; slot = np.zeros(len(v), int)
        for gg in range(gid.max() + 1):
            ix = np.where(gid == gg)[0]; slot[ix] = np.arange(len(ix))
        pos = {(gid[i], slot[i]): i for i in range(len(v))}; hits = []
        for i in range(len(v)):
            for dd in (-1, 1):
                t = []; G = gid[i] + dd
                while (G, slot[i]) in pos and len(t) < 12:
                    t.append(pos[(G, slot[i])]); G += dd
                    if len(t) >= 2 and v[i] >= 10 and v[t].sum() == v[i] and (v[t] > 0).sum() >= 2:
                        hits.append(f"p{i+1}={'+'.join(str(v[j]) for j in t)}")
        d["texto"] = "; ".join(hits)
    elif r.estructura == "T7_pares_suma":
        a, b = I1.t7_esquemas(v, q.g)[r.detalle.split(";")[0]]
        s = v[a] + v[b]; vals, cnt = np.unique(s[(s >= 2)], return_counts=True); m = vals[cnt.argmax()]
        d["texto"] = f"suma modal {m} en {cnt.max()} de {len(a)} pares: " + " ".join(f"({v[i]}+{v[j]})" for i, j in zip(a, b) if v[i] + v[j] == m)
    elif r.estructura == "T3_repeticion":
        W = pesos(v); best = (0, "")
        for dd in range(1, len(v) - 2):
            run = 0; s = 0
            for i in range(len(v) - dd):
                if v[i] > 0 and v[i + dd] > 0 and tol(v[i], v[i + dd]): run += 1; s += W[i]
                else: run = s = 0
                if run >= 3 and s > best[0]:
                    best = (s, f"desfase {dd}: {list(map(int, v[i-run+1:i+1]))} ~ {list(map(int, v[i-run+1+dd:i+1+dd]))}")
        d["texto"] = best[1]
    elif r.estructura.startswith("I") and "companero=" in str(r.detalle):
        P = companeros(r.kfg, "amplio"); B, own, _ = E.concat(P); u, I, wu, TB = E.prep_rachas(v, B)
        modo = {"I1": "copia", "I2": "copia", "I3": "diferencia", "I4": "razon"}[r.estructura[:2]]
        Ix = (I[::-1] if r.estructura.startswith("I2") else I)[None, :]
        # puntuacion por companero: especificidad
        sc = []
        for pi, p in enumerate(P):
            msk = own == pi
            Bp = np.concatenate([B[msk], [-1]]); op = np.concatenate([np.zeros(msk.sum(), int), [-1]])
            TBp = tol(u[:, None], Bp[None, :]) & (u[:, None] > 0) & (Bp[None, :] > 0)
            sc.append((float(E.stat_racha(Ix, modo, u, wu, TBp, Bp, op)[0]), p))
        sc.sort(reverse=True)
        d["texto"] = "mejores companeros: " + ", ".join(f"{p} {s:.1f}" for s, p in sc[:4])
    elif r.estructura.startswith("I9"):
        comp = str(r.detalle).split("companeros=")[1].split("|")[0]
        qq = quipu(comp); T = [int(qq.v[qq.g == g].sum()) for g in np.unique(qq.g) if (qq.v[qq.g == g] > 0).sum() >= 2]
        hits = [t for t in T if t >= 10 and t in set(q.todos)]
        d["texto"] = f"totales de {comp} hallados en {r.kfg}: {hits} (distintos: {sorted(set(hits))})"
    elif r.estructura.startswith("I6"):
        P = companeros(r.kfg, "amplio"); sb = E.sumas_bloque(v[None, :])[0]; sb = set(sb[sb >= 10]); sc = []
        for p in P:
            sc.append((len({ci for ci, x in enumerate(quipu(p).todos) if x >= 10 and any(w in sb for w in variantes(int(x)))}), p, len(quipu(p).todos)))
        sc.sort(reverse=True)
        d["texto"] = "mejores companeros (aciertos, cuerdas): " + ", ".join(f"{p} {s}/{n}" for s, p, n in sc[:4])
    out.append(d)
D = pd.DataFrame(out)
D.to_csv(AQUI / "diagnosticos.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 220)
print(D.to_string())
