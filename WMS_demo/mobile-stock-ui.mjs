import {stockLookup} from './mobile-stock.mjs?demo=45f52980507d3a1b';
import {productUnits,resolveProductBarcode,scannedQuantity} from './packaging.mjs?demo=45f52980507d3a1b';
import {translate} from './locale.mjs?demo=45f52980507d3a1b';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const field=(key,label,value='',extra='')=>`<label>${label}<input name="${key}" value="${e(value)}" ${extra}></label>`;
const scan=(key,label,value='')=>field(key,label,value,'required autocomplete="off"')+`<button type="button" data-scan-target="${key}">Camera</button>`;
export function stockWorkHTML(s,mode,warehouse,query=''){
 if(mode==='Move')return `<article><h2>Move stock</h2><p>Scan both bins and the exact product and lot. Only free stock in this warehouse can move.</p><p>Packaging counts are converted to base stock units before saving.</p></article><form data-execution="mobile:move">${scan('sourceCode','Source bin barcode')}${scan('code','Barcode or SKU')}${scan('lot','Lot / batch')}<label>Packaging unit<select name="unitId"><option value="base">Stock units</option></select></label>${field('qty','Quantity',1,'type="number" required min="1" step="1"')}<output class="conversion-preview" data-unit-preview aria-live="polite">Scan a product to see its packaging units.</output>${scan('destinationCode','Destination bin barcode')}<label>Serial numbers, if tracked<textarea name="serials" rows="3" placeholder="One serial per line"></textarea></label><label class="move-review"><input type="checkbox" name="reviewed" required><span>I reviewed both bins, the lot and the converted quantity.</span></label><button class="primary full">Save stock move</button></form>`;
 let body=`<article><h2>Stock lookup</h2><p>Scan a product, packaging barcode or location. Lookup does not change stock.</p></article><form data-stock-lookup>${scan('code','Product or location barcode',query)}<button class="primary full">Look up stock</button></form>`;
 if(!query)return body;
 try{
  const result=stockLookup(s,{warehouseId:warehouse,code:query});
  body+=`<article><h2>Stock results</h2>${result.product?`<h3 data-l10n-skip>${e(result.product.sku)} · ${e(result.product.name)}</h3><p data-l10n-skip>${e(result.product.description)}</p>`:''}${result.location?`<h3 data-l10n-skip>${e(result.location.code)} · ${e(result.location.name)}</h3>`:''}<dl class="stock-summary"><dt>On hand</dt><dd>${result.onHand}</dd><dt>Reserved</dt><dd>${result.reserved}</dd><dt>Available</dt><dd>${result.available}</dd></dl>${!result.rows.length?'<p>No stock in the selected warehouse.</p>':''}${result.rows.map(r=>`<section class="execution-slot"><strong data-l10n-skip>${e(r.sku)} · ${e(r.name)}</strong><p data-l10n-skip>${e(r.location)} · ${e(r.locationName)}<br>${e(r.lot)}<br>${e(r.owner)}</p><dl class="stock-summary"><dt>On hand</dt><dd>${r.qty} <span data-l10n-skip>${e(r.uom)}</span></dd><dt>Reserved</dt><dd>${r.reserved}</dd><dt>Available</dt><dd>${r.available}</dd></dl>${r.held?'<p>Held or controlled stock</p>':''}${r.expired?'<p>Expired lot</p>':''}${r.expiresOn?`<p><span>Expiry date</span>: <span data-l10n-skip>${e(r.expiresOn)}</span></p>`:''}${r.serials.length?`<details><summary>Serial numbers</summary><p data-l10n-skip>${r.serials.map(e).join('<br>')}</p></details>`:''}</section>`).join('')}</article>`;
 }catch(err){body+=`<article role="alert"><p>${e(translate(err.message))}</p></article>`;}
 return body;
}
export function updateUnitPreview(form,s,{productChanged=false}={}){
 const code=form?.querySelector('[name="code"]');if(!code)return;
 const preview=form.querySelector('[data-unit-preview]'),select=form.querySelector('[name="unitId"]');if(!select||!preview)return;
 try{
  const match=resolveProductBarcode(s,code.value);
  if(productChanged||select.dataset.item!==match.item.id){
   select.innerHTML=productUnits(s,match.item.id).map(u=>`<option data-l10n-skip value="${e(u.id)}">${e(u.code)} · ${e(u.name)} = ${u.factor} ${e(match.item.uom)}</option>`).join('');
   select.dataset.item=match.item.id;select.value=match.unit.id;
  }
  const capture=scannedQuantity(s,{code:code.value,unitId:select.value,qty:form.querySelector('[name="qty"]').value});
  preview.dataset.l10nSkip='';preview.textContent=`${capture.quantity} ${capture.name} × ${capture.factor} = ${capture.baseQty} ${match.item.uom}`;
 }catch(err){delete preview.dataset.l10nSkip;preview.textContent=code.value?translate(err.message):translate('Scan a product to see its packaging units.');}
}
