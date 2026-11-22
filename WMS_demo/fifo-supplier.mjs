// Commercial credit matching keeps the selected receipt; the accounting
// withdrawal consumes the warehouse's oldest FIFO ranges. Settlement retains
// the dispatch-time book cents even when the credit uses a different price.
import {isFIFO,rangeCost,layerWarehouse} from './fifo.mjs';
import {locationScope} from './business.mjs';
const must=(v,m)=>{if(!v)throw Error(m);};
const originFor=(s,id)=>s.costLayers.origins.find(o=>o.id===id);
const atMovement=(origin,m)=>origin.baseCost+origin.adjustments.filter(a=>a.ordinal<m.ordinal).reduce((n,a)=>n+a.amount,0);

export function prepareFIFOSupplierReturn(s,r){
 must(r?.kind==='Supplier'&&r.status==='Requested'&&isFIFO(s,r.itemId),'Choose an open FIFO supplier return.');
 const po=s.operations.purchases.find(x=>x.id===r.sourceId),warehouseId=po?.scope?.warehouseId||'wh-main';
 must(po&&(!po.scope||po.scope.ownerId==='owner-self')&&s.costing?.purchases.includes(po.id),'FIFO supplier returns require an owned, controlled purchase receipt.');
 const pool=s.costing.pools.find(x=>x.purchaseId===po.id&&x.receiptId===r.receiptId&&x.itemId===r.itemId);
 must(pool&&!pool.blocked,'Choose the original controlled FIFO receipt before dispatching this return.');
 const candidates=s.costLayers.layers.filter(l=>l.itemId===r.itemId&&l.qty>0&&!l.transitId&&layerWarehouse(s,l)===warehouseId).sort((a,b)=>Date.parse(a.createdAt)-Date.parse(b.createdAt)||a.ordinal-b.ordinal);
 let left=r.qty;const slices=[];
 for(const l of candidates){const qty=Math.min(left,l.qty);if(qty){const o=originFor(s,l.originId);slices.push({layerId:l.id,originId:l.originId,start:l.start,qty,value:rangeCost(o,l.start,qty)});left-=qty;}if(!left)break;}
 must(!left,'The purchase warehouse has insufficient settled FIFO ranges for this supplier return. Receive any transfer first.');
 const value=slices.reduce((n,x)=>n+x.value,0);must(value>0,'FIFO supplier return must remove positive book value.');
 return {poolId:pool.id,warehouseId,slices,value};
}

function sourceMovement(s,r){
 const snapshot=r.fifoSupplier,m=s.costLayers?.movements.find(x=>x.id===snapshot?.movementId);
 must(m?.kind==='SupplierReturn'&&m.sourceId===r.id&&m.itemId===r.itemId,'The frozen FIFO supplier-return movement is missing.');
 return m;
}

export function fifoSupplierCreditBookValue(s,r,used,qty){
 const m=sourceMovement(s,r);
 must(Number.isSafeInteger(used)&&used>=0&&Number.isSafeInteger(qty)&&qty>0&&used+qty<=r.qty,'Credits exceed the FIFO supplier-return quantity.');
 let offset=used,left=qty,value=0;
 for(const x of m.slices){if(offset>=x.qty){offset-=x.qty;continue;}const take=Math.min(left,x.qty-offset),o=originFor(s,x.originId);must(o,'FIFO credit cost origin is missing.');value+=rangeCost(o,x.start+offset,take,atMovement(o,m),m.ordinal);left-=take;offset=0;if(!left)break;}
 must(!left,'The frozen FIFO return does not cover this credit.');return value;
}

export function validateFIFOSupplierReturn(s,r){
 const snapshot=r.fifoSupplier;if(!snapshot){must(!isFIFO(s,r.itemId),'FIFO supplier-return ranges are missing.');return;}
 const m=sourceMovement(s,r),po=s.operations.purchases.find(x=>x.id===r.sourceId),pool=s.costing?.pools.find(x=>x.id===snapshot.poolId);
 must(r.status==='Sent'&&m.time===r.sentAt&&isFIFO(s,r.itemId)&&pool?.purchaseId===r.sourceId&&pool.receiptId===r.receiptId&&pool.itemId===r.itemId&&r.costPosting.poolId===snapshot.poolId&&snapshot.warehouseId===(po?.scope?.warehouseId||'wh-main'),'FIFO supplier return changed its receipt or warehouse.');
 must(m.value===snapshot.value&&snapshot.value===r.costPosting?.value&&JSON.stringify(m.slices)===JSON.stringify(snapshot.slices)&&m.slices.reduce((n,x)=>n+x.qty,0)===r.qty,'Frozen FIFO supplier-return book ranges changed.');
 for(const x of m.slices){const o=originFor(s,x.originId),l=s.costLayers.layers.find(l=>l.id===x.layerId);must(o?.itemId===r.itemId&&l&&layerWarehouse(s,l)===snapshot.warehouseId&&!l.transitId,'FIFO supplier return changed its source layer.');must(x.value===rangeCost(o,x.start,x.qty,atMovement(o,m),m.ordinal),'FIFO supplier-return dispatch cost changed.');}
 must(!r.stockId||locationScope(s,s.stock.find(x=>x.id===r.stockId)?.locationId).warehouseId===snapshot.warehouseId,'FIFO supplier-return physical stock changed its warehouse.');
}

