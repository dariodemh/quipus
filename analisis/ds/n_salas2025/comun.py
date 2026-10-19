# -*- coding: utf-8 -*-
"""Carga y limpieza comunes para las pruebas de Salas García (2025)."""
import re
import pandas as pd
import numpy as np

RAIZ = r"."


def cargar():
    c = pd.read_csv(RAIZ + r"\analisis\datos\cuerdas.csv",
                    usecols=["kfg", "orden", "cuerda", "nivel", "grupo",
                             "valor", "nudos", "color"])
    q = pd.read_csv(RAIZ + r"\analisis\datos\quipus.csv")
    # color: quitar rangos en cm, p.ej. "MB(0.0-33.0)"
    c["color"] = (c["color"].fillna("U").astype(str)
                  .str.replace(r"\([^)]*\)", "", regex=True).str.strip())
    c["color_base"] = c["color"].str.split(r"[:/\-]", regex=True).str[0]
    c["color_base"] = c["color_base"].replace("", "U")
    # cuerda con nudos registrados (distinto de 0 ausente)
    c["con_nudos"] = c["nudos"].notna() & (c["nudos"].astype(str).str.strip() != "")
    c["v"] = pd.to_numeric(c["valor"], errors="coerce")
    c["valida"] = c["con_nudos"] & c["v"].notna() & (c["v"] >= 0)
    c["vi"] = np.where(c["valida"], c["v"], np.nan)
    c["u"] = c["vi"] % 10
    c["t"] = (c["vi"] // 10) % 10
    c["h"] = (c["vi"] // 100) % 10
    c["par"] = (c["u"] % 2 == 0)
    c["u0"] = (c["u"] == 0)
    c["c100"] = (c["vi"] >= 100) & (c["u"] == 0) & (c["t"] == 0)
    # macro-región a partir de procedencia (nunca museo)
    c = c.merge(q[["kfg", "procedencia", "region"]], on="kfg", how="left")
    c["macro"] = c["procedencia"].map(macro_region)
    return c, q


def macro_region(p):
    s = "" if pd.isna(p) else str(p).lower()
    # territorio mochica / yunga histórica: La Libertad, Lambayeque, Piura, Tumbes
    norte = ["trujillo", "lambayeque", "moche", "chimu", "chimú", "piura",
             "tumbes", "chiclayo", "pacasmayo", "zaña", "zana", "jequetepeque",
             "virú", "viru", "pacatnamu", "pacatnamú", "ferreñafe", "morrope",
             "mórrope", "jayanca", "motupe", "olmos", "sechura", "tumbes"]
    norcentral = ["santa", "huarmey", "casma", "nepeña", "nepena", "huacho",
                  "huaura", "barranca", "paramonga", "fortaleza"]
    central = ["pachacamac", "lima", "rimac", "ríma", "armatambo", "maranga",
               "puruchuco", "la molina", "cieneguilla", "lurin", "lurín",
               "chancay", "huando", "chuquitanta", "cajamarquilla",
               "pueblo libre", "huaca", "central"]
    sur = ["ica", "nazca", "pisco", "paracas", "ocucaje", "ullujaya",
           "callango", "acari", "atarco", "marquez", "tambo colorado",
           "chile", "lluta", "arica", "quillagua", "loa", "sur"]
    sierra = ["chachapoyas", "leymebamba", "cuzco", "cusco", "huari",
              "mollepampa", "solar", "incahuasi"]
    if any(k in s for k in norte):
        return "costa_norte_yunga"
    if "santa clara" in s:
        return "costa_sur"
    if any(k in s for k in norcentral):
        return "costa_norcentral"
    if any(k in s for k in sierra):
        return "sierra_selva"
    if any(k in s for k in sur):
        return "costa_sur"
    if any(k in s for k in central):
        return "costa_central"
    return "desconocida"


def bh_holm(p):
    """Devuelve p ajustados BH y Holm para una lista/array."""
    p = np.asarray(p, float)
    n = len(p)
    orden = np.argsort(p)
    ps = p[orden]
    # Holm
    holm = np.empty(n)
    prev = 0.0
    for i, val in enumerate(ps):
        prev = max(prev, min(1.0, (n - i) * val))
        holm[i] = prev
    # BH
    bh = np.empty(n)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        prev = min(prev, ps[i] * n / (i + 1))
        bh[i] = prev
    out_h = np.empty(n); out_b = np.empty(n)
    out_h[orden] = holm; out_b[orden] = bh
    return out_h, out_b
