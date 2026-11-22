const must=(ok,msg)=>{if(!ok)throw Error(msg);};
const find=(rows,id)=>{const r=rows.find(x=>x.id===id);must(r,'Record not found.');return r;};
export const executionGroup=(s,id)=>s.warehouseExecution?.groups[id];
export const executionPack=(s,id)=>s.warehouseExecution?.packing[id];
export function groupView(s,id){
 const b=find(s.operations.batches,id),g=executionGroup(s,id);
 return {batch:b,control:g,slots:b.pickIds.map((pid,i)=>{const p=find(s.picks,pid),o=find(s.orders,p.orderId),slot=g?.slots.find(x=>x.pickId===pid);return {pick:p,order:o,tote:slot?.tote||`${b.name}-T${i+1}`,counts:slot?.counts||{},lines:p.allocations.map((a,index)=>({...a,index,sku:find(s.items,a.itemId).sku,name:find(s.items,a.itemId).name,bin:find(s.locations,find(s.stock,a.sourceStockId).locationId).code,scanned:slot?.counts[index]?.qty||0}))};})};
}
export function packView(s,id){const sh=find(s.shipments,id),p=find(s.picks,sh.pickId),m=executionPack(s,id);return {shipment:sh,order:find(s.orders,sh.orderId),control:m,lines:p.allocations.map((a,index)=>({...a,index,sku:find(s.items,a.itemId).sku,name:find(s.items,a.itemId).name,scanned:(m?.cartons||[]).reduce((n,c)=>n+(c.counts[index]?.qty||0),0)}))};}

