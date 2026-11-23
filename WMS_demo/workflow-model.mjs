import {navigationGroups,navigationContext} from './navigation.mjs?demo=2d15b6e9cd84b84d';
import {workAttention,orderAttention} from './production-signals.mjs?demo=2d15b6e9cd84b84d';
import {receivingSuggestions} from './receiving-control.mjs?demo=2d15b6e9cd84b84d';
import {purchaseStatus} from './procurement.mjs?demo=2d15b6e9cd84b84d';
import {billingStatus} from './billing.mjs?demo=2d15b6e9cd84b84d';
// Read-only projections of existing records. This module never dispatches or
// stores workflow states; transactional validation remains authoritative.
const spec=(path,steps,actions=[])=>({path,steps,actions});
const review=['Review records','Review details','Choose an action'];
const purchasing=['Draft','Pending approval','Approved','Issued','Closed'];
const shipping=['Entered','Packed','Shipped'];
const inspection=['Draft','Submitted','Released'];
const task=['Open','Completed'];
const definitions={
 inventory:spec('items',['Review stock','Review details','Choose an action'],['receive','move','count','lot-info','new-item']),
 purchasing:spec('operations.purchases',purchasing,['plan-submit','plan-approve','plan-issue','receive-purchase','new-purchase']),
 suppliers:spec('operations.suppliers',review,['edit-supplier','new-supplier']),
 orders:spec('orders',['Draft','Issued','Picked','Fulfilled'],['delivery-release','issue-order','new-order']),
 picking:spec('picks',['Entered','Committed','Started','Finished'],['reserve','start-pick','finish']),
 shipping:spec('shipments',shipping,['pack','ship','shipment-details']),
 locations:spec('locations',review,['new-location']),
 activity:spec('events',review,['export']),
 dashboards:spec('',review,['dash-refresh']),
 'business/production-orders':spec('production.orders',['Planned','In progress','Completed'],['prod-stage','prod-complete','prod-start','prod-plan']),
 'business/production-boms':spec('production.boms',review,['prod-bom']),
 'business/production-labor':spec('production.labor',['Submitted','Approved'],['prod-approve']),
 'business/production-materials':spec('production.orders',review,['prod-mrp-propose','prod-mrp-purchase']),
 'business/production-schedule':spec('production.orders',review,['prod-schedule','prod-center']),
 'business/manufacturing':spec('business.workOrders',['Planned','In progress','Completed'],['biz-startWork','biz-finishWork','biz-work']),
 'business/quality-inspections':spec('receivingControl.inspections',inspection,['rcv-submitInspection','rcv-approveInspection','rcv-createTask','rcv-createInspection']),
 'business/directed-putaway':spec('receivingControl.tasks',task,['rcv-finishTask','rcv-createTask','rcv-bin']),
 'business/bin-replenishment':spec('receivingControl.tasks',task,['rcv-finishTask','rcv-createTask']),
 'business/transfers':spec('business.transfers',['Draft','In transit','Received'],['biz-shipTransfer','biz-receiveTransfer','biz-transfer']),
 'business/counts':spec('insights.counts',['Counting','Review','Posted'],['ins-entry','ins-submit','ins-approve','ins-create']),
 'business/approvals':spec('operations.purchases',purchasing,['plan-submit','plan-approve','plan-issue']),
 'business/receiving':spec('operations.purchases',['Issued','Received','Closed'],['receive-purchase']),
 'business/returns/supplier':spec('business.returns',['Requested','Sent'],['biz-sendReturn','biz-supplierReturn']),
 'business/returns/customer':spec('business.returns',['Requested','Received','Restocked / Scrapped / Completed'],['biz-receiveReturn','biz-disposeReturn','biz-customerReturn']),
 'business/quotes':spec('salesDesk.quotes',['Draft','Issued','Accepted','Converted'],['biz-sales-issue','biz-sales-accept','biz-sales-convert','biz-sales-new']),
 'business/crm-customers':spec('crm.profiles',review,['biz-crm-profile']),
 'business/opportunities':spec('crm.opportunities',['Lead','Qualified','Quoted','Negotiation','Won'],['biz-crm-stage','biz-crm-opportunity']),
 'business/followups':spec('crm.activities',['Open','Completed'],['biz-crm-complete','biz-crm-activity']),
 'business/invoices':spec('billing.documents',['Draft','Issued','Paid'],['bill-issue','bill-payment','bill-newInvoice']),
 'business/bills':spec('billing.documents',['Draft','Issued','Paid'],['bill-issue','bill-payment','bill-newBill']),
 'business/credits':spec('billing.documents',['Draft','Credit issued'],['bill-issue','bill-chooseCredit']),
 'business/payments':spec('billing.payments',review,['bill-choosePayment']),
 'business/accounting':spec('business.journals',['Ready for review','Reviewed'],['biz-reviewJournal','biz-journalExport']),
 'business/costing':spec('costing.matches',review,['cost-inspect','cost-enable']),
 'business/quickbooks':spec('',review,['cloud-qbo-refresh','cloud-qbo-compare','cloud-qbo-view']),
 'business/reconciliation':spec('',review,['recon-preview','recon-refresh']),
 'business/fifo':spec('costLayers.layers',review,['value-refresh']),
 'business/reorder':spec('business.reorders',review,['biz-approveReorder','biz-reorder']),
 'business/products':spec('items',review,['biz-profile']),
 'business/units':spec('items',review,['biz-unitNew']),
 'business/buying':spec('business.vendorPrices',review,['biz-vendorPrice']),
 'business/trace':spec('',review,['ins-traceSearch']),
 'business/pricing':spec('',review,['biz-sales-rule']),
 'business/customers':spec('business.customers',review,['biz-customer']),
 'business/kits':spec('business.kits',review,['biz-kit']),
 'business/scanner':spec('',review,[]),
 'business/valuation':spec('',review,['value-refresh']),
 'business/dashboard':spec('',review,[]),
 'business/forecast':spec('',review,['plan-refresh']),
 'business/reports':spec('',review,['ins-reportPreview']),
 'business/network':spec('business.warehouses',review,['biz-warehouse']),
 'business/exchange':spec('',review,['biz-exchange']),
 'business/admin':spec('',review,['biz-audit']),
 overview:spec('',review,[])
};
export const workflowSpecs=Object.freeze(Object.fromEntries([...navigationGroups.flatMap(g=>g.modules).map(m=>[m.route,Object.freeze({...definitions[m.route],route:m.route,label:m.label})]),['overview',Object.freeze({...definitions.overview,route:'overview',label:'Overview'})]]));
const rowsAt=(s,path)=>path?path.split('.').reduce((v,k)=>v?.[k],s)||[]:[];
export function workflowModel(s,hash,{focusId=''}={}){
 const c=navigationContext(hash),route=c.module?.route||'overview',d=workflowSpecs[route];
 let rows=rowsAt(s,d.path);if(!Array.isArray(rows))rows=[];
 if(route==='business/directed-putaway')rows=rows.filter(t=>t.kind==='Putaway');
 if(route==='business/bin-replenishment')rows=rows.filter(t=>t.kind==='Replenishment');
 if(route==='business/returns/supplier')rows=rows.filter(t=>t.kind==='Supplier');
 if(route==='business/returns/customer')rows=rows.filter(t=>t.kind==='Customer');
 if(['business/invoices','business/bills','business/credits'].includes(route)){const kind={'business/invoices':'Invoice','business/bills':'Bill','business/credits':'Credit'}[route];rows=rows.filter(r=>r.kind===kind);}
 const id=(hash||'').replace(/^#/,'').slice(route.length+1).split('/')[0]||focusId;
 let record=rows.find(r=>r.id===id),order;
 if(route==='business/production-orders'&&id){order=(s.production?.orders||[]).find(o=>o.id===id||o.workOrders.some(w=>w.id===id));record=order?.id===id?order:order?.workOrders.find(w=>w.id===id);}
 let status=record?.status||record?.stage||(record?'Review details':rows.length?'Review records':d.path?'No records yet.':'Ready for review'),blockers=[],actions=d.actions,nextRoute='',nextLabel='';
 if(record&&route==='purchasing')status=purchaseStatus(s,record);
 if(record&&['business/invoices','business/bills','business/credits'].includes(route))status=billingStatus(s,record);
 if(record&&route==='business/production-orders'){
  const signals=record.workOrders?orderAttention(s,record):workAttention(s,order,record);
  blockers=signals.filter(a=>['waiting-children','material-shortage','missing-cost','labor-approval','labor-rejected'].includes(a.code)).map(a=>a.label);
  if(record.stages){const allDone=record.stages.every(x=>x.status==='Done');actions=status==='Planned'?['prod-start']:status==='In progress'?(allDone?['prod-complete']:['prod-stage','prod-labor']):[];if(allDone&&blockers.length)actions=['prod-complete'];if(signals.some(a=>a.code==='labor-rejected'))actions=['prod-labor'];}
  if(signals.some(a=>a.code==='labor-approval')){nextRoute='business/production-labor';nextLabel='Review labor approvals';}
 }
 if(record&&route==='business/quality-inspections'){
  actions=status==='Draft'?['rcv-submitInspection']:status==='Submitted'?['rcv-approveInspection']:status==='Released'&&record.accepted>record.moved?['rcv-createTask']:[];
  if(status==='Released'&&record.accepted>record.moved){
   if((s.receivingControl?.tasks||[]).some(t=>t.inspectionId===record.id&&t.status==='Open')){nextRoute='business/directed-putaway';nextLabel='Review putaway tasks';}
   else if(!receivingSuggestions(s,{stockId:record.stockId,inspectionId:record.id,kind:'Putaway'}).length)blockers=['No eligible bin or quantity is currently available.'];
  }
  if(status==='Released'&&record.accepted>0&&record.accepted===record.moved){nextRoute='business/bin-replenishment';nextLabel='Review picking replenishment';}
 }
 if(record&&route==='orders'&&record.pickId&&status!=='Cancelled'){nextRoute='picking/'+record.pickId;nextLabel='Review picking';}
 if(record&&route==='picking'&&status==='Finished'){const sh=(s.shipments||[]).find(x=>x.pickId===record.id);if(sh){nextRoute='shipping/'+sh.id;nextLabel='Review shipping';}}
 return {route,label:d.label,steps:d.steps,status,recordId:record?.id||'',recordLabel:record?.number||record?.reference||record?.sku||record?.id||'',count:rows.length,blockers,actionBlocked:blockers.length>0&&actions[0]!=='prod-labor',actions,nextRoute,nextLabel,terminal:!!record&&(['Completed','Cancelled','Closed','Fulfilled','Paid','Voided','Restocked','Scrapped','Sent'].includes(status)||route==='shipping'&&status==='Shipped'||route==='business/transfers'&&status==='Received'||route==='business/quality-inspections'&&status==='Released'&&record.moved===record.accepted)};
}
