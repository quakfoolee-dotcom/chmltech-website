import {documentScanHTML} from './scan-codes.mjs';
import {translate,translatedWords} from './locale.mjs';
import {invoiceHTML} from './invoice-layout.mjs';
import {purchaseFormLayout} from './commercial-layout.mjs';
import {forecastDocuments} from './forecast.mjs';
import {procurement,purchaseStatus} from './procurement.mjs';
import {ops,shippingMeta,shipmentLines} from './operations.mjs';
import {purchaseLines,purchaseTotals} from './purchasing.mjs';
export const languages=[['en','English'],['zh-Hans','简体中文 · Simplified Chinese'],['zh-Hant','繁體中文 · Traditional Chinese'],['fr','Français · French']];
const words={
 en:{purchase:'Purchase order',packing:'Packing slip',label:'Warehouse label',supplier:'Supplier',recipient:'Ship to',description:'Description',qty:'Quantity',cost:'Unit cost',total:'Order total',due:'Due date',status:'Status',delivery:'Delivery',reference:'Reference',carrier:'Carrier / service',carton:'Carton',dimensions:'Dimensions',weight:'Weight',received:'Received',note:'Local warehouse document. Currency is shown where specified. Not a tax invoice.',postage:'Local warehouse label. NOT POSTAGE.',page:'Page',continued:'continued',Warehouse:'To warehouse','Drop ship':'Direct to customer',Open:'Open',Closed:'Closed',Cancelled:'Cancelled',Entered:'Entered',Packed:'Packed',Shipped:'Shipped'},
 'zh-Hans':{purchase:'采购订单',packing:'装箱单',label:'仓库标签',supplier:'供应商',recipient:'收货人',description:'产品说明',qty:'数量',cost:'单价',total:'订单金额',due:'交货日期',status:'状态',delivery:'交货方式',reference:'参考编号',carrier:'承运商 / 服务',carton:'箱号',dimensions:'尺寸',weight:'重量',received:'已收数量',note:'本地仓库单据。金额币种以单据标注为准。本单据不是税务发票。',postage:'本地仓库标签，不含运费或邮资。',page:'页',continued:'续页',Warehouse:'送至仓库','Drop ship':'直送客户',Open:'未完成',Closed:'已完成',Cancelled:'已取消',Entered:'已录入',Packed:'已包装',Shipped:'已发货'},
 'zh-Hant':{purchase:'採購訂單',packing:'裝箱單',label:'倉庫標籤',supplier:'供應商',recipient:'收貨人',description:'產品說明',qty:'數量',cost:'單價',total:'訂單金額',due:'交貨日期',status:'狀態',delivery:'交貨方式',reference:'參考編號',carrier:'承運商 / 服務',carton:'箱號',dimensions:'尺寸',weight:'重量',received:'已收數量',note:'本地倉庫單據。金額幣種以單據標註為準。本單據不是稅務發票。',postage:'本地倉庫標籤，不含運費或郵資。',page:'頁',continued:'續頁',Warehouse:'送至倉庫','Drop ship':'直送客戶',Open:'未完成',Closed:'已完成',Cancelled:'已取消',Entered:'已錄入',Packed:'已包裝',Shipped:'已發貨'}
};
Object.assign(words.en,{outstanding:'Outstanding',supplierCode:'Supplier product code',supplierAddress:'Supplier address',contact:'Contact',terms:'Payment terms',purchaseNote:'Purchase note'});
Object.assign(words['zh-Hans'],{outstanding:'待收数量',supplierCode:'供应商货号',supplierAddress:'供应商地址',contact:'联系人',terms:'付款条件',purchaseNote:'采购备注'});
Object.assign(words['zh-Hant'],{outstanding:'待收數量',supplierCode:'供應商貨號',supplierAddress:'供應商地址',contact:'聯絡人',terms:'付款條件',purchaseNote:'採購備註'});
for(const [language,translations]of Object.entries({en:{Draft:'Draft - not issued','Pending approval':'Pending approval - not issued',Approved:'Approved - not issued',Rejected:'Rejected - not issued',Issued:'Issued locally',revision:'Purchase revision',approval:'Approval',confirmed:'Supplier-confirmed arrival',confirmation:'Supplier confirmation',custom:'Custom fields',history:'Review history'},'zh-Hans':{Draft:'草稿 - 尚未下单','Pending approval':'待审批 - 尚未下单',Approved:'已批准 - 尚未下单',Rejected:'已退回 - 尚未下单',Issued:'已在本地下单',revision:'采购修订版本',approval:'审批记录',confirmed:'供应商确认到货日',confirmation:'供应商确认编号',custom:'自定义字段',history:'审核历史'},'zh-Hant':{Draft:'草稿 - 尚未下單','Pending approval':'待審批 - 尚未下單',Approved:'已批准 - 尚未下單',Rejected:'已退回 - 尚未下單',Issued:'已在本地下單',revision:'採購修訂版本',approval:'審批記錄',confirmed:'供應商確認到貨日',confirmation:'供應商確認編號',custom:'自訂欄位',history:'審核歷史'}}))Object.assign(words[language],translations);
words.fr=translatedWords(words.en,'fr');
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function buildDocuments(s,kind,id,locale='en'){
 if(!words[locale])throw Error('Choose a supported document language.');
 if(kind==='forecast')return forecastDocuments(s,JSON.parse(id),locale);
 const w=words[locale],field=(label,text)=>({kind:'field',label:w[label]||translate(label,locale),text:String(text??'—')}),item=id=>{const i=s.items.find(i=>i.id===id);if(!i)throw Error('Item not found.');return i;};
 const product=(i,qty,unitCost)=>[{kind:'item',text:`${i.sku}  /  ${i.name}`},...(i.description?[field('description',i.description)]:[]),field('qty',`${qty} ${i.uom}`),...(unitCost!==undefined?[field('cost',Number(unitCost).toFixed(4))]:[])];
 const doc=(title,ref,blocks,size='A4')=>{
  const result={...(title==='packing'?{scanCode:ref}:{}),locale,title:w[title],ref,blocks,size,footer:size==='label'?w.postage:w.note,pageWord:w.page,continued:w.continued};
  if(title==='purchase'){const p=ops(s).purchases.find(p=>p.id===id),status=purchaseStatus(s,p);result.form=purchaseFormLayout(s,p,locale,blocks,w[status]||status,w[p.kind]||p.kind);}
  return result;
 };
 if(kind==='purchase'){
  const p=ops(s).purchases.find(p=>p.id===id);if(!p)throw Error('Purchase not found.');
  const v=p.snapshot||{},lines=purchaseLines(p);
  const foreign=l=>p.tradeLines?.find(t=>t.itemId===l.itemId);
  const purchaseProduct=l=>{const t=foreign(l),i=l.sku?l:item(l.itemId);return t?product({...i,uom:t.packName},t.foreignQty,t.foreignCost):product(i,l.qty,l.unitCost);};
  const currencyFields=p.currency?[field('Currency / 币种 / 幣別',p.currency),field('Exchange rate / 汇率 / 匯率',`1 ${p.currency} = ${p.exchangeRate} ${s.business?.homeCurrency||'CAD'}`)]:[];
  return [doc('purchase',p.number,[...currencyFields,field('supplier',[p.supplier,v.englishName].filter(Boolean).join('\n')),...(v.address?[field('supplierAddress',v.address)]:[]),...([v.contact,v.email,v.phone].some(Boolean)?[field('contact',[v.contact,v.email,v.phone].filter(Boolean).join(' / '))]:[]),...(v.paymentTerms?[field('terms',v.paymentTerms)]:[]),field('status',w[purchaseStatus(s,p)]||purchaseStatus(s,p)),field('delivery',w[p.kind]),...(p.customer?[field('recipient',p.customer)]:[]),field('due',p.due||'—'),...(procurement(s).orders[p.id]?(()=>{const m=procurement(s).orders[p.id];return [field('revision',m.revision),field('approval',m.approval?m.approval.actor+' / '+m.approval.time:'—'),field('confirmed',m.confirmedDate||'—'),field('confirmation',m.confirmedReference||'—'),...m.fields.map(f=>({kind:'field',label:f.name,text:String(f.value)})),...m.history.map(h=>field('history',h.time+' / '+h.actor+' / '+h.action+' / '+h.reason))];})():[]),...(p.reference?[field('reference',p.reference)]:[]),...lines.flatMap(l=>[...purchaseProduct(l),...(foreign(l)?[field('Stock units / 库存单位 / 庫存單位',`${l.qty} ${l.uom} (${foreign(l).packSize} per ${foreign(l).packName})`)]:[]),...(l.vendorSku?[field('supplierCode',l.vendorSku)]:[]),field('received',l.received),field('outstanding',!['Cancelled','Closed'].includes(p.status)?l.qty-l.received:0)].map(b=>({...b,group:l.id}))),field('total',p.currency?`${p.currency} ${p.tradeLines.reduce((n,l)=>n+l.foreignQty*l.foreignCost,0).toFixed(2)}`:purchaseTotals(p).amount.toFixed(2)),...(p.currency?[field('Home value / 本币金额 / 本幣金額',`${s.business?.homeCurrency||'CAD'} ${purchaseTotals(p).amount.toFixed(2)}`)]:[]),...(p.note?[field('purchaseNote',p.note)]:[])])];
 }
 const sh=s.shipments.find(x=>x.id===id);if(!sh)throw Error('Shipment not found.');if(sh.status==='Cancelled')throw Error('Cancelled shipments cannot print active documents.');
 const o=s.orders.find(o=>o.id===sh.orderId),m=shippingMeta(s,id),a=m.address;
 const address=[a.name||o.customer,a.line1,a.line2,[a.city,a.region,a.postal].filter(Boolean).join(' '),a.country].filter(Boolean).join('\n');
 const common=[field('reference',o.number+(o.reference?' / '+o.reference:'')),field('status',w[sh.status]),field('recipient',address),field('carrier',[sh.carrier,m.service].filter(Boolean).join(' / ')||'—')];
 if(kind==='packing')return [doc('packing',sh.number,[...common,...shipmentLines(s,id).flatMap(l=>product(item(l.itemId),l.qty)),field('carton',m.cartons.length),field('reference',sh.tracking||'—')])];
 if(kind==='label'){
  if(!m.cartons.length)throw Error('Add cartons or pack the shipment before printing labels.');
  return m.cartons.map((c,j)=>doc('label',`${sh.number} / ${j+1}-${m.cartons.length}`,[field('carton',`${c.name} / ${c.id}`),...common,field('reference',c.tracking||sh.tracking||'—'),...c.lines.flatMap(l=>product(item(l.itemId),l.qty)),field('weight',`${c.weight} ${c.weightUnit}`),field('dimensions',`${c.length} × ${c.width} × ${c.height} ${c.unit}`)],'label'));
 }
 throw Error('Unknown document type.');
}
export const documentHTML=docs=>docs.map(d=>d.invoice||d.form?invoiceHTML(d):`<article class="business-document ${d.size==='label'?'document-label':''}" lang="${d.locale}"><header><strong>HARBOR</strong><span>${e(d.title)}</span></header><h2>${e(d.ref)}</h2>${d.scanCode?documentScanHTML(d.scanCode,d.locale):''}${d.blocks.map(b=>b.kind==='item'?`<h3>${e(b.text)}</h3>`:`<div class="document-field"><b>${e(b.label)}</b><div>${e(b.text)}</div></div>`).join('')}<footer>${e(d.footer)}</footer></article>`).join('');

