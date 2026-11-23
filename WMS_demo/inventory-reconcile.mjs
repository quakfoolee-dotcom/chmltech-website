import {valuation} from './costing.mjs?demo=9c44c6dabb8d4728';
export function compareInventory(s,accounts,baseline=null,time=new Date().toISOString()){
 const local=valuation(s),ids=accounts.map(a=>String(a.Id)).sort(),available=accounts.length>0&&accounts.every(a=>Number.isFinite(a.CurrentBalance)),remote=available?Math.round(accounts.reduce((n,a)=>n+a.CurrentBalance,0)*100):null;
 const validBaseline=!!baseline&&JSON.stringify(ids)===JSON.stringify(baseline.accounts.map(a=>String(a.Id)).sort())&&baseline.currency===local.currency&&baseline.remote!==null;
 const localChange=validBaseline?local.value-baseline.local:null,remoteChange=validBaseline&&remote!==null?remote-baseline.remote:null;
 return {time,revision:s.revision,currency:local.currency,local:local.value,remote,missing:local.missing,accounts:accounts.map(a=>({Id:a.Id,Name:a.Name,CurrentBalance:a.CurrentBalance??null})),difference:remote===null?null:local.value-remote,baselineTime:validBaseline?baseline.time:null,baselineDifference:validBaseline?baseline.difference:null,localChange,remoteChange,movementDifference:localChange!==null&&remoteChange!==null?localChange-remoteChange:null,complete:local.missing.length===0,sampleCosts:local.rows.filter(x=>x.sample).map(x=>x.sku)};
}
