import {invoiceLayout} from './invoice-layout.mjs?demo=45f52980507d3a1b';
import {purchaseLines,purchaseTotals} from './purchasing.mjs?demo=45f52980507d3a1b';
const captions={
 en:{purchase:'Purchase order',bill:'Supplier bill',credit:'Credit note',supplierCredit:'Supplier credit',number:'Document #',source:'Source document',original:'Original document',reference:'Reference',supplier:'Supplier',to:'To supplier',issuer:'Our business',delivery:'Delivery',due:'Due date',currency:'Currency',receipt:'Receipt',kind:'Document type',purchaseType:'Purchase',billType:'Bill',creditType:'Credit',quantity:'Quantity',received:'Received (stock units)',orderTotal:'Order total',creditTotal:'Credit total',extra:'Additional details',tax:'Line tax',customer:'Customer',ship:'Ship to',terms:'Payment terms',date:'Date'},
 'zh-Hans':{purchase:'采购订单',bill:'供应商账单',credit:'贷项通知单',supplierCredit:'供应商贷项',number:'单据号',source:'来源单据',original:'原始单据',reference:'参考编号',supplier:'供应商',to:'供应商地址',issuer:'本公司',delivery:'交货方式',due:'到期日',currency:'币种',receipt:'收货单',kind:'单据类型',purchaseType:'采购',billType:'账单',creditType:'贷项',quantity:'数量',received:'已收（库存单位）',orderTotal:'订单总额',creditTotal:'贷项总额',extra:'其他明细',tax:'行税额',customer:'客户',ship:'收货地址',terms:'付款条件',date:'日期'},
 'zh-Hant':{purchase:'採購訂單',bill:'供應商帳單',credit:'貸項通知單',supplierCredit:'供應商貸項',number:'單據號',source:'來源單據',original:'原始單據',reference:'參考編號',supplier:'供應商',to:'供應商地址',issuer:'本公司',delivery:'交貨方式',due:'到期日',currency:'幣別',receipt:'收貨單',kind:'單據類型',purchaseType:'採購',billType:'帳單',creditType:'貸項',quantity:'數量',received:'已收（庫存單位）',orderTotal:'訂單總額',creditTotal:'貸項總額',extra:'其他明細',tax:'行稅額',customer:'客戶',ship:'收貨地址',terms:'付款條件',date:'日期'},
 fr:{purchase:'Bon de commande',bill:'Facture fournisseur',credit:'Avoir client',supplierCredit:'Avoir fournisseur',number:'N° de document',source:'Document source',original:'Document original',reference:'Référence',supplier:'Fournisseur',to:'Adresse fournisseur',issuer:'Notre entreprise',delivery:'Livraison',due:'Échéance',currency:'Devise',receipt:'Réception',kind:'Type de document',purchaseType:'Achat',billType:'Facture',creditType:'Avoir',quantity:'Quantité',received:'Reçu (unités de stock)',orderTotal:'Total commande',creditTotal:'Total avoir',extra:'Détails complémentaires',tax:'Taxe de ligne',customer:'Client',ship:'Livrer à',terms:'Conditions de paiement',date:'Date'}
};
const money=(v,c)=>`${c} ${Number(v).toLocaleString('en-CA',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
const trackingWords={en:{stock:'Stock units',outstanding:'Outstanding',reversed:'Reversed'},'zh-Hans':{stock:'库存单位',outstanding:'待收数量',reversed:'已冲销'},'zh-Hant':{stock:'庫存單位',outstanding:'待收數量',reversed:'已沖銷'},fr:{stock:'Unités de stock',outstanding:'Quantité restante',reversed:'Annulé'}};
export function billingFormLayout(s,d,balance,locale,status,blocks){
 const w=captions[locale],v=invoiceLayout(s,d,balance,locale,status),parent=s.billing.documents.find(p=>p.id===d.parentId),credit=d.kind==='Credit',supplier=d.kind==='Bill'||parent?.kind==='Bill';
 v.labels=[...v.labels];v.labels[0]=credit?(supplier?w.supplierCredit:w.credit):w.bill;
 v.meta=[[w.number,d.number],[credit?w.original:w.source,credit?parent?.number||d.sourceRef:d.sourceRef],[w.reference,d.reference||'—'],[w.date,d.date]];
 const issuer=v.company.join('\n');v.addresses=[[supplier?w.to:v.labels[5],[d.party.name,d.party.address].filter(Boolean).join('\n')],[w.issuer,issuer]];
 v.contacts=[[v.labels[8],d.party.contact||'—'],[v.labels[8],d.issuer.contact||'—']];
 v.details=[[w.kind,v.labels[0]],[w.currency,d.currency],[w.due,d.due||'—'],[credit?w.original:w.receipt,credit?parent?.number||'—':d.receiptId||'—'],[v.labels[8],d.party.contact||'—'],[w.reference,d.reference||'—']];
 v.heads=[...v.heads];v.heads[5]=w.quantity;v.rows=v.rows.map((row,i)=>{const l=d.lines[i];return row.map((value,k)=>k===1?(credit?w.creditType:w.billType):k===3?value+`\n${w.tax}: ${l.taxName||'—'} ${(l.taxBP/100).toFixed(2)}% / ${money(l.tax/100,d.currency)}`+(d.receiptId?.includes('+')?`\n${w.receipt}: ${l.sourceLineId}`:''):value);});
 v.payments=s.billing.payments.filter(p=>p.documentId===d.id).map(p=>[p.date,`${p.kind==='Refund'?v.labels[33]+' / ':''}${p.method}${p.status==='Reversed'?' / '+trackingWords[locale].reversed:''}`,money(p.amount/100,d.currency),`${p.number} / ${p.reference}`]);
 if(credit){v.totals=v.totals.slice(0,v.totals.findIndex(r=>r[0]===v.labels[29])+1);v.totals.at(-1)[0]=w.creditTotal;v.hidePayments=true;}
 v.instructions='';v.extraTitle=w.extra;
 // Retain settlement, return and reversal details from the original document model.
 const core=new Set(blocks.slice(0,blocks.findIndex(b=>b.kind==='item')).map(b=>b.label));
 v.extra=blocks.filter(b=>b.kind==='field'&&!b.group&&!core.has(b.label)&&b.text!==d.note&&!s.billing.payments.some(p=>p.documentId===d.id&&(b.text.includes(p.number+' / ')||b.text===`${p.method} / ${p.reference}`))).map(b=>[b.label,b.text]);
 if(d.voidReason&&!v.extra.some(r=>r[1]===d.voidReason))v.extra.push([status,d.voidReason]);
 return v;
}
export function purchaseFormLayout(s,p,locale,blocks,status,delivery){
 const w=captions[locale],profile=s.billing?.profile||{},currency=p.currency||s.business?.homeCurrency||'CAD',snapshot=p.snapshot||{},ordered=purchaseLines(p);
 const company=[profile.name||'Chmltech WMS warehouse',profile.address,profile.contact,profile.taxId].filter(Boolean),m=v=>money(Number(Number(v).toFixed(2)),currency);
 const base=invoiceLayout({...s,billing:{...s.billing,payments:[]}},{number:p.number,sourceRef:p.number,sourceId:'',currency,issuer:profile,party:{name:p.supplier},lines:[],status:'Draft',net:0,total:0,tax:0}, {},locale,status);
 const warehouse=s.business?.warehouses.find(x=>x.id===p.scope?.warehouseId),receiver=p.kind==='Drop ship'?p.customer:warehouse?.name||profile.name||'—';
 const productRows=ordered.map((line,i)=>{const product=line.sku?line:s.items.find(item=>item.id===line.itemId),foreign=p.tradeLines?.find(t=>t.itemId===line.itemId),qty=foreign?.foreignQty??line.qty,unit=foreign?.packName??product.uom,price=foreign?.foreignCost??line.unitCost;
  const tw=trackingWords[locale];
  return [String(i+1),w.purchaseType,product.sku,[product.name,product.description, line.vendorSku?`${snapshot.name||p.supplier}: ${line.vendorSku}`:'',...(foreign?[`${tw.stock}: ${line.qty} ${product.uom} (${foreign.packSize} / ${foreign.packName})`]:[]),`${tw.outstanding}: ${!['Cancelled','Closed'].includes(p.status)?line.qty-line.received:0} ${product.uom}`].filter(Boolean).join('\n'),`${currency} ${Number(price).toFixed(4)}`,`${qty} ${unit}`,`${line.received} ${product.uom}`,m(qty*price)];
 });
 const total=p.currency?p.tradeLines.reduce((n,l)=>n+l.foreignQty*l.foreignCost,0):purchaseTotals(p).amount;
 const grouped=new Set(blocks.filter(b=>b.group).map(b=>b.label));
 const customLabels=new Set((s.procurement?.orders[p.id]?.fields||[]).map(f=>f.name));
 const extra=blocks.filter(b=>b.kind==='field'&&!b.group&&(customLabels.has(b.label)||(!['—',p.note,p.supplier,[p.supplier,snapshot.englishName].filter(Boolean).join('\n'),p.reference,p.due,status,delivery,snapshot.address,snapshot.paymentTerms,[snapshot.contact,snapshot.email,snapshot.phone].filter(Boolean).join(' / ')].includes(b.text)&&!grouped.has(b.label)&&b.text!==m(total)))).map(b=>[b.label,b.text]);
 return {...base,labels:[w.purchase,...base.labels.slice(1)],company,number:p.number,status,meta:[[w.number,p.number],[w.reference,p.reference||'—'],[w.date,(p.createdAt||'').slice(0,10)||'—'],[w.currency,currency]],addresses:[[w.to,[p.supplier,snapshot.englishName,snapshot.address].filter(Boolean).join('\n')],[w.ship,receiver]],contacts:[[base.labels[8],[snapshot.contact,snapshot.email,snapshot.phone].filter(Boolean).join(' / ')||'—'],[base.labels[8],profile.contact||'—']],notes:p.note||'',details:[[w.terms,snapshot.paymentTerms||'—'],[w.delivery,delivery||p.kind],[w.due,p.due||'—'],[w.currency,currency],[w.reference,p.reference||'—'],[w.kind,w.purchase]],heads:['#',base.labels[16],base.labels[17],base.labels[18],base.labels[19],base.labels[20],w.received,base.labels[22]],rows:productRows,hidePayments:true,totals:[[w.orderTotal,m(total)]],extraTitle:w.extra,extra,instructions:''};
}
