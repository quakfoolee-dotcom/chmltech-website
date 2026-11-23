import {productUnits} from './packaging.mjs?demo=9c44c6dabb8d4728';
export function warehouseLabelRows(s,{warehouseId='wh-main',itemId=''}={}){
 const scope=id=>s.business?.locationMeta[id]||{warehouseId:'wh-main',ownerId:'owner-self'},rows=[];
 for(const l of s.locations.filter(l=>scope(l.id).warehouseId===warehouseId&&['Storage','Receiving','Hold'].includes(l.type)&&!scope(l.id).transit&&!scope(l.id).production))rows.push({code:l.code,caption:'Source / destination bin',description:l.name});
 for(const item of s.items.filter(i=>!itemId||i.id===itemId)){
  rows.push({code:item.sku,caption:'Product barcode',description:item.name});
  for(const unit of productUnits(s,item.id).filter(u=>u.id!=='base'))rows.push({code:unit.barcode,caption:'Packaging barcode',description:`${item.name} · ${unit.code} · 1 ${unit.name} = ${unit.factor} ${item.uom}`});
  for(const lot of new Set(s.stock.filter(r=>r.itemId===item.id&&r.qty>0&&scope(r.locationId).warehouseId===warehouseId).map(r=>r.lot)))rows.push({code:lot,caption:'Lot / batch',description:item.name,qr:true});
 }
 return rows;
}
