/* Warehouse operations series, Part 6: labour heat map of the Part 1 warehouse (needs three.js r128+ as window.THREE).
   Data (#wh3d6-data) come from content/articles/wh6_model.py: for each plan and week, the people in each zone each hour
   (core and temps), each zone's load against its capacity each hour, overtime a person, late orders and the plan's
   people; plus the yearly numbers. The day (06:00 to 14:30) loops; the figure tours four typical weeks on its own until
   the reader picks a week or a plan. In the flexible plan the movable core crew walk to the busiest zone each hour. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d6');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d6-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Z = D.zones, NZ = Z.length, PLANS = D.plans, HOURS = 8, KEYW = D.keyw;
  var S = { p: 'ot', all: false, w: KEYW[0][1] - 1 }, hour = reduce ? 4 : 0;
  var tourOn = !reduce, tourK = 0, tourT = 0, pauseT = 0, DAY_S = 14;      /* seconds per day; one day per toured week */
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function hm(h) { var m = 6 * 60 + Math.round(h * 60); return ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2); }
  function money(n) { return '$' + (n >= 10000 ? Math.round(n / 1000) + 'k' : fmt(n)); }

  /* zone areas on the Part 1 floor (x0, x1, z0, z1) */
  var AREA = { receive: [1.5, 11.5, 3.8, 20.4], ship: [1.5, 11.5, 21.2, 28.6], pick: [14.3, 40, 1.8, 31.2], putaway: [40.6, 70, 1.8, 31.2], pack: [3, 17, 39.6, 48.4] };
  function slots(z) {                                  /* standing spots in a zone: in the aisles for the rack zones, a grid elsewhere */
    var a = AREA[z], out = [], i, j;
    if (z === 'pick' || z === 'putaway') { for (j = 0; j < 6; j++) for (i = 0; i < D.aisles.length; i++) out.push([a[0] + 3 + j * (a[1] - a[0] - 6) / 5, D.aisles[i]]); }
    else { var cols = Math.max(2, Math.floor((a[1] - a[0]) / 1.8)), rows = Math.max(2, Math.floor((a[3] - a[2]) / 1.8)); for (j = 0; j < rows; j++) for (i = 0; i < cols; i++) out.push([a[0] + 1 + i * 1.8, a[2] + 1 + j * 1.8]); }
    return out;
  }
  var SLOTS = {}; Z.forEach(function (z) { SLOTS[z] = slots(z); });
  function W(p, w) { return D.P[p].w[w]; }
  function heads(p, w, h) { var x = W(p, w); return Z.map(function (z, i) { return [x[0][i][h], x[1][i][h]]; }); }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false, tiles = {}, people = {};
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d6-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  var CX = D.bld[0] / 2, CZ = D.bld[1] / 2;
  var MAXP = 0; PLANS.forEach(function (p) { D.P[p].w.forEach(function (x) { for (var h = 0; h < HOURS; h++) { var n = 0; for (var i = 0; i < NZ; i++) n += x[0][i][h] + x[1][i][h]; MAXP = Math.max(MAXP, n); } }); });
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 600);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.7); key.position.set(-30, 60, 40); scene.add(key);
    pivot = new T.Group(); pivot.rotation.order = 'YXZ'; scene.add(pivot); model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var BX = D.bld[0], BZ = D.bld[1], ROWS = D.rows, BAYS = D.bays, BW = D.bayW, X0 = D.x0, LV = D.levels, BEAM = D.beam, i, r, b, k;
    function box(w, h, d, x, y, z, m) { var o = new T.Mesh(new T.BoxGeometry(w, h, d), m); o.position.set(x, y + h / 2, z); model.add(o); return o; }
    box(BX, 0.2, BZ, BX / 2, -0.2, BZ / 2, mat(0x2a3446));
    var wall = mat(0x4b5b74, { op: 0.5 });
    box(BX, 1.2, 0.25, BX / 2, 0, 0, wall); box(0.25, 1.2, BZ, 0, 0, BZ / 2, wall); box(0.25, 1.2, BZ, BX, 0, BZ / 2, wall); box(BX, 1.2, 0.25, BX / 2, 0, BZ, wall);
    for (i = 0; i < 6; i++) box(0.3, 3.2, 3.0, -0.05, 0, 6 + i * 4.2, mat(i < 4 ? 0x8dc63f : 0xFF8A3D));
    var shelf = mat(0x56688a); for (i = 0; i < 7; i++) box(40, 2.4, 1.0, 44, 0, 35.5 + i * 2.3, shelf);
    for (i = 0; i < 4; i++) box(2.4, 0.95, 1.2, 6 + i * 3.2, 0, 46.5, mat(0xA7B6CC));
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3, { op: 0.55 }), ROWS.length * (BAYS + 1) * 2), m4 = new T.Matrix4(), q = new T.Quaternion(), sc = new T.Vector3(), ps = new T.Vector3(), n = 0;
    var topH = LV[LV.length - 1] + 0.2;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b <= BAYS; b++) for (k = -1; k <= 1; k += 2) { ps.set(X0 + b * BW, topH / 2, ROWS[r] + k * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4); }
    model.add(up);
    var bm = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), mat(0xE8862A, { op: 0.45 }), ROWS.length * BAYS * (LV.length - 1) * 2); n = 0;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b < BAYS; b++) for (k = 1; k < LV.length; k++) for (var f = -1; f <= 1; f += 2) { ps.set(X0 + (b + 0.5) * BW, LV[k] + BEAM / 2, ROWS[r] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); bm.setMatrixAt(n++, m4); }
    model.add(bm);
    Z.forEach(function (z) {
      var a = AREA[z], t = new T.Mesh(new T.PlaneGeometry(a[1] - a[0], a[3] - a[2]), new T.MeshBasicMaterial({ color: 0x3FA7F5, transparent: true, opacity: 0.42, depthWrite: false }));
      t.rotation.x = -Math.PI / 2; t.position.set((a[0] + a[1]) / 2, 0.03, (a[2] + a[3]) / 2); model.add(t); tiles[z] = t;
      var e = new T.LineLoop(new T.BufferGeometry().setFromPoints([[a[0], a[2]], [a[1], a[2]], [a[1], a[3]], [a[0], a[3]]].map(function (p) { return new T.Vector3(p[0], 0.05, p[1]); })), new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.35 }));
      model.add(e);
    });
    var body = new T.CylinderGeometry(0.42, 0.45, 1.5, 12), head = new T.SphereGeometry(0.34, 12, 10);
    PLANS.forEach(function (p) {
      var arr = [];
      for (var j = 0; j < MAXP; j++) {
        var g = new T.Group(), bmx = new T.MeshLambertMaterial({ color: 0x2f6db5 });
        var bo = new T.Mesh(body, bmx); bo.position.y = 0.75; g.add(bo);
        var hd = new T.Mesh(head, new T.MeshLambertMaterial({ color: 0xF2D1B3 })); hd.position.y = 1.8; g.add(hd);
        g.scale.setScalar(1.25); g.visible = false; model.add(g);
        arr.push({ g: g, mat: bmx, x: CX, z: CZ, tx: CX, tz: CZ, zone: null, temp: false, on: false });
      }
      people[p] = arr;
    });
  }

  /* ----- who stands where, hour by hour ----- */
  function assign(p, w, h) {
    var hd = heads(p, w, h), arr = people[p], i, k;
    var core = arr.filter(function (x, j) { return j < 40; });
    /* how many core and temps each zone needs this hour */
    var needCore = {}, needTemp = {}; Z.forEach(function (z, i) { needCore[z] = hd[i][0]; needTemp[z] = hd[i][1]; });
    var totCore = 0, totTemp = 0; Z.forEach(function (z) { totCore += needCore[z]; totTemp += needTemp[z]; });
    /* keep people where they are when the zone still needs them; others walk to zones that are short */
    var cores = arr.slice(0, totCore), temps = arr.slice(totCore, totCore + totTemp), rest = arr.slice(totCore + totTemp);
    rest.forEach(function (x) { x.on = false; });
    function fill(list, need, isTemp) {
      var have = {}; Z.forEach(function (z) { have[z] = 0; });
      var free = [];
      list.forEach(function (x) { if (x.on && x.zone && x.temp === isTemp && have[x.zone] < need[x.zone]) have[x.zone]++; else free.push(x); });
      list.forEach(function (x) { x.temp = isTemp; });
      Z.forEach(function (z) { while (have[z] < need[z] && free.length) { var x = free.shift(); if (!x.on) { var s0 = SLOTS[z][0]; x.x = x.tx = s0[0]; x.z = x.tz = s0[1]; } x.zone = z; x.on = true; have[z]++; } });
    }
    fill(cores, needCore, false); fill(temps, needTemp, true);
    /* spots inside each zone */
    var used = {}; Z.forEach(function (z) { used[z] = 0; });
    cores.concat(temps).forEach(function (x) { var s = SLOTS[x.zone][used[x.zone]++ % SLOTS[x.zone].length]; x.tx = s[0]; x.tz = s[1]; x.mat.color.setHex(x.temp ? 0xFF8A3D : 0x2f6db5); });
  }
  var lastKey = {};
  function updatePeople(p, dt, instant) {
    var h = Math.min(HOURS - 1, Math.floor(hour)), key = S.w + ':' + h;
    if (lastKey[p] !== key) { assign(p, S.w, h); lastKey[p] = key; }
    var e = instant ? 1 : 1 - Math.exp(-dt * 2.2);
    people[p].forEach(function (x) {
      x.g.visible = x.on;
      if (!x.on) return;
      var dx = x.tx - x.x, dz = x.tz - x.z; x.x += dx * e; x.z += dz * e;
      x.g.position.set(x.x, 0, x.z);
    });
  }
  function utilColor(u, c) {
    var stops = [[0, 0x3FA7F5], [0.6, 0x3FA7F5], [0.75, 0x6ECD69], [0.95, 0x6ECD69], [1.05, 0xF5A032], [1.2, 0xFF5A4A], [9, 0xFF5A4A]];
    for (var i = 1; i < stops.length; i++) if (u <= stops[i][0]) { var a = new T.Color(stops[i - 1][1]), b = new T.Color(stops[i][1]); return c.copy(a).lerp(b, (u - stops[i - 1][0]) / (stops[i][0] - stops[i - 1][0])); }
    return c.setHex(0xFF5A4A);
  }
  var colTmp = ok ? new T.Color() : null;
  function paint(p) {
    var h = Math.min(HOURS - 1, Math.floor(hour)), u = W(p, S.w)[2];
    Z.forEach(function (z, i) { tiles[z].material.color.copy(utilColor(u[i][h], colTmp)); tiles[z].material.opacity = 0.42 + Math.min(0.3, Math.max(0, u[i][h] - 1)); });
    PLANS.forEach(function (q) { people[q].forEach(function (x) { if (q !== p) x.g.visible = false; }); });
  }

  /* ----- labels ----- */
  var labels = Z.map(function (z, i) { var el = document.createElement('span'); el.className = 'wh3d-label wh3d6-zl'; stage.appendChild(el); return { z: z, i: i, el: el }; });
  var quads = PLANS.map(function (p, i) { var el = document.createElement('span'); el.className = 'wh3d2-q'; el.textContent = D.pnames[i]; el.style.setProperty('--c', ['#FF6B5A', '#B07CFF', '#F5A032', '#8DC63F'][i]); stage.appendChild(el); return el; });
  var Wd = 0, Hd = 0, wide = true, v3 = ok ? new T.Vector3() : null;
  function placeLabels(p) {
    var h = Math.min(HOURS - 1, Math.floor(hour)), x = W(p, S.w), boxes = [];
    labels.forEach(function (l) {
      if (S.all) { l.el.style.display = 'none'; return; }
      l.el.style.display = '';
      var n = x[0][l.i][h] + x[1][l.i][h], u = x[2][l.i][h];
      l.el.textContent = D.names[l.i] + ' · ' + n + ' · ' + Math.round(u * 100) + '%';
      l.el.classList.toggle('is-red', u > 1.05);
      var a = AREA[l.z]; v3.set((a[0] + a[1]) / 2, 2.6, (a[2] + a[3]) / 2); model.localToWorld(v3); v3.project(camera);
      var w = l.el.offsetWidth, hh = l.el.offsetHeight;
      boxes.push({ el: l.el, w: w, h: hh, x: Math.max(6, Math.min(Wd - w - 6, (v3.x * 0.5 + 0.5) * Wd - w / 2)), y: Math.max(36, Math.min(Hd - hh - 6, (-v3.y * 0.5 + 0.5) * Hd - hh / 2)) });
    });
    boxes.sort(function (a, b) { return a.y - b.y; });
    for (var i = 0; i < boxes.length; i++) for (var j = 0; j < i; j++) { var a = boxes[i], b = boxes[j]; if (a.x < b.x + b.w + 4 && b.x < a.x + a.w + 4 && a.y < b.y + b.h + 3 && b.y < a.y + a.h + 3) a.y = b.y + b.h + 3; }
    boxes.forEach(function (q) { q.el.style.transform = 'translate(' + q.x.toFixed(1) + 'px,' + Math.min(Hd - q.h - 6, q.y).toFixed(1) + 'px)'; });
  }

  /* ----- panel ----- */
  var SAY = {
    ot: 'Lean crew plus overtime: seven people all year. In busy weeks the red zones mean overtime, and when overtime runs out, orders ship late.',
    peak: 'Crew sized for the peak: eleven people all year. Nothing is ever red, but most of the year much of the floor is blue: paid and idle.',
    temps: 'Core crew plus planned temps: temps (orange) start two weeks before they are needed. Without cross-training, a zone still goes red at its own busiest hour.',
    flex: 'Temps plus a cross-trained crew: watch the blue figures walk to the busiest zone each hour, so fewer temps and less overtime are needed.'
  };
  function cell(id, f) { var el = $(id); el.style.fontSize = S.all ? '14px' : ''; el.style.whiteSpace = S.all ? 'normal' : ''; el.textContent = S.all ? PLANS.map(function (q) { return f(q); }).join(' · ') : f(S.p); }
  function ui() {
    var w = S.w, h = Math.min(HOURS - 1, Math.floor(hour));
    $('wh3d6-ord').textContent = fmt(D.orders[w]);
    cell('wh3d6-ppl', function (q) { var hd = heads(q, w, h), n = 0, t = 0; hd.forEach(function (x) { n += x[0]; t += x[1]; }); return S.all ? String(n + t) : n + t + (t ? ' (' + t + ' temps)' : ''); });
    cell('wh3d6-ot', function (q) { return W(q, w)[3].toFixed(1) + (S.all ? '' : ' h'); });
    cell('wh3d6-late', function (q) { return fmt(W(q, w)[4]); });
    cell('wh3d6-cost', function (q) { return money(D.P[q].s[0]); });
    cell('wh3d6-cpo', function (q) { return '$' + D.P[q].s[1].toFixed(2); });
    fig.querySelectorAll('[data-p]').forEach(function (b) { var v = b.getAttribute('data-p'); b.setAttribute('aria-pressed', (v === 'all' ? S.all : !S.all && v === S.p) ? 'true' : 'false'); });
    fig.querySelectorAll('[data-w]').forEach(function (b) { b.setAttribute('aria-pressed', +b.getAttribute('data-w') === w ? 'true' : 'false'); });
    var kw = KEYW.filter(function (k) { return k[1] - 1 === w; })[0];
    $('wh3d6-wk').textContent = 'Week ' + (w + 1) + (kw ? ' · ' + kw[0] : '');
    $('wh3d6-say').textContent = S.all ? 'Week ' + (w + 1) + ', all four plans at the same hour. Compare the colours: red is work the people there cannot keep up with, blue is paid time with no work.' : SAY[S.p];
    yearChart();
  }
  function yearChart() {
    var svgEl = $('wh3d6-ysvg'), mx = 13, bw = 600 / D.need.length, s = '';
    D.need.forEach(function (n, i) { var hgt = n / mx * 86; s += '<rect data-wk="' + i + '" x="' + (i * bw + 0.6).toFixed(1) + '" y="' + (88 - hgt).toFixed(1) + '" width="' + (bw - 1.2).toFixed(1) + '" height="' + hgt.toFixed(1) + '" fill="' + (i === S.w ? '#FFE27A' : 'rgba(159,178,204,.45)') + '"/>'; });
    var shown = S.all ? PLANS : [S.p], cols = { ot: '#FF6B5A', peak: '#B07CFF', temps: '#F5A032', flex: '#8DC63F' };
    shown.forEach(function (q) {
      var d = D.P[q].w.map(function (x, i) { return (i * bw + bw / 2).toFixed(1) + ',' + (88 - x[5] / mx * 86).toFixed(1); }).join(' ');
      s += '<polyline points="' + d + '" fill="none" stroke="' + cols[q] + '" stroke-width="2" vector-effect="non-scaling-stroke"/>';
    });
    svgEl.innerHTML = s;
  }
  $('wh3d6-ysvg').addEventListener('click', function (e) {
    var r = this.getBoundingClientRect(), i = Math.max(0, Math.min(D.need.length - 1, Math.floor((e.clientX - r.left) / r.width * D.need.length)));
    S.w = i; tourOn = false; pauseT = 0; ui(); if (!running) render();
  });
  fig.querySelectorAll('[data-p]').forEach(function (b) { b.addEventListener('click', function () { var v = b.getAttribute('data-p'); if (v === 'all') S.all = true; else { S.all = false; S.p = v; } ui(); if (!running) render(); }); });
  fig.querySelectorAll('[data-w]').forEach(function (b) { b.addEventListener('click', function () { S.w = +b.getAttribute('data-w'); tourOn = false; pauseT = 0; ui(); if (!running) render(); }); });
  var tb = $('wh3d6-tour'), tbFill = tb.querySelector('i'), tbText = tb.querySelector('span'), tbLast = '';
  function tourBar() {
    var txt;
    if (tourOn) { tbFill.style.width = (Math.min(1, tourT / DAY_S) * 100).toFixed(1) + '%'; txt = 'Touring four weeks · next week in ' + Math.max(1, Math.ceil(DAY_S - tourT)) + ' s · pick a week to stay on it'; }
    else { tbFill.style.width = '0%'; txt = 'Staying on week ' + (S.w + 1) + ' · the tour resumes after a minute without clicks'; }
    if (txt !== tbLast) { tbLast = txt; tbText.textContent = txt; }
  }

  /* ----- view ----- */
  var yawU = 0.62, pitchU = 0.78, yaw = yawU, pitch = pitchU, idle = 99, clock = 0;
  function resize() { var rc = stage.getBoundingClientRect(); Wd = rc.width; Hd = rc.height; wide = Wd >= 560; if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(Wd, Hd, false); }
  function aim(w, h) { camera.aspect = w / h; var dist = Math.max(60, (S.all ? 34 : 40) / (Math.tan(15 * Math.PI / 180) * Math.min(1.6, w / h))); camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix(); }
  var lastHour = -1;
  function render(dt) {
    dt = dt || 0;
    var h = Math.min(HOURS - 1, Math.floor(hour));
    $('wh3d6-chip').textContent = 'Week ' + (S.w + 1) + ' · ' + hm(hour);
    if (h !== lastHour) { lastHour = h; ui(); }
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -3, 0);
    PLANS.forEach(function (q) { updatePeople(q, dt, dt === 0); });
    renderer.setScissorTest(false); renderer.setViewport(0, 0, Wd, Hd); renderer.clear();
    if (!S.all) { paint(S.p); people[S.p].forEach(function (x) { x.g.visible = x.on; }); pivot.updateMatrixWorld(true); aim(Wd, Hd); renderer.render(scene, camera); quads.forEach(function (q) { q.style.display = 'none'; }); placeLabels(S.p); }
    else {
      renderer.setScissorTest(true); var hw = Wd / 2, hh = Hd / 2;
      PLANS.forEach(function (p, i) {
        var x = (i % 2) * hw, y = i < 2 ? hh : 0;
        paint(p); people[p].forEach(function (q) { q.g.visible = q.on; }); pivot.updateMatrixWorld(true);
        renderer.setViewport(x, y, hw, hh); renderer.setScissor(x, y, hw, hh); aim(hw, hh); renderer.render(scene, camera);
        var qd = quads[i]; qd.style.display = ''; qd.style.transform = 'translate(' + (x + 10) + 'px,' + ((i < 2 ? 0 : hh) + 34) + 'px)';
      });
      renderer.setScissorTest(false); placeLabels(S.p);
    }
    stage.classList.toggle('is-quad', S.all);
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawU, pitch: pitchU }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) { if (!drag) return; yawU = Math.max(-0.9, Math.min(2.6, drag.yaw + (e.clientX - drag.x) * 0.008)); pitchU = Math.max(0.2, Math.min(1.35, drag.pitch + (e.clientY - drag.y) * 0.005)); idle = 0; if (!running) { yaw = yawU; pitch = pitchU; render(); } });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  var last = 0, visible = true;
  function frame(ts) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (ts - last) / 1000 || 0)); last = ts; clock += dt; idle += dt;
    hour += dt * (HOURS + 0.5) / DAY_S; if (hour >= HOURS + 0.5) hour = 0;
    if (tourOn) { tourT += dt; if (tourT > DAY_S) { tourT = 0; tourK = (tourK + 1) % KEYW.length; S.w = KEYW[tourK][1] - 1; hour = 0; ui(); } }
    else { pauseT += dt; if (pauseT > 60 && idle > 60) { tourOn = true; tourT = 0; } }
    tourBar();
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.08 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(dt); requestAnimationFrame(frame);
  }
  function setRun(v) { if (reduce) return; if (v && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); } else if (!v) running = false; }
  if (ok) { build(); renderer.autoClear = false; stage.classList.add('is-live'); }
  resize(); ui(); tourBar(); render();
  window.addEventListener('resize', function () { resize(); if (!running) render(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
