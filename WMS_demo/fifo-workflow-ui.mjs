import {interfaceLanguage,translate} from './locale.mjs?demo=5d9e5d1ce6c83eb1';
import {business,locationScope} from './business.mjs?demo=5d9e5d1ce6c83eb1';
import {isFIFO,rangeCost,previewFIFOWithdrawal,fifoValue} from './fifo.mjs?demo=5d9e5d1ce6c83eb1';
import {documentHTML,languages} from './documents.mjs?demo=5d9e5d1ce6c83eb1';
import {createDocumentPDF} from './pdf.mjs?demo=5d9e5d1ce6c83eb1';
import {formatMoney} from './currency-display.mjs?demo=5d9e5d1ce6c83eb1';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const button=(label,action,id='')=>`<button class="btn" data-action="biz-${action}" data-id="${e(id)}">${e(label)}</button>`;
const origin=(s,id)=>s.costLayers.origins.find(o=>o.id===id);
export function transferFIFO(s,t){const stock=s.stock.find(r=>r.id===t.stockId);if(!isFIFO(s,stock?.itemId))return null;const moves=(t.fifoMovements||[]).map(id=>s.costLayers.movements.find(m=>m.id===id)),live=s.costLayers.layers.filter(l=>l.transitId===t.id&&l.qty);let draft=[];if(t.status==='Draft')draft=previewFIFOWithdrawal(s,stock.itemId,t.qty,locationScope(s,stock.locationId).warehouseId);return {itemId:stock.itemId,moves,live,dispatch:t.fifoDispatch?.value??draft.reduce((n,x)=>n+x.value,0),transit:live.reduce((n,l)=>n+rangeCost(origin(s,l.originId),l.start,l.qty),0),draft};}
export function transferFIFOHTML(s,t){const f=transferFIFO(s,t);if(!f)return '';return `<br><strong>FIFO</strong><br><span>Dispatch book value</span>: ${formatMoney(f.dispatch/100,business(s).homeCurrency)}<br><span>Current transit value</span>: ${formatMoney(f.transit/100,business(s).homeCurrency)}<br>`+button('Cost / PDF','fifoTransferDocument',t.id);}
export const returnFIFOHTML=(s,r)=>r.fifoSupplier?`<br><strong>FIFO</strong><br>`+button('Cost / PDF','fifoSupplierDocument',r.id):'';
let selection=null,locale='en';const fonts=new Map();
export function fifoWorkflowDocuments(s,kind,id,language='en'){
 const b=business(s),t=kind==='transfer'?b.transfers.find(t=>t.id===id):b.returns.find(r=>r.id===id);if(!t)throw Error('FIFO document source is missing.');const item=s.items.find(i=>i.id===(kind==='transfer'?s.stock.find(r=>r.id===t.stockId)?.itemId:t.itemId)),w=k=>translate(k,language),f=(k,v)=>({kind:'field',label:w(k),text:String(v)}),money=n=>formatMoney(n/100,b.homeCurrency);
 const blocks=[{kind:'item',text:item.sku+' / '+item.name},f('Description',item.description||''),f('Status',w(t.status)),f('Quantity',t.qty)];let title,slices;
 if(kind==='transfer'){
  const d=transferFIFO(s,t);title=w('FIFO warehouse transfer');blocks.push(f('Origin warehouse',b.warehouses.find(x=>x.id===locationScope(s,s.stock.find(x=>x.id===t.stockId).locationId).warehouseId)?.name),f('Destination warehouse',b.warehouses.find(x=>x.id===locationScope(s,t.destination).warehouseId)?.name),f('Received / quantity',t.received+' / '+t.qty),f('Dispatch book value',money(d.dispatch)),f('Current transit value',money(d.transit)),f('Current product value at destination',money(fifoValue(s,item.id,locationScope(s,t.destination).warehouseId))),f('Transfer note',t.note));
  for(const a of s.transferCosting?.allocations.filter(a=>a.transferIds.includes(t.id))||[]){const rows=a.rows.filter(r=>r.transferId===t.id),bill=s.billing.documents.find(b=>b.id===a.billId);blocks.push({kind:'item',text:w('Transfer freight costing')},f('Freight bill',bill.number),f('Inventory still held',money(rows.reduce((n,r)=>n+r.inventory,0))),f('Goods already sold',money(rows.reduce((n,r)=>n+r.cogs,0))),f('Write-offs',money(rows.reduce((n,r)=>n+r.adjustments,0))),f('Inventory journal',a.journalId),f('Review reason',a.reason));}
  for(const m of d.moves)blocks.push(f('Movement',m.id+' / '+w(m.phase)+' / '+m.time+' / '+m.slices.reduce((n,x)=>n+x.qty,0)+' / '+money(m.value)));slices=d.moves.find(m=>m.phase==='Dispatched')?.slices||d.draft;
 }else{
  title=w('FIFO supplier return');const po=s.operations.purchases.find(po=>po.id===t.sourceId);blocks.push(f('Supplier',po.supplier),f('Purchase order',po.number),f('Receipt',t.receiptId),f('Reason',t.reason),f('Dispatch book value',money(t.costPosting.value)),f('Inventory journal',t.costPosting.journalId));slices=t.fifoSupplier.slices;
  for(const c of s.costing.returnCredits.filter(c=>c.returnId===t.id)){const d=s.billing.documents.find(d=>d.id===c.creditId);blocks.push(f('Supplier credit',d.number+' / '+c.qty),f('Book value',money(c.bookValue)),f('Supplier credit amount',money(c.creditNet)),f('Settlement adjustment',money(c.variance)));}
 }
 for(const x of slices){const o=origin(s,x.originId);blocks.push({kind:'item',text:o.id},f('Original receipt',o.purchaseId+' / '+o.receiptId),f('Original layer date',s.costLayers.layers.find(l=>l.id===x.layerId)?.createdAt||o.time),f('Unit range',x.start+'-'+(x.start+x.qty-1)),f('Quantity',x.qty),f('Book value',money(x.value)));}
 return [{locale:language,title,ref:t.number,size:'A4',density:'compact',blocks,footer:w(kind==='transfer'?'Ordinary transfer preserves company inventory value. Later receipt costs are separate adjustments.':'FIFO dispatch value is frozen. The selected receipt identifies the supplier credit; oldest available warehouse layers determine book cost.'),pageWord:w('Page'),continued:w('continued')}];
}
export async function fifoWorkflowAction(act,id,el,{s,select,showModal,download}){
 if(!['fifoTransferDocument','fifoSupplierDocument','fifoDocumentLanguage','fifoDocumentPDF'].includes(act))return false;
 if(act==='fifoTransferDocument'||act==='fifoSupplierDocument'){selection={kind:act==='fifoTransferDocument'?'transfer':'supplier',id};locale=interfaceLanguage();}
 if(act==='fifoDocumentLanguage'||act==='fifoDocumentPDF')locale=document.querySelector('[name="fifoDocumentLanguage"]').value;
 const docs=fifoWorkflowDocuments(s,selection.kind,selection.id,locale);
 if(act==='fifoDocumentPDF'){const variant=locale==='zh-Hant'?'TC':'SC';el.disabled=true;try{if(!fonts.has(variant)){const r=await fetch('./fonts/NotoSans'+variant+'-Regular.ttf');if(!r.ok)throw Error('Chinese PDF font unavailable.');fonts.set(variant,new Uint8Array(await r.arrayBuffer()));}const bytes=await createDocumentPDF(docs,{PDFLib:globalThis.PDFLib,fontkit:globalThis.fontkit,fontBytes:fonts.get(variant)});download('harbor-fifo-'+selection.kind+'-'+locale+'.pdf',bytes,'application/pdf');}finally{el.disabled=false;}}
 else showModal('FIFO cost document',select('Document language','fifoDocumentLanguage',languages,locale)+button('Apply language','fifoDocumentLanguage')+button('Download PDF','fifoDocumentPDF')+documentHTML(docs));return true;
}

