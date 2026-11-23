import {availableStock,orderScope} from './business.mjs?demo=45f52980507d3a1b';
import {fulfillmentRows,openPicks} from './fulfillment.mjs?demo=45f52980507d3a1b';
import {transferCosting,transferFreightPreview} from './transfer-costing.mjs?demo=45f52980507d3a1b';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=(s,n)=>`${s.business?.homeCurrency||'CAD'} ${(n/100).toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
const button=(text,act,id='')=>`<button class="btn" data-action="delivery-${act}" data-id="${e(id)}">${e(text)}</button>`;
const table=(head,rows)=>`<div class="table-scroll"><table><thead><tr>${head.map(x=>`<th>${e(x)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>'<tr>'+row.map(x=>`<td>${x}</td>`).join('')+'</tr>').join('')}</tbody></table></div>`;
export function deliveryPanel(s,o){
 const active=openPicks(s,o),eligible=['Draft','Issued','Backordered','Part shipped'].includes(o.status)&&active.every(p=>p.status==='Entered'&&!s.operations?.picks[p.id]?.batchId)&&!Object.values(s.operations?.families||{}).some(f=>f.orderIds.includes(o.id));
 if(!o.fulfillment&&!eligible)return '';
 const rows=fulfillmentRows(s,o),shipments=s.shipments.filter(sh=>sh.orderId===o.id&&sh.status!=='Cancelled');
 return `<section class="delivery-panel card"><div class="card-head"><h3>Deliveries & backorders</h3>${eligible?button('Release shipment','release',o.id):''}</div><p>Each delivery retains its own quantities. The original sales order and prices stay unchanged.</p>${table(['Product','Ordered','Shipped','Released','Backordered','Stock shortage'],rows.map(r=>[e(s.items.find(i=>i.id===r.itemId)?.sku),r.qty,r.shipped,o.fulfillment?r.released:0,o.fulfillment?r.backorder:r.remaining,Math.max(0,(o.fulfillment?r.backorder:r.remaining)-availableStock(s,r.itemId,orderScope(s,o)))]))}${shipments.length?table(['Shipment','Status','Invoice'],shipments.map(sh=>{const d=s.billing?.documents.find(d=>d.kind==='Invoice'&&d.sourceId===sh.id&&d.status!=='Voided');return [`<a href="#shipping/${sh.id}">${e(sh.number)}</a>`,e(sh.status),d?`<a href="#business/invoices/${d.id}">${e(d.number)}</a>`:'—'];})):''}</section>`;
}
export function transferFreightPanel(s){const c=transferCosting(s);return `<section class="delivery-panel card"><div class="card-head"><h3>Transfer freight costing</h3>${button('Allocate transfer freight','freight')}</div><p>Allocate an issued freight bill to received transfers. FIFO follows the received ranges; Average uses prospective exposure after full receipt. Future receipts are excluded.</p>${table(['Freight bill','Transfers','Inventory still held','Goods already sold','Write-offs','Journal'],c.allocations.slice().reverse().map(a=>[e(s.billing.documents.find(d=>d.id===a.billId)?.number),a.transferIds.map(id=>e(s.business.transfers.find(t=>t.id===id)?.number)).join(', '),money(s,a.rows.reduce((n,r)=>n+r.inventory,0)),money(s,a.rows.reduce((n,r)=>n+r.cogs,0)),money(s,a.rows.reduce((n,r)=>n+r.adjustments,0)),`<a href="#business/accounting">${e(a.journalId)}</a>`]))}</section>`;}
export async function deliveryAction(name,id,el,{s,run,showModal,field,select}){
 if(!name.startsWith('delivery-'))return false;
 if(name==='delivery-release'){const o=s.orders.find(o=>o.id===id),rows=fulfillmentRows(s,o).filter(l=>l.remaining>0);showModal('Release shipment','<p>Each delivery retains its own quantities. The original sales order and prices stay unchanged.</p>'+rows.map(l=>field(s.items.find(i=>i.id===l.itemId).sku,l.itemId,'number',l.remaining,`required min="0" max="${l.remaining}" step="1"`)).join('')+field('Review reason','reason','text','','required maxlength="240"'),'Release shipment',v=>run('releaseShipment',{id,reason:v.reason,lines:rows.map(l=>({itemId:l.itemId,qty:Number(v[l.itemId])}))},rid=>`picking/${rid}`));}
 else if(name==='delivery-freight'){
  const docs=s.billing?.documents.filter(d=>d.kind==='Bill'&&d.status==='Issued'&&!d.costing&&s.costing?.charges.some(c=>c.id===d.sourceId&&c.kind==='Freight'))||[],ts=s.business?.transfers.filter(t=>t.received>0)||[];if(!docs.length||!ts.length)throw Error('Create and issue a freight charge bill, and receive a warehouse transfer first.');
  showModal('Allocate transfer freight',select('Freight bill','billId',docs.map(d=>[d.id,`${d.number} / ${d.party.name}`]))+select('Transfer','transferId',ts.map(t=>[t.id,`${t.number} / ${t.received} / ${t.qty}`]))+field('Review reason','reason','text','','required maxlength="240"'),'Review allocation',v=>{
   const p={billId:v.billId,transferIds:[v.transferId],reason:v.reason,reviewed:true},a=transferFreightPreview(s,p);
   showModal('Review transfer freight',`<p>${e(a.number)} · ${e(money(s,a.amount))}</p>`+table(['Product','Received quantity','Retained / sold / other'],a.rows.map(r=>[e(s.items.find(i=>i.id===r.itemId)?.sku),r.qty,`${r.remaining} / ${r.sold} / ${r.other}`]))+'<p>Future receipts are excluded.</p>','Apply allocation',()=>run('transferCost:allocate',p));return false;
  });
 }
 return true;
}
