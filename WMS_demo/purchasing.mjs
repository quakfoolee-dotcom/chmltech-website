import {charLength,validUnicode} from './unicode.mjs?demo=2d15b6e9cd84b84d';
const must=(ok,message)=>{if(!ok)throw Error(message);};
const find=(rows,id,label='Record')=>{const row=rows.find(x=>x.id===id);must(row,`${label} not found.`);return row;};
const text=(value,label,max=240,required=false)=>{const out=String(value??'').trim();must(validUnicode(out)&&charLength(out)<=max,`${label} must contain valid text up to ${max} characters.`);must(!required||out,`${label} is required.`);return out;};
const quantity=(value,zero=false)=>{const n=Number(value);must(Number.isSafeInteger(n)&&n>=(zero?0:1)&&n<=10000000,'Quantity must be a whole number within the allowed balance.');return n;};
const cost=value=>{const n=Number(value??0);must(Number.isFinite(n)&&n>=0&&n<=10000000,'Unit cost must be between 0 and 10000000.');return Math.round((n+Number.EPSILON)*10000)/10000;};
const date=value=>{const v=text(value,'Due date',10);must(!v||(/^\d{4}-\d{2}-\d{2}$/.test(v)&&!Number.isNaN(Date.parse(v))&&new Date(v+'T00:00:00Z').toISOString().slice(0,10)===v),'Use a valid due date.');return v;};
const event=(type,reference,message,resultId=null)=>({type,reference,message,resultId});
export const suppliers=s=>s.operations?.suppliers||[];
// Legacy one-product orders are read without rewriting or losing their history.
export const purchaseLines=p=>p.lines||[{id:'line-1',itemId:p.itemId,qty:p.qty,received:p.received,unitCost:p.unitCost,vendorSku:''}];
export const purchaseTotals=p=>purchaseLines(p).reduce((a,l)=>({ordered:a.ordered+l.qty,received:a.received+l.received,remaining:a.remaining+(p.status==='Open'?l.qty-l.received:0),amount:a.amount+l.qty*l.unitCost}),{ordered:0,received:0,remaining:0,amount:0});
export const supplierProductCode=(s,supplierId,itemId)=>suppliers(s).find(x=>x.id===supplierId)?.products.find(x=>x.itemId===itemId)?.vendorSku||'';

export function validatePurchasing(s){
 const f=s.operations;if(!f)return;
 const isText=(v,max=240)=>typeof v==='string'&&charLength(v)<=max&&validUnicode(v);
 const list=suppliers(s);must(Array.isArray(list)&&list.length<=10000,'Invalid supplier directory.');
 if(f.suppliers!==undefined)must(Number.isSafeInteger(f.counters.supplier)&&f.counters.supplier>=0,'Invalid supplier counter.');
 const ids=new Set(),codes=new Set();
 for(const v of list){
  must(/^supplier-\d+$/.test(v.id)&&Number(v.id.slice(9))<=f.counters.supplier&&!ids.has(v.id),'Invalid supplier identifier.');ids.add(v.id);
  must(isText(v.code,40)&&v.code.trim()&&!codes.has(v.code.toUpperCase()),'Supplier codes must be unique.');codes.add(v.code.toUpperCase());
  must(isText(v.name,100)&&v.name.trim()&&isText(v.englishName,100)&&isText(v.contact,100)&&isText(v.email,240)&&isText(v.phone,60)&&isText(v.address,1000)&&isText(v.notes,1000)&&isText(v.paymentTerms,100)&&typeof v.active==='boolean','Invalid supplier details.');
  must(Array.isArray(v.products)&&v.products.length<=200&&new Set(v.products.map(x=>x.itemId)).size===v.products.length,'Duplicate or invalid supplier products.');
  for(const p of v.products){find(s.items,p.itemId,'Product');must(isText(p.vendorSku,100)&&p.vendorSku.trim(),'Invalid supplier product code.');}
 }
 for(const p of f.purchases){
  if(p.lines!==undefined){
   find(list,p.supplierId,'Supplier');must(p.snapshot&&p.snapshot.name===p.supplier&&['name','englishName','contact','email','phone','address','paymentTerms'].every(k=>isText(p.snapshot[k],k==='address'?1000:k==='email'?240:k==='phone'?60:100)),'Invalid purchase supplier snapshot.');
   must(isText(p.reference,240)&&isText(p.note,1000)&&isText(p.createdAt,40),'Invalid purchase details.');
   must(Array.isArray(p.lines)&&p.lines.length>0&&p.lines.length<=50&&new Set(p.lines.map(l=>l.id)).size===p.lines.length&&new Set(p.lines.map(l=>l.itemId)).size===p.lines.length,'Purchase lines must contain unique products.');
   for(const l of p.lines){
    find(s.items,l.itemId,'Product');must(/^line-\d+$/.test(l.id)&&isText(l.sku,40)&&isText(l.name,100)&&isText(l.description,1000)&&isText(l.uom,20)&&isText(l.vendorSku,100),'Invalid purchase product snapshot.');
    must(Number.isSafeInteger(l.qty)&&l.qty>0&&l.qty<=10000000&&Number.isSafeInteger(l.received)&&l.received>=0&&l.received<=l.qty&&typeof l.unitCost==='number'&&Number.isFinite(l.unitCost)&&l.unitCost>=0&&l.unitCost<=10000000,'Invalid purchase line quantities or cost.');
   }
   must(p.status!=='Closed'||p.lines.every(l=>l.received===l.qty),'Closed purchase is incomplete.');
   must(p.status!=='Open'||p.lines.some(l=>l.received<l.qty),'Completed purchase must be closed.');
   must(Array.isArray(p.receipts)&&p.receipts.length<=10000,'Invalid receipt history.');
  }
  if(p.receipts!==undefined){
   must(Array.isArray(p.receipts)&&p.receipts.length<=10000,'Invalid receipt history.');
   const receiptIds=new Set(),sum={};
   for(const r of p.receipts){
    must(/^receipt-\d+$/.test(r.id)&&!receiptIds.has(r.id)&&isText(r.time,40)&&Number.isFinite(Date.parse(r.time))&&isText(r.reference,240)&&Array.isArray(r.lines)&&r.lines.length>0&&r.lines.length<=50,'Invalid receipt.');receiptIds.add(r.id);
    must(new Set(r.lines.map(l=>l.lineId)).size===r.lines.length,'Duplicate receipt line.');
    for(const l of r.lines){const ordered=find(purchaseLines(p),l.lineId,'Purchase line');must(ordered.itemId===l.itemId&&Number.isSafeInteger(l.qty)&&l.qty>0&&l.qty<=ordered.qty&&isText(l.lot,100)&&isText(l.locationId,100)&&Array.isArray(l.serials)&&l.serials.every(x=>isText(x,100))&&isText(l.expiresOn,10),'Invalid receipt line.');if(p.kind==='Warehouse')find(s.locations,l.locationId,'Location');sum[l.lineId]=(sum[l.lineId]||0)+l.qty;}
   }
   for(const l of purchaseLines(p))must(p.lines?(sum[l.id]||0)===l.received:(sum[l.id]||0)<=l.received,'Receipt history does not match received quantities.');
  }
 }
}

