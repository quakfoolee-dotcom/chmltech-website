/* Chmltech free course player (V4). Lessons are static HTML; labs, exam and progress are driven here. */
(function () {
  'use strict';
  var root = document.querySelector('[data-course]');
  if (!root) return;
  var DATA = JSON.parse(document.getElementById('course-data').textContent);
  var KEY = 'chmltech-course-' + DATA.id;
  var TOTAL = DATA.total_steps;
  var PASS = 0.7;

  /* ---------- progress (browser storage, optional) ---------- */
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* storage unavailable: progress lasts for this visit */ } }
  var state = load();
  state.done = state.done || []; state.labs = state.labs || {}; state.exam = state.exam || {};

  var views = Array.prototype.slice.call(root.querySelectorAll('[data-view]'));
  var outlineLinks = Array.prototype.slice.call(document.querySelectorAll('[data-goto]'));

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) { if (k === 'text') e.textContent = attrs[k]; else e.setAttribute(k, attrs[k]); }
    if (html) e.innerHTML = html;
    return e;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function refreshProgress() {
    var n = state.done.length, pct = Math.round(100 * n / TOTAL);
    Array.prototype.forEach.call(document.querySelectorAll('[data-progress-bar]'), function (b) { b.style.width = pct + '%'; });
    Array.prototype.forEach.call(document.querySelectorAll('[data-progress-text]'), function (t) { t.textContent = n + ' of ' + TOTAL + ' lessons complete (' + pct + '%)'; });
    outlineLinks.forEach(function (a) {
      var g = a.getAttribute('data-goto'), m = g.match(/^step-(\d+)$/), done = false;
      if (m) done = state.done.indexOf(+m[1]) !== -1;
      else if (g.indexOf('lab-') === 0) done = !!state.labs[g.slice(4)];
      else if (g === 'exam') done = !!state.exam.passed;
      a.classList.toggle('is-done', done);
    });
    var cont = document.querySelector('[data-continue]');
    if (cont) {
      var next = 1; while (state.done.indexOf(next) !== -1 && next <= TOTAL) next++;
      if (next > TOTAL) { cont.textContent = state.exam.passed ? 'View your certificate' : 'Take the final exam'; cont.setAttribute('href', state.exam.passed ? '#certificate' : '#exam'); }
      else { cont.textContent = n ? 'Continue: lesson ' + next : 'Start the course'; cont.setAttribute('href', '#step-' + next); }
    }
  }

  /* ---------- routing ---------- */
  function show(id) {
    if (!id || !root.querySelector('[data-view="' + id + '"]')) id = 'overview';
    if (id === 'certificate' && !state.exam.passed) id = 'exam';
    views.forEach(function (v) { v.hidden = v.getAttribute('data-view') !== id; });
    outlineLinks.forEach(function (a) { a.classList.toggle('is-current', a.getAttribute('data-goto') === id); if (a.getAttribute('data-goto') === id) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current'); });
    var view = root.querySelector('[data-view="' + id + '"]');
    if (id.indexOf('lab-') === 0) initLab(id.slice(4), view);
    if (window.ChmFig && DATA.figures) Array.prototype.forEach.call(view.querySelectorAll('.cfig'), function (f) {
      f.setAttribute('data-ready-host', '1');
      window.ChmFig.render(f.querySelector('.fig-host'), DATA.figures[+f.getAttribute('data-fig')]);
    });
    if (id === 'exam') initExam(view);
    if (id === 'certificate') initCert(view);
    var outline = document.querySelector('.course-outline details'); if (outline && window.innerWidth < 1000) outline.open = false;
    var top = root.getBoundingClientRect().top + window.pageYOffset - 90;
    if (window.pageYOffset > top) window.scrollTo(0, top);
    var h = view.querySelector('h2'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  }
  window.addEventListener('hashchange', function () { show(location.hash.slice(1)); });

  /* ---------- lessons: knowledge checks + completion ---------- */
  Array.prototype.forEach.call(root.querySelectorAll('.kcheck'), function (box) {
    var btn = box.querySelector('button'), fb = box.querySelector('.kcheck-feedback');
    var answer = +box.getAttribute('data-answer');
    btn.addEventListener('click', function () {
      var picked = box.querySelector('input:checked');
      if (!picked) { fb.className = 'kcheck-feedback err'; fb.textContent = 'Choose an answer first.'; return; }
      var ok = +picked.value === answer;
      Array.prototype.forEach.call(box.querySelectorAll('label'), function (l, i) { l.classList.toggle('is-right', i === answer); l.classList.toggle('is-wrong', i === +picked.value && !ok); });
      fb.className = 'kcheck-feedback ' + (ok ? 'ok' : 'err');
      fb.innerHTML = '<strong>' + (ok ? 'Correct. ' : 'Not quite. ') + '</strong>' + esc(box.getAttribute('data-why'));
    });
  });
  Array.prototype.forEach.call(root.querySelectorAll('[data-complete]'), function (a) {
    a.addEventListener('click', function () {
      var n = +a.getAttribute('data-complete');
      if (state.done.indexOf(n) === -1) { state.done.push(n); save(); refreshProgress(); }
    });
  });
  var reset = document.querySelector('[data-reset]');
  if (reset) reset.addEventListener('click', function () { state = { done: [], labs: {}, exam: {} }; save(); refreshProgress(); location.hash = '#overview'; });

  /* ---------- labs ---------- */
  var labsInit = {};
  function labConf(id) { for (var i = 0; i < DATA.labs.length; i++) if (DATA.labs[i].id === id) return DATA.labs[i]; return null; }
  function markLab(id) { state.labs[id] = true; save(); refreshProgress(); }
  function initLab(id, view) {
    if (labsInit[id]) return; labsInit[id] = true;
    var L = labConf(id), host = view.querySelector('[data-lab-host]');
    if (!L || !host) return;
    ({ assessment: labAssessment, matrix: labMatrix, classify: labClassify, calc: labCalc })[L.type](L, host);
  }

  function radar(dims, scores) {
    var n = dims.length, cx = 210, cy = 200, R = 140, s = '';
    function pt(i, r) { var a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; }
    for (var lv = 1; lv <= 5; lv++) {
      var ring = []; for (var i = 0; i < n; i++) ring.push(pt(i, R * lv / 5).join(','));
      s += '<polygon points="' + ring.join(' ') + '" fill="none" stroke="#D9D5CA" stroke-width="1"/>';
    }
    var poly = [];
    for (var j = 0; j < n; j++) {
      var p = pt(j, R), q = pt(j, R * scores[j] / 5), lab = pt(j, R + 26);
      s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + p[0] + '" y2="' + p[1] + '" stroke="#D9D5CA"/>';
      poly.push(q.join(','));
      var anchor = Math.abs(lab[0] - cx) < 10 ? 'middle' : (lab[0] > cx ? 'start' : 'end');
      s += '<text x="' + lab[0] + '" y="' + (lab[1] + 4) + '" text-anchor="' + anchor + '" class="radar-label">' + esc(dims[j].name) + '</text>';
    }
    s += '<polygon points="' + poly.join(' ') + '" fill="rgba(11,111,164,.22)" stroke="#0B6FA4" stroke-width="2.5"/>';
    poly.forEach(function (p) { var c = p.split(','); s += '<circle cx="' + c[0] + '" cy="' + c[1] + '" r="4" fill="#0B6FA4"/>'; });
    return '<svg viewBox="-110 0 640 400" role="img" aria-label="Radar chart of your scores">' + s + '</svg>';
  }

  function labAssessment(L, host) {
    var c = L.config, scores = c.dimensions.map(function () { return 3; });
    var form = el('div', { class: 'lab-form' });
    c.dimensions.forEach(function (d, i) {
      var f = el('fieldset', { class: 'lab-field' });
      f.innerHTML = '<legend><strong>' + esc(d.name) + '</strong><span>' + esc(d.question) + '</span></legend>';
      var row = el('div', { class: 'scale-row' });
      c.scale.forEach(function (lbl, k) {
        var id = L.id + '-d' + i + '-' + k;
        row.innerHTML += '<input type="radio" name="' + L.id + '-d' + i + '" id="' + id + '" value="' + (k + 1) + '"' + (k === 2 ? ' checked' : '') + '><label for="' + id + '" title="' + esc(lbl) + '"><b>' + (k + 1) + '</b><span>' + esc(lbl) + '</span></label>';
      });
      f.appendChild(row); form.appendChild(f);
    });
    var out = el('div', { class: 'lab-visual' });
    host.appendChild(form); host.appendChild(out);
    function render() {
      var avg = scores.reduce(function (a, b) { return a + b; }, 0) / scores.length;
      var level = c.scale[Math.min(4, Math.max(0, Math.round(avg) - 1))];
      var low = [], high = [];
      c.dimensions.forEach(function (d, i) { if (scores[i] <= 2) low.push(d); else if (scores[i] >= 4) high.push(d); });
      var html = radar(c.dimensions, scores) +
        '<div class="metric-row"><div class="metric"><span>Average score</span><strong>' + avg.toFixed(1) + ' / 5</strong></div><div class="metric"><span>Overall maturity</span><strong>' + esc(level) + '</strong></div></div>';
      if (low.length) html += '<h4>Priorities to strengthen</h4><ul>' + low.map(function (d) { return '<li><strong>' + esc(d.name) + ':</strong> ' + esc(d.low) + '</li>'; }).join('') + '</ul>';
      if (high.length) html += '<h4>Strengths to build on</h4><ul>' + high.map(function (d) { return '<li><strong>' + esc(d.name) + ':</strong> ' + esc(d.high) + '</li>'; }).join('') + '</ul>';
      if (!low.length && !high.length) html += '<p class="muted">Adjust the scores to reflect your organization honestly; areas scored 1–2 become your priorities.</p>';
      out.innerHTML = html;
    }
    form.addEventListener('change', function (e) {
      var m = e.target.name.match(/-d(\d+)$/); if (!m) return;
      scores[+m[1]] = +e.target.value; render(); markLab(L.id);
    });
    render();
  }

  function labMatrix(L, host) {
    var c = L.config, items = c.items.map(function (it) { return { name: it.name, x: it.x, y: it.y }; });
    var form = el('div', { class: 'lab-form' }), out = el('div', { class: 'lab-visual' });
    host.appendChild(form); host.appendChild(out);
    function sel(val, axis, i) {
      var s = '<select data-i="' + i + '" data-axis="' + axis + '" aria-label="' + esc(axis === 'x' ? c.x : c.y) + ' score">';
      for (var k = 1; k <= 5; k++) s += '<option' + (k === val ? ' selected' : '') + '>' + k + '</option>';
      return s + '</select>';
    }
    function renderForm() {
      var h = '<table class="matrix-table"><thead><tr><th>Item</th><th>' + esc(c.x) + ' (1–5)</th><th>' + esc(c.y) + ' (1–5)</th><th><span class="visually-hidden">Remove</span></th></tr></thead><tbody>';
      items.forEach(function (it, i) {
        h += '<tr><td><input type="text" data-i="' + i + '" data-axis="name" value="' + esc(it.name) + '" aria-label="Item name"></td><td>' + sel(it.x, 'x', i) + '</td><td>' + sel(it.y, 'y', i) + '</td><td><button type="button" class="icon-btn" data-remove="' + i + '" aria-label="Remove ' + esc(it.name) + '">×</button></td></tr>';
      });
      h += '</tbody></table><button type="button" class="btn btn-ghost" data-add>Add an item</button>';
      form.innerHTML = h;
    }
    // Midpoint is 3 on both axes; a 3 counts as low effort (left) and high value (top).
    function quadrant(it) { return (it.y >= 3 ? 'top' : 'bottom') + '_' + (it.x <= 3 ? 'left' : 'right'); }
    function renderPlot() {
      var W = 420, P = 40, s = '<svg viewBox="0 0 ' + (W + 60) + ' ' + (W + 50) + '" role="img" aria-label="Two-by-two matrix of your items">';
      var x0 = P + 20, y0 = 10, S = W - P;
      s += '<rect x="' + x0 + '" y="' + y0 + '" width="' + S + '" height="' + S + '" fill="#fff" stroke="#D9D5CA"/>';
      s += '<rect x="' + x0 + '" y="' + y0 + '" width="' + S / 2 + '" height="' + S / 2 + '" fill="rgba(141,198,63,.12)"/>';
      s += '<line x1="' + (x0 + S / 2) + '" y1="' + y0 + '" x2="' + (x0 + S / 2) + '" y2="' + (y0 + S) + '" stroke="#B9C0CC" stroke-dasharray="4 4"/><line x1="' + x0 + '" y1="' + (y0 + S / 2) + '" x2="' + (x0 + S) + '" y2="' + (y0 + S / 2) + '" stroke="#B9C0CC" stroke-dasharray="4 4"/>';
      var q = c.quadrants;
      s += '<text class="q-label" x="' + (x0 + 10) + '" y="' + (y0 + 22) + '">' + esc(q.top_left) + '</text><text class="q-label" x="' + (x0 + S - 10) + '" y="' + (y0 + 22) + '" text-anchor="end">' + esc(q.top_right) + '</text>';
      s += '<text class="q-label" x="' + (x0 + 10) + '" y="' + (y0 + S - 12) + '">' + esc(q.bottom_left) + '</text><text class="q-label" x="' + (x0 + S - 10) + '" y="' + (y0 + S - 12) + '" text-anchor="end">' + esc(q.bottom_right) + '</text>';
      s += '<text class="axis-label" x="' + (x0 + S / 2) + '" y="' + (y0 + S + 34) + '" text-anchor="middle">' + esc(c.x) + ' → (' + esc(c.x_low) + ' to ' + esc(c.x_high) + ')</text>';
      s += '<text class="axis-label" transform="translate(' + (x0 - 22) + ',' + (y0 + S / 2) + ') rotate(-90)" text-anchor="middle">' + esc(c.y) + ' → (' + esc(c.y_low) + ' to ' + esc(c.y_high) + ')</text>';
      var seen = {};
      items.forEach(function (it, i) {
        var k = it.x + '-' + it.y; seen[k] = (seen[k] || 0) + 1; var off = (seen[k] - 1) * 9;
        var px = x0 + (it.x - 0.5) / 5 * S + off, py = y0 + S - (it.y - 0.5) / 5 * S + off * 0.4;
        s += '<circle cx="' + px + '" cy="' + py + '" r="13" fill="#0B6FA4"/><text x="' + px + '" y="' + (py + 4.5) + '" text-anchor="middle" class="dot-num">' + (i + 1) + '</text>';
      });
      s += '</svg>';
      var groups = { top_left: [], top_right: [], bottom_left: [], bottom_right: [] };
      items.forEach(function (it, i) { groups[quadrant(it)].push((i + 1) + '. ' + esc(it.name)); });
      var lists = ['top_left', 'top_right', 'bottom_left', 'bottom_right'].map(function (k) { return '<div class="q-list"><strong>' + esc(q[k]) + '</strong><span>' + (groups[k].join('<br>') || '—') + '</span></div>'; }).join('');
      out.innerHTML = s + '<div class="q-lists">' + lists + '</div>';
    }
    form.addEventListener('change', function (e) {
      var i = e.target.getAttribute('data-i'), ax = e.target.getAttribute('data-axis'); if (i === null) return;
      items[+i][ax] = ax === 'name' ? e.target.value : +e.target.value; renderPlot(); markLab(L.id);
    });
    form.addEventListener('click', function (e) {
      if (e.target.hasAttribute('data-add')) { items.push({ name: 'New item ' + (items.length + 1), x: 3, y: 3 }); renderForm(); renderPlot(); }
      var r = e.target.getAttribute('data-remove'); if (r !== null) { items.splice(+r, 1); renderForm(); renderPlot(); }
    });
    renderForm(); renderPlot();
  }

  function labClassify(L, host) {
    var c = L.config, picks = {};
    var wrap = el('div', { class: 'classify' });
    c.items.forEach(function (it, i) {
      var row = el('div', { class: 'classify-row' });
      var opts = c.categories.map(function (cat, k) { return '<button type="button" class="chip" data-i="' + i + '" data-k="' + k + '" aria-pressed="false">' + esc(cat) + '</button>'; }).join('');
      row.innerHTML = '<p class="classify-text"><b>' + (i + 1) + '.</b> ' + esc(it.text) + '</p><div class="classify-opts" role="group" aria-label="Category for item ' + (i + 1) + '">' + opts + '</div><p class="classify-why" hidden></p>';
      wrap.appendChild(row);
    });
    var bar = el('div', { class: 'btn-row', style: 'margin-top:20px;align-items:center' });
    bar.innerHTML = '<button type="button" class="btn" data-check>Check my answers</button><button type="button" class="btn btn-ghost" data-retry>Start again</button><span class="lab-score" aria-live="polite"></span>';
    host.appendChild(wrap); host.appendChild(bar);
    wrap.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-k]'); if (!b) return;
      var i = b.getAttribute('data-i'); picks[i] = +b.getAttribute('data-k');
      Array.prototype.forEach.call(wrap.querySelectorAll('button[data-i="' + i + '"]'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    });
    bar.querySelector('[data-check]').addEventListener('click', function () {
      var right = 0;
      c.items.forEach(function (it, i) {
        var row = wrap.children[i], why = row.querySelector('.classify-why'), p = picks[i];
        var ok = p === it.answer; if (ok) right++;
        row.classList.toggle('is-right', ok); row.classList.toggle('is-wrong', p !== undefined && !ok);
        why.hidden = false;
        why.innerHTML = (p === undefined ? '<strong>Not answered.</strong> ' : (ok ? '<strong>Correct.</strong> ' : '<strong>Answer: ' + esc(c.categories[it.answer]) + '.</strong> ')) + esc(it.why);
      });
      bar.querySelector('.lab-score').textContent = 'You got ' + right + ' of ' + c.items.length + ' right.';
      markLab(L.id);
    });
    bar.querySelector('[data-retry]').addEventListener('click', function () {
      picks = {};
      Array.prototype.forEach.call(wrap.children, function (row) { row.classList.remove('is-right', 'is-wrong'); row.querySelector('.classify-why').hidden = true; });
      Array.prototype.forEach.call(wrap.querySelectorAll('button[data-k]'), function (x) { x.setAttribute('aria-pressed', 'false'); });
      bar.querySelector('.lab-score').textContent = '';
    });
  }

  var CALCS = {
    automation_roi: {
      inputs: [['hours', 'Manual hours per week on this task', 20, 1], ['rate', 'Loaded hourly cost (CA$)', 45, 1], ['pct', 'Share of the work automated (%)', 60, 1], ['build', 'One-time build cost (CA$)', 12000, 100], ['run', 'Monthly running cost (CA$)', 150, 10]],
      calc: function (v) {
        var saved = v.hours * 52 * v.pct / 100, gross = saved * v.rate, net = gross - v.run * 12;
        var payback = net > 0 ? v.build / (net / 12) : Infinity, roi3 = v.build > 0 ? ((net * 3 - v.build) / v.build) * 100 : 0;
        return [['Hours freed per year', fmt(saved, 0)], ['Annual net savings', money(net)], ['Payback period', isFinite(payback) ? fmt(payback, 1) + ' months' : 'Not reached'], ['3-year ROI', fmt(roi3, 0) + '%']];
      }
    },
    oee: {
      inputs: [['planned', 'Planned production time (minutes)', 480, 1], ['down', 'Unplanned downtime (minutes)', 45, 1], ['cycle', 'Ideal cycle time (seconds per unit)', 30, 0.1], ['total', 'Total units produced', 750, 1], ['good', 'Good units (first pass)', 720, 1]],
      calc: function (v) {
        var run = Math.max(0, v.planned - v.down), A = v.planned ? run / v.planned : 0;
        var P = run ? Math.min(1, (v.cycle * v.total / 60) / run) : 0, Q = v.total ? Math.min(1, v.good / v.total) : 0, O = A * P * Q;
        return [['Availability', pct(A)], ['Performance', pct(P)], ['Quality', pct(Q)], ['OEE', pct(O)]];
      }
    },
    evm: {
      inputs: [['bac', 'Budget at completion (CA$)', 120000, 100], ['planned', 'Planned % complete to date', 50, 1], ['actual', 'Actual % complete to date', 40, 1], ['ac', 'Actual cost to date (CA$)', 65000, 100]],
      calc: function (v) {
        var PV = v.bac * v.planned / 100, EV = v.bac * v.actual / 100, CV = EV - v.ac, SV = EV - PV;
        var CPI = v.ac ? EV / v.ac : 0, SPI = PV ? EV / PV : 0, EAC = CPI ? v.bac / CPI : 0;
        return [['Planned value (PV)', money(PV)], ['Earned value (EV)', money(EV)], ['Cost variance (CV)', money(CV)], ['Schedule variance (SV)', money(SV)], ['CPI', fmt(CPI, 2) + (CPI && CPI < 1 ? ' (over budget)' : ' (on/under budget)')], ['SPI', fmt(SPI, 2) + (SPI && SPI < 1 ? ' (behind schedule)' : ' (on/ahead of schedule)')], ['Estimate at completion', money(EAC)]];
      }
    },
    llm_cost: {
      inputs: [['req', 'Requests per working day', 500, 1], ['tin', 'Input tokens per request (prompt + context)', 1500, 10], ['tout', 'Output tokens per request', 400, 10], ['pin', 'Price per million input tokens ($, check your provider)', 3, 0.01], ['pout', 'Price per million output tokens ($, check your provider)', 15, 0.01], ['days', 'Working days per month', 21, 1]],
      calc: function (v) {
        var reqs = v.req * v.days, tin = reqs * v.tin, tout = reqs * v.tout;
        var cost = tin / 1e6 * v.pin + tout / 1e6 * v.pout, per = reqs ? cost / reqs : 0;
        return [['Requests per month', fmt(reqs, 0)], ['Tokens per month', fmt((tin + tout) / 1e6, 1) + ' million'], ['Cost per request', '$' + fmt(per, 4)], ['Estimated monthly cost', cost < 1000 ? '$' + fmt(cost, 2) : money(cost)]];
      }
    },
    search_waste: {
      inputs: [['people', 'Number of people', 12, 1], ['mins', 'Minutes per person per day searching or walking for items', 20, 1], ['days', 'Working days per year', 230, 1], ['rate', 'Loaded hourly cost (CA$)', 40, 1]],
      calc: function (v) {
        var hrs = v.people * v.mins * v.days / 60, cost = hrs * v.rate;
        return [['Hours lost per year', fmt(hrs, 0)], ['Cost per year', money(cost)], ['Equivalent full-time staff', fmt(hrs / (7.5 * v.days || 1), 2)], ['Saving if cut by half', money(cost / 2)]];
      }
    }
  };
  function fmt(n, d) { return (Math.round(n * Math.pow(10, d)) / Math.pow(10, d)).toLocaleString('en-CA', { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function money(n) { return (n < 0 ? '-$' : '$') + fmt(Math.abs(n), 0); }
  function pct(x) { return fmt(x * 100, 1) + '%'; }

  function labCalc(L, host) {
    var C = CALCS[L.config.calc]; if (!C) return;
    var form = el('div', { class: 'lab-form calc-form' }), out = el('div', { class: 'lab-visual' });
    C.inputs.forEach(function (inp) {
      var id = L.id + '-' + inp[0];
      form.innerHTML += '<div class="field"><label for="' + id + '">' + esc(inp[1]) + '</label><input id="' + id + '" type="number" min="0" step="' + inp[3] + '" value="' + inp[2] + '" data-k="' + inp[0] + '"></div>';
    });
    host.appendChild(form); host.appendChild(out);
    function render() {
      var v = {}; Array.prototype.forEach.call(form.querySelectorAll('input'), function (i) { v[i.getAttribute('data-k')] = parseFloat(i.value) || 0; });
      var res = C.calc(v);
      out.innerHTML = '<div class="metric-grid">' + res.map(function (r, i) { return '<div class="metric' + (i === res.length - 1 ? ' metric-key' : '') + '"><span>' + esc(r[0]) + '</span><strong>' + esc(r[1]) + '</strong></div>'; }).join('') + '</div>' +
        (L.config.note ? '<p class="lab-note">' + esc(L.config.note) + '</p>' : '');
    }
    form.addEventListener('input', function () { render(); markLab(L.id); });
    render();
  }

  /* ---------- final exam ---------- */
  var examBuilt = false;
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function initExam(view) {
    var host = view.querySelector('[data-exam-host]'); if (!host) return;
    if (examBuilt) return; examBuilt = true; buildExam(host);
  }
  function buildExam(host) {
    var order = shuffle(DATA.exam.map(function (_, i) { return i; }));
    var h = '<form class="exam-form" novalidate>';
    order.forEach(function (qi, n) {
      var q = DATA.exam[qi];
      h += '<fieldset class="exam-q" data-q="' + qi + '"><legend><b>' + (n + 1) + '.</b> ' + esc(q.q) + '</legend>';
      q.opts.forEach(function (o, k) { var id = 'ex-' + qi + '-' + k; h += '<label for="' + id + '"><input type="radio" name="ex-' + qi + '" id="' + id + '" value="' + k + '"> ' + esc(o) + '</label>'; });
      h += '<p class="exam-why" hidden></p></fieldset>';
    });
    h += '<div class="btn-row" style="align-items:center"><button class="btn" type="submit">Submit exam</button><span class="exam-msg" aria-live="polite"></span></div></form><div class="exam-result" aria-live="polite"></div>';
    host.innerHTML = h;
    var form = host.querySelector('form'), result = host.querySelector('.exam-result');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var unanswered = DATA.exam.filter(function (_, qi) { return !form.querySelector('input[name="ex-' + qi + '"]:checked'); }).length;
      if (unanswered) { form.querySelector('.exam-msg').textContent = unanswered + ' question' + (unanswered > 1 ? 's' : '') + ' still unanswered.'; return; }
      var right = 0;
      Array.prototype.forEach.call(form.querySelectorAll('.exam-q'), function (fs) {
        var qi = +fs.getAttribute('data-q'), q = DATA.exam[qi], p = +form.querySelector('input[name="ex-' + qi + '"]:checked').value, ok = p === q.a;
        if (ok) right++;
        fs.classList.toggle('is-right', ok); fs.classList.toggle('is-wrong', !ok);
        var why = fs.querySelector('.exam-why'); why.hidden = ok;
        if (!ok) why.innerHTML = '<strong>Correct answer: ' + esc(q.opts[q.a]) + '.</strong> ' + esc(q.why);
        Array.prototype.forEach.call(fs.querySelectorAll('input'), function (i) { i.disabled = true; });
      });
      var score = right / DATA.exam.length, passed = score >= PASS;
      state.exam.best = Math.max(state.exam.best || 0, right); if (passed) { state.exam.passed = true; state.exam.date = state.exam.date || new Date().toISOString().slice(0, 10); }
      save(); refreshProgress();
      form.querySelector('[type=submit]').hidden = true; form.querySelector('.exam-msg').textContent = '';
      result.innerHTML = '<div class="exam-score ' + (passed ? 'pass' : 'fail') + '"><strong>' + right + ' / ' + DATA.exam.length + ' (' + Math.round(score * 100) + '%)</strong><span>' +
        (passed ? 'You passed. Well done!' : 'The pass mark is ' + Math.round(PASS * 100) + '%. Review the explanations above, then try again.') + '</span>' +
        '<div class="btn-row">' + (passed ? '<a class="btn" href="#certificate">Get your certificate</a>' : '') + '<button type="button" class="btn btn-ghost" data-retake>Retake the exam</button></div></div>';
      result.querySelector('[data-retake]').addEventListener('click', function () { buildExam(host); window.scrollTo(0, host.getBoundingClientRect().top + window.pageYOffset - 120); });
      result.scrollIntoView({ block: 'center' });
    });
  }

  /* ---------- certificate ---------- */
  function initCert(view) {
    var input = view.querySelector('[data-cert-name]'), nameEl = view.querySelector('[data-cert-out-name]'), dateEl = view.querySelector('[data-cert-date]');
    if (state.exam.name) input.value = state.exam.name;
    var idEl = view.querySelector('[data-cert-id]'), cert = view.querySelector('.certificate');
    var d = state.exam.date ? new Date(state.exam.date + 'T12:00:00') : new Date();
    var ymd = state.exam.date || d.toISOString().slice(0, 10);
    // Course code from the certificate's course title: initials of the main words (before any colon), e.g. LLMBL.
    var titleEl = view.querySelector('.cert-course'), title = (titleEl ? titleEl.textContent : DATA.id).split(':')[0].replace(/\([^)]*\)/g, ' ');
    var code = title.split(/[\s-]+/).filter(function (w) { return w && !/^(for|and|the|of|via|your|a|an|to|in|&)$/i.test(w); })
      .map(function (w) { return w.charAt(0); }).join('').toUpperCase().slice(0, 5) || 'CRS';
    // Certificate number: CHM-<course initials>-<2-digit year>-<6-character check code from course + name + date>.
    function certId(name) {
      var s = DATA.id + '|' + name.toLowerCase().replace(/\s+/g, ' ') + '|' + ymd, h = 2166136261;
      for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
      return 'CHM-' + code + '-' + ymd.slice(2, 4) + '-' + ('000000' + h.toString(36).toUpperCase()).slice(-6);
    }
    function upd() {
      var name = input.value.trim();
      nameEl.textContent = name || 'Your name'; state.exam.name = name; save();
      if (idEl) idEl.textContent = name ? certId(name) : 'CHM-' + code + '-' + ymd.slice(2, 4) + '-······';
    }
    dateEl.textContent = d.toLocaleDateString('en-CA', { year: 'numeric', month: 'long', day: 'numeric' });
    input.oninput = upd; upd();
    // Printing: copy the certificate into a top-level holder so the print stylesheet can hide the rest of the
    // page entirely (one page, not several). Runs for the button and for Ctrl/Cmd+P.
    function preparePrint() {
      if (!cert || location.hash !== '#certificate') return;
      var holder = document.getElementById('cert-print');
      if (!holder) { holder = document.createElement('div'); holder.id = 'cert-print'; document.body.appendChild(holder); }
      holder.innerHTML = ''; holder.appendChild(cert.cloneNode(true));
      document.documentElement.classList.add('cert-printing');
    }
    if (!initCert.bound) {
      window.addEventListener('beforeprint', preparePrint);
      window.addEventListener('afterprint', function () { document.documentElement.classList.remove('cert-printing'); });
      initCert.bound = true;
    }
    view.querySelector('[data-print]').onclick = function () { preparePrint(); window.print(); };
  }

  refreshProgress();
  show(location.hash.slice(1) || 'overview');
  root.classList.add('ready');
})();
