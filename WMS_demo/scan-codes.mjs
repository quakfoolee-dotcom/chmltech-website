import qrcode from './vendor/qrcode.mjs?demo=45f52980507d3a1b';
import {barcodeSVG} from './barcode.mjs?demo=45f52980507d3a1b';
import {documentQRValue,getPhoneAddress} from './document-scan.mjs?demo=45f52980507d3a1b';
import {translate} from './locale.mjs?demo=45f52980507d3a1b';
// QR byte mode must preserve Chinese and French characters. ASCII document links are unchanged.
qrcode.stringToBytes=value=>Array.from(new TextEncoder().encode(value));
const e=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function qrMatrix(value){const qr=qrcode(0,'M');qr.addData(value,'Byte');qr.make();return Array.from({length:qr.getModuleCount()},(_,y)=>Array.from({length:qr.getModuleCount()},(_,x)=>qr.isDark(y,x)));}
export function qrSVG(value,label='QR'){const matrix=qrMatrix(value),n=matrix.length+8;let path='';for(let y=0;y<matrix.length;y++)for(let x=0;x<matrix.length;x++)if(matrix[y][x])path+=`M${x+4},${y+4}h1v1h-1z`;return `<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 ${n} ${n}" role="img" aria-label="${e(label)}" shape-rendering="crispEdges"><rect width="${n}" height="${n}" fill="white"/><path d="${path}" fill="black"/></svg>`;}
export function documentScanHTML(number,locale='en'){
 const bars=barcodeSVG(number).replace('<svg ','<svg preserveAspectRatio="none" ').replace(/viewBox="0 0 ([\d.]+) 125"/,'viewBox="0 0 $1 90"').replace(/<g fill="black" text-anchor="middle"[\s\S]*?<\/g>/,'');
 return `<div class="document-scan-codes" data-l10n-skip><div class="document-linear">${bars}<small>${e(number)}</small></div><div class="document-qr">${qrSVG(documentQRValue(number),number+' QR')}<small>${e(translate(getPhoneAddress()?'Open on phone':'Scan in Chmltech WMS',locale))}</small></div></div>`;
}
export function drawDocumentCodes(page,number,{x,top,width,height=94,pageHeight,font,rgb,locale='en'}){
 const black=rgb(0,0,0),svg=barcodeSVG(number),full=Number(svg.match(/viewBox="0 0 ([\d.]+)/)[1]),qrSize=82,barWidth=Math.min(280,width-qrSize-30),scale=barWidth/full;
 for(const match of svg.matchAll(/<rect x="([\d.]+)" y="12" width="([\d.]+)" height="65"/g))page.drawRectangle({x:x+Number(match[1])*scale,y:pageHeight-top-50,width:Number(match[2])*scale,height:42,color:black});
 page.drawText(number,{x:x+(barWidth-font.widthOfTextAtSize(number,10))/2,y:pageHeight-top-65,size:10,font,color:black});
 const matrix=qrMatrix(documentQRValue(number)),n=matrix.length+8,module=qrSize/n,qx=x+width-qrSize;
 for(let y=0;y<matrix.length;y++)for(let xx=0;xx<matrix.length;xx++)if(matrix[y][xx])page.drawRectangle({x:qx+(xx+4)*module,y:pageHeight-top-(y+5)*module,width:module,height:module,color:black});
 const label=translate(getPhoneAddress()?'Open on phone':'Scan in Chmltech WMS',locale);page.drawText(label,{x:qx+(qrSize-font.widthOfTextAtSize(label,7))/2,y:pageHeight-top-qrSize-10,size:7,font,color:black});return height;
}
