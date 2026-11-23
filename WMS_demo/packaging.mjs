// Original Chmltech WMS unit/packaging boundary. The inventory and costing ledgers
// continue to use their original, immutable whole base units.
import {validUnicode,charLength} from './unicode.mjs?demo=45f52980507d3a1b';
const must=(ok,message)=>{if(!ok)throw Error(message);};
const find=(rows,id)=>{const row=rows.find(r=>r.id===id);must(row,'Product not found.');return row;};
const text=(value,max=100,required=true)=>{const v=String(value??'').trim();must(validUnicode(v)&&charLength(v)<=max&&(!required||v),'Enter valid unit text.');return v;};
export function wholeUnits(value,zero=false){const n=Number(value);must(value!==''&&value!==undefined&&Number.isSafeInteger(n)&&n>=(zero?0:1)&&n<=10000000,'Enter a whole quantity within the allowed range.');return n;}
const setup=s=>s.packaging||(s.packaging={version:1,sequence:0,units:{},captures:[]});
export function productUnits(s,itemId,{inactive=false,legacy=false}={}){
 const i=find(s.items,itemId),rows=[{id:'base',code:i.uom,name:s.packaging?.baseNames?.[itemId]||(i.uom==='ea'?'Each':i.uom),factor:1,barcode:i.sku,active:true},...(s.packaging?.units[itemId]||[]).filter(u=>inactive||u.active)];
 const p=s.business?.profiles[itemId];
 if(legacy&&p?.packSize>1&&!rows.some(u=>u.factor===p.packSize&&u.name===p.packName))rows.push({id:'legacy',code:'PURCHASE',name:p.packName,factor:p.packSize,barcode:'',active:true});
 return rows;
}
export function selectedUnit(s,itemId,id='base',{legacy=false,inactive=false}={}){
 const unit=productUnits(s,itemId,{legacy,inactive}).find(u=>u.id===(id||'base'));
 must(unit,'The selected packaging unit is unavailable.');return {...unit};
}
export function resolveProductBarcode(s,value){
 const code=text(value,100).toUpperCase(),matches=[];
 for(const item of s.items){
  const p=s.business?.profiles[item.id];
  if(item.sku.toUpperCase()===code||p?.barcode?.toUpperCase()===code)matches.push({item,unit:selectedUnit(s,item.id)});
  for(const unit of s.packaging?.units[item.id]||[])if(unit.active&&unit.barcode&&unit.barcode.toUpperCase()===code)matches.push({item,unit:{...unit}});
 }
 must(matches.length===1,'Barcode is unknown or ambiguous. Check the product barcode in Product rules.');return matches[0];
}
export function unitQuantity(s,itemId,unitId,count,{zero=false,legacy=false}={}){
 const unit=selectedUnit(s,itemId,unitId,{legacy}),quantity=wholeUnits(count,zero),baseQty=wholeUnits(quantity*unit.factor,zero);
 return {itemId,unitId:unit.id,code:unit.code,name:unit.name,factor:unit.factor,quantity,baseQty};
}
export function scannedQuantity(s,p,{zero=false}={}){
 const match=resolveProductBarcode(s,p.code);
 const unitId=p.unitId||match.unit.id;
 must(match.unit.id==='base'||unitId===match.unit.id,'Packaging barcode and selected unit do not match.');
 return {...unitQuantity(s,match.item.id,unitId,p.qty,{zero}),barcode:String(p.code).trim()};
}
export function beforeUnits(s,command,p,ctx){
 delete p.unitCapture;
 if(!['business:scan','warehouse:scanGroup','warehouse:scanPack'].includes(command))return;
 const capture=scannedQuantity(s,p,{zero:command==='business:scan'&&p.mode==='Count'});
 // Untouched base-unit commands keep precisely their earlier behaviour.
 if(capture.unitId==='base')return;
 p.qty=capture.baseQty;p.unitCapture=capture;
}
export function afterUnits(s,current,command,p,ctx){
 if(ctx.nested||ctx.internal||!p.unitCapture)return;
 const u=setup(s);must(u.captures.length<100000,'Packaging scan history is full.');
 u.captures.push({...p.unitCapture,id:'unit-scan-'+(++u.sequence),command,time:ctx.time,actor:ctx.actor||'Local owner',reference:p.id||p.purchaseId||p.stockId||'',requestId:p.requestId||''});
}
export function unitsCommand(s,command,p,ctx){
 if(!['units:save','units:active'].includes(command))return null;
 const item=find(s.items,p.itemId),u=setup(s);u.units[item.id]||=[];
 if(command==='units:active'){
  const row=find(u.units[item.id],p.id);must(typeof p.active==='boolean','Choose the packaging status.');row.active=p.active;
  return {type:'Packaging status saved',message:'Existing order conversions were preserved.',reference:item.sku,resultId:row.id};
 }
 if(p.id==='base'){
  must((p.code===undefined||p.code===item.uom)&&(p.factor===undefined||Number(p.factor)===1)&&(p.barcode===undefined||p.barcode===item.sku),'The base stock unit code, quantity and SKU stay unchanged.');
  u.baseNames||={};u.baseNames[item.id]=text(p.name,60);
  return {type:'Unit label saved',message:'The base stock unit and historical records were preserved.',reference:item.sku,resultId:'base'};
 }
 const old=p.id?find(u.units[item.id],p.id):null;
 must(!old||old.active,'Activate this unit before editing it.');
 let code=text(p.code,20).toUpperCase(),barcode=text(p.barcode,100);const name=text(p.name,60);
 must(/^[A-Z0-9][A-Z0-9_-]*$/.test(code),'Use letters, numbers, hyphens or underscores for the unit code.');
 const factor=wholeUnits(p.factor);must(factor>1&&factor<=1000000,'A packaging unit must contain 2–1000000 base units.');
 const replacement=old&&factor!==old.factor,preferred=old&&s.business?.profiles[item.id];
 const updatePreferred=preferred&&preferred.packSize===old.factor&&preferred.packName===old.name;
 if(updatePreferred)must(charLength(name)<=30,'A preferred purchase unit name must be at most 30 characters.');
 const versioned=(value,max,used)=>{for(let n=2;n<=1000;n++){const suffix='-V'+n,next=Array.from(value).slice(0,max-suffix.length).join('')+suffix;if(!used.has(next.toUpperCase()))return next;}throw Error('No available unit version identifier.');};
 if(replacement){
  if(code===old.code)code=versioned(code,20,new Set(productUnits(s,item.id,{inactive:true}).map(r=>r.code.toUpperCase())));
  if(barcode.toUpperCase()===old.barcode.toUpperCase()){
   const used=new Set([...s.items.map(i=>i.sku),...Object.values(s.business?.profiles||{}).map(p=>p.barcode||''),...s.locations.map(l=>l.code),...Object.values(u.units).flat().map(r=>r.barcode)].map(v=>v.toUpperCase()));
   barcode=versioned(barcode,100,used);
  }
 }
 must(!productUnits(s,item.id,{inactive:true}).some(r=>r.id!==(replacement?null:old?.id)&&r.code.toUpperCase()===code),'This product already has that unit code.');
 if(old&&!replacement){
  Object.assign(old,{code,name,barcode,updatedAt:ctx.time});
  if(updatePreferred)preferred.packName=name;
  return {type:'Packaging unit updated',message:'Existing costs and order conversions were preserved.',reference:item.sku,resultId:old.id};
 }
 must(u.units[item.id].length<30,'A product can have at most 30 packaging definitions.');
 const row={id:'unit-'+(++u.sequence),code,name,factor,barcode,active:true,createdAt:ctx.time,...(replacement?{replaces:old.id}:{})};
 u.units[item.id].push(row);
 if(replacement){
  old.active=false;old.replacedBy=row.id;
  if(updatePreferred)Object.assign(preferred,{packName:name,packSize:factor});
  return {type:'Packaging conversion revised',message:'A replacement unit was created. Existing orders keep their original conversion. Print new unit labels.',reference:item.sku,resultId:row.id};
 }
 return {type:'Packaging unit saved',message:'The conversion is fixed; add a new unit to change a pack size.',reference:item.sku,resultId:row.id};
}
export function validateUnits(s){
 const u=s.packaging;if(!u)return true;
 must(u.version===1&&Number.isSafeInteger(u.sequence)&&u.sequence>=0&&u.units&&typeof u.units==='object'&&!Array.isArray(u.units)&&Array.isArray(u.captures)&&u.captures.length<=100000,'Invalid packaging records.');
 if(u.baseNames!==undefined){must(u.baseNames&&typeof u.baseNames==='object'&&!Array.isArray(u.baseNames),'Invalid base unit labels.');for(const [itemId,name]of Object.entries(u.baseNames)){find(s.items,itemId);text(name,60);}}
 const codes=new Set(),ids=new Set();
 const reserve=code=>{const key=String(code).toUpperCase();must(!codes.has(key),'Duplicate packaging barcode or SKU.');codes.add(key);};
 for(const i of s.items){reserve(i.sku);const alias=s.business?.profiles[i.id]?.barcode;if(alias)reserve(alias);}
 for(const [itemId,rows]of Object.entries(u.units)){
  find(s.items,itemId);must(Array.isArray(rows)&&rows.length<=30,'Invalid product packaging list.');const names=new Set([find(s.items,itemId).uom.toUpperCase()]);
  for(const row of rows){must(/^unit-\d+$/.test(row.id)&&Number(row.id.slice(5))<=u.sequence&&!ids.has(row.id),'Invalid packaging identifier.');ids.add(row.id);must(/^[A-Z0-9][A-Z0-9_-]{0,19}$/.test(row.code)&&!names.has(row.code),'Duplicate packaging unit code.');names.add(row.code);wholeUnits(row.factor);must(row.factor>1&&row.factor<=1000000&&typeof row.active==='boolean','Invalid packaging conversion.');text(row.name,60);text(row.barcode,100);must(!s.locations.some(l=>l.code.toUpperCase()===row.barcode.toUpperCase()),'Duplicate packaging barcode or SKU.');reserve(row.barcode);}
 }
 for(const record of u.captures){
  find(s.items,record.itemId);wholeUnits(record.quantity,true);wholeUnits(record.factor);must(record.baseQty===record.quantity*record.factor&&Number.isSafeInteger(record.baseQty),'Packaging scan conversion changed.');
  must(/^unit-scan-\d+$/.test(record.id)&&Number(record.id.slice(10))<=u.sequence&&!ids.has(record.id),'Invalid packaging scan history.');ids.add(record.id);
 }
 for(const order of s.orders)for(const line of order.unitLines||[]){const base=order.lines.find(l=>l.itemId===line.itemId);must(base&&line.baseQty===line.quantity*line.factor&&base.qty===line.baseQty,'Sales packaging snapshot no longer matches its original order.');wholeUnits(line.quantity);wholeUnits(line.factor);}
 return true;
}


