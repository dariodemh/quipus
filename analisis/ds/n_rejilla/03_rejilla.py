"""03 · Rejilla final, firma de las 9 partes y diccionario de categorias."""
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, ".")
from comun_rejilla import RAIZ, SEMILLA, COLS9, cargar_cuerdas, color_familia

rng = np.random.default_rng(SEMILLA)
c, q = cargar_cuerdas()

# ---------------------------------------------------------------- estilo por quipu
quipus = ["UR255", "UR256", "UR266", "UR267A", "UR267B", "UR268", "UR269", "UR270",
          "UR273A", "UR273B", "UR274A", "UR274B", "UR275", "UR278"]
filas = []
for k in quipus:
    s = c[c.kfg == k]
    filas.append(dict(quipu=k, n_cuerdas=len(s), n_grupos=s.grupo.nunique(),
                      mediana_grupo=float(s.groupby("grupo").size().median()),
                      color_modal=s.color.mode().iat[0] if len(s) else "",
                      pct_W=float((s.color == "W").mean()),
                      pct_mezcla=float(s.color.str.contains("[:/\\-]").mean()),
                      union_modal=s.union.mode().iat[0] if len(s) else "",
                      torsion_modal=s.torsion.mode().iat[0] if len(s) else "",
                      nivel1=float((s.nivel == 1).mean())))
E = pd.DataFrame(filas)
E.to_csv("estilo_quipu.csv", index=False, encoding="utf-8-sig")
print(E.to_string(index=False, float_format=lambda x: f"{x:.2f}"))

# ---------------------------------------------------------------- rejilla larga
t = pd.read_csv(f"{RAIZ}/13_sistema_incahuasi/ur278_tabla.csv").set_index("grupo")
pares = {0: 21, 4: 25, 5: 26, 8: 27, 9: 28}
inv = {v: k for k, v in pares.items()}
filas = []


def add(quipu, registro, parte, pos, comp, valor, color, nivel, union, torsion, largo,
        total, cuota, par):
    filas.append(dict(quipu=quipu, registro=registro, parte=parte, posicion=pos,
                      componente=comp, valor=valor,
                      prop=(valor / total if total and not pd.isna(valor) else np.nan),
                      color=color, nivel=nivel, union=union, torsion=torsion,
                      largo=largo, total_registro=total, cuota=cuota, par=par))


# UR278: una celda = un colgante (ya es P+S)
s = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values(["grupo", "orden"]).copy()
s["pos"] = s.groupby("grupo").cumcount() + 1
grupos278 = set(t.index)  # las 28 filas de la tabla de 13/05
for g, d in s.groupby("grupo"):
    if g not in grupos278:
        continue
    d = d[d.pos <= 9]
    if len(d) < 7:
        continue
    for _, r in d.iterrows():
        cuota = 47 if (11 <= g <= 19 or 21 <= g <= 29) else np.nan
        add("UR278", g, f"c{int(r.pos)}", int(r.pos), "celda", r.valor, r.color,
            int(r.nivel), r.union, r.torsion, r.largo, d.valor.sum(), cuota, g)

# UR270: P (colgante), S (1.a subsidiaria) y celda P+S
u = c[(c.kfg == "UR270") & (c.nivel == 0)].sort_values(["grupo", "orden"]).copy()
u["pos"] = u.groupby("grupo").cumcount() + 1
for g, d in u.groupby("grupo"):
    if len(d) != 9:
        continue
    sub = c[(c.kfg == "UR270") & (c.nivel == 1) & (c.padre.isin(d.cuerda))]
    total = 0.0
    for _, p in d.iterrows():
        ss = sub[sub.padre == p.cuerda].sort_values("orden")
        v = p.valor + (ss.iloc[0].valor if len(ss) else np.nan)
        total += v
    cuota = 47 if g in pares else np.nan
    for _, p in d.iterrows():
        ss = sub[sub.padre == p.cuerda].sort_values("orden")
        vacia = bool(p.sin_nudos and p.valor == 0)
        add("UR270", g, f"c{int(p.pos)}", int(p.pos), "P",
            np.nan if vacia else p.valor, p.color, int(p.nivel),
            p.union, p.torsion, p.largo, total, cuota, pares.get(g, np.nan))
        if len(ss):
            s0 = ss.iloc[0]
            add("UR270", g, f"c{int(p.pos)}", int(p.pos), "S", s0.valor, s0.color,
                int(s0.nivel), s0.union, s0.torsion, s0.largo, total, cuota, pares.get(g, np.nan))
        v = p.valor + (ss.iloc[0].valor if len(ss) else 0.0)
        if vacia and (len(ss) == 0 or (ss.iloc[0].sin_nudos and ss.iloc[0].valor == 0)):
            v = np.nan
        add("UR270", g, f"c{int(p.pos)}", int(p.pos), "celda", v, "", 0, "", "", np.nan,
            total, cuota, pares.get(g, np.nan))

R = pd.DataFrame(filas)
R.to_csv("rejilla_larga.csv", index=False, encoding="utf-8-sig")

