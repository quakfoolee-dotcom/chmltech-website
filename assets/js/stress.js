/* Uncertain economy article: profit stress test (V5.27).
   Profit = sales x (1 - variable share) - fixed; break-even = fixed / (1 - variable share). No libraries. */
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('st-r')) return;
  var money=function(v){ var a=Math.abs(v), s=v<0?'−$':'$';
    return a>=1e6 ? s+(a/1e6).toFixed(2)+'M' : s+Math.round(a/1000).toLocaleString('en-CA')+'k'; };
  function calc(){
    var r=+$('st-r').value, v=+$('st-v').value/100, f=+$('st-f').value, dv=+$('st-dv').value/100, dc=+$('st-dc').value/100;
    $('st-r-o').textContent=money(r); $('st-v-o').textContent=Math.round(v*100)+'%'; $('st-f-o').textContent=money(f);
    $('st-dv-o').textContent=(dv>0?'+':'')+Math.round(dv*100)+'%'; $('st-dc-o').textContent=(dc>0?'+':'')+(dc*100).toFixed(1)+'%';
    var p0=r*(1-v)-f, v1=v*(1+dc), r1=r*(1+dv), p1=r1*(1-v1)-f;
    $('st-p0').textContent=money(p0); $('st-p1').textContent=money(p1);
    $('st-be').textContent=v1>=1 ? 'None: costs exceed price' : money(f/(1-v1));
    var be0=f/(1-v); $('st-ms').textContent=v>=1||be0>=r ? 'None' : Math.round((r-be0)/r*100)+'%';
  }
  ['st-r','st-v','st-f','st-dv','st-dc'].forEach(function(id){ $(id).addEventListener('input',calc); });
  calc();
})();
