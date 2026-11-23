import {interfaceLanguage} from './locale.mjs?demo=9c44c6dabb8d4728';
import {languages,buildDocuments,documentHTML} from './documents.mjs?demo=9c44c6dabb8d4728';
import {createDocumentPDF} from './pdf.mjs?demo=9c44c6dabb8d4728';
let language='en',active=null;const fontCache=new Map();
try{const saved=localStorage.getItem('chmltech:WMS_demo:harbor-document-language');if(languages.some(([id])=>id===saved))language=saved;}catch{}
export async function documentAction(name,id,el,{s,showModal,select,download}){
 const selector=()=>select('Document language / 文档语言 / 文件語言','documentLanguage',languages,language);
 const preview=()=>showModal('Document preview / 单据预览 / 單據預覽',`<div class="document-controls">${selector()}<button type="button" class="btn" data-action="document-refresh">Apply language</button><button type="button" class="btn primary" data-action="document-pdf">Download PDF</button><button type="button" class="btn" data-action="document-print">Print preview</button><p>PDF embeds Chinese fonts. Warehouse labels are 4 × 6 inches; purchase orders and packing slips are A4. Long content continues on another page.</p></div>${documentHTML(buildDocuments(s,active.kind,active.id,language))}`);
 const choose=()=>{language=document.querySelector('[name="documentLanguage"]').value;try{localStorage.setItem('chmltech:WMS_demo:harbor-document-language',language);}catch{}};
 if(name==='document-settings'){language=interfaceLanguage();showModal('Document language / 中文单据',`${selector()}<p>This setting controls document headings and Chinese font forms. Your original supplier and product text is preserved. Choose the interface language at the top of the page. Choose a document from Purchases or Shipping.</p>`,'Save',()=>{choose();document.querySelector('#modal').close();});return true;}
 if(['forecast-document','purchase-document','packing-slip','label'].includes(name)){language=interfaceLanguage();active={kind:{'forecast-document':'forecast','purchase-document':'purchase','packing-slip':'packing',label:'label'}[name],id};preview();return true;}
 if(name==='document-refresh'){choose();preview();return true;}
 if(name==='document-pdf'){
  choose();const request={...active,language},docs=buildDocuments(s,request.kind,request.id,request.language);el.disabled=true;const label=el.textContent;el.textContent='Preparing PDF…';
  try{const variant=request.language==='zh-Hant'?'TC':'SC';if(!fontCache.has(variant)){const response=await fetch(`./fonts/NotoSans${variant}-Regular.ttf?v=1.3.1`);if(!response.ok)throw Error('Chinese font could not load. Refresh this page and try again.');fontCache.set(variant,new Uint8Array(await response.arrayBuffer()));}
   if(!globalThis.PDFLib||!globalThis.fontkit)throw Error('PDF libraries are not ready. Refresh Chmltech WMS and try again.');
   const bytes=await createDocumentPDF(docs,{PDFLib:globalThis.PDFLib,fontkit:globalThis.fontkit,fontBytes:fontCache.get(variant)});
   download(`Chmltech-WMS-${request.kind}-${request.kind==='forecast'?'report':request.id}-${request.language}.pdf`,bytes,'application/pdf');
  }finally{el.disabled=false;el.textContent=label;}return true;
 }
 if(name==='document-print'){
  choose();preview();const articles=[...document.querySelectorAll('.business-document')];
  for(const article of articles){const family=article.lang==='zh-Hant'?'HarborTC':'HarborSC',text=article.textContent;const fonts=await document.fonts.load(`400 14px ${family}`,text);if(!fonts.length&&/[\u3400-\u9fff\uf900-\ufaff]/.test(text))throw Error('Chinese print font could not load. Refresh this page and try again.');}
  await document.fonts.ready;window.print();return true;
 }
 return false;
}
