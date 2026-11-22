// Pinned local decoder; images and camera frames never leave the device.
import './vendor/zxing.min.js';
const Z=globalThis.ZXing;
export function decodePixels(pixels,width,height,{rotate=true}={}){
 if(!Number.isInteger(width)||!Number.isInteger(height)||width<10||height<10||width*height>16_000_000||pixels.length!==width*height*4)throw Error('Use an image smaller than 16 megapixels.');
 let gray=new Uint8ClampedArray(width*height);for(let i=0;i<gray.length;i++)gray[i]=pixels[i*4+3]<128?255:(pixels[i*4]+pixels[i*4+1]*2+pixels[i*4+2])/4;
 const hints=new Map([[Z.DecodeHintType.POSSIBLE_FORMATS,[Z.BarcodeFormat.CODE_39,Z.BarcodeFormat.QR_CODE,Z.BarcodeFormat.CODE_128,Z.BarcodeFormat.EAN_13,Z.BarcodeFormat.EAN_8,Z.BarcodeFormat.UPC_A]],[Z.DecodeHintType.TRY_HARDER,true]]);
 for(let turn=0;turn<(rotate?4:1);turn++){for(const reader of [new Z.QRCodeReader(),new Z.MultiFormatOneDReader(hints)]){try{const result=reader.decode(new Z.BinaryBitmap(new Z.HybridBinarizer(new Z.RGBLuminanceSource(gray,width,height))),hints);return {text:result.getText(),format:Z.BarcodeFormat[result.getBarcodeFormat()]};}catch{}finally{reader.reset();}}const next=new Uint8ClampedArray(gray.length);for(let y=0;y<height;y++)for(let x=0;x<width;x++)next[x*height+height-y-1]=gray[y*width+x];gray=next;[width,height]=[height,width];}
 throw Error('No readable barcode found. Move closer, improve lighting or choose a sharper photo.');
}

