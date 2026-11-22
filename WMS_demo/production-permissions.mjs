import {productionActionCommands,productionActionAllowed} from './production-policy.mjs';
import {translate} from './locale.mjs';
// Only mapped production mutations are restricted; previews, exports and filters stay readable.
export function applyProductionRoleControls(root,role){
 for(const el of root.querySelectorAll('[data-action]')){
  if(!Object.hasOwn(productionActionCommands,el.dataset.action))continue;
  if(!productionActionAllowed(el.dataset.action,role)){
   if(!el.disabled||el.dataset.productionRoleBlocked){el.disabled=true;el.dataset.productionRoleBlocked='true';el.title=translate('Your role cannot perform this production action.');}
  }else if(el.dataset.productionRoleBlocked){el.disabled=false;delete el.dataset.productionRoleBlocked;el.removeAttribute('title');}
 }
}

