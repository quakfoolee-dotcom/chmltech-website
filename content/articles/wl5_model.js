/* Warehouse layout series, Part 5: from layout to cash. Gathers the results of Parts 1-4 into the presets of the
   payback calculator, and runs one new check with the Layout Lab engine: can the dock take the same pallets in more,
   smaller deliveries? (the inventory lever: smaller, more frequent receipts mean less cycle stock).
   Usage: node content/articles/wl5_model.js   (writes content/articles/wl5_results.json) */
var path = require('path'), fs = require('fs');
var E = require(path.join(__dirname, '..', '..', 'assets', 'js', 'wl-engine.js'));
var R1 = require('./wl1_results.json'), R4 = require('./wl4_results.json');
var out = { P: E.P, deliveries: [] };
// the same pallets in 14 to 28 inbound deliveries a day, five seeds each, as-is against redesigned (Part 1)
[14, 18, 21, 24, 28].forEach(function (n) {
  var row = { trucks: n };
  ['asis', 'redesign'].forEach(function (k) {
    var a = { truckIn: 0, detYear: 0, notAway: 0, inPallets: 0, dts: 0 };
    for (var sd = 1; sd <= 5; sd++) { var r = E.Sim(k, { seed: sd, inTrucks: n }).run(); for (var q in a) a[q] += r[q] / 5; }
    row[k] = a;
  });
  out.deliveries.push(row);
});
// the same check with a second forklift in the as-is layout: is the dock bottleneck the forklift behind it?
out.twoForks = [14, 28].map(function (n) { var a = { truckIn: 0, detYear: 0, notAway: 0 }; for (var sd = 1; sd <= 5; sd++) { var r = E.Sim('asis', { seed: sd, inTrucks: n, forks: 2 }).run(); for (var q in a) a[q] += r[q] / 5; } return { trucks: n, asis: a }; });
// Part 1's own delivery mix (full and part loads): its ten simulated days and its example day, for reference
out.mix14 = {}; ['asis', 'redesign'].forEach(function (k) { out.mix14[k] = { truckIn: R1.seeds.reduce(function (s, x) { return s + x[k].truckIn; }, 0) / R1.seeds.length, day: R1.base[k].truckIn }; });
var P = E.P, fx = 1.42;
// ten simulated days from Part 1 (seeds 1-10), not the single day of its main table
function mean(k, q) { return R1.seeds.reduce(function (s, x) { return s + x[k][q]; }, 0) / R1.seeds.length; }
var A = { pickCostYear: mean('asis', 'pickCostYear'), detYear: mean('asis', 'detYear') }, D = { pickCostYear: mean('redesign', 'pickCostYear'), detYear: mean('redesign', 'detYear') };
var positions = 840 * 4;                                          // Part 1: 840 faces, floor plus three levels
/* the presets: everything a reader can change in the calculator */
out.presets = {
  dist: {
    name: 'Vancouver distributor (Parts 1 to 3)',
    labour: A.pickCostYear - D.pickCostYear, other: A.detYear - D.detYear, rent: 0,
    cost: [positions * 50 * 0.25 * fx + 15000, positions * 120 * 0.40 * fx + 20000],   // move the racks (Part 3 rates) plus engineering, permits and labels
    inv: 3000000, cogs: 18000000, cycShare: 20, freqX: 2, extraDel: 35, delCost: 40,
    dead: 120000, recov: 30, hold: 5, carry: 10, lineStock: 0
  },
  mfg: {
    name: 'Ridgeline Coatings (Part 4)',
    labour: 0, other: R4.econ.opts.mstore.otYear - R4.econ.opts.mkanban.otYear, rent: 0,
    cost: [R4.econ.opts.mkanban.rack[0] + 8000, R4.econ.opts.mkanban.rack[1] + 8000],     // supermarket racking plus bins, cards and set-up
    inv: 600000, cogs: 2400000, cycShare: 0, freqX: 1, extraDel: 0, delCost: 0,
    dead: 0, recov: 0, hold: 5, carry: 10, lineStock: R4.base.mkanban.mfg.lineStock - R4.base.mside.mfg.lineStock
  }
};
/* the calculator's arithmetic (the same as assets/js/wl5.js), for the article's tables */
function calc(p, cost) {
  var freed = p.inv * p.cycShare / 100 * (1 - 1 / Math.max(1, p.freqX));
  freed = Math.min(freed, p.inv); var dead = Math.min(p.dead, p.inv - freed); p = Object.assign({}, p, { dead: dead });
  var freight = p.extraDel * 52 * p.delCost;
  var deadCash = p.dead * p.recov / 100;
  var yearly = p.labour + p.other + p.rent + (freed - p.lineStock) * p.carry / 100 - freight + p.dead * p.hold / 100;
  var oneOffIn = freed + deadCash - p.lineStock;
  var invAfter = p.inv - freed - p.dead + p.lineStock;
  var net = cost - oneOffIn, run = p.labour + p.other + p.rent;
  return { freed: freed, freight: freight, deadCash: deadCash, writeDown: p.dead - deadCash, yearly: yearly, oneOffIn: oneOffIn,
    payback: yearly <= 0 ? null : (net <= 0 ? 0 : net / yearly * 12), paybackLayout: run > 0 ? cost / run * 12 : null, three: 3 * yearly + oneOffIn - cost,
    turns0: p.cogs / p.inv, turns1: p.cogs / invAfter, dio0: 365 * p.inv / p.cogs, dio1: 365 * invAfter / p.cogs,
    breakEven: p.extraDel > 0 ? (freed * p.carry / 100) / (p.extraDel * 52) : null };
}
out.calc = {};
Object.keys(out.presets).forEach(function (k) { var p = out.presets[k]; out.calc[k] = { lo: calc(p, p.cost[0]), hi: calc(p, p.cost[1]) }; });
// layout only (no inventory moves, no extra stock), for the article
var ml = Object.assign({}, out.presets.mfg, { lineStock: 0 });
out.calc.mfgLayout = { lo: calc(ml, ml.cost[0]), hi: calc(ml, ml.cost[1]) };
// the distributor without the dead stock, to show how much of the turns gain is the write-off
var nd = Object.assign({}, out.presets.dist, { dead: 0 });
out.calc.distNoDead = { lo: calc(nd, nd.cost[0]) };
// carrying cost at the full 25% (if the space and handling would really be saved), for the article
var c25 = Object.assign({}, out.presets.dist, { carry: 25 });
out.calc.dist25 = { lo: calc(c25, c25.cost[0]) };
// the distributor with the layout only (no inventory moves), for the article
var pl = Object.assign({}, out.presets.dist, { cycShare: 0, extraDel: 0, dead: 0 });
out.calc.distLayout = { lo: calc(pl, pl.cost[0]), hi: calc(pl, pl.cost[1]) };
fs.writeFileSync(path.join(__dirname, 'wl5_results.json'), JSON.stringify(out, null, 1));
console.error('wrote wl5_results.json');
