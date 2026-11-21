/* Warehouse Layout Lab, simulation engine (V1, warehouse layout series Part 1).
   One 8-hour shift (07:00 to 15:00) in the 72 x 52 m (about 40,300 sq ft) building of the warehouse operations
   series, for two layouts of the same racks: "asis" (rows along the building, aisles closed at the east wall, random
   slotting, shared doors, overflow staging in the main aisle, packing at the far end from the doors) and "redesign"
   (rows across the building with front and back cross-aisles, fast movers in the front bays next to packing, receiving
   doors on the left and shipping doors on the right in a U-flow, staging lanes kept out of the aisles).
   Pickers, forklifts, a pallet jack and trucks move on a 1 m grid (8-way paths). An agent gives way when another one
   is within one metre of the cell it is about to enter (forklifts give way to people standing still; otherwise the
   higher-priority agent keeps going), and squeezes past after a few seconds. Every number is the result of one run with
   a fixed seed, so the browser figure and the article quote the same values.
   Works in the browser (window.WLEngine) and in Node (module.exports). No libraries. */
(function (root) {
  'use strict';
  var BX = 72, BZ = 52, N = BX * BZ, YARD = 14;          // building cells (1 m); yard strip south of the dock wall
  var P = {
    vPick: 0.9, vFork: 2.0, vJack: 1.3, vTruck: 3.0,      // m/s (picker with a cart, as in Part 2)
    tPick: 20, tSetup: 45, tDrop: 30,                     // s a case pick; s to get list and cart; s to drop the totes at packing
    tLoad: 25, tPut: 60, tJack: 20,                       // s forklift takes a pallet from staging; puts it into a rack; jack pick-up/set-down
    tUnload: 150, tShipLoad: 60,                          // s to unload one inbound pallet into staging; to load one outbound pallet
    shift: 8 * 3600, dt: 0.5, start: 7,                   // s; s a step; 07:00
    lines: 3, ordersPallet: 20, backlog: 30, cutoff: 7 * 3600,   // orders waiting at 07:00; new orders stop at 14:00
    wage: 40, days: 250, detention: 65, freeMin: 120,     // $ an hour loaded; days a year; $ an hour after 2 h on site (Part 3)
    near: 0.95, maxWait: 6                                // m: give-way distance; s before squeezing past
  };
  var SKUS = 780;

  /* ---------- random numbers ---------- */
  function rng(seed) {
    var a = seed >>> 0;
    return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  }
  function poisson(r, m) { var L = Math.exp(-m), k = 0, p = 1; do { k++; p *= r(); } while (p > L); return k - 1; }

  /* ---------- SKU velocities: top 20% of SKUs carry `share` of the picks ---------- */
  function velocities(share) {
    function top(a) { var s = 0, t = 0, i, w; for (i = 0; i < SKUS; i++) { w = 1 / Math.pow(i + 1, a); s += w; if (i < SKUS * 0.2) t += w; } return t / s; }
    var lo = 0, hi = 3, k, a;
    for (k = 0; k < 50; k++) { a = (lo + hi) / 2; if (top(a) < share) lo = a; else hi = a; }
    var w = [], s = 0, i;
    for (i = 0; i < SKUS; i++) { w.push(1 / Math.pow(i + 1, a)); s += w[i]; }
    var cum = [], c = 0, cls = [];
    for (i = 0; i < SKUS; i++) { w[i] /= s; c += w[i]; cum.push(c); cls.push(c - w[i] < 0.8 - 1e-9 ? 'A' : c - w[i] < 0.95 - 1e-9 ? 'B' : 'C'); }
    return { w: w, cum: cum, cls: cls, alpha: a };
  }
  function pickSku(V, r) { var x = r(), lo = 0, hi = SKUS - 1; while (lo < hi) { var m = (lo + hi) >> 1; if (V.cum[m] < x) lo = m + 1; else hi = m; } return lo; }

  /* ---------- layouts ---------- */
  function cell(x, z) { return z * BX + x; }
  function rect(L, x0, z0, x1, z1) { for (var z = z0; z <= z1; z++) for (var x = x0; x <= x1; x++) L.blocked[cell(x, z)] = 1; }
  function spots(xs, zs) { var o = []; xs.forEach(function (x) { zs.forEach(function (z) { o.push({ x: x, z: z, c: cell(x, z), busy: null }); }); }); return o; }
  function range(a, b, s) { var o = []; for (var v = a; v <= b; v += s) o.push(v); return o; }

  function makeLayout(kind) {
    var L = { kind: kind, blocked: new Uint8Array(N), racks: [], faces: [], doors: [], recv: [], ship: [], drops: [], areas: [], faults: [], spill: [] };
    var x, z;
    for (x = 0; x < BX; x++) { L.blocked[cell(x, 0)] = 1; L.blocked[cell(x, BZ - 1)] = 1; }
    for (z = 0; z < BZ; z++) { L.blocked[cell(0, z)] = 1; L.blocked[cell(BX - 1, z)] = 1; }
    function row(x0, z0, x1, z1, dir) { L.racks.push({ x0: x0, z0: z0, x1: x1, z1: z1, dir: dir }); rect(L, x0, z0, x1, z1); }
    // a dock door on the south (S), west (W) or east (E) wall; pos is x for S, z for W and E. c: the floor cell just inside
    function door(pos, use, wall) {
      wall = wall || 'S';
      var d = { wall: wall, pos: pos, use: use, truck: null };
      if (wall === 'S') { d.x = pos; d.z = BZ - 1; d.c = cell(pos, BZ - 2); L.blocked[cell(pos, BZ - 1)] = 0; }
      else if (wall === 'W') { d.x = 0; d.z = pos; d.c = cell(1, pos); L.blocked[cell(0, pos)] = 0; }
      else { d.x = BX - 1; d.z = pos; d.c = cell(BX - 2, pos); L.blocked[cell(BX - 1, pos)] = 0; }
      L.doors.push(d);
    }
    function homeCol(x, z0, z1) { L.homeCol = [x, z0, z1]; }
    if (kind === 'asis') {
      L.name = 'As-is layout';
      // rows along the building (x), from the west cross-aisle (x 1-5) to the east wall: aisles open at one end only
      var zr = [[1, 1], [5, 6], [10, 11], [15, 16], [20, 21], [25, 26], [30, 30]];
      zr.forEach(function (q) { row(6, q[0], 70, q[1], 'x'); });
      rect(L, 1, 1, 5, 1);                                                    // the wall row's end
      // overflow staging that lives in the main aisle (returns, dead stock, pallets waiting for space)
      for (x = 37; x <= 53; x++) { L.spill.push(cell(x, 34), cell(x, 35)); }
      rect(L, 37, 34, 53, 35);
      // packing at the west end
      rect(L, 2, 40, 11, 41); L.bench = [2, 40, 11, 41]; L.drops = [cell(4, 39), cell(7, 39), cell(10, 39)]; L.homeRows = [[2, 11, 39], [2, 11, 38]];
      L.packSpot = cell(7, 44);
      // five doors shared by receiving and shipping, one staging area for both
      [38, 43, 48, 53, 58].forEach(function (x) { door(x, 'both'); });
      L.recv = spots(range(36, 60, 2), [43, 45]); L.ship = L.recv;          // 26 spots, shared
      L.fork0 = [cell(31, 47), cell(31, 45)]; L.jack0 = cell(14, 46);
      L.areas = [
        { t: 'Pallet racks', x: 38, z: 16, k: 'rack' },
        { t: 'Packing', x: 6.5, z: 42.5, k: 'pack' },
        { t: 'Shared staging', x: 48, z: 47.5, k: 'stage' },
        { t: 'Main aisle', x: 22, z: 33.5, k: 'aisle' }
      ];
      L.faults = [
        { n: 1, x: 69.5, z: 23, t: 'Dead-end aisles', d: 'The rows run to the east wall, so every pick and every put-away goes into a 65 m aisle and back out the same end.' },
        { n: 2, x: 38, z: 8, t: 'Random slotting', d: 'Fast movers sit wherever there was a gap, so pickers and the forklift travel the full length of the aisles.' },
        { n: 3, x: 27, z: 38.5, t: 'Crossing flows', d: 'Forklifts from the doors and pickers from packing share the main aisle and the west entrance to every aisle.' },
        { n: 4, x: 45, z: 34.5, t: 'Staging in the main aisle', d: 'Overflow pallets narrow the main aisle where all traffic meets.' },
        { n: 5, x: 48, z: 56.5, t: 'Shared doors and staging', d: 'Receiving and shipping share the doors and one staging area. When the forklift falls behind, staging fills and unloading stops.' },
        { n: 6, x: 14, z: 42.5, t: 'Packing far from the doors', d: 'Every outbound pallet is pushed across the receiving area to reach a door.' }
      ];
    } else if (kind === 'redesign') {
      L.name = 'Redesigned layout'; L.short = 'U-shape';
      // rows across the building (z), aisles open to a back cross-aisle (z 1-3) and a front cross-aisle (z 34-37)
      var xr = [[1, 1]]; for (x = 5; x <= 65; x += 5) xr.push([x, x + 1]); xr.push([70, 70]);
      xr.forEach(function (q) { row(q[0], 4, q[1], 33, 'z'); });
      rect(L, 1, 1, 1, 3);
      rect(L, 40, 39, 57, 40); L.bench = [40, 39, 57, 40]; L.drops = [cell(42, 38), cell(48, 38), cell(54, 38)]; L.homeRows = [[40, 57, 38], [40, 57, 37]];
      L.packSpot = cell(49, 42);
      [8, 14, 20].forEach(function (x) { door(x, 'in'); });
      [56, 63].forEach(function (x) { door(x, 'out'); });
      L.recv = spots(range(4, 26, 2), [42, 44, 46]);                       // 36 spots in lanes in front of the receiving doors
      L.ship = spots(range(52, 68, 2), [44, 46]);                          // 18 spots in front of the shipping doors
      L.fork0 = [cell(29, 45), cell(29, 47)]; L.jack0 = cell(45, 46);
      L.areas = [
        { t: 'Pallet racks', x: 36, z: 19, k: 'rack' },
        { t: 'Packing', x: 48.5, z: 39.5, k: 'pack' },
        { t: 'Receiving staging', x: 15, z: 48.5, k: 'stage' },
        { t: 'Shipping staging', x: 60, z: 48.5, k: 'stage' },
        { t: 'Front cross-aisle', x: 30, z: 35.5, k: 'aisle' }
      ];
      L.faults = [
        { n: 1, x: 36, z: 2, t: 'Open at both ends', d: 'Shorter aisles joined by front and back cross-aisles: no dead ends.' },
        { n: 2, x: 58, z: 30, t: 'Fast movers up front', d: 'The busiest SKUs sit in the front bays closest to packing.' },
        { n: 3, x: 30, z: 40, t: 'U-flow', d: 'Receiving on the left, shipping on the right: forklifts and pickers mostly keep apart.' },
        { n: 4, x: 7, z: 36.5, t: 'Main aisle kept clear', d: 'Staging has its own lanes in the dock zone, out of the aisles.' },
        { n: 5, x: 59.5, z: 56.5, t: 'Separate doors', d: 'Three receiving and two shipping doors, each with its own staging lanes.' },
        { n: 6, x: 48.5, z: 42.5, t: 'Packing next to shipping', d: 'Outbound pallets travel under 10 m to their lane.' }
      ];
    }

    if (kind === 'redesign') L.flow = [
      { n: 1, x: 30, z: 40, t: 'One dock wall', d: 'Receiving and shipping share the south wall, so one yard, one gatehouse and one set of dock equipment serve both.' },
      { n: 2, x: 58, z: 30, t: 'Fast movers by the doors', d: 'The busiest SKUs sit in the front bays, close to packing and to receiving, so both their picks and their put-aways are short.' },
      { n: 3, x: 20, z: 2, t: 'Slow movers at the back', d: 'C items fill the far end of the aisles, where few trips go.' },
      { n: 4, x: 33, z: 47, t: 'In and out side by side', d: 'Receiving and shipping lanes sit next to each other: trucks and staging have to be kept apart by markings and door rules.' },
      { n: 5, x: 54, z: 0.6, t: 'Room to grow away from the dock', d: 'The building can be extended north without moving a door.' }
    ];
    if (kind === 'ucentre') {
      // model-only variant for Part 2's article: the U-shape with its receiving doors moved toward the middle of the wall
      L.name = 'U-shape, receiving doors moved to the middle'; L.short = 'U-shape (doors moved)';
      var xu = [[1, 1]]; for (x = 5; x <= 65; x += 5) xu.push([x, x + 1]); xu.push([70, 70]);
      xu.forEach(function (q) { row(q[0], 4, q[1], 33, 'z'); });
      rect(L, 1, 1, 1, 3);
      rect(L, 44, 39, 57, 40); L.bench = [44, 39, 57, 40]; L.drops = [cell(46, 38), cell(51, 38), cell(56, 38)]; L.homeRows = [[44, 57, 38], [44, 57, 37]];
      L.packSpot = cell(51, 42);
      [24, 30, 36].forEach(function (x) { door(x, 'in'); });
      [56, 63].forEach(function (x) { door(x, 'out'); });
      L.recv = spots(range(18, 40, 2), [42, 44, 46]);
      L.ship = spots(range(52, 68, 2), [44, 46]);
      L.fork0 = [cell(10, 45), cell(10, 47)]; L.jack0 = cell(46, 46);
      L.areas = []; L.flow = [];
    }
    if (kind === 'thru') {
      L.name = 'Straight-through layout'; L.short = 'Straight-through';
      // rows along the building (x 15-56) between a receiving zone on the west wall and a shipping zone on the east wall
      var zt = [[1, 1]]; for (z = 5; z <= 45; z += 5) zt.push([z, z + 1]); zt.push([50, 50]);
      zt.forEach(function (q) { row(15, q[0], 56, q[1], 'x'); });
      rect(L, 60, 14, 61, 37); L.bench = [60, 14, 61, 37]; L.drops = [cell(59, 18), cell(59, 26), cell(59, 34)]; homeCol(59, 15, 36);
      L.packSpot = cell(62, 26);
      [18, 24, 30].forEach(function (z) { door(z, 'in', 'W'); });
      [22, 30].forEach(function (z) { door(z, 'out', 'E'); });
      L.recv = spots([4, 6, 8], range(13, 35, 2));                          // 36 spots on the receiving side
      L.ship = spots([63, 65, 67], range(20, 30, 2));                       // 18 spots on the shipping side
      L.fork0 = [cell(11, 40), cell(11, 42)]; L.jack0 = cell(63, 36);
      L.areas = [
        { t: 'Pallet racks', x: 36, z: 25.5, k: 'rack' },
        { t: 'Receiving', x: 6, z: 38, k: 'stage' },
        { t: 'Shipping', x: 65, z: 33, k: 'stage' },
        { t: 'Packing', x: 60.5, z: 12, k: 'pack' }
      ];
      L.flow = [
        { n: 1, x: 6, z: 9, t: 'In one side, out the other', d: 'Receiving on the west wall, shipping on the east wall: goods move one way through the building.' },
        { n: 2, x: 52, z: 25.5, t: 'Fast movers at the shipping end', d: 'The busiest SKUs sit at the east ends of the aisles, next to packing, so picks stay short.' },
        { n: 3, x: 30, z: 18, t: 'Long put-away for fast movers', d: 'The forklift carries every fast-mover pallet the full length of the building, from the receiving side to the shipping end.' },
        { n: 4, x: 12.5, z: 46, t: 'Separate sides, shared aisles', d: 'Receiving and packing are on opposite sides, but the forklift still carries fast-mover pallets to the east end, where the pickers work.' },
        { n: 5, x: 36, z: -0.2, t: 'Two yards', d: 'Trucks need a yard on both sides of the building: more paving, two gates and two sets of dock staff or a walk across the building.' }
      ];
    }
    if (kind === 'lshape') {
      L.name = 'L-shape layout'; L.short = 'L-shape';
      // the U-shape's racks (x 1-70, z 4-33, front and back cross-aisles); receiving on the south wall toward the
      // south-east corner, shipping on the east wall, packing between them in the corner
      var xl = [[1, 1]]; for (x = 5; x <= 65; x += 5) xl.push([x, x + 1]); xl.push([70, 70]);
      xl.forEach(function (q) { row(q[0], 4, q[1], 33, 'z'); });
      rect(L, 1, 1, 1, 3);
      rect(L, 46, 39, 59, 40); L.bench = [46, 39, 59, 40]; L.drops = [cell(48, 38), cell(53, 38), cell(58, 38)]; L.homeRows = [[46, 59, 38], [46, 59, 37]];
      L.packSpot = cell(61, 41);
      [28, 34, 40].forEach(function (x) { door(x, 'in', 'S'); });
      [42, 48].forEach(function (z) { door(z, 'out', 'E'); });
      L.recv = spots(range(20, 42, 2), [42, 44, 46]);                      // 36 spots in front of the receiving doors
      L.ship = spots([63, 65, 67], range(39, 49, 2));                       // 18 spots in front of the shipping doors
      L.fork0 = [cell(14, 44), cell(14, 46)]; L.jack0 = cell(56, 46);
      L.areas = [
        { t: 'Pallet racks', x: 36, z: 19, k: 'rack' },
        { t: 'Receiving staging', x: 31, z: 48.5, k: 'stage' },
        { t: 'Shipping', x: 65, z: 37.3, k: 'stage' },
        { t: 'Packing', x: 52.5, z: 42.6, k: 'pack' }
      ];
      L.flow = [
        { n: 1, x: 22, z: 49.5, t: 'In on one wall, out on the next', d: 'Receiving on the south wall, shipping on the east wall: goods turn one corner on the way through.' },
        { n: 2, x: 58, z: 30, t: 'Fast movers by the corner', d: 'The busiest SKUs sit in the front bays at the east end, close to packing and to the receiving doors near the corner.' },
        { n: 3, x: 80, z: 60, t: 'Two yards that meet', d: 'Inbound trucks use the south yard and outbound trucks the east yard. Their lanes meet beyond the corner, so the site needs room and traffic rules there.' },
        { n: 4, x: 10, z: 40, t: 'Free floor to the west', d: 'With the doors near the corner, the south-west of the dock zone is free for value-added work, returns or more staging.' },
        { n: 5, x: 0.6, z: 18, t: 'Two walls for growth', d: 'The north and west walls stay free to extend the building.' }
      ];
    }
    // pick faces: every rack cell on the long side of a row that borders an aisle; the picker stands in that aisle cell
    L.racks.forEach(function (r) {
      var i, a;
      if (r.dir === 'x') for (i = r.x0; i <= r.x1; i++) {
        [[r.z0, -1], [r.z1, 1]].forEach(function (q) { a = cell(i, q[0] + q[1]); if (!L.blocked[a]) L.faces.push({ c: a, rx: i + 0.5, rz: q[0] + 0.5, side: q[1], sku: -1 }); });
      } else for (i = r.z0; i <= r.z1; i++) {
        [[r.x0, -1], [r.x1, 1]].forEach(function (q) { a = cell(q[0] + q[1], i); if (!L.blocked[a]) L.faces.push({ c: a, rx: q[0] + 0.5, rz: i + 0.5, side: q[1], sku: -1 }); });
      }
    });
    L.recv.concat(L.ship).forEach(function (s) { L.blocked[s.c] = 0; });
    return L;
  }

  /* ---------- paths: shortest walks on the 8-way grid (10 per straight step, 14 per diagonal, no corner cutting),
     found with a bucket queue; one distance field per start cell, cached ---------- */
  var DX = [1, -1, 0, 0, 1, 1, -1, -1], DZ = [0, 0, 1, -1, 1, -1, 1, -1], DC = [10, 10, 10, 10, 14, 14, 14, 14];
  var INF = 1 << 30;
  function Paths(L) {
    var cache = new Map(), order = [];
    var NB = 64, bucket = [], bl = new Int32Array(NB), i;            // more buckets than the dearest step (14 + 4 + 30)
    for (i = 0; i < NB; i++) bucket.push(new Int32Array(N * 2));
    // neighbour table: for each cell, the 8 neighbour cells (or -1) honouring walls and corner cutting
    var nb = new Int32Array(N * 8), ex = new Int32Array(N);
    // keep through-traffic in the middle of an aisle: a cell next to a rack face costs a little more to enter
    for (var e = 0; e < N; e++) { var ex0 = e % BX, ez0 = (e - ex0) / BX; if (!L.blocked[e] && ((ex0 > 0 && L.blocked[e - 1] && ex0 > 0) || (ex0 < BX - 1 && L.blocked[e + 1]) || (ez0 > 0 && L.blocked[e - BX]) || (ez0 < BZ - 1 && L.blocked[e + BX]))) ex[e] = 4; }
    // a staging spot may hold a pallet: drive round it unless it is where you are going
    L.recv.concat(L.ship).forEach(function (q) { ex[q.c] += 30; });
    for (var c = 0; c < N; c++) {
      var x = c % BX, z = (c - x) / BX;
      for (var k = 0; k < 8; k++) {
        var nx = x + DX[k], nz = z + DZ[k], v = -1;
        if (nx >= 0 && nz >= 0 && nx < BX && nz < BZ) {
          v = nz * BX + nx;
          if (L.blocked[v] || (k >= 4 && (L.blocked[z * BX + nx] || L.blocked[nz * BX + x]))) v = -1;
        }
        nb[c * 8 + k] = v;
      }
    }
    function field(src) {
      var f = cache.get(src); if (f) return f;
      f = new Int32Array(N); f.fill(INF); f[src] = 0;
      for (var q = 0; q < NB; q++) bl[q] = 0;
      bucket[0][bl[0]++] = src;
      var d = 0, left = 1;
      while (left > 0) {
        var bi = d % NB, B = bucket[bi];
        while (bl[bi] > 0) {
          var c = B[--bl[bi]]; left--;
          if (f[c] !== d) continue;
          for (var k = 0; k < 8; k++) {
            var n = nb[c * 8 + k]; if (n < 0) continue;
            var nd = d + DC[k] + ex[n];
            if (nd < f[n]) { f[n] = nd; var b2 = nd % NB; bucket[b2][bl[b2]++] = n; left++; }
          }
        }
        d++;
      }
      cache.set(src, f); order.push(src);
      if (order.length > 1500) cache.delete(order.shift());
      return f;
    }
    function dist(src, dst) { return field(src)[dst] / 10; }
    // path from src to dst: walk back from dst along the field of src
    function path(src, dst) {
      if (src === dst) return [dst];
      var f = field(src), out = [dst], c = dst, guard = 0;
      if (f[dst] >= INF) return [dst];
      while (c !== src && guard++ < N) {
        var best = -1;
        for (var k = 0; k < 8; k++) {
          // a predecessor p of c satisfies f[p] + cost(p->c) == f[c]; the move is symmetric, so use c's own table
          var p = nb[c * 8 + k]; if (p < 0 && !(c === dst)) continue;
          if (p < 0) continue;
          if (f[p] + DC[k] + ex[c] === f[c]) { best = p; if (k < 4) break; }
        }
        if (best < 0) break;
        c = best; out.push(c);
      }
      out.reverse(); out.shift();
      return out;
    }
    return { field: field, path: path, dist: dist };
  }

  /* ---------- one simulation ---------- */
  function Sim(kind, opt) {
    opt = opt || {};
    var orders = opt.orders || 300, share = opt.share || 0.8, seed = opt.seed || 20261121;
    var L = makeLayout(kind), PT = Paths(L), V = velocities(share);
    var rS = rng(seed + 1), rO = rng(seed + 2), rT = rng(seed + 3), rF = rng(seed + 4);
    // slotting: as-is random; redesign by velocity, nearest faces (walking distance from packing) first
    var faces = L.faces, i;
    var slot = opt.slot || (kind === 'asis' ? 'random' : 'velocity');
    if (slot === 'random') {
      var idx = faces.map(function (_, k) { return k; });
      for (i = idx.length - 1; i > 0; i--) { var j = Math.floor(rS() * (i + 1)), t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
      for (i = 0; i < SKUS; i++) faces[idx[i]].sku = i;
    } else {
      var fd = new Float64Array(N); fd.fill(1e12);
      L.drops.forEach(function (d) { var f = PT.field(d); for (var c = 0; c < N; c++) if (f[c] < fd[c]) fd[c] = f[c]; });
      var ord = faces.map(function (_, k) { return k; }).sort(function (a, b) { return fd[faces[a].c] - fd[faces[b].c] || faces[a].c - faces[b].c; });
      for (i = 0; i < SKUS; i++) faces[ord[i]].sku = i;
    }
    var faceOf = new Int32Array(SKUS); faces.forEach(function (f, k) { if (f.sku >= 0) faceOf[f.sku] = k; });

    var S = {
      kind: kind, L: L, V: V, t: 0, agents: [], trucks: [], yard: [], pallets: [], outQ: 0, packed: 0,
      heat: new Float32Array(N), heatWait: new Float32Array(N), events: [],
      k: { orders: 0, lines: 0, walk: 0, tWalk: 0, tWait: 0, tPick: 0, tOther: 0, fWait: 0, fWalk: 0, dts: [], trucks: [], waits: 0, tIdle: 0, fBusy: 0, jWait: 0 }
    };
    var nPick = Math.max(3, Math.min(12, Math.round(orders / 50)));
    S.queue = P.backlog; S.released = P.backlog; var gap = P.cutoff / (orders - P.backlog), nextOrder = gap;
    var nForks = Math.max(1, Math.round(orders / 250));             // one forklift below 375 orders a day (350 on the slider), two from 375 (400)

    function agent(type, c) {
      var a = { id: S.agents.length, type: type, prio: type === 'fork' ? 3 : type === 'jack' ? 2 : 1, x: c % BX + 0.5, z: Math.floor(c / BX) + 0.5, cell: c, path: [], pi: 0,
        state: 'idle', timer: 0, waitT: 0, cleared: false, speed: type === 'fork' ? P.vFork : type === 'jack' ? P.vJack : P.vPick, dirx: 1, dirz: 0, load: null };
      S.agents.push(a); return a;
    }
    // each picker has its own place at the packing bench (where it starts an order and drops it off)
    var homes = [];
    if (L.homeCol) {                                                   // a bench along x: places spread down the column
      var hc = L.homeCol; for (i = 0; i < nPick; i++) homes.push(cell(hc[0] - (i % 2 && nPick > hc[2] - hc[1] + 1 ? 1 : 0), Math.round(hc[1] + (hc[2] - hc[1]) * (nPick > 1 ? i / (nPick - 1) : 0.5))));
    } else {
      var row0 = L.homeRows[0], n0 = Math.min(nPick, row0[1] - row0[0] + 1);
      for (i = 0; i < n0; i++) homes.push(cell(Math.round(row0[0] + (row0[1] - row0[0]) * (n0 > 1 ? i / (n0 - 1) : 0.5)), row0[2]));
      for (i = n0; i < nPick; i++) homes.push(cell(L.homeRows[1][0] + (i - n0) * 2 + 1, L.homeRows[1][2]));
    }
    for (i = 0; i < nPick; i++) { var p = agent('picker', homes[i]); p.state = 'setup'; S.queue--; p.timer = P.tSetup * (0.3 + 0.7 * i / nPick); p.home = homes[i]; }
    for (i = 0; i < nForks; i++) agent('fork', L.fork0[i]);
    var jack = agent('jack', L.jack0);

    // trucks: inbound from 07:15 to about 13:00 (5 full loads of 24 pallets, the rest part loads), carriers at 10:30, 12:30, 14:30
    var nIn = Math.max(4, Math.round(14 * orders / 300)), nFtl = Math.round(nIn * 5 / 14);
    for (i = 0; i < nIn; i++) {
      var arr = 900 + i * (21000 / nIn) + (rT() - 0.5) * 1200;
      S.trucks.push({ id: i, dir: 'in', arr: Math.max(300, arr), left: i % 3 === 0 && nFtl-- > 0 ? 24 : 4 + Math.floor(rT() * 7), door: null, state: 'due', next: 0, x: 0, z: 0 });
    }
    [3.5, 5.5, 7.5].forEach(function (h, k) { S.trucks.push({ id: 100 + k, dir: 'out', arr: h * 3600, left: 0, door: null, state: 'due', next: 0, x: 0, z: 0 }); });
    S.trucks.sort(function (a, b) { return a.arr - b.arr; });

    function cx(c) { return c % BX + 0.5; } function cz(c) { return Math.floor(c / BX) + 0.5; }
    function go(a, dst) { a.path = PT.path(a.cell, dst); a.pi = 0; a.cleared = false; a.dst = dst; }
    function moving(a) { return a.pi < a.path.length; }
    function blockedBy(a, nx, nz) {
      if (a.waitT > P.maxWait) return null;
      for (var k = 0; k < S.agents.length; k++) {
        var o = S.agents[k]; if (o === a) continue;
        var dx = o.x - nx, dz = o.z - nz; if (dx * dx + dz * dz > P.near * P.near) continue;
        var still = !moving(o);
        if (still || o.prio > a.prio || (o.prio === a.prio && o.id < a.id)) return o;
      }
      return null;
    }
    function step(a, dt) {                                       // returns metres walked; a.held: stood still this step, giving way
      var rem = a.speed * dt, walked = 0; a.held = false;
      while (rem > 1e-9 && a.pi < a.path.length) {
        var c = a.path[a.pi], tx = cx(c), tz = cz(c), dx = tx - a.x, dz = tz - a.z, d = Math.sqrt(dx * dx + dz * dz);
        if (!a.cleared) {
          var last = a.pi === a.path.length - 1;
          if (!last && blockedBy(a, tx, tz)) { a.waitT += dt; if (!walked) { a.held = true; S.heatWait[a.cell] += dt; } return walked; }
          if (a.waitT > 0) { if (a.waitT >= 1) S.k.waits++; a.waitT = 0; }
          a.cleared = true;
        }
        if (d > 1e-6) { a.dirx = dx / d; a.dirz = dz / d; }
        if (rem >= d) { a.x = tx; a.z = tz; rem -= d; walked += d; a.cell = c; a.pi++; a.cleared = false; }
        else { a.x += dx / d * rem; a.z += dz / d * rem; walked += rem; rem = 0; }
      }
      return walked;
    }

    /* picker: setup -> walk to nearest open line -> pick -> ... -> walk to packing -> drop */
    function newOrder(a) {
      var n = Math.min(8, 1 + poisson(rO, P.lines - 1)), set = {}, lines = [];
      while (lines.length < n) { var s = pickSku(V, rO); if (!set[s]) { set[s] = 1; lines.push(faceOf[s]); } }
      a.order = lines; a.nLines = n;
    }
    function nextLeg(a) {
      if (a.order.length) {
        var f = PT.field(a.cell), bi = 0, bd = 1e18;
        for (var k = 0; k < a.order.length; k++) { var d = f[faces[a.order[k]].c]; if (d < bd) { bd = d; bi = k; } }
        a.target = a.order.splice(bi, 1)[0]; go(a, faces[a.target].c); a.state = 'walk';
      } else {
        go(a, a.home); a.state = 'back';
      }
    }
    function picker(a, dt) {
      if (a.state === 'idle') { S.k.tIdle += dt; if (S.queue > 0) { S.queue--; a.state = 'setup'; a.timer = P.tSetup; } return; }
      if (a.state === 'setup' || a.state === 'pick' || a.state === 'drop') {
        a.timer -= dt; if (a.state === 'pick') S.k.tPick += dt; else S.k.tOther += dt;
        if (a.timer > 0) return;
        if (a.state === 'setup') { newOrder(a); nextLeg(a); }
        else if (a.state === 'pick') nextLeg(a);
        else { S.k.orders++; S.k.lines += a.nLines; S.packed++; if (S.packed % P.ordersPallet === 0) S.outQ++; if (S.queue > 0) { S.queue--; a.state = 'setup'; a.timer = P.tSetup; } else a.state = 'idle'; }
        return;
      }
      var w = step(a, dt); S.k.walk += w; if (w > 0) { S.k.tWalk += dt; S.heat[a.cell] += dt; } else if (a.held) S.k.tWait += dt; else if (moving(a)) S.k.tWalk += dt;
      if (!moving(a)) {
        if (a.state === 'walk') { a.state = 'pick'; a.timer = P.tPick; }
        else if (a.state === 'back') { a.state = 'drop'; a.timer = P.tDrop; }
      }
    }

    /* forklift: oldest pallet in receiving staging -> its SKU's rack location (reserve above the pick face) */
    function fork(a, dt) {
      if (a.state === 'load' || a.state === 'put') {
        a.timer -= dt; if (a.timer > 0) return;
        if (a.state === 'load') { a.load.spot.busy = null; a.load.spot = null; go(a, faces[faceOf[a.load.sku]].c); a.state = 'carry'; }
        else { S.k.dts.push(S.t - a.load.t0); S.k.fBusy += S.t - a.t0; a.load.done = S.t; a.load = null; a.state = 'idle'; }
        return;
      }
      if (a.state === 'idle' || a.state === 'park') {
        var best = null;
        S.pallets.forEach(function (p) { if (!p.claimed && p.spot && p.dir === 'in' && (!best || p.t0 < best.t0)) best = p; });
        if (best) { best.claimed = a.id; a.load = best; go(a, best.spot.c); a.state = 'fetch'; a.t0 = S.t; }
        else if (a.state === 'idle') { go(a, L.fork0[a.id - nPick] || L.fork0[0]); a.state = 'park'; }
      }
      var w = step(a, dt); if (w > 0) { S.k.fWalk += w; S.heat[a.cell] += dt; } else if (a.held) S.k.fWait += dt;
      if (!moving(a)) {
        if (a.state === 'fetch') { a.state = 'load'; a.timer = P.tLoad; }
        else if (a.state === 'carry') { a.state = 'put'; a.timer = P.tPut; }
      }
    }

    /* pallet jack: outbound pallets from packing to a free shipping spot */
    function freeShip() { var best = null, f = PT.field(L.packSpot); L.ship.forEach(function (s) { if (!s.busy && (!best || f[s.c] < f[best.c])) best = s; }); return best; }
    function jackRun(a, dt) {
      if (a.state === 'take' || a.state === 'set') {
        a.timer -= dt; if (a.timer > 0) return;
        if (a.state === 'take') { go(a, a.spot.c); a.state = 'carry'; }
        else { var p = { dir: 'out', spot: a.spot, t0: S.t }; a.spot.busy = p; S.pallets.push(p); a.spot = null; a.state = 'idle'; }
        return;
      }
      if ((a.state === 'idle' || a.state === 'park') && S.outQ > 0) {
        var s = freeShip(); if (s) { S.outQ--; s.busy = 'res'; a.spot = s; go(a, L.packSpot); a.state = 'fetch'; }
      } else if (a.state === 'idle') { go(a, L.jack0); a.state = 'park'; }
      var w = step(a, dt); if (w > 0) S.heat[a.cell] += dt; else if (a.held) S.k.jWait += dt;
      if (!moving(a)) {
        if (a.state === 'fetch') { a.state = 'take'; a.timer = P.tJack; }
        else if (a.state === 'carry') { a.state = 'set'; a.timer = P.tJack; }
      }
    }

    /* trucks and doors */
    function freeRecv(door) {                                    // the free staging spot nearest the door (south wall: same rule as Part 1)
      var best = null, bd = 1e9;
      L.recv.forEach(function (s) { var d = door.wall === 'S' ? Math.abs(s.x - door.x) + s.z * 0.1 : Math.abs(s.z - door.z) + Math.abs(s.x - door.x) * 0.1; if (!s.busy && d < bd) { bd = d; best = s; } });
      return best;
    }
    function doorFor(tr) {
      var ok = L.doors.filter(function (d) { return !d.truck && (d.use === 'both' || d.use === tr.dir); });
      if (!ok.length) return null;
      if (tr.dir === 'out') return ok[ok.length - 1];
      return ok[0];
    }
    function trucks(dt) {
      S.trucks.forEach(function (tr) {
        if (tr.state === 'due' && S.t >= tr.arr) { tr.state = 'yard'; S.yard.push(tr); }
      });
      // first come, first served for the doors
      for (var k = 0; k < S.yard.length; k++) {
        var tr = S.yard[k], d = doorFor(tr);
        if (d) { d.truck = tr; tr.door = d; tr.state = 'dock'; tr.docked = S.t; tr.next = S.t + (tr.dir === 'in' ? P.tUnload : 300); S.yard.splice(k, 1); k--; }
      }
      S.trucks.forEach(function (tr) {
        if (tr.state !== 'dock' || S.t < tr.next) return;
        if (tr.dir === 'in') {
          if (tr.left > 0) {
            var s = freeRecv(tr.door);
            if (s) { var p = { dir: 'in', spot: s, t0: S.t, sku: pickSku(V, rF) }; s.busy = p; S.pallets.push(p); tr.left--; tr.next = S.t + P.tUnload; }
            else { tr.next = S.t + 30; tr.stalled = (tr.stalled || 0) + 30; }
          }
          if (tr.left <= 0) { tr.state = 'gone'; tr.door.truck = null; S.k.trucks.push({ dir: 'in', time: S.t - tr.arr, wait: tr.docked - tr.arr, stall: tr.stalled || 0 }); }
        } else {
          var full = null; L.ship.forEach(function (s2) { if (s2.busy && s2.busy.dir === 'out' && (!full || s2.busy.t0 < full.busy.t0)) full = s2; });
          if (full) { full.busy.done = S.t; full.busy.spot = null; full.busy = null; tr.loaded = (tr.loaded || 0) + 1; tr.next = S.t + P.tShipLoad; }
          else { tr.state = 'gone'; tr.door.truck = null; S.k.trucks.push({ dir: 'out', time: S.t - tr.arr, wait: tr.docked - tr.arr, loaded: tr.loaded || 0 }); }
        }
      });
    }

    function tick(dt) {
      dt = dt || P.dt;
      if (S.t >= P.shift) return false;
      trucks(dt);
      while (S.t >= nextOrder && S.released < orders) { S.queue++; S.released++; nextOrder += gap; }
      for (var k = 0; k < S.agents.length; k++) {
        var a = S.agents[k];
        if (a.type === 'picker') picker(a, dt); else if (a.type === 'fork') fork(a, dt); else jackRun(a, dt);
      }
      S.t += dt;
      return S.t < P.shift;
    }
    function run() { while (tick(P.dt)) {} return results(); }
    function results() {
      var K = S.k, busy = (K.tWalk + K.tPick + K.tWait + K.tOther) / 3600;
      var lph = K.lines / Math.max(1e-9, busy), needH = busy * orders / Math.max(1, K.orders);
      // inbound trucks: those gone, plus those still waiting or at a door at 15:00, timed up to 15:00 (a lower bound)
      var onSite = S.trucks.filter(function (t) { return t.dir === 'in' && (t.state === 'yard' || t.state === 'dock'); });
      var inT = K.trucks.filter(function (t) { return t.dir === 'in'; }).concat(onSite.map(function (t) { return { dir: 'in', time: S.t - t.arr, wait: (t.docked || S.t) - t.arr, open: true }; }));
      var openP = S.pallets.filter(function (p) { return p.dir === 'in' && !p.done; });
      var dtsAll = K.dts.concat(openP.map(function (p) { return S.t - p.t0; }));     // pallets still waiting count up to now
      var det = inT.reduce(function (s, t) { return s + Math.max(0, t.time / 60 - P.freeMin) / 60 * P.detention; }, 0);
      return {
        kind: kind, slot: slot, orders: orders, share: share, pickers: nPick, done: K.orders, lines: K.lines,
        walkOrder: K.walk / Math.max(1, K.orders), lph: lph,
        split: { walk: K.tWalk / 3600, pick: K.tPick / 3600, wait: K.tWait / 3600, other: K.tOther / 3600 },
        waitShare: K.tWait / Math.max(1, busy * 3600), busy: busy, idle: K.tIdle / 3600, late: orders - K.orders, forkWait: K.fWait / 60, forkCycle: K.fBusy / Math.max(1, K.dts.length) / 60, forkKm: K.fWalk / 1000,
        dts: dtsAll.reduce(function (s, x) { return s + x; }, 0) / Math.max(1, dtsAll.length) / 60,
        dtsMax: Math.max.apply(null, dtsAll.concat([0])) / 60, putaway: K.dts.length, inPallets: dtsAll.length,
        truckIn: inT.reduce(function (s, t) { return s + t.time; }, 0) / Math.max(1, inT.length) / 60,
        truckWait: inT.reduce(function (s, t) { return s + t.wait; }, 0) / Math.max(1, inT.length) / 60,
        trucksIn: inT.length, trucksOnSite: onSite.length, detention: det, forklifts: nForks,
        notAway: S.pallets.filter(function (p) { return p.dir === 'in' && !p.done; }).length + S.trucks.reduce(function (s, t) { return s + (t.dir === 'in' && t.state !== 'gone' ? t.left : 0); }, 0),
        pickHoursDay: needH, pickCostYear: needH * P.wage * P.days, detYear: det * P.days,
        waits: K.waits
      };
    }
    S.tick = tick; S.run = run; S.results = results; S.P = P; S.faces = faces; S.cx = cx; S.cz = cz; S.nPick = nPick;
    return S;
  }

  var API = { Sim: Sim, makeLayout: makeLayout, P: P, BX: BX, BZ: BZ, YARD: YARD, SKUS: SKUS };
  if (typeof module !== 'undefined' && module.exports) module.exports = API; else root.WLEngine = API;
})(this);
