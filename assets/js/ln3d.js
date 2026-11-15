/* Line sizing article: 3D model of a length of the P-101 discharge line, cut in half along its axis
   (needs three.js r128+ as window.THREE). The hydraulics repeat the article's worked example: 850 kg/m3,
   0.60 mPa.s, rated 8.09 m3/h, roughness 0.045 mm, Swamee-Jain friction factor, Darcy-Weisbach pressure drop
   and a 60 m equivalent length (kept the same for every size). The viscosity slider is a what-if. Between
   Reynolds numbers of 2,100 and 4,000 the friction factor is interpolated. */
(function () {
  'use strict';
  var fig = document.getElementById('ln3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.ln3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.ln3d-lines');
  var inFlow = $('ln3d-flow'), inVisc = $('ln3d-visc'), sizeBtns = Array.prototype.slice.call(fig.querySelectorAll('[data-size]'));
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- hydraulics (same constants and formulas as the article) ----- */
  var G = 9.81, RHO = 850, MU0 = 0.0006, Q_N = 6250 / RHO, EPS = 0.045e-3, L_EQ = 60, MM = 17;   /* MM: millimetres of pipe per model unit */
  var SIZES = [{ n: '1', id: 26.64, od: 33.4, t: 3.38 }, { n: '1½', id: 40.9, od: 48.3, t: 3.68 }, { n: '2', id: 52.5, od: 60.3, t: 3.91 }, { n: '3', id: 77.9, od: 88.9, t: 5.49 }];
  function fTurb(re, D) { var lg = Math.log(EPS / (3.7 * D) + 5.74 / Math.pow(re, 0.9)) / Math.LN10; return 0.25 / (lg * lg); }
  function fric(re, D) { if (re <= 2100) return 64 / Math.max(re, 1e-6); if (re >= 4000) return fTurb(re, D); var u = (re - 2100) / 1900; return 64 / 2100 + (fTurb(4000, D) - 64 / 2100) * u; }
  var S = { size: 1, q: Q_N * 1.1, mu: MU0, v: 1.71, re: 99100, f: 0.0227, dp: 69, dpl: 41, head: 5, turb: 1, n: 6.6, vmax: 2.07, R: 0.85, Ro: 1.0 };
  /* local speed at a fraction s of the radius: a parabola in laminar flow, a blunt power law in turbulent flow */
  function speed(s) {
    s = Math.min(1, Math.abs(s));
    var lam = 2 * S.v * (1 - s * s), n = S.n, tur = S.v * (n + 1) * (2 * n + 1) / (2 * n * n) * Math.pow(1 - s, 1 / n);
    return lam + (tur - lam) * S.turb;
  }
  var lastKey = 'design';
  var SAY = {
    design: 'Design point: 8.09 m³/h in the 1½-inch line runs at 1.71 m/s. The flow is turbulent, the velocity profile is blunt, and the line loses 41 kPa over its 60 m.',
    small: 'A smaller pipe: the same flow has to go much faster, and the pressure drop climbs roughly with the fifth power of the change in diameter.',
    big: 'A larger pipe: the liquid slows down and the pressure drop almost disappears, but the pipe, its valves and its supports all cost more.',
    less: 'Less flow: in turbulent flow the pressure drop falls almost with the square of the flow. Half the flow needs about a quarter of the pressure.',
    more: 'More flow: in turbulent flow the pressure drop rises almost with the square of the flow.',
    visc: 'A thicker liquid lowers the Reynolds number. While the flow stays turbulent, the pressure drop rises only slowly.',
    trans: 'Transitional flow: between Reynolds numbers of about 2,100 and 4,000 the flow flips between laminar and turbulent and the friction factor is uncertain. Lines are not sized to run here.',
    lam: 'Laminar flow: the liquid slides in layers. The profile is a parabola with the centre moving at twice the average speed, the dye stays in a thread, and the pressure drop rises in direct proportion to the flow.'
  };
  function calc(changed) {
    var pct = parseFloat(inFlow.value), sl = parseFloat(inVisc.value), z = SIZES[S.size], D = z.id / 1000;
    S.q = pct / 100 * Q_N; S.mu = MU0 * Math.pow(5000, sl / 100);
    S.v = S.q / 3600 / (Math.PI * D * D / 4); S.re = RHO * S.v * D / S.mu; S.f = fric(S.re, D);
    S.dp = S.f * 100 / D * RHO * S.v * S.v / 2 / 1000; S.dpl = S.dp * L_EQ / 100; S.head = S.dpl * 1000 / (RHO * G);
    S.turb = Math.max(0, Math.min(1, (S.re - 2100) / 1900)); S.n = 1 / Math.sqrt(fTurb(Math.max(S.re, 4000), D)); S.vmax = speed(0);
    S.R = z.id / 2 / MM; S.Ro = z.od / 2 / MM;
    function kpa(x) { return x >= 10 ? Math.round(x).toLocaleString('en-CA') : x.toFixed(1); }
    $('ln3d-size-o').textContent = z.n + ' in. schedule 40 · bore ' + z.id.toFixed(1) + ' mm';
    $('ln3d-flow-o').textContent = S.q.toFixed(2) + ' m³/h · ' + pct.toFixed(0) + '% of normal';
    var cp = S.mu * 1000; $('ln3d-visc-o').textContent = (cp < 10 ? cp.toFixed(2) : cp < 100 ? cp.toFixed(1) : cp.toFixed(0)) + ' mPa·s';
    $('ln3d-v').textContent = S.v.toFixed(2) + ' m/s';
    $('ln3d-re').textContent = (S.re >= 10000 ? Math.round(S.re / 100) * 100 : Math.round(S.re / 10) * 10).toLocaleString('en-CA');
    $('ln3d-f').textContent = S.f.toFixed(4); $('ln3d-dp').textContent = kpa(S.dp) + ' kPa'; $('ln3d-dpl').textContent = kpa(S.dpl) + ' kPa'; $('ln3d-h').textContent = S.head.toFixed(S.head < 10 ? 1 : 0) + ' m';
    var lam = S.re <= 2100, trans = !lam && S.re < 4000, fast = !lam && !trans && S.v > 3, chip = $('ln3d-chip');
    chip.textContent = lam ? 'Laminar flow' : trans ? 'Transitional flow' : fast ? 'Turbulent · too fast' : 'Turbulent flow'; chip.classList.toggle('is-bad', trans || fast);
    var design = S.size === 1 && pct === 110 && sl === 0, key = lastKey;
    if (design) key = 'design';
    else if (lam) key = 'lam';
    else if (trans) key = 'trans';
    else if (changed === 'size') key = S.size < 1 ? 'small' : S.size > 1 ? 'big' : key;
    else if (changed === 'flow') key = pct < 110 ? 'less' : pct > 110 ? 'more' : key;
    else if (changed === 'visc') key = sl > 0 ? 'visc' : key;
    if ((key === 'design' && !design) || (key === 'lam' && !lam) || (key === 'trans' && !trans) || (key === 'small' && S.size >= 1) || (key === 'big' && S.size <= 1) || (key === 'visc' && sl === 0))
      key = S.size < 1 ? 'small' : S.size > 1 ? 'big' : sl > 0 ? 'visc' : pct < 110 ? 'less' : 'more';
    if (key !== lastKey) { lastKey = key; $('ln3d-say').textContent = SAY[key]; }
    var narrow = !wideNow;
    tags.id.el.textContent = (narrow ? 'ID ' : z.n + ' in. · inside diameter ') + z.id.toFixed(1) + ' mm';
    tags.mean.el.textContent = (narrow ? 'Mean ' : 'Mean velocity ') + S.v.toFixed(2) + ' m/s';
    tags.peak.el.textContent = (narrow ? 'Centre ' : 'Velocity profile · centre ') + S.vmax.toFixed(2) + ' m/s';
    tags.loss.el.textContent = 'Loses ' + kpa(S.dp) + ' kPa per 100 m';
    labels.wall.el.textContent = 'Pipe wall, schedule 40 · ' + z.t.toFixed(2) + ' mm';
    measured = false; chart();
    if (ok) { if (builtSize !== S.size) pipe(); paint(); if (!running) render(0); }
  }
  /* small live chart: friction factor against Reynolds number (a slice of the Moody chart for this pipe) */
  function chart() {
    var el = $('ln3d-svg'), D = SIZES[S.size].id / 1000, lx0 = Math.log(300) / Math.LN10, lx1 = Math.log(2e6) / Math.LN10, ly0 = Math.log(0.01) / Math.LN10, ly1 = Math.log(0.25) / Math.LN10;
    var X = function (re) { return 40 + (Math.log(Math.max(300, Math.min(2e6, re))) / Math.LN10 - lx0) / (lx1 - lx0) * 246; }, Y = function (f) { return 160 - (Math.log(Math.max(0.01, Math.min(0.25, f))) / Math.LN10 - ly0) / (ly1 - ly0) * 146; };
    var s = '<rect x="' + X(2100) + '" y="14" width="' + (X(4000) - X(2100)) + '" height="146" fill="#FF8A3D" opacity=".16"/>', re, d;
    [0.01, 0.02, 0.05, 0.1, 0.2].forEach(function (f) { s += '<line x1="40" x2="286" y1="' + Y(f) + '" y2="' + Y(f) + '" stroke="rgba(255,255,255,.10)"/><text x="35" y="' + (Y(f) + 3.5) + '" text-anchor="end">' + f + '</text>'; });
    [[1e3, '1,000'], [1e4, '10,000'], [1e5, '100,000'], [1e6, '1,000,000']].forEach(function (q) { s += '<line x1="' + X(q[0]) + '" x2="' + X(q[0]) + '" y1="14" y2="160" stroke="rgba(255,255,255,.07)"/><text x="' + X(q[0]) + '" y="173" text-anchor="middle">' + q[1] + '</text>'; });
    s += '<text x="163" y="187" text-anchor="middle">Friction factor against Reynolds number</text>';
    d = 'M' + X(300) + ' ' + Y(64 / 300) + 'L' + X(2100) + ' ' + Y(64 / 2100); s += '<path d="' + d + '" fill="none" stroke="#5EC8FF" stroke-width="2"/>';
    s += '<path d="M' + X(2100) + ' ' + Y(64 / 2100) + 'L' + X(4000) + ' ' + Y(fTurb(4000, D)) + '" fill="none" stroke="#5EC8FF" stroke-width="1.4" stroke-dasharray="3 3"/>';
    d = ''; for (re = 4000; re <= 2.0001e6; re *= 1.25) d += (d ? 'L' : 'M') + X(re).toFixed(1) + ' ' + Y(fTurb(re, D)).toFixed(1);
    s += '<path d="' + d + '" fill="none" stroke="#5EC8FF" stroke-width="2"/>';
    s += '<text x="' + (X(700)) + '" y="' + (Y(64 / 700) - 7) + '" style="fill:#5EC8FF;font-weight:600">Laminar</text><text x="282" y="' + (Y(fTurb(1e6, D)) - 8) + '" text-anchor="end" style="fill:#5EC8FF;font-weight:600">Turbulent</text>';
    s += '<circle cx="' + X(S.re).toFixed(1) + '" cy="' + Y(S.f).toFixed(1) + '" r="4.8" fill="#8DC63F" stroke="#061833" stroke-width="1.5"/>';
    el.innerHTML = s;
  }
  /* speed colour: blue at rest through cyan, green and yellow to red at 4 m/s */
  var STOPS = [[0, 40, 70, 200], [1, 40, 190, 230], [2, 90, 210, 110], [3, 250, 210, 60], [4, 240, 70, 50]];
  function speedRGB(v, out) {
    var p = Math.max(0, Math.min(4, v));
    for (var i = 1; i < STOPS.length; i++) if (p <= STOPS[i][0]) {
      var a = STOPS[i - 1], b = STOPS[i], u = (p - a[0]) / (b[0] - a[0]);
      out[0] = (a[1] + (b[1] - a[1]) * u) / 255; out[1] = (a[2] + (b[2] - a[2]) * u) / 255; out[2] = (a[3] + (b[3] - a[3]) * u) / 255; return out;
    }
    return out;
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, shell = null, builtSize = -1, field, lines = [], lineMat, trc, trcPos, trcCol, dye, dyePos, dyeCol, running = false;
  var shafts, heads = [], env, fill, needle, mats = {};
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('ln3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.ln3d-drag').style.display = 'none'; }
  var XA = -5.0, XB = 6.6, XR = 0.4, XD = -4.2, KA = 0.55, KT = 1.25, NY = 44, NA = 15, NTR = 5, TAIL = 5, NDYE = 900;
  /* streamline positions as fractions of the radius: a fan across the cut plane, and a few behind it */
  var SEEDS = [];
  (function () { var i; for (i = 0; i < 15; i++) SEEDS.push([-0.93 + 1.86 * i / 14, 0]); for (i = 0; i < 12; i++) { var a = Math.PI * (i + 0.5) / 12, r = i % 2 ? 0.45 : 0.78; SEEDS.push([r * Math.cos(a), -r * Math.sin(a)]); } })();
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.85));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.4); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); scene.add(pivot); model = new T.Group(); pivot.add(model);
    mats.steel = mat(0x55637b); mats.cut = mat(0xa9b5c6, 0.95, 0); mats.inner = mat(0x3a4c6b, 0.8, 0.15); mats.needle = mat(0xd3d9e2, 0.35, 0.45);
    var i, k;
    /* speed field on the cut plane */
    var pos = new Float32Array(2 * (NY + 1) * 3), col = new Float32Array(2 * (NY + 1) * 3), idx = [];
    for (k = 0; k < NY; k++) { var a = k * 2, b = a + 2; idx.push(a, a + 1, b + 1, a, b + 1, b); }
    var fg = new T.BufferGeometry(); fg.setAttribute('position', new T.BufferAttribute(pos, 3)); fg.setAttribute('color', new T.BufferAttribute(col, 3)); fg.setIndex(idx);
    field = new T.Mesh(fg, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.3, depthWrite: false, side: T.DoubleSide })); field.frustumCulled = false; model.add(field);
    /* streamlines: straight, one colour each */
    SEEDS.forEach(function (sd) {
      var g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(new Float32Array(6), 3));
      var m = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: sd[1] ? 0.5 : 0.85 }), ln = new T.Line(g, m); ln.frustumCulled = false; model.add(ln);
      var tr = []; for (k = 0; k < NTR; k++) tr.push({ x: XA + (XB - XA) * (k + Math.random()) / NTR, ph: Math.random() * 6.28, fr: 2 + Math.random() * 3 });
      lines.push({ sy: sd[0], sz: sd[1], s: Math.hypot(sd[0], sd[1]), line: ln, m: m, tr: tr });
    });
    /* velocity profile: a rake of arrows, their envelope and a faint fill */
    var sg = new T.BufferGeometry(); sg.setAttribute('position', new T.BufferAttribute(new Float32Array(NA * 6), 3));
    shafts = new T.LineSegments(sg, new T.LineBasicMaterial({ color: 0xffffff })); shafts.frustumCulled = false; model.add(shafts);
    var hm = new T.MeshBasicMaterial({ color: 0xffffff });
    for (i = 0; i < NA; i++) { var h = new T.Mesh(new T.ConeGeometry(0.055, 0.2, 10), hm); h.rotation.z = -Math.PI / 2; model.add(h); heads.push(h); }
    var eg = new T.BufferGeometry(); eg.setAttribute('position', new T.BufferAttribute(new Float32Array((NY + 3) * 3), 3));
    env = new T.Line(eg, new T.LineBasicMaterial({ color: 0xffffff })); env.frustumCulled = false; model.add(env);
    var flg = new T.BufferGeometry(); flg.setAttribute('position', new T.BufferAttribute(new Float32Array(2 * (NY + 1) * 3), 3)); flg.setIndex(idx);
    fill = new T.Mesh(flg, new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.13, depthWrite: false, side: T.DoubleSide })); fill.frustumCulled = false; model.add(fill);
    needle = new T.Mesh(new T.CylinderGeometry(0.035, 0.035, 1, 10), mats.needle); model.add(needle);
    var c2 = document.createElement('canvas'); c2.width = c2.height = 64; var x2 = c2.getContext('2d'), gr2 = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr2.addColorStop(0, 'rgba(255,255,255,1)'); gr2.addColorStop(0.3, 'rgba(255,255,255,.65)'); gr2.addColorStop(1, 'rgba(255,255,255,0)');
    x2.fillStyle = gr2; x2.fillRect(0, 0, 64, 64);
    var tex = new T.CanvasTexture(c2);
    function points(cnt, size) {
      var gp = new T.BufferGeometry(), ps = new Float32Array(cnt * 3), cl = new Float32Array(cnt * 3);
      gp.setAttribute('position', new T.BufferAttribute(ps, 3)); gp.setAttribute('color', new T.BufferAttribute(cl, 3));
      var pt = new T.Points(gp, new T.PointsMaterial({ size: size, map: tex, transparent: true, depthWrite: false, vertexColors: true, blending: T.AdditiveBlending, sizeAttenuation: true }));
      pt.frustumCulled = false; model.add(pt); return [pt, ps, cl];
    }
    var q = points(SEEDS.length * NTR * TAIL, 0.13); trc = q[0]; trcPos = q[1]; trcCol = q[2];
    q = points(NDYE, 0.26); dye = q[0]; dyePos = q[1]; dyeCol = q[2]; dye.material.blending = T.NormalBlending; dye.material.vertexColors = false; dye.material.color.set(0xff5fd0); dye.material.opacity = 0.9; dye.material.needsUpdate = true;
  }
  /* the pipe itself, rebuilt when the size changes: back half of the wall, its cut faces and the two ends */
  function pipe() {
    if (shell) { model.remove(shell); shell.traverse(function (o) { if (o.geometry) o.geometry.dispose(); }); }
    shell = new T.Group(); model.add(shell); builtSize = S.size;
    var R = S.R, Ro = S.Ro, prof = [[R, XA, mats.inner], [R, XB, mats.steel], [Ro, XB, mats.steel], [Ro, XA, mats.steel], [R, XA]], j;
    for (j = 0; j < 4; j++) {
      var ms = new T.Mesh(new T.LatheGeometry([new T.Vector2(prof[j][0], prof[j][1]), new T.Vector2(prof[j + 1][0], prof[j + 1][1])], 48, Math.PI / 2, Math.PI), prof[j][2]);
      ms.rotation.z = -Math.PI / 2; shell.add(ms);
    }
    [1, -1].forEach(function (sg) { var c = new T.Mesh(new T.PlaneGeometry(XB - XA, Ro - R), mats.cut); c.position.set((XA + XB) / 2, sg * (R + Ro) / 2, 0.002); shell.add(c); });
    needle.scale.y = Ro + 0.55; needle.position.set(XD, (Ro + 0.55) / 2, -0.03);
    dyes.forEach(function (d, i2) { d.x = XD + (XB - XD) * i2 / NDYE; d.y = 0; d.z = 0; });
  }
  var rgb = [0, 0, 0], dyes = [];
  for (var di = 0; di < NDYE; di++) dyes.push({ x: 0, y: 0, z: 0 });
  function paint() { /* recolour the field and streamlines and redraw the velocity profile for the current state */
    var R = S.R, k, pos = field.geometry.attributes.position, col = field.geometry.attributes.color, fp = fill.geometry.attributes.position, ep = env.geometry.attributes.position;
    ep.setXYZ(0, XR, -R, 0.02);
    for (k = 0; k <= NY; k++) {
      var s = -1 + 2 * k / NY, y = s * R, u = speed(s), len = Math.min(3.9, u * KA);
      pos.setXYZ(k * 2, XA, y, -0.004); pos.setXYZ(k * 2 + 1, XB, y, -0.004);
      speedRGB(u, rgb); col.setXYZ(k * 2, rgb[0], rgb[1], rgb[2]); col.setXYZ(k * 2 + 1, rgb[0], rgb[1], rgb[2]);
      fp.setXYZ(k * 2, XR, y, 0.015); fp.setXYZ(k * 2 + 1, XR + len, y, 0.015); ep.setXYZ(k + 1, XR + len, y, 0.02);
    }
    ep.setXYZ(NY + 2, XR, R, 0.02);
    pos.needsUpdate = true; col.needsUpdate = true; fp.needsUpdate = true; ep.needsUpdate = true;
    var sp = shafts.geometry.attributes.position;
    for (k = 0; k < NA; k++) {
      var s2 = -0.93 + 1.86 * k / (NA - 1), y2 = s2 * R, l2 = Math.min(3.9, speed(s2) * KA), show = l2 > 0.24;
      sp.setXYZ(k * 2, XR, y2, 0.02); sp.setXYZ(k * 2 + 1, XR + Math.max(0, l2 - 0.1), y2, 0.02);
      heads[k].visible = show; heads[k].position.set(XR + l2 - 0.1, y2, 0.02);
    }
    sp.needsUpdate = true;
    lines.forEach(function (l) {
      var p = l.line.geometry.attributes.position; p.setXYZ(0, XA, l.sy * R, l.sz * R - 0.006); p.setXYZ(1, XB, l.sy * R, l.sz * R - 0.006); p.needsUpdate = true;
      speedRGB(speed(l.s), rgb); l.m.color.setRGB(Math.min(1, rgb[0] * 0.55 + 0.5), Math.min(1, rgb[1] * 0.55 + 0.5), Math.min(1, rgb[2] * 0.55 + 0.5));
    });
  }
  function gauss() { return (Math.random() + Math.random() + Math.random() - 1.5) * 1.15; }
  function step(dt, clock) {
    var R = S.R, j, n, t, k, l, ti = 0, wob = S.turb * 0.045 * R;
    for (j = 0; j < lines.length; j++) {
      l = lines[j]; var u = speed(l.s);
      for (n = 0; n < l.tr.length; n++) {
        var tr = l.tr[n]; tr.x += dt * u * KT; if (tr.x > XB) tr.x -= XB - XA;
        var wy = wob * Math.sin(clock * tr.fr + tr.ph + tr.x * 2.1), wz = l.sz ? wob * Math.cos(clock * tr.fr * 0.8 + tr.ph) : 0;
        for (t = 0; t < TAIL; t++) {
          var xx = tr.x - t * 0.07 * Math.min(1.6, 0.35 + u * 0.5), vis = xx < XA ? 0 : 1 - t / TAIL;
          k = ti * 3; trcPos[k] = xx; trcPos[k + 1] = l.sy * R + wy; trcPos[k + 2] = l.sz * R + wz + 0.004;
          trcCol[k] = vis; trcCol[k + 1] = vis; trcCol[k + 2] = vis; ti++;
        }
      }
    }
    /* dye released at the centre: carried along at the local speed, and scattered across the bore by turbulence */
    var mix = S.turb * R * 0.55, lim = 0.92 * R;
    for (j = 0; j < NDYE; j++) {
      var d = dyes[j], s = Math.hypot(d.y, d.z) / R;
      d.x += dt * speed(s) * KT;
      if (mix > 0 && dt > 0) { var sq = Math.sqrt(dt * Math.max(0.3, S.v)); d.y += gauss() * mix * sq; d.z += gauss() * mix * sq; }
      if (d.z > 0) d.z = -d.z;
      var rr = Math.hypot(d.y, d.z); if (rr > lim) { d.y *= lim / rr * 0.96; d.z *= lim / rr * 0.96; }
      if (d.x > XB) { d.x = XD + Math.random() * 0.05; d.y = (Math.random() - 0.5) * 0.03; d.z = -Math.random() * 0.03; }
      k = j * 3; dyePos[k] = d.x; dyePos[k + 1] = d.y; dyePos[k + 2] = d.z + 0.006;
      dyeCol[k] = 1; dyeCol[k + 1] = 0.36; dyeCol[k + 2] = 0.8;
    }
    trc.geometry.attributes.position.needsUpdate = true; trc.geometry.attributes.color.needsUpdate = true;
    dye.geometry.attributes.position.needsUpdate = true; dye.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- names and tags: a row above and a row below the pipe, each joined to its part.
     Entries: kind, text, anchor (a function of the pipe size and state), band, key, wide screens only ----- */
  var ITEMS = [
    ['l', 'Dye injected at the centre', function () { return [XD, S.Ro + 0.4]; }, 'T'],
    ['t', 'Velocity profile · centre 2.07 m/s', function () { return [XR + Math.min(3.9, S.vmax * KA), 0]; }, 'T', 'peak'],
    ['l', 'Pipe wall, schedule 40 · 3.68 mm', function () { return [3.6, (S.R + S.Ro) / 2]; }, 'T', 'wall', 0, 1],
    ['t', '1½ in. · inside diameter 40.9 mm', function () { return [-3.0, -(S.R + S.Ro) / 2]; }, 'B', 'id'],
    ['t', 'Mean velocity 1.71 m/s', function () { return [XR + Math.min(3.9, S.v * KA) * 0.5, -0.62 * S.R]; }, 'B', 'mean'],
    ['t', 'Loses 69 kPa per 100 m', function () { return [4.1, -0.35 * S.R]; }, 'B', 'loss', 1]
  ];
  var tags = {}, labels = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'ln3d-tag' : 'ln3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, x: 0, tag: n[0] === 't', wideOnly: !!n[5], hidden: false };
    if (n[4]) (n[0] === 't' ? tags : labels)[n[4]] = it; return it;
  });
  var W = 0, H = 0, measured = false, wideNow = true, v3 = T ? new T.Vector3() : null;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function place() {
    if (!measured) { items.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    var pt = { x: 0, y: 0 }, gap = 8;
    ['T', 'B'].forEach(function (band) {
      items.forEach(function (q) { if (q.wideOnly) { var hide = !wideNow; if (q.hidden !== hide) { q.hidden = hide; q.el.style.display = hide ? 'none' : ''; q.path.style.display = hide ? 'none' : ''; q.dot.style.display = hide ? 'none' : ''; } } });
      var list = items.filter(function (q) { return q.n[3] === band && !q.hidden && (q.tag || (wideNow && q.w > 0)); }), i, l;
      list.forEach(function (q) { var a = q.n[2](); toScreen(a[0], a[1], 0.02, pt); q.ax = Math.max(6, Math.min(W - 6, pt.x)); q.ay = pt.y; q.x = q.ax; });
      list.sort(function (a, b) { return a.ax - b.ax; });
      for (i = 0; i < list.length; i++) { l = list[i]; l.x = Math.max(l.x, 8 + l.w / 2, i ? list[i - 1].x + (list[i - 1].w + l.w) / 2 + gap : -1e9); }
      for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.x = Math.min(l.x, W - 8 - l.w / 2, i < list.length - 1 ? list[i + 1].x - (list[i + 1].w + l.w) / 2 - gap : 1e9); }
      var by = band === 'T' ? 54 : H - 26;
      for (i = 0; i < list.length; i++) {
        l = list[i];
        l.el.style.transform = 'translate(' + (l.x - l.w / 2).toFixed(1) + 'px,' + (by - l.h / 2).toFixed(1) + 'px)';
        var lx = Math.max(l.x - l.w / 2 + 12, Math.min(l.x + l.w / 2 - 12, l.ax)), ly = band === 'T' ? by + l.h / 2 : by - l.h / 2;
        l.path.setAttribute('d', 'M' + l.ax.toFixed(1) + ' ' + l.ay.toFixed(1) + 'L' + lx.toFixed(1) + ' ' + ly.toFixed(1));
        l.dot.setAttribute('cx', l.ax.toFixed(1)); l.dot.setAttribute('cy', l.ay.toFixed(1));
      }
    });
  }

  /* ----- view ----- */
  var yawUser = -0.36, pitchUser = 0.3, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var px = Math.min(W / (wideNow ? 9.2 : 6.6), (H - 150) / 5.7), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180)), off = 8 / px;
    camera.aspect = W / H; camera.position.set(0.5, off, dist); camera.lookAt(0.5, off, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0);
    step(dt, clock);
    pivot.updateMatrixWorld(true);
    renderer.render(scene, camera);
    place();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(-0.9, Math.min(0.9, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.15, Math.min(0.6, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  function setSize(i) { S.size = i; sizeBtns.forEach(function (b) { b.setAttribute('aria-pressed', parseInt(b.getAttribute('data-size'), 10) === i ? 'true' : 'false'); }); }
  sizeBtns.forEach(function (b) { b.addEventListener('click', function () { setSize(parseInt(b.getAttribute('data-size'), 10)); calc('size'); }); });
  inFlow.addEventListener('input', function () { calc('flow'); });
  inVisc.addEventListener('input', function () { calc('visc'); });
  $('ln3d-reset').addEventListener('click', function () { inFlow.value = 110; inVisc.value = 0; setSize(1); calc(); });
  var btnNames = $('ln3d-names');
  btnNames.addEventListener('click', function () {
    var on = btnNames.getAttribute('aria-pressed') !== 'true';
    btnNames.setAttribute('aria-pressed', on ? 'true' : 'false'); stage.classList.toggle('no-names', !on);
    measured = false; if (!running) render(0);
  });

  var last = 0, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (t - last) / 1000 || 0)); last = t; clock += dt; idle += dt;
    sway += ((idle > 4 ? 1 : 0) - sway) * (1 - Math.exp(-dt * 2));
    var e = 1 - Math.exp(-dt * 10);
    yaw += (yawUser + 0.07 * Math.sin(clock * 0.3) * sway - yaw) * e; pitch += (pitchUser - pitch) * e;
    render(dt);
    requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce || !ok) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); calc();
  if (ok && reduce) { for (var w = 0; w < 120; w++) step(0.05, w * 0.05); }
  render(0);
  window.addEventListener('resize', function () { resize(); calc(); if (!running) render(0); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measured = false; if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
