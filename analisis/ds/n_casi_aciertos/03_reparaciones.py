# -*- coding: utf-8 -*-
"""Motor de reparaciones de UNA operacion sobre la cadena `nudos`.

Para cada casi-acierto de `relaciones_casi.csv` se buscan ediciones de un solo
racimo/nudo en las cuerdas implicadas que hagan la relacion EXACTA. Cada
candidata lleva:
  - probabilidad: tasa empirica del tipo de error en el catalogo (por cuerda),
  - p_nulo: fraccion de cuerdas no relacionadas que admiten la misma edicion
    con el mismo delta (nulo geometrico, 04_nulo.py).

Salidas: reparaciones.csv (una fila por candidata), reparaciones_resumen.csv.
"""
import os, re, sys
import pandas as pd
import numpy as np

ROOT = r"."
OUT = os.path.join(ROOT, "analisis", "ds", "n_casi_aciertos")
RE = re.compile(r"(\d+)([A-Z]+)\(([\d.]+),([SZU])\),([\d.]+)")

TASAS = pd.read_csv(os.path.join(OUT, "catalogo_tasas_resto.csv"), index_col=0)["tasa_por_cuerda"].to_dict()
P = {
    "factor10": TASAS.get("factor10", 8.6e-5),
    "vueltas": TASAS.get("vueltas", 2.6e-4),
    "racimo_omitido": TASAS.get("racimo_omitido_okr", 2.6e-4),
    "racimo_duplicado": TASAS.get("racimo_omitido_kfg", 5.8e-5),
    "S_vs_L": TASAS.get("S_vs_L", 2.9e-5),
    "ocho_vs_largo": TASAS.get("ocho_vs_largo", 5.8e-5),
    "conteo_simple": TASAS.get("bloque", 2.0e-4),
    "insercion": TASAS.get("racimo_omitido_kfg", 5.8e-5),
}
Qn = pd.read_csv(os.path.join(OUT, "nulo_ediciones.csv"))

def parse(chain):
    if not isinstance(chain, str):
        return []
    cl = []
    for m in RE.finditer(chain):
        n, tipo, pos, d, val = int(m.group(1)), m.group(2), float(m.group(3)), m.group(4), float(m.group(5))
        cl.append(dict(n=n, tipo=tipo, pos=pos, d=d, val=val, power=None))
    for c in cl:
        if c["tipo"].startswith("S") and c["val"] > 0 and c["n"] > 0:
            r = c["val"] / c["n"]
            p = round(np.log10(r)) if r > 0 else 0
            c["power"] = int(p) if abs(r - 10 ** p) < 1e-6 else 0
    for i, c in enumerate(cl):
        if c["power"] is None:
            below = [x["power"] for x in cl[i + 1:] if x["power"] is not None]
            c["power"] = int(max(below) + 1) if below and max(below) >= 0 else 0
    return cl

def fmt(cl):
    return ";".join(f"{c['n']}{c['tipo']}({c['pos']:.1f},{c['d']}),{c['val']:g}" for c in cl)

def total(cl):
    return sum(c["val"] for c in cl)

