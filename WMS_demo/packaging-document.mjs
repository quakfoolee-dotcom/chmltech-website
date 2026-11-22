// Read-only display: amounts and posted quantities remain base-unit values.
const caption={en:'Stock units','zh-Hans':'库存单位','zh-Hant':'庫存單位',fr:'Unités de stock'};
export function packagedDocumentLine(line,locale='en'){
 const u=line.unitSnapshot,base={price:line.price/10000,quantity:`${line.qty} ${line.uom}`,note:''};
 if(!u||!Number.isSafeInteger(u.factor)||u.factor<2)return base;
 const note=`${caption[locale]||caption.en}: ${line.qty} ${line.uom} (${u.factor} / ${u.name})`;
 return line.qty%u.factor===0?{price:base.price*u.factor,quantity:`${line.qty/u.factor} ${u.name}`,note}:{...base,note};
}

