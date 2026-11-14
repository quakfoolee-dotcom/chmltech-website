/* Pressure relief article: 3D model of a spring-loaded relief valve, cut in half (needs three.js r128+ as window.THREE).
   Pressure levels follow the article's R-101 example: normal 1 barg, set pressure = MAWP = 3 barg, limit while
   relieving 3.3 barg (+10%). Reseat at about 2.8 barg (blowdown). Part shapes are simplified. */
(function () {
  'use strict';
  var fig = document.getElementById('psv3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.psv3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.psv3d-lines');
  var slider = $('psv3d-p'), btnRun = $('psv3d-run'), btnNames = $('psv3d-names');
  var P_NORMAL = 1.0, P_RESEAT = 2.8, P_SET = 3.0, P_LIMIT = 3.3, LIFT_Y = 0.62;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- valve behaviour ----- */
  var P = P_NORMAL, prevP = P, open = false, wasOpen = false, lift = 0, mode = reduce ? 'manual' : 'auto', tScript = 0, rising = false;
  var KEYS = [[0, 1], [1.5, 1], [7.5, 3.0], [9.2, 3.24], [12.6, 3.26], [16.6, 2.8], [17.1, 2.77], [21.5, 1], [24.5, 1]];
  function scriptP(t) {
    for (var i = 1; i < KEYS.length; i++) if (t <= KEYS[i][0]) {
      var a = KEYS[i - 1], b = KEYS[i], u = (t - a[0]) / (b[0] - a[0]); u = u * u * (3 - 2 * u);
      return a[1] + (b[1] - a[1]) * u;
    }
    return KEYS[KEYS.length - 1][1];
  }
  function liftTarget() { return open ? Math.max(0.22, Math.min(1, 0.55 + 0.45 * (P - P_SET) / 0.2)) : 0; }
  function stepValve(dt) {
    if (!open && P >= P_SET) { open = true; wasOpen = true; }
    else if (open && P <= P_RESEAT) open = false;
    if (P < 1.6) wasOpen = false;
    if (Math.abs(P - prevP) > 1e-4) rising = P > prevP;
    prevP = P;
    var tg = liftTarget();
    lift = dt > 0 ? lift + (tg - lift) * (1 - Math.exp(-dt * (tg > lift ? 16 : 9))) : tg;
    if (Math.abs(lift - tg) < 0.002) lift = tg;
  }
  var SAY = {
    normal: 'Normal operation at 1 barg. The spring presses the disc onto the nozzle and the valve is shut tight.',
    rising: 'Pressure is rising. The gas pushes up on the disc, but the spring force is still larger, so the valve stays shut.',
    near: 'Close to the set pressure. The two forces are nearly equal. A valve that runs this close to its set pressure can simmer and leak.',
    opening: 'Set pressure reached at 3 barg. The gas now beats the spring, the disc lifts and gas escapes to the flare or scrubber. This is what stops the pressure climbing.',
    full: 'Fully open. With one relief device, the code lets the vessel reach 3.3 barg while relieving, 10% above its MAWP.',
    over: 'Above 3.3 barg the vessel is past what the code allows for a single device. A correctly sized valve keeps the pressure below this.',
    falling: 'Pressure is falling, but the valve stays open until about 2.8 barg. Once open, the gas also acts on the wider disc holder. This gap below the set pressure is called blowdown.',
    reseated: 'The spring has pushed the disc back onto the nozzle. The valve has reseated and the vessel is sealed again.',
    below: 'Below the set pressure the valve stays shut. It only opens once the vessel reaches 3 barg.'
  };
  var lastSay = '';
  function updatePanel() {
    var txt = P.toFixed(2) + ' barg';
    $('psv3d-po').textContent = txt; $('psv3d-pin').textContent = txt;
    if (document.activeElement !== slider || mode === 'auto') slider.value = P.toFixed(2);
    var fp = P * (open ? 1.1 : 1), fs = P_SET * (1 + 0.1 * lift);
    $('psv3d-fp').style.width = Math.min(100, fp / 4 * 100).toFixed(1) + '%';
    $('psv3d-fs').style.width = Math.min(100, fs / 4 * 100).toFixed(1) + '%';
    $('psv3d-fp').style.background = gasCss();
    $('psv3d-lift').textContent = Math.round(lift * 100) + '%';
    $('psv3d-flow').textContent = lift < 0.01 ? 'None' : lift < 0.97 ? 'Partial' : 'Full';
    var chip = $('psv3d-chip'); chip.textContent = open ? (lift > 0.97 ? 'Relieving' : 'Open') : 'Closed'; chip.classList.toggle('is-open', open);
    var k = open ? (P > P_LIMIT + 0.005 ? 'over' : P >= 3.2 ? 'full' : (P >= P_SET || rising) ? 'opening' : 'falling')
                 : (wasOpen ? 'reseated' : P <= 1.25 ? 'normal' : P >= 2.7 ? 'near' : rising ? 'rising' : 'below');
    if (k !== lastSay) { lastSay = k; $('psv3d-say').textContent = SAY[k]; }
  }
  function gasRGB() { /* blue at normal pressure, amber near the set pressure, red at the limit */
    var a, b, u;
    if (P <= 2.7) { a = [94, 200, 255]; b = [255, 190, 90]; u = Math.max(0, (P - 1) / 1.7); }
    else { a = [255, 190, 90]; b = [255, 106, 77]; u = Math.min(1, (P - 2.7) / 0.6); }
    return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
  }
  function gasCss() { var c = gasRGB(); return 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')'; }

  slider.addEventListener('input', function () { mode = 'manual'; P = parseFloat(slider.value); btnRun.textContent = 'Run an overpressure event'; if (!running) { stepValve(0); updatePanel(); render(0); } });
  btnRun.addEventListener('click', function () {
    mode = 'auto'; tScript = 1.2; P = P_NORMAL; open = false; wasOpen = false; lift = 0;
    if (reduce) { reduce = false; setRun(true); }
  });
  btnNames.addEventListener('click', function () {
    var on = btnNames.getAttribute('aria-pressed') !== 'true';
    btnNames.setAttribute('aria-pressed', on ? 'true' : 'false'); stage.classList.toggle('no-names', !on);
  });

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, moving, spring, gas, gasPos, gasCol, running = false;
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('psv3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.psv3d-drag').style.display = 'none'; }

  var HALF0 = Math.PI / 2, HALF = Math.PI;
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  /* A solid of revolution about the Y axis from a closed (r, y) outline. cut: keep only the back half and close it
     with flat section faces on the cut plane. Each outline edge is its own strip, so corners stay crisp. */
  function lathe(parent, outline, m, mCut, o) {
    o = o || {};
    var g = new T.Group(), n = outline.length, phi0 = o.phi0 == null ? (o.whole ? 0 : HALF0) : o.phi0, len = o.len == null ? (o.whole ? Math.PI * 2 : HALF) : o.len;
    for (var i = 0; i < n; i++) {
      var a = outline[i], b = outline[(i + 1) % n];
      if (a[0] === 0 && b[0] === 0) continue;
      g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(a[0], a[1]), new T.Vector2(b[0], b[1])], Math.max(6, Math.round((o.seg || 44) * len / Math.PI)), phi0, len), m));
    }
    if (!o.whole && mCut) {
      var sh = new T.Shape(outline.map(function (p) { return new T.Vector2(p[0], p[1]); })), sg = new T.ShapeGeometry(sh);
      if (o.capA !== false) g.add(new T.Mesh(sg, mCut));
      if (o.capB !== false) { var c2 = new T.Mesh(sg, mCut); c2.scale.x = -1; g.add(c2); }
    }
    parent.add(g); return g;
  }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.8));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-6, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.45); rim.position.set(10, 4, -8); scene.add(rim);
    model = new T.Group(); scene.add(model);

    var cast = mat(0x76849a), castCut = mat(0xc3ccd8, 0.95, 0.0), brass = mat(0xc8a04a, 0.45, 0.45), brassCut = mat(0xecd08a, 0.9, 0.05),
        steel = mat(0xc9d0da, 0.45, 0.25), steelCut = mat(0xf2f5f9, 0.9, 0.05), dark = mat(0x5d6a7c), darkCut = mat(0x8c98a9, 0.9, 0.05),
        green = mat(0x8dc63f, 0.5, 0.25);

    /* body: inlet neck, chamber and top flange; a notch in the +x side lets the outlet bore into the chamber */
    var Y0 = -1.4, Y1 = 2.0, RIN = 3.0, AL = Math.asin(1.7 / RIN);
    var BODY = [[1.3, -5.05], [1.3, -1.7], [RIN, -1.7], [RIN, 3.2], [4.3, 3.2], [4.3, 2.55], [3.5, 2.55], [3.5, -1.9], [1.95, -2.6], [1.95, -4.4], [3.3, -4.4], [3.3, -5.05]];
    var BODY_LO = [[1.3, -5.05], [1.3, -1.7], [RIN, -1.7], [RIN, Y0], [3.5, Y0], [3.5, -1.9], [1.95, -2.6], [1.95, -4.4], [3.3, -4.4], [3.3, -5.05]];
    var BODY_HI = [[RIN, Y1], [RIN, 3.2], [4.3, 3.2], [4.3, 2.55], [3.5, 2.55], [3.5, Y1]];
    lathe(model, BODY, cast, castCut, { phi0: HALF0 + AL, len: HALF - AL, capA: false });
    lathe(model, BODY_LO, cast, castCut, { phi0: HALF0, len: AL, capB: false });
    lathe(model, BODY_HI, cast, castCut, { phi0: HALF0, len: AL, capB: false });
    /* outlet branch: the same kind of solid, turned to lie along +x */
    var out = new T.Group(); out.position.y = 0.3; out.rotation.z = -Math.PI / 2; model.add(out);
    lathe(out, [[1.7, 2.45], [2.55, 2.45], [2.55, 3.9], [2.15, 4.4], [2.15, 5.75], [3.4, 5.75], [3.4, 6.4], [1.7, 6.4]], cast, castCut);
    /* nozzle */
    lathe(model, [[0.9, -5.3], [2.3, -5.3], [2.3, -5.05], [1.3, -5.05], [1.3, -0.6], [1.12, 0], [0.9, 0]], brass, brassCut);
    /* bonnet with the guide, cap, adjusting screw, lock nut, upper spring washer */
    lathe(model, [[0.68, 2.7], [1.0, 2.7], [1.0, 3.2], [4.3, 3.2], [4.3, 3.85], [2.3, 3.85], [2.3, 9.1], [1.25, 9.9], [0.56, 9.9], [0.56, 9.35], [1.0, 9.35], [1.9, 8.8], [1.9, 3.7], [0.68, 3.7]], cast, castCut);
    lathe(model, [[1.02, 9.9], [1.3, 9.9], [1.3, 11.5], [0.9, 12.1], [0, 12.1], [0, 11.8], [0.75, 11.8], [1.02, 11.4]], cast, castCut);
    lathe(model, [[0.34, 8.5], [0.54, 8.5], [0.54, 10.9], [0.34, 10.9]], brass, brassCut);
    lathe(model, [[0.56, 9.9], [0.95, 9.9], [0.95, 10.3], [0.56, 10.3]], dark, darkCut);
    lathe(model, [[0.34, 8.2], [1.55, 8.2], [1.55, 8.5], [0.34, 8.5]], dark, darkCut);
    /* studs and nuts on the body-bonnet joint */
    [0.5, 1.57, 2.64].forEach(function (a) {
      var x = 3.9 * Math.cos(a), z = -3.9 * Math.sin(a);
      var s = new T.Mesh(new T.CylinderGeometry(0.16, 0.16, 2.3, 12), steel); s.position.set(x, 3.2, z); model.add(s);
      [4.02, 2.38].forEach(function (y) { var nut = new T.Mesh(new T.CylinderGeometry(0.36, 0.36, 0.34, 6), dark); nut.position.set(x, y, z); model.add(nut); });
    });
    /* moving parts: disc, disc holder, spindle, lower spring washer */
    moving = new T.Group(); model.add(moving);
    lathe(moving, [[0, 0], [1.32, 0], [1.32, 0.36], [0, 0.36]], steel, steelCut);
    lathe(moving, [[0.3, 0.42], [1.5, 0.42], [1.5, -0.12], [1.78, -0.12], [1.78, 0.8], [0.66, 1.25], [0.66, 2.9], [0.3, 2.9]], brass, brassCut);
    lathe(moving, [[0.3, 4.3], [1.55, 4.3], [1.55, 4.6], [0.3, 4.6]], dark, darkCut);
    var sp = new T.Mesh(new T.CylinderGeometry(0.3, 0.3, 10.2, 20), steel); sp.position.y = 0.42 + 5.1; moving.add(sp);
    /* spring: a helix between the two washers, squeezed as the disc lifts */
    var hx = new T.Curve();
    hx.getPoint = function (t, target) { var a = t * 7.5 * Math.PI * 2; return (target || new T.Vector3()).set(1.22 * Math.cos(a), t * 3.6, 1.22 * Math.sin(a)); };
    spring = new T.Mesh(new T.TubeGeometry(hx, 300, 0.2, 10, false), green); model.add(spring);

    /* gas: points that crowd the inlet as pressure rises, then stream to the outlet when the disc lifts */
    var c = document.createElement('canvas'); c.width = c.height = 64; var x2 = c.getContext('2d'), gr = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.35, 'rgba(255,255,255,.75)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    x2.fillStyle = gr; x2.fillRect(0, 0, 64, 64);
    var geo = new T.BufferGeometry(); gasPos = new Float32Array(NG * 3); gasCol = new Float32Array(NG * 3);
    geo.setAttribute('position', new T.BufferAttribute(gasPos, 3)); geo.setAttribute('color', new T.BufferAttribute(gasCol, 3));
    gas = new T.Points(geo, new T.PointsMaterial({ size: 0.5, map: new T.CanvasTexture(c), transparent: true, depthWrite: false, vertexColors: true, blending: T.AdditiveBlending, sizeAttenuation: true }));
    gas.frustumCulled = false; model.add(gas);
  }

  /* ----- gas particles ----- */
  var NS = 260, NF = 460, NG = NS + NF, parts = [];
  var rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return s / 2147483647; }; })(90210);
  for (var i = 0; i < NS; i++) parts.push({ r: 0.78 * Math.sqrt(rnd()), th: Math.PI + rnd() * Math.PI, y: -5.2 + rnd() * 5.1, vy: (rnd() - 0.5), ph: rnd() * 6.28 });
  for (i = 0; i < NF; i++) {
    var oa = Math.PI + rnd() * Math.PI, orad = 1.45 * Math.sqrt(rnd());
    parts.push({ s: -1, r: 0.75 * Math.sqrt(rnd()), th: Math.PI + rnd() * Math.PI, th1: 2 * Math.PI - Math.pow(rnd(), 1.6) * Math.PI * 0.95,
      oy: Math.sin(oa) * orad, oz: -Math.abs(Math.cos(oa) * orad), v: 0.75 + rnd() * 0.5, on: false });
  }
  function mix(a, b, u) { return a + (b - a) * u; }
  function smooth(u) { return u * u * (3 - 2 * u); }
  function stepGas(dt, time) {
    var col = gasRGB(), cr = col[0] / 255, cg = col[1] / 255, cb = col[2] / 255, shown = Math.round(NS * Math.min(1, 0.16 + 0.84 * (P - 0.5) / 2.8)), p, k, j;
    var seatY = lift * LIFT_Y * 0.5;
    for (j = 0; j < NS; j++) {
      p = parts[j]; k = j * 3;
      p.y += p.vy * dt * (0.5 + P * 0.35 + lift * 4) + lift * dt * 2.2; p.th += Math.sin(time * 1.3 + p.ph) * dt * 0.8;
      if (p.th > 2 * Math.PI) p.th = 2 * Math.PI - 0.02; if (p.th < Math.PI) p.th = Math.PI + 0.02;
      if (p.y > -0.12) { if (lift > 0.02) p.y = -5.2; else { p.y = -0.12; p.vy = -Math.abs(p.vy); } }
      if (p.y < -5.2) { p.y = -5.2; p.vy = Math.abs(p.vy); }
      gasPos[k] = p.r * Math.cos(p.th); gasPos[k + 1] = p.y; gasPos[k + 2] = p.r * Math.sin(p.th);
      var b = j < shown ? 0.9 : 0; gasCol[k] = cr * b; gasCol[k + 1] = cg * b; gasCol[k + 2] = cb * b;
    }
    var active = Math.round(NF * lift), speed = 0.42 * (0.35 + 0.65 * lift);
    for (j = 0; j < NF; j++) {
      p = parts[NS + j]; k = (NS + j) * 3;
      if (p.s < 0) { if (j < active && Math.random() < dt * 3.5) p.s = 0; else { gasCol[k] = gasCol[k + 1] = gasCol[k + 2] = 0; continue; } }
      p.s += dt * speed * p.v * (p.s > 0.68 ? 1.25 : 1);
      if (p.s >= 1) { p.s = j < active ? 0 : -1; if (p.s < 0) { gasCol[k] = gasCol[k + 1] = gasCol[k + 2] = 0; continue; } }
      var s = p.s, x, y, z, u, br = 1, bx = 2.3 * Math.cos(p.th1), bz = 2.3 * Math.sin(p.th1), by = seatY - 0.55;
      if (s < 0.28) { u = s / 0.28; x = p.r * Math.cos(p.th); z = p.r * Math.sin(p.th); y = mix(-5.2, seatY - 0.02, u); br = Math.min(1, u * 8); }
      else if (s < 0.42) { u = (s - 0.28) / 0.14; var rr = mix(p.r, 2.3, u), th = mix(p.th, p.th1, smooth(u)); x = rr * Math.cos(th); z = rr * Math.sin(th); y = seatY - 0.02 - 0.53 * u * u; }
      else if (s < 0.68) { u = smooth((s - 0.42) / 0.26); x = mix(bx, 3.0, u); y = mix(by, 0.3 + p.oy, u); z = mix(bz, p.oz, u); }
      else { u = (s - 0.68) / 0.32; x = mix(3.0, 10.2, u); y = 0.3 + p.oy * (1 + 0.3 * u); z = p.oz * (1 + 0.3 * u); br = u > 0.55 ? Math.max(0, 1 - (u - 0.55) / 0.45) : 1; }
      gasPos[k] = x; gasPos[k + 1] = y; gasPos[k + 2] = z; gasCol[k] = cr * br; gasCol[k + 1] = cg * br; gasCol[k + 2] = cb * br;
    }
    gas.geometry.attributes.position.needsUpdate = true; gas.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- part names ----- */
  var NAMES = [
    ['Cap', -1.16, 11.0, 0, 'L'], ['Adjusting screw', -0.44, 10.6, 0, 'L'], ['Bonnet', -2.1, 7.6, 0, 'L'], ['Spring', -1.3, 6.0, 0.4, 'L'],
    ['Body', -3.25, 0.8, 0, 'L'], ['Nozzle', -1.1, -3.2, 0, 'L'],
    ['Spindle', 0.3, 5.3, 1, 'R'], ['Guide', 0.84, 3.0, 0, 'R'], ['Disc holder', 1.64, 0.5, 0, 'R', 1], ['Disc', 0.8, 0.18, 0, 'R', 1]
  ];
  var labels = NAMES.map(function (n) {
    var el = document.createElement('span'); el.className = 'psv3d-label'; el.textContent = n[0]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); svg.appendChild(path); svg.appendChild(dot);
    return { n: n, el: el, path: path, dot: dot, w: 0, h: 0, x: 0, y: 0 };
  });
  var tagIn = $('psv3d-tin'), tagOut = $('psv3d-tout'), v3 = T ? new T.Vector3() : null, W = 0, H = 0, measured = false;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function placeLabels() {
    if (!measured) { labels.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    var pt = { x: 0, y: 0 }, i, l, side, list, y, yy;
    for (i = 0; i < labels.length; i++) { l = labels[i]; toScreen(l.n[1], l.n[2] + (l.n[5] ? lift * LIFT_Y : 0), l.n[3], pt); l.x = pt.x; l.y = pt.y; }
    ['L', 'R'].forEach(function (sd) {
      list = labels.filter(function (q) { return q.n[4] === sd; }).sort(function (a, b) { return a.y - b.y; });
      var top = sd === 'R' ? 46 : 44, yPrev = -1e9;
      /* right-hand names stack above the outlet; left-hand names sit level with their part */
      var cap = sd === 'R' ? toScreen(4, 4.6, 0, pt).y : H - 30, n = list.length;
      for (i = 0; i < n; i++) {
        l = list[i]; yy = sd === 'R' ? Math.min(l.y - 22, cap - (n - 1 - i) * (l.h + 6)) : l.y;
        yy = Math.max(top, yy, yPrev + l.h + 6); yPrev = yy;
        var lx = sd === 'L' ? 14 : W - 14 - l.w, ex = sd === 'L' ? lx + l.w : lx;
        l.el.style.transform = 'translate(' + lx.toFixed(1) + 'px,' + (yy - l.h / 2).toFixed(1) + 'px)';
        var kx = sd === 'L' ? Math.min(l.x - 8, ex + 22) : Math.max(l.x + 8, ex - 22);
        l.path.setAttribute('d', 'M' + l.x.toFixed(1) + ' ' + l.y.toFixed(1) + 'L' + kx.toFixed(1) + ' ' + yy.toFixed(1) + 'L' + ex.toFixed(1) + ' ' + yy.toFixed(1));
        l.dot.setAttribute('cx', l.x.toFixed(1)); l.dot.setAttribute('cy', l.y.toFixed(1));
      }
    });
    toScreen(0, -5.3, 0, pt);
    tagIn.style.transform = 'translate(' + Math.max(8, Math.min(W - tagIn.offsetWidth - 8, pt.x - tagIn.offsetWidth / 2)).toFixed(1) + 'px,' + Math.min(H - tagIn.offsetHeight - 8, pt.y + 10).toFixed(1) + 'px)';
    toScreen(6.4, -3.1, 0, pt);
    tagOut.style.transform = 'translate(' + Math.max(8, Math.min(W - tagOut.offsetWidth - 8, pt.x - tagOut.offsetWidth * 0.3)).toFixed(1) + 'px,' + Math.min(H - tagOut.offsetHeight - 8, pt.y + 8).toFixed(1) + 'px)';
  }

  /* ----- view ----- */
  var yawUser = -0.3, pitchUser = 0.1, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var wide = W >= 560, px = Math.min((H - (wide ? 70 : 96)) / 18.6, (W - (wide ? 250 : 24)) / (wide ? 13.6 : 14.4));
    var dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180));
    camera.aspect = W / H; camera.position.set(wide ? 1.3 : 2.4, 3.0, dist); camera.lookAt(wide ? 1.3 : 2.4, 3.0, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    model.rotation.set(pitch, yaw, 0);
    moving.position.y = lift * LIFT_Y;
    var y0 = 4.6 + lift * LIFT_Y; spring.position.y = y0; spring.scale.y = (8.2 - y0) / 3.6;
    stepGas(dt, clock);
    model.updateMatrixWorld(true);
    renderer.render(scene, camera);
    placeLabels();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(-1.05, Math.min(1.05, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.3, Math.min(0.55, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  var last = 0, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (t - last) / 1000 || 0)); last = t; clock += dt; idle += dt;
    if (mode === 'auto') { tScript += dt; if (tScript > KEYS[KEYS.length - 1][0]) tScript = 0; P = scriptP(tScript); }
    stepValve(dt); updatePanel();
    sway += ((idle > 4 ? 1 : 0) - sway) * (1 - Math.exp(-dt * 2));
    var e = 1 - Math.exp(-dt * 10);
    yaw += (yawUser + 0.1 * Math.sin(clock * 0.35) * sway - yaw) * e; pitch += (pitchUser - pitch) * e;
    render(dt);
    requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); stepValve(0); updatePanel(); render(0);
  window.addEventListener('resize', function () { resize(); if (!running) render(0); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measured = false; if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
