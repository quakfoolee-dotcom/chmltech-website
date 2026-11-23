import {businessDay} from './company-date.mjs?demo=45f52980507d3a1b';
import {isFIFO,fifoCommand,applyFIFOAmount} from './fifo.mjs?demo=45f52980507d3a1b';
// Prospective receipt accounting and moving-average landed costs, in home-currency cents.
import {business,setupBusiness,locationScope,inventoryValue} from './business.mjs?demo=45f52980507d3a1b';
import {purchaseLines,suppliers} from './purchasing.mjs?demo=45f52980507d3a1b';
import {beforeReturns,afterReturns,returnCostCommand,validateReturns} from './return-costing.mjs?demo=45f52980507d3a1b';
import {billing,billingCommand,billingSource,receiptLine} from './billing.mjs?demo=45f52980507d3a1b';
const must=(v,m)=>{if(!v)throw Error(m);};
const get=(rows,id)=>{const r=rows.find(x=>x.id===id);must(r,'Costing record not found.');return r;};
const cents=v=>Math.round((v+Number.EPSILON)*100);
const text=v=>{const t=String(v||'').trim();must(t&&t.length<=240,'Enter a reference or review reason (up to 240 characters).');return t;};
const fresh=()=>({version:1,purchases:[],pools:[],matches:[],charges:[],allocations:[]});
export const costing=s=>s.costing||fresh();
const setup=s=>s.costing||(s.costing=fresh());
export const ownUnits=(s,id)=>s.stock.filter(r=>r.itemId===id&&locationScope(s,r.locationId).ownerId==='owner-self').reduce((n,r)=>n+r.qty,0);
export function valuation(s){return {currency:business(s).homeCurrency,value:cents(inventoryValue(s)),rows:s.items.map(i=>({itemId:i.id,sku:i.sku,name:i.name,qty:ownUnits(s,i.id),cost:s.operations?.costs[i.id]??null,sample:s.costing?.sampleCosts?.includes(i.id)||false})),missing:s.items.filter(i=>ownUnits(s,i.id)>0&&s.operations?.costs[i.id]===undefined).map(i=>i.sku)};}
function journal(s,ctx,reference,command,sourceId,amounts,dependencies=[]){
 const lines=Object.entries(amounts).filter(([,v])=>v).map(([account,v])=>({account,debit:Math.max(0,v),credit:Math.max(0,-v)}));
 if(!lines.length)return '';must(lines.reduce((n,l)=>n+l.debit-l.credit,0)===0,'Cost journal must balance.');
 const b=setupBusiness(s),id=`journal-${++b.sequence}`;b.journals.push({id,time:ctx.time,reference,sourceCommand:command,sourceId,currency:b.homeCurrency,status:'Ready for review',dependencies,lines});return id;
}
export function matchPreview(s,id){
 const d=get(billing(s).documents,id),po=get(s.operations.purchases,d.sourceId),c=costing(s);
 must(d.kind==='Bill'&&c.purchases.includes(po.id),'Enable receipt accounting before receiving this PO.');
 const rows=d.lines.map(l=>{const key=receiptLine(d,l),pool=c.pools.find(x=>x.purchaseId===po.id&&x.receiptId===key.receiptId&&x.lineId===key.lineId);must(pool,'Receipt cost record is missing.');must(!pool.blocked,pool.blocked);const prior=c.matches.flatMap(x=>x.lines).filter(x=>x.poolId===pool.id),used=prior.reduce((n,x)=>n+x.qty,0),expectedUsed=prior.reduce((n,x)=>n+x.expected,0);must(used+l.qty<=pool.qty,'Matched quantity exceeds the receipt.');const expected=used+l.qty===pool.qty?pool.base-expectedUsed:Math.round(pool.base*l.qty/pool.qty),actual=Math.round(l.net*(po.exchangeRate||1));return {poolId:pool.id,itemId:l.itemId,qty:l.qty,expected,actual,variance:actual-expected};});
 return {billId:d.id,number:d.number,rows,expected:rows.reduce((n,x)=>n+x.expected,0),actual:rows.reduce((n,x)=>n+x.actual,0),variance:rows.reduce((n,x)=>n+x.variance,0),outsideTolerance:rows.some(l=>Math.abs(l.variance)>Math.max(1,Math.abs(l.expected)*.02))};
}
function applyAmounts(s,ctx,parts,offset,reference,command,sourceId,dependencies){
 const before=cents(inventoryValue(s)),amounts={},rows=[];let asset=0,total=0;
 const add=(key,v)=>amounts[key]=(amounts[key]||0)+v;
 for(const {poolId,amount} of parts){must(Number.isSafeInteger(amount),'Invalid allocated amount.');const pool=get(costing(s).pools,poolId);must(!pool.blocked,pool.blocked);if(isFIFO(s,pool.itemId)){const exact=applyFIFOAmount(s,ctx,pool,amount,command,sourceId);asset+=exact.inventory;total+=amount;add('Cost of goods sold',exact.cogs);add('Inventory adjustments',exact.adjustments);pool.adjusted=true;rows.push({poolId,itemId:pool.itemId,amount,...exact});continue;}const retained=Math.round(amount*pool.remaining/pool.qty),sold=Math.round(amount*pool.sold/pool.qty),other=amount-retained-sold,units=ownUnits(s,pool.itemId);must(s.operations.costs[pool.itemId]!==undefined,'Opening cost is required before allocation.');must(!retained||units>0,'No stock remains for this inventory allocation.');if(retained){const cost=Number((s.operations.costs[pool.itemId]+retained/100/units).toFixed(4));must(cost>=0,'Adjustment would create a negative inventory cost.');s.operations.costs[pool.itemId]=cost;}asset+=retained;total+=amount;add('Cost of goods sold',sold);add('Inventory adjustments',other);pool.adjusted=true;rows.push({poolId,itemId:pool.itemId,amount,inventory:retained,cogs:sold,adjustments:other});}
 const actual=cents(inventoryValue(s))-before;add('Inventory asset',actual);add('Inventory rounding',asset-actual);add(offset,-total);
 return {rows,journalId:journal(s,ctx,reference,command,sourceId,amounts,dependencies),amount:total};
}
export function beforeCosting(s,command,p,ctx){
 const c=costing(s);if(ctx.nested||ctx.internal)return;beforeReturns(s,command,p,ctx);
 if(command==='receivePurchase'||(command==='business:scan'&&p.mode==='Receive')){const id=p.id||p.purchaseId;if(c.purchases.includes(id))for(const l of purchaseLines(get(s.operations.purchases,id)))must(!ownUnits(s,l.itemId)||s.operations.costs[l.itemId]!==undefined,'Set opening costs before receiving controlled stock.');}
 if(command==='business:reconcile'){const r=business(s).receipts.find(x=>x.id===p.id);must(!c.purchases.includes(r?.purchaseId),'Use Purchase cost reconciliation for this receipt.');}
 if(['billing:void','billing:edit'].includes(command))must(!c.matches.some(x=>x.billId===p.id)&&!c.allocations.some(x=>x.billId===p.id),'A reconciled bill is locked. Correct it through a reviewed accounting adjustment.');
 if(command==='billing:credit'){const d=billing(s).documents.find(x=>x.id===p.parentId);must(!c.charges.some(x=>x.id===d?.sourceId),'Credits on landed charges require manual accounting review in this release.');}
 if(command==='setCost')must(!c.pools.some(x=>x.itemId===(p.id||p.itemId)),'Use cost reconciliation for products with controlled receipt costs.');
 if(command==='voidShipment'){
  const orderId=command==='voidShipment'?s.shipments.find(x=>x.id===p.id)?.orderId:business(s).returns.find(x=>x.id===p.id)?.sourceId;
  must(!c.pools.some(x=>!isFIFO(s,x.itemId)&&x.adjusted&&x.orders.includes(orderId)),'This shipment has later cost allocations. Its return or reversal needs manual cost review first.');
 }
}
export function afterCosting(s,current,command,p,ctx){
 if(ctx.nested||ctx.internal)return;const c=s.costing;if(!c)return;
 if(command==='setCost'&&c.sampleCosts)c.sampleCosts=c.sampleCosts.filter(id=>id!==p.id);
 // Track exposure under global moving weighted average, not by physical lot.
 for(const pool of c.pools){if(isFIFO(s,pool.itemId))continue;const before=ownUnits(current,pool.itemId),after=ownUnits(s,pool.itemId);if(after<before&&before){const loss=pool.remaining*(before-after)/before;pool.remaining-=loss;
  if(command==='shipShipment'){pool.sold+=loss;const sh=s.shipments.find(x=>x.id===p.id);if(sh&&!pool.orders.includes(sh.orderId))pool.orders.push(sh.orderId);if(sh){pool.shipments||=[];pool.shipments.push({shipmentId:sh.id,qty:loss,returned:0,excluded:[...c.matches,...c.allocations].map(x=>x.billId)});}}
  else if(['scrapStock','countStock','count:post','business:disposeReturn','business:sendReturn'].includes(command)||(command==='business:scan'&&p.mode==='Count'))pool.other+=loss;
  else pool.blocked='Stock was consumed by production or supplier returns; manual cost review is required.';
 }
 if(after>before&&(command==='voidShipment'||(command==='business:receiveReturn'&&!business(s).returns.find(r=>r.id===p.id)?.costRestore?.exposures?.length)))pool.blocked='Returned stock requires manual cost review before further allocations.';
 }
 for(const po of s.operations?.purchases||[]){if(!c.purchases.includes(po.id))continue;for(const receipt of po.receipts||[]){if(c.pools.some(x=>x.purchaseId===po.id&&x.receiptId===receipt.id))continue;
  const pools=receipt.lines.map(l=>{const base=cents(purchaseLines(po).find(x=>x.id===l.lineId).unitCost*l.qty);return {id:`${po.id}/${receipt.id}/${l.lineId}`,purchaseId:po.id,receiptId:receipt.id,lineId:l.lineId,itemId:l.itemId,qty:l.qty,base,remaining:l.qty,sold:0,other:0,orders:[],adjusted:false};});
  const total=pools.reduce((n,x)=>n+x.base,0),actual=cents(inventoryValue(s))-cents(inventoryValue(current));const j=journal(s,ctx,`${po.number} / ${receipt.id} — received, not billed`,'cost:receipt',`${po.id}/${receipt.id}`,{'Inventory asset':actual,'Inventory rounding':total-actual,'Goods received not invoiced':-total});
  pools.forEach(x=>x.journalId=j);c.pools.push(...pools);
 }}
 afterReturns(s,current,command,p,ctx);
}
export function costCommand(s,command,p,ctx){
 if(!command.startsWith('cost:'))return null;const c=setup(s);setupBusiness(s);const handled=fifoCommand(s,command,p,ctx)||returnCostCommand(s,command,p,ctx);if(handled)return handled;const event=(type,id='')=>({type,message:type,reference:id,resultId:id});
 switch(command){
 case 'cost:enablePurchase':{const po=get(s.operations.purchases,p.id);must(!(po.receipts||[]).length&&!c.purchases.includes(po.id)&&po.status==='Open','Enable once, on an open PO before the first receipt.');must(po.kind==='Warehouse'&&(!po.scope||po.scope.ownerId==='owner-self'),'Use an owned warehouse purchase.');must(purchaseLines(po).every(l=>l.unitCost>0&&(ownUnits(s,l.itemId)===0||s.operations.costs[l.itemId]!==undefined)),'Set opening costs and positive PO prices first.');c.purchases.push(po.id);return event('Receipt accounting enabled',po.id);}
 case 'cost:sampleCosts':{const values=[12,8,.25,6,3,9];c.sampleCosts||=[];for(let n=0;n<6;n++){const id=`item-${n+1}`;if(s.items.some(i=>i.id===id)&&s.operations.costs[id]===undefined){s.operations.costs[id]=values[n];c.sampleCosts.push(id);}}return event('Illustrative opening costs recorded — sample values only');}
 case 'cost:matchBill':{const d=get(billing(s).documents,p.id);must(d.status==='Issued'&&!c.matches.some(x=>x.billId===d.id),'Match each issued bill once.');const preview=matchPreview(s,d.id);must(!preview.outsideTolerance||p.approved===true,'Price variance exceeds 2%. Approve it with a reason.');const reason=text(p.reason);const deps=[`document:${d.id}`,...new Set(preview.rows.map(r=>'journal:'+get(c.pools,r.poolId).journalId).filter(x=>x!=='journal:'))];const result=applyAmounts(s,ctx,preview.rows.map(r=>({poolId:r.poolId,amount:r.variance})),'Goods received not invoiced',`${d.number} — purchase price variance`,'cost:variance',d.id,deps);d.costing={posting:'Goods received not invoiced',rate:get(s.operations.purchases,d.sourceId).exchangeRate||1};c.matches.push({...preview,lines:preview.rows,time:ctx.time,reason,...result});return event('PO, receipt and supplier bill reconciled',d.id);}
 case 'cost:charge':{const supplier=get(suppliers(s),p.supplierId),amount=Number(p.amount),rate=Number(p.rate||1),currency=p.currency||business(s).homeCurrency;must(Number.isFinite(amount)&&amount>0&&amount<=1e7&&Math.abs(amount*100-Math.round(amount*100))<.00001,'Enter a positive charge with at most two decimals.');must(Number.isFinite(rate)&&rate>0&&rate<=1e5&&(currency!==business(s).homeCurrency||rate===1),'Enter a valid fixed home-currency rate.');must(['Freight','Duty','Brokerage'].includes(p.kind),'Choose freight, duty or brokerage.');const id=`cost-charge-${c.charges.length+1}`,name=text(p.description||p.kind);c.charges.push({id,supplierId:supplier.id,party:{name:supplier.name,address:supplier.address||'',contact:supplier.email||'',taxId:''},currency,rate,amount:cents(amount),name,kind:p.kind,date:businessDay(s,ctx.time)});
  const result=billingCommand(s,'billing:createBill',{sourceId:id,reference:text(p.reference),note:p.note||'',lines:[{sourceLineId:id,qty:1,unitPrice:amount.toFixed(2),taxPercent:0,taxName:'No tax'}]},ctx);return event('Landed charge bill drafted',result.resultId);}
 case 'cost:allocateCharge':{const d=get(billing(s).documents,p.id),charge=get(c.charges,d.sourceId);must(d.status==='Issued'&&!c.allocations.some(x=>x.billId===d.id),'Allocate each issued landed-charge bill once.');must(d.lines.length===1&&d.net>0,'Charge needs one positive net amount.');must(['Quantity','Value'].includes(p.basis),'Choose Quantity or Value.');must(Array.isArray(p.receipts)&&p.receipts.length>0&&new Set(p.receipts).size===p.receipts.length,'Select distinct receipts.');const pools=c.pools.filter(x=>p.receipts.includes(`${x.purchaseId}/${x.receiptId}`));must(new Set(pools.map(x=>`${x.purchaseId}/${x.receiptId}`)).size===p.receipts.length,'Select controlled receipt records.');const weights=pools.map(x=>p.basis==='Value'?x.base:x.qty),total=weights.reduce((a,b)=>a+b,0),amount=Math.round(d.net*charge.rate);must(total>0,'No allocation basis.');let used=0;const parts=pools.map((pool,i)=>{const v=i===pools.length-1?amount-used:Math.floor(amount*weights[i]/total);used+=v;return {poolId:pool.id,amount:v};});const result=applyAmounts(s,ctx,parts,'Landed cost clearing',`${d.number} — ${charge.name}`,'cost:landed',d.id,[`document:${d.id}`,...new Set(pools.map(x=>'journal:'+x.journalId).filter(x=>x!=='journal:'))]);d.costing={posting:'Landed cost clearing',rate:charge.rate};c.allocations.push({billId:d.id,basis:p.basis,receipts:p.receipts,time:ctx.time,reason:text(p.reason),...result});return event('Landed costs allocated to inventory and sold goods',d.id);}
 default:throw Error('Unknown cost action.');
 }
}
export function validateCosting(s){
 if(!s.costing)return;const c=s.costing,docs=billing(s).documents;
 must(c.version===1&&new Set(c.purchases).size===c.purchases.length,'Invalid cost ledger.');
 for(const id of c.purchases)get(s.operations.purchases,id);
 must(new Set(c.pools.map(x=>x.id)).size===c.pools.length,'Duplicate receipt pool.');
 for(const x of c.pools){
  const po=get(s.operations.purchases,x.purchaseId),receipt=get(po.receipts||[],x.receiptId),line=receipt.lines.find(l=>l.lineId===x.lineId);
  must(c.purchases.includes(po.id)&&line&&line.itemId===x.itemId&&line.qty===x.qty&&x.id===`${po.id}/${receipt.id}/${line.lineId}`&&x.base===cents(get(purchaseLines(po),x.lineId).unitCost*x.qty),'Receipt cost source changed.');
  must(Number.isSafeInteger(x.base)&&x.base>=0&&x.qty>0&&[x.remaining,x.sold,x.other].every(v=>Number.isFinite(v)&&v>=-.000001)&&x.remaining<=x.qty+.000001,'Invalid receipt cost exposure.');
  must(x.blocked||Math.abs(x.qty-x.remaining-x.sold-x.other)<.000001,'Receipt exposure is not balanced.');
  if(x.journalId){const j=get(business(s).journals,x.journalId);must(j.sourceCommand==='cost:receipt'&&j.sourceId===po.id+'/'+receipt.id,'Invalid receipt journal link.');}
 }
 for(const [list,posting,command] of [[c.matches,'Goods received not invoiced','cost:variance'],[c.allocations,'Landed cost clearing','cost:landed']]){
  must(new Set(list.map(x=>x.billId)).size===list.length,'Duplicate cost posting.');
  for(const r of list){const d=get(docs,r.billId);must(d.kind==='Bill'&&d.status==='Issued'&&d.costing?.posting===posting&&Number.isFinite(d.costing.rate)&&d.costing.rate>0,'Costed bill must remain issued and linked.');
   must(Number.isSafeInteger(r.amount)&&r.rows.every(l=>[l.amount,l.inventory,l.cogs,l.adjustments].every(Number.isSafeInteger)&&l.amount===l.inventory+l.cogs+l.adjustments)&&r.rows.reduce((n,l)=>n+l.amount,0)===r.amount,'Cost allocation does not balance.');
   for(const l of r.rows)must(get(c.pools,l.poolId).itemId===l.itemId,'Allocation item changed.');
   if(r.journalId){const j=get(business(s).journals,r.journalId);must(j.sourceCommand===command&&j.sourceId===d.id,'Invalid cost journal link.');}
  }
 }
 validateReturns(s);
 for(const d of docs.filter(x=>x.costing))must(d.kind==='Credit'&&d.costing.returnId||[...c.matches,...c.allocations,...(s.transferCosting?.allocations||[])].some(r=>r.billId===d.id),'Bill has an unrecognized cost posting.');
}
