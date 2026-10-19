"""Secuencias numéricas de transcripciones coloniales citadas en el material del repo.

Fuentes (todas en analisis/fuentes_txt/):
  - Medrano 2019 (tesis): citas de Pärssinen y Kiviharju (PK), Textos Andinos, con memoria y líneas.
  - Medrano y Urton 2018 (Santa): tabla 2 (padrón 1670).
  - Urton 2017, tabla 11.3 (tributarios de Chachapoyas, de Schjellerup 1997).
Salida: transcripciones_numeros.csv (una fila por cifra) y r1_resumen.txt (calibración por género).
"""
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parent

# (id, memoria, genero_medrano, fuente, [(etiqueta, valor, papel)])
# papel: item = cifra de la lista; total = total declarado; precio = precio unitario; dudoso = cifra corregida en el documento
SEC = [
    ("m4_chupaychos_inca", 4, "pnum (pre, servicio al Inca)", "Medrano 2019:23 = PK I:141 l.55-58, 63-83", [
        ("sembrar chácaras en el Cuzco", 400, "item"), ("yanaconas de Guayna Capac", 150, "item"),
        ("guarda del cuerpo de Topa Inka", 150, "item"), ("guarda de sus armas", 10, "item"),
        ("guarda de los Chachapoyas", 200, "item"), ("guarda de Quito", 200, "item"),
        ("guarda del cuerpo de Guayna Capac", 20, "item"), ("hacer plumas", 120, "item"),
        ("sacar miel", 60, "item")]),
    ("m5_chupaychos_gomez_arias", 5, "pnum (post, entrega a encomendero)", "Medrano 2019:42 = PK I:143-145 l.135-140, 222-224", [
        ("piezas de ropa cada 15 días", 100, "item"), ("piezas al mes (=2x100)", 200, "total"),
        ("piezas cada 15 días en adelante", 80, "item"), ("anaconas e indias de servicio (piezas)", 29, "item")]),
    ("m11_jauja_chicha", 11, "pnum (post)", "Medrano 2019:48 = PK I:202 l.203-204", [
        ("cántaros de chicha (corregido 1233->1033)", 1033, "dudoso")]),
    ("m13_chucuito_ganado", 13, "pnum (post)", "Medrano 2019:48 = PK I:255 l.125-127", [
        ("alpacas y ovejas (1479 corregido a 1514)", 1514, "dudoso")]),
    ("m16_sacaca_aves", 16, "pnum (post, con precios)", "Medrano 2019:47 = PK I:294 l.1169-1173", [
        ("gallinas", 15, "item"), ("precio gallina (pesos)", 1, "precio"), ("patos", 4, "item"),
        ("precio pato (pesos)", 1, "precio"), ("huevos", 540, "item"), ("precio por 100 huevos (pesos)", 5, "precio")]),
    ("m17_sacaca_montemayor", 17, "elicit (post, con precios)", "Medrano 2019:28 = PK I:304-305 l.76-149", [
        ("cargas de chuño", 500, "item"), ("precio carga (pesos)", 6, "precio"), ("carneros de la tierra", 605, "item"),
        ("arrobas de sebo", 20, "item"), ("precio arroba (pesos)", 4, "precio")]),
    ("m22_hinojosa_pilco", 22, "summ (encomienda)", "Medrano 2019:49 = PK II:417 l.193-194", [
        ("Cacajas", 13, "item"), ("Ynputi", 10, "item"), ("Quimayo (diez/cinco)", 5, "dudoso")]),
    ("m40_aldana_aullagas", 40, "summ (encomienda 1540)", "Medrano 2019:31-32 = PK II:151-152 l.36-52", [
        ("total provincia de los Aullagas", 823, "total"), ("con el cacique Acho", 260, "total"),
        ("Acaluo", 38, "item"), ("Berenguela", 18, "item"), ("Millme", 53, "item"), ("Pisquero", 9, "item"),
        ("Yana", 29, "item"), ("Callapa", 17, "item"), ("Taparo", 37, "item"), ("Yanaque", 21, "item"),
        ("Pucuro (chácara del cacique)", 3, "item"), ("Yanaqui (chácara del cacique)", 21, "item"),
        ("Sacina", 14, "item")]),
    ("santa_padron_1670", None, "padrón (revisita 1670)", "Medrano y Urton 2018, tabla 2", [
        ("Namus", 18, "item"), ("Corongo", 23, "item"), ("Cuyuchin", 9, "item"), ("Cusca", 7, "item"),
        ("Guauyan", 41, "item"), ("Ucore", 32, "item"), ("total nombrados", 130, "total")]),
    ("chachapoyas_tributarios", None, "serie temporal (1549-1793)", "Urton 2017, tabla 11.3 (Schjellerup 1997)", [
        ("1549", 17550, "item"), ("1559", 16309, "item"), ("1583", 10699, "item"), ("1586", 8062, "item"),
        ("1591", 7042, "item"), ("1601", 5626, "item"), ("1608", 4000, "item"), ("1793", 2200, "item")]),
]


def tabla():
    rows = []
    for sid, mem, gen, fuente, items in SEC:
        for k, (et, v, papel) in enumerate(items):
            rows.append(dict(secuencia=sid, memoria=mem, genero=gen, fuente=fuente, orden=k, etiqueta=et, valor=v, papel=papel))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    t = tabla()
    t.to_csv(OUT / "transcripciones_numeros.csv", index=False)
    # comprobación aritmética: el subtotal del cacique Acho = suma de sus 11 pueblos
    m40 = t[(t.secuencia == "m40_aldana_aullagas") & (t.papel == "item")].valor
    assert m40.sum() == 260, m40.sum()
    lines = ["Calibración por secuencia (cifras 'item' >= 10):"]
    for sid, g in t[t.papel == "item"].groupby("secuencia", sort=False):
        v = g.valor[g.valor >= 10]
        lines.append(f"  {sid:28s} n={len(g):2d}  >=10: {len(v):2d}  múltiplos de 10: {(v % 10 == 0).sum():2d}"
                     f"  ({(v % 10 == 0).mean() if len(v) else float('nan'):.2f})  rango {g.valor.min()}-{g.valor.max()}"
                     f"  repetidos adyacentes: {(g.valor.diff() == 0).sum()}")
    lines.append("m40: 38+18+53+9+29+17+37+21+3+21+14 = 260 = subtotal declarado ANTES de la lista (total al inicio).")
    (OUT / "r1_resumen.txt").write_text("\n".join(lines), encoding="utf8")
    print("\n".join(lines))
