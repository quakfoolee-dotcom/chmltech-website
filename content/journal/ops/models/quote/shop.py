import numpy as np, heapq, json, sys
from collections import defaultdict

HPW = 40.0  # working hours per week
STATIONS = {'Cut':2,'CNC':1,'Weld':1,'Clean':1,'Glaze':2,'Assemble':2,'DoorPrep':1,'Pack':1}
SETUP = defaultdict(lambda:0.25, {'Weld':0.4})
FAM = {  # mix, mean units, routing with per-unit hours
 'Casement window': (0.35, 10, [('Cut',.15),('Weld',.30),('Clean',.12),('Glaze',.20),('Assemble',.25),('Pack',.08)]),
 'Slider window':   (0.25, 10, [('Cut',.12),('Weld',.25),('Clean',.10),('Glaze',.18),('Pack',.06)]),
 'Patio door':      (0.15, 3,  [('Cut',.30),('CNC',.40),('Weld',.60),('Clean',.25),('Glaze',.50),('Assemble',.60),('Pack',.15)]),
 'Entry door':      (0.15, 3,  [('CNC',.50),('DoorPrep',.80),('Glaze',.30),('Assemble',.70),('Pack',.15)]),
 'Custom shape':    (0.10, 4,  [('Cut',.40),('CNC',.60),('Weld',.90),('Clean',.40),('Glaze',.60),('Assemble',.80),('Pack',.20)]),
}
FAMS=list(FAM); MIX=np.array([FAM[f][0] for f in FAMS])
QUOTE = 10*8.0   # quoted lead time: 10 working days, in working hours
WARM, WEEKS = 10, 50

def make_jobs(seed, rate, weeks=WARM+WEEKS, spike=None):
    r=np.random.default_rng(seed); jobs=[]; t=0.0
    end=weeks*HPW
    while True:
        lam = rate
        if spike and spike[0]*HPW <= t < spike[1]*HPW: lam = rate*spike[2]
        t += r.exponential(HPW/lam)
        if t>end: break
        f=FAMS[r.choice(len(FAMS),p=MIX)]; mu=FAM[f][1]
        n=max(1,int(r.geometric(1/mu)))
        ops=[(st, (SETUP[st]+n*u)*r.lognormal(-0.03,0.25)) for st,u in FAM[f][2]]
        jobs.append(dict(id=len(jobs),fam=f,units=n,arr=t,due=t+QUOTE,ops=ops))
    return jobs

