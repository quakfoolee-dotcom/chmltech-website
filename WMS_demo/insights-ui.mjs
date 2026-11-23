import {interfaceLanguage,translate,translatedWords} from './locale.mjs?demo=2d15b6e9cd84b84d';
import {business,locationScope} from './business.mjs?demo=2d15b6e9cd84b84d';
import {insights,countableLocations,countIsStale,countCSV,traceReport,warehouseReport,reportTypes,reportCSV} from './insights.mjs?demo=2d15b6e9cd84b84d';
import {documentHTML,languages} from './documents.mjs?demo=2d15b6e9cd84b84d';
import {createDocumentPDF} from './pdf.mjs?demo=2d15b6e9cd84b84d';

const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const button=(label,action,id='')=>`<button type="button" class="btn" data-action="ins-${action}" data-id="${e(id)}">${e(label)}</button>`;
const row=cells=>`<tr>${cells.map(c=>`<td>${c}</td>`).join('')}</tr>`;
const table=(headers,rows)=>`<div class="table-scroll"><table><thead><tr>${headers.map(h=>`<th>${e(h)}</th>`).join('')}</tr></thead><tbody>${rows.join('')||`<tr><td colspan="${headers.length}">No matching records.</td></tr>`}</tbody></table></div>`;
const area=(label,name,value='')=>`<label class="field">${e(label)}<textarea name="${e(name)}" rows="4">${e(value)}</textarea></label>`;
const note=v=>`<div class="note-box"><p>${e(v)}</p></div>`;
let selectedCount='',traceQuery='',traceItem='',reportType='valuation',filters={},preview=null,language='zh-Hans',lastReportRoute='';
const fontCache=new Map();
export const insightSections=[['counts','Cycle counts'],['trace','Traceability & recalls'],['reports','Report centre']];

