/* Digital Assessment page — V28 (funding links open the Funding Match); V26 (PDF emailed via report service; branded PDF report with logo; full report in the email; V7 + V10 independent-review fixes, V15 UI clean-up, vendor directory and AI tools).
   Data: #assess-data (content/assess/assess_data.json, built by content/assess/build_data_v3.py).
   Every Software Finder category is a capability matrix; ERP adds a workflow selector. */
(function () {
  'use strict';
  var A = JSON.parse(document.getElementById('assess-data').textContent);
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function by(arr) { var o = {}; arr.forEach(function (x) { o[x.id] = x; }); return o; }
  var IND = by(A.industries), FN = by(A.functions), CAT = by(A.categories), PRB = by(A.problems), PRI = by(A.priorities), WF = by(A.erp.workflows);
  var PRICE = ['', 'Under $25K', '$25K–$100K', '$100K–$300K', 'Over $300K'];
  var SIZE = { s: 'Small teams', m: 'Mid-size firms', l: 'Larger firms' };
  var LEVEL = ['Not offered', 'Add-on', 'Set up without code', 'Built in'];
  var STAFF = { xs: ['s'], sm: ['s', 'm'], md: ['m'], lg: ['m', 'l'] };
  function dollars(n) { return '<span title="Indicative first-year total cost: ' + PRICE[n] + '">' + '$$$$'.slice(0, n) + '</span>'; }
  function dot(v) { return v == null ? '<span class="dot na">n/a</span>' : '<span class="dot s' + v + '" title="' + LEVEL[v] + '" aria-label="' + LEVEL[v] + '"></span>'; }
  function avgFit(s) { if (!s) return null; var t = 0; s.forEach(function (x) { t += x; }); return Math.round(t / (3 * s.length) * 100); }
  function rcText(p) { return typeof p.rc === 'string' ? p.rc : p.rc.hidden; }

  /* ---------- category model: products, capabilities and scores for any category ---------- */
  function products(cid) {
    if (cid === 'erp') return A.erp.vendors;
    if (cid === 'wms') return A.wms.vendors;
    return A.products.filter(function (p) { return p.cat === cid; });
  }
  function caps(cid, wf) { return cid === 'erp' ? WF[wf].caps : CAT[cid].caps; }
  function scores(p, cid, wf) { return cid === 'erp' ? p.s[wf] : cid === 'wms' ? p.s.wm : p.s; }
  function typeLabel(p, cid) { return cid === 'erp' ? p.type : cid === 'wms' ? p.tag : (p.ca ? 'Canadian company' : ''); }
  function catFitsInd(cid, ind) { return products(cid).some(function (p) { return p.inds.indexOf(ind) >= 0; }); }

  /* ================= Assessment ================= */
  var STEPS = ['Your business', 'Priorities', 'Challenges', 'Digital maturity', 'Budget'];
  var SCREENS = [
    { k: 'ind', st: 0, q: 'Which industry best describes your business?', o: function () { return A.industries.map(function (i) { return [i.id, i.name, i.desc]; }); } },
    { k: 'sub', st: 0, q: '', qf: function () { return A.subtypes[ans.ind].q; }, when: function () { var t = A.subtypes[ans.ind]; return !!(t && t.q); }, o: function () { return A.subtypes[ans.ind].o; } },
    { k: 'size', st: 0, q: 'How many people work in the business?', o: function () { return [['xs', 'Fewer than 10'], ['sm', '10 to 49'], ['md', '50 to 99'], ['lg', '100 to 499']]; } },
    { k: 'tools', st: 0, q: 'What do you run the business on today?', hint: 'Pick all that apply.', max: 9, o: function () {
      return [['paper', 'Paper, whiteboards and memory'], ['sheets', 'Spreadsheets'], ['acct', 'Accounting software (QuickBooks, Sage, Xero)'], ['crm', 'A CRM'], ['erp', 'An ERP, MRP or inventory system'], ['ind', 'An industry app (job, clinic, POS, property or fleet software)'], ['m365', 'Microsoft 365'], ['gws', 'Google Workspace'], ['ai', 'AI tools such as ChatGPT, Claude, Copilot or Gemini']]; } },
    { k: 'prio', st: 1, q: 'What are your top business priorities for the next 2–3 years?', hint: 'Pick up to three.', max: 3, o: function () { return A.priorities.map(function (p) { return [p.id, p.name]; }); } },
    { k: 'prob', st: 2, q: 'Which of these problems do you face today?', hint: 'Pick up to five. They are grouped by business function.', max: 5, group: true },
    { k: 'mat', st: 3, q: 'Where is each part of your business today, and where should it be in two years?', custom: 'mat' },
    { k: 'budget', st: 4, q: 'What could you invest in your first digital project, including set-up?', o: function () { return [['1', 'Under $25,000'], ['2', '$25,000 to $100,000'], ['3', '$100,000 to $300,000'], ['4', 'Over $300,000']]; } }
  ];
  var ans = {}, idx = 0;
  var intro = $('#as-intro'), quiz = $('#as-quiz'), result = $('#as-result'), qbox = $('#as-qbox'), next = $('#as-next'), back = $('#as-back');
  function visible() { return SCREENS.filter(function (s) { return !s.when || s.when(); }); }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-as]'); if (!t) return;
    var a = t.dataset.as;
    if (a === 'start' || a === 'restart') { e.preventDefault(); ans = {}; idx = 0; intro.hidden = true; result.hidden = true; quiz.hidden = false; show(); $('#assessment').scrollIntoView({ behavior: 'smooth' }); }
    if (a === 'print') {
      var lbl = t.textContent; t.disabled = true; t.textContent = 'Preparing PDF…';
      makePdf().then(function (o) { o.doc.save(o.file); }).catch(function () {
        document.body.classList.add('erp-printing'); window.print(); setTimeout(function () { document.body.classList.remove('erp-printing'); }, 500);
      }).then(function () { t.disabled = false; t.textContent = lbl; });
    }
  });
  function show() {
    var list = visible(), s = list[idx];
    $('#as-steps').innerHTML = STEPS.map(function (n, i) { return '<li class="' + (i === s.st ? 'on' : i < s.st ? 'done' : '') + '">' + (i + 1) + '. ' + n + '</li>'; }).join('');
    $('#as-bar').style.width = (idx / list.length * 100) + '%';
    $('#as-qcount').textContent = 'Question ' + (idx + 1) + ' of ' + list.length;
    var h = '<legend class="finder-qtext h-md" style="font-size:24px">' + esc(s.qf ? s.qf() : s.q) + '</legend>' + (s.hint ? '<p class="erp-qhint">' + esc(s.hint) + '</p>' : '');
    h += s.custom === 'mat' ? matHTML() : s.group ? probHTML() : optsHTML(s, s.o());
    qbox.innerHTML = h;
    back.disabled = idx === 0;
    next.textContent = idx === list.length - 1 ? 'See my roadmap →' : 'Next →';
    update();
  }
  function optsHTML(s, opts) {
    var multi = !!s.max, sel = ans[s.k] || (multi ? [] : '');
    return '<div class="finder-opts">' + opts.map(function (o) {
      var on = multi ? sel.indexOf(o[0]) >= 0 : sel === o[0];
      return '<label class="finder-opt"><input type="' + (multi ? 'checkbox' : 'radio') + '" name="q_' + s.k + '" value="' + o[0] + '"' + (on ? ' checked' : '') + '><span>' + esc(o[1]) + (o[2] ? '<small>' + esc(o[2]) + '</small>' : '') + '</span></label>';
    }).join('') + '</div>';
  }
  function probHTML() {
    var s = SCREENS[5];
    return A.functions.map(function (f) {
      var wf = erpWf(); var ps = A.problems.filter(function (p) { return p.fn === f.id && p.ind.indexOf(ans.ind) >= 0 && (!p.sub || p.sub.indexOf(wf) >= 0); });
      return ps.length ? '<div class="as-group"><h4>' + esc(f.name) + '</h4>' + optsHTML(s, ps.map(function (p) { return [p.id, p.t]; })) + '</div>' : '';
    }).join('');
  }
  function matHTML() {
    var m = ans.mat || {};
    return '<div class="as-levels">' + A.levels.map(function (l, i) { return '<div><b>' + (i + 1) + '. ' + esc(l.n) + '</b>' + esc(l.d) + '</div>'; }).join('') + '</div><div class="as-mat" style="margin-top:14px">' +
      A.functions.map(function (f) {
        var v = m[f.id] || {};
        function seg(kind, cur) {
          return '<div class="as-seg' + (kind === 't' ? ' tgt' : '') + '"><span>' + (kind === 'c' ? 'Today' : 'Target') + '</span>' + A.levels.map(function (l, i) {
            return '<button type="button" data-mat="' + f.id + '" data-kind="' + kind + '" data-lv="' + i + '" aria-pressed="' + (cur === i) + '">' + esc(l.n) + '</button>';
          }).join('') + '</div>';
        }
        var ex = v.c != null ? '<b>Today:</b> ' + esc(A.level_examples[f.id][v.c]) + (v.t != null ? ' &nbsp;→&nbsp; <b>Target:</b> ' + esc(A.level_examples[f.id][v.t]) : '') : 'Pick a level for today and a target.';
        return '<div class="as-matrow"><h4>' + esc(f.name) + '</h4>' + seg('c', v.c) + seg('t', v.t) + '<p class="as-ex">' + ex + '</p></div>';
      }).join('') + '</div>';
  }
  qbox.addEventListener('click', function (e) {
    var b = e.target.closest('[data-mat]'); if (!b) return;
    ans.mat = ans.mat || {};
    var f = b.dataset.mat, k = b.dataset.kind, lv = +b.dataset.lv, v = ans.mat[f] = ans.mat[f] || {};
    v[k] = lv;
    if (k === 'c') { if (v.t == null) v.t = Math.min(3, lv + 1); else if (v.t < lv) v.t = lv; }
    if (k === 't' && v.c != null && lv < v.c) v.t = v.c;
    show();
  });
  qbox.addEventListener('change', function (e) {
    var s = visible()[idx];
    if (s.max) {
      var boxes = $$('input:checked', qbox);
      if (boxes.length > s.max) { e.target.checked = false; boxes = $$('input:checked', qbox); }
      ans[s.k] = boxes.map(function (b) { return b.value; });
    } else { ans[s.k] = e.target.value; if (s.k === 'ind') { delete ans.sub; delete ans.prob; }
      if (s.k === 'sub') { delete ans.prob; } }
    update();
  });
  function update() {
    var s = visible()[idx], ok;
    if (s.custom === 'mat') ok = A.functions.every(function (f) { var v = (ans.mat || {})[f.id]; return v && v.c != null && v.t != null; });
    else { var v = ans[s.k]; ok = !!(v && v.length); }
    next.disabled = !ok;
  }
  back.addEventListener('click', function () { if (idx > 0) { idx--; show(); } });
  next.addEventListener('click', function () { if (idx < visible().length - 1) { idx++; show(); } else finish(); });

  /* ---------- size-aware routing of system tokens ---------- */
  function small() { return ans.size === 'xs' || (ans.size === 'sm' && +ans.budget <= 2); }
  function resolve(c) {
    if (c === 'mfgsys') return small() ? 'mrp' : 'erp';
    if (c === 'whsys') return ((ans.size === 'md' || ans.size === 'lg') && +ans.budget >= 2) ? 'wms' : 'inv';
    if (c === 'distsys' || c === 'omsys') return small() ? 'inv' : 'erp';
    if (c === 'consys') return small() ? 'cpm' : 'erp';
    if (c === 'svcsys') return small() ? 'acct' : 'erp';
    var lite = { lgsys: 'tms', hssys: 'acct', hcsys: 'acct', resys: 'prop', fssys: 'fsm', coresys: 'acct' };
    if (lite[c]) return small() ? lite[c] : 'erp';
    return c;
  }
  var FALLBACK = { inv: ['wms', 'farm', 'erp'], wms: ['inv', 'erp'], mrp: ['inv', 'erp'], cpm: ['fsm'], fsm: ['cpm'], psa: ['acct'], prop: ['acct'], tms: ['inv'], erp: ['acct'], clinic: ['booking'], booking: ['clinic'] };
  function resolveFit(raw) {
    var c = resolve(raw); if (catFits(c)) return c;
    var f = FALLBACK[c] || []; for (var i = 0; i < f.length; i++) if (catFits(f[i])) return f[i];
    return null;
  }
  function erpWf() {
    var t = A.subtypes[ans.ind]; if (!t) return null;
    var w = t.auto || ans.sub; if (t.wf && t.wf[w]) w = t.wf[w]; return WF[w] ? w : null;
  }
  function catFits(cid) {
    if (cid === 'erp') { var w = erpWf(); return !!w && A.erp.vendors.some(function (v) { return v.s[w]; }); }
    if (cid === 'mrp' && ans.ind === 'agri' && erpWf() !== 'fb') return false;
    return catFitsInd(cid, ans.ind);
  }

  /* ---------- scoring ---------- */
  var OWN = { erp: ['erp', 'mrp', 'inv'], ind: ['clinic', 'pos', 'fsm', 'prop', 'tms', 'cpm', 'psa', 'farm', 'booking'], acct: ['acct'], crm: ['crm'], m365: ['collab'], gws: ['collab'], ai: ['ai'] };
  function owned(cid) { return (ans.tools || []).some(function (t) { return (OWN[t] || []).indexOf(cid) >= 0; }); }
  function analyse() {
    var gap = {}, pw = {};
    A.functions.forEach(function (f) { var v = ans.mat[f.id]; gap[f.id] = Math.max(0, v.t - v.c); pw[f.id] = 0; });
    (ans.prio || []).forEach(function (p) { var w = PRI[p].w; for (var k in w) pw[k] += w[k]; });
    var probMap = {}, unmatched = [];
    (ans.prob || []).forEach(function (pid) {
      var hit = false;
      PRB[pid].c.forEach(function (raw, i) { var c = resolveFit(raw); if (!c) return; hit = true; (probMap[c] = probMap[c] || []).push({ t: PRB[pid].t, w: i === 0 ? 3 : 2 }); });
      if (!hit) unmatched.push(PRB[pid].t);
    });
    var cats = A.categories.filter(function (c) { return catFits(c.id); }).map(function (c) {
      var s = 0, why = [];
      (probMap[c.id] || []).forEach(function (x) { s += x.w; if (why.indexOf(x.t) < 0) why.push(x.t); });
      var g = gap[c.fn];
      // the maturity gap only lifts categories that solve a stated problem, or broad foundations
      var direct = !!probMap[c.id], foundation = ['acct', 'payroll', 'crm', 'collab', 'sec', 'bi', 'ai'].indexOf(c.id) >= 0;
      if (direct || foundation) s += g * (1 + pw[c.fn] / 3) * (direct ? 1 : 0.6);
      if (ans.mat[c.fn].c === 0 && c.ease === 3 && foundation) s += 1;
      if (direct) s += pw[c.fn] * 0.3;                    // L15: priorities also lift problem-driven categories
      var own = owned(c.id); if (own) s *= 0.4;            // L8: already owned -> optimise, do not re-buy
      return { c: c, s: s, why: why, gap: g, own: own };
    }).filter(function (x) { return x.s >= 2 && (x.why.length || x.gap > 0); })   // L12: no filler cards
      .sort(function (a, b) { return b.s - a.s; });
    var top = cats.slice(0, 3), bud = +ans.budget;
    // L1/L2: quick win comes from the whole ranked list, never ERP or an owned system, prefers ease 3 (weeks), and checks budget
    function minPrice(cid) { var ps = products(cid).filter(function (p) { return p.inds.indexOf(ans.ind) >= 0; }); return ps.length ? Math.min.apply(null, ps.map(function (p) { return p.price; })) : 9; }
    function qwScore(x) { return x.s * (0.4 + x.c.ease / 3) - (minPrice(x.c.id) > bud ? 3 : 0); }
    var pool = cats.filter(function (x) { return x.c.id !== 'erp' && !x.own && x.c.ease >= 2 && minPrice(x.c.id) <= bud; });
    var topS = cats.length ? cats[0].s : 0;
    var easy = pool.filter(function (x) { return x.c.ease === 3 && x.s >= 0.4 * topS; });
    var qw = (easy.length ? easy : pool).slice().sort(function (a, b) { return qwScore(b) - qwScore(a); })[0] || null;
    return { gap: gap, top: top, qw: qw, quick: !!(qw && qw.c.ease === 3), unmatched: unmatched };
  }
  function options(cid) {
    var sizes = STAFF[ans.size], bud = +ans.budget, wf = erpWf() || 'mf';
    var subIds = ((A.subtypes[ans.ind] || {}).o || []).map(function (o) { return o[0]; });
    var cp = caps(cid, wf), wts = cp.map(function () { return 1; });
    (ans.prob || []).forEach(function (pid) { var w = (PRB[pid].w || {})[cid]; if (w) cp.forEach(function (k, i) { if (w[k.k] != null) wts[i] = Math.max(wts[i], w[k.k]); }); });
    return products(cid).filter(function (p) {
      if (!(cid === 'erp' || p.inds.indexOf(ans.ind) >= 0) || !scores(p, cid, wf)) return false;
      if (p.only && p.only.some(function (x) { return subIds.indexOf(x) >= 0; }) && p.only.indexOf(ans.sub) < 0 && p.only.indexOf(erpWf()) < 0) return false;
      return true;
    }).map(function (p) {
      var sc = scores(p, cid, wf), num = 0, den = 0;
      sc.forEach(function (x, i) { num += x * wts[i]; den += 3 * wts[i]; });
      var f = num / den * 100, flags = [], t = ans.tools || [];
      if (!sizes.some(function (z) { return p.size.indexOf(z) >= 0; })) { f -= 15; flags.push('Usually chosen by firms of a different size.'); }
      if (p.price > bud) { f -= 18 * (p.price - bud); flags.push('Usually above your budget (' + PRICE[p.price] + ' in year one).'); }
      if (p.ca) f += 3;
      if (p.inds.length <= 2) f += 3;
      if (cid === 'ai' || cid === 'collab') {                       // L14: fit the office suite they already use
        if (t.indexOf('m365') >= 0 && /copilot|m365/.test(p.id)) f += 10;
        if (t.indexOf('gws') >= 0 && /gemini|gws/.test(p.id)) f += 10;
        if (t.indexOf('m365') >= 0 && /gemini|gws/.test(p.id)) f -= 15;
        if (t.indexOf('gws') >= 0 && /copilot|m365/.test(p.id)) f -= 15;
      }
      if (p.unv && p.unv.length) flags.push('Some capability scores are unconfirmed; check them in the demo.');
      return { p: p, raw: f, fit: Math.max(0, Math.min(95, Math.round(f))), flags: flags };
    }).sort(function (a, b) { return b.raw - a.raw || (b.p.ca ? 1 : 0) - (a.p.ca ? 1 : 0) || a.p.price - b.p.price || a.p.name.localeCompare(b.p.name); }).slice(0, 3);
  }

  /* ---------- results ---------- */
  function radar() {
    var n = A.functions.length, cx = 210, cy = 190, R = 140, out = '';
    function pt(i, r) { var a = -Math.PI / 2 + i * 2 * Math.PI / n; return [cx + r * Math.cos(a), cy + r * Math.sin(a)]; }
    for (var l = 1; l <= 4; l++) out += '<polygon points="' + A.functions.map(function (f, i) { return pt(i, R * l / 4).join(','); }).join(' ') + '" fill="none" stroke="#E4E1D8"/>';
    A.functions.forEach(function (f, i) {
      var p = pt(i, R), q = pt(i, R + 26);
      out += '<line x1="' + cx + '" y1="' + cy + '" x2="' + p[0] + '" y2="' + p[1] + '" stroke="#E4E1D8"/><text x="' + q[0] + '" y="' + (q[1] + 4) + '" text-anchor="middle" font-size="17" font-weight="600" fill="#0B2A5A">' + esc(f.short) + '</text>';
    });
    function poly(k, fill, stroke, dash) { return '<polygon points="' + A.functions.map(function (f, i) { return pt(i, R * (ans.mat[f.id][k] + 1) / 4).join(','); }).join(' ') + '" fill="' + fill + '" stroke="' + stroke + '" stroke-width="2.5"' + (dash ? ' stroke-dasharray="6 4"' : '') + '/>'; }
    out += poly('t', 'rgba(77,127,18,.10)', '#4D7F12', true) + poly('c', 'rgba(11,111,164,.22)', '#0B6FA4');
    return '<svg viewBox="-50 -10 520 410" role="img" aria-label="Digital maturity today versus target">' + out + '</svg><div class="as-radar-key"><span><i style="background:rgba(11,111,164,.5)"></i>Today</span><span><i style="background:#fff;border:2px dashed #4D7F12"></i>Target</span></div>';
  }
  function finish() {
    $('#as-bar').style.width = '100%';
    var r = analyse(), lv = ['must', 'should', 'could'], lvn = ['Must', 'Should', 'Could'];
    $('#as-res-lead').textContent = IND[ans.ind].name + ' · ' + { xs: 'fewer than 10', sm: '10–49', md: '50–99', lg: '100–499' }[ans.size] + ' people · priorities: ' + (ans.prio || []).map(function (p) { return PRI[p].name.toLowerCase(); }).join(', ') + '.';
    $('#as-radar').innerHTML = radar();
    var gs = A.functions.map(function (f) { return { n: f.short, g: r.gap[f.id] }; }).sort(function (a, b) { return b.g - a.g; }), gmax = gs.length ? gs[0].g : 0;
    $('#as-gapsum').innerHTML = gmax > 0 ? 'Biggest gap' + (gs.filter(function (x) { return x.g === gmax; }).length > 1 ? 's' : '') + ': <strong>' + gs.filter(function (x) { return x.g === gmax; }).map(function (x) { return esc(x.n); }).join(', ') + '</strong> (' + gmax + ' level' + (gmax > 1 ? 's' : '') + ' to your two-year target).' : 'You are already at your two-year target in every function.';
    $('#as-gaps').innerHTML = '<thead><tr><th>Function</th><th>Today</th><th>Target</th><th>Gap</th></tr></thead><tbody>' + A.functions.map(function (f) {
      var v = ans.mat[f.id], g = r.gap[f.id];
      return '<tr><td><strong>' + esc(f.short) + '</strong></td><td>' + A.levels[v.c].n + '</td><td>' + A.levels[v.t].n + '</td><td><span class="as-gap g' + g + '">' + g + '</span></td></tr>';
    }).join('') + '</tbody>';
    $('#as-prios').innerHTML = r.top.map(function (x, i) {
      return '<div class="as-prio ' + lv[i] + '"><span class="lvl">Priority ' + (i + 1) + ' · ' + lvn[i] + '</span>' + (x === r.qw && r.quick ? '<span class="qwtag">Quick win</span>' : '') +
        (x.own ? '<span class="qwtag" style="background:var(--sand);color:var(--ink)">You have this</span>' : '') +
        '<h4>' + esc(x.c.name) + '</h4><p class="ben">' + esc(x.c.benefit) + '</p><ul>' + x.why.slice(0, 3).map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('') +
        (x.gap ? '<li>' + FN[x.c.fn].name + ': ' + x.gap + '-level gap to your target</li>' : '') + '</ul>' +
        '<button type="button" class="as-goto" data-goto="' + x.c.id + '">Compare products →</button></div>';
    }).join('') || '<p>Your answers show no clear gap. Try raising your two-year targets or picking more problems.</p>';
    var q = r.qw, opts = q ? options(q.c.id) : [];
    var notes = [];
    if (r.unmatched.length) notes.push('We don\'t yet list software for: ' + r.unmatched.map(esc).join('; ') + '.');
    if (A.gaps && A.gaps[ans.sub]) notes.push(esc(A.gaps[ans.sub]));
    $('#as-notes').innerHTML = notes.length ? '<div class="as-empty"><p>' + notes.join('<br>') + '</p></div>' : '';
    if (!q) {
      $('#as-qw').hidden = false;
      $('#as-qw').innerHTML = '<p class="eyebrow" style="color:var(--green-dark)">Your first step</p><h3>' + (r.top.some(function (x) { return x.c.id === 'erp'; }) ? 'Start with an ERP readiness review' : 'Start with a short process review') + '</h3><p>None of your priorities has a fast, low-risk project within your budget. A short review of processes and data will make the bigger project faster and cheaper.</p><div class="as-links">' + (r.top.length ? '<button type="button" class="as-goto" data-goto="' + r.top[0].c.id + '">Compare ' + esc(r.top[0].c.name) + ' options →</button>' : '') + '<a href="funding.html#match">Find funding for this project (free Funding Match)</a></div>';
      $('#as-opts-h').textContent = ''; $('#as-opts').innerHTML = '';
    }
    if (q) {
      var risk = ['', 'Higher', 'Medium', 'Low'][q.c.ease];
      $('#as-qw').hidden = false;
      $('#as-qw').innerHTML = '<p class="eyebrow" style="color:var(--green-dark)">' + (r.quick ? 'Your quick win' : 'Your first project') + '</p><h3>' + esc(q.c.name) + '</h3><p>' + esc(q.c.desc) + ' ' + esc(q.c.benefit) + '</p>' +
        '<div class="as-crit"><div><b>Time to value</b><span>' + q.c.weeks + '</span></div><div><b>Implementation risk</b><span>' + risk + '</span></div><div><b>Year-one cost</b><span>' + (opts.length ? PRICE[Math.min.apply(null, opts.map(function (o) { return o.p.price; }))] : '—') + '</span></div><div><b>Supports</b><span>' + esc(FN[q.c.fn].name) + '</span></div></div>' +
        '<div class="as-links">' + q.c.links.map(function (l) { return '<a href="' + esc(l[0]) + '">' + esc(l[1]) + '</a>'; }).join('') + '<a href="funding.html#match">Find funding for this project (free Funding Match)</a></div>';
      $('#as-opts-h').textContent = 'Three options to evaluate for ' + lcName(q.c.name);
      $('#as-opts').innerHTML = opts.map(function (o, i) {
        var p = o.p;
        return '<article class="erp-res' + (i === 0 ? ' top' : '') + '"><div class="erp-rank">' + (i + 1) + '</div>' +
          '<div><h4><button type="button" class="as-plink" data-p="' + q.c.id + ':' + p.id + '">' + esc(p.name) + '</button>'  + '</h4><p class="erp-best">' + esc(p.best) + '</p></div>' +
          '<div class="erp-res-fit"><strong>' + o.fit + '%</strong><span>fit</span></div>' +
          '<div class="erp-res-body"><div><b>In Canada</b>' + esc(p.canada) + '</div><div><b>Year-one cost</b>' + PRICE[p.price] + '</div>' +
          '<div class="rc"><b>Reality Check</b>' + esc(rcText(p)) + '</div>' + (o.flags.length ? '<div class="flag">⚠ ' + o.flags.map(esc).join(' ') + '</div>' : '') + '</div></article>';
      }).join('') || '<p>No options in the database yet for this combination.</p>';
    }
    var mc = (q ? [q] : []).concat(r.top), mhtml = '';
    for (var mi = 0; mi < mc.length && !mhtml; mi++) mhtml = moreVendors(mc[mi].c.id, mi > 0 && q ? 'For your priority: ' + mc[mi].c.name : '');
    $('#as-more').innerHTML = mhtml;
    $('#as-aitools').innerHTML = aiForProblems();
    var box = $('#as-f-report');
    REP = { secs: buildReport(r, q, opts), r: r };
    if (box) { box.innerHTML = ''; REP.secs.forEach(function (f) { var i = document.createElement('input'); i.type = 'hidden'; i.name = f[0]; i.value = f[1]; box.appendChild(i); }); }
    if (false) $('#as-f-sum').value = 'Industry: ' + IND[ans.ind].name + ' | Priorities: ' + r.top.map(function (x, i) { return lvn[i] + ' ' + x.c.name; }).join('; ') + ' | Quick win: ' + (q ? q.c.name : '-') + ' | Options: ' + opts.map(function (o) { return o.p.name + ' (' + o.fit + '%)'; }).join('; ');
    if (false) $('#as-f-ans').value = 'Size ' + ans.size + '; tools ' + (ans.tools || []).join(',') + '; problems ' + (ans.prob || []).map(function (p) { return PRB[p].t; }).join(' / ') + '; maturity ' + A.functions.map(function (f) { return f.short + ' ' + ans.mat[f.id].c + '>' + ans.mat[f.id].t; }).join(', ') + '; budget ' + PRICE[ans.budget];
    quiz.hidden = true; result.hidden = false;
    $('#assessment').scrollIntoView({ behavior: 'smooth' });
  }

  /* ================= Software Finder (one matrix layout for every category) ================= */
  var fs = { cat: 'acct', ind: '', wf: 'mf', all: false };
  var CATGROUPS = [['Money and people', ['acct', 'payroll']], ['Sales and customers', ['crm', 'mkt', 'ecom', 'pos', 'booking']],
    ['Operations', ['inv', 'mrp', 'erp', 'wms', 'fsm', 'cpm', 'tms', 'prop', 'farm', 'clinic', 'psa']], ['IT and AI', ['collab', 'bi', 'sec', 'ai']]];
  var catSel = $('#as-catsel'), indSel = $('#as-indsel');
  catSel.innerHTML = CATGROUPS.map(function (g) { return '<optgroup label="' + esc(g[0]) + '">' + g[1].filter(function (id) { return CAT[id]; }).map(function (id) { return '<option value="' + id + '">' + esc(CAT[id].name) + '</option>'; }).join('') + '</optgroup>'; }).join('');
  indSel.innerHTML = '<option value="">All industries</option>' + A.industries.map(function (i) { return '<option value="' + i.id + '">' + esc(i.name) + '</option>'; }).join('');
  catSel.addEventListener('change', function () { fs.cat = this.value; fs.all = false; renderFinder(); });
  indSel.addEventListener('change', function () { fs.ind = this.value; fs.all = false; renderFinder(); });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-ind]'); if (b && b.closest('#finder')) { fs.ind = b.dataset.ind; renderFinder(); return; }
    if (e.target.closest('#as-fall')) { fs.all = true; renderFinder(); }
  });
  function lcName(n) { return n.split(' ').map(function (w) { return /[A-Z].*[A-Z]|[0-9]/.test(w) ? w : w.toLowerCase(); }).join(' '); }
  $('#as-wf').addEventListener('change', function () { fs.wf = this.value; renderFinder(); });
  function wfFor(ind) { return A.erp.workflows.filter(function (w) { return !ind || w.ind.indexOf(ind) >= 0; }); }
  function wfOptions() {
    var list = wfFor(fs.ind), groups = [];
    list.forEach(function (w) { if (groups.indexOf(w.grp) < 0) groups.push(w.grp); });
    $('#as-wf').innerHTML = groups.map(function (g) { return '<optgroup label="' + esc(g) + '">' + list.filter(function (w) { return w.grp === g; }).map(function (w) { return '<option value="' + w.id + '">' + esc(w.name) + '</option>'; }).join('') + '</optgroup>'; }).join('');
    if (!list.some(function (w) { return w.id === fs.wf; }) && list.length) { var spec = list.filter(function (w) { return w.id !== 'core'; }); fs.wf = (fs.ind && spec.length ? spec[0] : list[0]).id; }
    $('#as-wf').value = fs.wf;
    return list.length;
  }
  document.addEventListener('click', function (e) {
    var g = e.target.closest('[data-goto]'); if (!g) return;
    fs.cat = g.dataset.goto; fs.ind = ans.ind || ''; fs.all = false; if (fs.cat === 'erp' && erpWf()) fs.wf = erpWf();
    renderFinder(); $('#finder').scrollIntoView({ behavior: 'smooth' });
  });
  function renderFinder() {
    var c = CAT[fs.cat], isErp = c.id === 'erp';
    catSel.value = fs.cat; indSel.value = fs.ind;
    var nwf = isErp ? wfOptions() : 0;
    $('#as-wfwrap').hidden = !isErp || !nwf;
    $('#as-catdesc').innerHTML = esc(c.desc + ' ' + c.benefit) + (isErp && nwf ? '<small class="as-wfhelp">' + esc(WF[fs.wf].desc) + '</small>' : '');
    if (isErp && !nwf) {
      $('#as-fbody').innerHTML = '<div class="as-empty"><p><strong>No ERP options for ' + esc(IND[fs.ind].name.toLowerCase()) + ' yet.</strong> Businesses in this industry usually start with the industry software in the other categories.</p><div class="btn-row"><button type="button" class="btn btn-ghost" data-ind="">Show ERP for all industries</button></div></div>';
      $('#as-fcount').textContent = ''; return;
    }
    var cp = caps(c.id, fs.wf);
    var all = products(c.id).filter(function (p) { return (!fs.ind || p.inds.indexOf(fs.ind) >= 0) && scores(p, c.id, fs.wf); })
      .sort(function (a, b) { return avgFit(scores(b, c.id, fs.wf)) - avgFit(scores(a, c.id, fs.wf)) || a.name.localeCompare(b.name); });
    var rows = fs.all ? all : all.slice(0, 8);
    var legend = '<p class="as-legend" role="note"><span><i class="dot s3"></i>Built in</span><span><i class="dot s2"></i>Set up without code</span><span><i class="dot s1"></i>Add-on</span><span><i class="dot s0"></i>Not offered</span><span>🍁 Canadian</span></p>';
    var more = all.length > rows.length ? '<p class="vd-more-link"><button type="button" class="as-goto" id="as-fall">Show all ' + all.length + ' products</button></p>' : '';
    $('#as-fbody').innerHTML = rows.length ? legend + '<div class="erp-tablewrap as-desk"><table class="erp-table"><thead><tr><th class="vend" scope="col">Product</th><th scope="col">Fit</th>' +
      cp.map(function (k) { return '<th class="cap" scope="col" title="' + esc(k.d) + '">' + esc(k.n) + '</th>'; }).join('') + '<th scope="col" title="First-year cost: $ under $25K, $$ $25–100K, $$$ $100–300K, $$$$ over $300K">Year-one cost</th></tr></thead><tbody>' +
      rows.map(function (p) {
        var s = scores(p, c.id, fs.wf), f = avgFit(s), t = typeLabel(p, c.id);
        return '<tr><td class="vend"><button type="button" data-p="' + c.id + ':' + p.id + '">' + esc(p.name) + '</button>' +
          '<small>' + (p.ca ? '🍁 ' : '') + esc(t || p.best) + '</small></td><td><span class="erp-fit">' + f + '%</span><span class="erp-fitbar"><i style="width:' + f + '%"></i></span></td>' +
          s.map(function (x) { return '<td>' + dot(x) + '</td>'; }).join('') + '<td class="erp-meta">' + dollars(p.price) + '</td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<div class="as-mcards">' + rows.map(function (p) {
        var f = avgFit(scores(p, c.id, fs.wf)), t = typeLabel(p, c.id);
        return '<button type="button" class="as-mcard" data-p="' + c.id + ':' + p.id + '"><span class="n">' + esc(p.name) + (p.ca ? ' 🍁' : '') + '</span><span class="b">' + esc(t || p.best) + '</span><span class="m"><b>' + f + '% fit</b> · ' + PRICE[p.price] + ' in year one · Details →</span></button>';
      }).join('') + '</div>' + more +
      (cp[0] && cp[0].r ? '<details class="as-guide"><summary>What "built in" means for each capability</summary><dl>' + cp.map(function (k) { return '<dt>' + esc(k.n) + '</dt><dd>' + esc(k.r) + '</dd>'; }).join('') + '</dl></details>' : '')
      : '<div class="as-empty"><p><strong>No products in this category for ' + (fs.ind ? esc(IND[fs.ind].name.toLowerCase()) : 'this selection') + ' yet.</strong></p><div class="btn-row"><button type="button" class="btn btn-ghost" data-ind="">Show all industries</button></div></div>';
    var nd = (A.dir || []).filter(function (e) { return e.g === c.id && !e.sc && indOk(e, fs.ind); }).length;
    if (nd && rows.length) $('#as-fbody').insertAdjacentHTML('beforeend', '<p class="vd-more-link"><button type="button" class="as-goto" data-vd="' + c.id + '">See ' + nd + ' more ' + esc(lcName(c.name)) + ' vendors →</button></p>');
    $('#as-fcount').textContent = all.length + ' product' + (all.length === 1 ? '' : 's') + (fs.ind ? ' for ' + IND[fs.ind].name.toLowerCase() : '') + ', best fit first';
  }
  renderFinder();

  /* ================= Product dialog ================= */
  var dlg = $('#erp-dlg');
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-p]');
    if (b) { var k = b.dataset.p.split(':'); openProd(k[0], k[1]); return; }
    if (e.target.closest('[data-close-dlg]') || e.target === dlg) dlg.close();
  });
  /* ================= Vendor Directory (listings from Chmltech master lists; not scored) ================= */
  var DIR = A.dir || [], GRP = {};
  (A.dir_groups || []).forEach(function (g) { GRP[g.id] = g; if (CAT[g.id]) g.name = CAT[g.id].name; });
  var SZN = { s: 'Small', m: 'Mid', l: 'Large' }, SZA = { xs: ['s'], sm: ['s', 'm'], md: ['m'], lg: ['m', 'l'] };
  function grpFitsInd(g, ind) {
    if (!ind) return true;
    if (CAT[g]) return catFitsInd(g, ind);
    var gi = (GRP[g] || {}).inds || []; return !gi.length || gi.indexOf(ind) >= 0;
  }
  function safeUrl(u) { return /^https?:\/\/[^\s"'<>]+$/i.test(u || '') ? u : ''; }
  function vlink(e) { return safeUrl(e.u) ? '<a href="' + esc(safeUrl(e.u)) + '" target="_blank" rel="noopener nofollow">' + esc(e.n) + '</a>' : esc(e.n); }
  function short(t, n) { t = t || ''; return t.length > n ? t.slice(0, n - 1).replace(/\s+\S*$/, '') + '…' : t; }
  var vd = { q: '', g: '', ind: '', size: '', ca: false, shown: 10 };
  function vdInit() {
    if (!$('#vd-body')) return;
    var gs = A.dir_groups.filter(function (g) { return DIR.some(function (e) { return e.g === g.id; }); });
    function cnt(id) { return DIR.filter(function (e) { return e.g === id; }).length; }
    function opts(list) { return list.map(function (g) { return '<option value="' + g.id + '">' + esc(g.name) + ' (' + cnt(g.id) + ')</option>'; }).join(''); }
    $('#vd-g').innerHTML = '<option value="">All categories (' + DIR.length + ')</option>' +
      '<optgroup label="Software in the assessment">' + opts(gs.filter(function (g) { return CAT[g.id]; })) + '</optgroup>' +
      '<optgroup label="Specialist software">' + opts(gs.filter(function (g) { return !CAT[g.id] && g.k === 's'; })) + '</optgroup>' +
      '<optgroup label="Service partners">' + opts(gs.filter(function (g) { return g.k === 'p'; })) + '</optgroup>';
    $('#vd-ind').innerHTML = '<option value="">All industries</option>' + A.industries.map(function (i) { return '<option value="' + i.id + '">' + esc(i.name) + '</option>'; }).join('');
    $('#vd-q').addEventListener('input', function () { vd.q = this.value; vd.shown = 10; vdRender(); });
    $('#vd-g').addEventListener('change', function () { vd.g = this.value; vd.shown = 10; vdRender(); });
    $('#vd-ind').addEventListener('change', function () { vd.ind = this.value; vd.shown = 10; vdRender(); });
    $('#vd-size').addEventListener('change', function () { vd.size = this.value; vd.shown = 10; vdRender(); });
    $('#vd-ca').addEventListener('change', function () { vd.ca = this.checked; vd.shown = 10; vdRender(); });
    $('#vd-more').addEventListener('click', function () { vd.shown += 20; vdRender(); });
    vdRender();
  }
  function indOk(e, ind) { return !ind || (e.i && e.i.length ? e.i.indexOf(ind) >= 0 : grpFitsInd(e.g, ind)); }
  function qScore(e, words, q) {   // 3 = name starts with the search, 2 = all words in the name, 1 = found elsewhere, 0 = no match
    if (!words.length) return 1;
    var n = e.n.toLowerCase(); if (n.indexOf(q) === 0 || (e.was || '').toLowerCase().indexOf(q) === 0) return 3;
    if (words.every(function (w) { return n.indexOf(w) >= 0 || (e.was || '').toLowerCase().indexOf(w) >= 0; })) return 2;
    var t = (e.n + ' ' + (e.was || '') + ' ' + e.d + ' ' + e.sub + ' ' + e.hq + ' ' + (GRP[e.g] || {}).name).toLowerCase();
    return words.every(function (w) { return t.indexOf(w) >= 0; }) ? 1 : 0;
  }
  function vdRows() {
    var q = vd.q.toLowerCase().trim(), words = q.split(/\s+/).filter(Boolean);
    return DIR.map(function (e) { return { e: e, s: qScore(e, words, q) }; }).filter(function (x) {
      var e = x.e;
      if (!x.s) return false;
      if (vd.g && e.g !== vd.g) return false;
      if (vd.ca && !e.ca) return false;
      if (vd.size && e.sz.length && e.sz.indexOf(vd.size) < 0) return false;
      return indOk(e, vd.ind);
    }).sort(function (a, b) {
      var A1 = a.e, B1 = b.e;
      return b.s - a.s || (vd.ind ? ((B1.i || []).indexOf(vd.ind) >= 0) - ((A1.i || []).indexOf(vd.ind) >= 0) : 0) ||
        (B1.sc ? 1 : 0) - (A1.sc ? 1 : 0) || (vd.size ? (B1.sz.length ? 1 : 0) - (A1.sz.length ? 1 : 0) : 0) || (B1.ca ? 1 : 0) - (A1.ca ? 1 : 0) || A1.n.localeCompare(B1.n);
    }).map(function (x) { x.e._s = x.s; return x.e; });
  }
  function hiddenNameMatches(shown) {   // name matches that the category / industry / size / Canadian filters are hiding
    var q = vd.q.toLowerCase().trim(), words = q.split(/\s+/).filter(Boolean); if (!words.length) return 0;
    var all = DIR.filter(function (e) { return qScore(e, words, q) >= 2; }).length;
    return all - shown.filter(function (e) { return e._s >= 2; }).length;
  }
  function vdRender() {
    var rows = vdRows(), show = rows.slice(0, vd.shown), hid = hiddenNameMatches(rows);
    var nInd = vd.ind ? rows.filter(function (e) { return (e.i || []).indexOf(vd.ind) >= 0; }).length : 0;
    $('#vd-count').innerHTML = esc(rows.length + ' vendor' + (rows.length === 1 ? '' : 's')) +
      (vd.ind && nInd ? ' · ' + nInd + ' built for ' + esc(IND[vd.ind].name.toLowerCase()) + ', shown first' : '') +
      (hid > 0 ? ' · <button type="button" class="as-goto" id="vd-clear" style="display:inline">' + hid + ' more name match' + (hid > 1 ? 'es' : '') + ' hidden by your filters: clear filters</button>' : '');
    $('#vd-body').innerHTML = rows.length ? '<div class="erp-tablewrap"><table class="vd-table"><thead><tr><th scope="col">Vendor</th><th scope="col">What they do</th><th scope="col">Category</th><th scope="col">Based in</th><th scope="col">Price</th></tr></thead><tbody>' +
      show.map(function (e) {
        var forInd = vd.ind && (e.i || []).indexOf(vd.ind) >= 0;
        return '<tr><td class="vd-n" data-label="">' + vlink(e) + (e.sc ? ' <button type="button" class="vd-sc" data-p="' + e.sc + '">Compare →</button>' : '') + '</td>' +
          '<td data-label="">' + esc(short(e.d, 150)) + (forInd ? '<small class="vd-for on">Built for ' + esc(IND[vd.ind].name.toLowerCase()) + '</small>' : '') + '</td>' +
          '<td data-label="Category">' + esc((GRP[e.g] || {}).name || '') + '</td>' +
          '<td data-label="Based in">' + (e.ca ? '🍁 ' : '') + esc(e.hq || (e.ca ? 'Canada' : '')) + '</td><td data-label="Price">' + esc(e.pr) + '</td></tr>';
      }).join('') + '</tbody></table></div>'
      : '<div class="as-empty"><p><strong>No listings match.</strong> Try fewer words or clear a filter.</p></div>';
    $('#vd-more').hidden = rows.length <= vd.shown;
    var cl = $('#vd-clear'); if (cl) cl.addEventListener('click', function () { vd.g = ''; vd.ind = ''; vd.size = ''; vd.ca = false; $('#vd-g').value = ''; $('#vd-ind').value = ''; $('#vd-size').value = ''; $('#vd-ca').checked = false; vdRender(); });
  }
  function vdGo(g) {
    vd.g = g; vd.ind = ans.ind && grpFitsInd(g, ans.ind) ? ans.ind : ''; vd.q = ''; vd.size = ({ xs: 's', sm: 's', md: 'm', lg: 'l' })[ans.size] || ''; vd.ca = false; vd.shown = 10;
    $('#vd-g').value = vd.g; $('#vd-ind').value = vd.ind; $('#vd-q').value = ''; $('#vd-size').value = vd.size; $('#vd-ca').checked = false;
    vdRender(); $('#vendors').scrollIntoView({ behavior: 'smooth' });
  }
  document.addEventListener('click', function (e) { var b = e.target.closest('[data-vd]'); if (b) vdGo(b.dataset.vd); });
  function moreVendors(cid, lead) {
    if (cid === 'ai') return '';   // AI products are covered by the AI tools suggestions; directory 'ai' rows are developer platforms
    var want = SZA[ans.size] || [], small = ans.size === 'xs' || ans.size === 'sm';
    var pool = DIR.filter(function (e) { return e.g === cid && !e.sc && !e.st && indOk(e, ans.ind); });
    function sort(L) { return L.sort(function (a, b) { return ((b.i || []).indexOf(ans.ind) >= 0) - ((a.i || []).indexOf(ans.ind) >= 0) || (b.ca ? 1 : 0) - (a.ca ? 1 : 0) || a.n.localeCompare(b.n); }); }
    var sized = sort(pool.filter(function (e) { return e.sz.length && (!want.length || e.sz.some(function (z) { return want.indexOf(z) >= 0; })); }));
    var unsized = sort(pool.filter(function (e) { return !e.sz.length && !(small && /custom|enterprise|contact/i.test(e.pr)); }));
    var list = sized.slice(0, 6).concat(unsized.slice(0, Math.max(0, (sized.length >= 3 ? 6 : 4) - sized.length)));
    if (!list.length) return '';
    var nm = esc(lcName(CAT[cid].name));
    return '<div class="vd-res">' + (lead ? '<p class="ai-why">' + esc(lead) + '</p>' : '') + '<h4>More ' + nm + ' vendors to consider</h4><p class="muted">Not scored: check fit in a demo.</p><ul>' +
      list.map(function (e) { return '<li><strong>' + vlink(e) + '</strong>' + (e.ca ? ' 🍁' : '') + ' <span>' + esc(short(e.d, 110)) + '</span></li>'; }).join('') + '</ul>' +
      '<button type="button" class="as-goto" data-vd="' + cid + '">See all ' + nm + ' vendors in the Vendor Directory →</button></div>';
  }

  /* ================= AI Tools ================= */
  var GORDER = (A.ai_groups || []).map(function (g) { return g[0]; }), GNAME = {};
  (A.ai_groups || []).forEach(function (g) { GNAME[g[0]] = g[1]; });
  var AIT = (A.ai_tools || []).map(function (t, i) { t._i = i; return t; }).sort(function (a, b) {   // owner groups first, free / low-price tools first
    return GORDER.indexOf(a.grp) - GORDER.indexOf(b.grp) || (/\bUS\b|United States/.test(a.note || '') - /\bUS\b|United States/.test(b.note || '')) || aiFit(b) - aiFit(a) || a._i - b._i;
  });
  var ai = { c: '', q: '', shown: 8 };
  var AI_PER = 3;   // tools previewed per job in the "All jobs" overview
  function aiInit() {
    if (!$('#ai-body')) return;
    var sel = $('#ai-cats');
    sel.innerHTML = '<option value="">All jobs</option>' + GORDER.map(function (g) { return '<option value="' + esc(g) + '">' + esc(GNAME[g]) + (g === 'dev' ? ' (for IT staff)' : '') + '</option>'; }).join('');
    sel.addEventListener('change', function () { ai.c = this.value; ai.shown = 8; aiRender(); });
    $('#ai-q').addEventListener('input', function () { ai.q = this.value; ai.shown = 8; aiRender(); });
    $('#ai-more').addEventListener('click', function () { ai.shown += 12; aiRender(); });
    $('#ai-body').addEventListener('click', function (e) {   // "See all" / "All jobs" links inside the list
      var b = e.target.closest('[data-aic]'); if (!b) return;
      ai.c = b.dataset.aic; ai.shown = 8; aiRender();
      var h = $('#ai-cats'); if (h) h.focus();
    });
    aiRender();
  }
  // Short price label for the badge; the full vendor text stays in the tooltip
  function aiPrice(pr) {
    var p = String(pr || ''), l = p.toLowerCase();
    var m = p.replace(/,/g, '').match(/(?:US|CAD\s?)?\$\s?~?(\d+(?:\.\d+)?)(\s*\/\s*(?:user|seat|member|agent)\s*)?(\/\s*(?:mo|yr))?/i);
    var amt = m ? '$' + (+m[1] % 1 ? (+m[1]).toFixed(2) : +m[1]) + (m[2] ? '/user' : '') + (m[3] ? (/yr/i.test(m[3]) ? '/yr' : '/mo') : '') : '';
    if (/^free(?! trial)/.test(l) || /^\$?0\b/.test(l)) return { k: 'free', t: 'Free plan', s: amt ? 'Paid from ' + amt : '' };
    if (/included/.test(l) && !amt) return { k: 'std', t: 'In existing plan', s: '' };
    if (amt) return { k: 'std', t: 'From ' + amt, s: /trial/.test(l) ? 'Free trial' : '' };
    if (/pay.as.you.go|usage|credit/.test(l)) return { k: 'std', t: 'Pay as you go', s: '' };
    if (/trial/.test(l)) return { k: 'std', t: 'Free trial', s: '' };
    if (/custom|enterprise|contact|quote|demo/.test(l)) return { k: 'ask', t: 'Price on request', s: '' };
    return { k: 'ask', t: 'See vendor site', s: '' };
  }
  function aiRow(t) {
    var u = safeUrl(t.u), pr = aiPrice(t.pr);
    var name = u ? '<a href="' + esc(u) + '" target="_blank" rel="noopener nofollow">' + esc(t.n) + '<span class="visually-hidden"> (opens in a new tab)</span></a>' : esc(t.n);
    return '<li class="ai-row"><h4 class="ai-n">' + name + '</h4><p class="ai-d">' + esc(t.d) + '</p>' +
      '<p class="ai-p" title="' + esc(t.pr) + '"><span class="ai-badge ai-' + pr.k + '">' + esc(pr.t) + '</span>' + (pr.s ? '<small>' + esc(pr.s) + '</small>' : '') + '<span class="visually-hidden">. Vendor price: ' + esc(t.pr) + '</span></p></li>';
  }
  /* ---- Compared AI tools per job (capability matrix, same design as the Software Finder) ---- */
  var AIM = A.ai_matrix || {};
  var SHL = { free: ['None', 'Demo only', 'Free trial', 'Free plan'], suite: ['No', 'Via Zapier or similar', 'One of the two', 'Both'],
    fr: ['English only', 'Partial French', 'French output, English screens', 'Full French'],
    priv: ['May train on your data', 'Opt-out only', 'Private by default', 'Private, with Canadian or regional data option'] };
  function lvl(k, v) { return SHL[k] ? SHL[k][v] : LEVEL[v]; }
  function adot(k, v) { return '<span class="dot s' + v + '" title="' + esc(lvl(k, v)) + '" aria-label="' + esc(lvl(k, v)) + '"></span>'; }
  function apr(t) { var p = aiPrice(t.price); return '<span class="ai-badge ai-' + p.k + '" title="' + esc(t.price) + '">' + esc(p.t) + '</span>' + (p.s ? '<small>' + esc(p.s) + '</small>' : ''); }
  function aiMatrix(g) {
    var m = AIM[g]; if (!m || !m.tools.length) return '';
    var ts = m.tools.slice().sort(function (a, b) { return avgFit(b.s) - avgFit(a.s) || a.n.localeCompare(b.n); });
    var legend = '<p class="as-legend" role="note"><span><i class="dot s3"></i>Built in</span><span><i class="dot s2"></i>Set up without code</span><span><i class="dot s1"></i>Add-on</span><span><i class="dot s0"></i>Not offered</span><span>First four columns: full dot = free plan, both suites, full French, data private with a Canadian option</span></p>';
    var table = '<div class="erp-tablewrap as-desk"><table class="erp-table ai-mtable"><thead><tr><th class="vend" scope="col">Tool</th><th scope="col">Fit</th>' +
      m.caps.map(function (k) { return '<th class="cap" scope="col" title="' + esc(k.r) + '">' + esc(k.n) + '</th>'; }).join('') + '<th scope="col">Price</th></tr></thead><tbody>' +
      ts.map(function (t) {
        var f = avgFit(t.s);
        return '<tr><td class="vend"><button type="button" data-aip="' + esc(g + ':' + t.id) + '">' + esc(t.n) + '</button><small>' + esc(t.best) + '</small></td>' +
          '<td><span class="erp-fit">' + f + '%</span><span class="erp-fitbar"><i style="width:' + f + '%"></i></span></td>' +
          t.s.map(function (x, i) { return '<td>' + adot(m.caps[i].k, x) + '</td>'; }).join('') + '<td class="erp-meta ai-mprice">' + apr(t) + '</td></tr>';
      }).join('') + '</tbody></table></div>';
    var cards = '<div class="as-mcards">' + ts.map(function (t) {
      return '<button type="button" class="as-mcard" data-aip="' + esc(g + ':' + t.id) + '"><span class="n">' + esc(t.n) + '</span><span class="b">' + esc(t.best) + '</span><span class="m"><b>' + avgFit(t.s) + '% fit</b> · ' + esc(aiPrice(t.price).t) + ' · Details →</span></button>';
    }).join('') + '</div>';
    return '<div class="ai-matrix"><div class="ai-mh"><h3>Compared: ' + ts.length + ' ' + esc(GNAME[g].charAt(0).toLowerCase() + GNAME[g].slice(1)) + ' tools</h3><span>Best fit first</span></div>' + legend + table + cards +
      '<details class="as-guide"><summary>What each column means</summary><dl>' + m.caps.map(function (k) { return '<dt>' + esc(k.n) + '</dt><dd>' + esc(k.r) + '</dd>'; }).join('') + '</dl></details></div>';
  }
  function aiCompared(g) { var m = AIM[g]; return m ? m.tools.map(function (t) { return (t.ex || t.n).toLowerCase(); }) : []; }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-aip]'); if (!b) return;
    var k = b.dataset.aip.split(':'), m = AIM[k[0]]; if (!m) return;
    var t = m.tools.filter(function (x) { return x.id === k[1]; })[0]; if (!t) return;
    var u = safeUrl(t.u);
    $('#erp-dlg-title').textContent = t.n;
    $('#erp-dlg-sub').textContent = GNAME[k[0]] + ' · Best for: ' + t.best;
    $('#erp-dlg-body').innerHTML =
      '<div class="erp-facts"><div><b>Price</b><span>' + esc(t.price) + '</span></div>' + (t.canada ? '<div><b>In Canada</b><span>' + esc(t.canada) + '</span></div>' : '') +
      (u ? '<div><b>Website</b><span><a href="' + esc(u) + '" target="_blank" rel="noopener nofollow">' + esc(t.n) + '</a></span></div>' : '') + '<div><b>Fit</b><span>' + avgFit(t.s) + '%</span></div></div>' +
      (t.rc ? '<div class="erp-rc"><h4>Consultant Reality Check</h4><p style="margin:0">' + esc(t.rc) + '</p></div>' : '') +
      '<div><h4 style="font-size:17px;margin-bottom:10px">Capabilities</h4><table class="as-captable">' + m.caps.map(function (c, i) {
        var ev = safeUrl((t.ev || [])[i]);
        return '<tr><td>' + adot(c.k, t.s[i]) + '</td><td><strong>' + esc(c.n) + '</strong><br><small>' + esc((t.notes || [])[i] || '') + (ev ? ' <a href="' + esc(ev) + '" target="_blank" rel="noopener nofollow">Source</a>' : '') + '</small></td><td class="muted">' + esc(lvl(c.k, t.s[i])) + '</td></tr>';
      }).join('') + '</table></div>' +
      (t.unv && t.unv.length ? '<div class="as-empty"><p><strong>Not yet confirmed:</strong> ' + t.unv.map(function (x) { var c = m.caps.filter(function (y) { return y.k === x; })[0]; return esc(c ? c.n : x); }).join('; ') + '. Check these in a trial.</p></div>' : '') +
      '<p class="muted" style="font-size:13.5px">Scores are our analyst rating from vendor information, ' + esc(m.asof || '') + ': confirm them in a trial.</p>';
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  });
  function aiRender() {
    var sel = $('#ai-cats'); if (sel.value !== ai.c) sel.value = ai.c;
    var words = ai.q.toLowerCase().split(/\s+/).filter(Boolean);
    var cmp = ai.c && !(ai.q || '').trim() ? aiCompared(ai.c) : [];
    var rows = AIT.filter(function (t) {
      if (ai.c && t.grp !== ai.c) return false;
      if (cmp.length && cmp.indexOf(t.n.toLowerCase()) >= 0) return false;
      if (!ai.c && !words.length && t.grp === 'dev') return false;    // developer tools only when chosen or searched
      var x = (t.n + ' ' + t.d + ' ' + t.c).toLowerCase(); return words.every(function (w) { return x.indexOf(w) >= 0; });
    });
    var body = $('#ai-body'), more = $('#ai-more'), n = rows.length + ' tool' + (rows.length === 1 ? '' : 's');
    if (!rows.length) {
      $('#ai-count').textContent = 'No tools';
      body.innerHTML = '<div class="as-empty"><p><strong>No AI tools match.</strong> Try fewer words or another job.</p></div>';
      more.hidden = true; return;
    }
    if (!ai.c && !words.length) {   // overview: one card per job with its top picks
      var by = {}; rows.forEach(function (t) { (by[t.grp] = by[t.grp] || []).push(t); });
      var gs = GORDER.filter(function (g) { return by[g]; });
      var dev = AIT.filter(function (t) { return t.grp === 'dev'; }).length;
      $('#ai-count').textContent = n + ' in ' + gs.length + ' jobs';
      body.innerHTML = '<div class="ai-jobs">' + gs.map(function (g) {
        return '<section class="ai-job" aria-labelledby="ai-h-' + esc(g) + '"><div class="ai-job-h"><h3 id="ai-h-' + esc(g) + '">' + esc(GNAME[g]) + '</h3><span>' + by[g].length + ' tools</span></div>' +
          '<ul class="ai-list">' + by[g].slice(0, AI_PER).map(aiRow).join('') + '</ul>' +
          (AIM[g] ? '<button type="button" class="ai-see ai-cmp" data-aic="' + esc(g) + '">Compare the top ' + AIM[g].tools.length + ' →</button>' : '') +
          '<button type="button" class="ai-see" data-aic="' + esc(g) + '">See all ' + by[g].length + ' ' + esc(GNAME[g].replace(/^[A-Z](?=[a-z])/, function (x) { return x.toLowerCase(); })) + ' tools</button></section>';
      }).join('') + '</div>' +
        (dev ? '<p class="ai-dev">For IT staff: <button type="button" class="ai-see" data-aic="dev">' + dev + ' developer tools</button></p>' : '');
      more.hidden = true; return;
    }
    $('#ai-count').textContent = words.length ? n + (rows.length === 1 ? ' matches' : ' match') + ' “' + ai.q.trim() + '”' + (ai.c ? ' in ' + GNAME[ai.c] : '') : n;
    var out = [], last = null;
    rows.slice(0, ai.shown).forEach(function (t) {
      if (!ai.c && t.grp !== last) { if (last !== null) out.push('</ul>'); out.push('<h3 class="ai-gh">' + esc(GNAME[t.grp] || '') + '</h3><ul class="ai-list ai-flat">'); last = t.grp; }
      out.push(aiRow(t));
    });
    var mx = ai.c && !words.length ? aiMatrix(ai.c) : '';
    if (mx) $('#ai-count').textContent = AIM[ai.c].tools.length + ' compared · ' + rows.length + ' more';
    body.innerHTML = (ai.c ? '<p class="ai-back"><button type="button" class="ai-see" data-aic="">← All jobs</button></p>' + mx + (mx ? '<h3 class="ai-gh">More ' + esc(GNAME[ai.c].charAt(0).toLowerCase() + GNAME[ai.c].slice(1)) + ' tools (not compared)</h3>' : '') + '<ul class="ai-list ai-flat">' : '') + out.join('') + '</ul>';
    var left = rows.length - ai.shown;
    more.hidden = left <= 0;
    more.textContent = 'Show ' + Math.min(12, left) + ' more (' + Math.min(ai.shown, rows.length) + ' of ' + rows.length + ' shown)';
  }
  function aiGo(c) { var t = AIT.filter(function (x) { return x.c === c; })[0]; ai.c = t ? t.grp : ''; ai.q = ''; ai.shown = 8; $('#ai-q').value = ''; aiRender(); $('#ai-tools').scrollIntoView({ behavior: 'smooth' }); }
  document.addEventListener('click', function (e) { var b = e.target.closest('[data-aigo]'); if (b) aiGo(b.dataset.aigo); });
  // SME fit for AI suggestions: free tier or published low price first; enterprise / custom / waitlist tools are not suggested
  function aiFit(t) {
    var p = (t.pr || '').toLowerCase();
    if (/enterprise|custom|contact|quote|waitlist|invite|demo/.test(p) && !/free/.test(p)) return -1;
    var m = p.replace(/,/g, '').match(/\$\s?(\d+(?:\.\d+)?)/); var v = m ? +m[1] : null;
    if (/free/.test(p)) return 3;
    if (v !== null && v <= 30) return 2;
    if (v !== null && v <= 60) return 1;
    return -1;
  }
  function aiPicks(c, n) {
    return AIT.map(function (t, i) { return { t: t, i: i, f: aiFit(t) }; })
      .filter(function (x) {
        var t = x.t, d = (t.d + ' ' + t.t).toLowerCase();
        if (t.c !== c || t.st || x.f < 0 || t.grp === 'dev') return false;
        if (/developer|prompt-to-code|coding|terminal|\bsql\b|python|notebook|\bapi\b|open-source framework/.test(d)) return false;   // not for business owners
        if (/practice management|accounting firm|law firm|\bcpas?\b|lawyers?/.test(d) && ans.ind !== 'prof') return false;           // built for professional firms
        if (/product teams?|data teams?|engineering teams?|for startups/.test(d) || /\bUS\b|United States/.test(t.note || '')) return false;   // not aimed at Canadian SME owners
        return true;
      })
      .sort(function (a, b) { return b.f - a.f || a.i - b.i; }).slice(0, n).map(function (x) { return x.t; });
  }
  function aiSuggest() {   // job groups for the visitor's problems, best compared tools first
    var groups = [], why = {};
    (ans.prob || []).forEach(function (pid) {
      ((A.ai_prob || {})[pid] || []).forEach(function (c) {
        var t = AIT.filter(function (x) { return x.c === c; })[0], g = t ? t.grp : null;
        if (!g || g === 'dev') return;
        if (groups.indexOf(g) < 0) groups.push(g);
        (why[g] = why[g] || []); if (why[g].indexOf(PRB[pid].t) < 0) why[g].push(PRB[pid].t);
      });
    });
    return groups.slice(0, 3).map(function (g) {
      var tools = AIM[g] ? AIM[g].tools.slice().sort(function (a, b) { return avgFit(b.s) - avgFit(a.s) || a.n.localeCompare(b.n); }).slice(0, 3)
        .map(function (t) { return { n: t.n, u: t.u, pr: t.price, d: t.best, fit: avgFit(t.s), k: g + ':' + t.id }; })
        : AIT.filter(function (t) { return t.grp === g && aiFit(t) >= 0; }).slice(0, 3).map(function (t) { return { n: t.n, u: t.u, pr: t.pr, d: t.d }; });
      return { g: g, name: GNAME[g], why: why[g], tools: tools };
    }).filter(function (x) { return x.tools.length; });
  }
  function aiForProblems() {
    var sug = aiSuggest(); if (!sug.length) return '';
    var probs = []; sug.forEach(function (x) { x.why.forEach(function (t) { if (probs.indexOf(t) < 0) probs.push(t); }); });
    return '<div class="ai-res"><h3 class="h-md" style="font-size:24px;margin-bottom:6px">AI tools that can help</h3><p class="muted" style="margin-bottom:14px">Our best-fit picks for: ' + probs.map(esc).join('; ') + '. Set rules on what company data goes into them.</p><div class="ai-groups">' +
      sug.map(function (x) {
        return '<div class="card"><p class="ai-cat">' + esc(x.name) + '</p><ul>' + x.tools.map(function (t) {
          var u = safeUrl(t.u);
          return '<li><strong>' + (t.k ? '<button type="button" class="ai-mlink" data-aip="' + esc(t.k) + '">' + esc(t.n) + '</button>' : (u ? '<a href="' + esc(u) + '" target="_blank" rel="noopener nofollow">' + esc(t.n) + '</a>' : esc(t.n))) + '</strong>' +
            (t.fit ? ' <span class="ai-fitp">' + t.fit + '% fit</span>' : '') + ' <span>' + esc(t.d) + '</span> <em>' + esc(aiPrice(t.pr).t) + '</em></li>';
        }).join('') + '</ul><button type="button" class="as-goto" data-aic="' + esc(x.g) + '" data-aijump="1">Compare ' + esc(x.name.charAt(0).toLowerCase() + x.name.slice(1)) + ' tools →</button></div>';
      }).join('') + '</div></div>';
  }
  document.addEventListener('click', function (e) {   // results "Compare … tools" jumps to that job in the AI section
    var b = e.target.closest('[data-aijump]'); if (!b) return;
    var sel = $('#ai-cats'); if (sel) { sel.value = b.dataset.aic; sel.dispatchEvent(new Event('change')); }
    $('#ai-tools').scrollIntoView({ behavior: 'smooth' });
  });

  /* ---- Branded PDF report (jsPDF, loaded on demand) ---- */
  var REP = null;
  function loadJsPDF() {
    if (window.jspdf) return Promise.resolve(window.jspdf);
    return new Promise(function (ok, no) {
      var sc = document.createElement('script'); sc.src = 'assets/js/vendor/jspdf.umd.min.js';
      sc.onload = function () { window.jspdf ? ok(window.jspdf) : no(); }; sc.onerror = no; document.head.appendChild(sc);
    });
  }
  function logoData() {
    var im = document.querySelector('.brand img'); if (!im || !im.naturalWidth) return null;
    try { var c = document.createElement('canvas'); c.width = im.naturalWidth; c.height = im.naturalHeight; c.getContext('2d').drawImage(im, 0, 0); return { d: c.toDataURL('image/png'), r: im.naturalWidth / im.naturalHeight }; } catch (e) { return null; }
  }
  function pdfTxt(x) { return String(x).replace(/→/g, 'to').replace(/≥/g, '>=').replace(/≤/g, '<=').replace(/✓/g, 'Yes').replace(/[^\x00-\xff–—‘’“”•…€™]/g, ''); }
  function makePdf() {
    if (!REP) return Promise.reject();
    return loadJsPDF().then(function (J) {
      var doc = new J.jsPDF({ unit: 'mm', format: 'a4' }), W = 210, M = 18, CW = W - 2 * M, y = 0, logo = logoData();
      var NAVY = [11, 42, 90], MUT = [90, 100, 117], LINE = [214, 220, 230], TINT = [232, 238, 247];
      var who = ($('#as-name') || {}).value || '', co = ($('#as-co') || {}).value || '';
      var date = new Date().toLocaleDateString('en-CA', { year: 'numeric', month: 'long', day: 'numeric' });
      function col(c) { doc.setTextColor(c[0], c[1], c[2]); }
      function head() {
        if (logo) doc.addImage(logo.d, 'PNG', M, 9, 12 * logo.r, 12, 'chmllogo', 'FAST');
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8.5); col(MUT);
        doc.text('Digital Needs Assessment  |  Roadmap report', W - M, 15, { align: 'right' }); doc.text(date, W - M, 19, { align: 'right' });
        doc.setDrawColor(NAVY[0], NAVY[1], NAVY[2]); doc.setLineWidth(0.6); doc.line(M, 24, W - M, 24); y = 32;
      }
      function room(h) { if (y + h > 274) { doc.addPage(); head(); } }
      function para(txt, o) {
        o = o || {}; var size = o.size || 9.6, lh = size * 0.47, ind = o.ind || 0, x = M + ind, w = CW - ind;
        doc.setFontSize(size);
        var m = !o.plain && /^([A-Z][A-Za-z0-9 ,'\/&–-]{1,44}): (.+)$/.exec(txt), key = m ? m[1] + ': ' : '', rest = m ? m[2] : txt;
        doc.setFont('helvetica', 'bold'); var kw = key ? doc.getTextWidth(key) : 0;
        doc.setFont('helvetica', o.bold ? 'bold' : 'normal');
        var first = doc.splitTextToSize(rest, w - kw), lines = [first[0]];
        if (first.length > 1) lines = lines.concat(doc.splitTextToSize(first.slice(1).join(' '), w - (o.hang || 0)));
        room(lh * lines.length + 1);
        lines.forEach(function (ln, i) {
          var lx = i === 0 ? x : x + (o.hang || 0);
          if (i === 0 && key) { doc.setFont('helvetica', 'bold'); col(NAVY); doc.text(key, lx, y); lx += kw; }
          doc.setFont('helvetica', o.bold ? 'bold' : 'normal'); col(o.color || [40, 48, 62]); doc.text(ln, lx, y);
          var u = /(https?:\/\/\S+)/.exec(ln);
          if (u) { var ux = lx + doc.getTextWidth(ln.slice(0, u.index)); doc.link(ux, y - 3.2, doc.getTextWidth(u[1]), 4.2, { url: u[1].replace(/[.,)]$/, '') }); }
          y += lh;
        });
      }
      function sectionHead(t) {
        room(28); y += 3; doc.setFont('helvetica', 'bold'); doc.setFontSize(13); col(NAVY); doc.text(pdfTxt(t), M, y);
        doc.setDrawColor(LINE[0], LINE[1], LINE[2]); doc.setLineWidth(0.3); doc.line(M, y + 2, W - M, y + 2); y += 8;
      }
      function maturity() {
        var cw = 28, x0 = M + 46, rh = 8;
        room(rh * (A.functions.length + 1) + 4);
        doc.setFont('helvetica', 'bold'); doc.setFontSize(8); col(MUT);
        A.levels.forEach(function (l, i) { doc.text(l.n, x0 + i * cw + cw / 2, y, { align: 'center' }); }); y += 3;
        A.functions.forEach(function (f) {
          var v = ans.mat[f.id];
          doc.setFont('helvetica', 'bold'); doc.setFontSize(9); col(NAVY); doc.text(pdfTxt(f.name), M, y + 5.3);
          A.levels.forEach(function (l, i) {
            var cx = x0 + i * cw;
            if (i === v.c) doc.setFillColor(NAVY[0], NAVY[1], NAVY[2]); else if (i > v.c && i <= v.t) doc.setFillColor(TINT[0], TINT[1], TINT[2]); else doc.setFillColor(247, 248, 250);
            doc.setDrawColor(255, 255, 255); doc.rect(cx, y, cw - 1, rh - 1.2, 'F');
            var lab = i === v.c ? (v.c === v.t ? 'Today = target' : 'Today') : (i === v.t ? 'Target' : '');
            if (lab) { doc.setFont('helvetica', 'bold'); doc.setFontSize(8); col(i === v.c ? [255, 255, 255] : NAVY); doc.text(lab, cx + (cw - 1) / 2, y + 4.6, { align: 'center' }); }
          });
          y += rh;
        });
        y += 3;
      }
      head();
      // title band
      doc.setFillColor(NAVY[0], NAVY[1], NAVY[2]); doc.rect(M, y - 4, CW, 30, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(21); doc.setTextColor(255, 255, 255); doc.text('Your Digital Roadmap', M + 7, y + 7);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
      doc.text(pdfTxt('Prepared for ' + ([who, co].filter(Boolean).join(', ') || 'your business') + '  |  ' + IND[ans.ind].name), M + 7, y + 15);
      doc.text(pdfTxt('Chmltech Digital Needs Assessment  |  ' + date), M + 7, y + 21);
      y += 34;
      REP.secs.forEach(function (sec) {
        sectionHead(sec[0]);
        if (/^3\./.test(sec[0])) { maturity(); }
        var lines = String(sec[1]).split('\n');
        lines.forEach(function (ln) {
          if (/^3\./.test(sec[0]) && !/^Levels/.test(ln)) return;
          if (!ln.trim()) { y += 2.5; return; }
          var t = pdfTxt(ln), ind = /^\s{3}/.test(ln) ? 6 : 0;
          if (/^(\d+)\. /.test(t) && /^6\.|^4\./.test(sec[0]) ) { room(36); y += 1; para(t, { bold: true, plain: true, hang: 6, color: NAVY, size: 10.2 }); return; }
          if (/^Priority \d/.test(t)) { room(24); y += 1; para(t, { bold: true, plain: true, color: NAVY, size: 10.2 }); return; }
          if (/^(\d+)\. /.test(t)) { para(t, { hang: 5.5 }); return; }
          if (/^- /.test(t)) { para('•  ' + t.slice(2), { hang: 4 }); return; }
          para(t.trim(), { ind: ind, hang: 0, color: /^Levels/.test(t) ? MUT : null, size: /^Levels/.test(t) ? 8.5 : null });
        });
        y += 2;
      });
      room(30); y += 4;
      doc.setFillColor(TINT[0], TINT[1], TINT[2]); doc.rect(M, y, CW, 20, 'F');
      doc.setFont('helvetica', 'bold'); doc.setFontSize(11); col(NAVY); doc.text('Talk it through with us', M + 6, y + 8);
      doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5); doc.text('Free 30-minute roadmap review:  www.chmltech.com/book   |   info@chmltech.com', M + 6, y + 14.5);
      doc.link(M, y, CW, 20, { url: SITE + 'book' });
      var n = doc.getNumberOfPages();
      for (var i = 1; i <= n; i++) {
        doc.setPage(i); doc.setDrawColor(LINE[0], LINE[1], LINE[2]); doc.setLineWidth(0.3); doc.line(M, 283, W - M, 283);
        doc.setFont('helvetica', 'normal'); doc.setFontSize(8); col(MUT);
        doc.text('Chmltech Ltd.  |  Burnaby, BC  |  www.chmltech.com', M, 288); doc.text('Page ' + i + ' of ' + n, W - M, 288, { align: 'right' });
      }
      doc.setProperties({ title: 'Your Digital Roadmap — Chmltech', author: 'Chmltech Ltd.', subject: 'Digital Needs Assessment report' });
      var slug = (co || 'Report').replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 40) || 'Report';
      return { doc: doc, file: 'Chmltech_Digital_Roadmap_' + slug + '.pdf' };
    });
  }
  window.ChmlReportText = function () { return REP ? REP.secs.map(function (x) { return x[0] + '\n' + x[1]; }).join('\n\n') : ''; };
  window.ChmlReportIndustry = function () { return ans.ind && IND[ans.ind] ? IND[ans.ind].name : ''; };
  window.ChmlReportPdf = function () { return makePdf().then(function (o) { return { blob: o.doc.output('blob'), file: o.file }; }); };

  /* ---- Full report as plain text for the email (Web3Forms sends each field in order) ---- */
  var SITE = 'https://www.chmltech.com/';
  function optLabel(k, v) { var sc = SCREENS.filter(function (x) { return x.k === k; })[0]; var o = sc && sc.o ? sc.o().filter(function (x) { return x[0] === v; })[0] : null; return o ? o[1] : v; }
  function demoQs(cid, prod) {
    var cp = caps(cid, cid === 'erp' ? erpWf() : null), wts = cp.map(function () { return 1; });
    (ans.prob || []).forEach(function (pid) { var w = (PRB[pid].w || {})[cid]; if (w) cp.forEach(function (k, i) { if (w[k.k] != null) wts[i] = Math.max(wts[i], w[k.k]); }); });
    var order = cp.map(function (k, i) { return { k: k, w: wts[i] }; }).sort(function (a, b) { return b.w - a.w; }).slice(0, 4);
    var qs = order.map(function (x) { return 'Show us, with our own data, how it handles ' + x.k.n.toLowerCase() + ' (' + x.k.d.replace(/\.$/, '') + ').'; });
    qs.push('What will the first year cost in total: licences, set-up, data migration, training and support?');
    qs.push('Who implements it in Canada, how long does it take, and can we speak to a Canadian client of a similar size?');
    if (prod && prod.rc) qs.push('Our reviewer noted: "' + prod.rc + '" How do you address this?');
    return qs;
  }
  function buildReport(r, q, opts) {
    var L = [], fnGap = {}, lvn = ['Must', 'Should', 'Could'];
    var biz = IND[ans.ind].name + (ans.sub && A.subtypes[ans.ind] ? ' (' + optLabel('sub', ans.sub) + ')' : '');
    L.push(['1. Your business',
      'Report date: ' + new Date().toLocaleDateString('en-CA', { year: 'numeric', month: 'long', day: 'numeric' }) + '\nIndustry: ' + biz + '\nPeople: ' + optLabel('size', ans.size) + '\nBudget for the first project: ' + optLabel('budget', ans.budget) +
      '\nRunning the business on: ' + ((ans.tools || []).map(function (t) { return optLabel('tools', t); }).join(', ') || 'not stated') +
      '\nPriorities for the next 2–3 years: ' + ((ans.prio || []).map(function (p) { return optLabel('prio', p); }).join(', ') || 'not stated')]);
    L.push(['2. Challenges you picked', (ans.prob || []).map(function (p, i) { return (i + 1) + '. ' + PRB[p].t; }).join('\n') || 'None picked']);
    L.push(['3. Digital maturity (today → two-year target)', A.functions.map(function (f) {
      var v = ans.mat[f.id], g = r.gap[f.id]; fnGap[f.id] = g;
      return f.name + ': ' + A.levels[v.c].n + ' → ' + A.levels[v.t].n + (g > 0 ? ' (gap ' + g + ')' : ' (on target)');
    }).join('\n') + '\nLevels: ' + A.levels.map(function (l) { return l.n; }).join(', ') + '.']);
    L.push(['4. Your technology priorities', r.top.map(function (x, i) {
      return 'Priority ' + (i + 1) + ' (' + lvn[i] + '): ' + x.c.name + (x.own ? ' — you have this: optimise it' : '') + '\n   ' + x.c.benefit +
        (x.why.length ? '\n   Why: ' + x.why.slice(0, 3).join('; ') : '') + (x.gap ? '\n   ' + FN[x.c.fn].name + ': ' + x.gap + '-level gap to your target' : '');
    }).join('\n\n') || 'No clear gap from the answers given.']);
    if (q) {
      L.push(['5. ' + (r.quick ? 'Your quick win' : 'Your first project') + ': ' + q.c.name, q.c.desc + ' ' + q.c.benefit +
        '\nTime to value: ' + q.c.weeks + '\nImplementation risk: ' + ['', 'Higher', 'Medium', 'Low'][q.c.ease] +
        '\nYear-one cost: ' + (opts.length ? PRICE[Math.min.apply(null, opts.map(function (o) { return o.p.price; }))] : 'see options') +
        '\nSupports: ' + FN[q.c.fn].name + ((q.c.links || []).length ? '\nFree resources:\n' + q.c.links.map(function (l) { return '- ' + l[1] + ': ' + SITE + l[0].replace(/\.html$/, ''); }).join('\n') : '')]);
    } else {
      L.push(['5. Your first step', (r.top.some(function (x) { return x.c.id === 'erp'; }) ? 'Start with an ERP readiness review.' : 'Start with a short process review.') + ' None of your priorities has a fast, low-risk project within your budget; a short review of processes and data makes the bigger project faster and cheaper.']);
    }
    var oc = q ? q.c.id : (r.top[0] ? r.top[0].c.id : null), ol = q ? opts : (oc ? options(oc) : []);
    if (ol.length) {
      L.push(['6. Software options to evaluate (' + CAT[oc].name + ')', ol.map(function (o, i) {
        var u = safeUrl(o.p.url);
        return (i + 1) + '. ' + o.p.name + ' — ' + o.fit + '% fit to your answers' + '\n   Best for: ' + (o.p.best || '') + '\n   Year-one cost: ' + PRICE[o.p.price] +
          '\n   In Canada: ' + (o.p.canada || '') + (o.p.rc ? '\n   Reality check: ' + o.p.rc : '') + (o.flags.length ? '\n   Note: ' + o.flags.join(' ') : '') + (u ? '\n   Website: ' + u : '');
      }).join('\n\n')]);
      L.push(['7. Questions to ask in demos', ol.slice(0, 1).map(function (o) { return demoQs(oc, o.p).map(function (x, i) { return (i + 1) + '. ' + x; }).join('\n'); }).join('')]);
    }
    var plan = [];
    plan.push('Weeks 1–2: confirm requirements for ' + (q ? q.c.name.toLowerCase() : 'your first priority') + ' with the people who will use it; list must-haves from the challenges above.');
    plan.push('Weeks 3–6: book demos with the options above using the demo questions; get written quotes for year one.');
    plan.push('Weeks 6–8: choose, check references, and check funding before you sign.');
    plan.push('Then (about ' + (q ? q.c.weeks : '2–4 months') + '): implement, clean and move your data, train staff, and measure the result.');
    r.top.forEach(function (x, i) { if (!q || x.c.id !== q.c.id) plan.push('Next: Priority ' + (i + 1) + ' (' + lvn[i] + ') ' + x.c.name + ', once the first project is running.'); });
    A.functions.forEach(function (f) { if (fnGap[f.id] > 0 && !r.top.some(function (x) { return x.c.fn === f.id; })) plan.push(f.name + ': close a ' + fnGap[f.id] + '-level gap; ask us which tool fits.'); });
    L.push(['8. Action plan', plan.map(function (x, i) { return (i + 1) + '. ' + x; }).join('\n')]);
    if (oc && oc !== 'ai') {
      var want = SZA[ans.size] || [];
      var mv = DIR.filter(function (e) { return e.g === oc && !e.sc && indOk(e, ans.ind) && (!e.sz.length || e.sz.some(function (z) { return want.indexOf(z) >= 0; })); })
        .sort(function (a, b) { return (b.sz.length ? 1 : 0) - (a.sz.length ? 1 : 0) || (b.ca ? 1 : 0) - (a.ca ? 1 : 0) || a.n.localeCompare(b.n); }).slice(0, 6);
      if (mv.length) L.push(['9. More vendors to consider (not scored)', mv.map(function (e) { return '- ' + e.n + (e.ca ? ' (Canadian)' : '') + (safeUrl(e.u) ? ': ' + e.u : ''); }).join('\n')]);
    }
    var sug = aiSuggest();
    if (sug.length) L.push(['10. AI tools to try', sug.map(function (x) {
      return x.name + ' (for: ' + x.why.join('; ') + ')\n' + x.tools.map(function (t) { return '- ' + t.n + (t.fit ? ', ' + t.fit + '% fit' : '') + ', ' + aiPrice(t.pr).t + (safeUrl(t.u) ? ': ' + t.u : ''); }).join('\n');
    }).join('\n\n') + '\nSet rules on what company data staff may put into AI tools.']);
    L.push(['11. Funding', 'Government programs can cover part of a digital project. Use the free Funding Match at ' + SITE + 'funding#match to see which programs fit your business and project, and ask us before you sign.']);
    L.push(['12. Next step', 'Book a free 30-minute review of this roadmap: ' + SITE + 'book\nTake the assessment again: ' + SITE + 'digital-assessment\nScores are our analyst rating from vendor information (November 2026); confirm them in a demo. Prices in US dollars unless marked.']);
    return L;
  }
  vdInit(); aiInit();

  function openProd(cid, id) {
    var p = products(cid).filter(function (x) { return x.id === id; })[0]; if (!p) return;
    var wf = cid === 'erp' ? (fs.cat === 'erp' && p.s[fs.wf] ? fs.wf : (erpWf() && p.s[erpWf()] ? erpWf() : Object.keys(p.s).filter(function (k) { return WF[k] && p.s[k]; })[0])) : null, cp = caps(cid, wf), s = scores(p, cid, wf);
    $('#erp-dlg-title').textContent = p.name;
    $('#erp-dlg-sub').textContent = CAT[cid].name + (cid === 'erp' ? ' · ' + WF[wf].name : '') + ' · Best for: ' + p.best;
    var rc = typeof p.rc === 'string' ? '<p style="margin:0">' + esc(p.rc) + '</p>' :
      '<dl><dt>Hidden cost</dt><dd>' + esc(p.rc.hidden) + '</dd><dt>Budget reality</dt><dd>' + esc(p.rc.cost) + '</dd><dt>Unit-of-measure</dt><dd>' + esc(p.rc.uom) + '</dd><dt>Shop-floor readiness</dt><dd>' + esc(p.rc.floor) + '</dd></dl>';
    $('#erp-dlg-body').innerHTML =
      '<div class="erp-facts"><div><b>Deployment</b><span>' + p.deploy.join(' / ') + '</span></div><div><b>Company size</b><span>' + p.size.map(function (z) { return SIZE[z]; }).join(', ') + '</span></div><div><b>Year-one cost</b><span>' + PRICE[p.price] + '</span></div><div><b>In Canada</b><span>' + esc(p.canada) + '</span></div>' + (safeUrl(p.url) ? '<div><b>Website</b><span><a href="' + esc(safeUrl(p.url)) + '" target="_blank" rel="noopener nofollow">' + esc(p.name) + '</a></span></div>' : '') + (p.months ? '<div><b>Typical go-live</b><span>' + p.months + ' months</span></div>' : '') + '</div>' +
      '<div class="erp-rc"><h4>Consultant Reality Check</h4>' + rc + '</div>' +
      '<div><h4 style="font-size:17px;margin-bottom:10px">Capabilities</h4><table class="as-captable">' + cp.map(function (k, i) { return '<tr><td>' + dot(s[i]) + '</td><td><strong>' + esc(k.n) + '</strong><br><small>' + esc(k.d) + (k.r ? ' <em>Native: ' + esc(k.r) + '</em>' : '') + '</small></td><td class="muted">' + LEVEL[s[i]] + '</td></tr>'; }).join('') + '</table></div>' +
      (cid === 'erp' ? '<div><h4 style="font-size:17px;margin-bottom:10px">Fit by type of business</h4><div class="erp-wfscores">' + A.erp.workflows.filter(function (w) { return p.s[w.id]; }).map(function (w) { return '<div><b>' + esc(w.short) + '</b><em>' + avgFit(p.s[w.id]) + '%</em></div>'; }).join('') + '</div></div>' : '') +
      (p.unv && p.unv.length ? '<div class="as-empty"><p><strong>Independent reviewers could not confirm:</strong> ' + p.unv.map(esc).join('; ') + '. Treat these scores as unconfirmed and test them in a demo.</p></div>' : '') +
      '<p class="muted" style="font-size:13.5px">' + (safeUrl(p.src) ? 'Source: <a href="' + esc(safeUrl(p.src)) + '" rel="noopener" target="_blank">vendor information</a>. ' : '') + 'Scores are our analyst rating: confirm them in a demo.</p>';
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
  }
})();
