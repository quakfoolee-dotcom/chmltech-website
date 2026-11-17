import json, time
from multiprocessing import Pool
from qsweep import task
GRID=dict(erp=[7,9], flat=[9,11,13,15], backlog=[-6,-5,-4,-3,-2,-1.5,-0.5], load=[1.5,2.5,3.5], fit=[1.5,2.5,3.5])
if __name__=='__main__':
    jobs=[(r,m,s) for s in ['FIFO','Rec'] for r,ms in GRID.items() for m in ms]
    with Pool(2) as p: res=p.map(task,jobs)
    old=json.load(open('qsweep.json')); json.dump(old+res,open('qsweep.json','w'))
    for r in res: print(r['sched'],r['rule'],r['m'],round(r['quote'],2),round(r['ot'],1))