def simulate(jobs, rule='FIFO', release='push', B=24.0, cap=None, down=None, strict=False, bn_rule=None, age_cap=None, hold_cap=None, late_cap=None):
    """rule: FIFO, EDD, SPT, CR. release: push | dbr (weld-load rope) | conwip (cap jobs)."""
    ev=[]; seq=0
    def push(t,typ,d):
        nonlocal seq; heapq.heappush(ev,(t,seq,typ,d)); seq+=1
    for j in jobs:
        j.update(wst={}, k=0, rel=None, done=None, qin=None, wait=0.0, proc=sum(p for _,p in j['ops']))
        push(j['arr'],'arr',j['id'])
    busy={s:0 for s in STATIONS}; Q={s:[] for s in STATIONS}
    pool=[]; weld_load=0.0; onfloor=0
    downuntil=-1; inproc={}  # weld job -> (finish, ver)
    ver=defaultdict(int)
    wip_area=0.0; last=0.0; wip=0
    if down: push(down[0],'down',down[1])
    def prio(j,s,now):
        p=j['ops'][j['k']][1]
        rule_=rule if (bn_rule is None or s=='Weld') else 'FIFO'
        if age_cap is not None and s=='Weld' and now-j['qin']>=age_cap:
            return -1e12+j['qin']          # aged order: oldest first, ahead of all others
        if late_cap is not None and s=='Weld' and now-j['due']>=late_cap:
            return -1e12+j['due']          # order more than late_cap late: earliest due first
        return prio2(j,s,now,rule_,p)
    def prio2(j,s,now,rule,p):
        if rule=='FIFO': return j['qin']
        if rule=='EDD': return j['due']
        if rule=='SPT': return p
        rem=sum(pp for _,pp in j['ops'][j['k']:])
        if rule=='MDD': return max(j['due'], now+rem)
        return (j['due']-now)/rem
    def weldh(j): return sum(p for s,p in j['ops'][j['k']:] if s=='Weld')
    def try_start(s,now):
        while Q[s] and busy[s]<STATIONS[s] and not (s=='Weld' and now<downuntil):
            j=min(Q[s], key=lambda x: prio(x,s,now)); Q[s].remove(j)
            busy[s]+=1; p=j['ops'][j['k']][1]; j['wait']+=now-j['qin']; j['wst'][s]=j['wst'].get(s,0)+now-j['qin']
            if s=='Weld': inproc[j['id']]=now+p
            push(now+p,'fin',(j['id'],ver[j['id']]))
    def enter(j,now):
        s=j['ops'][j['k']][0]; j['qin']=now; Q[s].append(j); try_start(s,now)
    def release_jobs(now):
        nonlocal weld_load, onfloor, wip
        pool.sort(key=lambda x:x['due'])
        i=0
        while i<len(pool):
            j=pool[i]; w=weldh(j); ok=True
            forced = hold_cap is not None and now-j['arr']>=hold_cap
            if release=='dbr' and w>0 and weld_load+w>B and weld_load>1e-6 and not forced: ok=False
            if release=='conwip' and onfloor>=cap: ok=False
            if ok:
                pool.pop(i); j['rel']=now; weld_load+=w; onfloor+=1; enter(j,now)
            else:
                if release=='conwip': break
                if strict:
                    # strict EDD rope: hold all later weld jobs; non-weld jobs may still pass
                    i+=1
                    while i<len(pool):
                        if weldh(pool[i])==0:
                            jj=pool.pop(i); jj['rel']=now; onfloor+=1; enter(jj,now)
                        else: i+=1
                    break
                i+=1
    J={j['id']:j for j in jobs}
    while ev:
        t,_,typ,d=heapq.heappop(ev)
        wip_area+=wip*(t-last); last=t
        if typ=='arr':
            j=J[d]; wip+=1
            if release=='push': j['rel']=t; onfloor+=1; enter(j,t)
            else: pool.append(j); release_jobs(t)
        elif typ=='fin':
            jid,v=d
            if v!=ver[jid]: continue
            j=J[jid]; s=j['ops'][j['k']][0]; busy[s]-=1
            if s=='Weld':
                inproc.pop(jid,None); weld_load-=j['ops'][j['k']][1]
            j['k']+=1
            if j['k']<len(j['ops']): enter(j,t)
            else:
                j['done']=t; wip-=1; onfloor-=1
            try_start(s,t)
            if release!='push': release_jobs(t)
        elif typ=='down':
            downuntil=t+d
            for jid,f in list(inproc.items()):
                ver[jid]+=1; inproc[jid]=f+d; push(f+d,'fin',(jid,ver[jid]))
            push(t+d,'up',None)
        elif typ=='up':
            try_start('Weld',t)
    return jobs, wip_area/last

def metrics(jobs, w0=WARM, w1=WARM+WEEKS):
    sel=[j for j in jobs if w0*HPW<=j['arr']<w1*HPW and j['done'] is not None]
    lt=np.array([j['done']-j['arr'] for j in sel])/8
    late=np.array([max(0,j['done']-j['due']) for j in sel])/8
    floor=np.array([j['done']-j['rel'] for j in sel])/8
    wait=np.array([j['wait'] for j in sel]); proc=np.array([j['proc'] for j in sel])
    return dict(n=len(sel), ontime=float((late==0).mean()*100), lt_mean=float(lt.mean()),
                lt_p95=float(np.percentile(lt,95)), tard=float(late.mean()), floor_lt=float(floor.mean()),
                queue_share=float(wait.sum()/(wait.sum()+proc.sum())*100))
