import json, numpy as np, qsim as Q
FIT=json.load(open('qfit.json'))
CFG={'FIFO erp base':('erp',2,'FIFO'),'FIFO erp 95':('erp',7.87,'FIFO'),'FIFO load':('load',2.99,'FIFO'),'Rec erp':('erp',3.01,'Rec'),'Rec load':('load',2.54,'Rec'),'Rec fit':('fit',2.42,'Rec')}
out={}
for name,(rule,m,sched) in CFG.items():
    q=[];buck={'small':[], 'medium':[], 'large':[]}; qb={'small':[], 'medium':[], 'large':[]}; late=[]
    for s in Q.SEEDS[:50]:
        js=Q.run(s,rule,m,sched,coef=FIT[sched]['coef'] if rule=='fit' else None)
        for j in js:
            if not (Q.WARM*Q.HPW<=j['arr']<(Q.WARM+Q.WEEKS)*Q.HPW): continue
            b='small' if j['pwork']<8 else ('medium' if j['pwork']<24 else 'large')
            ok=j['done']-j['due']<=1e-9; buck[b].append(ok); qb[b].append(j['quote']/8); q.append(j['quote']/8); late.append(max(0,(j['done']-j['due'])/8))
    q=np.array(q)
    out[name]=dict(p10=float(np.percentile(q,10)),p50=float(np.percentile(q,50)),p90=float(np.percentile(q,90)),
                   share={b:len(v) for b,v in buck.items()},ot={b:float(100*np.mean(v)) for b,v in buck.items()},q={b:float(np.mean(v)) for b,v in qb.items()},
                   n20=float(np.sum(np.array(late)>20)/50), n10=float(np.sum(np.array(late)>10)/50), worst=float(np.max(late)))
    print(name,{k:(round(v,1) if isinstance(v,float) else {a:round(b,1) for a,b in v.items()}) for k,v in out[name].items()})
json.dump(out,open('qsize.json','w'),indent=1)
