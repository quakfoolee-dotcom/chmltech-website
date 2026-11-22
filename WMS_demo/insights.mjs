import {businessDay} from './company-date.mjs';
import {returnShipment,deliveryLines} from './fulfillment.mjs';
import {isFIFO,allocatedFIFORowValue} from './fifo.mjs';
// Count approval, retained stock evidence and read-only warehouse reports.
import {business,locationScope,orderScope} from './business.mjs';
import {purchaseLines} from './purchasing.mjs';
import {csvText} from './exchange.mjs';
import {validUnicode,charLength} from './unicode.mjs';

const must=(ok,message)=>{if(!ok)throw Error(message);};
const find=(rows,id)=>{const value=rows.find(r=>r.id===id);must(value,'Record not found.');return value;};
const text=(v,label,max=240)=>{const value=String(v??'').trim();must(value&&validUnicode(value)&&charLength(value)<=max,`${label} is required (up to ${max} characters).`);return value;};
const quantity=v=>{const n=Number(v);must(v!==''&&v!==null&&v!==undefined&&Number.isSafeInteger(n)&&n>=0&&n<=10000000,'Enter a whole counted quantity of zero or more.');return n;};
const serialList=v=>{const a=(Array.isArray(v)?v:String(v??'').split(/[\n,]/)).map(x=>String(x).trim()).filter(Boolean);must(new Set(a).size===a.length&&a.every(x=>validUnicode(x)&&charLength(x)<=100),'Serial numbers must be unique valid text, up to 100 characters each.');return a;};
const serials=(s,id)=>s.operations?.serials[id]||[];
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const byId=(a,b)=>a.id.localeCompare(b.id);
const sorted=a=>[...a].sort();
const base=()=>({version:1,sequence:0,counts:[],movements:[],locationRevisions:{},shipments:{},links:[],startedAt:'',truncatedBefore:''});
export const insights=s=>s.insights||base();
const setup=s=>s.insights||(s.insights=base());
export const countableLocations=(s,scope={})=>s.locations.filter(l=>{
 const sc=locationScope(s,l.id);
 return l.type!=='Staging'&&!sc.transit&&!sc.production&&(!scope.warehouseId||sc.warehouseId===scope.warehouseId)&&(!scope.ownerId||sc.ownerId===scope.ownerId)&&(!scope.locationId||l.id===scope.locationId);
});
function countSnapshot(s,scope){
 const locations=countableLocations(s,scope).map(l=>l.id);
 return s.stock.filter(r=>locations.includes(r.locationId)&&(r.qty||r.committed)).sort(byId).map(r=>({stockId:r.id,itemId:r.itemId,locationId:r.locationId,lot:r.lot,expected:r.qty,committed:r.committed,tracked:s.operations?.tracking[r.itemId]==='Serial',expectedSerials:sorted(serials(s,r.id)),counted:null,countedSerials:[],note:'',enteredBy:'',enteredAt:''}));
}
const signature=lines=>lines.map(l=>[l.stockId,l.itemId,l.locationId,l.lot,l.expected,l.committed,l.tracked,l.expectedSerials]);
const stamps=(s,scope)=>countableLocations(s,scope).map(l=>[l.id,insights(s).locationRevisions[l.id]||0]).sort((a,b)=>a[0].localeCompare(b[0]));
export function countIsStale(s,c){return !same(c.stamps,stamps(s,c.scope))||!same(signature(c.lines),signature(countSnapshot(s,c.scope)));}
export function countCommand(s,command,p,ctx){
 if(!command.startsWith('count:'))return null;
 let data=setup(s);const actor=ctx.actor||'Local operator';
 const event=(type,c)=>({type,message:`${c.number} · ${c.name}`,reference:c.number,resultId:c.id});
 if(command==='count:create'){
  must(data.counts.length<1000,'Count history is full. Export a backup before starting a new workspace.');
  const scope={warehouseId:p.warehouseId||'wh-main',ownerId:p.ownerId||'owner-self',locationId:p.locationId||''};
  find(business(s).warehouses,scope.warehouseId);find(business(s).owners,scope.ownerId);
  must(countableLocations(s,scope).length,'Choose a storage, receiving or hold location in this warehouse and ownership.');
  const lines=countSnapshot(s,scope);must(lines.length,'There is no stock to count in this scope.');
  const number=++data.sequence,c={id:`count-${number}`,number:`CC-${number}`,name:text(p.name,'Count name',100),scope,status:'Counting',blind:p.blind!==false,createdAt:ctx.time,createdBy:actor,round:1,rounds:[],lines,stamps:stamps(s,scope),history:[{action:'Created',time:ctx.time,actor}]};
  data.counts.push(c);return event('Cycle count started',c);
 }
 let c=find(data.counts,p.id);
 const history=(action,details={})=>{must(c.history.length<10000,'This session has reached its entry limit. Cancel it and start a new count.');c.history.push({action,time:ctx.time,actor,...details});};
 if(command==='count:record'){
  must(c.status==='Counting','Only an active count accepts entries.');const line=c.lines.find(l=>l.stockId===p.stockId);must(line,'Choose a stock row in this count.');
  const n=quantity(p.qty),values=serialList(p.serials);must(!line.tracked||values.length===n,'Enter the complete counted serial list, one serial per counted unit.');must(line.tracked||!values.length,'This product is not serial tracked.');
  const note=String(p.note??'').trim();must(validUnicode(note)&&charLength(note)<=240,'Count note is limited to 240 valid characters.');
  Object.assign(line,{counted:n,countedSerials:values,note,enteredBy:actor,enteredAt:ctx.time});history('Count entered',{round:c.round,stockId:line.stockId,qty:n,serials:values,note});return event('Cycle count entry saved',c);
 }
 if(command==='count:submit'){
  must(c.status==='Counting'&&c.lines.every(l=>l.counted!==null),'Count every row before submitting for review.');must(!countIsStale(s,c),'Stock changed during this count. Start a recount before review.');
  c.status='Review';history('Submitted for review');return event('Cycle count submitted',c);
 }
 if(command==='count:recount'){
  must(['Counting','Review'].includes(c.status),'Only an unposted count can be recounted.');must(c.rounds.length<20,'Start a new count after 20 recounts.');
  c.rounds.push({round:c.round,lines:structuredClone(c.lines),stamps:c.stamps,time:ctx.time,actor,reason:text(p.reason,'Recount reason')});c.round++;
  c.lines=countSnapshot(s,c.scope);must(c.lines.length,'No stock remains in this scope. Cancel this count.');c.stamps=stamps(s,c.scope);c.status='Counting';history('Recount started');return event('Cycle count restarted',c);
 }
 if(command==='count:cancel'){
  must(['Counting','Review'].includes(c.status),'This count is already closed.');c.closeReason=text(p.reason,'Cancellation reason');c.status='Cancelled';history('Cancelled');return event('Cycle count cancelled',c);
 }
 if(command==='count:approve'){
  must(c.status==='Review'&&c.lines.every(l=>l.counted!==null),'Submit the completed count for review first.');must(!countIsStale(s,c),'Stock changed during this count. Start a recount; no stock was adjusted.');
  const reason=text(p.reason,'Approval reason');
  // Nested stock commands run on this transaction's clone. Any failure rolls back all rows.
  for(const line of c.lines){
   const result=ctx.dispatch(s,'countStock',{stockId:line.stockId,qty:line.counted,serials:line.countedSerials,reason:`${c.number}: ${reason}`.slice(0,240)},{now:ctx.time,internal:true});Object.assign(s,result.state);
  }
  data=setup(s);c=find(data.counts,p.id);c.status='Posted';c.approvedBy=actor;c.approvedAt=ctx.time;c.approvalReason=reason;history('Approved and posted');return event('Cycle count approved',c);
 }
 throw Error('Unknown cycle count action.');
}

