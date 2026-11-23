import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {createBrowserWorkspace,STORAGE_KEY} from '../WMS_demo/browser-store.mjs';import {productUnits} from '../WMS_demo/packaging.mjs';
const seed=JSON.parse(fs.readFileSync('WMS_demo/sample-workspace.json','utf8')); 
const storage=()=>{const rows=new Map();return {rows,getItem:k=>rows.get(k)??null,setItem:(k,v)=>rows.set(k,v)};};
const open=s=>createBrowserWorkspace({storage:s,seed,locks:null});
async function run(w,command,payload){return w.command({command,payload,revision:(await w.read()).revision});}
test('browser workflow receives cartons, edits units, ships packs and persists across reloads',async()=>{
 const s=storage(),w=open(s);let state=await w.start(),bottle=state.items.find(i=>i.sku==='HBR-UOM-BOTTLE');
 assert.ok(!/\p{Script=Han}/u.test(JSON.stringify(state)));const pack=productUnits(state,bottle.id).find(u=>u.code==='PACK3');await run(w,'units:save',{...pack,itemId:bottle.id,name:'Visitor pack of 3'});
 const po=state.operations.purchases.find(p=>p.status==='Open'&&p.lines.some(l=>l.itemId===bottle.id));await run(w,'receivePurchase',{id:po.id,reference:'Browser test',lines:[{lineId:'line-1',qty:24,locationId:'location-1',lot:'BROWSER'}]});
 const order=state.orders.find(o=>o.status==='Draft'&&o.lines.some(l=>l.itemId===bottle.id));const pick=(await run(w,'issueOrder',{id:order.id})).resultId;await run(w,'commitPick',{id:pick});const shipment=(await run(w,'finishPick',{id:pick})).resultId;await run(w,'packShipment',{id:shipment});await run(w,'shipShipment',{id:shipment});
 state=await open(s).start();assert.equal(state.stock.filter(r=>r.itemId===bottle.id).reduce((sum,r)=>sum+r.qty,0),66);assert.equal(productUnits(state,bottle.id).find(u=>u.code==='PACK3').name,'Visitor pack of 3');
});
test('independent browsers stay isolated and reset touches only the WMS warehouse',async()=>{
 const s=storage();s.setItem('another-app','keep');s.setItem('chmltech:WMS_demo:harbor-wms-view','harbor');const a=open(s),b=open(storage());await a.start();await b.start();const before=(await a.read()).revision;
 await run(a,'createItem',{sku:'BROWSER-ONLY',name:'Visitor item',uom:'ea',reorderPoint:0});assert.ok(!(await b.read()).items.some(i=>i.sku==='BROWSER-ONLY'));const reset=await a.reset();assert.ok(reset.revision>before);assert.ok(!reset.items.some(i=>i.sku==='BROWSER-ONLY'));assert.equal(s.getItem('another-app'),'keep');assert.equal(s.getItem('chmltech:WMS_demo:harbor-wms-view'),'harbor');
});
test('another tab cannot overwrite a newer change or replay a pre-reset command',async()=>{
 const s=storage(),a=open(s),b=open(s);const old=await a.start();await b.start();await run(b,'createItem',{sku:'TAB-B',name:'Other tab',uom:'ea',reorderPoint:0});
 const stale={command:'createItem',payload:{sku:'STALE',name:'Stale',uom:'ea',reorderPoint:0},revision:old.revision};await assert.rejects(a.command(stale),e=>e.status===409);await a.reset();await assert.rejects(b.command(stale),e=>e.status===409);assert.ok(!(await a.read()).items.some(i=>i.sku==='STALE'));
});
test('invalid changes and quota failures never replace saved data; corrupt data can be explicitly reset',async()=>{
 const s=storage(),w=open(s);await w.start();const raw=s.getItem(STORAGE_KEY);await assert.rejects(run(w,'createItem',{sku:'',name:''}));assert.equal(s.getItem(STORAGE_KEY),raw);
 const set=s.setItem;s.setItem=()=>{throw Error('Quota');};await assert.rejects(run(w,'createItem',{sku:'NO-SPACE',name:'No space',uom:'ea',reorderPoint:0}),e=>e.status===507);assert.equal(s.getItem(STORAGE_KEY),raw);s.setItem=set;
 s.setItem(STORAGE_KEY,'broken');await assert.rejects(open(s).start(),/Reset demo/);await open(s).reset();assert.ok((await open(s).start()).items.length>=17);
});
test('blocked storage is explicitly temporary and live integrations remain disconnected',async()=>{
 const w=open({getItem(){throw Error('Blocked');}});await w.start();assert.equal(w.storageMode,'memory');await run(w,'createItem',{sku:'MEMORY',name:'Temporary',uom:'ea',reorderPoint:0});assert.ok((await w.read()).items.some(i=>i.sku==='MEMORY'));
 for(const command of ['qbo:send','replace','loadChineseDemo','users'])await assert.rejects(run(w,command,{}),e=>e.status===403);
});

