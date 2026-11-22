import {executionGroup,executionPack} from './execution-view.mjs';
export {executionGroup,executionPack,groupView,packView} from './execution-view.mjs';
import {scanItem,orderScope,locationScope} from './business.mjs';
import {pickMeta,shippingMeta} from './operations.mjs';
import {validUnicode,charLength} from './unicode.mjs';
const must=(ok,msg)=>{if(!ok)throw Error(msg);};
const find=(rows,id)=>{const r=rows.find(x=>x.id===id);must(r,'Record not found.');return r;};
const text=(v,max=100)=>{const t=String(v??'').trim();must(validUnicode(t)&&charLength(t)<=max,'Invalid scan text.');return t;};
const code=v=>text(v).toUpperCase();
const qty=v=>{const n=Number(v);must(Number.isSafeInteger(n)&&n>0&&n<=10000000,'Quantity must be a positive whole number.');return n;};
const serials=v=>(Array.isArray(v)?v:String(v||'').split(/[\n,]/)).map(x=>text(x)).filter(Boolean);
const setup=s=>s.warehouseExecution||(s.warehouseExecution={version:1,groups:{},packing:{},requests:[]});
const event=(type,reference,resultId=null)=>({type,reference,resultId,message:type});
const sum=counts=>Object.values(counts||{}).reduce((n,x)=>n+x.qty,0);
const request=(s,p)=>{const id=text(p.requestId,80);must(/^[a-zA-Z0-9-]{16,80}$/.test(id),'A scan request identifier is required.');const w=setup(s);must(!w.requests.includes(id),'Scan already recorded. Refresh and review the saved quantity.');must(w.requests.length<100000,'Export and review the scan history before adding more scans.');w.requests.push(id);};
const scopeKey=(s,p)=>{const x=orderScope(s,find(s.orders,p.orderId));return x.warehouseId+'|'+x.ownerId;};
function scan(s,p,pick,counts,used,source=false){
 const item=scanItem(s,p.code),n=qty(p.qty),lot=text(p.lot),bin=code(p.sourceCode),values=serials(p.serials);
 const candidates=pick.allocations.map((a,i)=>({a,i})).filter(({a})=>a.itemId===item.id&&a.lot===lot&&(!source||find(s.locations,find(s.stock,a.sourceStockId).locationId).code.toUpperCase()===bin));
 must(candidates.length,'Product, lot or source bin does not match this order.');
 const tracked=s.operations.tracking[item.id]==='Serial';must(tracked?values.length===n&&new Set(values).size===n:values.length===0,tracked?'Scan one unique serial number for each unit.':'Serial numbers are not used for this product.');
 const allUsed=Object.values(used).flatMap(x=>x.serials||[]);must(values.every(v=>!allUsed.includes(v)),'This serial number was already scanned.');
 must(candidates.reduce((t,{a,i})=>t+a.qty-(used[i]?.qty||0),0)>=n,'Scanned quantity exceeds the remaining allocation.');
 let left=n,remaining=[...values];for(const {a,i}of candidates){const free=a.qty-(used[i]?.qty||0),selected=tracked?remaining.filter(v=>a.serials?.includes(v)):[];let take=tracked?selected.length:Math.min(left,free);must(!tracked||take<=free,'Scanned serials exceed the remaining allocation.');if(!take)continue;must(!tracked||selected.every(v=>a.serials.includes(v)),'Serial does not belong to this order.');counts[i]||={qty:0,serials:[]};counts[i].qty+=take;counts[i].serials.push(...selected);remaining=remaining.filter(v=>!selected.includes(v));left-=take;if(!left)break;}
 must(left===0&&remaining.length===0,'Serial does not belong to this order.');
}
const complete=(p,counts)=>p.allocations.length>0&&p.allocations.every((a,i)=>counts[i]?.qty===a.qty);
export function beforeExecution(s,command,p,ctx){
 if(command==='finishPick'){const b=s.operations?.batches.find(b=>b.pickIds.includes(p.id)),g=b&&executionGroup(s,b.id);if(g&&!g.abandoned)must(ctx.rootCommand==='warehouse:finishGroup','Finish this scan-controlled group from Grouped picking.');}
 if(['saveCarton','deleteCarton','packShipment','saveShipmentDetails','shipShipment'].includes(command)){
  const control=executionPack(s,p.id);if(p.mobile===true)must(control,'Open and scan this shipment in mobile Packing first.');
  if(!control)return;
  if(command==='shipShipment'){const sh=find(s.shipments,p.id),codes=String(p.cartonCodes||'').split(/[\n,]/).map(code).filter(Boolean);must(p.mobile===true&&p.reviewed===true&&sh.status==='Packed'&&control.sealed,'Review the scanned cartons in mobile Shipping before dispatch.');must(code(p.shipmentCode)===sh.number.toUpperCase(),'Shipment barcode does not match.');must(new Set(codes).size===codes.length&&codes.length===control.cartons.length&&control.cartons.every(c=>codes.includes(c.code)),'Scan every carton exactly once before dispatch.');}
  else must(ctx.rootCommand==='warehouse:sealPack','Use mobile Packing for this scan-controlled shipment.');
 }
}
export function afterExecution(s,command,p,current){
 if(command==='voidPick'){const b=s.operations?.batches.find(b=>b.pickIds.includes(p.id)),g=b&&executionGroup(s,b.id);if(g){g.abandoned=true;g.reason='Pick reversed; grouped scans are historical only.';}}
 if(command==='voidShipment'){const c=executionPack(s,p.id);if(c){c.reversed=true;c.sealed=false;}}
 if(command==='voidPick'){const old=current.picks.find(x=>x.id===p.id),c=old?.shipmentId&&executionPack(s,old.shipmentId);if(c){c.reversed=true;c.sealed=false;}}
 if(command==='dissolveBatch'&&executionGroup(s,p.id)){s.warehouseExecution.groupArchives||=[];s.warehouseExecution.groupArchives.push({id:p.id,...structuredClone(executionGroup(s,p.id))});delete s.warehouseExecution.groups[p.id];}
}
export function executionCommand(s,command,p,ctx){
 if(!command.startsWith('warehouse:'))return null;setup(s);const run=(cmd,payload)=>{const r=ctx.dispatch(s,cmd,payload,{now:ctx.time});Object.assign(s,r.state);return r.resultId;};
 let id=p.id;
 if(command==='warehouse:createGroup'){id=run('combinePicks',{pickIds:p.pickIds});command='warehouse:prepareGroup';}
 if(command==='warehouse:prepareGroup'){
  const b=find(s.operations.batches,id);must(!executionGroup(s,id),'This group already has scan controls.');const picks=b.pickIds.map(pid=>find(s.picks,pid));must(picks.every(pk=>pk.status==='Entered'&&!pickMeta(s,pk.id).hold),'Group before committing or finishing picks.');must(new Set(picks.map(pk=>scopeKey(s,pk))).size===1,'Grouped picks must share one warehouse and inventory owner.');
  setup(s).groups[id]={createdAt:ctx.time,actor:ctx.actor||'',slots:picks.map((pk,i)=>({pickId:pk.id,tote:`${b.name}-T${i+1}`,counts:{}})),completed:false,abandoned:false};return event('Scan group prepared',b.name,id);
 }
 if(['warehouse:commitGroup','warehouse:scanGroup','warehouse:finishGroup'].includes(command)){
  const b=find(s.operations.batches,id),g=executionGroup(s,id);must(g&&!g.abandoned&&!g.completed,'Choose an active scan group.');
  if(command==='warehouse:commitGroup'){must(b.pickIds.every(pid=>find(s.picks,pid).status==='Entered'),'Commit an unreserved group only once.');run('commitBatch',{id});return event('Scan group reserved',b.name,id);}
  must(b.pickIds.every(pid=>find(s.picks,pid).status==='Committed'&&!pickMeta(s,pid).hold),'All grouped picks must be reserved and unheld.');
  if(command==='warehouse:scanGroup'){request(s,p);const slot=g.slots.find(x=>x.tote===code(p.toteCode));must(slot,'Tote barcode does not belong to this group.');scan(s,p,find(s.picks,slot.pickId),slot.counts,slot.counts,true);return event('Tote scan saved',slot.tote,id);}
  must(g.slots.every(slot=>complete(find(s.picks,slot.pickId),slot.counts)),'Scan every allocated unit into its order tote before finishing.');run('finishBatch',{id});executionGroup(s,id).completed=true;executionGroup(s,id).finishedAt=ctx.time;return event('Grouped picking finished',b.name,id);
 }
 if(command==='warehouse:openPack'){
  const sh=find(s.shipments,id);must(sh.status==='Entered'&&!executionPack(s,id),'Choose an unpacked shipment without active scan controls.');must(!shippingMeta(s,id).cartons.length,'Remove existing draft cartons on the desktop before starting scanned packing.');setup(s).packing[id]={createdAt:ctx.time,actor:ctx.actor||'',cartons:[],sealed:false,reversed:false};return event('Scanned packing opened',sh.number,id);
 }
 if(command==='warehouse:resetPack'){
  const sh=find(s.shipments,id),c=executionPack(s,id);must(sh.status==='Entered'&&c&&p.reviewed===true&&text(p.reason,240),'Reverse packing first, then review a reset reason.');const m=s.operations.shipping[id];m.scanArchives||=[];must(m.scanArchives.length<100,'Packing archive is full.');m.scanArchives.push({...structuredClone(c),resetAt:ctx.time,reason:text(p.reason,240)});m.cartons=[];delete s.warehouseExecution.packing[id];return event('Scanned packing reset',sh.number,id);
 }
 if(['warehouse:addCarton','warehouse:scanPack','warehouse:sealPack'].includes(command)){
  const sh=find(s.shipments,id),c=executionPack(s,id),pk=find(s.picks,sh.pickId);must(sh.status==='Entered'&&c&&!c.sealed&&!c.reversed,'Choose active unpacked mobile packing.');
  if(command==='warehouse:addCarton'){must(c.cartons.length<50,'Maximum 50 cartons.');c.cartons.push({code:`${sh.number}-C${c.cartons.length+1}`,name:text(p.name,60)||`Carton ${c.cartons.length+1}`,counts:{}});return event('Scan carton added',sh.number,id);}
  if(command==='warehouse:scanPack'){request(s,p);const carton=c.cartons.find(x=>x.code===code(p.cartonCode));must(carton,'Carton barcode does not belong to this shipment.');const used={};for(const box of c.cartons)for(const [i,r]of Object.entries(box.counts)){used[i]||={qty:0,serials:[]};used[i].qty+=r.qty;used[i].serials.push(...r.serials);}scan(s,p,pk,carton.counts,used);return event('Carton scan saved',carton.code,id);}
  const used={};for(const box of c.cartons)for(const [i,r]of Object.entries(box.counts)){used[i]||={qty:0};used[i].qty+=r.qty;}
  must(p.reviewed===true&&c.cartons.length>0&&c.cartons.every(x=>sum(x.counts)>0)&&complete(pk,used),'Review and scan every unit; each carton must contain stock.');must(text(p.carrier,240),'Enter a carrier or local delivery name.');
  run('saveShipmentDetails',{id,name:find(s.orders,sh.orderId).customer,...shippingMeta(s,id).address,carrier:text(p.carrier,240),tracking:text(p.tracking,240),service:text(p.service,240)});
  for(let index=0;index<c.cartons.length;index++){const box=executionPack(s,id).cartons[index],byItem={};for(const [key,r]of Object.entries(box.counts)){const a=pk.allocations[Number(key)];byItem[a.itemId]=(byItem[a.itemId]||0)+r.qty;}const cartonId=run('saveCarton',{id,name:box.name,lines:Object.entries(byItem).map(([itemId,qty])=>({itemId,qty})),tracking:box.code});executionPack(s,id).cartons[index].cartonId=cartonId;}
  executionPack(s,id).sealed=true;executionPack(s,id).sealedAt=ctx.time;run('packShipment',{id,carrier:text(p.carrier,240),tracking:text(p.tracking,240)});return event('Scanned packing sealed',sh.number,id);
 }
 throw Error('Unknown warehouse execution action.');
}
export function validateExecution(s){
 const w=s.warehouseExecution;if(!w)return true;must(w.version===1&&w.groups&&w.packing&&Array.isArray(w.requests)&&w.requests.length<=100000&&new Set(w.requests).size===w.requests.length&&w.requests.every(x=>/^[a-zA-Z0-9-]{16,80}$/.test(x)),'Invalid scan request history.');
 const check=(pk,counts)=>{must(counts&&typeof counts==='object'&&!Array.isArray(counts),'Invalid scan counts.');for(const [i,r]of Object.entries(counts)){const a=pk.allocations[Number(i)];must(/^\d+$/.test(i)&&a&&Number.isSafeInteger(r.qty)&&r.qty>0&&r.qty<=a.qty&&Array.isArray(r.serials)&&new Set(r.serials).size===r.serials.length,'Invalid allocated scan count.');must(s.operations.tracking[a.itemId]==='Serial'?r.serials.length===r.qty&&r.serials.every(v=>a.serials.includes(v)):r.serials.length===0,'Scanned serials do not match allocated stock.');}};
 for(const [id,g]of Object.entries(w.groups)){const b=find(s.operations.batches,id);must(g.slots.length===b.pickIds.length&&new Set(g.slots.map(x=>x.pickId)).size===g.slots.length&&new Set(g.slots.map(x=>x.tote)).size===g.slots.length&&g.slots.every((x,i)=>x.pickId===b.pickIds[i]&&x.tote===`${b.name}-T${i+1}`),'Invalid order tote mapping.');if(!g.abandoned){must(new Set(b.pickIds.map(pid=>scopeKey(s,find(s.picks,pid)))).size===1,'Group warehouse scope changed.');for(const slot of g.slots){const pk=find(s.picks,slot.pickId);check(pk,slot.counts);if(g.completed)must(complete(pk,slot.counts),'Completed group is missing scans.');}}}
 for(const [id,c]of Object.entries(w.packing)){const sh=find(s.shipments,id),pk=find(s.picks,sh.pickId);must(Array.isArray(c.cartons)&&c.cartons.length<=50&&new Set(c.cartons.map(x=>x.code)).size===c.cartons.length,'Invalid scan cartons.');const used={};for(const [index,box]of c.cartons.entries()){must(box.code===`${sh.number}-C${index+1}`&&text(box.name,60),'Invalid carton barcode.');if(c.reversed)continue;check(pk,box.counts);for(const [i,r]of Object.entries(box.counts)){used[i]||={qty:0,serials:[]};used[i].qty+=r.qty;used[i].serials.push(...r.serials);}}if(!c.reversed){check(pk,used);if(c.sealed){must(c.cartons.length>0&&complete(pk,used),'Sealed packing is incomplete.');const actual=shippingMeta(s,id).cartons;must(actual.length===c.cartons.length&&c.cartons.every(box=>{const a=actual.find(a=>a.id===box.cartonId),lines={};for(const [i,r]of Object.entries(box.counts)){const item=pk.allocations[Number(i)].itemId;lines[item]=(lines[item]||0)+r.qty;}return a&&a.tracking===box.code&&a.lines.length===Object.keys(lines).length&&a.lines.every(l=>l.qty===lines[l.itemId]);}),'Sealed carton contents changed.');}if(['Packed','Shipped'].includes(sh.status))must(c.sealed,'Scan-controlled shipment must be sealed before dispatch.');}}
 return true;
}