export function afterInsights(s,previous,command,p,ctx,event){
 if(ctx.nested)return;
 const changes=s.stock.flatMap(r=>{
  const old=previous.stock.find(x=>x.id===r.id),before=serials(previous,r.id),after=serials(s,r.id);
  const added=after.filter(x=>!before.includes(x)),removed=before.filter(x=>!after.includes(x));
  return r.qty!==(old?.qty||0)||r.committed!==(old?.committed||0)||added.length||removed.length?[{stockId:r.id,itemId:r.itemId,locationId:r.locationId,lot:r.lot,quantity:r.qty-(old?.qty||0),reserved:r.committed-(old?.committed||0),balance:r.qty,added,removed,scope:{...locationScope(s,r.locationId)}}]:[];
 });
 const d=setup(s);d.startedAt||=ctx.time;
 if(changes.length){
  for(const id of new Set(changes.map(r=>r.locationId)))d.locationRevisions[id]=(d.locationRevisions[id]||0)+1;
  d.movements.push({id:`movement-${++d.sequence}`,revision:s.revision+1,time:ctx.time,command,actor:ctx.actor||'Local operator',reference:event.reference||'',description:event.type,changes});
  if(d.movements.length>2000){const removed=d.movements.splice(0,d.movements.length-2000);d.truncatedBefore=removed.at(-1).time;}
 }
 for(const sh of s.shipments){
  const old=previous.shipments.find(x=>x.id===sh.id);
  if(sh.status==='Shipped'&&old?.status!=='Shipped'){
   const o=find(s.orders,sh.orderId),pk=find(s.picks,sh.pickId);
   d.shipments[sh.id]={id:sh.id,number:sh.number,orderId:o.id,orderNumber:o.number,customer:o.customer,time:ctx.time,scope:{...orderScope(s,o)},allocations:structuredClone(pk.allocations)};
  }
 }
 if(command==='business:finishWork'){
  const w=find(business(s).workOrders,p.id),lot=changes.find(c=>c.itemId===w.outputId&&c.locationId===p.locationId&&c.quantity>0)?.lot;must(lot,'Production output stock evidence is missing.');
  d.links.push({id:w.id,reference:w.number,type:'Production',time:ctx.time,inputs:structuredClone(w.consumed),output:{itemId:w.outputId,lot,qty:w.qty,serials:serialList(p.serials)},scope:{...w.scope},uncertain:false});
 }
 if(command==='business:receiveReturn'){
  const r=find(business(s).returns,p.id),stock=find(s.stock,r.stockId),sh=returnShipment(s,r),evidence=d.shipments[sh.id]||{allocations:find(s.picks,sh.pickId).allocations};
  const inputs=evidence.allocations.filter(a=>a.itemId===r.itemId&&(!r.serials?.length||a.serials?.some(x=>r.serials.includes(x)))).map(a=>({itemId:a.itemId,lot:a.lot,qty:a.qty,serials:r.serials?.length?a.serials.filter(x=>r.serials.includes(x)):[]}));
  d.links.push({id:r.id,reference:r.number,type:'Customer return',time:ctx.time,inputs,output:{itemId:r.itemId,lot:stock.lot,qty:r.qty,serials:r.serials||[]},scope:{...locationScope(s,stock.locationId)},uncertain:inputs.length>1&&!r.serials?.length});
 }
}