test('the complete static import graph and nested-path pages contain no private or missing assets',()=>{
 const root='WMS_demo/',files=fs.readdirSync(root);assert.ok(fs.existsSync('.nojekyll'));
 for(const file of files.filter(p=>/\.(mjs|html)$/.test(p))){
  const source=fs.readFileSync(root+file,'utf8');assert.ok(!/(?:href|src)="\//.test(source),file);
  for(const match of source.matchAll(/(?:from\s*|import\s*\()(['"])(\.\/[^'"]+)\1/g))assert.ok(fs.existsSync(root+match[2].split(/[?#]/)[0]),file+' imports '+match[2]);
 }
 for(const file of ['index.html','mobile.html','scan.html','warehouse-labels.html','fonts/NotoSansSC-Regular.ttf','fonts/NotoSansTC-Regular.ttf','vendor/pdf-lib.min.js'])assert.ok(fs.existsSync(root+file),file);
 for(const file of ['.env','api','data','node_modules','service.mjs'])assert.equal(fs.existsSync(root+file),false);
 assert.ok(!fs.readFileSync(root+'shared.mjs','utf8').includes('/demo-api/'));
});

test('demo assets contain no legacy commercial product name and Classic layout uses neutral identifiers',()=>{
 const hits=[];const walk=dir=>{for(const row of fs.readdirSync(dir,{withFileTypes:true})){const file=dir+'/'+row.name;if(row.isDirectory())walk(file);else if(/fishbowl/i.test(fs.readFileSync(file).toString('latin1')))hits.push(file);}};walk('WMS_demo');assert.deepEqual(hits,[]);
 assert.ok(fs.readFileSync('WMS_demo/app.mjs','utf8').includes("let viewMode='classic'"));
 for(const file of ['classic.css','navigation.css','guest-theme.css'])assert.ok(fs.readFileSync('WMS_demo/'+file,'utf8').includes('data-view="classic"'),file);
});

// V5.73 public launch: analytics, search visibility, redirect and links to the showcase page.
test('demo pages carry Clarity with the notrack opt-out and stay out of search',()=>{
 const index=fs.readFileSync('WMS_demo/index.html','utf8');
 assert.ok(index.includes('"clarity","script"')&&index.includes('chm_notrack')&&index.includes('notrack'),'Clarity loader with opt-out');
 for(const file of ['mobile.html','scan.html'])assert.ok(fs.readFileSync('WMS_demo/'+file,'utf8').includes('"clarity","script"'),file);
 for(const file of fs.readdirSync('WMS_demo').filter(f=>f.endsWith('.html')))assert.match(fs.readFileSync('WMS_demo/'+file,'utf8'),/<meta name="robots" content="noindex/,file);
 const sitemap=fs.readFileSync('sitemap.xml','utf8');assert.ok(!/WMS_demo|wms_demo/.test(sitemap));assert.ok(sitemap.includes('<loc>https://www.chmltech.com/wms-demo</loc>'));
 assert.ok(!fs.readFileSync('WMS_demo/chinese.css','utf8').match(/(?:^|[}\s])body,input,button,textarea,select\{font-family:[^}]*HarborSC/),'no web font in the global interface rule');
});
test('lowercase /wms_demo/ forwards to /WMS_demo/ with the query and #module, without a second folder',()=>{
 const s=fs.readFileSync('404.html','utf8');assert.ok(s.includes('data-wms-demo-redirect'));
 assert.ok(s.includes('location.replace("/WMS_demo"+(m[1]||"/")+location.search+location.hash)'));
 assert.deepEqual(fs.readdirSync('.').filter(f=>/^wms_demo$/i.test(f)),['WMS_demo'],'only one demo folder (case-insensitive file systems)');
});
test('showcase page is indexable and linked from Solutions, Distribution & Warehousing and Part 7 (pages and generators)',()=>{
 const page=fs.readFileSync('wms-demo.html','utf8');assert.ok(!page.includes('Nothing is sent'));assert.ok(page.includes('Microsoft Clarity'));assert.ok(!/name="robots" content="noindex/.test(page));assert.ok(page.includes('href="WMS_demo/"'));assert.ok(page.includes('rel="canonical" href="https://www.chmltech.com/wms-demo"'));
 for(const file of ['solutions.html','distribution-and-warehousing.html','post/do-we-need-a-wms-yet-when-spreadsheets-stop-scaling.html']){const s=fs.readFileSync(file,'utf8');assert.ok(s.includes('data-wms-demo="1"'),file);assert.ok(/href="(\.\.\/)?wms-demo(\.html)?"/.test(s),file);}
 assert.ok(fs.readFileSync('content/gen/build_v3.py','utf8').includes('wms_demo_links.add_to_solutions(sol)'));
 assert.ok(fs.readFileSync('content/gen/industry_pages.py','utf8').includes('wms_demo_links.add_to_industry(b)'));
 assert.equal(JSON.parse(fs.readFileSync('content/industries/distribution-and-warehousing.json','utf8')).wms_demo,true);
 assert.ok(fs.readFileSync('content/articles/wh7_articles.py','utf8').includes('{WMS_DEMO}<h2>Key points</h2>'));
 assert.ok(JSON.parse(fs.readFileSync('content/articles/do-we-need-a-wms-yet-when-spreadsheets-stop-scaling.json','utf8')).body.includes('data-wms-demo="1"'));
});

// V5.76: Clarity runs only on chmltech.com, so local previews and test servers send nothing.
test('every Clarity loader is the host-checked version',()=>{
 const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.isDirectory()?(['.git','node_modules','content','assets'].includes(e.name)?[]:walk(d+'/'+e.name)):e.name.endsWith('.html')?[d+'/'+e.name]:[]);
 const pages=walk('.').filter(f=>fs.readFileSync(f,'utf8').includes('"clarity","script"'));
 assert.ok(pages.length>300,'Clarity pages found: '+pages.length);
 for(const f of pages)assert.ok(fs.readFileSync(f,'utf8').includes('if(!/(^|\\.)chmltech\\.com$/.test(l.location.hostname))return;'),f);
});
