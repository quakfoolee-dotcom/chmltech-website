import {drawDocumentCodes} from './scan-codes.mjs?demo=45f52980507d3a1b';
import {drawInvoicePDF} from './invoice-layout.mjs?demo=45f52980507d3a1b';
// One renderer shared by the browser download and the automated PDF checks.
export async function createDocumentPDF(documents,{PDFLib,fontkit,fontBytes}){
 const {PDFDocument,rgb}=PDFLib,pdf=await PDFDocument.create();pdf.registerFontkit(fontkit);
 // Full static TrueType embedding avoids CJK subset incompatibilities in PDF readers.
 const font=await pdf.embedFont(fontBytes,{subset:false}),supported=new Set(font.getCharacterSet());
 const strings=value=>typeof value==='string'?[value]:value&&typeof value==='object'?Object.values(value).flatMap(strings):[];
 const all=documents.flatMap(d=>[d.title,d.ref,d.footer,d.pageWord,d.continued,...d.blocks.flatMap(b=>[b.label||'',b.text]),...strings(d.invoice||d.form)]).join('');
 const missing=[...new Set(Array.from(all).filter(c=>!/[\r\n\t]/.test(c)&&!supported.has(c.codePointAt(0))))];
 if(missing.length)throw Error('PDF font does not contain these characters: '+missing.join(' ')+' — edit the text or choose another font-supported character.');
 pdf.setTitle(documents.map(d=>`${d.title} ${d.ref}`).join(' / '));pdf.setAuthor('Chmltech WMS');pdf.setSubject('Local warehouse document');
 const ink=rgb(.10,.20,.20),muted=rgb(.36,.42,.42),green=rgb(.08,.25,.23),rule=rgb(.78,.83,.81);
 const wrap=(text,size,width)=>wrapDocumentText(text,width,value=>font.widthOfTextAtSize(value,size));
 for(const d of documents){
  if(d.invoice||d.form){drawInvoicePDF(pdf,d,{font,rgb,wrap});continue;}
  const small=d.size==='label',compact=d.density==='compact',w=small?288:595.28,h=small?432:841.89,margin=small?18:42,size=small?9:compact?10:11,leading=size*(compact?1.45:1.55),gap=small?4:compact?6:9,width=w-margin*2;
  const footerLines=wrap(d.footer,small?7:8,width),bottom=margin+footerLines.length*11+22;
  const pages=[];let page,y;
  const draw=(text,x,yy,sz=size,color=ink)=>page.drawText(text,{x,y:yy,size:sz,font,color});
  const newPage=()=>{page=pdf.addPage([w,h]);pages.push(page);page.drawRectangle({x:0,y:h-(small?53:75),width:w,height:small?53:75,color:green});draw('HARBOR',margin,h-(small?20:28),small?10:13,rgb(1,1,1));draw(d.title+(pages.length>1?' / '+d.continued:''),margin,h-(small?40:53),small?13:19,rgb(1,1,1));y=h-(small?74:105);for(const line of wrap(d.ref,small?10:13,width)){draw(line,margin,y,small?10:13);y-=leading;}y-=small?9:20;if(pages.length===1&&d.scanCode){y-=drawDocumentCodes(page,d.scanCode,{x:margin,top:h-y,width,pageHeight:h,font,rgb,locale:d.locale})+12;}};
  const line=(text,sz=size,color=ink)=>{if(y<bottom+leading)newPage();draw(text,margin,y,sz,color);y-=leading;};
  newPage();
  for(const [index,b] of d.blocks.entries()){
   const lines=wrap(b.kind==='item'?b.text:`${b.label}: ${b.text}`,size,width);
   // Keep a purchase line's description and balances together when they fit
   // on one page; very long descriptions may still continue onto another page.
   if(b.kind==='item'&&b.group){
    let height=5;
    for(let j=index;j<d.blocks.length&&d.blocks[j].group===b.group;j++){
     const part=d.blocks[j];height+=wrap(part.kind==='item'?part.text:`${part.label}: ${part.text}`,size,width).length*leading+gap;
    }
    const pageTop=h-(small?74:105)-wrap(d.ref,small?10:13,width).length*leading-(small?9:20);
    if(height<=pageTop-bottom-leading&&y<bottom+height+leading)newPage();
   }
   if(y<bottom+(b.kind==='item'?4:Math.min(lines.length,3))*leading+14)newPage();
   if(b.kind==='item'){y-=5;page.drawLine({start:{x:margin,y:y+size+4},end:{x:w-margin,y:y+size+4},thickness:.7,color:rule});}
   for(const text of lines)line(text,size,b.kind==='item'?green:ink);
   y-=gap;
  }
  pages.forEach((p,index)=>{page=p;let fy=margin+footerLines.length*11+7;page.drawLine({start:{x:margin,y:fy+12},end:{x:w-margin,y:fy+12},thickness:.5,color:rule});for(const text of footerLines){draw(text,margin,fy,small?7:8,muted);fy-=11;}draw(`${d.pageWord} ${index+1} / ${pages.length}`,margin,margin-1,small?7:8,muted);});
 }
 return pdf.save();
}

// Keep ordinary words together while retaining Unicode-safe wrapping for
// Chinese text, long SKUs and serial numbers that exceed the page width.
export function wrapDocumentText(text,width,measure){
 const segmenter=new Intl.Segmenter('en',{granularity:'word'}),lines=[];
 for(const paragraph of String(text).replaceAll('\t','    ').split(/\r?\n/)){
  let line='';
  for(const {segment} of segmenter.segment(paragraph)){
   if(!segment.trim()){if(line)line+=segment;continue;}
   if(line&&measure(line+segment)>width){lines.push(line.trimEnd());line='';}
   for(const ch of segment){if(line&&measure(line+ch)>width){lines.push(line.trimEnd());line='';}line+=ch;}
  }
  lines.push(line.trimEnd());
 }
 return lines;
}
