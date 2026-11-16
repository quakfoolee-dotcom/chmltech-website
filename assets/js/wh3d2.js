/* Warehouse operations series, Part 2: pickers walking their trips in the Part 1 warehouse (needs three.js r128+
   as window.THREE). Data (#wh3d2-data) come from content/articles/wh2_model.py: the building and racks, the pallets in
   the as-is layout (0) and after Part 1's fixes (4), example trips for each layout, route and method, and the
   picker-hour grid behind the numbers. "Compare all" draws the four methods side by side in one canvas. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d2');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d2-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BAYS = D.bays, BW = D.bayW, X0 = D.x0, PB = D.perBay, ROWS = D.rows, LV = D.levels, BEAM = D.beam;
  var METHODS = ['single', 'batch', 'zone', 'wave'], NAMES = { single: 'Single-order', batch: 'Batch', zone: 'Zone', wave: 'Wave' };
  var HEX = { single: 0xF2F6FB, batch: 0x3FA7F5, zone: 0x8DC63F, wave: 0xFF8A3D }, CSSC = { single: '#9AA8BA', batch: '#3FA7F5', zone: '#8DC63F', wave: '#FF8A3D' };
  var S = { m: 'single', all: false, st: 0, r: 'return', vol: 300 };
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }

  /* ----- numbers ----- */
  function route(m) { return m === 'zone' || m === 'wave' ? 'return' : S.r; }
  function row(m) { var g = D.grid[S.st + m + route(m)[0]], i = D.vols.indexOf(S.vol); var x = g[i]; return { m: x[0], lph: x[1], h: x[2] / 3600, w: x[3] }; }
  var SAYS = {
    single: 'Single-order: one picker walks the whole route for every order, so picker-hours rise in step with the orders.',
    batch: 'Batch: one trip picks eight orders into a cart of totes, so the walk is shared by eight orders.',
    zone: 'Zone: one picker per aisle picks only that aisle\'s lines, and the totes meet at packing.',
    wave: 'Wave: orders are released three times a day for the carrier pickups, and each zone picker sweeps the aisle once per wave.'
  };
  function ui() {
    var x = row(S.m), lines = Math.round(S.vol * 3);
    $('wh3d2-m').textContent = fmt(x.m) + ' m'; $('wh3d2-lph').textContent = fmt(x.lph); $('wh3d2-h').textContent = x.h.toFixed(1);
    $('wh3d2-n').textContent = Math.ceil(x.h / D.shift - 1e-9); $('wh3d2-w').textContent = Math.round(x.w * 100) + '%';
    $('wh3d2-l').textContent = fmt(x.lph * x.h); $('wh3d2-vol-o').textContent = S.vol;
    $('wh3d2-chip').textContent = S.all ? 'Compare all' : NAMES[S.m];
    var lay = S.st ? 'after Part 1\'s fixes' : 'as-is', inLay = S.st ? 'in the layout after Part 1\'s fixes' : 'in the as-is layout';
    $('wh3d2-say').textContent = (S.all ? 'All four methods, ' + lay + ', ' + S.vol + ' orders a day. ' : SAYS[S.m] + ' ') +
      (S.all ? 'Batch, zone and wave share each walk between several orders.' : 'At ' + S.vol + ' orders a day ' + inLay + ': ' + fmt(x.m) + ' m of walking an order, ' + x.h.toFixed(1) + ' picker-hours.');
    /* comparison bars */
    var mx = 0, rows = METHODS.map(function (m) { var r = row(m); mx = Math.max(mx, r.h); return [m, r]; }), h = '';
    rows.forEach(function (q) {
      var on = S.all || q[0] === S.m;
      h += '<div class="b' + (on ? ' on' : '') + '"><span class="n">' + NAMES[q[0]] + '</span><span class="t"><i style="width:' + (q[1].h / mx * 100).toFixed(1) + '%;background:' + CSSC[q[0]] + '"></i></span><span class="v">' + q[1].h.toFixed(1) + ' h</span></div>';
    });
    $('wh3d2-bars').innerHTML = '<p class="cap">Picker-hours a day</p>' + h;
    fig.querySelectorAll('[data-m]').forEach(function (b) { b.setAttribute('aria-pressed', (b.getAttribute('data-m') === 'all' ? S.all : !S.all && b.getAttribute('data-m') === S.m) ? 'true' : 'false'); });
    fig.querySelectorAll('[data-l]').forEach(function (b) { b.setAttribute('aria-pressed', +b.getAttribute('data-l') === S.st ? 'true' : 'false'); });
    var rOff = !S.all && (S.m === 'zone' || S.m === 'wave');
    fig.querySelectorAll('[data-r]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-r') === S.r ? 'true' : 'false'); b.classList.toggle('is-off', rOff); });
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d2-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  var CX = D.bld[0] / 2 + 2, CZ = D.bld[1] / 2;
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  var beams = [], loads, bases, dotTex;
  function where(ix, st) {
    var lv = LV[st === 0 ? 0 : 1], nl = lv.length, k = ix % nl, t = (ix - k) / nl, s = t % PB, t2 = (t - s) / PB, b = t2 % BAYS, r = (t2 - b) / BAYS;
    return [X0 + b * BW + (s + 0.5) * BW / PB, lv[k] + (k ? BEAM : 0) + 0.02, ROWS[r]];
  }
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 600);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.7); key.position.set(-30, 60, 40); scene.add(key);
    pivot = new T.Group(); scene.add(pivot); model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var BX = D.bld[0], BZ = D.bld[1], H = D.bld[2], i;
    function box(w, h, d, x, y, z, m) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y + h / 2, z); model.add(b); return b; }
    box(BX, 0.2, BZ, BX / 2, -0.2, BZ / 2, mat(0x33435c));
    var wall = mat(0x4b5b74, { op: 0.55 });
    box(BX, 1.2, 0.25, BX / 2, 0, 0, wall); box(0.25, 1.2, BZ, 0, 0, BZ / 2, wall); box(0.25, 1.2, BZ, BX, 0, BZ / 2, wall); box(BX, 1.2, 0.25, BX / 2, 0, BZ, wall);
    var edge = new T.LineBasicMaterial({ color: 0x7f93b2, transparent: true, opacity: 0.4 });
    model.add(new T.Line(new T.BufferGeometry().setFromPoints([[0, 0], [BX, 0], [BX, BZ], [0, BZ], [0, 0]].map(function (p) { return new T.Vector3(p[0], H, p[1]); })), edge));
    for (i = 0; i < 6; i++) box(0.3, 3.2, 3.0, -0.05, 0, 6 + i * 4.2, mat(0x8dc63f));
    var lane = mat(0xF2C94C, { op: 0.3 }); for (i = 0; i < 6; i++) box(9, 0.03, 2.6, 6.5, 0.01, 6 + i * 4.2, lane);
    var shelf = mat(0x6f86a8); for (i = 0; i < 7; i++) box(40, 2.4, 1.0, 44, 0, 35.5 + i * 2.3, shelf);
    var pack = mat(0xA7B6CC); for (i = 0; i < 4; i++) box(2.4, 0.95, 1.2, 6 + i * 3.2, 0, 44, pack);
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3), ROWS.length * (BAYS + 1) * 2), m4 = new T.Matrix4(), q = new T.Quaternion(), sc = new T.Vector3(), ps = new T.Vector3(), n = 0, r, b, k;
    var topH = LV[1][LV[1].length - 1] + 0.2;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b <= BAYS; b++) for (k = -1; k <= 1; k += 2) { ps.set(X0 + b * BW, topH / 2, ROWS[r] + k * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4); }
    model.add(up);
    LV.forEach(function (lv) {
      var im = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), mat(0xE8862A), ROWS.length * BAYS * (lv.length - 1) * 2), j = 0;
      for (r = 0; r < ROWS.length; r++) for (b = 0; b < BAYS; b++) for (k = 1; k < lv.length; k++) for (var f = -1; f <= 1; f += 2) { ps.set(X0 + (b + 0.5) * BW, lv[k] + BEAM / 2, ROWS[r] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); im.setMatrixAt(j++, m4); }
      model.add(im); beams.push(im);
    });
    loads = new T.InstancedMesh(new T.BoxGeometry(1, 1, 1), new T.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.55 }), D.p.length);
    bases = new T.InstancedMesh(new T.BoxGeometry(1, 1, 1), new T.MeshLambertMaterial({ color: 0x8A6A3A }), D.p.length);
    model.add(loads); model.add(bases);
    var c2 = document.createElement('canvas'); c2.width = c2.height = 64; var x2 = c2.getContext('2d'), gr = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,.7)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x2.fillStyle = gr; x2.fillRect(0, 0, 64, 64);
    dotTex = new T.CanvasTexture(c2);
  }
  var PCOL = { A: 0x8C7A6E, B: 0x6E7C8E, C: 0x657083, D: 0x6E6680 };   /* muted, so the trips stand out */
  function layPallets() {
    var m4 = new T.Matrix4(), q = new T.Quaternion(), vs = new T.Vector3(), vp = new T.Vector3(), c = new T.Color();
    D.p.forEach(function (p, i) {
      var ix = S.st === 0 ? p[2] : p[3], h = S.st === 0 ? p[1] : p[4];
      if (ix < 0) { vs.set(0.001, 0.001, 0.001); vp.set(0, -60, 0); m4.compose(vp, q, vs); loads.setMatrixAt(i, m4); bases.setMatrixAt(i, m4); return; }
      var w = where(ix, S.st);
      vs.set(0.98, Math.max(0.01, h - 0.14), 1.18); vp.set(w[0], w[1] + 0.14 + (h - 0.14) / 2, w[2]); m4.compose(vp, q, vs); loads.setMatrixAt(i, m4);
      vs.set(1, 0.14, 1.2); vp.set(w[0], w[1] + 0.07, w[2]); m4.compose(vp, q, vs); bases.setMatrixAt(i, m4);
      loads.setColorAt(i, c.setHex(PCOL[p[0]]));
    });
    loads.instanceMatrix.needsUpdate = true; bases.instanceMatrix.needsUpdate = true; if (loads.instanceColor) loads.instanceColor.needsUpdate = true;
    beams[0].visible = S.st === 0; beams[1].visible = S.st !== 0;
  }

  /* ----- trips: a picker per trip, a faint full trail, a bright trail up to the picker, and the picks ----- */
  var groups = {}, trips = [];
  function densify(path) {
    var out = [], i, j;
    for (i = 0; i < path.length - 1; i++) {
      var a = path[i], b = path[i + 1], L = Math.abs(b[0] - a[0]) + Math.abs(b[1] - a[1]), n = Math.max(1, Math.ceil(L / 0.6));
      for (j = 0; j < n; j++) out.push([a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n]);
    }
    out.push(path[path.length - 1]); return out;
  }
  function ribbon(pts, w, y) {    /* a flat strip on the floor along the trail; 6 indices a segment, for drawRange */
    var n = pts.length, pos = new Float32Array(n * 6), idx = [], i;
    for (i = 0; i < n; i++) {
      var a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dz = b[1] - a[1], L = Math.hypot(dx, dz) || 1, nx = -dz / L * w / 2, nz = dx / L * w / 2;
      pos[i * 6] = pts[i][0] + nx; pos[i * 6 + 1] = y; pos[i * 6 + 2] = pts[i][1] + nz; pos[i * 6 + 3] = pts[i][0] - nx; pos[i * 6 + 4] = y; pos[i * 6 + 5] = pts[i][1] - nz;
    }
    for (i = 0; i < n - 1; i++) { var k = i * 2; idx.push(k, k + 1, k + 2, k + 1, k + 3, k + 2); }
    var g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setIndex(idx); return g;
  }
  function makeTrips() {
    METHODS.forEach(function (m) { if (groups[m]) { model.remove(groups[m]); groups[m].traverse(function (o) { if (o.geometry) o.geometry.dispose(); }); } });
    trips = [];
    var ex = D.ex[S.st + S.r[0]];
    METHODS.forEach(function (m, mi) {
      var g = new T.Group(); groups[m] = g; model.add(g);
      ex[m].forEach(function (tp, ti) {
        var pts = densify(tp[0]), cum = [0], i;
        for (i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.abs(pts[i][0] - pts[i - 1][0]) + Math.abs(pts[i][1] - pts[i - 1][1]));
        var lift = 0.06 + ti * 0.02;
        var full = new T.Mesh(ribbon(pts, 0.7, lift), new T.MeshBasicMaterial({ color: HEX[m], transparent: true, opacity: 0.3, depthWrite: false, depthTest: false, side: T.DoubleSide })); full.renderOrder = 10; g.add(full);
        var prog = new T.Mesh(ribbon(pts, 0.7, lift + 0.01), new T.MeshBasicMaterial({ color: HEX[m], transparent: true, opacity: 0.95, depthTest: false, side: T.DoubleSide })); prog.renderOrder = 11; prog.geometry.setDrawRange(0, 0); g.add(prog);
        var beacon = new T.Mesh(new T.CylinderGeometry(0.06, 0.06, 7, 6), new T.MeshBasicMaterial({ color: HEX[m], transparent: true, opacity: 0.8, depthWrite: false, depthTest: false })); beacon.renderOrder = 12;
        /* picks: where along the trail each one is reached */
        var stops = tp[1].map(function (s) {
          var best = 0, bd = 1e9; for (var k = 0; k < pts.length; k++) { var d = Math.abs(pts[k][0] - s[0]) + Math.abs(pts[k][1] - s[1]); if (d < bd - 1e-6) { bd = d; best = k; } }
          return { at: cum[best], x: s[0], z: s[1] };
        }).sort(function (a, b) { return a.at - b.at; });
        var pg = new T.BufferGeometry(), pp = new Float32Array(stops.length * 3), pc = new Float32Array(stops.length * 3);
        stops.forEach(function (s, k) { pp[k * 3] = s.x; pp[k * 3 + 1] = 0.6; pp[k * 3 + 2] = s.z; });
        pg.setAttribute('position', new T.BufferAttribute(pp, 3)); pg.setAttribute('color', new T.BufferAttribute(pc, 3));
        var dots = new T.Points(pg, new T.PointsMaterial({ size: 2.6, map: dotTex, transparent: true, depthWrite: false, vertexColors: true, blending: T.AdditiveBlending, depthTest: false })); dots.renderOrder = 13; g.add(dots);
        var body = new T.Group(), bm = new T.MeshLambertMaterial({ color: HEX[m] });
        var cyl = new T.Mesh(new T.CylinderGeometry(0.32, 0.32, 1.2, 12), bm); cyl.position.y = 0.6; body.add(cyl);
        var head = new T.Mesh(new T.SphereGeometry(0.28, 12, 10), new T.MeshLambertMaterial({ color: 0xF2D1B3 })); head.position.y = 1.5; body.add(head);
        var cart = new T.Mesh(new T.BoxGeometry(0.9, 0.7, 0.6), new T.MeshLambertMaterial({ color: 0xDCE4EE })); cart.position.set(0.8, 0.45, 0); body.add(cart);
        beacon.position.y = 5.6; body.add(beacon); body.scale.setScalar(1.6); g.add(body);
        trips.push({ m: m, pts: pts, cum: cum, len: cum[cum.length - 1], prog: prog, dots: dots, stops: stops, body: body, t: -ti * 2.2 - mi * 0.3, u: 0, pause: 0, next: 0 });
      });
    });
  }
  var VS = 9;   /* metres a second on screen */
  function stepTrips(dt) {
    trips.forEach(function (tr) {
      tr.t += dt; if (tr.t < 0) { tr.body.visible = false; tr.prog.geometry.setDrawRange(0, 0); return; }
      tr.body.visible = true;
      if (tr.pause > 0) tr.pause -= dt;
      else {
        tr.u += VS * dt;
        if (tr.next < tr.stops.length && tr.u >= tr.stops[tr.next].at) { tr.u = tr.stops[tr.next].at; tr.pause = 0.28; tr.next++; }
        if (tr.u >= tr.len) { tr.u = tr.len; if (tr.t > tr.len / VS + tr.stops.length * 0.28 + 1.4) { tr.t = 0; tr.u = 0; tr.next = 0; } }
      }
      var lo = 0, hi = tr.cum.length - 1, mid; while (hi - lo > 1) { mid = (lo + hi) >> 1; if (tr.cum[mid] <= tr.u) lo = mid; else hi = mid; }
      var f = (tr.u - tr.cum[lo]) / Math.max(1e-6, tr.cum[hi] - tr.cum[lo]), a = tr.pts[lo], b = tr.pts[hi];
      var x = a[0] + (b[0] - a[0]) * f, z = a[1] + (b[1] - a[1]) * f;
      tr.body.position.set(x, 0, z);
      if (Math.abs(b[0] - a[0]) + Math.abs(b[1] - a[1]) > 0.01) tr.body.rotation.y = Math.atan2(-(b[1] - a[1]), b[0] - a[0]);
      tr.prog.geometry.setDrawRange(0, lo * 6);
      var col = tr.dots.geometry.attributes.color;
      for (var k = 0; k < tr.stops.length; k++) { var on = k < tr.next ? 1 : 0.28; col.setXYZ(k, on, on * 0.89, on * 0.48); }
      col.needsUpdate = true;
    });
  }

  /* ----- view: one scene, or four viewports for Compare all ----- */
  var yawU = 1.2, pitchU = 1.0, yaw = yawU, pitch = pitchU, idle = 99, clock = 0, W = 0, H = 0, wide = true;
  var quads = METHODS.map(function (m) { var el = document.createElement('span'); el.className = 'wh3d2-q'; el.textContent = NAMES[m]; el.style.setProperty('--c', CSSC[m]); stage.appendChild(el); return el; });
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; wide = W >= 560;
    if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
  }
  function aim(w, h) {
    camera.aspect = w / h; var dist = Math.max(70, (wide || S.all ? 40 : 31) / (Math.tan(15 * Math.PI / 180) * Math.min(1.5, w / h)));
    camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix();
  }
  function render() {
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -4, 0); pivot.updateMatrixWorld(true);
    renderer.setScissorTest(false); renderer.setViewport(0, 0, W, H); renderer.clear();
    if (!S.all) {
      METHODS.forEach(function (m) { groups[m].visible = m === S.m; }); aim(W, H); renderer.render(scene, camera);
      quads.forEach(function (q) { q.style.display = 'none'; });
    } else {
      renderer.setScissorTest(true); var hw = W / 2, hh = H / 2;
      METHODS.forEach(function (m, i) {
        var x = (i % 2) * hw, y = i < 2 ? hh : 0;
        METHODS.forEach(function (n) { groups[n].visible = n === m; });
        renderer.setViewport(x, y, hw, hh); renderer.setScissor(x, y, hw, hh); aim(hw, hh); renderer.render(scene, camera);
        var q = quads[i]; q.style.display = ''; q.style.transform = 'translate(' + (x + 10) + 'px,' + ((i < 2 ? 0 : hh) + 34) + 'px)';
      });
      renderer.setScissorTest(false);
    }
    stage.classList.toggle('is-quad', S.all);
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawU, pitch: pitchU }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawU = Math.max(-0.9, Math.min(2.6, drag.yaw + (e.clientX - drag.x) * 0.008)); pitchU = Math.max(0.18, Math.min(1.3, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawU; pitch = pitchU; render(); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  /* ----- controls ----- */
  function rebuild() { if (ok) { layPallets(); makeTrips(); if (reduce) stepTrips(60); } }
  fig.querySelectorAll('[data-m]').forEach(function (b) { b.addEventListener('click', function () { var m = b.getAttribute('data-m'); if (m === 'all') S.all = true; else { S.all = false; S.m = m; } ui(); if (!running) render(); }); });
  fig.querySelectorAll('[data-l]').forEach(function (b) { b.addEventListener('click', function () { S.st = +b.getAttribute('data-l'); rebuild(); ui(); if (!running) render(); }); });
  fig.querySelectorAll('[data-r]').forEach(function (b) { b.addEventListener('click', function () { if (b.classList.contains('is-off')) return; S.r = b.getAttribute('data-r'); rebuild(); ui(); if (!running) render(); }); });
  $('wh3d2-vol').addEventListener('input', function () { S.vol = +this.value; ui(); });

  var last = 0, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (t - last) / 1000 || 0)); last = t; clock += dt; idle += dt;
    stepTrips(dt);
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.1 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(); requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if (ok) { build(); renderer.autoClear = false; stage.classList.add('is-live'); }
  resize(); rebuild(); ui(); render();
  window.addEventListener('resize', function () { resize(); if (!running) render(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
