/* Control valve article: 3D model of FV-104, a globe valve with a spring-and-diaphragm actuator, cut in half
   (needs three.js r128+ as window.THREE). The hydraulics repeat the article's worked example: 850 kg/m3,
   the pump curve and system of Part 1, rated 8.09 m3/h with 120 kPa across the valve, required Cv 7.87,
   a rated Cv of 25 and equal percentage trim. Illustrative assumptions: FL = 0.90, critical pressure 41 bar,
   rangeability 50. The vapour pressure slider is a what-if and changes nothing else. */
(function () {
  'use strict';
  var fig = document.getElementById('cv3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.cv3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.cv3d-lines');
  var inFlow = $('cv3d-flow'), inPv = $('cv3d-pv'), btnEq = $('cv3d-eq'), btnLin = $('cv3d-lin');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- hydraulics (same constants and formulas as the article) ----- */
  var G = 9.81, RHO = 850, MU = 0.0006, SG = 0.85, Q_N = 6250 / RHO, Q_R = Q_N * 1.1, PATM = 101.325;
  var D_DIS = 0.0409, L_DIS = 60, L_UP = 10, D_SUC = 0.0525, L_SUC = 8, P_R = 1e5, Z_R = 8, DP_E = 0.5e5, DP_CV = 1.2e5, DP_MISC = 0.2e5;
  var CV_R = 25, RANGE = 50, FL = 0.9, PC = 4100, PV0 = 2.9, PVMAX = 400, LMAX = 0.6;
  function darcy(q, D, L) { /* Swamee-Jain friction factor, Darcy-Weisbach pressure drop (Pa) */
    if (q <= 0) return 0;
    var v = q / 3600 / (Math.PI * D * D / 4), Re = RHO * v * D / MU, lg = Math.log(0.045e-3 / (3.7 * D) + 5.74 / Math.pow(Re, 0.9)) / Math.LN10;
    return 0.25 / (lg * lg) * L / D * RHO * v * v / 2;
  }
  var H_R = (P_R + RHO * G * Z_R + darcy(Q_R, D_DIS, L_DIS) + DP_E + DP_CV + DP_MISC - (RHO * G - darcy(Q_R, D_SUC, L_SUC))) / (RHO * G), SHUT = H_R * 1.22;
  function pumpH(q) { return SHUT - (SHUT - H_R) * Math.pow(q / Q_R, 2); }
  /* kPa absolute at the valve inlet (what the pump delivers) and at its outlet (what the system needs) */
  function pIn(q) { var r = q / Q_R; return (RHO * G - darcy(q, D_SUC, L_SUC) + RHO * G * pumpH(q) - DP_MISC * r * r - darcy(q, D_DIS, L_UP)) / 1000 + PATM; }
  function pOut(q) { var r = q / Q_R; return (P_R + RHO * G * Z_R + DP_E * r * r + darcy(q, D_DIS, L_DIS - L_UP)) / 1000 + PATM; }
  function at(q, pv) { /* Cv needed to pass q, allowing for choked flow */
    var a = pIn(q), b = pOut(q), dp = a - b, ff = 0.96 - 0.28 * Math.sqrt(pv / PC), ch = Math.max(1, FL * FL * (a - ff * pv)), choked = dp >= ch, eff = choked ? ch : dp;
    return { a: a, b: b, dp: dp, ch: ch, ff: ff, choked: choked, cv: eff > 0 ? q / (0.865 * Math.sqrt(eff / 100 / SG)) : 1e9 };
  }
  var S = { set: Q_R, q: Q_R, pv: PV0, trim: 'eq', a: 472.5, b: 352.5, dp: 120, ch: 380.5, pl: 324.4, cv: 7.87, x: 0.705, cav: 0, flash: false, choked: false, wide: false, ci: 0 };
  var lastKey = 'design';
  var SAY = {
    design: 'Design point: at the rated 8.09 m³/h the valve has 120 kPa to work with, needs a Cv of 7.87 and sits 70% open. The lowest pressure inside, 324 kPa abs, is far above the vapour pressure.',
    less: 'Less flow: the pump delivers more pressure and the system needs less, so the valve closes and absorbs the difference. Its pressure drop rises as its opening falls.',
    more: 'More flow: the pressure drop left for the valve shrinks while the flow grows, so the valve has to open quickly.',
    wide: 'The valve is wide open and passing all it can. The controller is asking for more than the pump and this valve can deliver.',
    linear: 'Linear trim: the same Cv is reached much lower in the travel. Everything from minimum to rated flow happens in the first third of the stroke, close to the seat.',
    vol: 'A more volatile liquid: the vapour pressure rises toward the lowest pressure in the valve. The gap between the two is the margin against cavitation.',
    cav: 'Cavitation: the pressure just past the seat has dipped below the vapour pressure. Bubbles form in the jet and collapse as the pressure recovers. In a real valve that means noise, vibration and pitted trim.',
    flash: 'Flashing: the outlet pressure is below the vapour pressure, so the bubbles do not collapse. A mixture of liquid and vapour leaves the valve.'
  };
  function calc(changed) {
    var pct = parseFloat(inFlow.value), sl = parseFloat(inPv.value), pv = PV0 + (PVMAX - PV0) * sl / 200, qs = pct / 100 * Q_N, q = qs, r = at(q, pv), wide = false, lo, hi, m, i;
    if (r.cv > CV_R) { wide = true; lo = 0.01; hi = qs; for (i = 0; i < 40; i++) { m = (lo + hi) / 2; if (at(m, pv).cv > CV_R) hi = m; else lo = m; } q = lo; r = at(q, pv); r.cv = CV_R; }
    var x = S.trim === 'eq' ? 1 + Math.log(r.cv / CV_R) / Math.log(RANGE) : r.cv / CV_R; x = Math.max(0, Math.min(1, x));
    var pl = r.choked ? r.ff * pv : r.a - r.dp / (FL * FL), flash = r.b <= pv, cav = !flash && pl <= pv;
    S.set = qs; S.q = q; S.pv = pv; S.a = r.a; S.b = r.b; S.dp = r.dp; S.ch = r.ch; S.pl = pl; S.cv = r.cv; S.x = x; S.flash = flash; S.cav = cav; S.choked = r.choked; S.wide = wide;
    S.ci = flash ? 1 : cav ? Math.max(0.3, Math.min(1, (pv - pl) / Math.max(1, r.b - pl))) : 0;
    $('cv3d-flow-o').textContent = qs.toFixed(2) + ' m³/h · ' + pct.toFixed(0) + '% of normal';
    $('cv3d-pv-o').textContent = (pv < 10 ? pv.toFixed(1) : pv.toFixed(0)) + ' kPa abs';
    $('cv3d-q').textContent = q.toFixed(2) + ' m³/h'; $('cv3d-x').textContent = (x * 100).toFixed(0) + '% open'; $('cv3d-cv').textContent = r.cv.toFixed(2) + ' of ' + CV_R;
    $('cv3d-dp').textContent = r.dp.toFixed(0) + ' kPa'; $('cv3d-pl').textContent = pl.toFixed(0) + ' kPa abs'; $('cv3d-ch').textContent = r.ch.toFixed(0) + ' kPa';
    var chip = $('cv3d-chip'), bad = flash || cav || wide;
    chip.textContent = (flash ? 'Flashing' : cav ? 'Cavitating' : wide ? 'Valve wide open' : 'Controlling normally') + ((flash || cav) && r.choked ? ' · choked' : '');
    chip.classList.toggle('is-bad', bad);
    var design = pct === 110 && sl === 0 && S.trim === 'eq', key = lastKey;
    if (design) key = 'design';
    else if (flash) key = 'flash';
    else if (cav) key = 'cav';
    else if (wide) key = 'wide';
    else if (changed === 'flow') key = pct < 110 ? 'less' : pct > 110 ? 'more' : key;
    else if (changed === 'trim') key = S.trim === 'lin' ? 'linear' : key;
    else if (changed === 'pv') key = sl > 0 ? 'vol' : key;
    if ((key === 'design' && !design) || (key === 'flash' && !flash) || (key === 'cav' && !cav) || (key === 'wide' && !wide) || (key === 'linear' && S.trim !== 'lin') || (key === 'vol' && sl === 0))
      key = S.trim === 'lin' ? 'linear' : sl > 0 ? 'vol' : pct < 110 ? 'less' : 'more';
    if (key !== lastKey) { lastKey = key; $('cv3d-say').textContent = SAY[key]; }
    var narrow = !wideNow;
    tags.inl.el.textContent = (narrow ? 'In · ' : 'Inlet · ') + r.a.toFixed(0) + (narrow ? '' : ' kPa abs');
    tags.low.el.textContent = (narrow ? 'Seat · ' : 'Lowest, just past the seat · ') + pl.toFixed(0) + (narrow ? '' : ' kPa abs');
    tags.out.el.textContent = (narrow ? 'Out · ' : 'Outlet · ') + r.b.toFixed(0) + ' kPa abs';
    tags.trv.el.textContent = 'Travel ' + (x * 100).toFixed(0) + '%' + (narrow ? '' : ' · Cv ' + r.cv.toFixed(2));
    tags.sig.el.textContent = 'Positioner · signal ' + (4 + 16 * x).toFixed(1) + ' mA';
    measured = false; chart();
    if (ok) { paint(); if (!running) render(0); }
  }
  /* small live chart: pressure through the valve against the vapour pressure */
  function prof(u) {
    function sm(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
    if (u < 0.5) return S.a + (S.pl - S.a) * sm((u - 0.3) / 0.2);
    return S.pl + (S.b - S.pl) * sm((u - 0.5) / 0.3);
  }
  function chart() {
    var el = $('cv3d-svg'), X = function (u) { return 38 + u * 248; }, Y = function (p) { return 160 - Math.max(0, Math.min(620, p)) / 600 * 146; }, s = '', p, u, d = '', area = '', open = false;
    for (p = 0; p <= 600; p += 100) s += '<line x1="38" x2="286" y1="' + Y(p) + '" y2="' + Y(p) + '" stroke="rgba(255,255,255,.10)"/><text x="33" y="' + (Y(p) + 3.5) + '" text-anchor="end">' + p + '</text>';
    s += '<text x="' + X(0.12) + '" y="174" text-anchor="middle">Inlet</text><text x="' + X(0.5) + '" y="174" text-anchor="middle">Seat</text><text x="' + X(0.9) + '" y="174" text-anchor="middle">Outlet</text>';
    s += '<text x="162" y="187" text-anchor="middle">Pressure through the valve (kPa abs)</text>';
    for (u = 0; u <= 1.0001; u += 0.01) {
      p = prof(u); d += (d ? 'L' : 'M') + X(u).toFixed(1) + ' ' + Y(p).toFixed(1);
      if (p < S.pv) { if (!open) { area += 'M' + X(u).toFixed(1) + ' ' + Y(S.pv).toFixed(1); open = true; } area += 'L' + X(u).toFixed(1) + ' ' + Y(p).toFixed(1); }
      else if (open) { area += 'L' + X(u).toFixed(1) + ' ' + Y(S.pv).toFixed(1) + 'Z'; open = false; }
    }
    if (open) area += 'L' + X(1).toFixed(1) + ' ' + Y(S.pv).toFixed(1) + 'Z';
    if (area) s += '<path d="' + area + '" fill="#FF7A5C" opacity=".45"/>';
    s += '<line x1="38" x2="286" y1="' + Y(S.pv).toFixed(1) + '" y2="' + Y(S.pv).toFixed(1) + '" stroke="#FF8A3D" stroke-width="1.4" stroke-dasharray="4 3"/>';
    s += '<text x="' + (S.pv > 60 ? 42 : 284) + '" y="' + (Y(S.pv) + (S.pv > 60 ? 11 : -4)).toFixed(1) + '" text-anchor="' + (S.pv > 60 ? 'start' : 'end') + '" style="fill:#FF8A3D;font-weight:600">Vapour pressure</text>';
    s += '<path d="' + d + '" fill="none" stroke="#5EC8FF" stroke-width="2.2"/>';
    [[0.12, S.a, -7], [0.5, S.pl, 13], [0.9, S.b, -7]].forEach(function (q) {
      s += '<circle cx="' + X(q[0]).toFixed(1) + '" cy="' + Y(q[1]).toFixed(1) + '" r="3.6" fill="' + (q[0] === 0.5 ? '#8DC63F' : '#fff') + '" stroke="#061833" stroke-width="1.2"/>';
      s += '<text x="' + X(q[0]).toFixed(1) + '" y="' + (Y(q[1]) + q[2]).toFixed(1) + '" text-anchor="middle" style="fill:#fff;font-weight:600">' + q[1].toFixed(0) + '</text>';
    });
    el.innerHTML = s;
  }
  /* pressure colour: blue at 100 kPa abs through cyan, green and yellow to red at 600 kPa abs */
  var STOPS = [[0, 40, 70, 200], [1.25, 40, 190, 230], [2.5, 90, 210, 110], [3.75, 250, 210, 60], [5, 240, 70, 50]];
  function presRGB(kpa, out) {
    var p = Math.max(0, Math.min(5, (kpa - 100) / 100));
    for (var i = 1; i < STOPS.length; i++) if (p <= STOPS[i][0]) {
      var a = STOPS[i - 1], b = STOPS[i], u = (p - a[0]) / (b[0] - a[0]);
      out[0] = (a[1] + (b[1] - a[1]) * u) / 255; out[1] = (a[2] + (b[2] - a[2]) * u) / 255; out[2] = (a[3] + (b[3] - a[3]) * u) / 255; return out;
    }
    return out;
  }
  /* pressure at a point of the cut plane: inlet pressure up to the seat, lowest in the gap, recovering beyond it */
  var RS = 0.42, lift = LMAX * 0.705;
  function presXY(x, y) {
    var up;
    if (x <= -1.7) up = true; else if (x >= 1.08) up = false;
    else up = y < (x < -0.75 ? 0.6 - (x + 1.7) / 0.95 * 0.46 : x <= 0.42 ? 0.12 : -(x - 0.42) / 0.66 * 0.23 + 0.06);
    var ty = 0.12 + lift / 2, d = Math.min(Math.hypot(x - 0.47, y - ty), Math.hypot(x + 0.47, y - ty)), t;
    if (up) { t = Math.max(0, 1 - d / 0.6); return S.a + (S.pl - S.a) * t * t; }
    t = Math.min(1, d / 1.5); return S.pl + (S.b - S.pl) * t * t * (3 - 2 * t);
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, trim, spring, flex = null, air = null, airMat, flexMat, field, fieldXY, tints = {}, lines = [], trc, trcPos, trcCol, bub, bubPos, bubCol, running = false;
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('cv3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.cv3d-drag').style.display = 'none'; }

  /* outline of the flow passage on the cut plane (x along the pipe, y up): wall A runs along the bottom from inlet to
     outlet and carries the right half of the seat; wall B runs along the top and carries the left half. The third
     value marks a corner that stays sharp. */
  var WALL_A = [[-3.2, -0.5, 1], [-1.7, -0.5], [-1.1, -0.72], [-0.4, -1.12], [0.45, -1.12], [0.92, -0.8], [1.0, -0.35], [0.42, -0.12, 1], [0.42, 0.12, 1], [0.75, 0.12], [1.15, -0.1], [1.6, -0.5], [3.2, -0.5, 1]];
  var WALL_B1 = [[-3.2, 0.5, 1], [-1.7, 0.5], [-1.2, 0.2], [-0.75, -0.12], [-0.42, -0.12, 1], [-0.42, 0.12, 1], [-0.8, 0.4], [-0.85, 0.9], [-0.6, 1.2], [-0.6, 1.6, 1]];
  var WALL_B2 = [[0.6, 1.6, 1], [0.6, 1.35], [0.75, 1.15], [1.15, 0.75], [1.7, 0.5], [3.2, 0.5, 1]];
  function smoothPath(pts) { /* round the corners that are not marked sharp (two rounds of corner cutting) */
    var out = [], run = [pts[0]], i, k;
    function flush() {
      var r = run;
      for (k = 0; k < 2 && r.length > 2; k++) {
        var n = [r[0]];
        for (var j = 0; j < r.length - 1; j++) { var a = r[j], b = r[j + 1]; n.push([a[0] * 0.75 + b[0] * 0.25, a[1] * 0.75 + b[1] * 0.25], [a[0] * 0.25 + b[0] * 0.75, a[1] * 0.25 + b[1] * 0.75]); }
        n.push(r[r.length - 1]); r = n;
      }
      if (out.length) r = r.slice(1);
      out = out.concat(r);
    }
    for (i = 1; i < pts.length; i++) { run.push(pts[i]); if (pts[i][2] || i === pts.length - 1) { flush(); run = [pts[i]]; } }
    return out;
  }
  var A_S = smoothPath(WALL_A), B1_S = smoothPath(WALL_B1), B2_S = smoothPath(WALL_B2), CAVITY = A_S.concat(B2_S.slice().reverse(), B1_S.slice().reverse());
  function inCavity(x, y) {
    var c = false, i, j, P = CAVITY;
    for (i = 0, j = P.length - 1; i < P.length; j = i++) if ((P[i][1] > y) !== (P[j][1] > y) && x < (P[j][0] - P[i][0]) * (y - P[i][1]) / (P[j][1] - P[i][1]) + P[i][0]) c = !c;
    return c;
  }
  /* plug: radius against height, measured from the seat line with the valve shut */
  var PLUG = [[0, -0.5], [0.1, -0.5], [0.2, -0.38], [0.3, -0.18], [0.37, 0], [0.4, 0.1], [0.52, 0.2], [0.52, 0.42], [0.09, 0.48], [0, 0.48]];
  function plugR(y) { if (y <= -0.5) return 0; for (var i = 2; i < 7; i++) if (y <= PLUG[i][1]) return PLUG[i - 1][0] + (PLUG[i][0] - PLUG[i - 1][0]) * (y - PLUG[i - 1][1]) / (PLUG[i][1] - PLUG[i - 1][1]); return 0.52; }
  var Y_PLATE = 3.85, Y_CLAMP = 4.11, Y_TOP = 5.7, NP = 150, NL = 28, TAIL = 5, NTR = 6, NBUB = 700;

  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.85));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.4); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); scene.add(pivot);
    model = new T.Group(); pivot.add(model);
    var cast = mat(0x55637b), cut = mat(0xa9b5c6, 0.95, 0), inner = mat(0x4a586e, 0.8, 0.1), floor = new T.MeshBasicMaterial({ color: 0x0a1f3d, side: T.DoubleSide }),
        steel = mat(0xd3d9e2, 0.35, 0.45), steelCut = mat(0xe3e7ee, 0.9, 0), bronze = mat(0xc8a04a, 0.5, 0.4), dark = mat(0x2c3646, 0.8, 0.1),
        act = mat(0x8dc63f, 0.5, 0.2), actCut = mat(0xc6e79a, 0.95, 0), rubber = mat(0x1c222b, 0.9, 0), box = mat(0xd5dbe5, 0.6, 0.1);
    var glass = new T.MeshStandardMaterial({ color: 0xcfe6ff, transparent: true, opacity: 0.14, roughness: 0.1, metalness: 0, depthWrite: false, side: T.DoubleSide });
    var i, k;
    function shape(pts) { return new T.Shape(pts.map(function (p) { return new T.Vector2(p[0], p[1]); })); }
    function cap(pts, m, z, parent) { var ms = new T.Mesh(new T.ShapeGeometry(shape(pts)), m); ms.position.z = z || 0; (parent || model).add(ms); return ms; }
    /* the back half of a solid of revolution, one flat band per edge of its profile; profile points are (radius, distance along the axis) */
    function lathe(prof, m, axis, parent) {
      var g = new T.Group();
      for (var j = 0; j < prof.length - 1; j++) {
        if (prof[j][0] === 0 && prof[j + 1][0] === 0) continue;
        g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(prof[j][0], prof[j][1]), new T.Vector2(prof[j + 1][0], prof[j + 1][1])], 40, Math.PI / 2, Math.PI), m));
      }
      if (axis === 'x') g.rotation.z = -Math.PI / 2;
      (parent || model).add(g); return g;
    }
    /* a solid of revolution about the stem axis, cut in half: back half plus the flat cut face */
    function half(prof, m, mCut, parent, z) {
      lathe(prof, m, 'y', parent);
      var pts = prof.map(function (p) { return [p[0], p[1]]; }), left = prof.slice().reverse().map(function (p) { return [-p[0], p[1]]; });
      if (prof[0][0] === 0 && prof[prof.length - 1][0] === 0) cap(pts.concat(left.slice(1, -1)), mCut, z || 0.002, parent);
      else { cap(pts, mCut, z || 0.002, parent); cap(left, mCut, z || 0.002, parent); }
    }

    /* body: the three pieces of metal on the cut face, the pocket behind them, and the outside of the casting */
    var TL = B1_S.concat([[-1.15, 1.6], [-1.15, 1.3], [-1.4, 0.95], [-1.8, 0.72], [-2.95, 0.72], [-2.95, 1.1], [-3.2, 1.1]]);
    var TR = B2_S.concat([[3.2, 1.1], [2.95, 1.1], [2.95, 0.72], [1.8, 0.72], [1.4, 0.95], [1.15, 1.3], [1.15, 1.6]]);
    var BT = A_S.concat([[3.2, -1.1], [2.95, -1.1], [2.95, -0.72], [1.8, -0.72], [1.3, -0.97], [0.6, -1.4], [-0.6, -1.4], [-1.3, -0.97], [-1.8, -0.72], [-2.95, -0.72], [-2.95, -1.1], [-3.2, -1.1]]);
    cap(TL, cut); cap(TR, cut); cap(BT, cut);
    var hidden = new T.MeshBasicMaterial({ visible: false });
    var pocket = new T.Mesh(new T.ExtrudeGeometry(shape(CAVITY), { depth: 0.45, bevelEnabled: false }), [hidden, inner]); pocket.position.z = -0.45; model.add(pocket);
    cap(CAVITY, floor, -0.45);
    lathe([[0.5, -3.2], [1.1, -3.2], [1.1, -2.95], [0.72, -2.95], [0.72, -1.8], [0.97, -1.3], [1.4, -0.6], [1.4, 0.6], [0.97, 1.3], [0.72, 1.8], [0.72, 2.95], [1.1, 2.95], [1.1, 3.2], [0.5, 3.2]], cast, 'x');
    lathe([[1.15, 0.3], [1.15, 1.6]], cast, 'y');
    /* seat ring, shown on the cut face */
    cap([[0.42, -0.12], [0.64, -0.12], [0.64, 0.04], [0.56, 0.12], [0.42, 0.12]], bronze, 0.003);
    cap([[-0.42, -0.12], [-0.64, -0.12], [-0.64, 0.04], [-0.56, 0.12], [-0.42, 0.12]], bronze, 0.003);
    /* bonnet, packing and yoke */
    half([[0, 1.6], [1.15, 1.6], [1.15, 1.86], [0.46, 1.86], [0.46, 2.5], [0.3, 2.56], [0.3, 2.76], [0, 2.76]], cast, cut);
    cap([[0.07, 1.98], [0.24, 1.98], [0.24, 2.5], [0.07, 2.5]], dark, 0.004); cap([[-0.07, 1.98], [-0.24, 1.98], [-0.24, 2.5], [-0.07, 2.5]], dark, 0.004);
    function bx(w, h, d, x, y, z, m, parent) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y, z); (parent || model).add(b); return b; }
    bx(0.16, 1.2, 0.34, -0.6, 3.1, -0.17, cast); bx(0.16, 1.2, 0.34, 0.6, 3.1, -0.17, cast);
    bx(0.05, 0.78, 0.03, 0.5, 3.24, 0.01, new T.MeshBasicMaterial({ color: 0xe9eef5 }));                              /* travel scale */
    for (i = 0; i <= 4; i++) bx(0.1, 0.012, 0.01, 0.45, 2.95 + LMAX * i / 4, 0.03, new T.MeshBasicMaterial({ color: 0x22304a }));
    /* actuator: lower case (air side), upper case and spring barrel */
    half([[0.2, 3.64], [0.98, 3.64], [1.62, 4.02], [1.78, 4.02], [1.78, 4.08], [1.6, 4.08], [0.95, 3.7], [0.2, 3.7]], act, actCut);
    half([[0, 5.7], [0.72, 5.7], [0.72, 4.45], [1.0, 4.45], [1.6, 4.14], [1.78, 4.14], [1.78, 4.2], [1.62, 4.2], [1.02, 4.51], [0.78, 4.51], [0.78, 5.76], [0, 5.76]], act, actCut);
    airMat = new T.MeshBasicMaterial({ color: 0xbfe9ff, transparent: true, opacity: 0.3, depthWrite: false, side: T.DoubleSide });
    flexMat = rubber;
    /* positioner on the yoke, with its air line to the lower case */
    bx(0.5, 0.62, 0.4, -1.05, 3.02, -0.2, box); bx(0.2, 0.08, 0.3, -0.75, 3.02, -0.17, cast);
    var disp = new T.Mesh(new T.PlaneGeometry(0.3, 0.18), new T.MeshBasicMaterial({ color: 0x8dc63f })); disp.position.set(-1.05, 3.1, 0.001); model.add(disp);
    var tube = new T.CatmullRomCurve3([new T.Vector3(-1.05, 3.33, -0.2), new T.Vector3(-1.1, 3.52, -0.2), new T.Vector3(-1.2, 3.66, -0.2), new T.Vector3(-1.2, 3.8, -0.2)]);
    model.add(new T.Mesh(new T.TubeGeometry(tube, 24, 0.04, 8, false), dark));

    /* moving parts: plug, stem, travel pointer and diaphragm plate; the group rises with the valve travel */
    trim = new T.Group(); model.add(trim);
    half(PLUG, steel, steelCut, trim, 0.004);
    var stem = new T.Mesh(new T.CylinderGeometry(0.07, 0.07, Y_PLATE - 0.48, 16), steel); stem.position.y = (Y_PLATE + 0.48) / 2; trim.add(stem);
    half([[0, 2.93], [0.22, 2.93], [0.22, 2.98], [0, 2.98]], act, actCut, trim, 0.006);
    half([[0, Y_PLATE], [1.0, Y_PLATE], [1.0, Y_PLATE + 0.06], [0, Y_PLATE + 0.06]], steel, steelCut, trim, 0.004);
    /* spring: a coil between the diaphragm plate and the top of the barrel, squeezed as the valve opens */
    var coil = new T.Curve(); coil.getPoint = function (t, target) { var a = t * Math.PI * 2 * 6.5; return (target || new T.Vector3()).set(0.5 * Math.cos(a), t, 0.5 * Math.sin(a)); };
    spring = new T.Mesh(new T.TubeGeometry(coil, 260, 0.05, 8, false), steel); model.add(spring);

    /* piping: clear stubs either side with their flanges, and a faint tint of liquid coloured by pressure */
    [-1, 1].forEach(function (sgn) {
      var p = new T.Mesh(new T.CylinderGeometry(0.5, 0.5, 1.3, 36, 1, true), glass); p.rotation.z = Math.PI / 2; p.position.x = sgn * 3.85; model.add(p);
      lathe([[0.5, sgn * 3.2], [1.1, sgn * 3.2], [1.1, sgn * 3.42], [0.5, sgn * 3.42]], cast, 'x');
      cap([[sgn * 3.2, 0.5], [sgn * 3.42, 0.5], [sgn * 3.42, 1.1], [sgn * 3.2, 1.1]], cut, 0.002); cap([[sgn * 3.2, -0.5], [sgn * 3.42, -0.5], [sgn * 3.42, -1.1], [sgn * 3.2, -1.1]], cut, 0.002);
      var m = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.2, depthWrite: false });
      var t = new T.Mesh(new T.CylinderGeometry(0.44, 0.44, 1.3, 28), m); t.rotation.z = Math.PI / 2; t.position.x = sgn * 3.85; model.add(t); tints[sgn < 0 ? 'a' : 'b'] = m;
    });

    /* pressure field on the floor of the pocket: a fine grid over the flow passage */
    var pos = [], col = [], idx = [], H = 0.05, x0 = -3.2, y0 = -1.15, nx = Math.round(6.4 / H), ny = Math.round(2.78 / H), id = {}, n = 0;
    fieldXY = [];
    function vid(ix, iy) { var q = ix + ',' + iy; if (id[q] == null) { id[q] = n++; var x = x0 + ix * H, y = y0 + iy * H; pos.push(x, y, -0.445); col.push(0, 0, 0); fieldXY.push(x, y); } return id[q]; }
    for (i = 0; i < nx; i++) for (k = 0; k < ny; k++) {
      var cx = x0 + (i + 0.5) * H, cy = y0 + (k + 0.5) * H;
      if (!(inCavity(cx, cy) || inCavity(cx - H, cy) || inCavity(cx + H, cy) || inCavity(cx, cy - H) || inCavity(cx, cy + H))) continue;
      var v0 = vid(i, k), v1 = vid(i + 1, k), v2 = vid(i + 1, k + 1), v3 = vid(i, k + 1); idx.push(v0, v1, v2, v0, v2, v3);
    }
    var fg = new T.BufferGeometry(); fg.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); fg.setAttribute('color', new T.Float32BufferAttribute(col, 3)); fg.setIndex(idx);
    field = new T.Mesh(fg, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.4, depthWrite: false, side: T.DoubleSide })); model.add(field);

    /* streamlines: lines along the floor of the inlet come up on the right of the plug, lines along the top come up on
       its left and pass over it behind the stem. Their shape follows the plug, so they are redrawn when it moves. */
    var lm = new T.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.92 });
    function frac(v) { return v - Math.floor(v); }
    for (i = 0; i < NL; i++) {
      var g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(new Float32Array((NP + 1) * 3), 3)); g.setAttribute('color', new T.BufferAttribute(new Float32Array((NP + 1) * 3), 3));
      var ln = new T.Line(g, lm); ln.frustumCulled = false; model.add(ln);
      var v = (i + 0.5) / NL, right = v < 0.5, tr = [];
      for (k = 0; k < NTR; k++) tr.push((k + Math.random() * 0.7) / NTR);
      lines.push({ v: v, right: right, z: right ? -0.07 - 0.3 * frac(i * 0.618 + 0.3) : -0.15 - 0.24 * frac(i * 0.618 + 0.3), line: ln, len: new Float32Array(NP + 1), sp: new Float32Array(NP + 1), total: 1, dThroat: 0, tr: tr });
    }
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
    var q = points(NL * NTR * TAIL, 0.13); trc = q[0]; trcPos = q[1]; trcCol = q[2];
    q = points(NBUB, 0.2); bub = q[0]; bubPos = q[1]; bubCol = q[2];
  }
  /* control points of one streamline for the present plug lift, and which of them sits in the gap at the seat */
  function route(l, L) {
    var v = l.v, yin = -0.42 + 0.84 * v, rp = plugR(-L), P, c, u, w, xg;
    if (l.right) {
      u = v / 0.5; xg = rp + (RS - rp) * (0.8 - 0.6 * u);
      P = [[-4.5, yin], [-3.2, yin], [-1.9, yin], [-1.15, -0.62 + 0.7 * v], [-0.1, -1.0 + 0.38 * u], [0.72 - 0.4 * u, -0.84 + 0.4 * u], [xg, -0.14], [0.5, 0.12 + L * (0.2 + 0.6 * u)],
           [0.95, 0.14 + 0.62 * v], [1.5, -0.33 + 0.8 * v], [2.2, yin], [3.2, yin], [4.5, yin]]; c = 7;
    } else {
      w = (v - 0.5) / 0.5; xg = rp + (RS - rp) * (0.2 + 0.6 * w);
      P = [[-4.5, yin], [-3.2, yin], [-1.9, yin], [-1.15, -0.62 + 0.7 * v], [-0.66, -0.3 - 0.22 * (1 - w)], [-xg, -0.14], [-0.5, 0.12 + L * (0.8 - 0.6 * w)],
           [-0.6 - 0.1 * w, L + 0.34 + 0.06 * w], [-0.22, L + 0.6 + 0.3 * w], [0.35, L + 0.56 + 0.3 * w], [0.95, 0.14 + 0.62 * v], [1.5, -0.33 + 0.8 * v], [2.2, yin], [3.2, yin], [4.5, yin]]; c = 6;
    }
    return { P: P, c: c };
  }
  var rgb = [0, 0, 0], bubs = [];
  for (var bi = 0; bi < NBUB; bi++) bubs.push({ on: false, j: 0, d: 0, lim: 0, life: 0, ox: 0, oy: 0, oz: 0 });
  function paint() { /* move the trim, redraw the streamlines and recolour everything for the current state */
    var L = LMAX * S.x, k, j; lift = L;
    trim.position.y = L;
    var yd = Y_PLATE + L;
    spring.position.y = yd + 0.06; spring.scale.y = Y_TOP - yd - 0.06;
    if (flex) { model.remove(flex); flex.geometry.dispose(); }
    flex = new T.Mesh(new T.LatheGeometry([new T.Vector2(1.0, yd + 0.03), new T.Vector2(1.3, yd + 0.03 + (Y_CLAMP - yd - 0.03) * 0.25), new T.Vector2(1.7, Y_CLAMP)], 40, Math.PI / 2, Math.PI), flexMat); model.add(flex);
    if (air) { model.remove(air); air.geometry.dispose(); }
    var sh = new T.Shape([new T.Vector2(-0.95, 3.7), new T.Vector2(0.95, 3.7), new T.Vector2(1.6, 4.08), new T.Vector2(1.3, yd + (Y_CLAMP - yd) * 0.25), new T.Vector2(1.0, yd), new T.Vector2(-1.0, yd), new T.Vector2(-1.3, yd + (Y_CLAMP - yd) * 0.25), new T.Vector2(-1.6, 4.08)]);
    air = new T.Mesh(new T.ShapeGeometry(sh), airMat); air.position.z = -0.004; model.add(air); airMat.opacity = 0.12 + 0.4 * S.x;
    var col = field.geometry.attributes.color;
    for (k = 0; k < fieldXY.length / 2; k++) { presRGB(presXY(fieldXY[k * 2], fieldXY[k * 2 + 1]), rgb); col.setXYZ(k, rgb[0], rgb[1], rgb[2]); }
    col.needsUpdate = true;
    var ty = 0.12 + L / 2;
    for (j = 0; j < lines.length; j++) {
      var l = lines[j], r = route(l, L), cu = new T.CatmullRomCurve3(r.P.map(function (p) { return new T.Vector3(p[0], p[1], l.z); }), false, 'centripetal'), pts = cu.getPoints(NP);
      var ps = l.line.geometry.attributes.position, c = l.line.geometry.attributes.color, x, y;
      for (k = 0; k <= NP; k++) {
        x = pts[k].x; y = pts[k].y; ps.setXYZ(k, x, y, l.z);
        l.len[k] = k ? l.len[k - 1] + Math.hypot(x - pts[k - 1].x, y - pts[k - 1].y) : 0;
        var d = Math.min(Math.hypot(x - 0.47, y - ty), Math.hypot(x + 0.47, y - ty));
        l.sp[k] = 0.75 + 1.9 * Math.exp(-d * d / 0.2);
        presRGB(presXY(x, y), rgb); c.setXYZ(k, Math.min(1, rgb[0] * 0.55 + 0.5), Math.min(1, rgb[1] * 0.55 + 0.5), Math.min(1, rgb[2] * 0.55 + 0.5));
      }
      l.total = l.len[NP]; l.dThroat = l.len[Math.round(r.c / (r.P.length - 1) * NP)];
      ps.needsUpdate = true; c.needsUpdate = true;
    }
    presRGB(S.a, rgb); tints.a.color.setRGB(rgb[0], rgb[1], rgb[2]);
    presRGB(S.b, rgb); var wm = S.flash ? 0.6 : 0; tints.b.color.setRGB(rgb[0] + (1 - rgb[0]) * wm, rgb[1] + (1 - rgb[1]) * wm, rgb[2] + (1 - rgb[2]) * wm); tints.b.opacity = S.flash ? 0.34 : 0.2;
  }
  function locate(l, d, out) { /* point at distance d along a streamline */
    var lo = 0, hi = NP, mid, ps = l.line.geometry.attributes.position.array;
    while (hi - lo > 1) { mid = (lo + hi) >> 1; if (l.len[mid] <= d) lo = mid; else hi = mid; }
    var fr = (d - l.len[lo]) / Math.max(1e-6, l.len[hi] - l.len[lo]);
    out[0] = ps[lo * 3] + (ps[hi * 3] - ps[lo * 3]) * fr; out[1] = ps[lo * 3 + 1] + (ps[hi * 3 + 1] - ps[lo * 3 + 1]) * fr; out[2] = ps[lo * 3 + 2]; out[3] = l.sp[lo];
    return out;
  }
  var loc = [0, 0, 0, 0];
  function step(dt) {
    var sf = S.q / Q_R, j, n, t, k, l, u, ti = 0, seg = 1;
    for (j = 0; j < lines.length; j++) {
      l = lines[j];
      for (n = 0; n < l.tr.length; n++) {
        u = l.tr[n];
        for (t = 0; t < TAIL; t++) {
          var uu = u - t * 0.0045, vis = 1 - t / TAIL; if (uu < 0) { uu = 0; vis = 0; }
          locate(l, uu * l.total, loc); if (t === 0) seg = loc[3];
          k = ti * 3; trcPos[k] = loc[0]; trcPos[k + 1] = loc[1]; trcPos[k + 2] = loc[2] + 0.01;
          trcCol[k] = vis; trcCol[k + 1] = vis; trcCol[k + 2] = vis; ti++;
        }
        u += dt * 1.9 * sf * seg / l.total; if (u >= 1) u -= 1; l.tr[n] = u;
      }
    }
    /* vapour bubbles start in the gap at the seat. Cavitation: they collapse as the pressure recovers. Flashing: they
       last, and the outlet stream turns to a mixture of liquid and vapour. */
    var want = sf <= 0 ? 0 : S.flash ? 520 : S.cav ? 90 + 200 * S.ci : 0;
    for (j = 0; j < NBUB; j++) {
      var b = bubs[j]; k = j * 3;
      if (!b.on) {
        if (dt > 0 && Math.random() < dt * want / NBUB * 2.2) {
          b.on = true; b.j = Math.floor(Math.random() * lines.length); l = lines[b.j]; b.d = l.dThroat - 0.05 + Math.random() * 0.12; b.life = 0;
          b.lim = S.flash ? l.total : l.dThroat + (0.12 + 1.15 * S.ci) * (0.5 + 0.5 * Math.random());
          b.ox = (Math.random() - 0.5) * 0.07; b.oy = (Math.random() - 0.5) * 0.07; b.oz = (Math.random() - 0.5) * 0.06;
        }
      } else {
        l = lines[b.j]; locate(l, Math.min(b.d, l.total), loc);
        b.d += dt * 1.9 * Math.max(0.25, sf) * loc[3]; b.life += dt;
        if (!S.flash && !S.cav) b.lim = Math.min(b.lim, b.d + 0.1);
        if (b.d >= b.lim || b.d >= l.total) b.on = false;
        bubPos[k] = loc[0] + b.ox; bubPos[k + 1] = loc[1] + b.oy; bubPos[k + 2] = loc[2] + b.oz + 0.02;
      }
      var vv = b.on ? Math.min(1, b.life * 8) * Math.min(1, (b.lim - b.d) * 8) : 0;
      bubCol[k] = vv; bubCol[k + 1] = vv; bubCol[k + 2] = vv;
    }
    trc.geometry.attributes.position.needsUpdate = true; trc.geometry.attributes.color.needsUpdate = true;
    bub.geometry.attributes.position.needsUpdate = true; bub.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- names and tags: a column each side of the actuator and a row under the valve, each joined to its part.
     Entries: kind, text, anchor x, y, z, band (L, R or B), key, wide screens only, anchor rises with the trim ----- */
  var ITEMS = [
    ['l', 'Actuator: air opens, spring closes', -1.5, 4.12, 0, 'L'],
    ['t', 'Positioner · signal 15.3 mA', -1.3, 3.02, 0, 'L', 'sig', 1],
    ['l', 'Bonnet and packing', -0.4, 2.2, 0, 'L'],
    ['l', 'Spring', 0.5, 5.15, 0, 'R'],
    ['l', 'Diaphragm', 1.25, 3.95, 0, 'R', null, 0, 1],
    ['t', 'Travel 70% · Cv 7.87', 0.22, 2.955, 0, 'R', 'trv', 0, 1],
    ['l', 'Stem', 0.07, 1.2, 0, 'R', null, 0, 1],
    ['t', 'Inlet · 473 kPa abs', -3.9, -0.5, 0, 'B', 'inl'],
    ['l', 'Seat ring', -0.56, -0.08, 0, 'B'],
    ['l', 'Plug', 0, -0.3, 0, 'B', null, 0, 1],
    ['t', 'Lowest, just past the seat · 324 kPa abs', 0.5, 0.2, 0, 'B', 'low'],
    ['t', 'Outlet · 353 kPa abs', 3.9, -0.5, 0, 'B', 'out']
  ];
  var tags = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'cv3d-tag' : 'cv3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, x: 0, y: 0, tag: n[0] === 't', wideOnly: !!n[7], hidden: false };
    if (n[6]) tags[n[6]] = it; return it;
  });
  var W = 0, H = 0, measured = false, wideNow = true, v3 = T ? new T.Vector3() : null;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function place() {
    if (!measured) { items.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    var pt = { x: 0, y: 0 }, gap = 8;
    items.forEach(function (q) {
      if (q.wideOnly) { var hide = !wideNow; if (q.hidden !== hide) { q.hidden = hide; q.el.style.display = hide ? 'none' : ''; q.path.style.display = hide ? 'none' : ''; q.dot.style.display = hide ? 'none' : ''; } }
      toScreen(q.n[2], q.n[3] + (q.n[8] ? lift : 0), q.n[4], pt); q.ax = pt.x; q.ay = pt.y;
    });
    function shown(band) { return items.filter(function (q) { return q.n[5] === band && !q.hidden && (q.tag || (wideNow && q.w > 0)); }); }
    ['L', 'R'].forEach(function (band) {
      var list = shown(band), i, l; list.sort(function (a, b) { return a.ay - b.ay; });
      for (i = 0; i < list.length; i++) { l = list[i]; l.y = Math.max(l.ay, 44 + l.h / 2, i ? list[i - 1].y + (list[i - 1].h + l.h) / 2 + gap : -1e9); }
      for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.y = Math.min(l.y, H - 84 - l.h / 2, i < list.length - 1 ? list[i + 1].y - (list[i + 1].h + l.h) / 2 - gap : 1e9); }
      for (i = 0; i < list.length; i++) {
        l = list[i]; var lx = band === 'L' ? 10 : W - 10 - l.w;
        l.el.style.transform = 'translate(' + lx.toFixed(1) + 'px,' + (l.y - l.h / 2).toFixed(1) + 'px)';
        l.path.setAttribute('d', 'M' + l.ax.toFixed(1) + ' ' + l.ay.toFixed(1) + 'L' + (band === 'L' ? lx + l.w : lx).toFixed(1) + ' ' + l.y.toFixed(1));
        l.dot.setAttribute('cx', l.ax.toFixed(1)); l.dot.setAttribute('cy', l.ay.toFixed(1));
      }
    });
    var list = shown('B'), i, l; list.forEach(function (q) { q.x = q.ax; }); list.sort(function (a, b) { return a.ax - b.ax; });
    for (i = 0; i < list.length; i++) { l = list[i]; l.x = Math.max(l.x, 8 + l.w / 2, i ? list[i - 1].x + (list[i - 1].w + l.w) / 2 + gap : -1e9); }
    for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.x = Math.min(l.x, W - 8 - l.w / 2, i < list.length - 1 ? list[i + 1].x - (list[i + 1].w + l.w) / 2 - gap : 1e9); }
    var by = H - 26;
    for (i = 0; i < list.length; i++) {
      l = list[i];
      l.el.style.transform = 'translate(' + (l.x - l.w / 2).toFixed(1) + 'px,' + (by - l.h / 2).toFixed(1) + 'px)';
      var bx = Math.max(l.x - l.w / 2 + 12, Math.min(l.x + l.w / 2 - 12, l.ax));
      l.path.setAttribute('d', 'M' + l.ax.toFixed(1) + ' ' + l.ay.toFixed(1) + 'L' + bx.toFixed(1) + ' ' + (by - l.h / 2).toFixed(1));
      l.dot.setAttribute('cx', l.ax.toFixed(1)); l.dot.setAttribute('cy', l.ay.toFixed(1));
    }
  }

  /* ----- view ----- */
  var yawUser = -0.4, pitchUser = 0.13, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0, CY = 2.18;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var px = Math.min((W - (wideNow ? 40 : 12)) / 9.3, (H - 122) / 7.5), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180)), off = 22 / px;
    camera.aspect = W / H; camera.position.set(0, CY - off, dist); camera.lookAt(0, CY - off, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    pivot.position.y = CY; model.position.y = -CY; pivot.rotation.set(pitch, yaw, 0);
    step(dt);
    pivot.updateMatrixWorld(true);
    renderer.render(scene, camera);
    place();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(-0.95, Math.min(0.95, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.1, Math.min(0.5, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  inFlow.addEventListener('input', function () { calc('flow'); });
  inPv.addEventListener('input', function () { calc('pv'); });
  function setTrim(t) { S.trim = t; btnEq.setAttribute('aria-pressed', t === 'eq' ? 'true' : 'false'); btnLin.setAttribute('aria-pressed', t === 'lin' ? 'true' : 'false'); }
  btnEq.addEventListener('click', function () { setTrim('eq'); calc('trim'); });
  btnLin.addEventListener('click', function () { setTrim('lin'); calc('trim'); });
  $('cv3d-reset').addEventListener('click', function () { inFlow.value = 110; inPv.value = 0; setTrim('eq'); calc(); });
  var btnNames = $('cv3d-names');
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
    yaw += (yawUser + 0.09 * Math.sin(clock * 0.3) * sway - yaw) * e; pitch += (pitchUser - pitch) * e;
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
