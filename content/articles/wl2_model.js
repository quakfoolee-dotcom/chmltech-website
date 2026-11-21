/* Warehouse layout series, Part 2: runs the Layout Lab engine (assets/js/wl-engine.js) for the three flow patterns
   (U-shape = 'redesign', straight-through = 'thru', L-shape = 'lshape'), so the article quotes the simulator's numbers.
   Usage: node content/articles/wl2_model.js   (writes content/articles/wl2_results.json) */
var path = require('path'), fs = require('fs');
var E = require(path.join(__dirname, '..', '..', 'assets', 'js', 'wl-engine.js'));
var K = ['redesign', 'thru', 'lshape'];
function run(kind, o) { return E.Sim(kind, o || {}).run(); }
function all(o) { var r = {}; K.forEach(function (k) { r[k] = run(k, o); }); return r; }
var out = { kinds: K, base: all(), volume: [], seeds: [], layout: {}, P: E.P };
// model-only check: the U-shape with its receiving doors moved toward the middle of the dock wall
out.base.ucentre = run('ucentre');
for (var v = 150; v <= 600; v += 50) { var x = all({ orders: v }); x.orders = v; out.volume.push(x); }
for (var sd = 1; sd <= 10; sd++) { var y = all({ seed: sd }); y.ucentre = run('ucentre', { seed: sd }); y.seed = sd; out.seeds.push(y); }
K.forEach(function (k) {
  var L = E.makeLayout(k);
  out.layout[k] = { name: L.short, faces: L.faces.length, rackCells: L.racks.reduce(function (n, r) { return n + (r.x1 - r.x0 + 1) * (r.z1 - r.z0 + 1); }, 0),
    aisles: L.racks.length - 1, aisleLen: L.racks[1].dir === 'x' ? L.racks[1].x1 - L.racks[1].x0 + 1 : L.racks[1].z1 - L.racks[1].z0 + 1,
    doors: L.doors.map(function (d) { return d.wall + ':' + d.use; }), walls: Object.keys(L.doors.reduce(function (m, d) { m[d.wall] = 1; return m; }, {})), flow: L.flow };
});
fs.writeFileSync(path.join(__dirname, 'wl2_results.json'), JSON.stringify(out, null, 1));
console.error('wrote wl2_results.json');
