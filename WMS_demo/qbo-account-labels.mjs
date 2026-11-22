// Display aliases only. Never use these labels as account identifiers or write
// them back to QuickBooks. Unrecognized/custom names remain exactly as entered.
const labels=new Map([
 ['Harbor Demo Production WIP',{'zh-Hans':'Harbor 示例生产在制品','zh-Hant':'Harbor 範例生產在製品',fr:'Production en cours de démonstration Harbor'}],
 ['Inventory Asset',{'zh-Hans':'库存资产','zh-Hant':'庫存資產',fr:'Actif des stocks'}],
 ['Prepaid expenses',{'zh-Hans':'预付费用','zh-Hant':'預付費用',fr:'Charges payées d’avance'}],
 ['Uncategorised Asset',{'zh-Hans':'未分类资产','zh-Hant':'未分類資產',fr:'Actif non catégorisé'}],
 ['Uncategorized Asset',{'zh-Hans':'未分类资产','zh-Hant':'未分類資產',fr:'Actif non catégorisé'}],
 ['Undeposited Funds',{'zh-Hans':'未存入银行款项','zh-Hant':'未存入銀行款項',fr:'Fonds non déposés'}]
]);
export function quickBooksAccountDisplayName(name,language='en'){
 const original=String(name??''),caption=labels.get(original)?.[language];
 if(!caption||caption===original)return original;
 return language.startsWith('zh')?`${caption}（${original}）`:`${caption} (${original})`;
}

