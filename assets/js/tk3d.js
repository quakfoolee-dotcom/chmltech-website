/* Tank article: 3D model of T-101, a vertical atmospheric storage tank cut in half (needs three.js r128+ as
   window.THREE). Numbers follow the article: 4.0 m diameter, 6.0 m shell, 850 kg/m3, 6,250 kg/h to P-101, level
   settings HHLL 5.3 / HLL 5.0 / NLL 3.2 / LLL 1.2 / LLLL 0.8 m, one-foot method for the shell. The level is
   simulated with time speeded up (1 s = 10 min). Assumed: a 30 m3 delivery unloading at 30 m3/h. */
(function () {
  'use strict';
  var fig = document.getElementById('tk3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.tk3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.tk3d-lines');
  var inFeed = $('tk3d-feed'), inLevel = $('tk3d-level'), btnDel = $('tk3d-deliver'), btnAuto = $('tk3d-auto');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- the tank and its level settings ----- */
  var RT = 2.0, HT = 6.0, AREA = Math.PI * RT * RT, RHO = 850, G = 9.81, Q_DEL = 30, V_DEL = 30, HOURS_PER_S = 1 / 6;
  var HH = 5.3, HI = 5.0, NL = 3.2, LO = 1.2, LL = 0.8;
  var LEVELS = [['HHLL', HH, 'trip', '#FF7A5C'], ['HLL', HI, 'alarm', '#FFB347'], ['NLL', NL, 'normal', '#5EC8FF'], ['LLL', LO, 'alarm', '#FFB347'], ['LLLL', LL, 'trip', '#FF7A5C']];
  var S = { h: NL, feed: 6250, deliv: 0, left: 0, inletTrip: false, pumpTrip: false, auto: true, t: 0, net: 0, qin: 0, qout: 0 };
  var hold = 0, uiClock = 9, lastKey = '';
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function hm(hr) { var m = Math.round(hr * 60); return Math.floor(m / 60) + ' h ' + ('0' + m % 60).slice(-2) + ' min'; }
  function sim(dt) {
    var dth = dt * HOURS_PER_S;
    S.qout = S.pumpTrip ? 0 : S.feed / RHO; S.qin = S.deliv > 0 && !S.inletTrip ? Q_DEL : 0; S.net = S.qin - S.qout;
    if (dth <= 0) return;
    if (S.qin > 0) { S.deliv -= S.qin * dth; if (S.deliv <= 0) S.deliv = 0; }
    S.h = Math.max(0.05, Math.min(HT - 0.05, S.h + S.net * dth / AREA)); S.t += dth;
    if (!S.inletTrip && S.h >= HH) { S.inletTrip = true; S.left = S.deliv; S.deliv = 0; }        /* high-high: close the inlet valve */
    else if (S.inletTrip && S.h < HI) { S.inletTrip = false; S.left = 0; }
    if (!S.pumpTrip && S.h <= LL) S.pumpTrip = true;                                               /* low-low: stop P-101 */
    else if (S.pumpTrip && S.h >= LO) S.pumpTrip = false;
    if (S.auto && S.h <= LO && S.deliv <= 0 && !S.inletTrip) S.deliv = V_DEL;                      /* low alarm: a delivery is arranged */
  }
  function ui(force) {
    var h = S.h, p = RHO * G * h / 1000, t = 4.9 * 4.0 * Math.max(0, h - 0.3) * 0.85 / 137 + 1.5, key, chip, txt, bad = false;
    $('tk3d-h').textContent = h.toFixed(2) + ' m'; $('tk3d-level-o').textContent = h.toFixed(2) + ' m'; $('tk3d-v').textContent = (AREA * h).toFixed(1) + ' m³';
    $('tk3d-p').textContent = p.toFixed(1) + ' kPa'; $('tk3d-t').textContent = t.toFixed(1) + ' mm'; $('tk3d-time').textContent = hm(S.t);
    $('tk3d-feed-o').textContent = fmt(S.feed) + ' kg/h';
    if (document.activeElement !== inLevel || hold <= 0) inLevel.value = h.toFixed(2);
    var nx = 'Level steady', tg = null, i;
    if (S.net < -1e-6) { for (i = 0; i < LEVELS.length; i++) if (LEVELS[i][1] < h - 0.005) { tg = LEVELS[i]; break; } }
    else if (S.net > 1e-6) { for (i = LEVELS.length - 1; i >= 0; i--) if (LEVELS[i][1] > h + 0.005) { tg = LEVELS[i]; break; } }
    if (tg) nx = tg[0] + ' in ' + hm(Math.abs(tg[1] - h) * AREA / Math.abs(S.net)); else if (Math.abs(S.net) > 1e-6) nx = S.net > 0 ? 'Filling' : 'Emptying';
    $('tk3d-next').textContent = nx;
    if (S.pumpTrip) { key = 'llll'; chip = 'Low-low trip'; bad = true; txt = 'Low-low trip at 0.8 m: P-101 has stopped before it loses suction. It restarts once the level is back above the low alarm.'; }
    else if (S.inletTrip) { key = 'hhll'; chip = 'High-high trip'; bad = true; txt = 'High-high trip at 5.3 m: the inlet valve has closed to prevent an overfill.' + (S.left > 0.5 ? ' The delivery did not fit: ' + S.left.toFixed(0) + ' m³ is still on the tanker.' : ''); }
    else if (h >= HI) { key = 'hll'; chip = 'High alarm'; bad = true; txt = 'High alarm at 5.0 m: time to stop filling. The gap to the trip at 5.3 m is the time operators have to act.'; }
    else if (h <= LO && S.qin > 0) { key = 'filllow'; chip = 'Tanker unloading'; txt = 'Low alarm at 1.2 m, and a delivery has been arranged. The tanker is unloading and the level is recovering.'; }
    else if (h <= LO) { key = 'lll'; chip = 'Low alarm'; bad = true; txt = 'Low alarm at 1.2 m: arrange a delivery or reduce the rate. The low-low trip at 0.8 m is next.'; }
    else if (S.qin > 0) { key = 'fill'; chip = 'Tanker unloading'; txt = 'A tanker is unloading at 30 m³/h. The level rises, and the vent breathes out the vapour the liquid displaces.'; }
    else if (S.feed <= 0) { key = 'hold'; chip = 'No feed to the plant'; txt = 'Feed to the plant is stopped, so the level holds steady.'; }
    else { key = 'normal'; chip = 'Normal operation'; txt = 'Normal operation. The tank feeds P-101 at ' + fmt(S.feed) + ' kg/h, and each metre of level is about ' + Math.round(AREA * RHO / S.feed * 60) + ' minutes of feed.'; }
    if (key + txt !== lastKey) { lastKey = key + txt; $('tk3d-say').textContent = txt; var c = $('tk3d-chip'); c.textContent = chip; c.classList.toggle('is-bad', bad); }
    var busy = S.deliv > 0 && !S.inletTrip, blocked = S.inletTrip;    /* the delivery button reports what it is doing */
    btnDel.classList.toggle('is-busy', busy); btnDel.classList.toggle('is-blocked', blocked); btnDel.setAttribute('aria-disabled', busy || blocked ? 'true' : 'false');
    btnDel.style.setProperty('--done', busy ? ((1 - S.deliv / V_DEL) * 100).toFixed(0) + '%' : '0%');
    $('tk3d-deliver-t').textContent = blocked ? 'Delivery blocked by the high-high trip' : busy ? 'Tanker unloading: ' + S.deliv.toFixed(0) + ' m³ left' : 'Start a tanker delivery (30 m³)';
    var on = [h >= HH - 0.005 || S.inletTrip, h >= HI, false, h <= LO, h <= LL + 0.005 || S.pumpTrip];
    levels.forEach(function (l, k) { if (l.on !== on[k]) { l.on = on[k]; l.el.classList.toggle('is-on', on[k]); } });
    var narrow = !wideNow, a;
    a = S.net > 0.05 ? 'breathing out' : S.net < -0.05 ? 'breathing in' : 'still'; setTag('vent', 'Vent · ' + a);
    setTag('inlet', S.inletTrip ? (narrow ? 'Inlet tripped shut' : 'Inlet valve tripped shut') : S.qin > 0 ? (narrow ? 'Delivery · 30 m³/h' : 'Delivery in · 30 m³/h') : (narrow ? 'Inlet closed' : 'Delivery inlet · closed'));
    setTag('pump', S.pumpTrip ? (narrow ? 'P-101 tripped' : 'P-101 stopped by the low-low trip') : 'To P-101 · ' + fmt(S.feed) + ' kg/h');
    setTag('bot', (narrow ? 'Bottom · ' : 'Bottom of tank · ') + p.toFixed(1) + ' kPa');
  }
  function setTag(k, t) { var it = tags[k]; if (it.text !== t) { it.text = t; it.el.textContent = t; measured = false; } }
  /* pressure colour: blue at 0 through cyan, green and yellow to red at 50 kPa */
  var STOPS = [[0, 40, 70, 200], [12.5, 40, 190, 230], [25, 90, 210, 110], [37.5, 250, 210, 60], [50, 240, 70, 50]], rgb = [0, 0, 0];
  function presRGB(p, out) {
    p = Math.max(0, Math.min(50, p));
    for (var i = 1; i < STOPS.length; i++) if (p <= STOPS[i][0]) {
      var a = STOPS[i - 1], b = STOPS[i], u = (p - a[0]) / (b[0] - a[0]);
      out[0] = (a[1] + (b[1] - a[1]) * u) / 255; out[1] = (a[2] + (b[2] - a[2]) * u) / 255; out[2] = (a[3] + (b[3] - a[3]) * u) / 255; return out;
    }
    return out;
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, running = false;
  var liqBody, liqFace, liqTop, beam, actMat, spinner, sink = [], jet = [], trc, trcPos, trcCol, gas, gasPos, gasCol;
  var jetMesh, jetTex, foam, rings = [], spl, splPos, splCol, bub, bubPos, bubCol;
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('tk3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.tk3d-drag').style.display = 'none'; }
  var HALF0 = Math.PI / 2, HALF = Math.PI, YIN = 5.55, YOUT = 0.35, XV = 2.95, XVENT = -0.9, XLT = 0.55, RL = RT - 0.06;
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.6 : rough, metalness: metal == null ? 0.25 : metal, side: T.DoubleSide }); }
  function lathe(parent, outline, m, mCut, o) { /* solid of revolution about y from a closed (r, y) outline; by default the back half, closed with section faces */
    o = o || {};
    var g = new T.Group(), n = outline.length, phi0 = o.whole ? 0 : HALF0, len = o.whole ? Math.PI * 2 : HALF;
    for (var i = 0; i < n; i++) {
      var a = outline[i], b = outline[(i + 1) % n];
      if (a[0] === 0 && b[0] === 0) continue;
      g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(a[0], a[1]), new T.Vector2(b[0], b[1])], o.whole ? 64 : 44, phi0, len), m));
    }
    if (!o.whole && mCut) {
      var sg = new T.ShapeGeometry(new T.Shape(outline.map(function (p) { return new T.Vector2(p[0], p[1]); })));
      g.add(new T.Mesh(sg, mCut)); var c2 = new T.Mesh(sg, mCut); c2.scale.x = -1; g.add(c2);
    }
    parent.add(g); return g;
  }
  function rect(r0, r1, y0, y1) { return [[r0, y0], [r1, y0], [r1, y1], [r0, y1]]; }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.85));
    var key = new T.DirectionalLight(0xffffff, 0.85); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.4); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); scene.add(pivot);
    model = new T.Group(); model.position.set(-PIVX, -PIVY, 0); pivot.add(model);
    var steelM = mat(0x8a97aa), cut = mat(0xc6ced9, 0.95, 0), conc = mat(0x6d7786, 0.95, 0), dark = mat(0x3f4b5e, 0.7, 0.2), pipe = mat(0x7a879b), blue = mat(0x24528d, 0.5, 0.3);
    function box(w, h, d, x, y, z, m) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y, z); model.add(b); return b; }
    function cyl(r, len, x, y, z, axis, m, seg) { var c = new T.Mesh(new T.CylinderGeometry(r, r, len, seg || 20), m); if (axis === 'x') c.rotation.z = Math.PI / 2; if (axis === 'z') c.rotation.x = Math.PI / 2; c.position.set(x, y, z); model.add(c); return c; }

    /* ground, bund wall, foundation and tank */
    box(9.6, 0.12, 6.4, 1.3, -0.56, -0.2, conc);
    box(9.6, 0.95, 0.22, 1.3, -0.03, -3.3, conc); box(0.22, 0.95, 4.6, -3.4, -0.03, -1.0, conc); box(0.22, 0.95, 4.6, 6.0, -0.03, -1.0, conc);
    lathe(model, rect(0, RT + 0.32, -0.5, -0.07), conc, null, { whole: true });
    lathe(model, rect(0, RT + 0.12, -0.07, 0), steelM, null, { whole: true });
    lathe(model, rect(RT - 0.06, RT, 0, HT), steelM, cut);                                          /* shell: thickness exaggerated */
    lathe(model, [[0, HT + 0.5], [RT + 0.06, HT - 0.02], [RT + 0.06, HT + 0.04], [0, HT + 0.56]], steelM, cut);   /* cone roof */
    /* delivery line with its inlet valve; outlet to P-101; vent; level transmitter */
    cyl(0.13, 2.3, RT + 1.05, YIN, -0.02, 'x', pipe); cyl(0.2, 0.08, RT + 2.2, YIN, -0.02, 'x', pipe);
    var vb = new T.Mesh(new T.SphereGeometry(0.24, 24, 16), pipe); vb.position.set(XV, YIN, -0.02); model.add(vb);
    cyl(0.05, 0.5, XV, YIN + 0.4, -0.02, 'y', pipe, 10);
    actMat = mat(0x8a97aa, 0.5, 0.2); var ac = new T.Mesh(new T.CylinderGeometry(0.3, 0.3, 0.18, 28), actMat); ac.position.set(XV, YIN + 0.7, -0.02); model.add(ac);
    cyl(0.14, 1.5, RT + 0.7, YOUT, -0.02, 'x', pipe);
    cyl(0.42, 0.32, RT + 1.6, YOUT, -0.02, 'x', pipe, 32); cyl(0.09, 1.0, RT + 1.6, YOUT + 0.85, -0.02, 'y', pipe, 12);   /* P-101, simplified */
    cyl(0.15, 0.5, RT + 2.0, YOUT, -0.02, 'x', pipe); cyl(0.33, 0.95, RT + 2.75, YOUT, -0.02, 'x', blue, 28); box(1.9, 0.4, 0.9, RT + 2.2, -0.3, -0.02, dark);
    spinner = new T.Group(); spinner.position.set(RT + 2.24, YOUT, -0.02); model.add(spinner);
    var cp = new T.Mesh(new T.CylinderGeometry(0.2, 0.2, 0.1, 20), dark); cp.rotation.z = Math.PI / 2; spinner.add(cp);
    var mk = new T.Mesh(new T.BoxGeometry(0.11, 0.07, 0.42), new T.MeshBasicMaterial({ color: 0xffffff })); spinner.add(mk);
    cyl(0.1, 0.75, XVENT, HT + 0.62, -0.02, 'y', pipe, 14); var hood = new T.Mesh(new T.ConeGeometry(0.24, 0.16, 20), pipe); hood.position.set(XVENT, HT + 1.1, -0.02); model.add(hood);
    cyl(0.09, 0.3, XLT, HT + 0.5, -0.02, 'y', pipe, 12); box(0.3, 0.26, 0.24, XLT, HT + 0.75, -0.02, mat(0x8dc63f, 0.5, 0.2));
    beam = new T.Mesh(new T.CylinderGeometry(0.02, 0.2, 1, 20, 1, true), new T.MeshBasicMaterial({ color: 0x8dc63f, transparent: true, opacity: 0.16, depthWrite: false, side: T.DoubleSide })); beam.position.set(XLT, 0, -0.02); model.add(beam);

    /* liquid: a see-through body, a section face coloured by hydrostatic pressure, and the surface */
    var lg = lathe(model, rect(0, RL, 0, 1), new T.MeshBasicMaterial({ color: 0x2a78c8, transparent: true, opacity: 0.3, depthWrite: false, side: T.DoubleSide }), null); liqBody = lg;
    var fgm = new T.PlaneGeometry(2 * RL, 1, 1, 30); fgm.translate(0, 0.5, 0);
    fgm.setAttribute('color', new T.BufferAttribute(new Float32Array(fgm.attributes.position.count * 3), 3));
    liqFace = new T.Mesh(fgm, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.86, side: T.DoubleSide })); liqFace.position.z = -0.012; model.add(liqFace);
    liqTop = new T.Mesh(new T.CircleGeometry(RL, 48, 0, Math.PI), new T.MeshBasicMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.45, depthWrite: false, side: T.DoubleSide })); liqTop.rotation.x = -Math.PI / 2; model.add(liqTop);
    /* level settings: dashed lines across the section */
    LEVELS.forEach(function (l) {
      var g = new T.BufferGeometry().setFromPoints([new T.Vector3(-RL, l[1], 0.004), new T.Vector3(RL, l[1], 0.004)]);
      var ln = new T.Line(g, new T.LineDashedMaterial({ color: new T.Color(l[3]), dashSize: 0.14, gapSize: 0.1, transparent: true, opacity: 0.9 })); ln.computeLineDistances(); model.add(ln);
    });
    /* streamlines, redrawn as the level moves: liquid drawn down to the outlet, and the delivery falling in */
    var lmS = new T.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.9, blending: T.AdditiveBlending, depthWrite: false }), lmJ = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 }), i;
    function mk2(n, m) { var g = new T.BufferGeometry(), cl = new Float32Array(n * 3), k9; for (k9 = 0; k9 < n; k9++) cl[k9 * 3] = cl[k9 * 3 + 1] = cl[k9 * 3 + 2] = 0.75 * Math.pow(k9 / (n - 1), 1.3); g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute('color', new T.BufferAttribute(cl, 3));   /* lines fade in toward their end */ var ln = new T.Line(g, m); ln.frustumCulled = false; model.add(ln); return ln; }
    for (i = 0; i < NS; i++) sink.push({ line: mk2(NP, lmS), pts: new Float32Array(NP * 2), len: new Float32Array(NP), total: 1, tr: [0.1 + Math.random() * 0.15, 0.36 + Math.random() * 0.15, 0.62 + Math.random() * 0.15, 0.86 + Math.random() * 0.1] });
    for (i = 0; i < NJ; i++) jet.push({ line: mk2(NP, lmJ), pts: new Float32Array(NP * 2), len: new Float32Array(NP), total: 1, tr: [Math.random() * 0.2, 0.25 + Math.random() * 0.2, 0.5 + Math.random() * 0.2, 0.75 + Math.random() * 0.2] });
    var c2 = document.createElement('canvas'); c2.width = c2.height = 64; var x2 = c2.getContext('2d'), gr2 = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr2.addColorStop(0, 'rgba(255,255,255,1)'); gr2.addColorStop(0.3, 'rgba(255,255,255,.65)'); gr2.addColorStop(1, 'rgba(255,255,255,0)');
    x2.fillStyle = gr2; x2.fillRect(0, 0, 64, 64);
    var tex = new T.CanvasTexture(c2);
    function points(n, size) {
      var g = new T.BufferGeometry(), ps = new Float32Array(n * 3), cl = new Float32Array(n * 3);
      g.setAttribute('position', new T.BufferAttribute(ps, 3)); g.setAttribute('color', new T.BufferAttribute(cl, 3));
      var pt = new T.Points(g, new T.PointsMaterial({ size: size, map: tex, transparent: true, depthWrite: false, vertexColors: true, blending: T.AdditiveBlending, sizeAttenuation: true }));
      pt.frustumCulled = false; model.add(pt); return [pt, ps, cl];
    }
    /* the delivery stream: a solid jet of liquid that follows the real trajectory from the inlet (horizontal exit at
       about 1 m/s, then free fall) and thins as it speeds up. Its shape is recalculated as the level moves. */
    var sc = document.createElement('canvas'); sc.width = 256; sc.height = 32; var sg = sc.getContext('2d'), r2 = (function (s0) { return function () { s0 = (s0 * 16807) % 2147483647; return s0 / 2147483647; }; })(321);
    sg.fillStyle = '#c8c8c8'; sg.fillRect(0, 0, 256, 32);
    for (i = 0; i < 40; i++) { var ln0 = 24 + r2() * 70, a0 = r2() * 256, b0 = r2() * 32, lt = r2() > 0.3, w0;
      for (w0 = -1; w0 <= 1; w0++) { var gd = sg.createLinearGradient(a0 + w0 * 256, 0, a0 + w0 * 256 + ln0, 0), cc = lt ? '255,255,255' : '90,90,90';
        gd.addColorStop(0, 'rgba(' + cc + ',0)'); gd.addColorStop(0.5, 'rgba(' + cc + ',' + (0.3 + r2() * 0.5) + ')'); gd.addColorStop(1, 'rgba(' + cc + ',0)'); sg.fillStyle = gd; sg.fillRect(a0 + w0 * 256, b0, ln0, 2 + r2() * 5); } }
    jetTex = new T.CanvasTexture(sc); jetTex.wrapS = jetTex.wrapT = T.RepeatWrapping; jetTex.repeat.set(3, 1);
    var jg = new T.BufferGeometry(), jp = new Float32Array((JS + 1) * JR * 3), juv = new Float32Array((JS + 1) * JR * 2), jidx = [], a, b2;
    for (a = 0; a <= JS; a++) for (b2 = 0; b2 < JR; b2++) { juv[(a * JR + b2) * 2] = a / JS; juv[(a * JR + b2) * 2 + 1] = b2 / (JR - 1); }
    for (a = 0; a < JS; a++) for (b2 = 0; b2 < JR; b2++) { var v0 = a * JR + b2, v1 = a * JR + (b2 + 1) % JR, v2 = v0 + JR, v3n = v1 + JR; jidx.push(v0, v2, v1, v1, v2, v3n); }
    jg.setAttribute('position', new T.BufferAttribute(jp, 3)); jg.setAttribute('uv', new T.BufferAttribute(juv, 2)); jg.setIndex(jidx);
    jetMesh = new T.Mesh(jg, new T.MeshBasicMaterial({ color: 0x9fdcff, map: jetTex, transparent: true, opacity: 0.96, side: T.DoubleSide })); jetMesh.frustumCulled = false; model.add(jetMesh);
    foam = new T.Mesh(new T.CircleGeometry(1, 32, 0, Math.PI), new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.6, depthWrite: false, side: T.DoubleSide })); foam.rotation.x = -Math.PI / 2; model.add(foam);
    for (i = 0; i < 3; i++) { var rg = new T.Mesh(new T.RingGeometry(0.9, 1, 48, 1, 0, Math.PI), new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.4, depthWrite: false, side: T.DoubleSide })); rg.rotation.x = -Math.PI / 2; model.add(rg); rings.push({ m: rg, p: i / 3 }); }
    var q = points((NS + NJ) * 4 * TAIL, 0.13); trc = q[0]; trcPos = q[1]; trcCol = q[2];
    q = points(NSPL, 0.13); spl = q[0]; splPos = q[1]; splCol = q[2];
    q = points(NBUB, 0.16); bub = q[0]; bubPos = q[1]; bubCol = q[2];
    q = points(NGAS, 0.5); gas = q[0]; gasPos = q[1]; gasCol = q[2];
  }
  var NS = 9, NJ = 5, NP = 44, TAIL = 5, NGAS = 70, PIVX = 1.3, PIVY = 3.3, gasP = [], spin = 0;
  var JS = 30, JR = 12, NSPL = 60, NBUB = 110, V_JET = 1.06, R_JET = 0.125, splP = [], bubP = [], impact = { x: 1, t: 0.7, sub: false }, jetClock = 0;
  for (var i1 = 0; i1 < NSPL; i1++) splP.push({ on: false, x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0 });
  for (i1 = 0; i1 < NBUB; i1++) bubP.push({ on: false, x: 0, y: 0, z: 0, vx: 0, vy: 0, vz: 0 });
  for (var i0 = 0; i0 < NGAS; i0++) gasP.push({ t: Math.random(), a: Math.random() * 6.28, s: 0.5 + Math.random() * 0.8 });
  function setLine(l, k, x, y) { l.pts[k * 2] = x; l.pts[k * 2 + 1] = y; }
  function finish(l) {
    var pos = l.line.geometry.attributes.position, k;
    for (k = 0; k < NP; k++) { pos.setXYZ(k, l.pts[k * 2], l.pts[k * 2 + 1], -0.004); l.len[k] = k ? l.len[k - 1] + Math.hypot(l.pts[k * 2] - l.pts[k * 2 - 2], l.pts[k * 2 + 1] - l.pts[k * 2 - 1]) : 0; }
    l.total = l.len[NP - 1] || 1; pos.needsUpdate = true;
  }
  function shape() { /* everything that follows the level */
    var h = S.h, i, k, u, m, c0, c1, c2, c3;
    liqBody.scale.y = h; liqFace.scale.y = h; liqTop.position.y = h; beam.scale.y = HT + 0.35 - h; beam.position.y = h + (HT + 0.35 - h) / 2;
    var col = liqFace.geometry.attributes.color, ps = liqFace.geometry.attributes.position;
    for (k = 0; k < ps.count; k++) { presRGB(RHO * G * h * (1 - ps.getY(k)) / 1000, rgb); col.setXYZ(k, rgb[0], rgb[1], rgb[2]); }
    col.needsUpdate = true;
    for (i = 0; i < NS; i++) { /* only near the outlet does the liquid speed up: a short fan of lines converging on the nozzle */
      var ph = -0.48 + 1.95 * i / (NS - 1), RF = 0.66, xs = RL - RF * Math.cos(ph), y0 = Math.max(0.04, Math.min(h - 0.03, YOUT + RF * Math.sin(ph))), ya = Math.min(h - 0.03, YOUT - 0.09 + 0.18 * i / (NS - 1));
      for (k = 0; k < NP; k++) { u = k / (NP - 1); setLine(sink[i], k, xs + (RL - xs) * u, y0 + (ya - y0) * Math.pow(u, 0.8)); }
      finish(sink[i]);
    }
    /* where and when the falling stream meets the surface (free fall from the inlet height) */
    impact.sub = h >= YIN - 0.02; impact.t = impact.sub ? 0.06 : Math.sqrt(2 * (YIN - h) / G); impact.x = RL - V_JET * impact.t;
    for (i = 0; i < NJ; i++) { /* below the surface the delivery spreads as a plume */
      var sp = (i - 2) * 0.42, dep = Math.min(1.3, h * 0.7), xa = impact.x + (i - 2) * 0.02;
      for (k = 0; k < NP; k++) { u = k / (NP - 1); setLine(jet[i], k, xa - 0.32 * u - sp * u * u, h - 0.02 - dep * u * (1.4 - 0.4 * u)); }
      finish(jet[i]);
    }
  }
  function step(dt) {
    var ti = 0, sets = [[sink, S.qout / 7.35 * 0.5, 0], [jet, S.qin / 30 * 0.6, 0]], a, j, n, t, k, l, u, d, lo, hi, mid, fr;
    for (a = 0; a < 2; a++) for (j = 0; j < sets[a][0].length; j++) {
      l = sets[a][0][j]; l.line.visible = false; if (a === 1) l.line.visible = false;   /* plume lines under the delivery stream are switched off: the stream, bubbles and ripples show it */
      for (n = 0; n < 4; n++) {
        u = l.tr[n];
        for (t = 0; t < TAIL; t++) {
          var uu = u - t * 0.03, vis = (1 - t / TAIL) * sets[a][2]; if (uu < 0) { uu = 0; vis = 0; } vis *= Math.min(1, uu * 2.5);
          d = uu * l.total; lo = 0; hi = NP - 1;
          while (hi - lo > 1) { mid = (lo + hi) >> 1; if (l.len[mid] <= d) lo = mid; else hi = mid; }
          fr = (d - l.len[lo]) / Math.max(1e-6, l.len[hi] - l.len[lo]);
          k = ti * 3; trcPos[k] = l.pts[lo * 2] + (l.pts[hi * 2] - l.pts[lo * 2]) * fr; trcPos[k + 1] = l.pts[lo * 2 + 1] + (l.pts[hi * 2 + 1] - l.pts[lo * 2 + 1]) * fr; trcPos[k + 2] = -0.002;
          trcCol[k] = vis; trcCol[k + 1] = vis; trcCol[k + 2] = vis; ti++;
        }
        u += dt * sets[a][1] * (a === 0 ? 0.5 + 1.2 * u * u : 1); if (u >= 1) u -= 1; l.tr[n] = u;
      }
    }
    /* the falling stream: rings of the jet body follow the trajectory, thinning as the liquid speeds up, with a slight
       waver that grows on the way down. Splash, bubbles and ripples mark where it plunges into the liquid. */
    var filling = S.qin > 0, jp = jetMesh.geometry.attributes.position, sgn, tt, cx0, cy0, vy0, sp0, nx, ny, rj, wob, c, sn;
    jetClock += dt; jetMesh.visible = filling && !impact.sub; foam.visible = filling; 
    if (jetMesh.visible) {
      jetTex.offset.x -= dt * 2.4;
      for (a = 0; a <= JS; a++) {
        tt = impact.t * 1.04 * a / JS; vy0 = -G * tt; sp0 = Math.sqrt(V_JET * V_JET + vy0 * vy0); nx = -vy0 / sp0; ny = -V_JET / sp0;      /* unit normal in the plane of fall */
        rj = Math.max(0.058, R_JET * Math.sqrt(V_JET / sp0)); wob = 0.022 * Math.pow(a / JS, 2) * Math.sin(9 * tt * 6 - jetClock * 11);
        cx0 = RL + 0.04 - V_JET * tt + nx * wob; cy0 = YIN - 0.5 * G * tt * tt + ny * wob;
        for (j = 0; j < JR; j++) { c = Math.cos(j / JR * 6.2832); sn = Math.sin(j / JR * 6.2832); jp.setXYZ(a * JR + j, cx0 + nx * rj * c, Math.max(S.h - 0.03, cy0 + ny * rj * c), -0.02 + rj * sn); }
      }
      jp.needsUpdate = true;
    }
    foam.position.set(impact.x, S.h + 0.004, 0); foam.scale.setScalar(0.3 + 0.06 * Math.sin(jetClock * 17)); 
    for (a = 0; a < rings.length; a++) { var rgi = rings[a]; rgi.p += dt * 0.55; if (rgi.p > 1) rgi.p -= 1; rgi.m.visible = filling; rgi.m.position.set(impact.x, S.h + 0.005, 0); rgi.m.scale.setScalar(0.18 + 0.62 * rgi.p); rgi.m.material.opacity = 0.45 * (1 - rgi.p); }
    for (j = 0; j < NSPL; j++) { /* droplets thrown up by the impact */
      var d0 = splP[j]; k = j * 3;
      if (!d0.on) { if (filling && dt > 0 && Math.random() < dt * 1.2) { d0.on = true; d0.x = impact.x + (Math.random() - 0.5) * 0.12; d0.y = S.h + 0.02; d0.z = -0.02 - Math.random() * 0.1; d0.vx = (Math.random() - 0.55) * 1.6; d0.vy = 0.8 + Math.random() * 1.9; d0.vz = -Math.random() * 0.8; } }
      else { d0.vy -= G * dt; d0.x += d0.vx * dt; d0.y += d0.vy * dt; d0.z += d0.vz * dt; if (d0.y < S.h || Math.abs(d0.x) > RL) d0.on = false; }
      b = d0.on ? 0.9 : 0; splPos[k] = d0.x; splPos[k + 1] = d0.y; splPos[k + 2] = d0.z; splCol[k] = b; splCol[k + 1] = b; splCol[k + 2] = b;
    }
    for (j = 0; j < NBUB; j++) { /* air carried under by the stream, then rising back to the surface */
      var bb = bubP[j]; k = j * 3;
      if (!bb.on) { if (filling && dt > 0 && Math.random() < dt * 2.2) { bb.on = true; bb.x = impact.x + (Math.random() - 0.5) * 0.14; bb.y = S.h - 0.03; bb.z = -0.03 - Math.random() * 0.25; bb.vx = -0.15 + (Math.random() - 0.5) * 0.9; bb.vy = -(1.3 + Math.random() * 1.5); bb.vz = -Math.random() * 0.3; } }
      else { bb.vy += 3.6 * dt; bb.vx *= 1 - Math.min(1, dt * 1.2); bb.x += bb.vx * dt; bb.y += bb.vy * dt; bb.z += bb.vz * dt; if (bb.y > S.h - 0.015 || bb.y < 0.05 || Math.abs(bb.x) > RL - 0.03) bb.on = false; }
      b = bb.on ? 0.95 : 0; bubPos[k] = bb.x; bubPos[k + 1] = bb.y; bubPos[k + 2] = Math.min(-0.003, bb.z); bubCol[k] = b; bubCol[k + 1] = b; bubCol[k + 2] = b;
    }
    spl.geometry.attributes.position.needsUpdate = true; spl.geometry.attributes.color.needsUpdate = true;
    bub.geometry.attributes.position.needsUpdate = true; bub.geometry.attributes.color.needsUpdate = true;
    /* the vent breathes: out while the level rises, in while it falls */
    var dir = S.net > 0.05 ? 1 : S.net < -0.05 ? -1 : 0, rate = Math.min(1, 0.25 + Math.abs(S.net) / 30);
    for (j = 0; j < NGAS; j++) {
      var g = gasP[j]; k = j * 3; g.t += dt * dir * 0.45 * g.s * rate; if (g.t > 1) g.t -= 1; if (g.t < 0) g.t += 1;
      var rr = 0.12 + 0.55 * g.t, b = dir ? 0.24 * (1 - g.t) * Math.min(1, g.t * 8) : 0;
      gasPos[k] = XVENT + Math.cos(g.a) * rr * 1.1 - 0.25 * g.t * g.t; gasPos[k + 1] = HT + 1.05 + 1.25 * g.t; gasPos[k + 2] = -0.02 + Math.sin(g.a) * rr * 0.6;
      gasCol[k] = b; gasCol[k + 1] = b * 0.93; gasCol[k + 2] = b * 0.88;
    }
    if (!S.pumpTrip && S.feed > 0) { spin += dt * 9 * S.feed / 6250; spinner.rotation.x = -spin; }
    actMat.color.setHex(S.inletTrip ? 0xff7a5c : S.qin > 0 ? 0x8dc63f : 0x8a97aa);
    trc.geometry.attributes.position.needsUpdate = true; trc.geometry.attributes.color.needsUpdate = true;
    gas.geometry.attributes.position.needsUpdate = true; gas.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- level settings down the left; stream tags and part names in rows above and below ----- */
  var levels = LEVELS.map(function (l) {
    var el = document.createElement('span'); el.className = 'tk3d-level'; el.style.setProperty('--c', l[3]); stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'); path.setAttribute('class', 'lv'); path.style.stroke = l[3]; svg.appendChild(path);
    return { l: l, el: el, path: path, w: 0, h: 0, on: false };
  });
  var ITEMS = [
    ['t', 'Vent · still', XVENT, HT + 1.2, -0.02, 'T', 'vent'], ['l', 'Level transmitter', XLT, HT + 0.9, -0.02, 'T'], ['t', 'Delivery inlet · closed', XV, YIN + 0.82, -0.02, 'T', 'inlet'],
    ['t', 'Bottom of tank · 26.7 kPa', -0.7, 0.04, 0, 'B', 'bot'], ['t', 'To P-101 · 6,250 kg/h', RT + 2.3, YOUT - 0.3, 0.45, 'B', 'pump'], ['l', 'Bund wall', 5.3, 0.35, -3.2, 'B']
  ];
  var tags = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'tk3d-tag' : 'tk3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, x: 0, tag: n[0] === 't', text: n[1] };
    if (n[6]) tags[n[6]] = it; return it;
  });
  var W = 0, H = 0, measured = false, wideNow = true, v3 = T ? new T.Vector3() : null, lastWide = null;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function place() {
    if (lastWide !== wideNow) { lastWide = wideNow; levels.forEach(function (l) { l.el.textContent = wideNow ? l.l[0] + ' · ' + l.l[1].toFixed(1) + ' m · ' + l.l[2] : l.l[0] + ' ' + l.l[1].toFixed(1); }); measured = false; }
    if (!measured) { items.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); levels.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    var pt = { x: 0, y: 0 }, yPrev = -1e9, i, l;
    for (i = 0; i < levels.length; i++) { /* top to bottom, each level with the line it marks */
      l = levels[i]; toScreen(-RT, l.l[1], 0, pt);
      var yy = Math.max(pt.y, yPrev + l.h + 4); yPrev = yy; var lx = wideNow ? 12 : 6;
      l.el.style.transform = 'translate(' + lx + 'px,' + (yy - l.h / 2).toFixed(1) + 'px)';
      l.path.setAttribute('d', 'M' + (lx + l.w).toFixed(1) + ' ' + yy.toFixed(1) + 'L' + Math.max(lx + l.w + 6, pt.x - 14).toFixed(1) + ' ' + yy.toFixed(1) + 'L' + pt.x.toFixed(1) + ' ' + pt.y.toFixed(1));
    }
    ['T', 'B'].forEach(function (band) {
      var list = items.filter(function (q) { return q.n[5] === band && (q.tag || (wideNow && q.w > 0)); }), gap = 8, left = band === 'B' && wideNow ? 8 : 8;
      list.forEach(function (q) { toScreen(q.n[2], q.n[3], q.n[4], pt); q.ax = pt.x; q.ay = pt.y; q.x = pt.x; });
      list.sort(function (a, b) { return a.ax - b.ax; });
      for (i = 0; i < list.length; i++) { l = list[i]; l.x = Math.max(l.x, left + l.w / 2, i ? list[i - 1].x + (list[i - 1].w + l.w) / 2 + gap : -1e9); }
      for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.x = Math.min(l.x, W - 8 - l.w / 2, i < list.length - 1 ? list[i + 1].x - (list[i + 1].w + l.w) / 2 - gap : 1e9); }
      var by = band === 'T' ? 52 : H - 24;
      for (i = 0; i < list.length; i++) {
        l = list[i];
        l.el.style.transform = 'translate(' + (l.x - l.w / 2).toFixed(1) + 'px,' + (by - l.h / 2).toFixed(1) + 'px)';
        var lx2 = Math.max(l.x - l.w / 2 + 12, Math.min(l.x + l.w / 2 - 12, l.ax)), ly = band === 'T' ? by + l.h / 2 : by - l.h / 2;
        l.path.setAttribute('d', 'M' + l.ax.toFixed(1) + ' ' + l.ay.toFixed(1) + 'L' + lx2.toFixed(1) + ' ' + ly.toFixed(1));
        l.dot.setAttribute('cx', l.ax.toFixed(1)); l.dot.setAttribute('cy', l.ay.toFixed(1));
      }
    });
  }

  /* ----- view ----- */
  var yawUser = -0.24, pitchUser = 0.13, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var col = wideNow ? 150 : 62, px = Math.min((W - col - 24) / 9.8, (H - 150) / 8.6), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180)), cx = -(col / 2) / px;
    camera.aspect = W / H; camera.position.set(cx, 0.05, dist); camera.lookAt(cx, 0.05, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0);
    shape(); step(dt);
    pivot.updateMatrixWorld(true);
    renderer.render(scene, camera);
    place();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(-0.95, Math.min(0.95, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.15, Math.min(0.6, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  function still() { sim(0); ui(true); if (!running) render(0); }
  inFeed.addEventListener('input', function () { S.feed = parseFloat(inFeed.value); still(); });
  inLevel.addEventListener('input', function () { S.h = parseFloat(inLevel.value); S.deliv = 0; S.left = 0; S.inletTrip = S.h >= HH; S.pumpTrip = S.h <= LL; hold = 1.2; still(); });
  btnDel.addEventListener('click', function () { if (S.deliv <= 0 && !S.inletTrip) { S.deliv = V_DEL; if (reduce) { reduce = false; setRun(true); } still(); } });
  btnAuto.addEventListener('click', function () { S.auto = !S.auto; btnAuto.setAttribute('aria-checked', S.auto ? 'true' : 'false'); $('tk3d-auto-t').textContent = S.auto ? 'On' : 'Off'; still(); });
  $('tk3d-reset').addEventListener('click', function () {
    S.h = NL; S.deliv = 0; S.left = 0; S.inletTrip = false; S.pumpTrip = false; S.t = 0; S.feed = 6250; inFeed.value = 6250; hold = 0.8; still();
    var b = this; b.classList.add('is-flash'); setTimeout(function () { b.classList.remove('is-flash'); }, 500);
  });
  var btnNames = $('tk3d-names');
  btnNames.addEventListener('click', function () {
    var on = btnNames.getAttribute('aria-pressed') !== 'true';
    btnNames.setAttribute('aria-pressed', on ? 'true' : 'false'); stage.classList.toggle('no-names', !on);
    measured = false; if (!running) render(0);
  });

  var last = 0, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (t - last) / 1000 || 0)); last = t; clock += dt; idle += dt;
    if (hold > 0) { hold -= dt; sim(0); } else sim(dt);
    uiClock += dt; if (uiClock > 0.12) { uiClock = 0; ui(); }
    sway += ((idle > 4 ? 1 : 0) - sway) * (1 - Math.exp(-dt * 2));
    var e = 1 - Math.exp(-dt * 10);
    yaw += (yawUser + 0.07 * Math.sin(clock * 0.3) * sway - yaw) * e; pitch += (pitchUser - pitch) * e;
    render(dt);
    requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); sim(0); ui(true); render(0);
  window.addEventListener('resize', function () { resize(); ui(true); if (!running) render(0); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measured = false; if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
