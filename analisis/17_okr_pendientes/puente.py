"""Parte A: tabla puente KH (OKR) <-> AS/UR <-> KFG <-> khipu.db.

Salidas (en esta carpeta): puente.csv (una fila por KH) y puente_conteos.txt (resumen).
Solo stdlib. Ejecutar: python -I analisis/17_okr_pendientes/puente.py (desde la raiz del repo).

Reglas de normalizacion de alias (documentadas en informe.md):
  R1 separar tokens por ',' y '/'; quitar espacios sobrantes.
  R2 prefijo de 2 letras + numero: el numero se rellena a 3 cifras (UR1 -> UR001, UR44 -> UR044).
     Numeros de 4 cifras (UR1031, UR1107) se conservan: en khipu.db son etiquetas distintas
     (p. ej. UR1031 y UR044 aparecen juntos en KH0033 y son registros distintos).
  R3 sufijo de una o dos letras entre parentesis o pegado: AS063(A) -> AS063A.
  R4 calificadores (" - Part 1", " Detail 2") se quitan del alias y no se usan para emparejar.
  R5 para emparejar con KFG se compara la clave nk = solo alfanumerico en mayusculas
     (KFG usa '_' donde el OKR usa '/' o espacios: AS061_MA036 = AS061/MA036).
"""
import csv, re, sqlite3, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data/external/open-khipu-repository/data"
OUT = Path(__file__).resolve().parent
OKR_CSV = DATA / "okr-kh-numbers.csv"
KHDB = DATA / "khipu.db"
SUMMARY = RAIZ / "data/external/data-science-khipu-article/data/khipu_summary.csv"
SQLDUMP = RAIZ / "data/external/data-science-khipu-article/data/KFG_DB.SQL"
QUIPUS = RAIZ / "analisis/datos/quipus.csv"


def nk(s):
    return re.sub(r"[^A-Za-z0-9]", "", s).upper()


def norm(tok):
    """Devuelve (alias_normalizado, calificador, clave_nk) para un token."""
    t = tok.strip()
    calif = ""
    m = re.match(r"^(.*?)\s+((?:-\s*)?(?:Part|Detail)\s*\d+)$", t, re.I)
    if m:
        t, calif = m[1].strip(), m[2].strip()
    m = re.match(r"^([A-Za-z]{2})\s*(\d+)\s*\(?([A-Za-z]{1,2})?\)?$", t)
    if m:
        disp = m[1].upper() + m[2].zfill(3) + (m[3] or "").upper()
        return disp, calif, nk(tok)
    return t, calif, nk(tok)  # p. ej. "N2", "SA004": se conserva tal cual


def prefijo(alias):
    m = re.match(r"^([A-Za-z]+)", alias)
    return m[1].upper() if m else ""


def leer_khipu_db():
    con = sqlite3.connect(f"file:{KHDB}?mode=ro", uri=True)
    cols = ["KHIPU_ID", "INVESTIGATOR_NUM", "OKR_NUM", "MUSEUM_NUM", "orig_inv_num", "MUSEUM_NAME"]
    return {r[2]: dict(zip(cols, r)) for r in con.execute(
        "select KHIPU_ID, INVESTIGATOR_NUM, OKR_NUM, MUSEUM_NUM, orig_inv_num, MUSEUM_NAME from khipu_main")}


def tuplas_sql(path, tabla):
    """Parsea las filas del INSERT de una tabla en el volcado MySQL (maquina de estados sin dependencias).
    Termina en el ';' que cierra la sentencia fuera de comillas."""
    txt = path.read_text(encoding="utf-8", errors="replace")
    marca = f"INSERT INTO `{tabla}` VALUES"
    i = txt.index(marca) + len(marca)
    filas, vals, cur, inq, en_tupla = [], [], "", False, False
    while i < len(txt):
        c = txt[i]
        if inq:
            if c == "\\":
                cur += txt[i + 1]; i += 2; continue
            if c == "'":
                if txt[i + 1:i + 2] == "'":
                    cur += "'"; i += 2; continue
                inq = False
            else:
                cur += c
        elif c == "'":
            inq = True
        elif c == "(":
            en_tupla, vals, cur = True, [], ""
        elif c == ",":
            if en_tupla:
                vals.append(cur.strip()); cur = ""
        elif c == ")":
            vals.append(cur.strip()); filas.append(vals); en_tupla = False
        elif c == ";":
            break
        elif en_tupla:
            cur += c
        i += 1
    return filas