export function validateInsights(s){
 if(!s?.insights)return;
 const d=s.insights,validDate=v=>typeof v==='string'&&Number.isFinite(Date.parse(v)),str=v=>typeof v==='string'&&validUnicode(v),whole=v=>Number.isSafeInteger(v)&&v>=0&&v<=10000000;
 must(d.version===1&&Number.isSafeInteger(d.sequence)&&d.sequence>=0&&Array.isArray(d.counts)&&d.counts.length<=1000&&Array.isArray(d.movements)&&d.movements.length<=2000&&Array.isArray(d.links)&&d.links.length<=10000,'Invalid count or trace history.');
 must(d.locationRevisions&&Object.values(d.locationRevisions).every(v=>Number.isSafeInteger(v)&&v>=0)&&d.shipments&&typeof d.shipments==='object','Invalid stock history metadata.');
 must((!d.startedAt||validDate(d.startedAt))&&(!d.truncatedBefore||validDate(d.truncatedBefore)),'Invalid trace coverage dates.');
 const node=n=>n&&s.items.some(i=>i.id===n.itemId)&&str(n.lot)&&whole(n.qty)&&n.qty>0&&Array.isArray(n.serials)&&n.serials.every(str);
 const ids=new Set();
 for(const c of d.counts){
  must(/^count-\d+$/.test(c.id)&&!ids.has(c.id)&&Number(c.id.split('-')[1])<=d.sequence,'Invalid count identifier.');ids.add(c.id);
  must(str(c.name)&&str(c.number)&&validDate(c.createdAt)&&['Counting','Review','Posted','Cancelled'].includes(c.status)&&typeof c.blind==='boolean'&&c.scope&&Array.isArray(c.stamps)&&Array.isArray(c.lines)&&c.lines.length>0&&Array.isArray(c.rounds)&&c.rounds.length<=20&&Number.isInteger(c.round)&&c.round===c.rounds.length+1&&Array.isArray(c.history),'Invalid cycle count.');
  const checkLines=lines=>{const seen=new Set();must(Array.isArray(lines)&&lines.length<=10000,'Invalid count lines.');for(const l of lines){const r=s.stock.find(r=>r.id===l.stockId);must(r&&r.itemId===l.itemId&&r.locationId===l.locationId&&r.lot===l.lot&&!seen.has(l.stockId)&&whole(l.expected)&&whole(l.committed)&&l.committed<=l.expected&&(l.counted===null||whole(l.counted))&&typeof l.tracked==='boolean'&&Array.isArray(l.expectedSerials)&&Array.isArray(l.countedSerials)&&[...l.expectedSerials,...l.countedSerials].every(str)&&str(l.note),'Invalid count row.');seen.add(l.stockId);must(!l.tracked||((l.expectedSerials.length===l.expected)&&new Set(l.expectedSerials).size===l.expectedSerials.length&&(l.counted===null||l.countedSerials.length===l.counted)&&new Set(l.countedSerials).size===l.countedSerials.length),'Invalid count serials.');}};
  checkLines(c.lines);for(const r of c.rounds)checkLines(r.lines);
  must(!['Review','Posted'].includes(c.status)||c.lines.every(l=>l.counted!==null),'Incomplete submitted count.');
  must(c.status!=='Posted'||(validDate(c.approvedAt)&&str(c.approvedBy)&&str(c.approvalReason)),'Invalid count approval.');
 }
 for(const m of d.movements){must(/^movement-\d+$/.test(m.id)&&!ids.has(m.id)&&Number(m.id.split('-')[1])<=d.sequence&&validDate(m.time)&&Array.isArray(m.changes)&&str(m.command)&&str(m.reference),'Invalid stock movement.');ids.add(m.id);for(const c of m.changes)must(s.stock.some(r=>r.id===c.stockId&&r.itemId===c.itemId&&r.locationId===c.locationId&&r.lot===c.lot)&&Number.isSafeInteger(c.quantity)&&Number.isSafeInteger(c.reserved)&&whole(c.balance)&&Array.isArray(c.added)&&Array.isArray(c.removed)&&[...c.added,...c.removed].every(str)&&c.scope,'Invalid movement row.');}
 for(const sh of Object.values(d.shipments))must(s.shipments.some(x=>x.id===sh.id)&&validDate(sh.time)&&str(sh.customer)&&Array.isArray(sh.allocations)&&sh.allocations.every(a=>node({...a,serials:a.serials||[]})),'Invalid shipment evidence.');
 for(const link of d.links)must(str(link.id)&&validDate(link.time)&&Array.isArray(link.inputs)&&link.inputs.every(node)&&node(link.output)&&typeof link.uncertain==='boolean','Invalid lot genealogy.');
}

