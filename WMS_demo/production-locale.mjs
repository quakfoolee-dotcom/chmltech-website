import {interfaceLanguage,translate} from './locale.mjs?demo=9c44c6dabb8d4728';
import {catalogue} from './locale-catalog.mjs?demo=9c44c6dabb8d4728';
const escape=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
// Only recognized demo copy and standard stage names have reviewed translations.
// Custom work instructions and entered notes remain exactly as saved.
const originals=[
 ['Assembly','装配 / 組裝'],['Inspection','检验 / 檢驗'],['Packaging','包装 / 包裝'],
 ['Check components and assemble to the work instructions.','核对组件，按说明装配。核對組件，依說明組裝。'],
 ['Check quantity and appearance.','检查数量和外观。檢查數量及外觀。'],
 ['Confirm the lot and pack the output.','确认批次并包装。確認批號後包裝。'],
 ['Demo checks passed','Demo checks passed / 示例检查通过 / 範例檢查通過'],
 ['Verified demo minutes and costing rate','Verified demo minutes and costing rate / 已核对工时和费率 / 已確認工時及費率']
];
const aliases=new Map();for(const [key,original]of originals)for(const value of [key,original,...Object.values(catalogue[key]||{})])aliases.set(value,key);
export const productionCopyKey=value=>aliases.get(String(value??''));
export const productionCopy=(value,locale=interfaceLanguage())=>{const key=productionCopyKey(value);return key?translate(key,locale):String(value??'');};
export const productionCopyHTML=value=>{const key=productionCopyKey(value);return `<span data-l10n-skip${key?' data-production-copy="'+escape(key)+'"':''}>${escape(productionCopy(value))}</span>`;};
export const productionCopyValueAttribute=value=>{const key=productionCopyKey(value);return key?'data-production-copy-value="'+escape(key)+'"':'';};
export function refreshProductionCopy(doc=globalThis.document){if(!doc)return;for(const el of doc.querySelectorAll('[data-production-copy]')){const key=el.dataset.productionCopy;if(!originals.some(x=>x[0]===key))continue;const next=translate(key);if(el.textContent!==next)el.textContent=next;}for(const el of doc.querySelectorAll('input[readonly][data-production-copy-value]')){const key=el.dataset.productionCopyValue;if(originals.some(x=>x[0]===key))el.value=translate(key);}}
if(globalThis.document)document.addEventListener('harbor-language-changed',()=>refreshProductionCopy());
