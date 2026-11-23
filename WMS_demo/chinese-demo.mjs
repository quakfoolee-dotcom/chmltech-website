// Add examples to the current workspace without replacing existing records.
export const chineseDemoOrder=s=>s.operations?.purchases.find(p=>p.exampleSet==='chinese-purchasing-v1');
export const chineseDemoNeedsUpgrade=s=>!!chineseDemoOrder(s)&&chineseDemoOrder(s).exampleVersion!==2;
const unique=(base,rows,key)=>{const used=new Set(rows.map(r=>r[key].toUpperCase()));let value=base,n=2;while(used.has(value.toUpperCase()))value=`${base}-${n++}`;return value;};

function expandChineseDemo(s,ctx){
 const first=chineseDemoOrder(s);
 if(first.exampleVersion===2)return {type:'Chinese examples opened',reference:first.number,message:'Six previously loaded examples retained.',resultId:first.id};
 const second=s.operations.purchases.find(p=>p.id===`po-${Number(first.id.slice(3))+1}`);
 const cup=first.lines?.[0]?.itemId,scanner=first.lines?.[1]?.itemId;
 if(!cup||!scanner||second?.lines?.[0]?.itemId!==scanner)throw Error('The original Chinese example orders could not be identified. Existing records were kept.');
 let next=s;const added=[];
 const run=(command,payload)=>{const result=ctx.dispatch(next,command,payload,{now:ctx.time});next=result.state;return result.resultId;};
 const create=(supplierId,reference,lines,extra={})=>{const id=run('createPurchase',{supplierId,reference,note:'中文演示数据 / Chinese example data',lines,...extra});added.push(id);return id;};
 create(first.supplierId,'补货采购 / Replenishment demo',[{itemId:cup,qty:12,unitCost:28.75}]);
 create(second.supplierId,'繁體採購 / Scanner order demo',[{itemId:scanner,qty:8,unitCost:145.50}]);
 const cancelled=create(first.supplierId,'取消采购 / Cancelled demo',[{itemId:cup,qty:6,unitCost:28.75},{itemId:scanner,qty:2,unitCost:145.50}]);
 run('cancelPurchase',{id:cancelled});
 const direct=create(second.supplierId,'直送客戶 / Direct delivery demo',[{itemId:scanner,qty:3,unitCost:145.50}],{kind:'Drop ship',customer:'中文示範商行'});
 run('receivePurchase',{id:direct,reference:'已送達 / Delivered demo',lines:[{lineId:'line-1',qty:3}]});
 const anchor=chineseDemoOrder(next);anchor.exampleVersion=2;anchor.examplePurchaseIds=[first.id,second.id,...added];
 Object.assign(s,next);
 return {type:'Six Chinese examples ready',reference:first.number,message:'Added four example purchase orders. Existing purchases and warehouse stock retained.',resultId:first.id};
}

export function loadChineseDemo(s,ctx){
 const existing=chineseDemoOrder(s);
 if(existing)return expandChineseDemo(s,ctx);
 let next=s;
 const run=(command,payload)=>{const result=ctx.dispatch(next,command,payload,{now:ctx.time});next=result.state;return result.resultId;};
 const supplierSC='深圳市华兴供应链有限公司',supplierTC='臺灣宏達貿易股份有限公司';
 const cup=run('createItem',{sku:unique('DEMO-CN-SC-001',next.items,'sku'),name:'不锈钢保温杯',description:'双层真空保温，容量 500 mL。\n颜色：海蓝；包装：12 个/箱。含 "食品级" 内胆, BPA-free。',supplier:supplierSC,category:'中文演示 / Chinese demo',uom:'ea',reorderPoint:5,tracking:'Lot'});
 const scanner=run('createItem',{sku:unique('DEMO-CN-TC-002',next.items,'sku'),name:'無線條碼掃描器',description:'支援繁體中文標籤與 USB-C 連線。\n型號：TW-2026；規格：5 V / 2 A；供應商備註：𠮷祥。',supplier:supplierTC,category:'中文示範 / Chinese demo',uom:'ea',reorderPoint:5,tracking:'Lot'});
 const firstSupplier=run('saveSupplier',{code:unique('DEMO-CN-SUP',next.operations.suppliers||[],'code'),name:supplierSC,englishName:'Huaxing Supply (demo)',contact:'王小明 / 王曉明',email:'warehouse@example.com',address:'中国深圳市南山区\n示例路 88 号（演示地址）',paymentTerms:'30 天 / 30 days',notes:'中文演示数据 / Chinese example data',products:[{itemId:cup,vendorSku:'华兴-杯-001'},{itemId:scanner,vendorSku:'華興-掃描-002'}]});
 const secondSupplier=run('saveSupplier',{code:unique('DEMO-TW-SUP',next.operations.suppliers||[],'code'),name:supplierTC,englishName:'Hongda Trading (demo)',contact:'陳曉華',email:'supplier@example.com',address:'臺灣臺北市\n示範路 66 號（示範地址）',paymentTerms:'月結 30 天',notes:'繁體中文示範資料',products:[{itemId:scanner,vendorSku:'宏達-掃描器-002'}]});
 const firstOrder=run('createPurchase',{supplierId:firstSupplier,reference:'中文采购示例 / Chinese demo',note:'演示采购 / 示範採購。分批交货，保留简体及繁體产品描述。',lines:[{itemId:cup,qty:24,unitCost:28.75},{itemId:scanner,qty:12,unitCost:145.50}]});
 const location=next.locations.find(l=>l.type==='Storage')||next.locations.find(l=>l.type==='Receiving');
 if(!location)throw Error('Add a storage or receiving location before loading the examples.');
 run('receivePurchase',{id:firstOrder,reference:'演示送货单 / 示範送貨單',lines:[{lineId:'line-1',qty:10,locationId:location.id,lot:'DEMO-华兴-甲'},{lineId:'line-2',qty:5,locationId:location.id,lot:'DEMO-華興-乙'}]});
 run('createPurchase',{supplierId:secondSupplier,reference:'繁體中文採購示範',note:'示範資料，尚未收貨。',lines:[{itemId:scanner,qty:6,unitCost:145.50}]});
 const order=next.operations.purchases.find(p=>p.id===firstOrder);order.exampleSet='chinese-purchasing-v1';
 expandChineseDemo(next,ctx);
 Object.assign(s,next);
 return {type:'Chinese examples loaded',reference:order.number,message:'Added two demo suppliers, two demo products, six purchases and a sample partial receipt. Existing records retained.',resultId:firstOrder};
}
