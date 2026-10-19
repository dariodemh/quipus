"""Extrae el Apéndice B (metadatos de 72 memorias) de Medrano 2019 a CSV."""
import re, fitz, pandas as pd
from pathlib import Path
R = Path(__file__).resolve().parents[2]
d = fitz.open(R / 'encontrado/MEDRANO-SENIORTHESIS-2019.pdf')
pages = []
for i in range(177, 189):
    t = re.sub(r'\s+', ' ', d[i].get_text())
    t = re.sub(r'^\d{3} (Appendix B Transcription Metadata )?', '', t)  # número de página
    t = re.sub(r'memoria title author .*? lat_zone ', '', t)            # cabecera repetida
    pages.append(t)
txt = ' '.join(pages).replace('***Volume 2 Begins*** ', '')
pat = re.compile(r'(?P<memoria>\d{1,2}) (?P<pre>.{0,400}?)(?P<ls>\d+) (?P<le>\d+) (?P<year>1[4-7]\d\d) (?P<lat>-?\d+\.\d+) (?P<lon>-?\d+\.\d+) '
                 r'(?P<dist>[\d.,]+) (?P<alt>\d+) (?P<city>.{1,60}?) (?P<type>pnar|pnum|elicit|summ) (?P<prepost>pre|post) '
                 r'(?P<lang>quechua|aymara) (?P<int>int|unint) (?P<pop>[sml]) (?P<spk>sng|mult|na) (?P<cur>yes|no) (?P<zone>south|central|north)')
rows = [m.groupdict() for m in pat.finditer(txt)]
df = pd.DataFrame(rows)
df['memoria'] = df.memoria.astype(int)
df = df.drop_duplicates('memoria').sort_values('memoria')
df.rename(columns={'pre': 'titulo_autor'}).to_csv(Path(__file__).with_name('medrano_metadatos_72.csv'), index=False)
print(len(df), sorted(set(range(1, 73)) - set(df.memoria)))
print(df.type.value_counts().to_dict())
