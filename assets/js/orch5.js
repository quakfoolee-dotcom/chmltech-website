/* Figure 1 of Vol. 106, Issue 1: interactive explorer of five multi-agent orchestration models.
   Data: the JSON in #o5-data, written by content/journal/figure-scripts/orch5.py. Styles: "Vol. 106 orch5" in journal.css.
   Each step sends message tokens along edges, then highlights the nodes that act. Loops through all five models continuously; there are no reader controls (V3). */
(function () {
  var root = document.getElementById('o5');
  if (!root) return;
  var M = JSON.parse(document.getElementById('o5-data').textContent);
  var fig = root.closest('figure');
  root.hidden = false;
  if (fig) fig.classList.add('j-fig-live-on');

  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.getElementById('o5-svg');
  var $ = function (id) { return document.getElementById(id); };
  var reduce = false;   // V3: the figure always animates and loops (owner's decision)
  var cur = 0, step = 0, playing = !reduce, timer = null, raf = null, visible = true, nodeEls = {}, stepId = 0, comparing = false;
  var STEP_MS = 3200, TRAVEL_MS = 1100;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  function nodeSize(n) {
    if (n.k === 'board') return { w: 150, h: 70 };
    if (n.k === 'lead' || n.k === 'sup') return { w: n.label.length * 7.4 + 30, h: 36 };
    if (n.k === 'req' || n.k === 'gate' || n.k === 'ledger') return { w: n.label.length * 7 + 24, h: 30 };
    return { r: 19 };
  }

  // point on the boundary of node n, in the direction of (tx, ty)
  function edgePoint(n, tx, ty) {
    var s = nodeSize(n), dx = tx - n.x, dy = ty - n.y, L = Math.hypot(dx, dy) || 1;
    if (s.r) return [n.x + dx / L * (s.r + 3), n.y + dy / L * (s.r + 3)];
    var hw = s.w / 2 + 3, hh = s.h / 2 + 3, t = Math.min(hw / Math.abs(dx || 1e-6), hh / Math.abs(dy || 1e-6));
    return [n.x + dx * t, n.y + dy * t];
  }

  function draw() {
    var m = M[cur], byId = {};
    m.nodes.forEach(function (n) { byId[n.id] = n; });
    while (svg.lastChild && svg.lastChild.nodeName !== 'title') svg.removeChild(svg.lastChild);
    svg.style.setProperty('--c', m.color);
    var gE = el('g', { 'class': 'o5-edges' }, svg);
    m.edges.forEach(function (e) {
      var a = byId[e[0]], b = byId[e[1]], p = edgePoint(a, b.x, b.y), q = edgePoint(b, a.x, a.y);
      el('line', { x1: p[0], y1: p[1], x2: q[0], y2: q[1], 'class': 'o5-edge', 'data-e': e[0] + '>' + e[1] }, gE);
    });
    el('g', { 'class': 'o5-tokens', id: 'o5-tokens' }, svg);
    var gN = el('g', { 'class': 'o5-nodes' }, svg);
    nodeEls = {};
    m.nodes.forEach(function (n) {
      var g = el('g', { 'class': 'o5-node o5-k-' + n.k, transform: 'translate(' + n.x + ',' + n.y + ')' }, gN), s = nodeSize(n);
      if (s.r) {
        el('circle', { r: s.r, 'class': 'o5-shape' }, g);
        el('text', { y: 4, 'class': 'o5-glyph' }, g).textContent = n.label.replace(/^\D+\s?/, '') || n.label[0];
        el('text', { y: s.r + 16, 'class': 'o5-label' }, g).textContent = n.label;
      } else {
        el('rect', { x: -s.w / 2, y: -s.h / 2, width: s.w, height: s.h, rx: n.k === 'board' ? 8 : 7, 'class': 'o5-shape' }, g);
        el('text', { y: n.k === 'board' ? -8 : 4.5, 'class': 'o5-label-in' }, g).textContent = n.label;
        if (n.k === 'board') el('text', { y: 16, 'class': 'o5-ver', id: 'o5-ver' }, g).textContent = '';
      }
      nodeEls[n.id] = g;
    });
    if (m.id === 'mesh') el('text', { x: 548, y: 22, 'class': 'o5-hops', id: 'o5-hops', 'text-anchor': 'end' }, svg);
    m._byId = byId;
  }

  function setStep(i, animate) {
    var m = M[cur], s = m.steps[i];
    step = i; stepId++;
    [].forEach.call($('o5-list').children, function (li, k) {
      li.classList.toggle('on', k === i); li.classList.toggle('done', k < i);
      li.setAttribute('aria-current', k === i ? 'step' : 'false');
    });
    $('o5-desc').textContent = s.d;
    $('o5-count').textContent = 'Step ' + (i + 1) + ' of ' + m.steps.length;
    for (var id in nodeEls) {
      nodeEls[id].classList.remove('hl');
      nodeEls[id].classList.toggle('dim', (s.dim || []).indexOf(id) >= 0);
    }
    [].forEach.call(svg.querySelectorAll('.o5-edge'), function (e) { e.classList.remove('live'); });
    var ver = $('o5-ver'); if (ver) ver.textContent = s.board ? 'version ' + s.board.slice(1) : '';
    var hops = $('o5-hops');
    if (hops) { var h = [0, 0, 1, 2, 3, 3, 3][i + 1] || 0; hops.textContent = 'Hops used: ' + h + ' of 3'; hops.classList.toggle('max', h >= 3); }
    var tk = $('o5-tokens'); while (tk.firstChild) tk.removeChild(tk.firstChild);
    cancelAnimationFrame(raf);
    var toks = s.msgs.map(function (mm) {
      var a = m._byId[mm[0]], b = m._byId[mm[1]], p = edgePoint(a, b.x, b.y), q = edgePoint(b, a.x, a.y);
      var line = svg.querySelector('[data-e="' + mm[0] + '>' + mm[1] + '"],[data-e="' + mm[1] + '>' + mm[0] + '"]');
      if (line) { line.classList.add('live'); line.classList.toggle('rev', line.getAttribute('data-e') !== mm[0] + '>' + mm[1]); }
      if (mm[2]) {   // the message label stays on the edge for the whole step: near the spread-out end when several messages share an end
        var nS = s.msgs.filter(function (o) { return o[0] === mm[0]; }).length, nT = s.msgs.filter(function (o) { return o[1] === mm[1]; }).length;
        var f = nS > 1 ? 0.66 : nT > 1 ? 0.34 : 0.5, lx = p[0] + (q[0] - p[0]) * f, ly = p[1] + (q[1] - p[1]) * f;
        var lab = el('text', { x: lx.toFixed(1), y: (ly - 7).toFixed(1), 'class': 'o5-tok-l' }, tk); lab.textContent = mm[2];
      }
      var g = el('g', { 'class': 'o5-tok' }, tk);
      el('circle', { r: 6 }, g);
      return { g: g, p: p, q: q };
    });
    function place(t) {
      toks.forEach(function (o) {
        var x = o.p[0] + (o.q[0] - o.p[0]) * t, y = o.p[1] + (o.q[1] - o.p[1]) * t;
        o.g.setAttribute('transform', 'translate(' + x.toFixed(1) + ',' + y.toFixed(1) + ')');
        o.g.style.opacity = t > 0.9 ? String(1 - (t - 0.9) / 0.1) : '1';
      });
    }
    function lightUp() { s.hl.forEach(function (id) { if (nodeEls[id]) nodeEls[id].classList.add('hl'); }); }
    if (!toks.length) { lightUp(); return; }
    if (!animate || reduce) { place(1); lightUp(); return; }
    var my = ++stepId, t0 = performance.now(), lit = false, GAP = 450;
    (function frame(now) {   // tokens keep travelling for the whole step, so the flow stays visible
      if (my !== stepId) return;
      var k = ((now - t0) % (TRAVEL_MS + GAP)) / TRAVEL_MS, t = Math.min(1, k), e = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      place(e);
      if (!lit && now - t0 >= TRAVEL_MS) { lit = true; lightUp(); }
      raf = requestAnimationFrame(frame);
    })(t0);
  }

  function select(i, animate) {
    cur = i; setCompare(false);
    var m = M[i];
    [].forEach.call(root.querySelectorAll('.o5-tab:not(.o5-tab-all)'), function (b, k) {
      b.classList.toggle('on', k === i); b.setAttribute('aria-pressed', k === i ? 'true' : 'false');
    });
    root.style.setProperty('--c', m.color);
    $('o5-kind').textContent = m.n + ' · ' + m.kind;
    $('o5-name').textContent = m.name;
    $('o5-svg-t').textContent = 'Diagram of the ' + m.name + ' model';
    $('o5-list').innerHTML = m.steps.map(function (s, k) { return '<li><span>' + s.t + '</span></li>'; }).join('');
    $('o5-prof').innerHTML = m.profile.map(function (p) { return '<div><dt>' + p[0] + '</dt><dd>' + p[1] + '</dd></div>'; }).join('');
    $('o5-fit').textContent = m.fit; $('o5-haz').textContent = m.hazard; $('o5-key').textContent = m.key;
    $('o5-combine').textContent = m.combine;
    draw();
    setStep(0, animate);
  }

  function tick() {
    clearTimeout(timer);
    var bar = $('o5-bar'); if (!bar) return;
    bar.style.transition = 'none'; bar.style.width = '0%';
    if (!playing || !visible || comparing) return;
    void bar.offsetWidth; bar.style.transition = 'width ' + STEP_MS + 'ms linear'; bar.style.width = '100%';
    timer = setTimeout(function () {
      var m = M[cur];
      if (step < m.steps.length - 1) setStep(step + 1, true);
      else select((cur + 1) % M.length, true);
      tick();
    }, STEP_MS);
  }


  // V5: "Compare all" shows the five models side by side and holds the loop; choosing a model resumes it
  function setCompare(on) {
    comparing = on;
    $('o5-compare').hidden = !on; $('o5-panel').hidden = on;
    var all = $('o5-tab-all'); all.classList.toggle('on', on); all.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (on) [].forEach.call(root.querySelectorAll('.o5-tab:not(.o5-tab-all)'), function (b) { b.classList.remove('on'); b.setAttribute('aria-pressed', 'false'); });
  }
  // V4: a reader can pick a model; it starts from step 1 and the loop carries on from there (no pause)
  root.querySelector('.o5-tabs').addEventListener('click', function (ev) {
    var b = ev.target.closest('.o5-tab'); if (!b) return;
    if (b.dataset.m === 'all') { setCompare(true); tick(); return; }
    select(M.findIndex(function (m) { return m.id === b.dataset.m; }), true); tick();
  });
  select(0, true);
  document.addEventListener('visibilitychange', function () { visible = !document.hidden; tick(); });
  tick();
})();
