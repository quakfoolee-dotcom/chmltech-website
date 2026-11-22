import {productUnits} from './packaging.mjs?demo=5d9e5d1ce6c83eb1';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function packagingPanel(s){
 const rows=s.items.flatMap(item=>productUnits(s,item.id,{inactive:true}).map(u=>`<tr><td data-l10n-skip>${e(item.sku)}<br>${e(item.name)}</td><td data-l10n-skip>${e(u.code)} · ${e(u.name)}</td><td data-l10n-skip>1 ${e(u.code)} = ${u.factor} ${e(item.uom)}</td><td data-l10n-skip>${e(u.barcode)}</td><td><span>${u.active?'Active':'Archived'}</span></td><td><a class="btn" href="./warehouse-labels.html?item=${encodeURIComponent(item.id)}" target="_blank">Print unit labels</a>${u.active?` <button class="btn" data-action="biz-unitEdit" data-id="${e(u.id)}" data-item="${e(item.id)}" aria-label="Edit UoM for ${e(item.sku)} ${e(u.code)}">Edit UoM</button>`:''}${u.id==='base'?'':` <button class="btn" data-action="biz-unitStatus" data-id="${e(u.id)}" data-item="${e(item.id)}" data-active="${!u.active}">${u.active?'Archive unit':'Activate unit'}</button>`}</td></tr>`));
 return {intro:'Edit units without rewriting existing stock or order conversions.',actions:'<button class="btn" data-action="biz-unitNew">New packaging unit</button><button class="btn" data-action="biz-purchase">New purchase order</button><button class="btn" data-action="biz-sale">New sales order</button>',body:`<p>Purchase, receive, move and sell in packs while stock stays in base units.</p><div class="table-scroll"><table><thead><tr>${['Product','Packaging unit','Conversion','Barcode','Status','Actions'].map(v=>`<th>${v}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`};
}
export async function packagingAction(act,id,el,ctx){
 if(!['unitNew','unitEdit','unitStatus'].includes(act))return false;
 const {s,run,showModal,select,itemOptions,field}=ctx;
 if(act==='unitStatus'){await run('units:active',{itemId:el.dataset.item,id,active:el.dataset.active==='true'});return true;}
 if(act==='unitEdit'){
  const item=s.items.find(i=>i.id===el.dataset.item),unit=productUnits(s,item.id).find(u=>u.id===id);if(!unit)throw Error('The selected packaging unit is unavailable.');
  const base=id==='base',preferred=s.business?.profiles[item.id],nameMax=preferred?.packSize===unit.factor&&preferred?.packName===unit.name?30:60;
  const readonly=base?' readonly':'';
  showModal('Edit UoM',`<p data-l10n-skip>${e(item.sku)} — ${e(item.name)}</p>`+field('Unit code','code','text',unit.code,'required maxlength="20"'+readonly)+field('Unit name','name','text',unit.name,`required maxlength="${nameMax}"`)+field('Base units per pack','factor','number',unit.factor,base?'readonly':'required min="2" max="1000000" step="1"')+field('Packaging barcode','barcode','text',unit.barcode,'required maxlength="100"'+readonly)+`<p>${base?'Only the display name can change. The base stock unit stays the same.':'Changing the conversion creates a replacement unit and archives this one. Existing orders keep their original conversion. Print new labels after changing a barcode or conversion.'}</p>`,'Save UoM',data=>run('units:save',{...data,itemId:item.id,id}));
  return true;
 }
 showModal('New packaging unit',select('Product','itemId',itemOptions())+field('Unit code','code','text','','required maxlength="20" placeholder="CARTON12"')+field('Unit name','name','text','','required maxlength="60" placeholder="Carton / 纸箱 / 紙箱"')+field('Base units per pack','factor','number','12','required min="2" max="1000000" step="1"')+field('Packaging barcode','barcode','text','','required maxlength="100"')+'<p>Conversions are fixed when saved. Existing costs and order conversions are preserved.</p>','Save packaging unit',data=>run('units:save',data));
 return true;
}
export function unitLineOptions(s,itemId,buying=false){const units=productUnits(s,itemId,{legacy:buying}),p=s.business?.profiles[itemId],defaultId=buying&&p?.packSize>1?units.find(u=>u.factor===p.packSize&&u.name===p.packName)?.id||'base':'base';return units.map(u=>`<option value="${e(u.id)}"${u.id===defaultId?' selected':''} data-l10n-skip>${e(u.code)} · ${e(u.name)} (× ${u.factor})</option>`).join('');}

