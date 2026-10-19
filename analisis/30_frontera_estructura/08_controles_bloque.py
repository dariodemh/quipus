"""Controles positivos bajo el nulo por tramos de la Enmienda 3 (potencia del nulo conservador).
Uso: python 08_controles_bloque.py"""
import importlib.util
import numpy as np, pandas as pd
from comun import *

def _mod(n, a):
    s = importlib.util.spec_from_file_location(n, AQUI / a); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
E = _mod("e2", "02_entre.py"); S = _mod("s5", "05_sensibilidad.py")

filas = []
for k, extra, prueba in [("UR1107", "UR237", "I2_invertida"), ("UR1084", "HP055", "I1_copia")]:
    v = quipu(k).v; P = sorted(set(companeros(k, "amplio")) | {extra})
    B, own, _ = E.concat(P); u, I, wu, TB = E.prep_rachas(v, B); segs = S.segmentos(v)
    inv = prueba == "I2_invertida"
    st = lambda Ix: E.stat_racha(Ix[:, ::-1] if inv else Ix, "copia", u, wu, TB, B, own)
    obs = float(st(I[None, :])[0])
    p, N, b = p_escalada(obs, lambda n, rng: np.concatenate([st(I[S.perm_bloques(segs, c, rng)]) for c in E.chunks(n, 400)]), [199, 1999], 1, 300.0)
    filas.append(dict(control=f"{prueba} {k}~{extra}", estadistico=obs, p_bloque=p, N=N, segmentos=f"{len(segs)}/{len(v)}"))
    print(filas[-1], flush=True)
pd.DataFrame(filas).to_csv(AQUI / "controles_bloque.csv", index=False)
