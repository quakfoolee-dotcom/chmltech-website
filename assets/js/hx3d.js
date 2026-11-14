/* Heat exchanger article: 3D model of E-101, a horizontal U-tube shell-and-tube steam heater, cut in half
   (needs three.js r128+ as window.THREE). Numbers follow the article's worked example: 6,250 kg/h of feed,
   cp 2.0 kJ/kg.K, 20 to 80 C, steam at 3.0 barg (143.6 C), U = 500 W/m2.K, required area 4.61 m2, 22 tube ends
   in 2 passes. The model holds U x A fixed and recalculates the outlet temperature. Drawn shortened. */
(function () {
  'use strict';
  var fig = document.getElementById('hx3d');
  if (!fig) return;
  var $ = function (id) { return document.getElementById(id); };
  var stage = fig.querySelector('.hx3d-stage'), cv = stage.querySelector('canvas'), svg = stage.querySelector('.hx3d-lines');
  var inFlow = $('hx3d-flow'), inSteam = $('hx3d-steam'), inFoul = $('hx3d-foul');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ----- the calculation ----- */
  var CP = 2.0, T_IN = 20, U0 = 500, AREA = 4.6142, RHO = 850, TUBE_AREA = 11 * Math.PI / 4 * 0.0158 * 0.0158;
  var SAT = [[1, 120.4, 2201], [2, 133.7, 2163], [3, 143.6, 2133], [4, 151.9, 2108], [5, 158.9, 2086]];   /* barg, C, kJ/kg */
  function sat(p) { var i = Math.min(3, Math.max(0, Math.floor(p) - 1)), a = SAT[i], b = SAT[i + 1], u = p - a[0]; return [a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u]; }
  var S = { flow: 6250, p: 3, foul: 0, ts: 143.6, ntu: 0.664, tout: 80, q: 208.3, lmtd: 90.3, ms: 352, v: 0.95 };
  var lastKey = 'design';
  function fmt(n) { return Math.round(n).toLocaleString('en-CA'); }
  function calc(changed) {
    S.flow = parseFloat(inFlow.value); S.p = parseFloat(inSteam.value); S.foul = parseFloat(inFoul.value);
    var st = sat(S.p), c = S.flow / 3600 * CP;                    /* kW/K */
    S.ts = st[0]; S.ntu = U0 * (1 - S.foul / 100) * AREA / (c * 1000);
    S.tout = S.ts - (S.ts - T_IN) * Math.exp(-S.ntu);
    S.q = c * (S.tout - T_IN);
    var d1 = S.ts - T_IN, d2 = S.ts - S.tout; S.lmtd = (d1 - d2) / Math.log(d1 / d2);
    S.ms = S.q / st[1] * 3600; S.v = S.flow / 3600 / RHO / TUBE_AREA;
    $('hx3d-flow-o').textContent = fmt(S.flow) + ' kg/h'; $('hx3d-steam-o').textContent = S.p.toFixed(1) + ' barg'; $('hx3d-foul-o').textContent = S.foul.toFixed(0) + '%';
    $('hx3d-tout').textContent = S.tout.toFixed(1) + ' °C'; $('hx3d-q').textContent = fmt(S.q) + ' kW'; $('hx3d-lmtd').textContent = S.lmtd.toFixed(1) + ' K';
    $('hx3d-ms').textContent = fmt(S.ms) + ' kg/h'; $('hx3d-v').textContent = S.v.toFixed(2) + ' m/s';
    S.tcond = S.ts;   /* condensate leaves as saturated liquid: no subcooling, as in the article's latent-heat balance */
    $('hx3d-tc').textContent = S.tcond.toFixed(1) + ' °C'; $('hx3d-tsn').textContent = S.ts.toFixed(1) + ' °C';
    var design = S.flow === 6250 && Math.abs(S.p - 3) < 0.001 && S.foul === 0, k = lastKey;
    if (design) k = 'design';
    else if (changed === 'foul' || (changed == null && S.foul > 0)) k = S.foul > 0 ? 'foul' : (S.flow !== 6250 ? (S.flow > 6250 ? 'flowUp' : 'flowDown') : (S.p > 3 ? 'steamUp' : 'steamDown'));
    else if (changed === 'flow') k = S.flow > 6250 ? 'flowUp' : S.flow < 6250 ? 'flowDown' : k;
    else if (changed === 'steam') k = S.p > 3.001 ? 'steamUp' : S.p < 2.999 ? 'steamDown' : k;
    if (k === 'design' && !design) k = S.foul > 0 ? 'foul' : S.flow !== 6250 ? (S.flow > 6250 ? 'flowUp' : 'flowDown') : (S.p > 3 ? 'steamUp' : 'steamDown');
    if (k !== lastKey) { lastKey = k; $('hx3d-say').textContent = SAY[k]; }
    tags.fout.el.textContent = 'Feed out · ' + S.tout.toFixed(1) + ' °C';
    tags.steam.el.textContent = 'Steam in · ' + S.p.toFixed(1) + ' barg · ' + S.ts.toFixed(1) + ' °C';
    tags.cond.el.textContent = 'Condensate out · ' + S.tcond.toFixed(1) + ' °C';
    measured = false;
    if (ok) { paintTubes(); if (!running) render(0); }
  }
  var SAY = {
    design: 'Design point from the worked example: 6,250 kg/h heated from 20 to 80 °C needs 208 kW and about 352 kg/h of steam.',
    flowUp: 'More feed through the same area: each kilogram picks up less heat, so the outlet is cooler, even though the total duty is higher.',
    flowDown: 'Less feed through the same area: each kilogram stays longer and leaves hotter, but the total duty falls.',
    steamUp: 'Higher steam pressure means a hotter condensing temperature. The wider temperature difference drives more heat into the feed, and the condensate leaves hotter too.',
    steamDown: 'Lower steam pressure condenses cooler. The temperature difference shrinks, the feed leaves cooler and so does the condensate.',
    foul: 'Fouling adds a resistance at the tube wall, so the same area transfers less heat. This is why the design adds a 20% area margin.'
  };
  /* liquid colour by temperature: blue at 20 C through yellow, orange and red to magenta at 160 C */
  var STOPS = [[20, 63, 169, 245], [50, 255, 214, 102], [80, 255, 138, 61], [110, 255, 80, 60], [160, 214, 48, 140]];
  function tempRGB(t, out) {
    t = Math.max(20, Math.min(160, t));
    for (var i = 1; i < STOPS.length; i++) if (t <= STOPS[i][0]) {
      var a = STOPS[i - 1], b = STOPS[i], u = (t - a[0]) / (b[0] - a[0]);
      out[0] = (a[1] + (b[1] - a[1]) * u) / 255; out[1] = (a[2] + (b[2] - a[2]) * u) / 255; out[2] = (a[3] + (b[3] - a[3]) * u) / 255; return out;
    }
    return out;
  }
  function feedT(s) { return S.ts - (S.ts - T_IN) * Math.exp(-S.ntu * Math.max(0, Math.min(1, s))); }   /* s: fraction of tube length travelled */

  /* ----- 3D ----- */
  var T = window.THREE, renderer = null, scene, camera, model, pivot, tubes = [], cores = [], flows = [], liqIn, liqOut, condMats = [], lines = [], trc, trcPos, trcCol, vap, vapPos, vapCol, drop, dropPos, dropCol, running = false;
  var ok = !!T;
  if (ok) { try { renderer = new T.WebGLRenderer({ canvas: cv, antialias: true, alpha: true }); } catch (e) { ok = false; } }
  if (!ok) { $('hx3d-nogl').hidden = false; cv.style.display = 'none'; fig.querySelector('.hx3d-drag').style.display = 'none'; }

  var HALF0 = Math.PI / 2, HALF = Math.PI;
  var RI = 1.75, RO = 1.95, XL = 11, XB = 9.4, XS = 3.6, XC = 9.6, XN = -1.65, NR = 0.6, AL = Math.asin(NR / RI);
  var ROWS = [[0.28, [-1, -0.5, 0, 0.5, 1]], [0.72, [-0.75, -0.25, 0.25, 0.75]], [1.15, [-0.25, 0.25]]], PATHS = [];
  ROWS.forEach(function (r) { r[1].forEach(function (z) { PATHS.push({ a: r[0], z: z, l1: XB + 0.3, arc: Math.PI * r[0] }); }); });
  function pathPoint(p, s, out) { /* s in 0..1 along one U-tube, by length: lower leg, bend, upper leg */
    var len = 2 * p.l1 + p.arc, d = s * len;
    if (d <= p.l1) return out.set(-0.3 + d, -p.a, p.z);
    if (d <= p.l1 + p.arc) { var th = -Math.PI / 2 + (d - p.l1) / p.a; return out.set(XB + p.a * Math.cos(th), p.a * Math.sin(th), p.z); }
    return out.set(XB - (d - p.l1 - p.arc), p.a, p.z);
  }
  function mat(color, rough, metal) { return new T.MeshStandardMaterial({ color: color, roughness: rough == null ? 0.55 : rough, metalness: metal == null ? 0.3 : metal, side: T.DoubleSide }); }
  /* solid of revolution from a closed (r, axis) outline, back half only, closed with flat section faces */
  function lathe(parent, outline, m, mCut, o) {
    o = o || {};
    var g = new T.Group(), n = outline.length, phi0 = o.phi0 == null ? HALF0 : o.phi0, len = o.len == null ? HALF : o.len;
    for (var i = 0; i < n; i++) {
      var a = outline[i], b = outline[(i + 1) % n];
      if (a[0] === 0 && b[0] === 0) continue;
      g.add(new T.Mesh(new T.LatheGeometry([new T.Vector2(a[0], a[1]), new T.Vector2(b[0], b[1])], Math.max(6, Math.round(44 * len / Math.PI)), phi0, len), m));
    }
    if (mCut) {
      var sg = new T.ShapeGeometry(new T.Shape(outline.map(function (p) { return new T.Vector2(p[0], p[1]); })));
      if (o.capA !== false) g.add(new T.Mesh(sg, mCut));
      if (o.capB !== false) { var c2 = new T.Mesh(sg, mCut); c2.scale.x = -1; g.add(c2); }
    }
    parent.add(g); return g;
  }
  function rect(r0, r1, x0, x1) { return [[r0, x0], [r1, x0], [r1, x1], [r0, x1]]; }
  /* a cylinder wall along x with openings where nozzles enter at the bottom (gapsB) and top (gapsT) of the cut plane */
  function wall(parent, r0, r1, x0, x1, gapsB, gapsT, m, mCut) {
    lathe(parent, rect(r0, r1, x0, x1), m, null, { phi0: HALF0 + AL, len: HALF - 2 * AL });
    [[gapsB, HALF0, true], [gapsT, HALF0 + HALF - AL, false]].forEach(function (q) {
      var x = x0;
      q[0].concat([x1 + NR]).forEach(function (gx) {
        if (gx - NR > x) lathe(parent, rect(r0, r1, x, gx - NR), m, mCut, { phi0: q[1], len: AL, capA: q[2], capB: !q[2] });
        x = gx + NR;
      });
    });
  }
  function build() {
    scene = new T.Scene();
    camera = new T.PerspectiveCamera(24, 1, 1, 400);
    scene.add(new T.HemisphereLight(0xdfeaff, 0x1a2a44, 0.8));
    var key = new T.DirectionalLight(0xffffff, 0.9); key.position.set(-8, 14, 18); scene.add(key);
    var rim = new T.DirectionalLight(0x9fd0ff, 0.45); rim.position.set(12, 4, -8); scene.add(rim);
    pivot = new T.Group(); pivot.position.x = 4.25; scene.add(pivot);   /* turn about the middle of the exchanger */
    model = new T.Group(); model.position.x = -4.25; pivot.add(model);
    /* everything turned about the x axis is built in this frame: lathe axis -> world x, section faces on z = 0 */
    var ax = new T.Group(); ax.rotation.z = -Math.PI / 2; model.add(ax);
    var cast = mat(0x76849a), castCut = mat(0xc3ccd8, 0.95, 0), dark = mat(0x566375), darkCut = mat(0x8c98a9, 0.95, 0), plate = mat(0x8f9bb0, 0.7, 0.2);
    var i, th, o = [], inn = [];

    wall(ax, RI, RO, 0.7, XL, [XC], [XS], cast, castCut);                         /* shell */
    for (i = 0; i <= 10; i++) { th = i / 10 * Math.PI / 2; o.push([RO * Math.cos(th), XL + 1.05 * Math.sin(th)]); inn.push([RI * Math.cos(th), XL + 0.85 * Math.sin(th)]); }
    lathe(ax, o.concat(inn.reverse()), cast, castCut);                             /* rear head */
    wall(ax, RI, RO, -2.6, -0.7, [XN], [XN], cast, castCut);                       /* channel */
    o = []; inn = [];
    for (i = 0; i <= 10; i++) { th = i / 10 * Math.PI / 2; o.push([RO * Math.cos(th), -2.6 - 0.95 * Math.sin(th)]); inn.push([RI * Math.cos(th), -2.6 - 0.75 * Math.sin(th)]); }
    lathe(ax, o.concat(inn.reverse()), cast, castCut);                             /* channel head */
    lathe(ax, rect(0, 2.45, -0.3, 0.3), dark, darkCut);                            /* tubesheet */
    lathe(ax, rect(RO, 2.45, -0.72, -0.3), cast, castCut); lathe(ax, rect(RO, 2.45, 0.3, 0.72), cast, castCut);   /* flanges */
    [2.4, 5.3, 8.0].forEach(function (x) { lathe(ax, rect(0, RI - 0.03, x - 0.04, x + 0.04), plate, darkCut); });  /* support plates */
    var pp = new T.Mesh(new T.BoxGeometry(2.95, 0.1, RI), dark); pp.position.set(-1.775, 0, -RI / 2); model.add(pp);  /* pass partition */
    /* nozzles: vertical, with a flange; the bottom ones are mirrored */
    var NOZ = [[0.45, 1.6], [NR, 1.6], [NR, 2.82], [0.98, 2.82], [0.98, 3.05], [0.45, 3.05]];
    [[XS, 1], [XC, -1], [XN, 1], [XN, -1]].forEach(function (q) { var g = lathe(model, NOZ, cast, castCut); g.position.x = q[0]; g.scale.y = q[1]; });
    /* saddles */
    [1.7, 8.7].forEach(function (x) {
      var s = new T.Mesh(new T.BoxGeometry(0.5, 1.35, 1.7), dark); s.position.set(x, -2.55, -0.85); model.add(s);
      var b = new T.Mesh(new T.BoxGeometry(1.2, 0.12, 2.1), dark); b.position.set(x, -3.28, -1.05); model.add(b);
    });
    /* streak textures: light bands on a mid tone, scrolled along the flow so a surface reads as moving liquid */
    function streaks(alongV) {
      var c = document.createElement('canvas'); c.width = alongV ? 64 : 256; c.height = alongV ? 256 : 64;
      var g = c.getContext('2d'), L = 256, B = 64, r2 = (function (s) { return function () { s = (s * 16807) % 2147483647; return s / 2147483647; }; })(alongV ? 911 : 577);
      g.fillStyle = '#9c9c9c'; g.fillRect(0, 0, c.width, c.height);
      for (var k = 0; k < 46; k++) {
        var len = 30 + r2() * 90, th = 2 + r2() * 7, a0 = r2() * L, b0 = r2() * B, lt = r2() > 0.25, al = 0.25 + r2() * 0.55;
        for (var w = -1; w <= 1; w++) {
          var gr = alongV ? g.createLinearGradient(0, a0 + w * L, 0, a0 + w * L + len) : g.createLinearGradient(a0 + w * L, 0, a0 + w * L + len, 0);
          var cc = lt ? '255,255,255' : '70,70,70';
          gr.addColorStop(0, 'rgba(' + cc + ',0)'); gr.addColorStop(0.5, 'rgba(' + cc + ',' + al + ')'); gr.addColorStop(1, 'rgba(' + cc + ',0)');
          g.fillStyle = gr; if (alongV) g.fillRect(b0, a0 + w * L, th, len); else g.fillRect(a0 + w * L, b0, len, th);
        }
      }
      var t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; return t;
    }
    var texU = streaks(false), texV = streaks(true), points;
    function flowTex(base, rx, ry, axis, dir, rate) { var t = base.clone(); t.needsUpdate = true; t.repeat.set(rx, ry); flows.push({ t: t, axis: axis, dir: dir, rate: rate }); return t; }
    /* U-tubes: a glass wall around a liquid core coloured by the feed temperature at that point */
    var glass = new T.MeshStandardMaterial({ vertexColors: true, transparent: true, opacity: 0.3, roughness: 0.25, metalness: 0.1, depthWrite: false });
    var coreMat = new T.MeshBasicMaterial({ vertexColors: true, map: flowTex(texU, 9, 1, 'x', -1, 'feed') });
    PATHS.forEach(function (p) {
      var c = new T.Curve(); c.getPoint = function (t, target) { return pathPoint(p, t, target || new T.Vector3()); };
      [[0.105, glass, tubes], [0.072, coreMat, cores]].forEach(function (q) {
        var g = new T.TubeGeometry(c, 90, q[0], 8, false);
        g.setAttribute('color', new T.BufferAttribute(new Float32Array(g.attributes.position.count * 3), 3));
        var m = new T.Mesh(g, q[1]); model.add(m); q[2].push(m);
      });
    });
    /* liquid in the channel: the lower chamber holds the cold feed, the upper chamber the heated feed */
    function liquid(tex, opacity) { return new T.MeshBasicMaterial({ color: 0xffffff, map: tex, transparent: opacity < 1, opacity: opacity, side: T.DoubleSide }); }
    var CH = [[0, -0.3], [RI - 0.02, -0.3], [RI - 0.02, -2.6]];
    for (i = 1; i <= 10; i++) { th = i / 10 * Math.PI / 2; CH.push([(RI - 0.02) * Math.cos(th), -2.6 - 0.73 * Math.sin(th)]); }
    liqIn = liquid(null, 0.92); liqOut = liquid(null, 0.92);
    var lq = new T.Group(); lq.position.z = -0.012; model.add(lq);
    var lax = new T.Group(); lax.rotation.z = -Math.PI / 2; lq.add(lax);
    lathe(lax, CH, liqIn, liqIn, { phi0: HALF0, len: HALF / 2, capB: false });
    lathe(lax, CH, liqOut, liqOut, { phi0: HALF0 + HALF / 2, len: HALF / 2, capA: false });
    var COL = [[0, 1.55], [0.44, 1.55], [0.44, 3.3], [0, 3.3]], gcol;
    var mIn = liquid(null, 0.95), mOut = liquid(null, 0.95);
    mIn.color = liqIn.color; mOut.color = liqOut.color;
    gcol = lathe(lq, COL, mIn, mIn); gcol.position.x = XN; gcol.scale.y = -1;
    gcol = lathe(lq, COL, mOut, mOut); gcol.position.x = XN;
    /* condensate: a film along the bottom of the shell and a stream down the outlet nozzle */
    var cond = liquid(flowTex(texV, 0.5, 0.6, 'y', -1, 'cond'), 0.92); condMats.push(cond);
    lathe(lax, rect(RI - 0.13, RI - 0.01, 0.74, XL), cond, cond, { phi0: HALF0, len: 0.55, capB: false });
    var cs = liquid(flowTex(texV, 0.6, 0.6, 'y', -1, 'cond'), 0.95); condMats.push(cs);
    gcol = lathe(lq, [[0, 1.6], [0.26, 1.6], [0.26, 3.3], [0, 3.3]], cs, cs); gcol.position.x = XC; gcol.scale.y = -1;
    /* CFD-style streamlines on the section plane: inlet nozzle -> lower chamber -> tube ends, and tube ends ->
       upper chamber -> outlet nozzle. Lines do not cross; one slow eddy sits in each half of the dished head. */
    var slg = new T.Group(); slg.position.z = -0.004; model.add(slg);
    var lm = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.42 }), lmE = new T.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.26 });
    var ENDS = [1.185, 1.115, 0.755, 0.685, 0.315, 0.245];
    [-1, 1].forEach(function (sg) {                      /* -1: inlet (lower) chamber, +1: outlet (upper) chamber */
      ENDS.forEach(function (ye, n) {
        var x0 = XN + 0.34 - n * 0.136, pts = [], k, u, ax0 = x0, ay0 = 1.75, bx = -0.3, by = ye, k1 = (1.75 - ye) * 0.8, k2 = (bx - x0) * 0.62;
        for (k = 0; k <= 8; k++) pts.push([x0, 3.3 - (3.3 - 1.75) * k / 8, 1.0]);                 /* in the nozzle: fast */
        for (k = 1; k <= 48; k++) {                                                                  /* cubic turn into the tube end */
          u = k / 48; var m = 1 - u, c0 = m * m * m, c1 = 3 * m * m * u, c2 = 3 * m * u * u, c3 = u * u * u;
          pts.push([c0 * ax0 + c1 * ax0 + c2 * (bx - k2) + c3 * bx, c0 * ay0 + c1 * (ay0 - k1) + c2 * by + c3 * by, 0.38 + 0.9 * Math.pow(u, 5)]);
        }
        pts = pts.map(function (q) { return [q[0], q[1] * sg, q[2]]; });
        if (sg > 0) pts.reverse();                       /* outlet side runs from the tubes to the nozzle */
        lines.push(makeLine(pts, false, lm, sg));
      });
      var e = [], a2; for (a2 = 0; a2 <= 40; a2++) { var an = a2 / 40 * Math.PI * 2 * -sg; e.push([-2.86 + 0.3 * Math.cos(an), sg * (0.88 + 0.5 * Math.sin(an)), 0.22]); }
      lines.push(makeLine(e, true, lmE, sg));
    });
    function makeLine(pts, closed, m, sg) {
      var g = new T.BufferGeometry(), arr = new Float32Array(pts.length * 3), len = [0], k;
      for (k = 0; k < pts.length; k++) { arr[k * 3] = pts[k][0]; arr[k * 3 + 1] = pts[k][1]; arr[k * 3 + 2] = 0; if (k) len.push(len[k - 1] + Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1])); }
      g.setAttribute('position', new T.BufferAttribute(arr, 3)); slg.add(new T.Line(g, m));
      var tr = [], n = closed ? 3 : 5; for (k = 0; k < n; k++) tr.push((k + 0.5 * Math.random()) / n);
      return { pts: pts, len: len, total: len[len.length - 1], closed: closed, tr: tr, sg: sg };
    }
    var nT = 0; lines.forEach(function (l) { nT += l.tr.length * TAIL; });
    var ta = null;
    /* steam is a gas: soft, faint puffs that overlap into a cloud. Droplets are small and bright. */
    var c2 = document.createElement('canvas'); c2.width = c2.height = 64; var x2 = c2.getContext('2d'), gr = x2.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.3, 'rgba(255,255,255,.6)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    x2.fillStyle = gr; x2.fillRect(0, 0, 64, 64);
    var tex = new T.CanvasTexture(c2);
    function points_unused() {} points = function (n, size) {
      var g = new T.BufferGeometry(), pos = new Float32Array(n * 3), col = new Float32Array(n * 3);
      g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setAttribute('color', new T.BufferAttribute(col, 3));
      var pt = new T.Points(g, new T.PointsMaterial({ size: size, map: tex, transparent: true, depthWrite: false, vertexColors: true, blending: T.AdditiveBlending, sizeAttenuation: true }));
      pt.frustumCulled = false; model.add(pt); return [pt, pos, col];
    };
    var a = points(NVAP, 1.45); vap = a[0]; vapPos = a[1]; vapCol = a[2];
    a = points(NDROP, 0.3); drop = a[0]; dropPos = a[1]; dropCol = a[2];
    ta = points(nT, 0.17); trc = ta[0]; trcPos = ta[1]; trcCol = ta[2]; trc.position.z = -0.003;
  }
  var rgb = [0, 0, 0], condRGB = [1, 0.3, 0.4], TAIL = 5;
  function paintTubes() {
    tubes.concat(cores).forEach(function (m) {
      var uv = m.geometry.attributes.uv, col = m.geometry.attributes.color;
      for (var i = 0; i < uv.count; i++) { tempRGB(feedT(uv.getX(i)), rgb); col.setXYZ(i, rgb[0], rgb[1], rgb[2]); }
      col.needsUpdate = true;
    });
    tempRGB(T_IN, rgb); liqIn.color.setRGB(rgb[0], rgb[1], rgb[2]);
    tempRGB(S.tout, rgb); liqOut.color.setRGB(rgb[0], rgb[1], rgb[2]);
    tempRGB(S.ts, condRGB); condMats.forEach(function (m) { m.color.setRGB(condRGB[0], condRGB[1], condRGB[2]); });
  }

  /* ----- steam (gas) and condensate droplets ----- */
  var rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return s / 2147483647; }; })(4242);
  var NVAP = 520, NDROP = 150, vp = [], dp = [], v3 = T ? new T.Vector3() : null;
  function spawnSteam(q, fresh) {
    if (fresh) { q.x = 0.6 + rnd() * (XL - 0.3); var r = 1.6 * Math.sqrt(rnd()), a = rnd() * Math.PI; q.y = r * Math.cos(a); q.z = -r * Math.sin(a); q.entering = 0; }
    else { q.x = XS + (Math.random() - 0.5) * 0.6; q.y = 3.2; q.z = -Math.random() * 0.35; q.entering = 1; }
    q.vx = (Math.random() - 0.5) * 1.2; q.vy = (Math.random() - 0.5) * 1.2; q.vz = (Math.random() - 0.5) * 1.2;
  }
  for (var i = 0; i < NVAP; i++) { var q0 = {}; spawnSteam(q0, true); vp.push(q0); }
  for (i = 0; i < NDROP; i++) dp.push({ on: false, x: 0, y: 0, z: 0 });
  function stepParticles(dt) {
    var j, k, q, d, rate = 0.3 * S.ms / 352, RR = 1.6, shown = Math.round(NVAP * (0.45 + 0.55 * (S.p + 1) / 6)), speedFeed = S.flow / 6250, speedCond = 0.35 + 0.65 * S.ms / 352;
    for (j = 0; j < flows.length; j++) { var f = flows[j], sp = dt * (f.rate === 'feed' ? 0.42 * speedFeed : 0.5 * speedCond) * f.dir; if (f.axis === 'x') f.t.offset.x += sp * 0.22; else f.t.offset.y += sp; }
    for (j = 0; j < NVAP; j++) {
      q = vp[j]; k = j * 3;
      if (q.entering) { q.y -= dt * 1.7; q.x += q.vx * dt * 0.12; if (q.y < 1.1) q.entering = 0; }
      else {
        q.vx += (Math.random() - 0.5) * dt * 5; q.vy += (Math.random() - 0.5) * dt * 5; q.vz += (Math.random() - 0.5) * dt * 5;
        q.vx *= 1 - dt * 1.4; q.vy *= 1 - dt * 1.4; q.vz *= 1 - dt * 1.4;
        q.x += q.vx * dt; q.y += q.vy * dt; q.z += q.vz * dt;
        if (q.z > -0.05) { q.z = -0.05; q.vz = -Math.abs(q.vz); }
        var r2 = q.y * q.y + q.z * q.z; if (r2 > RR * RR) { var fz = RR / Math.sqrt(r2); q.y *= fz; q.z *= fz; q.vy *= -0.5; q.vz *= -0.5; }
        if (q.x < 0.5) { q.x = 0.5; q.vx = Math.abs(q.vx); } if (q.x > XL + 0.3) { q.x = XL + 0.3; q.vx = -Math.abs(q.vx); }
        if (dt > 0 && j < shown && Math.random() < dt * rate) { /* gives up its heat on a tube: the gas becomes a liquid droplet */
          for (d = 0; d < NDROP; d++) if (!dp[d].on) { dp[d].on = true; dp[d].x = q.x; dp[d].y = q.y; dp[d].z = q.z; break; }
          spawnSteam(q, false);
        }
      }
      var b = j < shown ? 0.24 : 0;
      vapPos[k] = q.x; vapPos[k + 1] = q.y; vapPos[k + 2] = q.z; vapCol[k] = b; vapCol[k + 1] = b * 0.93; vapCol[k + 2] = b * 0.88;
    }
    for (j = 0; j < NDROP; j++) {
      q = dp[j]; k = j * 3;
      if (q.on) { q.y -= dt * 2.8; if (q.y <= -Math.sqrt(Math.max(0.01, 1.62 * 1.62 - q.z * q.z))) q.on = false; }
      dropPos[k] = q.x; dropPos[k + 1] = q.y; dropPos[k + 2] = q.z; b = q.on ? 1 : 0;
      dropCol[k] = condRGB[0] * b; dropCol[k + 1] = condRGB[1] * b; dropCol[k + 2] = condRGB[2] * b;
    }
    /* tracers ride the streamlines: quick in the nozzle and at the tube ends, slow across the chamber */
    var ti = 0, n2, t2, u2, seg, lo, hi, mid, fr, l2;
    for (j = 0; j < lines.length; j++) {
      l2 = lines[j];
      for (n2 = 0; n2 < l2.tr.length; n2++) {
        u2 = l2.tr[n2];
        for (t2 = 0; t2 < TAIL; t2++) {
          var uu = u2 - t2 * 0.016 * (l2.closed ? 1.6 : 1), vis = 1 - t2 / TAIL;
          if (l2.closed) uu = ((uu % 1) + 1) % 1; else if (uu < 0) { uu = 0; vis = 0; }
          d = uu * l2.total; lo = 0; hi = l2.len.length - 1;
          while (hi - lo > 1) { mid = (lo + hi) >> 1; if (l2.len[mid] <= d) lo = mid; else hi = mid; }
          fr = (d - l2.len[lo]) / Math.max(1e-6, l2.len[hi] - l2.len[lo]);
          k = ti * 3; trcPos[k] = l2.pts[lo][0] + (l2.pts[hi][0] - l2.pts[lo][0]) * fr; trcPos[k + 1] = l2.pts[lo][1] + (l2.pts[hi][1] - l2.pts[lo][1]) * fr; trcPos[k + 2] = 0;
          if (t2 === 0) seg = l2.pts[lo][2] + (l2.pts[hi][2] - l2.pts[lo][2]) * fr;
          vis *= l2.closed ? 0.6 : 1; trcCol[k] = vis; trcCol[k + 1] = vis; trcCol[k + 2] = vis; ti++;
        }
        u2 += dt * 0.55 * speedFeed * seg / l2.total * 2.4; if (u2 >= 1) u2 -= 1; l2.tr[n2] = u2;
      }
    }
    trc.geometry.attributes.position.needsUpdate = true; trc.geometry.attributes.color.needsUpdate = true;
    vap.geometry.attributes.position.needsUpdate = true; vap.geometry.attributes.color.needsUpdate = true;
    drop.geometry.attributes.position.needsUpdate = true; drop.geometry.attributes.color.needsUpdate = true;
  }

  /* ----- names and stream tags: two rows, above and below the exchanger, each joined to its part ----- */
  var ITEMS = [
    ['l', 'Channel', -2.3, 1.85, 0, 'T'], ['t', 'Feed out · 80.0 °C', XN, 3.05, 0, 'T', 'fout'], ['l', 'Tubesheet', 0, 2.3, 0, 'T'],
    ['t', 'Steam in · 3.0 barg · 143.6 °C', XS, 3.05, 0, 'T', 'steam'], ['l', 'Shell', 6.7, 1.85, 0, 'T'], ['l', 'U-bends', XB + 1.0, 0.55, 0.25, 'T'],
    ['t', 'Feed in · 20 °C', XN, -3.05, 0, 'B', 'fin'], ['l', 'Pass partition', -2.5, -0.05, 0, 'B'], ['l', 'U-tubes', 4.4, -0.72, 0.75, 'B'],
    ['l', 'Support plate', 8.0, -1.55, 0, 'B'], ['t', 'Condensate out · 143.6 °C', XC, -3.05, 0, 'B', 'cond']
  ];
  var tags = {}, items = ITEMS.map(function (n) {
    var el = document.createElement('span'); el.className = n[0] === 't' ? 'hx3d-tag' : 'hx3d-label'; el.textContent = n[1]; stage.appendChild(el);
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path'), dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 2.4); if (n[0] === 't') { path.setAttribute('class', 't'); dot.setAttribute('class', 't'); }
    svg.appendChild(path); svg.appendChild(dot);
    var it = { n: n, el: el, path: path, dot: dot, w: 0, h: 0, ax: 0, ay: 0, x: 0, tag: n[0] === 't' };
    if (n[6]) tags[n[6]] = it; return it;
  });
  var W = 0, H = 0, measured = false, wideNow = true;
  function toScreen(x, y, z, out) { v3.set(x, y, z); model.localToWorld(v3); v3.project(camera); out.x = (v3.x * 0.5 + 0.5) * W; out.y = (-v3.y * 0.5 + 0.5) * H; return out; }
  function place() {
    if (!measured) { items.forEach(function (l) { l.w = l.el.offsetWidth; l.h = l.el.offsetHeight; }); measured = true; }
    var pt = { x: 0, y: 0 };
    ['T', 'B'].forEach(function (band) {
      var list = items.filter(function (q) { return q.n[5] === band && (q.tag || (wideNow && q.w > 0)); }), i, l, gap = 10;
      list.forEach(function (q) { toScreen(q.n[2], q.n[3], q.n[4], pt); q.ax = pt.x; q.ay = pt.y; q.x = pt.x; });
      list.sort(function (a, b) { return a.ax - b.ax; });
      for (i = 0; i < list.length; i++) { l = list[i]; l.x = Math.max(l.x, 8 + l.w / 2, i ? list[i - 1].x + (list[i - 1].w + l.w) / 2 + gap : -1e9); }
      for (i = list.length - 1; i >= 0; i--) { l = list[i]; l.x = Math.min(l.x, W - 8 - l.w / 2, i < list.length - 1 ? list[i + 1].x - (list[i + 1].w + l.w) / 2 - gap : 1e9); }
      var by = band === 'T' ? 50 : H - 26;
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
  var yawUser = 0.3, pitchUser = 0.2, yaw = yawUser, pitch = pitchUser, idle = 99, sway = 1, clock = 0;
  function resize() {
    var rc = stage.getBoundingClientRect(); W = rc.width; H = rc.height; measured = false; wideNow = W >= 560;
    if (!ok) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); renderer.setSize(W, H, false);
    var px = Math.min((W - (wideNow ? 44 : 20)) / 16.8, (H - 172) / 6.9), dist = (H / px) / (2 * Math.tan(12 * Math.PI / 180));
    camera.aspect = W / H; camera.position.set(4.25, -0.1, dist); camera.lookAt(4.25, -0.1, 0); camera.updateProjectionMatrix();
  }
  function render(dt) {
    if (!ok) return;
    pivot.rotation.set(pitch, yaw, 0);
    stepParticles(dt);
    pivot.updateMatrixWorld(true);
    renderer.render(scene, camera);
    place();
  }
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, pitch: pitchUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = Math.max(-1.0, Math.min(1.0, drag.yaw + (e.clientX - drag.x) * 0.008));
    pitchUser = Math.max(-0.35, Math.min(0.7, drag.pitch + (e.clientY - drag.y) * 0.005));
    idle = 0; if (!running) { yaw = yawUser; pitch = pitchUser; render(0); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  inFlow.addEventListener('input', function () { calc('flow'); });
  inSteam.addEventListener('input', function () { calc('steam'); });
  inFoul.addEventListener('input', function () { calc('foul'); });
  $('hx3d-reset').addEventListener('click', function () { inFlow.value = 6250; inSteam.value = 3; inFoul.value = 0; calc(); });
  var btnNames = $('hx3d-names');
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
  window.addEventListener('resize', function () { resize(); if (!running) render(0); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measured = false; if (!running) render(0); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
