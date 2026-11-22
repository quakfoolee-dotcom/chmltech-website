import {APP_VERSION} from './version.mjs';
import {createBrowserWorkspace} from './browser-store.mjs';
let workspace,starting;
export const invalidateAuthRequests=()=>{};
export const hasPending=()=>false;
export const retryGuest=async()=>{};
export const storageMode=()=>workspace?.storageMode||'saved';
export function startGuest(){return starting??=(async()=>{
 const response=await fetch(new URL('./sample-workspace.json',import.meta.url));if(!response.ok)throw Error('Sample warehouse could not load. Refresh this page.');
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
 if(route==='command')return workspace.command(data);
 if(route==='workspace')return {state:await workspace.read()};
 if(route==='status'){const state=await workspace.read();return {version:APP_VERSION,user:{username:'browser-demo',name:'Demo visitor',role:'Admin'},serverTime:Date.now(),initialized:true,setupRequired:false,readOnly:false,revision:state.revision,phoneAddress:'',demo:true};}
 if(route==='audit'){const state=await workspace.read();return {rows:state.events.map(e=>({time:e.time,actor:'Demo visitor',action:e.type,revision:state.revision}))};}
 if(route==='users')return {users:[{username:'browser-demo',name:'Demo visitor',role:'Admin',active:true}]};
 if(route==='backups')return {backups:[],archives:[]};
 throw Object.assign(Error('This browser demo uses fictional records. Real accounts, server backups and external connections are unavailable. Use Reset demo to start again.'),{status:403});
}
