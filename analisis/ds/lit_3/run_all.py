"""Ejecuta todas las pruebas de lit_3 y guarda la salida en resultados.txt.

Uso:  python run_all.py
"""
import io
import os
import runpy
import sys
import contextlib

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["t1_ur028.py", "t2_ur267a.py", "t3_santa.py",
           "t4_direccion_nudos.py", "t5_torsion.py", "t6_metadatos.py",
           "t7_color_okr.py"]

buf = io.StringIO()
for s in SCRIPTS:
    buf.write("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78 + "\n")
    ruta = os.path.join(AQUI, s)
    with contextlib.redirect_stdout(buf):
        runpy.run_path(ruta, run_name="__main__")

salida = buf.getvalue()
print(salida)
with open(os.path.join(AQUI, "resultados.txt"), "w", encoding="utf-8") as f:
    f.write(salida)
print("\n[guardado en resultados.txt]")
