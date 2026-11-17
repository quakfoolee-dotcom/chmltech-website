import shop
from shop import *
shop.STATIONS.update({'Cut':1,'Glaze':1,'Assemble':1})
FAM['Casement window'][2][2]=('Clean',.18); FAM['Slider window'][2][2]=('Clean',.15)
def mj(seed,rate,cv=0.4,bmean=2.0,spike=None,weeks=WARM+WEEKS+8):
    r=np.random.default_rng(seed); jobs=[]; t=0.0; end=weeks*HPW
    s2=np.log(1+cv**2)
    while True:
        lam=rate/bmean
        if spike and spike[0]*HPW<=t<spike[1]*HPW: lam*=spike[2]
        t+=r.exponential(HPW/lam)
        if t>end: break
        for _ in range(int(r.geometric(1/bmean))):
            f=FAMS[r.choice(len(FAMS),p=MIX)]; mu=FAM[f][1]; n=max(1,int(r.geometric(1/mu)))
            ops=[(st,(SETUP[st]+n*u)*r.lognormal(-s2/2,np.sqrt(s2))) for st,u in FAM[f][2]]
            plan=(len(ops)+2)*8.0
            jobs.append(dict(id=len(jobs),fam=f,units=n,arr=t,due=t+plan,plan=plan,ops=ops))
    return jobs
