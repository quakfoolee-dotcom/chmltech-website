import {rangeTransferFees} from './fifo-fees.mjs';
import {deliveryLines,returnShipment} from './fulfillment.mjs';
// Independent FIFO accounting. Physical pick-lot order remains separate.
// Each cost origin owns unit-index ranges, so partial withdrawals and later
// charges conserve integer cents instead of multiplying a rounded unit cost.
import {business,locationScope} from './business.mjs';
import {prepareFIFOSupplierReturn} from './fifo-supplier.mjs';
import {validUnicode,charLength} from './unicode.mjs';
const must=(v,m)=>{if(!v)throw Error(m);};
const cents=n=>Math.round((n+Number.EPSILON)*100);
const setup=s=>s.costLayers||(s.costLayers={version:1,sequence:0,policies:{},origins:[],layers:[],movements:[],history:null});
const uid=(c,p)=>p+'-'+(++c.sequence);
export const isFIFO=(s,id)=>s.costLayers?.policies[id]?.method==='FIFO';
export const nextFIFOCost=(s,id)=>{const layer=ordered(s,id)[0];return layer?rangeCost(originFor(s,layer.originId),layer.start,1)/100:null;};
export const layerWarehouse=(s,l)=>l.warehouseId||s.costLayers.policies[l.itemId].warehouseId;
export const fifoValue=(s,id,warehouseId='')=>s.costLayers?.layers.filter(l=>l.itemId===id&&(!warehouseId||layerWarehouse(s,l)===warehouseId)).reduce((n,l)=>n+rangeCost(s.costLayers.origins.find(o=>o.id===l.originId),l.start,l.qty),0)||0;
export const rangeCost=(origin,start,qty,total=origin.totalCost,feeOrdinal=Infinity)=>Number(BigInt(total)*BigInt(start+qty)/BigInt(origin.qty)-BigInt(total)*BigInt(start)/BigInt(origin.qty))+rangeTransferFees(origin,start,qty,feeOrdinal);
export function allocatedFIFORowValue(s,row){const rows=s.stock.filter(r=>r.itemId===row.itemId&&r.qty>0&&locationScope(s,r.locationId).ownerId==='owner-self'&&locationScope(s,r.locationId).warehouseId===locationScope(s,row.locationId).warehouseId),qty=rows.reduce((n,r)=>n+r.qty,0),index=rows.findIndex(r=>r.id===row.id),start=rows.slice(0,index).reduce((n,r)=>n+r.qty,0);return qty&&index>=0?rangeCost({qty,totalCost:fifoValue(s,row.itemId,locationScope(s,row.locationId).warehouseId)},start,row.qty):0;}
const physical=(s,id)=>s.stock.filter(r=>r.itemId===id&&locationScope(s,r.locationId).ownerId==='owner-self').reduce((n,r)=>n+r.qty,0);
const ordered=(s,id,returnId='',warehouseId='',transitId='')=>s.costLayers.layers.filter(l=>l.itemId===id&&l.qty>0&&(!returnId||l.returnId===returnId)&&(!warehouseId||layerWarehouse(s,l)===warehouseId)&&(l.transitId||'')===transitId).sort((a,b)=>Date.parse(a.createdAt)-Date.parse(b.createdAt)||a.ordinal-b.ordinal);
const originFor=(s,id)=>s.costLayers.origins.find(o=>o.id===id);
const label=v=>{const t=String(v||'').trim();must(t&&validUnicode(t)&&charLength(t)<=120,'Enter a valid Chinese or English label (up to 120 characters).');return t;};
function updateDisplayCost(s,id){const q=physical(s,id);if(q)s.operations.costs[id]=Number((fifoValue(s,id)/100/q).toFixed(4));}
function subtractRanges(slices,removed){
 let result=slices.map(x=>({...x}));for(const r of removed){result=result.flatMap(x=>{if(x.originId!==r.originId||r.start>=x.start+x.qty||r.start+r.qty<=x.start)return [x];const rows=[];if(r.start>x.start)rows.push({...x,qty:r.start-x.start});if(r.start+r.qty<x.start+x.qty)rows.push({...x,start:r.start+r.qty,qty:x.start+x.qty-r.start-r.qty});return rows;});}return result;
}
export function fifoOpenShipmentSlices(s,m){const reversed=s.costLayers.movements.some(t=>t.kind==='Void'&&t.reverses===m.id);if(reversed)return [];return subtractRanges(m.slices,s.costLayers.movements.filter(t=>t.kind==='Return'&&t.shipmentMovement===m.id).flatMap(t=>t.slices));}
function previewWithdrawal(s,id,qty,returnId='',warehouseId='',transitId=''){
 let left=qty;const slices=[];for(const l of ordered(s,id,returnId,warehouseId,transitId)){const q=Math.min(left,l.qty);if(q){slices.push({layerId:l.id,originId:l.originId,start:l.start,qty:q,value:rangeCost(originFor(s,l.originId),l.start,q),warehouseId:layerWarehouse(s,l),createdAt:l.createdAt,transitId:l.transitId||''});left-=q;}if(!left)break;}must(left===0,'FIFO cost layers do not cover the requested quantity.');return slices;
}
export const previewFIFOWithdrawal=(s,id,qty,warehouseId)=>previewWithdrawal(s,id,qty,'',warehouseId);
function movement(s,ctx,id,kind,slices,extra={}){
 const c=setup(s),record={id:uid(c,'fifo-move'),ordinal:c.sequence,itemId:id,kind,command:ctx.rootCommand||ctx.command,sourceId:ctx.rootPayload?.id||ctx.rootPayload?.purchaseId||ctx.rootPayload?.stockId||'',time:ctx.time,slices,value:slices.reduce((n,x)=>n+x.value,0),...extra};c.movements.push(record);return record;
}
function withdraw(s,ctx,id,qty,kind,returnId='',warehouseId=''){
 const slices=previewWithdrawal(s,id,qty,returnId,warehouseId);for(const x of slices){const l=s.costLayers.layers.find(l=>l.id===x.layerId);l.start+=x.qty;l.qty-=x.qty;}return movement(s,ctx,id,kind,slices);
}
function newLayer(s,ctx,id,origin,start,qty,returnId='',meta={}){
 const c=setup(s),layer={id:uid(c,'fifo-layer'),ordinal:c.sequence,itemId:id,originId:origin.id,start,qty,createdAt:ctx.time,returnId,...meta};c.layers.push(layer);return layer;
}
export function consumeFIFOProduction(s,ctx,itemId,qty,warehouseId,sourceId){const m=withdraw(s,ctx,itemId,qty,'Production','',warehouseId);m.sourceId=sourceId;return m;}
export function receiveFIFOProduction(s,ctx,itemId,qty,value,warehouseId,sourceId,receiptId){
 const c=setup(s),origin={id:uid(c,'fifo-origin'),itemId,qty,baseCost:value,totalCost:value,time:ctx.time,adjustments:[],purchaseId:'',receiptId:'',poolId:'',productionReceiptId:receiptId};c.origins.push(origin);const l=newLayer(s,ctx,itemId,origin,0,qty,'',{warehouseId});return movement(s,ctx,itemId,'Receipt',[{layerId:l.id,originId:origin.id,start:0,qty,value}],{sourceId,productionReceiptId:receiptId});
}
function returnSlices(s,r){
 const sh=returnShipment(s,r),m=s.costLayers.movements.find(x=>x.kind==='Shipment'&&x.sourceId===sh?.id&&x.itemId===r.itemId);must(m,'The original FIFO shipment movement is missing.');let left=r.qty;const slices=[];
 for(const x of fifoOpenShipmentSlices(s,m)){const q=Math.min(left,x.qty);if(q){slices.push({...x,qty:q,value:rangeCost(originFor(s,x.originId),x.start,q)});left-=q;}if(!left)break;}must(!left,'The FIFO shipment quantity has already been returned.');return {shipmentMovement:m.id,slices,value:slices.reduce((n,x)=>n+x.value,0)};
}
export function beforeFIFO(s,command,p,ctx){
 if(!s.costLayers)return;ctx.command=command;const c=s.costLayers;
 if(command==='setCost')must(!isFIFO(s,p.id||p.itemId),'FIFO values come from receipt layers; manual average-cost edits are blocked.');
 if(command==='receiveStock'&&isFIFO(s,p.itemId)){const scope=locationScope(s,p.locationId);must(scope.ownerId==='owner-self'&&!scope.transit&&!scope.production,'FIFO receipt must use an owned warehouse outside transit/production.');must(Number.isFinite(Number(p.unitCost))&&Number(p.unitCost)>0,'FIFO receipts need a known positive acquisition cost.');}
 if(command==='moveStock'){const stock=s.stock.find(x=>x.id===p.stockId);if(isFIFO(s,stock?.itemId)){const a=locationScope(s,stock.locationId),b=locationScope(s,p.locationId);must(a.ownerId==='owner-self'&&b.ownerId==='owner-self'&&(['business:shipTransfer','business:receiveTransfer'].includes(ctx.rootCommand)||(a.warehouseId===b.warehouseId&&!a.transit&&!b.transit)),'Use the FIFO transfer order workflow to move between owned warehouses or transit.');}}
 if(command==='shipShipment'){const sh=s.shipments.find(x=>x.id===p.id),o=s.orders.find(x=>x.id===sh?.orderId);for(const l of (sh?deliveryLines(s,sh):[]))if(isFIFO(s,l.itemId)){const slices=previewWithdrawal(s,l.itemId,l.qty,'',o.scope?.warehouseId||'wh-main');s.operations.shipping[sh.id].costSnapshot[l.itemId]=Number((slices.reduce((n,x)=>n+x.value,0)/100/l.qty).toFixed(4));}}
 if(command==='business:receiveReturn'){const r=s.business.returns.find(x=>x.id===p.id);if(isFIFO(s,r?.itemId)){const restore=returnSlices(s,r);r.fifoRestore=restore;r.costRestore={unitCost:Number((restore.value/100/r.qty).toFixed(4)),exposures:[],fifo:true};}}
 if(command==='voidShipment'){const sh=s.shipments.find(x=>x.id===p.id);for(const m of c.movements.filter(x=>x.kind==='Shipment'&&x.sourceId===sh?.id&&isFIFO(s,x.itemId)))must(!c.movements.some(t=>t.kind==='Return'&&t.shipmentMovement===m.id),'A FIFO shipment with customer returns cannot be voided; use separate reviewed corrections.');}
 if(['countStock','count:post'].includes(command)){if(command==='countStock'){const r=s.stock.find(x=>x.id===p.stockId);if(isFIFO(s,r?.itemId))must(Number(p.qty)<=r.qty,'Positive FIFO count adjustments need a costed receipt, not an invented opening layer.');}else {const count=s.insights?.counts?.find(x=>x.id===p.id);for(const row of count?.lines||[])if(isFIFO(s,row.itemId))must(row.counted<=row.expected,'Positive FIFO counts require a costed receipt.');}}
 if(command==='business:scan'&&p.mode==='Count'){const row=s.stock.find(x=>x.id===p.stockId);if(isFIFO(s,row?.itemId))must(Number(p.qty)<=row.qty,'Positive FIFO counts require a costed receipt.');}
 if(command==='business:sendReturn'){const r=s.business.returns.find(x=>x.id===p.id);if(isFIFO(s,r?.itemId))r.fifoSupplier=prepareFIFOSupplierReturn(s,r);}
 if(['business:startWork','business:finishWork'].includes(command)){const record=command.includes('Work')?s.business.workOrders.find(x=>x.id===p.id):s.business.transfers.find(x=>x.id===p.id);const ids=[record?.outputId,...(record?.components||record?.lines||[]).map(x=>x.itemId)];must(!ids.some(id=>isFIFO(s,id)),'FIFO production requires separate cost handling; existing average-cost workflows remain available.');}
}
export function afterFIFOStock(s,current,command,p,ctx){
 if(!s.costLayers)return;ctx.command=command;const root=ctx.rootCommand||command,rootP=ctx.rootPayload||p;
 if(command==='moveStock'&&['business:shipTransfer','business:receiveTransfer'].includes(root))relocateTransfer(s,current,p,ctx,root,rootP);
 for(const id of Object.keys(s.costLayers.policies)){
  const delta=physical(s,id)-s.costLayers.layers.filter(l=>l.itemId===id).reduce((n,l)=>n+l.qty,0);if(!delta){updateDisplayCost(s,id);continue;}
  if(delta>0){
   if(command==='receiveStock'){
    if(root==='business:receiveReturn'){
     const r=s.business.returns.find(x=>x.id===rootP.id);must(r?.itemId===id&&r.fifoRestore,'FIFO return source is missing.');const restored=r.fifoRestore;must(restored.slices.reduce((n,x)=>n+x.qty,0)===delta,'FIFO return quantity changed.');const slices=restored.slices.map(x=>{const l=newLayer(s,ctx,id,originFor(s,x.originId),x.start,x.qty,r.id,{warehouseId:locationScope(s,p.locationId).warehouseId});return {...x,layerId:l.id};});movement(s,ctx,id,'Return',slices,{returnId:r.id,shipmentMovement:restored.shipmentMovement});
    }else{
     const cost=cents(Number(p.unitCost)*delta);must(Number.isSafeInteger(cost)&&cost>0,'FIFO receipt cost exceeds supported precision or amount.');const c=s.costLayers,origin={id:uid(c,'fifo-origin'),itemId:id,qty:delta,baseCost:cost,totalCost:cost,time:ctx.time,adjustments:[],purchaseId:['receivePurchase','business:scan'].includes(root)?rootP.id||rootP.purchaseId:'',receiptId:'',poolId:''};c.origins.push(origin);const l=newLayer(s,ctx,id,origin,0,delta,'',{warehouseId:locationScope(s,p.locationId).warehouseId});movement(s,ctx,id,'Receipt',[{layerId:l.id,originId:origin.id,start:0,qty:delta,value:cost}]);
    }
   }else if(command==='voidShipment'){
    const m=s.costLayers.movements.find(x=>x.kind==='Shipment'&&x.sourceId===p.id&&x.itemId===id);must(m&&!s.costLayers.movements.some(x=>x.reverses===m.id),'FIFO shipment has already been restored.');const slices=m.slices.map(x=>{const old=s.costLayers.layers.find(l=>l.id===x.layerId),origin=originFor(s,x.originId);must(old&&old.start===x.start+x.qty,'Void FIFO shipments in reverse consumption order.');old.start=x.start;old.qty+=x.qty;return {...x,value:rangeCost(origin,x.start,x.qty)};});must(slices.reduce((n,x)=>n+x.qty,0)===delta,'FIFO void quantity changed.');movement(s,ctx,id,'Void',slices,{reverses:m.id});
   }else throw Error('This FIFO quantity increase requires a costed receipt or supported customer return.');
  }else{
   const returned=root==='business:disposeReturn'?s.business.returns.find(x=>x.id===rootP.id):null;
   if(root==='business:sendReturn'){
    const r=s.business.returns.find(x=>x.id===rootP.id),f=r?.fifoSupplier;must(f&&r.itemId===id&&f.slices.reduce((n,x)=>n+x.qty,0)===-delta,'FIFO supplier return quantity changed.');
    for(const x of f.slices){const l=cLayer(s,x.layerId);must(l.start===x.start&&l.qty>=x.qty&&!l.transitId,'FIFO supplier-return source range changed.');l.start+=x.qty;l.qty-=x.qty;}f.movementId=movement(s,ctx,id,'SupplierReturn',f.slices,{sourceId:r.id,returnId:r.id,warehouseId:f.warehouseId}).id;
   }else{
    const kind=command==='shipShipment'?'Shipment':command==='scrapStock'?'Scrap':'Adjustment',warehouseId=command==='shipShipment'?(s.orders.find(o=>o.id===s.shipments.find(sh=>sh.id===p.id)?.orderId)?.scope?.warehouseId||'wh-main'):locationScope(current,current.stock.find(r=>r.id===p.stockId)?.locationId).warehouseId;
    withdraw(s,ctx,id,-delta,kind,returned?.id||'',warehouseId);
   }
  }
  updateDisplayCost(s,id);
 }
 // Link child receipt origins after the parent has created its receipt record.
 if(command==='receivePurchase'||(command==='business:scan'&&p.mode==='Receive')){
  const po=s.operations.purchases.find(x=>x.id===(p.id||p.purchaseId)),old=current.operations.purchases.find(x=>x.id===po?.id);for(const receipt of po?.receipts||[]){if(old?.receipts?.some(x=>x.id===receipt.id))continue;for(const line of receipt.lines){if(!isFIFO(s,line.itemId))continue;const origins=s.costLayers.origins.filter(o=>o.purchaseId===po.id&&o.itemId===line.itemId&&(!o.receiptId||o.receiptId===receipt.id));must(origins.reduce((n,o)=>n+o.qty,0)===line.qty,'FIFO receipt origins do not match received units.');for(const o of origins){o.receiptId=receipt.id;o.poolId=s.costing?.purchases.includes(po.id)?po.id+'/'+receipt.id+'/'+line.lineId:'';}}}
 }
}
const cLayer=(s,id)=>{const l=s.costLayers.layers.find(l=>l.id===id);must(l,'FIFO source layer is missing.');return l;};
function relocateTransfer(s,current,p,ctx,root,rootP){
 const stock=current.stock.find(r=>r.id===p.stockId);if(!isFIFO(s,stock?.itemId))return;
 const t=s.business.transfers.find(t=>t.id===rootP.id),from=locationScope(current,stock.locationId),to=locationScope(s,p.locationId),dispatch=root==='business:shipTransfer';must(t,'FIFO transfer source is missing.');
 const slices=previewWithdrawal(s,stock.itemId,Number(p.qty),'',from.warehouseId,dispatch?'':t.id);
 for(const x of slices){const l=cLayer(s,x.layerId);l.start+=x.qty;l.qty-=x.qty;newLayer(s,ctx,stock.itemId,originFor(s,x.originId),x.start,x.qty,l.returnId||'',{warehouseId:to.warehouseId,createdAt:x.createdAt,transitId:dispatch?t.id:'',transitLocationId:dispatch?p.locationId:''});}
 const m=movement(s,ctx,stock.itemId,'Transfer',slices,{sourceId:t.id,transferId:t.id,phase:dispatch?'Dispatched':'Received',fromWarehouse:from.warehouseId,toWarehouse:to.warehouseId});
 t.fifoMovements=[...(t.fifoMovements||[]),m.id];if(dispatch)t.fifoDispatch={value:m.value,qty:Number(p.qty),movementId:m.id};
}
export function applyFIFOAmount(s,ctx,pool,amount,command,sourceId){
 const c=s.costLayers,origins=c.origins.filter(o=>o.poolId===pool.id);must(origins.length===1,'FIFO controlled receipt needs one exact origin.');const origin=origins[0],previous=origin.totalCost,next=previous+amount;must(Number.isSafeInteger(next)&&next>=0,'FIFO charge would create a negative or invalid layer cost.');
 const live=c.layers.filter(l=>l.originId===origin.id),retained=live.reduce((n,l)=>n+rangeCost(origin,l.start,l.qty,next)-rangeCost(origin,l.start,l.qty,previous),0),sold=c.movements.filter(m=>m.kind==='Shipment').flatMap(m=>fifoOpenShipmentSlices(s,m)).filter(x=>x.originId===origin.id).reduce((n,x)=>n+rangeCost(origin,x.start,x.qty,next)-rangeCost(origin,x.start,x.qty,previous),0);
 origin.totalCost=next;origin.adjustments.push({id:uid(c,'fifo-adjust'),ordinal:c.sequence,time:ctx.time,amount,command,sourceId});updateDisplayCost(s,pool.itemId);return {inventory:retained,cogs:sold,adjustments:amount-retained-sold};
}
export function afterFIFOAccounting(s,current,command,p,ctx){
 if(!s.costLayers)return;const c=s.costLayers;
 for(const pool of s.costing?.pools||[])if(isFIFO(s,pool.itemId)){
  const origins=c.origins.filter(o=>o.poolId===pool.id),ids=new Set(origins.map(o=>o.id));pool.remaining=c.layers.filter(l=>ids.has(l.originId)).reduce((n,l)=>n+l.qty,0);pool.sold=c.movements.filter(m=>m.kind==='Shipment').flatMap(m=>fifoOpenShipmentSlices(s,m)).filter(x=>ids.has(x.originId)).reduce((n,x)=>n+x.qty,0);pool.other=pool.qty-pool.remaining-pool.sold;
 }
 if(ctx.nested||ctx.internal)return;
 const newMovements=c.movements.filter(m=>!current.costLayers?.movements.some(x=>x.id===m.id)),newJournals=business(s).journals.filter(j=>!business(current).journals.some(x=>x.id===j.id));
 for(const j of newJournals)if(newMovements.length){j.fifoMovements=newMovements.map(m=>m.id);const layerReceipts=newMovements.flatMap(m=>m.slices).map(x=>originFor(s,x.originId)?.poolId).filter(Boolean).map(id=>s.costing?.pools.find(x=>x.id===id)?.journalId).filter(Boolean);const freightJournals=newMovements.flatMap(m=>m.slices.flatMap(x=>(originFor(s,x.originId)?.transferFees||[]).filter(f=>f.ordinal<m.ordinal&&f.start<x.start+x.qty&&x.start<f.start+f.qty).map(f=>s.transferCosting?.allocations.find(a=>a.id===f.allocationId)?.journalId))).filter(Boolean);j.dependencies=[...new Set([...(j.dependencies||[]),...freightJournals.filter(id=>id!==j.id).map(id=>'journal:'+id),...layerReceipts.filter(id=>id!==j.id).map(id=>'journal:'+id),...newMovements.flatMap(m=>m.slices).map(x=>originFor(s,x.originId)?.productionJournalId).filter(id=>id&&id!==j.id).map(id=>'journal:'+id)])];}
 for(const m of newMovements)m.journalIds=newJournals.map(j=>j.id);
 captureHistory(s,ctx,command,p);
}
export function historicalRows(s){
 const rows=[];for(const item of s.items){const stocks=s.stock.filter(r=>r.itemId===item.id&&r.qty>0&&locationScope(s,r.locationId).ownerId==='owner-self'),warehouses=[...new Set(stocks.map(r=>locationScope(s,r.locationId).warehouseId))];for(const warehouseId of warehouses){const qty=stocks.filter(r=>locationScope(s,r.locationId).warehouseId===warehouseId).reduce((n,r)=>n+r.qty,0),cost=s.operations?.costs[item.id]??null,fifo=isFIFO(s,item.id),value=fifo?fifoValue(s,item.id,warehouseId):cost===null?null:cents(qty*cost);rows.push({itemId:item.id,sku:item.sku,name:item.name,description:item.description||'',warehouseId,warehouse:business(s).warehouses.find(w=>w.id===warehouseId)?.name||warehouseId,qty,method:fifo?'FIFO':'Average',unitCost:cost,value,sample:s.costing?.sampleCosts?.includes(item.id)||false});}}
 return rows;
}
function captureHistory(s,ctx,command,p,force=false){
 const c=s.costLayers;if(!c?.history||ctx.nested||ctx.internal)return;const rows=historicalRows(s),previous=c.history.snapshots.at(-1);if(!force&&previous&&JSON.stringify(previous.rows)===JSON.stringify(rows))return;
 must(c.history.snapshots.length<5000,'Historical snapshot capacity reached. Export and review before extending retention.');const id=uid(c,'valuation'),currency=business(s).homeCurrency,total=cents(business(s).warehouses.reduce((n,w)=>n+rows.filter(r=>r.warehouseId===w.id&&r.value!==null).reduce((v,r)=>v+r.value,0)/100,0));c.history.snapshots.push({id,ordinal:c.sequence,time:ctx.time,revision:s.revision+1,label:command.startsWith('cost:history')?p.label:command,command,sourceId:p.id||p.stockId||'',currency,rows,total,missing:rows.filter(r=>r.value===null).map(r=>r.sku),layerRows:c.layers.filter(l=>l.qty>0).map(l=>({...l,warehouseId:layerWarehouse(s,l),value:rangeCost(originFor(s,l.originId),l.start,l.qty)}))});
}
export function fifoCommand(s,command,p,ctx){
 if(!['cost:enableFIFO','cost:historyStart','cost:historySnapshot'].includes(command))return null;must(p.reviewed===true,'Review and confirm the costing/history action.');const c=setup(s);let id='';
 if(command==='cost:enableFIFO'){
  const item=s.items.find(x=>x.id===p.itemId),warehouse=business(s).warehouses.find(x=>x.id===p.warehouseId);must(item&&warehouse,'Choose a product and owned warehouse.');must(!c.policies[item.id]&&!s.stock.some(r=>r.itemId===item.id)&&!s.operations.purchases.some(po=>(po.receipts||[]).some(r=>r.lines.some(l=>l.itemId===item.id)))&&!s.shipments.some(sh=>s.orders.find(o=>o.id===sh.orderId)?.lines.some(l=>l.itemId===item.id)),'Enable FIFO only once on a new product with no stock or receipt/shipment history. Existing average costs are preserved.');c.policies[item.id]={method:'FIFO',warehouseId:warehouse.id,enabledAt:ctx.time,reason:label(p.reason),actor:ctx.actor||'Local owner'};id=item.id;
 }else if(command==='cost:historyStart'){must(!c.history,'Historical recording already started.');c.history={startedAt:ctx.time,snapshots:[]};captureHistory(s,ctx,command,{label:label(p.label)},true);id=c.history.snapshots[0].id;}
 else {must(c.history,'Start historical recording first.');captureHistory(s,ctx,command,{label:label(p.label)},true);id=c.history.snapshots.at(-1).id;}
 return {type:command==='cost:enableFIFO'?'FIFO enabled for new product':'Historical valuation snapshot saved',message:'Costing record saved',reference:id,resultId:id};
}
export function historicalValuation(s,{snapshotId='',asOf='',warehouseId='',itemId=''}={}){
 const h=s.costLayers?.history;must(h?.snapshots.length,'Historical recording has not started. Earlier balances cannot be reconstructed from current costs.');let snapshot=h.snapshots.find(x=>x.id===snapshotId);must(!snapshotId||snapshot,'The selected preserved snapshot is unavailable.');
 if(!snapshot){const cutoff=asOf?(asOf.length===10?Date.parse(asOf+'T23:59:59.999Z'):Date.parse(asOf)):Infinity;must(!Number.isNaN(cutoff),'Choose a valid as-of date/time.');snapshot=h.snapshots.filter(x=>Date.parse(x.time)<=cutoff).sort((a,b)=>Date.parse(b.time)-Date.parse(a.time)||b.ordinal-a.ordinal)[0];}must(snapshot,'No preserved snapshot exists at or before this date/time.');
 const rows=snapshot.rows.filter(r=>(!warehouseId||r.warehouseId===warehouseId)&&(!itemId||r.itemId===itemId));return {...snapshot,rows,total:rows.reduce((n,r)=>n+(r.value||0),0),missing:rows.filter(r=>r.value===null).map(r=>r.sku),coverageStart:h.startedAt,layerRows:snapshot.layerRows.filter(l=>(!itemId||l.itemId===itemId)&&(!warehouseId||layerWarehouse(s,l)===warehouseId))};
}
export function validateFIFO(s,validationContext={}){
 const c=s.costLayers;if(!c)return;must(c.version===1&&Number.isSafeInteger(c.sequence)&&c.sequence>=0&&Array.isArray(c.origins)&&Array.isArray(c.layers)&&Array.isArray(c.movements),'Invalid FIFO ledger.');must(c.origins.length<=50000&&c.layers.length<=50000&&c.movements.length<=50000,'FIFO ledger capacity exceeded.');
 for(const [id,p]of Object.entries(c.policies)){must(s.items.some(i=>i.id===id)&&p.method==='FIFO'&&business(s).warehouses.some(w=>w.id===p.warehouseId)&&Number.isFinite(Date.parse(p.enabledAt)),'Invalid FIFO policy.');must(s.stock.filter(r=>r.itemId===id&&r.qty>0).every(r=>{const scope=locationScope(s,r.locationId);return scope.ownerId==='owner-self';}),'FIFO stock must retain company ownership.');must(c.layers.filter(l=>l.itemId===id).reduce((n,l)=>n+l.qty,0)===physical(s,id),'FIFO layer quantity does not match physical stock.');}
 for(const id of Object.keys(c.policies)){
  for(const w of business(s).warehouses){const rows=s.stock.filter(r=>r.itemId===id&&locationScope(s,r.locationId).ownerId==='owner-self'&&locationScope(s,r.locationId).warehouseId===w.id&&!locationScope(s,r.locationId).transit),layers=c.layers.filter(l=>l.itemId===id&&layerWarehouse(s,l)===w.id&&!l.transitId);must(rows.reduce((n,r)=>n+r.qty,0)===layers.reduce((n,l)=>n+l.qty,0),'FIFO warehouse layers do not match physical stock.');}
  for(const t of business(s).transfers){const layers=c.layers.filter(l=>l.itemId===id&&l.transitId===t.id),locationIds=new Set(layers.map(l=>l.transitLocationId)),quantity=s.stock.filter(r=>r.itemId===id&&locationIds.has(r.locationId)).reduce((n,r)=>n+r.qty,0);must(quantity===layers.reduce((n,l)=>n+l.qty,0),'FIFO transit layers do not match physical stock.');}
 }
 const ids=[...c.origins,...c.layers,...c.movements,...c.origins.flatMap(o=>o.adjustments||[]),...(c.history?.snapshots||[])].map(x=>x.id);must(new Set(ids).size===ids.length,'Duplicate FIFO/history identity.');
 for(const o of c.origins){must(o.adjustments.every(a=>Number.isSafeInteger(a.amount)&&Number.isSafeInteger(a.ordinal)&&a.ordinal>0&&a.ordinal<=c.sequence&&Number.isFinite(Date.parse(a.time))),'Invalid FIFO adjustment history.');must(isFIFO(s,o.itemId)&&Number.isSafeInteger(o.qty)&&o.qty>0&&Number.isSafeInteger(o.baseCost)&&o.baseCost>0&&Number.isSafeInteger(o.totalCost)&&o.totalCost>=0&&o.totalCost===o.baseCost+o.adjustments.reduce((n,a)=>n+a.amount,0),'Invalid FIFO origin amount.');const receipt=c.movements.filter(m=>m.kind==='Receipt'&&m.slices.some(x=>x.originId===o.id));must(receipt.length===1&&receipt[0].slices.filter(x=>x.originId===o.id).reduce((n,x)=>n+x.qty,0)===o.qty,'FIFO origin receipt quantity changed.');const sold=c.movements.filter(m=>m.kind==='Shipment').flatMap(m=>fifoOpenShipmentSlices(s,m)).filter(x=>x.originId===o.id).reduce((n,x)=>n+x.qty,0),other=c.movements.filter(m=>['Scrap','Adjustment','SupplierReturn','Production'].includes(m.kind)).flatMap(m=>m.slices).filter(x=>x.originId===o.id).reduce((n,x)=>n+x.qty,0),remaining=c.layers.filter(l=>l.originId===o.id).reduce((n,l)=>n+l.qty,0);must(remaining+sold+other===o.qty,'FIFO origin exposure does not conserve units.');const ranges=c.layers.filter(l=>l.originId===o.id&&l.qty>0).sort((a,b)=>a.start-b.start);for(let i=1;i<ranges.length;i++)must(ranges[i-1].start+ranges[i-1].qty<=ranges[i].start,'FIFO live unit ranges overlap.');}
 for(const l of c.layers){const o=originFor(s,l.originId);must(o&&o.itemId===l.itemId&&Number.isSafeInteger(l.start)&&Number.isSafeInteger(l.qty)&&l.start>=0&&l.qty>=0&&l.start+l.qty<=o.qty&&Number.isFinite(Date.parse(l.createdAt)),'Invalid FIFO layer range.');must(business(s).warehouses.some(w=>w.id===layerWarehouse(s,l))&&(!l.transitId||business(s).transfers.some(t=>t.id===l.transitId)&&locationScope(s,l.transitLocationId).transit),'Invalid FIFO layer warehouse or transit scope.');}
 for(const m of c.movements){must(['Receipt','Shipment','Return','Scrap','Adjustment','Void','SupplierReturn','Transfer','Production'].includes(m.kind)&&isFIFO(s,m.itemId)&&Number.isSafeInteger(m.value)&&m.value>=0&&m.slices.length>0&&Number.isFinite(Date.parse(m.time)),'Invalid FIFO movement.');for(const x of m.slices){const o=originFor(s,x.originId);must(o&&o.itemId===m.itemId&&Number.isSafeInteger(x.start)&&Number.isSafeInteger(x.qty)&&x.start>=0&&x.qty>0&&x.start+x.qty<=o.qty&&x.value===rangeCost(o,x.start,x.qty,o.baseCost+o.adjustments.filter(a=>a.ordinal<m.ordinal).reduce((n,a)=>n+a.amount,0),m.ordinal),'FIFO movement source value changed.');}must(m.value===m.slices.reduce((n,x)=>n+x.value,0),'FIFO movement amount changed.');if(m.kind==='Return'){const original=c.movements.find(x=>x.id===m.shipmentMovement);must(original?.kind==='Shipment','FIFO return has no original shipment.');const previous=c.movements.filter(x=>x.kind==='Return'&&x.shipmentMovement===original.id&&x.ordinal<m.ordinal).flatMap(x=>x.slices),available=subtractRanges(original.slices,previous);for(const x of m.slices)must(available.some(a=>a.originId===x.originId&&x.start>=a.start&&x.start+x.qty<=a.start+a.qty),'FIFO shipment range was returned twice.');}}
 validateFIFOTransfers(s,validationContext);
 if(c.history){must(Number.isFinite(Date.parse(c.history.startedAt))&&c.history.snapshots.length<=5000,'Invalid historical coverage.');for(const snap of c.history.snapshots){must(validUnicode(snap.label)&&charLength(snap.label)<=120&&snap.rows.every(r=>['Average','FIFO'].includes(r.method)&&(r.unitCost===null||Number.isFinite(r.unitCost)&&r.unitCost>=0)),'Historical method or label is invalid.');for(const layer of snap.layerRows){const origin=originFor(s,layer.originId);must(origin&&layer.qty>0&&layer.value===rangeCost(origin,layer.start,layer.qty,origin.baseCost+origin.adjustments.filter(a=>a.ordinal< snap.ordinal).reduce((n,a)=>n+a.amount,0),snap.ordinal),'Historical FIFO layer value changed.');}for(const r of snap.rows.filter(r=>r.method==='FIFO'))must(r.qty===snap.layerRows.filter(l=>l.itemId===r.itemId&&layerWarehouse(s,l)===r.warehouseId).reduce((n,l)=>n+l.qty,0)&&r.value===snap.layerRows.filter(l=>l.itemId===r.itemId&&layerWarehouse(s,l)===r.warehouseId).reduce((n,l)=>n+l.value,0),'Historical FIFO row does not match saved layers.');must(Number.isFinite(Date.parse(snap.time))&&Date.parse(snap.time)>=Date.parse(c.history.startedAt)&&Number.isSafeInteger(snap.total)&&snap.rows.every(r=>Number.isSafeInteger(r.qty)&&r.qty>=0&&(r.value===null||Number.isSafeInteger(r.value)&&r.value>=0))&&snap.total===snap.rows.reduce((n,r)=>n+(r.value||0),0),'Historical valuation snapshot is invalid.');}}
}
function validateFIFOTransfers(s,ctx){
 const c=s.costLayers;
 for(const m of c.movements.filter(m=>m.kind==='Transfer')){
  const t=business(s).transfers.find(t=>t.id===m.transferId),dispatch=m.phase==='Dispatched';must(t&&m.sourceId===t.id&&t.fifoMovements?.includes(m.id)&&['Dispatched','Received'].includes(m.phase)&&m.command===(dispatch?'business:shipTransfer':'business:receiveTransfer'),'Invalid FIFO transfer movement link.');
  const source=locationScope(s,s.stock.find(r=>r.id===t.stockId)?.locationId),dest=locationScope(s,t.destination);must(m.fromWarehouse===source.warehouseId&&m.toWarehouse===(dispatch?source.warehouseId:dest.warehouseId),'FIFO transfer warehouses changed.');
  for(const x of m.slices){const l=c.layers.find(l=>l.id===x.layerId);must(l&&x.createdAt===l.createdAt&&x.warehouseId===m.fromWarehouse,'FIFO transfer origin date or source changed.');}
 }
 for(const t of business(s).transfers.filter(t=>t.fifoDispatch)){
  const moves=c.movements.filter(m=>m.kind==='Transfer'&&m.transferId===t.id),sent=moves.filter(m=>m.phase==='Dispatched'),received=moves.filter(m=>m.phase==='Received');must(sent.length===1&&JSON.stringify(t.fifoMovements)===JSON.stringify(moves.map(m=>m.id))&&t.fifoDispatch.movementId===sent[0].id&&t.fifoDispatch.value===sent[0].value&&t.fifoDispatch.qty===t.qty&&sent[0].slices.reduce((n,x)=>n+x.qty,0)===t.qty,'FIFO transfer dispatch snapshot changed.');
  let available=sent[0].slices;for(const m of received){must(m.ordinal>sent[0].ordinal,'FIFO transfer receipt predates dispatch.');for(const x of m.slices)must(available.some(a=>a.originId===x.originId&&x.start>=a.start&&x.start+x.qty<=a.start+a.qty),'FIFO transfer range was received twice.');available=subtractRanges(available,m.slices);}
  const receivedQty=received.flatMap(m=>m.slices).reduce((n,x)=>n+x.qty,0),transit=c.layers.filter(l=>l.transitId===t.id&&l.qty);must(receivedQty<=t.qty&&transit.reduce((n,l)=>n+l.qty,0)===t.qty-receivedQty,'FIFO transfer transit balance changed.');for(const l of transit)must(available.some(a=>a.originId===l.originId&&l.start>=a.start&&l.start+l.qty<=a.start+a.qty),'FIFO transit origin range changed.');
  // A child move is validated before its parent advances the transfer counter.
  // The committed transaction, imports and reopened workspaces must agree fully.
  if(!ctx.nested)must(t.received===receivedQty&&t.status===(receivedQty===t.qty?'Received':'In transit'),'FIFO transfer received quantity or status changed.');
 }
}

