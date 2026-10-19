# -*- coding: utf-8 -*-
"""Construye los corpus de lengua y los modelos de silabas.

Quechua colonial: manuscrito de Huarochiri (texto quechua, ed. Arguedas, c. 1600),
  filtrado por palabras-funcion quechuas y ausencia de vocales acentuadas.
Quechua moderno (control de robustez): Wikipedia en quechua.
Aymara: Wikipedia en aymara, filtrada por densidad de funcionales; es un corpus
  auxiliar (el texto colonial aymara de la Doctrina 1584 esta en OCR a dos
  columnas intercaladas y no se puede separar sin alinear a mano; se documenta).

Modelo: bigramas de silabas sobre el flujo continuo (los limites de palabra se
marcan como <s>/</s>, pero el modelo se evalua sobre secuencias continuas).
"""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm_utils import CORP, silabas, fetch_wiki, build_lm

ACC = re.compile(r"[\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da]")
QW = set("""chay chaysi chayca chaymanta chaypi chayhina chaytam chaypacha
ñispa ñisca ñiscan mana manam manataq manacha can canmi canqui canchic cancuna
cay caypi cayca caypim cunanca cunan pay payca paycuna paymi hina hinatac hinam
hinaspas hinaspa cuna cunapas cunacta cunamanta pacha pachapi runa runacuna
huaca huacacuna ancha achca yaya churi ñoca ñocap ñocapmi pim ima imam imatac""".split())
QX = re.compile(r"\b(" + "|".join(sorted(QW, key=len, reverse=True)) + r")\b", re.I)

def filtro_quechua(path):
    out = []
    for raw in open(path, encoding="utf-8", errors="replace"):
        s = raw.strip()
        if len(s) < 40 or ACC.search(s):
            continue
        w = re.findall(r"[a-zA-ZñÑçÇ]+", s.lower())
        if len(w) < 6:
            continue
        hits = len(QX.findall(s))
        if hits >= 2 and hits / len(w) > 0.08:
            out.append(s)
    return out

hpath = os.path.join(CORP, "huarochiri_arguedas.txt")
qlines = filtro_quechua(hpath)
qtxt = "\n".join(qlines)
open(os.path.join(CORP, "quechua.txt"), "w", encoding="utf-8").write(qtxt)
print("huarochiri: lineas", len(qlines), "palabras", len(re.findall(r"[a-zA-ZñÑ]+", qtxt)))

# --- aymara: filtro por linea
AY = set("""ukax ukat uka ukham jichhax jichha jan janira jani kunas kuna kunata
kunjamsa khaya ankhax sapa walja utji utj utjawa jaqi jaqinaka marka markanaka
aru arunaka qillqa qillqata wawanaka wawa mayni maya paya kimsa pusi aka akax
akat uraqi uraqinaka yati yatxata suma jasaki juk'ampi kikpa yaqha yaqhipa
khitis khitirus kunatsa kunjamasa pachpa nayra nayraru nisqaqa suyu jisk'a
jach'a t'aqa distritu piruw qusqu""".split())
AYX = re.compile(r"\b(" + "|".join(re.escape(x) for x in sorted(AY, key=len, reverse=True)) + r")\b", re.I)

def filtro_aymara(path):
    out = []
    for raw in open(path, encoding="utf-8", errors="replace"):
        s = raw.strip()
        if len(s) < 60:
            continue
        alpha = sum(c.isalpha() or c.isspace() for c in s) / len(s)
        if alpha < 0.75:
            continue
        w = re.findall(r"[a-zA-ZñÑáéíóúü]+", s.lower())
        if len(w) < 8:
            continue
        hits = len(AYX.findall(s))
        if hits >= 2 and hits / len(w) > 0.12:
            out.append(re.sub(r"[^A-Za-zñÑáéíóúü' ]+", " ", s))
    return out

apath = os.path.join(CORP, "aymara.txt")
if not os.path.exists(apath) or os.path.getsize(apath) < 5000:
    atxt = fetch_wiki("ay.wikipedia.org", 900)
    open(apath, "w", encoding="utf-8").write(atxt)
else:
    atxt = open(apath, encoding="utf-8").read()
alines = filtro_aymara(apath)
atxt2 = "\n".join(alines)
open(os.path.join(CORP, "aymara_limpio.txt"), "w", encoding="utf-8").write(atxt2)
print("aymara: lineas", len(alines), "palabras", len(re.findall(r"[a-zA-ZñÑ]+", atxt2)))

# --- quechua moderno (robustez)
qpath = os.path.join(CORP, "quechua_wiki.txt")
if not os.path.exists(qpath) or os.path.getsize(qpath) < 5000:
    qw = fetch_wiki("qu.wikipedia.org", 700)
    open(qpath, "w", encoding="utf-8").write(qw)
else:
    qw = open(qpath, encoding="utf-8").read()
print("quechua wiki: palabras", len(re.findall(r"[a-zA-ZñÑ]+", qw)))

build_lm(qtxt, "quechua")
build_lm(atxt2, "aymara")
build_lm(qw, "quechua_wiki")

for t in ["ñispa", "chaysi", "huaccha", "pariacaca", "quipu", "aymara", "atipanacun"]:
    print("  ", t.encode("ascii", "replace").decode(), silabas(t))
