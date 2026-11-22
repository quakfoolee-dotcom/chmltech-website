// Preserve the script entered by the user; normalize only for searching.
export const charLength=value=>Array.from(value).length;
export const cutText=(value,max)=>Array.from(String(value??'')).slice(0,max).join('');
export const validUnicode=value=>!/[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]/u.test(value);
export const searchText=value=>String(value??'').normalize('NFKC').toLocaleLowerCase('en');
export const matchesText=(value,query)=>searchText(value).includes(searchText(query));
export function decodeUTF8(bytes){
  try{return new TextDecoder('utf-8',{fatal:true}).decode(bytes).replace(/^\uFEFF/,'');}
  catch{throw Error('This file is not valid UTF-8. In Excel, save it as CSV UTF-8, then try again. GBK, Big5 and UTF-16 files must be converted first.');}
}
export function createSearchHandler(update){
  let composing=false;
  return {start(){composing=true;},end(target){composing=false;update(target);},input(event){if(!composing&&!event.isComposing)update(event.target);}};
}

