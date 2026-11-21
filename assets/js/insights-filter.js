/* Insights filter (sidebar facets) — V2, 2026-11-21 (red team fixes; first published in site V5.62).
   Reads everything from the article cards already in the page, so the cards need no extra attributes and the
   build scripts (add_article, add_journal_paper, refresh_article, insights_finder) keep working:
     format   <- data-cats (chmltech-online-journal / case-study / book-review, else article)
     date     <- the last "Mon D, YYYY" in .meta        read time <- "N min read" in .meta
     series   <- .series "Name series · Part N of M"    journal division <- the card's subject label
   Then it shows, hides and re-orders the cards. Live counts, #format=…&topic=… in the address,
   old #cat= links still work. No libraries. */
(function () {
  var root = document.querySelector('[data-ifl]'); if (!root) return;
  var $ = function (s, r) { return (r || root).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || root).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var PAGE = 24;

  /* ---------- taxonomy ---------- */
  var FORMATS = [['all', 'All'], ['post', 'Articles'], ['journal', 'Journal papers'], ['case', 'Case studies'], ['book', 'Book reviews']];
  var NOUN = { all: ['article', 'articles'], post: ['article', 'articles'], journal: ['paper', 'papers'], case: ['case study', 'case studies'], book: ['book review', 'book reviews'] };
  var FMT_CAT = { 'chmltech-online-journal': 'journal', 'case-study': 'case', 'book-review': 'book' };
  var GROUPS = [
    { k: 'ops', n: 'Operations', col: '#13366E', subs: [['operational-efficiency', 'Operational Efficiency'], ['inventory-management', 'Inventory Management']] },
    { k: 'quality', n: 'Improvement & Quality', col: '#4D7F12', subs: [['process-improvement', 'Process Improvement'], ['lean', 'Lean'], ['six-sigma', 'Six Sigma'], ['iso', 'ISO']] },
    { k: 'digital', n: 'AI & Digital', col: '#0B6FA4', subs: [['artificial-intelligence', 'Artificial Intelligence'], ['digital-technology', 'Digital Technology'], ['erp', 'ERP & Systems']] },
    { k: 'eng', n: 'Process Engineering', col: '#1F6B6B', subs: [['process-engineering', 'Process Engineering']] },
    { k: 'growth', n: 'Strategy & Growth', col: '#8A5A1F', subs: [['strategy', 'Strategy'], ['marketing', 'Sales & Marketing'], ['change-pm', 'Change & Project Mgmt'], ['esg', 'ESG']] }
  ];
  var SUB = {}, SUB2G = {};
  GROUPS.forEach(function (g) { g.subs.forEach(function (s) { SUB[s[0]] = s[1]; SUB2G[s[0]] = g; }); });
  /* journal division follows the paper's subject label (checked against all 31 paper pages, Nov 2026) */
  var DIVS = [['ai', 'AI & Machine Learning', 'Artificial Intelligence'], ['energy', 'Clean Energy Technology', 'Process Engineering'], ['opex', 'Operational Excellence', 'Operational Efficiency']];
  var READ = [['quick', 'Quick read (under 8 min)', function (r) { return r < 8; }], ['std', 'Standard (8–14 min)', function (r) { return r >= 8 && r < 15; }], ['deep', 'In-depth (15 min or more)', function (r) { return r >= 15; }]];
  var SORTS = [['new', 'Newest first'], ['old', 'Oldest first'], ['short', 'Quick reads first'], ['long', 'In-depth first']];
  var MON = { Jan: '01', Feb: '02', Mar: '03', Apr: '04', May: '05', Jun: '06', Jul: '07', Aug: '08', Sep: '09', Oct: '10', Nov: '11', Dec: '12' };
  var slug = function (s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''); };
  var txt = function (el, sel) { var x = el.querySelector(sel); return x ? x.textContent.replace(/\s+/g, ' ').trim() : ''; };

  /* ---------- read the cards ---------- */
  var grid = $('[data-items]');
  var SERIES = {}, SERIES_ORDER = [], YEARSET = {};
  var ITEMS = $$('article', grid).map(function (el, i) {
    var c = (el.getAttribute('data-cats') || '').split(/\s+/).filter(Boolean);
    var meta = txt(el, '.meta'), label = txt(el, '.cat-label'), ser = txt(el, '.series');
    var dm = meta.match(/([A-Z][a-z]{2}) (\d{1,2}), (\d{4})(?!.*[A-Z][a-z]{2} \d{1,2}, \d{4})/);
    var rm = meta.match(/(\d+)\s*min read/);
    var o = { el: el, i: i, c: c, f: 'post', d: dm && MON[dm[1]] ? dm[3] + '-' + MON[dm[1]] + '-' + ('0' + dm[2]).slice(-2) : '0000-00-00', r: rm ? +rm[1] : 0,
      sk: null, sn: null, p: 0, dv: null, hay: (el.getAttribute('data-search') || '') + ' ' + ser.toLowerCase() };
    c.forEach(function (x) { if (FMT_CAT[x]) o.f = FMT_CAT[x]; });
    o.t = c.filter(function (x) { return SUB[x]; });
    if (c.indexOf('change-management') > -1 || c.indexOf('project-management') > -1) o.t.push('change-pm');
    if (o.f === 'journal') DIVS.forEach(function (d) { if (label === d[2]) o.dv = d[0]; });
    if (ser) {
      var sm = ser.match(/^(.*?series)(?:\s*·\s*Part (\d+) of (\d+))?/i);
      if (sm) { o.sn = sm[1]; o.sk = slug(sm[1].replace(/ series$/i, '')); o.p = sm[2] ? +sm[2] : 0;
        if (!SERIES[o.sk]) { SERIES[o.sk] = { k: o.sk, n: o.sn, items: [] }; SERIES_ORDER.push(o.sk); } SERIES[o.sk].items.push(o); }
    }
    o.y = o.d.slice(0, 4); YEARSET[o.y] = 1;
    return o;
  });
  SERIES_ORDER.sort(function (a, b) { return /case/.test(a) - /case/.test(b) || SERIES[b].items.length - SERIES[a].items.length; });
  /* years from the data: the three latest years each get an option, anything older is grouped */
  var ys = Object.keys(YEARSET).filter(function (y) { return y !== '0000'; }).sort().reverse(), YEARS = ys.slice(0, 3).map(function (y) { return [y, y]; });
  if (ys.length > 3) { var old = ys.slice(3); YEARS.push(['older', (old.length > 1 ? old[old.length - 1] + '–' : '') + old[0]]); }
  var yearKey = function (y) { return YEARS.some(function (x) { return x[0] === y; }) ? y : 'older'; };
  ITEMS.forEach(function (o) { o.yk = yearKey(o.y); });

  /* ---------- state ---------- */
  function blank() { return { f: 'all', dv: null, t: [], s: null, rt: null, y: null, q: '', sort: 'new' }; }
  var st = blank(), shown = PAGE, open = {};
  var words = function (q) { return q.toLowerCase().split(/\s+/).filter(function (x) { return x.length > 1; }); };
  function matches(o, s) {
    if (s.f !== 'all' && o.f !== s.f) return false;
    if (s.dv && o.dv !== s.dv) return false;
    if (s.t.length && !s.t.some(function (t) { return o.t.indexOf(t) > -1; })) return false;
    if (s.s && o.sk !== s.s) return false;
    if (s.rt) { var fn = READ.filter(function (r) { return r[0] === s.rt; })[0][2]; if (!fn(o.r)) return false; }
    if (s.y && o.yk !== s.y) return false;
    var w = words(s.q); if (w.length && !w.every(function (x) { return o.hay.indexOf(x) > -1; })) return false;
    return true;
  }
  function count(patch) { var s = {}, k; for (k in st) s[k] = st[k]; for (k in patch) s[k] = patch[k]; var n = 0; ITEMS.forEach(function (o) { if (matches(o, s)) n++; }); return n; }
  var partOrder = function () { return st.s && !/case/.test(st.s); };
  function sorted(list) {
    var newest = function (a, b) { return a.d < b.d ? 1 : a.d > b.d ? -1 : a.i - b.i; };
    var by = st.sort === 'series' ? function (a, b) { return (a.p || 99) - (b.p || 99) || a.i - b.i; }
      : st.sort === 'old' ? function (a, b) { return a.d < b.d ? -1 : a.d > b.d ? 1 : a.i - b.i; }
      : st.sort === 'short' ? function (a, b) { return a.r - b.r || newest(a, b); }
      : st.sort === 'long' ? function (a, b) { return b.r - a.r || newest(a, b); }
      : newest;
    return list.slice().sort(by);
  }
  /* topic groups that are fully selected, plus loose sub-topics */
  function topicParts() {
    var full = GROUPS.filter(function (g) { return g.subs.length > 1 && g.subs.every(function (x) { return st.t.indexOf(x[0]) > -1; }); });
    var inFull = {}; full.forEach(function (g) { g.subs.forEach(function (x) { inFull[x[0]] = 1; }); });
    return { groups: full, subs: st.t.filter(function (t) { return !inFull[t]; }) };
  }

  /* ---------- address bar ---------- */
  function toHash() {
    var p = [];
    if (st.f !== 'all') p.push('format=' + st.f);
    if (st.dv) p.push('division=' + st.dv);
    if (st.t.length) { var tp = topicParts(); p.push('topic=' + tp.groups.map(function (g) { return g.k; }).concat(tp.subs).join(',')); }
    if (st.s) p.push('series=' + st.s);
    if (st.rt) p.push('read=' + st.rt);
    if (st.y) p.push('year=' + st.y);
    if (st.q) p.push('q=' + encodeURIComponent(st.q));
    var dflt = partOrder() ? 'series' : 'new';
    if (st.sort !== dflt) p.push('sort=' + st.sort);
    return p.join('&');
  }
  function writeHash() {
    var h = toHash();
    if (!h && /^#goal-/.test(location.hash)) return;           /* keep an open "Start here" goal in the address */
    try { history.replaceState(null, '', location.pathname + location.search + (h ? '#' + h : '')); } catch (e) {}
  }
  function dec(v) { try { return decodeURIComponent(v); } catch (e) { return null; } }   /* a bad %-escape is ignored, not fatal */
  function readHash() {
    var h = location.hash.replace(/^#/, ''), s = blank(), legacy = false, sort = null;
    if (!h || h.indexOf('=') < 0) return { s: s, legacy: false };
    h.split('&').forEach(function (kv) {
      var i = kv.indexOf('='); if (i < 1) return;
      var k = kv.slice(0, i), v = dec(kv.slice(i + 1)); if (v === null) return;
      if (k === 'cat') { /* old chip links, post tags and the "Start here" panel: #cat=lean, #cat=chmltech-online-journal, #cat=clean-energy */
        legacy = true;
        if (v === 'clean-energy') v = 'chmltech-online-journal';
        if (v === 'change-management' || v === 'project-management') v = 'change-pm';
        if (FMT_CAT[v]) s.f = FMT_CAT[v]; else if (SUB[v]) s.t = [v];
      }
      if (k === 'format' && FORMATS.some(function (f) { return f[0] === v; })) s.f = v;
      if (k === 'division' && DIVS.some(function (d) { return d[0] === v; })) s.dv = v;
      if (k === 'topic') v.split(',').forEach(function (tok) {
        var g = GROUPS.filter(function (x) { return x.k === tok; })[0];
        if (g) g.subs.forEach(function (x) { if (s.t.indexOf(x[0]) < 0) s.t.push(x[0]); }); else if (SUB[tok] && s.t.indexOf(tok) < 0) s.t.push(tok);
      });
      if (k === 'series' && SERIES[v]) s.s = v;
      if (k === 'read' && READ.some(function (r) { return r[0] === v; })) s.rt = v;
      if (k === 'year' && YEARS.some(function (y) { return y[0] === v; })) s.y = v;
      if (k === 'q') s.q = v.slice(0, 200);
      if (k === 'sort') sort = v;
    });
    if (s.f !== 'journal') s.dv = null;
    var pOrder = s.s && !/case/.test(s.s);
    s.sort = sort && (SORTS.some(function (x) { return x[0] === sort; }) || (sort === 'series' && pOrder)) ? sort : pOrder ? 'series' : 'new';
    return { s: s, legacy: legacy };
  }

  /* ---------- sidebar ---------- */
  function opt(type, name, val, label, n, checked, extra) {
    var zero = n === 0 && !checked;
    return '<label class="ifl-opt' + (zero ? ' zero' : '') + '"><input type="' + type + '" name="' + name + '" value="' + esc(val) + '"' + (checked ? ' checked' : '') + (zero ? ' disabled' : '') + '><span>' + (extra || '') + esc(label) + '</span><span class="c">' + n + '</span></label>';
  }
  var CHEV = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M3 5l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>';
  function renderSide() {
    $('[data-f]').innerHTML = FORMATS.map(function (f) { return opt('radio', 'ifl-f', f[0], f[1], count({ f: f[0], dv: null }), st.f === f[0]); }).join('');
    $('[data-dvwrap]').hidden = st.f !== 'journal';
    $('[data-dv]').innerHTML = opt('radio', 'ifl-dv', '', 'All divisions', count({ dv: null }), !st.dv) +
      DIVS.map(function (d) { return opt('radio', 'ifl-dv', d[0], d[1], count({ dv: d[0] }), st.dv === d[0]); }).join('');
    $('[data-t]').innerHTML = GROUPS.map(function (g) {
      var subs = g.subs.map(function (x) { return x[0]; });
      var on = subs.filter(function (s) { return st.t.indexOf(s) > -1; }).length;
      var n = count({ t: subs });
      var multi = subs.length > 1, ex = multi && (open[g.k] || (on > 0 && on < subs.length));
      var html = '<div class="ifl-tg">' + opt('checkbox', 'ifl-g', g.k, g.n, n, on === subs.length, '<span class="ifl-dot" style="background:' + g.col + '" aria-hidden="true"></span>') +
        (multi ? '<button type="button" class="ifl-x" data-x="' + g.k + '" aria-expanded="' + !!ex + '" aria-controls="ifl-subs-' + g.k + '" aria-label="' + (ex ? 'Hide ' : 'Show ') + esc(g.n) + ' sub-topics">' + CHEV + '</button>' : '') + '</div>';
      if (ex) html += '<div class="ifl-subs" id="ifl-subs-' + g.k + '" role="group" aria-label="' + esc(g.n) + ' sub-topics">' + g.subs.map(function (s) { return opt('checkbox', 'ifl-t', s[0], s[1], count({ t: [s[0]] }), st.t.indexOf(s[0]) > -1); }).join('') + '</div>';
      return html;
    }).join('');
    $$('[data-t] input[name="ifl-g"]').forEach(function (cb) {
      var g = GROUPS.filter(function (x) { return x.k === cb.value; })[0], on = g.subs.filter(function (s) { return st.t.indexOf(s[0]) > -1; }).length;
      cb.indeterminate = on > 0 && on < g.subs.length;
    });
    $('[data-s]').innerHTML = opt('radio', 'ifl-s', '', 'Any', count({ s: null }), !st.s) +
      SERIES_ORDER.map(function (k) { return opt('radio', 'ifl-s', k, SERIES[k].n.replace(/ series$/i, ''), count({ s: k }), st.s === k); }).join('');
    $('[data-rt]').innerHTML = opt('radio', 'ifl-rt', '', 'Any length', count({ rt: null }), !st.rt) +
      READ.map(function (r) { return opt('radio', 'ifl-rt', r[0], r[1], count({ rt: r[0] }), st.rt === r[0]); }).join('');
    $('[data-y]').innerHTML = opt('radio', 'ifl-y', '', 'Any year', count({ y: null }), !st.y) +
      YEARS.map(function (y) { return opt('radio', 'ifl-y', y[0], y[1], count({ y: y[0] }), st.y === y[0]); }).join('');
    var tp = topicParts();
    var sel = { f: st.f !== 'all' ? 1 : 0, dv: st.dv ? 1 : 0, t: tp.groups.length + tp.subs.length, s: st.s ? 1 : 0, rt: st.rt ? 1 : 0, y: st.y ? 1 : 0 };
    $$('[data-seln]').forEach(function (el) { var n = sel[el.getAttribute('data-seln')]; el.hidden = !n; el.textContent = n; });
    if (st.s) $('[data-swrap]').open = true;
    if (st.rt) $('[data-rtwrap]').open = true;
    if (st.y) $('[data-ywrap]').open = true;
    var total = actives().length;                               /* badge = number of removable chips */
    var badge = $('[data-badge]'); badge.hidden = !total; badge.textContent = total;
    $('.ifl-head [data-clear]').hidden = !total;
  }

  /* ---------- results ---------- */
  var X = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" stroke-width="1.8"/></svg>';
  function actives() {
    var a = [];
    if (st.f !== 'all') a.push(['f', FORMATS.filter(function (f) { return f[0] === st.f; })[0][1]]);
    if (st.dv) a.push(['dv', DIVS.filter(function (d) { return d[0] === st.dv; })[0][1]]);
    var tp = topicParts();
    tp.groups.forEach(function (g) { a.push(['g:' + g.k, g.n]); });
    tp.subs.forEach(function (t) { a.push(['t:' + t, SUB[t]]); });
    if (st.s) a.push(['s', SERIES[st.s].n]);
    if (st.rt) a.push(['rt', READ.filter(function (r) { return r[0] === st.rt; })[0][1]]);
    if (st.y) a.push(['y', 'Published ' + YEARS.filter(function (y) { return y[0] === st.y; })[0][1]]);
    if (words(st.q).length) a.push(['q', '“' + st.q + '”']);
    return a;
  }
  function renderResults() {
    var list = sorted(ITEMS.filter(function (o) { return matches(o, st); }));
    var noun = NOUN[st.f];
    $('[data-count]').innerHTML = '<b>' + list.length + ' ' + noun[list.length === 1 ? 0 : 1] + '</b>' + (list.length !== ITEMS.length ? ' of ' + ITEMS.length : '');
    var act = actives();
    $('[data-act]').innerHTML = act.map(function (a) { return '<li><button type="button" data-rm="' + a[0] + '" aria-label="Remove filter: ' + esc(a[1]) + '">' + esc(a[1]) + X + '</button></li>'; }).join('');
    $('[data-res] [data-clear]').hidden = act.length < 2;
    var si = $('[data-sintro]');
    if (st.s) {
      var S = SERIES[st.s], isCase = /case/.test(st.s), byPart = S.items.slice().sort(function (a, b) { return (a.p || 99) - (b.p || 99); });
      var mins = S.items.reduce(function (t, o) { return t + o.r; }, 0), first = byPart[0].el.querySelector('h3 a');
      si.hidden = false;
      si.innerHTML = '<b>' + esc(S.n) + '</b><span>' + S.items.length + (isCase ? ' cases, read in any order' : ' parts, read in order') + ' · about ' + mins + ' min in total</span>' +
        (isCase || !first ? '' : '<a href="' + esc(first.getAttribute('href')) + '">Start at Part 1 →</a>');
    } else si.hidden = true;
    ITEMS.forEach(function (o) { o.el.hidden = true; });
    list.forEach(function (o, i) { grid.appendChild(o.el); o.el.hidden = i >= shown; });
    var empty = $('[data-empty]');
    empty.style.display = list.length ? 'none' : 'block';
    if (!list.length) {
      $('[data-emptytitle]').textContent = 'No ' + noun[1] + ' match these filters.';
      $('[data-emptyhint]').textContent = words(st.q).length ? 'Try fewer or different words, or clear the filters to search all ' + ITEMS.length + ' articles.' : 'Try removing a filter.';
    }
    var mw = $('[data-morewrap]'); mw.style.display = list.length > shown ? '' : 'none';
    $('[data-moreinfo]').textContent = 'Showing ' + Math.min(shown, list.length) + ' of ' + list.length;
    $('[data-showbtn]').textContent = 'Show ' + list.length + ' ' + noun[list.length === 1 ? 0 : 1];
  }
  function fillSort() {
    var opts = partOrder() ? [['series', 'Part order']].concat(SORTS) : SORTS;
    $('[data-sort]').innerHTML = opts.map(function (o) { return '<option value="' + o[0] + '"' + (st.sort === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('');
    var q = $('[data-q]'); if (q.value !== st.q && document.activeElement !== q) q.value = st.q;
  }
  function render(keepHash) { fillSort(); renderSide(); renderResults(); if (!keepHash) writeHash(); }
  function change(fn) { var hadSeries = st.s; fn(); shown = PAGE;
    if (st.s !== hadSeries) st.sort = partOrder() ? 'series' : (st.sort === 'series' ? 'new' : st.sort);
    if (st.sort === 'series' && !partOrder()) st.sort = 'new';
    render(); }

  /* ---------- events ---------- */
  var side = $('[data-side]');
  side.addEventListener('change', function (e) {
    var t = e.target; if (!t.name) return; var v = t.value, name = t.name;
    change(function () {
      if (name === 'ifl-f') { st.f = v; if (v !== 'journal') st.dv = null; }
      if (name === 'ifl-dv') st.dv = v || null;
      if (name === 'ifl-s') st.s = v || null;
      if (name === 'ifl-rt') st.rt = v || null;
      if (name === 'ifl-y') st.y = v || null;
      if (name === 'ifl-g') { var g = GROUPS.filter(function (x) { return x.k === v; })[0], subs = g.subs.map(function (x) { return x[0]; });
        st.t = st.t.filter(function (s) { return subs.indexOf(s) < 0; }); if (t.checked) st.t = st.t.concat(subs); }
      if (name === 'ifl-t') { if (t.checked) st.t.push(v); else st.t = st.t.filter(function (s) { return s !== v; }); open[SUB2G[v].k] = true; }
    });
    var again = side.querySelector('input[name="' + name + '"][value="' + v + '"]'); if (again) again.focus();
  });
  side.addEventListener('click', function (e) {
    var x = e.target.closest('[data-x]'); if (!x) return;
    var k = x.getAttribute('data-x'); open[k] = x.getAttribute('aria-expanded') !== 'true'; renderSide();
    var b = side.querySelector('[data-x="' + k + '"]'); if (b) b.focus();
  });
  var timer;
  $('[data-q]').addEventListener('input', function (e) { var v = e.target.value.slice(0, 200); clearTimeout(timer); timer = setTimeout(function () { change(function () { st.q = v.trim(); }); }, 120); });
  $('[data-sort]').addEventListener('change', function (e) { var v = e.target.value; change(function () { st.sort = v; }); });
  root.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.hasAttribute('data-clear')) {
      var inSheet = !!b.closest('[data-side]') && side.classList.contains('open');
      change(function () { st = blank(); });
      if (!inSheet) $('[data-q]').focus();                        /* keep keyboard users in place, not at the top of the page */
    }
    if (b.hasAttribute('data-rm')) {
      var k = b.getAttribute('data-rm'), idx = $$('[data-act] button').indexOf(b);
      change(function () {
        if (k === 'f') { st.f = 'all'; st.dv = null; } else if (k === 'dv') st.dv = null;
        else if (k.indexOf('g:') === 0) { var g = GROUPS.filter(function (x) { return x.k === k.slice(2); })[0]; st.t = st.t.filter(function (t) { return !g.subs.some(function (x) { return x[0] === t; }); }); }
        else if (k.indexOf('t:') === 0) st.t = st.t.filter(function (t) { return t !== k.slice(2); });
        else if (k === 's') st.s = null; else if (k === 'rt') st.rt = null; else if (k === 'y') st.y = null; else if (k === 'q') st.q = '';
      });
      var chips = $$('[data-act] button');
      (chips[Math.min(idx, chips.length - 1)] || $('[data-q]')).focus();
    }
    if (b.hasAttribute('data-more')) {
      var firstNew = shown; shown += PAGE; render(true);
      var vis = $$('article', grid).filter(function (a) { return !a.hidden; }), a = vis[firstNew] && vis[firstNew].querySelector('h3 a'); if (a) a.focus({ preventScroll: true });
    }
  });

  /* ---------- phone and tablet: the filters are a modal bottom sheet ---------- */
  var bd = $('[data-bd]'), opener = $('[data-open]'), mq = window.matchMedia('(max-width:980px)'), scrollY0 = 0, outside = [];
  function setOutsideInert(on) {
    if (on) {
      outside = [];
      var n = side; while (n && n !== document.body) {             /* everything except the sheet's own branch */
        Array.prototype.forEach.call(n.parentNode.children, function (sib) { if (sib !== n && sib !== bd && sib.tagName !== 'SCRIPT' && !sib.hasAttribute('inert')) { sib.setAttribute('inert', ''); outside.push(sib); } });
        n = n.parentNode;
      }
    } else { outside.forEach(function (el) { el.removeAttribute('inert'); }); outside = []; }
  }
  function sheet(on) {
    if (on === side.classList.contains('open')) return;
    side.classList.toggle('open', on); bd.classList.toggle('open', on); opener.setAttribute('aria-expanded', on);
    if (on) {
      side.setAttribute('role', 'dialog'); side.setAttribute('aria-modal', 'true'); side.setAttribute('aria-labelledby', 'ifl-sheet-title');
      scrollY0 = window.scrollY;                                   /* iOS-safe scroll lock */
      document.body.style.position = 'fixed'; document.body.style.top = -scrollY0 + 'px'; document.body.style.left = '0'; document.body.style.right = '0';
      setOutsideInert(true);
      var f = side.querySelector('input:not([disabled])'); if (f) f.focus();
    } else {
      side.setAttribute('role', 'complementary'); side.removeAttribute('aria-modal'); side.removeAttribute('aria-labelledby');
      setOutsideInert(false);
      document.body.style.position = document.body.style.top = document.body.style.left = document.body.style.right = '';
      window.scrollTo({ top: scrollY0, left: 0, behavior: 'instant' });   /* the site scrolls smoothly; restore in one jump */
      if (mq.matches) opener.focus();
    }
  }
  opener.addEventListener('click', function () { sheet(true); });
  bd.addEventListener('click', function () { sheet(false); });
  $$('[data-close]').forEach(function (b) { b.addEventListener('click', function () { sheet(false); }); });
  document.addEventListener('keydown', function (e) {
    if (!side.classList.contains('open')) return;
    if (e.key === 'Escape') { sheet(false); return; }
    if (e.key === 'Tab') {                                         /* keep focus inside the sheet */
      var f = $$('button:not([hidden]), input:not([disabled]), select, summary, a[href]', side).filter(function (el) { return el.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
  (mq.addEventListener ? mq.addEventListener.bind(mq, 'change') : mq.addListener.bind(mq))(function () { if (!mq.matches) sheet(false); });

  /* ---------- links in the "Start here" panel and on post pages (#cat=…), and the back button ---------- */
  function fromHash(scroll) {
    var r = readHash(); st = r.s; shown = PAGE; render(!r.legacy);
    if (r.legacy && scroll) setTimeout(function () { root.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 0);
  }
  window.addEventListener('hashchange', function () { if (!/^#goal-/.test(location.hash)) fromHash(true); });
  document.addEventListener('click', function (e) {               /* same #cat= link clicked twice: no hashchange, so apply it here */
    var a = e.target.closest ? e.target.closest('a[href^="#cat="]') : null;
    if (a && a.getAttribute('href') === location.hash) { e.preventDefault(); fromHash(true); }
  });
  fromHash(true);
  root.classList.add('ready');
})();
