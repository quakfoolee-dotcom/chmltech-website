/* Warehouse operations series, Part 8: three automations in the Part 1 warehouse (needs three.js r128+ as window.THREE).
   Data (#wh3d8-data) come from content/articles/wh8_model.py: for each set-up and volume, the one-time cost, yearly
   running cost, saving, net saving, payback, labour hours saved a day, equipment and floor freed. The racks at the front
   hold case picks; the shelving at the back holds small items.
     base  pickers walk to every location
     ptl   lights flash on the fastest shelving locations ahead of the picker
     vlm   two vertical lift modules replace the shelving; pickers stand at the windows; the freed floor glows green
     amr   robots carry totes through the rack aisles to pickers who stay in their zones
   People and robots are drawn solid where they can be seen, as a faint outline behind racks, with a ring on the floor. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d8');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d8-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var OPTS = D.opts, VOLS = D.vols, STEP_S = 14;
  var TOUR = [['base', D.today], ['ptl', D.today], ['vlm', D.today], ['amr', D.today], ['amr', VOLS.indexOf(900)], ['vlm', VOLS.indexOf(600)]];
  var S = { o: 'base', all: false, v: D.today };
  var tourOn = !reduce, tourK = 0, tourT = 0, pauseT = 0;
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function money(n) { return '$' + (n >= 10000 ? Math.round(n / 1000) + 'k' : fmt(n)); }
  function R(o, v) { return D.R[o][v]; }   /* [one-time, running, saving, net, payback, hours saved, units, freed m2, utilisation] */
  function oi(o) { return OPTS.indexOf(o); }
  function pbText(p) { return p === null ? 'Never' : p >= 10 ? 'Over 10 years' : p.toFixed(1) + ' years'; }
  var rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })(11);

  /* layout */
  var WALK_X = 12.8, PACK = [12.5, 40.5], SH_X0 = 24, SH_X1 = 64, SH_Z = [], SH_AZ = [], i;
  for (i = 0; i < 7; i++) SH_Z.push(35.5 + i * 2.3);
  for (i = 0; i < 6; i++) SH_AZ.push(36.65 + i * 2.3);
  var TOWERS = [[30, 41.6], [36, 41.6]];
  function people(o, v) {                       /* case pickers, small-item pickers, robots */
    var vol = VOLS[v], lines = vol * D.lines, cs = lines * D.caseShare, es = lines - cs, r = R(o, v);
    var caseH = cs * 1.0 / 60, eachH = es * 1.1 / 60;
    if (o === 'amr') caseH -= r[5]; else if (o !== 'base') eachH -= r[5];
    return [Math.max(1, Math.ceil(caseH / 7)), o === 'vlm' ? D.vlmUnits : Math.max(1, Math.ceil(eachH / 7)), o === 'amr' ? r[6] : 0];
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false, G = {};
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d8-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  var CX = D.bld[0] / 2, CZ = D.bld[1] / 2, body, head, ringGeo, ghostM, shelves = [];
  function box(w, h, d, x, y, z, m, parent) { var o = new T.Mesh(new T.BoxGeometry(w, h, d), m); o.position.set(x, y + h / 2, z); (parent || model).add(o); return o; }
  function figure(parent, col, isBot) {
    var g = new T.Group(), ghost = function (c) { return new T.MeshBasicMaterial({ color: c, depthTest: false, depthWrite: false, transparent: true, opacity: 0.24 }); };
    if (isBot) {
      var bg = new T.BoxGeometry(1.0, 0.45, 0.8), tg = new T.BoxGeometry(0.7, 0.45, 0.55);
      var b1 = new T.Mesh(bg, mat(0x2b3442)); b1.position.y = 0.3; g.add(b1);
      var t1 = new T.Mesh(tg, mat(0xFF8A3D)); t1.position.y = 0.75; g.add(t1);
      var b2 = new T.Mesh(bg, ghost(0x9aa7b8)); b2.position.y = 0.3; b2.renderOrder = 10; g.add(b2);
      var t2 = new T.Mesh(tg, ghost(0xFF8A3D)); t2.position.y = 0.75; t2.renderOrder = 10; g.add(t2);
    } else {
      var bo = new T.Mesh(body, mat(col)); bo.position.y = 0.75; g.add(bo);
      var hd = new T.Mesh(head, mat(0xF2D1B3)); hd.position.y = 1.8; g.add(hd);
      var gb = new T.Mesh(body, ghost(0x7fb6ff)); gb.position.y = 0.75; gb.renderOrder = 10; g.add(gb);
      var gh = new T.Mesh(head, ghost(0xF2D1B3)); gh.position.y = 1.8; gh.renderOrder = 10; g.add(gh);
    }
    var ring = new T.Mesh(ringGeo, new T.MeshBasicMaterial({ color: isBot ? 0xFF8A3D : 0x5FE3FF, transparent: true, opacity: 0.55, depthWrite: false })); ring.rotation.x = -Math.PI / 2; ring.position.y = 0.04; g.add(ring);
    g.scale.setScalar(1.6); g.visible = false; parent.add(g);
    return { g: g, x: PACK[0], z: PACK[1], route: null, wait: 0, on: false };
  }
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 600);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.7); key.position.set(-30, 60, 40); scene.add(key);
    pivot = new T.Group(); pivot.rotation.order = 'YXZ'; scene.add(pivot); model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var BX = D.bld[0], BZ = D.bld[1], ROWS = D.rows, BAYS = D.bays, BW = D.bayW, X0 = D.x0, LV = D.levels, BEAM = D.beam, rr, bb, kk, f, s, n = 0;
    box(BX, 0.2, BZ, BX / 2, -0.2, BZ / 2, mat(0x2a3446));
    var wall = mat(0x4b5b74, { op: 0.5 });
    box(BX, 1.2, 0.25, BX / 2, 0, 0, wall); box(0.25, 1.2, BZ, 0, 0, BZ / 2, wall); box(0.25, 1.2, BZ, BX, 0, BZ / 2, wall); box(BX, 1.2, 0.25, BX / 2, 0, BZ, wall);
    for (i = 0; i < 6; i++) box(0.3, 3.2, 3.0, -0.05, 0, 6 + i * 4.2, mat(i < 4 ? 0x8dc63f : 0xFF8A3D));
    for (i = 0; i < 4; i++) box(2.4, 0.95, 1.2, 6 + i * 3.2, 0, 46.5, mat(0xA7B6CC));
    var q = new T.Quaternion(), sc = new T.Vector3(), ps = new T.Vector3(), m4 = new T.Matrix4();
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3, { op: 0.5 }), ROWS.length * (BAYS + 1) * 2), topH = LV[LV.length - 1] + 0.2;
    for (rr = 0; rr < ROWS.length; rr++) for (bb = 0; bb <= BAYS; bb++) for (kk = -1; kk <= 1; kk += 2) { ps.set(X0 + bb * BW, topH / 2, ROWS[rr] + kk * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4); }
    model.add(up);
    var bm = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), mat(0xE8862A, { op: 0.4 }), ROWS.length * BAYS * (LV.length - 1) * 2); n = 0;
    for (rr = 0; rr < ROWS.length; rr++) for (bb = 0; bb < BAYS; bb++) for (kk = 1; kk < LV.length; kk++) for (f = -1; f <= 1; f += 2) { ps.set(X0 + (bb + 0.5) * BW, LV[kk] + BEAM / 2, ROWS[rr] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); bm.setMatrixAt(n++, m4); }
    model.add(bm);
    var locs = []; for (rr = 0; rr < ROWS.length; rr++) for (bb = 0; bb < BAYS; bb++) for (s = 0; s < D.perBay; s++) for (kk = 0; kk < LV.length; kk++) if (rnd() < 0.86) locs.push([X0 + bb * BW + (s + 0.5) * BW / D.perBay, LV[kk] + BEAM + 0.64, ROWS[rr]]);
    var pal = new T.InstancedMesh(new T.BoxGeometry(BW / D.perBay - 0.25, 1.25, D.rowD * 0.9), mat(0x5D7FA8), locs.length);
    locs.forEach(function (L, j) { ps.set(L[0], L[1], L[2]); sc.set(1, 1, 1); m4.compose(ps, q, sc); pal.setMatrixAt(j, m4); }); model.add(pal);
    var shelfM = mat(0x56688a); SH_Z.forEach(function (z) { shelves.push(box(SH_X1 - SH_X0, 2.4, 1.0, (SH_X0 + SH_X1) / 2, 0, z, shelfM)); });
    body = new T.CylinderGeometry(0.42, 0.45, 1.5, 12); head = new T.SphereGeometry(0.34, 12, 10); ringGeo = new T.RingGeometry(0.55, 0.85, 20);
    OPTS.forEach(function (o) {
      var grp = new T.Group(); model.add(grp); var x = { grp: grp, cp: [], ep: [], bots: [], lights: [] };
      for (var j = 0; j < 8; j++) x.cp.push(figure(grp, 0x3f86e8));
      for (j = 0; j < 8; j++) x.ep.push(figure(grp, 0x3f86e8));
      if (o === 'amr') for (j = 0; j < 8; j++) x.bots.push(figure(grp, 0, true));
      if (o === 'ptl') {
        var lg = new T.BoxGeometry(0.9, 0.18, 0.7);
        for (j = 0; j < 60; j++) {
          var row = j % 6, side = Math.floor(j / 6) % 2, lx = SH_X0 + 1 + rnd() * (SH_X1 - SH_X0 - 2), lz = SH_Z[row + side] + (side ? -0.56 : 0.56);
          var m = new T.Mesh(lg, new T.MeshBasicMaterial({ color: 0x2a5a33 })); m.position.set(lx, 2.5, SH_Z[row + side]); grp.add(m);
          x.lights.push({ m: m, t: 0, x: lx, az: SH_AZ[row] });
        }
      }
      if (o === 'vlm') {
        TOWERS.forEach(function (tw) {                            /* tower, pick window facing the camera (+z), tray, items, travel light */
          box(3.4, 8.6, 2.8, tw[0], 0, tw[1], mat(0x8e6cdc), grp);
          box(3.5, 0.3, 2.9, tw[0], 8.6, tw[1], mat(0x6a4fb8), grp);
          box(2.0, 1.1, 0.08, tw[0], 0.8, tw[1] + 1.44, new T.MeshBasicMaterial({ color: 0x141b28 }), grp);
          var tray = box(1.7, 0.16, 1.1, tw[0], 1.0, tw[1] + 0.9, mat(0xd8dde6), grp);
          [[-0.5, 0x3FA7F5], [0, 0xF5A032], [0.5, 0x6ECD69]].forEach(function (it) { var b0 = new T.Mesh(new T.BoxGeometry(0.32, 0.28, 0.32), mat(it[1])); b0.position.set(it[0], 0.22, 0); tray.add(b0); });
          var item = box(0.32, 0.28, 0.32, tw[0], 1.2, tw[1] + 2, mat(0xF5A032), grp); item.visible = false;
          var tote = box(0.9, 0.5, 0.6, tw[0] + 1.3, 0.6, tw[1] + 3.2, mat(0xFF8A3D), grp); box(0.9, 0.6, 0.6, tw[0] + 1.3, 0, tw[1] + 3.2, mat(0x2b3442), grp);
          var lamp = box(0.5, 0.25, 0.06, tw[0] - 1.2, 1, tw[1] + 1.43, new T.MeshBasicMaterial({ color: 0xFFE27A }), grp);
          x.trays = (x.trays || []).concat([{ m: tray, z0: tw[1] + 0.9, t: x.trays ? 2.5 : 0, item: item, tote: tote, lamp: lamp, tw: tw }]);
        });
        var fl = new T.Mesh(new T.PlaneGeometry(SH_X1 - SH_X0, 15.2), new T.MeshBasicMaterial({ color: 0x6ECD69, transparent: true, opacity: 0.32, depthWrite: false }));
        fl.rotation.x = -Math.PI / 2; fl.position.set((SH_X0 + SH_X1) / 2 + 0, 0.04, 42.4); grp.add(fl);
        var cut = new T.Mesh(new T.PlaneGeometry(13, 6), new T.MeshBasicMaterial({ color: 0x2a3446 })); cut.rotation.x = -Math.PI / 2; cut.position.set(33, 0.05, 41.2); grp.add(cut);
      }
      G[o] = x;
    });
  }

  /* ----- motion ----- */
  function rackRoute() {
    var a = Math.floor(rnd() * D.aisles.length), az = D.aisles[a], x1 = D.x0 + 2 + rnd() * (D.bays * D.bayW - 4), x2 = Math.min(D.x0 + D.bays * D.bayW - 1, x1 + 4 + rnd() * 10);
    return [[WALK_X, PACK[1] - 4], [WALK_X, az], [x1, az, 1], [x2, az, 1], [WALK_X, az], [WALK_X, PACK[1] - 4], [PACK[0] + (rnd() - 0.5) * 3, PACK[1] + (rnd() - 0.5) * 2, 2]];
  }
  function shelfRoute(x, lit) {
    var r = Math.floor(rnd() * SH_AZ.length), az = SH_AZ[r], pts = [[20, PACK[1]], [20, az]], k, l;
    if (lit) {                                                    /* walk straight to the lit locations in this aisle */
      var cand = x.lights.filter(function (q) { return q.az === az; }).sort(function () { return rnd() - 0.5; }).slice(0, 2).sort(function (p1, p2) { return p1.x - p2.x; });
      cand.forEach(function (q) { q.t = 2.6; pts.push([q.x, az, 3]); });
      if (!cand.length) pts.push([SH_X0 + 6, az, 1]);
    } else { var st = []; for (k = 0; k < 3; k++) st.push(SH_X0 + 2 + rnd() * (SH_X1 - SH_X0 - 4)); st.sort(function (p1, p2) { return p1 - p2; }).forEach(function (l2) { pts.push([l2, az, 1]); }); }
    pts.push([20, az], [20, PACK[1]], [PACK[0] + 2 + rnd() * 2, PACK[1] + 1 + rnd(), 2]);
    return pts;
  }
  function walk(p, dt, spd, routeFn, pause) {
    if (!p.on) return;
    if (p.wait > 0) { p.wait -= dt; return; }
    if (!p.route) { p.route = routeFn(); p.leg = 0; }
    var tg = p.route[p.leg], dx = tg[0] - p.x, dz = tg[1] - p.z, d = Math.sqrt(dx * dx + dz * dz), mv = spd * dt;
    if (d <= mv) { p.x = tg[0]; p.z = tg[1]; if (tg.length > 2) p.wait = tg[2] === 3 ? pause * 0.55 : pause; p.leg++; if (p.leg >= p.route.length) p.route = null; }
    else { p.x += dx / d * mv; p.z += dz / d * mv; p.g.rotation.y = Math.atan2(dx, dz); }
  }
  var ZONE = [];
  function setup() {
    OPTS.forEach(function (o) {
      var x = G[o], n = people(o, S.v), j;
      x.cp.forEach(function (p, k) { p.on = k < n[0]; p.route = null; p.x = PACK[0] - 1 - k; p.z = PACK[1] - 1; p.wait = k * 0.5; });
      x.ep.forEach(function (p, k) { p.on = o !== 'vlm' && k < n[1]; p.route = null; p.x = 18; p.z = PACK[1] + k * 0.8; p.wait = k * 0.6; });
      if (o === 'vlm') x.ep.forEach(function (p, k) { p.on = k < TOWERS.length; if (p.on) { p.x = TOWERS[k][0] - 1.55; p.z = TOWERS[k][1] + 2.5; p.g.rotation.y = Math.PI * 0.78; } });
      if (o === 'amr') {
        ZONE = []; for (j = 0; j < n[0]; j++) ZONE.push([D.x0 + 12 + (j % 2) * 22, D.aisles[(j * 2 + 1) % D.aisles.length]]);
        x.cp.forEach(function (p, k) { if (p.on) { p.x = ZONE[k][0]; p.z = ZONE[k][1]; } });
        x.bots.forEach(function (b, k) { b.on = k < n[2]; b.route = null; b.x = PACK[0] - 1 - k * 1.2; b.z = PACK[1] - 2; b.wait = k * 0.9; });
      }
    });
  }
  function botRoute() {
    var z = ZONE[Math.floor(rnd() * ZONE.length)], az = z[1];
    return [[WALK_X, PACK[1] - 4], [WALK_X, az], [z[0] - 1.6, az, 1], [D.x0 + 2 + rnd() * 40, az, 1], [WALK_X, az], [WALK_X, PACK[1] - 4], [PACK[0], PACK[1] - 2, 2]];
  }
  function step(o, dt) {
    var x = G[o];
    x.cp.forEach(function (p) { if (o === 'amr') return; walk(p, dt, 9, rackRoute, 0.5); });
    if (o !== 'vlm') x.ep.forEach(function (p) { walk(p, dt, 7, function () { return shelfRoute(x, o === 'ptl'); }, 0.7); });
    if (o === 'amr') x.bots.forEach(function (b) { walk(b, dt, 7, botRoute, 0.8); });
    if (o === 'ptl') x.lights.forEach(function (l) { if (l.t > 0) l.t -= dt; else if (rnd() < dt * 0.04) l.t = 1.5; l.m.material.color.setHex(l.t > 0 && Math.sin(l.t * 14) > -0.6 ? 0x6EF07A : 0x2a5a33); });
    if (o === 'vlm') x.trays.forEach(function (t) {
      /* cycle of 6 s: 0-1.5 the tower fetches the tray (light climbs and falls), 1.5-2.3 the tray slides out,
         2.3-3.6 the picker lifts an item into the tote, 3.6-4.4 the tray goes back, 4.4-6 it is stored */
      t.t += dt; var c = t.t % 6, e = c < 1.5 ? 0 : c < 2.3 ? (c - 1.5) / 0.8 : c < 3.6 ? 1 : c < 4.4 ? 1 - (c - 3.6) / 0.8 : 0;
      t.m.position.z = t.z0 + e * 1.3;
      var travel = c < 1.5 ? c / 1.5 : c >= 4.4 ? 1 - (c - 4.4) / 1.6 : -1;
      t.lamp.visible = travel >= 0; if (travel >= 0) t.lamp.position.y = 1 + Math.sin(travel * Math.PI) * 6.8;
      if (c >= 2.5 && c < 3.4) { var u = (c - 2.5) / 0.9; t.item.visible = true;
        t.item.position.set(t.tw[0] + u * 1.3, 1.25 + Math.sin(u * Math.PI) * 1.4, t.tw[1] + 2.2 + u * 1.0); }
      else t.item.visible = false;
    });
  }
  function draw(o) { var x = G[o]; x.cp.concat(x.ep, x.bots).forEach(function (p) { p.g.visible = p.on; p.g.position.set(p.x, 0, p.z); }); }
  function showOnly(o) { OPTS.forEach(function (q) { G[q].grp.visible = q === o; }); shelves.forEach(function (s) { s.visible = o !== 'vlm'; }); }

  /* ----- labels ----- */
  var lab = document.createElement('span'); lab.className = 'wh3d-label'; stage.appendChild(lab);
  var lab2 = document.createElement('span'); lab2.className = 'wh3d-label'; stage.appendChild(lab2);
  var quads = OPTS.map(function (o, k) { var el = document.createElement('span'); el.className = 'wh3d2-q'; el.textContent = D.onames[k]; el.style.setProperty('--c', ['#9FB2CC', '#6EF07A', '#B07CFF', '#FF8A3D'][k]); stage.appendChild(el); return el; });
  var Wd = 0, Hd = 0, v3 = ok ? new T.Vector3() : null;
  function place(el, p) {
    v3.set(p[0], p[1], p[2]); model.localToWorld(v3); v3.project(camera);
    var w = el.offsetWidth, h = el.offsetHeight, x = Math.max(6, Math.min(Wd - w - 6, (v3.x * 0.5 + 0.5) * Wd - w / 2)), y = Math.max(36, Math.min(Hd - h - 6, (-v3.y * 0.5 + 0.5) * Hd - h / 2));
    el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)'; return y;
  }
  function labels() {
    if (S.all || !ok) { lab.style.display = lab2.style.display = 'none'; return; }
    lab.style.display = lab2.style.display = '';
    var o = S.o, r = R(o, S.v), n = people(o, S.v);
    lab.textContent = o === 'base' ? n[1] + ' pickers walk the shelving' : o === 'ptl' ? D.ptlLocs + ' lights · ' + n[1] + ' picker' + (n[1] > 1 ? 's' : '') : o === 'vlm' ? D.vlmUnits + ' lifts bring trays to the pickers · ' + fmt(D.freedM2) + ' m² freed' : n[1] + ' pickers walk the shelving';
    lab2.textContent = o === 'amr' ? r[6] + ' robots, ' + Math.round(Math.min(1, r[8]) * 100) + '% busy · ' + n[0] + ' picker' + (n[0] > 1 ? 's' : '') + ' in zones' : n[0] + ' picker' + (n[0] > 1 ? 's' : '') + ' walk the racks';
    var y1 = place(lab, S.o === 'vlm' ? [33, 11, 41.6] : [44, 3.8, 42]); lab2.style.display = S.o === 'vlm' ? 'none' : ''; var y2 = place(lab2, [42, 10, 16]);
    if (Math.abs(y1 - y2) < 26) place(lab2, [42, 14, 10]);
  }

  /* ----- panel ----- */
  var SAY = {
    base: 'Manual picking with scanners and a WMS: pickers walk to every location in the racks and the shelving. This is the starting point the three automations are measured against.',
    ptl: 'Pick-to-light: lights on the fastest shelving locations show where to pick and how many, so pickers go straight to them. Cheap to buy, but at this volume it has little time to save.',
    vlm: 'Vertical lift modules: two towers of trays replace the shelving. The tower fetches the tray inside (the yellow light climbs), slides it out to the window, the picker lifts the item into the tote, and the tray goes back. Nobody walks to the shelf. The green floor is freed, and it is worth money only if the business needs it.',
    amr: 'Mobile robots: robots carry the totes through the rack aisles and stop at the pickers, who stay in their zones. Robots pay when there is enough work to keep the fleet busy.'
  };
  function cell(id, f) { var el = $(id); el.style.fontSize = S.all ? '14px' : ''; el.style.whiteSpace = S.all ? 'normal' : ''; el.textContent = S.all ? OPTS.slice(1).map(f).join(' · ') : f(S.o); }
  function ui() {
    var v = S.v, base = !S.all && S.o === 'base';
    cell('wh3d8-one', function (o) { return o === 'base' ? '-' : money(R(o, v)[0]); });
    cell('wh3d8-pb', function (o) { return o === 'base' ? '-' : pbText(R(o, v)[4]); });
    cell('wh3d8-sav', function (o) { return o === 'base' ? '-' : money(R(o, v)[2]); });
    cell('wh3d8-run', function (o) { return o === 'base' ? '-' : money(R(o, v)[1]); });
    cell('wh3d8-hrs', function (o) { return o === 'base' ? '-' : R(o, v)[5].toFixed(1); });
    cell('wh3d8-eq', function (o) { return o === 'base' ? 'None added' : o === 'ptl' ? R(o, v)[6] + ' lights' : o === 'vlm' ? R(o, v)[6] + ' lifts' : R(o, v)[6] + ' robots'; });
    if (S.all) $('wh3d8-eq').textContent = OPTS.slice(1).map(function (o) { return R(o, v)[6] + (o === 'ptl' ? ' lights' : o === 'vlm' ? ' lifts' : ' robots'); }).join(' · ');
    fig.querySelectorAll('[data-o]').forEach(function (b) { var x = b.getAttribute('data-o'); b.setAttribute('aria-pressed', (x === 'all' ? S.all : !S.all && x === S.o) ? 'true' : 'false'); });
    fig.querySelectorAll('[data-v]').forEach(function (b) { b.setAttribute('aria-pressed', +b.getAttribute('data-v') === v ? 'true' : 'false'); });
    var best = null; OPTS.slice(1).forEach(function (o) { var p = R(o, v)[4]; if (p !== null && (best === null || p < R(best, v)[4])) best = o; });
    $('wh3d8-cv').textContent = VOLS[v] + ' orders a day · fastest payback: ' + (best ? D.onames[oi(best)] + ' (' + pbText(R(best, v)[4]) + ')' : 'none');
    $('wh3d8-say').textContent = S.all ? 'The four set-ups at ' + VOLS[v] + ' orders a day. The numbers are for pick-to-light, vertical lifts and mobile robots, in that order.' : SAY[S.o];
    chart();
  }
  var CCOL = { ptl: '#6EF07A', vlm: '#B07CFF', amr: '#FF8A3D' };
  function cx(vol) { return 4 + (vol - 150) / 750 * 592; }
  function cy(p) { return 86 - Math.min(8, p) / 8 * 82; }
  function chart() {
    var s = '<line x1="0" y1="' + cy(3).toFixed(1) + '" x2="600" y2="' + cy(3).toFixed(1) + '" stroke="rgba(255,255,255,.35)" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>';
    var xc = cx(VOLS[S.v]).toFixed(1); s += '<line x1="' + xc + '" y1="0" x2="' + xc + '" y2="90" stroke="#FFE27A" stroke-width="2" vector-effect="non-scaling-stroke"/>';
    ['ptl', 'vlm', 'amr'].forEach(function (o) {
      var seg = [], segs = [];
      VOLS.forEach(function (vol, k) { var p = R(o, k)[4]; if (p === null || p > 8) { if (seg.length) segs.push(seg); seg = []; } else seg.push(cx(vol).toFixed(1) + ',' + cy(p).toFixed(1)); });
      if (seg.length) segs.push(seg);
      var hi = S.all || S.o === o || S.o === 'base';
      segs.forEach(function (sg) { s += '<polyline points="' + sg.join(' ') + '" fill="none" stroke="' + CCOL[o] + '" stroke-width="' + (hi ? 2.4 : 1.2) + '" opacity="' + (hi ? 1 : 0.45) + '" vector-effect="non-scaling-stroke"/>'; });
    });
    $('wh3d8-csvg').innerHTML = s;
  }
  function setVol(v) { S.v = v; if (ok) setup(); ui(); if (!running) render(0); }
  $('wh3d8-csvg').addEventListener('click', function (e) {
    var rc = this.getBoundingClientRect(), vol = 150 + (e.clientX - rc.left) / rc.width * 750, bi = 0;
    VOLS.forEach(function (x, k) { if (Math.abs(x - vol) < Math.abs(VOLS[bi] - vol)) bi = k; });
    tourOn = false; pauseT = 0; setVol(bi);
  });
  fig.querySelectorAll('[data-o]').forEach(function (b) { b.addEventListener('click', function () { var x = b.getAttribute('data-o'); if (x === 'all') S.all = true; else { S.all = false; S.o = x; } tourOn = false; pauseT = 0; ui(); if (!running) render(0); }); });
  fig.querySelectorAll('[data-v]').forEach(function (b) { b.addEventListener('click', function () { tourOn = false; pauseT = 0; setVol(+b.getAttribute('data-v')); }); });
  var tb = $('wh3d8-tour'), tbFill = tb.querySelector('i'), tbText = tb.querySelector('span'), tbLast = '';
  function tourBar() {
    var txt;
    if (tourOn) { tbFill.style.width = (Math.min(1, tourT / STEP_S) * 100).toFixed(1) + '%'; txt = 'Touring ' + (tourK + 1) + ' of ' + TOUR.length + ' · next in ' + Math.max(1, Math.ceil(STEP_S - tourT)) + ' s · pick a set-up or volume to stay'; }
    else { tbFill.style.width = '0%'; txt = 'Staying here · the tour resumes after a minute without clicks'; }
    if (txt !== tbLast) { tbLast = txt; tbText.textContent = txt; }
  }
  function goTour(k) { tourK = k; S.o = TOUR[k][0]; S.all = false; setVol(TOUR[k][1]); }

  /* ----- view ----- */
  var yawU = 0.5, pitchU = 1.15, yaw = yawU, pitch = pitchU, idle = 99, clock = 0;
  function resize() { var rc = stage.getBoundingClientRect(); Wd = rc.width; Hd = rc.height; if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(Wd, Hd, false); }
  var focus = 0;
  function aim(w, h) { camera.aspect = w / h; var dist = Math.max(60, (S.all ? 34 : 40) / (Math.tan(15 * Math.PI / 180) * Math.min(1.6, w / h))) * (1 - 0.62 * focus); camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix(); }
  function render(dt) {
    var o = S.all ? null : S.o, r = o && o !== 'base' ? R(o, S.v) : null;
    $('wh3d8-chip').textContent = VOLS[S.v] + ' orders a day' + (r ? ' · payback ' + pbText(r[4]).toLowerCase() : '');
    if (!ok) return;
    var f = S.all ? 0 : focus; pivot.rotation.set(pitch - 0.38 * f, yaw - 0.3 * f, 0); pivot.position.set(0, -3 - 1.5 * f, 0);
    model.position.set(-CX - (33 - CX) * f, 0, -CZ - (43 - CZ) * f);
    OPTS.forEach(draw);
    renderer.setScissorTest(false); renderer.setViewport(0, 0, Wd, Hd); renderer.clear();
    if (!S.all) { showOnly(S.o); pivot.updateMatrixWorld(true); aim(Wd, Hd); renderer.render(scene, camera); quads.forEach(function (qd) { qd.style.display = 'none'; }); }
    else {
      renderer.setScissorTest(true); var hw = Wd / 2, hh = Hd / 2;
      OPTS.forEach(function (q, k) {
        var x = (k % 2) * hw, y = k < 2 ? hh : 0;
        showOnly(q); pivot.updateMatrixWorld(true);
        renderer.setViewport(x, y, hw, hh); renderer.setScissor(x, y, hw, hh); var fs = focus; focus = 0; aim(hw, hh); focus = fs; renderer.render(scene, camera);
        var qd = quads[k]; qd.style.display = ''; qd.style.transform = 'translate(' + (x + 10) + 'px,' + ((k < 2 ? 0 : hh) + 34) + 'px)';
      });
      renderer.setScissorTest(false);
    }
    stage.classList.toggle('is-quad', S.all);
    labels();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawU, pitch: pitchU }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) { if (!drag) return; yawU = Math.max(-0.9, Math.min(2.6, drag.yaw + (e.clientX - drag.x) * 0.008)); pitchU = Math.max(0.2, Math.min(1.35, drag.pitch + (e.clientY - drag.y) * 0.005)); idle = 0; if (!running) { yaw = yawU; pitch = pitchU; render(0); } });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  var last = 0, visible = true;
  function frame(ts) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (ts - last) / 1000 || 0)); last = ts; clock += dt; idle += dt;
    if (ok) OPTS.forEach(function (o) { step(o, dt); });
    if (tourOn) { tourT += dt; if (tourT > STEP_S) { tourT = 0; goTour((tourK + 1) % TOUR.length); } }
    else { pauseT += dt; if (pauseT > 60 && idle > 60) { tourOn = true; tourT = 0; goTour(0); } }
    tourBar();
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.08 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e; focus += ((!S.all && S.o === 'vlm' ? 1 : 0) - focus) * (1 - Math.exp(-dt * 3));
    render(dt); requestAnimationFrame(frame);
  }
  function setRun(v) { if (reduce) return; if (v && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); } else if (!v) running = false; }
  if (ok) { build(); renderer.autoClear = false; stage.classList.add('is-live'); setup(); }
  if (ok && reduce) OPTS.forEach(function (o) { for (var k = 0; k < 200; k++) step(o, 0.05); });
  if (reduce) fig.querySelectorAll('[data-o]').forEach(function (b) { b.addEventListener('click', function () { focus = !S.all && S.o === 'vlm' ? 1 : 0; render(0); }); });
  resize(); ui(); tourBar(); render(0);
  window.addEventListener('resize', function () { resize(); if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
