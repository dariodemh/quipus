"""Parte B3: inventario de archivos NO convertibles por script (jpg, pdf, docx y xlsx sin formato util).

No transcribe nada. Para cada archivo: tipo, KH asociado (desde puente.csv cuando hay alias o n.o de inventario),
si tiene capa de texto (pdftotext / texto de docx) y si requiere transcripcion manual.
Salida: inventario_manual.csv. Uso: python -I analisis/17_okr_pendientes/inventario_manual.py
"""
import csv, re, subprocess, sys
from pathlib import Path

sys.path.append(r"~\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages")
import docx  # python-docx

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data/external/open-khipu-repository/data"
OUT = Path(__file__).resolve().parent
PDFTOTEXT = "pdftotext"

# (carpeta, archivo, kh, qué parece contener, requiere transcripción manual, nota)
FILAS = [
    ("KH0002_0010", "DB input for AS1 thorugh AS9.txt", "KH0002-KH0010",
     "Sentencias INSERT de ascher_cord_color para AS001-AS009 (carga de colores por cordon)", "no",
     "Entrada SQL de la base AS1-AS9.db; no es transcripcion"),
    ("KH0631_0632", "C14 date for SH001.jpg", "KH0631",
     "Foto/registro de la datacion C14 de SH001", "no", "La fecha (1498 BP +/-27) figura en el docx"),
    ("KH0631_0632", "SH 001 upper half with ruler & greyscale.jpeg", "KH0631",
     "Fotografia de la mitad superior de SH001 con regla y escala de grises", "no", "Solo documentacion fotografica"),
    ("KH0631_0632", "SH001 Description 2023.docx", "KH0631",
     "Descripcion de Sabine Hyland (2023): khipu del Horizonte Tardio, 22 colgantes sin subsidiarias, C14 1498 BP +/-27, procedencia desconocida", "no",
     "Texto extraido; el xlsx SH001 ya se convierte a cuerdas_extra.csv"),
    ("KH0631_0632", "(sin archivos)", "KH0632",
     "No hay ningun archivo de datos para SH002 en la carpeta", "sí",
     "Requiere pedir datos o transcribir de fuente externa; OKR: SH002 = SA005"),
    ("KH0638_0652", "KHIPU ENLAZADO-MNAAHP.15.xlsx", "KH0652",
     "Hojas primary_cord y 'wrapped threads' (hilos envueltos W1..), sin hoja pendant_cords", "sí",
     "Formato distinto: no genera cuerdas; no se convierte"),
    ("KH0638_0652", "Croquis KhipusEnlazadosEnglish.jpg", "KH0638-KH0652",
     "Croquis del conjunto de 15 quipus enlazados (disposicion sobre el marco)", "sí",
     "Los enlaces entre quipus no aparecen en los xlsx; hay que transcribir el croquis"),
    ("KH0638_0652", "Description RT 16905 MNAAHP.docx", "KH0638-KH0652",
     "Descripcion general del conjunto RT-16905 (MNAAHP), sep. 2023, Chirinos, Ghezzi, Alvarez; diagrama y 2 tablas", "no",
     "Texto extraido; tablas no transcritas"),
    ("KH0674_0675", "PC.WBC.2016.072.pdf", "KH0674",
     "Documento escaneado de Dumbarton Oaks (PC.WBC.2016.072 = UR297); sin capa de texto", "sí",
     "Escaneo de imagenes; requiere OCR o transcripcion manual"),
    ("KH0674_0675", "PC.WBC.2016.071.pdf", "KH0675",
     "Documento escaneado de Dumbarton Oaks (PC.WBC.2016.071 = UR298); sin capa de texto", "sí",
     "Escaneo de imagenes; requiere OCR o transcripcion manual"),
    ("KH0676", "JS01_Strauss_Harvard_Senior_Thesis.xlsx", "KH0676",
     "Exportacion KDB (1/2/2019), hoja 'Pendant Detail' con 141 filas de cuerdas en notacion sin columna de valor", "sí",
     "No convertido: la regla de la hoja ('long knots = their value in parentheses') es ambigua; decidir decodificacion"),
    ("KH0676", "Struass_Original_Notes.pdf", "KH0676",
     "Notas originales de Strauss (tesis Harvard) sobre JS01; sin capa de texto", "sí",
     "Escaneo de imagenes; requiere transcripcion manual"),
    ("KH0702", "R4303.xlsx", "KH0702",
     "Formato KFG (FitzPatrick), Museo Amano R4303", "no", "Convertido a cuerdas_extra.csv"),
]


