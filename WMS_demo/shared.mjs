import {APP_VERSION} from './version.mjs?demo=45f52980507d3a1b';
import {createBrowserWorkspace} from './browser-store.mjs?demo=45f52980507d3a1b';
let workspace,starting;
// Microsoft Clarity custom events. The site adds Clarity (with its ?notrack=on opt-out)
// to the demo page; when it is absent or opted out, these calls do nothing.
const MILESTONES={receivePurchase:'wms_milestone_po_received',issueOrder:'wms_milestone_order_issued',finishPick:'wms_milestone_pick_finished',shipShipment:'wms_milestone_order_shipped','units:save':'wms_milestone_units_edited'};
export function track(name,tag){try{const c=globalThis.clarity;if(typeof c!=='function')return;c('event',String(name).replace(/[^a-z0-9_]+/gi,'_').toLowerCase().slice(0,60));if(tag)c('set',tag[0],tag[1]);}catch{}}
const UNSUPPORTED='This action is not available in the browser demo because it needs a real account or server. Your demo data is unchanged.';
const unsupported=route=>{track('wms_blocked_'+String(route).split(/[/?]/)[0]);return Object.assign(Error(UNSUPPORTED),{status:403});};
export const invalidateAuthRequests=()=>{};
export const hasPending=()=>false;
export const retryGuest=async()=>{};
export const storageMode=()=>workspace?.storageMode||'saved';
// Saved warehouses from before the V5.73 sample tidy-up still carry test codes.
export async function savedIsOutdated(){try{const state=await workspace.read();return state.items.some(i=>/^PLAY-/.test(i.sku));}catch{return false;}}
export function startGuest(){return starting??=(async()=>{
 const response=await fetch(new URL('./sample-workspace.json?demo=45f52980507d3a1b',import.meta.url));if(!response.ok)throw Error('Sample warehouse could not load. Refresh this page.');
 let storage;try{storage=globalThis.localStorage;}catch{}
 workspace=createBrowserWorkspace({storage,seed:await response.json()});return workspace.start();
})();}
export async function resetGuest(){
 // A corrupt saved record can be reset even when initial startup failed.
 try{await startGuest();}catch(e){if(!workspace)throw e;}
 return workspace.reset();
}
export async function api(route,data){
 await startGuest();
 if(route==='command'){const result=await workspace.command(data);track('wms_cmd_'+data.command);if(MILESTONES[data.command])track(MILESTONES[data.command]);return result;}
 if(route==='workspace')return {state:await workspace.read()};
 if(route==='status'){const state=await workspace.read();return {version:APP_VERSION,user:{username:'browser-demo',name:'Demo visitor',role:'Admin'},serverTime:Date.now(),initialized:true,setupRequired:false,readOnly:false,revision:state.revision,phoneAddress:'',demo:true};}
 if(route==='audit'){const state=await workspace.read();return {rows:state.events.slice(0,500).map(e=>({time:new Date(e.time).toLocaleString(),actor:'Demo visitor',action:e.type,revision:e.revision??''}))};}
 // Creating or changing accounts must never appear to succeed.
 if(route==='users'&&data!==undefined)throw unsupported(route);
 if(route==='users')return {users:[{username:'browser-demo',name:'Demo visitor',role:'Admin',active:true}]};
 if(route==='backups')return {backups:[],archives:[]};
 throw unsupported(route);
}
