import {salesDesk} from './pricing.mjs?demo=5d9e5d1ce6c83eb1';import {quotationStatus} from './quotations.mjs?demo=5d9e5d1ce6c83eb1';import {invoiceLayout} from './invoice-layout.mjs?demo=5d9e5d1ce6c83eb1';import {translate} from './locale.mjs?demo=5d9e5d1ce6c83eb1';
export function quotationDocuments(s,id,locale='en',revision=null){
 if(!['en','zh-Hans','zh-Hant','fr'].includes(locale))throw Error('Choose a supported document language.');const current=salesDesk(s).quotes.find(q=>q.id===id);if(!current)throw Error('Quotation not found.');const q=revision&&Number(revision)!==current.revision?current.versions.find(v=>v.revision===Number(revision)):current;if(!q)throw Error('Quotation revision not found.');
 const t=text=>translate(text,locale),lines=q.lines.map(l=>({...l,price:l.price4,unitSnapshot:l.unit,discount:0,net:l.total,tax:0,total:l.total})),doc={number:q.number,sourceRef:q.number,sourceId:'',currency:q.currency,issuer:q.issuer,party:q.party,lines,status:'Draft',net:q.total,total:q.total,tax:0,date:q.date,reference:q.reference,note:q.note};
 const status=t(quotationStatus(q)),v=invoiceLayout({...s,billing:{payments:[],...s.billing}},doc,{},locale,status),money=n=>`${q.currency} ${(n/100).toFixed(2)}`;
 v.labels=[...v.labels];v.labels[0]=t('Sales quotation');v.meta=[[t('Quotation #'),q.number],[t('Revision'),String(q.revision)],[t('Date'),q.date],[t('Valid until'),q.validUntil]];
 v.details=[[t('Revision'),String(q.revision)],[t('Currency'),q.currency],[t('Valid until'),q.validUntil],[t('Price date'),q.date],[t('Customer reference'),q.reference||'—'],[t('Document type'),t('Quotation only')]];
 v.rows=v.rows.map(r=>r.map((value,k)=>k===1?t('Quotation'):value));v.heads=[...v.heads];v.heads[5]=t('Quoted quantity');v.hidePayments=true;v.instructions='';v.totals=[[t('Subtotal'),money(q.total)],[t('Tax'),money(0)],[t('Quotation total'),money(q.total)]];
 // Customer PDFs deliberately exclude internal cost bases, rule candidates and margins.
 return [{locale,title:t('Sales quotation'),ref:q.number,size:'A4',density:'compact',form:v,blocks:[],footer:t('Quotation only. Taxes are not included. No stock movement, invoice or payment is recorded.'),pageWord:t('Page'),continued:t('continued')}];
}

