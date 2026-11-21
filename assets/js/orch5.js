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
    for (var k in attrs) if (attrs[k] != null) e.setAttribute(k, attrs[k]);
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
        el('text', { y: 4, 'class': 'o5-glyph' }, g).textContent = n.g || n.label.replace(/^\D+\s?/, '') || n.label[0];
        el('text', { y: s.r + 16, 'class': 'o5-label' }, g).textContent = n.label;
      } else {
        el('rect', { x: -s.w / 2, y: -s.h / 2, width: s.w, height: s.h, rx: n.k === 'board' ? 8 : 7, 'class': 'o5-shape' }, g);
        el('text', { y: n.k === 'board' ? -8 : 4.5, 'class': 'o5-label-in', id: n.k === 'board' ? 'o5-boardl' : null }, g).textContent = n.label;
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
    var bl = $('o5-boardl'); if (bl) bl.setAttribute('y', s.board ? -8 : 4.5);   // centred when no version line shows
    var hops = $('o5-hops');
    if (hops) { var h = [0, 0, 1, 2, 3, 3, 3][i + 1] || 0; hops.textContent = 'Hops used: ' + h + ' of 3'; hops.classList.toggle('max', h >= 3); }
    var tk = $('o5-tokens'); while (tk.firstChild) tk.removeChild(tk.firstChild);
    var tl = $('o5-toklab'); if (!tl) tl = el('g', { 'class': 'o5-toklab', id: 'o5-toklab' }, svg);   // labels sit above the nodes
    while (tl.firstChild) tl.removeChild(tl.firstChild);
    cancelAnimationFrame(raf);
    var obst = nodeBoxes();
    var toks = s.msgs.map(function (mm) {
      var a = m._byId[mm[0]], b = m._byId[mm[1]], p = edgePoint(a, b.x, b.y), q = edgePoint(b, a.x, a.y);
      var line = svg.querySelector('[data-e="' + mm[0] + '>' + mm[1] + '"],[data-e="' + mm[1] + '>' + mm[0] + '"]');
      if (line) { line.classList.add('live'); line.classList.toggle('rev', line.getAttribute('data-e') !== mm[0] + '>' + mm[1]); }
      if (mm[2]) placeLabel(mm, p, q, s.msgs, tl, obst);
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


  // Boxes (SVG user units) of every node shape plus its label, so message labels can be kept clear of them.
  function nodeBoxes() {
    var out = [];
    Object.keys(nodeEls).forEach(function (id) {
      var g = nodeEls[id], n = M[cur]._byId[id], bb;
      try { bb = g.getBBox(); } catch (e) { return; }
      if (!bb.width) return;
      out.push({ x: n.x + bb.x - 2, y: n.y + bb.y - 2, w: bb.width + 4, h: bb.height + 4 });
    });
    return out;
  }
  // A message label goes at the first spot along or beside its edge that overlaps no node, node label or earlier label
  // and stays inside the 560 x 330 frame; failing that, at the spot with the least overlap.
  function placeLabel(mm, p, q, msgs, layer, obst) {
    var nS = msgs.filter(function (o) { return o[0] === mm[0]; }).length, nT = msgs.filter(function (o) { return o[1] === mm[1]; }).length;
    var f0 = nS > 1 ? 0.66 : nT > 1 ? 0.34 : 0.5;
    var lab = el('text', { x: 0, y: 0, 'class': 'o5-tok-l' }, layer); lab.textContent = mm[2];
    var w, h;
    try { var bb = lab.getBBox(); w = bb.width + 6; h = bb.height + 2; } catch (e) { w = 0; }
    if (!w) { w = mm[2].length * 7 + 6; h = 15; }
    var dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    if (ny > 0 || (Math.abs(ny) < 1e-6 && nx < 0)) { nx = -nx; ny = -ny; }   // normal points up (or right on vertical edges)
    var off = h / 2 + 3, best = null;
    [f0, 0.5, 0.36, 0.64, 0.25, 0.75].forEach(function (f) {
      [off, -off, off + 12, -off - 12, off + 24, -off - 24].forEach(function (d) {
        var cx = p[0] + dx * f + nx * d, cy = p[1] + dy * f + ny * d;
        if (Math.abs(ny) < 0.3) cx += (d > 0 ? 1 : -1) * w / 2;   // beside a near-vertical edge: start the text next to the line
        var r = { x: cx - w / 2, y: cy - h / 2, w: w, h: h }, sc = 0;
        obst.forEach(function (o) {
          var ix = Math.min(r.x + r.w, o.x + o.w) - Math.max(r.x, o.x), iy = Math.min(r.y + r.h, o.y + o.h) - Math.max(r.y, o.y);
          if (ix > 0 && iy > 0) sc += ix * iy;
        });
        if (r.x < 2 || r.x + r.w > 558 || r.y < 2 || r.y + r.h > 328) sc += 5000;
        if (!best || sc < best.sc - 0.5) best = { sc: sc, cx: cx, cy: cy, r: r };
      });
    });
    lab.setAttribute('x', best.cx.toFixed(1)); lab.setAttribute('y', (best.cy + h * 0.32).toFixed(1));
    obst.push(best.r);
  }

  function select(i, animate) {
    cur = i; setCompare(false);
    var m = M[i];
    [].forEach.call(root.querySelectorAll('.o5-tab:not(.o5-tab-all)'), function (b, k) {
      b.classList.toggle('on', k === i); b.setAttribute('aria-pressed', k === i ? 'true' : 'false');
    });
    var strip = root.querySelector('.o5-tabs'), at = root.querySelectorAll('.o5-tab:not(.o5-tab-all)')[i];
    if (strip && at && strip.scrollWidth > strip.clientWidth + 2)   // phone: keep the playing tab in view (scroll the strip only, never the page)
      strip.scrollTo({ left: strip.scrollLeft + at.getBoundingClientRect().left - strip.getBoundingClientRect().left - (strip.clientWidth - at.offsetWidth) / 2, behavior: 'smooth' });
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
