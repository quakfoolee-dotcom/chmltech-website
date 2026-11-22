/* Warehouse layout series, Part 5 (V5.71): the layout-to-cash payback calculator.
   Presets come from the article (data-presets on #wl5-calc), built by content/articles/wl5_model.js from the
   results of Parts 1-4. The arithmetic matches calc() in wl5_model.js. No libraries. */
(function () {
  'use strict';
  var box = document.getElementById('wl5-calc');
  if (!box) return;
  var PRE = JSON.parse(box.getAttribute('data-presets'));
  var F = ['labour', 'other', 'rent', 'cost', 'inv', 'cogs', 'cycShare', 'freqX', 'extraDel', 'delCost', 'dead', 'recov', 'hold', 'carry', 'lineStock'];
  var $ = function (id) { return document.getElementById(id); };
  function val(k) { var v = parseFloat($('wl5-' + k).value); return isFinite(v) ? Math.max(0, v) : 0; }   // blanks and negatives count as zero
  function money(x) {
    var s = x < 0 ? '−' : '', a = Math.abs(x);
    if (a >= 1e12) return s + '$' + (a / 1e12).toFixed(2) + 'T';
    if (a >= 1e9) return s + '$' + (a / 1e9).toFixed(2) + 'B';
    if (a >= 1e6) return s + '$' + (a / 1e6).toFixed(2) + 'M';
    if (a >= 1e4) return s + '$' + Math.round(a / 1e3) + 'K';
    return s + '$' + Math.round(a).toLocaleString('en-CA');
  }
  function calc(p) {
    var freqX = Math.max(1, p.freqX);
    var freed = Math.min(p.inv, p.inv * Math.min(100, p.cycShare) / 100 * (1 - 1 / freqX));
    p.dead = Math.min(p.dead, p.inv - freed); p.recov = Math.min(100, p.recov);         // cannot clear more stock than there is
    var freight = p.extraDel * 52 * p.delCost;
    var deadCash = p.dead * p.recov / 100;
    var yearly = p.labour + p.other + p.rent + (freed - p.lineStock) * p.carry / 100 - freight + p.dead * p.hold / 100;
    var oneOffIn = freed + deadCash - p.lineStock;
    var invAfter0 = p.inv - freed - p.dead + p.lineStock, invAfter = Math.max(1, invAfter0);
    var net = p.cost - oneOffIn;
    return { freed: freed, freight: freight, deadCash: deadCash, writeDown: p.dead - deadCash, yearly: yearly, oneOffIn: oneOffIn, net: net,
      payback: yearly <= 0 ? null : (net <= 0 ? 0 : net / yearly * 12), three: 3 * yearly + oneOffIn - p.cost,
      cleared: invAfter0 <= 0, turns0: p.inv > 0 ? p.cogs / p.inv : 0, turns1: p.inv > 0 ? p.cogs / invAfter : 0, dio0: p.cogs > 0 ? 365 * p.inv / p.cogs : 0, dio1: p.cogs > 0 && p.inv > 0 ? 365 * invAfter / p.cogs : 0,
      breakEven: p.extraDel > 0 ? (freed * p.carry / 100) / (p.extraDel * 52) : null };
  }
  function load(key) {
    var p = PRE[key];
    F.forEach(function (k) { var v = k === 'cost' ? Math.round((p.cost[0] + p.cost[1]) / 2 / 1000) * 1000 : p[k]; $('wl5-' + k).value = /^(freqX)$/.test(k) ? v : Math.round(v); });
    box.querySelectorAll('[data-preset]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-preset') === key ? 'true' : 'false'); });
    $('wl5-note').textContent = key === 'own' ? '' : PRE[key].note;
    update();
  }
  function update() {
    var p = {}; F.forEach(function (k) { p[k] = val(k); });
    var r = calc(p);
    $('wl5-yearly').textContent = money(r.yearly);
    $('wl5-once').textContent = money(r.oneOffIn - p.cost);
    $('wl5-pay').textContent = r.payback === 0 ? 'Covered' : r.payback === null ? 'Never' : (r.payback < 24 ? r.payback.toFixed(1) + ' months' : (r.payback / 12).toFixed(1) + ' years');
    $('wl5-pay-n').textContent = r.payback === 0 ? 'by the stock freed, once deliveries change' : r.payback === null ? 'the yearly result is not positive' : 'after the one-off stock change';
    $('wl5-three').textContent = money(r.three);
    var dg = Math.abs(r.turns1 - r.turns0) < 0.1 ? 2 : 1;
    $('wl5-turns').textContent = r.turns0.toFixed(dg) + ' → ' + r.turns1.toFixed(dg);
    var run = p.labour + p.other + p.rent, pl = run > 0 ? p.cost / run * 12 : null;
    $('wl5-payl').textContent = pl === null ? 'Never' : pl < 24 ? pl.toFixed(1) + ' months' : (pl / 12).toFixed(1) + ' years';
    $('wl5-dio').textContent = p.inv > 0 && p.cogs > 0 ? Math.round(r.dio0) + ' → ' + Math.round(r.dio1) + ' days of stock' : 'Enter inventory and cost of goods sold';
    if (p.inv <= 0 || p.cogs <= 0) $('wl5-turns').textContent = '–';
    else if (r.cleared) { $('wl5-turns').textContent = r.turns0.toFixed(1) + ' → –'; $('wl5-dio').textContent = 'all stock cleared'; }
    $('wl5-freed').textContent = money(r.freed);
    $('wl5-be').textContent = r.breakEven === null ? 'No extra deliveries' : 'Break-even: ' + money(r.breakEven) + ' an extra delivery' + (p.freqX < 1 ? ' (deliveries as often as now)' : '');
    $('wl5-wd').textContent = p.dead > 0 ? 'Dead stock: ' + money(r.deadCash) + ' cash in, ' + money(r.writeDown) + ' written off' : 'No dead stock cleared';
  }
  box.querySelectorAll('[data-preset]').forEach(function (b) { b.addEventListener('click', function () { load(b.getAttribute('data-preset')); }); });
  F.forEach(function (k) {
    $('wl5-' + k).addEventListener('input', function () {
      box.querySelectorAll('[data-preset]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      $('wl5-note').textContent = 'Your own numbers.';
      update();
    });
  });
  load('dist');
})();
