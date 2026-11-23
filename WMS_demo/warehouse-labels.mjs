import {api} from './shared.mjs?demo=9c44c6dabb8d4728';
import {warehouseLabelRows} from './warehouse-label-model.mjs?demo=9c44c6dabb8d4728';
import {barcodeSVG} from './barcode.mjs?demo=9c44c6dabb8d4728';
import {qrSVG} from './scan-codes.mjs?demo=9c44c6dabb8d4728';
import {interfaceLanguage,startLocalization} from './locale.mjs?demo=9c44c6dabb8d4728';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let state;
try{
 state=(await api('workspace')).state;
 const query=new URLSearchParams(location.search),warehouse=document.querySelector('#warehouse');
 warehouse.innerHTML=state.business.warehouses.map(w=>`<option data-l10n-skip value="${e(w.id)}">${e(w.name)}</option>`).join('');
 warehouse.value=query.get('warehouse')||'wh-main';if(!warehouse.value)warehouse.value='wh-main';
 function draw(){document.querySelector('#labels').innerHTML=warehouseLabelRows(state,{warehouseId:warehouse.value,itemId:query.get('item')||''}).map(r=>{
  const qr=r.qr||r.code.length>35||!/^[A-Z0-9 .$/+%\-]+$/.test(r.code);
  return `<section class="scan-label"><h2>${r.caption}</h2><p data-l10n-skip>${e(r.description)}</p><div data-l10n-skip class="${qr?'qr':''}">${qr?qrSVG(r.code,r.code):barcodeSVG(r.code).replace('<svg ','<svg preserveAspectRatio="none" ').replace(/<g fill="black" text-anchor="middle"[\s\S]*?<\/g>/,'')}</div><p data-l10n-skip>${e(r.code)}</p></section>`;
 }).join('');}
 warehouse.onchange=draw;draw();
}catch(err){document.querySelector('#labels').textContent=err.message;}
document.querySelector('#print').onclick=()=>window.print();document.querySelector('#interface-language').value=interfaceLanguage();startLocalization(()=>state);
