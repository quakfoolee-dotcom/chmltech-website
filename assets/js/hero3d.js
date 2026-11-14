/* Chmltech homepage 3D hero (V5.3). No library: a small perspective renderer on a 2D canvas.
   Scene: a wireframe "operations core" with data pulses, and an orbit carrying the five cycle stages. */
(function () {
  'use strict';
  var stage = document.getElementById('orbit');
  if (!stage) return;
  var cv = stage.querySelector('canvas');
  var ctx = cv.getContext && cv.getContext('2d');
  var labels = Array.prototype.slice.call(stage.querySelectorAll('.orbit-label'));
  var STAGES = [
    ['Discover', 'Goals, pain points, data, systems'],
    ['Map', 'Current-state process and information flows'],
    ['Prioritize', 'Quick wins, automation, AI use cases'],
    ['Implement', 'Systems, workflows, KPIs, training'],
    ['Measure', 'Dashboards and continuous improvement']
  ];
  var elCount = document.getElementById('orbit-count'), elName = document.getElementById('orbit-name'),
      elDesc = document.getElementById('orbit-desc'),
      bars = Array.prototype.slice.call(document.querySelectorAll('#orbit-readout .orbit-bar i'));
  var N = 5, TAU = Math.PI * 2, DWELL = 3.6;
  var step = 0, sinceStep = 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setActive() {
    var a = ((step % N) + N) % N;
    labels.forEach(function (l, i) { l.classList.toggle('is-active', i === a); l.setAttribute('aria-pressed', i === a ? 'true' : 'false'); });
    bars.forEach(function (b, i) { b.classList.toggle('on', i <= a); });
    if (elCount) elCount.textContent = 'Stage 0' + (a + 1) + ' of 05';
    if (elName) elName.textContent = STAGES[a][0];
    if (elDesc) elDesc.textContent = STAGES[a][1];
    sizes = null;
  }
  labels.forEach(function (l) {
    l.addEventListener('click', function () {
      var want = +l.getAttribute('data-i'), cur = ((step % N) + N) % N;
      step += (want - cur + N) % N; sinceStep = 0; setActive();
      if (reduce) { ringA = -step * TAU / N; draw(0); }
    });
  });
  setActive();
  if (!ctx) { stage.style.display = 'none'; return; }
  stage.classList.add('is-live');

  /* ----- geometry ----- */
  function norm(p) { var l = Math.sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2]); return [p[0] / l, p[1] / l, p[2] / l]; }
  var V, E, NB;
  (function ico(sub) {
    var t = (1 + Math.sqrt(5)) / 2;
    V = [[-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0], [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t], [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1]].map(norm);
    var F = [[0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11], [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
             [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9], [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]];
    for (var s = 0; s < sub; s++) {
      var cache = {}, nf = [];
      var mid = function (a, b) {
        var k = a < b ? a + '_' + b : b + '_' + a;
        if (cache[k] === undefined) { cache[k] = V.length; V.push(norm([V[a][0] + V[b][0], V[a][1] + V[b][1], V[a][2] + V[b][2]])); }
        return cache[k];
      };
      F.forEach(function (f) {
        var a = mid(f[0], f[1]), b = mid(f[1], f[2]), c = mid(f[2], f[0]);
        nf.push([f[0], a, c], [f[1], b, a], [f[2], c, b], [a, b, c]);
      });
      F = nf;
    }
    var seen = {}; E = []; NB = V.map(function () { return []; });
    F.forEach(function (f) {
      for (var i = 0; i < 3; i++) {
        var a = f[i], b = f[(i + 1) % 3], k = a < b ? a + '_' + b : b + '_' + a;
        if (!seen[k]) { seen[k] = 1; E.push([a, b]); NB[a].push(b); NB[b].push(a); }
      }
    });
  })(2);

  var rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return s / 2147483647; }; })(20261113);
  var dust = [];
  for (var i = 0; i < 150; i++) {
    var d = norm([rnd() * 2 - 1, (rnd() * 2 - 1) * 0.7, rnd() * 2 - 1]), r = 2.3 + rnd() * 1.5;
    dust.push([d[0] * r, d[1] * r, d[2] * r, 0.6 + rnd() * 0.9, 0.12 + rnd() * 0.38]);
  }
  var pulses = [];
  for (i = 0; i < 16; i++) {
    var a0 = Math.floor(rnd() * V.length);
    pulses.push({ a: a0, b: NB[a0][0], t: rnd(), v: 0.7 + rnd() * 0.9 });
  }

  /* ----- view ----- */
  var W = 0, H = 0, SW = 0, SH = 0, dpr = 1, R = 100, CAM = 6.2, sizes = null;
  var spin = 0.6, ringA = 0, dustA = 0, tiltX = 0.4, tiltY = 0, mx = 0, my = 0, clock = 0, intro = reduce ? 1 : 0;
  var RING = 1.62, RING_ROLL = -0.2;

  function resize() {
    var rc = stage.getBoundingClientRect();
    SW = rc.width; SH = rc.height;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = SW * 1.4; H = SH * 1.5;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    R = SW * 0.215; sizes = null; lpos = [];
  }
  /* rotate about Y by ry, roll about Z by rz, tilt about X by rx; then perspective. Returns [x, y, depth z, scale] in canvas px */
  var sx = 0, cx = 1, cyaw = 1, syaw = 0;
  function proj(x, y, z, ry, rz, out) {
    var c = Math.cos(ry), s = Math.sin(ry), x1 = x * c + z * s, z1 = -x * s + z * c, y1 = y;
    if (rz) { var cz = Math.cos(rz), sz = Math.sin(rz), xr = x1 * cz - y1 * sz; y1 = x1 * sz + y1 * cz; x1 = xr; }
    var x2 = x1 * cyaw + z1 * syaw, z2 = -x1 * syaw + z1 * cyaw;
    var y3 = y1 * cx - z2 * sx, z3 = y1 * sx + z2 * cx;
    var k = CAM / (CAM - z3);
    out[0] = W / 2 + x2 * R * k; out[1] = H / 2 - y3 * R * k; out[2] = z3; out[3] = k;
    return out;
  }
  var P = V.map(function () { return [0, 0, 0, 1]; }), tmp = [0, 0, 0, 1], tmp2 = [0, 0, 0, 1];
  var lpos = [];
  var BLUE = '120,200,245', GREEN = '141,198,63';

  function ringArc(radius, roll, from, to, front, alpha, width) {
    var seg = 120;
    ctx.lineWidth = width;
    for (var i = 0; i < seg; i++) {
      var a = from + (to - from) * i / seg, b = from + (to - from) * (i + 1) / seg, m = (a + b) / 2;
      proj(Math.sin(m) * radius, 0, Math.cos(m) * radius, 0, roll, tmp);
      if ((tmp[2] >= 0) !== front) continue;
      var al = alpha * (0.35 + 0.65 * (tmp[2] / radius + 1) / 2);
      proj(Math.sin(a) * radius, 0, Math.cos(a) * radius, 0, roll, tmp);
      proj(Math.sin(b) * radius, 0, Math.cos(b) * radius, 0, roll, tmp2);
      ctx.strokeStyle = 'rgba(' + BLUE + ',' + al.toFixed(3) + ')';
      ctx.beginPath(); ctx.moveTo(tmp[0], tmp[1]); ctx.lineTo(tmp2[0], tmp2[1]); ctx.stroke();
    }
  }

  function draw(dt) {
    clock += dt;
    var active = ((step % N) + N) % N;
    cx = Math.cos(tiltX); sx = Math.sin(tiltX); cyaw = Math.cos(tiltY); syaw = Math.sin(tiltY);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    var ease = 1 - Math.pow(1 - intro, 3);
    ctx.globalAlpha = 0.4 + 0.6 * ease;
    var keepR = R; R = R * (0.93 + 0.07 * ease);
    ctx.globalCompositeOperation = 'lighter';

    /* dust */
    for (var i = 0; i < dust.length; i++) {
      var d = dust[i]; proj(d[0], d[1], d[2], dustA, 0, tmp);
      ctx.fillStyle = 'rgba(' + BLUE + ',' + (d[4] * (0.5 + 0.5 * (tmp[2] / 3.8 + 1) / 2)).toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(tmp[0], tmp[1], d[3] * tmp[3], 0, TAU); ctx.fill();
    }
    /* far rings */
    ringArc(2.12, 0.42, 0, TAU, false, 0.16, 1);
    ringArc(RING, RING_ROLL, 0, TAU, false, 0.5, 1.2);
    stageNodes(true);

    /* core volume */
    var cxp = W / 2, cyp = H / 2, g = ctx.createRadialGradient(cxp - R * 0.35, cyp - R * 0.4, R * 0.1, cxp, cyp, R * 1.25);
    g.addColorStop(0, 'rgba(40,150,220,.34)'); g.addColorStop(0.6, 'rgba(14,84,150,.16)'); g.addColorStop(1, 'rgba(10,60,120,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cxp, cyp, R * 1.25, 0, TAU); ctx.fill();

    /* core lattice */
    for (i = 0; i < V.length; i++) proj(V[i][0], V[i][1], V[i][2], spin, 0, P[i]);
    ctx.lineWidth = 1;
    for (i = 0; i < E.length; i++) {
      var a = P[E[i][0]], b = P[E[i][1]], f = ((a[2] + b[2]) / 2 + 1) / 2;
      ctx.strokeStyle = 'rgba(' + BLUE + ',' + (0.06 + 0.5 * f * f).toFixed(3) + ')';
      ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke();
    }
    for (i = 0; i < V.length; i++) {
      var p = P[i], fz = (p[2] + 1) / 2;
      ctx.fillStyle = 'rgba(190,232,255,' + (0.1 + 0.7 * fz * fz).toFixed(3) + ')';
      ctx.beginPath(); ctx.arc(p[0], p[1], (0.8 + 1.1 * fz) * p[3], 0, TAU); ctx.fill();
    }
    /* scan line: a latitude circle sweeping the core */
    var h = Math.sin(clock * 0.45) * 0.86, rr = Math.sqrt(1 - h * h) * 1.012;
    ctx.lineWidth = 1.4;
    for (i = 0; i < 64; i++) {
      var a1 = TAU * i / 64, a2 = TAU * (i + 1) / 64;
      proj(Math.sin(a1) * rr, h, Math.cos(a1) * rr, 0, 0, tmp); proj(Math.sin(a2) * rr, h, Math.cos(a2) * rr, 0, 0, tmp2);
      var fs = (tmp[2] + 1) / 2;
      ctx.strokeStyle = 'rgba(' + GREEN + ',' + (0.05 + 0.6 * fs * fs).toFixed(3) + ')';
      ctx.beginPath(); ctx.moveTo(tmp[0], tmp[1]); ctx.lineTo(tmp2[0], tmp2[1]); ctx.stroke();
    }
    /* data pulses along lattice edges */
    for (i = 0; i < pulses.length; i++) {
      var q = pulses[i], pa = P[q.a], pb = P[q.b], x = pa[0] + (pb[0] - pa[0]) * q.t, y = pa[1] + (pb[1] - pa[1]) * q.t,
          z = pa[2] + (pb[2] - pa[2]) * q.t, fp = (z + 1) / 2, al = 0.15 + 0.85 * fp * fp;
      ctx.fillStyle = 'rgba(' + GREEN + ',' + (al * 0.22).toFixed(3) + ')'; ctx.beginPath(); ctx.arc(x, y, 6.5, 0, TAU); ctx.fill();
      ctx.fillStyle = 'rgba(200,240,140,' + al.toFixed(3) + ')'; ctx.beginPath(); ctx.arc(x, y, 2.1, 0, TAU); ctx.fill();
    }

    /* near rings */
    ringArc(2.12, 0.42, 0, TAU, true, 0.2, 1);
    ringArc(RING, RING_ROLL, 0, TAU, true, 0.62, 1.3);

    /* front stage nodes + labels (nodes on the far side were drawn before the core, so the core covers them) */
    stageNodes(false);
    R = keepR; ctx.globalAlpha = 1;

    function stageNodes(backPass) {
    ctx.globalCompositeOperation = 'source-over';
    if (!sizes) sizes = labels.map(function (l) { return [l.offsetWidth, l.offsetHeight]; });
    var ox = (W - SW) / 2, oy = (H - SH) / 2;
    for (var i = 0; i < N; i++) {
      var ang = ringA + i * TAU / N;
      proj(Math.sin(ang) * RING, 0, Math.cos(ang) * RING, 0, RING_ROLL, tmp);
      var nx = tmp[0], ny = tmp[1], front = (tmp[2] / RING + 1) / 2, on = i === active, k = tmp[3];
      var isBack = !on && tmp[2] < 0;
      if (isBack !== backPass) continue;
      if (on) {
        var halo = ctx.createRadialGradient(nx, ny, 0, nx, ny, 30 * k);
        halo.addColorStop(0, 'rgba(' + GREEN + ',.5)'); halo.addColorStop(1, 'rgba(' + GREEN + ',0)');
        ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(nx, ny, 30 * k, 0, TAU); ctx.fill();
        ctx.fillStyle = 'rgb(' + GREEN + ')'; ctx.beginPath(); ctx.arc(nx, ny, 6.5 * k, 0, TAU); ctx.fill();
        ctx.strokeStyle = 'rgba(' + GREEN + ',.3)'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.arc(nx, ny, 13 * k, 0, TAU); ctx.stroke();
        if (!reduce) { /* dwell timer: the ring fills, then the cycle advances */
          ctx.strokeStyle = 'rgb(' + GREEN + ')'; ctx.lineWidth = 2;
          ctx.beginPath(); ctx.arc(nx, ny, 13 * k, -Math.PI / 2, -Math.PI / 2 + TAU * Math.min(1, sinceStep / DWELL)); ctx.stroke();
        }
      } else {
        ctx.fillStyle = '#0B2A5A'; ctx.beginPath(); ctx.arc(nx, ny, 5 * k, 0, TAU); ctx.fill();
        ctx.strokeStyle = 'rgba(205,232,250,' + (0.4 + 0.6 * front).toFixed(2) + ')'; ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.arc(nx, ny, 5 * k, 0, TAU); ctx.stroke();
      }
      /* label is centred beneath its node; on the far side it sits above the node and goes behind the core */
      var sz = sizes[i];
      var lx = Math.min(Math.max(nx - ox, sz[0] / 2 - 18), SW + 18 - sz[0] / 2);
      var ly = isBack ? ny - oy - 11 * k - sz[1] / 2 - 5 : ny - oy + (on ? 19 : 11) * k + sz[1] / 2 + 5;
      if (labels[i]._back !== isBack) { labels[i]._back = isBack; labels[i].classList.toggle('is-back', isBack); }
      var lp = lpos[i];
      if (!lp || !dt) lp = lpos[i] = [lx, ly];
      else { var e = Math.min(1, dt * 9); lp[0] += (lx - lp[0]) * e; lp[1] += (ly - lp[1]) * e; }
      labels[i].style.transform = 'translate(' + lp[0].toFixed(1) + 'px,' + lp[1].toFixed(1) + 'px) translate(-50%,-50%)';
      labels[i].style.opacity = on ? 1 : (0.78 + 0.22 * front).toFixed(2);
    }
    ctx.globalCompositeOperation = 'lighter';
    }
  }

  var last = 0, running = false, visible = true;
  function frame(t) {
    if (!running) return;
    var dt = Math.min(0.05, (t - last) / 1000 || 0); last = t;
    intro = Math.min(1, intro + dt / 1.3);
    spin += dt * 0.16; dustA -= dt * 0.025;
    sinceStep += dt;
    if (sinceStep >= DWELL) { sinceStep = 0; step++; setActive(); }
    var target = -step * TAU / N;
    ringA += (target - ringA) * (1 - Math.exp(-dt * 2.4));
    tiltX += (0.4 - my * 0.1 - tiltX) * (1 - Math.exp(-dt * 3));
    tiltY += (mx * 0.16 - tiltY) * (1 - Math.exp(-dt * 3));
    for (var i = 0; i < pulses.length; i++) {
      var q = pulses[i]; q.t += dt * q.v;
      if (q.t >= 1) { var from = q.a; q.a = q.b; var nb = NB[q.a], pick = nb[Math.floor(Math.random() * nb.length)];
        if (pick === from) pick = nb[(nb.indexOf(pick) + 1) % nb.length]; q.b = pick; q.t = 0; }
    }
    draw(dt);
    requestAnimationFrame(frame);
  }
  function setRun(on) {
    if (reduce) return;
    if (on && !running) { running = true; last = performance.now(); requestAnimationFrame(frame); }
    else if (!on) running = false;
  }
  resize(); draw(0);
  window.addEventListener('resize', function () { resize(); if (!running) draw(0); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { sizes = null; if (!running) draw(0); });
  if (!reduce) {
    var hero = document.getElementById('hero') || stage;
    hero.addEventListener('pointermove', function (e) {
      var rc = hero.getBoundingClientRect();
      mx = ((e.clientX - rc.left) / rc.width) * 2 - 1; my = ((e.clientY - rc.top) / rc.height) * 2 - 1;
    });
    hero.addEventListener('pointerleave', function () { mx = 0; my = 0; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; setRun(visible && !document.hidden); }).observe(stage);
    }
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    setRun(true);
  }
})();
