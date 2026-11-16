/* Warehouse operations series, Part 5: the packing line, with the checkpoints of each step (needs three.js r128+ as
   window.THREE). Data (#wh3d5-data) come from content/articles/wh5_model.py: for each step, per error kind, the chance
   an order has that error, the share stopped by the pick scanner, and the shares caught at packing and at the scale;
   plus the model's yearly numbers. In the animation errors are made `mag` times as often as in the model so that they
   can be seen; every catch rate is the model's. Steps advance on their own until the reader picks one. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d5');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d5-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cur = 0, KINDS = ['item', 'qty', 'tote'];
  var tourOn = !reduce, tourT = 0, pauseT = 0, HOLD = 22;   /* seconds on each step in the tour */
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function money(n) { var r = Math.abs(n) < 10000 ? Math.round(n / 100) * 100 : Math.round(n / 1000) * 1000; return (r < 0 ? '-$' : '$') + Math.abs(r).toLocaleString('en-CA'); }

  /* line layout, metres along x */
  var X_START = -16, X_PICK = -12, X_PACK = -3, X_SCALE = 5, X_SHIP = 13, X_END = 14.5, Z_REPICK = -4.2, Z_RET = 3.4, SPEED = 3.2, Y = 0.82;

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d5-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op, emissive: o.em || 0x000000 }); }
  var gates = {}, pool = [], returnsPile = [];
  function box(w, h, d, x, y, z, m, parent) { var o = new T.Mesh(new T.BoxGeometry(w, h, d), m); o.position.set(x, y + h / 2, z); (parent || model).add(o); return o; }
  function conveyor(x0, x1, z, h, col) {
    var L = x1 - x0, g = new T.Group();
    box(L, 0.08, 1.0, (x0 + x1) / 2, h - 0.08, z, mat(col), g);
    box(L, 0.12, 0.06, (x0 + x1) / 2, h - 0.04, z - 0.53, mat(0x8a96a8), g); box(L, 0.12, 0.06, (x0 + x1) / 2, h - 0.04, z + 0.53, mat(0x8a96a8), g);
    for (var x = x0 + 0.5; x < x1; x += 3) { box(0.08, h - 0.08, 0.08, x, 0, z - 0.45, mat(0x5a6577), g); box(0.08, h - 0.08, 0.08, x, 0, z + 0.45, mat(0x5a6577), g); }
    var rg = new T.CylinderGeometry(0.05, 0.05, 0.98, 8), rm = mat(0x9aa4b2), n = Math.floor(L / 0.5), im = new T.InstancedMesh(rg, rm, n), m4 = new T.Matrix4(), q = new T.Quaternion().setFromEuler(new T.Euler(Math.PI / 2, 0, 0)), s1 = new T.Vector3(1, 1, 1), p = new T.Vector3();
    for (var i = 0; i < n; i++) { p.set(x0 + 0.25 + i * 0.5, h + 0.01, z); m4.compose(p, q, s1); im.setMatrixAt(i, m4); }
    g.add(im); model.add(g); return g;
  }
  function gate(x, label) {
    var g = new T.Group(), off = mat(0x4b5b74), on = mat(0x8dc63f, { em: 0x2a4410 }), hit = mat(0xc8ff8a, { em: 0x5a8f20 }), bad = mat(0xFF5A4A, { em: 0x6a1008 });
    var l = box(0.14, 2.4, 0.14, x, 0, -0.75, off, g), r = box(0.14, 2.4, 0.14, x, 0, 0.75, off, g), t = box(0.14, 0.14, 1.64, x, 2.3, 0, off, g);
    var beam = new T.Mesh(new T.PlaneGeometry(1.5, 1.4), new T.MeshBasicMaterial({ color: 0x8dc63f, transparent: true, opacity: 0, side: T.DoubleSide, depthWrite: false }));
    beam.rotation.y = Math.PI / 2; beam.position.set(x, 1.6, 0); g.add(beam);
    model.add(g); return { parts: [l, r, t], beam: beam, on: on, off: off, hit: hit, bad: bad, flash: 0, isBad: false };
  }
  function person(x, z, col) {
    var g = new T.Group(); var b = new T.Mesh(new T.CylinderGeometry(0.28, 0.3, 1.25, 12), mat(col)); b.position.y = 0.62; g.add(b);
    var h = new T.Mesh(new T.SphereGeometry(0.22, 12, 10), mat(0xF2D1B3)); h.position.y = 1.47; g.add(h); g.position.set(x, 0, z); model.add(g); return g;
  }
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.75); key.position.set(-20, 40, -30); scene.add(key);
    pivot = new T.Group(); pivot.rotation.order = 'YXZ'; scene.add(pivot); model = new T.Group(); model.position.set(-1.5, 0, 0); pivot.add(model);
    box(60, 0.2, 22, 1, -0.2, 0, mat(0x33435c));
    /* pick zone: a few rack bays */
    for (var r = 0; r < 3; r++) for (var b = 0; b < 3; b++) {
      var x = -25 + b * 2.7, z = -5 + r * 5;
      for (var k = 0; k < 4; k++) box(2.5, 1.1, 1.1, x + 1.35, 0.15 + k * 1.7, z, mat(0x6E7C8E));
      box(0.09, 7, 0.09, x, 0, z - 0.55, mat(0x3d6fb3)); box(0.09, 7, 0.09, x, 0, z + 0.55, mat(0x3d6fb3));
    }
    conveyor(X_START, X_END, 0, Y, 0x2b3646);
    conveyor(X_START, 7, Z_REPICK, 0.6, 0x3a3240);                                 /* re-pick lane, back to the pick zone */
    box(X_SHIP + 1 + 12, 0.03, 1.2, (X_SHIP + 1 - 12) / 2, 0.01, Z_RET, mat(0xFF7A5C, { op: 0.16 }));  /* return path on the floor */
    box(4.6, 0.03, 3.2, -13.4, 0.01, Z_RET + 0.6, mat(0xFF7A5C, { op: 0.22 }));          /* returns area */
    gates.pick = gate(X_PICK); gates.pack = gate(X_PACK);
    var table = box(2.2, 0.9, 1.0, X_PACK, 0, -1.55, mat(0xA7B6CC)); person(X_PACK, -2.5, 0x3fa7f5);
    /* check scale: a weighing plate in the line, a post and a display that shows each parcel's weight against its expected weight */
    var scale = new T.Group();
    var plate = box(1.4, 0.1, 1.2, X_SCALE, Y + 0.01, 0, mat(0x6f86a8), scale);
    var housing = box(1.5, Y, 1.25, X_SCALE, 0, 0, mat(0x3a4a62), scale);
    var post = box(0.14, 2.1, 0.14, X_SCALE, 0, -0.95, mat(0x4b5b74), scale);
    var dispBox = box(2.3, 1.08, 0.1, X_SCALE, 2.0, -0.95, mat(0x0f1a2a), scale);
    scaleCanvas = document.createElement('canvas'); scaleCanvas.width = 512; scaleCanvas.height = 240;
    scaleTex = new T.CanvasTexture(scaleCanvas);
    var screen = new T.Mesh(new T.PlaneGeometry(2.2, 1.03), new T.MeshBasicMaterial({ map: scaleTex })); screen.position.set(X_SCALE, 2.54, -0.89); scale.add(screen);
    model.add(scale);
    gates.scale = { parts: [plate, housing, post, dispBox, screen], tint: [plate], on: mat(0x6f86a8), off: mat(0x4b5b74), hit: mat(0xc8ff8a, { em: 0x5a8f20 }), bad: mat(0xFF5A4A, { em: 0x6a1008 }), flash: 0, isBad: false };
    drawScale(null);
    /* dock and truck */
    box(0.3, 3.6, 3.4, X_SHIP + 1.2, 0, 0, mat(0x8dc63f, { op: 0.35 }));
    var tr = new T.Group(); var tl = new T.Mesh(new T.BoxGeometry(12, 2.9, 2.5), mat(0xDCE4EE)); tl.position.set(6, 2.55, 0); tr.add(tl);
    var cab = new T.Mesh(new T.BoxGeometry(2.3, 2.5, 2.4), mat(0x2f6db5)); cab.position.set(15.2, 2.25, 0); tr.add(cab);
    var tg = new T.CylinderGeometry(0.48, 0.48, 0.32, 14), tm = mat(0x1b1f26);
    [1.2, 2.5, 12.9, 14.2, 15.9].forEach(function (x) { [-1.08, 1.08].forEach(function (z) { var w = new T.Mesh(tg, tm); w.rotation.x = Math.PI / 2; w.position.set(x, 0.48, z); tr.add(w); }); });
    tr.position.set(X_SHIP + 1.6, 0, 0); model.add(tr);
    /* tote and carton pool */
    var tg2 = new T.BoxGeometry(0.62, 0.34, 0.44);
    for (var i = 0; i < 90; i++) { var m = new T.Mesh(tg2, mat(0x9FB2CC)); m.visible = false; model.add(m); pool.push({ mesh: m, live: false }); }
  }

  /* ----- the flow ----- */
  var seed = 1, items = [], spawnT = 0, tally = { pick: 0, pack: 0, scale: 0, esc: 0, ret: 0, scanned: 0, packed: 0, weighed: 0 }, scaleCanvas, scaleTex, lastWeigh = null;
  function rnd() { seed |= 0; seed = seed + 0x6D2B79F5 | 0; var t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }
  function grab() { for (var i = 0; i < pool.length; i++) if (!pool[i].live) { pool[i].live = true; pool[i].mesh.visible = true; return pool[i]; } return null; }
  function free(it) { it.p.live = false; it.p.mesh.visible = false; }
  var C_OK = 0x9FB2CC, C_ERR = 0xFF5A4A, C_BOX = 0xC9A46A, C_BOXERR = 0xE0705A;   /* tote, tote with an error, parcel, parcel with an error */
  function spawn() {
    var P = D.steps[cur].p, p = grab(); if (!p) return;
    var kind = null, u = rnd(), acc = 0;
    for (var i = 0; i < KINDS.length; i++) { acc += P[KINDS[i]][0] * D.mag; if (u < acc) { kind = KINDS[i]; break; } }
    var fate = 'ok';
    if (kind) {
      var q = P[kind];
      if (rnd() < q[1]) fate = 'pick'; else if (rnd() < q[2]) fate = 'pack'; else if (rnd() < q[3]) fate = 'scale'; else fate = 'esc';
    }
    items.push({ p: p, x: X_START, z: 0, y: Y, err: !!kind, fate: fate, mode: 'line', carton: false, t: 0 });
  }
  function setCol(it) {
    var c = it.carton ? (it.err ? C_BOXERR : C_BOX) : (it.err ? C_ERR : C_OK);
    it.p.mesh.material.color.setHex(c); it.p.mesh.material.emissive.setHex(it.err ? 0x3a0806 : 0x000000);
    it.p.mesh.scale.set(it.carton ? 0.95 : 1, it.carton ? 1.25 : 1, 1);
  }
  function step(dt) {
    spawnT += dt; if (spawnT > 0.55) { spawnT = 0; spawn(); }
    for (var i = items.length - 1; i >= 0; i--) {
      var it = items[i];
      if (it.mode === 'line') {
        if (it.hold > 0) { it.hold -= dt; if (it.hold <= 0 && it.fate === 'scale') { it.mode = 'divert'; it.t = 0; } it.p.mesh.position.set(it.x, it.y + 0.17 * (it.carton ? 1.25 : 1), it.z); setCol(it); continue; }
        var x0 = it.x; it.x += SPEED * dt;
        if (x0 < X_PICK && it.x >= X_PICK && cur >= 2) {                                    /* every pick is scanned */
          tally.scanned++;
          if (it.fate === 'pick') { it.err = false; tally.pick++; ping('pick', true); } else ping('pick', false);   /* refused at the shelf, re-picked right */
        }
        if (x0 < X_PACK && it.x >= X_PACK) {
          if (cur >= 1) tally.packed++;
          if (it.fate === 'pack') { it.mode = 'divert'; it.t = 0; tally.pack++; if (cur >= 3) ping('pack', true); }
          else { it.carton = true; if (cur >= 3) ping('pack', false); }
        }
        if (x0 < X_SCALE && it.x >= X_SCALE && cur >= 4) {                                  /* every parcel stops on the scale and is weighed */
          it.x = X_SCALE; it.hold = 0.3; tally.weighed++;
          var exp = 6 + rnd() * 14, got = exp;
          if (it.fate === 'scale') { got = exp - (1.2 + rnd() * 2.5); tally.scale++; }
          drawScale({ exp: exp, got: got, bad: it.fate === 'scale' }); ping('scale', it.fate === 'scale');
        }
        if (it.x >= X_SHIP) { if (it.err) { tally.esc++; it.mode = 'out'; it.t = 0; } else { free(it); items.splice(i, 1); continue; } }
      } else if (it.mode === 'divert') {                       /* lift across to the re-pick lane, then back to the pick zone */
        it.t += dt;
        if (it.t < 0.6) { var u = it.t / 0.6; it.z = Z_REPICK * u; it.y = Y + Math.sin(Math.PI * u) * 0.9 + (0.6 - Y) * u; }
        else { it.z = Z_REPICK; it.y = 0.6; it.x -= SPEED * 1.1 * dt; if (it.x < X_START) { free(it); items.splice(i, 1); continue; } }
      } else if (it.mode === 'out') {                          /* into the truck, then back later as a return */
        it.t += dt; it.x += SPEED * dt; if (it.t > 0.6) { it.mode = 'away'; it.t = 0; it.p.mesh.visible = false; }
      } else if (it.mode === 'away') {
        it.t += dt; if (it.t > 3.5) { it.mode = 'return'; it.x = X_SHIP + 1; it.z = Z_RET; it.y = 0.05; it.carton = true; it.p.mesh.visible = true; }
      } else if (it.mode === 'return') {
        it.x -= SPEED * 0.9 * dt;
        if (it.x <= -11.5) { tally.ret++; free(it); items.splice(i, 1); addReturn(); continue; }
      }
      it.p.mesh.position.set(it.x, it.y + 0.17 * (it.carton ? 1.25 : 1), it.z); setCol(it);
    }
    ['pick', 'pack', 'scale'].forEach(function (k) { var g = gates[k]; if (g.flash > 0) g.flash -= dt; });
  }
  function ping(k, bad) { var g = gates[k]; if (!g) return; if (bad || !g.isBad || g.flash <= 0) { g.flash = bad ? 0.7 : 0.18; g.isBad = bad; } }
  function drawScale(r) {         /* the scale's screen: expected and actual weight of the last parcel */
    lastWeigh = r; if (!scaleCanvas) return;
    var c = scaleCanvas.getContext('2d'); c.fillStyle = '#0b1626'; c.fillRect(0, 0, 512, 240);
    c.fillStyle = '#7f93b2'; c.font = '600 30px sans-serif'; c.fillText('CHECK SCALE', 24, 44);
    if (!r) { c.fillStyle = '#9FB2CC'; c.font = '600 40px sans-serif'; c.fillText('Waiting for a parcel', 24, 130); }
    else {
      c.font = '600 34px sans-serif'; c.fillStyle = '#9FB2CC'; c.fillText('Expected ' + r.exp.toFixed(1) + ' kg', 24, 104);
      c.fillStyle = r.bad ? '#FF6B5A' : '#8DC63F'; c.font = '700 46px sans-serif'; c.fillText('Weighed ' + r.got.toFixed(1) + ' kg', 24, 162);
      c.font = '700 34px sans-serif'; c.fillText(r.bad ? 'SHORT: back to re-pick' : 'OK: ship it', 24, 214);
    }
    if (scaleTex) scaleTex.needsUpdate = true;
  }
  var pileG = null;
  function addReturn() {
    if (!ok) return;
    if (!pileG) { pileG = new T.Group(); model.add(pileG); }
    var n = returnsPile.length; if (n >= 24) return;
    var b = new T.Mesh(new T.BoxGeometry(0.58, 0.48, 0.44), mat(C_BOXERR)); b.position.set(-15.2 + (n % 6) * 0.68, 0.24 + Math.floor(n / 12) * 0.5, Z_RET + 0.4 + Math.floor((n % 12) / 6) * 0.6); pileG.add(b); returnsPile.push(b);
  }
  function clearFlow() {
    items.forEach(free); items = []; tally = { pick: 0, pack: 0, scale: 0, esc: 0, ret: 0, scanned: 0, packed: 0, weighed: 0 }; seed = 1000 + cur * 77; if (scaleCanvas) drawScale(null);
    if (pileG) { pileG.children.slice().forEach(function (c) { pileG.remove(c); c.geometry.dispose(); }); returnsPile = []; }
  }
  function gatesOn() {          /* a checkpoint is drawn only when its step is on; it lights up when it catches an error */
    var on = { pick: cur >= 2, pack: cur >= 3, scale: cur >= 4 };
    ['pick', 'pack', 'scale'].forEach(function (k) {
      var g = gates[k]; if (!g) return;
      var m = g.flash > 0 ? (g.isBad ? g.bad : g.hit) : g.on, tint = g.tint || g.parts;
      g.parts.forEach(function (p) { p.visible = on[k]; if (tint.indexOf(p) >= 0) p.material = m; });
      if (g.beam) { g.beam.material.opacity = on[k] ? (g.flash > 0 ? 0.6 : 0.14) : 0; g.beam.material.color.setHex(g.flash > 0 && g.isBad ? 0xFF5A4A : 0x8dc63f); }
    });
  }

  /* ----- labels ----- */
  var LBL = [['pick', 'Pick zone', -22, 7.6, 0], ['spick', 'Scan at pick', X_PICK, 2.9, 0], ['pack', 'Pack station', X_PACK, 2.9, -1.8], ['scale', 'Check scale', X_SCALE, 0.3, 1.6],
             ['truck', 'To customers', X_SHIP + 7, 4.4, 0], ['repick', 'Re-pick lane', -9, 1.2, Z_REPICK], ['ret', 'Returns', -13.4, 1.6, Z_RET + 1.4]];
  var labels = LBL.map(function (a) { var el = document.createElement('span'); el.className = 'wh3d-label'; stage.appendChild(el); return { a: a, el: el }; });
  var W = 0, H = 0, wide = true, v3 = ok ? new T.Vector3() : null;
  function labelText(id) {
    var on = { spick: cur >= 2, pack: cur >= 1, scale: cur >= 4 }[id];
    if (id === 'spick') return on ? 'Scan at pick · ' + tally.scanned + ' scanned · ' + tally.pick + ' stopped' : 'No pick scan';
    if (id === 'pack') return on ? (cur >= 3 ? 'Scan at pack' : 'Pack check') + ' · ' + tally.packed + ' packed · ' + tally.pack + ' caught' : 'Packing, no check';
    if (id === 'scale') return on ? 'Check scale · ' + (lastWeigh ? lastWeigh.got.toFixed(1) + ' kg vs ' + lastWeigh.exp.toFixed(1) + (lastWeigh.bad ? ' SHORT' : ' OK') + ' · ' : '') + tally.weighed + ' weighed · ' + tally.scale + ' caught' : 'No scale';
    if (id === 'truck') return 'Parcels to customers · ' + tally.esc + ' wrong';
    if (id === 'ret') return 'Returns · ' + tally.ret;
    return LBL.filter(function (a) { return a[0] === id; })[0][1];
  }
  function placeLabels() {        /* project each label, then push apart any that overlap */
    var boxes = labels.map(function (l) {
      l.el.textContent = labelText(l.a[0]);
      v3.set(l.a[2], l.a[3], l.a[4]); model.localToWorld(v3); v3.project(camera);
      var w = l.el.offsetWidth, h = l.el.offsetHeight;
      return { l: l, w: w, h: h, x: Math.max(6, Math.min(W - w - 6, (v3.x * 0.5 + 0.5) * W - w / 2)), y: Math.max(36, Math.min(H - h - 6, (-v3.y * 0.5 + 0.5) * H - h / 2)) };
    }).sort(function (a, b) { return a.y - b.y; });
    for (var i = 0; i < boxes.length; i++) for (var j = 0; j < i; j++) {
      var a = boxes[i], b = boxes[j];
      if (a.x < b.x + b.w + 4 && b.x < a.x + a.w + 4 && a.y < b.y + b.h + 3 && b.y < a.y + a.h + 3) a.y = b.y + b.h + 3;
    }
    boxes.forEach(function (q) { q.l.el.style.transform = 'translate(' + q.x.toFixed(1) + 'px,' + Math.min(H - q.h - 6, q.y).toFixed(1) + 'px)'; });
  }

  /* ----- panel ----- */
  var steps = [].slice.call(fig.querySelectorAll('.wh3d-step'));
  var SAY = [
    'As-is: paper pick lists and no check. Every error that is made goes to the customer and comes back as a return.',
    'Pack check: the packer compares the cases with the packing slip and sends about half to two-thirds of the errors back to be re-picked.',
    'Scan at pick: the scanner refuses a wrong item or a wrong tote at the shelf, where it costs seconds to fix. Quantity errors still get through.',
    'Scan at pack: every case is scanned against the order, so almost nothing wrong reaches the truck.',
    'Weigh at ship: every parcel stops on the scale for a few seconds and is weighed. It catches most remaining quantity errors, but after scanning so few are left that it rarely finds one, and it costs more than it saves.'
  ];
  function ui() {
    var s = D.steps[cur].s;
    $('wh3d5-right').textContent = (s[0] * 100).toFixed(2) + '%'; $('wh3d5-esc').textContent = fmt(s[1]);
    $('wh3d5-cerr').textContent = money(s[2]); $('wh3d5-cchk').textContent = money(s[3]); $('wh3d5-tot').textContent = money(s[4]);
    $('wh3d5-sav').textContent = cur ? money(s[5]) : '—';
    $('wh3d5-sav').parentNode.classList.toggle('is-bad', cur === 4);
    $('wh3d5-say').textContent = SAY[cur]; $('wh3d5-chip').textContent = (cur ? 'Step ' + cur + ' · ' : '') + D.names[cur]; $('wh3d5-chip').classList.toggle('is-bad', cur === 0);
    steps.forEach(function (b, k) { b.setAttribute('aria-pressed', k === cur ? 'true' : 'false'); b.classList.toggle('is-done', k < cur); });
  }
  function setStep(n) {
    cur = n; clearFlow(); ui();
    if (ok) { gatesOn(); for (var k = 0; k < 220; k++) step(0.05); }   /* start with the line already running (11 s), so results show at once */
    tourT = 0;
  }

  /* ----- view ----- */
  var yawU = -0.18, pitchU = 0.64, yaw = yawU, pitch = pitchU, idle = 99, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; wide = W >= 560;
    if (!wide && idle > 90) { yawU = -0.62; pitchU = 0.6; yaw = yawU; pitch = pitchU; }   /* on a phone, look along the line */
    if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    camera.aspect = W / H; var dist = Math.max(wide ? 40 : 24, (wide ? 21 : 7.5) / (Math.tan(15 * Math.PI / 180) * Math.min(1.6, W / H)));
    camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix();
  }
  function render() { if (!ok) return; pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -1.5, 0); gatesOn(); pivot.updateMatrixWorld(true); renderer.render(scene, camera); placeLabels(); }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawU, pitch: pitchU }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) { if (!drag) return; yawU = Math.max(-1.4, Math.min(1.0, drag.yaw + (e.clientX - drag.x) * 0.008)); pitchU = Math.max(0.12, Math.min(1.3, drag.pitch + (e.clientY - drag.y) * 0.005)); idle = 0; if (!running) { yaw = yawU; pitch = pitchU; render(); } });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);
  steps.forEach(function (b) { b.addEventListener('click', function () { tourOn = false; pauseT = 0; setStep(+b.getAttribute('data-s')); if (!running) render(); }); });
  var bn = $('wh3d5-names');
  bn.addEventListener('click', function () { var on = bn.getAttribute('aria-pressed') !== 'true'; bn.setAttribute('aria-pressed', on ? 'true' : 'false'); stage.classList.toggle('no-names', !on); if (!running) render(); });

  var tb = $('wh3d5-tour'), tbFill = tb && tb.querySelector('i'), tbText = tb && tb.querySelector('span'), tbLast = '';
  function tourBar() {            /* how long until the tour moves on, or that it is paused on the reader's pick */
    if (!tb) return;
    var txt;
    if (tourOn) { tbFill.style.width = (Math.min(1, tourT / HOLD) * 100).toFixed(1) + '%'; txt = 'Next step in ' + Math.max(1, Math.ceil(HOLD - tourT)) + ' s · pick a step to stay on it'; }
    else { tbFill.style.width = '0%'; txt = 'Staying on step ' + cur + ' · the tour resumes after a minute without clicks'; }
    if (txt !== tbLast) { tbLast = txt; tbText.textContent = txt; }
  }
  var last = 0, visible = true;
  function frame(ts) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (ts - last) / 1000 || 0)); last = ts; clock += dt; idle += dt;
    if (ok) step(dt);
    if (tourOn) { tourT += dt; if (tourT > HOLD) { tourT = 0; setStep((cur + 1) % 5); } }
    else { pauseT += dt; if (pauseT > 60 && idle > 60) { tourOn = true; tourT = 0; } }
    tourBar();
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.08 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(); requestAnimationFrame(frame);
  }
  function setRun(v) { if (reduce) return; if (v && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); } else if (!v) running = false; }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); setStep(0);
  if (reduce && ok) { for (var k = 0; k < 400; k++) step(0.05); }
  render();
  window.addEventListener('resize', function () { resize(); if (!running) render(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
