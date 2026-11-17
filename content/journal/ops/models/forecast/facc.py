"""Table 4 (accuracy) on the same five populations as the inventory runs. V2."""
import json, numpy as np, fsim as F
M=['zero','ma','ses','croston','sba','tsb']; out={}
for seed in [11,22,33,44,55]:
    items=F.make_items(seed); r=np.random.default_rng(seed+100); n=F.WARM+F.EVAL
    for it in items:
        r.random()                       # same draw as frun.py (stop decision), so the items match
        d=F.demand_series(it,r,n); c=F.classify(d[:F.WARM]); md=d[F.WARM:].mean()
        if md==0: continue
        for m in M:
            f=np.zeros(n) if m=='zero' else F.FORECASTS[m](d)
            e=(d[F.WARM:]-f[F.WARM:])/md
            o=out.setdefault(c,{}).setdefault(m,[[],[]]); o[0].append(np.abs(e).mean()); o[1].append(np.sqrt((e**2).mean()))
res={c:{m:(round(float(np.mean(v[0])),2),round(float(np.mean(v[1])),2)) for m,v in d.items()} for c,d in out.items()}
for c in ['intermittent','lumpy']: print(c,res[c])
zw=np.mean([ (F.demand_series(it,np.random.default_rng(0),156)[52:]==0).mean() for it in F.make_items(11)])
json.dump(res,open('facc_v2.json','w'),indent=1)
