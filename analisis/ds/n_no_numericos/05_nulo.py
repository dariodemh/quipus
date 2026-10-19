"""Indice final de anomalia decimal (v3) + nulos por permutacion dentro de quipu.
Salidas: cuerdas_anom.csv, quipus_indice.csv, nulo_resumen.csv
"""
import pandas as pd, numpy as np, re, json

RNG = np.random.default_rng(20261018)
C = pd.read_csv('analisis/ds/n_no_numericos/cuerdas_dedup.csv', dtype={'nudos': str, 'color': str, 'notas': str})
Q = pd.read_csv('analisis/datos/quipus.csv')
pat = re.compile(r'^(\d+)([A-Z?]+)\(([\d.]+),([SZU?])\)(?:,([\d.]+))?$')
rows = []
for r in C.itertuples():
    s = r.nudos
    if not isinstance(s, str) or not s.strip(): continue
    for k, seg in enumerate(s.split(';')):
        seg = seg.strip()
        if not seg: continue
        m = pat.match(seg)
        if not m: continue
        n, t, pos, d, v = m.groups()
        rows.append((r.kfg, r.cuerda, int(k), int(n), t, float(pos), d,
                     float(v) if v is not None else np.nan))
K = pd.DataFrame(rows, columns=['kfg','cuerda','k','n','tipo','pos','dir','val'])

def expo(v):
    if pd.isna(v) or v <= 0: return -1
    iv = int(round(v))
    return len(str(iv)) - len(str(iv).rstrip('0'))
K['exp'] = [expo(v) for v in K.val]
K['turns'] = [ (v/10.0**e) if (e>=0 and pd.notna(v)) else np.nan for v,e in zip(K.val,K.exp)]
K['isl'] = K.groupby(['kfg','cuerda'])['k'].transform('max') == K.k
K['exp_next'] = K.groupby(['kfg','cuerda'])['exp'].shift(-1)

K['v_S_unit']  = (K.tipo=='S') & (K.exp==0)
K['v_LE_big']  = (K.tipo.isin(['L','LL','E','EE'])) & (K.turns>9)
K['v_E_weird'] = (K.tipo.isin(['E','EE'])) & (K.val>0) & (np.abs(np.log10(K.val)-np.round(np.log10(K.val)))>1e-9)
K['v_inv']     = (K.exp_next>K.exp) & (K.exp>=0) & (K.exp_next>=0)
K['v_dup']     = (K.exp>=0) & (K.groupby(['kfg','cuerda','exp'])['k'].transform('size')>1)
K['anom'] = K[['v_S_unit','v_LE_big','v_E_weird','v_inv','v_dup']].any(axis=1)

cord = K.groupby(['kfg','cuerda']).agg(nclust=('k','size'),
    vS=('v_S_unit','sum'), vLE=('v_LE_big','sum'), vEw=('v_E_weird','sum'),
    vinv=('v_inv','sum'), vdup=('v_dup','sum')).reset_index()
cord = C[['kfg','cuerda','nivel','padre','color','torsion','union','largo','terminacion','valor','grupo']].merge(
    cord, on=['kfg','cuerda'], how='left')
for c in ['nclust','vS','vLE','vEw','vinv','vdup']: cord[c]=cord[c].fillna(0)
cord['knotless']=cord.nclust==0
cord['color']=cord.color.fillna('')
cord['color_comp']=cord.color.str.count(r'[:\-/]')+1
cord['rich_color']=cord.color_comp>=2
cord['has_child']=cord.cuerda.isin(cord.padre.dropna())
cord['impossible_zero']=(~cord.knotless)&(cord.valor==0)
# flags estructurales por cuerda
cl = K[K.exp>=0].groupby(['kfg','cuerda']).agg(nv=('exp','size'), nu=('exp','nunique'), mx=('exp','max'), mn=('exp','min')).reset_index()
cord = cord.merge(cl, on=['kfg','cuerda'], how='left')
cord['nv']=cord.nv.fillna(0); cord['nu']=cord.nu.fillna(0)
cord['dup_cord'] = cord.vdup>0
cord['inv_cord'] = cord.vinv>0
cord['same_cord'] = (cord.nv>=2) & (cord.nu==1)
cord['multi_cord'] = cord.nv>=2
cord['span_exp'] = cord.mx - cord.mn
cord.to_csv('analisis/ds/n_no_numericos/cuerdas_anom.csv', index=False)

def qagg(d):
    n=len(d); nk=(~d.knotless).sum(); ncl=d.nclust.sum()
    multi=d.multi_cord.sum()
    return pd.Series(dict(ncuerdas=n, ncuerdas_nudo=nk, nclusters=ncl,
        frac_sin_nudo=1-nk/n if n else np.nan,
        D=((d.dup_cord)&d.multi_cord).sum()/max(multi,1),
        I=d.vinv.sum()/max(d.nv.sum()-nk,1),
        Q=d.same_cord.sum()/max(multi,1),
        R=((d.knotless)&(d.rich_color)).sum()/max((d.knotless).sum(),1),
        Z=d.impossible_zero.sum()/max(n,1),
        C=(d.vS.sum()+d.vLE.sum()+d.vEw.sum())/max(ncl,1),
        vS=d.vS.sum(), vLE=d.vLE.sum(), vEw=d.vEw.sum(), vinv=d.vinv.sum(), vdup=d.vdup.sum(),
        n_multi=multi, n_same=d.same_cord.sum(), n_dup=(d.dup_cord&d.multi_cord).sum(),
        n_sin_nudo_rico=((d.knotless)&(d.rich_color)).sum(),
        frac_rico=(d.color_comp>=2).mean(), n_color=len(set(d.color[d.color!=''])),
        n_subs=(d.nivel>0).sum(), frac_subs=(d.nivel>0).mean(), n_top=(d.union=='T').sum(),
        frac_topd=(d.union=='T').mean(), n_imposible=d.impossible_zero.sum()))
