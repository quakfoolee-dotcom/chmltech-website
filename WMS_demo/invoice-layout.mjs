import {documentScanHTML,drawDocumentCodes} from './scan-codes.mjs?demo=2d15b6e9cd84b84d';
import {barcodeSVG} from './barcode.mjs?demo=2d15b6e9cd84b84d';
import {packagedDocumentLine} from './packaging-document.mjs?demo=2d15b6e9cd84b84d';
const labels={
 en:['Invoice','Invoice #','Order #','Customer PO / reference','Date','Bill to','Ship to','Customer','Contact','Notes','Sales rep','Payment terms','FOB point','Carrier','Ship service','Date scheduled','Type','Item','Description','Unit price','Qty ordered','Discount','Total price','Date','Payment','Amount','Reference','Subtotal','Tax','Total','Paid','Balance due','Credits','Refunds','Refund due','Due date','Sale','No payments recorded'],
 'zh-Hans':['销售发票','发票号','订单号','客户采购单 / 参考编号','日期','账单地址','收货地址','客户','联系人','备注','销售代表','付款条件','FOB 交货点','承运商','运输服务','计划日期','类型','货号','产品说明','单价','订购数量','折扣','金额','日期','付款方式','金额','参考编号','小计','税额','总额','已付','应付余额','贷项','退款','应退金额','到期日','销售','暂无付款记录'],
 'zh-Hant':['銷售發票','發票號','訂單號','客戶採購單 / 參考編號','日期','帳單地址','收貨地址','客戶','聯絡人','備註','銷售代表','付款條件','FOB 交貨點','承運商','運輸服務','計畫日期','類型','貨號','產品說明','單價','訂購數量','折扣','金額','日期','付款方式','金額','參考編號','小計','稅額','總額','已付','應付餘額','貸項','退款','應退金額','到期日','銷售','暫無付款記錄'],
 fr:['Facture','N° de facture','N° de commande','Bon client / référence','Date','Facturer à','Livrer à','Client','Contact','Notes','Commercial','Conditions de paiement','Point FOB','Transporteur','Service de livraison','Date prévue','Type','Article','Description','Prix unitaire','Qté commandée','Remise','Montant','Date','Paiement','Montant','Référence','Sous-total','Taxes','Total','Payé','Solde dû','Avoirs','Remboursements','À rembourser','Échéance','Vente','Aucun paiement enregistré']
};
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function invoiceLayout(s,d,balance,locale,status){
 const l=labels[locale],m=v=>`${d.currency} ${(v/100).toLocaleString('en-CA',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
 const sh=s.shipments.find(sh=>sh.id===d.sourceId),shipping=s.operations?.shipping?.[d.sourceId],a=shipping?.address||{};
 const shipAddress=[a.name,a.line1,a.line2,[a.city,a.region,a.postal].filter(Boolean).join(' '),a.country].filter(Boolean).join('\n');
 const order=d.sourceRef.split(' / ').at(-1),discount=d.lines.reduce((sum,line)=>sum+line.discount,0);
 return {labels:l,company:[d.issuer.name,d.issuer.address,d.issuer.contact,d.issuer.taxId].filter(Boolean),number:d.number,status,
  meta:[[l[1],d.number],[l[2],order],[l[3],d.reference||'—'],[l[4],d.date]],
  addresses:[[l[5],[d.party.name,d.party.address].filter(Boolean).join('\n')],[l[6],shipAddress||'—']],
  contacts:[[l[7],d.party.name],[l[8],a.contact||d.party.contact||'—']],
  notes:d.note||'',details:[[l[10],'—'],[l[11],d.due?`${l[35]}: ${d.due}`:'—'],[l[12],'—'],[l[13],sh?.carrier||'—'],[l[14],shipping?.service||'—'],[l[15],'—']],
  heads:['#',...l.slice(16,23)],rows:d.lines.map((line,index)=>{const pack=packagedDocumentLine(line,locale);return [String(index+1),l[36],line.sku,[line.name,line.description,pack.note].filter(Boolean).join('\n'),`${d.currency} ${pack.price.toFixed(4)}`,pack.quantity,m(line.discount),m(line.total)];}),
  paymentHeads:l.slice(23,27),payments:s.billing.payments.filter(p=>p.documentId===d.id&&p.status==='Recorded').map(p=>[p.date,`${p.kind==='Refund'?l[33]+' / ':''}${p.method}`,m(p.amount),p.reference]),
  totals:[[l[27],m(d.net+discount)],...(discount?[[l[21],m(discount)]]:[]),[l[28],m(d.tax)],[l[29],m(d.total)],...(d.status==='Issued'?[[l[32],m(balance.credits)],[l[30],m(balance.paid)],...(balance.refunded?[[l[33],m(balance.refunded)]]:[]),[balance.refundDue?l[34]:l[31],m(balance.refundDue||balance.due)]]:[])],
  instructions:d.issuer.paymentInstructions||'',currency:d.currency};
}
export function invoiceHTML(d){
 const v=d.invoice||d.form,table=(heads,rows,cls='')=>`<table class="invoice-table ${cls}"><thead><tr>${heads.map(h=>`<th>${e(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(x=>`<td>${e(x)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
 return `<article class="business-document invoice-document" lang="${e(d.locale)}"><header class="invoice-heading"><div class="invoice-company">${v.company.map((x,i)=>i?`<div>${e(x)}</div>`:`<strong>${e(x)}</strong>`).join('')}</div><div class="invoice-title"><h2>${e(v.labels[0])}</h2><div>${e(v.status)}</div></div></header>${documentScanHTML(v.number,d.locale)}<div class="invoice-meta">${table(v.meta.map(x=>x[0]),[v.meta.map(x=>x[1])])}</div><div class="invoice-addresses">${v.addresses.map(([label,value],i)=>`<section><h3>${e(label)}</h3><div>${e(value)}</div><p>${e(v.contacts[i][0])}: ${e(v.contacts[i][1])}</p></section>`).join('')}</div><div class="invoice-notes"><b>${e(v.labels[9])}</b><div>${e(v.notes||'—')}</div></div>${table(v.details.map(x=>x[0]),[v.details.map(x=>x[1])],'invoice-logistics')}<div class="invoice-lines">${table(v.heads,v.rows,'invoice-items')}</div>${v.hidePayments?'':`<div class="invoice-payment">${table(v.paymentHeads,v.payments.length?v.payments:[[v.labels[37],'—','—','—']])}</div>`}<div class="invoice-total"><b>${e(v.currency)}</b>${table([],v.totals)}</div>${v.instructions?`<p class="invoice-instructions">${e(v.instructions)}</p>`:''}${v.extra?.length?`<section class="invoice-extra"><h3>${e(v.extraTitle)}</h3>${table([],v.extra)}</section>`:''}<footer>${e(d.footer)}</footer></article>`;
}

// The browser preview and PDF consume the same read-only invoice presentation model.
export function drawInvoicePDF(pdf,d,{font,rgb,wrap}){
 const v=d.invoice||d.form,W=595.28,H=841.89,M=32,C=W-2*M,black=rgb(.08,.08,.08),gray=rgb(.82,.83,.85),stripe=rgb(.95,.95,.95),pages=[];let page,y;
 const text=(value,x,top,size=8)=>page.drawText(String(value),{x,y:H-top-size,font,size,color:black});
 const lines=(value,width,size=8)=>wrap(String(value),size,width);
 const rect=(x,top,width,height,fill)=>page.drawRectangle({x,y:H-top-height,width,height,borderColor:gray,borderWidth:.5,...(fill?{color:fill}:{})});
 const newPage=()=>{page=pdf.addPage([W,H]);pages.push(page);y=34;if(pages.length>1){text(`${v.labels[0]} ${v.number} / ${d.continued}`,M,y,11);y+=30;}};
 const ensure=height=>{if(y+height>H-70)newPage();};
 const table=(heads,rows,widths,{shaded=true}={})=>{
  const row=(values,isHead=false,index=0,prepared)=>{const content=prepared||values.map((t,i)=>lines(t,widths[i]-10,8)),height=Math.max(1,...content.map(x=>x.length))*11+10;ensure(height);let x=M;
   for(let i=0;i<values.length;i++){rect(x,y,widths[i],height,isHead||shaded&&index%2===0?stripe:undefined);content[i].forEach((line,j)=>text(line,x+5,y+5+j*11));x+=widths[i];}y+=height;
  };
  if(heads.length)row(heads,true);for(let i=0;i<rows.length;i++){
   const content=rows[i].map((t,k)=>lines(t,widths[k]-10)),count=Math.max(...content.map(c=>c.length));let offset=0;
   if(y+Math.min(count*11+10,300)>H-70){newPage();if(heads.length)row(heads,true);}
   while(offset<count){let capacity=Math.floor((H-70-y-10)/11);if(capacity<1){newPage();if(heads.length)row(heads,true);capacity=Math.floor((H-70-y-10)/11);}
    const take=Math.min(capacity,count-offset);row(rows[i],false,i,content.map(c=>c.slice(offset,offset+take)));offset+=take;
    if(offset<count){newPage();if(heads.length)row(heads,true);}
   }
  }y+=10;
 };
 newPage();
 let companyY=y;v.company.forEach((value,i)=>{for(const line of lines(value,250,i===0?16:9)){text(line,M,companyY,i===0?16:9);companyY+=i===0?23:14;}});
 const titleSize=Math.min(24,130/font.widthOfTextAtSize(v.labels[0],1));text(v.labels[0],W-M-font.widthOfTextAtSize(v.labels[0],titleSize),y,titleSize);text(v.status,W-M-font.widthOfTextAtSize(v.status,10),y+32,10);
 y=Math.max(90,companyY+12);y+=drawDocumentCodes(page,v.number,{x:M,top:y,width:C,pageHeight:H,font,rgb,locale:d.locale})+12;table(v.meta.map(x=>x[0]),[v.meta.map(x=>x[1])],[90,95,241,C-426]);
 const addressTop=y,half=(C-18)/2;let maxEnd=y;
 for(let i=0;i<2;i++){const x=M+i*(half+18),addressLines=lines(v.addresses[i][1],half-14,9),contactLines=lines(v.contacts[i].join(': '),half-14,8),height=30+Math.max(2,addressLines.length)*12+contactLines.length*12+10;rect(x,addressTop,half,height);text(v.addresses[i][0],x+7,addressTop+7,10);addressLines.forEach((t,j)=>text(t,x+7,addressTop+28+j*12,9));const contactY=addressTop+30+Math.max(2,addressLines.length)*12;contactLines.forEach((t,j)=>text(t,x+7,contactY+j*12));maxEnd=Math.max(maxEnd,addressTop+height);}
 y=maxEnd+12;text(v.labels[9],M,y,10);y+=14;for(const line of lines(v.notes||'—',C)){ensure(14);text(line,M,y);y+=12;}y+=12;
 table(v.details.map(x=>x[0]),[v.details.map(x=>x[1])],[70,117,65,82,88,C-422]);
 table(v.heads,v.rows,[16,45,68,138,65,61,64,C-457]);
 if(!v.hidePayments)table(v.paymentHeads,v.payments.length?v.payments:[[v.labels[37],'—','—','—']],[105,135,110,C-350]);
 const totalWidth=265,totalX=W-M-totalWidth;ensure(v.totals.length*22+20);text(v.currency,W-M-font.widthOfTextAtSize(v.currency,10),y,10);y+=18;
 for(const [i,[label,value]]of v.totals.entries()){rect(totalX,y,totalWidth,22,i%2===0?stripe:undefined);text(label,totalX+8,y+5,9);text(value,W-M-8-font.widthOfTextAtSize(value,9),y+5,9);y+=22;}
 if(v.instructions?.trim()){y+=16;for(const line of lines(v.instructions,C)){ensure(14);text(line,M,y);y+=12;}}
 if(v.extra?.length){const height=20+v.extra.reduce((sum,row)=>sum+Math.max(lines(row[0],145).length,lines(row[1],C-165).length)*11+10,0);ensure(Math.min(height,H-134));text(v.extraTitle,M,y,10);y+=20;table([],v.extra,[155,C-155]);}
 pages.forEach((p,i)=>{page=p;let top=H-48;for(const line of lines(d.footer,C,7)){text(line,M,top,7);top+=10;}text(`${d.pageWord} ${i+1} / ${pages.length}`,M,H-20,7);});
}
