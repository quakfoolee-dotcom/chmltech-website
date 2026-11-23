export function mountAccount({onChange=()=>{}}={}){let info;return {observe(value){info=value;},check:async()=>{},open(){},html:()=>'<span class="account-identity"><strong>Demo visitor</strong><small>Browser workspace</small></span>',get user(){return info?.user;}};}

