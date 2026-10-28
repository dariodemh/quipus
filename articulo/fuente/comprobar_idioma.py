"""Abre una página del artículo ya construida, pulsa todos los botones de las figuras y busca palabras del otro idioma
en todo el texto visible (incluidos los SVG). Uso: python articulo/fuente/comprobar_idioma.py articulo/index.html en
Requiere playwright: pip install playwright && python -m playwright install chromium"""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

pagina, lang = pathlib.Path(sys.argv[1]).resolve(), sys.argv[2]
# palabras frecuentes que solo existen en el otro idioma
OTRO = {'en': r'\b(de|del|los|las|que|con|sin|para|por|una|sumas?|cuerdas?|fila|grupo|libro|valores?|exactas?|barajad\w*|cabeceras?|coinciden\w*|también|según|cuenta|todavía|vueltas)\b',
        'es': r'\b(the|and|of|with|without|sums?|cords?|row|group|ledger|values?|exact|shuffl\w*|headers?|match\w*|also|according|still|turns)\b'}[lang]
# nombres propios, títulos de obras y citas textuales que no se traducen
PERMITIDO = re.compile(r'Banco Central de Reserva del Perú|Depósito del Inga|Nueva corónica y buen gobierno|Valle del Santa|'
                       r'San Pedro de Corongo|Museo de Arte de Cleveland|Lo que suman los quipus|resumen en español|Leer en español|'
                       r'Read in English|Guamán Poma de Ayala|Depósito del Inga|\((SIN|SUM)\)|Before: SIN|coincidences?|Code of the Quipu|Inka History in Knots|Khipu Field Guide|Open Khipu Repository|'
                       r'«[^»]*»|“[^”]*”|\b[A-Z][a-z]+, [A-Z]\. \(\d{4}\)[^\n]*', re.S)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1200, 'height': 900})
    errores = []
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.goto(pagina.as_uri())
    pg.wait_for_timeout(800)
    textos = set()
    leer = lambda: textos.update(t.strip() for t in pg.evaluate(
        "() => [...document.querySelectorAll('body *')].filter(e => !['SCRIPT','STYLE'].includes(e.tagName) && !e.closest('#referencias'))"
        ".flatMap(e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent))") if t.strip())
    leer()
    for bt in pg.query_selector_all('figure button'):     # cada botón cambia lo que dibuja la figura
        bt.scroll_into_view_if_needed(); bt.click(); pg.wait_for_timeout(2500); leer()
    for h in pg.query_selector_all('#svg-copias path[tabindex]')[:5]:
        h.focus(); leer()
    b.close()

hallados = []
for t in sorted(textos):
    limpio = PERMITIDO.sub(' ', t)
    m = re.findall(OTRO, limpio, re.I)
    if m:
        hallados.append(f'  {set(w.lower() for w in m)}  ←  {t[:140]}')
print(f'{pagina.name}: {len(textos)} textos revisados; errores JS: {errores or "ninguno"}')
print('\n'.join(hallados) if hallados else '  sin palabras del otro idioma')
