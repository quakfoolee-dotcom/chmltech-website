import {pickLines,deliveryLines} from './fulfillment.mjs?demo=5d9e5d1ce6c83eb1';
import {businessDay} from './company-date.mjs?demo=5d9e5d1ce6c83eb1';
import {isFIFO,fifoValue,nextFIFOCost} from './fifo.mjs?demo=5d9e5d1ce6c83eb1';
// Local warehouse extensions. Optional metadata keeps v1 backups readable.
import {charLength,cutText,validUnicode} from './unicode.mjs?demo=5d9e5d1ce6c83eb1';
import {purchaseLines,validatePurchasing,purchasingCommand} from './purchasing.mjs?demo=5d9e5d1ce6c83eb1';
import {loadChineseDemo} from './chinese-demo.mjs?demo=5d9e5d1ce6c83eb1';
import {locationScope,orderScope} from './business.mjs?demo=5d9e5d1ce6c83eb1';
const must=(ok,message)=>{if(!ok)throw Error(message);};
const find=(rows,id)=>{const row=rows.find(r=>r.id===id);must(row,'Record not found.');return row;};
const text=(v,max=240)=>cutText(String(v??'').trim(),max);
const required=(v,label,max=240)=>{const out=text(v,max);must(out,`${label} is required.`);return out;};
const number=(v,label,max=10000000)=>{const x=Number(v);must(Number.isFinite(x)&&x>=0&&x<=max,`${label} must be between 0 and ${max}.`);return x;};
const qty=(v,zero=false)=>{const x=number(v,'Quantity');must(Number.isSafeInteger(x)&&(zero||x>0),'Quantity must be a positive whole number.');return x;};
const round=v=>Math.round((v+Number.EPSILON)*10000)/10000;
const validDate=v=>v===''||(/^\d{4}-\d{2}-\d{2}$/.test(v)&&new Date(v+'T00:00:00Z').toISOString().slice(0,10)===v);
const safeDate=v=>{const x=text(v,10);must(validDate(x),'Use a valid date.');return x;};
const key=(itemId,lot)=>`${itemId}|${lot}`;
const baseOps=()=>({version:1,counters:{purchase:0,batch:0,carton:0},costs:{},tracking:{},lots:{},serials:{},picks:{},custom:{},shipping:{},purchases:[],batches:[],families:{}});
export const ops=s=>s.operations||baseOps();
export const setupOps=s=>s.operations||(s.operations=baseOps());
export const pickMeta=(s,id)=>ops(s).picks[id]||{started:false,hold:false,reason:'',priority:3,scheduled:'',slot:'',batchId:null};
export const pickStatus=(s,p)=>pickMeta(s,p.id).hold?'Hold':p.status==='Entered'&&pickMeta(s,p.id).started?'Started':p.status;
export const shippingMeta=(s,id)=>ops(s).shipping[id]||{address:{},service:'',cartons:[],costSnapshot:{}};
export const shipmentLines=(s,id)=>deliveryLines(s,find(s.shipments,id));
export const lotExpiry=(s,row)=>ops(s).lots[key(row.itemId,row.lot)]?.expiresOn||'';
export const expired=(s,row,now=new Date().toISOString())=>{const exp=lotExpiry(s,row);return !!exp&&exp<businessDay(s,now);};
export const stockCandidates=(s,itemId,now)=>s.stock.filter(r=>r.itemId===itemId&&find(s.locations,r.locationId).pickable&&!expired(s,r,now)).sort((a,b)=>(lotExpiry(s,a)||'9999').localeCompare(lotExpiry(s,b)||'9999'));
export const physical=(s,id)=>s.stock.filter(r=>r.itemId===id).reduce((a,r)=>a+r.qty,0);
const ownedPhysical=(s,id)=>s.stock.filter(r=>r.itemId===id&&locationScope(s,r.locationId).ownerId==='owner-self').reduce((a,r)=>a+r.qty,0);
export const costSummary=(s,id)=>{const average=ops(s).costs[id]??null;return {average,total:isFIFO(s,id)?fifoValue(s,id)/100:average===null?null:round(average*ownedPhysical(s,id)),method:isFIFO(s,id)?'FIFO':'Average',next:isFIFO(s,id)?nextFIFOCost(s,id):average};};
export const supplyTotals=(s,id)=>ops(s).purchases.filter(p=>p.status==='Open').reduce((r,p)=>{r[p.kind==='Drop ship'?'dropShip':'onOrder']+=purchaseLines(p).filter(l=>l.itemId===id).reduce((n,l)=>n+l.qty-l.received,0);return r;},{onOrder:0,dropShip:0});
export const customFields=(s,scope,id)=>ops(s).custom[`${scope}/${id}`]||[];
export const familyOrders=(s,id)=>{const f=Object.values(ops(s).families).find(f=>f.orderIds.includes(id));return f?f.orderIds.map(id=>find(s.orders,id)):[];};
const serialMode=(s,id)=>ops(s).tracking[id]==='Serial';
const listSerials=v=>Array.isArray(v)?v.map(x=>text(x,100)).filter(Boolean):String(v??'').split(/[\n,]/).map(x=>text(x,100)).filter(Boolean);
const reservedSerials=(s,stockId)=>s.picks.flatMap(p=>p.status==='Committed'?p.allocations.filter(a=>a.sourceStockId===stockId).flatMap(a=>a.serials||[]):p.status==='Finished'&&find(s.shipments,p.shipmentId).status!=='Shipped'?p.allocations.filter(a=>a.stagingStockId===stockId).flatMap(a=>a.serials||[]):[]);
const chooseSerials=(s,r,count,provided)=>{
  if(!serialMode(s,r.itemId))return [];
  const all=ops(s).serials[r.id]||[],reserved=new Set(reservedSerials(s,r.id));
  const selected=provided?listSerials(provided):all.filter(x=>!reserved.has(x)).slice(0,count);
  must(selected.length===count&&new Set(selected).size===count&&selected.every(x=>all.includes(x)&&!reserved.has(x)),'Choose exactly the free serial numbers for this quantity.');return selected;
};
const removeSerials=(s,r,serials)=>{const f=setupOps(s);f.serials[r.id]=(f.serials[r.id]||[]).filter(x=>!serials.includes(x));};
const addSerials=(s,r,serials)=>{const f=setupOps(s);f.serials[r.id]=[...(f.serials[r.id]||[]),...serials];};
const metaPick=(s,id)=>{const f=setupOps(s);return f.picks[id]||(f.picks[id]={...pickMeta(s,id)});};
const metaShip=(s,id)=>{const f=setupOps(s),m=f.shipping[id]||(f.shipping[id]={...shippingMeta(s,id),address:{},cartons:[],costSnapshot:{}});m.orderLines||=structuredClone(deliveryLines(s,find(s.shipments,id)));return m;};
const event=(type,reference,message,resultId=null)=>({type,reference,message,resultId});

