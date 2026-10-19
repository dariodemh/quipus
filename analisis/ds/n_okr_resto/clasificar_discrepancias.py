"""Clasifica las 21 discrepancias de cuerdas_extra.csv y las 6 de AS1-AS9.db frente a KFG.
Salida: discrepancias_clasificadas.csv
"""
import csv
import os
import re

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# clase, valor propuesto, confianza, causa, evidencia
# (a) error de transcripcion del valor/aportacion; (b) nudo mal registrado;
# (c) cuerda rota/incompleta; (d) indecidible; (e) error de parseo del equipo 17
CASOS = {
    ("KH0631", "p1"): ("b", 404, "media-alta", "grupos de nudos por debajo del nudo largo",
                       "La hoja da 404=100+300+4; los dos ultimos racimos (2S a 12.8 y 4S a 15.8) caen junto/al sur del 4L de 12.7. Probable duplicacion de otra cuerda."),
    ("KH0631", "p4"): ("b", 1375, "alta", "racimo de menos de una unidad",
                       "El 1S(28.0) final aporta 1 tras las unidades (5L a 21.6). Se ignora: 1375."),
    ("KH0631", "p6"): ("b", 259, "alta", "grupos de nudos por debajo del nudo largo",
                       "2S(21.5) y 3L(30.5) estan bajo el 9L(18.0); la hoja suma 200+50+9=259."),
    ("KH0634", "p3"): ("e", 18, "alta", "error de parseo (8L sin parentesis)",
                       "La fuente dice '1S(6.5,S,10), 8L,15.0,S,8'; 10+8=18=valor de la hoja."),
    ("KH0634", "p17s3"): ("a", 29, "media", "valor de la hoja incompleto",
                          "2S(4.5)=20 y 9L(11.0)=9; la hoja solo anota 9."),
    ("KH0635", "p19s2"): ("e", 11, "alta", "error de parseo (1S con '5.0S')",
                          "La fuente tiene 1S(5.0S,10) y 1E(...,1): 11=valor de la hoja."),
    ("KH0635", "p37s2"): ("a", 15, "alta", "aporte del nudo largo mal escrito",
                          "1D aporta 10 y el 5L tiene 5 vueltas (la hoja escribe 9): 10+5=15."),
    ("KH0638", "p3"): ("e", 31, "alta", "error de parseo (coma decimal 25,0)",
                       "3S=30 + 1E=1; la hoja da 31."),
    ("KH0638", "p6"): ("e", 33, "alta", "error de parseo (coma decimal 20,5)",
                       "3S=30 + 3L=3; la hoja da 33."),
    ("KH0638", "p8"): ("e", 13, "alta", "error de parseo (coma decimal 10,0)",
                       "1S=10 + 3L=3; la hoja da 13."),
    ("KH0640", "p5"): ("b", 222, "media-alta", "tipo de nudo mal registrado",
                       "Tres racimos con aportes 200/20/2 pero anotados como 2L; el valor 222 es coherente con las posiciones 3.0/8.0/13.5."),
    ("KH0644", "p1"): ("a", 30, "alta", "aporte del racimo simple mal escrito",
                       "Un unico 3S(8.5) vale 30 (decenas), no 3; la hoja da 30."),
    ("KH0644", "p2"): ("a", 16, "alta", "aporte del racimo simple mal escrito",
                       "1S(9.0) vale 10 + 6L=6; la hoja da 16."),
    ("KH0647", "p19"): ("e", 106, "alta", "error de parseo (parentesis '1S/3.0,S,100)')",
                        "1S=100 + 6L=6; la hoja da 106."),
    ("KH0647", "p21"): ("e", 31, "alta", "error de parseo (1E sin aporte)",
                        "3S=30 + 1E=1; la hoja da 31."),
    ("KH0647", "p26"): ("e", 102, "alta", "error de parseo (2L sin direccion)",
                        "1S=100 + 2L=2; la hoja da 102."),
    ("KH0648", "p6"): ("b", 23, "media-alta", "tipo de nudo mal registrado",
                       "2L(3.5) con aporte 20 deberia ser 2S; 3L(9.0)=3. La hoja da 23."),
    ("KH0648", "p19"): ("e", 29, "alta", "error de parseo (punto por coma 'Z.20')",
                        "2S=20 + 9L=9; la hoja da 29."),
    ("KH0649", "p3"): ("e", 9, "alta", "error de parseo (8L sin parentesis)",
                       "8L=8 + 1E=1; la hoja da 9."),
    ("KH0649", "p18"): ("e", 18, "alta", "error de parseo (1S con '7.0,5,10')",
                        "1S=10 + 1E=1 + 2L=2 + 5L=5; la hoja da 18."),
    ("KH0651", "p6"): ("a", 33, "alta", "aporte del nudo largo mal escrito",
                       "3L tiene 3 vueltas (la hoja escribe 5): 30+3=33."),
}

