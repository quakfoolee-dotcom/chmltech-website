import numpy as np, json, time, fsim as F
from multiprocessing import Pool
KP=[0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,3.0,3.5,4.0]
KB=[0.5,0.6,0.7,0.8,0.85,0.9,0.93,0.95,0.96,0.97,0.98,0.99,0.995]
import os
METHODS=os.environ.get('METHODS','ma,ses,croston,sba,tsb,boot,boot52,boot26,normfull,norm52').split(',')
TAG=os.environ.get('TAG','frun2')
CLASSES=['smooth','erratic','intermittent','lumpy']
def pop(seed, stop_share=0.0):
    items=F.make_items(seed); r=np.random.default_rng(seed+100)
    n=F.WARM+F.EVAL; res={}
    acc={m:dict(ae=0.0,e=0.0,dm=0.0) for m in METHODS if m in F.FORECASTS}
    stops=[]
    D=[]
    for it in items:
        if stop_share < 0:      # level-shift scenario: every item's demand frequency changes by x1.5 or x0.5 at a random week
            wk = int(r.integers(F.WARM, F.WARM+52)); fac = 1.5 if r.random() < 0.5 else 0.5
            D.append(F.demand_series(it,r,n,None,(wk,fac))); stops.append(None); continue
        stop = int(r.integers(F.WARM+26, F.WARM+F.EVAL-26)) if r.random()<stop_share else None
        D.append(F.demand_series(it,r,n,stop)); stops.append(stop)
    cls=[F.classify(d[:F.WARM]) for d in D]
    # aggregates[method][k][class] = [dem, fill, oh, md, endstock]
    agg={m:{} for m in METHODS}
    for d,c,st in zip(D,cls,stops):
        md=d[F.WARM:].mean() if st is None else d[F.WARM:st].mean()
        for m in METHODS:
            if m in ('boot','boot52','boot26'):
                levels=[(k,F.order_up_to_levels(d,m,k)) for k in KB]
            elif m in ('normfull','norm52'):
                levels=[(k,F.order_up_to_levels(d,m,k)) for k in KP]
            else:
                base,sig=F.parametric_parts(d,m)
                levels=[(k,base+k*sig) for k in KP]
                f=F.FORECASTS[m](d)[F.WARM:]; e=d[F.WARM:]-f
                acc[m]['ae']+=np.abs(e).mean(); acc[m]['e']+=e.mean(); acc[m]['dm']+=d[F.WARM:].mean()
            for k,S in levels:
                a,b,oh,end=F.simulate_inventory(d,S)
                key=str(k)
                agg[m].setdefault(key,{cc:[0,0,0,0,0,0] for cc in CLASSES+['all','stopped']})
                for cc in ([c,'all'] + (['stopped'] if st is not None else [])):
                    v=agg[m][key][cc]; v[0]+=a; v[1]+=b; v[2]+=oh; v[3]+=md; v[4]+=end; v[5]+=1
    return dict(agg=agg,acc=acc,classes={c:cls.count(c) for c in CLASSES})
def run(args):
    seed,stop=args; return pop(seed,stop)
if __name__=='__main__':
    import sys
    stop=float(sys.argv[1]) if len(sys.argv)>1 else 0.0
    t=time.time()
    with Pool(2) as p: R=p.map(run,[(s,stop) for s in [11,22,33,44,55]])
    json.dump(R,open(f'{TAG}_shift.json' if stop<0 else f'{TAG}_stop{int(stop*100)}.json','w'))
    print('t',round(time.time()-t), [r['classes'] for r in R])
