/* Warehouse operations series, Part 7: what the system knows, a day in the Part 1 warehouse on four systems
   (needs three.js r128+ as window.THREE). Data (#wh3d7-data) come from content/articles/wh7_model.py: for each system
   and volume, the yearly cost, cost an order, floor people, errors reaching customers a day and the stock-record
   accuracy; plus how far behind each system's records run. Pallets are coloured by their record: right, not in the
   system yet (stock has moved, the paperwork has not been keyed in) or wrong. Pickers on paper carry their lists to
   the office, where they pile up until the end of the shift; pickers with scanners send each pick to the system. */
(function () {
  'use strict';
  var fig = document.getElementById('wh3d7');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var D = JSON.parse($('wh3d7-data').textContent);
  var stage = fig.querySelector('.wh3d-stage'), cv = stage.querySelector('canvas');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var OPTS = D.opts, NO = OPTS.length, VOLS = D.vols, DAY_H = 8.5, DAY_S = 16;
  var TOUR = [['sheet', VOLS.indexOf(50)], ['sheet', D.today], ['erp', D.today], ['cloud', D.today], ['tier1', D.today], ['cloud', VOLS.indexOf(900)]];
  var S = { o: 'sheet', all: false, v: TOUR[0][1] }, hour = reduce ? 7.9 : 0;
  var tourOn = !reduce, tourK = 0, tourT = 0, pauseT = 0;
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function money(n) { return '$' + (n >= 10000 ? Math.round(n / 1000) + 'k' : fmt(n)); }
  function hm(h) { var m = 6 * 60 + Math.round(Math.min(h, DAY_H) * 60); return ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2); }
  function R(o, v) { return D.R[o][v]; }                         /* [total, per order, floor people, errors a day, accuracy, floor min an order] */
  function oi(o) { return OPTS.indexOf(o); }
  var rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })(7);

  /* ----- locations ----- */
  var LOC = [], r, b, s, k;
  for (r = 0; r < D.rows.length; r++) for (b = 0; b < D.bays; b++) for (s = 0; s < D.perBay; s++) for (k = 0; k < D.levels.length; k++) {
    if (rnd() < 0.86) LOC.push({ x: D.x0 + b * D.bayW + (s + 0.5) * D.bayW / D.perBay, y: D.levels[k] + D.beam, z: D.rows[r], az: D.aisles[D.rowAisle[r]], k: k });
  }
  var NL = LOC.length, ORDER = LOC.map(function (_, i) { return i; }).sort(function () { return rnd() - 0.5; });
  var WALK_X = 12.8, PACK = [12.5, 40.5], DESK = [5.2, 0, 35.2];

  /* ----- one simulation per system ----- */
  var SIM = {};
  function resetSim(o) {
    var x = SIM[o], acc = R(o, S.v)[4], nWrong = Math.round(NL * (1 - acc)), i;
    x.st = new Uint8Array(NL); for (i = 0; i < nWrong; i++) x.st[ORDER[i]] = 2;
    x.stale = []; x.pile = 0; x.keyed = 0; x.err = 0; x.touchAcc = 0; x.dirty = true; x.flash = new Float32Array(NL);
    var n = Math.min(26, R(o, S.v)[2]);
    x.pk.forEach(function (p, j) { p.on = j < n; p.route = null; p.x = PACK[0] - 1 - (j % 5) * 0.9; p.z = PACK[1] + Math.floor(j / 5) * 0.9; p.wait = j * 0.35; });
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, pivot, model, ok = !!T, running = false;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('wh3d7-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.wh3d-drag').style.display = 'none'; }
  function mat(c, o) { o = o || {}; return new T.MeshLambertMaterial({ color: c, transparent: !!o.op, opacity: o.op || 1, depthWrite: !o.op }); }
  var CX = D.bld[0] / 2, CZ = D.bld[1] / 2, C_OK, C_STALE, C_BAD, C_HI, pileMesh, monitor, monMat, palGeo, m4, q, sc, ps;
  function build() {
    scene = new T.Scene(); camera = new T.PerspectiveCamera(30, 1, 1, 600);
    scene.add(new T.HemisphereLight(0xe6efff, 0x223048, 0.95));
    var key = new T.DirectionalLight(0xffffff, 0.7); key.position.set(-30, 60, 40); scene.add(key);
    pivot = new T.Group(); pivot.rotation.order = 'YXZ'; scene.add(pivot); model = new T.Group(); model.position.set(-CX, 0, -CZ); pivot.add(model);
    var BX = D.bld[0], BZ = D.bld[1], ROWS = D.rows, BAYS = D.bays, BW = D.bayW, X0 = D.x0, LV = D.levels, BEAM = D.beam, i, rr, bb, kk, f, n = 0;
    function box(w, h, d, x, y, z, m) { var o = new T.Mesh(new T.BoxGeometry(w, h, d), m); o.position.set(x, y + h / 2, z); model.add(o); return o; }
    box(BX, 0.2, BZ, BX / 2, -0.2, BZ / 2, mat(0x2a3446));
    var wall = mat(0x4b5b74, { op: 0.5 });
    box(BX, 1.2, 0.25, BX / 2, 0, 0, wall); box(0.25, 1.2, BZ, 0, 0, BZ / 2, wall); box(0.25, 1.2, BZ, BX, 0, BZ / 2, wall); box(BX, 1.2, 0.25, BX / 2, 0, BZ, wall);
    for (i = 0; i < 6; i++) box(0.3, 3.2, 3.0, -0.05, 0, 6 + i * 4.2, mat(i < 4 ? 0x8dc63f : 0xFF8A3D));
    var shelf = mat(0x56688a); for (i = 0; i < 7; i++) box(40, 2.4, 1.0, 44, 0, 35.5 + i * 2.3, shelf);
    for (i = 0; i < 4; i++) box(2.4, 0.95, 1.2, 6 + i * 3.2, 0, 46.5, mat(0xA7B6CC));
    /* office: desk, monitor and the pile of pick lists */
    box(4.2, 0.9, 2.0, DESK[0], 0, DESK[2], mat(0x8a6a4a));
    monMat = new T.MeshBasicMaterial({ color: 0x1b4f6b }); monitor = box(1.6, 1.0, 0.12, DESK[0] - 0.8, 0.95, DESK[2] - 0.6, monMat);
    pileMesh = box(0.9, 1, 1.2, DESK[0] + 1.1, 0.9, DESK[2] + 0.1, new T.MeshLambertMaterial({ color: 0xffffff })); pileMesh.scale.y = 0.001;
    q = new T.Quaternion(); sc = new T.Vector3(); ps = new T.Vector3(); m4 = new T.Matrix4();
    var up = new T.InstancedMesh(new T.BoxGeometry(0.09, 1, 0.09), mat(0x3d6fb3, { op: 0.5 }), ROWS.length * (BAYS + 1) * 2);
    var topH = LV[LV.length - 1] + 0.2;
    for (rr = 0; rr < ROWS.length; rr++) for (bb = 0; bb <= BAYS; bb++) for (kk = -1; kk <= 1; kk += 2) { ps.set(X0 + bb * BW, topH / 2, ROWS[rr] + kk * D.rowD / 2); sc.set(1, topH, 1); m4.compose(ps, q, sc); up.setMatrixAt(n++, m4); }
    model.add(up);
    var bm = new T.InstancedMesh(new T.BoxGeometry(1, BEAM, 0.06), mat(0xE8862A, { op: 0.4 }), ROWS.length * BAYS * (LV.length - 1) * 2); n = 0;
    for (rr = 0; rr < ROWS.length; rr++) for (bb = 0; bb < BAYS; bb++) for (kk = 1; kk < LV.length; kk++) for (f = -1; f <= 1; f += 2) { ps.set(X0 + (bb + 0.5) * BW, LV[kk] + BEAM / 2, ROWS[rr] + f * D.rowD / 2); sc.set(BW - 0.09, 1, 1); m4.compose(ps, q, sc); bm.setMatrixAt(n++, m4); }
    model.add(bm);
    C_OK = new T.Color(0x5D7FA8); C_STALE = new T.Color(0xB9C2CE); C_BAD = new T.Color(0xFF5A4A); C_HI = new T.Color(0x5FE3FF);
    palGeo = new T.BoxGeometry(BW / D.perBay - 0.25, 1.25, D.rowD * 0.9);
    var body = new T.CylinderGeometry(0.42, 0.45, 1.5, 12), head = new T.SphereGeometry(0.34, 12, 10), sheet = new T.BoxGeometry(0.75, 0.05, 0.95), scan = new T.BoxGeometry(0.3, 0.3, 0.5), spark = new T.SphereGeometry(0.42, 10, 8), ringGeo = new T.RingGeometry(0.55, 0.85, 20);
    OPTS.forEach(function (o) {
      var pal = new T.InstancedMesh(palGeo, new T.MeshLambertMaterial({ color: 0xffffff }), NL);
      LOC.forEach(function (L, j) { ps.set(L.x, L.y + 0.64, L.z); sc.set(1, 1, 1); m4.compose(ps, q, sc); pal.setMatrixAt(j, m4); pal.setColorAt(j, C_OK); });
      model.add(pal);
      var pk = [];
      for (var j = 0; j < 26; j++) {
        var g = new T.Group();
        /* solid figure where it can be seen, a faint outline where a rack is in front of it, and a ring on the floor under it */
        var ghost = function (c) { return new T.MeshBasicMaterial({ color: c, depthTest: false, depthWrite: false, transparent: true, opacity: 0.22 }); };
        var bo = new T.Mesh(body, new T.MeshLambertMaterial({ color: 0x3f86e8 })); bo.position.y = 0.75; g.add(bo);
        var hd = new T.Mesh(head, new T.MeshLambertMaterial({ color: 0xF2D1B3 })); hd.position.y = 1.8; g.add(hd);
        var gb = new T.Mesh(body, ghost(0x7fb6ff)); gb.position.y = 0.75; gb.renderOrder = 10; g.add(gb);
        var gh = new T.Mesh(head, ghost(0xF2D1B3)); gh.position.y = 1.8; gh.renderOrder = 10; g.add(gh);
        var ring = new T.Mesh(ringGeo, new T.MeshBasicMaterial({ color: 0x5FE3FF, transparent: true, opacity: 0.55, depthWrite: false })); ring.rotation.x = -Math.PI / 2; ring.position.y = 0.04; g.add(ring);
        var tool = o === 'sheet' ? new T.Mesh(sheet, new T.MeshBasicMaterial({ color: 0xffffff })) : new T.Mesh(scan, new T.MeshBasicMaterial({ color: 0x5FE3FF }));
        tool.position.set(0.55, 1.2, 0); g.add(tool);
        g.scale.setScalar(1.7); g.visible = false; model.add(g);
        pk.push({ g: g, on: false, x: 0, z: 0, route: null, wait: 0 });
      }
      var sp = [];
      for (j = 0; j < 40; j++) { var m = new T.Mesh(o === 'sheet' ? sheet : spark, new T.MeshBasicMaterial({ color: o === 'sheet' ? 0xffffff : 0x5FE3FF, depthTest: false, transparent: true })); m.renderOrder = 13; m.scale.setScalar(1.6); m.visible = false; model.add(m); sp.push({ m: m, t: 1, a: [0, 0, 0] }); }
      SIM[o] = { pal: pal, pk: pk, sp: sp };
    });
  }
  if (!ok) OPTS.forEach(function (o) { SIM[o] = { pk: [], sp: [] }; });

  /* ----- day simulation ----- */
  var lagH = {}; OPTS.forEach(function (o, i) { lagH[o] = D.lagH[i]; });
  function touch(x, o, j, now) {
    if (x.st[j] === 2) return;
    if (lagH[o] > 0 && x.st[j] === 0) { x.st[j] = 1; x.stale.push([j, now]); x.dirty = true; }
  }
  function emit(x, o, from) {
    for (var i = 0; i < x.sp.length; i++) if (x.sp[i].t >= 1) {
      var p = x.sp[i]; p.t = 0; p.a = from; p.b = o === 'sheet' ? [DESK[0] + 1.1, 1.0 + Math.min(1.6, x.pile * 0.03), DESK[2] + 0.1] : [DESK[0] - 0.8, 1.45, DESK[2] - 0.6]; p.m.visible = true; return;
    }
  }
  function newRoute(p) {                                         /* one aisle a trip: in, two or three picks along it, back out */
    var a = Math.floor(rnd() * D.aisles.length), az = D.aisles[a], cand = [], i;
    for (i = 0; i < 40 && cand.length < 2 + (rnd() < 0.5 ? 1 : 0); i++) { var j = Math.floor(rnd() * NL); if (LOC[j].az === az) cand.push(j); }
    if (!cand.length) cand.push(Math.floor(rnd() * NL));
    cand.sort(function (u, w) { return LOC[u].x - LOC[w].x; });
    var pts = [[WALK_X, PACK[1] - 4], [WALK_X, LOC[cand[0]].az]];
    cand.forEach(function (j) { pts.push([LOC[j].x, LOC[j].az, j]); });
    pts.push([WALK_X, LOC[cand[0]].az], [WALK_X, PACK[1] - 4], [PACK[0] + (rnd() - 0.5) * 3, PACK[1] + (rnd() - 0.5) * 2, -1]);
    p.route = pts; p.leg = 0;
  }
  function step(o, dt, simH) {
    var x = SIM[o], spd = 30, now = hour;
    var vol = VOLS[S.v], touchRate = vol * D.lines * 0.6 / DAY_H;           /* locations touched an hour */
    x.err += R(o, S.v)[3] * simH / DAY_H;
    if (hour < 8) {
      x.touchAcc += touchRate * simH;
      while (x.touchAcc >= 1) { x.touchAcc -= 1; touch(x, o, Math.floor(rnd() * NL), now); }
    }
    /* records catch up: within minutes for scanners; keyed in from 14:00 on paper */
    if (lagH[o] > 0 && lagH[o] < 1) { while (x.stale.length && now - x.stale[0][1] > lagH[o] + 0.05 * rnd()) { var j0 = x.stale.shift()[0]; if (x.st[j0] === 1) { x.st[j0] = 0; x.dirty = true; } } }
    if (lagH[o] >= 1 && hour >= 8) {
      var share = Math.min(1, (hour - 8) / 0.45), keep = Math.round(x.stale.length * (1 - share));
      while (x.keyed < x.stale.length - keep) { var j1 = x.stale[x.keyed++][0]; if (x.st[j1] === 1) { x.st[j1] = 0; x.dirty = true; } }
      x.pileShow = x.pile * (1 - share);
    } else x.pileShow = x.pile;
    x.pk.forEach(function (p) {
      if (!p.on) return;
      if (p.wait > 0) { p.wait -= dt; return; }
      if (hour >= 8) return;                                       /* the shift's picking is done; the office keys in */
      if (!p.route) newRoute(p);
      var tgt = p.route[p.leg], dx = tgt[0] - p.x, dz = tgt[1] - p.z, d = Math.sqrt(dx * dx + dz * dz), mv = spd * dt;
      if (d <= mv) {
        p.x = tgt[0]; p.z = tgt[1];
        if (tgt.length > 2 && tgt[2] >= 0) {                        /* a pick */
          var j = tgt[2]; x.flash[j] = 1; x.dirty = true; touch(x, o, j, now); p.wait = 0.35;
          if (o !== 'sheet') emit(x, o, [p.x, 2.2, p.z]);
        }
        if (tgt.length > 2 && tgt[2] === -1) { p.route = null; p.wait = 0.4; if (o === 'sheet') { x.pile++; emit(x, o, [p.x, 2.0, p.z]); } return; }
        p.leg++;
      } else { p.x += dx / d * mv; p.z += dz / d * mv; p.g.rotation.y = Math.atan2(dx, dz); }
    });
  }
  function draw(o, dt) {
    var x = SIM[o];
    x.pk.forEach(function (p) { p.g.visible = p.on; p.g.position.set(p.x, 0, p.z); });
    x.sp.forEach(function (p) {
      if (p.t >= 1) { p.m.visible = false; return; }
      p.t = Math.min(1, p.t + dt / 0.8); var t = p.t, a = p.a, bb = p.b;
      p.m.position.set(a[0] + (bb[0] - a[0]) * t, a[1] + (bb[1] - a[1]) * t + Math.sin(Math.PI * t) * 7, a[2] + (bb[2] - a[2]) * t);
      if (t >= 1) { p.m.visible = false; if (o !== 'sheet') x.mon = 1; }
    });
    if (x.dirty || x.flashing) {
      var any = false, col = new T.Color();
      for (var j = 0; j < NL; j++) {
        var base = x.st[j] === 2 ? C_BAD : x.st[j] === 1 ? C_STALE : C_OK;
        if (x.flash[j] > 0) { x.flash[j] = Math.max(0, x.flash[j] - dt * 1.6); col.copy(base).lerp(C_HI, x.flash[j]); x.pal.setColorAt(j, col); any = true; }
        else if (x.dirty) x.pal.setColorAt(j, base);
      }
      x.pal.instanceColor.needsUpdate = true; x.dirty = false; x.flashing = any;
      if (any) x.dirty = true;
    }
    x.mon = Math.max(0, (x.mon || 0) - dt * 2.5);
  }
  function showOnly(o) {
    OPTS.forEach(function (q2) { var x = SIM[q2], on = q2 === o; x.pal.visible = on; x.pk.forEach(function (p) { p.g.visible = on && p.on; }); x.sp.forEach(function (p) { p.m.visible = on && p.t < 1; }); });
    var x = SIM[o]; pileMesh.scale.y = Math.max(0.001, Math.min(1.8, (x.pileShow || 0) * 0.03)); pileMesh.position.y = 0.9 + pileMesh.scale.y / 2;
    monMat.color.setHex(o === 'sheet' ? 0x1b4f6b : 0x1b4f6b).lerp(C_HI, o === 'sheet' ? 0 : 0.35 + 0.65 * (x.mon || 0));
  }

  /* ----- labels ----- */
  var LBL = [{ id: 'office', p: [DESK[0], 3.8, DESK[2]] }, { id: 'pack', p: [10.5, 3.4, 46.5] }, { id: 'racks', p: [42, 9.6, 16] }].map(function (l) { var el = document.createElement('span'); el.className = 'wh3d-label'; stage.appendChild(el); l.el = el; return l; });
  var quads = OPTS.map(function (o, i) { var el = document.createElement('span'); el.className = 'wh3d2-q'; el.textContent = D.onames[i]; el.style.setProperty('--c', ['#FF6B5A', '#F5A032', '#8DC63F', '#B07CFF'][i]); stage.appendChild(el); return el; });
  var Wd = 0, Hd = 0, v3 = ok ? new T.Vector3() : null;
  function counts(o) { var x = SIM[o], st = 0, bad = 0; for (var j = 0; j < NL; j++) { if (x.st[j] === 1) st++; else if (x.st[j] === 2) bad++; } return [st, bad]; }
  function placeLabels(o) {
    var x = SIM[o], c = counts(o), boxes = [];
    LBL.forEach(function (l) {
      if (S.all) { l.el.style.display = 'none'; return; }
      l.el.style.display = '';
      if (l.id === 'office') l.el.textContent = o === 'sheet' ? (hour >= 8 ? 'Office · keying in ' + Math.round(x.pileShow) + ' pick lists' : 'Office · ' + x.pile + ' pick lists to key in') : 'Office · system live';
      else if (l.id === 'pack') { var ne = Math.floor(x.err); l.el.textContent = 'Packing · ' + ne + ' wrong order' + (ne === 1 ? '' : 's') + ' shipped today'; }
      else l.el.textContent = c[0] + ' not in the system yet · ' + c[1] + ' wrong';
      l.el.classList.toggle('is-red', l.id === 'racks' && c[0] + c[1] > NL * 0.1);
      v3.set(l.p[0], l.p[1], l.p[2]); model.localToWorld(v3); v3.project(camera);
      var w = l.el.offsetWidth, hh = l.el.offsetHeight;
      boxes.push({ el: l.el, w: w, h: hh, x: Math.max(6, Math.min(Wd - w - 6, (v3.x * 0.5 + 0.5) * Wd - w / 2)), y: Math.max(36, Math.min(Hd - hh - 6, (-v3.y * 0.5 + 0.5) * Hd - hh / 2)) });
    });
    boxes.sort(function (a, b2) { return a.y - b2.y; });
    for (var i = 0; i < boxes.length; i++) for (var j = 0; j < i; j++) { var a = boxes[i], bq = boxes[j]; if (a.x < bq.x + bq.w + 4 && bq.x < a.x + a.w + 4 && a.y < bq.y + bq.h + 3 && bq.y < a.y + a.h + 3) a.y = bq.y + bq.h + 3; }
    boxes.forEach(function (qq) { qq.el.style.transform = 'translate(' + qq.x.toFixed(1) + 'px,' + Math.min(Hd - qq.h - 6, qq.y).toFixed(1) + 'px)'; });
  }

  /* ----- panel ----- */
  var SAY = {
    sheet: 'Paper and a spreadsheet: each pick list goes back to the office and waits to be keyed in at the end of the shift. All day the grey pallets are stock the system thinks is still there.',
    erp: 'The ERP module with scanners: each pick is scanned and reaches the records within minutes. Fewer errors and far less keying, but the work is still planned by people.',
    cloud: 'A cloud WMS: every move is scanned and the records are right within seconds. The system also directs the work, so fewer people walk less.',
    tier1: 'An enterprise WMS does the same job on the floor. At SME volumes its software, integrator and IT costs outweigh what it adds.'
  };
  function cell(id, f) { var el = $(id); el.style.fontSize = S.all ? '14px' : ''; el.style.whiteSpace = S.all ? 'normal' : ''; el.textContent = S.all ? OPTS.map(f).join(' · ') : f(S.o); }
  function best(v) { var m = OPTS[0]; OPTS.forEach(function (o) { if (R(o, v)[0] < R(m, v)[0]) m = o; }); return m; }
  function ui() {
    var v = S.v;
    cell('wh3d7-cost', function (o) { return money(R(o, v)[0]); });
    cell('wh3d7-cpo', function (o) { return '$' + R(o, v)[1].toFixed(2); });
    cell('wh3d7-ppl', function (o) { return String(R(o, v)[2]); });
    cell('wh3d7-err', function (o) { return R(o, v)[3].toFixed(R(o, v)[3] < 1 ? 2 : 1); });
    cell('wh3d7-acc', function (o) { var a = R(o, v)[4]; return (a < 0.99 ? Math.round(a * 100) : (a * 100).toFixed(1)) + '%'; });
    cell('wh3d7-lag', function (o) { return D.lag[oi(o)]; });
    fig.querySelectorAll('[data-o]').forEach(function (bt) { var x = bt.getAttribute('data-o'); bt.setAttribute('aria-pressed', (x === 'all' ? S.all : !S.all && x === S.o) ? 'true' : 'false'); });
    fig.querySelectorAll('[data-v]').forEach(function (bt) { bt.setAttribute('aria-pressed', +bt.getAttribute('data-v') === v ? 'true' : 'false'); });
    var bo = best(v);
    $('wh3d7-cv').textContent = VOLS[v] + ' orders a day · cheapest: ' + D.onames[oi(bo)];
    $('wh3d7-say').textContent = S.all ? 'All four systems on the same day at ' + VOLS[v] + ' orders a day. Compare the grey and red pallets: what each system does not know. At this volume the cheapest is ' + D.onames[oi(bo)] + '.' : SAY[S.o];
    chart();
  }
  var CCOL = { sheet: '#FF6B5A', erp: '#F5A032', cloud: '#8DC63F', tier1: '#B07CFF' };
  function cx(vol) { return 4 + (vol - 50) / 1150 * 592; }
  function cy(c) { return 86 - (Math.min(14, Math.max(5, c)) - 5) / 9 * 82; }
  function chart() {
    var s = '', xc = cx(VOLS[S.v]).toFixed(1);
    s += '<line x1="' + xc + '" y1="0" x2="' + xc + '" y2="90" stroke="#FFE27A" stroke-width="2" vector-effect="non-scaling-stroke"/>';
    (S.all ? OPTS : OPTS).forEach(function (o) {
      var pts = VOLS.map(function (vol, i) { return cx(vol).toFixed(1) + ',' + cy(R(o, i)[1]).toFixed(1); }).join(' ');
      s += '<polyline points="' + pts + '" fill="none" stroke="' + CCOL[o] + '" stroke-width="' + (S.all || o === S.o ? 2.4 : 1.2) + '" opacity="' + (S.all || o === S.o ? 1 : 0.45) + '" vector-effect="non-scaling-stroke"/>';
    });
    $('wh3d7-csvg').innerHTML = s;
  }
  function setVol(v) { S.v = v; hour = 0; OPTS.forEach(resetSim); ui(); if (!running) render(0); }
  $('wh3d7-csvg').addEventListener('click', function (e) {
    var rc = this.getBoundingClientRect(), vol = 50 + (e.clientX - rc.left) / rc.width * 1150, bi = 0;
    VOLS.forEach(function (x, i) { if (Math.abs(x - vol) < Math.abs(VOLS[bi] - vol)) bi = i; });
    tourOn = false; pauseT = 0; setVol(bi);
  });
  fig.querySelectorAll('[data-o]').forEach(function (bt) { bt.addEventListener('click', function () { var x = bt.getAttribute('data-o'); if (x === 'all') S.all = true; else { S.all = false; S.o = x; } tourOn = false; pauseT = 0; ui(); if (!running) render(0); }); });
  fig.querySelectorAll('[data-v]').forEach(function (bt) { bt.addEventListener('click', function () { tourOn = false; pauseT = 0; setVol(+bt.getAttribute('data-v')); }); });
  var tb = $('wh3d7-tour'), tbFill = tb.querySelector('i'), tbText = tb.querySelector('span'), tbLast = '';
  function tourBar() {
    var txt;
    if (tourOn) { tbFill.style.width = (Math.min(1, tourT / DAY_S) * 100).toFixed(1) + '%'; txt = 'Touring ' + (tourK + 1) + ' of ' + TOUR.length + ' · next in ' + Math.max(1, Math.ceil(DAY_S - tourT)) + ' s · pick a system or volume to stay'; }
    else { tbFill.style.width = '0%'; txt = 'Staying here · the tour resumes after a minute without clicks'; }
    if (txt !== tbLast) { tbLast = txt; tbText.textContent = txt; }
  }
  function goTour(k2) { tourK = k2; S.o = TOUR[k2][0]; S.all = false; setVol(TOUR[k2][1]); }

  /* ----- view ----- */
  var yawU = 0.5, pitchU = 1.18, yaw = yawU, pitch = pitchU, idle = 99, clock = 0;
  function resize() { var rc = stage.getBoundingClientRect(); Wd = rc.width; Hd = rc.height; if (!ok) return; renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(Wd, Hd, false); }
  function aim(w, h) { camera.aspect = w / h; var dist = Math.max(60, (S.all ? 34 : 40) / (Math.tan(15 * Math.PI / 180) * Math.min(1.6, w / h))); camera.position.set(0, 0, dist); camera.lookAt(0, 0, 0); camera.updateProjectionMatrix(); }
  var lastLab = 0;
  function render(dt) {
    $('wh3d7-chip').textContent = VOLS[S.v] + ' orders a day · ' + hm(hour) + (hour >= 8 && (S.all || S.o === 'sheet') ? ' · keying in' : '');
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0); pivot.position.set(0, -3, 0);
    OPTS.forEach(function (o) { draw(o, dt); });
    renderer.setScissorTest(false); renderer.setViewport(0, 0, Wd, Hd); renderer.clear();
    if (!S.all) { showOnly(S.o); pivot.updateMatrixWorld(true); aim(Wd, Hd); renderer.render(scene, camera); quads.forEach(function (qd) { qd.style.display = 'none'; }); }
    else {
      renderer.setScissorTest(true); var hw = Wd / 2, hh = Hd / 2;
      OPTS.forEach(function (o, i) {
        var x = (i % 2) * hw, y = i < 2 ? hh : 0;
        showOnly(o); pivot.updateMatrixWorld(true);
        renderer.setViewport(x, y, hw, hh); renderer.setScissor(x, y, hw, hh); aim(hw, hh); renderer.render(scene, camera);
        var qd = quads[i]; qd.style.display = ''; qd.style.transform = 'translate(' + (x + 10) + 'px,' + ((i < 2 ? 0 : hh) + 34) + 'px)';
      });
      renderer.setScissorTest(false);
    }
    stage.classList.toggle('is-quad', S.all);
    if (clock - lastLab > 0.2 || !dt) { lastLab = clock; placeLabels(S.o); }
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
    var simH = dt * (DAY_H + 1) / DAY_S; hour += simH;
    if (ok) OPTS.forEach(function (o) { step(o, dt, simH); });
    if (hour >= DAY_H + 1) { hour = 0; OPTS.forEach(resetSim); }
    if (tourOn) { tourT += dt; if (tourT > DAY_S) { tourT = 0; goTour((tourK + 1) % TOUR.length); } }
    else { pauseT += dt; if (pauseT > 60 && idle > 60) { tourOn = true; tourT = 0; goTour(0); } }
    tourBar();
    var e = 1 - Math.exp(-dt * 8), sway = idle > 4 ? 0.08 * Math.sin(clock * 0.25) : 0;
    yaw += (yawU + sway - yaw) * e; pitch += (pitchU - pitch) * e;
    render(dt); requestAnimationFrame(frame);
  }
  function setRun(v) { if (reduce) return; if (v && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); } else if (!v) running = false; }
  if (ok) { build(); renderer.autoClear = false; stage.classList.add('is-live'); }
  if (ok) OPTS.forEach(resetSim);
  if (ok && reduce) { OPTS.forEach(function (o) { for (var i = 0; i < 400; i++) step(o, 0.05, 0.02); }); }
  resize(); ui(); tourBar(); render(0);
  window.addEventListener('resize', function () { resize(); if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
