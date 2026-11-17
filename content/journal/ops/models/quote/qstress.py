import json, numpy as np, time, qsim as Q
from multiprocessing import Pool
FIT=json.load(open('qfit.json'))
CFG={'FIFO erp':('erp',7.87,'FIFO'),'FIFO load':('load',2.99,'FIFO'),'Rec erp':('erp',3.01,'Rec'),'Rec load':('load',2.54,'Rec'),'Rec fit':('fit',2.42,'Rec')}
def weekly(js,w0=14,w1=36):
    ot=[];q=[]
    for w in range(w0,w1):
        s=[j for j in js if w*Q.HPW<=j['arr']<(w+1)*Q.HPW]
        ot.append([j['done']-j['due']<=1e-9 for j in s]); q.append([j['quote']/8 for j in s])
    return ot,q
def t_spike(name):
    rule,m,sched=CFG[name]; OT=[[] for _ in range(22)]; QQ=[[] for _ in range(22)]; win=[]
    for s in Q.SEEDS:
        js=Q.run(s,rule,m,sched,coef=FIT[sched]['coef'] if rule=='fit' else None,spike=(20,24,1.4))
        ot,q=weekly(js)
        for i in range(22): OT[i]+=ot[i]; QQ[i]+=q[i]
        sel=[j for j in js if 20*Q.HPW<=j['arr']<30*Q.HPW]; win.append(100*np.mean([j['done']-j['due']<=1e-9 for j in sel]))
    win=np.array(win)
    return name,dict(weekly_ot=[float(100*np.mean(x)) for x in OT],weekly_q=[float(np.mean(x)) for x in QQ],
                     win_ot=float(win.mean()),win_ci=float(1.96*win.std(ddof=1)/10))
def t_load(a):
    name,rate=a; rule,m,sched=CFG[name]
    rs=[Q.measure(Q.run(s,rule,m,sched,coef=FIT[sched]['coef'] if rule=='fit' else None,rate=rate)) for s in Q.SEEDS]
    return name,rate,dict(ot=float(np.mean([r['ot'] for r in rs])),quote=float(np.mean([r['quote'] for r in rs])),lt=float(np.mean([r['lt'] for r in rs])))
if __name__=='__main__':
    t=time.time()
    with Pool(2) as p:
        sp=dict(p.map(t_spike,list(CFG)))
        ld=p.map(t_load,[(n,r) for n in CFG for r in [10,11,11.8,12.4,13.0,13.6]])
    out=dict(spike=sp,load=[dict(name=n,rate=r,**v) for n,r,v in ld])
    json.dump(out,open('qstress.json','w'),indent=1)
    for n,v in sp.items(): print(n,round(v['win_ot'],1),round(v['win_ci'],1),[round(x) for x in v['weekly_ot']],[round(x,1) for x in v['weekly_q']])
    for x in out['load']: print(x['name'],x['rate'],round(x['ot'],1),round(x['quote'],2),round(x['lt'],2))
    print('t',round(time.time()-t))
