import pandas as pd, numpy as np
pd.set_option('display.width',200)
c=pd.read_csv('analisis/datos/cuerdas.csv')
d=c[c.kfg=='AS069'].copy().sort_values('orden').reset_index(drop=True)
d['pos_in']=d.orden-d.groupby('grupo').orden.transform('min')
print("== resumen estructural ==")
print("cuerdas:", len(d), "| grupos:", d.grupo.nunique())
print("nivel:", d.nivel.value_counts().to_dict())
print("con nudos:", int(d.nudos.notna().sum()), "| sin nudos:", int(d.nudos.isna().sum()))
print("valor max:", d.valor.max(), "| suma valores:", d.valor.sum())
print("valores distintos (>0):", d[d.valor>0].valor.nunique(), "| cuerdas valor>0:", int((d.valor>0).sum()))
print("cuerdas valor>0 repetido (valor aparece >1 vez):",
      int(d[d.valor>0].valor.map(d[d.valor>0].valor.value_counts()).gt(1).sum()))
print("largo: media %.1f min %.1f max %.1f"%(d.largo.mean(),d.largo.min(),d.largo.max()))
print("torsion:", d.torsion.value_counts().to_dict(), "| union:", d.union.value_counts(dropna=False).to_dict())
print("terminacion:", d.terminacion.value_counts().to_dict())
print()
# color
print("color == W:", int((d.color=='W').sum()), "| != W:", int((d.color!='W').sum()))
print("colores distintos:", d.color.nunique())
mk=d[d.pos_in==0]
print("primeras cuerdas de grupo (pos_in=0):", len(mk), " de ellas coloreadas:", int((mk.color!='W').sum()))
print("colores del marcador (pos_in=0 y color!=W) distintos:", mk[mk.color!='W'].color.nunique())
# base palette of markers
base = mk[mk.color!='W'].color.str.extract(r'^([A-Za-z:]+)')[0]
print("base dominante de marcadores (top):", base.value_counts().head(12).to_dict())
print()
# group size dist
print("distribucion tamano grupo:", d.groupby('grupo').size().value_counts().sort_index().to_dict())
# subsidiaries
print("nivel1:", int((d.nivel==1).sum()), "nivel2:", int((d.nivel==2).sum()))
print("cuerdas con subsidiarias (madres):", d[d.nivel>0].padre.nunique())
