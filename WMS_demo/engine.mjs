import {receivingCommand,beforeReceiving,validateReceiving} from './receiving-control.mjs?demo=9c44c6dabb8d4728';
import {productionCommand,validateProduction,beforeProduction} from './production.mjs?demo=9c44c6dabb8d4728';
import {pickLines,deliveryLines,outstandingLines,releaseDelivery,fulfillmentStatus,validateFulfillment} from './fulfillment.mjs?demo=9c44c6dabb8d4728';
import {beforeExecution,afterExecution,executionCommand,validateExecution} from './warehouse-execution.mjs?demo=9c44c6dabb8d4728';
import {beforeUnits,afterUnits,unitsCommand,validateUnits} from './packaging.mjs?demo=9c44c6dabb8d4728';
import {mobileStockCommand,validateMobileStock} from './mobile-stock.mjs?demo=9c44c6dabb8d4728';
import {pricingCommand,validateSalesDesk} from './pricing.mjs?demo=9c44c6dabb8d4728';
import {quotationCommand,validateQuotations} from './quotations.mjs?demo=9c44c6dabb8d4728';
import {crmCommand,validateCRM} from './crm.mjs?demo=9c44c6dabb8d4728';
import {beforeTransferCosting,afterTransferCosting,transferCostCommand,validateTransferCosting} from './transfer-costing.mjs?demo=9c44c6dabb8d4728';
import {beforeFIFO,afterFIFOStock,afterFIFOAccounting,validateFIFO} from './fifo.mjs?demo=9c44c6dabb8d4728';
import {procurementCommand,beforeProcurement,afterProcurement,validateProcurement} from './procurement.mjs?demo=9c44c6dabb8d4728';
// Original implementation of the stock-state model documented in this project.
// Every command operates on a clone and validates before returning a new state.
import {expired,stockCandidates,validateOperations,beforeOperation,afterOperation,extendedCommand,setupOps} from './operations.mjs?demo=9c44c6dabb8d4728';
import {charLength,cutText,validUnicode} from './unicode.mjs?demo=9c44c6dabb8d4728';
import {businessCommand,validateBusiness,beforeBusiness,afterBusiness,stockInScope,orderScope,locationScope} from './business.mjs?demo=9c44c6dabb8d4728';
import {countCommand,validateInsights,afterInsights} from './insights.mjs?demo=9c44c6dabb8d4728';
import {dashboardCommand,validateDashboard} from './dashboard.mjs?demo=9c44c6dabb8d4728';
import {costCommand,beforeCosting,afterCosting,validateCosting} from './costing.mjs?demo=9c44c6dabb8d4728';
import {billingCommand,validateBilling,beforeBilling} from './billing.mjs?demo=9c44c6dabb8d4728';
export class WmsError extends Error {}
const fail = message => { throw new WmsError(message); };
const requireThat = (condition, message) => { if (!condition) fail(message); };
const find = (rows, id, label) => rows.find(row => row.id === id) || fail(`${label} not found.`);
const whole = (value, label = 'Quantity', allowZero = false) => {
  const n = Number(value);
  requireThat(Number.isSafeInteger(n) && n >= (allowZero ? 0 : 1) && n <= 10000000, `${label} must be a whole number ${allowZero ? 'of zero or more' : 'greater than zero'}.`);
  return n;
};
const clean = (value, label, max = 100) => {
  const text = String(value ?? '').trim();
  requireThat(text.length > 0 && charLength(text) <= max && validUnicode(text), `${label} is required (up to ${max} characters).`);
  return text;
};
const optionalText=(value,label,max)=>{const t=String(value??'');requireThat(charLength(t)<=max&&validUnicode(t),`${label} exceeds ${max} characters or contains invalid Unicode.`);return t;};
const uid = (s, type) => `${type}-${++s.counters[type]}`;
const note = (value = '') => cutText(String(value).trim(),240);
const stockAt = (s, itemId, locationId, lot) => {
  let stock = s.stock.find(r => r.itemId === itemId && r.locationId === locationId && r.lot === lot);
  if (!stock) { stock = { id: uid(s, 'stock'), itemId, locationId, lot, qty: 0, committed: 0 }; s.stock.push(stock); }
  return stock;
};
export const itemById = (s, id) => find(s.items, id, 'Item');
export const locationById = (s, id) => find(s.locations, id, 'Location');
export const orderById = (s, id) => find(s.orders, id, 'Order');
export const pickById = (s, id) => find(s.picks, id, 'Pick');
export const shipmentById = (s, id) => find(s.shipments, id, 'Shipment');

