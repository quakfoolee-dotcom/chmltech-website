import json, numpy as np
METHODS=['ma','ses','croston','sba','tsb','boot']
def curve(R,m,cls):
    keys=sorted(R[0]['agg'][m].keys(),key=float); pts=[]
    for k in keys:
        per=[r['agg'][m][k][cls] for r in R]
        fill=[v[1]/v[0]*100 for v in per]; wos=[v[2]/v[3] for v in per]
        pts.append((float(k),np.mean(fill),np.mean(wos),fill,wos))
    return pts
def at(pts,tgt):
    for a,b in zip(pts,pts[1:]):
        if a[1]<tgt<=b[1]:
            f=(tgt-a[1])/(b[1]-a[1]); per=[wa+f*(wb-wa) for wa,wb in zip(a[4],b[4])]
            return a[2]+f*(b[2]-a[2]), per
    return None,None
def table(fn,tgts=(90,95)):
    R=json.load(open(fn)); out={}
    for cls in ['all','smooth','erratic','intermittent','lumpy']:
        out[cls]={}
        for m in METHODS:
            out[cls][m]={t:at(curve(R,m,cls),t) for t in tgts}
    return R,out
if __name__=='__main__':
    R,out=table('frun_stop0.json')
    for cls in out:
        print(cls,{m:{t:(round(v[0],2) if v[0] else None) for t,v in out[cls][m].items()} for m in METHODS})
    # paired difference vs ses at 95 overall per pop
    for cls in ['all','intermittent','lumpy']:
        for m in METHODS:
            a=np.array(out[cls][m][95][1]); b=np.array(out[cls]['ma'][95][1]); d=a-b
            print(cls,m,'vs MA',round(d.mean(),2),'+-',round(1.96*d.std(ddof=1)/np.sqrt(len(d)),2), 'pct',round((d/b).mean()*100,1))
    acc={m:np.mean([r['acc'][m]['ae']/r['acc'][m]['dm'] for r in R]) for m in METHODS if m!='boot'}
    bias={m:np.mean([r['acc'][m]['e']/r['acc'][m]['dm'] for r in R]) for m in METHODS if m!='boot'}
    print('scaled MAE',{m:round(v,3) for m,v in acc.items()}); print('bias',{m:round(v,3) for m,v in bias.items()})
