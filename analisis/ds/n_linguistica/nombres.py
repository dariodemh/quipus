# -*- coding: utf-8 -*-
"""Genera nombres_propios.csv: pachacas, ayllus, curacas y barrios, en orden
documental, con segmentación silábica aproximada (para plantillas)."""
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import csv, re

VOW = set('aeiou')
def norm(w):
    w = w.lower()
    for a, b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ü','u')]:
        w = w.replace(a, b)
    w = w.replace('ç','s').replace('z','s').replace('x','S')
    w = w.replace('ch','C').replace('ll','L').replace('ñ','N').replace('rr','r').replace('qu','k')
    w = re.sub(r'hu(?=[aeiou])','w',w); w = w.replace('hu','u')
    w = re.sub(r'gu([ao])',r'w\1',w); w = re.sub(r'g([ei])',r'h\1',w)
    w = re.sub(r'c([ei])',r's\1',w); w = w.replace('c','k').replace('q','k').replace('h','')
    return w.replace('v','b')

def syll(w):
    w = norm(w)
    if not any(c in VOW for c in w): return []
    nu=[]; i=0
    while i < len(w):
        if w[i] in VOW:
            j=i+1
            while j < len(w) and w[j] in VOW: j+=1
            nu.append((i,j)); i=j
        else: i+=1
    sy=[]; prev=0
    for k,(a,b) in enumerate(nu):
        cons=w[prev:a]
        if k==0: on=cons
        else:
            if len(cons)>=2 and cons[-1] in 'lr': on=cons[-2:]; ex=cons[:-2]
            else: on=cons[-1:] if cons else ''; ex=cons[:-1]
            if ex: sy[-1]+=ex
        sy.append(on+w[a:b]); prev=b
    if prev < len(w): sy[-1]+=w[prev:]
    return [x for x in sy if x]

R=[]
def add(nombre,tipo,entidad,fuente,orden,nota=''):
    parts=[syll(w) for w in nombre.split()]
    s=[x for p in parts for x in p]
    R.append(dict(nombre=nombre,tipo=tipo,entidad=entidad,fuente=fuente,
                  orden=orden,silabas=' '.join('-'.join(p) for p in parts),
                  n_silabas=len(s),nota=nota))

# Collique, visita de Martínez Rengifo 1571 (Rostworowski, Costa peruana, pachacas)
for i,n in enumerate(['Chuquiruro','Caxa Chumbi','Vilca Tanta','Vilca Chumbi','Chumbi Guarco',
                      'Chumbi Tanta','Carua Guanco','Carua Chumbi','Chinqui Yanga','Chuquitanta'],1):
    add(n,'pachaca','Collique (valle del Chillón)','Rostworowski, Costa peruana, Visita 1571',i,
        'la primera pachaca lleva el nombre del cacique principal Chuquiruro' if i == 1 else '')

# curacas y principales
for i,(n,ent,src,nota) in enumerate([
    ('Chuquiruro','Collique','Rostworowski, Costa peruana, Visita 1571','cacique principal epónimo'),
    ('don Francisco Yaybi','Collique','Rostworowski, Costa peruana, Visita 1571','cacique que vende tierras de Vilca Tanta'),
    ('don Hernando Nacar','Collique','Rostworowski, Costa peruana (AGI 1586)','curaca de Collique en 1586'),
    ('Francisco Nacar','Collique','Rostworowski, Costa peruana (AGI 1586)','hijo/mozo del curaca'),
    ('Rodrigo Asmat','Collique','Rostworowski, Costa peruana (AGI 1586)','figura en el padrón de 1571'),
    ('don Diego Sacllachumbi','Guancayo (Carabayllo)','Rostworowski, Costa peruana (AGN 1605)','cacique de los guancayos'),
    ('Lunaguanay','Lunahuaná','Rostworowski, Costa peruana (AGI 1534)','curaca principal, primera guaranga'),
    ('Llaquipa / Llaquixa','Lunahuaná','Rostworowski, Costa peruana (AGI 1534)','señor residente en las minas'),
    ('Allauca','Lunahuaná (Mullibamba)','Rostworowski, Costa peruana (AGI 1534)','curaca mitmaq, tercera guaranga'),
    ('don Francisco Llacsaguana','Lunahuaná','Rostworowski, Costa peruana (BN A-537, 1580)','cacique principal y gobernador del valle'),
    ('don Diego Allaucan','Pacarán (Lunahuaná)','Rostworowski, Costa peruana (BN A-537, 1580)','cacique de Pacarán'),
    ('don Pedro Camaluana','Jucxu (Lunahuaná)','Rostworowski, Costa peruana (BN A-537, 1580)','curaca de la guaranga de Jucxu'),
    ('Chuquimancu','Lunahuaná / Guarco','Garcilaso, citado por Rostworowski','señor que resiste a los incas; atribución discutida'),
    ('don Alonso Guarac','Guarco','Rostworowski, Costa peruana (AGI 1558)','cacique principal del valle del Guarco'),
    ('don Thomas','Guarco','Rostworowski, Costa peruana (AGI 1558)','principal del valle'),
    ('don Juan Caruatanta','Guarco','Rostworowski, Costa peruana (AGI 1558)','indio antiguo natural del valle'),
    ('Llactamala','Guarco','Rostworowski, Costa peruana (AGI 1558)','indio antiguo natural del valle'),
],1):
    add(n,'curaca',ent,src,i,nota)

