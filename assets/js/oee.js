/* OEE article series (V4.35): the three calculators and their charts.
   Each article holds only its own calculator, so every block runs only when its elements are on the page.
   No libraries. The example line: availability 85%, performance 90%, quality 96%, $3.0M revenue. */
(function(){
  var $=function(id){return document.getElementById(id)};
  var NS='http://www.w3.org/2000/svg';
  var C={good:'#0B6FA4',ink:'#0B2A5A',plan:'#A9B2C0',down:'#C27712',speed:'#5B5BD0',qual:'#B43E3E',line:'#D9D5CA',muted:'#5A6475'};
  function pct(x,d){return (x*100).toFixed(d==null?1:d)+'%'}
  function short(x){var s=x<0?'−':'';var a=Math.abs(x);
    if(a>=1e6) return s+'$'+(a/1e6).toFixed(2)+'M';
    if(a>=1e3) return s+'$'+Math.round(a/1e3)+'K';
    return s+'$'+Math.round(a)}
  function svg(w,h,label){var s=document.createElementNS(NS,'svg');s.setAttribute('viewBox','0 0 '+w+' '+h);s.setAttribute('role','img');s.setAttribute('aria-label',label);return s}
  function el(p,tag,a,txt){var e=document.createElementNS(NS,tag);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e}
  function put(id,node){var c=$(id);c.textContent='';c.appendChild(node)}
  function v(id){return parseFloat($(id).value)}

  /* Post 1: where the hours go */
  function post1(){
    var TOTAL=17, PLAN=2, IDEAL=2000, sched=TOTAL-PLAN;
    var down=v('p1-down'), rate=v('p1-rate'), rej=v('p1-rej')/100;
    var op=sched-down, A=op/sched, P=rate/IDEAL, Q=1-rej;
    var net=op*P, val=net*Q, O=A*P*Q;
    $('p1-down-o').textContent=down.toFixed(2)+' h';
    $('p1-rate-o').textContent=rate.toLocaleString('en-US')+' units/h';
    $('p1-rej-o').textContent=(rej*100).toFixed(1)+'%';
    $('p1-A').textContent=pct(A); $('p1-P').textContent=pct(P); $('p1-Q').textContent=pct(Q);
    $('p1-O').textContent=pct(O); $('p1-T').textContent=pct(val/TOTAL);
    $('p1-units').textContent=Math.round(rate*op*Q).toLocaleString('en-US')+' good units';
    var W=720,rowH=56,s=svg(W,rowH*5+6,'Bar chart of the hours remaining after each loss');
    var rows=[
      ['Total time',TOTAL,null,0,C.plan],
      ['Scheduled time',sched,'Planned stops',PLAN,C.plan],
      ['Operating time',op,'Downtime',down,C.down],
      ['Net operating time',net,'Speed loss',op-net,C.speed],
      ['Valuable time',val,'Quality loss',net-val,C.qual]];
    rows.forEach(function(r,i){
      var y=i*rowH, x=r[1]/TOTAL*W, lw=r[3]/TOTAL*W;
      el(s,'text',{x:0,y:y+18,'class':'b'},r[0]+'  ·  '+r[1].toFixed(2)+' h');
      if(r[2]) el(s,'text',{x:W,y:y+18,'text-anchor':'end','class':'m'},r[2]+' '+r[3].toFixed(2)+' h');
      el(s,'rect',{x:0,y:y+26,width:Math.max(x,0),height:20,rx:2,fill:i===4?C.good:C.ink,opacity:i===4?1:0.85});
      if(lw>0.5) el(s,'rect',{x:x+2,y:y+26,width:Math.max(lw-2,1),height:20,rx:2,fill:r[4]});
    });
    put('oee-cascade',s);
  }

  /* Post 2: what the losses cost */
  function post2(){
    var R=v('p2-R')*1e6, A=v('p2-A')/100, P=v('p2-P')/100, Q=v('p2-Q')/100, O=A*P*Q;
    var pot=R/O, d=R*(1-A)/O, sp=R*A*(1-P)/O, q=R*A*P*(1-Q)/O;
    $('p2-R-o').textContent='$'+(R/1e6).toFixed(1)+'M';
    $('p2-A-o').textContent=pct(A,0); $('p2-P-o').textContent=pct(P,0); $('p2-Q-o').textContent=pct(Q,1);
    $('p2-O').textContent=pct(O); $('p2-d').textContent=short(d); $('p2-s').textContent=short(sp); $('p2-q').textContent=short(q);
    var m=v('p2-m')/100; $('p2-m-o').textContent=pct(m,0);
    function pr(x){return short(x*m)+' profit per year'}
    $('p2-dn').textContent=pr(d); $('p2-sn').textContent=pr(sp); $('p2-qn').textContent=pr(q);
    $('p2-t').textContent=short(pot-R); $('p2-tn').textContent=pr(pot-R);
    $('p2-pt').textContent=short(R*0.01/O); $('p2-ptn').textContent=pr(R*0.01/O);
    var W=720,H=330,top=30,bot=H-48,s=svg(W,H,'Waterfall chart from potential revenue at 100% OEE down to actual revenue'), band=W/5, bw=86;
    function y(val){return bot-(val/pot)*(bot-top)}
    var cols=[
      ['At 100% OEE',0,pot,C.plan,short(pot)],
      ['Downtime',pot-d,pot,C.down,short(-d)],
      ['Speed loss',pot-d-sp,pot-d,C.speed,short(-sp)],
      ['Quality loss',R,pot-d-sp,C.qual,short(-q)],
      ['Actual revenue',0,R,C.good,short(R)]];
    el(s,'line',{x1:0,x2:W,y1:bot,y2:bot,stroke:C.line,'stroke-width':1});
    cols.forEach(function(c,i){
      var x=i*band+(band-bw)/2, y1=y(c[2]), h=Math.max(y(c[1])-y1,1);
      el(s,'rect',{x:x,y:y1,width:bw,height:h,rx:2,fill:c[3]});
      el(s,'text',{x:x+bw/2,y:y1-8,'text-anchor':'middle','class':'b'},c[4]);
      el(s,'text',{x:x+bw/2,y:bot+22,'text-anchor':'middle','class':'m'},c[0]);
      if(i<4){var yy=(i===3)?y(R):y(c[1]===0?c[2]:c[1]);
        el(s,'line',{x1:x+bw,x2:x+band,y1:yy,y2:yy,stroke:C.muted,'stroke-width':1,'stroke-dasharray':'3 3'});}
    });
    put('oee-waterfall',s);
  }

  /* Post 3: the business case. Year 1 delivers half of the OEE gain; flows are before financing. */
  function roi(p){
    var o0=p.A*p.P*p.Q, o1=Math.min(1,p.A+p.dA)*Math.min(1,p.P+p.dP)*Math.min(1,p.Q+p.dQ);
    var extraRev=p.R*(o1/o0-1), gp=extraRev*p.m, full=gp+p.sav-p.run, y1=gp*0.5+p.sav-p.run;
    var flows=[y1],i; for(i=2;i<=10;i++) flows.push(full);
    var cum=-p.I, pay=null, cums=[-p.I], npv=-p.I;
    flows.forEach(function(f,k){var prev=cum; cum+=f; cums.push(cum);
      if(pay===null&&cum>=0&&f>0) pay=k+(-prev)/f; npv+=f/Math.pow(1+p.r,k+1);});
    var mr=p.r/12, pmt=p.I*mr/(1-Math.pow(1+mr,-120))*12;
    return {o0:o0,o1:o1,extraRev:extraRev,full:full,y1:y1,pay:pay,npv:npv,pmt:pmt,cums:cums};
  }
  function post3(){
    var p={A:0.85,P:0.90,Q:0.96,r:0.10,run:10800,
      I:v('p3-I')*1e6,R:v('p3-R')*1e6,m:v('p3-m')/100,dA:v('p3-dA')/100,dP:v('p3-dP')/100,dQ:v('p3-dQ')/100,sav:v('p3-sav')*1e3};
    var r=roi(p);
    $('p3-I-o').textContent='$'+(p.I/1e6).toFixed(2)+'M';
    $('p3-R-o').textContent='$'+(p.R/1e6).toFixed(1)+'M';
    $('p3-m-o').textContent=pct(p.m,0);
    $('p3-dA-o').textContent='+'+(p.dA*100).toFixed(1)+' pts';
    $('p3-dP-o').textContent='+'+(p.dP*100).toFixed(1)+' pts';
    $('p3-dQ-o').textContent='+'+(p.dQ*100).toFixed(1)+' pts';
    $('p3-sav-o').textContent=short(p.sav);
    $('p3-O').textContent=pct(r.o1); $('p3-On').textContent='from '+pct(r.o0);
    $('p3-x').textContent=short(r.extraRev); $('p3-b').textContent=short(r.full);
    $('p3-pay').textContent=r.pay===null?'Over 10 years':r.pay.toFixed(1)+' years';
    $('p3-npv').textContent=short(r.npv); $('p3-net').textContent=short(r.full-r.pmt);
    var W=720,H=350,left=8,top=58,bot=H-58,s=svg(W,H,'Bar chart of the cumulative cash position by year');
    var mx=Math.max.apply(null,r.cums.concat([0])), mn=Math.min.apply(null,r.cums.concat([0]));
    var span=(mx-mn)||1; function y(val){return top+(mx-val)/span*(bot-top)}
    var band=(W-left)/11, bw=band*0.62;
    r.cums.forEach(function(c,i){
      var x=left+i*band+(band-bw)/2, y0=y(0), yc=y(c);
      el(s,'rect',{x:x,y:Math.min(y0,yc),width:bw,height:Math.max(Math.abs(yc-y0),1),rx:2,fill:c<0?C.qual:C.good});
      el(s,'text',{x:x+bw/2,y:c<0?yc+15:yc-6,'text-anchor':'middle','class':'s'},short(c).replace('$',''));
      el(s,'text',{x:x+bw/2,y:H-22,'text-anchor':'middle','class':'m s'},i===0?'Start':'Yr '+i);
    });
    el(s,'line',{x1:0,x2:W,y1:y(0),y2:y(0),stroke:C.ink,'stroke-width':1});
    el(s,'text',{x:0,y:16,'class':'b'},r.pay===null?'No payback within 10 years':'Payback after '+r.pay.toFixed(1)+' years');
    el(s,'text',{x:W,y:16,'text-anchor':'end','class':'m s'},'Cumulative cash, $ (K = thousand, M = million)');
    put('oee-cum',s);
  }

  var run={p1:$('oee-cascade')?post1:null,p2:$('oee-waterfall')?post2:null,p3:$('oee-cum')?post3:null};
  document.querySelectorAll('.oee-calc input[type=range]').forEach(function(inp){
    var f=run[inp.id.slice(0,2)]; if(f) inp.addEventListener('input',f);
  });
  for(var k in run) if(run[k]) run[k]();
})();