export function validateOperations(s){
  if(!s.operations)return true;
  const f=s.operations;must(f.version===1,'Unsupported warehouse extensions.');
  const mapNames=['costs','tracking','lots','serials','picks','custom','shipping','families'];
  for(const name of mapNames)must(f[name]&&typeof f[name]==='object'&&!Array.isArray(f[name]),`Invalid ${name} metadata.`);
  must(f.counters&&['purchase','batch','carton'].every(k=>Number.isSafeInteger(f.counters[k])&&f.counters[k]>=0),'Invalid extension counters.');
  must(Array.isArray(f.purchases)&&f.purchases.length<=10000&&Array.isArray(f.batches)&&f.batches.length<=10000,'Invalid warehouse work lists.');
  const isText=(v,max=240)=>typeof v==='string'&&charLength(v)<=max&&validUnicode(v);
  const nonneg=v=>typeof v==='number'&&Number.isFinite(v)&&v>=0&&v<=10000000;
  for(const [id,value] of Object.entries(f.costs)){find(s.items,id);must(nonneg(value),'Invalid average cost.');}
  for(const [id,mode] of Object.entries(f.tracking)){find(s.items,id);must(['Lot','Serial'].includes(mode),'Invalid tracking mode.');}
  for(const [k,l] of Object.entries(f.lots)){must(s.stock.some(r=>key(r.itemId,r.lot)===k),'Unknown lot metadata.');must(isText(l.expiresOn,10)&&validDate(l.expiresOn),'Invalid expiration date.');}
  const serialSet=new Set();
  for(const [id,values] of Object.entries(f.serials)){
    const r=find(s.stock,id);must(Array.isArray(values)&&values.every(x=>isText(x,100)&&x.trim()),'Invalid serial list.');
    must(values.length===0||values.length===r.qty,'Serial count must match the stock quantity.');
    for(const serial of values){const k=key(r.itemId,serial);must(!serialSet.has(k),'Duplicate serial number in stock.');serialSet.add(k);}
  }
  for(const r of s.stock)if(serialMode(s,r.itemId))must((f.serials[r.id]||[]).length===r.qty,'Serial count must match stock.');
  const committedSerials=new Set();
  for(const p of s.picks)if(p.status!=='Entered')for(const a of p.allocations){
    if(!serialMode(s,a.itemId))continue;
    must(Array.isArray(a.serials)&&a.serials.length===a.qty&&new Set(a.serials).size===a.qty,'Pick serials do not match quantity.');
    const active=p.status==='Committed'||find(s.shipments,p.shipmentId).status!=='Shipped';
    if(active)for(const serial of a.serials){const k=key(a.itemId,serial);must(!committedSerials.has(k),'Serial reserved by more than one pick.');committedSerials.add(k);must((f.serials[p.status==='Committed'?a.sourceStockId:a.stagingStockId]||[]).includes(serial),'Reserved serial is missing from stock.');}
  }
  for(const [id,m] of Object.entries(f.picks)){find(s.picks,id);must(typeof m.started==='boolean'&&typeof m.hold==='boolean'&&isText(m.reason)&&Number.isInteger(m.priority)&&m.priority>=1&&m.priority<=5&&isText(m.scheduled,10)&&validDate(m.scheduled)&&isText(m.slot,40),'Invalid pick instructions.');if(m.hold)must(m.reason.trim(),'A hold needs a reason.');if(m.batchId)must(f.batches.some(b=>b.id===m.batchId&&b.pickIds.includes(id)),'Invalid batch link.');}
  for(const [k,fields] of Object.entries(f.custom)){
    const [scope,id]=k.split('/'),collection={inventory:'items',orders:'orders',picking:'picks',shipping:'shipments'}[scope];must(collection,'Invalid custom field target.');find(s[collection],id);
    must(Array.isArray(fields)&&fields.length<=30&&fields.every(x=>isText(x.name,60)&&x.name.trim()&&isText(x.value,500)),'Invalid custom fields.');must(new Set(fields.map(x=>x.name.toLowerCase())).size===fields.length,'Custom field names must be unique.');
  }
  const cartonIds=new Set();
  for(const [id,m] of Object.entries(f.shipping)){
    const sh=find(s.shipments,id),order=find(s.orders,sh.orderId),o={...order,lines:m.orderLines||order.lines};must(m.address&&typeof m.address==='object'&&Object.values(m.address).every(x=>isText(x,240))&&isText(m.service)&&Array.isArray(m.cartons)&&m.cartons.length<=50,'Invalid shipment details.');
    must(Array.isArray(o.lines)&&o.lines.length>0&&o.lines.every(l=>s.items.some(i=>i.id===l.itemId)&&Number.isSafeInteger(l.qty)&&l.qty>0)&&new Set(o.lines.map(l=>l.itemId)).size===o.lines.length,'Invalid shipment line snapshot.');
    if(sh.status!=='Cancelled')must(o.lines.length===deliveryLines(s,sh).length&&o.lines.every(l=>deliveryLines(s,sh).some(x=>x.itemId===l.itemId&&x.qty===l.qty)),'Active shipment differs from its order.');
    const sums={};
    for(const c of m.cartons){must(/^ct-\d+$/.test(c.id)&&Number(c.id.slice(3))<=f.counters.carton&&!cartonIds.has(c.id),'Invalid carton identifier.');cartonIds.add(c.id);must(isText(c.name,60)&&c.name.trim()&&isText(c.tracking)&&['cm','in'].includes(c.unit)&&['kg','lb'].includes(c.weightUnit)&&['length','width','height','weight','cost','declaredValue'].every(k=>nonneg(c[k]))&&Array.isArray(c.lines)&&c.lines.length>0,'Invalid carton.');must(new Set(c.lines.map(l=>l.itemId)).size===c.lines.length,'Duplicate carton item.');for(const l of c.lines){must(o.lines.some(x=>x.itemId===l.itemId)&&Number.isSafeInteger(l.qty)&&l.qty>0,'Invalid carton contents.');sums[l.itemId]=(sums[l.itemId]||0)+l.qty;}}
    must(o.lines.every(l=>(sums[l.itemId]||0)<=l.qty),'Cartons exceed the order quantity.');
    if(['Packed','Shipped'].includes(sh.status)&&m.cartons.length)must(o.lines.every(l=>sums[l.itemId]===l.qty),'Packed cartons must cover every order line.');
    must(m.costSnapshot&&Object.entries(m.costSnapshot).every(([id,v])=>o.lines.some(l=>l.itemId===id)&&(v===null||nonneg(v))),'Invalid shipment cost snapshot.');
  }
  const purchaseIds=new Set();
  for(const p of f.purchases){must(/^po-\d+$/.test(p.id)&&Number(p.id.slice(3))<=f.counters.purchase&&!purchaseIds.has(p.id),'Invalid purchase identifier.');purchaseIds.add(p.id);must(isText(p.number,40)&&p.number===`PO-${Number(p.id.slice(3))}`&&isText(p.supplier,100)&&p.supplier.trim()&&['Warehouse','Drop ship'].includes(p.kind)&&isText(p.customer,100)&&isText(p.due,10)&&validDate(p.due)&&['Open','Closed','Cancelled','Draft','Pending approval','Approved','Rejected'].includes(p.status),'Invalid purchase order.');if(p.lines===undefined){find(s.items,p.itemId);must(Number.isSafeInteger(p.qty)&&p.qty>0&&p.qty<=10000000&&Number.isSafeInteger(p.received)&&p.received>=0&&p.received<=p.qty&&nonneg(p.unitCost),'Invalid purchase order.');must(p.status!=='Closed'||p.received===p.qty,'Closed purchase is incomplete.');}}
  validatePurchasing(s);
  const batchIds=new Set();
  for(const b of f.batches){must(/^batch-\d+$/.test(b.id)&&Number(b.id.slice(6))<=f.counters.batch&&!batchIds.has(b.id),'Invalid batch identifier.');batchIds.add(b.id);must(isText(b.name,100)&&Array.isArray(b.pickIds)&&b.pickIds.length>=2&&b.pickIds.length<=20&&new Set(b.pickIds).size===b.pickIds.length,'Invalid pick batch.');for(const id of b.pickIds){find(s.picks,id);must(f.picks[id]?.batchId===b.id,'Batch and pick links disagree.');}}
  const familyMembers=new Set();
  for(const [root,family] of Object.entries(f.families)){
    find(s.orders,root);must(Array.isArray(family.orderIds)&&family.orderIds.includes(root)&&family.orderIds.length<=100&&new Set(family.orderIds).size===family.orderIds.length&&Array.isArray(family.originalLines),'Invalid split-order family.');
    const sums={};for(const id of family.orderIds){must(!familyMembers.has(id),'Order is in multiple families.');familyMembers.add(id);for(const l of find(s.orders,id).lines)sums[l.itemId]=(sums[l.itemId]||0)+l.qty;}
    must(new Set(family.originalLines.map(l=>l.itemId)).size===family.originalLines.length&&family.originalLines.length===Object.keys(sums).length&&family.originalLines.every(l=>Number.isSafeInteger(l.qty)&&l.qty>0&&sums[l.itemId]===l.qty),'Split orders do not conserve the original demand.');
  }
  return true;
}