export function purchasingCommand(s,command,payload,ctx){
 const f=s.operations;
 if(command==='saveSupplier'){
  f.suppliers||=[];f.counters.supplier??=0;
  const old=payload.id?find(f.suppliers,payload.id,'Supplier'):null;
  const code=text(payload.code,'Supplier code',40,true).toUpperCase();must(!f.suppliers.some(v=>v.id!==old?.id&&v.code.toUpperCase()===code),'This supplier code already exists.');
  const products=payload.products||[];must(Array.isArray(products)&&products.length<=200,'Use up to 200 supplier product codes.');
  const value={id:old?.id||`supplier-${++f.counters.supplier}`,code,name:text(payload.name,'Supplier name',100,true),englishName:text(payload.englishName,'English name',100),contact:text(payload.contact,'Contact',100),email:text(payload.email,'Email',240),phone:text(payload.phone,'Phone',60),address:text(payload.address,'Address',1000),notes:text(payload.notes,'Notes',1000),paymentTerms:text(payload.paymentTerms,'Payment terms',100),active:old?.active??true,products:products.map(p=>({itemId:find(s.items,p.itemId,'Product').id,vendorSku:text(p.vendorSku,'Supplier product code',100,true)}))};
  if(old)Object.assign(old,value);else f.suppliers.push(value);
  return event(old?'Supplier updated':'Supplier created',code,value.name,value.id);
 }
 if(command==='setSupplierActive'){
  const v=find(suppliers(s),payload.id,'Supplier');must(typeof payload.active==='boolean','Choose the supplier status.');v.active=payload.active;
  return event(v.active?'Supplier activated':'Supplier archived',v.code,'Existing purchase orders and their details are retained.',v.id);
 }
 if(command==='createPurchase'&&payload.lines!==undefined){
  const fields=purchaseFields(s,payload),id=`po-${++f.counters.purchase}`,p={id,number:`PO-${f.counters.purchase}`,...fields,createdAt:ctx.time,receipts:[]};
  f.purchases.push(p);return event('Purchase created',p.number,`${p.lines.length} product lines ordered from ${p.supplier}.`,id);
 }
 if(command==='receivePurchase'){
  const original=find(f.purchases,payload.id,'Purchase');must(original.status==='Open','This purchase has no open balance to receive.');
  const request=payload.lines??[{...payload,lineId:purchaseLines(original)[0].id}];
  must(Array.isArray(request)&&request.length>0&&request.length<=50,'Enter quantities for at least one purchase line.');
  const seen=new Set(),lines=request.map(l=>{const ordered=find(purchaseLines(original),l.lineId,'Purchase line');must(!seen.has(l.lineId),'Duplicate receipt line.');seen.add(l.lineId);const q=quantity(l.qty,true);must(q<=ordered.qty-ordered.received,'Quantity exceeds the open purchase balance.');return {...l,qty:q,ordered};}).filter(l=>l.qty>0);
  must(lines.length,'Enter a received quantity greater than zero.');must((original.receipts?.length||0)<10000,'Receipt history is full.');
  const reference=text(payload.reference??payload.note,'Delivery reference'),receiptId=`receipt-${Math.max(0,...(original.receipts||[]).map(r=>Number(r.id.slice(8))))+1}`;
  let next=s;const receipts=[];
  // Nested immutable stock commands validate costs, lots and serial numbers.
  // Publish the result only after every line succeeds.
  for(const l of lines){
   const lot=text(l.lot,'Lot',100)||'UNTRACKED';
   if(original.kind==='Warehouse')next=ctx.dispatch(next,'receiveStock',{itemId:l.ordered.itemId,qty:l.qty,unitCost:l.ordered.unitCost,locationId:l.locationId,lot,expiresOn:l.expiresOn||undefined,serials:l.serials,note:`${original.number}${reference?' / '+reference:''}`},{now:ctx.time}).state;
   const p=find(next.operations.purchases,original.id,'Purchase');
   if(p.lines)find(p.lines,l.lineId,'Purchase line').received+=l.qty;else p.received+=l.qty;
   const receiptLine={lineId:l.lineId,itemId:l.ordered.itemId,qty:l.qty,locationId:original.kind==='Warehouse'?String(l.locationId):'',lot:original.kind==='Warehouse'?lot:'',expiresOn:original.kind==='Warehouse'?(next.operations.lots[`${l.ordered.itemId}|${lot}`]?.expiresOn||''):'',serials:original.kind==='Warehouse'?(Array.isArray(l.serials)?l.serials.map(x=>text(x,'Serial number',100)):String(l.serials||'').split(/[\n,]/).map(x=>text(x,'Serial number',100)).filter(Boolean)):[]};
   receipts.push(receiptLine);
   // Keep receipt invariants valid for the next nested stock command.
   p.receipts||=[];
   let receipt=p.receipts.find(r=>r.id===receiptId);
   if(!receipt){receipt={id:receiptId,time:ctx.time,reference,lines:[]};p.receipts.push(receipt);}
   receipt.lines.push(receiptLine);
   if(purchaseLines(p).every(x=>x.qty===x.received))p.status='Closed';
  }
  Object.assign(s,next);const p=find(s.operations.purchases,original.id,'Purchase');
  return event(original.kind==='Warehouse'?'Purchase received':'Direct delivery recorded',p.number,`${receipts.length} product line(s) received${reference?' / '+reference:''}. ${original.kind==='Drop ship'?'No warehouse movement.':''}`,p.id);
 }
 if(command==='cancelPurchase'){
  const p=find(f.purchases,payload.id,'Purchase');must(p.status==='Open','Only an open purchase can be cancelled.');p.status='Cancelled';return event('Purchase cancelled',p.number,'Unreceived balances cancelled. Receipt history and received stock are retained.',p.id);
 }
 return null;
}

