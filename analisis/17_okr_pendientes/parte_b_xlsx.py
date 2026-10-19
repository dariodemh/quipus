"""Parte B2: convierte los xlsx de KH0631-KH0702 que NO estan en el KFG local a cuerdas_extra.csv.

Formatos encontrados (ver informe.md):
  - formato KFG (hojas Khipu/PrimaryCord/Clusters/Cords): SH001.xlsx (KH0631), R4303.xlsx (KH0702).
    La logica de lectura de cuerdas es la de scripts/construir_tabla.py (copiada aqui para no tocar el original).
  - formato "recording sheet" (hojas primary_cord/pendant_cords/code_descriptions):
    KH0633_0635 (3 archivos) y KH0638_0652 (14 archivos con pendant_cords; el .15 trae 'wrapped threads').
  - KH0676 (JS01, exportacion KDB, hoja 'Pendant Detail'): sin columna de valor; la regla de decodificacion
    es ambigua ("long knots = their value in parentheses"), NO se convierte. Va a inventario_manual.csv.

Validacion: valor de cada cuerda == suma de los valores de sus racimos de nudos (ultimo numero de cada racimo).
Uso: python -I analisis/17_okr_pendientes/parte_b_xlsx.py
"""
import csv, re, sys, glob, collections
from pathlib import Path

sys.path.append(r"~\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages")
import openpyxl

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data/external/open-khipu-repository/data"
OUT = Path(__file__).resolve().parent
GRUPO_RE = re.compile(r"([\d.]+)cm (?:group of (\d+) \w+ \((\d+)-(\d+)\)(?: space of ([\d.]+)cm)?|1 \((\d+)\))")
CAMPOS = ["kfg", "orden", "cuerda", "tipo", "nivel", "padre", "grupo", "valor", "alt", "nudos", "color",
          "torsion", "union", "largo", "terminacion", "notas"]


def kv(ws):
    """Igual que construir_tabla.kv: pares 'Clave: valor' de la primera columna."""
    d = {}
    for fila in ws.iter_rows(values_only=True):
        v = fila[0] if fila else None
        if isinstance(v, str) and ":" in v and not v.startswith("!"):
            k, _, x = v.partition(":")
            d[k.strip()] = x.strip()
    return d


def valor_nudos(s):
    """Suma el ultimo numero de cada racimo: '3S(7.5,U),30;9L(9.0,U),9' -> 39. None si no hay nudos."""
    if not s or not s.strip():
        return 0
    tot = 0
    for racimo in re.split(r"[;]", s):
        m = re.search(r",\s*(\d+)\s*(\[[^\]]*\])?\s*$", racimo.strip())  # p. ej. ',2[D]' en R4303
        if not m:
            return None
        tot += int(m[1])
    return tot


def valor_nudos_rec(s):
    """Formato de hojas 'recording': '3S(11.0,Z,30), 4L(24.0,Z,4)d' -> 34."""
    if s is None or str(s).strip() in ("", "None"):
        return 0
    tot, n = 0, 0
    for m in re.finditer(r"(\d+)\s*([A-Za-z]+)\(([\d.]+)\s*,\s*([A-Za-z]+)\s*,\s*(\d+)\)", str(s)):
        tot += int(m[5]); n += 1
    return tot if n else None


def nudos_kfg_desde_rec(s):
    """Reescribe a la notacion KFG: '3S(11.0,Z,30), 4L(24.0,Z,4)d' -> '3S(11.0,Z),30;4L(24.0,Z),4'."""
    if s is None or str(s).strip() in ("", "None"):
        return ""
    out = []
    for m in re.finditer(r"(\d+)\s*([A-Za-z]+)\(([\d.]+)\s*,\s*([A-Za-z]+)\s*,\s*(\d+)\)", str(s)):
        out.append(f"{m[1]}{m[2]}({m[3]},{m[4]}),{m[5]}")
    return ";".join(out)