export function insightView(s,section){
 const d=insights(s),b=business(s),item=id=>s.items.find(i=>i.id===id),loc=id=>s.locations.find(l=>l.id===id)?.code||id;
 let actions='',body='',intro='';
 if(section==='counts'){
  actions=button('New count session','create');intro='Count → review variances → approve adjustments. Existing stock stays unchanged until an administrator posts the count.';
  const c=d.counts.find(c=>c.id===selectedCount)||d.counts.at(-1);
  body=table(['Session','Name','Status','Progress','Round',''],[...d.counts].reverse().map(c=>row([e(c.number),e(c.name),e(c.status),`${c.lines.filter(l=>l.counted!==null).length} / ${c.lines.length}`,c.round,button('Open count','open',c.id)])));
  if(c){
   const editable=c.status==='Counting',active=['Counting','Review'].includes(c.status),visible=!c.blind||!editable,stale=active&&countIsStale(s,c);
   body+=`<div class="insight-detail"><div class="page-head"><div><h2>${e(c.number)} · ${e(c.name)}</h2><p>${e(c.status)} · round ${c.round} · ${e(c.scope.locationId?loc(c.scope.locationId):'All countable locations')} · ${e(b.warehouses.find(w=>w.id===c.scope.warehouseId)?.name)} · ${e(b.owners.find(o=>o.id===c.scope.ownerId)?.name)}</p></div><div class="actions">${button('Export count CSV','countExport',c.id)}${button('Count sheet / PDF','countPreview',c.id)}${editable?button('Submit for review','submit',c.id):''}${c.status==='Review'?button('Approve & post','approve',c.id):''}${active?button('Start recount','recount',c.id)+button('Cancel session','cancel',c.id):''}</div></div>`;
   if(stale)body+=`<div class="alert" role="status">Stock changed in this count’s locations. Start a recount before submitting or posting. Your previous round will be kept.</div>`;
   body+=note(editable&&c.blind?'Blind entry: expected quantities stay hidden on this sheet until review. Count every row, including zero. Record unexpected products through Receiving, then recount. This hides figures for counting; it is not a restriction on Inventory access.':'Review quantities and serial numbers before approval. Posting applies the entire session together; reserved stock cannot be removed.');
   body+=table(['Product / description','Location / lot',...(visible?['Expected']:[]),'Counted',...(visible?['Variance']:[]),'Serials / note',''],c.lines.map(l=>row([`${e(item(l.itemId)?.sku)}<br><strong>${e(item(l.itemId)?.name)}</strong><br>${e(item(l.itemId)?.description||'')}`,`${e(loc(l.locationId))}<br>${e(l.lot)}`,...(visible?[l.expected]:[]),l.counted===null?'Not counted':l.counted,...(visible?[l.counted===null?'—':l.counted-l.expected]:[]),`${e(l.tracked?'Serial tracked':'Lot tracked')}<br>${e(l.countedSerials.join(', '))}<br>${e(l.note)}`,editable?button(l.counted===null?'Enter count':'Edit count','entry',`${c.id}|${l.stockId}`):e(l.enteredBy)])));
   if(c.status==='Posted')body+=note(`Posted by ${c.approvedBy} at ${c.approvedAt}. ${c.approvalReason}`);
   if(c.rounds.length)body+=`<h3>Previous rounds</h3>`+table(['Round','Recount reason','Counted rows',''],c.rounds.map(r=>row([r.round,e(r.reason),`${r.lines.filter(l=>l.counted!==null).length} / ${r.lines.length}`,button('Download round CSV','roundExport',`${c.id}|${r.round}`)])));
   body+=`<details><summary>Session history</summary>${table(['Time (UTC)','Action','Operator'],c.history.map(h=>row([e(h.time),e(h.action),e(h.actor)])))}</details></div>`;
  }else body+=note('Start with one storage or receiving location. Staging, in-transit and production-controlled locations are excluded.');
 }
 if(section==='trace'){
  actions=button('Search lot / serial','traceSearch');intro='Follow a lot or serial through suppliers, stock locations, production and customer shipments.';
  if(!traceQuery)body=note('Search an exact lot or serial number. You can copy one from Inventory → product → stock rows. Chinese lot and serial text is supported.');
  else{
   const t=traceReport(s,traceQuery,traceItem);actions+=button('Export trace JSON','traceExport')+button('Recall preview / PDF','tracePreview');
   body=`<h2>Trace: ${e(traceQuery)}</h2>`+note(t.note)+(t.nodes.length?'':note('No matching lot or serial was found. Try an exact value and check the product filter.'));
   body+=`<h3>Current stock · searched lot and downstream lots</h3>`+table(['Product','Location','Lot','Bucket quantity','Matched serial','Status'],t.inventory.map(r=>row([`${e(item(r.itemId)?.sku)}<br>${e(item(r.itemId)?.name)}`,e(loc(r.locationId)),e(r.lot),r.qty,e(r.matchedSerials.join(', ')||'Lot scope'),e(s.locations.find(l=>l.id===r.locationId)?.type)])));
   body+=`<h3>Supplier receipts · searched lot and upstream materials</h3>`+table(['Purchase / receipt','Supplier','Date','Product / lot','Receipt quantity'],t.purchases.map(({purchase:p,receipt:r,line:l})=>row([`<a href="#purchasing/${e(p.id)}">${e(p.number)}</a><br>${e(r.id)}`,e(p.supplier),e(r.time.slice(0,10)),`${e(item(l.itemId)?.name)}<br>${e(l.lot)}`,l.qty])));
   body+=`<h3>Potentially affected customer shipments</h3>`+note('Only rows marked Shipped are active shipments. Reversed records remain as history. Quantity is the shipment’s lot quantity; a serial search lists the matching serial separately. This report does not contact customers or place stock on hold.');
   body+=table(['Shipment / order','Customer','Shipped (UTC)','Status','Product / lot / quantity','Matched serial'],t.customers.map(sh=>row([`${e(sh.number)}<br><a href="#orders/${e(sh.orderId)}">${e(sh.orderNumber)}</a>`,e(sh.customer),e(sh.time||'Unknown'),e(sh.status==='Shipped'?'Shipped':'Reversed / '+sh.status),sh.allocations.map(a=>`${e(item(a.itemId)?.name)} / ${e(a.lot)} × ${a.qty}`).join('<br>'),e(sh.allocations.flatMap(a=>t.descendants.filter(n=>n.serial&&n.itemId===a.itemId&&n.lot===a.lot&&a.serials?.includes(n.serial)).map(n=>n.serial)).join(', ')||'Lot scope')])));
   body+=`<h3>Production and return links</h3>`+table(['Reference','Type','Input lots','Output lot','Evidence'],t.links.map(l=>row([e(l.reference),e(l.type),l.inputs.map(n=>`${e(item(n.itemId)?.sku)} / ${e(n.lot)}`).join('<br>'),`${e(item(l.output.itemId)?.sku)} / ${e(l.output.lot)}`,e(l.uncertain?'Possible sources; mixed return':'Recorded link')])));
   if(t.unlinkedBuilds.length)body+=note(`${t.unlinkedBuilds.map(w=>w.number).join(', ')} consumed a matching lot before output-lot recording was enabled. Inspect these builds manually.`);
   body+=`<h3>Retained movements</h3>`+table(['Time (UTC)','Action / reference','Product / lot','Location','Quantity change'],t.movements.slice().reverse().flatMap(m=>m.changes.map(c=>row([e(m.time),`${e(m.description)}<br>${e(m.reference)}`,`${e(item(c.itemId)?.sku)} / ${e(c.lot)}`,e(loc(c.locationId)),c.quantity]))));
  }
 }
 if(section==='reports'){
  if(typeof location!=='undefined'&&lastReportRoute!==location.hash){const requested=location.hash.split('/')[2];if(reportTypes.some(([id])=>id===requested))reportType=requested;lastReportRoute=location.hash;}
  const r=warehouseReport(s,reportType,filters);intro='Filtered warehouse reports, UTF-8 CSV exports and printable documents with Chinese fonts.';
  actions=button('Choose report & filters','reportFilter')+button('Download report CSV','reportExport')+button('Preview / PDF','reportPreview');
  body=`<div class="report-choices">${reportTypes.map(([k,title])=>button(title,'reportType',k)).join('')}</div><h2>${e(r.title)}</h2><p>Warehouse: ${e(b.warehouses.find(w=>w.id===filters.warehouseId)?.name||'All')} · Owner: ${e(b.owners.find(o=>o.id===filters.ownerId)?.name||'All')} · Product: ${e(item(filters.itemId)?.name||'All')} · Dates: ${e(r.filters.from||'Any')} to ${e(r.filters.to||'Any')}</p>`+note(r.note);
  if(reportType==='valuation')body+=`<div class="insight-summary"><strong>Known value: ${e(b.homeCurrency)} ${r.knownValue.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}</strong><span>Unvalued units: ${r.unknownUnits}</span></div>`;
  body+=`<p>${r.rows.length} rows · Generated ${e(r.generatedAt)}</p>`+table(r.headers,r.rows.map(c=>row(c.map(e))));
 }
 return {actions,body,intro};
}

