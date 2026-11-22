/* Warehouse layout series, Part 3: density against access. Runs the Layout Lab engine (assets/js/wl-engine.js) for
   three aisle widths on the U-shape plan of Part 2 (wide = 4 m, counterbalance truck; redesign = 3 m, reach truck;
   vna = 2 m, wire-guided turret truck) and prices the extra pallet positions against leasing more space.
   Usage: node content/articles/wl3_model.js   (writes content/articles/wl3_results.json) */
var path = require('path'), fs = require('fs');
var E = require(path.join(__dirname, '..', '..', 'assets', 'js', 'wl-engine.js'));
var K = ['wide', 'redesign', 'vna'], LEVELS = 4;                 // floor plus three beam levels, the same clear height for all
function run(kind, o) { return E.Sim(kind, o || {}).run(); }
function all(o) { var r = {}; K.forEach(function (k) { r[k] = run(k, o); }); return r; }
var out = { kinds: K, levels: LEVELS, base: all(), volume: [], seeds: [], layout: {}, P: E.P };
for (var v = 150; v <= 600; v += 50) { var x = all({ orders: v }); x.orders = v; out.volume.push(x); }
for (var sd = 1; sd <= 10; sd++) { var y = all({ seed: sd }); y.seed = sd; out.seeds.push(y); }
var M2FT = 10.7639;
K.forEach(function (k) {
  var L = E.makeLayout(k);
  out.layout[k] = { short: L.short, truck: L.truck, aisle: L.aisleW || 3, faces: L.faces.length, positions: L.faces.length * LEVELS,
    aisles: L.racks.length - 1, flow: k === 'redesign' ? L.p3 : L.flow };
});
/* ---- costs. Published ranges in US dollars, converted at FX; rent in Canadian dollars (Metro Vancouver). ---- */
var C = {
  fx: 1.42,                                    // CAD per USD, mid-November 2026
  rack: [50, 120],                             // USD per position, selective pallet rack, new
  rackVNA: [80, 200],                          // USD per position, VNA-tolerance racking
  move: [0.25, 0.40],                          // taking down and re-erecting existing racks, as a share of the new price (our assumption)
  reach: [25000, 60000], turret: [100000, 200000],   // USD per truck, new
  floor: [1.5 * 1.75, 8 * 1.75],               // USD per sq ft of the rack zone: superflat grinding to replacement, 2003 prices x 1.75
  netRent: 18.87, addRent: 7.12,               // CAD per sq ft a year: CBRE Q3 2026 net asking; Avison Young additional rent
  rackZoneM2: 70 * 30                          // the rack block, x 1-70 by z 4-33 on the 1 m grid
};
var B = out.base, P = E.P, posW = out.layout.wide.positions;
var sqftPerPos = C.rackZoneM2 * M2FT / posW, rentPos = sqftPerPos * (C.netRent + C.addRent);
function lab(r) { return r.pickHoursDay * P.wage * P.days + r.forkCycle / 60 * r.putaway * P.wage * P.days; }
var econ = { C: C, sqftPerPos: sqftPerPos, rentPerPosYear: rentPos, opts: {} };
['redesign', 'vna'].forEach(function (k) {
  var add = out.layout[k].positions - posW, vna = k === 'vna';
  // narrow: new racking for the added positions and the existing racks moved; VNA: new VNA-tolerance racking for every position
  function cost(i) { return C.fx * (vna ? C.rackVNA[i] * out.layout[k].positions + C.turret[i] + C.floor[i] * C.rackZoneM2 * M2FT
                                        : C.rack[i] * add + C.rack[i] * C.move[i] * posW + C.reach[i]); }
  var lo = cost(0), hi = cost(1);
  var dLab = lab(B.wide) - lab(B[k]);                           // labour a year saved (+) or added (-) against wide aisles
  var gain = add * rentPos + dLab;
  econ.opts[k] = { add: add, capex: [lo, hi], perPos: [lo / add, hi / add], rentAvoided: add * rentPos, labour: dLab, gain: gain, payback: [lo / gain, hi / gain],
    leaseSqft: add * sqftPerPos };
});
out.econ = econ;
fs.writeFileSync(path.join(__dirname, 'wl3_results.json'), JSON.stringify(out, null, 1));
console.error('wrote wl3_results.json');