AS = {
    "AS004": ("b", 4736, "media", "KFG p14 con '100E' (100 nudos) en vez de 1E en centenas; la DB suma 2 porque su TOTAL_VALUE ignora el lugar",
              "Unica diferencia de multiconjunto: DB 2 vs KFG 101. El nudo E tiene knot_value_type=100; 100+1=101. La DB deberia valer 101, no 2. Se mantiene KFG y se corrige la notacion de p14."),
    "AS005": ("d", 179, "baja", "cuatro cuerdas con valores 5,6,7,20 (DB) frente a 3,4,8,9 (KFG)",
              "Sin nombres de cuerda en la DB no se puede alinear. Diferencias pequenas, compatibles con uno o dos nudos mal registrados. Se mantiene KFG."),
    "AS006": ("b", 1604, "baja", "la DB parte un nudo largo de 9 vueltas en dos racimos y desplaza valores",
              "DB extra 2,14,46 / KFG extra 6,52,140; la DB tiene un cordon con 40+3+3 donde KFG tiene 40+9+3. Se mantiene KFG."),
    "AS007": ("d", 2512, "baja", "13 cuerdas con un solo nudo simple: DB lo valora 10, KFG 1",
              "Sin la posicion fisica no se sabe si el nudo esta en decenas o unidades. Se mantiene KFG; quedan ademas 6 cuerdas con diferencias no explicadas (246)."),
    "AS008": ("c", 87638, "media", "la DB tiene una cuerda de 17.612 ausente en KFG; ademas 6 cuerdas con corrimiento de decena",
              "DB extra 17612 (10000+7000+600+10+2); KFG 248 cuerdas vs DB 249. Sumar esa cuerda lleva KFG a 87638; quedan 446 de diferencia."),
    "AS009": ("d", 467, "baja", "un solo nudo simple: DB lo valora 10, KFG 1",
              "Unica diferencia: DB 10 vs KFG 1 en p25 (1S(18.0)). Ambas lecturas son posibles segun la posicion; se mantiene KFG."),
}


def main():
    d = pd.read_csv(os.path.join(RAIZ, "analisis", "17_okr_pendientes", "cuerdas_extra.csv"))
    v = d[d.notas.fillna("").str.contains("VALIDACION")].copy()
    filas = []
    for _, r in v.iterrows():
        cl, prop, conf, causa, ev = CASOS[(r.kfg, r.cuerda)]
        m = re.search(r"suma_nudos=(\d+)", r.notas)
        filas.append({"fuente": "cuerdas_extra.csv", "kfg": r.kfg, "cuerda": r.cuerda,
                      "valor_fuente": int(r.valor), "suma_nudos_fuente": int(m.group(1)),
                      "clase": cl, "valor_propuesto": prop, "confianza": conf,
                      "causa": causa, "evidencia": ev})
    for kh, (cl, prop, conf, causa, ev) in AS.items():
        filas.append({"fuente": "AS1-AS9.db vs KFG", "kfg": kh, "cuerda": "(nivel quipu)",
                      "valor_fuente": "", "suma_nudos_fuente": "", "clase": cl,
                      "valor_propuesto": prop, "confianza": conf, "causa": causa,
                      "evidencia": ev})
    dst = os.path.join(HERE, "discrepancias_clasificadas.csv")
    with open(dst, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(pd.DataFrame(filas).clase.value_counts().to_dict(), "filas", len(filas))


if __name__ == "__main__":
    main()
