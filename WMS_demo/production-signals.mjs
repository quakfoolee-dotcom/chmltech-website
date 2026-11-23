import {production,productionShortages} from './production.mjs?demo=2d15b6e9cd84b84d';
import {localDay} from './dashboard.mjs?demo=2d15b6e9cd84b84d';
// Read-only projections. No alert is persisted as a workflow state or cost.
const presentations=new Map([
 ['Planned',['neutral','○']],['Pending',['neutral','○']],['Cancelled',['neutral','—']],
 ['In progress',['blue','▶']],['Active',['blue','▶']],
 ['Completed',['green','✓']],['Done',['green','✓']],['Approved',['green','✓']],
 ['Submitted',['amber','◷']],['Rejected',['red','!']]
]);
export function productionStatus(status){const [tone,icon]=presentations.get(status)||['neutral','○'];return {label:status,tone,icon};}
const signal=(code,label,tone)=>({code,label,tone}),none=()=>[signal('none','No action needed','neutral')];
const rank={red:0,amber:1,blue:2,green:3,neutral:4};
const sorted=rows=>rows.sort((a,b)=>rank[a.tone]-rank[b.tone]);
const terminal=w=>['Completed','Cancelled'].includes(w.status);
const overdue=(s,order,now)=>order.due&&order.due<localDay(now,s.organization?.timezone);
export function workAttention(s,order,w,now=new Date().toISOString()){
 if(terminal(w)||order.status==='Cancelled')return none();const out=[];
 if(overdue(s,order,now))out.push(signal('overdue','Overdue','red'));
 if(w.status==='Planned'){
  const waiting=w.dependsOn.some(id=>order.workOrders.find(child=>child.id===id)?.status!=='Completed');
  if(waiting)out.push(signal('waiting-children','Waiting for child work','amber'));
  // Unfinished subassemblies are a dependency, not a purchased-material shortage.
  const rows=productionShortages(s,w,order.warehouseId,typeof now==='string'?now:new Date(now).toISOString()).filter(r=>!waiting||!r.bomId);
  if(rows.some(r=>r.short>0))out.push(signal('material-shortage','Material shortage','red'));
  if(rows.some(r=>!Number.isFinite(s.operations.costs[r.itemId])||s.operations.costs[r.itemId]<=0))out.push(signal('missing-cost','Material cost missing','red'));
  if(!out.length)out.push(signal('ready-start','Ready to start','green'));
 }else if(w.status==='In progress'){
  const labor=production(s).labor.filter(l=>l.workId===w.id);
  if(labor.some(l=>l.status==='Submitted'))out.push(signal('labor-approval','Labor awaiting approval','amber'));
  const active=w.stages.find(stage=>stage.status==='Active'),last=active?labor.filter(l=>l.stage===active.number).at(-1):null;
  if(last?.status==='Rejected')out.push(signal('labor-rejected','Rejected labor needs review','red'));
  if(w.stages.every(stage=>stage.status==='Done'))out.push(w.completed>0?signal('partial-receipt','Finish remaining receipt','amber'):signal('ready-receipt','Ready to receive finished goods','blue'));
  else if(!out.some(a=>['labor-approval','labor-rejected'].includes(a.code)))out.push(signal('active-stage','Continue active stage','blue'));
 }
 return out.length?sorted(out):none();
}
export function orderAttention(s,order,now=new Date().toISOString()){
 if(terminal(order))return none();const all=order.workOrders.flatMap(w=>workAttention(s,order,w,now)).filter(a=>a.code!=='none'),unique=[...new Map(all.map(a=>[a.code,a])).values()];
 const urgent=unique.filter(a=>['red','amber'].includes(a.tone));if(urgent.length)return sorted(urgent).slice(0,2);
 return unique.length?sorted(unique).slice(0,1):none();
}
export function stageAttention(s,order,w,stage,now=new Date().toISOString()){
 if(stage.status==='Done'||terminal(w))return none();
 if(stage.status==='Active')return workAttention(s,order,w,now);
 return [signal('earlier-stage',w.status==='Planned'?'Start work order first':'Waiting for earlier stage','neutral')];
}
export function laborAttention(s,l){
 if(l.status==='Submitted')return [signal('labor-approval','Labor awaiting approval','amber')];
 if(l.status==='Rejected'){const w=production(s).orders.flatMap(o=>o.workOrders).find(w=>w.id===l.workId);if(w&&!terminal(w)&&w.stages[l.stage-1]?.status==='Active'&&production(s).labor.filter(entry=>entry.workId===w.id&&entry.stage===l.stage).at(-1)?.id===l.id)return [signal('labor-rejected','Rejected labor needs review','red')];}
 return none();
}
