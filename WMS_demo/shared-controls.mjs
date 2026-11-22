import {translate} from './locale.mjs';
const pending=new WeakMap();
export const formSavePending=form=>pending.has(form);
export function beginFormSave(form){
 if(pending.has(form))return false;
 const buttons=[...form.querySelectorAll('button')].map(el=>({el,disabled:el.disabled}));
 const status=document.createElement('p');status.className='control-save-status';status.setAttribute('role','status');status.setAttribute('aria-live','polite');status.dataset.l10nSkip='';status.textContent=translate('Saving changes…');
 form.append(status);form.setAttribute('aria-busy','true');buttons.forEach(({el})=>el.disabled=true);pending.set(form,{buttons,status});return true;
}
export function endFormSave(form){
 const x=pending.get(form);if(!x)return;pending.delete(form);form.removeAttribute('aria-busy');x.status.remove();x.buttons.forEach(({el,disabled})=>{if(el.isConnected)el.disabled=disabled;});
}
export function enhanceSharedControls(root){
 for(const b of root.querySelectorAll('button[data-action]:not([type])'))b.type='button';
 for(const input of root.querySelectorAll('input[type="date"],input[type="datetime-local"]')){
  const time=input.type==='datetime-local';if(!input.min||input.min<'0001-01-01')input.min=time?'0001-01-01T00:00':'0001-01-01';
  if(!input.max||input.max.slice(0,4)>'9999'||input.max.split('-')[0].length>4)input.max=time?'9999-12-31T23:59:59':'9999-12-31';
 }
}

