import {businessDay} from './company-date.mjs?demo=45f52980507d3a1b';
import {returnShipment,deliveryLines} from './fulfillment.mjs?demo=45f52980507d3a1b';
// A received customer return can be inspected in several batches.
import {business,locationScope,sameScope} from './business.mjs?demo=45f52980507d3a1b';
const must=(v,m)=>{if(!v)throw Error(m);};
export const dispositionTotals=r=>({restocked:(r.dispositions||[]).filter(x=>x.disposition==='Restock').reduce((n,x)=>n+x.qty,0),scrapped:(r.dispositions||[]).filter(x=>x.disposition==='Scrap').reduce((n,x)=>n+x.qty,0),pending:r.status==='Received'?r.qty-(r.dispositions||[]).reduce((n,x)=>n+x.qty,0):0});
export function disposeCustomerReturn(s,p,ctx,run){
 const r=business(s).returns.find(x=>x.id===p.id);must(r?.kind==='Customer'&&r.status==='Received','Receive and inspect the customer return first.');const left=dispositionTotals(r).pending,q=Number(p.qty??left);
 must(Number.isSafeInteger(q)&&q>0&&q<=left,'Disposition quantity exceeds the uninspected return balance.');const stock=s.stock.find(x=>x.id===r.stockId);must(stock,'Return inspection stock is missing.');
 const serials=Array.isArray(p.serials)?p.serials:String(p.serials||'').split(/[\n,]/).map(x=>x.trim()).filter(Boolean);
 if(s.operations.tracking[r.itemId]==='Serial'){const used=(r.dispositions||[]).flatMap(x=>x.serials);must(serials.length===q&&serials.every(x=>r.serials.includes(x)&&!used.includes(x)),'Select only uninspected serials from this customer return.');}
 if(p.disposition==='Restock'){
  const dest=s.locations.find(x=>x.id===p.locationId);must(dest?.type==='Storage','Restock into a storage location.');must(sameScope(locationScope(s,dest.id),locationScope(s,stock.locationId)),'Restock into the same warehouse and owner.');
  run('moveStock',{stockId:r.stockId,qty:q,locationId:dest.id,serials});
 }else{must(p.disposition==='Scrap','Choose restock or scrap.');run('scrapStock',{stockId:r.stockId,qty:q,serials,reason:r.reason});}
 const latest=business(s).returns.find(x=>x.id===r.id);latest.dispositions||=[];latest.dispositions.push({qty:q,disposition:p.disposition,serials,locationId:p.disposition==='Restock'?p.locationId:stock.locationId,time:ctx.time,actor:ctx.actor||'Local operator'});
 const t=dispositionTotals(latest);latest.status=t.pending?'Received':t.restocked===r.qty?'Restocked':t.scrapped===r.qty?'Scrapped':'Completed';
 return {type:'Return disposition recorded',reference:r.number,message:'Return disposition recorded',resultId:r.id};
}
export function recordCustomerReturn(s,current,command,p,ctx){
 if(!['business:receiveReturn','business:disposeReturn','billing:credit'].includes(command))return;const b=business(s),old=new Set(business(current).journals.map(x=>x.id)),j=b.journals.find(x=>!old.has(x.id)&&x.sourceCommand===command&&x.sourceId===p.id);
 if(command==='business:receiveReturn'){
  const r=b.returns.find(x=>x.id===p.id),sh=returnShipment(s,r);r.receivedAt=ctx.time;
  const line=j?.lines.find(x=>x.account==='Inventory asset');r.receiptPosting={journalId:j?.id||'',value:(line?.debit||0)-(line?.credit||0),unitCost:r.costRestore?.unitCost??s.operations.shipping[sh.id].costSnapshot[r.itemId],shipmentId:sh.id};
  if(j){j.reference=r.number+' — customer return / 客户退货 / 客戶退貨';const ship=b.journals.find(x=>x.sourceCommand==='shipShipment'&&x.sourceId===sh.id);j.dependencies=ship?['journal:'+ship.id]:[];}
 }
 if(command==='business:disposeReturn'){
  const r=b.returns.find(x=>x.id===p.id),d=r.dispositions.at(-1);d.journalId=j?.id||'';const asset=j?.lines.find(x=>x.account==='Inventory asset');d.value=(asset?.credit||0)-(asset?.debit||0);
  if(j){j.reference=r.number+' — inspection scrap / 检验报废 / 檢驗報廢';j.dependencies=r.receiptPosting?.journalId?['journal:'+r.receiptPosting.journalId]:[];}
 }
 if(command==='billing:credit'){
  const d=s.billing.documents.at(-1),r=b.returns.find(x=>x.id===d.returnId);if(r?.kind==='Customer'&&r.receiptPosting)d.returnAccounting={returnId:r.id,journalId:r.receiptPosting.journalId,receivedValue:r.receiptPosting.value,unitCost:r.receiptPosting.unitCost};
 }
}
export function validateCustomerReturns(s){
 const b=business(s);for(const r of b.returns){
  if(r.dispositions){must(r.kind==='Customer'&&Array.isArray(r.dispositions)&&r.dispositions.length<=r.qty,'Invalid customer inspection history.');const t=dispositionTotals(r),count=t.restocked+t.scrapped;must(count<=r.qty,'Return inspection exceeds the received quantity.');must(r.status===(count<r.qty?'Received':t.restocked===r.qty?'Restocked':t.scrapped===r.qty?'Scrapped':'Completed'),'Return disposition status does not match its quantities.');const all=[];for(const x of r.dispositions){must(Number.isSafeInteger(x.qty)&&x.qty>0&&['Restock','Scrap'].includes(x.disposition)&&Number.isFinite(Date.parse(x.time))&&Array.isArray(x.serials),'Invalid return inspection.');if(s.operations.tracking[r.itemId]==='Serial'){must(x.serials.length===x.qty&&x.serials.every(sn=>r.serials.includes(sn)&&!all.includes(sn)),'Return serial disposed more than once.');all.push(...x.serials);}if(x.journalId){const j=b.journals.find(j=>j.id===x.journalId);must(j?.sourceCommand==='business:disposeReturn'&&j.sourceId===r.id,'Invalid scrap journal source.');}}
  }
  if(r.receiptPosting){const p=r.receiptPosting;must(r.kind==='Customer'&&['Received','Restocked','Scrapped','Completed'].includes(r.status)&&Number.isSafeInteger(p.value)&&p.value>=0&&Number.isFinite(p.unitCost)&&p.unitCost>=0&&Number.isFinite(Date.parse(r.receivedAt)),'Invalid customer return cost snapshot.');const sh=s.shipments.find(x=>x.id===p.shipmentId);must(sh?.orderId===r.sourceId,'Customer return shipment changed.');if(p.journalId){const j=b.journals.find(x=>x.id===p.journalId),line=j?.lines.find(x=>x.account==='Inventory asset');must(j?.sourceCommand==='business:receiveReturn'&&j.sourceId===r.id&&(line?.debit||0)-(line?.credit||0)===p.value,'Customer return value journal changed.');}}
 }
 for(const d of s.billing?.documents||[])if(d.returnAccounting){const r=b.returns.find(x=>x.id===d.returnAccounting.returnId);must(d.kind==='Credit'&&d.returnId===r?.id&&r.kind==='Customer'&&r.sourceId===d.orderId&&d.date>=businessDay({organization:{timezone:d.dateTimezone}},r.receivedAt)&&JSON.stringify(d.returnAccounting)===JSON.stringify({returnId:r.id,journalId:r.receiptPosting.journalId,receivedValue:r.receiptPosting.value,unitCost:r.receiptPosting.unitCost}),'Invalid customer credit cost linkage.');}
}
