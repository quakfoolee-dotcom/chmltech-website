import {pickLines,deliveryLines,outstandingLines} from './fulfillment.mjs?demo=5d9e5d1ce6c83eb1';
// Read-only dashboard projections. Invoice amounts remain integer cents.
import {business,locationScope,orderScope,reorderSuggestions} from './business.mjs?demo=5d9e5d1ce6c83eb1';
import {billing} from './billing.mjs?demo=5d9e5d1ce6c83eb1';
import {purchaseLines} from './purchasing.mjs?demo=5d9e5d1ce6c83eb1';
import {validUnicode,charLength} from './unicode.mjs?demo=5d9e5d1ce6c83eb1';
const must=(v,m)=>{if(!v)throw Error(m);};
const byId=(a,id)=>a.find(x=>x.id===id);
export const dashboardData=s=>s.dashboard||{version:1,orders:{},customerGroups:{}};
export const zone='America/Vancouver';
export function localDay(value=new Date(),timeZone=zone){
 if(typeof value==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(value))return value;
 const d=new Date(value);if(!Number.isFinite(d.getTime()))return '';
 return new Intl.DateTimeFormat('en-CA',{timeZone,year:'numeric',month:'2-digit',day:'2-digit'}).format(d);
}
const date=v=>{must(/^\d{4}-\d{2}-\d{2}$/.test(v||'')&&Number.isFinite(Date.parse(v))&&new Date(v+'T12:00:00Z').toISOString().slice(0,10)===v,'Choose a valid calendar date.');return v;};
const iso=(y,m,d)=>new Date(Date.UTC(y,m,d,12)).toISOString().slice(0,10);
const addDays=(v,n)=>{const d=new Date(v+'T12:00:00Z');d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);};
export const rangePresets=[['year','This year'],['lastYear','Last year'],['month','This month'],['lastMonth','Last month'],['quarter','This quarter'],['lastQuarter','Last quarter'],['financial','This financial year'],['lastFinancial','Last financial year'],['30','Last 30 days'],['60','Last 60 days'],['90','Last 90 days'],['180','Last 180 days'],['365','Last 365 days'],['custom','Custom range']];
export function dateRange(kind='year',today=localDay(),custom={},financialStart=1){
 date(today);must(Number.isInteger(financialStart)&&financialStart>=1&&financialStart<=12,'Financial year starts in a month from 1 to 12.');
 const [y,m]=today.split('-').map(Number),quarter=Math.floor((m-1)/3)*3;
 let from,to;
 if(kind==='custom'){from=date(custom.from);to=date(custom.to);}
 else if(/^\d+$/.test(kind)){const n=Number(kind);must([30,60,90,180,365].includes(n),'Unknown rolling range.');from=addDays(today,1-n);to=today;}
 else if(['year','lastYear'].includes(kind)){const year=y-(kind==='lastYear'?1:0);from=iso(year,0,1);to=iso(year,11,31);}
 else if(['month','lastMonth'].includes(kind)){const mon=m-1-(kind==='lastMonth'?1:0);from=iso(y,mon,1);to=iso(y,mon+1,0);}
 else if(['quarter','lastQuarter'].includes(kind)){const mon=quarter-(kind==='lastQuarter'?3:0);from=iso(y,mon,1);to=iso(y,mon+3,0);}
 else if(['financial','lastFinancial'].includes(kind)){const year=y-(m<financialStart?1:0)-(kind==='lastFinancial'?1:0);from=iso(year,financialStart-1,1);to=iso(year+1,financialStart-1,0);}
 else throw Error('Unknown dashboard date range.');
 must(from<=to,'Start date must precede end date.');must((Date.parse(to)-Date.parse(from))/86400000<=3660,'Use a range of up to ten years.');
 return {from,to,days:Math.round((Date.parse(to)-Date.parse(from))/86400000)+1};
}
export function previousRange(kind,range,today=localDay(),financialStart=1){
 if(kind==='year')return dateRange('lastYear',today,{},financialStart);
 if(kind==='month')return dateRange('lastMonth',today,{},financialStart);
 if(kind==='quarter')return dateRange('lastQuarter',today,{},financialStart);
 if(kind==='financial')return dateRange('lastFinancial',today,{},financialStart);
 return {from:addDays(range.from,-range.days),to:addDays(range.from,-1),days:range.days};
}
const inRange=(d,r)=>!!d&&d>=r.from&&d<=r.to;
const margin=(revenue,cost)=>cost===null||revenue<=0?null:(revenue-cost)/revenue*100;
export const percentChange=(current,previous)=>previous===0?(current===0?{value:0,label:'No change'}:{value:null,label:'New'}):{value:(current-previous)/Math.abs(previous)*100,label:''};
const matchScope=(s,o,warehouse)=>orderScope(s,o).ownerId==='owner-self'&&(!warehouse||warehouse==='*'||orderScope(s,o).warehouseId===warehouse);
export function salesLines(s){
 const b=billing(s),home=business(s).homeCurrency,rows=[];
 for(const d of b.documents.filter(d=>d.status==='Issued'&&(d.kind==='Invoice'||d.kind==='Credit'&&byId(b.documents,d.parentId)?.kind==='Invoice'))){
  const parent=d.kind==='Credit'?byId(b.documents,d.parentId):d,order=byId(s.orders,parent.orderId),shipment=byId(s.shipments,parent.sourceId);
  if(!order||!shipment||shipment.status!=='Shipped'||d.currency!==home||orderScope(s,order).ownerId!=='owner-self')continue;
  for(const l of d.lines){const i=byId(s.items,l.itemId),unit=s.operations?.shipping[shipment.id]?.costSnapshot?.[l.itemId],credit=d.kind==='Credit',returned=credit&&d.returnId&&business(s).returns.some(r=>r.id===d.returnId&&['Received','Restocked','Scrapped'].includes(r.status)),cost=credit&&!returned?0:unit===null||unit===undefined?null:Math.round(unit*l.qty*100)*(credit?-1:1),meta=dashboardData(s).orders[order.id]||{};
   rows.push({id:d.id+'/'+l.sourceLineId,documentId:d.id,number:d.number,kind:d.kind,date:d.date,orderId:order.id,orderNumber:order.number,shipmentId:shipment.id,customerKey:parent.partyKey||'name:'+parent.party.name,customer:parent.party.name,customerGroup:dashboardData(s).customerGroups[parent.partyKey]||'Ungrouped',salesperson:meta.salesperson||'Unassigned',warehouseId:orderScope(s,order).warehouseId,itemId:l.itemId,sku:l.sku,name:l.name,description:l.description,category:i?.category||'Uncategorised',qty:l.qty*(credit?-1:1),revenue:l.net*(credit?-1:1),cost,margin:margin(l.net*(credit?-1:1),cost),currency:d.currency});
  }
 }
 return rows;
}
const sumRows=rows=>{const revenue=rows.reduce((n,r)=>n+r.revenue,0),knownCost=rows.reduce((n,r)=>n+(r.cost??0),0),missing=rows.filter(r=>r.cost===null).length;return {revenue,cost:missing?null:knownCost,knownCost,missing,margin:margin(revenue,missing?null:knownCost),qty:rows.reduce((n,r)=>n+r.qty,0)};};
function group(rows,key,name){const map=new Map();for(const r of rows){const id=r[key],g=map.get(id)||{key:id,name:typeof name==='function'?name(r):r[name||key],rows:[]};g.rows.push(r);map.set(id,g);}return [...map.values()].map(g=>({...g,...sumRows(g.rows),orders:new Set(g.rows.filter(r=>r.kind==='Invoice').map(r=>r.orderId)).size})).sort((a,b)=>b.revenue-a.revenue||a.name.localeCompare(b.name));}
export function salesDashboard(s,filters={},today=localDay(undefined,s.organization?.timezone)){
 const range=filters.range||dateRange('year',today),previous=filters.previous||previousRange('year',range,today),warehouse=filters.warehouse||'*',all=salesLines(s),filter=r=>(warehouse==='*'||r.warehouseId===warehouse)&&(!filters.category||r.category===filters.category)&&(!filters.customer||r.customerKey===filters.customer)&&(!filters.group||r.customerGroup===filters.group)&&(!filters.salesperson||r.salesperson===filters.salesperson)&&(!filters.margin||r.margin!==null&&(filters.margin==='good'?r.margin>=30:filters.margin==='medium'?r.margin>=15&&r.margin<30:filters.margin==='negative'?r.margin<0:r.margin>=0&&r.margin<15));
 const current=all.filter(r=>filter(r)&&inRange(r.date,range)),prior=all.filter(r=>filter(r)&&inRange(r.date,previous)),summary=sumRows(current),priorSummary=sumRows(prior),orders=group(current,'orderId',r=>r.orderNumber),previousOrders=group(prior,'orderId',r=>r.orderNumber),invoiceOrders=orders.filter(g=>g.rows.some(r=>r.kind==='Invoice'));
 const kpis={...summary,orders:invoiceOrders.length,average:invoiceOrders.length?Math.round(summary.revenue/invoiceOrders.length):null},previousKPIs={...priorSummary,orders:previousOrders.filter(g=>g.rows.some(r=>r.kind==='Invoice')).length};
 previousKPIs.average=previousKPIs.orders?Math.round(previousKPIs.revenue/previousKPIs.orders):null;
 const months=[];let [y,m]=range.from.split('-').map(Number);for(let guard=0;guard<121;guard++){const key=`${y}-${String(m).padStart(2,'0')}`;if(key>range.to.slice(0,7))break;const rows=current.filter(r=>r.date.startsWith(key)),summary=sumRows(rows),index=months.length,py=new Date(previous.from+'T12:00:00Z');py.setUTCMonth(py.getUTCMonth()+index);const previousKey=py.toISOString().slice(0,7);months.push({key,label:new Intl.DateTimeFormat('en',{month:'short',year:'2-digit',timeZone:'UTC'}).format(new Date(key+'-15T12:00:00Z')),rows,...summary,previous:sumRows(prior.filter(r=>r.date.startsWith(previousKey)))});if(++m===13){y++;m=1;}}
 const customers=group(current,'customerKey','customer'),products=group(current,'itemId',r=>r.sku+' · '+r.name),categories=group(current,'category'),groups=group(current,'customerGroup'),people=group(current,'salesperson');
 const operationalFilter=o=>matchScope(s,o,warehouse)&&(!filters.category||o.lines.some(l=>(byId(s.items,l.itemId)?.category||'Uncategorised')===filters.category))&&(!filters.customer||(o.customerId||'order:'+o.id)===filters.customer)&&(!filters.group||(dashboardData(s).customerGroups[o.customerId||'order:'+o.id]||'Ungrouped')===filters.group)&&(!filters.salesperson||(dashboardData(s).orders[o.id]?.salesperson||'Unassigned')===filters.salesperson);
 const drafts=s.orders.filter(o=>o.status==='Draft'&&operationalFilter(o)&&inRange(localDay(o.createdAt,s.organization?.timezone),range)),draftValues=drafts.map(o=>({order:o,value:o.pricedLines?.length===o.lines.length?Math.round(o.pricedLines.reduce((n,l)=>n+l.qty*l.unitPrice,0)*100):null}));
 const physical=s.shipments.filter(sh=>sh.status==='Shipped'&&operationalFilter(byId(s.orders,sh.orderId))&&(!filters.margin||orders.some(o=>o.key===sh.orderId))&&inRange(localDay(sh.shippedAt,s.organization?.timezone),range));
 const delivery=physical.map(sh=>{const o=byId(s.orders,sh.orderId),promised=dashboardData(s).orders[o.id]?.promisedDate||'',completed=localDay(sh.shippedAt,s.organization?.timezone),family=Object.values(s.operations?.families||{}).find(f=>f.orderIds.includes(o.id));let full=true,last=completed;
  if(family){full=family.orderIds.every(id=>byId(s.orders,id)?.status==='Fulfilled');const dates=s.shipments.filter(x=>x.status==='Shipped'&&family.orderIds.includes(x.orderId)).map(x=>localDay(x.shippedAt,s.organization?.timezone));last=dates.sort().at(-1)||completed;}
  return {orderId:o.id,number:o.number,promised,completed:last,eligible:!!promised,onTime:!!promised&&full&&last<=promised,lateDays:promised?Math.max(0,Math.round((Date.parse(last)-Date.parse(promised))/86400000)):null};});
 const eligible=delivery.filter(x=>x.eligible),ifot=eligible.length?eligible.filter(x=>x.onTime).length/eligible.length*100:null;
 const earliest=new Map();for(const r of all.filter(r=>r.kind==='Invoice'))if(!earliest.has(r.customerKey)||r.date<earliest.get(r.customerKey))earliest.set(r.customerKey,r.date);
 const cohorts=customers.map(c=>({...c,cohort:inRange(earliest.get(c.key),range)?'New':'Repeat'}));
 const inactive=group(all.filter(r=>filter(r)),'customerKey','customer').map(c=>({...c,lastDate:c.rows.filter(r=>r.kind==='Invoice').map(r=>r.date).sort().at(-1)||'',days:Math.round((Date.parse(today)-Date.parse(c.rows.filter(r=>r.kind==='Invoice').map(r=>r.date).sort().at(-1)))/86400000)})).filter(c=>c.days>=90);
 const unsold=s.items.filter(i=>(!filters.category||i.category===filters.category)&&!current.some(r=>r.itemId===i.id&&r.kind==='Invoice'));
 const slow=s.items.filter(i=>!filters.category||i.category===filters.category).map(i=>{const onHand=s.stock.filter(r=>r.itemId===i.id&&locationScope(s,r.locationId).ownerId==='owner-self'&&(warehouse==='*'||locationScope(s,r.locationId).warehouseId===warehouse)).reduce((n,r)=>n+r.qty,0),sold=Math.max(0,current.filter(r=>r.itemId===i.id).reduce((n,r)=>n+r.qty,0)),velocity=sold/range.days;return {itemId:i.id,sku:i.sku,name:i.name,onHand,sold,velocity,days:velocity?onHand/velocity:null};}).filter(i=>i.onHand>0&&i.velocity<1).sort((a,b)=>(b.days??Infinity)-(a.days??Infinity));
 const lateCogs=[...(s.costing?.matches||[]),...(s.costing?.allocations||[])].filter(a=>inRange(localDay(a.time,s.organization?.timezone),range)).flatMap(a=>a.rows).filter(r=>(!filters.category||byId(s.items,r.itemId)?.category===filters.category)&&(warehouse==='*'||s.operations?.purchases.find(p=>p.id===s.costing?.pools.find(x=>x.id===r.poolId)?.purchaseId)?.scope?.warehouseId===warehouse)).reduce((n,r)=>n+r.cogs,0);
 const closedShort=(dashboardData(s).closedShort||[]).filter(r=>inRange(localDay(r.time,s.organization?.timezone),range)&&(warehouse==='*'||r.warehouseId===warehouse)&&(!filters.category||r.category===filters.category)&&(!filters.customer||r.customerKey===filters.customer)&&(!filters.group||(dashboardData(s).customerGroups[r.customerKey]||'Ungrouped')===filters.group)&&(!filters.salesperson||r.salesperson===filters.salesperson));
 return {range,previous,today,currency:business(s).homeCurrency,lines:current,all,kpis,previousKPIs,months,orders,customers,products,categories,groups,people,drafts:draftValues,estimatesValue:draftValues.reduce((n,r)=>n+(r.value??0),0),unpricedDrafts:draftValues.filter(r=>r.value===null).length,delivery,ifot,missingDelivery:delivery.length-eligible.length,unsold,slow,cohorts,inactive,closedShort,closedShortQty:closedShort.reduce((n,r)=>n+r.qty,0),closedShortValue:closedShort.reduce((n,r)=>n+(r.value??0),0),unpricedClosures:closedShort.filter(r=>r.value===null).length,low:orders.filter(o=>o.margin!==null&&o.margin>=0&&o.margin<15),negative:orders.filter(o=>o.margin!==null&&o.margin<0),high:orders.filter(o=>o.revenue>1000000),lateCogs,foreignExcluded:billing(s).documents.filter(d=>d.kind==='Invoice'&&d.status==='Issued'&&d.currency!==business(s).homeCurrency).length};
}
export const gadgets=[['salesGoal','Sales Goal Chart'],['topProducts','Top Products Chart'],['openSales','Open Sales Orders'],['openPurchases','Open Purchase Orders'],['work','Open Work Orders'],['transfers','Open Transfer Orders'],['returns','Open RMA Orders'],['pick','Items to be Picked'],['receive','Items to be Received'],['ship','Items to be Shipped'],['inventory','Inventory Value'],['short','Low Stock'],['report','Report'],['links','Quick Links'],['website','Website']];
export function warehouseDashboard(s,warehouse='*',today=localDay(undefined,s.organization?.timezone)){
 const scope=o=>matchScope(s,o,warehouse),rows={};
 const make=(id,number,name,qty,status,href)=>({id,number,name,qty,status,href});
 rows.openSales=s.orders.filter(o=>!['Fulfilled','Cancelled'].includes(o.status)&&scope(o)).map(o=>make(o.id,o.number,o.customer,(o.fulfillment?outstandingLines(s,o):o.lines).reduce((n,l)=>n+l.qty,0),o.status,`#orders/${o.id}`));
 rows.openPurchases=(s.operations?.purchases||[]).filter(p=>p.status==='Open'&&scope(p)).map(p=>make(p.id,p.number,p.supplier,purchaseLines(p).reduce((n,l)=>n+l.qty-l.received,0),p.due&&p.due<today?'Overdue':'Open',`#purchasing/${p.id}`));
 rows.work=business(s).workOrders.filter(w=>!['Completed','Cancelled'].includes(w.status)&&scope(w)).map(w=>make(w.id,w.number,byId(s.items,w.outputId)?.name,w.qty,w.status,'#business/manufacturing'));
 rows.transfers=business(s).transfers.filter(t=>['Draft','In transit'].includes(t.status)).filter(t=>{const r=byId(s.stock,t.stockId);return warehouse==='*'||locationScope(s,r.locationId).warehouseId===warehouse||locationScope(s,t.destination).warehouseId===warehouse;}).map(t=>make(t.id,t.number,byId(s.items,byId(s.stock,t.stockId).itemId)?.name,t.qty-t.received,t.status,'#business/transfers'));
 rows.returns=business(s).returns.filter(r=>!['Restocked','Scrapped','Sent','Cancelled'].includes(r.status)).filter(r=>{const o=byId(r.kind==='Customer'?s.orders:s.operations?.purchases||[],r.sourceId);return o&&scope(o);}).map(r=>make(r.id,r.number,r.kind+' · '+byId(s.items,r.itemId)?.name,r.qty,r.status,'#business/returns'));
 rows.pick=s.picks.filter(p=>p.status!=='Finished'&&scope(byId(s.orders,p.orderId))&&byId(s.orders,p.orderId).status!=='Cancelled').map(p=>{const o=byId(s.orders,p.orderId);return make(p.id,p.number,o.customer,pickLines(s,p).reduce((n,l)=>n+l.qty,0),p.status,`#picking/${p.id}`);});
 rows.receive=rows.openPurchases;rows.ship=s.shipments.filter(sh=>!['Shipped','Cancelled'].includes(sh.status)&&scope(byId(s.orders,sh.orderId))).map(sh=>{const o=byId(s.orders,sh.orderId);return make(sh.id,sh.number,o.customer,deliveryLines(s,sh).reduce((n,l)=>n+l.qty,0),sh.status,`#shipping/${sh.id}`);});
 const stock=s.stock.filter(r=>locationScope(s,r.locationId).ownerId==='owner-self'&&(warehouse==='*'||locationScope(s,r.locationId).warehouseId===warehouse)),missing=new Set(stock.filter(r=>r.qty>0&&s.operations?.costs[r.itemId]===undefined).map(r=>r.itemId));
 return {rows,units:stock.reduce((n,r)=>n+r.qty,0),value:Math.round(stock.reduce((n,r)=>n+r.qty*(s.operations?.costs[r.itemId]??0),0)*100),missing:missing.size,currency:business(s).homeCurrency,short:reorderSuggestions(s,warehouse).map(r=>({...r,item:byId(s.items,r.itemId)}))};
}
const text=(v,max)=>{const t=String(v??'').trim();must(validUnicode(t)&&charLength(t)<=max,'Enter valid text within the field limit.');return t;};
export function dashboardCommand(s,command,p,ctx){
 if(!command.startsWith('dashboard:'))return null;
 const d=s.dashboard||(s.dashboard={version:1,orders:{},customerGroups:{}});
 if(command==='dashboard:closeShort'){
  const o=byId(s.orders,p.id),line=o?.lines.find(l=>l.itemId===p.itemId),qty=Number(p.qty);
  must(o&&['Draft','Issued'].includes(o.status)&&orderScope(s,o).ownerId==='owner-self','Close short only an owned draft or issued order before reserving stock.');
  must(!o.pickId||byId(s.picks,o.pickId)?.status==='Entered','Release reservations before closing short.');
  must(line&&Number.isSafeInteger(qty)&&qty>0&&qty<=line.qty,'Close a whole quantity within the remaining order line.');
  const reason=text(p.reason,240);must(reason,'Enter the close-short reason.');
  const item=byId(s.items,p.itemId),price=o.pricedLines?.find(l=>l.itemId===p.itemId)?.unitPrice,record={id:'short-'+((d.closedShort||[]).length+1),time:ctx.time,sourceOrderId:o.id,sourceNumber:o.number,orderId:o.id,warehouseId:orderScope(s,o).warehouseId,customerKey:o.customerId||'order:'+o.id,customer:o.customer,itemId:item.id,sku:item.sku,name:item.name,category:item.category||'Uncategorised',salesperson:d.orders[o.id]?.salesperson||'Unassigned',qty,value:price===undefined?null:Math.round(price*qty*100),reason};
  if(o.lines.length===1&&qty===line.qty){const result=ctx.dispatch(s,'cancelOrder',{id:o.id},{now:ctx.time});Object.assign(s,result.state);}
  else {const keep=o.lines.map(l=>({itemId:l.itemId,qty:l.qty-(l.itemId===p.itemId?qty:0)})),split=ctx.dispatch(s,'splitOrder',{id:o.id,lines:keep},{now:ctx.time});Object.assign(s,split.state);record.orderId=split.resultId;const cancelled=ctx.dispatch(s,'cancelOrder',{id:split.resultId},{now:ctx.time});Object.assign(s,cancelled.state);}
  s.dashboard.closedShort||=[];s.dashboard.closedShort.push(record);
  return {type:'Sales order closed short',message:`${qty} ${item.uom} of ${item.sku} closed short. ${reason}`,reference:o.number,resultId:record.orderId};
 }
 if(command==='dashboard:orderDetails'){must(byId(s.orders,p.id),'Order not found.');const promisedDate=p.promisedDate?date(p.promisedDate):'';d.orders[p.id]={promisedDate,salesperson:text(p.salesperson,100)};return {type:'Dashboard order details saved',message:'Promised dispatch date and salesperson saved.',reference:p.id,resultId:p.id};}
 if(command==='dashboard:customerGroup'){must(business(s).customers.some(c=>c.id===p.id)||billing(s).documents.some(x=>x.kind==='Invoice'&&x.partyKey===p.id),'Customer not found.');d.customerGroups[p.id]=text(p.group,100);return {type:'Dashboard customer group saved',message:'Customer group saved.',reference:p.id,resultId:p.id};}
 throw Error('Unknown dashboard action.');
}
export function validateDashboard(s){if(!s.dashboard)return;const d=s.dashboard;must(d.version===1&&d.orders&&d.customerGroups,'Invalid dashboard metadata.');for(const [id,m]of Object.entries(d.orders)){must(byId(s.orders,id),'Dashboard order not found.');if(m.promisedDate)date(m.promisedDate);text(m.salesperson,100);}for(const [id,g]of Object.entries(d.customerGroups)){must(business(s).customers.some(c=>c.id===id)||billing(s).documents.some(x=>x.kind==='Invoice'&&x.partyKey===id),'Dashboard customer not found.');text(g,100);}const records=d.closedShort||[];must(Array.isArray(records)&&new Set(records.map(r=>r.id)).size===records.length,'Invalid close-short history.');for(const r of records){must(byId(s.orders,r.sourceOrderId)&&byId(s.orders,r.orderId)?.status==='Cancelled'&&byId(s.items,r.itemId)&&Number.isSafeInteger(r.qty)&&r.qty>0&&(r.value===null||Number.isSafeInteger(r.value)&&r.value>=0)&&Number.isFinite(Date.parse(r.time)),'Invalid closed-short source.');must(text(r.reason,240),'Close-short reason is required.');}}

