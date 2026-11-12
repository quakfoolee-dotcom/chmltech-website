/* Process safety series, Part 1: cooling failure calculator (MTSR and criticality class).
   MTSR = Tp + accumulation x adiabatic temperature rise. Classes after Stoessel:
   1: MTSR < MTT < TD24   2: MTSR < TD24 < MTT   3: MTT < MTSR < TD24   4: MTT < TD24 < MTSR   5: TD24 < MTT and TD24 < MTSR
   The example: 150 kJ/kg, 2.0 kJ/kg.K, Tp 60 C, MTT 110 C, TD24 150 C, 20% accumulation. No libraries. */
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('rw-H')) return;
  var NS='http://www.w3.org/2000/svg';
  var C={ink:'#0B2A5A',blue:'#0B6FA4',orange:'#C27712',red:'#B43E3E',green:'#4D7F12',purple:'#5B5BD0',line:'#D9D5CA',muted:'#5A6475',sand:'#ECE9E1'};
  var CLS={
    1:['Class 1','Boiling point and decomposition are both out of reach. Avoid heat build-up from long holds.',C.green],
    2:['Class 2','Boiling is out of reach, but decomposition starts below the boiling point. Avoid long holds at MTSR.',C.green],
    3:['Class 3','The batch would boil before it decomposes. The condenser and vent must handle boiling at full rate.',C.orange],
    4:['Class 4','Boiling comes first, but decomposition can follow. Evaporative cooling must be proven to hold the batch.',C.red],
    5:['Class 5','Decomposition starts before the batch can boil. Boiling gives no protection. Change the process conditions.',C.red]};
  function el(p,tag,a,txt){var e=document.createElementNS(NS,tag);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e}
  function v(id){return parseFloat($(id).value)}
  function n0(x){return Math.round(x).toLocaleString('en-US')}
  function klass(mtsr,mtt,td){
    if(mtsr<=td){ if(mtsr<=mtt) return td>=mtt?1:2; return 3 }
    return mtt<td?4:5;
  }
  function draw(){
    var H=v('rw-H'), cp=v('rw-cp'), tp=v('rw-Tp'), acc=v('rw-acc'), mtt=v('rw-MTT'), td=v('rw-TD');
    var dTad=H/cp, mtsr=tp+acc/100*dTad, k=klass(mtsr,mtt,td), c=CLS[k];
    $('rw-H-o').textContent=n0(H)+' kJ/kg'; $('rw-cp-o').textContent=cp.toFixed(1)+' kJ/kg·K'; $('rw-Tp-o').textContent=n0(tp)+' °C';
    $('rw-acc-o').textContent=n0(acc)+'%'; $('rw-MTT-o').textContent=n0(mtt)+' °C'; $('rw-TD-o').textContent=n0(td)+' °C';
    $('rw-ad').textContent=n0(dTad)+' K'; $('rw-mtsr').textContent=n0(mtsr)+' °C';
    $('rw-gap').textContent=(mtsr<mtt?n0(mtt-mtsr)+' K below':n0(mtsr-mtt)+' K above');
    $('rw-cls').textContent=c[0]; $('rw-cls').style.color=c[2]; $('rw-msg').textContent=c[1];
    var warn=(tp>=mtt||tp>=td)?'The process temperature is at or above the boiling point or TD24. Check the inputs.':'';
    $('rw-warn').textContent=warn;

    // chart: one horizontal temperature scale with the four temperatures marked
    var W=720,Hh=170,x0=30,x1=700,lo=0,hi=Math.max(200,Math.ceil((Math.max(mtsr,mtt,td)+20)/50)*50);
    function X(t){return x0+(t-lo)/(hi-lo)*(x1-x0)}
    var s=document.createElementNS(NS,'svg'); s.setAttribute('viewBox','0 0 '+W+' '+Hh); s.setAttribute('role','img');
    s.setAttribute('aria-label','Temperature scale: process '+n0(tp)+' °C, MTSR '+n0(mtsr)+' °C, boiling point '+n0(mtt)+' °C, TD24 '+n0(td)+' °C. '+c[0]+'.');
    el(s,'rect',{x:x0,y:78,width:x1-x0,height:14,rx:7,fill:C.sand});
    el(s,'rect',{x:X(tp),y:78,width:Math.max(2,X(mtsr)-X(tp)),height:14,rx:7,fill:c[2],opacity:.85});
    for(var t=lo;t<=hi;t+=50){el(s,'line',{x1:X(t),y1:96,x2:X(t),y2:102,stroke:C.muted});el(s,'text',{x:X(t),y:118,'text-anchor':'middle','class':'m s'},t+' °C')}
    var marks=[[tp,'Process',C.ink,'b'],[mtsr,'MTSR',c[2],'b'],[mtt,'Boiling (MTT)',C.blue,'t'],[td,'TD24',C.purple,'t']];
    // stagger labels that would overlap
    marks.sort(function(a,b){return a[0]-b[0]});
    var lastTop=-99,lastBot=-99;
    marks.forEach(function(m){
      var x=X(m[0]), top=m[3]==='t';
      el(s,'line',{x1:x,y1:top?50:78,x2:x,y2:top?92:120,stroke:m[2],'stroke-width':2});
      var lx=x, row=0;
      if(top){ if(x-lastTop<92) row=1; lastTop=row?lastTop:x; }
      else { if(x-lastBot<72) row=1; lastBot=row?lastBot:x; }
      var y=top?(row?18:42):(row?160:140);
      el(s,'text',{x:lx,y:y,'text-anchor':'middle','class':'b',style:'fill:'+m[2]},m[1]+' '+n0(m[0])+' °C');
    });
    var c0=$('rw-chart'); c0.textContent=''; c0.appendChild(s);
  }
  ['rw-H','rw-cp','rw-Tp','rw-acc','rw-MTT','rw-TD'].forEach(function(id){$(id).addEventListener('input',draw)});
  draw();
})();
