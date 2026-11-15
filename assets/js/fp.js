/* First principles thinking article: the yield-gap calculator (V5.25).
   Saving a year = M (1 - Y / Y*), where M is material bought a year, Y the yield today and Y* the target yield.
   Runs only when the calculator is on the page. No libraries. */
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('fp-m')) return;
  var money=function(v){ return '$'+Math.round(v).toLocaleString('en-CA'); };
  function calc(){
    var M=parseFloat($('fp-m').value), y=parseFloat($('fp-y').value)/100, t=parseFloat($('fp-t').value)/100, c=parseFloat($('fp-c').value);
    $('fp-m-o').textContent=money(M);
    $('fp-y-o').textContent=(y*100).toFixed(1)+'%';
    $('fp-t-o').textContent=(t*100).toFixed(1)+'%';
    $('fp-c-o').textContent=money(c);
    var save=t>y ? M*(1-y/t) : 0, months=save>0 ? c/save*12 : Infinity;
    $('fp-gap').textContent=money(M*(1-y));
    $('fp-save').textContent=save>0 ? money(save) : 'None';
    $('fp-pay').textContent=save<=0 ? 'Set a target above today' : months<1 ? 'Under 1 month' : months>120 ? 'Over 10 years' :
      Math.round(months)+(Math.round(months)===1?' month':' months');
    $('fp-pt').textContent=money(M*(1-y/Math.min(1,y+0.01)));
  }
  ['fp-m','fp-y','fp-t','fp-c'].forEach(function(id){ $(id).addEventListener('input',calc); });
  calc();
})();
