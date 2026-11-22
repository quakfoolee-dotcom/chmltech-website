import {business,locationScope,inventoryValue} from './business.mjs?demo=5d9e5d1ce6c83eb1';
import {businessDay} from './company-date.mjs?demo=5d9e5d1ce6c83eb1';
import {resolveProductBarcode} from './packaging.mjs?demo=5d9e5d1ce6c83eb1';
import {validUnicode,charLength} from './unicode.mjs?demo=5d9e5d1ce6c83eb1';
import {receivingRoleAllowed} from './receiving-policy.mjs?demo=5d9e5d1ce6c83eb1';
const must=(ok,msg)=>{if(!ok)throw Error(msg);};
const get=(rows,id)=>{const r=rows.find(x=>x.id===id);must(r,'Receiving record not found.');return r;};
const text=(v,max=500,required=true)=>{const t=String(v??'').trim();must(validUnicode(t)&&charLength(t)<=max&&(!required||t),'Enter valid receiving text within the allowed length.');return t;};
const qty=(v,zero=false)=>{const n=Number(v);must(v!==''&&v!==undefined&&Number.isSafeInteger(n)&&n>=(zero?0:1)&&n<=10000000,'Enter a whole receiving quantity within the allowed range.');return n;};
export const receivingControl=s=>s.receivingControl||{version:1,sequence:0,bins:[],inspections:[],tasks:[],history:[]};
const setup=s=>s.receivingControl||(s.receivingControl=receivingControl(s));
const next=(d,type)=>'receiving-'+type+'-'+(++d.sequence);
const loc=(s,id)=>get(s.locations,id),stock=(s,id)=>get(s.stock,id);
const scope=(s,id)=>locationScope(s,id);
const usableScope=(s,id)=>{const x=scope(s,id);return x.ownerId==='owner-self'&&!x.transit&&!x.production;};
const same=(s,a,b)=>scope(s,a).warehouseId===scope(s,b).warehouseId&&scope(s,a).ownerId===scope(s,b).ownerId;
const active=q=>q.status!=='Cancelled';
const open=t=>t.status==='Open';
const heldInspection=(s,stockId)=>receivingControl(s).inspections.find(q=>active(q)&&q.stockId===stockId);
const expired=(s,r,time=new Date().toISOString())=>{const date=s.operations?.lots?.[r.itemId+'|'+r.lot]?.expiresOn;return !!date&&date<businessDay(s,time);};
const reserved=(s,stockId)=>receivingControl(s).tasks.filter(t=>open(t)&&t.stockId===stockId).reduce((n,t)=>n+t.qty,0);
export function receivingBinCapacity(s,locationId){const bin=receivingControl(s).bins.find(b=>b.locationId===locationId);if(!bin)return null;const onHand=s.stock.filter(r=>r.locationId===locationId).reduce((n,r)=>n+r.qty,0),incoming=receivingControl(s).tasks.filter(t=>open(t)&&t.destinationId===locationId).reduce((n,t)=>n+t.qty,0);return {...bin,onHand,incoming,free:Math.max(0,bin.capacity-onHand-incoming)};}
export function receivingSuggestions(s,{stockId,kind='Putaway',inspectionId=''},time=new Date().toISOString()){
 const r=stock(s,stockId),source=loc(s,r.locationId),q=heldInspection(s,r.id),d=receivingControl(s),available=r.qty-r.committed-reserved(s,r.id);
 if(!usableScope(s,source.id)||expired(s,r,time))return [];
 if(q&&!(kind==='Putaway'&&q.id===inspectionId&&q.status==='Released'))return [];
 if(kind==='Putaway'&&!q&&source.type!=='Receiving')return [];
 if(kind==='Replenishment'&&(source.type!=='Storage'||d.bins.find(b=>b.locationId===source.id)?.role!=='Reserve'))return [];
 const remaining=q?Math.min(available,q.accepted-q.moved-reserved(s,r.id)):available;
 return d.bins.filter(b=>b.itemId===r.itemId&&b.locationId!==source.id&&same(s,source.id,b.locationId)&&usableScope(s,b.locationId)&&loc(s,b.locationId).type==='Storage'&&(kind!=='Replenishment'||b.role==='Pick face')).map(b=>{
  const c=receivingBinCapacity(s,b.locationId),limit=kind==='Replenishment'?Math.max(0,b.maximum-c.onHand-c.incoming):c.free;
  return {...c,code:loc(s,b.locationId).code,suggested:Math.max(0,Math.min(remaining,c.free,limit)),needsReplenishment:b.role==='Pick face'&&c.onHand+c.incoming<=b.minimum};
 }).filter(b=>b.suggested>0&&(kind!=='Replenishment'||b.needsReplenishment)).sort((a,b)=>(a.role==='Reserve'?0:1)-(b.role==='Reserve'?0:1)||a.code.localeCompare(b.code));
}
function photos(values=[]){must(Array.isArray(values)&&values.length<=3,'Attach up to three PNG, JPEG or WebP images.');return values.map(v=>{const name=text(v.name,120),data=String(v.data||'');must(data.length<=140000&&/^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+/]+={0,2}$/.test(data),'Each inspection image must be PNG, JPEG or WebP and no larger than 100 KB.');let bytes;try{bytes=atob(data.split(',')[1]);}catch{throw Error('Invalid inspection image.');}must(bytes.length<=102400,'Each inspection image must be PNG, JPEG or WebP and no larger than 100 KB.');must(data.startsWith('data:image/png;')?bytes.startsWith('\x89PNG\r\n\x1a\n'):data.startsWith('data:image/jpeg;')?bytes.startsWith('\xff\xd8\xff'):bytes.startsWith('RIFF')&&bytes.slice(8,12)==='WEBP','Invalid inspection image.');return {name,data};});}
function request(d,p){const id=text(p.requestId,80);must(/^[a-zA-Z0-9-]{16,80}$/.test(id),'A unique receiving request is required.');must(![...d.inspections,...d.tasks].some(r=>r.requestId===id),'This receiving request was already saved. Refresh and review it.');return id;}
const history=(d,ctx,action,id,note='')=>{must(d.history.length<10000,'Receiving history is full. Export and review before continuing.');d.history.push({time:ctx.time,actor:ctx.actor||'Local owner',actorId:ctx.actorId||ctx.actor||'Local owner',action,id,note});};
export function beforeReceiving(s,command,p,ctx){
 const d=receivingControl(s);if(!d.inspections.length)return;
 const r=['moveStock','countStock','scrapStock'].includes(command)?s.stock.find(r=>r.id===p.stockId):null,q=r&&heldInspection(s,r.id);
 if(q){const t=d.tasks.find(t=>t.id===ctx.rootPayload?.id);must(command==='moveStock'&&ctx.rootCommand==='receiving:finishTask'&&t&&open(t)&&t.inspectionId===q.id&&q.status==='Released'&&t.stockId===r.id&&t.destinationId===p.locationId&&t.qty===Number(p.qty),'Use the approved inspection putaway task for this held stock.');}
 if(command==='receiveStock'||command==='moveStock'){
  const itemId=r?.itemId||p.itemId,lot=r?.lot||String(p.lot||'UNTRACKED'),dest=s.stock.find(x=>x.locationId===p.locationId&&x.itemId===itemId&&x.lot===lot);
  must(!dest||!heldInspection(s,dest.id),'Do not mix new stock into an active inspection lot.');
 }
}
export function receivingCommand(s,command,p,ctx){
 if(!command.startsWith('receiving:'))return null;
 must(receivingRoleAllowed(command,ctx.role||'Admin'),'Your role cannot perform this receiving action.');
 let d=setup(s),id=p.id;const value=Math.round(inventoryValue(s)*100),run=(c,payload)=>{const result=ctx.dispatch(s,c,payload,{now:ctx.time});Object.assign(s,result.state);d=setup(s);return result.resultId;};
 if(command==='receiving:loadDemo'){
  if(d.demo)return {type:'Receiving demo already loaded',message:'Receiving demo already loaded',reference:d.demo.warehouseId,resultId:d.demo.warehouseId};
  must(p.reviewed===true,'Review the demo scope before creating sample stock.');
  const warehouseId=run('business:warehouse',{code:'RCV222',name:'Receiving Demo 2.22 / 收货示例 / 收貨範例'}),locations=s.locations.filter(l=>scope(s,l.id).warehouseId===warehouseId),receiving=locations.find(l=>l.type==='Receiving').id,hold=locations.find(l=>l.type==='Hold').id,batches=[];
  for(const language of ['EN','CN']){const itemId=run('createItem',{sku:'RCV222-'+language,name:language==='EN'?'Demo inspected tumbler':'示例检验保温杯 / 範例檢驗保溫杯',description:'DEMO ONLY / 仅供示例 / 僅供範例',uom:'ea',reorderPoint:0});run('setCost',{id:itemId,unitCost:12.5,reason:'Explicit demo acquisition cost; original products unchanged'});run('receiveStock',{itemId,locationId:receiving,lot:'RCV222-'+language+'-LOT',qty:100});const source=s.stock.find(r=>r.itemId===itemId&&r.locationId===receiving),reserve=run('business:location',{warehouseId,ownerId:'owner-self',code:'R222-'+language+'-R',name:language==='EN'?'Demo reserve':'示例储备位 / 範例儲備位',type:'Storage'}),pick=run('business:location',{warehouseId,ownerId:'owner-self',code:'R222-'+language+'-P',name:language==='EN'?'Demo pick face':'示例拣货位 / 範例揀貨位',type:'Storage'});d.bins.push({locationId:reserve,itemId,capacity:100,role:'Reserve',minimum:0,maximum:100},{locationId:pick,itemId,capacity:20,role:'Pick face',minimum:5,maximum:20});batches.push({language,itemId,stockId:source.id,receiving,hold,reserve,pick});}
  d.demo={warehouseId,batches};history(d,ctx,'Receiving demo created',warehouseId);return {type:'Receiving demo created',message:'Receiving demo created',reference:warehouseId,resultId:warehouseId};
 }
 if(command==='receiving:bin'){
  const l=loc(s,p.locationId);get(s.items,p.itemId);must(l.type==='Storage'&&l.pickable&&usableScope(s,l.id),'Choose an owned storage bin outside transit and production.');const capacity=qty(p.capacity),role=p.role;must(['Reserve','Pick face'].includes(role),'Choose Reserve or Pick face.');const minimum=role==='Pick face'?qty(p.minimum,true):0,maximum=role==='Pick face'?qty(p.maximum):capacity;must(minimum<maximum&&maximum<=capacity,'Bin minimum must be below maximum, within capacity.');must(!s.stock.some(r=>r.locationId===l.id&&r.qty>0&&r.itemId!==p.itemId),'This bin contains another product.');must(!d.tasks.some(t=>open(t)&&t.destinationId===l.id),'Finish or cancel incoming tasks before changing bin rules.');const entry={locationId:l.id,itemId:p.itemId,capacity,role,minimum,maximum};const old=d.bins.find(b=>b.locationId===l.id);if(old)Object.assign(old,entry);else d.bins.push(entry);id=l.id;
 }else if(command==='receiving:createInspection'){
  const source=stock(s,p.stockId),hold=loc(s,p.holdLocationId),sourceLoc=loc(s,source.locationId);must(['Receiving','Hold'].includes(sourceLoc.type)&&!sourceLoc.pickable&&usableScope(s,sourceLoc.id)&&source.qty>0&&!source.committed,'Inspect unreserved stock from receiving or quality hold.');must(hold.type==='Hold'&&!hold.pickable&&usableScope(s,hold.id)&&same(s,source.locationId,hold.id),'Choose a quality-hold bin in the same owned warehouse.');must(s.operations?.tracking?.[source.itemId]!=='Serial','This inspection workflow supports lot-tracked stock.');must(!heldInspection(s,source.id),'This stock already has an active inspection.');const requestId=request(d,p),total=source.qty,itemId=source.itemId,lot=source.lot;must(!s.stock.some(r=>r.id!==source.id&&r.locationId===hold.id&&r.itemId===itemId&&r.lot===lot&&r.qty>0),'Choose a hold bin without other stock of this product and lot.');if(source.locationId!==hold.id)run('moveStock',{stockId:source.id,locationId:hold.id,qty:total});const held=s.stock.find(r=>r.locationId===hold.id&&r.itemId===itemId&&r.lot===lot);id=next(d,'inspection');d.inspections.push({id,requestId,stockId:held.id,itemId,lot,qty:total,status:'Draft',accepted:0,rejected:0,moved:0,reference:text(p.reference,120),note:text(p.note,1000,false),results:null,photos:[],createdAt:ctx.time,createdBy:ctx.actor||'Local owner'});
 }else if(command==='receiving:submitInspection'){
  const q=get(d.inspections,id);must(q.status==='Draft','Only a draft inspection can be submitted.');const accepted=qty(p.accepted,true),rejected=qty(p.rejected,true);must(accepted+rejected===q.qty,'Accepted and rejected quantities must equal the inspected quantity.');const reason=text(p.defectReason,500,rejected>0),results={};for(const key of ['quantity','appearance','lot']){must(['Pass','Fail','Not applicable'].includes(p[key]),'Record every inspection checklist result.');results[key]=p[key];}must(!Object.values(results).includes('Fail')||rejected>0,'Failed checks require rejected units and a defect reason.');q.accepted=accepted;q.rejected=rejected;q.defectReason=reason;q.results=results;q.outcome=text(p.outcome,1000,false);q.photos=photos(p.photos);q.status='Submitted';q.inspectedAt=ctx.time;q.inspectedBy=ctx.actor||'Local owner';
 }else if(command==='receiving:approveInspection'){
  const q=get(d.inspections,id);must(q.status==='Submitted'&&p.reviewed===true,'Review a submitted inspection before release.');must(!expired(s,stock(s,q.stockId),ctx.time),'Expired stock cannot be released.');q.releaseReason=text(p.reason);q.status='Released';q.approvedAt=ctx.time;q.approvedBy=ctx.actor||'Local owner';q.approvedRole=ctx.role||'Admin';
 }else if(command==='receiving:cancelInspection'){
  const q=get(d.inspections,id);must(['Draft','Submitted'].includes(q.status),'Released inspections cannot be cancelled.');q.cancelReason=text(p.reason);q.status='Cancelled';
 }else if(command==='receiving:createTask'){
  const requestId=request(d,p),r=stock(s,p.stockId),kind=p.kind;must(['Putaway','Replenishment'].includes(kind),'Choose a receiving task type.');const recommendation=receivingSuggestions(s,p,ctx.time).find(b=>b.locationId===p.destinationId),amount=qty(p.qty);must(recommendation&&amount<=recommendation.suggested,'Stock, release or bin capacity changed. Review the suggested quantity.');id=next(d,'task');d.tasks.push({id,requestId,kind,stockId:r.id,itemId:r.itemId,lot:r.lot,sourceId:r.locationId,destinationId:p.destinationId,qty:amount,inspectionId:p.inspectionId||'',status:'Open',note:text(p.note,500,false),createdAt:ctx.time,createdBy:ctx.actor||'Local owner'});
 }else if(command==='receiving:finishTask'){
  const t=get(d.tasks,id),r=stock(s,t.stockId);must(open(t),'Only an open receiving task can be completed.');must(p.reviewed===true&&String(p.sourceCode||'').trim().toUpperCase()===loc(s,t.sourceId).code.toUpperCase()&&String(p.destinationCode||'').trim().toUpperCase()===loc(s,t.destinationId).code.toUpperCase(),'Scan the exact source and destination bins and review the move.');must(resolveProductBarcode(s,p.productCode).item.id===t.itemId&&String(p.lot||'').trim()===t.lot&&qty(p.qty)===t.qty,'Product, lot and quantity must match the task.');must(r.locationId===t.sourceId&&r.itemId===t.itemId&&r.lot===t.lot&&r.qty-r.committed>=t.qty&&!expired(s,r,ctx.time),'Task source changed or is expired. Cancel and plan again.');const capacity=receivingBinCapacity(s,t.destinationId);must(capacity&&capacity.itemId===t.itemId&&capacity.onHand+capacity.incoming<=capacity.capacity,'Destination capacity changed. Review the task.');run('moveStock',{stockId:t.stockId,locationId:t.destinationId,qty:t.qty,serials:p.serials});const latest=get(d.tasks,id);latest.status='Completed';latest.completedAt=ctx.time;latest.completedBy=ctx.actor||'Local owner';if(latest.inspectionId)get(d.inspections,latest.inspectionId).moved+=latest.qty;
 }else if(command==='receiving:cancelTask'){
  const t=get(d.tasks,id);must(open(t),'Only an open receiving task can be cancelled.');t.cancelReason=text(p.reason);t.status='Cancelled';
 }else throw Error('Unknown receiving action.');
 must(Math.round(inventoryValue(s)*100)===value,'Receiving actions must preserve company inventory value.');history(d,ctx,command,id);return {type:'Receiving workflow saved',message:'Receiving workflow saved',reference:id,resultId:id};
}
export function validateReceiving(s,ctx={}){
 if(!s.receivingControl)return true;const d=s.receivingControl;must(d.version===1&&Number.isSafeInteger(d.sequence)&&d.sequence>=0&&['bins','inspections','tasks','history'].every(k=>Array.isArray(d[k])&&d[k].length<=10000),'Invalid receiving controls.');
 const transitional=ctx.nested&&ctx.rootCommand==='receiving:finishTask';
 must(new Set(d.bins.map(b=>b.locationId)).size===d.bins.length,'Duplicate receiving bin rules.');
 for(const b of d.bins){get(s.items,b.itemId);must(loc(s,b.locationId).type==='Storage'&&usableScope(s,b.locationId),'Invalid receiving bin.');qty(b.capacity);qty(b.minimum,true);qty(b.maximum);must(['Reserve','Pick face'].includes(b.role)&&b.minimum<b.maximum&&b.maximum<=b.capacity,'Invalid bin capacity or replenishment levels.');const c=receivingBinCapacity(s,b.locationId);must(c.onHand+(transitional?0:c.incoming)<=c.capacity&&!s.stock.some(r=>r.qty>0&&r.locationId===b.locationId&&r.itemId!==b.itemId),'Bin capacity or product restriction exceeded.');}
 const ids=new Set(),requests=new Set();let imageBytes=0;
 for(const q of d.inspections){must(!ids.has(q.id)&&!requests.has(q.requestId),'Duplicate receiving identifier.');ids.add(q.id);requests.add(q.requestId);const r=stock(s,q.stockId);get(s.items,q.itemId);qty(q.qty);qty(q.moved,true);must(['Draft','Submitted','Released','Cancelled'].includes(q.status)&&r.itemId===q.itemId&&r.lot===q.lot,'Invalid inspection identity.');if(q.status!=='Draft'&&q.results){must(q.accepted+q.rejected===q.qty,'Inspection quantities changed.');photos(q.photos);imageBytes+=q.photos.reduce((n,p)=>n+p.data.length,0);}if(q.status==='Released')must(q.approvedBy&&q.approvedRole==='Admin'&&q.releaseReason&&q.moved<=q.accepted,'Inspection approval evidence is missing.');if(active(q)&&!transitional)must(loc(s,r.locationId).type==='Hold'&&!loc(s,r.locationId).pickable&&r.qty===q.qty-q.moved&&!r.committed,'Controlled inspection stock changed outside approved putaway.');}
 must(imageBytes<=1400000,'Inspection attachments exceed the workspace limit of 1 MB.');
 for(const t of d.tasks){must(!ids.has(t.id)&&!requests.has(t.requestId),'Duplicate receiving identifier.');ids.add(t.id);requests.add(t.requestId);qty(t.qty);get(s.items,t.itemId);stock(s,t.stockId);must(['Open','Completed','Cancelled'].includes(t.status)&&['Putaway','Replenishment'].includes(t.kind)&&t.sourceId!==t.destinationId&&same(s,t.sourceId,t.destinationId),'Invalid receiving task.');if(t.inspectionId){const q=get(d.inspections,t.inspectionId);must(q.status==='Released'&&q.stockId===t.stockId&&q.itemId===t.itemId,'Task release evidence is missing.');}if(t.status==='Completed')must(t.completedBy&&t.completedAt,'Task completion evidence is missing.');}
 if(!transitional)for(const q of d.inspections.filter(active)){const tasks=d.tasks.filter(t=>t.inspectionId===q.id);must(tasks.filter(t=>t.status==='Completed').reduce((n,t)=>n+t.qty,0)===q.moved&&tasks.filter(open).reduce((n,t)=>n+t.qty,0)+q.moved<=q.accepted,'Inspection task quantities exceed the approved release.');}
 return true;
}

