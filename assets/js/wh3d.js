/* Warehouse operations series, Part 1: 3D pallet-rack zone of the example distributor (needs three.js r128+ as
   window.THREE). All data come from content/articles/wh_model.py through the JSON block #wh3d-data: the building,
   the racks, every pallet (class, load height, position in each of the five states) and the statistics quoted in the
   article. States are cumulative: 0 as-is, 1 beams re-set, 2 partial pallets combined, 3 dead stock cleared,
   4 fast movers re-slotted. The figure steps through them on its own until the reader picks one. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas'), svgL = stage.querySelector('.wh3d-lines');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BAYS = D.bays, BW = D.bayW, X0 = D.x0, PB = D.perBay, ROWS = D.rows, LV = D.levels, BEAM = D.beam;
  var NAMES = ['As-is', 'Beams re-set', 'Partials combined', 'Dead stock cleared', 'Fast movers re-slotted'];
  var SAY = [
    function (s) { return 'As-is: ' + pc(s.loc_util) + ' of the positions hold a pallet, so the building feels full, yet the loads fill only ' + pc(s.cube_occ) + ' of the openings they sit in.'; },
    function (s, p) { return 'Beams re-set: the same uprights carry five levels instead of four, so positions rise from ' + fmt(p.positions) + ' to ' + fmt(s.positions) + '. Each load now fills ' + pc(s.cube_occ) + ' of its opening.'; },
    function (s, p) { return 'Partial pallets combined: ' + fmt(p.occupied - s.occupied) + ' broken pallets were merged into others of the same SKU, freeing the same number of positions.'; },
    function (s, p) { return 'Dead stock cleared: ' + fmt(p.occupied - s.occupied) + ' pallets with no picks in twelve months have left the racks. ' + fmt(s.free) + ' positions are now free.'; },
    function (s, p) { return 'Fast movers re-slotted: the busiest pallets now sit low and near the front, so ' + pc(s.easy) + ' of picks are within easy reach and the walk per pick falls from ' + fmt(p.walk) + ' m to ' + fmt(s.walk) + ' m.'; }
  ];
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function pc(x) { return Math.round(x * 100) + '%'; }

  /* ----- geometry of a position index (same order as positions() in wh_model.py: row, bay, slot, level) ----- */
  function opening(levels, k) { return (k + 1 < levels.length ? levels[k + 1] - BEAM : D.maxTop) - levels[k]; }
  function where(ix, st, out) {
    var lv = LV[st === 0 ? 0 : 1], nl = lv.length, k = ix % nl, t = (ix - k) / nl, s = t % PB, t2 = (t - s) / PB, b = t2 % BAYS, r = (t2 - b) / BAYS;
    out.x = X0 + b * BW + (s + 0.5) * BW / PB; out.z = ROWS[r]; out.y = lv[k] + (k ? BEAM : 0) + 0.02; out.open = opening(lv, k); out.b = b; out.k = k;
    return out;
  }
  var N = D.p.length, CX = D.bld[0] / 2 + 2, CZ = D.bld[1] / 2;

  /* ----- colours ----- */
  var FILL = [[0, 225, 60, 55], [0.35, 230, 70, 60], [0.55, 245, 160, 50], [0.7, 235, 215, 75], [0.82, 110, 205, 105], [1, 70, 190, 110]];
  var ABC = { A: 0xFF8A3D, B: 0x3FA7F5, C: 0x9AA8BA, D: 0xB07CFF };
  function fillCol(f, c) {
    f = Math.max(0, Math.min(1, f));
    for (var i = 1; i < FILL.length; i++) if (f <= FILL[i][0]) { var a = FILL[i - 1], b = FILL[i], u = (f - a[0]) / (b[0] - a[0]); c.setRGB((a[1] + (b[1] - a[1]) * u) / 255, (a[2] + (b[2] - a[2]) * u) / 255, (a[3] + (b[3] - a[3]) * u) / 255); return c; }
    return c;
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, loads, bases, beams = [], golden, ok = !!T, running = false;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  var P = [];   /* per pallet: animation state */
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(30, 1, 1, 600);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.75); key.position.set(-30, 60, 40); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.3); rim.position.set(40, 20, -30); scene.add(rim);
    pivot = new T.Group(); scene.add(pivot);
    model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var BX = D.bld[0], BZ = D.bld[1], H = D.bld[2];
    function box(w, h, d, x, y, z, m) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y + h / 2, z); model.add(b); return b; }
    /* floor, low walls (cut away), dock doors on the front wall */
    box(BX, 0.2, BZ, BX / 2, -0.2, BZ / 2, mat(0x33435c));
    var wall = mat(0x4b5b74, { op: 0.55 });
    box(BX, 1.2, 0.25, BX / 2, 0, 0, wall); box(0.25, 1.2, BZ, 0, 0, BZ / 2, wall); box(0.25, 1.2, BZ, BX, 0, BZ / 2, wall); box(BX, 1.2, 0.25, BX / 2, 0, BZ, wall);
    var edge = new T.LineBasicMaterial({ color: 0x7f93b2, transparent: true, opacity: 0.45 });
    var eg = new T.BufferGeometry().setFromPoints([[0, 0], [BX, 0], [BX, BZ], [0, BZ], [0, 0]].map(function (p) { return new T.Vector3(p[0], H, p[1]); }));
    model.add(new T.Line(eg, edge));
    [[0, 0], [BX, 0], [BX, BZ], [0, BZ]].forEach(function (p) { model.add(new T.Line(new T.BufferGeometry().setFromPoints([new T.Vector3(p[0], 0, p[1]), new T.Vector3(p[0], H, p[1])]), edge)); });
    var door = mat(0x8dc63f);
    for (var i = 0; i < 6; i++) { box(0.3, 3.2, 3.0, -0.05, 0, 6 + i * 4.2, door); }
    /* staging lanes (front) and the front cross-aisle where picks start */
    var lane = mat(0xF2C94C, { op: 0.35 });
    for (i = 0; i < 6; i++) box(9, 0.03, 2.6, 6.5, 0.01, 6 + i * 4.2, lane);
    /* small-parts shelving and packing */
    var shelf = mat(0x6f86a8), pack = mat(0xA7B6CC);
    for (i = 0; i < 7; i++) box(40, 2.4, 1.0, 44, 0, 35.5 + i * 2.3, shelf);
    for (i = 0; i < 4; i++) box(2.4, 0.95, 1.2, 6 + i * 3.2, 0, 44, pack);
    /* golden zone: the floor and first beam level of the seven bays nearest the front */
    golden = new T.Mesh(new T.PlaneGeometry(7 * BW, ROWS[ROWS.length - 1] - ROWS[0] + 2.6), new T.MeshBasicMaterial({ color: 0x8dc63f, transparent: true, opacity: 0, depthWrite: false }));
    golden.rotation.x = -Math.PI / 2; golden.position.set(X0 + 3.5 * BW, 0.03, (ROWS[0] + ROWS[ROWS.length - 1]) / 2); model.add(golden);
    /* racks: uprights at every bay line, beams for each layout */
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3), ROWS.length * (BAYS + 1) * 2), m4 = new T.Matrix4(), q = new T.Quaternion(), sc = new T.Vector3(), ps = new T.Vector3(), n = 0, r, b, k;
    var topH = LV[1][LV[1].length - 1] + 0.2;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b <= BAYS; b++) for (k = -1; k <= 1; k += 2) {
      ps.set(X0 + b * BW, topH / 2, ROWS[r] + k * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4);
    }
    model.add(up);
    LV.forEach(function (lv, li) {
      var cnt = ROWS.length * BAYS * (lv.length - 1) * 2, im = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), new T.MeshLambertMaterial({ color: 0xE8862A, transparent: true, opacity: li ? 0 : 1 }), cnt), j = 0;
      for (r = 0; r < ROWS.length; r++) for (b = 0; b < BAYS; b++) for (k = 1; k < lv.length; k++) for (var f = -1; f <= 1; f += 2) {
        ps.set(X0 + (b + 0.5) * BW, lv[k] + BEAM / 2, ROWS[r] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); im.setMatrixAt(j++, m4);
      }
      im.visible = !li; model.add(im); beams.push(im);
    });
    /* pallets: a wooden base and the load, both instanced */
    loads = new T.InstancedMesh(new T.BoxGeometry(1, 1, 1), new T.MeshLambertMaterial({ color: 0xffffff }), N);
    bases = new T.InstancedMesh(new T.BoxGeometry(1, 1, 1), new T.MeshLambertMaterial({ color: 0x8A6A3A }), N);
    loads.instanceMatrix.setUsage(T.DynamicDrawUsage); bases.instanceMatrix.setUsage(T.DynamicDrawUsage);
    var c = new T.Color();
    for (i = 0; i < N; i++) { loads.setColorAt(i, c.setHex(0xffffff)); }
    model.add(loads); model.add(bases);
  }

  /* ----- pallet poses ----- */
  var DOCK = { x: 2.5, y: 0.3, z: D.dock, open: 2, b: 0, k: 0 }, tmp = {};
  function pose(i, st, out) {      /* where pallet i sits in state st, and whether it is there */
    var p = D.p[i], ix = p[3][st];
    if (ix >= 0) { where(ix, st, out); out.h = st < 2 ? p[1] : p[2]; out.on = 1; return out; }
    if (p[4] >= 0 && D.p[p[4]][3][st] >= 0) { where(D.p[p[4]][3][st], st, out); out.h = 0.05; out.on = 0; return out; }   /* merged into another pallet */
    out.x = DOCK.x; out.y = DOCK.y; out.z = DOCK.z + ((i * 37) % 21 - 10) * 0.9; out.open = 2; out.h = 0.05; out.on = 0; out.b = 0; out.k = 0; return out;
  }
  for (var i0 = 0; i0 < N; i0++) P.push({ a: {}, b: {}, t0: 0, dur: 1, delay: 0 });
  var cur = 0, from = 0, prog = 1, mode = 'fill', col = ok ? new T.Color() : null, m4b = ok ? new T.Matrix4() : null, qb = ok ? new T.Quaternion() : null, vs = ok ? new T.Vector3() : null, vp = ok ? new T.Vector3() : null;
  function setState(st, instant) {
    if (st === cur && prog >= 1) return;
    var A0 = [];
    for (var i = 0; i < N; i++) { var cx = curPose(i); A0.push([cx.x, cx.y, cx.z, cx.h, cx.on, cx.open]); }
    from = cur; cur = st;
    for (i = 0; i < N; i++) {
      var A = P[i].a, B = P[i].b, q0 = A0[i];
      A.x = q0[0]; A.y = q0[1]; A.z = q0[2]; A.h = q0[3]; A.on = q0[4]; A.open = q0[5];
      pose(i, st, B);
      var moving = Math.abs(A.x - B.x) + Math.abs(A.y - B.y) + Math.abs(A.z - B.z) > 0.01;
      P[i].delay = moving ? ((i * 7919) % 1000) / 1000 * 0.9 : 0; P[i].dur = moving ? 1.1 + ((i * 104729) % 100) / 250 : 0.6;
    }
    prog = instant || reduce ? 1 : 0; anim = 0;
    paint(); ui();
  }
  var anim = 0, CP = {}, bmix = 0;
  function ease(u) { return u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; }
  function curPose(i) {
    var pp = P[i], A = pp.a, B = pp.b;
    if (prog >= 1 || A.x === undefined) { return pose(i, cur, CP); }
    var u = Math.max(0, Math.min(1, (anim - pp.delay) / pp.dur)), e = ease(u), lift = Math.sin(Math.PI * e) * (Math.abs(A.x - B.x) + Math.abs(A.z - B.z) > 0.5 ? 1.4 : 0);
    CP.x = A.x + (B.x - A.x) * e; CP.z = A.z + (B.z - A.z) * e; CP.y = A.y + (B.y - A.y) * e + lift; CP.h = A.h + (B.h - A.h) * e;
    CP.on = A.on + (B.on - A.on) * e; CP.open = B.open;
    return CP;
  }
  function paint() {
    if (!ok) return;
    for (var i = 0; i < N; i++) {
      var p = D.p[i], B = pose(i, cur, tmp), h = B.on ? B.h : (cur < 2 ? p[1] : p[2]);
      if (mode === 'abc') col.setHex(ABC[p[0]]); else fillCol(h / (B.on ? B.open : 2), col);
      loads.setColorAt(i, col);
    }
    loads.instanceColor.needsUpdate = true;
  }
  function place() {
    for (var i = 0; i < N; i++) {
      var c = curPose(i), s = c.on > 0.02 ? Math.min(1, c.on * 1.2) : 0;
      if (s === 0) { vs.set(0.001, 0.001, 0.001); vp.set(0, -60, 0); m4b.compose(vp, qb, vs); loads.setMatrixAt(i, m4b); bases.setMatrixAt(i, m4b); continue; }
      vs.set(0.98 * s, Math.max(0.01, c.h - 0.14) * s, 1.18 * s); vp.set(c.x, c.y + 0.14 + (c.h - 0.14) / 2, c.z); m4b.compose(vp, qb, vs); loads.setMatrixAt(i, m4b);
      vs.set(1.0 * s, 0.14 * s, 1.2 * s); vp.set(c.x, c.y + 0.07, c.z); m4b.compose(vp, qb, vs); bases.setMatrixAt(i, m4b);
    }
    loads.instanceMatrix.needsUpdate = true; bases.instanceMatrix.needsUpdate = true;
    var bt = cur === 0 ? 0 : 1; bmix += (bt - bmix) * (reduce ? 1 : 0.06); if (Math.abs(bt - bmix) < 0.01) bmix = bt;
    beams[0].material.opacity = 1 - bmix; beams[0].visible = bmix < 0.99; beams[1].material.opacity = bmix; beams[1].visible = bmix > 0.01;
    var g = golden.material, gt = cur === 4 ? 0.22 : 0; g.opacity += (gt - g.opacity) * (reduce ? 1 : 0.08);
  }

  /* ----- labels for the areas ----- */
  var AREAS = [['Dock doors', 0, 3.4, 16.5], ['Staging lanes', 6.5, 0.2, 31], ['Picks start here', 12.5, 0.2, 15.5], ['Pallet racks', X0 + BAYS * BW / 2, 8.8, ROWS[0]],
               ['Small-parts shelving', 50, 2.6, 46], ['Packing', 11, 1.1, 44]];
  var labels = AREAS.map(function (a) { var el = document.createElement('span'); el.className = 'wh3d-label'; el.textContent = a[0]; stage.appendChild(el); return { a: a, el: el, w: 0, h: 0 }; });
  var gold = document.createElement('span'); gold.className = 'wh3d-tag'; gold.textContent = 'Easy reach: fast movers here'; stage.appendChild(gold);
  var W = 0, H = 0, wide = true, v3 = ok ? new T.Vector3() : null, measured = false;
  function toScreen(x, y, z) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); return [(v3.x * 0.5 + 0.5) * W, (-v3.y * 0.5 + 0.5) * H, v3.z]; }
  function placeLabels() {
    if (!measured) { labels.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); gold.w = gold.offsetWidth; gold.h = gold.offsetHeight; measured = true; }
    labels.forEach(function (l) {
      var s = toScreen(l.a[1], l.a[2], l.a[3]), x = Math.max(6, Math.min(W - l.w - 6, s[0] - l.w / 2)), y = Math.max(36, Math.min(H - l.h - 6, s[1] - l.h / 2));
      l.el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
    });
    var g = toScreen(X0 + 3.5 * BW, 0.2, ROWS[ROWS.length - 1] + 2.2), gx = Math.max(6, Math.min(W - gold.w - 6, g[0] - gold.w / 2)), gy = Math.max(36, Math.min(H - gold.h - 6, g[1] + 6));
    gold.style.transform = 'translate(' + gx.toFixed(1) + 'px,' + gy.toFixed(1) + 'px)'; gold.classList.toggle('is-on', cur === 4 && prog >= 1);
  }

  /* ----- numbers and text ----- */
  var steps = [].slice.call(fig.querySelectorAll('.wh3d-step'));
  function ui() {
    var s = D.stats[cur], p = D.stats[Math.max(0, cur - 1)];
    $('wh3d-loc').textContent = pc(s.loc_util); $('wh3d-cube').textContent = pc(s.cube_occ);
    $('wh3d-free').textContent = fmt(s.free) + ' of ' + fmt(s.positions); $('wh3d-pal').textContent = fmt(s.occupied);
    $('wh3d-walk').textContent = fmt(s.walk) + ' m'; $('wh3d-easy').textContent = pc(s.easy);
    $('wh3d-say').textContent = SAY[cur](s, p); $('wh3d-chip').textContent = (cur ? 'Step ' + cur + ' · ' : '') + NAMES[cur];
    $('wh3d-chip').classList.toggle('is-bad', cur === 0);
    steps.forEach(function (b, k) { b.setAttribute('aria-pressed', k === cur ? 'true' : 'false'); b.classList.toggle('is-done', k < cur); });
    var locCell = $('wh3d-loc').parentNode; locCell.classList.toggle('is-bad', s.loc_util > 0.85);
  }

  /* ----- view ----- */
  var yawU = 0.82, pitchU = 0.6, yaw = yawU, pitch = pitchU, idle = 99, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wide = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    camera.aspect = W / H; var dist = Math.max(70, (wide ? 40 : 31) / (Math.tan(15 * Math.PI / 180) * Math.min(1.5, W / H))); camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix();
  }
  function render() {
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -4, 0);
    place(); pivot.updateMatrixWorld(true); renderer.render(scene, camera); placeLabels();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawU, pitch: pitchU }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawU = Math.max(-0.9, Math.min(2.6, drag.yaw + (e.clientX - drag.x) * 0.008)); pitchU = Math.max(0.18, Math.min(1.2, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawU; pitch = pitchU; render(); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  /* ----- the tour: steps forward on its own, holds the last step, then starts again; a reader's pick pauses it ----- */
  var tourT = 0, tourOn = !reduce, pauseT = 0, HOLD = [14, 14, 14, 14, 18];   /* seconds on each step in the tour */
  var tb = $('wh3d-tour'), tbFill = tb && tb.querySelector('i'), tbText = tb && tb.querySelector('span'), tbLast = '';
  function tourBar() {            /* how long until the tour moves on, or that it is paused on the reader's pick */
    if (!tb) return;
    var txt;
    if (tourOn) { tbFill.style.width = (Math.min(1, tourT / HOLD[cur]) * 100).toFixed(1) + '%'; txt = 'Next step in ' + Math.max(1, Math.ceil(HOLD[cur] - tourT)) + ' s · pick a step to stay on it'; }
    else { tbFill.style.width = '0%'; txt = 'Staying on step ' + cur + ' · the tour resumes after a minute without clicks'; }
    if (txt !== tbLast) { tbLast = txt; tbText.textContent = txt; }
  }
  steps.forEach(function (b) { b.addEventListener('click', function () { tourOn = false; pauseT = 0; setState(+b.getAttribute('data-s')); if (!running) render(); }); });
  function setMode(m) { mode = m; $('wh3d-m-fill').setAttribute('aria-pressed', m === 'fill' ? 'true' : 'false'); $('wh3d-m-abc').setAttribute('aria-pressed', m === 'abc' ? 'true' : 'false');
    $('wh3d-leg-fill').hidden = m !== 'fill'; $('wh3d-leg-abc').hidden = m !== 'abc'; paint(); if (!running) render(); }
  $('wh3d-m-fill').addEventListener('click', function () { setMode('fill'); });
  $('wh3d-m-abc').addEventListener('click', function () { setMode('abc'); });
  var bn = $('wh3d-names');
  bn.addEventListener('click', function () { var on = bn.getAttribute('aria-pressed') !== 'true'; bn.setAttribute('aria-pressed', on ? 'true' : 'false'); stage.classList.toggle('no-names', !on); if (!running) render(); });

  var last = 0, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (t - last) / 1000 || 0)); last = t; clock += dt; idle += dt;
    if (prog < 1) { anim += dt; if (anim > 2.2) prog = 1; }
    if (tourOn) { tourT += dt; if (tourT > HOLD[cur]) { tourT = 0; setState((cur + 1) % 5); } }
    else { pauseT += dt; if (pauseT > 60 && idle > 60) { tourOn = true; tourT = 0; } }
    tourBar();
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.12 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(); requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); if (ok) paint(); ui(); render();
  window.addEventListener('resize', function () { resize(); if (!running) render(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measured = false; if (!running) render(); });
  if (reduce) { steps.forEach(function (b) { b.addEventListener('click', function () { render(); }); }); }
  else {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
