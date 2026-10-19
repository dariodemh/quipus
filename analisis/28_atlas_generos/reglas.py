# -*- coding: utf-8 -*-
"""Reglas jerarquicas explicitas del atlas de generos.

Cada regla mira solo columnas de matriz.csv y devuelve (nivel, lineas, texto):
nivel 3 = alta, 2 = media, 1 = baja; `lineas` = cuantas lineas de evidencia
independientes la apoyan. Asignacion: el genero de mayor nivel; empate -> el de
mas arriba en ORDEN (el mas especifico). Umbrales en U (perillas explicitas).
"""
import numpy as np, pandas as pd

ORDEN = ["CAL", "NAZ", "ARC", "PAD", "FOR", "NON", "TAL", "SUM", "ASG", "TAB", "SEG"]
NOMBRE = {
    "CAL": "Calendario (tipo UR006)",
    "NAZ": "Ficha con encabezado y par marcador (Nazca/Berlin)",
    "ARC": "Archivo jerarquico con relaciones entre quipus (Incahuasi, Puruchuco)",
    "PAD": "Padron por persona (tipo Santa 1670)",
    "FOR": "Formulario con clave de reparto",
    "TAL": "Registro aditivo/tally (torsion Z)",
    "NON": "No numerico (sin nudos o nudos no axiales)",
    "SUM": "Contabilidad decimal con totales internos",
    "ASG": "Lista de asignacion (cifras redondas, cuotas)",
    "TAB": "Tabla de recuento (unidades x categorias)",
    "SEG": "Lista segmentada (solo formato: color por grupo, marcadoras)",
    "SIN": "Sin genero",
}
CONF = {3: "alta", 2: "media", 1: "baja"}
# umbrales (perillas): se mueven +-25 % en la prueba de sensibilidad
U = dict(nodec=0.5, nodec_baja=0.25, Z=0.5, camel=0.5, red=0.8, rho=0.3, anud_non=0.2,
         rota_pobre=0.5, anud_min=10, ncuerdas_min=10)
NAZ_HOLM = {"UR1140", "UR1131", "UR234"}       # pasan Holm en n_ficha_nazca
SUAVES = {"FOR", "TAL", "NON", "ASG", "TAB", "SEG"}  # se rebajan un nivel con datos pobres


def _lt(x, t):
    return pd.notna(x) and x < t


def _ge(x, t):
    return pd.notna(x) and x >= t


