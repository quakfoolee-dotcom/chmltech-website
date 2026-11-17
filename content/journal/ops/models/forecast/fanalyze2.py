import json, numpy as np, fanalyze as A
from scipy import stats
M=['ma','ses','croston','sba','tsb','boot','boot52','boot26','normfull','norm52']
A.METHODS=M
T=stats.t.ppf(0.975,4)
for fn in ['frun2_stop0.json','frun2_shift.json']:
    R,out=A.table(fn); print('==',fn)
    for cls in out:
        print(cls,{m:(round(out[cls][m][95][0],3) if out[cls][m][95][0] else None) for m in M})
    print('90%',{m:round(out['all'][m][90][0],2) for m in M})
    for t in (95,90):
      for m in M:
        a=np.array(out['all'][m][t][1]); b=np.array(out['all']['ma'][t][1]); p=(a-b)/b*100
        print(t,m,'pct',round(p.mean(),1),'+-',round(T*p.std(ddof=1)/np.sqrt(5),1))
