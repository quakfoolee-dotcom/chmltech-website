import {businessDay} from './company-date.mjs?demo=9c44c6dabb8d4728';
import {validUnicode,charLength} from './unicode.mjs?demo=9c44c6dabb8d4728';
const must=(v,m)=>{if(!v)throw Error(m);};
const text=(v,max=240,required=false)=>{const out=String(v??'').trim();must(validUnicode(out)&&charLength(out)<=max&&(!required||out),'Enter valid CRM text within the allowed length.');return out;};
const day=v=>{const out=String(v??'').trim();must(!out||(/^\d{4}-\d{2}-\d{2}$/.test(out)&&Number(out.slice(0,4))>=1&&Number.isFinite(Date.parse(out))&&new Date(out+'T12:00:00Z').toISOString().slice(0,10)===out),'Use a valid CRM date.');return out;};
const email=v=>{const out=text(v,240);must(!out||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(out),'Enter a valid contact email.');return out;};
const integer=(v,min=0,max=100)=>{const n=Number(v);must(v!==''&&Number.isSafeInteger(n)&&n>=min&&n<=max,'Enter a valid CRM number.');return n;};
export const crmDay=(value=new Date(),s)=>s?.organization?.timezone?businessDay(s,value):new Intl.DateTimeFormat('en-CA',{timeZone:'America/Vancouver',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(value));
export const crmStages=['Lead','Qualified','Quoted','Negotiation','Won','Lost'];
export const crmKinds=['Call','Email','Meeting','Task','Note'];
const probabilities={Lead:10,Qualified:25,Quoted:50,Negotiation:75,Won:100,Lost:0};
export const freshCRM=()=>({version:1,revision:0,sequence:0,profiles:[],opportunities:[],activities:[],history:[]});
export const crm=s=>s.crm||freshCRM();
export function crmProfile(s,id){
 if(!id)return null;
 const saved=crm(s).profiles.find(p=>p.id===id||p.customerId===id);if(saved)return saved;
 const c=s.business?.customers.find(c=>c.id===id);return c?{id:c.id,customerId:c.id,company:c.name,email:c.email||'',phone:'',website:'',owner:'',language:'en',status:'Active',notes:'',contacts:[],addresses:c.address?[{id:'address-1',label:'Main address',type:'Bill to',line1:c.address,line2:'',city:'',region:'',postal:'',country:'',primary:true}]:[],createdAt:'',updatedAt:''}:null;
}
export const crmProfiles=s=>[...(s.business?.customers||[]).map(c=>crmProfile(s,c.id)),...crm(s).profiles.filter(p=>!p.customerId)];
export const crmAddress=p=>(p.addresses.find(a=>a.type==='Bill to'&&a.primary)||p.addresses.find(a=>a.type==='Bill to')||p.addresses[0]);
export const crmAddressText=p=>{const a=crmAddress(p);return a?[a.line1,a.line2,[a.city,a.region,a.postal].filter(Boolean).join(' '),a.country].filter(Boolean).join('\n'):'';};
const cents=value=>{const t=String(value);must(/^\d+(?:\.\d{1,2})?$/.test(t),'Enter an opportunity value with at most two decimals.');const [a,b='']=t.split('.'),n=Number(BigInt(a)*100n+BigInt(b.padEnd(2,'0')));return integer(n,0,1e12);};
function profileContent(s,p,id){
 const prior=crmProfile(s,id),customerId=prior?.customerId||'';must(!p.customerId||p.customerId===customerId,'Customer links cannot be reassigned.');
 const contacts=p.contacts||[],addresses=p.addresses||[];must(Array.isArray(contacts)&&contacts.length<=10&&Array.isArray(addresses)&&addresses.length<=8,'Use up to ten contacts and eight addresses.');
 const result={id,customerId,company:text(p.company,100,true),email:email(p.email),phone:text(p.phone,80),website:text(p.website,240),owner:text(p.owner,100),language:p.language||'en',status:p.status||'Active',notes:text(p.notes,2000),
  contacts:contacts.map((c,i)=>({id:'contact-'+(i+1),name:text(c.name,100,true),title:text(c.title,100),email:email(c.email),phone:text(c.phone,80),primary:c.primary===true})),
  addresses:addresses.map((a,i)=>({id:'address-'+(i+1),label:text(a.label,80,true),type:a.type,line1:text(a.line1,400,true),line2:text(a.line2,200),city:text(a.city,100),region:text(a.region,100),postal:text(a.postal,40),country:text(a.country,80),primary:a.primary===true}))};
 must(['en','zh-Hans','zh-Hant','fr'].includes(result.language)&&['Active','Prospect','Inactive'].includes(result.status),'Choose a supported CRM language and customer status.');
 must(result.contacts.filter(c=>c.primary).length<=1,'Choose one primary contact.');
 for(const type of ['Bill to','Ship to'])must(result.addresses.filter(a=>a.type===type&&a.primary).length<=1,'Choose one default address of each type.');
 must(result.addresses.every(a=>['Bill to','Ship to','Other'].includes(a.type)),'Choose a supported address type.');return result;
}
export function crmCommand(s,command,p,ctx){
 if(!command.startsWith('crm:'))return null;
 must(['Admin','Sales'].includes(ctx.role||'Admin'),'Your role cannot edit CRM records.');
 const d=s.crm||(s.crm=freshCRM()),next=prefix=>prefix+'-'+(++d.sequence);let id,profileId,action;
 if(command==='crm:saveProfile'){
  must(p.id||d.profiles.length<10000,'CRM profile limit reached.');id=p.id||next('crm-profile');must(!p.id||crmProfile(s,p.id),'Customer profile not found.');const previous=crmProfile(s,id),value=profileContent(s,p,id);profileId=id;action=previous?'Customer profile updated':'Customer profile created';
  const target=d.profiles.find(x=>x.id===id),record={...value,createdAt:target?.createdAt||ctx.time,updatedAt:ctx.time};if(target)Object.assign(target,record);else d.profiles.push(record);
 }else if(command==='crm:linkCustomer'){
  const p0=d.profiles.find(x=>x.id===p.id),customer=s.business?.customers.find(c=>c.id===p.customerId);must(p0&&!p0.customerId&&customer,'Choose an unlinked prospect and an existing customer.');must(!d.profiles.some(x=>x.customerId===customer.id),'This customer already has a saved CRM profile.');must(p.reviewed===true,'Review linking this customer.');
  p0.customerId=customer.id;p0.status='Active';p0.updatedAt=ctx.time;for(const rows of [d.opportunities,d.activities,d.history])for(const r of rows)if(r.profileId===customer.id)r.profileId=p0.id;id=p0.id;profileId=id;action='Customer linked';
 }else if(command==='crm:saveOpportunity'){
  const existing=d.opportunities.find(o=>o.id===p.id);must(!p.id||existing,'Opportunity not found.');const profile=crmProfile(s,p.profileId);must(profile,'Choose an existing customer profile.');
  must(!existing||!['Won','Lost'].includes(existing.stage)||!p.stage||p.stage===existing.stage,'Use Change stage to review reopening a closed opportunity.');
  must(!existing?.quoteId||s.salesDesk?.quotes.find(q=>q.id===existing.quoteId)?.customerId===profile.customerId,'The linked quotation belongs to another customer.');
  id=existing?.id||next('opportunity');profileId=profile.id;const stage=p.stage||existing?.stage||'Lead';must(crmStages.includes(stage),'Choose a supported opportunity stage.');
  const currency=p.currency||s.business?.homeCurrency||'CAD';must(['CAD','USD','EUR','GBP','CNY','TWD','HKD','SGD','AUD','NZD'].includes(currency),'Choose a supported opportunity currency.');
  const record={id,number:existing?.number||'OP-'+id.split('-').at(-1),profileId,title:text(p.title,140,true),owner:text(p.owner,100,true),stage,currency,value:cents(p.value),probability:stage==='Won'?100:stage==='Lost'?0:integer(p.probability??probabilities[stage]),closeDate:day(p.closeDate),source:text(p.source,100),reason:text(p.reason,1000),notes:text(p.notes,2000),quoteId:existing?.quoteId||'',createdAt:existing?.createdAt||ctx.time,updatedAt:ctx.time};
  must(stage!=='Lost'||record.reason,'Record a reason for a lost opportunity.');if(existing?.quoteId)must(s.salesDesk.quotes.find(q=>q.id===existing.quoteId).currency===currency,'Opportunity and quotation currencies must match.');
  if(existing)Object.assign(existing,record);else{must(d.opportunities.length<10000,'CRM opportunity limit reached.');d.opportunities.push(record);}action=existing?'Opportunity updated':'Opportunity created';
 }else if(command==='crm:stage'){
  const o=d.opportunities.find(o=>o.id===p.id);must(o&&crmStages.includes(p.stage),'Choose an existing opportunity and supported stage.');must(!['Won','Lost'].includes(o.stage)||p.reviewed===true,'Review before reopening a closed opportunity.');
  const reason=text(p.reason,1000);must(p.stage!=='Lost'||reason,'Record a reason for a lost opportunity.');o.stage=p.stage;o.probability=probabilities[p.stage];o.reason=reason;o.updatedAt=ctx.time;id=o.id;profileId=o.profileId;action='Opportunity stage changed';
 }else if(command==='crm:linkQuote'){
  const o=d.opportunities.find(o=>o.id===p.id),q=s.salesDesk?.quotes.find(q=>q.id===p.quoteId);must(o&&q,'Choose an opportunity and quotation.');const profile=crmProfile(s,o.profileId);must(profile.customerId&&q.customerId===profile.customerId,'The quotation belongs to another customer.');must(o.currency===q.currency,'Opportunity and quotation currencies must match.');must(!['Won','Lost'].includes(o.stage),'Reopen the opportunity before linking a quotation.');
  o.quoteId=q.id;o.value=q.total;o.stage='Quoted';o.probability=50;o.updatedAt=ctx.time;id=o.id;profileId=o.profileId;action='Quotation linked';
 }else if(command==='crm:saveActivity'){
  const existing=d.activities.find(a=>a.id===p.id),profile=crmProfile(s,p.profileId);must(!p.id||existing,'Follow-up not found.');must(profile,'Choose an existing customer profile.');const opportunityId=p.opportunityId||'';must(!opportunityId||d.opportunities.some(o=>o.id===opportunityId&&o.profileId===profile.id),'The opportunity belongs to another customer.');
  id=existing?.id||next('activity');profileId=profile.id;const kind=p.kind||'Task',due=day(p.due);must(crmKinds.includes(kind),'Choose a supported activity type.');must(kind==='Note'||due,'Set a due date for the follow-up.');
  const record={id,profileId,opportunityId,kind,title:text(p.title,140,true),owner:text(p.owner,100,true),due,priority:p.priority||'Normal',notes:text(p.notes,2000),status:existing?.status||(kind==='Note'?'Done':'Open'),outcome:existing?.outcome||'',createdAt:existing?.createdAt||ctx.time,updatedAt:ctx.time,completedAt:existing?.completedAt||(kind==='Note'?ctx.time:'')};must(['Low','Normal','High'].includes(record.priority),'Choose a supported follow-up priority.');
  if(existing)Object.assign(existing,record);else{must(d.activities.length<20000,'CRM activity limit reached.');d.activities.push(record);}action=existing?'Follow-up updated':'Follow-up created';
 }else if(command==='crm:completeActivity'){
  const a=d.activities.find(a=>a.id===p.id);must(a&&a.status==='Open','Choose an open follow-up.');must(['Done','Cancelled'].includes(p.status),'Choose a supported follow-up result.');a.status=p.status;a.outcome=text(p.outcome,1000,true);a.completedAt=ctx.time;a.updatedAt=ctx.time;id=a.id;profileId=a.profileId;action='Follow-up completed';
 }else throw Error('Unknown CRM action.');
 must(d.history.length<20000,'CRM history limit reached.');d.history.unshift({id:next('crm-event'),profileId,recordId:id,time:ctx.time,actor:text(ctx.actor||'Sales operator',100),action});d.revision++;
 validateCRM(s);return {type:action,reference:id,resultId:id,message:'CRM saved. Stock, costs and issued documents were preserved.'};
}
export function validateCRM(s){
 if(!s.crm)return;const d=s.crm;must(d.version===1&&Number.isSafeInteger(d.revision)&&d.revision>=0&&Number.isSafeInteger(d.sequence)&&d.sequence>=0,'Invalid CRM version or revision.');
 for(const key of ['profiles','opportunities','activities','history']){must(Array.isArray(d[key])&&d[key].length<=20000,'Invalid CRM records.');must(new Set(d[key].map(r=>r.id)).size===d[key].length,'Duplicate CRM record identifier.');}
 must(new Set(d.profiles.filter(p=>p.customerId).map(p=>p.customerId)).size===d.profiles.filter(p=>p.customerId).length,'Duplicate CRM customer link.');
 for(const p of d.profiles){must(/^(customer-\d+|crm-profile-\d+)$/.test(p.id),'Invalid CRM profile identifier.');must(p.customerId?s.business?.customers.some(c=>c.id===p.customerId):p.id.startsWith('crm-profile-'),'Invalid linked customer.');profileContent(s,p,p.id);}
 for(const o of d.opportunities){must(/^opportunity-\d+$/.test(o.id)&&crmProfile(s,o.profileId)&&crmStages.includes(o.stage),'Invalid opportunity reference or stage.');text(o.title,140,true);text(o.owner,100,true);integer(o.value,0,1e12);integer(o.probability);day(o.closeDate);must(['CAD','USD','EUR','GBP','CNY','TWD','HKD','SGD','AUD','NZD'].includes(o.currency),'Choose a supported opportunity currency.');text(o.source,100);text(o.reason,1000);text(o.notes,2000);must(o.stage!=='Won'||o.probability===100,'Invalid won probability.');must(o.stage!=='Lost'||o.probability===0&&o.reason,'Invalid lost opportunity.');if(o.quoteId){const q=s.salesDesk?.quotes.find(q=>q.id===o.quoteId);must(q&&q.customerId===crmProfile(s,o.profileId).customerId&&q.currency===o.currency,'Invalid CRM quotation link.');}}
 for(const a of d.activities){must(/^activity-\d+$/.test(a.id)&&crmProfile(s,a.profileId)&&crmKinds.includes(a.kind)&&['Open','Done','Cancelled'].includes(a.status)&&['Low','Normal','High'].includes(a.priority),'Invalid CRM activity.');text(a.title,140,true);text(a.owner,100,true);day(a.due);text(a.notes,2000);text(a.outcome,1000);must(a.status!=='Cancelled'||a.outcome,'Record a cancellation outcome.');must(a.kind==='Note'||a.due,'Missing follow-up date.');must(!a.opportunityId||d.opportunities.some(o=>o.id===a.opportunityId&&o.profileId===a.profileId),'Invalid activity opportunity.');}
 for(const h of d.history){must(/^crm-event-\d+$/.test(h.id)&&crmProfile(s,h.profileId)&&typeof h.time==='string'&&Number.isFinite(Date.parse(h.time)),'Invalid CRM history.');text(h.actor,100);text(h.action,100,true);must([...d.profiles,...d.opportunities,...d.activities].some(r=>r.id===h.recordId)||crmProfile(s,h.recordId),'Invalid CRM history target.');}
 const suffixes=[...d.profiles.filter(p=>p.id.startsWith('crm-profile-')),...d.opportunities,...d.activities,...d.history].map(r=>Number(r.id.split('-').at(-1)));must(suffixes.every(n=>Number.isSafeInteger(n)&&n<=d.sequence),'Invalid CRM sequence.');
}
export function crmTimeline(s,profileId){
 const p=crmProfile(s,profileId);if(!p)return [];const id=p.customerId,rows=crm(s).history.filter(h=>h.profileId===profileId).map(h=>({date:h.time,kind:h.action,reference:h.recordId,detail:h.actor,href:''}));if(!id)return rows;
 const orders=s.orders.filter(o=>o.customerId===id),ids=new Set(orders.map(o=>o.id));
 for(const q of s.salesDesk?.quotes||[])if(q.customerId===id)rows.push({date:q.createdAt||q.date,kind:'Quotation',reference:q.number,detail:q.status,href:'#business/quotes/'+q.id});
 for(const o of orders)rows.push({date:o.createdAt||o.date||'',kind:'Sales order',reference:o.number,detail:o.status,href:'#orders/'+o.id});
 for(const sh of s.shipments)if(ids.has(sh.orderId))rows.push({date:sh.shippedAt||sh.createdAt||'',kind:'Shipment',reference:sh.number,detail:sh.status,href:'#shipping/'+sh.id});
 const docs=(s.billing?.documents||[]).filter(d=>d.partyKey===id&&(d.kind==='Invoice'||d.kind==='Credit'&&(s.billing.documents.find(x=>x.id===d.parentId)?.kind==='Invoice'))),docIds=new Set(docs.map(d=>d.id));
 for(const d of docs)rows.push({date:d.date,kind:d.kind==='Credit'?'Credit note':'Invoice',reference:d.number,detail:d.status,href:'#business/'+(d.kind==='Credit'?'credits':'invoices')+'/'+d.id});
 for(const a of s.billing?.payments||[])if(docIds.has(a.documentId))rows.push({date:a.date,kind:'Payment',reference:a.number,detail:a.status,href:'#business/invoices/'+a.documentId});
 for(const r of s.business?.returns||[])if(r.kind==='Customer'&&ids.has(r.sourceId))rows.push({date:r.createdAt||r.time||'',kind:'Customer return',reference:r.number,detail:r.status,href:'#business/returns/customer'});
 return rows.sort((a,b)=>String(b.date).localeCompare(String(a.date))||a.reference.localeCompare(b.reference));
}
export function crmTotals(s){
 const d=crm(s),totals={};for(const o of d.opportunities)if(!['Won','Lost'].includes(o.stage)){const t=totals[o.currency]||(totals[o.currency]={value:0,weighted:0});t.value+=o.value;t.weighted+=Math.round(o.value*o.probability/100);}return totals;
}