def tiene_texto_pdf(p):
    try:
        out = subprocess.run([PDFTOTEXT, "-q", str(p), "-"], capture_output=True, timeout=120)
        txt = out.stdout.decode("utf-8", errors="replace")
        return len(re.sub(r"\s", "", txt))
    except (OSError, subprocess.SubprocessError):
        return -1


def caracteres_docx(p):
    d = docx.Document(str(p))
    return sum(len(par.text.strip()) for par in d.paragraphs) + sum(
        len(c.text) for t in d.tables for row in t.rows for c in row.cells)


def main():
    # n.o de inventario -> KH para los PDF (ya conocido en puente.csv)
    puente = {r["kh"]: r for r in csv.DictReader(open(OUT / "puente.csv", encoding="utf-8"))}
    filas_out = []
    for carpeta, archivo, kh, que, manual, nota in FILAS:
        ruta = DATA / carpeta / archivo
        if archivo.startswith("("):
            tam, texto = "", "no aplica"
        elif ruta.exists():
            tam = ruta.stat().st_size
            if ruta.suffix.lower() == ".pdf":
                n = tiene_texto_pdf(ruta)
                texto = "sí" if n > 0 else "no (sin capa de texto)"
            elif ruta.suffix.lower() == ".docx":
                n = caracteres_docx(ruta)
                texto = f"sí ({n} caracteres)"
            elif ruta.suffix.lower() in (".jpg", ".jpeg"):
                texto = "no (imagen)"
            elif ruta.suffix.lower() == ".xlsx":
                texto = "sí (hojas de datos)"
            else:
                texto = "sí (texto plano)"
        else:
            tam, texto = "", "archivo no encontrado"
        if archivo.endswith(".jpg") and "..." in archivo:
            # lista de jpg: el tamano que se reporta es el total de la serie
            tam = sum(p.stat().st_size for p in (DATA / carpeta).glob("JC*_record.jpg"))
        tipo = ("jpg" if ".jpg" in archivo.lower() or ".jpeg" in archivo.lower() else
                "pdf" if archivo.endswith(".pdf") else "docx" if archivo.endswith(".docx") else
                "xlsx" if archivo.endswith(".xlsx") else "db" if archivo.endswith(".db") else
                "txt" if archivo.endswith(".txt") else "-")
        if "..." in archivo or archivo.startswith("("):
            tipo = "jpg" if "jpg" in archivo else "-"
        filas_out.append({"carpeta": carpeta, "archivo": archivo, "tipo": tipo, "kh": kh,
                          "bytes": tam, "tiene_texto": texto, "que_parece_contener": que,
                          "requiere_transcripcion_manual": manual, "nota": nota})
    # jpg de KH0653_0663 (uno por KH), para que el inventario lo liste completo
    for p in sorted((DATA / "KH0653_0663").glob("JC*_record.jpg")):
        jc = p.name[:5]
        kh = next((k for k, r in puente.items() if jc in r["as"] + r["otros_alias"] + r["ur"]), "")
        filas_out.append({"carpeta": "KH0653_0663", "archivo": p.name, "tipo": "jpg", "kh": kh,
                          "bytes": p.stat().st_size, "tiene_texto": "no (imagen)",
                          "que_parece_contener": "Ficha de registro (segun el nombre)",
                          "requiere_transcripcion_manual": "sí", "nota": "Una ficha por quipu"})
    cab = ["carpeta", "archivo", "tipo", "kh", "bytes", "tiene_texto", "que_parece_contener",
           "requiere_transcripcion_manual", "nota"]
    with open(OUT / "inventario_manual.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        w.writerows(filas_out)
    print(f"filas: {len(filas_out)}; requieren transcripcion manual: "
          f"{sum(1 for r in filas_out if r['requiere_transcripcion_manual'] == 'sí')}")


if __name__ == "__main__":
    main()
