# -*- coding: utf-8 -*-
"""Mapeo de procedencias a los 12 archivos de la Tabla 2 de Urton & Brezine (2009)."""


def arch12(p):
    p0 = str(p).lower().strip()
    if p0 == "sin" or p0 == "" or p0 == "unknown":
        return "SIN"
    if "leymebamba" in p0:
        return "Laguna de los Condores"
    if "pachac" in p0:
        return "Pachacamac"
    if "puruchuco" in p0:
        return "Puruchuco"
    if "tambo colorado" in p0:
        return "Tambo Colorado"
    if "paracas" in p0 or "puntilla" in p0:
        return "Paracas"
    if "ocucaje" in p0 or "ullujaya" in p0 or "ullujalla" in p0:
        return "Ocucaje"
    if "atarco" in p0:
        return "Atarco"
    if "nazca" in p0 or "nasca" in p0 or "copara" in p0 or "cacatilla" in p0 or "santa clara" in p0:
        return "Nazca"
    if "arica" in p0 or "lluta" in p0 or "miller" in p0:
        return "Arica"
    if "chancay" in p0 or "huando" in p0:
        return "Chancay"
    if p0 == "santa" or "santa rosalia" in p0:
        return "Santa"
    if p0 == "ica" or "ica/" in p0 or "between ica" in p0 or "ica valley" in p0 or "callango" in p0:
        return "Ica"
    return "Otros/vago"
