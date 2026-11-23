// Read-only document recognition. A scanned URL is data, never a navigation target.
const pattern=/^(INV|BILL|CN|SCN|PO|SH|QT)-[1-9]\d{0,8}$/;
let phoneAddress='';
export function normalizePhoneAddress(value){
 if(!String(value||'').trim())return '';let u;try{u=new URL(String(value).trim());}catch{throw Error('Use a trusted HTTPS phone address on your private network.');}
 const a=u.hostname.split('.').map(Number),privateIP=a.length===4&&a.every(n=>Number.isInteger(n)&&n>=0&&n<=255)&&(a[0]===10||a[0]===172&&a[1]>=16&&a[1]<=31||a[0]===192&&a[1]===168);
 if(!privateIP||u.protocol!=='https:'||u.username||u.password||u.search||u.hash||!['/','/scan.html','/mobile.html'].includes(u.pathname))throw Error('Use a trusted HTTPS phone address on your private network.');return u.origin;
}
export const setPhoneAddress=value=>phoneAddress=normalizePhoneAddress(value);
export const getPhoneAddress=()=>phoneAddress;
export const documentQRValue=number=>phoneAddress?`${phoneAddress}/scan.html#document/${documentNumber(number)}`:`HARBOR:DOC:${documentNumber(number)}`;
export function documentNumber(value){const code=String(value??'').trim().toUpperCase();if(!pattern.test(code))throw Error('Scan an invoice, purchase order or shipment document number.');return code;}
export function parseDocumentScan(value,{origin='',phoneOrigin=phoneAddress}={}){
 let code=String(value??'').trim();if(code.length>500)throw Error('Scanned text is too long.');
 if(/^https?:/i.test(code)){let u;try{u=new URL(code);}catch{throw Error('Invalid document link.');}const allowed=[origin,phoneOrigin].filter(Boolean);if(!allowed.includes(u.origin)||u.username||u.password||u.pathname!==new URL('./scan.html',import.meta.url).pathname||u.search||!u.hash.startsWith('#document/'))throw Error('This QR link belongs to another site. Enter the Chmltech WMS document number instead.');code=u.hash.slice(10);}
 else if(/^HARBOR:DOC:/i.test(code))code=code.slice(11);
 if(code.startsWith('*')&&code.endsWith('*'))code=code.slice(1,-1);
 return documentNumber(code);
}
export function resolveDocument(s,value,options={}){
 const code=parseDocumentScan(value,options),matches=[];
 for(const d of s.billing?.documents||[])if(d.number===code)matches.push({id:d.id,number:code,kind:d.kind==='Invoice'?'Invoice':d.kind==='Bill'?'Supplier bill':'Credit note',route:`business/${d.kind==='Invoice'?'invoices':d.kind==='Bill'?'bills':'credits'}/${d.id}`,status:d.status,party:d.party.name,date:d.date,currency:d.currency,total:d.total,lines:d.lines.map(l=>({sku:l.sku,name:l.name,description:l.description,qty:l.qty,uom:l.uom})),reference:d.sourceRef});
 for(const q of s.salesDesk?.quotes||[])if(q.number===code)matches.push({id:q.id,number:q.number,kind:'Sales quotation',route:`business/quotes/${q.id}`,status:q.status,party:q.party.name,date:q.date,currency:q.currency,total:q.total,reference:q.reference,lines:q.lines.map(l=>({sku:l.sku,name:l.name,description:l.description,qty:l.qty,uom:l.uom}))});
 for(const p of s.operations?.purchases||[])if(p.number===code)matches.push({id:p.id,number:code,kind:'Purchase order',route:`purchasing/${p.id}`,status:p.status,party:p.supplier,currency:p.currency,reference:p.reference||'',lines:(p.lines||[p]).map(l=>({...l,sku:l.sku||s.items.find(i=>i.id===l.itemId)?.sku,name:l.name||s.items.find(i=>i.id===l.itemId)?.name,description:l.description||'',uom:l.uom||s.items.find(i=>i.id===l.itemId)?.uom}))});
 for(const sh of s.shipments)if(sh.number===code){const o=s.orders.find(o=>o.id===sh.orderId),p=s.picks.find(p=>p.id===sh.pickId),lines=sh.lines||s.operations?.shipping?.[sh.id]?.orderLines||p?.lines||o.lines;matches.push({id:sh.id,number:code,kind:'Shipment',route:`shipping/${sh.id}`,status:sh.status,party:o.customer,date:sh.shippedAt||sh.createdAt,reference:o.number,lines:lines.map(l=>({...l,sku:s.items.find(i=>i.id===l.itemId)?.sku,name:s.items.find(i=>i.id===l.itemId)?.name,description:s.items.find(i=>i.id===l.itemId)?.description||'',uom:s.items.find(i=>i.id===l.itemId)?.uom}))});}
 if(matches.length!==1)throw Error(matches.length?'Document number is ambiguous. Choose the record manually.':'Document not found. Refresh Chmltech WMS and check the printed number.');return matches[0];
}
