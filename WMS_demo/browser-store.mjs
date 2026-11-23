import {dispatch,validateState} from './engine.mjs?demo=9c44c6dabb8d4728';
import {operationalCommands} from './operational-policy.mjs?demo=9c44c6dabb8d4728';
import {productionCommands} from './production.mjs?demo=9c44c6dabb8d4728';
export const STORAGE_KEY='chmltech:WMS_demo:warehouse:v1';
export const STORAGE_PREFIX='chmltech:WMS_demo:';
const allowed=new Set([...operationalCommands,...productionCommands,'crm:saveProfile','crm:linkCustomer','crm:saveOpportunity','crm:stage','crm:linkQuote','crm:saveActivity','crm:completeActivity']);
const failure=(message,status=422)=>Object.assign(Error(message),{status});
// The sample warehouse is built once; when a visitor starts or resets the demo, every
// date in it moves forward by the whole days (24-hour periods) since the build, so due dates, ages and
// history keep the same distance from today (nothing turns overdue as the build ages).
const DATE=/^(\d{4}-\d{2}-\d{2})(T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z)?$/;
export function shiftSeedDates(seed,now){
 const built=Date.parse(seed?.updatedAt);if(!Number.isFinite(built))return seed;
 // Whole 24-hour periods since the build, so shifted timestamps never pass the current time.
 const days=Math.floor((now-built)/86400000);
 if(days<=0)return seed;const ms=days*86400000;
 const move=v=>{if(typeof v==='string'){const m=DATE.exec(v);if(!m)return v;const t=new Date(Date.parse(m[2]?v:m[1]+'T00:00:00Z')+ms).toISOString();return m[2]?t:t.slice(0,10);}
  if(Array.isArray(v))return v.map(move);if(v&&typeof v==='object'){const o={};for(const k of Object.keys(v))o[k]=move(v[k]);return o;}return v;};
 return move(seed);
}
export function createBrowserWorkspace({storage,seed,clock=Date.now,locks=globalThis.navigator?.locks}={}){
 validateState(seed);let memory=null,mode=storage?'saved':'memory';
 const fresh=()=>{const state=shiftSeedDates(structuredClone(seed),clock());validateState(state);return state;};
 function read(){
  if(mode==='memory')return memory;
  let raw;try{raw=storage.getItem(STORAGE_KEY);}catch{mode='memory';return memory;}
  if(!raw)return null;
  try{const value=JSON.parse(raw);if(value.format!==1)throw Error();validateState(value.state);return value;}
  catch{throw failure('Saved demo data could not be opened. Use Reset demo to restore the sample warehouse.',409);}
 }
 function write(state){
  validateState(state);const value={format:1,state};
  if(mode==='memory'){memory=value;return;}
  try{storage.setItem(STORAGE_KEY,JSON.stringify(value));}
  catch{throw failure('The browser could not save this change. Free browser storage or use Reset demo. Your previous saved warehouse is unchanged.',507);}
 }
 const exclusive=fn=>locks?locks.request(STORAGE_PREFIX+'save',fn):Promise.resolve().then(fn);
 const workspace=()=>{let value=read();if(!value){write(fresh());value=read()||memory;}return structuredClone(value.state);};
 return {
  get storageMode(){return mode;},
  start:()=>exclusive(workspace),
  read:()=>exclusive(workspace),
  command:data=>exclusive(()=>{
   const state=workspace();if(data?.revision!==state.revision)throw failure('The demo changed in another tab. Refresh and try again.',409);
   if(!allowed.has(data.command))throw failure('Real accounts, external integrations and workspace replacement are unavailable in this browser demo.',403);
   if(data.command==='importCatalog'&&(!Array.isArray(data.payload?.rows)||data.payload.rows.length<1||data.payload.rows.length>25))throw failure('Demo imports accept 1–25 rows at a time.');
   const result=dispatch(state,data.command,data.payload,{now:new Date(clock()).toISOString(),role:'Admin',actor:'Browser demo visitor',expectedRevision:state.revision});
   write(result.state);return structuredClone(result);
  }),
  reset:()=>exclusive(()=>{
   let previous;try{previous=read();}catch{}const state=fresh();state.revision=Math.max(state.revision,(previous?.state.revision||0)+1,clock());
   write(state);return structuredClone(state);
  })
 };
}