export function totals(s, itemId, asOf) {
  if(!itemId)return s.items.reduce((sum,item)=>{const t=totals(s,item.id,asOf);for(const key of Object.keys(sum))sum[key]+=t[key];return sum;},{onHand:0,committed:0,allocated:0,available:0,pickable:0});
  const rows = s.stock.filter(r => !itemId || r.itemId === itemId);
  const onHand = rows.reduce((v, r) => v + r.qty, 0);
  const committed = rows.reduce((v, r) => v + r.committed, 0);
  const allocated = s.orders.filter(o => !['Draft', 'Cancelled', 'Fulfilled'].includes(o.status)).reduce((n, o) => n + (o.fulfillment?outstandingLines(s,o):o.lines).filter(l => !itemId || l.itemId === itemId).reduce((m, l) => m + l.qty, 0), 0);
  const unavailable = rows.filter(r => !locationById(s, r.locationId).available || expired(s,r,asOf)).reduce((v, r) => v + r.qty - r.committed, 0);
  const unpickable = rows.filter(r => !locationById(s, r.locationId).pickable || expired(s,r,asOf)).reduce((v, r) => v + r.qty - r.committed, 0);
  return { onHand, committed, allocated, available: Math.max(0, onHand - allocated - unavailable), pickable: Math.max(0, onHand - committed - unpickable) };
}
export function shortages(s, order, asOf) {
  return order.lines.map(l => {const available=stockCandidates(s,l.itemId,asOf).filter(r=>stockInScope(s,r,orderScope(s,order))).reduce((n,r)=>n+r.qty-r.committed,0);return {item:itemById(s,l.itemId),required:l.qty,available,short:Math.max(0,l.qty-available)};}).filter(r=>r.short>0);
}

export function createSeed(now = '2026-10-13T09:00:00.000Z') {
  return {
    schemaVersion: 1, revision: 0, updatedAt: now,
    counters: { stock: 7, item: 6, order: 1043, pick: 2043, shipment: 3040, event: 1, location: 5 },
    items: [
      { id: 'item-1', sku: 'TOTE-042', name: 'Stackable utility tote', category: 'Storage', uom: 'ea', reorderPoint: 25, color: '#d9e8dc', icon: 'box' },
      { id: 'item-2', sku: 'LBL-100', name: 'Thermal shipping labels', category: 'Packaging', uom: 'roll', reorderPoint: 40, color: '#e8decd', icon: 'layers' },
      { id: 'item-3', sku: 'BOLT-M8', name: 'Hex bolt · M8 × 40', category: 'Hardware', uom: 'ea', reorderPoint: 120, color: '#dce1ec', icon: 'hex' },
      { id: 'item-4', sku: 'GLOVE-07', name: 'Work gloves · medium', category: 'Safety', uom: 'pair', reorderPoint: 30, color: '#ebddd4', icon: 'hand' },
      { id: 'item-5', sku: 'TAPE-048', name: 'Packing tape · 48 mm', category: 'Packaging', uom: 'roll', reorderPoint: 50, color: '#e8e4d1', icon: 'circle' },
      { id: 'item-6', sku: 'BIN-012', name: 'Small parts organizer', category: 'Storage', uom: 'ea', reorderPoint: 20, color: '#dae8e8', icon: 'grid' }
    ],
    locations: [
      { id: 'location-1', code: 'A-01', name: 'Main picking aisle', type: 'Storage', pickable: true, available: true },
      { id: 'location-2', code: 'A-02', name: 'Bulk storage', type: 'Storage', pickable: true, available: true },
      { id: 'location-3', code: 'SHIP-01', name: 'Outbound staging', type: 'Staging', pickable: false, available: false },
      { id: 'location-4', code: 'HOLD-01', name: 'Quality hold', type: 'Hold', pickable: false, available: false },
      { id: 'location-5', code: 'RECV-01', name: 'Receiving dock', type: 'Receiving', pickable: false, available: true }
    ],
    stock: [
      { id: 'stock-1', itemId: 'item-1', locationId: 'location-1', lot: 'LOT-101', qty: 100, committed: 0 },
      { id: 'stock-2', itemId: 'item-2', locationId: 'location-1', lot: 'LOT-202', qty: 160, committed: 0 },
      { id: 'stock-3', itemId: 'item-3', locationId: 'location-2', lot: 'LOT-303', qty: 800, committed: 0 },
      { id: 'stock-4', itemId: 'item-4', locationId: 'location-1', lot: 'LOT-404', qty: 18, committed: 0 },
      { id: 'stock-5', itemId: 'item-5', locationId: 'location-2', lot: 'LOT-505', qty: 240, committed: 0 },
      { id: 'stock-6', itemId: 'item-6', locationId: 'location-1', lot: 'LOT-606', qty: 65, committed: 0 },
      { id: 'stock-7', itemId: 'item-1', locationId: 'location-4', lot: 'LOT-Q01', qty: 8, committed: 0 }
    ],
    orders: [
      { id: 'order-1042', number: 'SO-1042', customer: 'Northline Supply', reference: 'Demo walkthrough', status: 'Draft', createdAt: now, lines: [{ itemId: 'item-1', qty: 10 }], pickId: null },
      { id: 'order-1043', number: 'SO-1043', customer: 'Juniper Workshop', reference: 'Weekly replenishment', status: 'Issued', createdAt: now, lines: [{ itemId: 'item-2', qty: 12 }, { itemId: 'item-5', qty: 24 }], pickId: 'pick-2043' }
    ],
    picks: [{ id: 'pick-2043', number: 'PK-2043', orderId: 'order-1043', status: 'Entered', allocations: [], shipmentId: null }],
    shipments: [],
    events: [{ id: 'event-1', time: now, type: 'Demo ready', message: 'Sample inventory and two customer orders are ready to work.', reference: 'Vancouver warehouse', changes: [] }]
  };
}

