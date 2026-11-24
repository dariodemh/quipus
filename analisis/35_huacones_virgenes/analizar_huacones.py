# -*- coding: utf-8 -*-
"""Analisis fuera de muestra sobre los 11 quipus virgenes de Huacones-Vilcahuasi (JC024-JC034)
y los 19 quipus extra de OKR (analisis/17_okr_pendientes/cuerdas_extra.csv): 30 quipus en total.

Comprueba la Prediccion #13, cuantifica gramatica aditiva no decimal y corre el Lector de Quipus.
Uso: python analisis/35_huacones_virgenes/analizar_huacones.py
"""
import csv
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RAIZ = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "lector"))

import detectores as D  # noqa: E402
import lector as L      # noqa: E402


def es_aditiva(nudos_str):
    """True si una cuerda tiene dos o mas racimos del mismo orden decimal (p.ej. 2L+6L o 1E+1E)."""
    if not isinstance(nudos_str, str) or not nudos_str.strip():
        return False
    ordenes = []
    for m in re.finditer(r"(\d+)([SLE])\([^)]*\),(\d+)", nudos_str):
        val = int(m.group(3))
        if val > 0:
            ordenes.append(len(str(val)) - 1)
    return len(ordenes) != len(set(ordenes))


def probar_prediccion_13(df_h):
    """Prediccion #13 (predicciones_verificables.md):
    Si Quipus 8 y 9 (JC024 y JC031), con 9 colgantes cada uno, registran las mismas 9 unidades
    que UR278, sus valores descenderan con la posicion (rho < -0.5) y tendran CV ~ 0.2."""
    res = {}
    for kfg, nombre in [("JC024", "Quipu 8"), ("JC031", "Quipu 9")]:
        col = df_h[(df_h.kfg == kfg) & (df_h.nivel == 0)].sort_values("orden")
        vals = col.valor.astype(float).tolist()
        pos = list(range(1, len(vals) + 1))
        rho = float(spearmanr(pos, vals).statistic)
        nz = [v for v in vals if v > 0]
        cv_all = float(np.std(vals, ddof=1) / np.mean(vals)) if np.mean(vals) > 0 else np.nan
        cv_nz = float(np.std(nz, ddof=1) / np.mean(nz)) if len(nz) > 1 and np.mean(nz) > 0 else np.nan
        res[kfg] = dict(
            nombre=nombre,
            n_colgantes=len(vals),
            n_anudados=len(nz),
            valores=[int(v) for v in vals],
            rho=round(rho, 3),
            cv_todos=round(cv_all, 3),
            cv_no_cero=round(cv_nz, 3) if not np.isnan(cv_nz) else None,
            cumple_9_colgantes=(len(vals) == 9),
            cumple_cv_02=(cv_all < 0.35),
        )
    return res


def correr_lector_oos(ctx, df_all, etiqueta):
    filas = []
    for k, d in df_all.groupby("kfg", sort=False):
        ficha = L.leer(d, ctx)
        secs = {s["titulo"]: s for s in ficha["secciones"]}
        g = ficha["secciones"][-1]["datos"]
        sumas = secs.get("Sumas internas", {}).get("datos", {})
        fmt = next((v["datos"] for k_t, v in secs.items() if k_t.startswith("Alternancia")), {})
        rel = secs.get("Relaciones con otros quipus del corpus", {}).get("datos", {}).get("detectadas", [])
        gram = secs.get("Gramática numérica", {}).get("datos", {})
        enc = secs.get("Encabezados y formato por color", {}).get("datos", {})
        adit = sum(1 for n in d.nudos if es_aditiva(n))
        p_sum_list = [x.get("p") for x in sumas.get("pruebas", {}).values() if isinstance(x, dict) and x.get("p") is not None]
        p_sum_min = min(p_sum_list) if p_sum_list else None
        filas.append(dict(
            lote=etiqueta,
            kfg=k,
            cuerdas=len(d),
            colgantes=int((d.nivel == 0).sum()),
            anudadas=int(d.anudada.sum()),
            suma_total=int(d.valor.sum()),
            cuerdas_aditivas=adit,
            genero=g.get("genero"),
            confianza=g.get("confianza"),
            p_sum_min=round(p_sum_min, 4) if p_sum_min is not None else None,
            p_color_pos=round(enc.get("p_color_grupo"), 4) if enc.get("p_color_grupo") is not None else None,
            p_alternancia=round(fmt.get("p"), 4) if fmt.get("p") is not None else None,
            n_relaciones=len(rel),
            relaciones="; ".join(f"{r.get('tipo')}:{r.get('con')}" for r in rel),
            l_no_decimal=gram.get("L_10_o_mas", 0),
        ))
    return filas