def reglas(k, r, u=U):
    out = {}
    cop = r.copias if isinstance(r.copias, str) else ""
    # CAL ------------------------------------------------------------------
    if _lt(r.calend_q, .05):
        out["CAL"] = (3, 2, f"plantilla calendario P8ar q={r.calend_q:.3f}; Urton 2017 (24 pares de conjuntos, 730 cuerdas)")
    elif "UR006" in cop:
        out["CAL"] = (2, 1, "copia de UR006 (04/14_copias); P8ar no lo reconoce por si solo")
    # NAZ ------------------------------------------------------------------
    if pd.notna(r.nazca_p):
        mk = _ge(r.okr_marcadoras, 1)
        if k in NAZ_HOLM:
            out["NAZ"] = (3, 2 + mk, f"ficha encabezado+par marcador, pasa Holm (barrido p_holm={r.nazca_p:.1e})")
        elif r.nazca_p < .05:
            out["NAZ"] = (2, 1 + mk, f"ficha detectada (p_holm={r.nazca_p:.1e}); ficha completa no confirmada")
        else:
            out["NAZ"] = (1, 1, "candidato del barrido de ficha que no pasa")
    # ARC ------------------------------------------------------------------
    if r.rel_archivo == "demostrada":
        n = 1 + bool(r.trio_xcx) + _lt(r.sumas_q, .05) + bool(cop)
        ev = "relacion numerica con otros quipus demostrada (13/04/n_puruchuco_pacha)"
        ev += "; trio [x,c,x-c]" if r.trio_xcx else ""
        ev += f"; sumas internas q={r.sumas_q:.3f}" if _lt(r.sumas_q, .05) else ""
        out["ARC"] = (3, n, ev)
    elif r.rel_archivo == "propuesta":
        out["ARC"] = (2, 1, "relacion con otros quipus propuesta, no demostrada")
    # PAD ------------------------------------------------------------------
    if _lt(r.santa_q, .05) and r.procedencia == "Santa":
        out["PAD"] = (3, 2, f"formato P4r (grupos monocromos alternos) q={r.santa_q:.4f} + archivo del padron del Santa (Radicati)")
    elif r.procedencia == "Santa":
        out["PAD"] = (2, 1, "archivo del Santa sin formato P4r")
    elif _lt(r.santa_q, .05) and _lt(r.santa_pcorpus, .05):
        out["PAD"] = (1, 1, f"formato P4r q={r.santa_q:.4f}, destaca sobre el corpus (p={r.santa_pcorpus:.3f}); no replica tras Holm")
    # FOR ------------------------------------------------------------------
    if r.form_archivo == "demostrado-local":
        out["FOR"] = (3, 2, f"clave local demostrada en el archivo (22_formularios); deteccion {r.form_Q}")
    elif r.form_archivo == "apoyado-indeterminado" and r.form_Q != "no":
        out["FOR"] = (2, 2, f"formulario {r.form_Q} y clave de archivo apoyada (22_formularios)")
    elif r.form_Q != "no" and _lt(r.form_holm, .05):
        out["FOR"] = (2, 1, f"formulario {r.form_Q}, Holm={r.form_holm:.3f}")
    elif r.form_Q != "no":
        out["FOR"] = (1, 1, f"formulario {r.form_Q} (BH q={r.form_qbh:.3f}, no Holm)")
    # TAL ------------------------------------------------------------------
    lines = [_ge(r.frac_nodec, u["nodec"]), _ge(r.frac_Z, u["Z"]), _ge(r.okr_frac_camelido, u["camel"]),
             r.vueltas10 > 0, bool(r.pure_tally) or (isinstance(r.nonum_subtipo, str) and "seq" in r.nonum_subtipo)]
    txt = (f"{r.frac_nodec:.0%} cuerdas no decimales" if pd.notna(r.frac_nodec) else "") + \
          (f"; torsion Z {r.frac_Z:.0%}" if pd.notna(r.frac_Z) else "") + \
          (f"; camelido {r.okr_frac_camelido:.0%}" if pd.notna(r.okr_frac_camelido) else "") + \
          (f"; {int(r.vueltas10)} nudos de >=10 vueltas" if r.vueltas10 > 0 else "") + \
          ("; tally puro (n_no_numericos)" if lines[4] else "")
    if lines[0] and r.n_cuerdas >= u["ncuerdas_min"]:
        st0 = r.nonum_subtipo if isinstance(r.nonum_subtipo, str) else ""
        tope = 2 if ("NU" in st0 or "NC" in st0) else 3   # morfologia no axial: no es tally decimal-aditivo seguro
        out["TAL"] = (min(tope, 3 if sum(lines) >= 3 else 2), sum(lines), txt)
    elif _ge(r.frac_nodec, u["nodec_baja"]) and any(lines[1:4]):
        out["TAL"] = (1, sum(lines) + 1, txt)
    # NON ------------------------------------------------------------------
    st = r.nonum_subtipo if isinstance(r.nonum_subtipo, str) else ""
    if "NC" in st or "NU" in st:
        out["NON"] = (2, 1 + (r.frac_anudada < .5), f"clase no numerica {st} (n_no_numericos); {r.frac_anudada:.0%} cuerdas anudadas")
    elif r.frac_anudada < u["anud_non"] and r.n_cuerdas >= u["ncuerdas_min"] and r.frac_rota < .3:
        out["NON"] = (1, 1, f"solo {r.frac_anudada:.0%} de cuerdas anudadas con {r.frac_rota:.0%} rotas")
    # SUM ------------------------------------------------------------------
    s1, s2 = _lt(r.sumas_q, .05), _lt(r.filatotal_q, .05)
    if s1 or s2:
        ev = (f"sumas locales robustas a M1 y M2 q={r.sumas_q:.3f}" if s1 else "") + \
             ("; " if s1 and s2 else "") + (f"fila + total suelto q={r.filatotal_q:.3f}" if s2 else "")
        out["SUM"] = (3, s1 + s2, ev)
    elif _lt(r.sumas_q_M1, .05) or r.sumas_01:
        out["SUM"] = (2, 1, "sumas solo con el nulo M1" if _lt(r.sumas_q_M1, .05) else "cuerdas superiores o cierre (01)")
    # ASG ------------------------------------------------------------------
    red = _ge(r.red_frac, u["red"])
    cuo = _lt(r.cuotas_rep_q, .05)
    if red and _lt(r.red_q, .05) and cuo:
        out["ASG"] = (3, 2, f"{r.red_frac:.0%} cifras redondas (n={int(r.red_n)}) y cuotas repetidas q={r.cuotas_rep_q:.3f}")
    elif red and _lt(r.red_q, .05):
        out["ASG"] = (2, 1, f"{r.red_frac:.0%} cifras redondas (n={int(r.red_n)}, q={r.red_q:.3f})")
    elif cuo and _ge(r.red_frac, .5):
        out["ASG"] = (2, 2, f"cuotas repetidas q={r.cuotas_rep_q:.3f} con {r.red_frac:.0%} redondas")
    elif red:
        out["ASG"] = (1, 1, f"{r.red_frac:.0%} cifras redondas pero n={int(r.red_n)} (q={r.red_q:.2f})")
    # TAB ------------------------------------------------------------------
    if pd.notna(r.tabla_R):
        l = [_lt(r.tabla_q_orden, .05), _ge(r.tabla_rho, u["rho"]), _lt(r.red_frac, .5)]
        out["TAB"] = (2 if sum(l) >= 2 else 1, sum(l) + 1,
                      f"tabla {int(r.tabla_R)}x{int(r.tabla_K)}" + ("; 1.a columna mayor" if l[0] else "") +
                      (f"; filas coescalan rho={r.tabla_rho:.2f}" if l[1] else "") + ("; no redonda (recuento)" if l[2] else ""))
    # SEG ------------------------------------------------------------------
    l = [_lt(r.color_grupo_p, .05), _ge(r.okr_marcadoras, 2), _lt(r.segm_q, .05)]
    if any(l):
        out["SEG"] = (2 if sum(l) == 3 else 1, sum(l),
                      "; ".join(t for t, b in zip(["color marca el grupo (NMI>nulo)", f"{r.okr_marcadoras:.0f} marcadoras OKR",
                                                   "bloques repetidos P11a"], l) if b))
    # rebaja por datos pobres ---------------------------------------------
    n_anud = r.n_cuerdas * r.frac_anudada
    pobre = n_anud < u["anud_min"] or (r.frac_rota > u["rota_pobre"] and n_anud < 3 * u["anud_min"])
    for g in list(out):
        if pobre and g in SUAVES and g != "NON":
            lv, n, t = out[g]
            out[g] = (lv - 1, n, t + " [rebajado: datos pobres]")
            if lv - 1 <= 0:
                del out[g]
    return out, pobre