export function validateState(s,validationContext={}) {
  validateBusiness(s);
  requireThat(s && s.schemaVersion === 1, 'This is not a supported Chmltech WMS backup.');
  requireThat(Number.isSafeInteger(s.revision) && s.revision >= 0, 'Invalid data revision.');
  for (const key of ['items','locations','stock','orders','picks','shipments','events']) {
    requireThat(Array.isArray(s[key]) && s[key].length <= 10000, `Invalid ${key} data.`);
    requireThat(new Set(s[key].map(r => r.id)).size === s[key].length, `Duplicate ${key} records.`);
    s[key].forEach(r => requireThat(typeof r.id === 'string' && r.id.length < 100, `Invalid ${key} identifier.`));
  }
  requireThat(s.counters && ['stock','item','order','pick','shipment','event','location'].every(k => Number.isSafeInteger(s.counters[k]) && s.counters[k] >= 0), 'Invalid counters.');
  for (const [type, collection] of Object.entries({stock:'stock',item:'items',order:'orders',pick:'picks',shipment:'shipments',event:'events',location:'locations'})) {
    requireThat(s[collection].every(r => new RegExp(`^${type}-[0-9]+$`).test(r.id) && Number(r.id.split('-')[1]) <= s.counters[type]), 'Backup identifiers exceed counters.');
  }
  const textField=(value,label,max=240,optional=false)=>requireThat(typeof value==='string'&&charLength(value)<=max&&validUnicode(value)&&(optional||value.trim().length>0),`Invalid ${label}.`);
  const quantity=(value,label)=>{requireThat(typeof value==='number',`Invalid ${label}.`);whole(value,label,true);};
  const timestamp=value=>requireThat(typeof value==='string'&&Number.isFinite(Date.parse(value)), 'Invalid record date.');
  timestamp(s.updatedAt);
  for (const i of s.items) { textField(i.sku, 'SKU',40); textField(i.name, 'Item name',100); textField(i.category,'Category'); if(i.description!==undefined)textField(i.description,'Description',1000,true); if(i.supplier!==undefined)textField(i.supplier,'Supplier',100,true); requireThat(['ea','roll','pair','case'].includes(i.uom),'Invalid unit.'); quantity(i.reorderPoint, 'Reorder point'); }
  requireThat(new Set(s.items.map(i => i.sku.toLowerCase())).size === s.items.length, 'SKUs must be unique.');
  for (const l of s.locations) { textField(l.code,'Location code',20); textField(l.name,'Location name',100); requireThat(['Storage','Receiving','Hold','Staging'].includes(l.type),'Invalid location type.'); requireThat(l.pickable===(l.type==='Storage')&&l.available===['Storage','Receiving'].includes(l.type), 'Invalid location settings.'); }
  requireThat(new Set(s.locations.map(l=>l.code.toLowerCase())).size===s.locations.length,'Location codes must be unique.');
  requireThat(s.locations.some(l => l.type === 'Staging'), 'An outbound staging location is required.');
  requireThat(new Set(s.stock.map(r => `${r.itemId}|${r.locationId}|${r.lot}`)).size === s.stock.length, 'Duplicate stock buckets.');
  for (const row of s.stock) { itemById(s, row.itemId); locationById(s, row.locationId); quantity(row.qty, 'Stock'); quantity(row.committed, 'Committed'); requireThat(row.committed <= row.qty, 'Reserved quantity exceeds stock.'); requireThat(typeof row.lot === 'string' && charLength(row.lot) <= 100 && validUnicode(row.lot), 'Invalid lot.'); }
  for (const order of s.orders) {
    textField(order.customer, 'Customer',100);textField(order.number,'Order number',40);textField(order.reference,'Order reference',240,true);timestamp(order.createdAt); requireThat(['Draft','Issued','Picking','Picked','Fulfilled','Cancelled','Backordered','Part shipped'].includes(order.status), 'Invalid order status.');
    requireThat(Array.isArray(order.lines) && order.lines.length > 0 && order.lines.length <= 50, 'Orders need 1–50 lines.');
    requireThat(new Set(order.lines.map(l => l.itemId)).size === order.lines.length, 'Duplicate order items.');
    order.lines.forEach(l => { itemById(s, l.itemId); quantity(l.qty,'Order quantity');whole(l.qty); });
    if(order.status==='Draft')requireThat(!order.pickId,'A draft order cannot have a pick.');
    if (order.pickId) requireThat(pickById(s, order.pickId).orderId === order.id, 'Invalid order/pick link.');
    if (['Issued','Picking','Picked','Fulfilled','Backordered','Part shipped'].includes(order.status)) requireThat(!!order.pickId, 'An issued order needs a pick.');
  }
  const expected = Object.fromEntries(s.stock.map(r => [r.id,0]));
  for (const pick of s.picks) {
    const order = orderById(s, pick.orderId);
    textField(pick.number,'Pick number',40);requireThat((order.fulfillment || order.pickId === pick.id) && ['Entered','Committed','Finished'].includes(pick.status), 'Invalid pick.');
    requireThat(Array.isArray(pick.allocations), 'Invalid allocations.');
    if (pick.status === 'Entered') requireThat(pick.allocations.length === 0&&!pick.shipmentId, 'Entered picks cannot reserve stock or link a shipment.');
    if (pick.status === 'Committed') requireThat(!pick.shipmentId,'An unfinished pick cannot have a shipment.');
    if (pick.status !== 'Entered') {
      const sums = {};
      for (const a of pick.allocations) {
        const source = find(s.stock, a.sourceStockId, 'Source stock');quantity(a.qty,'Pick quantity'); whole(a.qty); requireThat(a.itemId === source.itemId && a.lot === source.lot&&locationById(s,source.locationId).pickable, 'Invalid pick source.');
        sums[a.itemId] = (sums[a.itemId] || 0) + a.qty;
        if (pick.status === 'Committed') expected[source.id] += a.qty;
        else {
          const dest = find(s.stock, a.stagingStockId, 'Staging stock');
          requireThat(dest.itemId === a.itemId && dest.lot === a.lot&&locationById(s,dest.locationId).type==='Staging', 'Invalid staging allocation.');
          const shipment = shipmentById(s, pick.shipmentId);
          requireThat(shipment.pickId === pick.id && shipment.status !== 'Cancelled', 'Invalid active shipment.');
          if (shipment.status !== 'Shipped') expected[dest.id] += a.qty;
        }
      }
      requireThat(pickLines(s,pick).every(l => sums[l.itemId] === l.qty) && Object.keys(sums).length === pickLines(s,pick).length, 'Pick quantities must match the order.');
    }
    const shipment = pick.shipmentId ? shipmentById(s,pick.shipmentId) : null;
    const status = pick.status === 'Entered' ? 'Issued' : pick.status === 'Committed' ? 'Picking' : shipment?.status === 'Shipped' ? 'Fulfilled' : 'Picked';
    requireThat(order.fulfillment || order.status === status || (order.status === 'Cancelled' && pick.status === 'Entered'), 'Order and pick states disagree.');
  }
  for (const ship of s.shipments) {textField(ship.number,'Shipment number',40);textField(ship.carrier,'Carrier',240,true);textField(ship.tracking,'Tracking',240,true);timestamp(ship.createdAt);if(ship.status==='Shipped')timestamp(ship.shippedAt); const p = pickById(s,ship.pickId); requireThat(ship.orderId === p.orderId && ['Entered','Packed','Shipped','Cancelled'].includes(ship.status), 'Invalid shipment.'); if(ship.status !== 'Cancelled') requireThat(p.shipmentId === ship.id && p.status === 'Finished', 'Shipment must link to a finished pick.'); }
  for(const event of s.events){timestamp(event.time);textField(event.type,'Event type',100);textField(event.message,'Event message',600);textField(event.reference,'Event reference',240,true);requireThat(Array.isArray(event.changes),'Invalid event deltas.');for(const c of event.changes){itemById(s,c.itemId);locationById(s,c.locationId);textField(c.lot,'Event lot',100,true);requireThat(Number.isSafeInteger(c.onHand)&&Number.isSafeInteger(c.committed),'Invalid event quantities.');}}
  for (const row of s.stock) requireThat(expected[row.id] === row.committed, 'Stock commitments do not match active picks.');
  validateFulfillment(s);
  validateTransferCosting(s);
  validateOperations(s);
  validateInsights(s);
  validateBilling(s);
  validateCosting(s);
  validateFIFO(s,validationContext);
  validateDashboard(s);
  validateProcurement(s);
  validateExecution(s);
  validateUnits(s);
  validateMobileStock(s);
  validateSalesDesk(s);
  validateQuotations(s);
  validateCRM(s);validateProduction(s);validateReceiving(s,validationContext);
  return true;
}