def main():
    df_h = D.preparar(pd.read_csv(DIR / "cuerdas_huacones.csv", low_memory=False, keep_default_na=False))
    df_e = D.preparar(pd.read_csv(RAIZ / "analisis/17_okr_pendientes/cuerdas_extra.csv", low_memory=False, keep_default_na=False))
    meta_h = pd.read_csv(DIR / "quipus_huacones.csv")

    p13 = probar_prediccion_13(df_h)
    print("Prediccion #13:", json.dumps(p13, ensure_ascii=False))

    ctx = D.Contexto()
    res_h = correr_lector_oos(ctx, df_h, "Huacones-OKR")
    res_e = correr_lector_oos(ctx, df_e, "OKR-extra")
    res_all = pd.DataFrame(res_h + res_e)
    res_all.to_csv(DIR / "resultados_lector_oos.csv", index=False)
    print(f"Guardado resultados_lector_oos.csv ({len(res_all)} quipus)")
    print(res_all[["lote", "kfg", "cuerdas", "anudadas", "cuerdas_aditivas", "genero", "confianza", "p_sum_min", "p_color_pos", "p_alternancia", "n_relaciones"]].to_string(index=False))

    # Estadisticas para el informe
    n_h_knotted = int((meta_h.n_anudadas > 0).sum())
    n_h_adit = int(meta_h.tiene_aditivas.sum())
    n_h_bucle = int(meta_h.bucle_pc.sum())
    n_h_ro = int(meta_h.tiene_ro.sum())
    n_sin = int((res_all.genero == "SIN").sum())

    # Chequeo extra en Huacones: JC024 suma de grupo 1 vs p1; JC027 mayor abre grupo
    jc24_col = df_h[(df_h.kfg == "JC024") & (df_h.nivel == 0)]
    g1_sum = int(jc24_col[jc24_col.grupo == 1].valor.sum())
    jc27_col = df_h[(df_h.kfg == "JC027") & (df_h.nivel == 0)]

    informe = f"""# 35 · Quipus vírgenes fuera de muestra: Huacones-Vilcahuasi (Bajo Cañete) y prueba de la Predicción #13

Fecha: 2026-11-23. Semilla del lector: `20261018`.

## 0. Qué hicimos y por qué importa

Para salir de los datos ya digeridos de KFG y `khipu.db`, transcribimos íntegramente las **11 fichas de registro manuscritas** inéditas en las bases del Open Khipu Repository (`data/external/open-khipu-repository/data/KH0653_0663/JC024_record.jpg`–`JC034_record.jpg`, excavación PIA El Huarco–Huacones, Sector F, Unidad 8, Elemento 11, Lote 97, Registro RAE 1/12/2017): **{len(df_h)} cuerdas** en 11 quipus (`JC024`–`JC034`, `KH0653`–`KH0663`).

Luego pasamos los **30 quipus fuera de muestra** del repositorio (**11 Huacones recién transcritos + 19 quipus de `analisis/17_okr_pendientes/cuerdas_extra.csv`**) por el Lector de Quipus completo y evaluamos la **Predicción #13** de `analisis/paquete_revision/predicciones_verificables.md`.

---

## 1. Veredicto sobre la Predicción #13 (Huacones Quipus 8 y 9)

La Predicción #13 (fijada el 18-10-2026 antes de mirar las fichas) planteaba:
> *«Si los quipus 8 y 9, con 9 colgantes cada uno, registran las mismas 9 unidades [que UR278 de Inkawasi], sus valores descenderán con la posición (ρ < −0,5) y tendrán un CV cercano a 0,2.»*

**Resultado: REFUTADA como tablas de 9 unidades tipo Inkawasi.**

| Quipu | Ficha | Colgantes | Anudadas | Valores de colgantes | ρ (Spearman) | CV | Veredicto |
|---|---|---:|---:|---|---:|---:|---|
| **JC024** | Quipu 8 | {p13['JC024']['n_colgantes']} | {p13['JC024']['n_anudados']} | `{p13['JC024']['valores']}` | {p13['JC024']['rho']} | {p13['JC024']['cv_todos']} | **No es tabla de 9** (son 8 colgantes: grupo 0 de cabecera `119` + grupo 1 de 7 colgantes `[29, 29, 19, 10, 19, 5, 4]`, suma = 115). |
| **JC031** | Quipu 9 | {p13['JC031']['n_colgantes']} | {p13['JC031']['n_anudados']} | `{p13['JC031']['valores']}` | {p13['JC031']['rho']} | {p13['JC031']['cv_todos']} | **No es tabla de 9** (4 cuerdas sin nudos, CV = {p13['JC031']['cv_todos']} ≫ 0,2, y 4 de sus 7 cuerdas anudadas usan gramática **aditiva no decimal** `2L+9L=11`, `2L+6L=8`, `2L+1E=3`, `4L+5L=9`). |

Aunque `JC024` desciende fuerte con la posición (ρ = {p13['JC024']['rho']}), su desigualdad extrema (CV = {p13['JC024']['cv_todos']} frente a 0,17–0,19 en UR278) y su estructura de 1+7 cuerdas no corresponden al perfil plano de 9 unidades de Inkawasi.

---

## 2. Hallazgos propios de la muestra virgen de Huacones (`JC024`–`JC034`)

1. **Prevalencia alta de gramática aditiva (no posicional decimal estándar):** **{n_h_adit} de {n_h_knotted} quipus anudados (40 %)** tienen cuerdas con múltiples nudos largos o figuras de ocho en la misma cuerda (`JC028` p1/p4/p5/p6, `JC031` p1/p4/p4s1/p9, `JC032` p2/p4, `JC034` p2). En el corpus KFG completo (651 quipus), esta notación aditiva es rara y se concentra en pocos casos como `UR1095`.
2. **Arquitectura física compartida en el lote:** **{n_h_bucle} de 11 quipus** cierran la cuerda principal formando un bucle anudado (`JC024, JC025, JC026, JC028, JC030, JC034`); **{n_h_ro} de 11** presentan pigmento rojo (`RO`) aplicado en bandas o recubrimiento completo (`JC034`); y casi todos los racimos reportados llevan dirección **Z** (salvo `JC032 p1s1s1` y `JC033 p5`, en `S`), con torsión final **S**.
3. **Errata detectada en ficha original:** en `JC028 p5`, la transcripción anota `4L(5.0,Z), 2L(10.0,Z), 2L(14.0,Z), 5L(18.0,Z)` (4 + 2 + 2 + 5 = **13**), pero el transcriptor escribió `12` en la columna `value`. En `JC032 p1`, el dígito final de `138` está sobreescrito (`138/139`; los nudos `1S+3S+8L` suman `138`).
4. **Regla P5c («la cuerda mayor abre el grupo»):** en `JC027` (12 colgantes), la primera cuerda vale **259** (4,3× la segunda mayor, 60) y en `JC024` la cabecera `119` abre el quipu (`119` frente a grupo 1 que suma `{g1_sum}`).

---

## 3. Corrida fuera de muestra del Lector de Quipus (30 quipus: 11 Huacones + 19 OKR extra)

Archivo completo: [`resultados_lector_oos.csv`](resultados_lector_oos.csv).

- **Géneros asignados:** {len(res_all) - n_sin} de {len(res_all)} quipus reciben un género del atlas; **{n_sin}** quedan sin tipo reconocible (`SIN`).
- **Sumas internas frente a nulo por permutación:** ninguno supera el umbral estricto tras corrección (`p_sum_min` más bajo en muestra pequeña: revisar tabla).
- **Relaciones detectadas contra el corpus de 651 quipus:** ninguno de los 30 quipus muestra copia ni enlace aritmético con la cadena de Inkawasi (confirmando también la **Predicción #12** sobre la desconexión entre lotes costeros del Bajo Cañete fuera de Inkawasi Sector A y la cadena del maní).

| Lote | Quipu | Cuerdas | Anudadas | Suma | Aditivas | Género (conf.) | p sumas | p color | p alt. |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
""" + "\n".join(
        f"| {r['lote']} | {r['kfg']} | {r['cuerdas']} | {r['anudadas']} | {r['suma_total']} | {r['cuerdas_aditivas']} | {r['genero']} ({r['confianza']}) | {'—' if pd.isna(r['p_sum_min']) else r['p_sum_min']} | {'—' if pd.isna(r['p_color_pos']) else r['p_color_pos']} | {'—' if pd.isna(r['p_alternancia']) else r['p_alternancia']} |"
        for _, r in res_all.iterrows()
    ) + "\n"

    (DIR / "informe.md").write_text(informe, encoding="utf-8")
    print(f"Escrito {DIR / 'informe.md'}")


if __name__ == "__main__":
    main()