def clasificar(M, u=U):
    filas = []
    for k, r in M.iterrows():
        out, pobre = reglas(k, r, u)
        if out:
            g = sorted(out, key=lambda x: (-out[x][0], ORDEN.index(x)))[0]
            lv, n, t = out[g]
            sec = "; ".join(f"{x}({CONF[out[x][0]]})" for x in ORDEN if x in out and x != g)
            filas.append(dict(kfg=k, genero=g, nivel=lv, confianza=CONF[lv], lineas=n, ev=t, secundarios=sec, pobre=pobre))
        else:
            filas.append(dict(kfg=k, genero="SIN", nivel=0, confianza="sin genero", lineas=0,
                              ev="datos insuficientes" if pobre else "decimal sin estructura detectada",
                              secundarios="", pobre=pobre))
    return pd.DataFrame(filas).set_index("kfg")


if __name__ == "__main__":
    # autocomprobacion minima: controles positivos conocidos
    M = pd.read_csv(r"./analisis/28_atlas_generos/matriz.csv", index_col=0)
    A = clasificar(M)
    esperado = {"UR006": "CAL", "UR1140": "NAZ", "UR278": "ARC", "UR068": "ARC", "UR087": "PAD",
                "UR053A": "FOR", "UR193": "TAL", "UR118": "SUM"}
    for k, g in esperado.items():
        assert A.loc[k, "genero"] == g, (k, A.loc[k].to_dict())
    print("controles positivos OK:", esperado)