QI = cord.groupby('kfg').apply(qagg, include_groups=False).reset_index().merge(Q, on='kfg', how='left')
QI['score'] = 0.35*QI.D + 0.25*QI.I + 0.20*QI.Q + 0.10*QI.R + 0.05*QI.Z + 0.05*QI.C
QI.to_csv('analisis/ds/n_no_numericos/quipus_indice.csv', index=False)

# ---------- NULOS ----------
B = 999
rowsn=[]
for q, dk in K.groupby('kfg'):
    dc = cord[cord.kfg==q]
    nk=len(dc); 
    cord_sizes = dc.nclust.astype(int).values
    # mascaras por posicion para C (tipo)
    type_codes = dk.tipo.values
    maskS = (dk.exp.values==0)
    maskLE = ((dk.tipo.isin(['L','LL','E','EE'])).values) & (dk.turns.values>9)
    maskEw = ((dk.tipo.isin(['E','EE'])).values) & (dk.val.values>0) & (np.abs(np.log10(dk.val.values)-np.round(np.log10(dk.val.values)))>1e-9)
    # posiciones: shift por cuerda para inversion
    # recomputar por cuerda requiere codigos
    cords_idx = pd.factorize(dk.cuerda)[0]
    ncl_cord = np.bincount(cords_idx)
    # observados
    expv = dk.exp.values.copy()
    # D,I,Q desde cuerdas
    obs = QI[QI.kfg==q].iloc[0]
    o = np.array([obs.D, obs.I, obs.Q, obs.R, obs.Z, obs.C])
    null = np.zeros((B,6))
    # precompute R hypergeom-like null by permuting rich among cords
    rich = dc.rich_color.values.astype(bool); kn = dc.knotless.values.astype(bool)
    nknotless = kn.sum(); nrich = rich.sum()
    for b in range(B):
        # permutar exponentes entre todos los clusters del quipu (preserva tamaños de cuerda)
        ep = RNG.permutation(expv)
        # D, Q, I
        dup=0; inv=0; same=0; multi=0; npairs=0; nv=0
        start=0
        for m in ncl_cord:
            e = ep[start:start+m]; start+=m
            ev = e[e>=0]; nv += len(ev)
            if len(e)>=2:
                multi+=1
                if len(ev)>=2:
                    npairs += len(ev)-1
                    inv += int((ev[1:]>ev[:-1]).sum())
                    if len(np.unique(ev))==1: same+=1
            if len(ev)!=len(np.unique(ev)): dup+=1
        # tipos permutados para C
        tp = RNG.permutation(type_codes)
        cS = ((tp=='S')&maskS).sum(); cLE=((np.isin(tp,['L','LL','E','EE']))&maskLE).sum(); cEw=((np.isin(tp,['E','EE']))&maskEw).sum()
        # color permutado dentro de cuerdas
        rp = RNG.permutation(rich)
        R = (rp&kn).sum()/max(nknotless,1)
        null[b] = [dup/max(multi,1), inv/max(npairs,1), same/max(multi,1), R, obs.Z, (cS+cLE+cEw)/max(len(tp),1)]
    comp = 0.35*null[:,0]+0.25*null[:,1]+0.20*null[:,2]+0.10*null[:,3]+0.05*null[:,4]+0.05*null[:,5]
    obscomp = 0.35*o[0]+0.25*o[1]+0.20*o[2]+0.10*o[3]+0.05*o[4]+0.05*o[5]
    p_hi = (1+(comp>=obscomp).sum())/(B+1)
    p_lo = (1+(comp<=obscomp).sum())/(B+1)
    rowsn.append(dict(kfg=q, score_obs=obscomp, null_mean=comp.mean(), null_sd=comp.std(),
        z=(obscomp-comp.mean())/(comp.std()+1e-9), p_hi=p_hi, p_lo=p_lo,
        D=o[0], I=o[1], Q=o[2], R=o[3], Z=o[4], C=o[5],
        D_null=null[:,0].mean(), I_null=null[:,1].mean(), Q_null=null[:,2].mean(),
        C_null=null[:,5].mean(), nclusters=len(dk)))
NUL=pd.DataFrame(rowsn)
NUL.to_csv('analisis/ds/n_no_numericos/nulo_resumen.csv', index=False)
print('Nulos:', len(NUL), 'B=',B)
print(NUL[['score_obs','null_mean','D','D_null','I','I_null','Q','Q_null','C','C_null','p_hi']].describe().round(3).to_string())
print('\nTop 20 score (>=10 cuerdas con nudo):')
m=NUL.merge(QI[['kfg','ncuerdas','ncuerdas_nudo','n_multi','procedencia']],on='kfg')
m=m[m.ncuerdas_nudo>=10].sort_values('score_obs',ascending=False)
print(m[['kfg','ncuerdas','ncuerdas_nudo','n_multi','score_obs','D','I','Q','C','p_hi','procedencia']].head(25).round(3).to_string(index=False))
