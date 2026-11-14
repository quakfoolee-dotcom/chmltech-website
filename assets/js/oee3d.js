/* OEE series: OEE as a 3D volume. No library: a small perspective renderer on a 2D canvas.
   The cube is scheduled time at ideal speed with no rejects. Width = availability, depth = performance,
   height = quality. Downtime, speed loss and quality loss each cut a slab off it; what remains is OEE.
   Follows the article's sliders (p1-down, p1-rate, p1-rej) and the same fixed figures as oee.js. */
(function () {
  'use strict';
  var fig = document.getElementById('oee3d');
  if (!fig) return;
  var cv = fig.querySelector('canvas'), ctx = cv.getContext && cv.getContext('2d');
  var $ = function (id) { return document.getElementById(id); };
  var inDown = $('p1-down'), inRate = $('p1-rate'), inRej = $('p1-rej');
  var TOTAL = 17, PLAN = 2, IDEAL = 2000, SCHED = TOTAL - PLAN, TAU = Math.PI * 2;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var tA = 0.85, tP = 0.9, tQ = 0.96, A = tA, Pf = tP, Q = tQ;

  function pct(x) { return (x * 100).toFixed(1) + '%'; }
  function hrs(x) { return (x * SCHED).toFixed(2) + ' h'; }
  function put(id, t) { var e = $(id); if (e) e.textContent = t; }
  function read() {
    if (inDown && inRate && inRej) {
      tA = (SCHED - parseFloat(inDown.value)) / SCHED; tP = parseFloat(inRate.value) / IDEAL; tQ = 1 - parseFloat(inRej.value) / 100;
    }
    var o = tA * tP * tQ, d = 1 - tA, s = tA * (1 - tP), q = tA * tP * (1 - tQ);
    put('oee3d-O', pct(o)); put('oee3d-A', pct(tA)); put('oee3d-P', pct(tP)); put('oee3d-Q', pct(tQ));
    put('oee3d-g', pct(o)); put('oee3d-gh', hrs(o)); put('oee3d-d', pct(d)); put('oee3d-dh', hrs(d));
    put('oee3d-s', pct(s)); put('oee3d-sh', hrs(s)); put('oee3d-q', pct(q)); put('oee3d-qh', hrs(q));
    if (reduce || !running) { A = tA; Pf = tP; Q = tQ; if (ctx) draw(); }
  }
  [inDown, inRate, inRej].forEach(function (i) { if (i) i.addEventListener('input', read); });
  var running = false;
  if (!ctx) { fig.querySelector('.oee3d-stage').style.display = 'none'; read(); return; }

  /* ----- view ----- */
  var W = 0, H = 0, dpr = 1, R = 80, cx = 0, cyc = 0, CAM = 8.5, clock = 0;
  var yawUser = 0.6, tiltUser = 0.46, yaw = yawUser, tilt = tiltUser, sway = 1, idle = 99;
  var cyw = 1, syw = 0, ct = 1, st = 0;
  function resize() {
    var rc = cv.getBoundingClientRect();
    W = rc.width; H = rc.height; dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    var narrow = W < 360;
    R = Math.min(W * (narrow ? 0.17 : 0.2), H * 0.235); cx = W * (narrow ? 0.64 : 0.56); cyc = H * 0.47;
  }
  function P(x, y, z) {
    var x1 = x * cyw + z * syw, z1 = -x * syw + z * cyw, y2 = y * ct - z1 * st, z2 = y * st + z1 * ct, k = CAM / (CAM - z2);
    return [cx + x1 * R * k, cyc - y2 * R * k, z2, k];
  }
  /* model space: a (availability) runs along +x, q (quality) along +y, p (performance) runs back from the front face */
  function M(a, q, p) { return P(-1 + 2 * a, -1 + 2 * q, 1 - 2 * p); }
  function poly(pts, fill, stroke, lw) {
    ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
    for (var i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
    ctx.closePath();
    if (fill) { ctx.fillStyle = fill; ctx.fill(); }
    if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = lw || 1; ctx.stroke(); }
  }
  /* corner index = ix + 2*iy + 4*iz in x,y,z; faces wound outward, visible when screen area is negative */
  var FACES = [[6, 7, 3, 2, 't'], [0, 1, 5, 4, 't'], [5, 1, 3, 7, 'x'], [0, 4, 6, 2, 'x'], [4, 5, 7, 6, 'z'], [1, 0, 2, 3, 'z']];
  function box(a0, a1, q0, q1, p0, p1, s) {
    if (a1 - a0 < 0.003 || q1 - q0 < 0.003 || p1 - p0 < 0.003) return;
    var x0 = -1 + 2 * a0, x1 = -1 + 2 * a1, y0 = -1 + 2 * q0, y1 = -1 + 2 * q1, z0 = 1 - 2 * p1, z1 = 1 - 2 * p0, c = [], i;
    for (i = 0; i < 8; i++) c.push(P(i & 1 ? x1 : x0, i & 2 ? y1 : y0, i & 4 ? z1 : z0));
    for (var pass = 0; pass < 2; pass++) for (i = 0; i < 6; i++) {
      var f = FACES[i], q = [c[f[0]], c[f[1]], c[f[2]], c[f[3]]], ar = 0;
      for (var k = 0; k < 4; k++) { var p = q[k], n = q[(k + 1) % 4]; ar += p[0] * n[1] - n[0] * p[1]; }
      var facing = ar < 0;
      if (pass === 0 && !facing && s.back) poly(q, s.back, s.line, 0.8);       /* far faces of a see-through slab */
      if (pass === 1 && facing) poly(q, f[4] === 't' ? s.top : f[4] === 'x' ? s.sx : s.sz, s.line, s.lw);
    }
  }
  var GOOD = { top: 'rgba(84,176,238,.97)', sx: 'rgba(13,104,160,.97)', sz: 'rgba(26,132,198,.97)', line: 'rgba(214,240,255,.95)', lw: 1.3 };
  function slab(r, g, b) {
    var c = r + ',' + g + ',' + b;
    return { top: 'rgba(' + c + ',.30)', sx: 'rgba(' + c + ',.20)', sz: 'rgba(' + c + ',.24)', back: 'rgba(' + c + ',.10)', line: 'rgba(' + c + ',.9)', lw: 1.1 };
  }
  var DOWN = slab(232, 160, 60), SPEED = slab(140, 140, 245), QUAL = slab(238, 110, 110);

  function pill(x, y, name, val) {
    ctx.font = '600 12.5px "Space Grotesk", system-ui, sans-serif';
    var w1 = ctx.measureText(name + ' ').width, w2 = ctx.measureText(val).width, w = w1 + w2 + 22, h = 26;
    x = Math.max(w / 2 + 6, Math.min(W - w / 2 - 6, x)); y = Math.max(h / 2 + 6, Math.min(H - h / 2 - 6, y));
    var l = x - w / 2, t = y - h / 2, r = h / 2;
    ctx.beginPath(); ctx.moveTo(l + r, t); ctx.lineTo(l + w - r, t); ctx.arc(l + w - r, y, r, -Math.PI / 2, Math.PI / 2);
    ctx.lineTo(l + r, t + h); ctx.arc(l + r, y, r, Math.PI / 2, Math.PI * 1.5); ctx.closePath();
    ctx.fillStyle = 'rgba(6,24,51,.9)'; ctx.fill(); ctx.strokeStyle = 'rgba(255,255,255,.22)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    ctx.fillStyle = '#C4D4E8'; ctx.fillText(name, l + 11, y + 0.5);
    ctx.fillStyle = '#fff'; ctx.fillText(val, l + 11 + w1, y + 0.5);
  }
  var pills = [], bb = [0, 0, 0];   /* bb: left, right and bottom of the cube on screen */
  function dim(p0, p1, name, val, zone) { /* a measured edge of the box; its label sits outside the cube, joined by a leader */
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(p0[0], p0[1]); ctx.lineTo(p1[0], p1[1]); ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(p1[0], p1[1], 3.2, 0, TAU); ctx.fill();
    var mxp = (p0[0] + p1[0]) / 2, myp = (p0[1] + p1[1]) / 2;
    ctx.font = '600 12.5px "Space Grotesk", system-ui, sans-serif';
    var w = ctx.measureText(name + ' ' + val).width + 22;
    pills.push(zone === 'left' ? { x: bb[0] - 14 - w / 2, y: myp, w: w, name: name, val: val, ax: mxp, ay: myp, zone: zone }
                               : { x: mxp, y: bb[2] + 26, w: w, name: name, val: val, ax: mxp, ay: myp, zone: zone });
  }
  function flushPills() {
    var i, a, b, below = [];
    for (i = 0; i < pills.length; i++) { a = pills[i]; a.x = Math.max(a.w / 2 + 6, Math.min(W - a.w / 2 - 6, a.x)); a.y = Math.max(19, Math.min(H - 19, a.y)); if (a.zone !== 'left') below.push(a); }
    if (below.length === 2) {   /* the two labels under the cube sit side by side */
      a = below[0].x <= below[1].x ? below[0] : below[1]; b = a === below[0] ? below[1] : below[0];
      var need = (a.w + b.w) / 2 + 8 - (b.x - a.x);
      if (need > 0) { a.x -= need / 2; b.x += need / 2;
        if (a.x < a.w / 2 + 6) { b.x += a.w / 2 + 6 - a.x; a.x = a.w / 2 + 6; }
        if (b.x > W - b.w / 2 - 6) { a.x -= b.x - (W - b.w / 2 - 6); b.x = W - b.w / 2 - 6; } }
    }
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 1;
    for (i = 0; i < pills.length; i++) { a = pills[i]; ctx.beginPath(); ctx.moveTo(a.ax, a.ay); ctx.lineTo(a.x, a.y); ctx.stroke(); }
    for (i = 0; i < pills.length; i++) pill(pills[i].x, pills[i].y, pills[i].name, pills[i].val);
    pills.length = 0;
  }

  function draw() {
    cyw = Math.cos(yaw); syw = Math.sin(yaw); ct = Math.cos(tilt); st = Math.sin(tilt);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
    var g = ctx.createRadialGradient(cx, cyc, R * 0.4, cx, cyc, R * 3.2);
    g.addColorStop(0, 'rgba(22,104,170,.30)'); g.addColorStop(1, 'rgba(22,104,170,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.lineJoin = 'round';

    /* direction toward the camera in model axes decides the back-to-front order of the four volumes */
    var dx = -syw * ct, dy = st, dz = cyw * ct;
    function column() {            /* a < A and p < P: the good box with the quality slab on top */
      if (dy > 0) { box(0, A, 0, Q, 0, Pf, GOOD); box(0, A, Q, 1, 0, Pf, QUAL); }
      else { box(0, A, Q, 1, 0, Pf, QUAL); box(0, A, 0, Q, 0, Pf, GOOD); }
    }
    function left() {              /* a < A: the column in front, the speed slab behind it */
      if (dz > 0) { box(0, A, 0, 1, Pf, 1, SPEED); column(); }
      else { column(); box(0, A, 0, 1, Pf, 1, SPEED); }
    }
    if (dx > 0) { left(); box(A, 1, 0, 1, 0, 1, DOWN); }
    else { box(A, 1, 0, 1, 0, 1, DOWN); left(); }

    /* outline of the full cube: 100% x 100% x 100% */
    var c = [], i;
    for (i = 0; i < 8; i++) c.push(P(i & 1 ? 1 : -1, i & 2 ? 1 : -1, i & 4 ? 1 : -1));
    var E = [[0, 1], [1, 3], [3, 2], [2, 0], [4, 5], [5, 7], [7, 6], [6, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
    ctx.strokeStyle = 'rgba(255,255,255,.34)'; ctx.lineWidth = 1; ctx.setLineDash([4, 4]);
    for (i = 0; i < 12; i++) { ctx.beginPath(); ctx.moveTo(c[E[i][0]][0], c[E[i][0]][1]); ctx.lineTo(c[E[i][1]][0], c[E[i][1]][1]); ctx.stroke(); }
    ctx.setLineDash([]);

    /* the three measured edges meet at the box's front lower corner */
    bb[0] = 1e9; bb[1] = -1e9; bb[2] = -1e9;
    for (i = 0; i < 8; i++) { bb[0] = Math.min(bb[0], c[i][0]); bb[1] = Math.max(bb[1], c[i][0]); bb[2] = Math.max(bb[2], c[i][1]); }
    var o = M(0, 0, 0);
    dim(o, M(A, 0, 0), 'Availability', pct(A), 'below');
    dim(o, M(0, 0, Pf), 'Performance', pct(Pf), 'below');
    dim(o, M(0, Q, 0), 'Quality', pct(Q), 'left');
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(o[0], o[1], 3.2, 0, TAU); ctx.fill();
    flushPills();
  }

  /* ----- drag to turn ----- */
  var drag = null;
  cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, yaw: yawUser, tilt: tiltUser }; cv.classList.add('is-drag'); try { cv.setPointerCapture(e.pointerId); } catch (err) {} });
  cv.addEventListener('pointermove', function (e) {
    if (!drag) return;
    yawUser = drag.yaw + (e.clientX - drag.x) * 0.009;
    tiltUser = Math.max(0.1, Math.min(1.05, drag.tilt + (e.clientY - drag.y) * 0.006));
    idle = 0;
    if (!running) { yaw = yawUser; tilt = tiltUser; draw(); }
  });
  function endDrag() { drag = null; cv.classList.remove('is-drag'); }
  cv.addEventListener('pointerup', endDrag); cv.addEventListener('pointercancel', endDrag);

  var last = 0, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.max(0, Math.min(0.05, (t - last) / 1000 || 0)); last = t; clock += dt; idle += dt;
    var e = 1 - Math.exp(-dt * 9);
    A += (tA - A) * e; Pf += (tP - Pf) * e; Q += (tQ - Q) * e;
    sway += ((idle > 4 ? 1 : 0) - sway) * (1 - Math.exp(-dt * 2));
    var e2 = 1 - Math.exp(-dt * 10);
    yaw += (yawUser + 0.16 * Math.sin(clock * 0.3) * sway - yaw) * e2;
    tilt += (tiltUser - tilt) * e2;
    draw();
    requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  resize(); read(); A = tA; Pf = tP; Q = tQ; draw();
  window.addEventListener('resize', function () { resize(); if (!running) draw(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (!running) draw(); });
  if (!reduce) {
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(cv);
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
