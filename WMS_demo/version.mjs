// The browser, HTTP service and launcher share one release identifier.
export const APP_VERSION='2.24.3';
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function versionCompatibility(info){
 const server=info?.version;
 if(!server||server===APP_VERSION)return 'ready';
 const parts=value=>/^\d+\.\d+\.\d+$/.test(value)?value.split('.').map(Number):null,a=parts(server),b=parts(APP_VERSION);
 if(a&&b){for(let i=0;i<3;i++)if(a[i]!==b[i])return a[i]<b[i]?'restart':'refresh';}
 return 'refresh';
}
export const requiresVersionUpdate=info=>versionCompatibility(info)!=='ready';
export function versionUpdateMessage(info){
 return versionCompatibility(info)==='restart'?'Restart Harbor with Start Harbor.cmd, then refresh this page.':'Refresh this page to load the running Harbor version.';
}
export function versionNoticeHTML(info){
 if(!requiresVersionUpdate(info))return '';
 return `<div class="alert" role="status" data-version-notice><strong>Harbor versions do not match.</strong><p><span>Interface version</span>: <span data-l10n-skip>${APP_VERSION}</span> · <span>Server version</span>: <span data-l10n-skip>${escape(info.version)}</span></p><p>${versionUpdateMessage(info)}</p><p>Your saved warehouse records are preserved. No migration is needed.</p></div>`;
}