def carpetas():
    """KH#### -> nombre de carpeta en open-khipu-repository/data (rangos como KH0002_0010)."""
    out = {}
    for d in DATA.iterdir():
        if d.is_dir() and d.name.startswith("KH"):
            m = re.match(r"KH(\d{4})(?:_(\d{4}))?$", d.name)
            if m:
                for k in range(int(m[1]), int(m[2] or m[1]) + 1):
                    out[f"KH{k:04d}"] = d.name
    return out


def main():
    okr = list(csv.DictReader(open(OKR_CSV, encoding="utf-8-sig", newline="")))
    khdb = leer_khipu_db()
    carp = carpetas()
    quip = list(csv.DictReader(open(QUIPUS, encoding="utf-8", newline="")))
    summ = {nk(r["kfg_name"]): r for r in csv.DictReader(open(SUMMARY, encoding="utf-8", newline=""))}
    sql_ids = {int(r[0]) for r in tuplas_sql(SQLDUMP, "khipu_main")}
    kh_list = [r["OKR Number"] for r in okr]
    assert len(kh_list) == len(set(kh_list)) == 702, len(kh_list)
    id_a_kh = {v["KHIPU_ID"]: kh for kh, v in khdb.items()}

    # 1) nombres por KH: alias del OKR + INVESTIGATOR_NUM de khipu.db
    filas = {}
    for r in okr:
        kh = r["OKR Number"]
        ali, nks = [], set()
        for tok in re.split(r"[,/]", r["Other Names"] or ""):
            if tok.strip():
                disp, _, k = norm(tok)
                if disp not in ali: ali.append(disp)
                nks.update({nk(disp), k})
        filas[kh] = {"aliases": ali, "nks": nks, "kfg": [], "via": [], "okr": r, "solo_db": []}
        if kh in khdb:
            for tok in re.split(r"[/,]", khdb[kh]["INVESTIGATOR_NUM"] or ""):
                if tok.strip():
                    disp, _, k = norm(tok)
                    if nk(disp) not in nks:
                        filas[kh]["solo_db"].append(disp)
                    nks.update({nk(disp), k})
    clave_kh = collections.defaultdict(set)
    for kh, f in filas.items():
        for k in f["nks"]:
            clave_kh[k].add(kh)

    # 2) KFG -> KH: (a) khipu_id del resumen KFG, (b) okr del xlsx, (c) nombre en alias
    kfg_kh, metodo, conflictos = {}, {}, []
    for q in quip:
        name = q["kfg"]; k = nk(name); kh = None; m = ""
        s = summ.get(k)
        if s and s["khipu_id"] and int(s["khipu_id"]) in id_a_kh:
            kh, m = id_a_kh[int(s["khipu_id"])], "khipu_id"
            if re.match(r"^KH\d{4}$", s["okr_name"] or "") and s["okr_name"] != kh:
                conflictos.append(f"{name}: resumen KFG okr_name {s['okr_name']} != khipu.db {kh}")
        if kh is None and re.match(r"^KH\d{4}$", q["okr"]):
            kh, m = q["okr"], "okr_kfg"
        if kh is None and k in clave_kh:
            cands = clave_kh[k]
            if len(cands) == 1:
                kh, m = next(iter(cands)), "alias"
            else:
                conflictos.append(f"{name}: alias en varios KH {sorted(cands)}")
        if kh is None:
            partes = [nk(x) for x in re.split(r"[_/ ]+", name) if nk(x)]
            conj = None
            for x in partes:
                if x in clave_kh:
                    conj = clave_kh[x] if conj is None else conj & clave_kh[x]
            if conj and len(conj) == 1:
                kh, m = next(iter(conj)), "alias_compuesto"
        kfg_kh[name] = kh
        if kh is None:
            continue
        metodo[name] = m
        filas[kh]["kfg"].append(name); filas[kh]["via"].append(m)

    # 3) duplicados y conflictos
    dup_alias = {k: sorted(v) for k, v in clave_kh.items() if len(v) > 1 and k}
    # n_inventario base: quita el sufijo (A)/(B) que el OKR anade a veces (VA63038(A) = VA63038)
    MARCAS = {"", "n/a", "unknown", "na", "none", "-"}
    base = lambda num: re.sub(r"\s*\([A-Za-z]\)$", "", num.strip())
    inv = collections.defaultdict(list)
    for r in okr:
        num = base(r["Collection Number"])
        if num.lower() not in MARCAS:
            inv[(r["Collection / Location"].strip(), num)].append(r["OKR Number"])
    inv_comp = {k: v for k, v in inv.items() if len(v) > 1}
    inv_por_kh = {kh: k for k, v in inv_comp.items() for kh in v}
    # mismo numero en museos distintos (posible duplicado entre colecciones; solo numeros de 5+ caracteres)
    inv_xm = collections.defaultdict(set)
    for r in okr:
        num = base(r["Collection Number"])
        if len(num) >= 5 and num.lower() not in MARCAS:
            inv_xm[num].add(r["OKR Number"])
    inv_xm = {k: sorted(v) for k, v in inv_xm.items() if len(v) > 1 and len({
        r["Collection / Location"] for r in okr if base(r["Collection Number"]) == k}) > 1}

    # 4) puente.csv
    cab = ["kh", "ur", "as", "otros_alias", "kfg", "kfg_enlace", "en_khipu_db", "khipu_id", "museo",
           "n_inventario", "carpeta", "comentario"]
    with open(OUT / "puente.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        for kh in kh_list:
            f = filas[kh]; r = f["okr"]
            ali = f["aliases"] + [a for a in f["solo_db"] if a not in f["aliases"]]
            ur = [a for a in ali if prefijo(a) == "UR"]
            asn = [a for a in ali if prefijo(a) == "AS"]
            otros = [a for a in ali if prefijo(a) not in ("UR", "AS")]
            notas = []
            com = re.sub(r"\s+", " ", r["Comments"] or "").strip()
            if com: notas.append("OKR: " + com[:400])
            if f["solo_db"]: notas.append("alias solo en khipu.db: " + ", ".join(f["solo_db"]))
            if kh not in khdb: notas.append("sin fila en khipu.db")
            if kh not in carp: notas.append("sin carpeta de datos")
            inv_n = base(r["Collection Number"])
            if inv_n in inv_xm:
                notas.append("mismo n_inventario en otro museo: " + ", ".join(h for h in inv_xm[inv_n] if h != kh))
            if kh in inv_por_kh:
                notas.append("inventario compartido con " + ", ".join(h for h in inv_comp[inv_por_kh[kh]] if h != kh))
            comp = sorted({h for a in f["nks"] for h in clave_kh[a] if h != kh})
            if comp: notas.append("alias compartido con " + ", ".join(comp))
            if len(f["kfg"]) > 1: notas.append("varios KFG: " + ", ".join(f["kfg"]))
            if kh in khdb and "/" in (khdb[kh]["INVESTIGATOR_NUM"] or ""):
                notas.append("khipu.db INVESTIGATOR_NUM=" + khdb[kh]["INVESTIGATOR_NUM"])
            w.writerow({"kh": kh, "ur": ";".join(ur), "as": ";".join(asn), "otros_alias": ";".join(otros),
                        "kfg": ";".join(f["kfg"]), "kfg_enlace": ";".join(sorted(set(f["via"]))),
                        "en_khipu_db": "sí" if kh in khdb else "no",
                        "khipu_id": khdb[kh]["KHIPU_ID"] if kh in khdb else "",
                        "museo": (r["Collection / Location"] or "").strip(),
                        "n_inventario": inv_n, "carpeta": carp.get(kh, ""), "comentario": " | ".join(notas)})

    # 5) conteos
    kh_db = set(khdb)
    kh_kfg = {kh for kh in kh_list if filas[kh]["kfg"]}
    kfg_sin_kh = [n for n, h in kfg_kh.items() if h is None]
    kh_sin_kfg = [kh for kh in kh_list if not filas[kh]["kfg"]]
    kh_2kfg = [kh for kh in kh_list if len(filas[kh]["kfg"]) > 1]
    c = []
    p = c.append
    p(f"KH en la lista OKR (filas de okr-kh-numbers.csv): {len(kh_list)}")
    p(f"KH con fila en khipu.db (khipu_main.OKR_NUM): {len(kh_db & set(kh_list))} (filas khipu_main: {len(khdb)})")
    fuera = [k for k in kh_list if k not in kh_db]
    p(f"KH sin fila en khipu.db: {len(fuera)}; de ellos sin carpeta de datos: {sum(1 for k in fuera if k not in carp)}; con carpeta: {sum(1 for k in fuera if k in carp)}")
    p(f"quipus KFG (quipus.csv): {len(quip)}; con KH: {len(quip) - len(kfg_sin_kh)}; sin KH: {len(kfg_sin_kh)} -> {kfg_sin_kh}")
    p(f"KH con al menos un quipu KFG: {len(kh_kfg)}; KH sin KFG: {len(kh_sin_kfg)}; KH con 2+ KFG: {kh_2kfg}")
    p(f"  metodo de enlace KFG: {dict(collections.Counter(metodo.values()))}")
    p(f"KH en khipu.db y en KFG: {len(kh_db & kh_kfg)}; en khipu.db sin KFG: {len(kh_db - kh_kfg)}; en KFG sin khipu.db: {len(kh_kfg - kh_db)}")
    p(f"khipu.db OKR_NUM fuera de la lista OKR: {sorted(kh_db - set(kh_list))}")
    ids_db = {v["KHIPU_ID"] for v in khdb.values()}
    p(f"KHIPU_ID de khipu.db presentes en KFG_DB.SQL: {len(ids_db & sql_ids)} de {len(khdb)}; filas khipu_main en SQL: {len(sql_ids)}")
    ids_res = {int(r["khipu_id"]) for r in summ.values() if r["khipu_id"]}
    p(f"KFG_DB.SQL vs khipu_summary.csv: ids SQL {len(sql_ids)}, ids resumen {len(ids_res)}, en ambos {len(sql_ids & ids_res)}, solo SQL {len(sql_ids - ids_res)}, solo resumen {len(ids_res - sql_ids)}")
    p(f"alias (clave nk) asignados a 2+ KH: {len(dup_alias)}")
    for k, v in sorted(dup_alias.items()):
        p(f"   {k}: {v}")
    p(f"n_inventario (mismo museo, sin sufijo A/B) compartido por 2+ KH: {len(inv_comp)} grupos, {len(inv_por_kh)} KH")
    p(f"n_inventario igual en museos distintos: {inv_xm}")
    for k, v in inv_comp.items():
        p(f"   {k[0]} | {k[1]}: {v}")
    p(f"conflictos de enlace KFG: {len(conflictos)}")
    for x in conflictos:
        p("   " + x)
    p("KH con 'duplicate' en Comments del OKR:")
    for kh in kh_list:
        com = filas[kh]["okr"]["Comments"] or ""
        if re.search(r"duplicate", com, re.I):
            p(f"   {kh}: {re.sub(chr(10), ' ', com)[:110]}")
    txt = "\n".join(c)
    (OUT / "puente_conteos.txt").write_text(txt + "\n", encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
