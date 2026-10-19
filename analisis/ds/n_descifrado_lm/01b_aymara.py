# -*- coding: utf-8 -*-
"""Limpieza del corpus aymara (Wikipedia): filtra texto con densidad de palabras
funcion aymara, para separar articulos realmente en aymara de los que estan en
espanol/ingles."""
import re, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm_utils import CORP, build_lm

AY = set("""ukax ukat uka ukham ukhamawa jichhax jichha jan janira jani kunas kuna
kunata kunjamsa khaya ankhax sapa walja utji utj utjawa jaqi jaqinaka marka
markanaka aru arunaka qillqa qillqata wawanaka wawa mayni maya paya kimsa
pusi qallta qhipa aka akax akat aynacha alaxa manqha pata uraqi uraqinaka
yati yatxata yatxatiri amuyt'a lup'ixa ch'ama suma jasaki juk'ampi jukhu
kikpa yaqha yaqhipa inaki ina khitis khitirus kunatsa kunjamasa
pachpa pachanakana qhipurunaka nayra nayraru""".split())
AYX = re.compile(r"\b(" + "|".join(sorted(AY, key=len, reverse=True)) + r")\b", re.I)
ACC = re.compile(r"[\u00e1\u00e9\u00ed\u00f3\u00fa\u00c1\u00c9\u00cd\u00d3\u00da\u00fc]")

raw = open(os.path.join(CORP, "aymara.txt"), encoding="utf-8").read()
# partir en parrafos y filtrar
paras = re.split(r"\n\s*\n", raw)
keep = []
for p in paras:
    if len(p) < 120 or ACC.search(p):
        continue
    w = re.findall(r"[a-zA-ZñÑ]+", p.lower())
    if len(w) < 20:
        continue
    hits = len(AYX.findall(p))
    # Aymara tiene sufijos aglutinantes: exigir densidad de funcionales y
    # terminaciones tipicas (-na, -xa, -wa, -ta, -pi)
    suf = sum(1 for x in w if re.search(r"(na|xa|wa|ta|pi|sa|pa|ki|sti)$", x)) / len(w)
    if hits / len(w) > 0.04 and suf > 0.45:
        keep.append(p)
atxt = "\n".join(keep)
open(os.path.join(CORP, "aymara_limpio.txt"), "w", encoding="utf-8").write(atxt)
print("parrafos", len(paras), "->", len(keep), "palabras", len(re.findall(r"[a-zA-ZñÑ]+", atxt)))
for p in keep[:2]:
    print("  >", p[:150].replace("\n", " "))

uni, bi, sents = build_lm(atxt, "aymara", save=False)
print("tipos silaba", len(uni), "total silabas", sum(uni.values()))
print("top", uni.most_common(10))
rare = [s for s, n in uni.items() if n == 1]
print("hapax", len(rare), "ej", rare[:8])
