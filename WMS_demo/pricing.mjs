import {businessDay} from './company-date.mjs?demo=9c44c6dabb8d4728';
import {validUnicode,charLength} from './unicode.mjs?demo=9c44c6dabb8d4728';
const must=(v,m)=>{if(!v)throw Error(m);};
export const salesToday=(value=new Date(),s)=>s?.organization?.timezone?businessDay(s,value):new Intl.DateTimeFormat('en-CA',{timeZone:'America/Vancouver',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(value));
export const salesDesk=s=>s.salesDesk||{version:1,sequence:0,groups:[],rules:[],quotes:[]};
export const setupSalesDesk=s=>s.salesDesk||(s.salesDesk={version:1,sequence:0,groups:[],rules:[],quotes:[]});
export const salesText=(v,max=240,required=false)=>{const t=String(v??'').trim();must(validUnicode(t)&&charLength(t)<=max&&(!required||t),'Enter valid sales text within the field limit.');return t;};
export function salesDay(v){const d=String(v??'');must(/^\d{4}-\d{2}-\d{2}$/.test(d)&&Number.isFinite(Date.parse(d))&&new Date(d+'T00:00:00Z').toISOString().slice(0,10)===d,'Use a valid calendar date.');return d;}
export function priceScaled(v,places=4){const t=String(v??'').trim();must(new RegExp(`^\\d+(?:\\.\\d{1,${places}})?$`).test(t),'Enter a nonnegative amount with the allowed decimal places.');const [a,b='']=t.split('.'),n=Number(BigInt(a)*10n**BigInt(places)+BigInt(b.padEnd(places,'0')));must(Number.isSafeInteger(n)&&n<=1e11,'Price exceeds the allowed range.');return n;}
const whole=(v,min=0,max=10000000)=>{const n=Number(v);must(v!==''&&v!==undefined&&Number.isSafeInteger(n)&&n>=min&&n<=max,'Enter a whole quantity within the allowed range.');return n;};
const rounded=(a,b)=>Number((BigInt(a)+BigInt(b)/2n)/BigInt(b));
export const lineCents=(qty,price4)=>{const n=rounded(BigInt(qty)*BigInt(price4),100);must(Number.isSafeInteger(n)&&n<=1e12,'Quotation total exceeds the allowed range.');return n;};
export function legacyPrice(s,customerId,itemId,qty,date){const rows=(s.business?.prices||[]).filter(p=>p.itemId===itemId&&(!p.customerId||p.customerId===customerId)&&qty>=p.minimum&&(!p.until||p.until>=date)&&(!p.from||p.from<=date));rows.sort((a,b)=>Number(!!b.customerId)-Number(!!a.customerId)||b.minimum-a.minimum||b.id.localeCompare(a.id));return rows[0]||null;}
function rulePrice(rule,base4,cost4){
 let value;if(rule.type==='Fixed')value=rule.value4;else if(rule.type==='Discount')value=rounded(BigInt(base4)*BigInt(10000-rule.percentBP),10000);else{must(cost4!==null,'A recorded unit cost is required for this pricing rule.');value=rule.type==='Markup'?rounded(BigInt(cost4)*BigInt(10000+rule.percentBP),10000):rounded(BigInt(cost4)*10000n,10000-rule.percentBP);}
 const step=rule.roundStep4;if(rule.rounding!=='None'){value=(rule.rounding==='Up'?Math.ceil(value/step):rule.rounding==='Down'?Math.floor(value/step):Math.floor(value/step+.5))*step;}
 must(Number.isSafeInteger(value)&&value>=0&&value<=1e11,'Price exceeds the allowed range.');return value;
}
export function explainPrice(s,{customerId,itemId,qty,date=salesToday(undefined,s)}){
 salesDay(date);whole(qty,1);const item=s.items.find(i=>i.id===itemId);must(item,'Product not found.');must(s.business?.customers.some(c=>c.id===customerId),'Customer not found.');
 const legacy=legacyPrice(s,customerId,itemId,qty,date),base4=Math.round((legacy?.price||0)*10000),recorded=s.operations?.costs?.[itemId],cost4=Number.isFinite(recorded)?Math.round(recorded*10000):null,d=salesDesk(s),groups=d.groups.filter(g=>g.customerIds.includes(customerId)).map(g=>g.id);
 const candidates=d.rules.filter(r=>r.active&&(!r.itemId||r.itemId===itemId)&&(!r.category||r.category===item.category)&&(!r.customerId||r.customerId===customerId)&&(!r.groupId||groups.includes(r.groupId))&&qty>=r.minimum&&(!r.maximum||qty<=r.maximum)&&(!r.from||r.from<=date)&&(!r.until||r.until>=date)).map(r=>{
  let price4=null,error='';try{must(r.type!=='Discount'||legacy,'A legacy list price is required for a discount rule.');price4=rulePrice(r,base4,cost4);}catch(e){error=e.message;}
  return {id:r.id,name:r.name,type:r.type,priority:r.priority,customerSpecificity:r.customerId?2:r.groupId?1:0,productSpecificity:r.itemId?2:r.category?1:0,minimum:r.minimum,price4,error,rule:structuredClone(r)};
 });
 candidates.sort((a,b)=>b.priority-a.priority||b.customerSpecificity-a.customerSpecificity||b.productSpecificity-a.productSpecificity||b.minimum-a.minimum||(a.price4??Infinity)-(b.price4??Infinity)||a.id.localeCompare(b.id));
 const winner=candidates[0];if(winner?.error)throw Error(winner.error);
 return {itemId,customerId,date,qty,currency:s.business.homeCurrency,price4:winner?.price4??base4,legacyRuleId:legacy?.id||'',legacyPrice4:base4,recordedCost4:cost4,ruleId:winner?.id||'',ruleName:winner?.name||'Legacy pricing',type:winner?.type||'Legacy',candidates:candidates.slice(0,50),candidateCount:candidates.length,selection:'Priority, customer specificity, product specificity, quantity break, price, rule ID'};
}
export function pricingCommand(s,command,p,ctx){
 if(!command.startsWith('pricing:'))return null;const d=setupSalesDesk(s),event=(type,id)=>({type,reference:id,resultId:id,message:'Existing quotations and issued prices were preserved.'});
 if(command==='pricing:group'){
  const name=salesText(p.name,100,true),customerIds=p.customerIds;must(Array.isArray(customerIds)&&customerIds.length<=1000&&new Set(customerIds).size===customerIds.length&&customerIds.every(id=>s.business.customers.some(c=>c.id===id)),'Choose distinct existing customers for the pricing group.');
  const group=p.id?d.groups.find(g=>g.id===p.id):null;must(!p.id||group,'Pricing group not found.');if(group){group.name=name;group.customerIds=[...customerIds];return event('Pricing group saved',group.id);}const id='pricing-group-'+(++d.sequence);d.groups.push({id,name,customerIds:[...customerIds]});return event('Pricing group saved',id);
 }
 if(command==='pricing:active'){const rule=d.rules.find(r=>r.id===p.id);must(rule&&typeof p.active==='boolean','Choose an existing pricing rule and status.');rule.active=p.active;return event('Pricing rule status saved',rule.id);}
 must(command==='pricing:rule','Unknown pricing action.');must(d.rules.length<10000,'Pricing rule limit reached.');
 const type=p.type;must(['Fixed','Discount','Markup','Margin'].includes(type),'Choose a supported pricing calculation.');
 const customerId=p.customerId||'',groupId=p.groupId||'',itemId=p.itemId||'',category=salesText(p.category,100);must(!(customerId&&groupId)&&!(itemId&&category),'Choose one customer scope and one product scope.');
 must(!customerId||s.business.customers.some(c=>c.id===customerId),'Customer not found.');must(!groupId||d.groups.some(g=>g.id===groupId),'Pricing group not found.');must(!itemId||s.items.some(i=>i.id===itemId),'Product not found.');must(!category||s.items.some(i=>i.category===category),'Product category not found.');
 const minimum=whole(p.minimum??1,1),maximum=whole(p.maximum??0);must(!maximum||maximum>=minimum,'Maximum quantity must cover the minimum.');const from=p.from?salesDay(p.from):'',until=p.until?salesDay(p.until):'';must(!from||!until||until>=from,'End date must follow start date.');
 const percentBP=type==='Fixed'?0:priceScaled(p.percent,2);must(percentBP<=(type==='Markup'?100000:10000)&&!(type==='Margin'&&percentBP===10000),'Enter a valid percentage for the calculation.');
 const rounding=p.rounding||'None';must(['None','Nearest','Up','Down'].includes(rounding),'Choose a supported rounding method.');const roundStep4=rounding==='None'?0:priceScaled(p.roundStep);must(rounding==='None'||roundStep4>0,'Enter a positive price rounding step.');
 const id='pricing-rule-'+(++d.sequence);d.rules.push({id,name:salesText(p.name,100,true),type,itemId,category,customerId,groupId,minimum,maximum,from,until,priority:whole(p.priority??0,0,1000),active:p.active!==false,value4:type==='Fixed'?priceScaled(p.value):0,percentBP,rounding,roundStep4,createdAt:ctx.time});return event('Advanced pricing rule saved',id);
}
export function validateSalesDesk(s){
 if(!s.salesDesk)return;const d=s.salesDesk;must(d.version===1&&Number.isSafeInteger(d.sequence)&&d.sequence>=0&&['groups','rules','quotes'].every(k=>Array.isArray(d[k])&&d[k].length<=10000),'Invalid sales desk records.');
 const ids=new Set();for(const row of [...d.groups,...d.rules,...d.quotes]){must(typeof row.id==='string'&&!ids.has(row.id),'Duplicate sales desk identifier.');ids.add(row.id);const n=Number(row.id.split('-').at(-1));must(Number.isSafeInteger(n)&&n>0&&n<=d.sequence,'Sales desk sequence is invalid.');}
 for(const g of d.groups){salesText(g.name,100,true);must(Array.isArray(g.customerIds)&&new Set(g.customerIds).size===g.customerIds.length&&g.customerIds.every(id=>s.business.customers.some(c=>c.id===id)),'Invalid pricing group membership.');}
 for(const r of d.rules){salesText(r.name,100,true);must(typeof r.active==='boolean'&&['Fixed','Discount','Markup','Margin'].includes(r.type),'Invalid pricing rule.');whole(r.priority,0,1000);whole(r.minimum,1);whole(r.maximum);must(!r.maximum||r.maximum>=r.minimum,'Invalid pricing quantity range.');must(!r.customerId||s.business.customers.some(c=>c.id===r.customerId),'Pricing customer is missing.');must(!r.groupId||d.groups.some(g=>g.id===r.groupId),'Pricing group is missing.');must(!r.itemId||s.items.some(i=>i.id===r.itemId),'Pricing product is missing.');must(!(r.customerId&&r.groupId)&&!(r.itemId&&r.category),'Invalid pricing scope.');if(r.from)salesDay(r.from);if(r.until)salesDay(r.until);must(!r.from||!r.until||r.until>=r.from,'Invalid pricing dates.');must(Number.isSafeInteger(r.percentBP)&&r.percentBP>=0&&r.percentBP<=(r.type==='Markup'?100000:10000)&&!(r.type==='Margin'&&r.percentBP===10000),'Invalid pricing percentage.');must(Number.isSafeInteger(r.value4)&&r.value4>=0&&r.value4<=1e11,'Invalid fixed price.');must(['None','Nearest','Up','Down'].includes(r.rounding)&&Number.isSafeInteger(r.roundStep4)&&(r.rounding==='None'?r.roundStep4===0:r.roundStep4>0),'Invalid rounding.');}
}
