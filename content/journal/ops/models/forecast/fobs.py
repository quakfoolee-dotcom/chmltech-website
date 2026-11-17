"""Obsolescence test (Table 4). V2. Items stop selling at week 104; 64 further weeks.
Each method runs at its safety factor for 95% fill in the stationary runs."""
import json, numpy as np, fsim as F, fanalyze as A
R0=json.load(open('frun2_stop0.json')); Rb=json.load(open('frun_tsbb_stop0.json'))
M=['ma','ses','croston','sba','tsb','tsb10','tsb20','boot','norm52']
def kat(R,m):
    pts=A.curve(R,m,'all')
    for a,b in zip(pts,pts[1:]):
        if a[1]<95<=b[1]: return a[0]+(95-a[1])/(b[1]-a[1])*(b[0]-a[0])
ks={m:kat(Rb if m.startswith('tsb') and m!='tsb' else R0,m) for m in M}
wos={m:A.at(A.curve(Rb if m in('tsb10','tsb20') else R0,m,'all'),95)[0] for m in M}
items=F.make_items(11)[:300]; r=np.random.default_rng(999); STOP=104; n=STOP+64
out={m:dict(lag=[],orders=0,units=0.0,dead=[],rise=0) for m in M}
for it in items:
    d=F.demand_series(it,r,n,STOP); nz=np.flatnonzero(d[:STOP])
    if len(nz)==0: continue
    last=nz[-1]; md=d[F.WARM:STOP].mean()
    for m in M:
        S=F.order_up_to_levels(d,m,ks[m]); o=out[m]
        ref=S[last]; below=np.flatnonzero(S[last+1:]<0.2*ref)
        o['lag'].append(below[0]+1 if len(below) else np.inf)
        if S[min(n-1,last+20)]>ref*1.001: o['rise']+=1
        pipe=np.zeros(n+F.L+2); oh=max(S[F.WARM],0.0); bk=0.0
        for t in range(F.WARM,n):
            oh+=pipe[t]; c=min(bk,oh); oh-=c; bk-=c
            ip=oh-bk+pipe[t+1:t+F.L].sum(); q=max(0.0,S[t]-ip); pipe[t+F.L]+=q
            if t>last and q>0: o['orders']+=1; o['units']+=q
            x=d[t]; s=min(x,oh); oh-=s; bk+=x-s
        o['dead'].append(oh/md if md>0 else np.nan)
res={}
for m in M:
    o=out[m]; L=np.array(o['lag']); med=np.median(L)
    res[m]=dict(k95=round(ks[m],3),stock95=round(wos[m],3),median_lag=None if np.isinf(med) else float(med),
                share_never=round(float(np.isinf(L).mean()),2),orders_after=o['orders'],units_after=round(o['units']),
                rise_share=round(o['rise']/len(L),2),median_dead_wks=round(float(np.nanmedian(o['dead'])),1))
    print(m,res[m])
json.dump(res,open('fobs_v2.json','w'),indent=1)
