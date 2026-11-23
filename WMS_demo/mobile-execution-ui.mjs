import {groupView,packView,executionGroup,executionPack} from './execution-view.mjs?demo=2d15b6e9cd84b84d';
const orderScope=(s,o)=>o.scope||{warehouseId:'wh-main',ownerId:'owner-self'};
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const input=(name,label,value='',type='text',extra='')=>`<label>${label}<input name="${name}" value="${e(value)}" type="${type}" ${extra}></label>`;
const scanField=(name,label)=>input(name,label,'','text','required autocomplete="off"')+`<button type="button" data-scan-target="${name}">Camera</button>`;
const button=(label,action)=>`<button type="button" data-execution="${action}">${label}</button>`;
const form=(action,body,caption)=>`<form data-execution="${action}">${body}<button class="primary full">${caption}</button></form>`;
const checks=`<label><input name="reviewed" type="checkbox" required> <span>I reviewed quantities and the selected shipment.</span></label>`;
const serials='<label>Serial numbers, if tracked<textarea name="serials" rows="2" placeholder="One serial per line"></textarea></label>';
const scope=(s,pk)=>orderScope(s,s.orders.find(o=>o.id===pk.orderId));
export function executionCandidates(s,mode,warehouse){
 if(mode==='Group')return s.operations.batches.filter(b=>!executionGroup(s,b.id)?.abandoned&&b.pickIds.every(pid=>scope(s,s.picks.find(p=>p.id===pid)).warehouseId===warehouse)).map(b=>[b.id,b.name+' · '+b.pickIds.map(pid=>s.orders.find(o=>o.id===s.picks.find(p=>p.id===pid).orderId).number).join(', ')]);
 return s.shipments.filter(sh=>sh.status===(mode==='Pack'?'Entered':'Packed')&&orderScope(s,s.orders.find(o=>o.id===sh.orderId)).warehouseId===warehouse).map(sh=>[sh.id,sh.number+' · '+s.orders.find(o=>o.id===sh.orderId).customer]);
}
export function groupCreationHTML(s,warehouse){const ready=s.picks.filter(pk=>pk.status==='Entered'&&s.orders.find(o=>o.id===pk.orderId).status==='Issued'&&!s.operations.picks[pk.id]?.batchId&&!s.operations.picks[pk.id]?.hold&&scope(s,pk).warehouseId===warehouse);return `<details><summary>Create grouped pick</summary>${form('warehouse:createGroup',ready.map(pk=>`<label class="group-choice"><input type="checkbox" name="pickIds" value="${pk.id}"><span data-l10n-skip>${e(pk.number)} · ${e(s.orders.find(o=>o.id===pk.orderId).customer)}</span></label>`).join('')+'<p>Choose 2–20 uncommitted picks in one warehouse and owner.</p>','Create grouped pick')}</details>`;}
export function executionWorkHTML(s,mode,id){
 if(mode==='Group'){
  const v=groupView(s,id),g=v.control;
  let body=`<article><h2 data-l10n-skip>${e(v.batch.name)}</h2><p>Each tote belongs to one customer order. Original quantities and costs stay unchanged.</p>`;
  if(!g)return body+button('Prepare order totes','warehouse:prepareGroup')+'</article>';
  body+=v.slots.map(slot=>`<section class="execution-slot"><h3 data-l10n-skip>${e(slot.tote)}</h3><p data-l10n-skip>${e(slot.order.number)} · ${e(slot.order.customer)}</p>${slot.lines.map(l=>`<div class="product" data-l10n-skip><strong>${e(l.sku)} · ${e(l.name)}</strong>${e(l.bin)} / ${e(l.lot)} · ${l.scanned} / ${l.qty}</div>`).join('')}</section>`).join('');
  body+='<p><a href="./execution-labels.html?group='+encodeURIComponent(id)+'" target="_blank">Print tote and bin barcodes</a></p>';
  if(g.completed)return body+'<p>Grouped picking finished. Open Packing for each shipment.</p></article>';
  if(v.slots.every(x=>x.pick.status==='Entered'))return body+button('Reserve group','warehouse:commitGroup')+'</article>';
  const totals=new Map();for(const slot of v.slots)for(const l of slot.lines){const key=l.bin+'|'+l.sku+'|'+l.lot,old=totals.get(key)||{...l,qty:0,scanned:0};old.qty+=l.qty;old.scanned+=l.scanned;totals.set(key,old);}
  body+='<h3>Combined pick list</h3>'+[...totals.values()].sort((a,b)=>a.bin.localeCompare(b.bin)||a.sku.localeCompare(b.sku)).map(l=>`<p data-l10n-skip>${e(l.bin)} / ${e(l.sku)} / ${e(l.lot)} · ${l.scanned} / ${l.qty}</p>`).join('');
  return body+'</article>'+form('warehouse:scanGroup',scanField('toteCode','Order tote barcode')+scanField('sourceCode','Source bin barcode')+scanField('code','Barcode or SKU')+scanField('lot','Lot / batch')+input('qty','Quantity',1,'number','required min="1" step="1"')+serials,'Save tote scan')+button('Finish scanned group','warehouse:finishGroup');
 }
 const v=packView(s,id),c=v.control;let body=`<article><h2 data-l10n-skip>${e(v.shipment.number)}</h2><p data-l10n-skip>${e(v.order.number)} · ${e(v.order.customer)}</p>${v.lines.map(l=>`<div class="product" data-l10n-skip><strong>${e(l.sku)} · ${e(l.name)}</strong>${e(l.lot)} · ${l.scanned} / ${l.qty}</div>`).join('')}`;
 if(mode==='Ship'){
  if(!c?.sealed)return body+'<p>This shipment needs scanned packing before mobile dispatch.</p></article>';
  return body+`<h3>Reviewed cartons</h3>${c.cartons.map(x=>`<p data-l10n-skip>${e(x.code)} · ${e(x.name)}</p>`).join('')}<p data-l10n-skip>${e(v.shipment.carrier)} · ${e(v.shipment.tracking)}</p></article>`+form('shipShipment',scanField('shipmentCode','Shipment barcode')+'<label>Carton barcodes (one per line)<textarea name="cartonCodes" required rows="3"></textarea></label><button type="button" data-scan-target="cartonCodes">Camera</button>'+checks,'Dispatch reviewed shipment');
 }
 if(!c)return body+button('Start scanned packing','warehouse:openPack')+'</article>';
 if(c.reversed)return body+form('warehouse:resetPack',input('reason','Reset reason','','text','required')+checks,'Reset scanned packing')+'</article>';
 body+=c.cartons.map(box=>`<section class="execution-slot"><h3 data-l10n-skip>${e(box.code)}</h3><p data-l10n-skip>${e(box.name)} · ${Object.values(box.counts).reduce((n,l)=>n+l.qty,0)}</p></section>`).join('');
 body+='<p><a href="./execution-labels.html?shipment='+encodeURIComponent(id)+'" target="_blank">Print carton barcodes</a></p></article>';
 return body+form('warehouse:addCarton',input('name','Carton name','','text','maxlength="60"'),'Add scan carton')+(c.cartons.length?form('warehouse:scanPack',scanField('cartonCode','Carton barcode')+scanField('code','Barcode or SKU')+scanField('lot','Lot / batch')+input('qty','Quantity',1,'number','required min="1" step="1"')+serials,'Save carton scan')+form('warehouse:sealPack',input('carrier','Carrier / local delivery','','text','required maxlength="240"')+input('tracking','Tracking reference')+input('service','Carrier service')+checks,'Seal scanned packing'):'');
}