# Huarochirí: ayllus (Rostworowski, lista de padrones del s. XVIII)
ayllus = {
 'Casta':['Yacapar','Yanac','Binquiguamo','Allauca','Guallacocha'],
 'Carapoma':['Capam','Guari','Collana','Allauca','Julca','Sulca','Callan','Tres Casas','Pariac','Iapani'],
 'Collata':['Ayna michuy','Huanca yanac','Paucartambo','Mango','Huchu','Vilca','Colca','Mango rraqui','Collata'],
 'Chacalla':['Chulla','Callan'],
 'Santa Eulalia de Apocaya':['Xipu','Vicas','Namoc'],
 'Huanza':['Sulca','Churi','Tres Casas','Pariac','Vilca','Capcha','Callan','Ichoca','Chaupin'],
 'Iris':['Curaca','Julcamarca','Chaupin','Araui'],
 'Jicamarca':['Cullí','Chullas','Yechaca'],
 'Larao':['Pauza','Allauca','Chaupin','Liviac'],
 'Otao':['Otao','Chauca','Bimqui','Yacarpar','Yanac'],
}
for ent, names in ayllus.items():
    for i,n in enumerate(names,1):
        add(n,'ayllu',f'Huarochirí: {ent}','Rostworowski, Costa peruana (padrones s. XVIII)',i)

# linajes de Collata/Casta según Hyland 2017 (lectura discutida)
add('Alluka','linaje','Collata / Casta (Huarochirí)','Hyland 2017 (hipótesis de desciframiento)',1,
    'nombre que Hyland lee en tres cordones finales del khipu A')
add('Yakapar','linaje','Collata / Casta (Huarochirí)','Hyland 2017 (hipótesis de desciframiento)',2,
    'nombre leído por analogía en el khipu B')

# Lunahuaná: barrios actuales (posibles ayllus reducidos), orden de la lista
barrios = ['Caltopilla','Paraíso','Caltopa','Lúcumo','Casalla','San Pedro','Catapaya',
           'Con-Con y Ramadilla','Socsi','Paullu','San Jerónimo','Langla','Lunahuaná',
           'Patapampa','Condoray','Uchupampa']
for i,n in enumerate(barrios,1):
    add(n,'barrio/ayllu','Lunahuaná','Rostworowski, Costa peruana (trabajo de campo)',i,
        'posible rezago de ayllu prehispánico')

# Chincha: categorías documentales (no hay lista de pachacas en la fuente local)
for i,n in enumerate(['labradores','pescadores','mercaderes'],1):
    add(n,'categoría social','Chincha','Rostworowski, Costa peruana (Aviso, s. XVI)',i,
        '10 000 de cada grupo según la relación; no son nombres propios')

with open('nombres_propios.csv','w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['nombre','tipo','entidad','fuente','orden','silabas','n_silabas','nota'])
    w.writeheader(); w.writerows(R)
print('filas',len(R))
from collections import Counter
print(Counter(r['tipo'] for r in R))
for r in R[:12]: print(r['nombre'],r['silabas'],r['n_silabas'])
