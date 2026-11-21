/* Warehouse Layout Lab V1: drawing, controls and numbers for assets/sim/layout-lab.html (warehouse layout series,
   Part 1). Needs WLEngine (wl-engine.js) and, for the 3D view, three.js r128 with OrbitControls.
   Each layout runs twice with the same seed: once straight through for the table and the heat map (the full shift),
   and once live, replayed faster than life, for the animation. The figure plays and loops on its own; the reader picks
   what to look at (side by side or one layout, 2D or 3D). In side-by-side mode it switches between 2D and 3D every
   30 seconds until the reader picks a view, and starts again after a minute without clicks. */
(function () {
  'use strict';
  var E = window.WLEngine; if (!E) return;
  var BX = E.BX, BZ = E.BZ;
  // which layouts to show: Part 1 compares as-is with the redesign (p1), Part 2 the three flow patterns (p2).
  // Chosen with s=p2 in the address (#embed&s=p2 inside an article) or window.WL_SCENE in the self-contained preview.
  var SCN = window.WL_SCENE || ((location.hash + location.search).match(/[#&?]s=(p\d)/) || [])[1] || 'p1';
  var SETS = { p1: { kinds: ['asis', 'redesign'], tone: { asis: 'bad', redesign: 'good' } }, p2: { kinds: ['redesign', 'thru', 'lshape'], tone: {} } };
  if (!SETS[SCN]) SCN = 'p1';
  var KINDS = SETS[SCN].kinds, P2 = SCN === 'p2';
  var LAYS = {}; KINDS.forEach(function (k) { LAYS[k] = E.makeLayout(k); });
  function nameOf(k) { return P2 ? LAYS[k].short : LAYS[k].name; }
  var EMBED = /embed/.test(location.hash) || (window.parent !== window && location.href === 'about:srcdoc');   // srcdoc: the self-contained preview
  if (EMBED) document.documentElement.classList.add('embed');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (id) { return document.getElementById(id); };
  var stage = $('stage'), busy = $('busy');
  var S = { v: 'both', d: '2d', heat: true, faults: true, orders: 300, share: 0.8, tour: !reduce, idleAt: 0 };
  var SPEED = 12;                                  // simulated seconds per real second
  // truck yards: each dock wall has its own frame (u along the wall, w out from it), so the yard, the lane and the
  // truck manoeuvres are the same on the south (S), west (W) and east (E) walls
  var YD = 31, LANE_W = 18;
  var WF = { S: { o: [0, BZ], U: [1, 0], W: [0, 1], th: 0, len: BX }, E: { o: [BX, BZ], U: [0, -1], W: [1, 0], th: -Math.PI / 2, len: BZ }, W: { o: [0, 0], U: [0, 1], W: [-1, 0], th: Math.PI / 2, len: BZ } };
  function toW(f, u, w) { return [f.o[0] + u * f.U[0] + w * f.W[0], f.o[1] + u * f.U[1] + w * f.W[1]]; }
  function doorU(q) { return q.wall === 'S' ? q.x + 0.5 : q.wall === 'W' ? q.z + 0.5 : BZ - (q.z + 0.5); }
  var WALLS = {}; KINDS.forEach(function (k) { LAYS[k].doors.forEach(function (d) { WALLS[d.wall] = 1; }); });
  var WX0 = WALLS.W ? -YD : -1.5, WX1 = WALLS.E ? BX + YD : BX + 1.5, WZ0 = -1.5, WZ1 = WALLS.S ? BZ + YD : BZ + 1.5;   // plan extents: building and yards
  var LANE = BZ + LANE_W;                                        // lane in the truck frame (the south-wall frame)
  var COL = { A: '#8DC63F', B: '#3FA7F5', C: '#7F93B2' };
  var H = {}, LIVE = {}, PANE = {}, TV = {}, TLAST = {};
  function fmt(n, d) { return Number(n).toLocaleString('en-CA', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function money(n) { return '$' + fmt(Math.round(n / 1000) * 1000); }
  function clock(t) { var m = Math.floor(t / 60) + 7 * 60; return ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2); }

  /* ---------- panes, view buttons and lists, built for the chosen layouts ---------- */
  stage.querySelectorAll('.pane').forEach(function (e) { e.remove(); });
  stage.insertAdjacentHTML('afterbegin', KINDS.map(function (k) {
    return '<div class="pane ' + (SETS[SCN].tone[k] || 'neu') + '" data-k="' + k + '"><div class="tag"><b>' + nameOf(k) + '</b><em class="clk">07:00</em></div><canvas class="c2"></canvas><canvas class="gl" hidden></canvas><div class="ov"></div></div>';
  }).join(''));
  stage.classList.add('n' + KINDS.length);
  var vg = document.querySelector('[data-v]').parentNode;
  vg.querySelectorAll('[data-v]').forEach(function (b) { b.remove(); });
  vg.insertAdjacentHTML('beforeend', '<button class="chip" data-v="both" aria-pressed="true">' + (KINDS.length > 2 ? 'All three' : 'Side by side') + '</button>' +
    KINDS.map(function (k) { return '<button class="chip" data-v="' + k + '" aria-pressed="false">' + (P2 ? LAYS[k].short : k === 'asis' ? 'As-is' : 'Redesigned') + '</button>'; }).join(''));
  var fc0 = document.querySelector('.card.faults');
  fc0.classList.add('n' + KINDS.length);                        // column count set in CSS, so phones still stack
  fc0.innerHTML = KINDS.map(function (k) {
    var t = P2 ? LAYS[k].short + ': what to notice' : k === 'asis' ? 'What is wrong with the as-is layout' : 'What the redesign changes';
    return '<div class="' + (SETS[SCN].tone[k] || 'neu') + '"><h3>' + t + '</h3><ol id="f-' + k + '"></ol></div>';
  }).join('');
  if (P2 && !EMBED) {
    document.querySelector('header .eyebrow').textContent = 'Warehouse layout series · Part 2';
    document.querySelector('header h1').textContent = 'Warehouse Layout Lab: U-shape, straight-through or L-shape?';
    document.querySelector('header .lede').textContent = 'The same Vancouver distributor, racks, orders and trucks in three flow patterns. Only where the docks sit, and so where packing and the fast movers go, changes.';
  }
  if (P2) {                                                      // the model box and legend in Part 2 wording
    var li = document.querySelectorAll('details li');
    if (li[0]) li[0].textContent = 'All three layouts hold the same pallet racks (about 840 pallet positions a level, 780 SKUs) in the same 72 × 52 m building, with three receiving and two shipping doors each. Only the walls the doors are on, and so where staging, packing and the fast movers go, differ.';
    document.querySelectorAll('.legend span').forEach(function (sp) { if (/same scale/.test(sp.textContent)) sp.lastChild.textContent = 'Travel (same scale for all)'; });
  }
  KINDS.forEach(function (k) {
    var el = stage.querySelector('.pane[data-k="' + k + '"]');
    el.querySelectorAll('canvas').forEach(function (c) { c.setAttribute('role', 'img'); c.setAttribute('aria-label', nameOf(k) + ', animated plan of pickers, forklifts and trucks during the shift. The numbered points and the table below give the same information.'); });
    PANE[k] = { k: k, el: el, c2: el.querySelector('.c2'), gl: el.querySelector('.gl'), ov: el.querySelector('.ov'), clk: el.querySelector('.clk'), W: 0, H: 0, dpr: 1, stat: null, badges: [], lbls: [] };
  });

  /* ---------- simulation runs ---------- */
  function runAll(cb) {
    busy.hidden = false;
    setTimeout(function () {
      KINDS.forEach(function (k) {
        var sim = E.Sim(k, { orders: S.orders, share: S.share }), r = sim.run();
        var hot = [], c, w = sim.heatWait;
        for (c = 0; c < w.length; c++) if (w[c] > 0) hot.push({ c: c, w: w[c] });
        hot.sort(function (a, b) { return b.w - a.w; });
        var keep = [];                                   // strongest give-way spots, at least 3 m apart
        hot.forEach(function (h) {
          if (keep.length >= 14 || h.w < 6) return;
          var x = h.c % BX + 0.5, z = Math.floor(h.c / BX) + 0.5;
          if (keep.every(function (q) { return Math.abs(q.x - x) + Math.abs(q.z - z) > 3; })) keep.push({ x: x, z: z, w: h.w });
        });
        var hv = Array.prototype.slice.call(sim.heat).filter(function (v) { return v > 0; }).sort(function (a, b) { return a - b; });
        H[k] = { sim: sim, r: r, hot: keep, p95: hv.length ? hv[Math.floor(hv.length * 0.96)] : 1 };
        LIVE[k] = E.Sim(k, { orders: S.orders, share: S.share }); while (LIVE[k].t < JUMP) LIVE[k].tick(E.P.dt);
        TV[k] = {};
        PANE[k].stat = null;
      });
      var shared = Math.max.apply(null, KINDS.map(function (k) { return H[k].p95; })); KINDS.forEach(function (k) { H[k].p95 = shared; });   // one heat scale for every floor, set by the busiest one's 96th percentile
      busy.hidden = true;
      build3d(); if (!GL) noGL();
      numbers(); faults();
      if (cb) cb();
    }, 30);
  }
  var JUMP = +((location.search.match(/jump=(\d+)/) || [])[1] || 0);   // test hook: start the replay later in the shift
  if (reduce && !JUMP) JUMP = 12600;                              // reduced motion: show the floor at 10:30, still
  function restartLive() { KINDS.forEach(function (k) { LIVE[k] = E.Sim(k, { orders: S.orders, share: S.share }); TV[k] = {}; }); }

  /* ---------- numbers ---------- */
  function numbersN() {                                          // three or more layouts: best value in each row marked
    var R = KINDS.map(function (k) { return H[k].r; });
    var rows = [
      ['Walk per order', 'walkOrder', ' m', 0, -1], ['Lines per picker-hour', 'lph', '', 0, 1], ['Picker-hours a day', 'pickHoursDay', '', 1, -1],
      ['Give-way stops in the shift', 'waits', '', 0, -1], ['Forklift time per pallet put away', 'forkCycle', ' min', 1, -1], ['Dock-to-stock time (average)', 'dts', ' min', 0, -1],
      ['Inbound truck time on site*', 'truckIn', ' min', 0, -1], ['Inbound pallets not put away by 15:00', 'notAway', '', 0, -1], ['Picking labour a year', 'pickCostYear', '$', 0, -1]
    ];
    $('kpi').querySelector('thead').innerHTML = '<tr><th>Measure</th>' + KINDS.map(function (k) { return '<th>' + LAYS[k].short + '</th>'; }).join('') + '</tr>';
    $('kpi').querySelector('tbody').innerHTML = rows.map(function (q) {
      var vals = R.map(function (r) { return r[q[1]]; }), best = q[4] < 0 ? Math.min.apply(null, vals) : Math.max.apply(null, vals);
      var fv = function (z) { return q[2] === '$' ? money(z) : fmt(z, q[3]) + q[2]; };
      var allSame = vals.every(function (v) { return fv(v) === fv(vals[0]); });
      return '<tr><td>' + q[0] + '</td>' + vals.map(function (v) { return '<td class="' + (!allSame && fv(v) === fv(best) ? 'good' : '') + '">' + fv(v) + '</td>'; }).join('') + '</tr>';
    }).join('');
    var mx = Math.max.apply(null, R.map(function (r) { return r.busy; })), sp = '';
    KINDS.forEach(function (k, i) {
      var r = R[i], s2 = r.split, w = function (v) { return (v / mx * 100).toFixed(2) + '%'; };
      sp += '<span>' + LAYS[k].short + '</span><span class="t"><i style="width:' + w(s2.walk) + ';background:#0B6FA4"></i><i style="width:' + w(s2.pick) + ';background:#8DC63F"></i><i style="width:' + w(s2.other) + ';background:#9AA8BA"></i><i style="width:' + w(s2.wait) + ';background:#E2574C"></i></span><span class="v">' + fmt(r.busy, 1) + ' h</span>';
    });
    $('split').innerHTML = '<span></span><span style="font-size:12px;color:#5A6475">Picker-hours a day, by activity</span><span></span>' + sp;
    var hs = R.map(function (r) { return r.pickHoursDay; }), spread = (Math.max.apply(null, hs) - Math.min.apply(null, hs)) / Math.min.apply(null, hs);
    $('say').textContent = 'At ' + fmt(S.orders) + ' orders a day: ' + KINDS.map(function (k, i) { return LAYS[k].short + ' ' + fmt(R[i].walkOrder) + ' m an order and ' + fmt(R[i].pickHoursDay, 1) + ' picker-hours'; }).join('; ') + '. ' +
      (spread < 0.03 ? 'Picking is within ' + fmt(spread * 100) + '% across the three; the difference is in put-away: the forklift needs ' : 'The forklift needs ') +
      KINDS.map(function (k, i) { return fmt(R[i].forkCycle, 2); }).join(', ') + ' minutes a pallet, depending on how far the receiving doors are from the fast movers.';
    $('wl-orders-o').textContent = fmt(S.orders); $('wl-share-o').textContent = Math.round(S.share * 100) + '%';
    var trucks = H[KINDS[0]].sim.trucks.filter(function (t) { return t.dir === 'in'; }).length;
    $('wl-crew').textContent = R[0].pickers + ' pickers, ' + R[0].forklifts + ' forklift' + (R[0].forklifts > 1 ? 's' : '') + ', ' + trucks + ' inbound trucks a day';
    report();
  }
  function numbers() {
    if (KINDS.length !== 2 || KINDS[0] !== 'asis') return numbersN();
    var a = H.asis.r, b = H.redesign.r;
    function pct(x, y) { return (y - x) / x; }
    var rows = [
      ['Walk per order', a.walkOrder, b.walkOrder, ' m', 0, 'pct'],
      ['Lines per picker-hour', a.lph, b.lph, '', 0, 'pct+'],
      ['Picker-hours a day', a.pickHoursDay, b.pickHoursDay, '', 1, 'pct'],
      ['Give-way stops in the shift', a.waits, b.waits, '', 0, 'pct'],
      ['Inbound truck time on site*', a.truckIn, b.truckIn, ' min', 0, 'pct'],
      ['Inbound trucks still on site at 15:00', a.trucksOnSite, b.trucksOnSite, '', 0, 'diff'],
      ['Inbound pallets not put away by 15:00', a.notAway, b.notAway, '', 0, 'diff'],
      ['Picking labour a year', a.pickCostYear, b.pickCostYear, '', 0, 'money'],
      ['Truck detention a year*', a.detYear, b.detYear, '', 0, 'money']
    ];
    var h = '';
    rows.forEach(function (q) {
      var x = q[1], y = q[2], ch = '', cls = '';
      if (q[5] === 'money') { var d = y - x; ch = d === 0 ? '–' : (d < 0 ? '−' : '+') + money(Math.abs(d)); cls = d < 0 ? 'good' : d > 0 ? 'bad' : ''; }
      else if (q[5] === 'diff') { var dd = y - x; ch = dd === 0 ? '–' : (dd < 0 ? '−' : '+') + fmt(Math.abs(dd)); cls = dd < 0 ? 'good' : dd > 0 ? 'bad' : ''; }
      else { var p = x ? pct(x, y) : 0, up = q[5] === 'pct+'; ch = Math.abs(p) < 0.005 ? '–' : (p < 0 ? '−' : '+') + fmt(Math.abs(p) * 100) + '%'; cls = Math.abs(p) < 0.005 ? '' : (p > 0) === up ? 'good' : 'bad'; }
      var v = function (z) { return q[5] === 'money' ? money(z) : fmt(z, q[4]) + q[3]; };
      h += '<tr><td>' + q[0] + '</td><td>' + v(x) + '</td><td>' + v(y) + '</td><td class="' + cls + '">' + ch + '</td></tr>';
    });
    $('kpi').querySelector('tbody').innerHTML = h;
    var mx = Math.max(a.busy, b.busy), sp = '';
    [['As-is', a], ['Redesigned', b]].forEach(function (q) {
      var s = q[1].split, w = function (v) { return (v / mx * 100).toFixed(2) + '%'; };
      sp += '<span>' + q[0] + '</span><span class="t"><i style="width:' + w(s.walk) + ';background:#0B6FA4"></i><i style="width:' + w(s.pick) + ';background:#8DC63F"></i><i style="width:' + w(s.other) + ';background:#9AA8BA"></i><i style="width:' + w(s.wait) + ';background:#E2574C"></i></span><span class="v">' + fmt(q[1].busy, 1) + ' h</span>';
    });
    $('split').innerHTML = '<span></span><span style="font-size:12px;color:#5A6475">Picker-hours a day, by activity</span><span></span>' + sp;
    var save = a.pickCostYear - b.pickCostYear + a.detYear - b.detYear;
    $('say').textContent = 'At ' + fmt(S.orders) + ' orders a day the redesigned floor walks ' + fmt(b.walkOrder) + ' m an order instead of ' + fmt(a.walkOrder) +
      ' m and needs ' + fmt(b.pickHoursDay, 1) + ' picker-hours instead of ' + fmt(a.pickHoursDay, 1) + '. Trucks spend ' + fmt(b.truckIn) + ' minutes on site instead of ' + fmt(a.truckIn) +
      (save > 0 ? '. Together that is at least ' + money(save) + ' a year in picking labour and detention, from the same building and about the same racks.' : '.');
    $('wl-orders-o').textContent = fmt(S.orders);
    $('wl-share-o').textContent = Math.round(S.share * 100) + '%';
    var trucks = H.asis.sim.trucks.filter(function (t) { return t.dir === 'in'; }).length;
    $('wl-crew').textContent = a.pickers + ' pickers, ' + a.forklifts + ' forklift' + (a.forklifts > 1 ? 's' : '') + ', ' + trucks + ' inbound trucks a day';
    report();
  }

  /* ---------- fault lists and badges ---------- */
  function faults() {
    KINDS.forEach(function (k) {
      var L = H[k].sim.L, ol = $('f-' + k), p = PANE[k];
      var FL = P2 ? L.flow : L.faults;
      ol.innerHTML = FL.map(function (f) { return '<li><button type="button" data-k="' + k + '" data-n="' + f.n + '" aria-pressed="false"><span>' + f.n + '</span><span style="all:unset"><strong>' + f.t + '</strong>' + f.d + '</span></button></li>'; }).join('');
      p.ov.innerHTML = '';
      p.badges = FL.map(function (f) {
        var b = document.createElement('div'); b.className = 'badge'; b.textContent = f.n; b.setAttribute('role', 'button'); b.tabIndex = 0; b.setAttribute('aria-label', nameOf(k) + ', ' + f.n + '. ' + f.t + ': ' + f.d);
        b.addEventListener('mouseenter', function () { tip(k, f, b); }); b.addEventListener('mouseleave', untip);
        b.addEventListener('focus', function () { tip(k, f, b); }); b.addEventListener('blur', untip);
        b.addEventListener('click', function () { tip(k, f, b); });
        p.ov.appendChild(b); return { el: b, f: f };
      });
      p.lbls = L.areas.map(function (a) { var e = document.createElement('div'); e.className = 'lbl k-' + a.k; e.textContent = a.t; p.ov.appendChild(e); return { el: e, a: a }; });
    });
    document.querySelectorAll('.faults button').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-k'), n = +b.getAttribute('data-n');
        document.querySelectorAll('.faults button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        if (S.v !== 'both' && S.v !== k) setView(k);
        var q = PANE[k].badges[n - 1]; if (!q) return;
        stage.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });   // the plan is above the list
        q.el.classList.remove('hot'); void q.el.offsetWidth; q.el.classList.add('hot');
        clearTimeout(tip.t); setTimeout(function () { tip(k, q.f, q.el); }, reduce ? 0 : 450); tip.t = setTimeout(untip, 6000);
        hold();
      });
    });
  }
  var tipEl = null;
  function tip(k, f, b) {
    untip(); tipEl = document.createElement('div'); tipEl.className = 'tip';
    tipEl.innerHTML = '<b>' + f.n + '. ' + f.t + '</b>' + f.d;
    var p = PANE[k].el; p.appendChild(tipEl);
    var r = b.getBoundingClientRect(), pr = p.getBoundingClientRect(), x = r.left - pr.left + 16, y = r.top - pr.top + 14;
    if (x + 250 > pr.width) x = Math.max(6, r.left - pr.left - 250); if (y + 90 > pr.height) y = Math.max(6, y - 100);
    tipEl.style.left = x + 'px'; tipEl.style.top = y + 'px';
  }
  function untip() { if (tipEl) { tipEl.remove(); tipEl = null; } }

  /* ---------- 2D plan ---------- */
  function sizePanes() {
    KINDS.forEach(function (k) {
      var p = PANE[k], r = p.el.getBoundingClientRect(), d = Math.min(2, window.devicePixelRatio || 1);
      if (!r.width) return;
      if (Math.abs(r.width - p.W) > 0.5 || Math.abs(r.height - p.H) > 0.5 || d !== p.dpr) {
        p.W = r.width; p.H = r.height; p.dpr = d; p.el.classList.toggle('small', p.W < 520); /* small panes: area labels off, badges only */ p.c2.width = Math.round(p.W * d); p.c2.height = Math.round(p.H * d); p.stat = null;
        if (p.R) { p.R.setPixelRatio(d); p.R.setSize(p.W, p.H, false); p.cam.aspect = p.W / p.H; p.cam.fov = 34; p.cam.updateProjectionMatrix(); frame3d(p); }
      }
    });
  }
  function ext(p) {                                              // plan extents: all layouts' yards side by side (same scale), its own yards alone
    if (!P2 || S.v === 'both') return [WX0, WX1, WZ0, WZ1];
    var w = {}; LAYS[p.k].doors.forEach(function (d) { w[d.wall] = 1; });
    return [w.W ? -YD : -1.5, w.E ? BX + YD : BX + 1.5, -1.5, w.S ? BZ + YD : BZ + 1.5];
  }
  function view(p) {                                         // world metres -> canvas pixels
    var e = ext(p), W = p.W, Hh = p.H - 8, s = Math.min(W / (e[1] - e[0]), Hh / (e[3] - e[2]));
    return { s: s, ox: (W - s * (e[1] - e[0])) / 2 - s * e[0], oz: 34 + (Hh - 34 - s * (e[3] - e[2])) / 2 - s * e[2] + 0 };
  }
  function fitView(p) { var e = ext(p), v = view(p); if (v.oz + v.s * e[2] < 36) { var s = Math.min(p.W / (e[1] - e[0]), (p.H - 46) / (e[3] - e[2])); v = { s: s, ox: (p.W - s * (e[1] - e[0])) / 2 - s * e[0], oz: 38 - s * e[2] }; } return v; }
  function heatColor(v) {                                    // 0..1 -> rgba, dark orange to pale yellow
    v = Math.min(1, v); var r = 255, g = Math.round(70 + 170 * v), b = Math.round(20 + 120 * v * v), a = 0.1 + 0.55 * Math.sqrt(v);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + a.toFixed(3) + ')';
  }
  function drawStatic(k) {
    var p = PANE[k], h = H[k], L = h.sim.L, V = h.sim.V, d = p.dpr, v = fitView(p);
    var cv = document.createElement('canvas'); cv.width = p.c2.width; cv.height = p.c2.height;
    var g = cv.getContext('2d'); g.scale(d, d);
    var X = function (x) { return v.ox + x * v.s; }, Z = function (z) { return v.oz + z * v.s; }, s = v.s;
    // a truck yard on each wall that has doors: paving, the one-way lane and its direction
    var walls = {}; L.doors.forEach(function (q) { walls[q.wall] = 1; });
    Object.keys(walls).forEach(function (wk) {
      var f = WF[wk], a = toW(f, -1.5, 0), b = toW(f, f.len + 1.5, YD);
      g.fillStyle = 'rgba(255,255,255,0.045)'; g.fillRect(X(Math.min(a[0], b[0])), Z(Math.min(a[1], b[1])), Math.abs(b[0] - a[0]) * s, Math.abs(b[1] - a[1]) * s);
      g.strokeStyle = 'rgba(255,255,255,0.28)'; g.setLineDash([6, 6]); g.lineWidth = 1;
      [LANE_W - 2.6, LANE_W + 2.6].forEach(function (ww) { var p1 = toW(f, -1.5, ww), p2 = toW(f, f.len + 1.5, ww); g.beginPath(); g.moveTo(X(p1[0]), Z(p1[1])); g.lineTo(X(p2[0]), Z(p2[1])); g.stroke(); }); g.setLineDash([]);
      g.fillStyle = 'rgba(220,230,245,0.55)'; g.font = '600 ' + Math.max(9, s * 1.5) + 'px "Space Grotesk",system-ui';
      [[-1, 'left', 'Trucks in ▸'], [f.len + 1, 'right', 'Trucks out ▸']].forEach(function (q) { var pt = toW(f, q[0], LANE_W + 5); g.save(); g.translate(X(pt[0]), Z(pt[1])); g.rotate(f.th); g.textAlign = q[1]; g.fillText(q[2], 0, 0); g.restore(); });
    });
    // floor
    g.fillStyle = '#123866'; g.fillRect(X(0), Z(0), BX * s, BZ * s);
    // heat map (whole shift)
    if (S.heat) {
      var heat = h.sim.heat, p95 = h.p95, c;
      for (c = 0; c < heat.length; c++) { if (heat[c] <= 0) continue; var hv = heat[c] / p95; if (hv < 0.02) continue; g.fillStyle = heatColor(hv); g.fillRect(X(c % BX), Z(Math.floor(c / BX)), s + 0.5, s + 0.5); }
    }
    // staging spots
    g.strokeStyle = 'rgba(242,201,76,0.55)'; g.lineWidth = 1; g.setLineDash([3, 2]);
    var spots = L.recv === L.ship ? L.recv : L.recv.concat(L.ship);
    spots.forEach(function (q) { g.strokeRect(X(q.x + 0.1), Z(q.z + 0.1), s * 0.8, s * 0.8); });
    g.setLineDash([]);
    // racks and pick faces
    L.racks.forEach(function (r) {
      g.fillStyle = '#28466F'; g.fillRect(X(r.x0), Z(r.z0), (r.x1 - r.x0 + 1) * s, (r.z1 - r.z0 + 1) * s);
      g.strokeStyle = '#5577A6'; g.lineWidth = 1; g.strokeRect(X(r.x0) + 0.5, Z(r.z0) + 0.5, (r.x1 - r.x0 + 1) * s - 1, (r.z1 - r.z0 + 1) * s - 1);
      g.strokeStyle = 'rgba(85,119,166,0.6)'; g.beginPath();
      if (r.dir === 'x') { for (var i = r.x0 + 3; i <= r.x1; i += 3) { g.moveTo(X(i), Z(r.z0)); g.lineTo(X(i), Z(r.z1 + 1)); } }
      else { for (var j = r.z0 + 3; j <= r.z1; j += 3) { g.moveTo(X(r.x0), Z(j)); g.lineTo(X(r.x1 + 1), Z(j)); } }
      g.stroke();
    });
    h.sim.faces.forEach(function (f) {
      if (f.sku < 0) return; g.fillStyle = COL[V.cls[f.sku]];
      var fx = f.c % BX, fz = Math.floor(f.c / BX), t = Math.max(1.5, s * 0.28);
      if (Math.abs(fz + 0.5 - f.rz) > 0.1) { var zz = fz + 0.5 < f.rz ? Z(fz + 1) - 0 : Z(fz) - t; g.fillRect(X(fx) + s * 0.12, zz, s * 0.76, t); }
      else { var xx = fx + 0.5 < f.rx ? X(fx + 1) : X(fx) - t; g.fillRect(xx, Z(fz) + s * 0.12, t, s * 0.76); }
    });
    // overflow pallets in the main aisle
    if (L.spill.length) {
      L.spill.forEach(function (c, i) { if (i % 2) return; var x = c % BX, z = Math.floor(c / BX); g.fillStyle = '#9C7A4E'; g.fillRect(X(x + 0.12), Z(z + 0.12), s * 0.76, s * 1.76); });
      g.strokeStyle = '#FF5A4E'; g.lineWidth = 1.5; g.setLineDash([4, 3]);
      var sx = L.spill.map(function (c) { return c % BX; }), sz = L.spill.map(function (c) { return Math.floor(c / BX); });
      g.strokeRect(X(Math.min.apply(null, sx)) - 2, Z(Math.min.apply(null, sz)) - 2, (Math.max.apply(null, sx) - Math.min.apply(null, sx) + 1) * s + 4, (Math.max.apply(null, sz) - Math.min.apply(null, sz) + 1) * s + 4);
      g.setLineDash([]);
    }
    // pack benches (blocked cells near the drops)
    var pb = L.bench, vert = pb[3] - pb[1] > pb[2] - pb[0];
    g.fillStyle = '#A7B6CC'; g.fillRect(X(pb[0]), Z(pb[1]), (pb[2] - pb[0] + 1) * s, (pb[3] - pb[1] + 1) * s);
    g.fillStyle = '#6F86A8';
    if (vert) for (var bz = pb[1] + 1; bz < pb[3]; bz += 3) g.fillRect(X(pb[0]) + 2, Z(bz), s * 2 - 4, s * 1.4);
    else for (var b = pb[0] + 1; b < pb[2]; b += 3) g.fillRect(X(b), Z(pb[1]) + 2, s * 1.4, s * 2 - 4);
    // walls with door openings
    g.strokeStyle = '#9DB2D2'; g.lineWidth = 2.5;
    wallRuns(L).forEach(function (r) { g.beginPath(); g.moveTo(X(r[0]), Z(r[1])); g.lineTo(X(r[2]), Z(r[3])); g.stroke(); });
    L.doors.forEach(function (q) {
      var col = q.use === 'in' ? '#3FA7F5' : q.use === 'out' ? '#8DC63F' : '#C9A2FF', f = WF[q.wall], u = doorU(q), a = toW(f, u - 1.5, 0), b = toW(f, u + 1.5, 0);
      g.strokeStyle = col; g.lineWidth = 4; g.beginPath(); g.moveTo(X(a[0]), Z(a[1])); g.lineTo(X(b[0]), Z(b[1])); g.stroke();
      var tp = toW(f, u, 2.6); g.fillStyle = col; g.font = '600 ' + Math.max(8, s * 1.15) + 'px "Space Grotesk",system-ui'; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.fillText(q.use === 'in' ? 'IN' : q.use === 'out' ? 'OUT' : 'IN/OUT', X(tp[0]), Z(tp[1])); g.textBaseline = 'alphabetic';   // in the yard, clear of the staging labels
    });
    p.stat = cv; p.view = v;
  }
  function wallRuns(L) {                                         // the four walls as segments, with a 3 m gap at each door
    var out = [], ends = { N: [[0, 0], [BX, 0]], S: [[0, BZ], [BX, BZ]], W: [[0, 0], [0, BZ]], E: [[BX, 0], [BX, BZ]] };
    Object.keys(ends).forEach(function (wk) {
      var a = ends[wk][0], b = ends[wk][1], horiz = a[1] === b[1], len = horiz ? BX : BZ, cuts = [];
      L.doors.forEach(function (q) { if (q.wall === wk) { var c = horiz ? q.x + 0.5 : q.z + 0.5; cuts.push([c - 1.5, c + 1.5]); } });
      cuts.sort(function (p, q) { return p[0] - q[0]; });
      var t0 = 0; cuts.concat([[len, len]]).forEach(function (c) { if (c[0] > t0) out.push(horiz ? [t0, a[1], c[0], a[1]] : [a[0], t0, a[0], c[0]]); t0 = c[1]; });
    });
    return out;
  }
  function rectAt(g, X, Z, s, cx, cz, th, u0, u1, w, col) {     // a box along heading th, from u0 to u1 metres
    g.save(); g.translate(X(cx), Z(cz)); g.rotate(th); g.fillStyle = col; g.fillRect(u0 * s, -w / 2 * s, (u1 - u0) * s, w * s); g.restore();
  }
  function truckShape(g, X, Z, s, t) {
    var A = t.A, R = t.R;
    [-0.65, 0.65].forEach(function (u) { rectAt(g, X, Z, s, A[0] + u * Math.cos(t.th2), A[1] + u * Math.sin(t.th2), t.th2, -0.45, 0.45, TW + 0.5, '#1A2230'); });
    rectAt(g, X, Z, s, A[0], A[1], t.th2, -LTA, LT - LTA, TW, '#E9EEF5');                      // trailer
    rectAt(g, X, Z, s, R[0], R[1], t.th1, -0.45, 0.45, TW + 0.5, '#1A2230');                              // drive axle
    rectAt(g, X, Z, s, R[0] + 2.4 * Math.cos(t.th1), R[1] + 2.4 * Math.sin(t.th1), t.th1, -0.4, 0.4, TW + 0.4, '#1A2230');
    rectAt(g, X, Z, s, R[0], R[1], t.th1, -RA, LC - RA, TW * 0.94, t.dir === 'in' ? '#3FA7F5' : '#8DC63F');   // tractor
    rectAt(g, X, Z, s, R[0], R[1], t.th1, LC - RA - 0.5, LC - RA - 0.25, TW * 0.8, '#26324A');           // windscreen
  }
  function draw2d(k) {
    var p = PANE[k], g = p.c2.getContext('2d'), sim = LIVE[k], L = sim.L, d = p.dpr;
    if (!p.stat) drawStatic(k);
    var v = p.view, s = v.s, X = function (x) { return v.ox + x * s; }, Z = function (z) { return v.oz + z * s; };
    g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, p.c2.width, p.c2.height); g.drawImage(p.stat, 0, 0); g.setTransform(d, 0, 0, d, 0, 0);
    // give-way hot spots over the whole shift
    var ph = (performance.now() / 900) % 1;
    H[k].hot.forEach(function (q, i) {
      var f = reduce ? 0.3 : (ph + i * 0.13) % 1, r = (0.9 + Math.sqrt(q.w) / 6) * s, a = 0.85 - 0.45 * f;
      g.strokeStyle = 'rgba(255,176,46,' + a.toFixed(2) + ')'; g.lineWidth = 2; g.setLineDash([4, 3]); g.beginPath(); g.arc(X(q.x), Z(q.z), r * (1 + 0.25 * f), 0, 7); g.stroke(); g.setLineDash([]);
    });
    // staged pallets
    var spots = L.recv === L.ship ? L.recv : L.recv.concat(L.ship);
    spots.forEach(function (q) {
      if (!q.busy) return; var out = q.busy !== 'res' && q.busy.dir === 'out';
      g.fillStyle = out ? '#E6DFC9' : '#C9955A'; g.fillRect(X(q.x + 0.15), Z(q.z + 0.15), s * 0.7, s * 0.7);
      if (out) { g.strokeStyle = '#8DC63F'; g.lineWidth = 1.2; g.strokeRect(X(q.x + 0.15), Z(q.z + 0.15), s * 0.7, s * 0.7); }
    });
    for (var o = 0; o < Math.min(3, sim.outQ); o++) { var pc = L.packSpot; g.fillStyle = '#E6DFC9'; g.fillRect(X(pc % BX + 0.1 + o * 1.0), Z(Math.floor(pc / BX) + 0.15), s * 0.8, s * 0.7); }
    // trucks
    trucks(k);
    for (var id in TV[k]) {                                       // each truck is drawn only on its own yard's paving
      var t = TV[k][id]; if (!t.show) continue;
      var f = WF[t.wall], a = toW(f, -1.5, 0), b = toW(f, f.len + 1.5, YD);
      g.save(); g.beginPath(); g.rect(X(Math.min(a[0], b[0])), Z(Math.min(a[1], b[1])), Math.abs(b[0] - a[0]) * s, Math.abs(b[1] - a[1]) * s); g.clip();
      truckShape(g, X, Z, s, wpose(t)); g.restore();
    }
    // agents
    sim.agents.forEach(function (a) {
      var x = X(a.x), z = Z(a.z);
      if (a.waitT > 0.4) { g.strokeStyle = '#FF5A4E'; g.lineWidth = 2; g.beginPath(); g.arc(x, z, s * 1.25, 0, 7); g.stroke(); }
      if (a.type === 'picker') {
        g.fillStyle = a.state === 'pick' ? '#FFE27A' : '#FFFFFF'; g.strokeStyle = '#0B6FA4'; g.lineWidth = 1.5;
        g.beginPath(); g.arc(x, z, Math.max(2.6, s * 0.55), 0, 7); g.fill(); g.stroke();
      } else {
        var len = a.type === 'fork' ? 2.3 : 1.7, wd = a.type === 'fork' ? 1.2 : 0.8, ang = Math.atan2(a.dirz, a.dirx);
        g.save(); g.translate(x, z); g.rotate(ang);
        g.fillStyle = a.type === 'fork' ? '#FF8A3D' : '#B18CFF'; g.fillRect(-len / 2 * s, -wd / 2 * s, len * s, wd * s);
        if (a.load || (a.type === 'jack' && a.state === 'carry')) { g.fillStyle = '#C9955A'; g.fillRect((len / 2 - 0.2) * s, -0.45 * s, 0.9 * s, 0.9 * s); }
        g.restore();
      }
    });
  }

  /* ---------- trucks: tractor and trailer, driven like real rigs ----------
     Each truck is a tractor (drive axle R, heading th1) pulling a trailer (axle A, heading th2) hitched at the drive
     axle. Driving forward, the tractor follows its path and the trailer follows the hitch (no sideways slip, so it cuts
     inside on turns). Backing, the trailer axle follows its path and the tractor follows the hitch.
     Arrival: in from the west along the lane with the door on the driver's (left) side, swing the nose to the right
     and straighten up at an angle, then back the trailer in: a short straight, one curve, then straight into the door,
     so the trailer is square before it passes the trucks at the next doors. Departure: pull straight out, turn left onto
     the lane and drive out to the east. A truck waits while another moving truck is in its way. */
  var LT = 9.0, LTA = 1.5, KP = 1.0, LC = 4.2, RA = 1.0, TW = 2.6, L2 = LT - KP - LTA;
  var SET = { PP: -2, RR: 8, AL: 0.6, LS: 9, RB: 8, TURN: BZ + 11, VF: 7, VB: 2.5 };
  var DOCK_A = BZ + LTA;                                          // trailer axle when the trailer is against the door
  function ang(a) { return Math.atan2(Math.sin(a), Math.cos(a)); }
  function hitchFromA(t) { t.R = [t.A[0] + L2 * Math.cos(t.th2), t.A[1] + L2 * Math.sin(t.th2)]; }
  function aFromHitch(t) { t.A = [t.R[0] - L2 * Math.cos(t.th2), t.R[1] - L2 * Math.sin(t.th2)]; }
  function docked(t, D) { t.th1 = t.th2 = Math.PI / 2; t.A = [D, DOCK_A]; hitchFromA(t); }
  function line(a, b) { var o = [], d = Math.hypot(b[0] - a[0], b[1] - a[1]), n = Math.max(1, Math.ceil(d / 0.25)); for (var i = 1; i <= n; i++) o.push([a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n]); return o; }
  function simForward(t0, pts) {                                 // where the trailer ends up after driving pts
    var R = t0.R.slice(), th1 = t0.th1, th2 = t0.th2;
    pts.forEach(function (q) { var dx = q[0] - R[0], dz = q[1] - R[1], ds = Math.hypot(dx, dz); if (ds < 1e-9) return; th1 = Math.atan2(dz, dx); th2 += ds / L2 * Math.sin(th1 - th2); R = q; });
    return { R: R, th1: th1, th2: th2, A: [R[0] - L2 * Math.cos(th2), R[1] - L2 * Math.sin(th2)] };
  }
  function backPath(A0, th2, D, rb) {                            // straight, one curve to the right, straight north into the door
    var p0 = th2 + Math.PI, p1 = 1.5 * Math.PI; while (p1 - p0 > Math.PI) p1 -= 2 * Math.PI; while (p1 - p0 < -Math.PI) p1 += 2 * Math.PI;
    var sg = p1 > p0 ? 1 : -1, dx = sg * rb * (Math.sin(p1) - Math.sin(p0)), ls = (D - A0[0] - dx) / Math.cos(p0);
    if (!(ls >= 0)) return null;
    var B = [A0[0] + ls * Math.cos(p0), A0[1] + ls * Math.sin(p0)], pts = line(A0, B);
    var cx = B[0] + sg * rb * Math.cos(p0 + Math.PI / 2), cz = B[1] + sg * rb * Math.sin(p0 + Math.PI / 2), n = Math.ceil(Math.abs(p1 - p0) * rb / 0.25);
    for (var i = 1; i <= n; i++) { var pp = p0 + (p1 - p0) * i / n; pts.push([cx - sg * rb * Math.cos(pp + Math.PI / 2), cz - sg * rb * Math.sin(pp + Math.PI / 2)]); }
    var E = pts[pts.length - 1]; if (E[1] < BZ + 13.5) return null;   // still curving next to the trucks at the other doors
    return pts.concat(line([D, E[1]], [D, DOCK_A]));
  }
  function planArrive(t, D) {
    var f = line(t.R, [D + SET.PP, LANE]), cx = D + SET.PP, cz = LANE + SET.RR, i, n = Math.ceil(SET.AL * SET.RR / 0.25);
    for (i = 1; i <= n; i++) { var a = SET.AL * i / n; f.push([cx + SET.RR * Math.sin(a), cz - SET.RR * Math.cos(a)]); }
    var E = f[f.length - 1]; f = f.concat(line(E, [E[0] + SET.LS * Math.cos(SET.AL), E[1] + SET.LS * Math.sin(SET.AL)]));
    var end = simForward(t, f), b = null;
    for (var rb = SET.RB; rb >= 5 && !b; rb -= 0.5) b = backPath(end.A, end.th2, D, rb);
    if (!b) return null;
    return [{ k: 'f', p: f }, { k: 'b', p: b }];
  }
  function planLeave(t) {
    var D = t.A[0], f = line(t.R, [D, SET.TURN]), r = LANE - SET.TURN, n = Math.ceil(Math.PI / 2 * r / 0.25), i;
    for (i = 1; i <= n; i++) { var a = Math.PI / 2 * i / n; f.push([D + r - r * Math.cos(a), SET.TURN + r * Math.sin(a)]); }
    return [{ k: 'f', p: f.concat(line(f[f.length - 1], [t.len + 30, LANE])) }];
  }
  function bodyPts(t) {                                           // points along both bodies, for keeping trucks apart
    var o = [], k;
    for (k = 0; k <= 4; k++) { var u = -LTA + (LT) * k / 4; o.push([t.A[0] + u * Math.cos(t.th2), t.A[1] + u * Math.sin(t.th2)]); }
    for (k = 0; k <= 2; k++) { var v = -RA + LC * k / 2; o.push([t.R[0] + v * Math.cos(t.th1), t.R[1] + v * Math.sin(t.th1)]); }
    return o;
  }
  function wpose(t) {                                             // the truck in world coordinates (it is driven in its wall's frame)
    var f = WF[t.wall], A = toW(f, t.A[0], t.A[1] - BZ), R = toW(f, t.R[0], t.R[1] - BZ);
    return { A: A, R: R, th1: t.th1 + f.th, th2: t.th2 + f.th, dir: t.dir };
  }
  function onYard(t) { return t.A[0] > -3 && t.A[0] < t.len + 3 && t.R[0] > -3 && t.R[0] < t.len + 3; }   // inside its own yard's paving
  function prio(t) { return t.segs.length && t.segs[0].k === 'b' ? 4 : t.st === 'leave' ? 3 : t.st === 'dock' ? 2 : 1; }   // backing > pulling out > arriving > queued
  function blockers(t0, tv) {                                     // the trucks in this truck's way (list of ids)
    var t = wpose(t0), seg = t0.segs[0], probe = [], k, out = [];
    if (seg.k === 'f') for (k = 1; k <= 4; k++) probe.push([t.R[0] + (LC - RA + k * 1.5) * Math.cos(t.th1), t.R[1] + (LC - RA + k * 1.5) * Math.sin(t.th1)]);
    else for (k = 1; k <= 3; k++) probe.push([t.A[0] - (LTA + k * 1.2) * Math.cos(t.th2), t.A[1] - (LTA + k * 1.2) * Math.sin(t.th2)]);
    for (var id in tv) {
      var o = tv[id]; if (o === t0 || !o.show || o.st === 'dock' && !o.segs.length) continue;       // parked at a door: paths keep clear
      if (o.wall !== t0.wall && !onYard(o)) continue;               // off the plan in another yard's lane
      var bp = bodyPts(wpose(o)), hit = false;
      for (var i = 0; i < probe.length && !hit; i++) for (var j = 0; j < bp.length; j++) if (Math.hypot(probe[i][0] - bp[j][0], probe[i][1] - bp[j][1]) < 2.4) { hit = true; break; }
      if (hit) out.push(id);
    }
    return out;
  }
  function advance(t, dist) {
    while (dist > 1e-6 && t.segs.length) {
      var seg = t.segs[0];
      if (t.pi >= seg.p.length) { t.segs.shift(); t.pi = 0; continue; }
      var q = seg.p[t.pi];
      if (seg.k === 'f') {
        var dx = q[0] - t.R[0], dz = q[1] - t.R[1], d = Math.hypot(dx, dz);
        if (d < 1e-9) { t.pi++; continue; }
        var st = Math.min(d, dist), nx = t.R[0] + dx / d * st, nz = t.R[1] + dz / d * st;
        t.th1 = Math.atan2(dz, dx); t.th2 += st / L2 * Math.sin(t.th1 - t.th2); t.R = [nx, nz]; aFromHitch(t);
        dist -= st; if (st >= d - 1e-9) t.pi++;
      } else {
        var ex = q[0] - t.A[0], ez = q[1] - t.A[1], e = Math.hypot(ex, ez);
        if (e < 1e-9) { t.pi++; continue; }
        var sb = Math.min(e, dist), R0 = t.R;
        t.A = [t.A[0] + ex / e * sb, t.A[1] + ez / e * sb]; t.th2 = Math.atan2(-ez, -ex); hitchFromA(t);
        var hx = t.R[0] - R0[0], hz = t.R[1] - R0[1];
        if (Math.hypot(hx, hz) > 1e-6) { var target = Math.atan2(-hz, -hx); t.th1 += ang(target - t.th1) * Math.min(1, sb / 1.2); }
        dist -= sb; if (sb >= e - 1e-9) t.pi++;
      }
    }
  }
  function trucks(k) {
    var sim = LIVE[k], tv = TV[k], now = performance.now();
    var fifo = {};                                                 // per lane: once a truck has to wait for its door, the trucks behind it wait too
    sim.trucks.forEach(function (tr) {
      if (tr.state === 'due') return;
      var t = tv[tr.id];
      if (!t) {
        if (tr.state === 'gone') return;
        var dr = tr.door || sim.L.doors.filter(function (q) { return q.use === 'both' || q.use === tr.dir; })[0];   // a queued truck waits in its doors' yard
        var u0 = -22; for (var oi in tv) { var o2 = tv[oi]; if (o2.wall === dr.wall && o2.st === 'road') u0 = Math.min(u0, o2.R[0] - 15); }   // behind the last truck on this lane, never on top of it
        t = tv[tr.id] = { id: tr.id, dir: tr.dir, wall: dr.wall, len: WF[dr.wall].len, th1: 0, th2: 0, R: [u0, LANE], A: null, segs: [], pi: 0, show: true, st: 'road', hold: 0 };
        aFromHitch(t);
        if (tr.state === 'dock' && sim.t - tr.docked > 60) { docked(t, doorU(tr.door)); t.st = 'dock'; t.D = doorU(tr.door); }
      }
      if (t.st === 'road' && (tr.state === 'yard' || t.segs.length) ) fifo[t.wall] = fifo[t.wall] || (tr.state === 'yard' || t.qx != null);   // a truck still queuing holds the trucks behind it
      if (tr.state === 'yard' && t.st === 'road') {                 // queue on the lane at the west end of the yard
        var slot = sim.yard.indexOf(tr), qx = 4 - slot * 15;
        if (t.qx !== qx) { t.qx = qx; t.segs = [{ k: 'f', p: line(t.R, [Math.max(t.R[0], qx), LANE]) }]; t.pi = 0; }
      } else if ((tr.state === 'dock' || tr.state === 'gone') && t.st === 'road' && !t.segs.length) {
        var D0 = doorU(tr.door), busy = false;                     // wait until the last truck at this door has pulled clear
        for (var ok in tv) { var o4 = tv[ok]; if (o4 !== t && o4.show && o4.wall === t.wall && o4.D === D0 && (o4.st === 'dock' || (o4.st === 'leave' && o4.R[1] < LANE - 1))) busy = true;
          if (o4 !== t && o4.show && o4.wall === t.wall && o4.st === 'leave' && o4.segs.length && Math.abs(o4.R[0] - D0) < 30) busy = true; }   // let a truck that is pulling out clear the lane first
        if (fifo[t.wall]) busy = true;
        if (busy) fifo[t.wall] = true;
        if (!busy) {
          var plan = planArrive(t, D0);
          if (plan) { t.segs = plan; t.pi = 0; } else docked(t, D0);
          t.st = 'dock'; t.D = D0;
        }
      } else if (tr.state === 'dock' && t.st === 'road' && t.segs.length && t.qx == null) {
        // still driving in from the edge with no queue: let the arrival plan take over once on the lane
      }
      if (tr.state === 'gone' && t.st === 'dock' && !t.segs.length) {   // pull out only when no moving truck is near this door
        var clear = true, me = wpose(t).R;
        for (var oj in tv) { var o3 = tv[oj]; if (o3 !== t && o3.show && o3.moving && onYard(o3)) { var r3 = wpose(o3).R; if (Math.hypot(r3[0] - me[0], r3[1] - me[1]) < 30) clear = false; } }
        if (clear) { t.segs = planLeave(t); t.pi = 0; t.st = 'leave'; }
      }
    });
    var dt = reduce ? 0 : Math.min(0.05, (now - (TLAST[k] || now)) / 1000); TLAST[k] = now;
    var B = {};
    for (var bid in tv) if (tv[bid].segs.length && tv[bid].show) B[bid] = blockers(tv[bid], tv);
    function ahead(a, b) { var pa = prio(tv[a]), pb = prio(tv[b]); return pa > pb || (pa === pb && +a < +b); }
    for (var id in tv) {
      var t = tv[id];
      if (!t.segs.length) { t.moving = false; if (t.st === 'leave') t.show = false; continue; }
      // wait for any truck in the way; if two block each other, the one with right of way goes first
      var wait = (B[id] || []).some(function (o) { return !((B[o] || []).indexOf(id) >= 0 && ahead(id, o)); });
      t.moving = false;
      if (wait && t.hold < 25) { t.hold += dt; continue; }
      t.hold = 0; t.moving = true;
      advance(t, (t.segs[0].k === 'f' ? SET.VF : SET.VB) * dt * (SPEED / 12));
      if (t.st === 'road' && t.qx != null && !t.segs.length) t.queued = true;
    }
  }

  /* ---------- 3D ---------- */
  var T = window.THREE, GL = !!T;
  function dispose(sc) {                                         // free the old scene's GPU memory before a rebuild
    sc.traverse(function (o) {
      if (o.geometry) o.geometry.dispose();
      if (o.material) (Array.isArray(o.material) ? o.material : [o.material]).forEach(function (m) { if (m.map) m.map.dispose(); m.dispose(); });
    });
  }
  function build3d() {
    if (!GL) return;
    KINDS.forEach(function (k) {
      var p = PANE[k], h = H[k], L = h.sim.L, V = h.sim.V;
      if (!p.R) {
        try { p.R = new T.WebGLRenderer({ canvas: p.gl, antialias: true, alpha: true }); } catch (e) { GL = false; return; }
        p.R.setPixelRatio(p.dpr || 1);
        // one camera and one pivot for both panes, so the two buildings are always seen from exactly the same angle
        if (!CAM) { CAM = new T.PerspectiveCamera(34, 1, 1, 800); CAM.position.set(BX / 2 + 18, 80, WZ1 + 70); PIVOT = new T.Vector3(BX / 2, 0, BZ / 2); }
        p.cam = CAM; p.ctl = new T.OrbitControls(CAM, p.gl); p.ctl.target = PIVOT; p.ctl.enableDamping = true; p.ctl.dampingFactor = 0.12;
        p.ctl.minDistance = 30; p.ctl.maxDistance = 320; p.ctl.maxPolarAngle = 1.38; p.ctl.enablePan = false; p.ctl.update();
        p.ctl.addEventListener('start', function () { hold(); KINDS.forEach(function (o) { PANE[o].turned = true; }); });
      }
      if (p.scene) dispose(p.scene);
      var sc = new T.Scene(); p.scene = sc;
      sc.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
      var key = new T.DirectionalLight(0xffffff, 0.65); key.position.set(-40, 80, 30); sc.add(key);
      var M = function (c, op) { return new T.MeshLambertMaterial({ color: c, transparent: !!op, opacity: op || 1, depthWrite: !op }); };
      function box(w, hh, dd, x, y, z, m, par) { var b = new T.Mesh(new T.BoxGeometry(w, hh, dd), m); b.position.set(x, y + hh / 2, z); (par || sc).add(b); return b; }
      // floor with the heat map drawn into its texture
      // floor texture over the whole plan: building floor, heat map, staging spots, and paving for this layout's yards
      var FX = function (x) { return (x - WX0) * 8; }, FZ = function (z) { return (z - WZ0) * 8; };
      var fc = document.createElement('canvas'); fc.width = Math.round((WX1 - WX0) * 8); fc.height = Math.round((WZ1 - WZ0) * 8); var g = fc.getContext('2d');
      var walls = {}; L.doors.forEach(function (q) { walls[q.wall] = 1; });
      Object.keys(walls).forEach(function (wk) {
        var f = WF[wk], a = toW(f, -1.5, 0), b = toW(f, f.len + 1.5, YD);
        g.fillStyle = '#1b2d4a'; g.fillRect(FX(Math.min(a[0], b[0])), FZ(Math.min(a[1], b[1])), Math.abs(b[0] - a[0]) * 8, Math.abs(b[1] - a[1]) * 8);
        g.setLineDash([6, 6]); g.strokeStyle = 'rgba(255,255,255,0.4)'; g.lineWidth = 1.5;
        [LANE_W - 2.6, LANE_W + 2.6].forEach(function (ww) { var p1 = toW(f, -1.5, ww), p2 = toW(f, f.len + 1.5, ww); g.beginPath(); g.moveTo(FX(p1[0]), FZ(p1[1])); g.lineTo(FX(p2[0]), FZ(p2[1])); g.stroke(); });
      });
      g.setLineDash([]);
      g.fillStyle = '#16406f'; g.fillRect(FX(0), FZ(0), BX * 8, BZ * 8);
      if (S.heat) { var heat = h.sim.heat; for (var c = 0; c < heat.length; c++) { var hv = heat[c] / h.p95; if (hv < 0.02) continue; g.fillStyle = heatColor(hv); g.fillRect(FX(c % BX), FZ(Math.floor(c / BX)), 8, 8); } }
      g.strokeStyle = 'rgba(242,201,76,0.7)'; g.lineWidth = 1.5; g.setLineDash([4, 3]);
      (L.recv === L.ship ? L.recv : L.recv.concat(L.ship)).forEach(function (q) { g.strokeRect(FX(q.x) + 1, FZ(q.z) + 1, 6.5, 6.5); });
      g.setLineDash([]);
      var tex = new T.CanvasTexture(fc); tex.anisotropy = 4;
      var fl = new T.Mesh(new T.PlaneGeometry(WX1 - WX0, WZ1 - WZ0), new T.MeshLambertMaterial({ map: tex, transparent: true }));
      fl.rotation.x = -Math.PI / 2; fl.position.set((WX0 + WX1) / 2, 0, (WZ0 + WZ1) / 2); sc.add(fl);
      // walls with door gaps
      var wall = M(0x6e86aa, 0.5);
      wallRuns(L).forEach(function (r) { var horiz = r[1] === r[3]; box(horiz ? r[2] - r[0] : 0.25, 1.4, horiz ? 0.25 : r[3] - r[1], (r[0] + r[2]) / 2, 0, (r[1] + r[3]) / 2, wall); });
      L.doors.forEach(function (q) {                      // dock leveller just inside, and a door frame in the wall
        var col = q.use === 'in' ? 0x3fa7f5 : q.use === 'out' ? 0x8dc63f : 0xc9a2ff, f = WF[q.wall], u = doorU(q), fr = M(0x9db2d2);
        var lv = toW(f, u, -0.7), j1 = toW(f, u - 1.5, 0), j2 = toW(f, u + 1.5, 0), hd = toW(f, u, 0), along = q.wall === 'S';
        box(along ? 3 : 1.6, 0.15, along ? 1.6 : 3, lv[0], 0, lv[1], M(col));
        box(0.2, 4.2, 0.3, j1[0], 0, j1[1], fr); box(0.2, 4.2, 0.3, j2[0], 0, j2[1], fr);
        box(along ? 3.2 : 0.3, 0.25, along ? 0.3 : 3.2, hd[0], 4.2, hd[1], fr);
      });
      // racks: uprights, beams and pallets (ground level coloured by the SKU's class)
      var LV = [0, 1.7, 3.4, 5.1], TOP = 6.6, m4 = new T.Matrix4(), qt = new T.Quaternion(), sv = new T.Vector3(), pv = new T.Vector3();
      var nUp = 0, nBeam = 0, cells = [];
      L.racks.forEach(function (r) {
        var len = r.dir === 'x' ? r.x1 - r.x0 + 1 : r.z1 - r.z0 + 1, dep = r.dir === 'x' ? r.z1 - r.z0 + 1 : r.x1 - r.x0 + 1;
        nUp += (Math.floor(len / 3) + 1) * 2 * (dep > 1 ? 2 : 1); nBeam += Math.ceil(len / 3) * (LV.length - 1) * 2 * (dep > 1 ? 2 : 1);
        for (var x = r.x0; x <= r.x1; x++) for (var z = r.z0; z <= r.z1; z++) cells.push([x, z, r]);
      });
      var up = new T.InstancedMesh(new T.BoxGeometry(0.1, TOP, 0.1), M(0x3d6fb3), nUp), bm = new T.InstancedMesh(new T.BoxGeometry(1, 0.13, 0.07), M(0xe8862a), nBeam), iu = 0, ib = 0;
      L.racks.forEach(function (r) {
        var along = r.dir === 'x', a0 = along ? r.x0 : r.z0, a1 = (along ? r.x1 : r.z1) + 1, b0 = along ? r.z0 : r.x0, b1 = (along ? r.z1 : r.x1) + 1;
        var faces = b1 - b0 > 1 ? [[b0, b0 + 1], [b0 + 1, b1]] : [[b0, b1]];
        faces.forEach(function (fb) {
          [fb[0] + 0.05, fb[1] - 0.05].forEach(function (bb) {
            for (var a = a0; a <= a1 + 0.01; a += 3) { var aa = Math.min(a, a1); pv.set(along ? aa : bb, TOP / 2, along ? bb : aa); sv.set(1, 1, 1); m4.compose(pv, qt, sv); up.setMatrixAt(iu++, m4); }
            for (var a2 = a0; a2 < a1; a2 += 3) { var l = Math.min(3, a1 - a2); for (var lv = 1; lv < LV.length; lv++) { pv.set(along ? a2 + l / 2 : bb, LV[lv], along ? bb : a2 + l / 2); sv.set(along ? l : 1, 1, along ? 1 : l); if (!along) { sv.set(1, 1, 1); qt.setFromAxisAngle(new T.Vector3(0, 1, 0), Math.PI / 2); sv.set(l, 1, 1); } m4.compose(pv, qt, sv); bm.setMatrixAt(ib++, m4); qt.set(0, 0, 0, 1); } }
          });
        });
      });
      up.count = iu; bm.count = ib; sc.add(up); sc.add(bm);
      var cls = {}; h.sim.faces.forEach(function (f) { if (f.sku >= 0) cls[Math.floor(f.rx) + ',' + Math.floor(f.rz)] = V.cls[f.sku]; });
      var pal = new T.InstancedMesh(new T.BoxGeometry(0.86, 1.15, 0.86), new T.MeshLambertMaterial({ color: 0xffffff }), cells.length * LV.length), ip = 0, colr = new T.Color(), rr = 1234567;
      var rnd = function () { rr = (rr * 16807) % 2147483647; return rr / 2147483647; };
      cells.forEach(function (q) {
        for (var lv = 0; lv < LV.length; lv++) {
          var key2 = q[0] + ',' + q[1], cl = lv === 0 ? cls[key2] : null;
          if (lv === 0 && !cl) continue; if (lv > 0 && rnd() > 0.72) continue;
          pv.set(q[0] + 0.5, LV[lv] + (lv ? 0.13 : 0) + 0.15 + 0.575 - 0.15, q[1] + 0.5); sv.set(1, 1, 1); m4.compose(pv, qt, sv); pal.setMatrixAt(ip, m4);
          colr.set(lv === 0 ? COL[cl] : (rnd() > 0.5 ? 0x9fb0c6 : 0x9a8466)); pal.setColorAt(ip, colr); ip++;
        }
      });
      pal.count = ip; if (pal.instanceColor) pal.instanceColor.needsUpdate = true; sc.add(pal);
      // overflow pallets in the main aisle, pack benches
      L.spill.forEach(function (c, i) { if (i % 2) return; box(0.85, 1.1, 1.8, c % BX + 0.5, 0, Math.floor(c / BX) + 1, M(0x9c7a4e)); });
      if (L.spill.length) { var ring = new T.Mesh(new T.PlaneGeometry(18, 3), new T.MeshBasicMaterial({ color: 0xff5a4e, transparent: true, opacity: 0.18, depthWrite: false })); ring.rotation.x = -Math.PI / 2; ring.position.set(45.5, 0.03, 35); sc.add(ring); }
      var pb = L.bench;
      box(pb[2] - pb[0] + 1, 0.95, pb[3] - pb[1] + 1, (pb[0] + pb[2] + 1) / 2, 0, (pb[1] + pb[3] + 1) / 2, M(0xa7b6cc));
      // dynamic things
      p.stage3 = new T.InstancedMesh(new T.BoxGeometry(0.85, 1.1, 0.85), new T.MeshLambertMaterial({ color: 0xffffff }), 80);
      var c0 = new T.Color(0xc9955a); for (var ci = 0; ci < 80; ci++) p.stage3.setColorAt(ci, c0);   // colour buffer exists before the first render
      p.stage3.count = 0; sc.add(p.stage3);
      p.hot3 = h.hot.map(function (q) { var m = new T.Mesh(new T.RingGeometry(0.85, 1.1, 40), new T.MeshBasicMaterial({ color: 0xffb02e, transparent: true, opacity: 0.8, depthWrite: false, side: T.DoubleSide })); m.rotation.x = -Math.PI / 2; m.position.set(q.x, 0.06, q.z); m.userData.r = 0.9 + Math.sqrt(q.w) / 6; sc.add(m); return m; });
      p.ag3 = {}; p.tr3 = {};
      function person() {
        var gp = new T.Group();
        var body = new T.Mesh(new T.CylinderGeometry(0.24, 0.28, 1.15, 10), M(0xf2f6fb)); body.position.y = 0.6; gp.add(body);
        var head = new T.Mesh(new T.SphereGeometry(0.2, 12, 10), M(0xffd8b0)); head.position.y = 1.4; gp.add(head);
        var vest = new T.Mesh(new T.CylinderGeometry(0.26, 0.29, 0.5, 10), M(0xffe27a)); vest.position.y = 0.85; gp.add(vest);
        var cart = new T.Mesh(new T.BoxGeometry(0.9, 0.55, 0.6), M(0x0b6fa4)); cart.position.set(0.75, 0.45, 0); gp.add(cart);
        return gp;
      }
      function lift(type) {
        var gp = new T.Group(), col = type === 'fork' ? 0xff8a3d : 0xb18cff;
        if (type === 'fork') {
          box(1.7, 1.0, 1.1, -0.2, 0.25, 0, M(col), gp); box(0.7, 0.9, 1.0, -0.6, 1.25, 0, M(0x26324a), gp);
          box(0.12, 2.6, 0.12, 0.7, 0.2, -0.4, M(0x26324a), gp); box(0.12, 2.6, 0.12, 0.7, 0.2, 0.4, M(0x26324a), gp);
          box(1.1, 0.06, 0.15, 1.25, 0.15, -0.3, M(0x26324a), gp); box(1.1, 0.06, 0.15, 1.25, 0.15, 0.3, M(0x26324a), gp);
          [[-0.7, -0.55], [-0.7, 0.55], [0.4, -0.55], [0.4, 0.55]].forEach(function (w) { var wh = new T.Mesh(new T.CylinderGeometry(0.26, 0.26, 0.2, 14), M(0x1a2230)); wh.rotation.x = Math.PI / 2; wh.position.set(w[0], 0.26, w[1]); gp.add(wh); });
        } else {
          box(0.6, 0.9, 0.7, -0.5, 0.0, 0, M(col), gp); box(1.2, 0.1, 0.7, 0.3, 0.05, 0, M(0x26324a), gp);
          var pr = person(); pr.children[3].visible = false; pr.position.set(-1.1, 0, 0); gp.add(pr);
        }
        var ld = new T.Mesh(new T.BoxGeometry(1.0, 1.1, 1.0), M(0xc9955a)); ld.position.set(type === 'fork' ? 1.35 : 0.35, type === 'fork' ? 0.78 : 0.7, 0); ld.visible = false; gp.add(ld); gp.userData.load = ld;
        var rg = new T.Mesh(new T.RingGeometry(1.2, 1.45, 32), new T.MeshBasicMaterial({ color: 0xff5a4e, transparent: true, opacity: 0.95, side: T.DoubleSide, depthWrite: false })); rg.rotation.x = -Math.PI / 2; rg.position.y = 0.05; rg.visible = false; gp.add(rg); gp.userData.ring = rg;
        return gp;
      }
      p.mkAgent = function (a) {
        var gp;
        if (a.type === 'picker') { gp = person(); var rg = new T.Mesh(new T.RingGeometry(1.0, 1.25, 32), new T.MeshBasicMaterial({ color: 0xff5a4e, transparent: true, opacity: 0.95, side: T.DoubleSide, depthWrite: false })); rg.rotation.x = -Math.PI / 2; rg.position.y = 0.05; rg.visible = false; gp.add(rg); gp.userData.ring = rg; }
        else gp = lift(a.type);
        var sk = a.type === 'picker' ? 1.7 : 1.3; gp.scale.set(sk, sk, sk); sc.add(gp); return gp;
      };
      p.mkTruck = function (dir) {                       // two groups: trailer (origin at its axles) and tractor (origin at its drive axle)
        var tr = new T.Group(), tc = new T.Group(), wm = M(0x1a2230);
        box(LT, 2.9, TW, LT / 2 - LTA, 1.1, 0, M(0xe9eef5), tr);
        box(LT - 0.4, 0.25, TW - 0.3, LT / 2 - LTA, 0.85, 0, M(0x5a6475), tr);
        [-0.65, 0.65].forEach(function (u) { [-1.05, 1.05].forEach(function (v) { var w = new T.Mesh(new T.CylinderGeometry(0.5, 0.5, 0.4, 16), wm); w.rotation.x = Math.PI / 2; w.position.set(u, 0.5, v); tr.add(w); }); });
        box(LC, 0.5, TW - 0.4, LC / 2 - RA, 0.5, 0, M(0x26324a), tc);
        box(2.1, 2.7, TW * 0.94, LC - RA - 1.05, 0.7, 0, M(dir === 'in' ? 0x3fa7f5 : 0x8dc63f), tc);
        box(0.06, 0.9, TW * 0.75, LC - RA + 0.01, 2.2, 0, M(0x26324a), tc);
        [0, 2.4].forEach(function (u) { [-1.05, 1.05].forEach(function (v) { var w = new T.Mesh(new T.CylinderGeometry(0.5, 0.5, 0.4, 16), wm); w.rotation.x = Math.PI / 2; w.position.set(u, 0.5, v); tc.add(w); }); });
        sc.add(tr); sc.add(tc); return { tr: tr, tc: tc };
      };
    });
  }
  var CAM = null, PIVOT = null;
  /* Frame the whole site (building, racks and yard) in the pane: keep the current viewing direction, aim at the
     middle of the site and move in or out until every corner sits just inside the picture. */
  function frame3d(p) {
    if (!p.cam || !p.W) return;
    // aim at the building and the part of the yard where trucks turn; a narrow pane looks down more steeply so the
    // wide site still fills it. Once the reader has turned the view, keep their direction and only refit the distance.
    var WS = WALLS; if (P2 && S.v !== 'both') { WS = {}; LAYS[S.v].doors.forEach(function (d) { WS[d.wall] = 1; }); }
    var bx0 = WS.W ? -22 : 0, bx1 = WS.E ? BX + 22 : BX, bz1 = WS.S ? BZ + 22 : BZ;   // building and the turning part of each yard
    var c = new T.Vector3((bx0 + bx1) / 2, 0, bz1 / 2), dir = p.cam.position.clone().sub(p.ctl.target);
    if (!p.turned || dir.lengthSq() < 1e-6) dir = p.W / p.H < 1.2 ? new T.Vector3(12, 100, 60) : new T.Vector3(18, 80, 100);
    dir.normalize();
    var corners = [], v = new T.Vector3();
    [0, BX].forEach(function (x) { [0, BZ].forEach(function (z) { [0, 7].forEach(function (y) { corners.push(new T.Vector3(x, y, z)); }); }); });
    [bx0, bx1].forEach(function (x) { [0, bz1].forEach(function (z) { corners.push(new T.Vector3(x, 0, z)); }); });
    function fits(dist) {
      p.cam.position.copy(c).addScaledVector(dir, dist); p.cam.lookAt(c); p.cam.updateMatrixWorld(); p.cam.updateProjectionMatrix();
      var mx = 0, my = 0, top = -9;
      corners.forEach(function (q) { v.copy(q).project(p.cam); mx = Math.max(mx, Math.abs(v.x)); my = Math.max(my, Math.abs(v.y)); top = Math.max(top, v.y); });
      return mx <= 0.96 && my <= 0.84 && top <= 0.8;            // room at the top for the layout tag
    }
    var lo = 20, hi = 600;
    for (var i = 0; i < 40; i++) { var m = (lo + hi) / 2; if (fits(m)) hi = m; else lo = m; }
    fits(hi); p.ctl.target.copy(c); p.ctl.update();
  }
  function draw3d(k) {
    var p = PANE[k], sim = LIVE[k], L = sim.L; if (!p.R || !p.scene) return;
    var ph = (performance.now() / 900) % 1;
    p.hot3.forEach(function (m, i) { var f = reduce ? 0.3 : (ph + i * 0.13) % 1, r = m.userData.r * (1 + 0.3 * f); m.scale.set(r, r, r); m.material.opacity = 0.85 - 0.5 * f; });
    var m4 = new T.Matrix4(), pv = new T.Vector3(), qt = new T.Quaternion(), sv = new T.Vector3(1, 1, 1), col = new T.Color(), n = 0;
    var spots = L.recv === L.ship ? L.recv : L.recv.concat(L.ship);
    spots.forEach(function (q) { if (!q.busy || n >= 80) return; var out = q.busy !== 'res' && q.busy.dir === 'out'; pv.set(q.x + 0.5, 0.7, q.z + 0.5); m4.compose(pv, qt, sv); p.stage3.setMatrixAt(n, m4); col.set(out ? 0xe6dfc9 : 0xc9955a); p.stage3.setColorAt(n, col); n++; });
    for (var o = 0; o < Math.min(3, sim.outQ) && n < 80; o++) { pv.set(L.packSpot % BX + 0.5 + o, 0.7, Math.floor(L.packSpot / BX) + 0.5); m4.compose(pv, qt, sv); p.stage3.setMatrixAt(n, m4); col.set(0xe6dfc9); p.stage3.setColorAt(n, col); n++; }
    p.stage3.count = n; p.stage3.instanceMatrix.needsUpdate = true; if (p.stage3.instanceColor) p.stage3.instanceColor.needsUpdate = true;
    sim.agents.forEach(function (a) {
      var gp = p.ag3[a.id] || (p.ag3[a.id] = p.mkAgent(a));
      gp.position.set(a.x, 0, a.z); gp.rotation.y = -Math.atan2(a.dirz, a.dirx);
      if (gp.userData.ring) gp.userData.ring.visible = a.waitT > 0.4;
      if (gp.userData.load) gp.userData.load.visible = !!a.load || (a.type === 'jack' && a.state === 'carry');
    });
    trucks(k);
    var seen = {};
    for (var id in TV[k]) {
      var t = wpose(TV[k][id]), tm = p.tr3[id] || (p.tr3[id] = p.mkTruck(t.dir)); seen[id] = 1;
      tm.tr.visible = tm.tc.visible = TV[k][id].show && onYard(TV[k][id]);
      tm.tr.position.set(t.A[0], 0, t.A[1]); tm.tr.rotation.y = -t.th2;
      tm.tc.position.set(t.R[0], 0, t.R[1]); tm.tc.rotation.y = -t.th1;
    }
    for (var id2 in p.tr3) if (!seen[id2]) { p.scene.remove(p.tr3[id2].tr); p.scene.remove(p.tr3[id2].tc); delete p.tr3[id2]; }
    p.ctl.update(); p.R.render(p.scene, p.cam);
  }

  /* ---------- overlay: labels and badges in both views ---------- */
  var vproj = T ? new T.Vector3() : null;
  function place(k) {
    var p = PANE[k], s3 = S.d === '3d' && p.R;
    function xy(x, y, z) {
      if (s3) { vproj.set(x, y, z).project(p.cam); return [(vproj.x + 1) / 2 * p.W, (1 - vproj.y) / 2 * p.H, vproj.z < 1]; }
      var v = p.view || fitView(p); return [v.ox + x * v.s, v.oz + z * v.s, true];
    }
    p.badges.forEach(function (b) { var q = xy(b.f.x, 3, b.f.z); b.el.hidden = !S.faults || !q[2]; b.el.style.transform = 'translate(' + q[0].toFixed(1) + 'px,' + q[1].toFixed(1) + 'px)'; });
    p.lbls.forEach(function (l) { var q = xy(l.a.x, s3 ? 7.5 : 0, l.a.z); l.el.hidden = !q[2] || (s3 && (l.a.k === 'aisle' || l.a.k === 'rack')); var w = l.el.offsetWidth; l.el.style.transform = 'translate(' + (q[0] - w / 2).toFixed(1) + 'px,' + (q[1] - 7).toFixed(1) + 'px)'; });
  }

  /* ---------- loop ---------- */
  var last = 0, visible = true, acc = 0;
  function frame(now) {
    requestAnimationFrame(frame);
    if (!visible || document.hidden || !H[KINDS[0]]) { last = now; return; }
    var dt = Math.min(0.1, (now - (last || now)) / 1000); last = now;
    sizePanes();
    acc += reduce ? 0 : dt * SPEED;
    var steps = 0;
    while (acc >= E.P.dt && steps < 120) {
      KINDS.forEach(function (k) { if (!LIVE[k].tick(E.P.dt)) { /* shift over: start again */ } });
      acc -= E.P.dt; steps++;
    }
    if (KINDS.every(function (k) { return LIVE[k].t >= E.P.shift; })) restartLive();
    KINDS.forEach(function (k) {
      var p = PANE[k]; if (p.el.hidden) return;
      p.clk.textContent = clock(LIVE[k].t);
      if (S.d === '3d' && GL) draw3d(k); else draw2d(k);
      place(k);
    });
    tour(now);
  }

  /* ---------- tour: alternate 2D and 3D side by side until the reader takes over ---------- */
  var TOUR = 30000, tStart = 0, bar = $('tour').querySelector('i');
  function hold() { S.idleAt = performance.now(); }
  function tour(now) {
    if (!S.tour || reduce) { $('tour').classList.add('off'); return; }
    var idle = now - S.idleAt > 60000 || !S.idleAt;
    if (!idle) { $('tour').classList.add('off'); tStart = now; return; }
    $('tour').classList.remove('off');
    if (!tStart) tStart = now;
    var f = (now - tStart) / TOUR; bar.style.width = Math.min(100, f * 100) + '%';
    if (f >= 1) { tStart = now; setDisp(S.d === '2d' && GL ? '3d' : '2d', true); }      // keeps the layout the reader chose
  }

  /* ---------- controls ---------- */
  function aspect() {                                            // Part 2: panes shaped like the plan (building and yards on three sides)
    if (!P2) return;
    KINDS.forEach(function (k) { var e = ext(PANE[k]); PANE[k].el.style.aspectRatio = String(Math.max(1.2, (e[1] - e[0]) / (e[3] - e[2] + 6))); });
  }
  function setView(v, auto) {
    S.v = v; if (!auto) hold();
    document.querySelectorAll('[data-v]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false'); });
    stage.classList.toggle('one', v !== 'both'); aspect();
    KINDS.forEach(function (k) { PANE[k].el.hidden = v !== 'both' && v !== k; PANE[k].W = 0; });
    report();
  }
  function setDisp(d, auto) {
    if (d === '3d' && !GL) return;
    S.d = d; if (!auto) hold();
    document.querySelectorAll('[data-d]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-d') === d ? 'true' : 'false'); });
    KINDS.forEach(function (k) { PANE[k].c2.hidden = d === '3d'; PANE[k].gl.hidden = d !== '3d'; PANE[k].W = 0; });
  }
  document.querySelectorAll('[data-v]').forEach(function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-v')); }); });
  document.querySelectorAll('[data-d]').forEach(function (b) { b.addEventListener('click', function () { setDisp(b.getAttribute('data-d')); }); });
  document.querySelectorAll('[data-h]').forEach(function (b) {
    b.addEventListener('click', function () {
      var key = b.getAttribute('data-h'); S[key] = !S[key]; b.setAttribute('aria-pressed', S[key] ? 'true' : 'false'); hold();
      if (key === 'heat') { KINDS.forEach(function (k) { PANE[k].stat = null; }); build3d(); }
    });
  });
  var pend = 0;
  function slid() {
    S.orders = +$('wl-orders').value; S.share = +$('wl-share').value / 100; hold();
    $('wl-orders-o').textContent = fmt(S.orders); $('wl-share-o').textContent = Math.round(S.share * 100) + '%';
    clearTimeout(pend); pend = setTimeout(function () { runAll(); }, 250);
  }
  $('wl-orders').addEventListener('input', slid); $('wl-share').addEventListener('input', slid);
  function noGL() { var b3 = document.querySelector('[data-d="3d"]'); b3.disabled = true; b3.title = '3D needs WebGL, which this browser has turned off'; if (S.d === '3d') setDisp('2d', true); }
  if (!GL) noGL();

  /* ---------- embedding: report the height to the article ---------- */
  var lastH = 0;
  function report() { if (!EMBED) return; var h = Math.ceil($('lab').getBoundingClientRect().height) + 4; /* content height, not the frame's: no feedback loop */ if (Math.abs(h - lastH) > 2) { lastH = h; try { window.parent.postMessage({ wlHeight: h }, '*'); } catch (e) {} } }
  window.addEventListener('message', function (e) { if (e.data === 'wlSize?') { lastH = 0; report(); } });
  window.addEventListener('resize', function () { report(); });
  if ('ResizeObserver' in window) new ResizeObserver(function () { report(); }).observe($('lab'));   // e.g. opening "How the model works"
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(stage);

  aspect();
  runAll(function () { setDisp('2d', true); requestAnimationFrame(frame); setTimeout(report, 100); });
})();