export function beforeOperation(s,command,payload,ctx){
  const f=setupOps(s);
  if(['commitPick','finishPick'].includes(command)){
    const p=find(s.picks,payload.id);must(!pickMeta(s,p.id).hold,'Release the pick hold before continuing.');
    if(command==='finishPick')must(p.allocations.every(a=>!expired(s,find(s.stock,a.sourceStockId),ctx.time)),'A reserved lot has expired. Void the pick and choose valid stock.');
  }
  if(command==='shipShipment'){
    const sh=find(s.shipments,payload.id),p=find(s.picks,sh.pickId),m=metaShip(s,sh.id);
    must(!pickMeta(s,p.id).hold,'Release the pick hold before shipping.');
    must(p.allocations.every(a=>!expired(s,find(s.stock,a.stagingStockId),ctx.time)),'A staged lot has expired. Void and replace it before shipping.');
    for(const l of deliveryLines(s,sh))m.costSnapshot[l.itemId]=f.costs[l.itemId]??null;
    for(const a of p.allocations)if(serialMode(s,a.itemId))removeSerials(s,find(s.stock,a.stagingStockId),a.serials);
  }
  if(command==='voidShipment'){
    const sh=find(s.shipments,payload.id);
    if(sh.status==='Shipped'){
      const m=metaShip(s,sh.id);
      if(orderScope(s,find(s.orders,sh.orderId)).ownerId==='owner-self')for(const l of deliveryLines(s,sh)){const previous=ownedPhysical(s,l.itemId),old=f.costs[l.itemId],restored=m.costSnapshot[l.itemId];if(old!==undefined&&restored!==null&&restored!==undefined)f.costs[l.itemId]=round((previous*old+l.qty*restored)/(previous+l.qty));else delete f.costs[l.itemId];}
      for(const a of find(s.picks,sh.pickId).allocations)if(serialMode(s,a.itemId))addSerials(s,find(s.stock,a.stagingStockId),a.serials);
    }
  }
  if(command==='voidPick'){
    const p=find(s.picks,payload.id);
    if(p.shipmentId)metaShip(s,p.shipmentId);
    if(p.status==='Finished')for(const a of p.allocations)if(serialMode(s,a.itemId)){removeSerials(s,find(s.stock,a.stagingStockId),a.serials);addSerials(s,find(s.stock,a.sourceStockId),a.serials);}
  }
  if(command==='moveStock'){
    const r=find(s.stock,payload.stockId),serials=chooseSerials(s,r,qty(payload.qty),payload.serials);
    if(serials.length){removeSerials(s,r,serials);addSerials(s,ctx.stockAt(s,r.itemId,payload.locationId,r.lot),serials);}
  }
  if(command==='countStock'){
    const r=find(s.stock,payload.stockId);if(serialMode(s,r.itemId)){const values=listSerials(payload.serials);must(values.length===qty(payload.qty,true),'A serial-tracked cycle count needs the complete counted serial list.');must(reservedSerials(s,r.id).every(x=>values.includes(x)),'A reserved serial cannot be removed by a count.');f.serials[r.id]=values;}
  }
  if(command==='packShipment'){
    const sh=find(s.shipments,payload.id),m=metaShip(s,sh.id);
    if(!m.cartons.length)m.cartons.push({id:`ct-${++f.counters.carton}`,name:'Carton 1',tracking:text(payload.tracking),length:0,width:0,height:0,weight:0,unit:'cm',weightUnit:'kg',cost:0,declaredValue:0,lines:structuredClone(deliveryLines(s,sh))});
  }
}

