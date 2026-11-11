/* Scale-up series, Part 1: jacket cooling calculator and chart.
   Assumes a jacket on the wall only, liquid depth equal to diameter and a batch density of 1,000 kg/m3.
   No libraries. The example: U = 300 W/m2.K, dT = 30 K, heat of reaction 150 kJ/kg, 10,000 L. */
(function(){
  var $=function(id){return document.getElementById(id)};
  if(!$('su-V')) return;
  var NS='http://www.w3.org/2000/svg', RHO=1000;
  var C={ink:'#0B2A5A',blue:'#0B6FA4',orange:'#C27712',red:'#B43E3E',green:'#4D7F12',line:'#D9D5CA',muted:'#5A6475'};
  function el(p,tag,a,txt){var e=document.createElementNS(NS,tag);for(var k in a)e.setAttribute(k,a[k]);if(txt!=null)e.textContent=txt;p.appendChild(e);return e}
  function v(id){return parseFloat($(id).value)}
  function num(x,d){return x.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d})}
  function vol(L){return L>=1000?num(L/1000,L>=10000?0:1)+' m³':num(L,L<10?1:0)+' L'}
  function hours(h){return h<1?Math.round(h*60)+' min':num(h,1)+' h'}
  function cap(Vm3,U,dT){var D=Math.pow(4*Vm3/Math.PI,1/3);return {D:D,av:4/D,c:U*dT*4/D/1000}}   // kW per m3

  function draw(){
    var L=Math.pow(10,v('su-V')), Vm3=L/1000, U=v('su-U'), dT=v('su-T'), H=v('su-H'), t=v('su-t');
    var g=cap(Vm3,U,dT), E=H*RHO/3600, gen=E/t, tmin=E/g.c, ok=g.c>=gen;
    $('su-V-o').textContent=vol(L); $('su-U-o').textContent=num(U,0)+' W/m²·K'; $('su-T-o').textContent=num(dT,0)+' K';
    $('su-H-o').textContent=num(H,0)+' kJ/kg'; $('su-t-o').textContent=hours(t);
    $('su-av').textContent=num(g.av,1)+' m²/m³';
    $('su-c').textContent=num(g.c,g.c<100?1:0)+' kW';
    $('su-g').textContent=num(gen,gen<100?1:0)+' kW';
    $('su-m').textContent=hours(tmin);
    $('su-ok').textContent=ok?'Cooling keeps up at the planned time':'Planned time is too short';
    $('su-ok').style.color=ok?C.green:C.red; $('su-ok').style.fontWeight='600';

    var W=720,Hh=300,x0=62,x1=704,y0=24,y1=244;
    var lo=Math.min(g.c,gen,cap(40,U,dT).c), hi=Math.max(cap(0.001,U,dT).c,gen);
    var a=Math.floor(Math.log10(lo)), b=Math.ceil(Math.log10(hi)); if(b-a<2)b=a+2;
    function X(l){return x0+(Math.log10(l))/4.6*(x1-x0)}                     // l in litres, 1 to 40,000
    function Y(k){return y1-(Math.log10(k)-a)/(b-a)*(y1-y0)}
    var s=document.createElementNS(NS,'svg'); s.setAttribute('viewBox','0 0 '+W+' '+Hh); s.setAttribute('role','img');
    s.setAttribute('aria-label','Cooling capacity of '+num(g.c,1)+' kilowatts per cubic metre at '+vol(L)+', against a heat release rate of '+num(gen,1)+' kilowatts per cubic metre.');
    for(var k=a;k<=b;k++){el(s,'line',{x1:x0,y1:Y(Math.pow(10,k)),x2:x1,y2:Y(Math.pow(10,k)),stroke:C.line});
      el(s,'text',{x:x0-8,y:Y(Math.pow(10,k))+4,'text-anchor':'end','class':'m s'},num(Math.pow(10,k),k<0?-k:0))}
    [[1,'1 L'],[10,'10 L'],[100,'100 L'],[1000,'1 m³'],[10000,'10 m³']].forEach(function(t){el(s,'line',{x1:X(t[0]),y1:y1,x2:X(t[0]),y2:y1+5,stroke:C.muted});
      el(s,'text',{x:X(t[0]),y:y1+20,'text-anchor':'middle','class':'m s'},t[1])});
    el(s,'text',{x:x0-46,y:14,'class':'m s'},'kW per m³ of batch');
    el(s,'text',{x:(x0+x1)/2,y:Hh-8,'text-anchor':'middle','class':'m s'},'Reactor volume');
    var d='';for(var i=0;i<=46;i++){var l=Math.pow(10,i/10);d+=(i?'L':'M')+X(l).toFixed(1)+','+Y(cap(l/1000,U,dT).c).toFixed(1)+' '}
    el(s,'path',{d:d,fill:'none',stroke:C.blue,'stroke-width':3});
    el(s,'line',{x1:x0,y1:Y(gen),x2:x1,y2:Y(gen),stroke:C.orange,'stroke-width':2.2,'stroke-dasharray':'7 4'});
    el(s,'line',{x1:X(L),y1:y0,x2:X(L),y2:y1,stroke:C.muted,'stroke-dasharray':'3 4'});
    el(s,'circle',{cx:X(L),cy:Y(g.c),r:7,fill:ok?C.green:C.red,stroke:'#fff','stroke-width':2});
    var right=X(L)<(x0+x1)/2;
    // The cooling label sits on the far side of the point from the heat release line, so the two never overlap.
    el(s,'text',{x:X(L)+(right?12:-12),y:Y(g.c)+(ok?-12:(right?40:24)),'text-anchor':right?'start':'end','class':'b'},'Cooling '+num(g.c,g.c<100?1:0)+' kW/m³');
    var gy=Y(gen), near=Math.abs(gy-Y(cap(0.0012,U,dT).c))<26;
    el(s,'text',{x:near?x1:x0+8,y:gy-8,'text-anchor':near?'end':'start','class':'b',style:'fill:'+C.orange},'Heat release '+num(gen,gen<100?1:0)+' kW/m³');
    var c=$('su-chart'); c.textContent=''; c.appendChild(s);
  }
  ['su-V','su-U','su-T','su-H','su-t'].forEach(function(id){$(id).addEventListener('input',draw)});
  draw();
})();
