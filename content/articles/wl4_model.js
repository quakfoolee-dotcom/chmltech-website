/* Warehouse layout series, Part 4: feeding the filling lines. Runs the Layout Lab engine (assets/js/wl-engine.js) for
   Ridgeline Coatings' three ways of feeding two filling lines (mstore = central store, call when empty; mside =
   line-side supermarket, call when empty; mkanban = supermarket, two bins and a 20-minute milk run), and turns the
   line minutes lost into money.
   Usage: node content/articles/wl4_model.js   (writes content/articles/wl4_results.json) */
var path = require('path'), fs = require('fs');
var E = require(path.join(__dirname, '..', '..', 'assets', 'js', 'wl-engine.js'));
var K = ['mstore', 'mside', 'mkanban'];
function run(kind, o) { var r = E.Sim(kind, o || {}).run(); return { mfg: r.mfg, dts: r.dts, notAway: r.notAway, forkCycle: r.forkCycle, putaway: r.putaway }; }
function all(o) { var r = {}; K.forEach(function (k) { r[k] = run(k, o); }); return r; }
var out = { kinds: K, base: all(), speed: [], seeds: [], layout: {}, P: E.P };
for (var v = 150; v <= 600; v += 75) { var x = all({ orders: v }); x.speed = v / 300; out.speed.push(x); }
for (var sd = 1; sd <= 10; sd++) { var y = all({ seed: sd }); y.seed = sd; out.seeds.push(y); }
// the milk-run interval: what happens at standard speed as the loop gets longer
out.loop = [10, 20, 30, 40, 50, 60].map(function (m) { var p0 = E.P.mLoop; E.P.mLoop = m; var r = run('mkanban'); E.P.mLoop = p0; return { loop: m, starved: r.mfg.starved, hh: r.mfg.handlerHours, loops: r.mfg.loops }; });
// what each change contributes: ten-seed averages of the shipped set-ups and of model-only variants
function avg10(k, o) { var st = 0, hh = 0; for (var sd = 1; sd <= 10; sd++) { var m = run(k, Object.assign({ seed: sd }, o || {})).mfg; st += m.starved; hh += m.handlerHours; } return { starved: st / 10, hh: hh / 10 }; }
out.steps = [
  ['store', 'Central store, as set up', avg10('mstore')],
  ['noIssue', 'Central store, no 2-minute issue booking', avg10('mstore', { issue: 0 })],
  ['near', 'Central store, no issue booking, line materials in the store faces nearest the lines', avg10('mstore', { issue: 0, storeNear: true })],
  ['side', 'Line-side supermarket, called when a load runs out', avg10('mside')],
  ['store2', 'Central store, two bins at the line, called when the first runs out', avg10('mstore', { twoBin: true })],
  ['side2', 'Supermarket, two bins at the line, called when the first runs out', avg10('mside', { twoBin: true })],
  ['kanban', 'Supermarket, two bins and a 20-minute milk run', avg10('mkanban')]
].map(function (q) { return { id: q[0], t: q[1], starved: q[2].starved, hh: q[2].hh }; });
// cards collected on the round (seen one loop late), against cards seen when posted
out.late = [300, 450, 600].map(function (v) { return { speed: v / 300, late: run('mkanban', { orders: v, lateCards: true }).mfg.starved, onTime: run('mkanban', { orders: v }).mfg.starved }; });
K.forEach(function (k) { var L = E.makeLayout(k); out.layout[k] = { short: L.short, name: L.name, faces: L.faces.length, sm: L.faces.filter(function (f) { return f.rx > 40; }).length, flow: L.flow }; });
/* money: assumptions stated in the article */
var C = {
  crew: 3,                 // operators per filling line
  wage: E.P.wage, ot: 1.5, // $ an hour loaded; overtime premium
  margin: 8,               // $ contribution margin a pail (if lost output is a lost sale)
  carry: 0.25,             // inventory carrying cost a year, share of value
  days: E.P.days,
  rackUSD: [50, 120], fx: 1.42,  // supermarket racking, US$ a position (Part 3 sources), CAD per USD
  levels: 2                      // supermarket: floor plus one beam level (up to 5 loads of a material across its positions)
};
var B = out.base, econ = { C: C, opts: {} };
K.forEach(function (k) {
  var m = B[k].mfg, st = m.starved / 60;                        // line-hours lost a day (both lines)
  econ.opts[k] = {
    lostHours: st, lostPails: (B.mkanban.mfg.made - m.made),
    otYear: st * C.crew * C.wage * C.ot * C.days,               // make the pails up on overtime
    marginYear: (B.mkanban.mfg.made - m.made) * C.margin * C.days,
    handlerYear: m.handlerHours * C.wage * C.days,
    stockCarry: (m.lineStock + m.smStock) * C.carry,
    rack: k === 'mstore' ? [0, 0] : [out.layout[k].sm * C.levels * C.rackUSD[0] * C.fx, out.layout[k].sm * C.levels * C.rackUSD[1] * C.fx]
  };
});
out.econ = econ;
fs.writeFileSync(path.join(__dirname, 'wl4_results.json'), JSON.stringify(out, null, 1));
console.error('wrote wl4_results.json');