def leer_kfg(path, kh):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    meta = kv(wb["Khipu"])
    grupo_de = {}
    for g, v in enumerate(r[0] for r in wb["Clusters"].iter_rows(values_only=True)
                          if r and r[0] and not str(r[0]).startswith("!")):
        m = GRUPO_RE.match(str(v))
        if not m:
            continue
        a, b = (int(m[3]), int(m[4])) if m[2] else (int(m[6]), int(m[6]))
        for n in range(a, b + 1):
            grupo_de[n] = g
    filas = [r for r in wb["Cords"].iter_rows(values_only=True) if r and any(x is not None for x in r)]
    i0 = next(i for i, r in enumerate(filas) if r[0] == "Cord_Name")
    cab = filas[i0]
    out = []
    for orden, r in enumerate(filas[i0 + 1:]):
        d = dict(zip(cab, r))
        if d.get("Cord_Name") is None:
            continue
        nom = str(d["Cord_Name"])
        m = re.match(r"([a-z]+)(\d+)", nom)
        raiz = int(m[2]) if m else None
        padre = nom[: nom.rfind("s")] if re.search(r"\ds\d", nom) else ""
        out.append({"kfg": kh, "orden": orden, "cuerda": nom, "tipo": m[1] if m else "",
                    "nivel": len(re.findall(r"s\d+", nom)), "padre": padre,
                    "grupo": grupo_de.get(raiz, "") if m and m[1] == "p" else "",
                    "valor": d.get("Value") or "", "alt": d.get("Alt_Value") or "", "nudos": d.get("Knots") or "",
                    "color": d.get("Color") or "", "torsion": d.get("Twist") or "", "union": d.get("Attachment") or "",
                    "largo": d.get("Length") or "", "terminacion": d.get("Termination") or "",
                    "notas": (d.get("Notes") or "").replace("\n", " "), "_val_nudos": valor_nudos(d.get("Knots") or "")})
    return out, meta


def okr_en_hoja(ws):
    """Busca la celda 'OKR Number' en primary_cord y devuelve el KH####."""
    filas = list(ws.iter_rows(values_only=True))
    for i, r in enumerate(filas):
        for x in r:
            if isinstance(x, str) and x.strip().startswith("OKR Number"):
                for rr in filas[i + 1:i + 4]:
                    for y in rr:
                        if isinstance(y, str) and re.search(r"KH\s*\d{4}", y):
                            return "KH" + re.search(r"\d{4}", y)[0]
    return None


