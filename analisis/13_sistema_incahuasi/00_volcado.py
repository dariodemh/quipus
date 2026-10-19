"""Vuelca los 52 quipus del archivo de Incahuasi, grupo a grupo, a volcado_archivo.txt."""
import comun13 as C

c, q = C.archivo()
with open(C.AQUI / "volcado_archivo.txt", "w", encoding="utf-8") as f:
    for k in C.ARCHIVO:
        C.volcar(c, k, f)
