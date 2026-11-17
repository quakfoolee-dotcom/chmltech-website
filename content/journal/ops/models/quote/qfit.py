import numpy as np, json, qsim as Q
TRAIN=list(range(2000,2050))
out={}
for sched in ['FIFO','Rec']:
    X=[];y=[]
    for s in TRAIN:
        js=Q.run(s,'erp',2,sched)
        for j in js:
            if Q.WARM*Q.HPW<=j['arr']<(Q.WARM+Q.WEEKS)*Q.HPW:
                X.append([1,j['backlog'],j['pwork'],j['pweld'],j['nops']]); y.append((j['done']-j['arr'])/8)
    X=np.array(X); y=np.array(y)
    c,*_=np.linalg.lstsq(X,y,rcond=None)
    r2=1-((y-X@c)**2).sum()/((y-y.mean())**2).sum()
    # compare: R2 of erp-only predictor (nops)
    X0=X[:,[0,4]]; c0,*_=np.linalg.lstsq(X0,y,rcond=None); r20=1-((y-X0@c0)**2).sum()/((y-y.mean())**2).sum()
    out[sched]=dict(coef=c.tolist(),r2=float(r2),r2_routing=float(r20),n=len(y))
    print(sched,np.round(c,4),round(r2,3),round(r20,3),len(y))
json.dump(out,open('qfit.json','w'),indent=1)