def edits(cl):
    """(tipo, delta, descripcion, indice, n_candidatos, funcion_de_aplicacion)."""
    out = []
    n_L = max(sum(1 for c in cl if c["tipo"].startswith("L")), 1)
    n_E = max(sum(1 for c in cl if c["tipo"].startswith("E")), 1)
    n_S = max(sum(1 for c in cl if c["tipo"].startswith("S")), 1)
    for i, c in enumerate(cl):
        v, p = c["val"], c["power"]
        et = f"{c['tipo']}{c['n']}"
        for sgn in (1, -1):
            if sgn < 0 and (v % 10 != 0 or v < 10):
                continue
            out.append(("factor10", sgn * 9 * v, f"{et}@{c['pos']:.1f} se decodifica un lugar "
                        f"{'arriba' if sgn > 0 else 'abajo'} (x10{'^+1' if sgn>0 else '^-1'})", i, 1,
                        lambda cl, i=i, sgn=sgn: _cambia(cl, i, val=cl[i]["val"] * (10 if sgn > 0 else 0.1))))
        out.append(("racimo_omitido", -v, f"se omite el racimo {et}@{c['pos']:.1f}={v:g}", i, 1,
                    lambda cl, i=i: _borra(cl, i)))
        out.append(("racimo_duplicado", +v, f"se duplica el racimo {et}@{c['pos']:.1f}={v:g}", i, 1,
                    lambda cl, i=i: _duplica(cl, i)))
        if c["tipo"].startswith("L"):
            for k in (1, -1):
                if not (1 <= c["n"] + k <= 9):
                    continue
                out.append(("vueltas", k * 10 ** p, f"{et}@{c['pos']:.1f} pasa a {c['n']+k} vueltas",
                            i, n_L, lambda cl, i=i, k=k: _cambia(cl, i, n=cl[i]["n"] + k, val=cl[i]["val"] + k)))
            out.append(("S_vs_L", 10 ** p - v, f"{et}@{c['pos']:.1f} se lee como 1 simple en 10^{p}",
                        i, n_L, lambda cl, i=i: _cambia(cl, i, tipo="S", n=1, val=10 ** cl[i]["power"])))
            for k in range(2, 10):
                out.append(("ocho_vs_largo", 1 - k, f"{et}@{c['pos']:.1f} se lee como figura de ocho",
                            i, n_L, lambda cl, i=i: _cambia(cl, i, tipo="E", n=1, val=1)))
        if c["tipo"].startswith("S"):
            for k in (1, -1):
                if not (1 <= c["n"] + k <= 9):
                    continue
                out.append(("conteo_simple", k * 10 ** p, f"{et}@{c['pos']:.1f} pasa a {c['n']+k} nudos",
                            i, n_S, lambda cl, i=i, k=k: _cambia(cl, i, n=cl[i]["n"] + k, val=cl[i]["val"] + k * 10 ** cl[i]["power"])))
            out.append(("S_vs_L", 1 - v, f"{et}@{c['pos']:.1f} se lee como largo de 1 vuelta",
                        i, n_S, lambda cl, i=i: _cambia(cl, i, tipo="L", n=1, val=1)))
            out.append(("ocho_vs_largo", 1 - v, f"{et}@{c['pos']:.1f} se lee como figura de ocho",
                        i, n_S, lambda cl, i=i: _cambia(cl, i, tipo="E", n=1, val=1)))
        if c["tipo"].startswith("E"):
            for k in range(2, 10):
                out.append(("ocho_vs_largo", k - 1, f"{et}@{c['pos']:.1f} se lee como largo de {k} vueltas",
                            i, n_E, lambda cl, i=i, k=k: _cambia(cl, i, tipo="L", n=k, val=k)))
    for p in range(0, 5):
        for m in range(1, 10):
            out.append(("insercion", m * 10 ** p, f"falta un racimo de {m} simples en 10^{p}", -1, 1,
                        lambda cl, p=p, m=m: _inserta(cl, p, "S", m, m * 10 ** p)))
    for k in range(1, 10):
        out.append(("insercion", k, f"falta un nudo largo de {k} vueltas", -1, 1,
                    lambda cl, k=k: _inserta(cl, 0, "L", k, k)))
    out.append(("insercion", 1, "falta una figura de ocho", -1, 1,
                lambda cl: _inserta(cl, 0, "E", 1, 1)))
    return out

def _cambia(cl, i, **kw):
    cl = [dict(c) for c in cl]
    cl[i].update(kw)
    return cl

def _borra(cl, i):
    return [dict(c) for j, c in enumerate(cl) if j != i]

def _duplica(cl, i):
    cl = [dict(c) for c in cl]
    return cl[:i + 1] + [dict(cl[i])] + cl[i + 1:]

def _inserta(cl, p, tipo, n, val):
    cl = [dict(c) for c in cl]
    # posicion: antes del primer racimo de potencia menor; si no, al final
    pos = (cl[-1]["pos"] + 1.0) if cl else 1.0
    for j, c in enumerate(cl):
        if c["power"] < p:
            pos = max(0.5, c["pos"] - 0.5) if j > 0 else max(0.5, c["pos"] - 1.0)
            idx = j
            break
    else:
        idx = len(cl)
    cl.insert(idx, dict(n=n, tipo=tipo, pos=pos, d="U", val=val, power=p))
    return cl

def buscar(chain, delta):
    cl = parse(chain)
    if not cl:
        return []
    base = total(cl)
    hits, seen = [], set()
    for tipo, d, desc, i, ncand, fn in edits(cl):
        if abs(d - delta) > 1e-9:
            continue
        prop = fn(cl)
        if abs(total(prop) - (base + delta)) > 1e-6:
            continue
        s = fmt(prop)
        if s in seen:
            continue
        seen.add(s)
        hits.append(dict(tipo=tipo, delta=d, descripcion=desc, idx=i, n_cand=max(ncand, 1), propuesta=s))
    return hits


# ---------------- relaciones ----------------
R = pd.read_csv(os.path.join(OUT, "relaciones_casi.csv"))
c = pd.read_csv(os.path.join(OUT, "subset_cuerdas.csv"), dtype={"valor": float})
nudos = {(r.kfg, r.cuerda): r.nudos for r in c.itertuples()}
# ---- cuerdas del lado "libro" (objetivo) que tambien pueden estar mal leidas ----
R1_OBJ = {4: [("UR266", "p21"), ("UR275", "p1")], 8: [("UR266", "p45"), ("UR275", "p21")],
          12: [("UR266", "p64"), ("UR275", "p41")], 13: [("UR266", "p69"), ("UR275", "p45")],
          17: [("UR266", "p86")], 19: [("UR266", "p96"), ("UR275", "p78")],
          21: [("UR266", "p101"), ("UR275", "p82")]}
