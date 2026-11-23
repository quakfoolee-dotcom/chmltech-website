import {resolveProductBarcode,scannedQuantity,wholeUnits} from './packaging.mjs?demo=2d15b6e9cd84b84d';
import {businessDay} from './company-date.mjs?demo=2d15b6e9cd84b84d';
const must=(ok,message)=>{if(!ok)throw Error(message);};
const scope=(s,id)=>s.business?.locationMeta[id]||{warehouseId:'wh-main',ownerId:'owner-self'};
const loc=(s,code)=>{const rows=s.locations.filter(l=>l.code.toUpperCase()===String(code||'').trim().toUpperCase());must(rows.length===1,'Scan a known location barcode.');return rows[0];};
export function stockLookup(s,{warehouseId='wh-main',code='',lot=''}={},now=new Date().toISOString()){
 const value=String(code).trim();must(value,'Scan or enter a product or location barcode.');
 const location=s.locations.find(l=>l.code.toUpperCase()===value.toUpperCase());
 let product=null,unit=null;if(!location){const match=resolveProductBarcode(s,value);product=match.item;unit=match.unit;}
 const rows=s.stock.filter(r=>r.qty>0&&scope(s,r.locationId).warehouseId===warehouseId&&(!location||r.locationId===location.id)&&(!product||r.itemId===product.id)&&(!lot||r.lot===lot)).map(r=>{
  const l=s.locations.find(l=>l.id===r.locationId),item=s.items.find(i=>i.id===r.itemId),meta=scope(s,l.id),expiresOn=s.operations?.lots?.[`${r.itemId}|${r.lot}`]?.expiresOn||'',expired=!!expiresOn&&expiresOn<businessDay(s,now),held=l.type==='Hold'||!!meta.transit||!!meta.production;
  return {stockId:r.id,itemId:item.id,sku:item.sku,name:item.name,description:item.description||'',uom:item.uom,location:l.code,locationName:l.name,lot:r.lot,qty:r.qty,reserved:r.committed,available:!held&&!expired&&l.pickable?r.qty-r.committed:0,held,expired,expiresOn,owner:s.business?.owners.find(o=>o.id===meta.ownerId)?.name||meta.ownerId,serials:s.operations?.serials?.[r.id]||[]};
 });
 return {product,location,unit,rows,onHand:rows.reduce((n,r)=>n+r.qty,0),reserved:rows.reduce((n,r)=>n+r.reserved,0),available:rows.reduce((n,r)=>n+r.available,0)};
}
export function mobileStockCommand(s,command,p,ctx){
 if(command!=='mobile:move')return null;
 must(p.reviewed===true,'Review the source, destination and converted quantity.');
 must(/^[a-zA-Z0-9-]{16,80}$/.test(p.requestId||''),'A unique move request is required.');
 must(!(s.mobileStock?.moves||[]).some(m=>m.requestId===p.requestId),'This move was already saved. Refresh before scanning again.');
 const source=loc(s,p.sourceCode),destination=loc(s,p.destinationCode),from=scope(s,source.id),to=scope(s,destination.id);
 must(from.warehouseId===p.warehouseId&&to.warehouseId===p.warehouseId,'Mobile moves must stay in the selected warehouse. Use a transfer order between warehouses.');
 must(from.ownerId===to.ownerId,'Mobile moves must retain inventory ownership.');
 must(source.id!==destination.id,'Choose a different destination.');
 must(['Storage','Receiving'].includes(source.type)&&!from.transit&&!from.production,'Use inspection or the controlled workflow for this source.');
 must(['Storage','Receiving','Hold'].includes(destination.type)&&!to.transit&&!to.production,'Choose a storage, receiving or quality-hold destination.');
 const capture=scannedQuantity(s,p),item=s.items.find(i=>i.id===capture.itemId),lot=String(p.lot||'').trim();must(lot,'Scan the exact lot or batch.');
 const row=s.stock.find(r=>r.locationId===source.id&&r.itemId===item.id&&r.lot===lot);
 must(row&&capture.baseQty<=row.qty-row.committed,'The source does not have enough unreserved stock for this lot.');
 const serials=Array.isArray(p.serials)?p.serials:String(p.serials||'').split(/[\n,]/).map(v=>v.trim()).filter(Boolean);
 if(s.operations?.tracking?.[item.id]==='Serial')must(serials.length===capture.baseQty&&new Set(serials).size===serials.length,'Scan one distinct serial number for every base unit moved.');
 const result=ctx.dispatch(s,'moveStock',{stockId:row.id,locationId:destination.id,qty:wholeUnits(capture.baseQty),serials},{now:ctx.time});Object.assign(s,result.state);
 s.mobileStock||={version:1,moves:[]};must(s.mobileStock.moves.length<100000,'Mobile move history is full.');
 s.mobileStock.moves.push({requestId:p.requestId,time:ctx.time,actor:ctx.actor||'Local owner',warehouseId:p.warehouseId,ownerId:from.ownerId,sourceId:source.id,destinationId:destination.id,stockId:row.id,lot,...capture,serials});
 p.unitCapture=capture;
 return {type:'Mobile stock move saved',reference:item.sku,message:'Stock moved without changing its company inventory value.',resultId:row.id};
}
export function validateMobileStock(s){
 if(!s.mobileStock)return true;const m=s.mobileStock;
 must(m.version===1&&Array.isArray(m.moves)&&m.moves.length<=100000,'Invalid mobile move history.');const ids=new Set();
 for(const r of m.moves){must(/^[a-zA-Z0-9-]{16,80}$/.test(r.requestId)&&!ids.has(r.requestId),'Duplicate mobile move request.');ids.add(r.requestId);must(s.items.some(i=>i.id===r.itemId)&&s.locations.some(l=>l.id===r.sourceId)&&s.locations.some(l=>l.id===r.destinationId)&&r.sourceId!==r.destinationId,'Mobile move references are missing.');wholeUnits(r.baseQty);must(r.baseQty===r.quantity*r.factor,'Mobile move unit snapshot changed.');}
 return true;
}