export function afterOperation(s,current,command,payload,ctx){
  const f=setupOps(s);
  if(command==='receiveStock'){
    const id=payload.itemId,lot=text(payload.lot,100)||'UNTRACKED',r=s.stock.find(r=>r.itemId===id&&r.locationId===payload.locationId&&r.lot===lot);
    if(serialMode(s,id)){const serials=listSerials(payload.serials);must(serials.length===qty(payload.qty),'Enter one serial number per received unit.');addSerials(s,r,serials);}
    if(payload.expiresOn!==undefined){const expiry=safeDate(payload.expiresOn);const existing=f.lots[key(id,lot)];must(!existing||existing.expiresOn===expiry,'This lot already has a different expiry date. Edit Tracking to correct it.');f.lots[key(id,lot)]={expiresOn:expiry};}
    const before=ownedPhysical(current,id),old=ops(current).costs[id],incoming=payload.unitCost===undefined||payload.unitCost===''?old:number(payload.unitCost,'Unit cost');
    if(locationScope(s,r.locationId).ownerId==='owner-self'&&incoming!==undefined&&(old!==undefined||before===0))f.costs[id]=round((before*(old||0)+Number(payload.qty)*incoming)/(before+Number(payload.qty)));
  }
  if(command==='commitPick'){
    const p=find(s.picks,payload.id),used={};
    for(const a of p.allocations)if(serialMode(s,a.itemId)){
      const reserved=new Set(reservedSerials(current,a.sourceStockId));
      const candidates=(f.serials[a.sourceStockId]||[]).filter(x=>!reserved.has(x)&&!(used[a.sourceStockId]||[]).includes(x));
      a.serials=candidates.slice(0,a.qty);must(a.serials.length===a.qty,'Insufficient free serial numbers.');used[a.sourceStockId]=[...(used[a.sourceStockId]||[]),...a.serials];
    }
  }
  if(command==='finishPick')for(const a of find(s.picks,payload.id).allocations)if(serialMode(s,a.itemId)){removeSerials(s,find(s.stock,a.sourceStockId),a.serials);addSerials(s,find(s.stock,a.stagingStockId),a.serials);}
  if(command==='finishPick')metaShip(s,find(s.picks,payload.id).shipmentId);
  if(command==='voidPick')metaPick(s,payload.id).started=false;
}

