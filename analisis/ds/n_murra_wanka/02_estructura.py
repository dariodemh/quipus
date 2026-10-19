"""02_estructura.py — Estructura del registro wanka: eventos, clústeres, celdas, duplicados.
Salidas: wanka.csv (long: un renglón por cantidad impresa), wanka_grupos.csv (evento x clúster),
resumen_estructura.txt
"""
import os, csv, re
import pandas as pd, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))

d = pd.read_csv("wanka_celdas.csv")

# --- años y orden de eventos -------------------------------------------------
ev = d[["pagina", "evento", "anio", "descripcion", "n_valores"]].copy()
orden = ["a","b","c","ch","d","e","f","g","h","i","j","k","l","ll","m","n","o","p","q"]
assert set(ev.evento) == set(orden), set(ev.evento) ^ set(orden)
ev["i_evento"] = ev.evento.map({e: i for i, e in enumerate(orden)})

# propagar el año visible más cercano (los eventos intermedios no llevan año)
anio = None
anios = []
for _, r in ev.iterrows():
    if pd.notna(r.anio):
        anio = int(r.anio)
    anios.append(anio)
ev["anio_aprox"] = anios

# --- una fila por cantidad impresa ------------------------------------------
cl = {"I":"I","II":"II","III":"III","IV":"IV","V":"V","VI":"VI","VII":"VII",
      "VIII":"VIII","IX":"IX","X":"X","XI":"XI","XII":"XII"}
largo = []
for _, r in d.iterrows():
    vals = str(r.valores)
    vals = [] if vals == "nan" else [float(x) for x in vals.split(";")]
    grupos = r.clusteres.split("+")
    # repartir la secuencia entre los dos clústeres de la página es imposible:
    # se conserva la secuencia completa con la etiqueta del par.
    for k, v in enumerate(vals, start=1):
        largo.append(dict(saya="Hatun Xauxa", evento=r.evento, i_evento=orden.index(r.evento),
                          anio=None, categoria="+".join(grupos), orden_en_grupo=k,
                          cantidad=v, unidad="mixta", columna="desconocida"))
largo = pd.DataFrame(largo)

# años aproximados
largo["anio"] = largo.evento.map(dict(zip(ev.evento, ev.anio_aprox)))
largo = largo[["saya","anio","evento","i_evento","categoria","orden_en_grupo","cantidad","unidad","columna"]]
largo.to_csv("wanka.csv", index=False)

# --- totales por (evento, par de clústeres), formato largo -------------------
NOMBRE = {"I+II":"seres vivos", "III+IV":"textiles y cultivos", "V+VI":"fibra y cerámica",
          "VII+VIII":"aves y vegetales silvestres", "IX+X":"bebida/fruta/sal/pescado + gente",
          "XI+XII":"a la salida: gente, camélidos, comida"}
d["v"] = d.valores.fillna("").apply(lambda s: sum(float(x) for x in s.split(";") if x))
d["n"] = d.valores.fillna("").apply(lambda s: len([x for x in str(s).split(";") if x]))
g = (d.groupby(["evento","clusteres"]).agg(total=("v","sum"), n_celdas=("n","sum"))
       .reset_index())
g["i_evento"] = g.evento.map({e: i for i, e in enumerate(orden)})
g["anio"] = g.evento.map(dict(zip(ev.evento, ev.anio_aprox)))
g["macro"] = g.clusteres.map(NOMBRE)
g = g.sort_values(["i_evento","clusteres"])[["evento","i_evento","anio","clusteres","macro","total","n_celdas"]]
g.to_csv("wanka_grupos.csv", index=False)

# --- resumen ---------------------------------------------------------------
L = []
def p(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)

p("EVENTOS:", len(orden), "| CUERDAS (columnas) declaradas:", 43, "| CLÚSTERES:", 12)
p("Celdas impresas con cantidad:", len(largo), "de", len(orden)*43, "posibles",
  f"({100*len(largo)/(len(orden)*43):.1f} %)")
p("")
p("Por evento: n.º de cantidades y año aproximado")
t = largo.groupby(["i_evento","evento"]).agg(n=("cantidad","size"), suma=("cantidad","sum")).reset_index()
t["anio"] = t.evento.map(dict(zip(ev.evento, ev.anio_aprox)))
p(t.to_string(index=False))
p("")
p("Por clúster: n.º de cantidades, suma bruta (unidades heterogéneas), máximo")
s = largo.groupby("categoria").agg(n=("cantidad","size"), suma=("cantidad","sum"),
                                   maximo=("cantidad","max"), mediana=("cantidad","median"))
p(s.to_string())
p("")
# duplicados de filas completas entre eventos consecutivos
filas = d.groupby("evento").apply(lambda x: tuple(sorted(x.valores.fillna("").tolist())), include_groups=False)
dup = [(a,b) for a,b in zip(orden[:-1], orden[1:]) if filas[a]==filas[b] and filas[a]]
p("Pares de eventos consecutivos con vector de valores IDÉNTICO:", dup)
# también por página
dupp = []
for pg, sub in d.groupby("pagina"):
    sub = sub.set_index("evento").reindex(orden)
    for a, b in zip(orden[:-1], orden[1:]):
        va, vb = str(sub.loc[a,"valores"]), str(sub.loc[b,"valores"])
        if va == vb and va not in ("nan",""):
            dupp.append((pg,a,b,va))
p("Duplicados por página:", dupp)
open("resumen_estructura.txt","w",encoding="utf8").write("\n".join(L))