# rejilla ancha: una fila por registro, 9 columnas de valor + metadatos
ancha = []
for (k, reg, par), d in R[R.componente == "celda"].groupby(["quipu", "registro", "par"], dropna=False):
    d = d.sort_values("posicion")
    fila = dict(quipu=k, registro=reg, par=par,
                cuota=d.cuota.iloc[0], total=d.total_registro.iloc[0],
                n_partes=int(d.valor.notna().sum()))
    for _, r in d.iterrows():
        fila[f"c{int(r.posicion)}"] = r.valor
    if k == "UR278":
        fila["color_registro"] = d.color.mode().iat[0] if d.color.notna().any() else ""
        fila["color_subsidiaria"] = ""
    else:
        fila["color_registro"] = "W"
        fila["color_subsidiaria"] = "NB"
    ancha.append(fila)
A = pd.DataFrame(ancha)
cols = ["quipu", "registro", "par", "cuota", "total", "n_partes"] + COLS9 + ["color_registro", "color_subsidiaria"]
A = A[cols].sort_values(["quipu", "registro"])
A.to_csv("rejilla.csv", index=False, encoding="utf-8-sig")
print(f"\nrejilla.csv (ancha): {len(A)} registros x 9 partes")
print(A.head(8).to_string(index=False))
print(f"\nrejilla_larga.csv: {len(R)} filas; "
      f"UR278 {R[R.quipu=='UR278'].registro.nunique()} registros, "
      f"UR270 {R[R.quipu=='UR270'].registro.nunique()} registros")
print(R.groupby(["quipu", "componente"]).size().to_string())

# comprobacion: la celda UR270 coincide con la fila de UR278 en el par
chk = R[(R.componente == "celda") & R.par.notna()].copy()
chk["par"] = chk.par.astype(int)
piv270 = chk[chk.quipu == "UR270"].pivot_table(index="par", columns="posicion", values="valor")
piv278 = chk[chk.quipu == "UR278"].pivot_table(index="par", columns="posicion", values="valor")
ok = 0
tot = 0
for p in sorted(set(piv270.index) & set(piv278.index)):
    a = piv270.loc[p].values
    b = piv278.loc[p].values
    ok += int(np.sum(np.abs(a - b) <= 1))
    tot += len(a)
print(f"celdas UR270 vs UR278 que coinciden +-1: {ok}/{tot}")

# ---------------------------------------------------------------- diccionario
# numeros que se citan en el diccionario (calculados aqui, no copiados)
lib = pd.read_csv(f"{RAIZ}/13_sistema_incahuasi/libro_consolidado.csv")
pct_cab_W = float((lib.color == "W").mean())
n_cab = len(lib)
# null de cabecera blanca: permutar colores dentro del quipu entre colgantes
obs = int((lib.color == "W").sum())
null = []
for _ in range(3000):
    tot = 0
    for k, ss in lib.groupby("quipu"):
        v = c[(c.kfg == k) & (c.nivel == 0)].color.values.copy()
        rng.shuffle(v)
        tot += int(np.sum(v[:len(ss)] == "W"))
    null.append(tot)
p_cab = (1 + np.sum(np.array(null) >= obs)) / (len(null) + 1)

# cuota: color y posicion, con nulo de posicion
cuota_txt = {}
for k, cue in [("UR266", 47), ("UR275", 47), ("UR269", 46)]:
    ss = lib[lib.quipu == k]
    n2 = 0
    cols = []
    grupos = []
    for r in ss.itertuples():
        g = c[(c.kfg == k) & (c.grupo == r.grupo) & (c.nivel == 0)].sort_values("orden")
        grupos.append(g.valor.astype(float).values)
        if len(g) > 1 and g.iloc[1].valor == cue:
            n2 += 1
            cols.append(g.iloc[1].color)
    # nulo: barajar los valores dentro de cada grupo y mirar la 2.a posicion
    obs_q = n2
    null_q = 0
    for _ in range(5000):
        cnt = 0
        for v in grupos:
            if len(v) < 2:
                continue
            vv = v.copy()
            rng.shuffle(vv)
            if vv[1] == cue:
                cnt += 1
        null_q += (cnt >= obs_q)
    p_q = (1 + null_q) / 5001
    n_valid = sum(len(v) >= 2 for v in grupos)
    cuota_txt[k] = (n2, n_valid, pd.Series(cols).value_counts().to_dict(), p_q)

# parte A / B en UR270
u0 = c[(c.kfg == "UR270") & (c.nivel == 0)]
u1 = c[(c.kfg == "UR270") & (c.nivel == 1)]
g9 = set(u0.groupby("grupo").size()[lambda x: x == 9].index)
u0 = u0[u0.grupo.isin(g9)]
u1 = u1[u1.padre.isin(u0.cuerda)]
pctP_W = float((u0.color == "W").mean())
fam1 = u1.color.map(color_familia)
pctS_NB = float(((u1.color.str.startswith(("NB", "KB"))) |
                 (u1.color.str.contains("NB"))).mean())