export function extendedCommand(s,command,payload,ctx){
  const f=setupOps(s),{uid,stockAt,time}=ctx;
  if(command==='loadChineseDemo')return loadChineseDemo(s,ctx);
  const purchaseResult=purchasingCommand(s,command,payload,ctx);if(purchaseResult)return purchaseResult;
  switch(command){
    case 'setCost':{const i=find(s.items,payload.id);f.costs[i.id]=number(payload.unitCost,'Average unit cost');return event('Cost updated',i.sku,`Average cost set to ${f.costs[i.id]}. ${required(payload.reason,'Valuation reason')}`);}
    case 'scrapStock':{const r=find(s.stock,payload.stockId),q=qty(payload.qty);must(q<=r.qty-r.committed,'Only unreserved stock can be scrapped.');const reason=required(payload.reason,'Scrap reason');removeSerials(s,r,chooseSerials(s,r,q,payload.serials));r.qty-=q;return event('Stock scrapped',find(s.items,r.itemId).sku,`${q} removed from ${find(s.locations,r.locationId).code}. ${reason}`);}
    case 'setTracking':{
      const i=find(s.items,payload.itemId);must(['Lot','Serial'].includes(payload.mode),'Choose Lot or Serial tracking.');
      must(!s.picks.some(p=>p.status!=='Entered'&&p.allocations.some(a=>a.itemId===i.id))||payload.mode===(f.tracking[i.id]||'Lot'),'Tracking mode cannot change after this item has been picked.');
      if(payload.stockSerials){for(const r of s.stock.filter(r=>r.itemId===i.id)){must(r.committed===0,'Void reservations before editing serial tracking.');f.serials[r.id]=payload.mode==='Serial'?listSerials(payload.stockSerials[r.id]):[];}}
      if(payload.stockId){const r=find(s.stock,payload.stockId);must(r.itemId===i.id,'Wrong stock item.');must(r.committed===0,'Void the reservation before editing tracking.');f.serials[r.id]=payload.mode==='Serial'?listSerials(payload.serials):[];f.lots[key(i.id,r.lot)]={expiresOn:safeDate(payload.expiresOn)};}
      if(payload.mode==='Lot')for(const r of s.stock.filter(r=>r.itemId===i.id))f.serials[r.id]=[];
      f.tracking[i.id]=payload.mode;return event('Tracking updated',i.sku,`${payload.mode} tracking updated. Expired lots cannot supply new picks.`);
    }
    case 'saveCustom':{
      const collection={inventory:'items',orders:'orders',picking:'picks',shipping:'shipments'}[payload.scope];must(collection,'Invalid custom field target.');const r=find(s[collection],payload.id);
      must(Array.isArray(payload.fields),'Enter name/value fields.');f.custom[`${payload.scope}/${r.id}`]=payload.fields.map(x=>({name:required(x.name,'Field name',60),value:text(x.value,500)}));return event('Custom fields saved',r.sku||r.number,`${payload.fields.length} custom fields saved.`);
    }
    case 'setPickDetails':{const p=find(s.picks,payload.id),m=metaPick(s,p.id);m.priority=qty(payload.priority);must(m.priority<=5,'Priority is 1 through 5.');m.scheduled=safeDate(payload.scheduled);m.slot=text(payload.slot,40);return event('Pick scheduled',p.number,`Priority ${m.priority}; date ${m.scheduled||'unscheduled'}; slot ${m.slot||'none'}.`);}
    case 'startPick':{const p=find(s.picks,payload.id),m=metaPick(s,p.id);must(p.status==='Entered'&&find(s.orders,p.orderId).status==='Issued'&&!m.hold&&!m.started,'Only a ready pick can be started.');m.started=true;return event('Pick started',p.number,'Work started. Stock is assigned only when committed.');}
    case 'holdPick':{const p=find(s.picks,payload.id),m=metaPick(s,p.id);must(!p.shipmentId||!['Shipped','Cancelled'].includes(find(s.shipments,p.shipmentId).status),'A completed shipment cannot be held.');must(find(s.orders,p.orderId).status!=='Cancelled','Cancelled order cannot be held.');if(m.hold){m.hold=false;m.reason='';}else{m.hold=true;m.reason=required(payload.reason,'Hold reason');}return event(m.hold?'Pick held':'Pick released',p.number,m.hold?m.reason:'Hold released; previous stock reservations are unchanged.');}
    case 'combinePicks':{
      const ids=payload.pickIds;must(Array.isArray(ids)&&ids.length>=2&&ids.length<=20&&new Set(ids).size===ids.length,'Choose 2–20 different picks.');
      for(const id of ids){const p=find(s.picks,id);must(p.status==='Entered'&&find(s.orders,p.orderId).status==='Issued'&&!pickMeta(s,id).batchId&&!pickMeta(s,id).hold,'Only unheld, uncommitted picks outside another batch can be combined.');}
      const id=`batch-${++f.counters.batch}`,name=`WB-${f.counters.batch}`;f.batches.push({id,name,pickIds:ids});ids.forEach(pid=>metaPick(s,pid).batchId=id);return event('Pick batch created',name,`${ids.length} picks grouped; original orders retained.`,id);
    }
    case 'commitBatch':case 'finishBatch':{
      const b=find(f.batches,payload.id);let next=s;for(const id of b.pickIds)next=ctx.dispatch(next,command==='commitBatch'?'commitPick':'finishPick',{id},{now:time}).state;Object.assign(s,next);return event(command==='commitBatch'?'Batch committed':'Batch finished',b.name,`All ${b.pickIds.length} picks processed atomically.`);
    }
    case 'dissolveBatch':{const b=find(f.batches,payload.id);must(b.pickIds.every(id=>find(s.picks,id).status==='Entered'),'Void all picks before releasing a batch.');for(const id of b.pickIds)metaPick(s,id).batchId=null;f.batches=f.batches.filter(x=>x.id!==b.id);return event('Batch released',b.name,'Picks can now be worked or combined individually.');}
    case 'splitOrder':{must(!find(s.orders,payload.id).fulfillment,'Use delivery releases for a partially shipped order.');
      const o=find(s.orders,payload.id);must(['Draft','Issued'].includes(o.status),'Split before committing the pick.');if(o.pickId)must(!pickMeta(s,o.pickId).batchId,'Split before combining picks into a batch.');
      must(Array.isArray(payload.lines)&&new Set(payload.lines.map(l=>l.itemId)).size===payload.lines.length&&payload.lines.every(l=>o.lines.some(x=>x.itemId===l.itemId)),'Invalid split lines.');
      const chosen=new Map(payload.lines.map(l=>[l.itemId,qty(l.qty,true)])),now=[],later=[];for(const l of o.lines){const q=chosen.get(l.itemId)||0;must(q<=l.qty,'Split quantity exceeds the order.');if(q)now.push({itemId:l.itemId,qty:q});if(l.qty-q)later.push({itemId:l.itemId,qty:l.qty-q});}must(now.length&&later.length,'Keep some quantity on this order and some on the backorder.');
      let root=Object.keys(f.families).find(id=>f.families[id].orderIds.includes(o.id))||o.id;
      f.families[root]||={orderIds:[o.id],originalLines:structuredClone(o.lines)};
      for(const sh of s.shipments.filter(sh=>sh.orderId===o.id))metaShip(s,sh.id);
      const id=uid(s,'order'),back={...structuredClone(o),id,number:`SO-${s.counters.order}`,createdAt:time,reference:`Backorder of ${o.number}`,pickId:null,lines:later};
      if(['Issued','Part shipped'].includes(o.status)){const pid=uid(s,'pick');back.pickId=pid;s.picks.push({id:pid,number:`PK-${s.counters.pick}`,orderId:id,status:'Entered',allocations:[],shipmentId:null});}
      s.orders.push(back);o.lines=now;f.families[root].orderIds.push(id);return event('Order split',o.number,`Remaining quantities moved to ${back.number}. Original demand is retained across linked orders.`,id);
    }
    case 'saveShipmentDetails':{
      const sh=find(s.shipments,payload.id);must(['Entered','Packed'].includes(sh.status),'Void the shipment before editing its details.');const m=metaShip(s,sh.id);m.address=Object.fromEntries(['name','line1','line2','city','region','postal','country'].map(k=>[k,text(payload[k])]));m.service=text(payload.service);sh.carrier=text(payload.carrier);sh.tracking=text(payload.tracking);return event('Shipment details saved',sh.number,'Address, carrier and service updated locally.');
    }
    case 'saveCarton':{
      const sh=find(s.shipments,payload.id);must(sh.status==='Entered','Void packing before changing cartons.');const m=metaShip(s,sh.id);must(!payload.cartonId||m.cartons.some(c=>c.id===payload.cartonId),'Carton not found.');
      must(Array.isArray(payload.lines),'Enter carton contents.');const c={id:payload.cartonId||`ct-${++f.counters.carton}`,name:required(payload.name,'Carton name',60),tracking:text(payload.tracking),unit:payload.unit||'cm',weightUnit:payload.weightUnit||'kg',lines:payload.lines.map(l=>({itemId:l.itemId,qty:qty(l.qty,true)})).filter(l=>l.qty>0)};for(const k of ['length','width','height','weight','cost','declaredValue'])c[k]=number(payload[k]||0,k);m.cartons=m.cartons.filter(x=>x.id!==c.id);m.cartons.push(c);return event('Carton saved',sh.number,`${c.name} contents and dimensions saved.`,c.id);
    }
    case 'deleteCarton':{const sh=find(s.shipments,payload.id);must(sh.status==='Entered','Void packing before removing cartons.');const m=metaShip(s,sh.id);find(m.cartons,payload.cartonId);m.cartons=m.cartons.filter(c=>c.id!==payload.cartonId);return event('Carton removed',sh.number,'Carton removed. Inventory is unchanged.');}
    case 'createPurchase':{
      const item=find(s.items,payload.itemId),id=`po-${++f.counters.purchase}`,q=qty(payload.qty),kind=payload.kind||'Warehouse';must(['Warehouse','Drop ship'].includes(kind),'Invalid purchase type.');const customer=kind==='Drop ship'?required(payload.customer,'Delivery customer',100):'';
      f.purchases.push({id,number:`PO-${f.counters.purchase}`,itemId:item.id,supplier:required(payload.supplier,'Supplier',100),kind,customer,qty:q,received:0,unitCost:number(payload.unitCost||0,'Unit cost'),due:safeDate(payload.due),status:'Open'});return event('Purchase created',`PO-${f.counters.purchase}`,`${q} ${item.uom} ordered from supplier.`,id);
    }
    default:return null;
  }
}

