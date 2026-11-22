import {charLength,validUnicode} from './unicode.mjs?demo=5d9e5d1ce6c83eb1';
import {ops} from './operations.mjs?demo=5d9e5d1ce6c83eb1';
export const catalogColumns=['sku','name','description','supplier','category','uom','reorderPoint','tracking'];
// Prefix potentially active spreadsheet cells with an apostrophe. Escape an
// original apostrophe too, making the transformation reversible on import.
const protect=value=>/^(?:'|\s*[=+@-]|[\t\r\n])/.test(value)?"'"+value:value;
const unprotect=value=>value.startsWith("'")&&/^(?:'|\s*[=+@-]|[\t\r\n])/.test(value.slice(1))?value.slice(1):value;
export function csvText(rows){return '\uFEFF'+rows.map(row=>row.map(v=>'"'+protect(String(v??'')).replaceAll('"','""')+'"').join(',')).join('\r\n')+'\r\n';}
export function parseCSV(text){
  text=text.replace(/^\uFEFF/,'');const rows=[];let row=[],cell='',quoted=false,closed=false;
  const push=()=>{row.push(unprotect(cell));cell='';closed=false;};
  for(let p=0;p<text.length;p++){
    const c=text[p];
    if(quoted){if(c==='"'){if(text[p+1]==='"'){cell+='"';p++;}else{quoted=false;closed=true;}}else cell+=c;continue;}
    if(c==='"'){if(cell||closed)throw Error('Unexpected quote in CSV.');quoted=true;}
    else if(c===',')push();
    else if(c==='\n'||c==='\r'){if(c==='\r'&&text[p+1]==='\n')p++;push();if(row.some(Boolean))rows.push(row);row=[];}
    else{if(closed)throw Error('Unexpected text after a quoted CSV field.');cell+=c;}
  }
  if(quoted)throw Error('CSV has an unclosed quoted field.');
  if(cell||closed||row.length){push();if(row.some(Boolean))rows.push(row);}
  return rows;
}
export const exportCatalog=s=>csvText([catalogColumns,...s.items.map(i=>[i.sku,i.name,i.description||'',i.supplier||'',i.category,i.uom,i.reorderPoint,ops(s).tracking[i.id]||'Lot'])]);
export function catalogRows(text){
  const [heads,...rows]=parseCSV(text);
  if(!heads||heads.length!==catalogColumns.length||catalogColumns.some(k=>!heads.includes(k)))throw Error('Use the Harbor catalog CSV columns: '+catalogColumns.join(', '));
  if(!rows.length||rows.length>500)throw Error('Import between 1 and 500 catalog rows at a time.');
  const seen=new Set();
  return rows.map((r,index)=>{
    const fail=message=>{throw Error(`CSV row ${index+2}: ${message}`);};
    if(r.length!==heads.length)fail('wrong number of columns.');
    const out=Object.fromEntries(heads.map((k,j)=>[k,r[j]]));
    for(const [k,max] of Object.entries({sku:40,name:100,description:1000,supplier:100,category:240})){
      if(!validUnicode(out[k])||charLength(out[k])>max||/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/u.test(out[k]))fail(`${k} has invalid text or exceeds ${max} characters.`);
    }
    if(!out.sku.trim()||!out.name.trim())fail('SKU and name are required.');
    const key=out.sku.trim().toUpperCase();if(seen.has(key))fail('duplicate SKU.');seen.add(key);
    if(!['ea','roll','pair','case'].includes(out.uom))fail('unit must be ea, roll, pair or case.');
    if(!['Lot','Serial'].includes(out.tracking))fail('tracking must be Lot or Serial.');
    if(!/^\d+$/.test(out.reorderPoint)||Number(out.reorderPoint)>10000000)fail('invalid reorder point.');
    out.reorderPoint=Number(out.reorderPoint);return out;
  });
}

