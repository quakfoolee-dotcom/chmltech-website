import {workflowModel} from './workflow-model.mjs';
import {actionRoleAllowed,isReadAction} from './action-permissions.mjs';
import {translate} from './locale.mjs';
import {enhanceSharedControls,formSavePending} from './shared-controls.mjs';
import {cloudQBOActionAllowed} from './qbo-access.mjs';
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=v=>e(translate(v));
const roles=['Admin','Warehouse','Purchasing','Sales','Manufacturing','Accounting','Viewer'];
export const requiredActionRoles=action=>action.startsWith('cloud-qbo-')?roles.filter(role=>cloudQBOActionAllowed(action,role,false)):isReadAction(action)?['Viewer']:roles.filter(role=>actionRoleAllowed(action,role));
const ignored=/(?:cancel|remove|delete|reverse|void|loadDemo|sample|seed|reset|replace|reject|withdraw|unschedule|Demo|chinese-demo|menu|nav-group|record-tab|filter|sort|export|Download|pdf|print|language)/i;
const caption=el=>(el.textContent||el.getAttribute('aria-label')||'Review details').trim().replace(/\s+/g,' ');
const candidates=root=>[...root.querySelectorAll('button[data-action]')].filter(b=>!b.closest('.workflow-panel')&&!ignored.test(b.dataset.action)&&b.getClientRects().length&&!b.closest('[hidden]'));
export function controlBlockReason(el,info,model){
 if(model.blockers.length)return model.blockers.join(' · ');
 if(!el)return model.terminal?'No action needed.':'Choose a record to see its next step.';
 if(!el.disabled)return 'No blocking issue detected.';
 if(info?.workspace?.isDemo||info?.user?.role==='Viewer')return 'This workspace is read-only.';
 if(el.dataset.cloudBlocked==='true')return el.title||'Available in local Harbor.';
 if(el.dataset.roleBlocked==='true')return 'Permission required.';
 return el.title||'This action is unavailable for the current record.';
}
export function chooseWorkflowControl(model,controls){
 if(model.terminal)return null;
 for(const action of model.actions){const matches=controls.filter(c=>c.dataset.action===action&&(!model.recordId||!c.dataset.id||c.dataset.id===model.recordId||action==='rcv-createTask'));if(matches.length)return matches.find(c=>!c.disabled)||matches[0];}
 if(model.recordId)return null;
 return controls.find(c=>!c.disabled&&!isReadAction(c.dataset.action))||controls.find(c=>!c.disabled)||controls[0]||null;
}
export function workflowPanelHTML(model,{nextLabel,reason,required,disabled,action='',unavailable=[]}){
 return '<section class="workflow-panel" aria-label="'+t('Workflow guidance')+'" data-workflow-route="'+e(model.route)+'" data-l10n-skip><div class="workflow-heading"><strong>'+t('Workflow guidance')+'</strong><span>'+t(model.label)+'</span></div>'+
 (model.recordLabel?'<p class="workflow-record">'+t('Current record')+': <span>'+e(model.recordLabel)+'</span></p>':'')+
 '<dl class="workflow-fields"><div><dt>'+t('Current state')+'</dt><dd data-workflow-state>'+t(model.status)+'</dd></div><div><dt>'+t('Next action')+'</dt><dd><button type="button" class="btn primary workflow-next" data-workflow-trigger data-workflow-action="'+e(action)+'"'+(disabled?' disabled':'')+'>'+e(nextLabel||translate(model.terminal?'No action needed.':'Review details'))+'</button></dd></div><div><dt>'+t('Blocking reason')+'</dt><dd data-workflow-reason>'+e(reason)+'</dd></div><div><dt>'+t('Required role')+'</dt><dd>'+e(required)+'</dd></div></dl>'+
 '<div class="workflow-steps" aria-label="'+t('Workflow steps')+'">'+model.steps.map(step=>'<span'+(step===model.status?' class="current" aria-current="step"':'')+'>'+t(step)+'</span>').join('<span aria-hidden="true">›</span>')+'</div>'+
 (unavailable.length?'<details class="workflow-unavailable"><summary>'+t('Unavailable controls')+' ('+unavailable.length+')</summary><ul>'+unavailable.map(x=>'<li><strong>'+e(x.label)+'</strong> — '+e(x.reason)+'</li>').join('')+'</ul></details>':'')+'</section>';
}
export function startWorkflowControls(context){
 const main=document.querySelector('#main'),modal=document.querySelector('#modal');let queued=false,last='',target=null,updating=false;
 function update(){
  queued=false;if(updating)return;updating=true;
  try{
   enhanceSharedControls(main);enhanceSharedControls(modal);
   const {state,info,ready,hash}=context();
   if(!ready||!info?.user||main.querySelector('.account-gate')){if(info?.user&&!ready)for(const control of main.querySelectorAll('button[data-action]'))if(!isReadAction(control.dataset.action)&&!control.disabled){control.disabled=true;control.title=translate('Refresh the workspace before saving.');}main.querySelector('.workflow-panel')?.remove();last='';target=null;return;}
   const controls=candidates(main);let model=workflowModel(state,hash),next=chooseWorkflowControl(model,controls);
   if(!model.recordId&&next?.dataset.id){const focused=workflowModel(state,hash,{focusId:next.dataset.id});if(focused.recordId){model=focused;next=chooseWorkflowControl(model,controls);}}
   const reason=controlBlockReason(next,info,model),disabled=!next||next.disabled||model.actionBlocked;
   const required=(model.nextRoute==='business/production-labor'?['Admin','Accounting']:model.nextRoute==='business/directed-putaway'?['Admin','Warehouse']:next?requiredActionRoles(next.dataset.action):['Viewer']).map(r=>translate(r)).join(' / ');
   const unavailable=[...new Map(controls.filter(c=>c.disabled).map(c=>{const label=caption(c),why=controlBlockReason(c,info,{...model,blockers:[]});return [label+'|'+why,{label,reason:translate(why)}];})).values()];
   const html=workflowPanelHTML(model,{nextLabel:next?caption(next):'',action:next?.dataset.action||'',reason:model.blockers.map(x=>translate(x)).join(' · ')||translate(reason),required,disabled,unavailable});
   target=next;if(html===last&&main.querySelector('.workflow-panel'))return;last=html;
   let panel=main.querySelector('.workflow-panel');if(!panel){panel=document.createElement('div');const anchor=main.querySelector('.page-head,.fb-module,.card');(anchor||main.firstElementChild)?.before(panel);if(!panel.isConnected)main.prepend(panel);}
   panel.outerHTML=html;
   if(model.nextRoute){const nextButton=main.querySelector('[data-workflow-trigger]'),a=document.createElement('a');a.className='btn primary workflow-next';a.href='#'+model.nextRoute;a.textContent=translate(model.nextLabel);nextButton.replaceWith(a);}
  }finally{updating=false;}
 }
 const queue=()=>{if(!queued){queued=true;queueMicrotask(update);}};
 const observer=new MutationObserver(queue);observer.observe(main,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['disabled','title','hidden']});observer.observe(modal,{subtree:true,childList:true});
 const click=event=>{const b=event.target.closest('[data-workflow-trigger]');if(!b)return;event.preventDefault();if(!b.disabled&&target?.isConnected&&!target.disabled){target.focus({preventScroll:true});target.click();}};
 main.addEventListener('click',click);
 const language=()=>{last='';queue();};document.addEventListener('harbor-language-changed',language);
 const cancel=event=>{const form=modal.querySelector('form');if(form&&formSavePending(form))event.preventDefault();};modal.addEventListener('cancel',cancel);
 const pendingClick=event=>{const form=modal.querySelector('form');if(form&&formSavePending(form)&&event.target.closest('button,a,[data-action]')){event.preventDefault();event.stopImmediatePropagation();const status=form.querySelector('.control-save-status');if(status)status.textContent=translate('Wait for the current save to finish.');}};
 document.addEventListener('click',pendingClick,true);
 queue();return {refresh:queue,disconnect(){observer.disconnect();main.removeEventListener('click',click);document.removeEventListener('harbor-language-changed',language);modal.removeEventListener('cancel',cancel);document.removeEventListener('click',pendingClick,true);}};
}

