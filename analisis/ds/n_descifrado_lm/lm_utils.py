# -*- coding: utf-8 -*-
"""Utilidades: silabificador quechua/aymara, descarga de corpus, modelos n-grama."""
import re, json, os, math
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
CORP = os.path.join(BASE, "corpus")

VOW = "aeiou"
DIG = ["ch", "ll", "rr", "sh", "tz", "th", "ph", "kh", "qh"]

def _units(w):
    w = w.lower()
    w = re.sub(r"[^a-zñ]", "", w)
    w = re.sub(r"qu([ei])", r"q\1", w)   # qu+ e/i -> q + vocal
    w = re.sub(r"gu([ei])", r"g\1", w)
    us, i = [], 0
    while i < len(w):
        if i + 1 < len(w) and w[i:i+2] in DIG:
            us.append(w[i:i+2]); i += 2; continue
        us.append(w[i]); i += 1
    out = []
    for k, u in enumerate(us):
        if u == "u" and out and out[-1] == "h" and k + 1 < len(us) and us[k+1] in "aeiou":
            out[-1] = "hu"; continue
        out.append(u)
    return out

def silabas(word):
    """Silabificacion ortografica CV(C). Onset maximo de una consonante;
    digrafos (ch, ll, rr, sh) cuentan como una consonante."""
    us = _units(word)
    if not us:
        return []
    vidx = [i for i, u in enumerate(us) if u in "aeiou"]
    if not vidx:
        return ["".join(us)]
    cuts = [0]
    for n in range(1, len(vidx)):
        a, b = vidx[n-1], vidx[n]
        cons = b - a - 1
        if cons == 0:
            cuts.append(b)
        elif cons == 1:
            cuts.append(b - 1)
        else:
            cuts.append(a + 2)
    cuts.append(len(us))
    return ["".join(us[cuts[n]:cuts[n+1]]) for n in range(len(vidx))]


def fetch_wiki(host, n_pages=600):
    """Descarga wikitexto de articulos via API (generator=allpages)."""
    import urllib.request, urllib.parse, time
    txt, cont = [], None
    while len(txt) < n_pages:
        url = (f"https://{host}/w/api.php?action=query&generator=allpages&gapnamespace=0"
               f"&gaplimit=50&prop=revisions&rvslots=main&rvprop=content&format=json")
        if cont:
            url += "&gapcontinue=" + urllib.parse.quote(cont)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "quipu-research/1.0 (quipu@example.org)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
        except Exception as e:
            print("wiki error", e); break
        for p in d.get("query", {}).get("pages", {}).values():
            try:
                c = p["revisions"][0]["slots"]["main"]["*"]
            except Exception:
                continue
            if len(c) > 300:
                txt.append(c)
        cont = d.get("continue", {}).get("gapcontinue")
        if not cont:
            break
        time.sleep(0.1)
    t = "\n".join(txt)
    t = re.sub(r"\{\{[^{}]*\}\}", " ", t)
    t = re.sub(r"\[\[([^\]|]*\|)?", "", t)
    t = re.sub(r"[=*#:;<>\[\]{}|]", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return t


def build_lm(txt, name, save=True):
    """Bigramas sobre el flujo continuo: cada linea es una secuencia de silabas
    (sin marcar limites de palabra, que en el quipu no se conocen)."""
    words = re.findall(r"[a-zA-ZñÑ]+", txt.lower())
    sents = []
    for line in txt.lower().split("\n"):
        s = []
        for w in re.findall(r"[a-zA-ZñÑ]+", line):
            s.extend(silabas(w))
        if len(s) >= 2:
            sents.append(s)
    flat = [x for s in sents for x in s]
    uni = Counter(flat)
    bi = Counter()
    for s in sents:
        prev = "<s>"
        for x in s:
            bi[(prev, x)] += 1
            prev = x
        bi[(prev, "</s>")] += 1
    print(f"{name}: palabras {len(words)} silabas {len(flat)} tipos {len(uni)} bigramas {len(bi)}")
    if save:
        json.dump({"uni": uni, "bi": {f"{a}\t{b}": c for (a, b), c in bi.items()},
                   "n_syl": len(flat), "n_words": len(words)},
                  open(os.path.join(CORP, f"lm_{name}.json"), "w", encoding="utf-8"))
    return uni, bi, sents


def load_lm(name):
    d = json.load(open(os.path.join(CORP, f"lm_{name}.json"), encoding="utf-8"))
    uni = Counter(d["uni"])
    bi = Counter({tuple(k.split("\t")): v for k, v in d["bi"].items()})
    return uni, bi, d["n_syl"]


class BigramLM:
    """Modelo bigrama con interpolacion (add-k) sobre el vocabulario de silabas."""
    def __init__(self, uni, bi, k=0.5):
        self.uni = uni; self.bi = bi; self.k = k
        self.V = len(uni)
        self.N = sum(uni.values())
        self.ctx = Counter()
        for (a, b), c in bi.items():
            self.ctx[a] += c
        self._cache = {}
    def logp(self, prev, cur):
        key = (prev, cur)
        v = self._cache.get(key)
        if v is None:
            cu = self.uni.get(cur, 0)
            cb = self.bi.get((prev, cur), 0)
            den = self.ctx.get(prev, 0) + self.k * self.V
            p = (cb + self.k * (cu + 0.5) / (self.N + 0.5 * self.V)) / (den if den > 0 else 1)
            v = math.log(max(p, 1e-12))
            self._cache[key] = v
        return v