const key=n=>JSON.stringify([n.itemId,n.lot,n.serial||'']);
const intersects=(a,b)=>a.itemId===b.itemId&&a.lot===b.lot&&(!a.serial||(b.serials||[]).includes(a.serial));
const includesNode=(nodes,row)=>nodes.some(n=>intersects(n,{...row,serials:row.serials||[]}));
export function shipmentEvidence(s){
 return s.shipments.filter(sh=>sh.status==='Shipped'||insights(s).shipments[sh.id]).map(sh=>{
  const o=find(s.orders,sh.orderId),pk=s.picks.find(p=>p.id===sh.pickId),saved=insights(s).shipments[sh.id];
  return {...(saved||{id:sh.id,number:sh.number,orderId:o.id,orderNumber:o.number,customer:o.customer,time:sh.shippedAt||'',scope:orderScope(s,o),allocations:pk?.shipmentId===sh.id?pk.allocations:[]}),status:sh.status,recorded:!!saved};
 });
}
export function traceReport(s,query,itemId=''){
 query=String(query||'').trim();must(query,'Enter an exact lot or serial number.');
 const d=insights(s),nodes=[];const add=(list,n)=>{if(!list.some(x=>key(x)===key(n)))list.push(n);};
 const consider=r=>{if(itemId&&r.itemId!==itemId)return;if(r.lot===query)add(nodes,{itemId:r.itemId,lot:r.lot});if((r.serials||[]).includes(query))add(nodes,{itemId:r.itemId,lot:r.lot,serial:query});};
 for(const r of s.stock)consider({...r,serials:serials(s,r.id)});
 for(const p of s.operations?.purchases||[])for(const r of p.receipts||[])for(const l of r.lines)consider(l);
 for(const sh of shipmentEvidence(s))for(const a of sh.allocations)consider(a);
 for(const m of d.movements)for(const c of m.changes)consider({...c,serials:[...c.added,...c.removed]});
 for(const l of d.links){consider(l.output);l.inputs.forEach(consider);}
 const descendants=[...nodes],ancestors=[...nodes],links=[];
 let grew=true;while(grew){grew=false;for(const l of d.links)if(l.inputs.some(n=>includesNode(descendants,n))){if(!links.includes(l))links.push(l);const size=descendants.length;const matches=descendants.filter(n=>l.inputs.some(i=>intersects(n,i)));if(l.type==='Customer return'&&matches.every(n=>n.serial)){for(const n of matches)if(l.output.serials.includes(n.serial))add(descendants,{itemId:l.output.itemId,lot:l.output.lot,serial:n.serial});}else add(descendants,{itemId:l.output.itemId,lot:l.output.lot});grew||=descendants.length>size;}}
 grew=true;while(grew){grew=false;for(const l of d.links)if(includesNode(ancestors,l.output)){if(!links.includes(l))links.push(l);const size=ancestors.length,matches=ancestors.filter(n=>intersects(n,l.output));for(const n of l.inputs){if(l.type==='Customer return'&&matches.every(n=>n.serial)){for(const m of matches)if(n.serials.includes(m.serial))add(ancestors,{itemId:n.itemId,lot:n.lot,serial:m.serial});}else add(ancestors,{itemId:n.itemId,lot:n.lot});}grew||=ancestors.length>size;}}
 const inventory=s.stock.filter(r=>r.qty>0&&includesNode(descendants,{...r,serials:serials(s,r.id)})).map(r=>({...r,serials:serials(s,r.id),scope:locationScope(s,r.locationId),matchedSerials:descendants.filter(n=>n.serial&&intersects(n,{...r,serials:serials(s,r.id)})).map(n=>n.serial)}));
 const purchases=[];for(const p of s.operations?.purchases||[])for(const receipt of p.receipts||[])for(const l of receipt.lines)if(includesNode(ancestors,l))purchases.push({purchase:p,receipt,line:l});
 const customers=shipmentEvidence(s).flatMap(sh=>{const allocations=sh.allocations.filter(a=>includesNode(descendants,a));return allocations.length?[{...sh,allocations}]:[];});
 const all=[...ancestors,...descendants],movements=d.movements.flatMap(m=>{const changes=m.changes.filter(c=>includesNode(all,{...c,serials:[...c.added,...c.removed]}));return changes.length?[{...m,changes}]:[];});
 const unlinkedBuilds=business(s).workOrders.filter(w=>w.status==='Completed'&&!d.links.some(l=>l.id===w.id)&&w.consumed?.some(n=>includesNode(all,n)));
 return {query,nodes,descendants,ancestors,inventory,purchases,customers,links,movements,unlinkedBuilds,note:'Exact lot / serial search. Production links identify potentially affected output lots. Returned mixed lots may have more than one possible source. Older records can lack shipment dates, serials or build output links; absence of a match is not proof that stock was never handled.'};
}

