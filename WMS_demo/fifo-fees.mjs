// Additive landed-fee overlays on exact FIFO origin unit-index ranges.
// This module is independent of fifo.mjs to avoid changing purchase-origin costs.
export function rangeTransferFees(origin,start,qty,beforeOrdinal=Infinity){
 if(!Number.isSafeInteger(start)||!Number.isSafeInteger(qty)||start<0||qty<0||start+qty>origin.qty)throw Error('Invalid FIFO fee range.');
 let value=0;for(const fee of origin.transferFees||[]){if(fee.ordinal>=beforeOrdinal)continue;const a=Math.max(start,fee.start),b=Math.min(start+qty,fee.start+fee.qty);if(b<=a)continue;
  value+=Number(BigInt(fee.amount)*BigInt(b-fee.start)/BigInt(fee.qty)-BigInt(fee.amount)*BigInt(a-fee.start)/BigInt(fee.qty));
 }return value;
}
export function validateTransferFees(origin){
 const ids=new Set();for(const f of origin.transferFees||[]){if(!f||typeof f.id!=='string'||ids.has(f.id)||!Number.isSafeInteger(f.ordinal)||f.ordinal<=0||!Number.isFinite(Date.parse(f.time))||!Number.isSafeInteger(f.start)||f.start<0||!Number.isSafeInteger(f.qty)||f.qty<=0||f.start+f.qty>origin.qty||!Number.isSafeInteger(f.amount)||f.amount<0||!f.billId||!f.allocationId||!f.transferId)throw Error('Invalid FIFO transfer fee overlay.');ids.add(f.id);}
}

