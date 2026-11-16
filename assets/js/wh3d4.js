/* Warehouse operations series, Part 4: a year of stock-record accuracy in the Part 1 racks (needs three.js r128+ as
   window.THREE). Data (#wh3d4-data) come from content/articles/wh4_model.py: every occupied location (class, rack
   position, load height) and, for each counting plan, the weeks when its record changed (0 right, 1 wrong quantity,
   2 phantom), the replayed year's weekly accuracy and the averaged numbers. The counting schedule is the model's own
   rule: a location is counted when week % period == (index * 7919) % period. 52 weeks play in about 45 seconds. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d4');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d4-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BAYS = D.bays, BW = D.bayW, X0 = D.x0, PB = D.perBay, ROWS = D.rows, LV = D.levels, BEAM = D.beam, N = D.locs.length, WK = D.weeks;
  var PLANS = ['annual', 'cycle', 'fixed'], NAMES = { annual: 'Annual count only', cycle: 'ABC cycle counting', fixed: 'Cycle counting + causes fixed' };
  var CURV = { annual: '#FF6B5A', cycle: '#3FA7F5', fixed: '#8DC63F' };
  var S = { p: 'annual', all: false }, week = reduce ? 40 : 0, wf = 0;
  function pc(x) { return (x * 100).toFixed(0) + '%'; }
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }

  /* status table: status[plan][week * N + i] */
  var status = {};
  PLANS.forEach(function (p) {
    var a = new Uint8Array((WK + 1) * N), ev = D.st[p].ev;
    for (var i = 0; i < N; i++) {
      var e = ev[i], k = 0, s = 0;
      for (var w = 0; w <= WK; w++) { while (k < e.length && e[k][0] <= w) { s = e[k][1]; k++; } a[w * N + i] = s; }
    }
    status[p] = a;
  });
  function counted(p, i, w) {
    if (p === 'annual') return w === WK;
    var per = (p === 'fixed' ? D.periodF : D.period)[D.locs[i][0]];
    return w > 0 && w % per === (i * 7919) % per;
  }
  function rackPos(ix) {
    var nl = LV.length, k = ix % nl, q = (ix - k) / nl, s = q % PB, q2 = (q - s) / PB, b = q2 % BAYS, r = (q2 - b) / BAYS;
    return { x: X0 + b * BW + (s + 0.5) * BW / PB, y: LV[k] + (k ? BEAM : 0) + 0.02, z: ROWS[r], r: r, b: b, k: k };
  }
  var POS = D.locs.map(function (l) { return rackPos(l[1]); });

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false, solid, ghost, rings, ringCol;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d4-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  var CX = X0 + BAYS * BW / 2, CZ = (ROWS[0] + ROWS[ROWS.length - 1]) / 2;
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 500);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.7); key.position.set(-30, 60, 40); scene.add(key);
    pivot = new T.Group(); scene.add(pivot); model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var fl = new T.Mesh(new T.BoxGeometry(BAYS * BW + 20, 0.2, ROWS[ROWS.length - 1] - ROWS[0] + 16), mat(0x33435c)); fl.position.set(CX, -0.1, CZ); model.add(fl);
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3), ROWS.length * (BAYS + 1) * 2), m4 = new T.Matrix4(), q = new T.Quaternion(), sc = new T.Vector3(), ps = new T.Vector3(), n = 0, r, b, k;
    var topH = LV[LV.length - 1] + 0.2;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b <= BAYS; b++) for (k = -1; k <= 1; k += 2) { ps.set(X0 + b * BW, topH / 2, ROWS[r] + k * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4); }
    model.add(up);
    var bm = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), mat(0xE8862A), ROWS.length * BAYS * (LV.length - 1) * 2); n = 0;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b < BAYS; b++) for (k = 1; k < LV.length; k++) for (var f = -1; f <= 1; f += 2) { ps.set(X0 + (b + 0.5) * BW, LV[k] + BEAM / 2, ROWS[r] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); bm.setMatrixAt(n++, m4); }
    model.add(bm);
    solid = new T.InstancedMesh(new T.BoxGeometry(0.98, 1, 1.18), new T.MeshLambertMaterial({ color: 0xffffff }), N);
    ghost = new T.InstancedMesh(new T.BoxGeometry(0.98, 1, 1.18), new T.MeshBasicMaterial({ color: 0xFF5A4A, transparent: true, opacity: 0.38, depthWrite: false }), N);
    var ge = new T.LineSegments(new T.EdgesGeometry(new T.BoxGeometry(0.98, 1, 1.18)), new T.LineBasicMaterial({ color: 0xFF7A6A }));
    var c = new T.Color(0xffffff); for (var i = 0; i < N; i++) solid.setColorAt(i, c);
    model.add(solid); model.add(ghost);
    ghostEdges = []; /* outlines for ghosts are drawn as one merged buffer, rebuilt when the week changes */
    edgeTpl = ge.geometry.attributes.position.array; edgeBuf = new Float32Array(N * edgeTpl.length);   /* one buffer, reused every frame */
    edgeGeo = new T.BufferGeometry(); edgeGeo.setAttribute('position', new T.BufferAttribute(edgeBuf, 3)); edgeGeo.setDrawRange(0, 0);
    edgeLines = new T.LineSegments(edgeGeo, new T.LineBasicMaterial({ color: 0xFF8A7A, transparent: true, opacity: 0.9 })); edgeLines.frustumCulled = false; model.add(edgeLines);
    var c2 = document.createElement('canvas'); c2.width = c2.height = 64; var x2 = c2.getContext('2d'), gr = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,.7)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x2.fillStyle = gr; x2.fillRect(0, 0, 64, 64);
    var rg = new T.BufferGeometry(); ringPos = new Float32Array(N * 3); ringCol = new Float32Array(N * 3);
    for (i = 0; i < N; i++) { ringPos[i * 3] = POS[i].x; ringPos[i * 3 + 1] = POS[i].y + D.locs[i][2] + 0.5; ringPos[i * 3 + 2] = POS[i].z - 0.75; }
    rg.setAttribute('position', new T.BufferAttribute(ringPos, 3)); rg.setAttribute('color', new T.BufferAttribute(ringCol, 3));
    rings = new T.Points(rg, new T.PointsMaterial({ size: 2.2, map: new T.CanvasTexture(c2), transparent: true, depthWrite: false, depthTest: false, vertexColors: true, blending: T.AdditiveBlending }));
    rings.renderOrder = 5; model.add(rings);
  }
  var ghostEdges, edgeGeo, edgeLines, edgeTpl, edgeBuf, ringPos;
  var m4b = ok ? new T.Matrix4() : null, qb = ok ? new T.Quaternion() : null, vs = ok ? new T.Vector3() : null, vp = ok ? new T.Vector3() : null, col = ok ? new T.Color() : null;
  var COLS = [0x5E6A7C, 0xF5A032];
  function paint(p, w, pulse) {      /* the racks as plan p's records stand in week w */
    var a = status[p], base = w * N, i, n, ep = edgeBuf, ei = 0;
    for (i = 0; i < N; i++) {
      var s = a[base + i], P = POS[i], h = D.locs[i][2];
      vs.set(1, h, 1); vp.set(P.x, P.y + h / 2, P.z); m4b.compose(vp, qb, vs);
      if (s === 2) {
        ghost.setMatrixAt(i, m4b); vs.set(0.001, 0.001, 0.001); m4b.compose(vp, qb, vs); solid.setMatrixAt(i, m4b);
        for (n = 0; n < edgeTpl.length; n += 3) { ep[ei++] = P.x + edgeTpl[n]; ep[ei++] = P.y + h / 2 + edgeTpl[n + 1] * h; ep[ei++] = P.z + edgeTpl[n + 2]; }
      } else {
        solid.setMatrixAt(i, m4b); solid.setColorAt(i, col.setHex(COLS[s])); vs.set(0.001, 0.001, 0.001); m4b.compose(vp, qb, vs); ghost.setMatrixAt(i, m4b);
      }
      var on = counted(p, i, w) ? pulse : 0; ringCol[i * 3] = on; ringCol[i * 3 + 1] = on * 0.89; ringCol[i * 3 + 2] = on * 0.48;
    }
    solid.instanceMatrix.needsUpdate = true; ghost.instanceMatrix.needsUpdate = true; solid.instanceColor.needsUpdate = true;
    edgeGeo.setDrawRange(0, ei / 3); edgeGeo.attributes.position.needsUpdate = true;
    rings.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- panel ----- */
  function accNow(p, w) { return D.st[p].acc[w]; }
  var SAY = {
    annual: 'Annual count only: records drift wrong all year, and phantom stock is found by pickers until the year-end count puts it right.',
    cycle: 'ABC cycle counting: a few locations every day, the busy A items every four weeks, so errors are found and corrected within weeks.',
    fixed: 'Cycle counting with the causes fixed: scanning at receiving, put-away and picking means fewer records go wrong, and B and C need fewer counts.'
  };
  function ui() {
    var p = S.p, s = D.st[p].s;
    function cell(id, k, f) { $(id).textContent = S.all ? PLANS.map(function (q) { return f(D.st[q].s[k]); }).join(' · ') : f(s[k]); }
    cell('wh3d4-avg', 0, function (v) { return S.all ? pc(v) : (v * 100).toFixed(1) + '%'; }); cell('wh3d4-short', 1, fmt);
    cell('wh3d4-hours', 2, function (v) { return fmt(v) + (S.all ? '' : ' h'); }); cell('wh3d4-total', 3, function (v) { return fmt(v) + (S.all ? '' : ' h'); }); cell('wh3d4-closed', 4, String);
    fig.querySelectorAll('[data-s]').forEach(function (b) { var v = b.getAttribute('data-s'); b.setAttribute('aria-pressed', (v === 'all' ? S.all : !S.all && v === p) ? 'true' : 'false'); });
    var g = '';
    PLANS.forEach(function (q) {
      var d = D.curves[q].map(function (a, w) { return (w / WK * 600).toFixed(1) + ',' + (110 - (a - 0.6) / 0.4 * 110).toFixed(1); }).join(' ');
      var on = S.all || q === p;
      g += '<polyline points="' + d + '" fill="none" stroke="' + CURV[q] + '" stroke-width="' + (on ? 2 : 1.2) + '" opacity="' + (on ? 1 : 0.3) + '" vector-effect="non-scaling-stroke"/>';
    });
    $('wh3d4-lines').innerHTML = g;
  }
  var lastSay = '';
  function live() {
    var p = S.p, w = week, a = accNow(p, w);
    $('wh3d4-chip').textContent = 'Week ' + w + (S.all || !wide ? '' : ' · ' + NAMES[p]);
    $('wh3d4-chip').classList.toggle('is-bad', !S.all && a < 0.85);
    $('wh3d4-now').textContent = S.all ? PLANS.map(function (q) { return pc(accNow(q, w)); }).join(' · ') : (a * 100).toFixed(1) + '%';
    var x = (w / WK * 600).toFixed(1), cl = $('wh3d4-cur'); cl.setAttribute('x1', x); cl.setAttribute('x2', x); cl.setAttribute('y1', 0); cl.setAttribute('y2', 110);
    var txt = S.all ? 'Week ' + w + ', records right: ' + PLANS.map(function (q) { return NAMES[q] + ' ' + pc(accNow(q, w)); }).join(', ') + '.'
      : (p === 'annual' && w === WK ? 'Week 52: the warehouse closes for two days for the wall-to-wall count, and accuracy jumps back up.' : SAY[p]);
    if (txt !== lastSay) { lastSay = txt; $('wh3d4-say').textContent = txt; }
  }

  /* ----- the "System 40, shelf 12" tag on one phantom location ----- */
  var tag = $('wh3d4-tag'), tagIx = -1, tagT = 0, v3 = ok ? new T.Vector3() : null;
  function sysQty(i) { return Math.max(6, Math.round(D.locs[i][2] * 20)); }
  function pickTag() {
    var a = status[S.p], base = week * N, list = [];
    for (var i = 0; i < N; i++) if (a[base + i] === 2 && POS[i].k <= 2) list.push(i);
    tagIx = list.length ? list[Math.floor(Math.random() * list.length)] : -1;
    if (tagIx >= 0) { var P = POS[tagIx], sq = sysQty(tagIx), sh = (tagIx % 3) ? Math.round(sq * 0.3 * (tagIx % 2)) : 0;
      tag.textContent = 'R' + (P.r + 1) + '-B' + (P.b + 1) + '-L' + (P.k + 1) + ' · System ' + sq + ' · Shelf ' + sh; }
  }
  function placeTag(w0, h0) {
    if (S.all || tagIx < 0 || status[S.p][week * N + tagIx] !== 2) { tag.classList.remove('is-on'); return; }
    var P = POS[tagIx]; v3.set(P.x, P.y + D.locs[tagIx][2] + 0.8, P.z); model.localToWorld(v3); v3.project(camera);
    var x = (v3.x * 0.5 + 0.5) * w0, y = (-v3.y * 0.5 + 0.5) * h0, tw = tag.offsetWidth;
    tag.style.transform = 'translate(' + Math.max(6, Math.min(w0 - tw - 6, x - tw / 2)).toFixed(1) + 'px,' + Math.max(36, y - 34).toFixed(1) + 'px)'; tag.classList.add('is-on');
  }

  /* ----- view ----- */
  var yawU = 0.5, pitchU = 0.7, yaw = yawU, pitch = pitchU, idle = 99, clock = 0, W = 0, H = 0, wide = true;
  var quads = PLANS.map(function (p) { var el = document.createElement('span'); el.className = 'wh3d2-q'; el.textContent = NAMES[p]; el.style.setProperty('--c', CURV[p]); stage.appendChild(el); return el; });
  function resize() { var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; wide = W >= 560; if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false); }
  function aim(w, h) { camera.aspect = w / h; var dist = Math.max(45, (S.all ? 21 : 38) / (Math.tan(15 * Math.PI / 180) * Math.min(1.6, w / h))); camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix(); }
  function render() {
    live();
    if (!ok) return;
    var pulse = 0.55 + 0.45 * Math.sin(clock * 6);
    pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -3.5, 0); pivot.updateMatrixWorld(true);
    renderer.setScissorTest(false); renderer.setViewport(0, 0, W, H); renderer.clear();
    if (!S.all) { paint(S.p, week, pulse); aim(W, H); renderer.render(scene, camera); quads.forEach(function (q) { q.style.display = 'none'; }); placeTag(W, H); }
    else {
      renderer.setScissorTest(true); var cols = wide ? 3 : 1, rowsN = wide ? 1 : 3, vw = W / cols, vh = H / rowsN;
      PLANS.forEach(function (p, i) {
        var x = wide ? i * vw : 0, yTop = wide ? 0 : i * vh, y = H - yTop - vh;
        paint(p, week, pulse); renderer.setViewport(x, y, vw, vh); renderer.setScissor(x, y, vw, vh); aim(vw, vh); renderer.render(scene, camera);
        var q = quads[i]; q.style.display = ''; q.style.transform = 'translate(' + (x + 10) + 'px,' + (yTop + 34) + 'px)';
      });
      renderer.setScissorTest(false); tag.classList.remove('is-on');
    }
    stage.classList.toggle('is-tri', S.all); stage.classList.toggle('is-tri-v', S.all && !wide);
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawU, pitch: pitchU }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) { if (!drag) return; yawU = Math.max(-1.2, Math.min(1.8, drag.yaw + (e.clientX - drag.x) * 0.008)); pitchU = Math.max(0.15, Math.min(1.3, drag.pitch + (e.clientY - drag.y) * 0.005)); idle = 0; if (!running) { yaw = yawU; pitch = pitchU; render(); } });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);
  fig.querySelectorAll('[data-s]').forEach(function (b) { b.addEventListener('click', function () { var v = b.getAttribute('data-s'); if (v === 'all') S.all = true; else { S.all = false; S.p = v; } pickTag(); ui(); if (!running) render(); }); });

  var last = 0, visible = true, hold = 0, PER_WEEK = 0.85;
  function frame(ts) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (ts - last) / 1000 || 0)); last = ts; clock += dt; idle += dt;
    if (hold > 0) { hold -= dt; if (hold <= 0) { week = 0; wf = 0; pickTag(); } }
    else { wf += dt / PER_WEEK; if (wf >= 1) { wf = 0; week++; if (week >= WK) { week = WK; hold = 3; } } }
    tagT += dt; if (tagT > 2.6) { tagT = 0; pickTag(); }
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.1 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(); requestAnimationFrame(frame);
  }
  function setRun(v) { if (reduce) return; if (v && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); } else if (!v) running = false; }
  if (ok) { build(); renderer.autoClear = false; stage.classList.add('is-live'); }
  resize(); pickTag(); ui(); render();
  window.addEventListener('resize', function () { resize(); if (!running) render(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
