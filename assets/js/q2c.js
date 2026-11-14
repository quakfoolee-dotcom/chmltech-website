/* Quote-to-cash article series.
   Part 2: sizes the embedded simulator (assets/sim/q2c-factory.html#embed) to its content.
   Part 3: the payback calculator. Each block runs only when its elements are on the page. No libraries. */
(function(){
  var $=function(id){return document.getElementById(id)};

  var f=$('q2c-sim');
  if(f){
    window.addEventListener('message',function(e){
      if(e.source===f.contentWindow&&e.data&&e.data.q2cHeight) f.style.height=(e.data.q2cHeight+2)+'px';
    });
    var ask=function(){ try{ f.contentWindow.postMessage('q2cSize?','*'); }catch(err){} };
    f.addEventListener('load',ask); ask();
  }

  if($('q3-cash')){
    var money=function(x){ return '$'+Math.round(x).toLocaleString('en-US'); };
    var calc=function(){
      var cash=parseFloat($('q3-cash').value), rate=parseFloat($('q3-rate').value), cost=parseFloat($('q3-cost').value);
      var yearly=cash*rate/100, months=yearly>0?cost/yearly*12:0;
      $('q3-cash-o').textContent=money(cash);
      $('q3-rate-o').textContent=rate.toFixed(1)+'%';
      $('q3-cost-o').textContent=money(cost);
      $('q3-int').textContent=money(yearly);
      $('q3-pay').textContent=months<1?'Under 1 month':months>120?'Over 10 years':Math.round(months)+(Math.round(months)===1?' month':' months');
      $('q3-mult').textContent=(cash/cost).toFixed(1)+' times';
    };
    ['q3-cash','q3-rate','q3-cost'].forEach(function(id){ $(id).addEventListener('input',calc); });
    calc();
  }
})();
