import {deliveryLines} from './fulfillment.mjs?demo=2d15b6e9cd84b84d';
import {businessDay} from './company-date.mjs?demo=2d15b6e9cd84b84d';
// Local commercial subledger. Amounts are integer cents; unit prices have four decimals.
// This module never moves stock and never sends money or connects to an accounting service.
import {business} from './business.mjs?demo=2d15b6e9cd84b84d';
import {purchaseLines} from './purchasing.mjs?demo=2d15b6e9cd84b84d';
import {validUnicode,charLength} from './unicode.mjs?demo=2d15b6e9cd84b84d';
import {csvText} from './exchange.mjs?demo=2d15b6e9cd84b84d';
const must=(ok,msg)=>{if(!ok)throw Error(msg);};
const get=(rows,id,label='Record')=>{const r=rows.find(r=>r.id===id);must(r,`${label} not found.`);return r;};
const txt=(v,label,max=240,required=false)=>{const t=String(v??'').trim();must(validUnicode(t)&&charLength(t)<=max&&(!required||t),`${label} must contain valid text${required?' and is required':''} (up to ${max} characters).`);return t;};
const integer=(v,label,max=1e12,min=0)=>{must(Number.isSafeInteger(v)&&v>=min&&v<=max,`Invalid ${label}.`);return v;};
const qty=v=>{must(v!==''&&v!==null&&v!==undefined,'Enter a quantity.');return integer(Number(v),'quantity',1e7,1);};
const scaled=(v,places,label,max)=>{const t=String(v??'').trim();must(new RegExp(`^\\d+(?:\\.\\d{1,${places}})?$`).test(t),`Enter ${label} with no more than ${places} decimal places.`);const [a,b='']=t.split('.');const value=Number(BigInt(a)*10n**BigInt(places)+BigInt(b.padEnd(places,'0')));return integer(value,label,max);};
const rounded=(n,d)=>Number((BigInt(n)+BigInt(d)/2n)/BigInt(d));
const mul=(a,b,d)=>rounded(BigInt(a)*BigInt(b),d);
const day=(v,required=true)=>{const t=txt(v,'Date',10,required);must(!t||(/^\d{4}-\d{2}-\d{2}$/.test(t)&&Number.isFinite(Date.parse(t))&&new Date(t+'T00:00:00Z').toISOString().slice(0,10)===t),'Use a valid calendar date.');return t;};
const currencies=['CAD','USD','CNY','TWD','HKD','SGD','AUD','NZD','EUR','GBP'];
const currency=v=>{must(currencies.includes(v),'Billing supports CAD, USD, CNY, TWD, HKD, SGD, AUD, NZD, EUR and GBP.');return v;};
const fresh=()=>({version:1,sequence:0,profile:{name:'Chmltech WMS warehouse',address:'',contact:'',taxId:'',paymentInstructions:''},documents:[],payments:[]});
export const billing=s=>s.billing||fresh();
export const money=(cents,code)=>`${code} ${(cents/100).toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
const active=d=>d.status!=='Voided';
const totals=lines=>lines.reduce((a,l)=>{for(const k of ['gross','discount','net','tax','total'])a[k]+=l[k];return a;},{gross:0,discount:0,net:0,tax:0,total:0});
function amounts(l){const gross=mul(l.qty,l.price,100),discount=mul(gross,l.discountBP,10000),net=gross-discount,tax=mul(net,l.taxBP,10000);return {gross,discount,net,tax,total:net+tax};}
export function billingBalance(s,d){
 const b=billing(s),credits=b.documents.filter(c=>c.kind==='Credit'&&c.parentId===d.id&&c.status==='Issued').reduce((n,c)=>n+c.total,0),payments=b.payments.filter(p=>p.documentId===d.id&&p.status==='Recorded');
 const paid=payments.filter(p=>p.kind==='Payment').reduce((n,p)=>n+p.amount,0),refunded=payments.filter(p=>p.kind==='Refund').reduce((n,p)=>n+p.amount,0),balance=d.total-credits-paid+refunded;
 return {credits,paid,refunded,balance,due:Math.max(0,balance),refundDue:Math.max(0,-balance)};
}
export function billingStatus(s,d){if(d.status!=='Issued')return d.status;if(d.kind==='Credit')return 'Credit issued';const x=billingBalance(s,d);return x.refundDue?'Refund due':!x.due?(x.credits===d.total?'Credited':'Paid'):x.paid?'Part paid':'Open';}
export function billingSource(s,kind,sourceId,receiptId='',dateTimezone=s.organization?.timezone){
 const sourceDay=time=>businessDay({organization:{timezone:dateTimezone}},time);
 if(kind==='Invoice'){
  const sh=get(s.shipments,sourceId,'Shipment'),o=get(s.orders,sh.orderId,'Sales order'),c=business(s).customers.find(c=>c.id===o.customerId);
  must(sh.status==='Shipped','Invoice only a shipped order.');must(!o.scope||o.scope.ownerId==='owner-self','Consigned inventory cannot be invoiced as our sale.');
  return {sourceId,receiptId:'',sourceRef:`${sh.number} / ${o.number}`,sourceDate:sourceDay(sh.shippedAt),orderId:o.id,partyKey:o.customerId||`order:${o.id}`,party:o.quoteSnapshot?structuredClone(o.quoteSnapshot.party):{name:o.customer,address:c?.address||'',contact:c?.email||'',taxId:''},currency:currency(o.currency||business(s).homeCurrency),lines:deliveryLines(s,sh).map(l=>{const live=get(s.items,l.itemId),i={...live,...(o.quoteSnapshot?.lines.find(x=>x.itemId===l.itemId)||{}),id:live.id};return {sourceLineId:l.itemId,itemId:i.id,sku:i.sku,name:i.name,description:i.description||'',uom:i.uom,qty:l.qty,...(o.unitLines?.find(u=>u.itemId===i.id)?{unitSnapshot:structuredClone(o.unitLines.find(u=>u.itemId===i.id))}:{}),unitPrice:o.pricedLines?.find(x=>x.itemId===l.itemId)?.unitPrice??0};})};
 }
 must(kind==='Bill','Choose an invoice or supplier bill.');
 const charge=s.costing?.charges.find(x=>x.id===sourceId);if(charge)return {sourceId,receiptId:'',sourceRef:charge.kind+' / '+charge.id,sourceDate:charge.date,orderId:charge.id,partyKey:charge.supplierId,party:charge.party,currency:currency(charge.currency),lines:[{sourceLineId:charge.id,receiptId:'',purchaseLineId:charge.id,itemId:'',sku:charge.kind.toUpperCase(),name:charge.name,description:charge.name,uom:'charge',qty:1,unitPrice:charge.amount/100}]};
 const po=get(s.operations?.purchases||[],sourceId,'Purchase'),ids=receiptId.split('+');must(ids.length&&ids.length<=50&&new Set(ids).size===ids.length,'Select distinct receipts from one PO.');const receipts=ids.map(id=>get(po.receipts||[],id,'Receipt')),multi=ids.length>1;
 must(!po.scope||po.scope.ownerId==='owner-self','Consigned inventory cannot be billed to our business.');
 return {sourceId,receiptId,sourceRef:`${po.number} / ${receiptId}`,sourceDate:receipts.map(r=>sourceDay(r.time)).sort().at(-1),orderId:po.id,partyKey:po.supplierId||`purchase:${po.id}`,party:{name:po.supplier,address:po.snapshot?.address||'',contact:[po.snapshot?.contact,po.snapshot?.email].filter(Boolean).join(' / '),taxId:''},currency:currency(po.currency||business(s).homeCurrency),lines:receipts.flatMap(r=>r.lines.map(l=>{const p=get(purchaseLines(po),l.lineId),i=s.items.find(i=>i.id===l.itemId),f=po.tradeLines?.find(t=>t.itemId===l.itemId);return {sourceLineId:multi?`${r.id}/${l.lineId}`:l.lineId,receiptId:r.id,purchaseLineId:l.lineId,itemId:l.itemId,sku:p.sku||i.sku,name:p.name||i.name,description:p.description??i.description??'',uom:p.uom||i.uom,qty:l.qty,...(f?.unitId&&f.packSize>1?{unitSnapshot:{unitId:f.unitId,code:f.unitCode,name:f.packName,factor:f.packSize}}:{}),unitPrice:f?Number((f.foreignCost/f.packSize).toFixed(4)):p.unitCost};}))};
}
// A canonical receipt/line identity prevents single- and multi-receipt drafts
// from reserving the same received units twice. Credits never reopen receipts.
export function receiptLine(d,l){const parts=l.sourceLineId.split('/');return {receiptId:parts.length===2?parts[0]:d.receiptId,lineId:parts.length===2?parts[1]:l.sourceLineId};}
export function unbilledSource(s,kind,sourceId,receiptId='',exclude=''){
 const src=billingSource(s,kind,sourceId,receiptId),docs=billing(s).documents.filter(d=>d.id!==exclude&&d.kind===kind&&d.sourceId===sourceId&&active(d));
 return {...src,lines:src.lines.map(l=>({...l,qty:l.qty-docs.reduce((n,d)=>n+d.lines.filter(x=>kind==='Invoice'?x.sourceLineId===l.sourceLineId:(receiptLine(d,x).receiptId===l.receiptId&&receiptLine(d,x).lineId===l.purchaseLineId)).reduce((v,x)=>v+x.qty,0),0)})).filter(l=>l.qty>0)};
}
export function billingCandidates(s,kind){
 const choices=kind==='Invoice'?s.shipments.filter(sh=>sh.status==='Shipped').map(sh=>[sh.id,'']):(s.operations?.purchases||[]).flatMap(p=>(p.receipts||[]).map(r=>[p.id,r.id]));
 if(kind==='Bill')choices.push(...(s.costing?.charges||[]).map(x=>[x.id,'']));
 return choices.flatMap(([id,rid])=>{try{const src=billingSource(s,kind,id,rid),docs=billing(s).documents.filter(d=>d.kind===kind&&d.sourceId===id&&d.receiptId===rid&&active(d));if(kind==='Invoice'&&docs.length)return [];const lines=unbilledSource(s,kind,id,rid).lines;return lines.length?[{...src,lines}]:[];}catch{return [];}});
}
const previousCredits=(s,parentId,exclude='')=>billing(s).documents.filter(d=>d.kind==='Credit'&&d.parentId===parentId&&active(d)&&d.id!==exclude);
export function creditableLines(s,parent){const prev=previousCredits(s,parent.id);return parent.lines.map(l=>({...l,remaining:l.qty-prev.reduce((n,d)=>n+d.lines.filter(x=>x.sourceLineId===l.sourceLineId).reduce((n,x)=>n+x.qty,0),0)})).filter(l=>l.remaining>0);}
function checkSource(s,d){
 const source=billingSource(s,d.kind,d.sourceId,d.receiptId,d.dateTimezone||null);must(source.currency===d.currency&&source.partyKey===d.partyKey&&source.orderId===d.orderId&&source.receiptId===d.receiptId,'Source currency, party or order changed. Recreate this draft.');must(d.date>=source.sourceDate,'Document date cannot precede the shipment or receipt.');
 const others=billing(s).documents.filter(x=>x.id!==d.id&&x.kind===d.kind&&x.sourceId===d.sourceId&&active(x));
 must(d.kind!=='Invoice'||!others.length,'This shipment already has an invoice or draft.');
 for(const l of d.lines){const orig=get(source.lines.map(x=>({...x,id:x.sourceLineId})),l.sourceLineId,'Source line');must(orig.itemId===l.itemId,'Source product does not match.');const used=others.reduce((n,x)=>n+x.lines.filter(a=>d.kind==='Invoice'?a.sourceLineId===l.sourceLineId:(receiptLine(x,a).receiptId===orig.receiptId&&receiptLine(x,a).lineId===orig.purchaseLineId)).reduce((m,a)=>m+a.qty,0),0);must(l.qty+used<=orig.qty,'Billed quantity exceeds the unbilled receipt balance.');if(d.kind==='Invoice')must(l.qty===orig.qty,'Invoice quantities must match the shipment.');}
 if(d.kind==='Invoice')must(d.lines.length===source.lines.length,'Invoice must include every shipped product.');
}
function profile(p){return {name:txt(p.name,'Business name',100,true),address:txt(p.address,'Business address',1000),contact:txt(p.contact,'Contact',240),taxId:txt(p.taxId,'Tax registration',100),paymentInstructions:txt(p.paymentInstructions,'Payment instructions',1000)};}
function editDocument(s,d,p){
 const date=day(p.date),due=day(p.due,false);must(!due||due>=date,'Due date cannot precede the document date.');
 must(Array.isArray(p.lines)&&p.lines.length&&p.lines.length<=50,'Enter 1–50 product lines.');const source=billingSource(s,d.kind,d.sourceId,d.receiptId);
 const lines=p.lines.map(raw=>{const original=get(source.lines.map(l=>({...l,id:l.sourceLineId})),raw.sourceLineId,'Source line'),l={sourceLineId:original.sourceLineId,itemId:original.itemId,sku:original.sku,name:original.name,description:original.description,uom:original.uom,...(original.unitSnapshot?{unitSnapshot:structuredClone(original.unitSnapshot)}:{}),qty:qty(raw.qty),price:scaled(raw.unitPrice,4,'unit price',1e11),discountBP:scaled(raw.discountPercent??0,2,'discount percentage',10000),taxBP:scaled(raw.taxPercent??0,2,'tax percentage',10000),taxName:txt(raw.taxName,'Tax label',60)};return {...l,...amounts(l)};});
 must(new Set(lines.map(l=>l.sourceLineId)).size===lines.length,'Each source line can appear only once.');
 Object.assign(d,{date,due,reference:txt(p.reference,'Reference'),note:txt(p.note,'Note',1000),lines,...totals(lines)});checkSource(s,d);
}
export function beforeBilling(s,command,p){
 const b=billing(s);
 if(command==='voidShipment')must(!b.documents.some(d=>d.kind==='Invoice'&&d.sourceId===p.id&&active(d)),'Void the linked invoice or draft before reversing the shipment.');
 if(command==='business:settings')must(!b.documents.length,'Home currency cannot change after billing documents exist.');
}
export function billingCommand(s,command,p,ctx){
 if(!command.startsWith('billing:'))return null;
 const b=s.billing||(s.billing=fresh()),actor=txt(ctx.actor||'Local operator','Operator',100,true),today=businessDay(s,ctx.time);
 const event=(message,d)=>({type:message,message,reference:d?.number||'Billing',resultId:d?.id||null});
 const next=(prefix)=>{const n=++b.sequence;return {id:`billing-${n}`,number:`${prefix}-${n}`};};
 const doc=()=>get(b.documents,p.id,'Billing document');const history=(d,action,reason='')=>d.history.push({time:ctx.time,actor,action,reason});
 switch(command){
  case 'billing:profile':b.profile=profile(p);return event('Billing business details saved');
  case 'billing:createInvoice':case 'billing:createBill':{
   const kind=command.endsWith('Invoice')?'Invoice':'Bill',source=billingSource(s,kind,p.sourceId,p.receiptId||'');
   const d={...next(kind==='Invoice'?'INV':'BILL'),kind,status:'Draft',...(s.organization?.timezone?{dateTimezone:s.organization.timezone}:{}),sourceId:source.sourceId,receiptId:source.receiptId,sourceRef:source.sourceRef,orderId:source.orderId,partyKey:source.partyKey,party:source.party,currency:source.currency,issuer:structuredClone(b.profile),parentId:'',returnId:'',createdAt:ctx.time,createdBy:actor,history:[]};
   editDocument(s,d,{...p,date:p.date||today,due:p.due||'',lines:p.lines||unbilledSource(s,kind,source.sourceId,source.receiptId).lines.map(l=>({sourceLineId:l.sourceLineId,qty:l.qty,unitPrice:l.unitPrice.toFixed(4)}))});b.documents.push(d);history(d,'Created');return event(`${kind} drafted`,d);
  }
  case 'billing:edit':{const d=doc();must(d.status==='Draft'&&d.kind!=='Credit','Edit only a draft invoice or bill.');editDocument(s,d,p);d.issuer=structuredClone(b.profile);history(d,'Draft edited');return event('Billing draft saved',d);}
  case 'billing:issue':{const d=doc();must(d.status==='Draft','Only a draft can be issued.');must(p.reviewed===true,'Confirm prices, taxes, quantities and party details before issuing.');if(d.kind!=='Credit')checkSource(s,d);else must(get(b.documents,d.parentId).status==='Issued','Original invoice or bill must be issued.');if(d.kind==='Bill'){must(d.reference,'Enter the supplier invoice number before issuing.');must(!b.documents.some(x=>x.id!==d.id&&x.kind==='Bill'&&active(x)&&x.partyKey===d.partyKey&&x.reference.toLocaleLowerCase()===d.reference.toLocaleLowerCase()),'This supplier invoice number is already recorded.');}d.status='Issued';d.issuedAt=ctx.time;d.issuedBy=actor;history(d,'Issued');return event(`${d.kind} issued`,d);}
  case 'billing:credit':{
   const parent=get(b.documents,p.parentId,'Original document');must(parent.status==='Issued'&&parent.kind!=='Credit','Credit an issued invoice or bill.');const prior=previousCredits(s,parent.id),available=creditableLines(s,parent);must(Array.isArray(p.lines)&&p.lines.length&&p.lines.length<=50,'Select quantities to credit.');
   const lines=p.lines.map(raw=>{const l=get(available.map(l=>({...l,id:l.sourceLineId})),raw.sourceLineId,'Creditable line'),q=qty(raw.qty);must(q<=l.remaining,'Credit exceeds the remaining invoiced quantity.');const used=prior.flatMap(d=>d.lines).filter(x=>x.sourceLineId===l.sourceLineId),part={};for(const k of ['gross','discount','net','tax'])part[k]=mul(l[k]-used.reduce((n,x)=>n+x[k],0),q,l.remaining);part.discount=part.gross-part.net;part.total=part.net+part.tax;return {sourceLineId:l.sourceLineId,itemId:l.itemId,sku:l.sku,name:l.name,description:l.description,uom:l.uom,...(l.unitSnapshot?{unitSnapshot:structuredClone(l.unitSnapshot)}:{}),qty:q,price:l.price,discountBP:l.discountBP,taxBP:l.taxBP,taxName:l.taxName,...part};});must(new Set(lines.map(l=>l.sourceLineId)).size===lines.length,'Duplicate credit line.');
   const date=day(p.date||today);must(date>=parent.date,'Credit date cannot precede the original document.');const d={...next(parent.kind==='Invoice'?'CN':'SCN'),kind:'Credit',status:'Draft',...(s.organization?.timezone?{dateTimezone:s.organization.timezone}:{}),parentId:parent.id,returnId:p.returnId||'',sourceId:parent.sourceId,receiptId:parent.receiptId,sourceRef:parent.number,orderId:parent.orderId,partyKey:parent.partyKey,party:structuredClone(parent.party),issuer:structuredClone(parent.issuer),currency:parent.currency,date,due:'',reference:txt(p.reference,'Reference'),note:txt(p.note,'Credit reason',1000,true),lines,...totals(lines),createdAt:ctx.time,createdBy:actor,history:[]};b.documents.push(d);history(d,'Created');return event('Credit note drafted',d);
  }
  case 'billing:void':{const d=doc();must(active(d),'Document is already voided.');const reason=txt(p.reason,'Void reason',240,true);if(d.kind!=='Credit'){must(!b.documents.some(c=>c.parentId===d.id&&active(c)),'Void linked credit notes first.');must(!b.payments.some(x=>x.documentId===d.id&&x.status==='Recorded'),'Reverse recorded payments and refunds first.');}d.status='Voided';d.voidedAt=ctx.time;d.voidReason=reason;history(d,'Voided',reason);return event(`${d.kind} voided`,d);}
  case 'billing:payment':{
   const d=doc();must(d.status==='Issued'&&d.kind!=='Credit','Record payments against an issued invoice or bill.');must(['Payment','Refund'].includes(p.kind),'Choose payment or refund.');const x=billingBalance(s,d),amount=scaled(p.amount,2,'amount',1e12);must(amount>0&&amount<=(p.kind==='Refund'?x.refundDue:x.due),p.kind==='Refund'?'Refund exceeds the refundable balance.':'Payment exceeds the outstanding balance.');
   const date=day(p.date||today);must(date>=d.date,'Payment date cannot precede the document.');const reference=txt(p.reference,'Payment reference',240,true);must(!b.payments.some(x=>x.documentId===d.id&&x.status==='Recorded'&&x.kind===p.kind&&x.reference.toLocaleLowerCase()===reference.toLocaleLowerCase()),'This payment reference is already recorded.');const payment={...next('PAY'),documentId:d.id,kind:p.kind,status:'Recorded',currency:d.currency,amount,date,method:txt(p.method,'Payment method',60,true),reference,note:txt(p.note,'Payment note',1000),createdAt:ctx.time,createdBy:actor};b.payments.push(payment);history(d,`${p.kind} recorded`,payment.number);return event(`${p.kind} recorded`,d);
  }
  case 'billing:reversePayment':{const pay=get(b.payments,p.id,'Payment');must(pay.status==='Recorded','Payment is already reversed.');pay.status='Reversed';pay.reversalReason=txt(p.reason,'Reversal reason',240,true);pay.reversedAt=ctx.time;pay.reversedBy=actor;const d=get(b.documents,pay.documentId);history(d,'Payment reversed',`${pay.number}: ${pay.reversalReason}`);return event('Payment reversed',d);}
  default:throw Error('Unknown billing action.');
 }
}
export function validateBilling(s){
 if(!s.billing)return;const b=s.billing;must(b.version===1,'Unsupported billing data.');integer(b.sequence,'billing sequence');profile(b.profile);
 for(const key of ['documents','payments']){must(Array.isArray(b[key])&&b[key].length<=10000,'Invalid billing records.');must(new Set(b[key].map(d=>d.id)).size===b[key].length,'Duplicate billing records.');}
 must(new Set([...b.documents,...b.payments].map(d=>d.number)).size===b.documents.length+b.payments.length,'Duplicate billing document numbers.');
 const ids=new Set();for(const d of [...b.documents,...b.payments]){must(/^billing-\d+$/.test(d.id)&&Number(d.id.slice(8))<=b.sequence&&!ids.has(d.id),'Invalid billing identifier.');ids.add(d.id);txt(d.number,'Document number',40,true);currency(d.currency);day(d.date);if(d.dateTimezone){txt(d.dateTimezone,'Timezone',100,true);businessDay({organization:{timezone:d.dateTimezone}},d.createdAt);}must(Number.isFinite(Date.parse(d.createdAt)),'Invalid billing timestamp.');txt(d.createdBy,'Creator',100,true);}
 for(const d of b.documents){
  must(['Invoice','Bill','Credit'].includes(d.kind)&&['Draft','Issued','Voided'].includes(d.status),'Invalid billing type or status.');profile(d.issuer);txt(d.party?.name,'Party',100,true);txt(d.party?.address,'Address',1000);txt(d.party?.contact,'Contact',240);txt(d.party?.taxId,'Tax registration',100);txt(d.partyKey,'Party key',100,true);txt(d.sourceRef,'Source reference',240,true);txt(d.reference,'Reference');txt(d.note,'Note',1000);day(d.due,false);must(!d.due||d.due>=d.date,'Invalid billing due date.');must(Array.isArray(d.history)&&d.history.length<=10000,'Invalid billing history.');for(const h of d.history){must(Number.isFinite(Date.parse(h.time)),'Invalid history date.');txt(h.actor,'Actor',100,true);txt(h.action,'Action',100,true);txt(h.reason,'Reason',300);}
  if(d.status==='Issued'){must(Number.isFinite(Date.parse(d.issuedAt)),'Invalid issue timestamp.');txt(d.issuedBy,'Issuer',100,true);if(d.kind==='Bill')txt(d.reference,'Supplier invoice number',240,true);}
  if(d.status==='Voided'){must(Number.isFinite(Date.parse(d.voidedAt)),'Invalid void timestamp.');txt(d.voidReason,'Void reason',240,true);}
  must(Array.isArray(d.lines)&&d.lines.length>0&&d.lines.length<=50&&new Set(d.lines.map(l=>l.sourceLineId)).size===d.lines.length,'Invalid billing lines.');
  for(const l of d.lines){if(!s.costing?.charges.some(x=>x.id===d.sourceId))get(s.items,l.itemId);txt(l.sourceLineId,'Line identifier',100,true);integer(l.qty,'billing quantity',1e7,1);integer(l.price,'unit price',1e11);integer(l.discountBP,'discount',10000);integer(l.taxBP,'tax rate',10000);txt(l.taxName,'Tax label',60);txt(l.sku,'SKU',40,true);txt(l.name,'Product',100,true);txt(l.description,'Description',1000);txt(l.uom,'Unit',20,true);for(const k of ['gross','discount','net','tax','total'])integer(l[k],'line '+k);if(d.kind!=='Credit')for(const [k,v] of Object.entries(amounts(l)))must(l[k]===v,'Billing line amounts do not match quantities and rates.');must(l.total===l.net+l.tax&&l.gross-l.discount===l.net,'Invalid credit total.');}
  for(const [k,v] of Object.entries(totals(d.lines)))must(d[k]===v&&Number.isSafeInteger(v)&&v<=1e12,'Invalid billing totals.');
  if(d.kind!=='Credit'&&active(d))checkSource(s,d);
  if(d.kind==='Bill'&&active(d)&&d.reference)must(!b.documents.some(x=>x.id!==d.id&&x.kind==='Bill'&&active(x)&&x.partyKey===d.partyKey&&x.reference.toLocaleLowerCase()===d.reference.toLocaleLowerCase()),'This supplier invoice number is already recorded.');
  if(d.kind==='Credit'){
   const parent=get(b.documents,d.parentId,'Original billing document');must(parent.kind!=='Credit'&&d.currency===parent.currency&&d.partyKey===parent.partyKey&&d.date>=parent.date&&d.sourceId===parent.sourceId&&d.receiptId===parent.receiptId&&d.orderId===parent.orderId,'Invalid credit link.');if(active(d))must(parent.status==='Issued','Credit needs an issued original document.');
   for(const l of d.lines){const orig=get(parent.lines.map(l=>({...l,id:l.sourceLineId})),l.sourceLineId);must(l.itemId===orig.itemId&&l.price===orig.price&&l.taxBP===orig.taxBP&&l.discountBP===orig.discountBP,'Credit must retain original prices and taxes.');}
   if(d.returnId){const r=get(business(s).returns,d.returnId,'Return');must(r.kind===(parent.kind==='Invoice'?'Customer':'Supplier')&&r.sourceId===parent.orderId&&(!r.shipmentId||r.shipmentId===parent.sourceId),'Return does not match the original document.');if(active(d)){must(['Received','Restocked','Scrapped','Completed','Sent'].includes(r.status),'Complete the physical return before linking a credit.');const linked=b.documents.filter(c=>c.kind==='Credit'&&c.returnId===r.id&&active(c));must(linked.every(c=>c.lines.every(l=>l.itemId===r.itemId))&&linked.flatMap(c=>c.lines).reduce((n,l)=>n+l.qty,0)<=r.qty,'Linked credits exceed the physical return.');}}
  }
 }
 for(const d of b.documents.filter(d=>d.kind!=='Credit')){
  const credits=previousCredits(s,d.id);for(const l of d.lines){const lines=credits.flatMap(c=>c.lines).filter(x=>x.sourceLineId===l.sourceLineId);for(const k of ['qty','gross','discount','net','tax','total'])must(lines.reduce((n,x)=>n+x[k],0)<=l[k],'Credits exceed the original quantity or amount.');}
  const x=billingBalance(s,d);must(x.refunded<=x.paid,'Reverse refunds before reversing the payment.');must(x.paid-x.refunded<=d.total,'Void or reverse payments would overpay this document.');must(x.refunded<=x.credits,'Refunds must remain covered by issued credits.');must(!x.refunded||x.paid-x.refunded>=d.total-x.credits,'Reverse refunds before reducing the payments or credits supporting them.');if(d.status!=='Issued')must(!b.payments.some(p=>p.documentId===d.id&&p.status==='Recorded'),'Payments require an issued document.');
 }
 for(const p of b.payments){const d=get(b.documents,p.documentId,'Payment document');must(d.kind!=='Credit'&&p.currency===d.currency&&p.date>=d.date,'Invalid payment link.');must(['Payment','Refund'].includes(p.kind)&&['Recorded','Reversed'].includes(p.status),'Invalid payment state.');integer(p.amount,'payment amount',1e12,1);txt(p.method,'Method',60,true);txt(p.reference,'Reference',240,true);txt(p.note,'Note',1000);if(p.status==='Reversed'){txt(p.reversalReason,'Reversal reason',240,true);txt(p.reversedBy,'Reversed by',100,true);must(Number.isFinite(Date.parse(p.reversedAt)),'Invalid reversal timestamp.');}if(p.status==='Recorded')must(!b.payments.some(x=>x.id!==p.id&&x.documentId===p.documentId&&x.kind===p.kind&&x.status==='Recorded'&&x.reference.toLocaleLowerCase()===p.reference.toLocaleLowerCase()),'Duplicate recorded payment reference.');}
}
export function billingCSV(s){return csvText([['Number','Type','Party','Currency','Date','Due date','Status','Net','Tax','Total','Credits','Paid','Refunded','Balance','Source','Reference'],...billing(s).documents.map(d=>{const x=billingBalance(s,d);return [d.number,d.kind,d.party.name,d.currency,d.date,d.due,billingStatus(s,d),d.net/100,d.tax/100,d.total/100,...(d.kind==='Credit'?[0,0,0,0]:[x.credits/100,x.paid/100,x.refunded/100,x.balance/100]),d.sourceRef,d.reference];})]);}