export function purchaseFields(s,payload){
  const v=find(suppliers(s),payload.supplierId,'Supplier');must(v.active,'Choose an active supplier.');must(Array.isArray(payload.lines)&&payload.lines.length>0&&payload.lines.length<=50,'Add 1 to 50 purchase lines.');
  const lines=payload.lines.map((l,index)=>{const i=find(s.items,l.itemId,'Product');return {id:`line-${index+1}`,itemId:i.id,sku:i.sku,name:i.name,description:i.description||'',uom:i.uom,vendorSku:text(l.vendorSku??supplierProductCode(s,v.id,i.id),'Supplier product code',100),qty:quantity(l.qty),received:0,unitCost:cost(l.unitCost)};});
  must(new Set(lines.map(l=>l.itemId)).size===lines.length,'Each product may appear once. Combine duplicate product quantities.');
  const kind=payload.kind||'Warehouse';must(['Warehouse','Drop ship'].includes(kind),'Invalid purchase type.');
  const snapshot=Object.fromEntries(['name','englishName','contact','email','phone','address','paymentTerms'].map(k=>[k,v[k]]));
  return {supplierId:v.id,supplier:v.name,snapshot,kind,customer:kind==='Drop ship'?text(payload.customer,'Delivery customer',100,true):'',due:date(payload.due),status:'Open',reference:text(payload.reference,'Supplier reference'),note:text(payload.note,'Purchase note',1000),lines};

}
