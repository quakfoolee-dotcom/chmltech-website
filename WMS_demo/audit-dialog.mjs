// A read dialog acknowledges the click before waiting for the server. Repeated
// clicks share the pending read, and a dismissed/replaced dialog ignores it.
export function createAuditDialog({read,showLoading,showRows,showError,isCurrent}){
 let active=null;
 return function open(){
  if(active&&isCurrent(active.view))return active.promise;
  const entry={view:showLoading()};active=entry;
  entry.promise=(async()=>{try{const result=await read();if(isCurrent(entry.view))showRows(result);}catch(error){if(isCurrent(entry.view))showError(error);}finally{if(active===entry)active=null;}})();
  return entry.promise;
 };
}
const readers=new WeakMap(),title='Demo activity — latest 500 changes';
const escape=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
export function openServerAudit({showModal,read,renderRows}){
 const dialog=document.querySelector('#modal');let open=readers.get(dialog);
 if(!open){open=createAuditDialog({read,
  showLoading(){showModal(title,'<section data-audit-view aria-busy="true"><p role="status">Loading activity…</p></section>');return dialog.querySelector('[data-audit-view]');},
  showRows(result){showModal(title,renderRows(result.rows));},
  showError(error){showModal(title,'<section data-audit-view><p role="alert">Activity could not be loaded.</p><p>'+escape(error.message)+'</p><button type="button" class="btn" data-action="biz-audit">Retry</button></section>');},
  isCurrent:view=>dialog.open&&view?.isConnected&&dialog.contains(view)
 });readers.set(dialog,open);}
 return open();
}
