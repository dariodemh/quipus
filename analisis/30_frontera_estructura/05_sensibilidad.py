"""Enmienda 3 (posterior, conservadora): nulos que conservan la estructura local que podria imitar la senal.
- T3, I1-I4: permutar como bloques los tramos maximos de valores consecutivos tol-iguales (rachas y escalones),
  de modo que la autocorrelacion local de F se conserva y solo se rompe su alineacion.
- T5: mover el conjunto de subsidiarias de un colgante entero a otro colgante DEL MISMO GRUPO (conserva el agrupamiento
  de hermanas y la magnitud propia de cada grupo).
- I6: mismo nulo por tramos que I1-I4.
Se aplica a todas las filas con p < 0.05 de esas familias (para que la replica binomial tambien use p corregidos). p efectivo = max(p, p_bloque).
Uso: python 05_sensibilidad.py [--nulo R]"""
import sys, importlib.util
from multiprocessing import Pool
import numpy as np, pandas as pd
from comun import *

def _mod(nombre, archivo):
    s = importlib.util.spec_from_file_location(nombre, AQUI / archivo); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

FAM = {"T3_repeticion", "T5_subsidiaria", "I1_copia", "I2_invertida", "I3_diferencia", "I4_razon", "I6_suma_bloque_F_en_otro"}


def segmentos(v):
    seg = [[0]]
    for i in range(1, len(v)):
        if v[i] > 0 and v[i - 1] > 0 and tol(v[i], v[i - 1]): seg[-1].append(i)
        else: seg.append([i])
    return [np.array(s) for s in seg]


def perm_bloques(segs, N, rng):
    order = np.argsort(rng.random((N, len(segs))), 1)
    return np.array([np.concatenate([segs[j] for j in o]) for o in order])


def fila(args):
    k, prueba, nulo = args
    I1 = _mod("i1", "01_internas.py"); E = _mod("e2", "02_entre.py")
    q = quipu(k)
    if nulo is None: v, g = q.v, q.g
    else: v, g = E.nulo_frontera(k, nulo)
    if prueba == "T5_subsidiaria":
        sv = q.sub_v if nulo is None else I1.quipu_nulo(q, nulo)[4]
        pv = v[q.sub_padre]; m = (pv > 0) & (sv > 0)
        padres = np.unique(q.sub_padre[m]); pos = np.searchsorted(padres, q.sub_padre[m])
        rs = pd.Series(sv[m]).rank().to_numpy(); base = v[padres].astype(float)
        from scipy.stats import rankdata
        st = lambda P: I1._corr_rows(rs, rankdata(P[:, pos], axis=1))
        obs = float(st(base[None, :])[0])
        # bloques DENTRO de cada grupo: el conjunto de subsidiarias de un colgante pasa a otro colgante del mismo grupo
        gpad = g[padres]; idx_g = [np.where(gpad == x)[0] for x in np.unique(gpad)]
        def perm_g(n, rng):
            P = np.broadcast_to(base, (n, len(base))).copy()
            for ix in idx_g:
                if len(ix) > 1: P[:, ix] = base[ix][np.argsort(rng.random((n, len(ix))), 1)]
            return P
        p, N, b = p_escalada(obs, lambda n, rng: np.concatenate([st(perm_g(min(5000, n - i), rng)) for i in range(0, n, 5000)]), [999, 9999, 99999], 2)
        movibles = sum(len(ix) for ix in idx_g if len(ix) > 1)
        return dict(kfg=k, prueba=prueba, p_bloque=p, N_bloque=N, nota=f"rho={obs:.3f};padres={len(padres)};movibles_en_grupo={movibles}")
    segs = segmentos(v)
    if prueba == "T3_repeticion":
        base, f = I1.t3(v)
        obs = float(f(base[None, :])[0])
        p, N, b = p_escalada(obs, lambda n, rng: np.concatenate([f(base[perm_bloques(segs, min(5000, n - i), rng)]) for i in range(0, n, 5000)]), [999, 9999, 99999], 2)
        return dict(kfg=k, prueba=prueba, p_bloque=p, N_bloque=N, nota=f"segmentos={len(segs)}/{len(v)}")
    partners = companeros(k, "amplio")
    if prueba == "I6_suma_bloque_F_en_otro":
        tabla = E.prep_tabla_variantes(partners)
        st6 = lambda X: E.contar_hits(E.sumas_bloque(X), tabla, len(partners))
        obs = float(st6(v[None, :])[0])
        p, N, b = p_escalada(obs, lambda n, rng: np.concatenate([st6(v[perm_bloques(segs, c, rng)]) for c in E.chunks(n, 2000)]), E.ETAPAS, E.BMAX, 300.0)
        return dict(kfg=k, prueba=prueba, p_bloque=p, N_bloque=N, nota=f"segmentos={len(segs)}/{len(v)}")
    B, own, _ = E.concat(partners)
    u, I, wu, TB = E.prep_rachas(v, B)
    modo = "copia" if prueba in ("I1_copia", "I2_invertida") else ("diferencia" if prueba == "I3_diferencia" else "razon")
    inv = prueba == "I2_invertida"
    st = lambda Ix: E.stat_racha(Ix[:, ::-1] if inv else Ix, modo, u, wu, TB, B, own)
    obs = float(st(I[None, :])[0])
    nul = lambda n, rng: np.concatenate([st(I[perm_bloques(segs, c, rng)]) for c in E.chunks(n, 400)])
    p, N, b = p_escalada(obs, nul, E.ETAPAS, E.BMAX, 300.0)
    return dict(kfg=k, prueba=prueba, p_bloque=p, N_bloque=N, nota=f"segmentos={len(segs)}/{len(v)}")


if __name__ == "__main__":
    nulo = int(sys.argv[sys.argv.index("--nulo") + 1]) if "--nulo" in sys.argv else None
    D = _mod("d3", "03_decision.py")
    df = D.cargar(nulo)
    sel = df[df.estructura.isin(FAM) & (df.p_congelado < 0.05)]
    tareas = [(r.kfg, r.estructura, nulo) for r in sel.itertuples()]
    print(len(tareas), "filas", flush=True)
    with Pool(8) as pool:
        res = pool.map(fila, tareas, chunksize=1)
    out = pd.DataFrame(res)
    out.to_csv(AQUI / (f"sensibilidad_nulo{nulo}.csv" if nulo is not None else "sensibilidad.csv"), index=False)
    print(out.merge(sel[["kfg", "estructura", "p_congelado"]], left_on=["kfg", "prueba"], right_on=["kfg", "estructura"]).drop(columns="estructura").to_string())
