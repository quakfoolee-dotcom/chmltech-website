/* Insights page: "Start here" panel. A goal button opens its reading list; "#goal-<id>" in the address opens one on load.
   "All articles on this topic" presses the matching filter chip in the list below. No libraries. */
(function(){
  var box=document.querySelector('.if'); if(!box) return;
  box.classList.add('js');
  var goals=box.querySelectorAll('.if-goal'), panels=box.querySelectorAll('.if-panel');
  function open(id,focus){
    Array.prototype.forEach.call(goals,function(g){ g.setAttribute('aria-pressed', g.getAttribute('data-goal')===id?'true':'false'); });
    Array.prototype.forEach.call(panels,function(p){
      p.hidden = p.id!=='goal-'+id;
      if(!p.hidden&&focus){ p.focus({preventScroll:true}); var r=p.getBoundingClientRect(); if(r.bottom>window.innerHeight||r.top<80) p.scrollIntoView({behavior:'smooth',block:'nearest'}); }
    });
  }
  Array.prototype.forEach.call(goals,function(g){
    g.addEventListener('click',function(){
      var id=g.getAttribute('data-goal'), on=g.getAttribute('aria-pressed')==='true';
      open(on?'':id,!on);
      try{ if(history.replaceState) history.replaceState(null,'',on?location.pathname+location.search:'#goal-'+id); }catch(e){}
    });
  });
  var m=location.hash.match(/^#goal-([\w-]+)$/); open(m?m[1]:'',false);
  box.addEventListener('click',function(e){
    var a=e.target.closest?e.target.closest('a[data-cat]'):null; if(!a) return;
    var chip=document.querySelector('.chip[data-cat="'+a.getAttribute('data-cat')+'"]'); if(!chip) return;
    e.preventDefault(); chip.click(); chip.parentNode.scrollIntoView({behavior:'smooth',block:'start'});
  });
})();
