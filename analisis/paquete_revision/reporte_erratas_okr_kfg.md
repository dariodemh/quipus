# Reporte de erratas detectadas en OKR (v2.1.0) y KFG (v2.1.0)

Resumen técnico de inconsistencias, duplicados y errores de codificación verificados en las dos bases abiertas del corpus digital, listo para reportarse como *issues* en los repositorios originales (`open-khipu-repository` y `data-science-khipu-article` / KFG).

---

## 1. Colisiones de números KH y archivos desplazados en KFG (`KFG_DB_Excel/`)

| ID / Archivo | Problema verificado | Evidencia |
|---|---|---|
| `KH0197.xlsx` | El archivo Excel contiene un quipu distinto del que corresponde a `KH0197`; colisiona con `UR1180` | `analisis/17_okr_pendientes/informe.md` §1.4; `tabla_hallazgos.csv` (`C26`) |
| `KH0227.xlsx` | Colisión de KH: asignado a `KH0227` (221 cuerdas, Huaura) y a `AS207C` (14 cuerdas, `C14459`) | `17_okr_pendientes/puente.csv`; `resumen_para_especialista.md` §5.9 |
| `KH0267.xlsx` | Colisión de KH: `KH0267` (22 cuerdas) y `UR034` (188 cuerdas) comparten número KH | `17_okr_pendientes/informe.md` §1.4 |
| `KH0350.xlsx` | Colisión de KH: `KH0350` (55 cuerdas) y `UR114` (260 cuerdas) comparten número KH | `17_okr_pendientes/informe.md` §1.4 |
| `UR044.xlsx` | Duplicado incompleto del quipu `AS031 / KH0033` (66 cuerdas, marcado como duplicado en OKR) | `khipu_summary.csv` tiene 650 filas (excluye `UR044`) frente a 651 `.xlsx` |
| `KFG_DB.SQL` vs CSV/XLSX | `khipu_main` en SQL tiene **685** filas, `KFG_DB_Excel/` tiene **651** `.xlsx` y `khipu_summary.csv` **650** | Explicación exacta (650 + 35) en `17_okr_pendientes/informe.md` §1.5 |

## 2. Duplicados no señalados y errores de inventario entre objetos

* **`UR1107` (`KH0121`, Berlín `VA24370(B)`) = `UR237` (`KH0473`, Berlín `VA66834`):** coinciden en **23 de 26** valores con nudos en orden invertido (`r` de largos = **0,99**), pero **0 de 23** etiquetas de color coinciden (`analisis/14_copias/verificacion_UR1107_UR237.csv`). Son dos transcripciones del mismo objeto leídas en sentidos opuestos; el inventario `VA66834` en `KH0473` difiere de `VA24370`.
* **`KH0676` (`JS01`, Brooklyn `36.718`) vs `KH0700` (`SB001`):** el número de museo `80.1012 aka 2708` aparece asignado tanto a `KH0676` como a `KH0700` (`17_okr_pendientes/informe.md` §1.6; `resumen_para_especialista.md` §3.1).

## 3. Pérdidas sistemáticas de KFG respecto a OKR (`khipu.db`)

* **Cuerdas perdidas en Inkawasi:** KFG pierde **111 cuerdas** presentes en OKR en la muestra de Inkawasi, incluidas **58 cuerdas de `UR256`** y **32 subsidiarias de `UR274B`** (`resumen_para_especialista.md` §1).
* **Cuerdas superiores y marcadoras:** KFG pierde **92 de 95** cuerdas superiores de nivel 1 y **502 de 502** cuerdas marcadoras (`resumen_para_especialista.md` §1), por lo que todo análisis de `T` o marcadoras requiere leer `khipu.db` directamente.
* **Discrepancias numéricas concentradas:** KFG y OKR coinciden al **99,33 %** en cuerdas con nudos, pero el **86 %** de las discrepancias se concentra en cinco quipus (`UR090`, `UR144`, `UR235`, `UR193`, `UR190`), la mitad por desplazamiento de factor `×10`.

## 4. Inconsistencias internas en OKR (`data/khipu.db` y carpetas auxiliares)

* **`AS001–AS009` fuera de `khipu.db`:** los nueve quipus están únicamente en `KH0002_0010/AS1-AS9.db` (`681` cuerdas, `1872` nudos), ausentes de `khipu.db` (`619` quipus).
* **Datos sueltos sin integrar:** `83` números KH de `okr-kh-numbers.csv` (`702` filas reales) no están en `khipu.db`; `19` están en `.xlsx` convertibles (`cuerdas_extra.csv`, `776` cuerdas) y `11` (`KH0653–KH0663`, Huacones `JC024–JC034`) solo como fotos (`analisis/35_huacones_virgenes/`).
* **Codificación dañada en `okr-kh-numbers.csv`:** contiene caracteres de reemplazo UTF-8 (`U+FFFD`) y saltos de línea dentro de celdas entrecomilladas (`761` líneas físicas para `702` filas).
* **Errata aritmética en ficha manuscrita `JC028_record.jpg` (`KH0657`, cuerda `p5`):** los nudos aditivos `4L + 2L + 2L + 5L` suman **13**, pero la columna `value` de la hoja anota **12**.
