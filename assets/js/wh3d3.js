/* Warehouse operations series, Part 3: one simulated receiving day replayed in 3D (needs three.js r128+ as window.THREE).
   Data (#wh3d3-data) come from content/articles/wh3_model.py: for each of the 16 combinations of the four fixes, the
   trucks (arrive, dock, leave, door, pallets), every pallet (unloaded, leaves staging, put away, cross-dock, staging
   spot, rack position, door) and the staging curve, plus the averaged numbers. Everything drawn is a function of the
   clock, so switching a fix changes the scene at once. 06:00 to 21:00 plays in about 75 seconds and loops. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d3');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d3-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var BAYS = D.bays, BW = D.bayW, X0 = D.x0, PB = D.perBay, ROWS = D.rows, LV = D.levels, BEAM = D.beam, AIS = D.aisles;
  var FIXES = ['appt', 'scan', 'xdock', 'fork'], on = { appt: false, scan: false, xdock: false, fork: false };
  var TEND = 900, SPEED = 12, t = reduce ? 240 : 0;          /* minutes after 06:00; minutes a second */
  var DOORZ = function (d) { return 6 + d * 4.2; };
  function key() { var m = 0; FIXES.forEach(function (f, i) { if (on[f]) m |= 1 << i; }); return m; }
  function S() { return D.sc[key()]; }
  function hm(m) { var x = D.day0 + m; return ('0' + Math.floor(x / 60)).slice(-2) + ':' + ('0' + Math.floor(x % 60)).slice(-2); }
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }

  /* ----- places ----- */
  function rackPos(ix) {
    var nl = LV.length, k = ix % nl, q = (ix - k) / nl, s = q % PB, q2 = (q - s) / PB, b = q2 % BAYS, r = (q2 - b) / BAYS;
    var z = ROWS[r], a = AIS.reduce(function (best, az) { return Math.abs(az - z) < Math.abs(best - z) ? az : best; }, AIS[0]);
    return { x: X0 + b * BW + (s + 0.5) * BW / PB, y: LV[k] + (k ? BEAM : 0) + 0.02, z: z, az: a };
  }
  function spotPos(s) {
    if (s < D.cap) { var L = Math.floor(s / D.depth), k = s % D.depth, half = D.depth / 2; return { x: 2.6 + (k % half) * 1.45, y: 0.02, z: DOORZ(L) - 0.62 + Math.floor(k / half) * 1.24, over: false }; }
    var o = s - D.cap; return { x: 2.4 + (o % 8) * 1.4, y: 0.02, z: 31.2 + Math.floor(o / 8) * 1.3, over: true };
  }
  function outPos(n) { var L = 4 + Math.floor((n % 24) / 12), k = n % 12, lay = Math.floor(n / 24); return { x: 2.6 + (k % 6) * 1.45, y: 0.02 + lay * 1.25, z: DOORZ(L) - 0.62 + Math.floor(k / 6) * 1.24 }; }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d3-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  var CX = -14, CZ = 30;
  var DOCK_X = -0.4, LANE_X = -20, STALL_X = -38, STALL_Z0 = 32, STALL_W = 3.6, STALLS = 10;
  function smooth(u) { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); }
  var stallCache = {};
  function stallsFor(k) {
    /* Stalls: lowest free stall at arrival, held until the truck has pulled out of it (one column; extra stalls
       continue north, never in another truck's path). Lane: the yard lane takes one truck at a time, so each move
       onto a door (5 min) and each departure across the lane (first 2.2 min of leaving) is queued in time order;
       a truck may reach its door or leave a few minutes later than in the simulation, never through another truck. */
    if (stallCache[k]) return stallCache[k];
    var TR = D.sc[k].tr, held = [], out = [], order = TR.map(function (tr, j) { return j; }).sort(function (a, b) { return TR[a][0] - TR[b][0]; });
    order.forEach(function (j) { out[j] = { sx: STALL_X, sz: 0, v1: TR[j][1], v2: TR[j][2] }; });
    var ev = [];
    TR.forEach(function (tr, j) { ev.push([tr[1], 1, j]); ev.push([tr[2], 0, j]); });
    ev.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });   /* a departure before an arrival at the same minute */
    var laneFree = -1e9, doorFree = {};
    ev.forEach(function (e) {
      var j = e[2], o = out[j], d = TR[j][3];
      if (e[1] === 1) { var v = Math.max(e[0], laneFree, doorFree[d] || -1e9); o.v1 = v; laneFree = v + 5; }
      else { var w = Math.max(e[0], laneFree, o.v1 + 5.5); o.v2 = w; laneFree = w + 2.2; doorFree[d] = w + 1.2; }
    });
    order.forEach(function (j) {
      var tr = TR[j], s = 0;
      while (held[s] != null && held[s] > tr[0] - 7) s++;
      held[s] = out[j].v1 + 1.5; out[j].sz = STALL_Z0 + s * STALL_W;
    });
    return (stallCache[k] = out);
  }
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  var loads, bases, trucks = [], lifts = [], MAXP = 0, MAXT = 0;
  Object.keys(D.sc).forEach(function (k) { MAXP = Math.max(MAXP, D.sc[k].p.length); MAXT = Math.max(MAXT, D.sc[k].tr.length); });
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 700);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var keyL = new T.DirectionalLight(0xffffff, 0.7); keyL.position.set(-30, 60, 40); scene.add(keyL);
    pivot = new T.Group(); scene.add(pivot); model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var BX = D.bld[0], BZ = D.bld[1], i, r, b, k;
    function box(w, h, d, x, y, z, m) { var o = new T.Mesh(new T.BoxGeometry(w, h, d), m); o.position.set(x, y + h / 2, z); model.add(o); return o; }
    box(BX, 0.2, BZ, BX / 2, -0.2, BZ / 2, mat(0x33435c));
    box(72, 0.1, 88, -36, -0.15, 34, mat(0x2a3446));                          /* yard */
    for (i = 0; i <= STALLS; i++) {                                              /* waiting stalls, north of the dock doors */
      box(18, 0.02, 0.15, STALL_X - 8, -0.08, STALL_Z0 - STALL_W / 2 + i * STALL_W, mat(0xF2C94C, { op: 0.5 }));
    }
    box(0.15, 0.02, 80, LANE_X + 1.6, -0.08, 34, mat(0xffffff, { op: 0.25 }));      /* lane line */
    var wall = mat(0x4b5b74, { op: 0.55 });
    box(BX, 1.2, 0.25, BX / 2, 0, 0, wall); box(0.25, 1.2, BZ, BX, 0, BZ / 2, wall); box(BX, 1.2, 0.25, BX / 2, 0, BZ, wall);
    for (i = 0; i < 6; i++) {                                                   /* dock wall pieces between the doors, and the doors */
      box(0.3, 3.2, 3.0, -0.05, 0, DOORZ(i), mat(i < 3 ? 0x8dc63f : 0xFF8A3D));
    }
    box(0.25, 1.2, BZ - 29, 0, 0, 29 + (BZ - 29) / 2, wall);
    for (i = 0; i < 6; i++) box(9.2, 0.03, 2.8, 6.5, 0.01, DOORZ(i), mat(i < 4 ? 0xF2C94C : 0xFF8A3D, { op: 0.28 }));
    box(11.5, 0.03, 7.0, 7.4, 0.01, 34.4, mat(0xFF7A5C, { op: 0.12 }));
    var shelf = mat(0x6f86a8); for (i = 0; i < 7; i++) box(40, 2.4, 1.0, 44, 0, 35.5 + i * 2.3, shelf);
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3), ROWS.length * (BAYS + 1) * 2), m4 = new T.Matrix4(), q = new T.Quaternion(), sc = new T.Vector3(), ps = new T.Vector3(), n = 0;
    var topH = LV[LV.length - 1] + 0.2;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b <= BAYS; b++) for (k = -1; k <= 1; k += 2) { ps.set(X0 + b * BW, topH / 2, ROWS[r] + k * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4); }
    model.add(up);
    var bm = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), mat(0xE8862A), ROWS.length * BAYS * (LV.length - 1) * 2); n = 0;
    for (r = 0; r < ROWS.length; r++) for (b = 0; b < BAYS; b++) for (k = 1; k < LV.length; k++) for (var f = -1; f <= 1; f += 2) { ps.set(X0 + (b + 0.5) * BW, LV[k] + BEAM / 2, ROWS[r] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); bm.setMatrixAt(n++, m4); }
    model.add(bm);
    /* stock already in the racks (Part 1 layout), muted */
    var rk = new T.InstancedMesh(new T.BoxGeometry(1, 1, 1), new T.MeshLambertMaterial({ color: 0x6E7C8E, transparent: true, opacity: 0.6 }), D.rack.length);
    D.rack.forEach(function (p, j) { var w = rackPos(p[2]); sc.set(0.98, p[1], 1.18); ps.set(w.x, w.y + p[1] / 2, w.z); m4.compose(ps, q, sc); rk.setMatrixAt(j, m4); });
    model.add(rk);
    /* the day's pallets and trucks */
    loads = new T.InstancedMesh(new T.BoxGeometry(0.98, 1.15, 1.18), new T.MeshLambertMaterial({ color: 0xffffff }), MAXP);
    bases = new T.InstancedMesh(new T.BoxGeometry(1, 0.14, 1.2), new T.MeshLambertMaterial({ color: 0x8A6A3A }), MAXP);
    loads.instanceMatrix.setUsage(T.DynamicDrawUsage); bases.instanceMatrix.setUsage(T.DynamicDrawUsage);
    var c = new T.Color(0xffffff); for (i = 0; i < MAXP; i++) loads.setColorAt(i, c);
    model.add(loads); model.add(bases);
    /* trucks: the rear of the trailer is the group's origin (it backs onto the door); the tractor faces away, toward -x */
    var tyreG = new T.CylinderGeometry(0.48, 0.48, 0.32, 16), tyreM = new T.MeshLambertMaterial({ color: 0x1b1f26 }), hubM = new T.MeshLambertMaterial({ color: 0x9aa4b2 });
    var hubG = new T.CylinderGeometry(0.22, 0.22, 0.34, 10), chassisM = new T.MeshLambertMaterial({ color: 0x2a2f38 });
    function wheel(g, x, z) {
      var w = new T.Mesh(tyreG, tyreM); w.rotation.x = Math.PI / 2; w.position.set(x, 0.48, z); g.add(w);
      var h = new T.Mesh(hubG, hubM); h.rotation.x = Math.PI / 2; h.position.set(x, 0.48, z); g.add(h);
    }
    for (i = 0; i < MAXT; i++) {
      var g = new T.Group(), tm = new T.MeshLambertMaterial({ color: 0xDCE4EE }), cm = new T.MeshLambertMaterial({ color: 0x2f6db5 });
      var tl = new T.Mesh(new T.BoxGeometry(12, 2.9, 2.5), tm); tl.position.set(-6, 2.55, 0); g.add(tl);            /* trailer box, floor at 1.1 m */
      var ch = new T.Mesh(new T.BoxGeometry(5.2, 0.35, 1.6), chassisM); ch.position.set(-14.1, 0.85, 0); g.add(ch);  /* tractor frame */
      var cab = new T.Mesh(new T.BoxGeometry(2.3, 2.5, 2.4), cm); cab.position.set(-15.2, 2.25, 0); g.add(cab);
      var win = new T.Mesh(new T.BoxGeometry(0.05, 0.9, 2.0), new T.MeshLambertMaterial({ color: 0x9fd0ff })); win.position.set(-16.37, 2.8, 0); g.add(win);
      [-1.2, -2.5, -12.9, -14.2, -15.9].forEach(function (x) { wheel(g, x, 1.08); wheel(g, x, -1.08); });             /* trailer tandem, drive tandem, steer axle */
      g.visible = false; model.add(g); trucks.push(g);
    }
    for (i = 0; i < 4; i++) {
      var fl = new T.Group(), ym = new T.MeshLambertMaterial({ color: 0xF2C94C });
      var fb = new T.Mesh(new T.BoxGeometry(1.4, 1.1, 1.1), ym); fb.position.set(-0.9, 0.55, 0); fl.add(fb);
      var mast = new T.Mesh(new T.BoxGeometry(0.12, 2.2, 0.9), new T.MeshLambertMaterial({ color: 0x333a44 })); mast.position.set(-0.15, 1.1, 0); fl.add(mast);
      fl.visible = false; model.add(fl); lifts.push(fl);
    }
  }

  /* ----- the scene at time t ----- */
  var m4b = ok ? new T.Matrix4() : null, qb = ok ? new T.Quaternion() : null, vs = ok ? new T.Vector3() : null, vp = ok ? new T.Vector3() : null, col = ok ? new T.Color() : null;
  var C_REC = 0xE3C58E, C_OVER = 0xFF7A5C, C_XD = 0xFF8A3D, C_PUT = 0xD9B98A;
  function lerp(a, b, u) { return a + (b - a) * u; }
  function place() {
    var sc = S(), P = sc.p, TR = sc.tr, i, n = 0, li = 0, xdN = 0;
    var xdOrder = []; P.forEach(function (p, j) { if (p[3]) xdOrder.push(j); }); xdOrder.sort(function (a, b) { return P[a][1] - P[b][1]; });
    var xdIx = {}; xdOrder.forEach(function (j, k) { xdIx[j] = k; });
    for (i = 0; i < MAXP; i++) {
      var p = P[i], show = false, x = 0, y = 0, z = 0, c = C_REC, carry = false;
      if (p && t >= p[0]) {
        var sp = spotPos(p[4]);
        if (p[3]) {                                               /* cross-dock: staging, then the outbound lanes until the trucks leave */
          var o = outPos(xdIx[i]), u = Math.min(1, Math.max(0, (t - p[1]) / 6));
          if (t < D.block[1]) { show = true; c = C_XD; x = lerp(sp.x, o.x, u); z = lerp(sp.z, o.z, u); y = lerp(sp.y, o.y, u) + Math.sin(Math.PI * u) * 0.6; }
        } else if (t < p[1]) { show = true; x = sp.x; y = sp.y; z = sp.z; c = sp.over ? C_OVER : C_REC; }
        else {
          var rp = rackPos(p[5]), w = (t - p[1]) / Math.max(0.1, p[2] - p[1]); show = true;
          if (w >= 1) { x = rp.x; y = rp.y; z = rp.z; c = C_PUT; }
          else {                                                  /* to the aisle mouth, along the aisle, then up into the rack */
            carry = true; var fx = X0 - 0.9;
            if (w < 0.35) { var a = w / 0.35; x = lerp(sp.x, fx, a); z = lerp(sp.z, rp.az, a); y = 0.35; }
            else if (w < 0.75) { var b = (w - 0.35) / 0.4; x = lerp(fx, rp.x, b); z = rp.az; y = 0.35; }
            else { var d = (w - 0.75) / 0.25; x = rp.x; z = lerp(rp.az, rp.z, d); y = lerp(0.35, rp.y, d); }
          }
        }
      }
      if (!show) { vs.set(0.001, 0.001, 0.001); vp.set(0, -60, 0); m4b.compose(vp, qb, vs); loads.setMatrixAt(i, m4b); bases.setMatrixAt(i, m4b); continue; }
      vs.set(1, 1, 1); vp.set(x, y + 0.14 + 0.575, z); m4b.compose(vp, qb, vs); loads.setMatrixAt(i, m4b);
      vp.set(x, y + 0.07, z); m4b.compose(vp, qb, vs); bases.setMatrixAt(i, m4b);
      loads.setColorAt(i, col.setHex(c));
      if (carry && li < lifts.length) { var L = lifts[li++]; L.visible = true; L.position.set(x, 0, z); }
      n++;
    }
    for (; li < lifts.length; li++) lifts[li].visible = false;
    loads.instanceMatrix.needsUpdate = true; bases.instanceMatrix.needsUpdate = true; loads.instanceColor.needsUpdate = true;
    /* trucks: each one follows fixed paths, so no two share space at the same time.
       arrive  arr-7 .. arr      drive in from the road along its own stall row to a waiting stall (north of the doors)
       wait    arr .. start      parked in the stall (a stall is kept until the truck leaves it)
       to door start .. start+5  pull forward into the yard lane, down the lane to its door's row, back onto the door
       unload  start+5 .. end    at the door
       leave   end .. end+4      straight out along its door row to the road, which no waiting stall crosses
       Moves through the yard lane are queued (stallsFor), so only one truck is in the lane at a time. */
    var waiting = [], stalls = stallsFor(key());
    for (i = 0; i < MAXT; i++) {
      var tr = TR[i], g = trucks[i];
      if (!tr) { g.visible = false; continue; }
      var st = stalls[i], v1 = st.v1, v2 = st.v2;
      if (t < tr[0] - 7 || t > v2 + 4) { g.visible = false; continue; }
      g.visible = true; var dz = DOORZ(tr[3]), sx = st.sx, sz = st.sz, x, z;
      if (t >= tr[0] && t < v1) waiting.push(i);
      if (t < tr[0]) { x = lerp(-70, sx, smooth((t - tr[0] + 7) / 7)); z = sz; }
      else if (t < v1) { x = sx; z = sz; }
      else if (t < v1 + 5) {
        var u = (t - v1) / 5;
        if (u < 0.25) { x = lerp(sx, LANE_X, smooth(u / 0.25)); z = sz; }
        else if (u < 0.6) { x = LANE_X; z = lerp(sz, dz, smooth((u - 0.25) / 0.35)); }
        else { x = lerp(LANE_X, DOCK_X, smooth((u - 0.6) / 0.4)); z = dz; }
      }
      else if (t < v2) { x = DOCK_X; z = dz; }
      else { x = lerp(DOCK_X, -70, smooth((t - v2) / 4)); z = dz; }
      g.position.set(x, 0, z);
    }
    return waiting.length;
  }

  /* ----- numbers, text and the staging chart ----- */
  function ui() {
    var s = S().s;
    $('wh3d3-wait').textContent = fmt(s[0]) + ' min'; $('wh3d3-o2').textContent = s[1].toFixed(1) + ' of ' + S().tr.length;
    $('wh3d3-det').textContent = '$' + fmt(s[2]); $('wh3d3-dts').textContent = s[3].toFixed(1) + ' h';
    $('wh3d3-peak').textContent = fmt(s[4]) + ' of ' + D.cap; $('wh3d3-last').textContent = hm(s[5]);
    $('wh3d3-peak').parentNode.classList.toggle('is-bad', s[4] > D.cap); $('wh3d3-wait').parentNode.classList.toggle('is-bad', s[0] > 30);
    fig.querySelectorAll('[data-f]').forEach(function (b) { b.setAttribute('aria-checked', on[b.getAttribute('data-f')] ? 'true' : 'false'); });
    var c = S().c, d = 'M0,110', ymax = 120, last = 0;
    c.forEach(function (q) { d += ' H' + (q[0] / TEND * 600).toFixed(1) + ' V' + (110 - q[1] / ymax * 110).toFixed(1); });
    d += ' H600 V110 Z'; $('wh3d3-curve').setAttribute('d', d);
    var cy = (110 - D.cap / ymax * 110).toFixed(1), cl = $('wh3d3-cap'); cl.setAttribute('x1', 0); cl.setAttribute('x2', 600); cl.setAttribute('y1', cy); cl.setAttribute('y2', cy);
  }
  var lastSay = '';
  function live(waiting) {
    var P = S().p, inStage = 0, over = 0, i;
    for (i = 0; i < P.length; i++) { var p = P[i]; if (t >= p[0] && t < p[1] && !p[3]) { inStage++; if (p[4] >= D.cap) over++; } }
    $('wh3d3-clock').textContent = hm(t); $('wh3d3-clock').classList.toggle('is-bad', over > 0 || waiting > 1);
    var nx = (t / TEND * 600).toFixed(1), nl = $('wh3d3-now'); nl.setAttribute('x1', nx); nl.setAttribute('x2', nx); nl.setAttribute('y1', 0); nl.setAttribute('y2', 110);
    var txt = hm(t) + ' · ' + (waiting ? waiting + ' truck' + (waiting > 1 ? 's' : '') + ' waiting in the yard · ' : 'no trucks waiting · ') + inStage + ' pallets in staging' + (over ? ', ' + over + ' of them parked in the aisle.' : '.');
    if (txt !== lastSay) { lastSay = txt; $('wh3d3-say').textContent = txt; }
  }

  /* ----- view ----- */
  var yawU = 0.5, pitchU = 0.86, yaw = yawU, pitch = pitchU, idle = 99, clock = 0, W = 0, H = 0, wide = true;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; wide = W >= 560;
    if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    camera.aspect = W / H; var dist = Math.max(70, (wide ? 58 : 46) / (Math.tan(15 * Math.PI / 180) * Math.min(1.5, W / H)));
    camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix();
  }
  function render() {
    var w = 0;
    if (ok) { pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -4, 0); w = place(); renderer.render(scene, camera); }
    else { var P = S().tr; P.forEach(function (tr) { if (t >= tr[0] && t < tr[1]) w++; }); }
    live(w);
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
  fig.querySelectorAll('[data-f]').forEach(function (b) { b.addEventListener('click', function () { var f = b.getAttribute('data-f'); on[f] = !on[f]; ui(); if (!running) render(); }); });

  var last = 0, visible = true, hold = 0;
  function frame(ts) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (ts - last) / 1000 || 0)); last = ts; clock += dt; idle += dt;
    if (hold > 0) { hold -= dt; if (hold <= 0) t = 0; } else { t += dt * SPEED; if (t >= TEND) { t = TEND; hold = 2.5; } }
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.1 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(); requestAnimationFrame(frame);
  }
  function setRun(v) {
    if (reduce) return;
    if (v && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!v) running = false;
  }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); ui(); render();
  window.addEventListener('resize', function () { resize(); if (!running) render(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
