// First-class deliveries retain the original sales order and its prices.
import {validUnicode,charLength} from './unicode.mjs?demo=9c44c6dabb8d4728';
const must=(v,m)=>{if(!v)throw Error(m);};
export const pickLines=(s,p)=>p.lines||s.orders.find(o=>o.id===p.orderId).lines;
export const deliveryLines=(s,sh)=>sh.lines||s.operations?.shipping[sh.id]?.orderLines||pickLines(s,s.picks.find(p=>p.id===sh.pickId));
export const openPicks=(s,o)=>s.picks.filter(p=>p.orderId===o.id&&!(p.status==='Finished'&&s.shipments.find(sh=>sh.id===p.shipmentId)?.status==='Shipped'));
export function fulfillmentRows(s,o){
 const shipments=s.shipments.filter(sh=>sh.orderId===o.id&&sh.status==='Shipped'),active=openPicks(s,o);
 return o.lines.map(l=>{const shipped=shipments.reduce((n,sh)=>n+(deliveryLines(s,sh).find(x=>x.itemId===l.itemId)?.qty||0),0),released=active.reduce((n,p)=>n+(pickLines(s,p).find(x=>x.itemId===l.itemId)?.qty||0),0);return {...l,shipped,released,remaining:l.qty-shipped,backorder:Math.max(0,l.qty-shipped-released)};});
}
export function fulfillmentStatus(s,o){
 if(o.status==='Cancelled')return 'Cancelled';const active=openPicks(s,o),rows=fulfillmentRows(s,o);
 if(active.length){const p=active[0];return p.status==='Entered'?(rows.some(l=>l.shipped)?'Part shipped':'Issued'):p.status==='Committed'?'Picking':'Picked';}
 return rows.every(l=>l.remaining===0)?'Fulfilled':'Backordered';
}
export const outstandingLines=(s,o)=>fulfillmentRows(s,o).filter(l=>l.remaining>0).map(({itemId,remaining})=>({itemId,qty:remaining}));
export const returnShipment=(s,r)=>s.shipments.find(sh=>sh.orderId===r.sourceId&&sh.status==='Shipped'&&(!r.shipmentId||sh.id===r.shipmentId));
export function validateFulfillment(s){
 for(const o of s.orders.filter(o=>o.fulfillment)){
  const f=o.fulfillment;must(f.version===1&&Array.isArray(f.lines)&&JSON.stringify(f.lines)===JSON.stringify(o.lines),'Original partial-shipment order quantities changed.');
  must(JSON.stringify(f.prices)===JSON.stringify(o.pricedLines||[]),'Original partial-shipment prices changed.');
  must(typeof f.reason==='string'&&f.reason.trim()&&validUnicode(f.reason)&&charLength(f.reason)<=240&&Number.isFinite(Date.parse(f.time)),'Invalid partial shipment review.');
  const picks=s.picks.filter(p=>p.orderId===o.id);must(picks.length>0&&picks.length<=200&&picks.at(-1).id===o.pickId,'Invalid delivery pick history.');
  must(openPicks(s,o).length<=1,'Finish the current delivery before releasing another.');
  for(const p of picks){must(Array.isArray(p.lines)&&p.lines.length>0&&new Set(p.lines.map(l=>l.itemId)).size===p.lines.length&&p.lines.every(l=>o.lines.some(x=>x.itemId===l.itemId)&&Number.isSafeInteger(l.qty)&&l.qty>0),'Invalid delivery quantities.');
   for(const sh of s.shipments.filter(sh=>sh.pickId===p.id&&sh.status!=='Cancelled'))must(JSON.stringify(sh.lines)===JSON.stringify(p.lines),'Shipment quantities changed after picking.');
  }
  must(fulfillmentRows(s,o).every(l=>l.shipped>=0&&l.released>=0&&l.remaining>=l.released),'Delivery quantities exceed the original sales order.');
  must(o.status===fulfillmentStatus(s,o),'Order and partial shipment states disagree.');
  if(o.status==='Cancelled')must(!s.shipments.some(sh=>sh.orderId===o.id&&sh.status==='Shipped'),'Close outstanding backorders separately from shipped history.');
 }
 for(const sh of s.shipments)if(sh.lines)must(s.orders.find(o=>o.id===sh.orderId)?.fulfillment,'Delivery shipment lines require an original order snapshot.');
 for(const p of s.picks)if(p.lines)must(s.orders.find(o=>o.id===p.orderId)?.fulfillment,'Delivery lines require an original order snapshot.');
}
export function releaseDelivery(s,o,p,ctx){
 must(['Draft','Issued','Backordered','Part shipped'].includes(o.status),'Release quantities before committing or packing a delivery.');
 must(!Object.values(s.operations?.families||{}).some(f=>f.orderIds.includes(o.id)),'Keep existing split-order families separate from partial shipments.');
 const existing=openPicks(s,o);must(existing.length<=1&&existing.every(pk=>pk.status==='Entered'&&!s.operations?.picks[pk.id]?.batchId),'Release or change an uncommitted pick outside a batch.');
 must(!s.shipments.some(sh=>sh.orderId===o.id)&&!s.picks.some(pk=>pk.orderId===o.id&&pk.status!=='Entered')||!!o.fulfillment,'Enable partial deliveries before the first physical shipment.');
 const reason=String(p.reason||'').trim();must(reason&&validUnicode(reason)&&charLength(reason)<=240,'Enter a partial shipment reason (up to 240 characters).');
 const lines=(p.lines||[]).map(l=>({itemId:l.itemId,qty:Number(l.qty)})).filter(l=>l.qty!==0),remaining=fulfillmentRows(s,o);
 must(lines.length>0&&lines.length<=50&&new Set(lines.map(l=>l.itemId)).size===lines.length&&lines.every(l=>Number.isSafeInteger(l.qty)&&l.qty>0&&remaining.some(r=>r.itemId===l.itemId&&l.qty<=r.remaining)),'Choose positive whole delivery quantities within the remaining order balance.');
 o.fulfillment||={version:1,lines:structuredClone(o.lines),prices:structuredClone(o.pricedLines||[]),time:ctx.time,reason};
 let pk=existing[0];if(!pk){const id=ctx.uid(s,'pick');pk={id,number:`PK-${s.counters.pick}`,orderId:o.id,status:'Entered',allocations:[],shipmentId:null};s.picks.push(pk);o.pickId=id;}
 pk.lines=lines;pk.releaseReason=reason;pk.releasedAt=ctx.time;pk.scanCounts={};o.status=fulfillmentStatus(s,o);return pk;
}
