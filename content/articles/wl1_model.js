/* Warehouse layout series, Part 1: runs the Layout Lab engine (assets/js/wl-engine.js) for the numbers quoted in the
   article, so the text, the tables and the simulator agree.
   Usage: node content/articles/wl1_model.js   (writes content/articles/wl1_results.json) */
var path = require('path'), fs = require('fs');
var E = require(path.join(__dirname, '..', '..', 'assets', 'js', 'wl-engine.js'));
function run(kind, o) { return E.Sim(kind, o || {}).run(); }
var out = { base: { asis: run('asis'), redesign: run('redesign'), slotOnly: run('asis', { slot: 'velocity' }), layoutOnly: run('redesign', { slot: 'random' }) }, volume: [], share: [], P: E.P };
for (var v = 150; v <= 600; v += 50) out.volume.push({ orders: v, asis: run('asis', { orders: v }), redesign: run('redesign', { orders: v }) });
[0.6, 0.7, 0.8, 0.9].forEach(function (s) { out.share.push({ share: s, asis: run('asis', { share: s }), redesign: run('redesign', { share: s }) }); });
out.seeds = [];                                                    // ten other simulated days, for the spread
for (var sd = 1; sd <= 10; sd++) out.seeds.push({ seed: sd, asis: run('asis', { seed: sd }), redesign: run('redesign', { seed: sd }) });
var L = { asis: E.makeLayout('asis'), redesign: E.makeLayout('redesign') };
out.layout = {};
Object.keys(L).forEach(function (k) {
  out.layout[k] = { faces: L[k].faces.length, doors: L[k].doors.map(function (d) { return d.use; }), recv: L[k].recv.length, ship: L[k].ship === L[k].recv ? 0 : L[k].ship.length,
    aisles: L[k].racks.length - 1, faults: L[k].faults,
    rackCells: L[k].racks.reduce(function (n, r) { return n + (r.x1 - r.x0 + 1) * (r.z1 - r.z0 + 1); }, 0) };
});
fs.writeFileSync(path.join(__dirname, 'wl1_results.json'), JSON.stringify(out, null, 1));
console.error('wrote wl1_results.json');
