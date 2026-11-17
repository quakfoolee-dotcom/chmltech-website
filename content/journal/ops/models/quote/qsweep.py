import numpy as np, json, time, qsim as Q
from multiprocessing import Pool
FIT=json.load(open('qfit.json'))
GRID=dict(erp=[0,1,2,3,4,5,6,8,10,12], flat=[6,8,10,12,14,16,18,20,24,28], backlog=[-1,0,1,2,3,4,6,8,10],
          load=[0,1,2,3,4,5,6,8,10,12], fit=[0,1,2,3,4,5,6,8,10,12])
def task(a):
    rule,m,sched=a
    rs=[Q.measure(Q.run(s,rule,m,sched,coef=FIT[sched]['coef'] if rule=='fit' else None)) for s in Q.SEEDS]
    ot=np.array([r['ot'] for r in rs])
    return dict(rule=rule,m=m,sched=sched,ot=float(ot.mean()),ot_ci=float(1.96*ot.std(ddof=1)/10),
                quote=float(np.mean([r['quote'] for r in rs])),lt=float(np.mean([r['lt'] for r in rs])),
                tard=float(np.mean([r['tard'] for r in rs])),early=float(np.mean([r['early'] for r in rs])),
                p95late=float(np.mean([r['p95late'] for r in rs])),ots=ot.tolist())
if __name__=='__main__':
    t=time.time()
    jobs=[(r,m,s) for s in ['FIFO','Rec'] for r,ms in GRID.items() for m in ms]
    with Pool(2) as p: res=p.map(task,jobs)
    json.dump(res,open('qsweep.json','w'))
    for r in res: print(r['sched'],r['rule'],r['m'],round(r['quote'],2),round(r['ot'],1),round(r['tard'],2))
    print('t',round(time.time()-t))