def leer_recording(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    kh = okr_en_hoja(wb["primary_cord"])
    if kh is None:  # ficheros 'KHIPU ENLAZADO-MNAAHP.NN': NN = 01..15 -> KH0638..KH0652
        m = re.search(r"MNAAHP\.(\d+)", path.name)
        kh = f"KH{637 + int(m[1]):04d}" if m else None
    filas = list(wb["pendant_cords"].iter_rows(values_only=True))
    cab = [str(c).strip().lower() if c else "" for c in filas[0]]
    idx = {k: i for i, k in enumerate(cab)}
    col = lambda r, nombre: next((r[i] for k, i in idx.items() if k.startswith(nombre)), None)
    out = []
    for orden, r in enumerate(filas[1:]):
        nom = col(r, "cord")
        if nom is None:
            continue
        nom = str(nom).strip()
        if nom.endswith(".0"):
            nom = nom[:-2]
        if not re.match(r"^\d+(s\d+)*$", nom):
            continue
        sp = str(col(r, "spin") or "")
        partes = [x.strip() for x in sp.split("/")]
        nud = col(r, "knots")
        val = col(r, "value")
        largo_raw = str(col(r, "length") or "")
        m = re.match(r"([\d.]+)\s*([A-Za-z]*)", largo_raw)
        val_nud = valor_nudos_rec(nud)
        out.append({"kfg": kh, "orden": orden, "cuerda": "p" + nom,
                    "tipo": "p", "nivel": nom.count("s"),
                    "padre": ("p" + nom[: nom.rfind("s")]) if "s" in nom else "",
                    "grupo": "",
                    "valor": "" if val in (None, "None") else str(int(float(val))),
                    "alt": "", "nudos": nudos_kfg_desde_rec(nud),
                    "color": str(col(r, "color") or "") if col(r, "color") not in (None, "None") else "",
                    "torsion": partes[0] if partes and partes[0] else "",
                    "union": partes[-1] if len(partes) > 2 else "",
                    "largo": m[1] if m else "", "terminacion": m[2] if m else "",
                    "notas": ("clasificacion: " + str(col(r, "cord classification"))) if col(r, "cord classification") not in (None, "") else "",
                    "_val_nudos": val_nud})
    # grupos (colgantes): cluster ordinal -> rango de cordones (BEG_CORD, NUM_CORDS)
    pc = list(wb["primary_cord"].iter_rows(values_only=True))
    cab_cl = next(((i, list(r)) for i, r in enumerate(pc) if r and r[0] == "ORDINAL"), None)
    if cab_cl:
        fila_cl, cab_cl = cab_cl
        ib, inn = cab_cl.index("BEG_CORD"), cab_cl.index("NUM_CORDS")
        cluster_de = {}
        for r in pc[fila_cl + 1:]:
            if r and isinstance(r[0], (int, float)) and r[ib] is not None:
                beg, n = int(r[ib]), int(r[inn])
                for k in range(beg, beg + n):
                    cluster_de[k] = int(r[0]) - 1
        for row in out:
            if row["nivel"] == 0:
                row["grupo"] = cluster_de.get(int(row["cuerda"][1:]), "")
    return kh, out


def main():
    filas = []
    resumen = []
    fuentes = [
        ("KH0631", DATA / "KH0631_0632/SH001.xlsx", "kfg"),
        ("KH0702", DATA / "KH0702/R4303.xlsx", "kfg"),
    ]
    for f in sorted(glob.glob(str(DATA / "KH0633_0635/*.xlsx"))) + sorted(glob.glob(str(DATA / "KH0638_0652/*.xlsx"))):
        fuentes.append((None, Path(f), "rec"))
    for kh, path, tipo in fuentes:
        if tipo == "kfg":
            cuerdas, meta = leer_kfg(path, kh)
            for c in cuerdas:
                c["notas"] = (f"fuente: {path.name}; KFG Investigator_Num={meta.get('Investigator_Num','')}; "
                              f"museo={meta.get('Museum Number','')}; " + c["notas"]).strip("; ")
        else:
            hojas = openpyxl.load_workbook(path, read_only=True).sheetnames
            if "pendant_cords" not in hojas:
                resumen.append((kh or "?", path.name, 0, 0, 0, "omitido: sin hoja pendant_cords (" + ", ".join(hojas) + ")"))
                continue
            kh, cuerdas = leer_recording(path)
            for c in cuerdas:
                c["notas"] = f"fuente: {path.name}; " + c["notas"]
        ok = mal = sin = 0
        for c in cuerdas:
            vn = c.pop("_val_nudos")
            try:
                v = int(float(c["valor"])) if c["valor"] != "" else 0
            except ValueError:
                v = None
            if vn is None or v is None:
                sin += 1
            elif vn == v:
                ok += 1
            else:
                mal += 1
                c["notas"] = (c["notas"] + f"; VALIDACION: valor={c['valor']} suma_nudos={vn}").strip("; ")
        resumen.append((kh, path.name, len(cuerdas), ok, mal, sin))
        filas.extend(cuerdas)
    # cuerdas de KH0633-35 y KH0638-52 llevan KH en la hoja; si falta, avisar
    with open(OUT / "cuerdas_extra.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, extrasaction="ignore")
        w.writeheader()
        w.writerows(filas)
    print("KH | archivo | cuerdas | valor=suma nudos | discrepancias | sin comprobar")
    for r in resumen:
        print(" | ".join(str(x) for x in r))
    conv = [r for r in resumen if r[2] > 0]
    print("TOTAL |", len(conv), "quipus convertidos |", sum(r[2] for r in conv), "cuerdas |",
          sum(r[3] for r in conv), "validadas OK |", sum(r[4] for r in conv), "discrepancias |",
          sum(r[5] for r in conv), "sin comprobar")
    print("total cuerdas_extra.csv:", len(filas), "filas;", len({(r["kfg"], r["cuerda"]) for r in filas}), "claves kfg+cuerda unicas")


if __name__ == "__main__":
    main()
