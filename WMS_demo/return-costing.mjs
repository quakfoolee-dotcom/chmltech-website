import {returnShipment,deliveryLines} from './fulfillment.mjs';
import {businessDay} from './company-date.mjs';
import {isFIFO} from './fifo.mjs';
import {fifoSupplierCreditBookValue,validateFIFOSupplierReturn} from './fifo-supplier.mjs';
// Reviewed return accounting. Inventory uses its saved FIFO ranges or average;
// supplier credits retain their original bill's net price and frozen FX rate.
import {business,locationScope,inventoryValue} from './business.mjs';
import {billing,receiptLine} from './billing.mjs';
import {validUnicode,charLength} from './unicode.mjs';
import {csvText} from './exchange.mjs';
const must=(v,m)=>{if(!v)throw Error(m);};
const get=(rows,id)=>{const r=rows.find(x=>x.id===id);must(r,'Return accounting record not found.');return r;};
const cents=v=>Math.round((v+Number.EPSILON)*100);
const reason=v=>{const t=String(v||'').trim();must(t&&validUnicode(t)&&charLength(t)<=240,'Enter a valid review reason (up to 240 characters).');return t;};
const units=(s,item)=>s.stock.filter(r=>r.itemId===item&&locationScope(s,r.locationId).ownerId==='owner-self').reduce((n,r)=>n+r.qty,0);
const poolFor=(s,po,receipt,item)=>s.costing?.pools.find(x=>x.purchaseId===po&&x.receiptId===receipt&&x.itemId===item);
function post(s,ctx,reference,command,sourceId,amounts,dependencies=[]){
 const lines=Object.entries(amounts).filter(([,v])=>v).map(([account,v])=>({account,debit:Math.max(0,v),credit:Math.max(0,-v)}));
 must(lines.every(l=>Number.isSafeInteger(l.debit)&&Number.isSafeInteger(l.credit))&&lines.reduce((n,l)=>n+l.debit-l.credit,0)===0,'Return journal must balance.');
 if(!lines.length)return '';const b=s.business,id=`journal-${++b.sequence}`;b.journals.push({id,time:ctx.time,reference,sourceCommand:command,sourceId,currency:b.homeCurrency,status:'Ready for review',dependencies:[...new Set(dependencies)],lines});return id;
}
export function beforeReturns(s,command,p,ctx){
 if(ctx.internal||ctx.nested||!s.costing)return;const c=s.costing,b=business(s);
 if(command==='business:return'&&p.kind==='Supplier'&&c.purchases.includes(p.sourceId)){
  const pool=poolFor(s,p.sourceId,p.receiptId,p.itemId);must(pool,'Choose the original controlled receipt ID for this product.');must(!pool.blocked,pool.blocked);
  const previous=b.returns.filter(r=>r.kind==='Supplier'&&r.sourceId===p.sourceId&&r.receiptId===p.receiptId&&r.itemId===p.itemId&&r.status!=='Cancelled').reduce((n,r)=>n+r.qty,0);
  must(Number(p.qty)+previous<=pool.qty,'Return exceeds the original receipt quantity.');
 }
 if(command==='business:sendReturn'){
  const r=get(b.returns,p.id);if(c.purchases.includes(r.sourceId)){const pool=poolFor(s,r.sourceId,r.receiptId,r.itemId);must(pool&&!pool.blocked,'Review the original controlled receipt before sending this return.');must(s.operations.costs[r.itemId]>0,'Known positive inventory cost is required for a controlled return.');}
 }
 if(command==='billing:credit'){
  const parent=get(billing(s).documents,p.parentId);if(c.purchases.includes(parent.sourceId)){
   must(c.matches.some(m=>m.billId===parent.id),'Match the original supplier bill first.');const r=b.returns.find(x=>x.id===p.returnId);
   must(r,'Complete and link the physical supplier return before crediting controlled goods.');
   must(r.kind==='Supplier'&&r.status==='Sent'&&r.sourceId===parent.sourceId&&r.costPosting,'Complete the physical supplier return before crediting controlled goods.');
   must((p.date||businessDay(s,ctx.time))>=businessDay(s,r.sentAt),'Supplier credit date cannot precede the physical return.');
   for(const l of p.lines||[]){const orig=get(parent.lines.map(x=>({...x,id:x.sourceLineId})),l.sourceLineId),key=receiptLine(parent,orig);must(orig.itemId===r.itemId&&key.receiptId===r.receiptId,'Credit only the returned product from its original receipt.');}
  }
 }
 if(['billing:void','billing:edit'].includes(command)&&c.returnCredits?.some(x=>x.creditId===p.id))throw Error('A posted return credit is locked. Correct it through a separate reviewed accounting adjustment.');
 if(command==='business:receiveReturn'){
  const r=get(b.returns,p.id),sh=returnShipment(s,r);if(!sh||isFIFO(s,r.itemId))return;
  const involved=c.pools.filter(x=>x.orders.includes(r.sourceId));if(!involved.length)return;
  let cost=s.operations.shipping[sh.id]?.costSnapshot[r.itemId],exposures=[];
  must(Number.isFinite(cost),'Original shipment needs a known cost.');
  const shipped=deliveryLines(s,sh).find(l=>l.itemId===r.itemId).qty;
  for(const pool of involved.filter(x=>x.itemId===r.itemId)){
   must(!pool.blocked,pool.blocked);const exposure=pool.shipments?.find(x=>x.shipmentId===sh.id);
   must(exposure||!pool.adjusted,'Older shipments with late costs require manual cost review.');if(!exposure)continue;
   const fraction=exposure.qty*r.qty/shipped;must(fraction+(exposure.returned||0)<=exposure.qty+.000001,'Cost exposure was already returned.');
   const late=[...c.matches,...c.allocations].filter(a=>!exposure.excluded.includes(a.billId)).flatMap(a=>a.rows).filter(x=>x.poolId===pool.id).reduce((n,x)=>n+x.amount,0);
   cost+=late*exposure.qty/pool.qty/shipped/100;exposures.push({poolId:pool.id,shipmentId:sh.id,qty:fraction});
  }
  r.costRestore={unitCost:Number(cost.toFixed(4)),exposures};
 }
}
export function afterReturns(s,current,command,p,ctx){
 if(ctx.internal||ctx.nested||!s.costing)return;const c=s.costing,b=business(s);
 if(command==='billing:credit'){
  const d=billing(s).documents.at(-1),parent=get(billing(s).documents,d.parentId);
  if(c.purchases.includes(parent.sourceId))d.costing={posting:parent.costing.posting,rate:parent.costing.rate,returnId:d.returnId};
 }
 if(command==='business:sendReturn'){
  const r=get(b.returns,p.id);if(c.purchases.includes(r.sourceId)){
   const value=cents(inventoryValue(current))-cents(inventoryValue(s)),pool=poolFor(s,r.sourceId,r.receiptId,r.itemId);
   must(value>0,'Controlled return must remove positive owned inventory value.');
   // Replace the legacy local-only journal; export the physical value once.
   b.journals=b.journals.filter(j=>!(j.sourceCommand===command&&j.sourceId===r.id&&j.time===ctx.time));
   const dependencies=[...c.pools.filter(x=>x.itemId===r.itemId).map(x=>x.journalId),...[...c.matches,...c.allocations].filter(a=>a.rows.some(x=>x.itemId===r.itemId)).map(x=>x.journalId)].filter(Boolean).map(id=>'journal:'+id);
   if(isFIFO(s,r.itemId))must(r.fifoSupplier?.value===value,'FIFO supplier return inventory delta does not match its frozen receipt ranges.');
   r.costPosting={poolId:pool.id,value,unitCost:isFIFO(s,r.itemId)?Number((value/100/r.qty).toFixed(4)):current.operations.costs[r.itemId],basis:isFIFO(s,r.itemId)?'FIFO dispatch ranges; original receipt retained for credit matching':'Moving weighted average book value',journalId:post(s,ctx,r.number+' — supplier return / 供应商退货 / 供應商退貨','cost:supplierReturn',r.id,{'Supplier return clearing':value,'Inventory asset':-value},dependencies)};
  }
 }
 if(command==='billing:issue'){
  const d=get(billing(s).documents,p.id);if(d.kind==='Credit'&&d.costing?.returnId){
   c.returnCredits||=[];must(!c.returnCredits.some(x=>x.creditId===d.id),'Return credit is already posted.');
   const r=get(b.returns,d.returnId),qty=d.lines.reduce((n,l)=>n+l.qty,0),previous=c.returnCredits.filter(x=>x.returnId===r.id),used=previous.reduce((n,x)=>n+x.qty,0),bookUsed=previous.reduce((n,x)=>n+x.bookValue,0);
   must(used+qty<=r.qty,'Credits exceed physically returned units.');
   const bookValue=r.fifoSupplier?fifoSupplierCreditBookValue(s,r,used,qty):used+qty===r.qty?r.costPosting.value-bookUsed:Math.round(r.costPosting.value*qty/r.qty),creditNet=Math.round(d.net*d.costing.rate),variance=bookValue-creditNet;
   const journalId=post(s,ctx,d.number+' — return credit settlement / 退货贷项核销 / 退貨貸項核銷','cost:returnCredit',d.id,{'Goods received not invoiced':creditNet,'Supplier return clearing':-bookValue,'Inventory adjustments':variance},['document:'+d.id,'journal:'+r.costPosting.journalId]);
   c.returnCredits.push({creditId:d.id,returnId:r.id,qty,bookValue,creditNet,variance,journalId,time:ctx.time,reason:d.note});
  }
 }
 if(command==='business:receiveReturn'){
  const r=get(b.returns,p.id);for(const x of r.costRestore?.exposures||[]){const pool=get(c.pools,x.poolId),ship=pool.shipments.find(sh=>sh.shipmentId===x.shipmentId);must(ship,'Original shipment exposure is missing.');pool.remaining+=x.qty;pool.sold-=x.qty;ship.returned=(ship.returned||0)+x.qty;}if(r.receiptPosting?.journalId){const j=get(b.journals,r.receiptPosting.journalId);j.dependencies=[...new Set([...(j.dependencies||[]),...[...c.matches,...c.allocations].filter(a=>a.rows.some(x=>x.itemId===r.itemId)).map(a=>a.journalId).filter(Boolean).map(id=>'journal:'+id)])];}
 }
}
export function receiptMatching(s){
 const c=s.costing||{purchases:[],pools:[],matches:[]};return c.pools.map(pool=>{
  const po=get(s.operations.purchases,pool.purchaseId),line=po.lines?.find(x=>x.id===pool.lineId)||po;
  const docs=billing(s).documents.filter(d=>d.kind==='Bill'&&d.sourceId===po.id&&d.status!=='Voided');
  const lines=docs.flatMap(d=>d.lines.filter(l=>{const k=receiptLine(d,l);return k.receiptId===pool.receiptId&&k.lineId===pool.lineId;}).map(l=>({d,l})));
  const billed=lines.filter(x=>x.d.status==='Issued').reduce((n,x)=>n+x.l.qty,0),reserved=lines.filter(x=>x.d.status==='Draft').reduce((n,x)=>n+x.l.qty,0),matched=c.matches.flatMap(x=>x.lines).filter(x=>x.poolId===pool.id).reduce((n,l)=>n+l.qty,0);
  const returns=business(s).returns.filter(r=>r.sourceId===po.id&&r.receiptId===pool.receiptId&&r.itemId===pool.itemId&&r.status==='Sent'),returned=returns.reduce((n,r)=>n+r.qty,0),credited=(c.returnCredits||[]).filter(x=>returns.some(r=>r.id===x.returnId)).reduce((n,x)=>n+x.qty,0);
  return {...pool,po:po.number,supplier:po.supplier,ordered:line.qty,receivedOnPO:line.received,billed,reserved,matched,unbilled:pool.qty-billed-reserved,returned,credited,status:billed>pool.qty?'Overbilled':matched<pool.qty?'Awaiting bill / match':returned>credited?'Awaiting supplier credit':'Matched'};
 });
}
export function matchingCSV(s){return csvText([['PO','Supplier','Receipt','SKU','Product','Ordered','PO received','Receipt units','Billed units','Draft units','Unbilled','Returned','Credited','Status','Review history'],...receiptMatching(s).map(r=>[r.po,r.supplier,r.receiptId,s.items.find(i=>i.id===r.itemId)?.sku,s.items.find(i=>i.id===r.itemId)?.name,r.ordered,r.receivedOnPO,r.qty,r.billed,r.reserved,r.unbilled,r.returned,r.credited,r.status,(s.costing.discrepancies||[]).filter(x=>x.poolId===r.id).map(x=>`${x.kind}: ${x.qty} / ${x.reason}`).join(' | ')])]);}
export function returnCostCommand(s,command,p,ctx){
 if(!['cost:inspect','cost:discrepancy'].includes(command))return null;const c=s.costing;must(c,'Enable receipt accounting first.');const pool=get(c.pools,p.poolId),q=Number(p.qty),why=reason(p.reason);
 must(Number.isSafeInteger(q)&&q>0&&q<=pool.qty,'Use a whole quantity within the original receipt.');c.discrepancies||=[];
 if(command==='cost:inspect'){
  const stock=get(s.stock,p.stockId),dest=get(s.locations,p.locationId),scope=locationScope(s,stock.locationId),po=get(s.operations.purchases,pool.purchaseId);
  must(stock.itemId===pool.itemId&&scope.ownerId==='owner-self'&&scope.warehouseId===(po.scope?.warehouseId||'wh-main'),'Choose stock from the receipt product and warehouse.');must(dest.type==='Hold','Choose quality hold for damaged goods.');must(locationScope(s,dest.id).warehouseId===scope.warehouseId&&locationScope(s,dest.id).ownerId===scope.ownerId,'Quality hold must match the receipt warehouse and owner.');must(stock.locationId!==dest.id,'Goods are already in this quality hold.');
  const result=ctx.dispatch(s,'moveStock',{stockId:stock.id,qty:q,locationId:dest.id,serials:p.serials||[]},{now:ctx.time,internal:true});Object.assign(s,result.state);
  s.costing.discrepancies.push({id:'discrepancy-'+(c.discrepancies.length+1),poolId:pool.id,kind:'Damaged / quality hold',qty:q,reason:why,time:ctx.time,actor:ctx.actor||'Local operator'});
 }else{
  must(['Short delivery','Price dispute','Resolved'].includes(p.kind),'Choose a discrepancy type.');c.discrepancies.push({id:'discrepancy-'+(c.discrepancies.length+1),poolId:pool.id,kind:p.kind,qty:q,reason:why,time:ctx.time,actor:ctx.actor||'Local operator'});
 }
 return {type:'Receipt discrepancy recorded',message:'Receipt discrepancy recorded',reference:pool.receiptId,resultId:pool.id};
}
export function validateReturns(s){
 const c=s.costing;if(!c)return;
 for(const d of billing(s).documents.filter(d=>d.costing?.returnId)){
  const parent=get(billing(s).documents,d.parentId),r=get(business(s).returns,d.returnId);
  must(d.kind==='Credit'&&d.costing.returnId===r.id&&d.costing.rate===parent.costing?.rate&&d.costing.posting===parent.costing?.posting&&r.costPosting&&d.date>=r.sentAt.slice(0,10),'Invalid controlled return credit.');
  for(const l of d.lines)must(l.itemId===r.itemId&&receiptLine(d,l).receiptId===r.receiptId,'Controlled credit changed its original receipt.');
 }
 for(const pool of c.pools){
  const shipments=pool.shipments||[];must(new Set(shipments.map(x=>x.shipmentId)).size===shipments.length,'Duplicate shipment cost exposure.');
  for(const x of shipments){const sh=get(s.shipments,x.shipmentId);must(pool.orders.includes(sh.orderId)&&Number.isFinite(x.qty)&&x.qty>=0&&Number.isFinite(x.returned)&&x.returned>=0&&x.returned<=x.qty+.000001&&Array.isArray(x.excluded),'Invalid shipment cost exposure.');}
 }
 for(const r of business(s).returns.filter(x=>x.costPosting)){
  const pool=get(c.pools,r.costPosting.poolId);must(pool.purchaseId===r.sourceId&&pool.receiptId===r.receiptId&&pool.itemId===r.itemId&&r.status==='Sent','Return cost source changed.');
  const j=get(business(s).journals,r.costPosting.journalId);must(j.sourceCommand==='cost:supplierReturn'&&j.sourceId===r.id&&Number.isSafeInteger(r.costPosting.value)&&r.costPosting.value>0&&j.lines.find(l=>l.account==='Inventory asset')?.credit===r.costPosting.value,'Invalid return book value.');
  validateFIFOSupplierReturn(s,r);
 }
 const credits=c.returnCredits||[];must(new Set(credits.map(x=>x.creditId)).size===credits.length,'Duplicate return credit posting.');
 for(const x of credits){const d=get(billing(s).documents,x.creditId),r=get(business(s).returns,x.returnId),j=get(business(s).journals,x.journalId);must(d.kind==='Credit'&&d.status==='Issued'&&d.returnId===r.id&&d.costing?.returnId===r.id&&j.sourceId===d.id&&j.sourceCommand==='cost:returnCredit','Return credit source changed.');must([x.qty,x.bookValue,x.creditNet,x.variance].every(Number.isSafeInteger)&&x.qty===d.lines.reduce((n,l)=>n+l.qty,0)&&x.qty>0&&x.bookValue>=0&&x.creditNet===Math.round(d.net*d.costing.rate)&&x.variance===x.bookValue-x.creditNet,'Invalid return credit settlement.');const signed=account=>{const l=j.lines.find(l=>l.account===account);return (l?.debit||0)-(l?.credit||0);};must(signed('Goods received not invoiced')===x.creditNet&&signed('Supplier return clearing')===-x.bookValue&&signed('Inventory adjustments')===x.variance,'Return settlement journal changed.');}
 for(const r of business(s).returns.filter(x=>x.costPosting)){const linked=credits.filter(x=>x.returnId===r.id);must(linked.reduce((n,x)=>n+x.qty,0)<=r.qty&&linked.reduce((n,x)=>n+x.bookValue,0)<=r.costPosting.value,'Return credited more than once.');let used=0,bookUsed=0;for(const x of linked){const expected=r.fifoSupplier?fifoSupplierCreditBookValue(s,r,used,x.qty):used+x.qty===r.qty?r.costPosting.value-bookUsed:Math.round(r.costPosting.value*x.qty/r.qty);used+=x.qty;must(x.bookValue===expected,'Partial return credit book value changed.');bookUsed+=x.bookValue;}}
 for(const x of c.discrepancies||[]){get(c.pools,x.poolId);reason(x.reason);must(Number.isSafeInteger(x.qty)&&x.qty>0&&Number.isFinite(Date.parse(x.time)),'Invalid receipt review history.');}
}