const day=v=>{if(!v)return '';must(/^\d{4}-\d{2}-\d{2}$/.test(v)&&Number.isFinite(Date.parse(v))&&new Date(v+'T00:00:00Z').toISOString().slice(0,10)===v,'Use a valid report date.');return v;};
const dateMatches=(value,f,s)=>{if(!f.from&&!f.to)return true;if(!value)return false;const d=businessDay(s,value);return (!f.from||d>=f.from)&&(!f.to||d<=f.to);};
const scopeMatches=(scope,f)=>!f.warehouseId&&!f.ownerId||(!f.warehouseId||f.warehouseId===scope.warehouseId)&&(!f.ownerId||f.ownerId===scope.ownerId);
const itemMatches=(id,f)=>!f.itemId||id===f.itemId;
const round=n=>Math.round(n*10000)/10000;
export const reportTypes=[['valuation','Inventory valuation'],['aging','Stock age & expiry'],['movements','Stock movements'],['purchases','Open & overdue purchases'],['fulfillment','Order fulfillment'],['slow','Slow-moving stock']];
export function warehouseReport(s,type='valuation',filters={},now=new Date().toISOString()){
 must(reportTypes.some(([k])=>k===type),'Choose a report.');const f={...filters,from:day(filters.from),to:day(filters.to)};must(!f.from||!f.to||f.from<=f.to,'Start date must be on or before end date.');
 const b=business(s),d=insights(s),today=businessDay(s,now),i=id=>find(s.items,id),l=id=>find(s.locations,id),warehouse=id=>b.warehouses.find(w=>w.id===id)?.name||id,owner=id=>b.owners.find(o=>o.id===id)?.name||id;
 const stock=s.stock.filter(r=>r.qty>0&&scopeMatches(locationScope(s,r.locationId),f)&&itemMatches(r.itemId,f));
 const ident=r=>[i(r.itemId).sku,i(r.itemId).name,i(r.itemId).description||'',r.lot,l(r.locationId).code,warehouse(locationScope(s,r.locationId).warehouseId),owner(locationScope(s,r.locationId).ownerId)];
 const result={type,title:reportTypes.find(([k])=>k===type)[1],generatedAt:now,filters:f,headers:[],rows:[],note:''};
 if(type==='valuation'){
  result.headers=['SKU','Product','Description','Lot','Location','Warehouse','Owner','On hand','Reserved','Unit cost','Known value','Currency'];
  result.rows=stock.map(r=>{const cost=locationScope(s,r.locationId).ownerId==='owner-self'?s.operations?.costs[r.itemId]:undefined;return [...ident(r),r.qty,r.committed,cost??'Unknown',cost===undefined?'Unknown':isFIFO(s,r.itemId)?allocatedFIFORowValue(s,r)/100:round(r.qty*cost),b.homeCurrency];});
  result.note='Current snapshot. Unknown costs and customer-owned stock are excluded from value totals. Dates do not reconstruct past balances.';if(stock.some(r=>isFIFO(s,r.itemId)))result.note+=' FIFO book value is allocated across physical stock rows for display; this is not specific lot costing. Historical valuation uses separately preserved snapshots.';result.knownValue=round(result.rows.reduce((n,r)=>n+(typeof r[10]==='number'?r[10]:0),0));result.unknownUnits=result.rows.filter(r=>r[10]==='Unknown').reduce((n,r)=>n+r[7],0);
 }
 if(type==='aging'){
  result.headers=['SKU','Product','Description','Lot','Location','Warehouse','Owner','On hand','Earliest recorded receipt','Observed age (days)','Expiry','Expiry status'];
  result.rows=stock.map(r=>{const dates=[];for(const p of s.operations?.purchases||[])for(const rec of p.receipts||[])if(rec.lines.some(n=>n.itemId===r.itemId&&n.lot===r.lot&&n.locationId))dates.push(rec.time);for(const m of d.movements)if(['receiveStock','business:finishWork'].includes(m.command)&&m.changes.some(c=>c.quantity>0&&c.itemId===r.itemId&&c.lot===r.lot))dates.push(m.time);const first=dates.sort()[0],expiry=s.operations?.lots[`${r.itemId}|${r.lot}`]?.expiresOn||'';return [...ident(r),r.qty,first?businessDay(s,first):'Unknown',first?Math.max(0,Math.floor((Date.parse(today)-Date.parse(businessDay(s,first)))/86400000)):'Unknown',expiry||'None',!expiry?'No expiry recorded':expiry<today?'Expired':expiry===today?'Expires today':'Within expiry'];});
  result.note='Current stock; observed age uses the earliest retained receipt for this product / lot, not an exact FIFO age. Opening stock and missing history show Unknown. Date filters do not change this snapshot.';
 }
 if(type==='movements'){
  result.headers=['Time (UTC)','Action','Reference','SKU','Product','Lot','Location','Warehouse','Owner','Quantity change','Reservation change','Recorded balance','Serials added','Serials removed','Operator'];
  result.rows=d.movements.filter(m=>dateMatches(m.time,f,s)).flatMap(m=>m.changes.filter(c=>scopeMatches(c.scope,f)&&itemMatches(c.itemId,f)).map(c=>[m.time,m.description,m.reference,i(c.itemId).sku,i(c.itemId).name,c.lot,l(c.locationId).code,warehouse(c.scope.warehouseId),owner(c.scope.ownerId),c.quantity,c.reserved,c.balance,c.added.join('\n'),c.removed.join('\n'),m.actor]));
  result.note=`One entry per outer transaction and stock bucket; transfers show both sides. History starts ${d.startedAt||'with the next saved action'}. The latest 2,000 stock transactions are retained.${d.truncatedBefore?' Older transactions through '+d.truncatedBefore+' have been removed from this view.':''} Earlier activity remains in Activity and backups.`;
 }
 if(type==='purchases'){
  result.headers=['Purchase','Supplier','SKU','Product','Description','Warehouse','Owner','Ordered','Received','Outstanding','Due','Days overdue','Unit cost (home)','Open value (home)','Currency'];
  result.rows=(s.operations?.purchases||[]).filter(p=>p.status==='Open'&&scopeMatches(p.scope||{warehouseId:'wh-main',ownerId:'owner-self'},f)&&dateMatches(p.due,f,s)).flatMap(p=>purchaseLines(p).filter(n=>n.qty>n.received&&itemMatches(n.itemId,f)).map(n=>[p.number,p.supplier,n.sku||i(n.itemId).sku,n.name||i(n.itemId).name,n.description||i(n.itemId).description||'',warehouse(p.scope?.warehouseId||'wh-main'),owner(p.scope?.ownerId||'owner-self'),n.qty,n.received,n.qty-n.received,p.due||'Unscheduled',p.due?Math.max(0,Math.floor((Date.parse(today)-Date.parse(p.due))/86400000)):0,n.unitCost,round((n.qty-n.received)*n.unitCost),b.homeCurrency]));
  result.note='Current open purchase balances. Date filters apply to due dates; unscheduled purchases appear only when dates are blank. Cancelled and fully received lines are excluded. Includes direct deliveries.';
 }
 if(type==='fulfillment'){
  result.headers=['Order','Customer','Created (UTC)','Status','SKU','Product','Warehouse','Owner','Ordered','Shipped','Remaining'];
  result.rows=s.orders.filter(o=>scopeMatches(orderScope(s,o),f)&&dateMatches(o.createdAt,f,s)).flatMap(o=>o.lines.filter(n=>itemMatches(n.itemId,f)).map(n=>{const shipped=shipmentEvidence(s).filter(sh=>sh.status==='Shipped'&&sh.orderId===o.id).reduce((total,sh)=>total+sh.allocations.filter(a=>a.itemId===n.itemId).reduce((a,v)=>a+v.qty,0),0);return [o.number,o.customer,o.createdAt,o.status,i(n.itemId).sku,i(n.itemId).name,warehouse(orderScope(s,o).warehouseId),owner(orderScope(s,o).ownerId),n.qty,shipped,o.status==='Cancelled'?0:Math.max(0,n.qty-shipped)];}));
  result.note='Current order statuses and shipped quantities, filtered by order creation date. Reversed shipments are excluded; customer returns do not undo the original shipment.';
 }
 if(type==='slow'){
  const start=f.from||businessDay(s,new Date(Date.parse(now)-90*86400000)),end=f.to||today;must(start<=end,'Start date must be on or before end date.');result.filters={...f,from:start,to:end};
  result.headers=['SKU','Product','Warehouse','Owner','Current on hand','Recorded shipped units','Last recorded shipment','Coverage'];
  const groups=new Map();for(const r of stock){const sc=locationScope(s,r.locationId),k=JSON.stringify([r.itemId,sc.warehouseId,sc.ownerId]);if(!groups.has(k))groups.set(k,{itemId:r.itemId,scope:sc,qty:0});groups.get(k).qty+=r.qty;}
  result.rows=[...groups.values()].map(g=>{const sh=shipmentEvidence(s).filter(sh=>sh.status==='Shipped'&&sh.scope.warehouseId===g.scope.warehouseId&&sh.scope.ownerId===g.scope.ownerId),known=sh.filter(sh=>dateMatches(sh.time,{from:start,to:end},s)),units=known.reduce((n,sh)=>n+sh.allocations.filter(a=>a.itemId===g.itemId).reduce((n,a)=>n+a.qty,0),0),last=sh.filter(sh=>sh.time&&sh.allocations.some(a=>a.itemId===g.itemId)).map(sh=>sh.time).sort().at(-1);return [i(g.itemId).sku,i(g.itemId).name,warehouse(g.scope.warehouseId),owner(g.scope.ownerId),g.qty,units,last||'Unknown / none recorded',d.startedAt&&businessDay(s,d.startedAt)<=start&&!sh.some(sh=>!sh.time&&sh.allocations.some(a=>a.itemId===g.itemId))?'Recorded period':'Partial history'];}).sort((a,b)=>a[5]-b[5]);
  result.note=`Current stock ranked by recorded customer shipments from ${start} through ${end}. Production consumption is excluded. Zero with partial history does not establish that an item never moved.`;
 }
 result.filterSummary=`Warehouse: ${f.warehouseId?warehouse(f.warehouseId):'All'} · Owner: ${f.ownerId?owner(f.ownerId):'All'} · Product: ${f.itemId?i(f.itemId).name:'All'} · Dates: ${result.filters.from||'Any'} to ${result.filters.to||'Any'}`;
 return result;
}
export const reportCSV=report=>csvText([[report.title],['Generated (UTC)',report.generatedAt],['Note',report.note],['Filters',report.filterSummary],report.headers,...report.rows]);
export function countCSV(s,c){return csvText([['Cycle count',c.number,c.name],['Status',c.status],['Round',c.round],['SKU','Product','Location','Lot','Expected','Counted','Variance','Serials','Note','Operator'],...c.lines.map(l=>{const visible=!c.blind||c.status!=='Counting';return [find(s.items,l.itemId).sku,find(s.items,l.itemId).name,find(s.locations,l.locationId).code,l.lot,visible?l.expected:'Hidden',l.counted??'',visible&&l.counted!==null?l.counted-l.expected:'',l.countedSerials.join('\n'),l.note,l.enteredBy];})]);}

