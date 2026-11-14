/* Pump article: 3D model of P-101, a horizontal end-suction centrifugal pump with a clear front cover
   (needs three.js r128+ as window.THREE). The hydraulics repeat the article's worked example: 850 kg/m3,
   0.60 mPa.s, rated 8.09 m3/h at 46.9 m, NPSHa 12.6 m, shaft power 1.95 kW, and the pump and system curves of
   its Figure 1 (with the control valve as a fixed opening). Illustrative assumptions: vapour pressure above
   20 C (a curve through the article's 2.9 kPa at 20 C), NPSH required against flow, and the power curve. */
(function () {
  'use strict';
  var fig = document.getElementById('pm3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.pm3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.pm3d-lines');
  var inValve = $('pm3d-valve'), inSpeed = $('pm3d-speed'), inLevel = $('pm3d-level'), inTemp = $('pm3d-temp');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- hydraulics (same constants and formulas as the article) ----- */
  var G = 9.81, RHO = 850, MU = 0.0006, Q_N = 6250 / RHO, Q_R = Q_N * 1.1;
  var D_DIS = 0.0409, L_DIS = 60, D_SUC = 0.0525, L_SUC = 8, P_R = 1e5, Z_R = 8, DP_E = 0.5e5, DP_CV = 1.2e5, DP_MISC = 0.2e5, VALVE0 = 60;
  function darcy(q, D, L) { /* Swamee-Jain friction factor, Darcy-Weisbach pressure drop (Pa) */
    if (q <= 0) return 0;
    var v = q / 3600 / (Math.PI * D * D / 4), Re = RHO * v * D / MU, lg = Math.log(0.045e-3 / (3.7 * D) + 5.74 / Math.pow(Re, 0.9)) / Math.LN10;
    return 0.25 / (lg * lg) * L / D * RHO * v * v / 2;
  }
  function sysH(q, valve, level) {
    var r = q / Q_R, pd = P_R + RHO * G * Z_R + darcy(q, D_DIS, L_DIS) + (DP_E + DP_MISC) * r * r + DP_CV * r * r * Math.pow(VALVE0 / valve, 2);
    return (pd - (RHO * G * level - darcy(q, D_SUC, L_SUC))) / (RHO * G);
  }
  var H_R = sysH(Q_R, VALVE0, 1.0), SHUT = H_R * 1.22;
  /* affinity laws: at speed fraction n the head scales with n squared and the flow with n */
  function pumpH(q, k, n) { n = n == null ? 1 : n; return (n * n * SHUT - (SHUT - H_R) * Math.pow(q / Q_R, 2)) * (k == null ? 1 : k); }
  function pvap(t) { return Math.pow(10, 6.95464 - 1344.8 / (t + 219.482)) * 133.322; }       /* Pa; gives 2.9 kPa at 20 C */
  function npshr(q, n) { return 1.2 * n * n + 1.3 * Math.pow(q / Q_R, 2); }                     /* 2.5 m at rated flow and full speed */
  function solve(valve, level, k, n) {
    if (pumpH(0, k, n) <= sysH(0, valve, level)) return 0;                                      /* shutoff head below the static head: no flow */
    var lo = 0, hi = 14, i, m; for (i = 0; i < 40; i++) { m = (lo + hi) / 2; if (pumpH(m, k, n) > sysH(m, valve, level)) lo = m; else hi = m; } return (lo + hi) / 2;
  }
  var S = { valve: 60, n: 1, level: 1, temp: 20, q: Q_R, h: H_R, ps: 0.07, pd: 3.98, pa: 2.78, dpv: 120, na: 12.6, nr: 2.5, pw: 1.95, cav: 0, k: 1 };
  var lastKey = 'design';
  var SAY = {
    design: 'Design point: with the valve at its design opening the pump delivers the rated 8.1 m³/h at 46.9 m, and NPSH available is 12.6 m against 2.5 m required.',
    close: 'Closing the valve steepens the system curve. The operating point climbs back along the pump curve: less flow, more head.',
    open: 'Opening the valve flattens the system curve. The pump runs out along its curve: more flow, less head and more power.',
    low: 'A lower tank level means less pressure at the pump inlet, so NPSH available falls metre for metre.',
    high: 'A higher tank level adds pressure at the pump inlet, and with it NPSH available.',
    hot: 'Hotter liquid has a higher vapour pressure, which eats into NPSH available. Near the boiling point the margin disappears.',
    vfd: 'Slowing the pump with the VFD lowers the whole pump curve. Head falls with the square of speed and power with the cube, and no pressure is wasted across a throttled valve.',
    noflow: 'At this speed the pump\'s shutoff head is below the static head of the system, so it cannot push liquid up to the reactor. The flow is zero.',
    cav: 'Cavitation: the pressure at the impeller eye has fallen to the liquid\'s vapour pressure. Vapour bubbles form and collapse inside the impeller, and the pump loses head.'
  };
  function calc(changed) {
    S.valve = parseFloat(inValve.value); S.n = parseFloat(inSpeed.value) / 100; S.level = parseFloat(inLevel.value); S.temp = parseFloat(inTemp.value);
    var n = S.n, q = solve(S.valve, S.level, 1, n), na = (101325 - pvap(S.temp)) / (RHO * G) + S.level - darcy(q, D_SUC, L_SUC) / (RHO * G), nr = npshr(q, n), k = 1;
    if (q > 0 && na < nr) { /* cavitating: the pump sheds head; settle on the degraded curve */
      k = Math.max(0.55, 1 - 0.45 * (nr - na) / nr); q = solve(S.valve, S.level, k, n);
      na = (101325 - pvap(S.temp)) / (RHO * G) + S.level - darcy(q, D_SUC, L_SUC) / (RHO * G); nr = npshr(q, n);
    }
    var r = q / Q_R;
    S.q = q; S.k = k; S.h = pumpH(q, k, n); S.na = na; S.nr = nr; S.cav = k < 1 ? Math.min(1, (1 - k) / 0.3 + 0.25) : 0;
    S.ps = (RHO * G * S.level - darcy(q, D_SUC, L_SUC)) / 1e5; S.pd = S.ps + RHO * G * S.h / 1e5;
    S.dpv = DP_CV * r * r * Math.pow(VALVE0 / S.valve, 2) / 1000; S.pa = S.pd - S.dpv / 100;       /* kPa across the valve; barg after it */
    S.pw = (0.95 * n * n * n + 1.0 * n * n * r) * (k < 1 ? 0.5 + 0.5 * k : 1);
    $('pm3d-valve-o').textContent = S.valve.toFixed(0) + '%'; $('pm3d-speed-o').textContent = (n * 100).toFixed(0) + '% · ' + (60 * n).toFixed(0) + ' Hz · ' + (Math.round(3500 * n / 10) * 10).toLocaleString('en-CA') + ' rpm';
    $('pm3d-level-o').textContent = S.level.toFixed(1) + ' m'; $('pm3d-temp-o').textContent = S.temp.toFixed(0) + ' °C';
    $('pm3d-q').textContent = q.toFixed(2) + ' m³/h'; $('pm3d-h').textContent = S.h.toFixed(1) + ' m'; $('pm3d-pd').textContent = S.pd.toFixed(2) + ' barg';
    $('pm3d-dpv').textContent = S.dpv.toFixed(0) + ' kPa';
    $('pm3d-npsh').textContent = Math.max(0, na).toFixed(1) + ' / ' + nr.toFixed(1) + ' m'; $('pm3d-pw').textContent = S.pw.toFixed(2) + ' kW';
    var chip = $('pm3d-chip'); chip.textContent = q <= 0 ? 'No flow' : k < 1 ? 'Cavitating' : 'Running normally'; chip.classList.toggle('is-bad', k < 1 || q <= 0);
    var design = S.valve === 60 && n === 1 && Math.abs(S.level - 1) < 0.001 && S.temp === 20, key = lastKey;
    if (design) key = 'design';
    else if (q <= 0) key = 'noflow';
    else if (k < 1) key = 'cav';
    else if (changed === 'speed') key = n < 1 ? 'vfd' : key;
    else if (changed === 'valve') key = S.valve < 60 ? 'close' : S.valve > 60 ? 'open' : key;
    else if (changed === 'level') key = S.level < 1 ? 'low' : S.level > 1 ? 'high' : key;
    else if (changed === 'temp') key = S.temp > 20 ? 'hot' : key;
    if ((key === 'design' && !design) || (key === 'cav' && k >= 1) || (key === 'noflow' && q > 0) || (key === 'vfd' && n >= 1))
      key = n < 1 ? 'vfd' : S.temp > 20 ? 'hot' : S.valve !== 60 ? (S.valve < 60 ? 'close' : 'open') : (S.level < 1 ? 'low' : 'high');
    if (key !== lastKey) { lastKey = key; $('pm3d-say').textContent = SAY[key]; }
    var narrow = !wideNow;
    tags.suc.el.textContent = narrow ? 'Suction · ' + S.ps.toFixed(2) + ' barg' : 'Suction from T-101 · ' + S.ps.toFixed(2) + ' barg · ' + S.temp.toFixed(0) + ' °C';
    tags.dis.el.textContent = 'Discharge · ' + S.pd.toFixed(2) + ' barg';
    tags.val.el.textContent = (narrow ? 'Valve · ' : 'Control valve, downstream of pump · ') + S.valve.toFixed(0) + (narrow ? '% · ΔP ' : '% open · ΔP ') + S.dpv.toFixed(0) + ' kPa';
    tags.out.el.textContent = (narrow ? 'To E-101 · ' : 'To E-101, R-101 · ') + (q > 0 ? S.pa.toFixed(2) + ' barg' : 'no flow');
    tags.vfd.el.textContent = 'VFD · ' + (n * 100).toFixed(0) + '% · ' + (Math.round(3500 * n / 10) * 10).toLocaleString('en-CA') + ' rpm';
    measured = false; chart();
    if (ok) { paint(); if (!running) render(0); }
  }
  /* small live chart: pump curve, system curve for this valve opening, operating point */
  function chart() {
    var el = $('pm3d-svg'), X = function (q) { return 34 + q / 12 * 252; }, Y = function (h) { return 162 - h / 70 * 150; }, s = '', q, d1 = '', d2 = '', d0 = '';
    for (q = 0; q <= 70; q += 10) s += '<line x1="34" x2="286" y1="' + Y(q) + '" y2="' + Y(q) + '" stroke="rgba(255,255,255,.10)"/><text x="29" y="' + (Y(q) + 3.5) + '" text-anchor="end">' + q + '</text>';
    for (q = 0; q <= 12; q += 2) s += '<text x="' + X(q) + '" y="175" text-anchor="middle">' + q + '</text>';
    s += '<text x="160" y="188" text-anchor="middle">Flow (m³/h)</text><text x="9" y="90" text-anchor="middle" transform="rotate(-90 9 90)">Head (m)</text>';
    for (q = 0; q <= 12.001; q += 0.25) {
      var hp = pumpH(q, S.k, S.n), hs = sysH(q, S.valve, S.level), h0 = pumpH(q, 1, 1);
      if (hp >= 0) d1 += (d1 ? 'L' : 'M') + X(q).toFixed(1) + ' ' + Y(hp).toFixed(1);
      if (h0 >= 0) d0 += (d0 ? 'L' : 'M') + X(q).toFixed(1) + ' ' + Y(h0).toFixed(1);
      if (hs <= 70) d2 += (d2 ? 'L' : 'M') + X(q).toFixed(1) + ' ' + Y(hs).toFixed(1);
    }
    if (S.k < 1 || S.n < 1) s += '<path d="' + d0 + '" fill="none" stroke="#FF8A3D" stroke-width="1.2" stroke-dasharray="3 3" opacity=".55"/>';
    s += '<path d="' + d2 + '" fill="none" stroke="#5EC8FF" stroke-width="2"/><path d="' + d1 + '" fill="none" stroke="#FF8A3D" stroke-width="2"/>';
    s += '<circle cx="' + X(Q_R).toFixed(1) + '" cy="' + Y(H_R).toFixed(1) + '" r="3.2" fill="none" stroke="#fff" stroke-width="1.2" opacity=".7"/>';
    s += '<circle cx="' + X(S.q).toFixed(1) + '" cy="' + Y(S.h).toFixed(1) + '" r="4.6" fill="#8DC63F" stroke="#061833" stroke-width="1.5"/>';
    s += '<text x="282" y="' + (Y(sysH(11.6, S.valve, S.level)) > 20 ? Math.max(14, Y(sysH(11.6, S.valve, S.level)) - 6) : 14) + '" text-anchor="end" style="fill:#5EC8FF;font-weight:600">System</text>';
    s += '<text x="40" y="' + (Y(pumpH(0.6, S.k, S.n)) - 6) + '" style="fill:#FF8A3D;font-weight:600">Pump</text>';
    el.innerHTML = s;
  }
  /* pressure colour: blue at 0 barg through cyan, green and yellow to red at 5 barg */
  var STOPS = [[0, 40, 70, 200], [1.25, 40, 190, 230], [2.5, 90, 210, 110], [3.75, 250, 210, 60], [5, 240, 70, 50]];
  function presRGB(p, out) {
    p = Math.max(0, Math.min(5, p));
    for (var i = 1; i < STOPS.length; i++) if (p <= STOPS[i][0]) {
      var a = STOPS[i - 1], b = STOPS[i], u = (p - a[0]) / (b[0] - a[0]);
      out[0] = (a[1] + (b[1] - a[1]) * u) / 255; out[1] = (a[2] + (b[2] - a[2]) * u) / 255; out[2] = (a[3] + (b[3] - a[3]) * u) / 255; return out;
    }
    return out;
  }
  /* share of the pressure rise reached at radius r: none in the eye, most of it across the impeller, the rest in the volute */
  var R_EYE = 0.6, R_IMP = 1.55;
  function rise(r) {
    if (r <= R_EYE) return -0.03;
    if (r <= R_IMP) return 0.72 * (r * r - R_EYE * R_EYE) / (R_IMP * R_IMP - R_EYE * R_EYE);
    return Math.min(1, 0.72 + 0.28 * (r - R_IMP) / 0.75);
  }
  function presAt(r) { return S.ps + (S.pd - S.ps) * rise(r); }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, impeller, coupling, plug, stem, field, fieldR, tints = [], lines = [], trc, trcPos, trcCol, bub, bubPos, bubCol, running = false;
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('pm3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.pm3d-drag').style.display = 'none'; }

  /* volute: seen from the suction side (z to the right, y up) the impeller turns anticlockwise. The casing radius
     grows from the cutwater round to the discharge, which leaves straight up on the right. */
  var A_T = 0.5, TAU = Math.PI * 2, R_MIN = 1.72, R_GROW = 0.95, WALL = 0.18, WID = 1.1, Y_TOP = 3.6;
  function Rv(a) { return R_MIN + R_GROW * (a - A_T) / TAU; }
  var R_END = Rv(TAU), Z_T = R_MIN * Math.cos(A_T), Y_T = R_MIN * Math.sin(A_T);
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.85));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.4); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); pivot.position.set(0, 0, 0); scene.add(pivot);
    model = new T.Group(); model.position.x = -PIV; pivot.add(model);
    var cast = mat(0x76849a), cut = mat(0xc3ccd8, 0.95, 0), bronze = mat(0xc8a04a, 0.45, 0.45), steel = mat(0xc9d0da, 0.4, 0.3), dark = mat(0x3f4b5e, 0.7, 0.2),
        motorM = mat(0x24528d, 0.5, 0.3), motorD = mat(0x1a3d6b, 0.6, 0.3);
    var glass = new T.MeshStandardMaterial({ color: 0xcfe6ff, transparent: true, opacity: 0.14, roughness: 0.1, metalness: 0, depthWrite: false, side: T.DoubleSide });
    var i, a;
    /* extrude a flat outline given in (z, y) along x, ending at xBack */
    function ext(pts, depth, xBack, m, holes) {
      var sh = new T.Shape(pts.map(function (p) { return new T.Vector2(p[0], p[1]); }));
      if (holes) holes.forEach(function (h) { sh.holes.push(new T.Path(h.map(function (p) { return new T.Vector2(p[0], p[1]); }))); });
      var mesh = new T.Mesh(new T.ExtrudeGeometry(sh, { depth: depth, bevelEnabled: false, curveSegments: 8 }), m);
      mesh.rotation.y = -Math.PI / 2; mesh.position.x = xBack; return mesh;
    }
    function cylX(r, x0, x1, m, seg, parent) { var c = new T.Mesh(new T.CylinderGeometry(r, r, x1 - x0, seg || 32), m); c.rotation.z = Math.PI / 2; c.position.x = (x0 + x1) / 2; (parent || model).add(c); return c; }
    function ringX(r0, r1, x0, x1, m, parent) { /* a flat-sided ring about the x axis */
      var g = new T.Group(), pr = [[r0, x0], [r1, x0], [r1, x1], [r0, x1]];
      for (var k = 0; k < 4; k++) g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(pr[k][0], pr[k][1]), new T.Vector2(pr[(k + 1) % 4][0], pr[(k + 1) % 4][1])], 40), m));
      g.rotation.z = -Math.PI / 2; (parent || model).add(g); return g;
    }
    function box(w, h, d, x, y, z, m) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y, z); model.add(b); return b; }

    /* wetted outline of the casing: down the right wall of the discharge, back round the spiral, up the cutwater */
    var B = [[R_END, Y_TOP], [R_END, 0]];
    for (i = 1; i <= 96; i++) { a = TAU - (TAU - A_T) * i / 96; B.push([Rv(a) * Math.cos(a), Rv(a) * Math.sin(a)]); }
    var O = B.map(function (p, k) { /* the same line pushed outward by the wall thickness */
      var p0 = B[Math.max(0, k - 1)], p1 = B[Math.min(B.length - 1, k + 1)], dz = p1[0] - p0[0], dy = p1[1] - p0[1], l = Math.hypot(dz, dy) || 1;
      return [p[0] - dy / l * WALL, p[1] + dz / l * WALL];
    });
    O[0] = [R_END + WALL, Y_TOP];
    model.add(ext(B.concat(O.slice().reverse()), WID, WID, [cut, cast]));                    /* right wall and spiral, front edge shown as a cut face */
    model.add(ext([[Z_T, Y_T - 0.02], [Z_T, Y_TOP], [Z_T - WALL, Y_TOP], [Z_T - WALL, Y_T + 0.16]], WID, WID, [cut, cast]));   /* cutwater wall */
    B.push([Z_T, Y_TOP]);
    model.add(ext(B, 0.2, WID + 0.2, cast));                                                  /* casing back wall */
    var eye = []; for (i = 0; i < 40; i++) { a = i / 40 * TAU; eye.push([0.74 * Math.cos(a), 0.74 * Math.sin(a)]); }
    var cover = ext(B, 0.07, 0, glass, [eye]); model.add(cover);                              /* clear front cover */
    var sp = new T.Mesh(new T.CylinderGeometry(0.8, 0.8, 1.95, 40, 1, true), glass); sp.rotation.z = Math.PI / 2; sp.position.x = -1.045; model.add(sp);   /* clear suction pipe */
    ringX(0.8, 1.15, -2.2, -2.02, cast); ringX(0.74, 0.95, -0.16, -0.07, cast);                 /* suction flange and neck ring */
    var zc = (Z_T + R_END) / 2, zw = R_END - Z_T, fy = Y_TOP + 0.1;                           /* discharge flange: an open frame */
    box(WID + 0.9, 0.22, 0.36, WID / 2, fy, Z_T - 0.36, cast); box(WID + 0.9, 0.22, 0.36, WID / 2, fy, R_END + 0.36, cast);
    box(0.4, 0.22, zw + 0.36, -0.2, fy, zc, cast); box(0.4, 0.22, zw + 0.36, WID + 0.2, fy, zc, cast);
    box(1.3, 0.42, 2.6, WID / 2, -2.72, 0, cast);                                             /* casing foot */

    /* impeller: back shroud, hub and six backward-curved vanes; turns anticlockwise seen from the suction side */
    impeller = new T.Group(); model.add(impeller);
    cylX(R_IMP, 0.8, 0.9, bronze, 48, impeller); cylX(0.34, 0.2, 0.9, bronze, 24, impeller);
    var mark = new T.Mesh(new T.BoxGeometry(0.03, 0.16, 0.5), new T.MeshBasicMaterial({ color: 0xffffff })); mark.position.set(0.79, 0, 1.22); impeller.add(mark);   /* a white mark on the shroud makes the turning rate easy to read */
    var nose = new T.Mesh(new T.ConeGeometry(0.3, 0.3, 24), steel); nose.rotation.z = Math.PI / 2; nose.position.x = 0.06; impeller.add(nose);
    for (i = 0; i < 6; i++) {
      var left = [], right = [], b0 = i / 6 * TAU;
      for (a = 0; a <= 14; a++) { var r = 0.62 + (R_IMP - 0.62) * a / 14, be = b0 - 1.15 * Math.log(r / 0.62) / Math.log(R_IMP / 0.62), dl = 0.05 / r; left.push([r * Math.cos(be + dl), r * Math.sin(be + dl)]); right.push([r * Math.cos(be - dl), r * Math.sin(be - dl)]); }
      impeller.add(ext(left.concat(right.reverse()), 0.6, 0.8, bronze));
    }
    /* drive train: shaft, back cover boss, bearing frame, coupling, motor, baseplate */
    cylX(0.22, 0.9, 4.5, steel, 20); cylX(0.62, WID + 0.2, 1.65, cast, 32); cylX(0.75, 1.65, 3.55, cast, 32); cylX(0.9, 3.35, 3.55, cast, 32);
    box(0.6, 2.25, 1.1, 2.6, -1.8, 0, cast);
    coupling = new T.Group(); model.add(coupling);
    cylX(0.5, 3.72, 4.0, dark, 24, coupling); cylX(0.5, 4.06, 4.34, dark, 24, coupling);
    for (i = 0; i < 4; i++) { var bb = new T.Mesh(new T.BoxGeometry(0.72, 0.14, 0.14), steel); a = i / 4 * TAU; bb.position.set(4.03, 0.38 * Math.sin(a), 0.38 * Math.cos(a)); coupling.add(bb); }
    cylX(1.5, 4.55, 8.5, motorM, 40); cylX(1.56, 8.5, 9.15, motorD, 40); cylX(1.56, 4.5, 4.7, motorD, 40);
    for (i = 0; i < 18; i++) { a = i / 18 * TAU; if (Math.sin(a) < -0.75) continue; var fin = new T.Mesh(new T.BoxGeometry(3.7, 0.2, 0.06), motorM); fin.position.set(6.55, 1.56 * Math.sin(a), 1.56 * Math.cos(a)); fin.rotation.x = -a + Math.PI / 2; model.add(fin); }
    box(1.1, 0.5, 0.95, 6.3, 1.72, 0, motorD); box(3.4, 1.42, 2.3, 6.55, -2.19, 0, motorD);
    box(10.6, 0.25, 4.0, 4.3, -3.02, 0, dark);

    /* discharge line: a clear pipe up from the nozzle, round an elbow and along to the control valve, which sits
       downstream of the pump, then on toward heater E-101 and reactor R-101 */
    var red = new T.Mesh(new T.CylinderGeometry(0.5, 0.78, 0.58, 32, 1, true), glass); red.position.set(WID / 2, Y_TOP + 0.5, ZM); model.add(red);
    var pc = new T.Curve(); pc.getPoint = function (t, target) { var fr = dframe(LV * 0.95 + (DTOT - LV * 0.95) * t); return (target || new T.Vector3()).set(fr[0], fr[1], fr[2]); };
    model.add(new T.Mesh(new T.TubeGeometry(pc, 90, 0.5, 28, false), glass));
    function band(r, len, z, m) { var c = new T.Mesh(new T.CylinderGeometry(r, r, len, 32, 1, true), m); c.rotation.x = Math.PI / 2; c.position.set(WID / 2, YP, z); model.add(c); return c; }
    band(0.7, 0.14, ZV - 0.86, cast); band(0.7, 0.14, ZV + 0.86, cast); band(0.66, 0.14, ZEND - 0.07, cast);
    var vb = new T.Mesh(new T.SphereGeometry(0.8, 32, 20), glass); vb.position.set(WID / 2, YP, ZV); model.add(vb);                 /* valve body, clear */
    var seat = new T.Mesh(new T.TorusGeometry(0.3, 0.07, 10, 28), steel); seat.rotation.x = Math.PI / 2; seat.position.set(WID / 2, YP - 0.3, ZV); model.add(seat);
    plug = new T.Mesh(new T.CylinderGeometry(0.27, 0.16, 0.42, 24), steel); plug.position.set(WID / 2, YP, ZV); model.add(plug);
    stem = new T.Mesh(new T.CylinderGeometry(0.06, 0.06, 1.5, 12), steel); stem.position.set(WID / 2, YP + 0.9, ZV); model.add(stem);
    var bon = new T.Mesh(new T.CylinderGeometry(0.26, 0.34, 0.5, 24), cast); bon.position.set(WID / 2, YP + 0.95, ZV); model.add(bon);
    var act = mat(0x8dc63f, 0.5, 0.2), ac = new T.Mesh(new T.CylinderGeometry(0.72, 0.72, 0.26, 32), act); ac.position.set(WID / 2, YP + 1.5, ZV); model.add(ac);
    var ac2 = new T.Mesh(new T.CylinderGeometry(0.3, 0.6, 0.2, 32), act); ac2.position.set(WID / 2, YP + 1.73, ZV); model.add(ac2);
    /* variable frequency drive: a cabinet beside the motor, wired to its terminal box */
    var cab = mat(0xd5dbe5, 0.6, 0.1), vx = 8.3, vz = 2.75;
    box(0.4, 1.5, 1.0, vx, -0.75, vz, cab); box(0.16, 1.55, 0.16, vx, -2.3, vz, dark);
    var disp = new T.Mesh(new T.PlaneGeometry(0.55, 0.3), new T.MeshBasicMaterial({ color: 0x8dc63f })); disp.rotation.y = -Math.PI / 2; disp.position.set(vx - 0.205, -0.35, vz); model.add(disp);
    var cc = new T.CatmullRomCurve3([new T.Vector3(vx, 0, vz), new T.Vector3(vx - 0.2, 1.2, vz - 0.5), new T.Vector3(7.2, 2.3, 1.2), new T.Vector3(6.3, 1.97, 0.2)]);
    model.add(new T.Mesh(new T.TubeGeometry(cc, 40, 0.05, 8, false), dark));
    /* a faint tint of liquid in the pipes, coloured by the local pressure; the streamlines carry the motion */
    function tint(geo, key) { var m = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.2, depthWrite: false }); var ms = new T.Mesh(geo, m); model.add(ms); tints.push({ m: m, key: key }); return ms; }
    var ts = tint(new T.CylinderGeometry(0.72, 0.72, 2.75, 32), 'ps'); ts.rotation.z = Math.PI / 2; ts.position.x = -1.3;
    [['pd', LV * 0.6, DV], ['pa', DV, DTOT]].forEach(function (q) {
      var c3 = new T.Curve(); c3.getPoint = function (t, target) { var fr = dframe(q[1] + (q[2] - q[1]) * t); return (target || new T.Vector3()).set(fr[0], fr[1], fr[2]); };
      tint(new T.TubeGeometry(c3, 60, 0.44, 20, false), q[0]);
    });

    /* pressure field on a plane just in front of the vanes: a fan of rings out to the casing wall, plus the discharge */
    var pos = [], col = [], idx = [], rr = [], NA = 200, NR = 26, j, base0;
    function bound(al) { return al < A_T ? Math.min(R_END / Math.cos(al), 9) : Rv(al) - 0.02; }
    for (i = 0; i <= NA; i++) { a = i / NA * TAU; var bd = bound(a);
      for (j = 0; j <= NR; j++) { var r3 = bd * j / NR; pos.push(0.14, r3 * Math.sin(a), r3 * Math.cos(a)); rr.push(r3); col.push(0, 0, 0); } }
    for (i = 0; i < NA; i++) for (j = 0; j < NR; j++) { var p0 = i * (NR + 1) + j, p1 = p0 + NR + 1; idx.push(p0, p1, p0 + 1, p1, p1 + 1, p0 + 1); }
    base0 = pos.length / 3;                                                                    /* discharge duct, above the line through the cutwater */
    for (i = 0; i <= 8; i++) { var z = Z_T + (R_END - Z_T) * i / 8, y0 = z * Math.tan(A_T); for (j = 0; j <= 8; j++) { pos.push(0.14, y0 + (Y_TOP + 0.2 - y0) * j / 8, z); rr.push(9); col.push(0, 0, 0); } }
    for (i = 0; i < 8; i++) for (j = 0; j < 8; j++) { p0 = base0 + i * 9 + j; p1 = p0 + 9; idx.push(p0, p1, p0 + 1, p1, p1 + 1, p0 + 1); }
    var fg = new T.BufferGeometry(); fg.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); fg.setAttribute('color', new T.Float32BufferAttribute(col, 3)); fg.setIndex(idx);
    field = new T.Mesh(fg, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.4, depthWrite: false, side: T.DoubleSide })); fieldR = rr; model.add(field);

    /* streamlines, each one continuous: along the suction pipe, into the eye, out through the impeller, round the
       volute, up the discharge, round the elbow and through the control valve. Liquid that leaves the impeller just
       after the cutwater travels furthest and ends up against the outer wall, so lines do not cross in the volute.
       Each point carries: position, how far up the pressure rise it is (2 = after the valve), and a relative speed. */
    var lm = new T.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.9 }), NL = 44, SWEEP = 1.6;
    function frac(v) { return v - Math.floor(v); }
    for (i = 0; i < NL; i++) {
      var a0 = i / NL * TAU + 0.07, a1 = a0 + SWEEP, s = ((a1 - A_T) % TAU + TAU) % TAU + A_T;      /* where it meets the volute, A_T .. A_T + 2pi */
      if (s > TAU - 0.3) continue;
      var f = 1 - (s - A_T) / (TAU - A_T), pts = [], k, u, al, rad, zf = 1.62 + (0.08 + 0.84 * f) * (R_END - 1.62);
      var rs = 0.14 + 0.5 * Math.sqrt(frac(i * 0.7548 + 0.2)), ph0 = a0 - 0.5;
      for (k = 0; k <= 14; k++) pts.push([-2.65 + 1.95 * k / 14, rs * Math.sin(ph0), rs * Math.cos(ph0), 0, 0.8]);                    /* suction pipe */
      for (k = 1; k <= 22; k++) { u = k / 22; rad = rs + (0.62 - rs) * u * u; al = ph0 + 0.5 * u; pts.push([-0.7 + 0.8 * Math.pow(u, 0.75), rad * Math.sin(al), rad * Math.cos(al), -0.03 * u, 0.75]); }   /* turn into the eye */
      for (k = 1; k <= 60; k++) { u = k / 60; rad = 0.62 + 0.98 * u; al = a0 + SWEEP * Math.log(rad / 0.62) / Math.log(1.6 / 0.62); pts.push([0.1, rad * Math.sin(al), rad * Math.cos(al), rise(rad), 0.45 + 0.95 * u]); }   /* through the impeller */
      var steps = Math.max(10, Math.round((TAU - s) / 0.03));
      for (k = 1; k <= steps; k++) { al = s + (TAU - s) * k / steps; var tg = 1.62 + (0.08 + 0.84 * f) * (Rv(al) - 1.62); u = Math.min(1, (al - s) / 0.8); u = u * u * (3 - 2 * u); rad = 1.6 + (tg - 1.6) * u; pts.push([0.1, rad * Math.sin(al), rad * Math.cos(al), rise(rad), 1.0]); }   /* round the volute */
      var zl = pts[pts.length - 1][2], U = 0.4 * Math.sqrt(frac(i * 0.7548 + 0.55)), th = i * 2.39996, tu = U * Math.cos(th), tv = U * Math.sin(th);
      for (k = 1; k <= 20; k++) { u = k / 20; pts.push([0.1 + (WID / 2 + tu * 0.9 - 0.1) * u * u * 0.6, Y_TOP * u, zl + (zf - zl) * Math.min(1, u * 2.2), 1, 1.05]); }   /* up the discharge nozzle */
      var x0 = pts[pts.length - 1][0] - WID / 2, z0 = zf - ZM;
      for (k = 1; k <= 110; k++) {                                                                                                      /* pipe, elbow and valve */
        var d = DTOT * k / 110, fr = dframe(d), b = Math.min(1, d / 1.0); b = b * b * (3 - 2 * b);
        var ou = x0 + (tu - x0) * b, ov = z0 + (tv - z0) * b, w = Math.exp(-Math.pow((d - DV) / 0.4, 2));
        pts.push([fr[0] + ou * fr[3] + ov * fr[6], fr[1] + ou * fr[4] + ov * fr[7], fr[2] + ou * fr[5] + ov * fr[8], d < DV ? 1 : 2, 1.0 + 1.1 * w,
                  fr[0], fr[1], fr[2], ou * fr[3] + ov * fr[6], ou * fr[4] + ov * fr[7], ou * fr[5] + ov * fr[8], w]);
      }
      lines.push(makeLine(pts));
    }
    function makeLine(pts) {
      var g = new T.BufferGeometry(), arr = new Float32Array(pts.length * 3), len = [0], k2;
      for (k2 = 0; k2 < pts.length; k2++) { arr[k2 * 3] = pts[k2][0]; arr[k2 * 3 + 1] = pts[k2][1]; arr[k2 * 3 + 2] = pts[k2][2]; if (k2) len.push(len[k2 - 1] + Math.hypot(pts[k2][0] - pts[k2 - 1][0], pts[k2][1] - pts[k2 - 1][1], pts[k2][2] - pts[k2 - 1][2])); }
      g.setAttribute('position', new T.BufferAttribute(arr, 3)); g.setAttribute('color', new T.BufferAttribute(new Float32Array(pts.length * 3), 3));
      var ln = new T.Line(g, lm); ln.frustumCulled = false; model.add(ln);
      var tr = [], n = 7; for (k2 = 0; k2 < n; k2++) tr.push((k2 + Math.random() * 0.7) / n);
      return { pts: pts, len: len, total: len[len.length - 1], tr: tr, line: ln };
    }
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
    var nT = 0; lines.forEach(function (l) { nT += l.tr.length * TAIL; });
    var q = points(nT, 0.15); trc = q[0]; trcPos = q[1]; trcCol = q[2];
    q = points(NBUB, 0.3); bub = q[0]; bubPos = q[1]; bubCol = q[2];
  }
  /* centreline of the discharge line beyond the nozzle, by distance d: straight up, a quarter-turn elbow, then a
     level run that holds the control valve. Returns the centre and two unit vectors across the pipe. */
  var LV = 0.8, RE = 0.8, LR = 4.4, DTOT = LV + RE * Math.PI / 2 + LR, DV = LV + RE * Math.PI / 2 + 2.3, YP = Y_TOP + LV + RE, ZM0 = (Z_T + R_END) / 2, ZM = ZM0, ZV = ZM0 + RE + 2.3, ZEND = ZM0 + RE + LR;
  function dframe(d) {
    var x = WID / 2;
    if (d <= LV) return [x, Y_TOP + d, ZM0, 1, 0, 0, 0, 0, 1];
    var e = (d - LV) / RE;
    if (e <= Math.PI / 2) return [x, Y_TOP + LV + RE * Math.sin(e), ZM0 + RE * (1 - Math.cos(e)), 1, 0, 0, 0, -Math.sin(e), Math.cos(e)];
    return [x, YP, ZM0 + RE + (d - LV - RE * Math.PI / 2), 1, 0, 0, 0, -1, 0];
  }
  var rgb = [0, 0, 0], TAIL = 5, NBUB = 220, PIV = 3.4, bubs = [];
  for (var i = 0; i < NBUB; i++) bubs.push({ on: false, r: 0, a: 0, x: 0, life: 0 });
  function presZone(z) { return z >= 2 ? S.pa : S.ps + (S.pd - S.ps) * z; }
  function paint() { /* recolour the pressure field, streamlines and liquid tints, and set the valve, for the current state */
    var col = field.geometry.attributes.color, k, cf = 0.2 + 0.7 * S.valve / 100;
    for (k = 0; k < fieldR.length; k++) { presRGB(presAt(fieldR[k]), rgb); col.setXYZ(k, rgb[0], rgb[1], rgb[2]); }
    col.needsUpdate = true;
    lines.forEach(function (l) {
      var c = l.line.geometry.attributes.color, ps = l.line.geometry.attributes.position, q;
      for (k = 0; k < l.pts.length; k++) {
        q = l.pts[k]; presRGB(presZone(q[3]), rgb); c.setXYZ(k, Math.min(1, rgb[0] * 0.6 + 0.45), Math.min(1, rgb[1] * 0.6 + 0.45), Math.min(1, rgb[2] * 0.6 + 0.45));
        if (q.length > 5) { var sc = 1 - (1 - cf) * q[11]; q[0] = q[5] + q[8] * sc; q[1] = q[6] + q[9] * sc - 0.3 * q[11] * (1 - sc); q[2] = q[7] + q[10] * sc; ps.setXYZ(k, q[0], q[1], q[2]); }   /* squeeze through the valve seat */
      }
      c.needsUpdate = true; ps.needsUpdate = true;
    });
    tints.forEach(function (t) { presRGB(S[t.key], rgb); t.m.color.setRGB(rgb[0], rgb[1], rgb[2]); });
    var lift = 0.5 * S.valve / 100; plug.position.y = YP - 0.32 + lift; stem.position.y = YP + 0.55 + lift;
  }
  var spin = 0, SPIN = 13.2, RPM = 3500;   /* 2.1 turns a second on screen at full speed; full speed taken as a 2-pole motor at 60 Hz */
  function step(dt) {
    var sf = S.q / Q_R, j, n, t, k, l, u, d, lo, hi, mid, fr, seg = 1, ti = 0;
    spin += dt * SPIN * S.n; impeller.rotation.x = -spin; coupling.rotation.x = -spin;   /* slow motion, strictly in proportion to speed */
    for (j = 0; j < lines.length; j++) {
      l = lines[j];
      for (n = 0; n < l.tr.length; n++) {
        u = l.tr[n];
        for (t = 0; t < TAIL; t++) {
          var uu = u - t * 0.0045, vis = 1 - t / TAIL; if (uu < 0) { uu = 0; vis = 0; } if (sf <= 0) vis *= 0.35;
          d = uu * l.total; lo = 0; hi = l.len.length - 1;
          while (hi - lo > 1) { mid = (lo + hi) >> 1; if (l.len[mid] <= d) lo = mid; else hi = mid; }
          fr = (d - l.len[lo]) / Math.max(1e-6, l.len[hi] - l.len[lo]);
          k = ti * 3; trcPos[k] = l.pts[lo][0] + (l.pts[hi][0] - l.pts[lo][0]) * fr - 0.01; trcPos[k + 1] = l.pts[lo][1] + (l.pts[hi][1] - l.pts[lo][1]) * fr; trcPos[k + 2] = l.pts[lo][2] + (l.pts[hi][2] - l.pts[lo][2]) * fr;
          if (t === 0) seg = l.pts[lo][4];
          trcCol[k] = vis; trcCol[k + 1] = vis; trcCol[k + 2] = vis; ti++;
        }
        u += dt * 2.2 * sf * seg / l.total; if (u >= 1) u -= 1; l.tr[n] = u;
      }
    }
    /* cavitation: vapour bubbles appear at the vane inlets, are carried outward and collapse as the pressure recovers */
    var want = S.cav * 260;
    for (j = 0; j < NBUB; j++) {
      var b = bubs[j]; k = j * 3;
      if (!b.on) { if (dt > 0 && Math.random() < dt * want / NBUB * 3) { b.on = true; b.r = 0.62 + Math.random() * 0.12; b.a = Math.random() * TAU; b.x = 0.22 + Math.random() * 0.5; b.life = 0; } }
      else { b.r += dt * 0.55; b.a += dt * 3.2; b.life += dt; if (b.r > 0.95 + 0.45 * S.cav) b.on = false; }
      var v = b.on ? Math.min(1, b.life * 6) : 0;
      bubPos[k] = b.x; bubPos[k + 1] = b.r * Math.sin(b.a); bubPos[k + 2] = b.r * Math.cos(b.a); bubCol[k] = v; bubCol[k + 1] = v; bubCol[k + 2] = v;
    }
    trc.geometry.attributes.position.needsUpdate = true; trc.geometry.attributes.color.needsUpdate = true;
    bub.geometry.attributes.position.needsUpdate = true; bub.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- names and stream tags: two rows, above and below the pump, each joined to its part ----- */
  var ITEMS = [
    ['t', 'Pump discharge · 3.98 barg', WID / 2, Y_TOP + 0.95, ZM0 - 0.5, 'T', 'dis', 1],
    ['t', 'Control valve, downstream of the pump · 60% open · ΔP 120 kPa', WID / 2, YP + 1.85, ZV, 'T', 'val'],
    ['t', 'To E-101 and R-101 · 2.78 barg', WID / 2, YP + 0.5, ZEND - 0.1, 'T', 'out'],
    ['t', 'Suction from T-101 · 0.07 barg · 20 °C', -2.1, -0.8, 0.2, 'B', 'suc'], ['l', 'Impeller', 0.2, -0.95, -0.7, 'B'],
    ['l', 'Volute casing', 0.55, -2.3, 0.9, 'B'], ['l', 'Motor, 3 kW', 6.6, -1.2, 1.5, 'B'], ['t', 'VFD · 100% speed', 8.1, -1.5, 2.75, 'B', 'vfd', 1]
  ];
  var tags = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'pm3d-tag' : 'pm3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, x: 0, tag: n[0] === 't', wideOnly: !!n[7] };
    if (n[6]) tags[n[6]] = it; return it;
  });
  var W = 0, H = 0, measured = false, wideNow = true, v3 = T ? new T.Vector3() : null;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function place() {
    if (!measured) { items.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    var pt = { x: 0, y: 0 };
    ['T', 'B'].forEach(function (band) {
      items.forEach(function (q) { if (q.wideOnly) { var hide = !wideNow; if (q.hidden !== hide) { q.hidden = hide; q.el.style.display = hide ? 'none' : ''; q.path.style.display = hide ? 'none' : ''; q.dot.style.display = hide ? 'none' : ''; } } });
      var list = items.filter(function (q) { return q.n[5] === band && !q.hidden && (q.tag || (wideNow && q.w > 0)); }), i, l, gap = 8;
      list.forEach(function (q) { toScreen(q.n[2], q.n[3], q.n[4], pt); q.ax = pt.x; q.ay = pt.y; q.x = pt.x; });
      list.sort(function (a, b) { return a.ax - b.ax; });
      for (i = 0; i < list.length; i++) { l = list[i]; l.x = Math.max(l.x, 8 + l.w / 2, i ? list[i - 1].x + (list[i - 1].w + l.w) / 2 + gap : -1e9); }
      for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.x = Math.min(l.x, W - 8 - l.w / 2, i < list.length - 1 ? list[i + 1].x - (list[i + 1].w + l.w) / 2 - gap : 1e9); }
      var by = band === 'T' ? 52 : H - 26;
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
  var yawUser = 1.02, pitchUser = 0.2, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var px = Math.min((W - (wideNow ? 40 : 16)) / (wideNow ? 9.4 : 10.6), (H - 150) / 10.6), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180));
    camera.aspect = W / H; camera.position.set(0.6, 1.85, dist); camera.lookAt(0.6, 1.85, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0);
    step(dt);
    pivot.updateMatrixWorld(true);
    renderer.render(scene, camera);
    place();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(0.15, Math.min(1.5, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.2, Math.min(0.6, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  inValve.addEventListener('input', function () { calc('valve'); });
  inSpeed.addEventListener('input', function () { calc('speed'); });
  inLevel.addEventListener('input', function () { calc('level'); });
  inTemp.addEventListener('input', function () { calc('temp'); });
  $('pm3d-reset').addEventListener('click', function () { inValve.value = 60; inSpeed.value = 100; inLevel.value = 1; inTemp.value = 20; calc(); });
  var btnNames = $('pm3d-names');
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
    yaw += (yawUser + 0.08 * Math.sin(clock * 0.3) * sway - yaw) * e; pitch += (pitchUser - pitch) * e;
    render(dt);
    requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce || !ok) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  if (ok) { build(); stage.classList.add('is-live'); }
  resize(); calc(); render(0);
  window.addEventListener('resize', function () { resize(); calc(); if (!running) render(0); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measured = false; if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
