# -*- coding: utf-8 -*-
"""05. Control de plausibilidad del volumen de Qolqawasi y comparacion con otros
sitios incas de almacenamiento. Solo aritmetica sobre dimensiones publicadas.
"""
import numpy as np
from comun import VOL_SITIO_M3, N_CAMARAS, N_COLCAS

print("=== 1. Descomposicion del volumen de Qolqawasi (6 400 m3, 245 unidades) ===")
for lado, h in [(2.0, 1.3), (2.0, 1.8), (2.5, 1.8)]:
    v_bin = lado * lado * h
    v_cam = (VOL_SITIO_M3 - N_COLCAS * v_bin) / N_CAMARAS
    print(f"   colca {lado}x{lado}x{h} m = {v_bin:4.1f} m3 -> "
          f"{N_COLCAS} colcas = {N_COLCAS*v_bin:5.0f} m3; "
          f"quedan {v_cam:6.1f} m3 por camara grande (36)")
print("   una camara de 112-148 m3 = 15 x 5-6 m x 1,5-1,8 m de carga; plausible")
print()

print("=== 2. Volumen por unidad: Qolqawasi frente a la qolqa redonda de altura ===")
print(f"   Qolqawasi: 6 400/245 = {VOL_SITIO_M3/245:.1f} m3 por unidad (media, dominated by 36 salas)")
diam = 3.23
for h in [1.5, 2.0, 2.5]:
    v = np.pi * (diam / 2) ** 2 * h
    print(f"   qolqa redonda d=3,23 m, altura {h} m -> {v:4.1f} m3 geometricos")
print("   D'Altroy (1992:175) da 3,7-5,5 m3 por qolqa pequena, cifra INCOMPATIBLE con")
print("   un cilindro de 3,23 m de diametro y 2 m de alto (16 m3): la cifra de D'Altroy")
print("   debe de referirse a la parte util de un silo estrecho o a otra clase de estructura.")
print("   => NO uso 3,7-5,5 m3 para extrapolar; solo comparo numero de unidades.")
print()

print("=== 3. Numero de unidades de almacenamiento ===")
sitios = [("Qolqawasi (Incahuasi)", 245, "36 salas + 209 colcas; Urton 2017"),
          ("Huanuco Pampa", 497, "Morris & Thompson 1970"),
          ("Mantaro", 2573, "LeVine 1992; D'Altroy 2003"),
          ("Cotapachi (Cochabamba)", 2400, "D'Altroy 2003"),
          ("Paria", 1000, "Faldin et al. 2010")]
for s, n, ref in sitios:
    print(f"   {s:24s} {n:5d} unidades   ({ref})")
print("   Qolqawasi tiene la MITAD de las unidades de Huanuco Pampa y 1/10 de las del Mantaro,")
print("   pero sus unidades son mucho mayores (26 m3 de media): 6 400 m3 es plausible.")
print()

print("=== 4. Sensibilidad: y si 6 400 m3 fuera 3x demasiado? ===")
for f in [1.0, 0.5, 0.33]:
    cap = VOL_SITIO_M3 * f
    print(f"   capacidad {cap:5.0f} m3 -> masa 0,40-0,70: {cap*0.4:5.0f}-{cap*0.7:5.0f} t; "
          f"ledger maestro a 25 kg ({122609*25/1000:5.0f} t) = "
          f"{122609*25/1000/(cap*0.7):.2f}-{122609*25/1000/(cap*0.4):.2f} llenados")
print("   Aun con 1/3 del volumen, un ledger de 122 609 bultos de 25 kg son 2-4 llenados:")
print("   sigue siendo un archivo de deposito, no un registro de raciones ni de items.")
