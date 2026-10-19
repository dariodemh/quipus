# -*- coding: utf-8 -*-
"""Genera lexico_contable.csv (términos, lengua, fuente, glosa, categoría, equivalencia)."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import csv

R = []
def add(term, lang, src, gloss, cat, eq='', note=''):
    R.append(dict(termino=term, lengua=lang, fuente=src, glosa=gloss,
                  categoria=cat, equivalencia=eq, nota=note))

# ---------- números quechuas ----------
for t, g in [('huk', 'uno'), ('iskay', 'dos'), ('kimsa', 'tres'), ('tawa', 'cuatro'),
             ('pichqa', 'cinco'), ('suqta', 'seis'), ('qanchis', 'siete'),
             ('pusaq', 'ocho'), ('isqun', 'nueve'), ('chunka', 'diez')]:
    add(t, 'quechua', 'González Holguín 1608, s.v.; Santo Tomás 1560, s.v.',
        g, 'número', note='grafía colonial: huc, iscay, quimça, taua, pichca, çocta, canchis, puçac, iscon, chunca')
add('pachak', 'quechua', 'González Holguín 1608, s.v. pachac; Santo Tomás 1560',
    'cien', 'número', '100', 'también unidad sociopolítica de 100 tributarios (pachaca)')
add('waranqa', 'quechua', 'González Holguín 1608, s.v. guaranga',
    'mil', 'número', '1 000', 'también unidad sociopolítica (guaranga)')
add('hunu', 'quechua', 'González Holguín 1608, s.v. hunu; Santo Tomás 1560',
    'diez mil', 'número', '10 000', '')

# ---------- operaciones y registro ----------
add('yupay', 'quechua', 'González Holguín 1608, s.v. yupani', 'contar, numerar', 'operación')
add('yupana', 'quechua', 'González Holguín 1608, s.v. yupana', 'tabla o tablero para contar; ábaco de piedras', 'registro',
    note='Barraza et al. 2022, tabla 1, la glosa como "tabla para contar"')
add('chuncachani', 'quechua', 'González Holguín 1608, I:103, 113 (apud Barraza et al. 2022)',
    'contar por decenas, hacer montones de diez', 'operación')
add('yayanchani', 'quechua', 'González Holguín 1608, I:113; Santo Tomás 1560, I:98v',
    'sumar, juntar y consolidar cuentas; reducir dieces y cientos a un número', 'operación',
    note='el "yayan" es la ficha de sustitución decimal')
add('taripani', 'quechua', 'González Holguín 1608, I:339', 'averiguar, verificar o tomar cuentas; ajustar cuentas', 'operación')
add('quipuni', 'quechua', 'González Holguín 1608, I:308', 'contar por nudos', 'operación')
add('quipu pucuni', 'quechua', 'González Holguín 1608, I:308', 'dar cuentas por nudos', 'operación')
add('quipucta huñuni', 'quechua', 'González Holguín 1608, II:22', 'sumar o consolidar todas las cuentas', 'operación')
add('quipucta ttiuni', 'quechua', 'González Holguín 1608, I:308', 'contar llamando por nudos (en voz alta)', 'operación')
add('llulla quipu', 'quechua', 'Santo Tomás 1560, II:171', 'cuenta falsa, quipu falseado', 'registro')
add('quipu', 'quechua', 'González Holguín 1608, s.v.; Santo Tomás 1560',
    'nudo; cuenta o registro anudado', 'registro', note='también "quipo" en las fuentes españolas')
add('qillqa', 'quechua', 'González Holguín 1608, s.v. quellca', 'escritura, pintura, signo gráfico', 'registro')
add('yupa', 'quechua', 'González Holguín 1608, s.v. yupa', 'cuenta, número, cómputo', 'registro')
add('quipucamayoc', 'quechua', 'González Holguín 1608, s.v. quipucamayoc',
    'el que tiene oficio de contar por nudos; contador', 'oficio')
add('waskha', 'quechua', 'González Holguín 1608, s.v. huasca', 'soga, cuerda', 'parte del quipu')

# ---------- unidades de medida y carga ----------
add('tupu', 'quechua', 'González Holguín 1608, s.v. tupu; Rostworowski 1962',
    'medida de tierra; también medida de tela y prenda', 'unidad de medida',
    '≈0,27 ha (88 × 44 varas ≈ 2 700 m²); variable por región',
    'no confundir con el tupu alfiler; equivalencia agraria aproximada')
add('raki', 'quechua', 'González Holguín 1608, s.v. raqui', 'partición, porción, reparto', 'unidad de medida',
    'sin equivalencia métrica fija', 'en riego designa el turno o la porción de agua; requiere verificación local')
add('rakhi', 'aimara/quechua', 'Bertonio 1612, s.v. raki; González Holguín 1608, s.v. raqui',
    'división, parte, porción; en riego, turno o cuota de agua', 'unidad de medida',
    'sin equivalencia métrica fija', 'variante de raki; el mismo término circula en quechua y aimara')
add('poqcha', 'quechua', 'vocabulario local de riego andino (uso en Huarochirí/Yauyos)',
    'porción o turno de agua de riego', 'unidad de medida', 'sin equivalencia métrica',
    'término local, no estándar en los diccionarios coloniales; nivel: propuesto, verificar')
add('costal', 'español', 'documentos coloniales; Barraza et al. 2022',
    'saco o costal para transportar y almacenar productos', 'unidad de medida',
    'capacidad variable, del orden de 1–2 fanegas', 'la marca del costal podía ser un signo de control')
add('carga', 'español', 'Murra 2024:1277, 1315',
    'carga transportada por un hombre o animal', 'unidad de medida',
    '≈2 arrobas ≈ 23 kg; muy variable según producto', 'para maíz podía equivaler a una fanega')
add('fanega', 'español', 'Murra 2024:1310–1313 (nota editorial)',
    'medida castellana de capacidad para áridos', 'unidad de medida', '≈55,5 L en Castilla', 'grafía colonial: hanega')
add('hanega', 'español', 'Murra 2024:1310', 'variante de fanega', 'unidad de medida', '≈55,5 L', '')
add('arroba', 'español', 'documentos coloniales', 'medida de peso o de capacidad', 'unidad de medida',
    '≈11,5 kg; ≈16,1 L para líquidos', '')
add('libra', 'español', 'Murra 2024:1277', 'libra castellana de peso', 'unidad de medida', '≈460 g', '')
add('peso ensayado', 'español', 'tasas y visitas coloniales', 'unidad de cuenta de la plata ensayada', 'unidad de medida',
    'unidad monetaria de cuenta; no equivale a un peso físico fijo', 'usada en las tasas de Lunahuaná y Guarco')
add('patacón', 'español', 'documentos coloniales', 'peso de plata de ocho reales', 'unidad de medida', '8 reales', '')
add('real', 'español', 'documentos coloniales', 'moneda de plata', 'unidad de medida', '8 reales = 1 peso', '')

# ---------- clasificadores numerales mochica/yunga ----------
add('na', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'uno', 'número', '1', '')
add('pac', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'dos', 'número', '2', '')
add('coc', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'tres', 'número', '3', '')
add('noc', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'cuatro', 'número', '4', '')
add('exllmeetzh', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'cinco', 'número', '5', '')
add('tzhaxlltzha', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'seis', 'número', '6', '')
add('ñite', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'siete', 'número', '7', '')
add('langæss', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'ocho', 'número', '8', '')
add('tap', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'nueve', 'número', '9', '')
add('nassop', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'diez monedas / diez reales', 'número',
    '10', 'serie clasificatoria de monedas')
add('napong', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'diez hombres, caballos, cabras, casas o cualquier cosa que no sea moneda, fruta ni día', 'número',
    '10', 'serie clasificatoria "general" (animados y cosas)')
add('nacqoquixll', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'diez frutas o mazorcas', 'número', '10', 'serie clasificatoria de frutas')
add('naceess', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]', 'diez días', 'número',
    '10', 'serie clasificatoria de días')
add('ssop', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'sufijo de las decenas cuando se cuentan monedas (pac.ssop = 20; coc.ssop = 30; noc.ssop = 40)', 'número',
    note='clasificador ligado al numeral, no palabra independiente')
add('pong', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'sufijo de las decenas para personas, animales y cosas (pac.pong = 20)', 'número',
    note='clasificador "general"')
add('cqoquixll', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'sufijo de las decenas para frutas y mazorcas (pac.cqoquixll = 20)', 'número', note='clasificador de frutas')
add('ceess', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'sufijo de las decenas para días (pac.ceess = 20)', 'número', note='clasificador de días')
add('alio', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'partícula que se intercala entre unidades, decenas, centenas y millares (p. ej. napong alio oneec = 12)', 'número')
add('paleec', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'cien, en las series de monedas/animales (na.paleec = 100)', 'número', '100')
add('chieeng', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'cien, en la serie de frutas (na.chieeng = 100)', 'número', '100', 'la centena cambia según la clase contada')
add('cunö', 'mochica/yunga', 'Carrera 1644 [Villarreal 1921:112–113]',
    'mil, en las dos primeras series (na.cunö = 1 000)', 'número', '1 000')

# ---------- aimara: piedras y cuentas ----------
add('cala', 'aimara', 'Bertonio 1612, II:240', 'piedra; piedra de contar', 'registro')
add('cala paachatha', 'aimara', 'Bertonio 1612, II:240',
    'poner dos piedras en la cuenta cuando no hay más de una', 'operación')
add('calana apanocatha', 'aimara', 'Bertonio 1612, I:139',
    'poner dos piedras en la cuenta; contar por piedrecitas', 'operación')
add('hanko', 'aimara', 'Bertonio 1612, II:72', 'blanco; piedra blanca para contar lo ya pagado', 'color')
add('cchaara', 'aimara', 'Bertonio 1612, II:83', 'negro; piedra negra para contar lo que se debe', 'color')
add('chino', 'aimara', 'Bertonio 1612, II:83', 'piedrecita de contar lo que se debe de la tasa', 'registro')
add('chinocamana', 'aimara', 'Bertonio 1612, I:139', 'el que tiene cuenta de lo que se debe; contador', 'oficio')
add('chinotha', 'aimara', 'Bertonio 1612, II:174', 'el que tiene cuenta; contador', 'oficio')
add('chinoquipatha', 'aimara', 'Bertonio 1612, I:139',
    'la cuenta que se señala por nudos de lo que se da o recibe', 'registro')
add('phiscachatha', 'aimara', 'Bertonio 1612, II:270',
    'poner cinco en la cuenta cuando se cuenta con piedrecitas', 'operación')

# ---------- colores quechuas ----------
for t, g in [('yuraq', 'blanco'), ('yana', 'negro'), ('puka', 'rojo'),
             ('q\'illu', 'amarillo'), ('anqas', 'azul'), ('qumir', 'verde'),
             ('ch\'umpi', 'marrón, pardo'), ('allqa', 'mezclado, de dos colores')]:
    add(t, 'quechua', 'González Holguín 1608, s.v.', g, 'color')

# ---------- nudos y partes (términos técnicos actuales) ----------
add('cordón principal', 'español (técnico)', 'Ascher & Ascher 1981; Urton 2003',
    'cuerda horizontal de la que penden las cuerdas', 'parte del quipu')
add('cuerda superior', 'español (técnico)', 'Urton & Brezine 2005; Medrano',
    'cuerda sumatoria o "top cord"', 'parte del quipu')
add('colgante', 'español (técnico)', 'Ascher & Ascher 1981', 'cuerda que pende del cordón principal', 'parte del quipu')
add('subsidiaria', 'español (técnico)', 'Ascher & Ascher 1981', 'cuerda que pende de otra cuerda', 'parte del quipu')
add('grupo', 'español (técnico)', 'KFG; Urton 2017', 'conjunto de colgantes separado por un espacio en el cordón', 'parte del quipu')
add('nudo simple', 'español (técnico)', 'Ascher & Ascher 1981; Urton 2003', 'nudo de una o más vueltas en las unidades', 'nudo')
add('nudo largo', 'español (técnico)', 'Ascher & Ascher 1981; Urton 2003', 'nudo de 2–9 vueltas', 'nudo')
add('figura de ocho', 'español (técnico)', 'Ascher & Ascher 1981', 'nudo en ocho, normalmente en las unidades', 'nudo')
add('vuelta', 'español (técnico)', 'Ascher & Ascher 1981', 'cada giro de un nudo largo; su número es el valor', 'nudo')

with open('lexico_contable.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['termino', 'lengua', 'fuente', 'glosa',
                                      'categoria', 'equivalencia', 'nota'])
    w.writeheader(); w.writerows(R)
print('filas', len(R))
from collections import Counter
print(Counter(r['categoria'] for r in R))
print(Counter(r['lengua'] for r in R))
