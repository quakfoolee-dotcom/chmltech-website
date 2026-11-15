/* Reactor jacket article: 3D model of R-101, a jacketed stirred reactor cut in half (needs three.js r128+ as
   window.THREE). The numbers repeat the article's worked example: 10,000 kg batch, 150 kJ/kg of reaction heat,
   2.34 m diameter with liquid depth equal to diameter, batch held at 60 C, cooling water at 25 C and 14 m3/h,
   and an overall coefficient built from four resistances (plain jacket 300 W/m2.K). Typical values, not vendor
   data: jacket side coefficients of 1,000 / 2,500 / 5,000 W/m2.K and their dependence on flow and agitator speed. */
(function () {
  'use strict';
  var fig = document.getElementById('rx3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.rx3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.rx3d-lines');
  var inAdd = $('rx3d-add'), inFlow = $('rx3d-flow'), inTin = $('rx3d-tin'), inAgi = $('rx3d-agi'), btnCoil = $('rx3d-coil');
  var typeBtns = Array.prototype.slice.call(fig.querySelectorAll('[data-type]'));
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- heat transfer (same constants and formulas as the article) ----- */
  var D_R = Math.pow(4 * 10 / Math.PI, 1 / 3), A_J = Math.PI * D_R * D_R, Q_BATCH = 10000 * 150, T_SET = 60, T_BOIL = 110, CP_W = 4.18;
  var H_I = 800, R_WALL = 0.012 / 16, R_FOUL = 1 / 300 - 1 / H_I - R_WALL - 1 / 1000, HJ = [1000, 2500, 5000], NX = [0.6, 0.8, 0.8], VEL = [0.3, 0.9, 1.6];
  var A_C = Math.PI * 0.0603 * Math.PI * 1.6 * 9, R_CW = 0.0039 / 16, F0 = 14, RPM = 84, D_IMP = 0.88;   /* full agitator speed and impeller diameter, m */
  var NAMES = ['Plain jacket', 'Dimple jacket', 'Half-pipe coil jacket'];
  var S = { view: 'speed', type: 0, coil: false, tadd: 3, F: 14, tin: 25, n: 1, gen: 139, cap: 154, u: 300, tb: 60, out: 33.5, use: 0.9, state: 'hold', shown: 60, K: 4.4 };
  var lastKey = 'design';
  function say(key) {
    var u = S.u.toFixed(0);
    switch (key) {
      case 'design': return 'Design point: the reaction releases 139 kW and the plain jacket can remove 154 kW at 60 °C, so the temperature controller holds the batch with about 10% in hand.';
      case 'type': return S.type === 0 ? 'The plain jacket: water drifts through the gap at about 0.3 m/s, so the water film takes a large share of the temperature difference and the heat arrows through the wall are short.' : 'The water now moves at about ' + S.vw.toFixed(1) + ' m/s, so its film takes a smaller share of the temperature difference. More is left to drive heat out of the batch: the arrows through the wall grow and the liquid at the wall runs cooler. A better jacket improves only the water side. The overall coefficient rises from 300 to ' + u + ' W/m²·K, because the batch film and the vessel wall are still in the way.';
      case 'coil': return S.coil ? 'An internal coil adds 8.6 m² of area with only a thin pipe wall in the way. Capacity rises far more than with any change of jacket.' : 'Without the coil, the wall is the only cooling surface.';
      case 'fast': return 'A shorter addition releases the same heat in less time. The cooling still holds 60 °C, with less in hand.';
      case 'slow': return 'A longer addition spreads the same heat over more time. The cooling has capacity to spare, at the cost of a longer batch.';
      case 'flowup': return 'More cooling water stays colder on its way round and moves faster, so the capacity rises, but each extra cubic metre adds less than the last.';
      case 'flowdn': return 'Less cooling water warms up more on its way round and moves more slowly, so the capacity falls.';
      case 'warm': return 'Warmer cooling water, as in summer, shrinks the temperature difference that drives the heat out. Capacity falls in proportion.';
      case 'cold': return 'Colder cooling water widens the temperature difference between the batch and the jacket. Capacity rises in proportion.';
      case 'agidn': return 'A slower agitator keeps the same circulation pattern but moves the liquid more slowly, in proportion to its speed. The film of liquid on the wall thickens, and since that is the largest resistance, capacity falls whatever the jacket.';
      case 'agiup': return 'A faster agitator keeps the same circulation pattern and moves the liquid faster, in proportion to its speed. The film of liquid on the wall thins, so every jacket type gains, at the cost of power that rises with the cube of speed.';
      case 'hot': return 'The reaction is releasing more heat than the cooling can remove at 60 °C. The batch warms until the wider temperature difference restores the balance, here at ' + S.tb.toFixed(0) + ' °C.';
      case 'boil': return 'The cooling is overwhelmed: the balance point is above the 110 °C boiling point. In the plant the addition must be slowed or stopped long before this.';
    }
    return '';
  }
  function calc(changed) {
    S.tadd = parseFloat(inAdd.value); S.F = parseFloat(inFlow.value); S.tin = parseFloat(inTin.value); S.n = parseFloat(inAgi.value) / 100;
    var hi = H_I * Math.pow(S.n, 0.67), fr = S.F / F0, hj = HJ[S.type] * Math.pow(fr, NX[S.type]);
    S.u = 1 / (1 / hi + R_WALL + R_FOUL + 1 / hj); S.fi = S.u / hi; S.fc = 1 / hi / (1 / hi + R_CW + R_FOUL + 1 / (5000 * Math.pow(fr, 0.8)));
    var ua = S.u * A_J; if (S.coil) ua += A_C / (1 / hi + R_CW + R_FOUL + 1 / (5000 * Math.pow(fr, 0.8)));
    var mcp = S.F * 1000 / 3600 * CP_W, K = mcp * (1 - Math.exp(-ua / 1000 / mcp));        /* kW/K */
    S.K = K; S.gen = Q_BATCH / (S.tadd * 3600); S.cap = K * (T_SET - S.tin);
    var qrem;
    if (S.cap >= S.gen) { S.tb = T_SET; S.state = 'hold'; qrem = S.gen; }
    else { S.tb = S.tin + S.gen / K; if (S.tb >= T_BOIL) { S.tb = T_BOIL; S.state = 'boil'; qrem = K * (T_BOIL - S.tin); } else { S.state = 'hot'; qrem = S.gen; } }
    S.qrem = qrem; S.out = S.tin + qrem / mcp; S.use = S.gen / S.cap;
    /* what the jacket can do with the batch at its present temperature and the water at full flow: outlet temperature,
       heat flux through the wall, and how the temperature difference is shared between the four resistances */
    S.outCap = S.tin + K * (S.tb - S.tin) / mcp; S.hi = hi; S.hj = hj; S.vw = VEL[S.type] * fr;
    var dtm = S.tb - (S.tin + S.outCap) / 2; S.flux = S.u * dtm / 1000;                      /* kW/m2 at mid-height */
    S.drops = [S.u / hi * dtm, S.u * R_WALL * dtm, S.u * R_FOUL * dtm, S.u / hj * dtm]; S.twm = (S.tin + S.outCap) / 2;
    var uP = 1 / (1 / hi + R_WALL + R_FOUL + 1 / (HJ[0] * Math.pow(fr, NX[0])));               /* the plain jacket, for comparison */
    S.dropsP = [uP / hi * dtm, uP * R_WALL * dtm, uP * R_FOUL * dtm, uP / (HJ[0] * Math.pow(fr, NX[0])) * dtm];
    $('rx3d-type-o').textContent = NAMES[S.type] + (S.coil ? ' + coil' : '');
    $('rx3d-add-o').textContent = S.tadd.toFixed(1) + ' h · ' + S.gen.toFixed(0) + ' kW of heat'; $('rx3d-flow-o').textContent = S.F.toFixed(0) + ' m³/h';
    $('rx3d-tin-o').textContent = S.tin.toFixed(0) + ' °C'; $('rx3d-agi-o').textContent = (S.n * 100).toFixed(0) + '% · ' + (RPM * S.n).toFixed(0) + ' rpm · tip ' + (Math.PI * D_IMP * RPM * S.n / 60).toFixed(1) + ' m/s';
    $('rx3d-tb').textContent = S.state === 'boil' ? '110 °C, boiling' : S.tb.toFixed(0) + ' °C'; $('rx3d-gen').textContent = S.gen.toFixed(0) + ' kW'; $('rx3d-cap').textContent = S.cap.toFixed(0) + ' kW';
    $('rx3d-u').textContent = S.u.toFixed(0) + ' W/m²·K'; $('rx3d-out').textContent = S.out.toFixed(1) + ' °C'; $('rx3d-use').textContent = (S.use * 100).toFixed(0) + '%';
    var chip = $('rx3d-chip'); chip.textContent = S.state === 'hold' ? 'Holding 60 °C' : S.state === 'hot' ? 'Running hot · ' + S.tb.toFixed(0) + ' °C' : 'Cooling overwhelmed'; chip.classList.toggle('is-bad', S.state !== 'hold');
    var design = S.type === 0 && !S.coil && S.tadd === 3 && S.F === 14 && S.tin === 25 && S.n === 1, key = lastKey;
    if (design) key = 'design';
    else if (S.state === 'boil') key = 'boil';
    else if (S.state === 'hot') key = 'hot';
    else if (changed === 'type') key = 'type';
    else if (changed === 'coil') key = 'coil';
    else if (changed === 'add') key = S.tadd < 3 ? 'fast' : S.tadd > 3 ? 'slow' : key;
    else if (changed === 'flow') key = S.F > 14 ? 'flowup' : S.F < 14 ? 'flowdn' : key;
    else if (changed === 'tin') key = S.tin > 25 ? 'warm' : S.tin < 25 ? 'cold' : key;
    else if (changed === 'agi') key = S.n < 1 ? 'agidn' : S.n > 1 ? 'agiup' : key;
    if ((key === 'design' && !design) || (key === 'boil' && S.state !== 'boil') || (key === 'hot' && S.state !== 'hot'))
      key = S.coil ? 'coil' : S.type ? 'type' : S.tadd !== 3 ? (S.tadd < 3 ? 'fast' : 'slow') : S.F !== 14 ? (S.F > 14 ? 'flowup' : 'flowdn') : S.tin !== 25 ? (S.tin > 25 ? 'warm' : 'cold') : S.n < 1 ? 'agidn' : 'agiup';
    lastKey = key; $('rx3d-say').textContent = say(key);
    var narrow = !wideNow;
    tags.add.el.textContent = (narrow ? 'Added over ' : 'Reactant added over ') + S.tadd.toFixed(1) + ' h';
    tags.tb.el.textContent = 'Batch ' + (S.state === 'boil' ? '110 °C, boiling' : S.tb.toFixed(0) + ' °C');
    tags.inl.el.textContent = (narrow ? 'In ' : 'Cooling water in · ') + S.tin.toFixed(0) + ' °C';
    tags.out.el.textContent = (narrow ? 'Out ' : 'Cooling water out · ') + S.out.toFixed(1) + ' °C';
    tags.jk.el.textContent = narrow ? 'U ' + S.u.toFixed(0) : NAMES[S.type] + ' · U ' + S.u.toFixed(0) + ' W/m²·K · water ' + S.vw.toFixed(1) + ' m/s';
    tags.fx.el.textContent = (narrow ? 'Heat flow ' : 'Heat flow, batch to jacket · up to ') + S.flux.toFixed(1) + ' kW/m²';
    measured = false; chart(); wallChart();
    if (ok) { if (built !== S.type + (S.coil ? 10 : 0)) jacket(); paint(); if (!running) render(0); }
  }
  /* small live chart: heat released and heat removed against batch temperature */
  function chart() {
    var el = $('rx3d-svg'), X = function (t) { return 38 + (Math.max(20, Math.min(120, t)) - 20) / 100 * 248; }, Y = function (q) { return 160 - Math.max(0, Math.min(500, q)) / 500 * 146; }, s = '', q, t;
    for (q = 0; q <= 500; q += 100) s += '<line x1="38" x2="286" y1="' + Y(q) + '" y2="' + Y(q) + '" stroke="rgba(255,255,255,.10)"/><text x="33" y="' + (Y(q) + 3.5) + '" text-anchor="end">' + q + '</text>';
    for (t = 20; t <= 120; t += 20) s += '<text x="' + X(t) + '" y="173" text-anchor="middle">' + t + '</text>';
    s += '<text x="162" y="187" text-anchor="middle">Batch temperature (°C) against heat (kW)</text>';
    s += '<line x1="' + X(T_SET) + '" x2="' + X(T_SET) + '" y1="14" y2="160" stroke="rgba(255,255,255,.35)" stroke-dasharray="3 3"/><text x="' + (X(T_SET) - 4) + '" y="22" text-anchor="end">Set point</text>';
    s += '<line x1="' + X(T_BOIL) + '" x2="' + X(T_BOIL) + '" y1="14" y2="160" stroke="#FF7A5C" stroke-dasharray="3 3"/><text x="' + (X(T_BOIL) - 4) + '" y="22" text-anchor="end" style="fill:#FF7A5C">Boils</text>';
    var t0 = Math.max(20, S.tin), tq = Math.min(120, S.tin + 500 / S.K);
    s += '<path d="M' + X(t0).toFixed(1) + ' ' + Y(S.K * (t0 - S.tin)).toFixed(1) + 'L' + X(tq).toFixed(1) + ' ' + Y(S.K * (tq - S.tin)).toFixed(1) + '" fill="none" stroke="#5EC8FF" stroke-width="2.2"/>';
    s += '<line x1="38" x2="286" y1="' + Y(S.gen).toFixed(1) + '" y2="' + Y(S.gen).toFixed(1) + '" stroke="#FF8A3D" stroke-width="2.2"/>';
    s += '<text x="42" y="' + (Y(S.gen) - 5).toFixed(1) + '" style="fill:#FF8A3D;font-weight:600">Heat released</text>';
    var lx = Math.min(tq, 104), ly = Y(S.K * (lx - S.tin));
    s += '<text x="' + (X(lx) - 4).toFixed(1) + '" y="' + Math.max(34, ly - 6).toFixed(1) + '" text-anchor="end" style="fill:#5EC8FF;font-weight:600">Cooling</text>';
    s += '<circle cx="' + X(S.tb).toFixed(1) + '" cy="' + Y(S.qrem).toFixed(1) + '" r="4.8" fill="' + (S.state === 'hold' ? '#8DC63F' : '#FF7A5C') + '" stroke="#061833" stroke-width="1.5"/>';
    el.innerHTML = s;
  }
  /* second live chart: the temperature on its way through the wall, from the batch to the cooling water, at mid-height.
     Each step down is one resistance; a better jacket shrinks the last step and leaves more for the others. */
  function wallChart() {
    var el = $('rx3d-wall'); if (!el) return;
    var xs = [38, 92, 150, 186, 222, 268, 290], lo = Math.floor((S.twm - 4) / 5) * 5, hi2 = Math.ceil((S.tb + 3) / 5) * 5, Y = function (t) { return 150 - (t - lo) / (hi2 - lo) * 128; }, s = '', t, i;
    var bands = [[xs[1], xs[2], 'Batch film', 'rgba(94,200,255,.16)'], [xs[2], xs[3], 'Wall', 'rgba(255,255,255,.16)'], [xs[3], xs[4], 'Fouling', 'rgba(255,255,255,.07)'], [xs[4], xs[5], 'Water film', 'rgba(255,138,61,.2)']];
    bands.forEach(function (b, bi) { s += '<rect x="' + b[0] + '" y="22" width="' + (b[1] - b[0]) + '" height="128" fill="' + b[3] + '"/><text x="' + (b[0] + b[1]) / 2 + '" y="' + (bi === 2 ? 172 : 162) + '" text-anchor="middle">' + b[2] + '</text>'; });
    s += '<text x="' + (xs[0] + xs[1]) / 2 + '" y="163" text-anchor="middle">Batch</text><text x="' + (xs[5] + xs[6]) / 2 + '" y="163" text-anchor="middle">Water</text>';
    for (t = lo; t <= hi2; t += (hi2 - lo) > 45 ? 10 : 5) s += '<line x1="38" x2="290" y1="' + Y(t) + '" y2="' + Y(t) + '" stroke="rgba(255,255,255,.08)"/><text x="33" y="' + (Y(t) + 3.5) + '" text-anchor="end">' + t + '</text>';
    s += '<text x="164" y="12" text-anchor="middle" style="fill:#fff;font-weight:600">' + NAMES[S.type] + ': ' + S.flux.toFixed(1) + ' kW/m² through the wall</text>';
    s += '<text x="164" y="187" text-anchor="middle">Temperature through the wall (°C), at mid-height</text>';
    function line(dr, stroke, dash, wdt) {
      var tt = S.tb, d = 'M' + xs[0] + ' ' + Y(tt) + 'L' + xs[1] + ' ' + Y(tt);
      for (i = 0; i < 4; i++) { tt -= dr[i]; d += 'L' + xs[i + 2] + ' ' + Y(tt).toFixed(1); }
      d += 'L' + xs[6] + ' ' + Y(tt).toFixed(1);
      return '<path d="' + d + '" fill="none" stroke="' + stroke + '" stroke-width="' + wdt + '"' + (dash ? ' stroke-dasharray="4 3"' : '') + '/>';
    }
    if (S.type !== 0) s += line(S.dropsP, 'rgba(255,255,255,.55)', true, 1.4) + '<text x="' + (xs[4] + 4) + '" y="' + (Y(S.tb - S.dropsP[0] - S.dropsP[1] - S.dropsP[2]) - 5).toFixed(1) + '" style="fill:rgba(255,255,255,.75)">Plain jacket</text>';
    s += line(S.drops, '#8DC63F', false, 2.4);
    var tt = S.tb; for (i = 0; i < 4; i++) { var mid = Y(tt - S.drops[i] / 2), x = (xs[i + 1] + xs[i + 2]) / 2; tt -= S.drops[i]; if (S.drops[i] >= 0.8) s += '<text x="' + x + '" y="' + Math.max(32, mid - 9).toFixed(1) + '" text-anchor="middle" style="fill:#fff;font-weight:600">' + S.drops[i].toFixed(S.drops[i] < 10 ? 1 : 0) + ' K</text>'; }
    el.innerHTML = s;
  }
  /* temperature colour: blue at 5 C through cyan, green and yellow to red at 110 C */
  var STOPS = [[0, 40, 70, 200], [1, 40, 190, 230], [2, 90, 210, 110], [3, 250, 210, 60], [4, 240, 70, 50]];
  function tempRGB(tc, out) {
    var p = Math.max(0, Math.min(4, (tc - 5) / 105 * 4));
    for (var i = 1; i < STOPS.length; i++) if (p <= STOPS[i][0]) {
      var a = STOPS[i - 1], b = STOPS[i], u = (p - a[0]) / (b[0] - a[0]);
      out[0] = (a[1] + (b[1] - a[1]) * u) / 255; out[1] = (a[2] + (b[2] - a[2]) * u) / 255; out[2] = (a[3] + (b[3] - a[3]) * u) / 255; return out;
    }
    return out;
  }

  /* ----- CFD-style fields on the cut plane (schematic, not a solved flow) -----
     Velocity: the pitched blade turbine drives one circulation loop each side of the shaft, down the middle and up the
     wall, fastest in the stream leaving the impeller. Speeds are in m/s and scale with agitator speed.
     Temperature: the bulk is at the batch temperature; next to the cooled wall (and round the coil) there is a cooler
     film whose temperature drop is the share of the total resistance that sits on the batch side. */
  var FAM = { cx: 0.6, cy: 1.0, a: 0.5, b: 1.12, e: 0.75, jx: 0.3, jy: 0.25 }, vout = [0, 0, 0];
  function inLiquid(x, y) { var ax = Math.abs(x); return ax < R && y < YL && y > -HD * Math.sqrt(Math.max(0, 1 - ax * ax / (R * R))); }
  function vel(x, y, out) {
    out[0] = out[1] = out[2] = 0;
    if (!inLiquid(x, y)) return out;
    var ax = Math.abs(x), X = (ax - FAM.cx) / FAM.a, Y = (y - FAM.cy) / FAM.b, pw = 2 / FAM.e, q = Math.pow(Math.pow(Math.abs(X), pw) + Math.pow(Math.abs(Y), pw), 1 / pw);
    if (q > 1.6) return out;
    var gx = Math.pow(Math.abs(X), pw - 1) * (X < 0 ? -1 : 1) / FAM.a, gy = Math.pow(Math.abs(Y), pw - 1) * (Y < 0 ? -1 : 1) / FAM.b, gl = Math.hypot(gx, gy);
    if (gl < 1e-6) return out;
    var m = q <= 1 ? (q / 0.72) * Math.exp(1 - q / 0.72) : (1 / 0.72) * Math.exp(1 - 1 / 0.72) * Math.exp(-(q - 1) * 7);
    var dj = Math.hypot(ax - FAM.jx, y - FAM.jy), sp = 1.63 * S.n * m * (0.55 + 1.1 * Math.exp(-dj * dj / 0.09));
    out[0] = (x < 0 ? -1 : 1) * (-gy / gl) * sp; out[1] = (gx / gl) * sp; out[2] = sp;
    return out;
  }
  function tempAt(x, y, tb) { /* local batch temperature: bulk, less the cool film at the jacketed wall and round the coil */
    var ax = Math.abs(x), t = tb, film = 0.13 / Math.pow(S.n, 0.67), i;
    if (y > -0.1 && y < YJ + 0.1) {
      var tw = S.tin + (S.out - S.tin) * Math.max(0, Math.min(1, y / YJ)), drop = S.fi * (tb - tw);
      t -= drop * Math.exp(-(R - ax) / film);
    }
    if (S.coil) for (i = 0; i < 9; i++) { var d = Math.hypot(ax - 0.8, y - (0.35 + i * PITCH)); if (d < 0.3) t -= S.fc * (tb - S.tin - (S.out - S.tin) * (i + 0.5) / 9) * Math.exp(-Math.max(0, d - 0.03) / (film * 0.8)); }
    return t;
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, agit, jk = null, built = -1, liquid, surf, loopMat, loops = [], field, fieldXY = [], fnx = 0, fny = 0, par, parPos, parCol, pars = [], arrows = [], lastT = -99, trc, trcPos, trcCol, cw, cwPos, cwCol, feed, feedPos, feedCol, bub, bubPos, bubCol, running = false;
  var cool = [], mats = {}, RJ = 0.06;
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('rx3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.rx3d-drag').style.display = 'none'; }
  var R = D_R / 2, TW = 0.035, HD = 0.5, YT = 3.0, YL = D_R, YJ = 2.4, PITCH = 0.2, NTURN = 12, NLP = 72, NTRL = 7, TAIL = 6, NCW = 150, NCC = 70, NFEED = 40, NBUB = 110, FH = 0.045, NPAR = 1100, TP = 6;
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  function shape(pts) { return new T.Shape(pts.map(function (p) { return new T.Vector2(p[0], p[1]); })); }
  function cap(pts, m, z, parent) { var ms = new T.Mesh(new T.ShapeGeometry(shape(pts)), m); ms.position.z = z || 0; (parent || model).add(ms); return ms; }
  /* the back half of a solid of revolution about the vertical axis, one band per edge of its profile (radius, height) */
  function lathe(prof, m, parent) {
    var g = new T.Group();
    for (var j = 0; j < prof.length - 1; j++) {
      if (prof[j][0] === 0 && prof[j + 1][0] === 0) continue;
      g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(prof[j][0], prof[j][1]), new T.Vector2(prof[j + 1][0], prof[j + 1][1])], 56, Math.PI / 2, Math.PI), m));
    }
    (parent || model).add(g); return g;
  }
  function half(prof, m, mCut, parent, z) {
    lathe(prof, m, parent);
    var pts = prof.map(function (p) { return [p[0], p[1]]; }), left = prof.slice().reverse().map(function (p) { return [-p[0], p[1]]; });
    if (prof[0][0] === 0 && prof[prof.length - 1][0] === 0) cap(pts.concat(left.slice(1, -1)), mCut, z || 0.002, parent);
    else { cap(pts, mCut, z || 0.002, parent); cap(left, mCut, z || 0.002, parent); }
  }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.85));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.4); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); scene.add(pivot); model = new T.Group(); pivot.add(model);
    mats.mark = mat(0x8dc63f, 0.5, 0.2); mats.cast = mat(0x55637b); mats.back = mat(0x2a3a55, 0.85, 0.1); mats.cut = mat(0xa9b5c6, 0.95, 0); mats.steel = mat(0xd3d9e2, 0.35, 0.45); mats.dark = mat(0x2c3646, 0.8, 0.1); mats.motor = mat(0x24528d, 0.5, 0.3);
    mats.wall = new T.MeshStandardMaterial({ color: 0xa8b8d0, transparent: true, opacity: 0.2, roughness: 0.3, metalness: 0.2, depthWrite: false, side: T.DoubleSide });
    var i, a, prof = [], N = 12;
    /* vessel shell: outer surface up, inner surface back down */
    for (i = 0; i <= N; i++) { a = i / N * Math.PI / 2; prof.push([(R + TW) * Math.sin(a), -(HD + TW) * Math.cos(a)]); }
    for (i = 0; i <= N; i++) { a = i / N * Math.PI / 2; prof.push([(R + TW) * Math.cos(a), YT + (HD + TW) * Math.sin(a)]); }
    for (i = N; i >= 0; i--) { a = i / N * Math.PI / 2; prof.push([R * Math.cos(a), YT + HD * Math.sin(a)]); }
    for (i = N; i >= 0; i--) { a = i / N * Math.PI / 2; prof.push([R * Math.sin(a), -HD * Math.cos(a)]); }
    prof[0][0] = 0; prof[prof.length - 1][0] = 0;
    half(prof, mats.wall, mats.cut);
    /* batch: a tinted face on the cut plane and the liquid surface */
    var lq = []; for (i = 0; i <= N; i++) { a = i / N * Math.PI / 2; lq.push([R * Math.sin(a), -HD * Math.cos(a)]); }
    lq.push([R, YL], [-R, YL]); for (i = N; i >= 1; i--) { a = i / N * Math.PI / 2; lq.push([-R * Math.sin(a), -HD * Math.cos(a)]); }
    mats.liq = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.05, depthWrite: false, side: T.DoubleSide });
    liquid = cap(lq, mats.liq, -0.004);
    mats.surf = new T.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.28, depthWrite: false, side: T.DoubleSide });
    surf = new T.Mesh(new T.CircleGeometry(R, 56, Math.PI, Math.PI), mats.surf); surf.rotation.x = -Math.PI / 2; surf.position.y = YL; model.add(surf);
    function bx(w, h, d, x, y, z, m, parent) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y, z); (parent || model).add(b); return b; }
    function cyl(r, h, x, y, z, m, parent) { var c = new T.Mesh(new T.CylinderGeometry(r, r, h, 24), m); c.position.set(x, y, z); (parent || model).add(c); return c; }
    /* baffles, legs, bottom outlet, drive and feed nozzle */
    [-1, 1].forEach(function (sg) { var b = bx(0.19, 2.6, 0.02, sg * (R - 0.11) * 0.707, 1.3, -(R - 0.11) * 0.707, mats.steel); b.rotation.y = sg * Math.PI / 4; });
    [-0.9, 0.9].forEach(function (x) { bx(0.13, 1.0, 0.13, x, -0.85, -0.35, mats.dark); });
    cyl(0.07, 0.34, 0, -HD - 0.2, -0.07, mats.cast); cyl(0.13, 0.04, 0, -HD - 0.38, -0.07, mats.cast);
    var top = YT + HD + TW;
    bx(0.46, 0.34, 0.46, 0, top + 0.17, -0.23, mats.cast); cyl(0.24, 0.62, 0, top + 0.65, -0.23, mats.motor); cyl(0.26, 0.06, 0, top + 0.99, -0.23, mats.motor);
    cyl(0.055, 0.5, -0.6, YT + HD * 0.8 + 0.2, -0.06, mats.cast);
    /* agitator: shaft and a four-blade pitched turbine that pumps downward */
    agit = new T.Group(); model.add(agit);
    cyl(0.045, top - 0.45, 0, (top + 0.45) / 2, 0, mats.steel, agit); cyl(0.09, 0.14, 0, 0.5, 0, mats.steel, agit);
    for (i = 0; i < 4; i++) { var arm = new T.Group(); arm.rotation.y = i * Math.PI / 2; agit.add(arm); var bl = bx(0.36, 0.2, 0.025, 0.26, 0.5, 0, i ? mats.steel : mats.mark, arm); bl.rotation.x = Math.PI / 4; }
    /* circulation in the batch: down the middle, out along the bottom, up the wall and back in at the top */
    /* temperature field on the cut plane: a fine grid over the liquid */
    fnx = Math.ceil(2 * R / FH); fny = Math.ceil((YL + HD) / FH);
    var fpos = [], fcol = [], fidx = [], w1 = fnx + 1, ix, iy;
    for (iy = 0; iy <= fny; iy++) for (ix = 0; ix <= fnx; ix++) {
      var gx0 = -R + ix * (2 * R / fnx), gy0 = -HD + iy * ((YL + HD) / fny), gax = Math.min(Math.abs(gx0), R - 0.004), yb = -HD * Math.sqrt(Math.max(0, 1 - gax * gax / (R * R))) + 0.004;
      var px = (gx0 < 0 ? -1 : 1) * gax, py = Math.max(yb, Math.min(YL - 0.004, gy0)); fpos.push(px, py, -0.1); fcol.push(0, 0, 0); fieldXY.push(px, py);
    }
    for (iy = 0; iy < fny; iy++) for (ix = 0; ix < fnx; ix++) { var v0 = iy * w1 + ix; fidx.push(v0, v0 + 1, v0 + w1 + 1, v0, v0 + w1 + 1, v0 + w1); }
    var fgeo = new T.BufferGeometry(); fgeo.setAttribute('position', new T.Float32BufferAttribute(fpos, 3)); fgeo.setAttribute('color', new T.Float32BufferAttribute(fcol, 3)); fgeo.setIndex(fidx);
    field = new T.Mesh(fgeo, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.84, depthWrite: false, side: T.DoubleSide })); field.frustumCulled = false; model.add(field);
    /* streamlines of the circulation, with arrowheads: down the middle, out along the bottom, up the wall, back in at the top */
    loopMat = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.45 });
    function spow(v, e) { return (v < 0 ? -1 : 1) * Math.pow(Math.abs(v), e); }
    var am = new T.MeshBasicMaterial({ color: 0xffffff }), ag = new T.ConeGeometry(0.04, 0.12, 10);
    [-1, 1].forEach(function (sg) {
      [0.3, 0.52, 0.74, 0.94].forEach(function (q, qi) {
        var arr = new Float32Array((NLP + 1) * 3), k;
        for (k = 0; k <= NLP; k++) {
          var th = k / NLP * Math.PI * 2;
          arr[k * 3] = sg * (FAM.cx - FAM.a * q * spow(Math.cos(th), FAM.e)); arr[k * 3 + 1] = FAM.cy - FAM.b * q * spow(Math.sin(th), FAM.e); arr[k * 3 + 2] = -0.03 - 0.008 * qi;
        }
        var g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(arr, 3));
        var ln = new T.Line(g, loopMat); ln.frustumCulled = false; model.add(ln);
        for (k = 0; k < 2; k++) {
          var kk = Math.round(NLP * (0.12 + 0.5 * k)), a0 = new T.Mesh(ag, am); a0.position.set(arr[kk * 3], arr[kk * 3 + 1], arr[kk * 3 + 2] + 0.006);
          a0.rotation.z = Math.atan2(arr[kk * 3 + 4] - arr[kk * 3 - 2], arr[kk * 3 + 3] - arr[kk * 3 - 3]) - Math.PI / 2; model.add(a0);
        }
      });
    });
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
    var q = points(NPAR * TP, 0.075); par = q[0]; parPos = q[1]; parCol = q[2];
    for (i = 0; i < NPAR; i++) pars.push({ x: 0, y: 0, z: 0, age: 9, life: 0, h: new Float32Array(TP * 2) });
    q = points((NCW + NCC) * 3, 0.15); cw = q[0]; cwPos = q[1]; cwCol = q[2];
    q = points(NFEED, 0.11); feed = q[0]; feedPos = q[1]; feedCol = q[2];
    q = points(NBUB, 0.11); bub = q[0]; bubPos = q[1]; bubCol = q[2];
    arrowsBuild();
  }
  /* the jacket (and the coil when fitted), rebuilt when the type changes. Each piece of cooling water shown on the cut
     face remembers how far up the jacket it is, so that it can be coloured by the water temperature there. */
  function jacket() {
    if (jk) { model.remove(jk); jk.traverse(function (o) { if (o.geometry) o.geometry.dispose(); }); }
    jk = new T.Group(); model.add(jk); built = S.type + (S.coil ? 10 : 0); cool = [];
    var r0 = R + TW, i, k, a;
    function water(pts, frac, z) {
      var m = new T.MeshBasicMaterial({ color: 0xffffff, side: T.DoubleSide });
      [1, -1].forEach(function (sg) { cap(pts.map(function (p) { return [sg * p[0], p[1]]; }), m, z || 0.003, jk); });
      cool.push({ m: m, f: frac, coil: z === 0.005 });
    }
    if (S.type === 0) {            /* plain: a second shell with a gap */
      var g = 0.11; RJ = g / 2;
      half([[r0, -0.03], [r0 + g + 0.025, -0.03], [r0 + g + 0.025, YJ + 0.03], [r0, YJ + 0.03], [r0, YJ], [r0 + g, YJ], [r0 + g, 0], [r0, 0]], mats.cast, mats.cut, jk);
      lathe([[r0 + g - 0.004, 0], [r0 + g - 0.004, YJ]], mats.back, jk);
      for (k = 0; k < NTURN; k++) water([[r0, k * PITCH], [r0 + g, k * PITCH], [r0 + g, (k + 1) * PITCH], [r0, (k + 1) * PITCH]], (k + 0.5) / NTURN);
    } else if (S.type === 1) {     /* dimple: a thin sheet pressed in to touch the wall at each row of welds */
      RJ = 0.035;
      var outer = [], inner = [], y, NS = 96;
      for (i = 0; i <= NS; i++) { y = YJ * i / NS; var rr = r0 + 0.006 + 0.062 * Math.abs(Math.sin(Math.PI * y / PITCH)); outer.push([rr + 0.014, y]); inner.push([rr, y]); }
      half(outer.concat(inner.slice().reverse()), mats.cast, mats.cut, jk);
      for (k = 0; k < NTURN; k++) { var cell = [[r0, k * PITCH]]; for (i = k * 8; i <= (k + 1) * 8; i++) cell.push(inner[i]); cell.push([r0, (k + 1) * PITCH]); water(cell, (k + 0.5) / NTURN); }
      var dm = new T.MeshBasicMaterial({ color: 0x1f2b3d, side: T.DoubleSide }), dg = new T.CircleGeometry(0.024, 12);
      for (k = 0; k <= NTURN; k++) for (i = 0; i < 12; i++) {
        a = Math.PI + Math.PI * (i + (k % 2 ? 0.5 : 0) + 0.25) / 12; if (a > Math.PI * 2 - 0.08) continue;
        var d = new T.Mesh(dg, dm); d.position.set((r0 + 0.004) * Math.cos(a), k * PITCH, (r0 + 0.004) * Math.sin(a)); d.lookAt(0, k * PITCH, 0); jk.add(d);
      }
    } else {                       /* half-pipe: split pipe wound round the wall */
      var rp = 0.085; RJ = 0.045;
      for (k = 0; k < NTURN; k++) {
        var yc = (k + 0.5) * PITCH, arc = [], arcO = [];
        for (i = 0; i <= 10; i++) { a = -Math.PI / 2 + Math.PI * i / 10; arc.push([r0 + rp * Math.cos(a), yc + rp * Math.sin(a)]); arcO.push([r0 + (rp + 0.014) * Math.cos(a), yc + (rp + 0.014) * Math.sin(a)]); }
        lathe(arcO, mats.cast, jk);
        [1, -1].forEach(function (sg) { cap(arcO.concat(arc.slice().reverse()).map(function (p) { return [sg * p[0], p[1]]; }), mats.cut, 0.002, jk); });
        water(arc, (k + 0.5) / NTURN);
      }
    }
    /* the path of the water round the back of the vessel, one line per turn, coloured by its temperature in paint() */
    for (k = 0; k < NTURN; k++) {
      var hp = new Float32Array(33 * 3);
      for (i = 0; i <= 32; i++) { a = Math.PI + Math.PI * i / 32; hp[i * 3] = (r0 + RJ) * Math.cos(a); hp[i * 3 + 1] = (k + 0.25 + 0.5 * i / 32) * PITCH; hp[i * 3 + 2] = (r0 + RJ) * Math.sin(a); }
      var hg = new T.BufferGeometry(); hg.setAttribute('position', new T.BufferAttribute(hp, 3));
      var hm = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.75 }), hl = new T.Line(hg, hm); hl.frustumCulled = false; jk.add(hl);
      cool.push({ m: hm, f: (k + 0.5) / NTURN, line: true });
    }
    /* cooling water nozzles: in at the bottom left, out at the top right */
    [[-1, 0.12], [1, YJ - 0.12]].forEach(function (n) { var c = new T.Mesh(new T.CylinderGeometry(0.06, 0.06, 0.42, 20), mats.cast); c.rotation.z = Math.PI / 2; c.position.set(n[0] * (r0 + 0.3), n[1], -0.07); jk.add(c); });
    if (S.coil) {                  /* internal coil: nine turns of pipe in the liquid, shown as the back half of each turn */
      for (k = 0; k < 9; k++) {
        var ring = new T.Mesh(new T.TorusGeometry(0.8, 0.03, 10, 44, Math.PI), mats.steel); ring.rotation.x = -Math.PI / 2; ring.rotation.z = 0; ring.position.y = 0.35 + k * PITCH; jk.add(ring);
        var cc = []; for (i = 0; i < 14; i++) { a = i / 14 * Math.PI * 2; cc.push([0.8 + 0.022 * Math.cos(a), 0.35 + k * PITCH + 0.022 * Math.sin(a)]); }
        var ro = []; for (i = 0; i < 16; i++) { a = i / 16 * Math.PI * 2; ro.push([0.8 + 0.032 * Math.cos(a), 0.35 + k * PITCH + 0.032 * Math.sin(a)]); }
        [1, -1].forEach(function (sg) { cap(ro.map(function (p) { return [sg * p[0], p[1]]; }), mats.cut, 0.003, jk); });
        water(cc, (k + 0.5) / 9, 0.005);
      }
    }
    items.forEach(function (it) { if (it.n[6] === 'coil') it.off = !S.coil; }); measured = false;
  }
  var rgb = [0, 0, 0], bubs = [], cws = [], feeds = [];
  for (var bi = 0; bi < NBUB; bi++) bubs.push({ on: false, x: 0, y: 0, z: 0, v: 0 });
  for (bi = 0; bi < NCW + NCC; bi++) cws.push({ s: Math.random() });
  for (bi = 0; bi < NFEED; bi++) feeds.push({ u: Math.random() });
  function waterRGB(frac, coil) { if (S.view === 'temp') tempRGB(S.tin + (S.out - S.tin) * frac, rgb); else tempRGB(5 + 105 * Math.min(1, (coil ? 1.6 * S.F / F0 : S.vw) / 3), rgb); return rgb; }
  function paint() { fieldDirty = true; arrowsUpdate(); cool.forEach(function (c) { waterRGB(c.f, c.coil); var w = c.line ? 0.35 : 0; c.m.color.setRGB(rgb[0] + (1 - rgb[0]) * w, rgb[1] + (1 - rgb[1]) * w, rgb[2] + (1 - rgb[2]) * w); }); }
  /* heat flux arrows: from the batch into the jacketed wall, their length in proportion to the heat the wall can pass
     at that height (the water is coldest at the bottom, so the arrows are longest there) */
  var harrows = [];
  function arrowsBuild() {
    var m = new T.MeshBasicMaterial({ color: 0xffb648 }), i;
    for (i = 0; i < 16; i++) {
      var g = new T.Group(), sh = new T.Mesh(new T.CylinderGeometry(0.013, 0.013, 1, 8), m), hd = new T.Mesh(new T.ConeGeometry(0.04, 0.1, 10), m);
      sh.rotation.z = Math.PI / 2; hd.rotation.z = -Math.PI / 2; g.add(sh); g.add(hd); g.userData = { sh: sh, hd: hd, y: 0.2 + 2.0 * Math.floor(i / 2) / 7, sg: i % 2 ? 1 : -1 };
      g.position.set(0, g.userData.y, 0.012); g.scale.x = g.userData.sg; model.add(g); harrows.push(g);
    }
  }
  function arrowsUpdate() {
    harrows.forEach(function (g) {
      var u = g.userData, tw = S.tin + (S.outCap - S.tin) * Math.max(0, Math.min(1, u.y / YJ)), flux = Math.max(0, S.u * (S.tb - tw) / 1000), len = Math.min(0.62, 0.028 * flux);
      u.hd.position.x = R - 0.05; u.sh.scale.y = Math.max(0.01, len - 0.1); u.sh.position.x = R - 0.1 - Math.max(0.01, len - 0.1) / 2; g.visible = len > 0.11;
    });
  }
  var spin = 0, fieldDirty = true;
  function step(dt) {
    var j, n, t, k, l, ti = 0, e = dt > 0 ? 1 - Math.exp(-dt * 1.3) : 1;
    S.shown += (S.tb - S.shown) * e;
    tempRGB(S.shown, rgb); mats.liq.color.setRGB(rgb[0], rgb[1], rgb[2]); mats.surf.color.setRGB(rgb[0], rgb[1], rgb[2]);
    spin += dt * (RPM * Math.PI / 30) * S.n; agit.rotation.y = -spin;   /* turns at its real speed */
    /* temperature field: recoloured while the batch temperature is moving, or when something has changed */
    if (Math.abs(S.shown - lastT) > 0.04 || fieldDirty) {
      var col = field.geometry.attributes.color;
      for (j = 0; j < fieldXY.length / 2; j++) {
        if (S.view === 'temp') tempRGB(tempAt(fieldXY[j * 2], fieldXY[j * 2 + 1], S.shown), rgb);
        else { vel(fieldXY[j * 2], fieldXY[j * 2 + 1], vout); tempRGB(5 + 105 * Math.min(1, vout[2] / 3), rgb); }   /* same rainbow, 0 to 3 m/s */
        col.setXYZ(j, rgb[0], rgb[1], rgb[2]);
      }
      col.needsUpdate = true; lastT = S.shown; fieldDirty = false;
    }
    /* particles carried by the velocity field, each leaving a short streak: the animated CFD view */
    for (j = 0; j < NPAR; j++) {
      var pp = pars[j]; pp.age += dt;
      if (pp.age > pp.life) {
        var tries = 0; do { pp.x = (Math.random() * 2 - 1) * R; pp.y = -HD + Math.random() * (YL + HD); tries++; } while (!inLiquid(pp.x, pp.y) && tries < 20);
        pp.z = -0.012 - Math.random() * 0.03; pp.age = dt > 0 ? 0 : Math.random() * 3; pp.life = 1.6 + Math.random() * 2.6;
        for (t = 0; t < TP; t++) { pp.h[t * 2] = pp.x; pp.h[t * 2 + 1] = pp.y; }
      }
      vel(pp.x, pp.y, vout);
      if (dt > 0) {
        for (t = TP - 1; t > 0; t--) { pp.h[t * 2] = pp.h[t * 2 - 2]; pp.h[t * 2 + 1] = pp.h[t * 2 - 1]; }
        pp.x += vout[0] * dt; pp.y += vout[1] * dt; pp.h[0] = pp.x; pp.h[1] = pp.y;
        if (!inLiquid(pp.x, pp.y)) pp.age = 99;
      }
      var fade = Math.min(1, pp.age * 3) * Math.min(1, (pp.life - pp.age) * 3), br = Math.max(0, fade) * Math.min(1, 0.35 + vout[2] * 1.1);
      for (t = 0; t < TP; t++) { k = (j * TP + t) * 3; parPos[k] = pp.h[t * 2]; parPos[k + 1] = pp.h[t * 2 + 1]; parPos[k + 2] = pp.z; var bv = br * (1 - t / TP); parCol[k] = bv; parCol[k + 1] = bv; parCol[k + 2] = bv; }
    }
    /* cooling water: round and up the jacket behind the wall, and round the coil when fitted */
    var rj = R + TW + RJ, sp = dt * 0.03 * (S.F / F0) * (0.6 + 0.5 * VEL[S.type]);
    for (j = 0; j < NCW + NCC; j++) {
      var c = cws[j], coil = j >= NCW; c.s += coil ? sp * 1.6 : sp; if (c.s >= 1) c.s -= 1;
      var turns = coil ? 9 : NTURN, rad = coil ? 0.8 : rj, y0 = coil ? 0.35 - PITCH / 2 : 0, on = coil ? S.coil : true;
      waterRGB(c.s, coil);
      for (t = 0; t < 3; t++) {
        var ss = c.s - t * 0.0016, ph = ss * turns * Math.PI * 2, z = rad * Math.sin(ph), v = on && z < -0.02 && ss > 0 ? (1 - t / 3) : 0;
        k = (j * 3 + t) * 3; cwPos[k] = rad * Math.cos(ph); cwPos[k + 1] = y0 + ss * turns * PITCH; cwPos[k + 2] = z;
        cwCol[k] = (rgb[0] * 0.6 + 0.4) * v; cwCol[k + 1] = (rgb[1] * 0.6 + 0.4) * v; cwCol[k + 2] = (rgb[2] * 0.6 + 0.4) * v;
      }
    }
    /* reactant falling from the feed nozzle: more of it when the addition is faster */
    var nf = Math.min(NFEED, Math.round(NFEED * 1.6 / S.tadd)), fall = YT + HD * 0.8 - YL;
    for (j = 0; j < NFEED; j++) {
      var f = feeds[j]; f.u += dt * 1.3; if (f.u >= 1) f.u -= 1;
      k = j * 3; feedPos[k] = -0.6 + (j % 3 - 1) * 0.012; feedPos[k + 1] = YT + HD * 0.8 - fall * f.u * f.u; feedPos[k + 2] = -0.06;
      var fv = j < nf ? 0.9 : 0; feedCol[k] = fv; feedCol[k + 1] = fv * 0.75; feedCol[k + 2] = fv * 0.3;
    }
    /* boiling: vapour bubbles rise through the batch once the balance point passes the boiling point */
    var boiling = S.state === 'boil' && S.shown > T_BOIL - 4;
    for (j = 0; j < NBUB; j++) {
      var b = bubs[j]; k = j * 3;
      if (!b.on) { if (boiling && dt > 0 && Math.random() < dt * 1.2) { b.on = true; b.x = (Math.random() * 2 - 1) * (R - 0.15); b.y = Math.random() * 0.8; b.z = -0.02 - Math.random() * 0.5; b.v = 0.7 + Math.random() * 0.8; } }
      else { b.y += dt * b.v; b.x += dt * 0.15 * Math.sin(b.y * 9 + j); if (b.y >= YL || !boiling) b.on = false; }
      var bv = b.on ? 1 : 0; bubPos[k] = b.x; bubPos[k + 1] = b.y; bubPos[k + 2] = b.z; bubCol[k] = bv; bubCol[k + 1] = bv; bubCol[k + 2] = bv;
    }
    [par, cw, feed, bub].forEach(function (p) { p.geometry.attributes.position.needsUpdate = true; p.geometry.attributes.color.needsUpdate = true; });
  }

  /* ----- names and tags: a column each side of the reactor, each joined to its part.
     Entries: kind, text, anchor x, y, z, side (L or R), key, wide screens only ----- */
  var ITEMS = [
    ['l', 'Agitator drive', -0.24, YT + HD + 0.75, -0.1, 'L'],
    ['t', 'Reactant added over 3.0 h', -0.6, YT + HD * 0.8 + 0.3, 0, 'L', 'add'],
    ['t', 'Batch 60 °C', -0.5, 1.75, 0, 'L', 'tb'],
    ['l', 'Impeller', -0.3, 0.5, 0, 'L'],
    ['t', 'Cooling water in · 25 °C', -(R + TW + 0.42), 0.12, 0, 'L', 'inl'],
    ['t', 'Cooling water out · 33.5 °C', R + TW + 0.42, YJ - 0.12, 0, 'R', 'out'],
    ['t', 'Plain jacket · U 300 W/m²·K · water 0.3 m/s', R + TW + 0.05, 1.5, 0, 'R', 'jk'],
    ['t', 'Heat flow, batch to jacket · up to 9.1 kW/m²', R - 0.2, 0.77, 0, 'R', 'fx'],
    ['l', 'Internal coil', 0.8, 0.95, 0, 'R', 'coil'],
    ['l', 'Baffle', (R - 0.11) * 0.707, 2.45, -(R - 0.11) * 0.707, 'R'],
    ['l', 'Vessel wall, 12 mm', R + TW / 2, YT - 0.25, 0, 'R']
  ];
  var tags = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'rx3d-tag' : 'rx3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, y: 0, tag: n[0] === 't', off: n[6] === 'coil', shown: true };
    if (n[6] && n[0] === 't') tags[n[6]] = it; return it;
  });
  var W = 0, H = 0, measured = false, wideNow = true, v3 = T ? new T.Vector3() : null;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function place() {
    var pt = { x: 0, y: 0 }, gap = 8;
    items.forEach(function (q) {
      var show = !q.off && (q.tag || wideNow);
      if (q.shown !== show) { q.shown = show; q.el.style.display = show ? '' : 'none'; q.path.style.display = show ? '' : 'none'; q.dot.style.display = show ? '' : 'none'; measured = false; }
    });
    if (!measured) { items.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    items.forEach(function (q) { toScreen(q.n[2], q.n[3], q.n[4], pt); q.ax = pt.x; q.ay = pt.y; });
    ['L', 'R'].forEach(function (band) {
      var list = items.filter(function (q) { return q.n[5] === band && q.shown && q.w > 0; }), i, l; list.sort(function (a, b) { return a.ay - b.ay; });
      for (i = 0; i < list.length; i++) { l = list[i]; l.y = Math.max(l.ay, 46 + l.h / 2, i ? list[i - 1].y + (list[i - 1].h + l.h) / 2 + gap : -1e9); }
      for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.y = Math.min(l.y, H - 14 - l.h / 2, i < list.length - 1 ? list[i + 1].y - (list[i + 1].h + l.h) / 2 - gap : 1e9); }
      for (i = 0; i < list.length; i++) {
        l = list[i]; var lx = band === 'L' ? 10 : W - 10 - l.w;
        l.el.style.transform = 'translate(' + lx.toFixed(1) + 'px,' + (l.y - l.h / 2).toFixed(1) + 'px)';
        l.path.setAttribute('d', 'M' + l.ax.toFixed(1) + ' ' + l.ay.toFixed(1) + 'L' + (band === 'L' ? lx + l.w : lx).toFixed(1) + ' ' + l.y.toFixed(1));
        l.dot.setAttribute('cx', l.ax.toFixed(1)); l.dot.setAttribute('cy', l.ay.toFixed(1));
      }
    });
  }

  /* ----- view ----- */
  var yawUser = -0.34, pitchUser = 0.12, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0, CY = 1.55;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var px = Math.min(W / (wideNow ? 6.4 : 4.3), (H - 74) / 6.3), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180)), off = 10 / px;
    camera.aspect = W / H; camera.position.set(0, CY + off, dist); camera.lookAt(0, CY + off, 0); camera.updateProjectionMatrix();
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

  function setType(i) { S.type = i; typeBtns.forEach(function (b) { b.setAttribute('aria-pressed', parseInt(b.getAttribute('data-type'), 10) === i ? 'true' : 'false'); }); }
  function setCoil(on) { S.coil = on; btnCoil.setAttribute('aria-pressed', on ? 'true' : 'false'); }
  typeBtns.forEach(function (b) { b.addEventListener('click', function () { setType(parseInt(b.getAttribute('data-type'), 10)); calc('type'); }); });
  btnCoil.addEventListener('click', function () { setCoil(!S.coil); calc('coil'); });
  inAdd.addEventListener('input', function () { calc('add'); });
  inFlow.addEventListener('input', function () { calc('flow'); });
  inTin.addEventListener('input', function () { calc('tin'); });
  inAgi.addEventListener('input', function () { calc('agi'); });
  $('rx3d-reset').addEventListener('click', function () { inAdd.value = 3; inFlow.value = 14; inTin.value = 25; inAgi.value = 100; setType(0); setCoil(false); calc(); });
  var viewBtns = Array.prototype.slice.call(fig.querySelectorAll('[data-view]'));
  viewBtns.forEach(function (b) { b.addEventListener('click', function () {
    S.view = b.getAttribute('data-view'); viewBtns.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
    $('rx3d-leg').textContent = S.view === 'temp' ? 'Temperature, 5 to 110 °C (batch and cooling water)' : 'Liquid speed, 0 to 3 m/s (batch and cooling water)';
    paint(); if (!running) render(0);
  }); });
  var btnNames = $('rx3d-names');
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
