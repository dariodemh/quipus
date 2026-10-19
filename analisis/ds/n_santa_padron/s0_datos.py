"""s0_datos.py -- construye (a) los 133 grupos de seis cuerdas de los 6 quipus del Santa
(UR087-UR092) desde analisis/datos/cuerdas.csv, y (b) el padron de 1670 en orden,
transcrito de Urton 2017, Apendice A (lineas 4118-4145 de fuentes_txt) y contrastado
con Medrano y Urton 2018, tabla 4.
No modifica nada fuera de analisis/ds/n_santa_padron/.
"""
import pandas as pd, numpy as np, re, json

D = './analisis/datos/'
IDS = ['UR087', 'UR088', 'UR089', 'UR090', 'UR091', 'UR092']
KH = dict(zip(IDS, ['KH0323', 'KH0324', 'KH0325', 'KH0326', 'KH0327', 'KH0328']))
PUB_N = dict(zip(IDS, [48, 9, 34, 17, 15, 10]))  # Urton 2017:229 / Medrano y Urton 2018

# ---------------------------------------------------------------- (a) khipus
def grupos_seis(verbose=False):
    """Mismos criterios de exclusion que 05_etnohistoria/santa_grupos.py
    (cuerdas sueltas que no forman grupo de seis)."""
    c = pd.read_csv(D + 'cuerdas.csv', low_memory=False)
    out = []
    for k in IDS:
        x = c[(c.kfg == k) & (c.nivel == 0)].copy()
        x['n'] = x.cuerda.str[1:].astype(int)
        x = x.sort_values('n')
        if k == 'UR087':
            sz = x.groupby('grupo').cuerda.transform('size'); x = x[sz > 1]
        if k == 'UR089':
            x = x[~x.n.isin([73, 140])]
        if k == 'UR090':
            x = x[~x.n.isin([31, 38, 63, 64, 65, 66])]
        x = x.reset_index(drop=True)
        assert len(x) % 6 == 0, (k, len(x))
        for g in range(len(x)//6):
            b = x.iloc[6*g:6*g+6]
            out.append(dict(kfg=k, g=g, first=b.cuerda.iloc[0],
                            vals=[int(v) if pd.notna(v) else 0 for v in b.valor],
                            unions=b.union.tolist(), colors=b.color.tolist(),
                            color1=b.color.iloc[0], union1=b.union.iloc[0]))
    return pd.DataFrame(out)

if __name__ == '__main__':
    G = grupos_seis()
    G['nhom'] = G.colors.apply(lambda cs: len(set(map(str, cs))))
    print('grupos por quipu:', G.groupby('kfg').size().to_dict(), ' total', len(G),
          ' (Urton 48/9/34/17/15/10 = 133)')
    print('grupos con color homogeneo (6 iguales):', int((G.nhom == 1).sum()), '/', len(G))
    print('n colores distintos de 1.a cuerda por quipu:',
          G.groupby('kfg').color1.nunique().to_dict())
    print('primeras 12 filas (kfg,g,color1,union1,p1..p6):')
    print(G[['kfg','g','color1','union1']].join(
        pd.DataFrame(G.vals.tolist(), columns=[f'p{i}' for i in range(1,7)])).head(12).to_string())
    G.to_csv('santos_grupos133.csv', index=False)

# ---------------------------------------------------------------- (b) padron
# Transcripcion normalizada del Apendice A de Urton 2017 (pp. 239-240).
# Cada entrada = (nombre de pila, resto del nombre). Se conserva el ORDEN del documento.
PADRON = {
 'Namus': [
  ('Po','ticlla condor'), ('lorenso','tapia'), ('franco','nuñes'), ('Juo','chauca'),
  ('diego','pardaue'), ('diego','xara'), ('antonio','de Roxas'), ('Po','artiaga'),
  ('juo','salvador'), ('juo','de Roxas'), ('franco','rroxas'), ('Andres','Yapan'),
  ('gabriel','chuquimaygo'), ('juo','Bapta hijo del coxo'), ('juo','corongo hijo de simon'),
  ('juo','po haçaña hijo de coxo'), ('po','joseph hijo del coxo'),
  ('juo','chauca hijo de juo chauca')],
 'Corongo': [
  ('don franco','Ramos'), ('don Migl','carhuahuanca'), ('marcos','carhuayamoc'),
  ('juo','tantaruna'), ('Benito','colquixari'), ('Antonio','carhuahuanca'),
  ('Nicolas','colquixari'), ('Juo','Diego'), ('Antonio','ygnacio'), ('po','huaman'),
  ('franco','pomamango'), ('franco','salvador'), ('phelipe','paucarmango'),
  ('juo','chucimango'), ('Agn','Chuquimango'), ('nicolas','alexandro'),
  ('joseph','Roque'), ('donmingo','saluador'), ('jacinto','saluador'), ('pedro','pablo'),
  ('jacinto','de la cruz'), ('juo','de la cruz'), ('esteban','chuquimango')],
 'Cuyuchin': [
  ('don juo','chuquinaupa'), ('juo','carhuahuanca'), ('Joseph','colquimunan'),
  ('diego','tanta riexi'), ('Alonso','pon luis'), ('juo','Ramos rupay'),
  ('juo','cullquimunan'), ('po','marcos'), ('diego','huaman')],
 'Cusca': [
  ('juo','quispe'), ('domingo','quispi'), ('joseph','rincon'), ('Alonso','montoya'),
  ('Joseph','carhuapari'), ('Agn','montalbo'), ('Juo','belasques')],
 'Guauyan': [
  ('Alons','chucho'), ('luis','pari'), ('diego','carhuahuachic'), ('Po','Cochachin'),
  ('Agn','nunahuanca'), ('Franco','Pinedo'), ('franco','chuquinaupaico'),
  ('franco','incos'), ('Germo','Vilcayauri'), ('Agn','Rimanga'), ('Juo','Toribio'),
  ('Juo','Alonso'), ('Alonso','huanca'), ('Joseph','asencio'), ('Pedro','huanca'),
  ('Marcos','de la cruz'), ('Jacinto','Hanampa'), ('Jacinto','Collas'),
  ('felipe','Santiago'), ('d. Nicolas','lluyacpoma'), ('Miguel','llanqui'),
  ('Juo','carhuaxambo'), ('Diego','chuquihuanca'), ('franco','Asencio'),
  ('Agn','sebastian'), ('domingo','incos'), ('Nicolas','lara'),
  ('Juo','huaquin morales'), ('joseph','campos'), ('Juo','culquiyanac'),
  ('domingo','ancxito'), ('juo bapta','quispicondor'), ('franco','nunahuanca'),
  ('Agn','carhuacota'), ('Juo','cullquiyanac'), ('leon Domo','cullquiyanac'),
  ('leon xpoval','Tello'), ('leon Po','julez'), ('Felis','cochachin'),
  ('Nicolas','Ocxac'), ('juo','chicho')],
 'Ucore': [
  ('Franco','rrojas'), ('xpual','tantayari'), ('marcos','Juares'),
  ('juo','rimaycachin'), ('juo','de la cruz'), ('jacinto','carhuamenta'),
  ('juo','Albares'), ('Domingo','chuquimango'), ('juo','rimay cachin'),
  ('Alonso','Baltazar'), ('Andres','yanac'), ('domingo','felipe'),
  ('fabian','Ramos'), ('juo','Antonio'), ('juo','quispe'), ('juco','xpual'),
  ('felipe','parina'), ('domingo','garcia'), ('domingo','huacha'),
  ('franco','chuquicondor'), ('felipe','barbudo'), ('Po','martin'),
  ('Lorenso','asnabal'), ('Blas','clemente cruz'), ('Po','tomas pullic'),
  ('Juo','gaspar'), ('Alonso','yaulli fausto'), ('Martin','chuquirimac'),
  ('Antonio','carhuahuachic'), ('juo','francisco'), ('juo','de rroxas'),
  ('bernabe','principe')],
}
# Orden de las pachacas en el documento (Apendice A y tabla 12.3)
ORDEN_DOC = ['Namus', 'Corongo', 'Cuyuchin', 'Cusca', 'Guauyan', 'Ucore']
# Emparejamiento propuesto en Urton 2017, tabla 12.3
PACHACA_KHIPU = {'Namus': 'UR091', 'Corongo': 'UR090', 'Cuyuchin': 'UR092',
                 'Cusca': 'UR088', 'Guauyan': 'UR087', 'Ucore': 'UR089'}

def norm(s):
    s = s.lower().strip()
    s = (s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o')
          .replace('ú','u').replace('ñ','n'))
    return re.sub(r'\s+', ' ', s)

def tabla_padron():
    rows = []
    for p in ORDEN_DOC:
        for i, (fn, sn) in enumerate(PADRON[p]):
            rows.append(dict(pachaca=p, orden=i, nombre_pila=fn, resto=sn,
                             nombre=(fn + ' ' + sn).strip(),
                             norm=norm(fn + ' ' + sn), fnorm=norm(fn),
                             hijo_de=bool(re.search(r'hijo', sn, re.I)),
                             don=bool(re.search(r'\bdon\b', fn, re.I)),
                             ausente=False))
    return pd.DataFrame(rows)

if __name__ == '__main__':
    P = tabla_padron()
    print('\npadron: tamanos', P.groupby('pachaca').size().to_dict(),
          ' total', len(P), '(Urton: 19/23/9/7/41/32=131; Medrano: 18/23/9/7/41/32=130)')
    print('primeros nombres de pila por pachaca:',
          P.groupby('pachaca').fnorm.nunique().to_dict())
    print('nombres "hijo de":', P[P.hijo_de][['pachaca','orden','nombre']].to_string(index=False))
    P.to_csv('padron_orden.csv', index=False, encoding='utf-8-sig')
