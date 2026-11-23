import {catalogue} from './locale-catalog.mjs?demo=9c44c6dabb8d4728';
export const interfaceLanguages=[['en','English'],['zh-Hans','简体中文'],['zh-Hant','繁體中文'],['fr','Français']];
const key='chmltech:WMS_demo:harbor-interface-language',codes=new Set(interfaceLanguages.map(x=>x[0]));let current='en';
try{const saved=globalThis.localStorage?.getItem(key);if(codes.has(saved))current=saved;}catch{}
export const interfaceLanguage=()=>current;
const normalized=s=>s.replace(/\s+/g,' ').trim(),folded=new Map(Object.keys(catalogue).map(k=>[k.toLowerCase(),k]));
export function translate(text,locale=current){
 if(typeof text!=='string'||!codes.has(locale))return text;
 if(locale==='en'){if(/[\u3400-\u9fff]/.test(text)&&text.includes(' / '))return text.split(' / ').filter(part=>!/[\u3400-\u9fff]/.test(part)).join(' / ')||text;return text;}
 const clean=normalized(text),colon=/[:：]$/.test(clean),base=colon?clean.slice(0,-1):clean,known=catalogue[base]?base:folded.get(base.toLowerCase());
 if(base.startsWith('› '))return '› '+translate(base.slice(2),locale);
 if(known)return text.replace(text.trim(),catalogue[known][locale]+(colon?(locale.startsWith('zh')?'：':' :'):''));
 // Bilingual system captions retain one chosen interface language. Record data
 // is excluded by the DOM adapter and never passed through this fallback.
 if(/[\u3400-\u9fff]/.test(base)&&base.includes(' / ')){const english=base.split(' / ')[0];if(catalogue[english])return translate(english,locale)+(colon?(locale.startsWith('zh')?'：':' :'):'');}
 const dynamic=[
  [/^Live warehouse records · ([A-Z]{3}) · Vancouver calendar dates$/,m=>locale==='fr'?`Dossiers réels de l’entrepôt · ${m[1]} · Dates du calendrier de Vancouver`:locale==='zh-Hans'?`实际仓库记录 · ${m[1]} · 温哥华日历日期`:`實際倉庫記錄 · ${m[1]} · 溫哥華日曆日期`],
  [/^Sample data: (\d+) demo invoices in (\d{4}) and (\d+) in (\d{4})\. Totals include synthetic records\. Choose the Dashboard Demo warehouse to isolate the examples\. These samples have not been sent to QuickBooks\.$/,m=>locale==='fr'?`Données de démonstration : ${m[1]} factures en ${m[2]} et ${m[3]} en ${m[4]}. Les totaux incluent ces données synthétiques. Sélectionnez l’entrepôt Dashboard Demo pour les isoler. Elles n’ont pas été envoyées à QuickBooks.`:locale==='zh-Hans'?`示例数据：${m[2]} 年 ${m[1]} 张示例发票，${m[4]} 年 ${m[3]} 张。合计包含模拟数据。选择 Dashboard Demo 仓库可单独查看示例。这些示例未发送至 QuickBooks。`:`範例資料：${m[2]} 年 ${m[1]} 張範例發票，${m[4]} 年 ${m[3]} 張。合計包含模擬資料。選擇 Dashboard Demo 倉庫可單獨檢視範例。這些範例未傳送至 QuickBooks。`],
  [/^Historical values use costs and FIFO layer values saved at capture time\. Coverage starts (.+?)\. A snapshot is the last known balance at its recorded time; this is not a reconstruction before coverage or a future forecast\..*$/,m=>locale==='fr'?`Les valeurs historiques utilisent les coûts et les couches FIFO enregistrés. Début : ${m[1]}. Un instantané représente le dernier solde connu à sa date, sans reconstitution antérieure ni prévision. Choisissez « Dernier disponible / date limite » pour appliquer la limite UTC; un instantané sélectionné a priorité.`:locale==='zh-Hans'?`历史估值使用快照保存的成本及 FIFO 成本层。记录起点：${m[1]}。快照表示记录时的已知余额，不重建早期历史，也不作未来预测。选择“最新快照 / 使用截止日期”可使用 UTC 截止时间；指定快照优先。`:`歷史估值使用快照保存的成本及 FIFO 成本層。記錄起點：${m[1]}。快照表示記錄時的已知餘額，不重建早期歷史，也不作未來預測。選擇「最新快照 / 使用截止日期」可使用 UTC 截止時間；指定快照優先。`],
  [/^(Sales orders) (\d+)$/,m=>translate(m[1],locale)+' '+m[2]],
  [/^(Review and issue|Review|Edit|Revise|Confirm|Credit) (.+)$/,m=>translate(m[1],locale)+' '+m[2]],
  [/^Filter: (All|Open|Draft|Closed|Paid|Part paid|Voided)$/,m=>locale==='fr'?'Filtre : '+translate(m[1],locale):locale==='zh-Hans'?'筛选：'+translate(m[1],locale):'篩選：'+translate(m[1],locale)],
  [/^(Returned book value) (.+)$/,m=>({fr:'Valeur comptable retournée','zh-Hans':'退货账面价值','zh-Hant':'退貨帳面價值'}[locale])+' '+m[2]],
  [/^Restocked (\d+) · Scrapped (\d+) · Pending (\d+)$/,m=>locale==='fr'?`Remis en stock ${m[1]} · Rebut ${m[2]} · En attente ${m[3]}`:locale==='zh-Hans'?`重新入库 ${m[1]} · 报废 ${m[2]} · 待处理 ${m[3]}`:`重新入庫 ${m[1]} · 報廢 ${m[2]} · 待處理 ${m[3]}`],
  [/^(\d+) SKUs across (\d+) locations$/,m=>locale==='fr'?`${m[1]} références dans ${m[2]} emplacements`:locale==='zh-Hans'?`${m[1]} 个 SKU，分布于 ${m[2]} 个库位`:`${m[1]} 個 SKU，分布於 ${m[2]} 個庫位`],
  [/^Review (\d+) days; safety (\d+) days$/,m=>locale==='fr'?`Révision tous les ${m[1]} jours; sécurité ${m[2]} jours`:locale==='zh-Hans'?`检查周期 ${m[1]} 天；安全库存 ${m[2]} 天`:`檢查週期 ${m[1]} 天；安全庫存 ${m[2]} 天`],
  [/^(\d+) open orders$/,m=>m[1]+' '+translate('Open orders',locale)],
  [/^(\d+) draft · (\d+) quantity allocated$/,m=>locale==='fr'?`${m[1]} brouillons · ${m[2]} unités affectées`:locale==='zh-Hans'?`${m[1]} 个草稿 · 已分配 ${m[2]} 件`:`${m[1]} 個草稿 · 已分配 ${m[2]} 件`],
  [/^(\d+) packed and awaiting dispatch$/,m=>locale==='fr'?`${m[1]} emballés en attente d’expédition`:locale==='zh-Hans'?`${m[1]} 批已包装待发货`:`${m[1]} 批已包裝待出貨`]
 ];
 for(const [pattern,format]of dynamic){const m=clean.match(pattern);if(m)return format(m);}
 return text;
}
// The bundled CJK font has full-width curly quote forms. French document labels
// use a Latin apostrophe; original business text is never normalized here.
export function translatedWords(words,locale){return Object.fromEntries(Object.entries(words).map(([key,value])=>{const text=translate(value,locale);return [key,locale==='fr'?text.replaceAll('’',"'"):text];}));}
export function setInterfaceLanguage(code){if(!codes.has(code))throw Error('Unsupported interface language.');current=code;try{globalThis.localStorage?.setItem(key,code);}catch{}return code;}
export const languageControlHTML=({id='interface-language'}={})=>`<label class="language-switch"><span>Language</span><select id="${id}" data-interface-language aria-label="Interface language">${interfaceLanguages.map(([code,label])=>`<option value="${code}"${code===current?' selected':''}>${label}</option>`).join('')}</select></label>`;
// No business state is changed or serialized by localization. This conservative
// allowlist protects entered names, descriptions, references and notes even when
// they happen to equal a system caption such as "Open" or "Supplier".
export function protectedRecordText(state){
 const out=new Set(),fields=new Set(['label','name','description','englishName','address','contact','email','phone','supplier','customer','category','note','notes','reason','reference','sku','code','lot','number','paymentInstructions','paymentTerms','line1','line2','city','region','postal','country','value']);
 const seen=new WeakSet();function visit(x,depth=0){if(!x||typeof x!=='object'||seen.has(x)||depth>18)return;seen.add(x);for(const [key,value]of Object.entries(x)){if(typeof value==='string'&&fields.has(key)&&value.trim())out.add(normalized(value));else if(value&&typeof value==='object')visit(value,depth+1);}}
 visit(state);return out;
}
export const isRecordOptionText=(source,protectedText)=>[...protectedText].some(value=>value.length>=2&&normalized(source).includes(value));
export function startLocalization(getState){
 const doc=globalThis.document;if(!doc)return;const sources=new WeakMap(),attrs=new WeakMap();let pending=false;
 const skip='script,style,svg,textarea,[data-l10n-skip],.business-document';
 function apply(){
  pending=false;const protectedText=protectedRecordText(getState()),lang=interfaceLanguage();if(doc.documentElement.lang!==lang)doc.documentElement.lang=lang;
  const walker=doc.createTreeWalker(doc.body,4);let node;
  while((node=walker.nextNode())){if(node.parentElement?.closest(skip)||!node.data.trim())continue;const prior=sources.get(node),source=prior&&node.data===prior.last?prior.source:node.data;
   const value=protectedText.has(normalized(source))||(node.parentElement?.closest('option')&&isRecordOptionText(source,protectedText))?source:normalized(source)==='Open'&&node.parentElement?.closest('button')&&lang!=='en'?translate('Open record',lang):translate(source,lang);sources.set(node,{source,last:value});if(node.data!==value)node.data=value;
  }
  for(const el of doc.body.querySelectorAll('[aria-label],[placeholder],[title]')){
   if(el.closest(skip))continue;let memory=attrs.get(el);if(!memory){memory={};attrs.set(el,memory);}
   for(const attr of ['aria-label','placeholder','title']){if(!el.hasAttribute(attr))continue;const value=el.getAttribute(attr),old=memory[attr],source=old&&value===old.last?old.source:value,next=protectedText.has(normalized(source))?source:translate(source,lang);memory[attr]={source,last:next};if(value!==next)el.setAttribute(attr,next);}
  }
  for(const select of doc.querySelectorAll('#interface-language,[data-interface-language]'))if(select.value!==lang)select.value=lang;
 }
 const queue=()=>{if(!pending){pending=true;queueMicrotask(apply);}};
 const observer=new MutationObserver(queue);observer.observe(doc.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['aria-label','placeholder','title']});
 doc.addEventListener('change',event=>{if(event.target.id==='interface-language'||event.target.hasAttribute('data-interface-language')){setInterfaceLanguage(event.target.value);apply();doc.dispatchEvent(new CustomEvent('harbor-language-changed',{detail:current}));}});
 globalThis.addEventListener?.('storage',event=>{if(event.key===key&&codes.has(event.newValue)){current=event.newValue;apply();}});
 apply();return {apply,disconnect:()=>observer.disconnect()};
}
