import {commandRoleAllowed} from './command-policy.mjs?demo=9c44c6dabb8d4728';
import {dateInputBounds} from './date-input.mjs?demo=9c44c6dabb8d4728';
import {stockWorkHTML,updateUnitPreview} from './mobile-stock-ui.mjs?demo=9c44c6dabb8d4728';
import {mountAccount} from './account.mjs?demo=9c44c6dabb8d4728';
import {scannerMarkup,mountScanner} from './camera-scanner.mjs?demo=9c44c6dabb8d4728';
import {executionCandidates,executionWorkHTML,groupCreationHTML} from './mobile-execution-ui.mjs?demo=9c44c6dabb8d4728';
import {pickLines} from './fulfillment.mjs?demo=9c44c6dabb8d4728';
import {interfaceLanguages,interfaceLanguage,startLocalization,translate} from './locale.mjs?demo=9c44c6dabb8d4728';
import {api} from './shared.mjs?demo=9c44c6dabb8d4728';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const app=document.querySelector('#app'),notice=document.querySelector('#notice');let state,user,mode=({group:'Group',pack:'Pack',ship:'Ship',move:'Move',lookup:'Lookup'}[location.hash.slice(1)]||'Receive'),warehouse='wh-main',record='',busy=false,cameraReader,lookupCode='';
const scope=id=>state.business?.locationMeta[id]||{warehouseId:'wh-main',ownerId:'owner-self'};
const warehouses=()=>state.business?.warehouses||[{id:'wh-main',name:'Vancouver warehouse'}];
const select=(name,label,rows,value='')=>`<label>${e(label)}<select name="${name}">${rows.map(([id,title])=>`<option value="${e(id)}" ${id===value?'selected':''}>${e(title)}</option>`).join('')}</select></label>`;
const input=(name,label,value='',type='text',extra='')=>`<label>${e(label)}<input name="${name}" type="${type}" ${dateInputBounds(type)} value="${e(value)}" ${extra}></label>`;
function message(text,error=false){notice.textContent=text;notice.className=error?'error':'success';}
async function refresh(){stopCamera();try{const status=await api('status');user=status.user;account.observe(status);if(!user){signedOut();return;}state=(await api('workspace')).state;if(!state)throw Error('Open Chmltech WMS on the host computer and load its workspace first.');draw();}catch(err){message(err.message,true);}}
function candidates(){
 if(['Group','Pack','Ship'].includes(mode))return executionCandidates(state,mode,warehouse);
 if(mode==='Receive')return (state.operations?.purchases||[]).filter(p=>p.status==='Open'&&p.kind==='Warehouse'&&(p.scope?.warehouseId||'wh-main')===warehouse).map(p=>[p.id,p.number+' · '+p.supplier]);
 if(mode==='Pick')return state.picks.filter(p=>p.status==='Committed'&&(state.orders.find(o=>o.id===p.orderId)?.scope?.warehouseId||'wh-main')===warehouse).map(p=>[p.id,p.number+' · '+state.orders.find(o=>o.id===p.orderId).customer]);
 return state.stock.filter(r=>r.qty>0&&scope(r.locationId).warehouseId===warehouse&&!scope(r.locationId).transit&&!scope(r.locationId).production&&['Storage','Receiving','Hold'].includes(state.locations.find(l=>l.id===r.locationId).type)).map(r=>[r.id,state.items.find(i=>i.id===r.itemId).sku+' · '+state.locations.find(l=>l.id===r.locationId).code+' · '+r.lot]);
}
function draw(){
 if(['Move','Lookup'].includes(mode)){
  app.innerHTML=`<h1>Warehouse scanning</h1><p><a href="./scan.html">Scan to open documents</a></p>${select('warehouse','Warehouse',warehouses().map(w=>[w.id,w.name]),warehouse)}<nav class="modes">${['Lookup','Move','Receive','Pick','Group','Pack','Ship','Count'].map(m=>`<button type="button" data-mode="${m}" aria-pressed="${mode===m}">${m==='Group'?'Grouped picking':m}</button>`).join('')}</nav>${stockWorkHTML(state,mode,warehouse,lookupCode)}`;
  enhanceUnits();return;
 }
 const choices=candidates();if(!choices.some(([id])=>id===record))record=choices[0]?.[0]||'';
 if(['Group','Pack','Ship'].includes(mode)){
  app.innerHTML=`<h1>Warehouse scanning</h1><p><a href="./scan.html">Scan to open documents</a></p>${select('warehouse','Warehouse',warehouses().map(w=>[w.id,w.name]),warehouse)}<nav class="modes">${['Lookup','Move','Receive','Pick','Group','Pack','Ship','Count'].map(m=>`<button type="button" data-mode="${m}" aria-pressed="${mode===m}">${m==='Group'?'Grouped picking':m}</button>`).join('')}</nav>${mode==='Group'?groupCreationHTML(state,warehouse):''}${choices.length?select('record',mode==='Group'?'Pick group':'Shipment',choices,record):'<p>No matching work in this warehouse.</p>'}${record?executionWorkHTML(state,mode,record):''}<p>Changes are saved in this browser only. No carrier booking or postage purchase.</p>`;enhanceUnits();return;
 }
 app.innerHTML=`<h1>Warehouse scanning</h1><p><a href="./scan.html">Scan to open documents</a></p><p class="muted">${e(user.name)} · ${e(user.role)}.</p><p class="muted">Changes are saved in this browser only.</p>${select('warehouse','Warehouse',warehouses().map(w=>[w.id,w.name]),warehouse)}<nav class="modes">${['Lookup','Move','Receive','Pick','Group','Pack','Ship','Count'].map(m=>`<button type="button" data-mode="${m}" aria-pressed="${mode===m}">${m==='Group'?'Grouped picking':m}</button>`).join('')}</nav>${choices.length?select('record',mode==='Receive'?'Purchase order':mode==='Pick'?'Committed pick':'Stock row',choices,record):`<article><p>No ${mode==='Receive'?'open warehouse purchase orders':mode==='Pick'?'committed picks':'countable stock'} in this warehouse.</p><p class="muted">Prepare the work in Chmltech WMS on the host computer, then refresh.</p></article>`}<div id="work"></div><p class="muted">Use a keyboard scanner, type a SKU, or choose Camera. Each scan must be saved once.</p><div class="actions"></div>`;
 if(!record)return;
 const po=state.operations?.purchases.find(p=>p.id===record),pick=state.picks.find(p=>p.id===record),stock=state.stock.find(r=>r.id===record);let detail='',extra='';
 if(mode==='Receive'){
  const lines=po.lines||[{itemId:po.itemId,qty:po.qty,received:po.received}];detail=lines.map(l=>`<div class="product"><strong>${e(state.items.find(i=>i.id===l.itemId).name)}</strong>${e(state.items.find(i=>i.id===l.itemId).sku)} · ${l.qty-l.received} remaining</div>`).join('');
  const sc=po.scope||{warehouseId:'wh-main',ownerId:'owner-self'};extra=select('locationId','Receive into',state.locations.filter(l=>['Storage','Receiving','Hold'].includes(l.type)&&!scope(l.id).transit&&scope(l.id).warehouseId===sc.warehouseId&&scope(l.id).ownerId===sc.ownerId).map(l=>[l.id,l.code+' · '+l.name]))+input('lot','Lot / batch')+input('expiresOn','Expiry date','','date')+input('reference','Delivery reference');
 }else if(mode==='Pick'){const order=state.orders.find(o=>o.id===pick.orderId);detail=pickLines(state,pick).map(l=>`<div class="product"><strong>${e(state.items.find(i=>i.id===l.itemId).name)}</strong>${e(state.items.find(i=>i.id===l.itemId).sku)} · ${pick.scanCounts?.[l.itemId]||0} / ${l.qty} scanned</div>`).join('');}
 else {const i=state.items.find(i=>i.id===stock.itemId);detail=`<div class="product"><strong>${e(i.name)}</strong>${e(i.description)}<br>${e(stock.lot)} · ${stock.qty} recorded</div>`;extra=input('reason','Count reason','','text','required');}
 document.querySelector('#work').innerHTML=`<article>${detail}</article><form id="scan">${input('code','Barcode or SKU','','text','required autocomplete="off" autocapitalize="off"')}<button type="button" id="open-camera">Camera</button>${input('qty',mode==='Count'?'Actual counted quantity':'Quantity',mode==='Count'?'':'1','number',`required min="${mode==='Count'?0:1}" step="1"`)}${extra}${mode!=='Pick'?'<label>Serial numbers, if tracked<textarea name="serials" rows="3" placeholder="One serial per line"></textarea></label>':''}<button class="primary full" type="submit">${mode==='Count'?'Save count':'Save scan'}</button></form>${mode==='Pick'?'<button type="button" class="full" id="finish-pick">Finish scanned pick</button>':''}`;
 enhanceUnits();
}
function applyMobileRoles(){
 for(const form of app.querySelectorAll('form')){const command=form.dataset.execution||(form.id==='scan'?'business:scan':null);if(command&&!commandRoleAllowed(command,user?.role)){for(const b of form.querySelectorAll('button[type="submit"],button:not([type])')){b.disabled=true;b.title=translate('Your role cannot perform this action.');}}}
 for(const b of app.querySelectorAll('button[data-execution],#finish-pick'))if(!commandRoleAllowed(b.dataset.execution||'business:finishScannedPick',user?.role)){b.disabled=true;b.title=translate('Your role cannot perform this action.');}
 if(user?.role==='Viewer'&&!app.querySelector('.role-notice')){const p=document.createElement('p');p.className='role-notice';p.textContent=translate('Your Viewer account can browse records. Saving changes requires an authorized role.');app.prepend(p);}
}
function enhanceUnits(){
 applyMobileRoles();
 for(const form of app.querySelectorAll('form')){
  const code=form.querySelector('[name="code"]'),quantity=form.querySelector('[name="qty"]');
  if(!code||!quantity||form.querySelector('[name="unitId"]'))continue;
  quantity.closest('label').insertAdjacentHTML('beforebegin','<label>Packaging unit<select name="unitId"><option value="base">Stock units</option></select></label>');
  quantity.closest('label').insertAdjacentHTML('afterend','<output class="conversion-preview" data-unit-preview aria-live="polite">Scan a product to see its packaging units.</output>');
 }
}
app.addEventListener('input',event=>{if(['code','qty','unitId'].includes(event.target.name)&&state)updateUnitPreview(event.target.closest('form'),state,{productChanged:event.target.name==='code'});});
app.addEventListener('change',event=>{if(['qty','unitId'].includes(event.target.name)&&state)updateUnitPreview(event.target.closest('form'),state);});
async function save(command,payload){if(busy)return;if(!commandRoleAllowed(command,user?.role)){message(translate('Your role cannot perform this action.'),true);return;}const priorInert=app.inert,priorBusy=document.body.getAttribute('aria-busy');busy=true;app.inert=true;document.body.setAttribute('aria-busy','true');document.querySelectorAll('button').forEach(b=>b.disabled=true);try{const r=await api('command',{command,payload,revision:state.revision});state=r.state;if(command==='warehouse:createGroup')record=r.resultId;draw();message(translate('Saved.')+' '+translate(r.state.events[0].type));document.querySelector('[name="code"]')?.focus();}catch(err){await refresh();message(translate(err.message)+' '+translate('Nothing was automatically retried. Review the current record before scanning again.'),true);}finally{busy=false;app.inert=priorInert;if(priorBusy===null)document.body.removeAttribute('aria-busy');else document.body.setAttribute('aria-busy',priorBusy);document.querySelectorAll('button').forEach(b=>b.disabled=false);applyMobileRoles();}}
app.addEventListener('change',ev=>{if(ev.target.name==='warehouse'){stopCamera();warehouse=ev.target.value;record='';draw();}if(ev.target.name==='record'){stopCamera();record=ev.target.value;draw();}});
app.addEventListener('submit',async ev=>{ev.preventDefault();const data=new FormData(ev.target),d=Object.fromEntries(data);if(ev.target.dataset.stockLookup!==undefined){lookupCode=d.code;try{state=(await api('workspace')).state;draw();message('');}catch(err){message(err.message,true);}return;}if(ev.target.dataset.execution){const command=ev.target.dataset.execution;await save(command,{...d,id:record,warehouseId:warehouse,pickIds:data.getAll('pickIds'),reviewed:d.reviewed==='on',mobile:command==='shipShipment',requestId:crypto.randomUUID()});return;}if(ev.target.id==='login'){try{await api('login',d);ev.target.reset();await refresh();message('Signed in.');}catch(err){message(err.message,true);}return;}if(ev.target.id==='scan')await save('business:scan',{...d,mode,...(mode==='Receive'?{purchaseId:record}:mode==='Pick'?{pickId:record}:{stockId:record})});});
app.addEventListener('click',async ev=>{const b=ev.target.closest('button');if(!b)return;if(b.dataset.mode){stopCamera();mode=b.dataset.mode;record='';draw();message('');}if(b.dataset.execution)await save(b.dataset.execution,{id:record});if(b.dataset.scanTarget)await camera(b.dataset.scanTarget,b.closest('form'));if(b.id==='logout'){await api('logout',{});await refresh();}if(b.id==='finish-pick')await save('business:finishScannedPick',{id:record});if(b.id==='open-camera')await camera();});
function stopCamera(){cameraReader?.dispose();cameraReader=null;const dialog=document.querySelector('#camera');if(dialog.open)dialog.close();}
async function camera(target='code',form=null){const dialog=document.querySelector('#camera');dialog.querySelector('#camera-reader').innerHTML=scannerMarkup().replace('Document barcode or QR','Barcode or SKU').replace('INV-118, PO-25 or SH-3128','Barcode or SKU').replace('Open document','Use barcode').replace('Camera images are decoded on this device. Scanning a document does not change stock or accounting.','The camera fills the selected field. Review quantities and save the scan to update the warehouse.');dialog.showModal();cameraReader=mountScanner(dialog.querySelector('.scan-reader'),{onRead:text=>{const field=(form||app).querySelector(`[name="${target}"]`);if(!field?.isConnected){stopCamera();return;}if(target==='cartonCodes')field.value+=(field.value?'\n':'')+text;else field.value=text;field.dispatchEvent(new Event('input',{bubbles:true}));stopCamera();message('Barcode read. Review quantity, then save.');}});}
document.querySelector('#stop-camera').onclick=stopCamera;document.querySelector('#camera').addEventListener('cancel',stopCamera);document.querySelector('#refresh').onclick=refresh;window.addEventListener('pagehide',stopCamera);

const mobileLanguage=document.createElement('label');mobileLanguage.className='language-switch';mobileLanguage.innerHTML='<span>Language</span><select id="interface-language" aria-label="Interface language">'+interfaceLanguages.map(([code,label])=>'<option value="'+code+'"'+(code===interfaceLanguage()?' selected':'')+'>'+label+'</option>').join('')+'</select>';document.querySelector('header').append(mobileLanguage);startLocalization(()=>state);

function signedOut(){stopCamera();state=undefined;app.innerHTML='<h1>Sign in to Chmltech WMS</h1><p>Use Sign in at the top right to open the shared workspace.</p><button type="button" data-account-action="signin">Sign in</button>';}
const accountHost=document.createElement('div');accountHost.dataset.accountHost='';document.querySelector('header').append(accountHost);
const account=mountAccount({onChange:(status,expired)=>{user=status.user;if(!user){signedOut();message(expired?'Your session expired. Sign in again to continue.':'');}},afterSignIn:refresh,beforeSignOut:stopCamera});
refresh();
