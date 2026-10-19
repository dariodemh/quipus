"""Utilidades comunes del análisis de color (carpeta 02_color).
Unidad de análisis = quipu. Todo p-valor es empírico por permutación (semillas fijas)."""
import re, sqlite3
import numpy as np, pandas as pd
from scipy import stats

RAIZ = r"."
OUT = RAIZ + r"\analisis\02_color"
SEED = 20261017

# ---------- diccionario Ascher (OKR) ----------
def _dic():
    con = sqlite3.connect(RAIZ + r"\data\external\open-khipu-repository\data\khipu.db")
    d = pd.read_sql("select AS_COLOR_CD cod, COLOR fam, INTENSITY inten from ascher_color_dc", con)
    return {r.cod: (r.fam, r.inten) for r in d.itertuples()}
DIC = _dic()
NAT = set("ABMZ")        # blanco, marrones, grises, negro: fibra natural (algodón/camélido) plausible
TINTE = set("RNYHG")     # rojo, naranja, amarillo, azul, verde: requieren tinte
# tintes "vivos" (descriptor ISCC sin 'grayish'): sensibilidad estricta; los grisáceos pueden ser sombras/desvaído
ESTRICTO = {"SR","RM","VR","PB","VB","TG","GL","SY","YY","0Y","SB","R","R0","0R","PG","DG","VG","0R"}
# PK = "unknown Urton color", L (oliva) y códigos fuera del diccionario -> ambiguos

def parsea(s):
    if not isinstance(s, str) or not s.strip():
        return None
    base = re.sub(r"\([^)]*\)", "", s)
    toks = [t for t in re.split(r"[:/%*_\-]+", base) if t]
    ops = set(re.findall(r"[:/%*_\-]", base))
    if len(toks) <= 1: tipo = "simple"
    elif ":" in ops: tipo = "moteado"
    elif "-" in ops: tipo = "barber"
    elif "/" in ops: tipo = "segmentado"
    else: tipo = "otro"
    key = re.sub(r"\([^)]*\)", "", s)
    fams = [DIC.get(t, ("?", np.nan))[0] for t in toks]
    if any(f in TINTE and t != "PK" for f, t in zip(fams, toks)): nd = "tinte"
    elif any(f in ("L", "?") or t == "PK" for f, t in zip(fams, toks)): nd = "amb"
    else: nd = "nat"
    nd2 = "tinte" if any(t in ESTRICTO for t in toks) else ("amb" if nd == "tinte" else nd)
    import warnings; warnings.simplefilter("ignore")
    inten = np.nanmean([DIC.get(t, ("?", np.nan))[1] for t in toks]) if toks else np.nan
    return key, toks[0], tipo, nd, inten, "".join(sorted(set(fams))), nd2

def cargar():
    c = pd.read_csv(RAIZ + r"\analisis\datos\cuerdas.csv")
    q = pd.read_csv(RAIZ + r"\analisis\datos\quipus.csv")
    p = c.color.map(parsea)
    for i, n in enumerate(["ckey", "cmain", "ctipo", "nd", "inten", "fams", "nd2"]):
        c[n] = p.map(lambda x: x[i] if x else None)
    c["tiene_valor"] = c.nudos.notna()
    c["val"] = np.where(c.tiene_valor, c.valor, np.nan)
    c = c.sort_values(["kfg", "orden"]).reset_index(drop=True)
    c["col"] = c.kfg.str.extract(r"^([A-Z]+)")[0]
    # posición dentro del grupo (solo colgantes)
    pe = c.nivel == 0
    c["pos"] = np.nan; c["gsize"] = np.nan
    c.loc[pe, "pos"] = c[pe].groupby(["kfg", "grupo"]).cumcount() + 1
    c.loc[pe, "gsize"] = c[pe].groupby(["kfg", "grupo"]).cuerda.transform("size")
    return c, q

# ---------- permutaciones ----------
def mid_p(obs, nulo, cola="ge"):
    o = round(float(obs), 10); n = np.round(nulo, 10)
    if cola == "ge": a, b = (n > o).sum(), (n == o).sum()
    else: a, b = (n < o).sum(), (n == o).sum()
    return (a + 0.5 * b + 0.5) / (len(n) + 1)

def idx_perm(n, estrato, B, rng):
    """Índices (B,n) que permutan dentro de estratos. Los datos deben venir ordenados por estrato."""
    r = rng.random((B, n))
    if estrato is not None: r = r + np.asarray(estrato)[None, :]
    return np.argsort(r, axis=1)

def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    q = np.empty(n); m = 1.0
    for rank, i in zip(range(n, 0, -1), o[::-1]):
        m = min(m, p[i] * n / rank); q[i] = m
    return q

# ---------- metaanálisis por quipu ----------
def meta(df, dos_colas=True):
    """df: columnas kfg, col(ección), eff, z, p (p por quipu). Devuelve dict de resumen entre quipus."""
    d = df.dropna(subset=["z"]); n = len(d)
    if n == 0: return dict(n=0)
    r = dict(n=n, eff_med=d.eff.median(), eff_mean=d.eff.mean())
    pos = (d.eff > 0).sum(); neg = (d.eff < 0).sum()
    r["frac_pos"] = pos / max(pos + neg, 1)
    r["p_signo"] = stats.binomtest(pos, pos + neg, 0.5).pvalue if pos + neg > 0 else np.nan
    zz = d.z.values
    r["z_stouffer"] = zz.sum() / np.sqrt(n)
    r["p_stouffer"] = 2 * stats.norm.sf(abs(r["z_stouffer"])) if dos_colas else stats.norm.sf(r["z_stouffer"])
    try: r["p_wilcoxon"] = stats.wilcoxon(d.eff - 0).pvalue if n >= 8 and (d.eff != 0).any() else np.nan
    except ValueError: r["p_wilcoxon"] = np.nan
    sig = (d.p < 0.05).sum()
    r["frac_p05"] = sig / n
    r["p_exceso_p05"] = stats.binomtest(sig, n, 0.05, alternative="greater").pvalue
    r["n_bh05"] = int((bh(d.p.values) < 0.05).sum())
    return r
