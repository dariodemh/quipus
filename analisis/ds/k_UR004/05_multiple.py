"""UR004 - correccion por comparaciones multiples (Holm y BH).
p empiricos finales, definiciones CORRECTAS de grupo. Familia = 10 pruebas."""
import numpy as np
tests = {
 'T1  colgante=suma subsidiarias':   0.302,
 'T1b colgante=suma (>=2 subs)':    1.000,
 'T2  colgante=suma descendientes': 0.319,
 'T3  grupo: cuerda=suma resto (limpio)': 0.152,
 'T4  suma grupo=cuerda ajena':     0.003,
 'A   sumas de grupo repetidas':    0.002,
 'B   cord.1 adyacente=suma grupo': 1.000,
 'C   tramo maximo de color':       0.006,
 'T8  color adyacente igual (lag1)':0.001,
 'T9  entropia color por grupo':    0.014,
}
names=list(tests); p=np.array([tests[k] for k in names]); m=len(p)
order=np.argsort(p); ps=p[order]; nm=[names[i] for i in order]
holm=np.minimum(np.maximum.accumulate((m-np.arange(m))*ps),1)
bh=ps*m/np.arange(1,m+1); bh=np.minimum.accumulate(bh[::-1])[::-1]; bh=np.minimum(bh,1)
print(f'{"prueba":40s} {"p":>6s} {"Holm":>6s} {"BH":>6s}')
for i in range(m):
    print(f'{nm[i]:40s} {ps[i]:6.3f} {holm[i]:6.3f} {bh[i]:6.3f}')
