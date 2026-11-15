/* Innovation article: value of a portfolio of small tests (V5.27).
   Expected successes = tests x pass rate; expected value = successes x value of one success. No libraries. */
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('bt-n')) return;
  var money=function(v){ return '$'+Math.round(v).toLocaleString('en-CA'); };
  function calc(){
    var n=+$('bt-n').value, c=+$('bt-c').value, p=+$('bt-p').value/100, v=+$('bt-v').value;
    $('bt-n-o').textContent=n; $('bt-c-o').textContent=money(c); $('bt-p-o').textContent=Math.round(p*100)+'%'; $('bt-v-o').textContent=money(v);
    var s=n*p, tc=n*c, ev=s*v;
    $('bt-s').textContent=s.toFixed(1); $('bt-tc').textContent=money(tc); $('bt-ev').textContent=money(ev);
    $('bt-r').textContent=(ev/tc).toFixed(1)+' times';
  }
  ['bt-n','bt-c','bt-p','bt-v'].forEach(function(id){ $(id).addEventListener('input',calc); });
  calc();
})();
