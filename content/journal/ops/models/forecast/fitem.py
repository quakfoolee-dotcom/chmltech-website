"""Per-item fill spread at the pooled 95% safety factor (population 11). V2."""
import json, numpy as np, fsim as F
ks=json.load(open('fobs_v2.json'))
r=np.random.default_rng(111); items=F.make_items(11); n=F.WARM+F.EVAL
D=[F.demand_series(it,r,n) for it in items]
for m in ['ma','croston','norm52']:
    fr=[]
    for d in D:
        a,b,_,_=F.simulate_inventory(d,F.order_up_to_levels(d,m,ks[m]['k95']))
        if a>0: fr.append(b/a*100)
    print(m,'p10 %.1f median %.1f'%(np.percentile(fr,10),np.median(fr)))