export function dispatch(current, command, payload = {}, options = {}) {
  if (options.expectedRevision !== undefined) requireThat(current.revision === options.expectedRevision, 'The warehouse changed in another tab. Refresh and try again.');
  validateState(current);
  const s = structuredClone(current), time = options.now || new Date().toISOString();
  let type, message, reference = '', resultId = null;
  const order = () => orderById(s, payload.id);
  const pick = () => pickById(s, payload.id);
  const shipment = () => shipmentById(s,payload.id);
  payload=structuredClone(payload);
  const context={time,uid,stockAt,dispatch:(state,cmd,p,opts={})=>dispatch(state,cmd,p,{...opts,nested:true,actor:options.actor,role:options.role,actorId:options.actorId,rootCommand:options.rootCommand||command,rootPayload:options.rootPayload||payload}),rootCommand:options.rootCommand||command,rootPayload:options.rootPayload||payload,internal:!!options.internal,nested:!!options.nested,actor:options.actor,role:options.role,actorId:options.actorId};
  if(['voidShipment','voidPick'].includes(command)){const pk=command==='voidPick'?pick():pickById(s,shipment().pickId),o=orderById(s,pk.orderId);requireThat(!o.fulfillment||o.pickId===pk.id,'Reverse deliveries in reverse release order.');}
  beforeReceiving(s,command,payload,context);
  beforeUnits(s,command,payload,context);
  beforeTransferCosting(s,command,payload,context);
  beforeExecution(s,command,payload,context);
  beforeProcurement(s,command,payload,context);
  beforeBusiness(s,command,payload,context);
  beforeBilling(s,command,payload);
  beforeCosting(s,command,payload,context);
  beforeOperation(s,command,payload,context);
  beforeFIFO(s,command,payload,context);beforeProduction(s,command,payload);
  switch (command) {
    case 'createOrder': {
      requireThat(Array.isArray(payload.lines) && payload.lines.length > 0, 'Add at least one item.');
      const lineMap = new Map();
      for (const l of payload.lines) { itemById(s,l.itemId); lineMap.set(l.itemId,(lineMap.get(l.itemId)||0)+whole(l.qty)); }
      const id=uid(s,'order');const o={id,number:`SO-${s.counters.order}`,customer:clean(payload.customer,'Customer'),reference:note(payload.reference),status:'Draft',createdAt:time,pickId:null,lines:[...lineMap].map(([itemId,qty])=>({itemId,qty}))};
      s.orders.push(o);resultId=id;reference=o.number;type='Order created';message=`Draft order for ${o.customer}.`;break;
    }
    case 'releaseShipment': {const o=order(),pk=releaseDelivery(s,o,payload,context);resultId=pk.id;reference=o.number;type='Delivery released';message='Delivery quantities released; the original order and remaining backorder are retained.';break;}
    case 'issueOrder': {
      const o=order();requireThat(o.status==='Draft','Only a draft order can be issued.');const id=uid(s,'pick');
      s.picks.push({id,number:`PK-${s.counters.pick}`,orderId:o.id,status:'Entered',allocations:[],shipmentId:null});o.pickId=id;o.status='Issued';resultId=id;reference=o.number;type='Order issued';message='Demand allocated. Pick is ready to reserve stock.';break;
    }
    case 'cancelOrder': {
      const o=order();requireThat(!o.fulfillment||!s.shipments.some(sh=>sh.orderId===o.id&&sh.status==='Shipped'),'A delivered order cannot be cancelled.');requireThat(['Draft','Issued'].includes(o.status),'Reverse the pick and shipment before cancelling this order.');o.status='Cancelled';reference=o.number;type='Order cancelled';message='Outstanding demand released.';break;
    }
    case 'commitPick': {
      const p=pick(),o=orderById(s,p.orderId);requireThat(p.status==='Entered'&&['Issued','Part shipped'].includes(o.status),'This pick is not ready to reserve.');
      const shortage=shortages(s,{...o,lines:pickLines(s,p)},time);requireThat(!shortage.length,shortage.map(r=>`${r.item.sku}: short ${r.short} ${r.item.uom}`).join('; '));
      p.allocations=[];
      for(const line of pickLines(s,p)){let remaining=line.qty;for(const r of stockCandidates(s,line.itemId,time).filter(r=>stockInScope(s,r,orderScope(s,o)))){
        const qty=Math.min(remaining,r.qty-r.committed);if(qty>0){r.committed+=qty;remaining-=qty;p.allocations.push({sourceStockId:r.id,itemId:r.itemId,lot:r.lot,qty,stagingStockId:null});}if(!remaining)break;
      }requireThat(remaining===0,'Insufficient pickable stock.');}
      p.status='Committed';o.status='Picking';reference=p.number;type='Pick reserved';message='Stock reserved at the source. On-hand quantity is unchanged.';break;
    }
    case 'finishPick': {
      const p=pick(),o=orderById(s,p.orderId);requireThat(p.status==='Committed','Reserve stock before finishing the pick.');
      const destination=payload.locationId ? locationById(s,payload.locationId) : s.locations.find(l=>l.type==='Staging');requireThat(destination.type==='Staging','Finish picks into an outbound staging location.');
      for(const a of p.allocations){const src=find(s.stock,a.sourceStockId,'Source stock'),dst=stockAt(s,a.itemId,destination.id,a.lot);requireThat(src.committed>=a.qty&&src.qty>=a.qty,'Reserved source quantity has changed.');src.qty-=a.qty;src.committed-=a.qty;dst.qty+=a.qty;dst.committed+=a.qty;a.stagingStockId=dst.id;}
      const id=uid(s,'shipment');s.shipments.push({id,number:`SH-${s.counters.shipment}`,pickId:p.id,orderId:o.id,status:'Entered',createdAt:time,shippedAt:null,carrier:'',tracking:'',...(o.fulfillment?{lines:structuredClone(pickLines(s,p))}:{})});p.shipmentId=id;p.status='Finished';o.status='Picked';resultId=id;reference=p.number;type='Pick finished';message=`Moved to ${destination.code}. Stock remains reserved; shipment created.`;break;
    }
    case 'packShipment': {
      const sh=shipment();requireThat(sh.status==='Entered','Only an entered shipment can be packed.');sh.status='Packed';sh.carrier=note(payload.carrier);sh.tracking=note(payload.tracking);reference=sh.number;type='Shipment packed';message='Packing complete. Inventory quantities are unchanged.';break;
    }
    case 'shipShipment': {
      const sh=shipment();requireThat(['Entered','Packed'].includes(sh.status),'This shipment has already shipped or been cancelled.');const p=pickById(s,sh.pickId);
      for(const a of p.allocations){const r=find(s.stock,a.stagingStockId,'Staged stock');requireThat(r.committed>=a.qty&&r.qty>=a.qty,'Staged stock is not available.');r.committed-=a.qty;r.qty-=a.qty;}
      sh.status='Shipped';sh.shippedAt=time;const o=orderById(s,sh.orderId);o.status=o.fulfillment?fulfillmentStatus(s,o):'Fulfilled';reference=sh.number;type='Shipment shipped';message=o.status==='Fulfilled'?'On-hand and reserved quantities reduced. Order fulfilled.':'Delivery shipped; remaining quantities stay on the original order.';break;
    }
    case 'voidShipment': {
      const sh=shipment();requireThat(['Packed','Shipped'].includes(sh.status),'Only a packed or shipped shipment can be reversed.');const wasShipped=sh.status==='Shipped';
      if(wasShipped){for(const a of pickById(s,sh.pickId).allocations){const r=find(s.stock,a.stagingStockId,'Staged stock');r.qty+=a.qty;r.committed+=a.qty;}orderById(s,sh.orderId).status='Picked';}
      sh.status='Entered';sh.shippedAt=null;if(orderById(s,sh.orderId).fulfillment)orderById(s,sh.orderId).status=fulfillmentStatus(s,orderById(s,sh.orderId));reference=sh.number;type=wasShipped?'Shipment reversed':'Packing reversed';message=(wasShipped?'Stock restored to staging and reserved again for the pick.':'Shipment returned to Entered. Stock unchanged.')+(payload.reason?` ${note(payload.reason)}`:'');break;
    }
    case 'voidPick': {
      const p=pick(),o=orderById(s,p.orderId);requireThat(['Committed','Finished'].includes(p.status),'Only a reserved or finished pick can be reversed.');
      if(p.status==='Finished'){const sh=shipmentById(s,p.shipmentId);requireThat(sh.status==='Entered','Reverse the shipment or packing first.');for(const a of p.allocations){const dst=find(s.stock,a.stagingStockId,'Staged stock'),src=find(s.stock,a.sourceStockId,'Source stock');dst.qty-=a.qty;dst.committed-=a.qty;src.qty+=a.qty;}sh.status='Cancelled';}
      else for(const a of p.allocations)find(s.stock,a.sourceStockId,'Source stock').committed-=a.qty;
      p.status='Entered';p.allocations=[];p.shipmentId=null;o.status=o.fulfillment?fulfillmentStatus(s,o):'Issued';reference=p.number;type='Pick reversed';message='Reservation released and any staged units returned to their source. Order demand remains allocated.'+(payload.reason?` ${note(payload.reason)}`:'');break;
    }
    case 'receiveStock': {
      const item=itemById(s,payload.itemId),loc=locationById(s,payload.locationId),qty=whole(payload.qty);requireThat(loc.type!=='Staging','Receive into storage, receiving, or quality hold.');
      const lot=cutText(note(payload.lot),100)||'UNTRACKED';stockAt(s,item.id,loc.id,lot).qty+=qty;reference=item.sku;type='Stock received';message=`${qty} ${item.uom} received into ${loc.code}. ${note(payload.note)}`.trim();break;
    }
    case 'moveStock': {
      const r=find(s.stock,payload.stockId,'Stock'),qty=whole(payload.qty),loc=locationById(s,payload.locationId);requireThat(loc.id!==r.locationId,'Choose a different destination.');requireThat(loc.type!=='Staging','Use the picking workflow to move stock into staging.');requireThat(qty<=r.qty-r.committed,'Only unreserved stock can be moved.');
      const src=locationById(s,r.locationId);r.qty-=qty;stockAt(s,r.itemId,loc.id,r.lot).qty+=qty;reference=itemById(s,r.itemId).sku;type='Stock moved';message=`${qty} moved from ${src.code} to ${loc.code}.`;break;
    }
    case 'countStock': {
      const r=find(s.stock,payload.stockId,'Stock'),qty=whole(payload.qty,'Counted quantity',true);requireThat(qty>=r.committed,`Cannot count below ${r.committed} reserved units. Reverse the pick first.`);const reason=clean(payload.reason,'Count reason',240);r.qty=qty;reference=itemById(s,r.itemId).sku;type='Stock counted';message=`${locationById(s,r.locationId).code} counted as ${qty}. ${reason}`;break;
    }
    case 'createItem': {
      const sku=clean(payload.sku,'SKU',40).toUpperCase();requireThat(!s.items.some(i=>i.sku.toLowerCase()===sku.toLowerCase()),'This SKU already exists.');const id=uid(s,'item');s.items.push({id,sku,name:clean(payload.name,'Item name'),category:note(payload.category)||'General',description:optionalText(payload.description,'Description',1000),supplier:optionalText(payload.supplier,'Supplier',100),uom:['ea','roll','pair','case'].includes(payload.uom)?payload.uom:'ea',reorderPoint:whole(payload.reorderPoint??0,'Reorder point',true),color:'#d9e8dc',icon:'box'});resultId=id;reference=sku;type='Item created';message='Item added to the catalog. Receive stock to make it available.';break;
    }
    case 'saveItemText': {
      const i=itemById(s,payload.id);i.name=clean(payload.name,'Item name');i.description=optionalText(payload.description,'Description',1000);i.supplier=optionalText(payload.supplier,'Supplier',100);i.category=note(payload.category)||'General';
      if(payload.reorderPoint!==undefined)i.reorderPoint=whole(payload.reorderPoint,'Reorder point',true);
      resultId=i.id;reference=i.sku;type='Item details saved';message='Product description and supplier updated.';break;
    }
    case 'importCatalog': {
      requireThat(Array.isArray(payload.rows)&&payload.rows.length>0&&payload.rows.length<=500,'Import between 1 and 500 rows.');
      const seen=new Set();
      for(const row of payload.rows){
        const sku=clean(row.sku,'SKU',40).toUpperCase();requireThat(!seen.has(sku),'Duplicate SKU in import.');seen.add(sku);
        requireThat(['ea','roll','pair','case'].includes(row.uom)&&['Lot','Serial'].includes(row.tracking),'Invalid unit or tracking.');
        const existing=s.items.find(i=>i.sku.toUpperCase()===sku);
        if(existing)requireThat(existing.uom===row.uom&&(s.operations?.tracking[existing.id]||'Lot')===row.tracking,'CSV cannot change an existing stock unit or tracking mode. Use Tracking on the item.');
        Object.assign(s,dispatch(s,existing?'saveItemText':'createItem',{...row,id:existing?.id},{now:time}).state);
      }
      type='Catalog imported';message=`${payload.rows.length} catalog rows imported. Stock quantities were preserved.`;break;
    }
    case 'createLocation': {
      const code=clean(payload.code,'Location code',20).toUpperCase();requireThat(!s.locations.some(l=>l.code.toLowerCase()===code.toLowerCase()),'This location code already exists.');const id=uid(s,'location');const typeName=['Storage','Receiving','Hold'].includes(payload.type)?payload.type:'Storage';s.locations.push({id,code,name:clean(payload.name,'Location name'),type:typeName,pickable:typeName==='Storage',available:typeName!=='Hold'});resultId=id;reference=code;type='Location created';message=`${typeName} location added.`;break;
    }
    default: {const result=receivingCommand(s,command,payload,context)||productionCommand(s,command,payload,context)||crmCommand(s,command,payload,context)||quotationCommand(s,command,payload,context)||pricingCommand(s,command,payload,context)||unitsCommand(s,command,payload,context)||mobileStockCommand(s,command,payload,context)||executionCommand(s,command,payload,context)||transferCostCommand(s,command,payload,context)||procurementCommand(s,command,payload,context)||dashboardCommand(s,command,payload,context)||costCommand(s,command,payload,context)||billingCommand(s,command,payload,context)||countCommand(s,command,payload,context)||businessCommand(s,command,payload,context)||extendedCommand(s,command,payload,context);requireThat(result,'Unknown warehouse action.');({type,message,reference,resultId}=result);}
  }
  if(command==='createItem'&&payload.tracking){requireThat(['Lot','Serial'].includes(payload.tracking),'Invalid tracking mode.');setupOps(s).tracking[resultId]=payload.tracking;}
  afterProcurement(s,current,command,payload,context);
  afterOperation(s,current,command,payload,context);
  afterFIFOStock(s,current,command,payload,context);
  afterBusiness(s,current,command,payload,context);
  afterCosting(s,current,command,payload,context);
  afterTransferCosting(s,current,command,payload,context);
  afterFIFOAccounting(s,current,command,payload,context);
  afterInsights(s,current,command,payload,context,{type,reference});
  afterExecution(s,command,payload,current);
  afterUnits(s,current,command,payload,context);
  const changes=command.startsWith('business:')||command.startsWith('count:')||['commitBatch','finishBatch','receivePurchase','loadChineseDemo'].includes(command)?[]:s.stock.map(r=>{const prev=current.stock.find(x=>x.id===r.id);return{itemId:r.itemId,locationId:r.locationId,lot:r.lot,onHand:r.qty-(prev?.qty||0),committed:r.committed-(prev?.committed||0)};}).filter(r=>r.onHand||r.committed);
  requireThat(s.events.length<10000,'Activity history capacity reached. Export and review before continuing.');s.events.unshift({id:uid(s,'event'),time,type,message,reference,changes});s.revision++;s.updatedAt=time;
  validateState(s,context);return {state:s,resultId};
}
