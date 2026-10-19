"""Motor de legibilidad del corpus (carpeta ds/n_legibilidad).

Reglas ESTRUCTURALES declaradas a priori (ninguna se elige mirando el valor de la cuerda objetivo):

Intra-quipu
  subs        padre = suma de sus hijas inmediatas presentes (>=2)
  subs_res    hija  = padre - suma de las otras hijas (>=2 hermanas)
  hija_unica  padre = su unica hija presente / hija = padre (igualdad)
  superior    unidad superior (union=T, o padre de colgantes T) = suma de los colgantes
              (nivel 0) del grupo adyacente ANTERIOR; si no sirve, el siguiente (>=2 terminos)
  grupo_total colgante solo en su grupo = suma de los colgantes del grupo anterior (>=2)
  cierre      1.a colgante del grupo = suma del resto, y cada partida = cabecera - resto.
              Puerta por quipu: >=50 % de los OTROS grupos cierran y >=4 grupos evaluables.

Entre quipus de la misma procedencia (nunca 'Unknown')
  copia       alineamiento LCS de la secuencia de colgantes; la cuerda oculta solo se predice
              si su emparejamiento queda determinado por anclas vecinas (hueco equilibrado)
  suma_dos    X[i] = A[i] + B[i] sobre la misma cadena de anclas; exige >=2 posiciones
              vecinas ya comprobadas que suman

Toda prediccion se evalua leave-one-out: la instancia no contiene el valor de su objetivo.
El nulo baraja los valores DENTRO de cada quipu (posiciones, estructura, grupos y colores fijos).
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parents[1] / "datos"

REGLAS = ["subs", "subs_res", "hija_unica", "superior", "grupo_total", "cierre", "copia", "suma_dos"]
RID = {r: i for i, r in enumerate(REGLAS)}
TOL1 = frozenset({0, 1})


def cargar():
    c = pd.read_csv(DATOS / "cuerdas.csv", dtype={"kfg": str, "cuerda": str, "padre": str, "nudos": str})
    q = pd.read_csv(DATOS / "quipus.csv", dtype={"kfg": str})
    c["nudos"] = c["nudos"].fillna("")
    c["valor"] = pd.to_numeric(c["valor"], errors="coerce")
    c["pres"] = ~((c["valor"].fillna(0) == 0) & (c["nudos"].str.strip() == ""))
    c["pres"] &= c["valor"].notna()
    c["vi"] = c["valor"].where(c["pres"])
    return c.sort_values(["kfg", "orden"]).reset_index(drop=True), q


class Quipu:
    __slots__ = ("kfg", "n", "val", "pres", "nivel", "grupo", "gidx", "posg", "union", "nombre",
                 "kids", "grupos", "tunits", "rows", "inst", "M", "tgt", "rule",
                 "fi", "fin", "fc", "ni", "via", "regla_de")

    def __init__(self, kfg, d):
        self.kfg = kfg
        self.rows = d.reset_index(drop=True)
        self.n = len(self.rows)
        self.val = self.rows["valor"].fillna(0).to_numpy(float)
        self.pres = self.rows["pres"].to_numpy(bool)
        self.nivel = self.rows["nivel"].to_numpy(int)
        self.grupo = self.rows["grupo"].fillna(-1).to_numpy(int)
        self.union = self.rows["union"].fillna("?").astype(str).to_numpy()
        self.nombre = self.rows["cuerda"].astype(str).to_numpy()
        # indice de posicion dentro de su grupo (solo nivel 0 presentes)
        self.posg = np.full(self.n, -1)
        self.grupos = []      # [(g, [idx l0])] en orden
        for g, dd in self.rows[self.rows.nivel == 0].groupby("grupo", sort=True):
            idx = dd.index.to_numpy()
            self.grupos.append((int(g), idx))
        for g, idx in self.grupos:
            k = 0
            for i in idx:
                if self.pres[i]:
                    self.posg[i] = k
                    k += 1
        self.gidx = {g: t for t, (g, _) in enumerate(self.grupos)}
        # hijas inmediatas presentes
        self.kids = {}
        has = self.rows["padre"].notna().to_numpy()
        name2i = {nm: i for i, nm in enumerate(self.nombre)}
        for i in np.where(has)[0]:
            p = self.rows["padre"].iat[i]
            j = name2i.get(p)
            if j is None:
                continue
            self.kids.setdefault(j, []).append(i)
        # unidades superiores
        self.tunits = []
        for t, (g, idx) in enumerate(self.grupos):
            for i in idx:
                if self.union[i] == "T":
                    self.tunits.append(i)
                else:
                    kj = self.kids.get(i, [])
                    if any(self.nivel[x] == 1 and self.union[x] == "T" for x in kj):
                        self.tunits.append(i)
        self.tunits = sorted(set(self.tunits))
        self._instancias()
        self._matriz()

    # ------------------------------------------------------------------ instancias
    def _add(self, t, pares, rule):
        pares = tuple((int(i), float(c)) for i, c in pares)
        self.inst.append((int(t), pares, rule))

    def _instancias(self):
        self.inst = []
        pres = self.pres
        # --- subsidiarias
        for p, kj in self.kids.items():
            if not pres[p]:
                continue
            cp = [k for k in kj if pres[k]]
            if len(cp) >= 2:
                self._add(p, [(k, 1) for k in cp], "subs")
                for k in cp:
                    self._add(k, [(p, 1)] + [(o, -1) for o in cp if o != k], "subs_res")
            elif len(cp) == 1:
                self._add(p, [(cp[0], 1)], "hija_unica")
                self._add(cp[0], [(p, 1)], "hija_unica")
        # --- superior
        for u in self.tunits:
            if not pres[u]:
                continue
            t = self.gidx.get(int(self.grupo[u]))
            if t is None:
                continue
            for dt in (-1, 1):
                tt = t + dt
                if 0 <= tt < len(self.grupos):
                    _, idx = self.grupos[tt]
                    l0 = [x for x in idx if pres[x] and x != u]
                    if len(l0) >= 2:
                        self._add(u, [(x, 1) for x in l0], "superior")
                        break
        # --- grupo total: colgante solo en su grupo
        for t, (g, idx) in enumerate(self.grupos):
            lp = [x for x in idx if pres[x]]
            if len(lp) != 1:
                continue
            u = lp[0]
            if u in self.tunits:
                continue  # esa la cubre la regla superior
            for dt in (-1, 1):
                tt = t + dt
                if 0 <= tt < len(self.grupos):
                    _, idx2 = self.grupos[tt]
                    l0 = [x for x in idx2 if pres[x]]
                    if len(l0) >= 2:
                        self._add(u, [(x, 1) for x in l0], "grupo_total")
                        break
        # --- cierre
        ev = []
        for t, (g, idx) in enumerate(self.grupos):
            lp = [x for x in idx if pres[x]]
            if len(lp) >= 3:
                ev.append(t)
        if len(ev) >= 4:
            cerrados = {}
            for t in ev:
                lp = [x for x in self.grupos[t][1] if pres[x]]
                h = lp[0]
                cerrados[t] = abs(self.val[h] - sum(self.val[x] for x in lp[1:])) <= 1
            for t in ev:
                otros = [u for u in ev if u != t]
                if len(otros) < 4:
                    continue
                rate = sum(cerrados[u] for u in otros) / len(otros)
                if rate < 0.5:
                    continue
                lp = [x for x in self.grupos[t][1] if pres[x]]
                h, rest = lp[0], lp[1:]
                self._add(h, [(x, 1) for x in rest], "cierre")
                for x in rest:
                    self._add(x, [(h, 1)] + [(o, -1) for o in rest if o != x], "cierre")

    def _matriz(self):
        n = self.n
        ni = len(self.inst)
        self.tgt = np.array([t for t, _, _ in self.inst], int)
        self.rule = np.array([RID[r] for _, _, r in self.inst], int)
        fi, fin, fc = [], [], []
        for k, (_, p, _) in enumerate(self.inst):
            for i, c in p:
                fi.append(i); fin.append(k); fc.append(c)
        self.fi = np.array(fi, int)
        self.fin = np.array(fin, int)
        self.fc = np.array(fc, float)
        self.ni = ni
        self.via = np.bincount(self.tgt, minlength=n) if ni else np.zeros(n, int)
        self.regla_de = [set() for _ in range(n)]
        for k, t in enumerate(self.tgt):
            self.regla_de[t].add(int(self.rule[k]))

    # ------------------------------------------------------------------ evaluacion
    def evaluar(self, v):
        """Devuelve (via, acierto) por cuerda con la valoracion v (array n)."""
        if self.ni == 0:
            return self.via, np.zeros(self.n, int)
        pred = np.bincount(self.fin, weights=self.fc * v[self.fi], minlength=self.ni)
        h = np.abs(pred - v[self.tgt]) < 0.5
        hit = np.bincount(self.tgt[h], minlength=self.n) if h.any() else np.zeros(self.n, int)
        return self.via, hit

    def inst_hits(self, v):
        """Acierto por INSTANCIA (para el nulo por regla)."""
        if self.ni == 0:
            return np.zeros(0, bool)
        pred = np.bincount(self.fin, weights=self.fc * v[self.fi], minlength=self.ni)
        return np.abs(pred - v[self.tgt]) < 0.5

    # ------------------------------------------------------------------ baselines
    def moda(self):
        """Prediccion = valor mas frecuente entre las DEMAS cuerdas del quipu."""
        vals = self.val[self.pres]
        if len(vals) < 2:
            return np.full(self.n, np.nan)
        u, cnt = np.unique(vals, return_counts=True)
        out = np.full(self.n, np.nan)
        for i in np.where(self.pres)[0]:
            v = self.val[i]
            c = cnt.copy()
            j = np.searchsorted(u, v)
            if j < len(u) and u[j] == v:
                c[j] -= 1
            k = int(np.argmax(c))
            if c[k] == 0:
                continue
            out[i] = u[k]
        return out


def construir(c=None):
    if c is None:
        c, q = cargar()
    else:
        _, q = cargar()
    Q = {}
    for k, d in c.groupby("kfg", sort=True):
        Q[k] = Quipu(k, d)
    return Q, c, q
