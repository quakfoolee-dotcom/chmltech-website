/* Agitator article: 3D model of R-101, a stirred reactor cut in half, with four impellers to choose from
   (needs three.js r128+ as window.THREE). The numbers repeat the article's worked example: 10 m3 batch, 2.34 m
   across, 1,000 kg/m3, a 0.88 m pitched blade turbine at 84 rpm drawing 1.84 kW. Turbulent power numbers 1.27,
   0.30, 5.0 and 0.35 and flow numbers 0.79, 0.56 and 0.72 are typical values. Illustrative: the laminar constants,
   the anchor's figures, the tank without baffles and the size of the cavern in a thick liquid. */
(function () {
  'use strict';
  var fig = document.getElementById('ag3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.ag3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.ag3d-lines');
  var inRpm = $('ag3d-rpm'), inVisc = $('ag3d-visc'), btnBaf = $('ag3d-baf'), btnDye = $('ag3d-dye');
  var impBtns = Array.prototype.slice.call(fig.querySelectorAll('[data-imp]'));
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- mixing calculations (same constants and formulas as the article) ----- */
  var RHO = 1000, VOL = 10, TD = Math.pow(4 * VOL / Math.PI, 1 / 3);
  var IMP = [
    { name: 'Pitched blade turbine', D: 0.88, np: 1.27, kp: 45, nq: 0.79, rpm: 84, kind: 'axial' },
    { name: 'Hydrofoil', D: 0.88, np: 0.3, kp: 40, nq: 0.56, rpm: 136, kind: 'axial' },
    { name: 'Rushton turbine', D: 0.88, np: 5.0, kp: 70, nq: 0.72, rpm: 53, kind: 'radial' },
    { name: 'Anchor', D: 2.22, np: 0.35, kp: 200, nq: 0.05, rpm: 20, kind: 'tangential' }
  ];
  function npOf(im, re, baf) { return im.kp / re + im.np * (baf || im.kind === 'tangential' ? 1 : 0.35) * (1 - Math.exp(-re / 500)); }
  /* ----- the velocity field on the cut plane, CFD style. Each impeller sets up one or two families of closed
     circulation paths on each side of the shaft; the liquid follows them, fastest in the stream leaving the impeller
     and slow at the centre of each loop. A swirling tank adds a component round the shaft. Schematic, not a solved
     flow: the shapes and speeds are typical of each impeller. Speeds are in m/s. ----- */
  var FAMS = [
    [{ cx: 0.6, cy: 1.0, a: 0.5, b: 1.12, e: 0.75, dir: 1, jx: 0.3, jy: 0.5 }],
    [{ cx: 0.6, cy: 1.08, a: 0.47, b: 1.2, e: 0.75, dir: 1, jx: 0.28, jy: 0.45 }],
    [{ cx: 0.6, cy: 0.26, a: 0.5, b: 0.52, e: 0.8, dir: -1, jx: 0.66, jy: 0.78 }, { cx: 0.6, cy: 1.56, a: 0.5, b: 0.76, e: 0.8, dir: 1, jx: 0.66, jy: 0.78 }],
    []
  ];
  var VMAX = 3, vout = [0, 0, 0, 0];
  function inLiquid(x, y) { var ax = Math.abs(x); return ax < R && y < surfY(ax) && y > -HD * Math.sqrt(Math.max(0, 1 - ax * ax / (R * R))); }
  function vel(x, y, out) { /* out: in-plane x and y components, the component round the shaft, and the total speed */
    out[0] = out[1] = out[2] = out[3] = 0;
    if (!inLiquid(x, y)) return out;
    var ax = Math.abs(x), n = S.rpm / 60, fams = FAMS[S.imp], c = S.cav, xm = ax / c, ym = YI + (y - YI) / c, best = 9, bf = null, i, f, X, Y, q;
    for (i = 0; i < fams.length; i++) {
      f = fams[i]; X = (xm - f.cx) / f.a; Y = (ym - f.cy) / f.b; var pw = 2 / f.e; q = Math.pow(Math.pow(Math.abs(X), pw) + Math.pow(Math.abs(Y), pw), 1 / pw);
      if (q < best) { best = q; bf = f; }
    }
    if (bf && best < 1.6 && (c >= 0.999 || inLiquid(xm, ym))) {
      X = (xm - bf.cx) / bf.a; Y = (ym - bf.cy) / bf.b; var p2 = 2 / bf.e;
      var gx = Math.pow(Math.abs(X), p2 - 1) * (X < 0 ? -1 : 1) / bf.a, gy = Math.pow(Math.abs(Y), p2 - 1) * (Y < 0 ? -1 : 1) / bf.b, gl = Math.hypot(gx, gy);
      if (gl > 1e-6) {
        var m = best <= 1 ? (best / 0.72) * Math.exp(1 - best / 0.72) : (1 / 0.72) * Math.exp(1 - 1 / 0.72) * Math.exp(-(best - 1) * 7);
        var dj = Math.hypot(xm - bf.jx, ym - bf.jy), sp = S.v0 * m * (0.55 + 1.1 * Math.exp(-dj * dj / 0.09)) * (1 - 0.75 * S.swirl);
        out[0] = (x < 0 ? -1 : 1) * (-gy / gl) * bf.dir * sp; out[1] = (gx / gl) * bf.dir * sp;
      }
    }
    if (IMP[S.imp].kind === 'tangential') out[2] = 0.75 * 2 * Math.PI * n * ax;
    else if (S.swirl > 0) out[2] = 0.4 * S.swirl * 2 * Math.PI * n * Math.min(ax, 0.5 * R) * (ax > 0.5 * R ? Math.pow(0.5 * R / ax, 0.6) : 1);
    out[3] = Math.hypot(out[0], out[1], out[2]);
    return out;
  }
  function speedRGB(v, out) { /* CFD rainbow: blue at rest through cyan, green and yellow to red at VMAX */
    var t = Math.max(0, Math.min(1, v / VMAX)) * 4, k = Math.min(3, Math.floor(t)), u = t - k, C = [[0.07, 0.16, 0.62], [0.1, 0.72, 0.9], [0.3, 0.82, 0.36], [0.98, 0.84, 0.2], [0.93, 0.22, 0.16]];
    out[0] = C[k][0] + (C[k + 1][0] - C[k][0]) * u; out[1] = C[k][1] + (C[k + 1][1] - C[k][1]) * u; out[2] = C[k][2] + (C[k + 1][2] - C[k][2]) * u; return out;
  }
  var S = { imp: 0, baf: true, rpm: 84, mu: 0.001, re: 1.08e6, np: 1.27, p: 1.84, q: 0.75, tip: 3.87, blend: 24, cav: 1, swirl: 0, vd: 0, mode: 'axial' };
  var lastKey = 'design';
  function say(key) {
    switch (key) {
      case 'design': return 'Design point: the pitched blade turbine at 84 rpm pushes liquid down the centre and it returns up the wall. It draws 1.84 kW, pumps the whole batch through itself every 13 seconds and blends an addition in about 24 seconds.';
      case 'imp0': return 'Pitched blade turbine: angled blades push the liquid down the centre and it returns up the wall, one loop each side. A good all-round choice for blending and heat transfer.';
      case 'imp1': return 'Hydrofoil: narrow, curved blades give almost pure axial flow. At the same 1.84 kW it turns faster and pumps more than any other impeller here, with the least shear.';
      case 'imp2': return 'Rushton turbine: flat blades throw the liquid out to the wall, where it splits into a loop above and a loop below. At the same 1.84 kW it pumps about half as much, but its jet is intensely turbulent, which is what breaks up gas bubbles.';
      case 'imp3': return 'Anchor: it sweeps close to the wall and carries the liquid round with it. Little moves from top to bottom, so dye stays in bands. It earns its place in thick liquids, where turbines fail.';
      case 'nobaf': return 'No baffles: the liquid spins as one body, the surface dips into a vortex, and the top-to-bottom circulation almost stops. The impeller draws less power because it is turning in liquid that is already moving with it.';
      case 'baf': return 'Baffles fitted: they break the spin and turn it into top-to-bottom circulation.';
      case 'faster': return 'Faster: the pattern keeps its shape and the liquid speeds up in proportion. Power rises with the cube of speed, so 20% more speed costs about 73% more power.';
      case 'slower': return 'Slower: the pattern keeps its shape and the liquid slows in proportion. Power falls with the cube of speed, and blend time rises.';
      case 'thick': return 'A thicker liquid lowers the Reynolds number. The flow is still turbulent enough to reach the whole tank, but blending is slowing down.';
      case 'cavern': return 'Cavern: in this thick liquid the turbine moves only a pocket around itself. The liquid near the wall and the surface is still, so dye added at the top never reaches the impeller. More speed helps little; the answer is a different impeller.';
      case 'anchorthick': return 'The anchor in a thick liquid: it still reaches the wall, so the whole batch moves and the jacket surface is kept swept. This is the service it is made for.';
      case 'tip': return 'This speed is beyond what the impeller would be run at: the tip speed and the power are far above normal practice.';
    }
    return '';
  }
  function calc(changed) {
    var im = IMP[S.imp]; S.rpm = parseFloat(inRpm.value); S.mu = 0.001 * Math.pow(10, parseFloat(inVisc.value) / 20);
    var n = S.rpm / 60, re = RHO * n * im.D * im.D / S.mu, np = npOf(im, re, S.baf), turb = im.kind !== 'tangential';
    S.re = re; S.np = np; S.p = np * RHO * n * n * n * Math.pow(im.D, 5) / 1000; S.q = im.nq * n * Math.pow(im.D, 3) * re / (re + 100); S.tip = Math.PI * im.D * n;
    S.cav = turb ? Math.max(0.4, Math.min(1, 0.4 + 0.6 * (Math.log(re) / Math.LN10 - 1.5) / 1.5)) : 1;
    S.swirl = turb ? (S.baf ? 0 : Math.min(1, Math.max(0, (Math.log(re) / Math.LN10 - 2) / 1.5))) : 1;
    S.vd = turb && !S.baf ? Math.min(1.25, 0.75 * Math.pow(S.rpm / im.rpm, 2)) * S.swirl : 0;
    var nth, cavern = turb && re < 300;
    if (!turb) nth = 150;
    else { var fo = Math.pow(np, 1 / 3) * re; nth = (fo > 6370 ? 5.2 / Math.pow(np, 1 / 3) : 183 * 183 / (Math.pow(np, 2 / 3) * re)) * Math.pow(TD / im.D, 2) * (S.baf ? 1 : 3); }
    S.blend = cavern ? Infinity : nth / n; S.cavern = cavern; if (turb) S.q *= 1 - 0.7 * S.swirl;
    S.v0 = Math.min(2.4, 0.42 * S.tip * (im.kind === 'radial' ? 1.25 : 1) * Math.pow(im.nq / 0.79, 0.5)) * re / (re + 100);
    S.mode = !turb ? 'tangential' : cavern ? 'cavern' : S.swirl > 0.5 ? 'swirl' : im.kind;
    var cp = S.mu * 1000;
    $('ag3d-imp-o').textContent = im.name; $('ag3d-rpm-o').textContent = S.rpm.toFixed(0) + ' rpm · tip ' + S.tip.toFixed(1) + ' m/s';
    $('ag3d-visc-o').textContent = cp < 1000 ? (cp < 10 ? cp.toFixed(1).replace('.0', '') : cp.toFixed(0)) + ' mPa·s' : (cp / 1000).toFixed(cp < 10000 ? 1 : 0) + ' Pa·s';
    function big(x) { return x >= 1e4 ? (Math.round(x / Math.pow(10, Math.floor(Math.log(x) / Math.LN10) - 2)) * Math.pow(10, Math.floor(Math.log(x) / Math.LN10) - 2)).toLocaleString('en-CA') : x >= 100 ? Math.round(x).toLocaleString('en-CA') : x.toFixed(1); }
    function secs(t) { return !isFinite(t) ? 'Never' : t < 120 ? t.toFixed(0) + ' s' : t < 7200 ? (t / 60).toFixed(0) + ' min' : (t / 3600).toFixed(0) + ' h'; }
    $('ag3d-bl').textContent = secs(S.blend); $('ag3d-re').textContent = big(re);
    $('ag3d-p').textContent = (S.p < 10 ? S.p.toFixed(2) : S.p.toFixed(0)) + ' kW'; $('ag3d-pv').textContent = (S.p / VOL < 10 ? (S.p / VOL).toFixed(2) : (S.p / VOL).toFixed(0)) + ' kW';
    $('ag3d-q').textContent = S.q.toFixed(2) + ' m³/s'; $('ag3d-tn').textContent = im.kind === 'tangential' ? 'Not applicable' : cavern ? 'Cavern only' : secs(VOL / S.q);
    var fastTip = S.tip > 8, chip = $('ag3d-chip');
    var regime = re > 1e4 ? 'Turbulent' : re > 10 ? 'Transitional' : 'Laminar', patt = { axial: 'axial flow', radial: 'radial flow', tangential: 'tangential flow', swirl: 'swirl and vortex', cavern: 'cavern' }[S.mode];
    chip.textContent = regime + ' · ' + patt; chip.classList.toggle('is-bad', S.mode === 'cavern' || S.mode === 'swirl' || fastTip);
    var design = S.imp === 0 && S.baf && S.rpm === 84 && parseFloat(inVisc.value) === 0, key = lastKey, thick = parseFloat(inVisc.value) > 0;
    if (design) key = 'design';
    else if (cavern) key = 'cavern';
    else if (fastTip) key = 'tip';
    else if (changed === 'imp') key = 'imp' + S.imp;
    else if (changed === 'baf') key = S.baf ? 'baf' : (turb ? 'nobaf' : 'imp3');
    else if (changed === 'rpm') key = S.rpm > im.rpm ? 'faster' : S.rpm < im.rpm ? 'slower' : key;
    else if (changed === 'visc') key = !thick ? key : turb ? 'thick' : 'anchorthick';
    if ((key === 'design' && !design) || (key === 'cavern' && !cavern) || (key === 'tip' && !fastTip) || (key === 'nobaf' && (S.baf || !turb)) || ((key === 'thick' || key === 'anchorthick') && !thick))
      key = !S.baf && turb ? 'nobaf' : thick ? (turb ? 'thick' : 'anchorthick') : 'imp' + S.imp;
    lastKey = key; $('ag3d-say').textContent = say(key);
    btnBaf.textContent = S.baf ? 'Baffles fitted' : 'No baffles';
    var narrow = !wideNow;
    tags.imp.el.textContent = narrow ? 'Np ' + np.toFixed(2) : im.name + ' · power number ' + np.toFixed(2);
    tags.spd.el.textContent = S.rpm.toFixed(0) + ' rpm' + (narrow ? '' : ' · ' + (S.p < 10 ? S.p.toFixed(2) : S.p.toFixed(0)) + ' kW');
    tags.bl.el.textContent = (narrow ? 'Blend ' : 'Blend time ') + (isFinite(S.blend) ? secs(S.blend) : 'never');
    measured = false; chart();
    if (ok) { if (builtImp !== S.imp) impeller(); paint(); if (!running) render(0); }
  }
  /* small live chart: power number against Reynolds number for this impeller */
  function chart() {
    var el = $('ag3d-svg'), im = IMP[S.imp], L = function (v) { return Math.log(v) / Math.LN10; };
    var X = function (re) { return 40 + (L(Math.max(1, Math.min(1e7, re)))) / 7 * 246; }, Y = function (np) { return 160 - (L(Math.max(0.1, Math.min(100, np))) + 1) / 3 * 146; }, s = '', re, d = '';
    [0.1, 1, 10, 100].forEach(function (v) { s += '<line x1="40" x2="286" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="rgba(255,255,255,.10)"/><text x="35" y="' + (Y(v) + 3.5) + '" text-anchor="end">' + v + '</text>'; });
    [[1, '1'], [100, '100'], [1e4, '10,000'], [1e6, '1,000,000']].forEach(function (q) { s += '<line x1="' + X(q[0]) + '" x2="' + X(q[0]) + '" y1="14" y2="160" stroke="rgba(255,255,255,.07)"/><text x="' + X(q[0]) + '" y="173" text-anchor="middle">' + q[1] + '</text>'; });
    s += '<text x="163" y="187" text-anchor="middle">Power number against Reynolds number</text>';
    for (re = 1; re <= 1.0001e7; re *= 1.3) d += (d ? 'L' : 'M') + X(re).toFixed(1) + ' ' + Y(npOf(im, re, S.baf)).toFixed(1);
    s += '<path d="' + d + '" fill="none" stroke="#5EC8FF" stroke-width="2.2"/>';
    s += '<text x="' + (X(3) + 6) + '" y="' + (Y(npOf(im, 3, S.baf)) - 4) + '" style="fill:#5EC8FF;font-weight:600">Laminar</text><text x="282" y="' + (Y(npOf(im, 1e6, S.baf)) - 8) + '" text-anchor="end" style="fill:#5EC8FF;font-weight:600">Turbulent</text>';
    s += '<circle cx="' + X(S.re).toFixed(1) + '" cy="' + Y(S.np).toFixed(1) + '" r="4.8" fill="' + (S.mode === 'cavern' ? '#FF7A5C' : '#8DC63F') + '" stroke="#061833" stroke-width="1.5"/>';
    el.innerHTML = s;
  }

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, agit, impG = null, builtImp = -1, liquid = null, surf = null, bafG, running = false;
  var field, fieldXY = [], fnx = 0, fny = 0, par, parPos, parCol, pars = [], arrows = [], loopPool = [], ringPool = [], loops = [], rings = [], trc, trcPos, trcCol, rtr, rtrPos, rtrCol, dye, dyePos, mats = {};
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('ag3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.ag3d-drag').style.display = 'none'; }
  var R = TD / 2, TW = 0.035, HD = 0.5, YT = 3.0, YL = TD, YI = 0.78, NLP = 72, MAXL = 16, MAXR = 12, NTRL = 7, TAIL = 6, NRT = 5, RTAIL = 4, NDYE = 360, NH = 12, FH = 0.045, NPAR = 1300, TP = 6;
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  function shape(pts) { return new T.Shape(pts.map(function (p) { return new T.Vector2(p[0], p[1]); })); }
  function cap(pts, m, z, parent) { var ms = new T.Mesh(new T.ShapeGeometry(shape(pts)), m); ms.position.z = z || 0; (parent || model).add(ms); return ms; }
  function lathe(prof, m, parent) {
    var g = new T.Group();
    for (var j = 0; j < prof.length - 1; j++) {
      if (prof[j][0] === 0 && prof[j + 1][0] === 0) continue;
      g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(prof[j][0], prof[j][1]), new T.Vector2(prof[j + 1][0], prof[j + 1][1])], 56, Math.PI / 2, Math.PI), m));
    }
    (parent || model).add(g); return g;
  }
  function bx(w, h, d, x, y, z, m, parent) { var b = new T.Mesh(new T.BoxGeometry(w, h, d), m); b.position.set(x, y, z); (parent || model).add(b); return b; }
  function cyl(r, h, x, y, z, m, parent) { var c = new T.Mesh(new T.CylinderGeometry(r, r, h, 24), m); c.position.set(x, y, z); (parent || model).add(c); return c; }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.85));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.4); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); scene.add(pivot); model = new T.Group(); pivot.add(model);
    mats.cast = mat(0x55637b); mats.cut = mat(0xa9b5c6, 0.95, 0); mats.steel = mat(0xd3d9e2, 0.35, 0.45); mats.dark = mat(0x2c3646, 0.8, 0.1); mats.motor = mat(0x24528d, 0.5, 0.3); mats.mark = mat(0x8dc63f, 0.5, 0.2);
    mats.wall = new T.MeshStandardMaterial({ color: 0xa8b8d0, transparent: true, opacity: 0.2, roughness: 0.3, metalness: 0.2, depthWrite: false, side: T.DoubleSide });
    mats.liq = new T.MeshBasicMaterial({ color: 0x2aa8c8, transparent: true, opacity: 0.06, depthWrite: false, side: T.DoubleSide });
    mats.surf = new T.MeshBasicMaterial({ color: 0x7fd8ee, transparent: true, opacity: 0.3, depthWrite: false, side: T.DoubleSide });
    var i, a, prof = [], N = 12;
    for (i = 0; i <= N; i++) { a = i / N * Math.PI / 2; prof.push([(R + TW) * Math.sin(a), -(HD + TW) * Math.cos(a)]); }
    for (i = 0; i <= N; i++) { a = i / N * Math.PI / 2; prof.push([(R + TW) * Math.cos(a), YT + (HD + TW) * Math.sin(a)]); }
    for (i = N; i >= 0; i--) { a = i / N * Math.PI / 2; prof.push([R * Math.cos(a), YT + HD * Math.sin(a)]); }
    for (i = N; i >= 0; i--) { a = i / N * Math.PI / 2; prof.push([R * Math.sin(a), -HD * Math.cos(a)]); }
    prof[0][0] = 0; prof[prof.length - 1][0] = 0;
    lathe(prof, mats.wall);
    var pts = prof.map(function (p) { return [p[0], p[1]]; }), left = prof.slice().reverse().map(function (p) { return [-p[0], p[1]]; });
    cap(pts.concat(left.slice(1, -1)), mats.cut, 0.002);
    /* baffles: two on the cut plane and two on the back wall */
    bafG = new T.Group(); model.add(bafG);
    bx(0.19, 2.5, 0.02, R - 0.115, 1.3, -0.012, mats.steel, bafG); bx(0.19, 2.5, 0.02, -(R - 0.115), 1.3, -0.012, mats.steel, bafG);
    [-1, 1].forEach(function (sg) { var b = bx(0.19, 2.5, 0.02, sg * (R - 0.115) * 0.707, 1.3, -(R - 0.115) * 0.707, mats.steel, bafG); b.rotation.y = sg * Math.PI / 4; });
    [-0.9, 0.9].forEach(function (x) { bx(0.13, 1.0, 0.13, x, -0.85, -0.35, mats.dark); });
    cyl(0.07, 0.34, 0, -HD - 0.2, -0.07, mats.cast); cyl(0.13, 0.04, 0, -HD - 0.38, -0.07, mats.cast);
    var top = YT + HD + TW;
    bx(0.46, 0.34, 0.46, 0, top + 0.17, -0.23, mats.cast); cyl(0.24, 0.62, 0, top + 0.65, -0.23, mats.motor); cyl(0.26, 0.06, 0, top + 0.99, -0.23, mats.motor);
    cyl(0.055, 0.5, -0.6, YT + HD * 0.8 + 0.2, -0.06, mats.cast);
    agit = new T.Group(); model.add(agit);
    /* speed field on the cut plane: a fine grid over the liquid, coloured by the local speed */
    fnx = Math.ceil(2 * R / FH); fny = Math.ceil((YL + 0.75 + HD) / FH);
    var fpos = [], fcol = [];
    for (var iy = 0; iy <= fny; iy++) for (var ix = 0; ix <= fnx; ix++) { var fx = -R + ix * (2 * R / fnx), fy = -HD + iy * FH; fpos.push(fx, fy, -0.008); fcol.push(0, 0, 0); fieldXY.push(fx, fy); }
    var fgeo = new T.BufferGeometry(); fgeo.setAttribute('position', new T.Float32BufferAttribute(fpos, 3)); fgeo.setAttribute('color', new T.Float32BufferAttribute(fcol, 3));
    field = new T.Mesh(fgeo, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.86, depthWrite: false, side: T.DoubleSide })); field.frustumCulled = false; model.add(field);
    /* flow paths: a pool of closed loops on the cut plane and of half-circles round the back of the tank */
    var lm = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.42 }), rm = new T.LineBasicMaterial({ color: 0xcfeeff, transparent: true, opacity: 0.55 });
    for (i = 0; i < MAXL; i++) { var g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(new Float32Array((NLP + 1) * 3), 3)); var ln = new T.Line(g, lm); ln.frustumCulled = false; model.add(ln); loopPool.push(ln); }
    for (i = 0; i < MAXR; i++) { var g2 = new T.BufferGeometry(); g2.setAttribute('position', new T.BufferAttribute(new Float32Array(33 * 3), 3)); var l2 = new T.Line(g2, rm); l2.frustumCulled = false; model.add(l2); ringPool.push(l2); }
    var am = new T.MeshBasicMaterial({ color: 0xffffff }), ag = new T.ConeGeometry(0.04, 0.12, 10);
    for (i = 0; i < MAXL * 2; i++) { var ar = new T.Mesh(ag, am); ar.visible = false; model.add(ar); arrows.push(ar); }
    var c2 = document.createElement('canvas'); c2.width = c2.height = 64; var x2 = c2.getContext('2d'), gr2 = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr2.addColorStop(0, 'rgba(255,255,255,1)'); gr2.addColorStop(0.3, 'rgba(255,255,255,.65)'); gr2.addColorStop(1, 'rgba(255,255,255,0)');
    x2.fillStyle = gr2; x2.fillRect(0, 0, 64, 64);
    var tex = new T.CanvasTexture(c2);
    function points(cnt, size, additive) {
      var gp = new T.BufferGeometry(), ps = new Float32Array(cnt * 3), cl = new Float32Array(cnt * 3);
      gp.setAttribute('position', new T.BufferAttribute(ps, 3)); gp.setAttribute('color', new T.BufferAttribute(cl, 3));
      var pt = new T.Points(gp, new T.PointsMaterial({ size: size, map: tex, transparent: true, depthWrite: false, vertexColors: additive, blending: additive ? T.AdditiveBlending : T.NormalBlending, sizeAttenuation: true }));
      pt.frustumCulled = false; model.add(pt); return [pt, ps, cl];
    }
    var q = points(MAXL * NTRL * TAIL, 0.09, true); trc = q[0]; trcPos = q[1]; trcCol = q[2];
    q = points(MAXR * NRT * RTAIL, 0.1, true); rtr = q[0]; rtrPos = q[1]; rtrCol = q[2];
    q = points(NPAR * TP, 0.078, true); par = q[0]; parPos = q[1]; parCol = q[2]; trc.visible = false;
    for (i = 0; i < NPAR; i++) pars.push({ x: 0, y: 0, z: 0, age: 9, life: 0, h: new Float32Array(TP * 2) });
    q = points(NDYE, 0.17, false); dye = q[0]; dyePos = q[1]; dye.material.color.set(0xff5fd0); dye.material.opacity = 0.95;
    for (i = 0; i < NDYE; i++) dyePos[i * 3 + 1] = -50;
  }
  /* the impeller on its shaft, rebuilt when the type changes */
  function impeller() {
    if (impG) { agit.remove(impG); impG.traverse(function (o) { if (o.geometry) o.geometry.dispose(); }); }
    impG = new T.Group(); agit.add(impG); builtImp = S.imp;
    var top = YT + HD + TW, i, arm, b, ybot = S.imp === 3 ? 1.95 : YI;
    cyl(0.045, top - ybot + 0.06, 0, (top + ybot - 0.06) / 2, 0, mats.steel, impG);
    if (S.imp === 0) {            /* four flat blades at 45 degrees */
      cyl(0.09, 0.14, 0, YI, 0, mats.steel, impG);
      for (i = 0; i < 4; i++) { arm = new T.Group(); arm.rotation.y = i * Math.PI / 2; impG.add(arm); b = bx(0.36, 0.2, 0.025, 0.26, YI, 0, i ? mats.steel : mats.mark, arm); b.rotation.x = Math.PI / 4; }
    } else if (S.imp === 1) {     /* three narrow blades with a shallow pitch */
      cyl(0.08, 0.12, 0, YI, 0, mats.steel, impG);
      for (i = 0; i < 3; i++) {
        arm = new T.Group(); arm.rotation.y = i * Math.PI * 2 / 3; impG.add(arm);
        b = bx(0.2, 0.15, 0.02, 0.17, YI, 0, i ? mats.steel : mats.mark, arm); b.rotation.x = Math.PI / 3.2;
        b = bx(0.2, 0.11, 0.02, 0.35, YI, 0, i ? mats.steel : mats.mark, arm); b.rotation.x = Math.PI / 2.5;
      }
    } else if (S.imp === 2) {     /* a disc carrying six upright flat blades */
      cyl(0.33, 0.025, 0, YI, 0, mats.steel, impG); cyl(0.08, 0.12, 0, YI, 0, mats.steel, impG);
      for (i = 0; i < 6; i++) { arm = new T.Group(); arm.rotation.y = i * Math.PI / 3; impG.add(arm); bx(0.22, 0.18, 0.02, 0.33, YI, 0, i ? mats.steel : mats.mark, arm); }
    } else {                      /* anchor: two arms that follow the wall and the bottom head */
      var ra = 1.11, pathPts = [], k;
      pathPts.push(new T.Vector3(-ra, 1.95, 0)); pathPts.push(new T.Vector3(-ra, 0.15, 0));
      for (k = 1; k < 12; k++) { var a = Math.PI * k / 12; pathPts.push(new T.Vector3(-ra * Math.cos(a) * 0.98, 0.1 - 0.52 * Math.sin(a), 0)); }
      pathPts.push(new T.Vector3(ra, 0.15, 0)); pathPts.push(new T.Vector3(ra, 1.95, 0));
      impG.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pathPts, false, 'catmullrom', 0.1), 80, 0.045, 10, false), mats.steel));
      bx(2 * ra, 0.07, 0.05, 0, 1.95, 0, mats.steel, impG);
      bx(0.1, 0.5, 0.06, ra, 1.2, 0, mats.mark, impG);
    }
  }
  /* flow paths for the present impeller, baffles and viscosity. Each loop is a closed curve on the cut plane with a
     direction of travel; each ring is a half-circle round the back of the tank. */
  function spow(v, e) { return (v < 0 ? -1 : 1) * Math.pow(Math.abs(v), e); }
  function layout() {
    var L = [], Rg = [], kind = IMP[S.imp].kind, c = S.cav, k, sg, th;
    function add(fn, w) { var p = []; for (k = 0; k <= NLP; k++) { th = k / NLP * Math.PI * 2; var q = fn(th); p.push([q[0] * c, YI + (q[1] - YI) * c]); } L.push({ p: p, w: w == null ? 1 : w }); }
    if (kind !== 'tangential') {
      var qs = S.swirl > 0.5 ? [0.5, 0.85] : (kind === 'axial' ? [0.3, 0.52, 0.74, 0.94] : [0.4, 0.68, 0.94]);
      [-1, 1].forEach(function (s2) {
        FAMS[S.imp].forEach(function (f) {
          qs.forEach(function (q) {
            /* travel direction along the path matches the velocity field */
            add(function (t) { var a = f.dir > 0 ? t : -t; return f.cy > 0.9 || kind === 'axial' ? [s2 * (f.cx - f.a * q * spow(Math.cos(a), f.e)), f.cy - f.b * q * spow(Math.sin(a), f.e)] : [s2 * (f.cx - f.a * q * spow(Math.cos(a), f.e)), f.cy - f.b * q * spow(Math.sin(a), f.e)]; }, 1 - 0.75 * S.swirl);
          });
        });
      });
    }
    if (kind === 'tangential' || S.swirl > 0.5) {
      var hs = [0.25, 0.65, 1.05, 1.45, 1.85], top = YL + S.vd * 0.1 - 0.2;
      hs.forEach(function (y, i) { if (y < top) { Rg.push({ y: y, r: 0.92 * R, w: 1 }); Rg.push({ y: y + 0.2 * (i % 2 ? 1 : -1) * 0.5, r: 0.55 * R, w: kind === 'tangential' ? 0.6 : 1.5 }); } });
    }
    return { L: L.slice(0, MAXL), R: Rg.slice(0, MAXR) };
  }
  function surfY(r) { return YL + S.vd * (Math.pow(r / R, 2) - 0.5); }
  var rgb = [0, 0, 0];
  function paint() { /* redraw the flow paths, the liquid and its surface for the current state */
    var lay = layout(), i, k, old = loops;
    loops = [];
    for (i = 0; i < MAXL; i++) {
      var ln = loopPool[i], l = lay.L[i]; ln.visible = !!l; if (!l) { arrows[i * 2].visible = false; arrows[i * 2 + 1].visible = false; continue; }
      var arr = ln.geometry.attributes.position.array, len = [0];
      for (k = 0; k <= NLP; k++) { arr[k * 3] = l.p[k][0]; arr[k * 3 + 1] = l.p[k][1]; arr[k * 3 + 2] = -0.03 - 0.012 * (i % 4); if (k) len.push(len[k - 1] + Math.hypot(l.p[k][0] - l.p[k - 1][0], l.p[k][1] - l.p[k - 1][1])); }
      ln.geometry.attributes.position.needsUpdate = true;
      var tr = old[i] && old[i].tr; if (!tr) { tr = []; for (k = 0; k < NTRL; k++) tr.push((k + ((i * 7 + k * 3) % 10) / 16) / NTRL); }
      loops.push({ arr: arr, len: len, total: len[NLP], tr: tr, w: l.w });
      for (k = 0; k < 2; k++) { /* two arrowheads on each loop show which way the liquid goes */
        var kk = Math.round(NLP * (0.12 + 0.5 * k)), a0 = arrows[i * 2 + k];
        a0.visible = true; a0.position.set(arr[kk * 3], arr[kk * 3 + 1], arr[kk * 3 + 2] + 0.006);
        a0.rotation.z = Math.atan2(arr[kk * 3 + 4] - arr[kk * 3 - 2], arr[kk * 3 + 3] - arr[kk * 3 - 3]) - Math.PI / 2; a0.scale.setScalar(0.6 + 0.4 * S.cav);
      }
    }
    rings = [];
    for (i = 0; i < MAXR; i++) {
      var rl = ringPool[i], r = lay.R[i]; rl.visible = !!r; if (!r) continue;
      var ra = rl.geometry.attributes.position.array;
      for (k = 0; k <= 32; k++) { var a = Math.PI + Math.PI * k / 32; ra[k * 3] = r.r * Math.cos(a); ra[k * 3 + 1] = r.y; ra[k * 3 + 2] = r.r * Math.sin(a); }
      rl.geometry.attributes.position.needsUpdate = true;
      rings.push({ y: r.y, r: r.r, w: r.w, ph: i * 1.3 });
    }
    /* liquid face and surface, dished into a vortex when there are no baffles */
    if (liquid) { model.remove(liquid); liquid.geometry.dispose(); model.remove(surf); surf.geometry.dispose(); }
    var lq = [], N = 12, sp = [];
    for (i = 0; i <= N; i++) { var b = i / N * Math.PI / 2; lq.push([R * Math.sin(b), -HD * Math.cos(b)]); }
    for (i = 0; i <= 24; i++) { var rr = R - 2 * R * i / 24; lq.push([rr, surfY(Math.abs(rr))]); }
    for (i = N; i >= 1; i--) { var b2 = i / N * Math.PI / 2; lq.push([-R * Math.sin(b2), -HD * Math.cos(b2)]); }
    liquid = cap(lq, mats.liq, -0.004);
    for (i = 0; i <= 16; i++) sp.push(new T.Vector2(Math.max(0.001, R * i / 16), surfY(R * i / 16)));
    surf = new T.Mesh(new T.LatheGeometry(sp, 48, Math.PI / 2, Math.PI), mats.surf); model.add(surf);
    var col = field.geometry.attributes.color, idx = [], w1 = fnx + 1, ix, iy;
    var fpa = field.geometry.attributes.position;
    for (i = 0; i < fieldXY.length / 2; i++) { /* grid points outside the liquid are pulled onto its surface or the bottom head, so the edge is smooth */
      var gx0 = fieldXY[i * 2], gy0 = fieldXY[i * 2 + 1], gax = Math.min(Math.abs(gx0), R - 0.004), ys = surfY(gax) - 0.004, yb = -HD * Math.sqrt(Math.max(0, 1 - gax * gax / (R * R))) + 0.004, gy1 = Math.max(yb, Math.min(ys, gy0));
      fpa.setXYZ(i, (gx0 < 0 ? -1 : 1) * gax, gy1, -0.008);
      vel((gx0 < 0 ? -1 : 1) * gax, gy1, vout); speedRGB(vout[3], rgb); col.setXYZ(i, rgb[0], rgb[1], rgb[2]);
    }
    fpa.needsUpdate = true;
    for (iy = 0; iy < fny; iy++) for (ix = 0; ix < fnx; ix++) {
      var cx0 = -R + (ix + 0.5) * (2 * R / fnx), cy0 = -HD + (iy + 0.5) * FH, ax0 = Math.abs(cx0);
      if (cy0 > surfY(Math.min(ax0, R)) + FH * 1.1 || cy0 < -HD * Math.sqrt(Math.max(0, 1 - Math.min(ax0, R) * Math.min(ax0, R) / (R * R))) - FH * 1.1) continue;
      var v0 = iy * w1 + ix; idx.push(v0, v0 + 1, v0 + w1 + 1, v0, v0 + w1 + 1, v0 + w1);
    }
    field.geometry.setIndex(idx); col.needsUpdate = true;
    bafG.visible = S.baf && IMP[S.imp].kind !== 'tangential';
    items.forEach(function (it) { if (it.n[6] === 'baf') it.off = !bafG.visible; if (it.n[6] === 'stag') it.off = S.mode !== 'cavern'; if (it.n[6] === 'vor') it.off = !(S.vd > 0.25); });
    if (dyeOn) dyeAttach(false);
  }
  /* ----- dye: released at the surface near the feed nozzle, then carried along whatever paths the liquid follows ----- */
  var dyes = [], dyeOn = false, DX = -0.6;
  for (var di = 0; di < NDYE; di++) dyes.push({ kind: 0, i: 0, u: 0, x: 0, y: 0, z: 0, ox: 0, oy: 0, oz: 0, sp: 1 });
  function nearestLoop(x, y) { /* the loop and position on it nearest to a point of the cut plane */
    var best = 1e9, bi = -1, bu = 0, i, k;
    for (i = 0; i < loops.length; i++) for (k = 0; k < NLP; k += 3) { var d = Math.hypot(loops[i].arr[k * 3] - x, loops[i].arr[k * 3 + 1] - y); if (d < best) { best = d; bi = i; bu = k / NLP; } }
    return { d: best, i: bi, u: bu };
  }
  function dyeAttach(fresh) {
    var y0 = surfY(Math.abs(DX)) - 0.03, nl = nearestLoop(DX, y0), i;
    for (i = 0; i < NDYE; i++) {
      var d = dyes[i];
      if (fresh) { d.x = DX + (Math.random() - 0.5) * 0.16; d.y = y0 - Math.random() * 0.14; d.z = -0.05 - Math.random() * 0.1; d.ox = (Math.random() - 0.5) * 0.07; d.oy = (Math.random() - 0.5) * 0.07; d.oz = -Math.random() * 0.12; d.sp = 0.7 + Math.random() * 0.6; d.kind = 0; }
      if (fresh || d.kind) {
        if (rings.length && (!loops.length || Math.random() < 0.8)) { var bj = 0, bd = 1e9; rings.forEach(function (r, j) { var dd = Math.abs(r.y - d.y) + Math.abs(r.r - Math.abs(d.x)) * 0.5; if (dd < bd) { bd = dd; bj = j; } }); d.kind = 2; d.i = bj; d.u = fresh ? 0.5 + (d.x < 0 ? 0 : 0.5) + Math.random() * 0.04 : (Math.atan2(d.z, d.x) / (Math.PI * 2) + 1) % 1; }
        else if (loops.length) { var q = fresh ? nl : nearestLoop(d.x, d.y); if (q.d < 0.4) { d.kind = 1; d.i = q.i; d.u = q.u; } else d.kind = 3; }
        else d.kind = 3;
      }
    }
  }
  var spin = 0;
  function step(dt, clock) {
    var n = S.rpm / 60, j, k, t, l, ti = 0, kind = IMP[S.imp].kind, turb = S.re > 1e4 ? 1 : Math.max(0.05, (Math.log(S.re) / Math.LN10 - 1) / 3);
    spin += dt * n * Math.PI * 2; agit.rotation.y = -spin;   /* seen from above the agitator turns anticlockwise; the swirl tracers and the dye go the same way */
    /* liquid speed along the loops scales with tip speed and with how much of the impeller's flow number survives */
    var vl = Math.min(2.6, 0.3 * S.tip * (kind === 'radial' ? 0.75 : 1) * Math.min(1, S.re / (S.re + 100)) * Math.pow(IMP[S.imp].nq / 0.79, 0.5) * (IMP[S.imp].np < 1 ? 0.8 : 1));
    for (j = 0; j < 0; j++) {
      l = loops[j];
      for (var m = 0; m < NTRL; m++) {
        var u = l ? l.tr[m] : 0;
        for (t = 0; t < TAIL; t++) {
          k = ti * 3; ti++;
          if (!l) { trcCol[k] = trcCol[k + 1] = trcCol[k + 2] = 0; continue; }
          var uu = u - t * Math.min(0.03, 0.004 + 0.011 * vl); if (uu < 0) uu += 1;
          var d = uu * l.total, lo = 0, hi = NLP, mid; while (hi - lo > 1) { mid = (lo + hi) >> 1; if (l.len[mid] <= d) lo = mid; else hi = mid; }
          var fr = (d - l.len[lo]) / Math.max(1e-6, l.len[hi] - l.len[lo]), vis = (1 - t / TAIL) * Math.min(1, 0.4 + 0.5 * vl) * (0.35 + 0.65 * l.w);
          trcPos[k] = l.arr[lo * 3] + (l.arr[hi * 3] - l.arr[lo * 3]) * fr; trcPos[k + 1] = l.arr[lo * 3 + 1] + (l.arr[hi * 3 + 1] - l.arr[lo * 3 + 1]) * fr; trcPos[k + 2] = l.arr[lo * 3 + 2] + 0.004;
          trcCol[k] = vis; trcCol[k + 1] = vis; trcCol[k + 2] = vis;
        }
        if (l) { u += dt * vl * l.w / l.total; if (u >= 1) u -= 1; l.tr[m] = u; }
      }
    }
    /* particles carried by the velocity field, each leaving a short streak: the animated CFD view */
    for (j = 0; j < NPAR; j++) {
      var pp = pars[j]; pp.age += dt;
      if (pp.age > pp.life) {
        var tries = 0; do { pp.x = (Math.random() * 2 - 1) * R; pp.y = -HD + Math.random() * (YL + 0.6 + HD); tries++; } while (!inLiquid(pp.x, pp.y) && tries < 20);
        pp.z = -0.012 - Math.random() * 0.03; pp.age = dt > 0 ? 0 : Math.random() * 3; pp.life = 1.6 + Math.random() * 2.6;
        for (t = 0; t < TP; t++) { pp.h[t * 2] = pp.x; pp.h[t * 2 + 1] = pp.y; }
      }
      vel(pp.x, pp.y, vout);
      if (dt > 0) {
        for (t = TP - 1; t > 0; t--) { pp.h[t * 2] = pp.h[t * 2 - 2]; pp.h[t * 2 + 1] = pp.h[t * 2 - 1]; }
        pp.x += vout[0] * dt; pp.y += vout[1] * dt; pp.h[0] = pp.x; pp.h[1] = pp.y;
        if (!inLiquid(pp.x, pp.y)) pp.age = 99;
      }
      var inpl = Math.hypot(vout[0], vout[1]), fade = Math.min(1, pp.age * 3) * Math.min(1, (pp.life - pp.age) * 3), br = Math.max(0, fade) * Math.min(1, 0.35 + inpl * 1.1);
      for (t = 0; t < TP; t++) { k = (j * TP + t) * 3; parPos[k] = pp.h[t * 2]; parPos[k + 1] = pp.h[t * 2 + 1]; parPos[k + 2] = pp.z; var bv = br * (1 - t / TP); parCol[k] = bv; parCol[k + 1] = bv; parCol[k + 2] = bv; }
    }
    par.geometry.attributes.position.needsUpdate = true; par.geometry.attributes.color.needsUpdate = true;
    /* swirl: tracers round the back of the tank, turning with the liquid */
    var om = n * Math.PI * 2 * (kind === 'tangential' ? 0.75 : 0.5 * S.swirl); ti = 0;
    for (j = 0; j < MAXR; j++) {
      var r = rings[j]; if (r) r.ph += dt * om * r.w * (kind === 'tangential' ? r.r / R : 1);
      for (var m2 = 0; m2 < NRT; m2++) for (t = 0; t < RTAIL; t++) {
        k = ti * 3; ti++;
        if (!r) { rtrCol[k] = rtrCol[k + 1] = rtrCol[k + 2] = 0; continue; }
        var ang = (r.ph + m2 * Math.PI * 2 / NRT) - t * Math.min(0.12, 0.02 + om * 0.03),   /* same way round as the impeller */ z = r.r * Math.sin(ang), v = z < -0.03 ? (1 - t / RTAIL) : 0;
        rtrPos[k] = r.r * Math.cos(ang); rtrPos[k + 1] = r.y; rtrPos[k + 2] = z; rtrCol[k] = v; rtrCol[k + 1] = v; rtrCol[k + 2] = v;
      }
    }
    /* dye */
    if (dyeOn) {
      var hop = dt * n * 0.9 * turb;
      for (j = 0; j < NDYE; j++) {
        var q = dyes[j]; k = j * 3;
        if (q.kind === 1 && loops[q.i]) {
          l = loops[q.i]; q.u += dt * vl * l.w * q.sp / l.total; if (q.u >= 1) q.u -= 1;
          var kk = Math.floor(q.u * NLP); q.x = l.arr[kk * 3] + q.ox; q.y = l.arr[kk * 3 + 1] + q.oy; q.z = l.arr[kk * 3 + 2] + q.oz;
          if (Math.random() < hop) {                      /* turbulence moves it to a neighbouring path, sometimes across the tank */
            if (Math.random() < 0.25) { var nq = nearestLoop(-q.x, q.y); if (nq.i >= 0) { q.i = nq.i; q.u = nq.u; } }
            else { var ni = Math.floor(Math.random() * loops.length), a2 = loops[ni].arr, bu = 0, bd = 1e9; for (t = 0; t < NLP; t += 4) { var dd = Math.hypot(a2[t * 3] - q.x, a2[t * 3 + 1] - q.y); if (dd < bd) { bd = dd; bu = t / NLP; } } if (bd < (kind === 'radial' ? 0.3 : 0.45)) { q.i = ni; q.u = bu; } }
            q.ox = (Math.random() - 0.5) * 0.1; q.oy = (Math.random() - 0.5) * 0.1;
            if (rings.length && Math.random() < 0.6) { q.kind = 2; q.i = Math.floor(Math.random() * rings.length); q.u = Math.random(); }
          }
        } else if (q.kind === 2 && rings[q.i]) {
          var rg = rings[q.i]; q.u += dt * om * rg.w * q.sp / (Math.PI * 2) * (kind === 'tangential' ? rg.r / R : 1); if (q.u >= 1) q.u -= 1;
          var an = q.u * Math.PI * 2; q.x = rg.r * Math.cos(an) + q.ox; q.y = rg.y + q.oy * 2; q.z = rg.r * Math.sin(an);
          if (Math.random() < hop * (kind === 'tangential' ? 0.03 : 0.25)) { var nj = q.i + (Math.random() < 0.5 ? -2 : 2); if (rings[nj]) q.i = nj; }
          if (loops.length && Math.random() < hop * 0.3 && q.z > -0.15) { var nl2 = nearestLoop(q.x, q.y); if (nl2.d < 0.4) { q.kind = 1; q.i = nl2.i; q.u = nl2.u; } }
        } else if (q.kind === 3) { q.x += (Math.random() - 0.5) * dt * 0.02; q.y -= dt * 0.004; }
        dyePos[k] = q.x; dyePos[k + 1] = q.z > 0.02 ? -50 : q.y; dyePos[k + 2] = Math.min(q.z, -0.01) + 0.012;
      }
      dye.geometry.attributes.position.needsUpdate = true;
    }
    [trc, rtr].forEach(function (p) { p.geometry.attributes.position.needsUpdate = true; p.geometry.attributes.color.needsUpdate = true; });
  }

  /* ----- names and tags: a column each side of the reactor, each joined to its part.
     Entries: kind, text, anchor x, y, z, side (L or R), key ----- */
  var ITEMS = [
    ['t', '84 rpm · 1.84 kW', -0.24, YT + HD + 0.75, -0.1, 'L', 'spd'],
    ['l', 'Dye is added here', -0.6, YT + HD * 0.8, 0, 'L'],
    ['l', 'Vortex', -0.25, YL - 0.25, 0, 'L', 'vor'],
    ['l', 'Baffle', -(R - 0.115), 1.9, 0, 'L', 'baf'],
    ['l', 'Shaft', -0.045, 1.5, 0, 'L'],
    ['t', 'Blend time 24 s', 0.75, YL - 0.05, 0, 'R', 'bl'],
    ['l', 'Still liquid', 0.95, 1.95, 0, 'R', 'stag'],
    ['t', 'Pitched blade turbine · power number 1.27', 0.3, YI, 0, 'R', 'imp'],
    ['l', 'Vessel wall', R + TW / 2, YT - 0.2, 0, 'R']
  ];
  var tags = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'ag3d-tag' : 'ag3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, y: 0, tag: n[0] === 't', off: n[6] === 'stag' || n[6] === 'vor', shown: true };
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
  var yawUser = -0.34, pitchUser = 0.14, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0, CY = 1.55;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var px = Math.min(W / (wideNow ? 6.0 : 3.9), (H - 74) / 6.3), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180)), off = 10 / px;
    camera.aspect = W / H; camera.position.set(0, CY + off, dist); camera.lookAt(0, CY + off, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    pivot.position.y = CY; model.position.y = -CY; pivot.rotation.set(pitch, yaw, 0);
    step(dt, clock);
    pivot.updateMatrixWorld(true);
    renderer.render(scene, camera);
    place();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(-0.95, Math.min(0.95, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.1, Math.min(0.6, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  function setImp(i, keepSpeed) { S.imp = i; impBtns.forEach(function (b) { b.setAttribute('aria-pressed', parseInt(b.getAttribute('data-imp'), 10) === i ? 'true' : 'false'); }); if (!keepSpeed) inRpm.value = IMP[i].rpm; }
  function setBaf(on) { S.baf = on; btnBaf.setAttribute('aria-pressed', on ? 'true' : 'false'); }
  function clearDye() { dyeOn = false; if (ok) { for (var i = 0; i < NDYE; i++) dyePos[i * 3 + 1] = -50; dye.geometry.attributes.position.needsUpdate = true; } }
  impBtns.forEach(function (b) { b.addEventListener('click', function () { setImp(parseInt(b.getAttribute('data-imp'), 10)); clearDye(); calc('imp'); }); });
  btnBaf.addEventListener('click', function () { setBaf(!S.baf); calc('baf'); });
  btnDye.addEventListener('click', function () { if (!ok) return; dyeOn = true; dyeAttach(true); if (!running) { for (var i = 0; i < 40; i++) step(0.05, 0); render(0); } });
  inRpm.addEventListener('input', function () { calc('rpm'); });
  inVisc.addEventListener('input', function () { calc('visc'); });
  $('ag3d-reset').addEventListener('click', function () { inVisc.value = 0; setImp(0); setBaf(true); clearDye(); calc(); });
  var btnNames = $('ag3d-names');
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