_u8 = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values("orden")
def objetivo_cords(r):
    out = []
    if r.familia == "R1_ur278_fila":
        g = int(r.relacion.lstrip("g"))
        out = R1_OBJ.get(g, [])
    elif r.familia == "R2_ur278_celda":
        rel = r.relacion                      # g21c1~UR270g0
        gg = int(rel[1:rel.index("c")]); col = int(rel[rel.index("c") + 1])
        cs = list(_u8[_u8.grupo == gg].cuerda)
        if len(cs) >= col:
            out = [("UR278", cs[col - 1])]
    elif r.familia in ("R3_ur273ab", "R4_ur274a_273b") and isinstance(r.objetivo_cuerda, str):
        if r.objetivo_cuerda.startswith("UR"):
            q, g = r.objetivo_cuerda.split()
            g = int(g.lstrip("g"))
            cc = c[(c.kfg == q) & (c.nivel == 0) & (c.grupo == g) & (c.valor.fillna(0) > 0)].sort_values("orden")
            if len(cc):
                out = [(q, cc.cuerda.iloc[0])]
    return out



det, res, RELC = [], [], []
for _, r in R.iterrows():
    cuerdas = str(r.cuerdas).split(";")
    delta = r.residual
    cands = []
    if pd.isna(delta):
        res.append(dict(familia=r.familia, quipu=r.quipu, relacion=r.relacion, objetivo=np.nan,
                        observado=r.observado, residual=np.nan, cuerdas=r.cuerdas,
                        n_ediciones=0, n_cuerdas_reparables=0, prob_una_edicion=0.0,
                        tipos="", especificidad=0.0, mejor_edicion="sin destino en el libro"))
        continue
    lista = [(x, "detalle") for x in cuerdas] + [(":".join(t), "libro") for t in objetivo_cords(r)]
    relc = []
    for cq, lado in lista:
        qq, cu = cq.split(":", 1) if ":" in cq else (r.quipu, cq)
        relc.append((qq, cu, lado))
        ch = nudos.get((qq, cu))
        nr = ch.count(";") + 1 if isinstance(ch, str) else 1
        d_buscar = delta if lado == "detalle" else -delta
        for h in buscar(ch, d_buscar):
            q = Qn[(Qn.n_racimos == nr) & (Qn.delta == delta)]
            qv = float(q[h["tipo"]].iloc[0]) if len(q) else np.nan
            cands.append(dict(relacion=f"{r.familia}:{r.quipu}:{r.relacion}",
                              familia=r.familia, quipu=r.quipu, objetivo=r.objetivo,
                              observado=r.observado, residual=delta, cuerda=cu, quipu_cuerda=qq, lado=lado,
                              nudos_actual=ch, nudos_propuesto=h["propuesta"],
                              tipo_error=h["tipo"], probabilidad=P[h["tipo"]] / h["n_cand"],
                              p_nulo=qv, n_candidatos_cuerda=h["n_cand"], delta_aplicado=d_buscar,
                              descripcion=h["descripcion"]))
    RELC += [dict(relacion=f"{r.familia}:{r.quipu}:{r.relacion}", quipu=qq, cuerda=cu, lado=lado)
             for qq, cu, lado in relc]
    por_cuerda = {}
    for x in cands:
        k = (x["quipu_cuerda"], x["cuerda"])
        por_cuerda[k] = por_cuerda.get(k, 0) + x["probabilidad"]
    p_rel = 1 - np.prod([1 - min(v, 1) for v in por_cuerda.values()]) if por_cuerda else 0.0
    det += cands
    res.append(dict(familia=r.familia, quipu=r.quipu, relacion=r.relacion, objetivo=r.objetivo,
                    observado=r.observado, residual=delta, cuerdas=r.cuerdas,
                    n_ediciones=len(cands), n_cuerdas_reparables=len(por_cuerda),
                    prob_una_edicion=p_rel,
                    tipos=";".join(sorted({x["tipo_error"] for x in cands})),
                    especificidad=(1 / len(cands)) if cands else 0.0,
                    mejor_edicion=(cands[0]["descripcion"] + " [" + cands[0]["cuerda"] + "]") if cands else ""))

D = pd.DataFrame(det).sort_values(["familia", "quipu", "relacion", "probabilidad"], ascending=[True, True, True, False])
S = pd.DataFrame(res)
RELT = pd.DataFrame(RELC)
RELT.to_csv(os.path.join(OUT, "relacion_cuerdas.csv"), index=False)
D.to_csv(os.path.join(OUT, "reparaciones.csv"), index=False)
S.to_csv(os.path.join(OUT, "reparaciones_resumen.csv"), index=False)
print("relaciones:", len(S), "| con >=1 reparacion:", (S.n_ediciones > 0).sum())
print(S.groupby("familia").apply(lambda g: pd.Series({"n": len(g), "reparables": (g.n_ediciones > 0).sum(),
      "p_media": g.prob_una_edicion.mean()}), include_groups=False).to_string())
print()
print(S[S.n_ediciones > 0][["familia", "quipu", "relacion", "residual", "n_ediciones", "n_cuerdas_reparables", "tipos"]].to_string(max_rows=40))
print("\nSIN reparacion (delta):", sorted(set(S[S.n_ediciones == 0].residual.dropna().astype(int))))
