// Monetary totals have two decimals; editable unit prices retain four-decimal
// precision. Formatting never writes rounded values back into the ledger.
export const formatMoney=(value,currency='CAD')=>`${currency} ${Number(value??0).toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
export const formatUnitCost=(value,currency='CAD')=>`${currency} ${Number(value??0).toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:4})}`;

