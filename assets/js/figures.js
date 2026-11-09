/* Chmltech interactive course illustrations (V4.1): cycle, flow, stack, compare, timeline, bars.
   Usage: ChmFig.render(hostElement, figureConfig). Respects prefers-reduced-motion. */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function detail(host) { var d = host.querySelector('.fig-detail'); return function (title, text, extra) { d.innerHTML = '<strong>' + esc(title) + '</strong><p>' + esc(text) + '</p>' + (extra || ''); }; }

  /* ---------------- cycle ---------------- */
  function cycle(host, c) {
    var st = c.stages, n = st.length, R = 38, nodes = '';
    st.forEach(function (s, i) {
      var a = (-90 + i * 360 / n) * Math.PI / 180, x = 50 + R * Math.cos(a), y = 50 + R * Math.sin(a);
      nodes += '<button type="button" class="cyc-node" data-i="' + i + '" style="left:' + x.toFixed(2) + '%;top:' + y.toFixed(2) + '%"><b>' + (i + 1) + '</b>' + esc(s.label) + '</button>';
    });
    var arrows = '';
    for (var i = 0; i < n; i++) {
      var a1 = (-90 + i * 360 / n + 360 / n * 0.5) * Math.PI / 180;
      var ax = 50 + R * Math.cos(a1), ay = 50 + R * Math.sin(a1), rot = -90 + i * 360 / n + 360 / n * 0.5 + 90;
      arrows += '<path d="M -2.2 -2 L 1.8 0 L -2.2 2" transform="translate(' + ax.toFixed(2) + ' ' + ay.toFixed(2) + ') rotate(' + rot.toFixed(1) + ')" class="cyc-arrow"/>';
    }
    host.innerHTML = '<div class="fig-cycle"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="' + R + '" class="cyc-track"/><circle cx="50" cy="50" r="' + R + '" class="cyc-run" style="animation-duration:' + (n * 2.4) + 's"/>' + arrows + '</svg>' +
      '<div class="cyc-center">' + esc(c.center || '') + '</div>' + nodes + '</div><div class="fig-detail" aria-live="polite"></div>';
    var show = detail(host), btns = host.querySelectorAll('.cyc-node'), cur = 0, timer = null;
    function pick(i) {
      cur = i;
      Array.prototype.forEach.call(btns, function (b, k) { b.classList.toggle('is-on', k === i); b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      show('Stage ' + (i + 1) + ': ' + st[i].label, st[i].text);
    }
    host.addEventListener('click', function (e) { var b = e.target.closest('.cyc-node'); if (!b) return; clearInterval(timer); timer = null; pick(+b.getAttribute('data-i')); });
    pick(0);
    if (!reduce) timer = setInterval(function () { if (!host.isConnected || host.offsetParent === null) return; pick((cur + 1) % n); }, 2400);
  }

  /* ---------------- flow ---------------- */
  function flow(host, c) {
    var steps = c.steps, b = (c.bottleneck === null || c.bottleneck === undefined) ? -1 : c.bottleneck, h = '<div class="fig-flow' + (b >= 0 ? ' has-bn' : '') + '">';
    steps.forEach(function (s, i) {
      if (i > 0) {
        var slow = b >= 0 && i > b ? ' slow' : '', q = b >= 0 && i === b ? '<span class="flow-queue" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>' : '';
        h += '<span class="flow-link' + slow + '" aria-hidden="true"><i></i><i></i><i></i>' + q + '</span>';
      }
      h += '<button type="button" class="flow-step' + (i === b ? ' is-bn' : '') + '" data-i="' + i + '"><b>' + (i + 1) + '</b>' + esc(s.label) + (i === b ? '<em>Bottleneck</em>' : '') + '</button>';
    });
    h += '</div>';
    if (b >= 0) h += '<div class="btn-row" style="margin-top:14px"><button type="button" class="btn btn-ghost fig-fix" aria-pressed="false">Fix the bottleneck</button></div>';
    host.innerHTML = h + '<div class="fig-detail" aria-live="polite"></div>';
    var show = detail(host), wrap = host.querySelector('.fig-flow');
    host.addEventListener('click', function (e) {
      var s = e.target.closest('.flow-step');
      if (s) {
        var i = +s.getAttribute('data-i');
        Array.prototype.forEach.call(host.querySelectorAll('.flow-step'), function (x) { x.classList.toggle('is-on', x === s); });
        show('Step ' + (i + 1) + ': ' + steps[i].label, steps[i].text);
      }
      var f = e.target.closest('.fig-fix');
      if (f) {
        var on = wrap.classList.toggle('fixed');
        f.setAttribute('aria-pressed', on ? 'true' : 'false');
        f.textContent = on ? 'Show the original flow' : 'Fix the bottleneck';
        if (on) show('After the fix', c.fix_text || ''); else show('Bottleneck: ' + steps[b].label, steps[b].text);
      }
    });
    if (b >= 0) show('Bottleneck: ' + steps[b].label, steps[b].text + ' Click "Fix the bottleneck" to see the difference.');
    else show(steps[0].label, steps[0].text + ' Click any step for details.');
  }

  /* ---------------- stack ---------------- */
  function stack(host, c) {
    var L = c.layers, h = '<div class="fig-stack">';
    if (c.top_label) h += '<div class="stack-roof" style="--d:' + (L.length * 0.18 + 0.1) + 's">' + esc(c.top_label) + '</div>';
    for (var i = L.length - 1; i >= 0; i--) {
      h += '<button type="button" class="stack-layer" data-i="' + i + '" style="--d:' + (i * 0.18) + 's;--w:' + (100 - (L.length - 1 - i) * 0 ) + '%"><span class="stack-num">' + (i + 1) + '</span>' + esc(L[i].label) + '</button>';
    }
    h += '</div><div class="btn-row" style="margin-top:12px"><button type="button" class="btn btn-ghost fig-replay">Replay build-up</button></div><div class="fig-detail" aria-live="polite"></div>';
    host.innerHTML = h;
    var show = detail(host);
    host.addEventListener('click', function (e) {
      var s = e.target.closest('.stack-layer');
      if (s) { var i = +s.getAttribute('data-i'); Array.prototype.forEach.call(host.querySelectorAll('.stack-layer'), function (x) { x.classList.toggle('is-on', x === s); }); show('Layer ' + (i + 1) + ': ' + L[i].label, L[i].text); }
      if (e.target.closest('.fig-replay')) { var st = host.querySelector('.fig-stack'); st.classList.remove('play'); void st.offsetWidth; st.classList.add('play'); }
    });
    host.querySelector('.fig-stack').classList.add('play');
    show('Layer 1: ' + L[0].label, L[0].text + ' Each layer depends on the one beneath it. Click a layer for details.');
  }

  /* ---------------- compare ---------------- */
  function compare(host, c) {
    host.innerHTML = '<div class="fig-compare"><div class="cmp-toggle" role="group" aria-label="Switch view"><button type="button" data-side="left" aria-pressed="true">' + esc(c.left.title) + '</button><button type="button" data-side="right" aria-pressed="false">' + esc(c.right.title) + '</button><span class="cmp-thumb" aria-hidden="true"></span></div><div class="cmp-card" aria-live="polite"></div></div>';
    var card = host.querySelector('.cmp-card'), auto = null;
    function set(side) {
      var s = c[side];
      host.querySelector('.fig-compare').setAttribute('data-side', side);
      Array.prototype.forEach.call(host.querySelectorAll('[data-side]'), function (b) { if (b.tagName === 'BUTTON') b.setAttribute('aria-pressed', b.getAttribute('data-side') === side ? 'true' : 'false'); });
      card.className = 'cmp-card side-' + side;
      card.innerHTML = '<h4>' + esc(s.title) + '</h4><ul>' + s.points.map(function (p, i) { return '<li style="--d:' + (i * 0.09) + 's">' + esc(p) + '</li>'; }).join('') + '</ul>';
    }
    host.addEventListener('click', function (e) { var b = e.target.closest('button[data-side]'); if (!b) return; clearInterval(auto); set(b.getAttribute('data-side')); });
    set('left');
    if (!reduce) { var flip = 'right'; auto = setInterval(function () { if (host.offsetParent === null) return; set(flip); flip = flip === 'right' ? 'left' : 'right'; }, 4500); }
  }

  /* ---------------- timeline ---------------- */
  function timeline(host, c) {
    var P = c.phases, h = '<div class="fig-timeline" style="--n:' + P.length + '"><span class="tl-line" aria-hidden="true"><span></span></span>';
    P.forEach(function (p, i) { h += '<button type="button" class="tl-phase" data-i="' + i + '" style="--d:' + (0.35 + i * 0.45) + 's"><span class="tl-dot" aria-hidden="true"></span><small>' + esc(p.label) + '</small><b>' + esc(p.title) + '</b></button>'; });
    host.innerHTML = h + '</div><div class="fig-detail" aria-live="polite"></div>';
    var show = detail(host);
    function pick(i) {
      Array.prototype.forEach.call(host.querySelectorAll('.tl-phase'), function (x, k) { x.classList.toggle('is-on', k === i); });
      show(P[i].label + ': ' + P[i].title, '', '<ul>' + P[i].items.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>');
    }
    host.addEventListener('click', function (e) { var b = e.target.closest('.tl-phase'); if (b) pick(+b.getAttribute('data-i')); });
    host.querySelector('.fig-timeline').classList.add('play');
    pick(0);
  }

  /* ---------------- bars ---------------- */
  function bars(host, c) {
    var max = Math.max.apply(null, c.items.map(function (x) { return x.value; })), total = c.items.reduce(function (a, x) { return a + x.value; }, 0);
    var h = '<div class="fig-bars">';
    c.items.forEach(function (x, i) {
      var w = (x.value / max * 100).toFixed(1);
      h += '<div class="bar-row' + (x.highlight ? ' is-hl' : '') + '"><span class="bar-label">' + esc(x.label) + '</span><span class="bar-track"><span class="bar-fill" style="--w:' + w + '%;--d:' + (i * 0.12) + 's"></span></span><span class="bar-val">' + esc(fmt(x.value)) + ' ' + esc(c.unit) + '</span></div>';
    });
    h += '</div><div class="btn-row" style="margin-top:12px;align-items:center"><button type="button" class="btn btn-ghost fig-replay">Replay</button><span class="muted" style="font-size:14px">Total: ' + esc(fmt(total)) + ' ' + esc(c.unit) + '</span></div>';
    if (c.note) h += '<p class="fig-note">' + esc(c.note) + '</p>';
    host.innerHTML = h;
    host.querySelector('.fig-bars').classList.add('play');
    host.addEventListener('click', function (e) { if (e.target.closest('.fig-replay')) { var b = host.querySelector('.fig-bars'); b.classList.remove('play'); void b.offsetWidth; b.classList.add('play'); } });
  }
  function fmt(v) { return Number(v).toLocaleString('en-CA', { maximumFractionDigits: 1 }); }

  var TYPES = { cycle: cycle, flow: flow, stack: stack, compare: compare, timeline: timeline, bars: bars };
  window.ChmFig = {
    render: function (host, fig) {
      if (!host || host.getAttribute('data-ready')) return;
      var fn = TYPES[fig.type]; if (!fn) return;
      host.setAttribute('data-ready', '1');
      try { fn(host, fig.config); } catch (e) { host.removeAttribute('data-ready'); if (window.console) console.error('Figure failed', fig, e); }
    }
  };
})();