export function reportDoc(report,locale){
 const w=locale==='zh-Hant'?{title:'倉庫報表',generated:'產生時間',footer:'本地倉庫報表。請留意歷史資料的完整性。',page:'頁',continued:'續頁'}:locale==='zh-Hans'?{title:'仓库报表',generated:'生成时间',footer:'本地仓库报表。请留意历史数据的完整性。',page:'页',continued:'续页'}:{title:'Warehouse report',generated:'Generated',footer:'Local warehouse report. Review history coverage before use.',page:'Page',continued:'continued'};
 if(locale==='fr')Object.assign(w,translatedWords(w,'fr'));
 return [{locale,title:w.title,ref:report.title,size:'A4',footer:w.footer,pageWord:w.page,continued:w.continued,blocks:[{kind:'field',label:w.generated,text:report.generatedAt},{kind:'field',label:translate('Report notes',locale),text:report.note},...(report.filterSummary?[{kind:'field',label:translate('Filters',locale),text:report.filterSummary}]:[]),...report.rows.flatMap((r,index)=>[{kind:'item',text:`${index+1}. ${r[0]??''}`,group:`row-${index}`},...report.headers.slice(1).map((h,j)=>({kind:'field',label:translate(h,locale),text:String(r[j+1]??''),group:`row-${index}`}))])]}];
}
export async function insightAction(name,id,el,ctx){
 if(!name.startsWith('ins-'))return false;
 const {s,run,showModal,field,select,download,refreshView}=ctx,act=name.slice(4),b=business(s),d=insights(s),opts=(a,key='name')=>a.map(r=>[r.id,r[key]]);
 const f=(label,key,value='',type='text',extra='')=>field(label,key,type,value,extra);
 const optional=(label,key,options,value='')=>select(label,key,options,value).replace(' required>','>');
 const close=()=>document.querySelector('#modal').close();
 const c=()=>{const value=d.counts.find(c=>c.id===id);if(!value)throw Error('Count not found.');return value;};
 const submit=(title,body,command,payload={})=>showModal(title,body,'Save',data=>run('count:'+command,{...payload,...data}));
 const showPreview=()=>showModal('Report preview / 报表预览 / 報表預覽',`<div class="document-controls">${select('Document language','insLanguage',languages,language)}${button('Apply language','language')}${button('Download PDF','pdf')}${button('Print preview','print')}</div>${documentHTML(reportDoc(preview,language))}`);
 switch(act){
  case 'create':{
   const locations=countableLocations(s);if(!locations.length)throw Error('No countable locations.');
   // Capture the location scope from the chosen bin, preventing contradictory selectors.
   showModal('New cycle count',f('Session name','name','','text','required maxlength="100"')+select('Location','locationId',locations.map(l=>[l.id,`${l.code} · ${l.name} · ${b.warehouses.find(w=>w.id===locationScope(s,l.id).warehouseId)?.name} · ${b.owners.find(o=>o.id===locationScope(s,l.id).ownerId)?.name}`]))+select('Count method','method',[['Blind','Blind — hide expected quantities'],['Visible','Show expected quantities']])+note('Use one location per session. No inventory changes until approval.'),'Start count',async data=>{selectedCount='';const scope=locationScope(s,data.locationId);await run('count:create',{...data,...scope,blind:data.method==='Blind'});});break;
  }
  case 'open':selectedCount=id;refreshView();break;
  case 'entry':{
   const [cid,sid]=id.split('|'),count=d.counts.find(c=>c.id===cid),line=count?.lines.find(l=>l.stockId===sid);if(!line)throw Error('Count row not found.');selectedCount=cid;
   const item=s.items.find(i=>i.id===line.itemId);submit(`Count ${item.sku}`,note(`${item.name} · ${s.locations.find(l=>l.id===line.locationId).code} · ${line.lot}`)+f('Counted quantity','qty',line.counted??'','number','required min="0" max="10000000" step="1"')+(line.tracked?area('Complete counted serial list (one per line)','serials',line.countedSerials.join('\n')):'')+f('Note','note',line.note,'text','maxlength="240"'),'record',{id:cid,stockId:sid});break;
  }
  case 'submit':await run('count:submit',{id});break;
  case 'recount':submit('Start a new count round',note('The existing entries are kept in Previous rounds. New entries start empty with the current stock snapshot.')+f('Recount reason','reason','','text','required maxlength="240"'),'recount',{id});break;
  case 'cancel':submit('Cancel this count',f('Cancellation reason','reason','','text','required maxlength="240"'),'cancel',{id});break;
  case 'approve':{const count=c();showModal('Approve and post count',note(`${count.number}: ${count.lines.filter(l=>l.counted!==l.expected).length} quantity variances. All adjustments post together. This action requires Administrator access.`)+f('Approval reason','reason','','text','required maxlength="200"'),'Approve & post',data=>run('count:approve',{id,...data}));break;}
  case 'countExport':download(`${c().number}.csv`,countCSV(s,c()),'text/csv;charset=utf-8');break;
  case 'roundExport':{const [cid,round]=id.split('|'),count=d.counts.find(c=>c.id===cid),r=count?.rounds.find(r=>r.round===Number(round));if(!r)throw Error('Round not found.');download(`${count.number}-round-${round}.csv`,countCSV(s,{...count,...r,status:'Previous round'}),'text/csv;charset=utf-8');break;}
  case 'countPreview':{
   const count=c(),visible=!count.blind||count.status!=='Counting';preview={title:`${count.number} · ${count.name} · ${count.status}`,generatedAt:new Date().toISOString(),note:visible?'Review before posting. This printout does not change inventory.':'Blind count sheet: expected quantities hidden. Write physical quantities and serials, then enter them in Chmltech WMS.',headers:['SKU','Product','Location','Lot',...(visible?['Expected']:[]),'Counted','Serials','Note'],rows:count.lines.map(l=>[s.items.find(i=>i.id===l.itemId).sku,s.items.find(i=>i.id===l.itemId).name,s.locations.find(r=>r.id===l.locationId).code,l.lot,...(visible?[l.expected]:[]),l.counted??'________',l.countedSerials.join('\n')||'________',l.note])};language=interfaceLanguage();showPreview();break;
  }
  case 'traceSearch':showModal('Trace a lot or serial',f('Exact lot or serial','query',traceQuery,'text','required maxlength="100"')+optional('Product','itemId',[['','All products'],...s.items.map(i=>[i.id,`${i.sku} · ${i.name}`])],traceItem),'Search',data=>{traceReport(s,data.query,data.itemId);traceQuery=data.query.trim();traceItem=data.itemId;close();refreshView();});break;
  case 'traceExport':download('Chmltech-WMS-trace.json',JSON.stringify(traceReport(s,traceQuery,traceItem),null,2));break;
  case 'tracePreview':{
   const t=traceReport(s,traceQuery,traceItem);preview={title:`Recall review · ${traceQuery}`,generatedAt:new Date().toISOString(),note:t.note+' '+(t.unlinkedBuilds.length?'Unlinked older production: '+t.unlinkedBuilds.map(w=>w.number).join(', '):''),headers:['Record','Party / location','Product','Lot','Quantity','Status / date'],rows:[...t.inventory.map(r=>['Stock',s.locations.find(l=>l.id===r.locationId).code,s.items.find(i=>i.id===r.itemId).name,r.lot,r.qty,'Current bucket quantity']),...t.purchases.map(({purchase:p,receipt:r,line:l})=>[p.number,p.supplier,s.items.find(i=>i.id===l.itemId).name,l.lot,l.qty,r.time]),...t.customers.flatMap(sh=>sh.allocations.map(a=>[sh.number,sh.customer,s.items.find(i=>i.id===a.itemId).name,a.lot,a.qty,`${sh.status==='Shipped'?'Shipped':'Reversed / '+sh.status} · ${sh.time||'Unknown date'}${a.serials?.includes(traceQuery)?' · Serial '+traceQuery:''}`]))]};language=interfaceLanguage();showPreview();break;
  }
  case 'reportType':reportType=id;refreshView();break;
  case 'reportFilter':showModal('Report and filters',select('Report','type',reportTypes,reportType)+optional('Warehouse','warehouseId',[['','All warehouses'],...opts(b.warehouses)],filters.warehouseId)+optional('Owner','ownerId',[['','All owners'],...opts(b.owners)],filters.ownerId)+optional('Product','itemId',[['','All products'],...s.items.map(i=>[i.id,`${i.sku} · ${i.name}`])],filters.itemId)+f('From date (optional)','from',filters.from||'','date')+f('Through date (optional)','to',filters.to||'','date')+note('Dates use UTC calendar days. Movement dates, PO due dates, order creation dates or shipment dates apply according to the report. Valuation and age are current snapshots.'),'Apply filters',data=>{warehouseReport(s,data.type,data);reportType=data.type;filters={warehouseId:data.warehouseId,ownerId:data.ownerId,itemId:data.itemId,from:data.from,to:data.to};close();refreshView();});break;
  case 'reportExport':download(`Chmltech-WMS-${reportType}.csv`,reportCSV(warehouseReport(s,reportType,filters)),'text/csv;charset=utf-8');break;
  case 'reportPreview':language=interfaceLanguage();preview=warehouseReport(s,reportType,filters);showPreview();break;
  case 'language':language=document.querySelector('[name="insLanguage"]').value;showPreview();break;
  case 'pdf':{
   language=document.querySelector('[name="insLanguage"]').value;const variant=language==='zh-Hant'?'TC':'SC';el.disabled=true;
   try{if(!fontCache.has(variant)){const response=await fetch(`./fonts/NotoSans${variant}-Regular.ttf?v=1.3.1`);if(!response.ok)throw Error('Chinese font could not load. Refresh Chmltech WMS and try again.');fontCache.set(variant,new Uint8Array(await response.arrayBuffer()));}const bytes=await createDocumentPDF(reportDoc(preview,language),{PDFLib:globalThis.PDFLib,fontkit:globalThis.fontkit,fontBytes:fontCache.get(variant)});download(`Chmltech-WMS-report-${language}.pdf`,bytes,'application/pdf');}finally{el.disabled=false;}break;
  }
  case 'print':{language=document.querySelector('[name="insLanguage"]').value;showPreview();for(const article of document.querySelectorAll('.business-document')){const fonts=await document.fonts.load(`400 14px ${language==='zh-Hant'?'HarborTC':'HarborSC'}`,article.textContent);if(!fonts.length&&/[\u3400-\u9fff\uf900-\ufaff]/.test(article.textContent))throw Error('Chinese print font could not load. Refresh this page and try again.');}await document.fonts.ready;window.print();break;}
  default:throw Error('Unknown report action.');
 }
 return true;
}
