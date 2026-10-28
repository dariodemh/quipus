"""Arma el artículo en dos páginas: articulo/index.html (inglés) e index.es.html (español).
Cada una es plantilla + figuras.js + datos.json + imágenes en data URI.
Uso: python articulo/fuente/construir.py [carpeta_destino]   (por omisión, articulo/)"""
import base64, json, sys, os
S = os.path.dirname(os.path.abspath(__file__))
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(S)
uri = lambda f, m: f'data:{m};base64,' + base64.b64encode(open(f'{S}/{f}', 'rb').read()).decode()
datos = json.dumps(json.load(open(f'{S}/datos.json', encoding='utf-8')), ensure_ascii=False, separators=(',', ':'))
rep = {'__HERO__': uri('img_cleveland.jpg', 'image/jpeg'), '__LOCKE__': uri('img_locke.jpg', 'image/jpeg'),
       '__POMA1__': uri('img_poma_contador.png', 'image/png'), '__POMA2__': uri('img_poma_qollqa.jpg', 'image/jpeg'),
       '__DATOS__': datos.replace('</', '<\\/'), '__JS__': open(f'{S}/figuras.js', encoding='utf-8').read()}
os.makedirs(dest, exist_ok=True)
for lang, plantilla, salida in [('en', 'plantilla.en.html', 'index.html'), ('es', 'plantilla.html', 'index.es.html')]:
    t = open(f'{S}/{plantilla}', encoding='utf-8').read()
    for k, v in rep.items():
        assert t.count(k) == 1, (plantilla, k)
        t = t.replace(k, v)
    html = (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' + t + '\n</html>\n')
    open(f'{dest}/{salida}', 'w', encoding='utf-8', newline='\n').write(html)
    print(f'{dest}/{salida}', round(len(html.encode()) / 1024), 'KB')