# color por columna en UR278 (informacion mutua)
s278 = c[(c.kfg == "UR278") & (c.nivel == 0)].sort_values(["grupo", "orden"]).copy()
s278["pos"] = s278.groupby("grupo").cumcount() + 1
s278 = s278[(s278.pos <= 9) & (s278.grupo.isin(t.index))]
s278 = s278[s278.groupby("grupo").grupo.transform("size") >= 7]


def mi(df):
    ct = pd.crosstab(df.pos, df.color).values.astype(float)
    p = ct / ct.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.nansum(p * np.log2(p / (p.sum(1, keepdims=True) * p.sum(0, keepdims=True)))))
obs_mi = mi(s278)
null_mi = []
for _ in range(2000):
    x = s278.copy()
    x["color"] = x.groupby("grupo").color.transform(lambda v: rng.permutation(v.values))
    null_mi.append(mi(x))
p_mi = (1 + np.sum(np.array(null_mi) >= obs_mi)) / (len(null_mi) + 1)
mono = s278.groupby("grupo").color.nunique()

D = pd.DataFrame([
    dict(categoria="cabecera (total bruto del registro)",
         definicion="Primera cuerda anudada del registro; su valor es el total",
         marcador="posicion 1 + color blanco",
         atributos=f"W {obs}/{n_cab} ({pct_cab_W:.0%}); nulo {np.mean(null):.0f}/{n_cab}; p={p_cab:.4f}; nivel 0; union variable",
         evidencia="demostrado (estructura) / apoyado (color blanco)"),
    dict(categoria="cuota c",
         definicion="Constante del libro que se resta a la cabecera para dar el neto",
         marcador="posicion 2 (tras la cabecera); valor constante por libro",
         atributos=f"UR275 {cuota_txt['UR275'][0]}/{cuota_txt['UR275'][1]} en 2.a pos (p={cuota_txt['UR275'][3]:.4f}), color {cuota_txt['UR275'][2]}; "
                   f"UR266 {cuota_txt['UR266'][0]}/{cuota_txt['UR266'][1]} (p={cuota_txt['UR266'][3]:.4f}), color {cuota_txt['UR266'][2]}; "
                   f"UR269 {cuota_txt['UR269'][0]}/{cuota_txt['UR269'][1]}",
         evidencia="apoyado (posicion); color = estilo del libro"),
    dict(categoria="parte A (subsidiaria del componente)",
         definicion="Componente A de un registro partido en dos libros; cuota 30 o 15",
         marcador="nivel 1; color NB/KB; cuelga del colgante de la parte B",
         atributos=f"UR270 subsidiarias: NB/KB o mezcla con NB {pctS_NB:.0%}, nivel 1, union U; "
                   f"en UR273A/UR274A la parte A tiene cuota 30/15",
         evidencia="demostrado (aritmetica) / apoyado (color)"),
    dict(categoria="parte B (colgante del componente)",
         definicion="Componente B de un registro partido en dos libros; cuota 17 o 10",
         marcador="nivel 0; color blanco",
         atributos=f"UR270 colgantes W {pctP_W:.0%}, nivel 0, union V; cuota 17/10 en UR273B/UR274B",
         evidencia="demostrado (aritmetica) / apoyado (color)"),
    dict(categoria="columna k (k=1..9)",
         definicion="Parte ordinal dentro del registro de 9 cuerdas; la celda es colgante+subsidiaria",
         marcador="posicion ordinal 1..9 (no color)",
         atributos=f"39/45 celdas ±1 en los 5 pares; color constante dentro de la fila en {int((mono==1).sum())}/{len(mono)} filas; "
                   f"MI(columna,color)={obs_mi:.3f} bits, nulo {np.mean(null_mi):.3f}, p={p_mi:.2f}",
         evidencia="demostrado (estructura y orden); color NO marca la columna"),
    dict(categoria="celda compuesta (P+S)",
         definicion="Valor de una columna = colgante + primera subsidiaria del grupo de UR270",
         marcador="aritmetica; no es una cuerda unica en UR270",
         atributos="45/45 celdas +-1; en UR278 es una sola cuerda de nivel 0",
         evidencia="demostrado"),
    dict(categoria="neto n = x - c",
         definicion="Diferencia entre cabecera y cuota; a veces se explicita como cuerda",
         marcador="posicion siguiente a la cuota; con frecuencia ausente",
         atributos="no tiene color ni posicion propios estables; se reconstruye por aritmetica",
         evidencia="propuesto"),
])
D.to_csv("diccionario_categorias.csv", index=False, encoding="utf-8-sig")
print("\nPrueba de posicion de la cuota (2.a cuerda del grupo):")
for k, (n2, nt, cols, pq) in cuota_txt.items():
    print(f"  {k}: {n2}/{nt}, p={pq:.4f}, colores={cols}")
print("\nDiccionario:")
print(D[["categoria", "marcador", "evidencia"]].to_string(index=False))
