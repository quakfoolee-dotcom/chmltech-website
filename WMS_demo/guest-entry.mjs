import {startGuest,resetGuest,storageMode} from './shared.mjs?demo=5d9e5d1ce6c83eb1';
const banner=document.createElement('aside');banner.className='guest-demo-bar';banner.setAttribute('aria-label','Demo controls');
banner.innerHTML='<strong>Harbor WMS · Browser demo</strong><span id="demo-storage">Fictional sample records · Saved in this browser only</span><button id="demo-reset" type="button">Reset demo</button><a href="../">Back to Chmltech</a><span id="demo-message" role="status"></span>';
document.body.prepend(banner);
new ResizeObserver(()=>document.documentElement.style.setProperty('--guest-bar-height',banner.getBoundingClientRect().height+'px')).observe(banner);
const button=document.querySelector('#demo-reset'),message=document.querySelector('#demo-message');
const dialog=document.createElement('dialog');dialog.innerHTML='<h2>Reset this WMS demo?</h2><p>This replaces the WMS sample warehouse saved in this browser. Your other website apps and other visitors are unaffected.</p><form method="dialog"><button value="cancel">Keep exploring</button><button value="reset">Reset warehouse</button></form>';document.body.append(dialog);
button.onclick=()=>dialog.showModal();dialog.onclose=async()=>{if(dialog.returnValue!=='reset')return;button.disabled=true;try{await resetGuest();location.hash='overview';location.reload();}catch(e){message.textContent=e.message;button.disabled=false;}};
try{await startGuest();if(storageMode()==='memory')document.querySelector('#demo-storage').textContent='Temporary session · Browser storage unavailable · Changes disappear when you leave';await import('./app.mjs?demo=5d9e5d1ce6c83eb1');}
catch(e){message.textContent=e.message;}
