/* Chmltech LLM leaderboard: chart studio (V5.40).
   Effort curves, side-by-side model comparison and ranking bars, drawn from the same embedded dataset
   (#llm-data) as llm.js, plus a PNG download for every chart on the page.
   Colours: six validated categorical slots (dataviz palette check, light surface); a model keeps its colour
   while it stays selected. Text is always in ink colours, never the series colour. */
(function () {
  "use strict";
  var el = document.getElementById("llm-data"), root = document.getElementById("ls-root");
  if (!el || !root) return;
  var D = JSON.parse(el.textContent), MODELS = D.models, BENCH = D.benchmarks, BY = {}, MB = {};
  BENCH.forEach(function (b) { BY[b.id] = b; });
  MODELS.forEach(function (m) { MB[m.id] = m; });
  var SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"];
  var INK = "#0B1B33", MUTED = "#5B6472", GRID = "#E9E6DE", AXIS = "#B9B4A8";
  var PROP = "#0B6FA4", OPEN = "#C2571A";
  var NS = "http://www.w3.org/2000/svg";
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function num(v, d) { return Number(v).toLocaleString("en-CA", { maximumFractionDigits: d == null ? 1 : d }); }
  function money(v) { return v >= 100 ? "$" + num(v, 0) : v >= 1 ? "$" + num(v, 2) : "$" + Number(v).toPrecision(2); }
  function fmt(v, b) {
    if (!b) return num(v);
    if (b.unit === "USD") return "$" + num(v, 0);
    if (b.unit === "Elo") return num(v, 0);
    return Number(v).toLocaleString("en-CA", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + (b.unit === "%" ? "%" : "");
  }
  function tickMoney(v) { return v >= 1 ? "$" + (v >= 1000 ? num(v / 1000, 1) + "K" : num(v, 2).replace(/\.00$/, "")) : "$" + Number(v).toPrecision(1); }
  function tickK(v) { return v >= 1000 ? num(v / 1000, 0) + "K" : num(v, 0); }

  // ---------- shared axis helpers ----------
  function niceStep(span, n) {
    var raw = span / n, p = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / p;
    return (f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10) * p;
  }
  function linTicks(lo, hi, n) {
    var st = niceStep(hi - lo || 1, n || 5), out = [];
    for (var v = Math.ceil(lo / st) * st; v <= hi + 1e-9; v += st) out.push(+v.toFixed(10));
    return out;
  }
  function logTicks(lo, hi) {
    var out = [], steps = [1, 2, 5];
    for (var e = Math.floor(Math.log(lo) / Math.LN10); e <= Math.ceil(Math.log(hi) / Math.LN10); e++)
      steps.forEach(function (k) { var v = k * Math.pow(10, e); if (v >= lo * 0.999 && v <= hi * 1.001) out.push(v); });
    return out;
  }

  // ---------- tooltip ----------
  var tip = document.createElement("div");
  tip.className = "ls-tip"; tip.hidden = true; document.body.appendChild(tip);
  function showTip(evt, html) {
    tip.innerHTML = html; tip.hidden = false;
    var x = evt.clientX + 14, y = evt.clientY + 14, r = tip.getBoundingClientRect();
    if (x + r.width > window.innerWidth - 8) x = evt.clientX - r.width - 14;
    if (y + r.height > window.innerHeight - 8) y = evt.clientY - r.height - 14;
    tip.style.left = x + "px"; tip.style.top = y + "px";
  }
  function hideTip() { tip.hidden = true; }
  function bindTips(box) {
    Array.prototype.forEach.call(box.querySelectorAll("[data-tip]"), function (n) {
      n.addEventListener("mousemove", function (e) { showTip(e, n.getAttribute("data-tip")); });
      n.addEventListener("mouseleave", hideTip);
      n.addEventListener("focus", function () { var r = n.getBoundingClientRect(); showTip({ clientX: r.right, clientY: r.top }, n.getAttribute("data-tip")); });
      n.addEventListener("blur", hideTip);
    });
  }

  // ---------- model picker (shared by effort curves and compare) ----------
  function Picker(opts) {
    var self = this;
    self.sel = []; self.slot = {}; self.box = opts.box; self.onchange = opts.onchange; self.max = 6;
    self.set = function (ids) {
      self.sel = []; self.slot = {};
      ids.forEach(function (id) { self.add(id, true); });
      self.render(); self.onchange();
    };
    self.add = function (id, quiet) {
      if (!MB[id] || self.sel.indexOf(id) > -1 || self.sel.length >= self.max) return;
      var used = self.sel.map(function (s) { return self.slot[s]; }), k = 0;
      while (used.indexOf(k) > -1) k++;
      self.slot[id] = k; self.sel.push(id);
      if (!quiet) { self.render(); self.onchange(); }
    };
    self.remove = function (id) {
      self.sel = self.sel.filter(function (s) { return s !== id; }); delete self.slot[id];
      self.render(); self.onchange();
    };
    self.color = function (id) { return SLOTS[self.slot[id]]; };
    self.render = function () {
      var avail = opts.available().filter(function (id) { return self.sel.indexOf(id) < 0; });
      var chips = self.sel.map(function (id) {
        return '<li class="ls-chip"><svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="5" fill="' + self.color(id) + '"/></svg>' +
          esc(MB[id].name) + '<button type="button" data-rm="' + esc(id) + '" aria-label="Remove ' + esc(MB[id].name) + '">×</button></li>';
      }).join("");
      var add = self.sel.length < self.max && avail.length ?
        '<label class="ls-add"><span class="visually-hidden">Add a model</span><select data-add><option value="">+ Add a model</option>' +
        avail.map(function (id) { return '<option value="' + esc(id) + '">' + esc(MB[id].name) + "</option>"; }).join("") + "</select></label>" :
        (self.sel.length >= self.max ? '<span class="ls-hint">Up to six models</span>' : "");
      self.box.innerHTML = '<ul class="ls-chips" aria-label="Selected models">' + chips + "</ul>" + add;
      Array.prototype.forEach.call(self.box.querySelectorAll("[data-rm]"), function (b) { b.addEventListener("click", function () { self.remove(b.getAttribute("data-rm")); }); });
      var s = self.box.querySelector("[data-add]");
      if (s) s.addEventListener("change", function () { if (s.value) self.add(s.value); });
    };
  }

  // ---------- 1. Effort curves ----------
  var CURVE_BOARDS = [["aa_index", "AA Intelligence Index"], ["arc2", "ARC-AGI-2"], ["aa_coding", "AA Coding Agent Index"], ["tbench", "Terminal-Bench 4.1"]];
  // Effort order for joining points (V5.47): a line follows Low -> Max, not cost, so it reads as "what more effort buys".
  var EFFORT = ["minimal", "low", "medium", "high", "x-high", "xhigh", "max"];
  function effortRank(set) {
    var t = String(set || "").toLowerCase(), best = -1;
    EFFORT.forEach(function (e, i) { if (new RegExp("(^|[^a-z-])" + e.replace("-", "\\-") + "($|[^a-z])").test(t)) best = i; });
    return best;
  }
  function orderPoints(p) {
    var known = p.every(function (q) { return effortRank(q.set) >= 0; });
    return p.sort(function (a, b) { return known ? effortRank(a.set) - effortRank(b.set) || a.x - b.x : a.x - b.x; });
  }
  function curvePoints(m, bid, xm) {
    if (bid === "aa_index") {
      return (m.aa || []).filter(function (p) { return p[xm] != null && !/non-?reasoning/i.test(p.set || ""); }).map(function (p) { return { x: p[xm], y: p.v, set: p.set }; });
    }
    if (xm !== "cost") return [];
    var r = m.s && m.s[bid];
    if (!r) return [];
    if (r.alt) return r.alt.filter(function (a) { return a[1] > 0; }).map(function (a) { return { x: a[1], y: a[0], set: a[2] }; });
    return r.cost ? [{ x: r.cost, y: r.v, set: r.set }] : [];
  }
  function CurveView(P, opts) {
    var cState = { b: "aa_index", x: opts.x || "cost", log: !!opts.log };
    var cPick = new Picker({
      box: $(P + "pick"),
      available: function () { return MODELS.filter(function (m) { return curvePoints(m, cState.b, cState.x).length > 0; })
        .sort(function (a, b) { return a.name.localeCompare(b.name); }).map(function (m) { return m.id; }); },
      onchange: function () { drawCurves(); }
    });
    function curveDefaults() {
      if (cState.b === "aa_index") return opts.defaults.slice();
      return MODELS.filter(function (m) { return curvePoints(m, cState.b, "cost").length > 1; })
        .sort(function (a, b) { return b.s[cState.b].v - a.s[cState.b].v; }).slice(0, 4).map(function (m) { return m.id; });
    }
    function drawCurves() {
      var b = BY[cState.b], xm = cState.x, box = $(P + "chart");
      var series = cPick.sel.map(function (id) {
        return { m: MB[id], c: cPick.color(id), p: orderPoints(curvePoints(MB[id], cState.b, xm)) };
      }).filter(function (s) { return s.p.length; });
      var XL = { cost: "Cost per task (US$)", time: "Time per task (minutes)", tok: "Output tokens per task" }[xm];
      $(P + "title").textContent = b.name + " versus " + XL.replace(/ \(.*\)/, "").toLowerCase();
      if (!series.length) { box.innerHTML = '<p class="ls-empty">Add a model with results at more than one setting on this benchmark.</p>'; $(P + "table").innerHTML = ""; return; }
      var W = 860, H = 470, ml = 58, mr = 24, mb = 52, lrows = 1, lw0 = ml;
      series.forEach(function (s) { var iw = 40 + s.m.name.length * 7.4; if (lw0 > ml && lw0 + iw > W - mr) { lrows++; lw0 = ml; } lw0 += iw; });
      var mt = 44 + (lrows - 1) * 20; H += (lrows - 1) * 20;
      var xs = [], ys = [];
      series.forEach(function (s) { s.p.forEach(function (p) { xs.push(p.x); ys.push(p.y); }); });
      var log = cState.log, x0, x1;
      if (log) { x0 = Math.min.apply(0, xs) / 1.3; x1 = Math.max.apply(0, xs) * 1.3; }
      else { x0 = 0; x1 = Math.max.apply(0, xs) * 1.08; }
      var yMax = Math.max.apply(0, ys), yMin = Math.min.apply(0, ys), y0 = yMin > 40 ? Math.floor((yMin - 8) / 10) * 10 : 0;
      var y1 = b.unit === "%" && yMax > 80 ? 100 : linTicks(y0, yMax * 1.1, 5).pop();
      if (y1 < yMax) y1 = yMax * 1.1;
      var X = function (v) { return ml + (log ? (Math.log(v) - Math.log(x0)) / (Math.log(x1) - Math.log(x0)) : (v - x0) / (x1 - x0)) * (W - ml - mr); };
      var Y = function (v) { return H - mb - (v - y0) / (y1 - y0) * (H - mt - mb); };
      var tf = xm === "cost" ? tickMoney : xm === "tok" ? tickK : function (v) { return num(v, v < 10 ? 1 : 0); };
      var g = "";
      linTicks(y0, y1, 5).forEach(function (v) { g += '<line x1="' + ml + '" x2="' + (W - mr) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="' + GRID + '"/><text x="' + (ml - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end" fill="' + MUTED + '">' + fmt(v, b).replace(/\.0(%?)$/, "$1") + "</text>"; });
      (log ? logTicks(x0, x1) : linTicks(x0, x1, 6)).forEach(function (v) { if (X(v) - ml < 18 && v !== x0) return; g += '<line x1="' + X(v) + '" x2="' + X(v) + '" y1="' + mt + '" y2="' + (H - mb) + '" stroke="' + GRID + '"/><text x="' + X(v) + '" y="' + (H - mb + 18) + '" text-anchor="middle" fill="' + MUTED + '">' + tf(v) + "</text>"; });
      g += '<line x1="' + ml + '" x2="' + (W - mr) + '" y1="' + (H - mb) + '" y2="' + (H - mb) + '" stroke="' + AXIS + '"/>';
      g += '<text x="' + ((ml + W - mr) / 2) + '" y="' + (H - 10) + '" text-anchor="middle" fill="' + INK + '">' + esc(XL) + (log ? " · log scale" : "") + "</text>";
      g += '<text transform="translate(16 ' + ((mt + H - mb) / 2) + ') rotate(-90)" text-anchor="middle" fill="' + INK + '">' + esc(b.short || b.name) + "</text>";
      // Label placement: a setting label may not touch another label, any marker or any line segment (V5.40 review fix).
      var boxes = [], segs = [];
      series.forEach(function (s) {
        s.p.forEach(function (p, i) {
          boxes.push([X(p.x) - 7, Y(p.y) - 7, X(p.x) + 7, Y(p.y) + 7]);
          if (i) segs.push([X(s.p[i - 1].x), Y(s.p[i - 1].y), X(p.x), Y(p.y)]);
        });
      });
      function hitBox(bx, o) { return !(bx[2] < o[0] || bx[0] > o[2] || bx[3] < o[1] || bx[1] > o[3]); }
      function hitSeg(bx, sg) {  // segment vs rectangle (Liang-Barsky clip)
        var x0 = sg[0], y0 = sg[1], dx = sg[2] - x0, dy = sg[3] - y0, t0 = 0, t1 = 1;
        var pq = [[-dx, x0 - bx[0]], [dx, bx[2] - x0], [-dy, y0 - bx[1]], [dy, bx[3] - y0]];
        for (var i = 0; i < 4; i++) {
          var p = pq[i][0], q = pq[i][1];
          if (p === 0) { if (q < 0) return false; continue; }
          var r = q / p;
          if (p < 0) { if (r > t1) return false; if (r > t0) t0 = r; } else { if (r < t0) return false; if (r < t1) t1 = r; }
        }
        return true;
      }
      function place(px, py, txt) {
        var w = txt.length * 6.6 + 4, h = 13, cands = [];
        [[8, -6], [8, 16], [-8 - w, -6], [-8 - w, 16], [-w / 2, -11], [-w / 2, 23], [12, 4], [-12 - w, 4], [-w / 2, -24], [-w / 2, 36], [16, -18], [-16 - w, -18], [16, 28], [-16 - w, 28]]
          .forEach(function (c) { cands.push(c); });
        for (var i = 0; i < cands.length; i++) {
          var x = px + cands[i][0], y = py + cands[i][1], bx = [x - 1, y - 11, x + w, y + h - 10];
          if (bx[0] < ml + 2 || bx[2] > W - mr || bx[1] < mt - 2 || bx[3] > H - mb - 2) continue;
          if (boxes.some(function (o) { return hitBox(bx, o); })) continue;
          if (segs.some(function (sg) { return hitSeg(bx, sg); })) continue;
          boxes.push(bx); return [x, y];
        }
        return null;
      }
      var lx = ml, ly = 16;
      series.forEach(function (s) {
        if (lx > ml && lx + 40 + s.m.name.length * 7.4 > W - mr) { lx = ml; ly += 20; }
        g += '<line x1="' + lx + '" x2="' + (lx + 18) + '" y1="' + ly + '" y2="' + ly + '" stroke="' + s.c + '" stroke-width="2"/><circle cx="' + (lx + 9) + '" cy="' + ly + '" r="4.5" fill="' + s.c + '" stroke="#fff" stroke-width="1.5"/>';
        g += '<text x="' + (lx + 24) + '" y="' + (ly + 4) + '" font-size="12.5" font-weight="600" fill="' + INK + '">' + esc(s.m.name) + "</text>";
        lx += 40 + s.m.name.length * 7.4;
      });
      series.forEach(function (s) {
        var d = s.p.map(function (p, i) { return (i ? "L" : "M") + X(p.x).toFixed(1) + "," + Y(p.y).toFixed(1); }).join("");
        if (s.p.length > 1) g += '<path d="' + d + '" fill="none" stroke="' + s.c + '" stroke-width="2" stroke-linejoin="round"/>';
        s.p.forEach(function (p) {
          var t = "<b>" + esc(s.m.name) + "</b>" + (p.set ? " · " + esc(p.set) : "") + "<br>" + esc(b.short || b.name) + ": " + fmt(p.y, b) + "<br>" + XL.replace(/ \(.*\)/, "") + ": " + (xm === "cost" ? money(p.x) : xm === "tok" ? num(p.x, 0) : num(p.x, 1) + " min");
          g += '<circle cx="' + X(p.x).toFixed(1) + '" cy="' + Y(p.y).toFixed(1) + '" r="5" fill="' + s.c + '" stroke="#fff" stroke-width="2"/>';
          g += '<circle cx="' + X(p.x).toFixed(1) + '" cy="' + Y(p.y).toFixed(1) + '" r="12" fill="transparent" tabindex="0" data-tip="' + esc(t) + '"><title>' + esc(t.replace(/<[^>]+>/g, " ")) + "</title></circle>";
          var at = p.set && place(X(p.x), Y(p.y), p.set);
          if (at) g += '<text class="ls-setlab" x="' + at[0].toFixed(1) + '" y="' + at[1].toFixed(1) + '" font-size="11" fill="' + MUTED + '" stroke="#fff" stroke-width="3" stroke-linejoin="round" paint-order="stroke">' + esc(p.set) + "</text>";
        });
      });
      box.innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc($(P + "title").textContent) + '" data-export-title="' + esc($(P + "title").textContent) + '" data-export-caption="' + esc((b.what || "") + " Source: " + b.src + (b.updated ? ", " + b.updated : "") + ".") + '">' + g + "</svg>";
      bindTips(box);
      // data table (accessibility and exact values)
      var rows = series.map(function (s) { return s.p.map(function (p) {
        return "<tr><td>" + esc(s.m.name) + '</td><td>' + esc(p.set || "–") + '</td><td class="num">' + fmt(p.y, b) + '</td><td class="num">' + (xm === "cost" ? money(p.x) : xm === "tok" ? num(p.x, 0) : num(p.x, 1)) + "</td></tr>"; }).join(""); }).join("");
      $(P + "table").innerHTML = '<details><summary>Show the numbers</summary><div class="ll-tablewrap"><table class="ll-mini"><thead><tr><th>Model</th><th>Setting</th><th class="num">' + esc(b.short || b.name) + '</th><th class="num">' + esc(XL) + "</th></tr></thead><tbody>" + rows + "</tbody></table></div></details>";
      if ($(P + "cap")) $(P + "cap").textContent = b.what || "";
      var exportCap = (b.what || "") + " Source: " + b.src + ", " + (b.updated || "") + ".";
      $(P + "note").textContent = (cState.b === "aa_index" ?
        "Source: Artificial Analysis, every reasoning-effort setting it publishes. Time per task is Artificial Analysis's estimate from output tokens and output speed." :
        "Source: " + b.src + ", every setting with a published cost." + (b.derived ? " Cost is derived from the board's totals." : "")) + " Each line joins a model's settings in order of effort, Low to Max; one dot means one published setting. Labels that would overlap are left off; hover a point or open the numbers for every value." + (xm === "cost" && series.some(function (s) { return (s.m.aa || []).some(function (p) { return p.cost == null; }); }) && cState.b === "aa_index" ? " Settings without a published cost (for example GPT-6.2 Sol below Max) are not plotted; switch to output tokens to see them." : "") + (cState.b === "aa_index" ? " Non-reasoning modes are not part of the effort curve." : "");
    }
    function syncCurveControls() {
      var aa = cState.b === "aa_index";
      if (!$(P + "x")) return;
      Array.prototype.forEach.call($(P + "x").options, function (o) { o.disabled = !aa && o.value !== "cost"; });
      if (!aa) { cState.x = "cost"; $(P + "x").value = "cost"; }
    }
    if ($(P + "b")) $(P + "b").addEventListener("change", function () { cState.b = this.value; syncCurveControls(); cPick.set(curveDefaults()); });
    if ($(P + "x")) $(P + "x").addEventListener("change", function () { cState.x = this.value; cPick.render(); drawCurves(); });
    if ($(P + "log")) $(P + "log").addEventListener("change", function () { cState.log = this.checked; drawCurves(); });


    syncCurveControls();
    cPick.set(curveDefaults());
    return { redraw: drawCurves };
  }
  var mainCurves = CurveView("ls-c-", { defaults: ["gemini-4-hydrogen", "claude-sonnet-5-5", "gpt-6-1-terra"] });
  if ($("ls-h-chart")) CurveView("ls-h-", { defaults: ["gpt-6-2-astra", "gpt-6-2-sol", "claude-fable-5-2", "claude-opus-5-5", "gemini-4-carbon", "gemini-4-hydrogen"], log: true });

  // ---------- 2. Compare models ----------
  var kPick = new Picker({
    box: $("ls-k-pick"),
    available: function () { return MODELS.filter(function (m) { return Object.keys(m.s || {}).length; })
      .sort(function (a, b) { return a.name.localeCompare(b.name); }).map(function (m) { return m.id; }); },
    onchange: function () { drawCompare(); }
  });
  function drawCompare() {
    var box = $("ls-k-chart"), sel = kPick.sel;
    var boards = BENCH.filter(function (b) { return sel.filter(function (id) { return MB[id].s[b.id]; }).length >= Math.min(2, sel.length); });
    if (!sel.length || !boards.length) { box.innerHTML = '<p class="ls-empty">Pick at least two models that share a benchmark.</p>'; return; }
    var PW = 270, PH = 190, cols = 3, gapX = 20, gapY = 26, rowsN = Math.ceil(boards.length / cols);
    var W = cols * PW + (cols - 1) * gapX, g = "";
    // legend, wrapped onto as many rows as it needs
    var lx = 0, ly = 10;
    sel.forEach(function (id) {
      var iw = 30 + MB[id].name.length * 7.4;
      if (lx && lx + iw > W) { lx = 0; ly += 22; }
      g += '<circle cx="' + (lx + 6) + '" cy="' + ly + '" r="5" fill="' + kPick.color(id) + '"/><text x="' + (lx + 16) + '" y="' + (ly + 4) + '" fill="' + INK + '" font-size="12.5">' + esc(MB[id].name) + "</text>";
      lx += iw;
    });
    var headH = ly + 20, H = headH + rowsN * (PH + gapY);
    boards.forEach(function (b, bi) {
      var ox = (bi % cols) * (PW + gapX), oy = headH + Math.floor(bi / cols) * (PH + gapY);
      var vals = sel.map(function (id) { var r = MB[id].s[b.id]; return r ? r.v : null; });
      var have = vals.filter(function (v) { return v != null; });
      sel.forEach(function (id) { var r = MB[id].s[b.id]; if (r && r.ci95) { have.push(r.ci95[0]); have.push(r.ci95[1]); } });
      var elo = b.unit === "Elo";
      var lo = elo ? Math.floor((Math.min.apply(0, have) - 30) / 10) * 10 : 0;
      var hi = elo ? Math.ceil((Math.max.apply(0, have) + 20) / 10) * 10 : Math.max.apply(0, have) * 1.18 || 1;
      var top = oy + 62, bot = oy + PH - 22, left = ox + 8, right = ox + PW - 8;
      g += '<rect x="' + ox + '" y="' + oy + '" width="' + PW + '" height="' + PH + '" rx="10" fill="#fff" stroke="' + GRID + '"/>';
      g += '<text x="' + (ox + 12) + '" y="' + (oy + 20) + '" font-weight="600" font-size="13" fill="' + INK + '"><title>' + esc(b.name + ": " + (b.what || "") + " Source: " + b.src) + "</title>" + esc(b.short || b.name) + "</text>";
      g += '<text x="' + (ox + 12) + '" y="' + (oy + 34) + '" font-size="10.5" fill="' + MUTED + '">' + esc(b.section) + (b.hb === false ? " · lower is better" : "") + (elo ? " · axis from " + num(lo, 0) : "") + "</text>";
      var n = sel.length, slotW = (right - left) / n, bw = Math.min(30, slotW - 8), crowd = n >= 5;
      var lab = function (v) {
        if (crowd && b.unit === "USD") return "$" + num(v / 1000, 1) + "K";
        if (crowd && b.unit !== "Elo" && b.unit !== "%" && Math.abs(v) >= 100) return num(v, 0);
        return fmt(v, b);
      };
      sel.forEach(function (id, i) {
        var v = vals[i], cx = left + slotW * (i + 0.5);
        if (v == null) { g += '<text x="' + cx + '" y="' + (bot - 4) + '" text-anchor="middle" font-size="10.5" fill="' + MUTED + '">n/a</text>'; return; }
        var y = bot - (v - lo) / (hi - lo) * (bot - top), r = MB[id].s[b.id];
        var t = "<b>" + esc(MB[id].name) + "</b><br>" + esc(b.name) + ": " + fmt(v, b) + (r.ci95 ? " (95% range " + fmt(r.ci95[0], b) + " to " + fmt(r.ci95[1], b) + ")" : "") + (r.set ? "<br>Setting: " + esc(r.set) : "") + (r.cost != null ? "<br>Cost per task: " + money(r.cost) : "");
        if (elo) {
          g += '<line x1="' + cx + '" x2="' + cx + '" y1="' + bot + '" y2="' + y + '" stroke="' + kPick.color(id) + '" stroke-width="2"/><circle cx="' + cx + '" cy="' + y + '" r="6" fill="' + kPick.color(id) + '" stroke="#fff" stroke-width="2"/>';
        } else {
          var h = Math.max(1, bot - y);
          g += '<path d="M' + (cx - bw / 2) + "," + bot + "V" + (y + 4) + "Q" + (cx - bw / 2) + "," + y + " " + (cx - bw / 2 + 4) + "," + y + "H" + (cx + bw / 2 - 4) + "Q" + (cx + bw / 2) + "," + y + " " + (cx + bw / 2) + "," + (y + 4) + "V" + bot + 'Z" fill="' + kPick.color(id) + '"/>';
          if (h < 4) y = bot - 4;
        }
        if (r.ci95) {  // 95% range
          var Yv = function (q) { return bot - (q - lo) / (hi - lo) * (bot - top); }, ya = Yv(r.ci95[0]), yb = Yv(r.ci95[1]);
          g += '<line x1="' + cx + '" x2="' + cx + '" y1="' + ya.toFixed(1) + '" y2="' + yb.toFixed(1) + '" stroke="' + INK + '" stroke-width="1.5" opacity=".75"/>' +
            '<line x1="' + (cx - 4) + '" x2="' + (cx + 4) + '" y1="' + ya.toFixed(1) + '" y2="' + ya.toFixed(1) + '" stroke="' + INK + '" stroke-width="1.5" opacity=".75"/>' +
            '<line x1="' + (cx - 4) + '" x2="' + (cx + 4) + '" y1="' + yb.toFixed(1) + '" y2="' + yb.toFixed(1) + '" stroke="' + INK + '" stroke-width="1.5" opacity=".75"/>';
          y = Math.min(y, yb);
        }
        g += '<text x="' + cx + '" y="' + (y - 7) + '" text-anchor="middle" font-size="' + (crowd ? 10.5 : 11.5) + '" font-weight="600" fill="' + INK + '">' + lab(v) + "</text>";
        g += '<rect x="' + (cx - slotW / 2) + '" y="' + top + '" width="' + slotW + '" height="' + (bot - top) + '" fill="transparent" tabindex="0" data-tip="' + esc(t) + '"><title>' + esc(t.replace(/<[^>]+>/g, " ")) + "</title></rect>";
      });
      g += '<line x1="' + left + '" x2="' + right + '" y1="' + bot + '" y2="' + bot + '" stroke="' + AXIS + '"/>';
    });
    box.innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Side-by-side comparison of ' + sel.length + ' models on ' + boards.length + ' benchmarks" data-export-title="Model comparison: ' + esc(sel.map(function (id) { return MB[id].name; }).join(" vs ")) + '">' + g + "</svg>";
    bindTips(box);
    $("ls-k-note").textContent = boards.length + " benchmarks where at least two of the selected models have a result. Bars start at zero; Arena boards (Elo-like ratings) are drawn as dots on a range axis, because a zero baseline hides the gaps. Each model is shown at its best published setting. Whiskers show the 95% range where the board publishes a margin of error; overlapping ranges mean the gap may be chance. Hover a panel title for what the benchmark measures.";
  }

  // ---------- 3. Ranking bars ----------
  var rState = { b: D.default_benchmark, n: "15", a: "" };
  function drawRanks() {
    var b = BY[rState.b], box = $("ls-r-chart");
    var list = MODELS.filter(function (m) { return m.s[b.id] && (!rState.a || m.access === rState.a); })
      .sort(function (p, q) { return b.hb === false ? p.s[b.id].v - q.s[b.id].v : q.s[b.id].v - p.s[b.id].v; });
    if (rState.n !== "all") list = list.slice(0, +rState.n);
    $("ls-r-title").textContent = b.name + (rState.a ? " · " + rState.a.toLowerCase() : "") + (rState.n !== "all" ? " · top " + list.length : "");
    if (!list.length) { box.innerHTML = '<p class="ls-empty">No model has a result for this selection.</p>'; return; }
    var elo = b.unit === "Elo", W = 860, lw = 230, rw = 90, bh = 18, gap = 8, top = 10, H = top + list.length * (bh + gap) + 30;
    var vs = list.map(function (m) { return m.s[b.id].v; });
    list.forEach(function (m) { var ci = m.s[b.id].ci95; if (ci) { vs.push(ci[0]); vs.push(ci[1]); } });
    var vmin = Math.min.apply(0, vs), lo = elo ? Math.floor((vmin - 30) / 10) * 10 : Math.min(0, vmin * 1.15), hi = Math.max.apply(0, vs) * (elo ? 1 : 1.02);
    // Statistical tie with #1: the model's 95% range overlaps the leader's (V5.47).
    var lead = list[0].s[b.id], nTied = 0, hasCI = list.some(function (m) { return m.s[b.id].ci95; });
    function tiedWithLead(r) {
      if (r === lead || !r.ci95 || !lead.ci95) return false;
      return b.hb === false ? r.ci95[0] <= lead.ci95[1] : r.ci95[1] >= lead.ci95[0];
    }
    if (elo) hi = Math.ceil((hi + 10) / 10) * 10;
    var X = function (v) { return lw + (v - lo) / (hi - lo) * (W - lw - rw); };
    var g = "";
    linTicks(lo, hi, 6).forEach(function (v) { if (v < lo) return; g += '<line x1="' + X(v) + '" x2="' + X(v) + '" y1="' + (top - 4) + '" y2="' + (H - 24) + '" stroke="' + GRID + '"/><text x="' + X(v) + '" y="' + (H - 8) + '" text-anchor="middle" fill="' + MUTED + '">' + fmt(v, b).replace(/\.0(%?)$/, "$1") + "</text>"; });
    if (!elo && lo < 0) g += '<line x1="' + X(0) + '" x2="' + X(0) + '" y1="' + (top - 4) + '" y2="' + (H - 24) + '" stroke="' + AXIS + '"/>';
    var rank = 0, prev = null;
    list.forEach(function (m, i) {
      var r = m.s[b.id], y = top + i * (bh + gap), c = m.access === "Open weights" ? OPEN : PROP;
      if (r.v !== prev) rank = i + 1; prev = r.v;
      var tied = tiedWithLead(r); if (tied) nTied++;
      var t = "<b>" + esc(m.name) + "</b> · " + esc(m.dev) + "<br>" + esc(b.name) + ": " + fmt(r.v, b) + (r.ci95 ? " (95% range " + fmt(r.ci95[0], b) + " to " + fmt(r.ci95[1], b) + ")" : "") + (tied ? "<br>Statistically tied with #1" : "") + (r.set ? "<br>Setting: " + esc(r.set) : "") + (r.cost != null ? "<br>Cost per task: " + money(r.cost) : "") + "<br>" + esc(m.access);
      g += '<text x="' + (lw - 10) + '" y="' + (y + bh - 4) + '" text-anchor="end" font-size="12.5" fill="' + INK + '"><tspan fill="' + MUTED + '">' + rank + ".  </tspan>" + esc(m.name) + "</text>";
      if (elo) {
        g += '<line x1="' + lw + '" x2="' + X(r.v) + '" y1="' + (y + bh / 2) + '" y2="' + (y + bh / 2) + '" stroke="' + c + '" stroke-width="2"/><circle cx="' + X(r.v) + '" cy="' + (y + bh / 2) + '" r="5.5" fill="' + c + '" stroke="#fff" stroke-width="2"/>';
      } else if (r.v >= 0) {
        var x0 = X(0), w = Math.max(2, X(r.v) - x0);
        g += '<path d="M' + x0 + "," + y + "H" + (x0 + w - 4) + "Q" + (x0 + w) + "," + y + " " + (x0 + w) + "," + (y + 4) + "V" + (y + bh - 4) + "Q" + (x0 + w) + "," + (y + bh) + " " + (x0 + w - 4) + "," + (y + bh) + "H" + x0 + 'Z" fill="' + c + '"/>';
      } else {
        var z = X(0), xl = X(r.v);
        g += '<path d="M' + z + "," + y + "H" + (xl + 4) + "Q" + xl + "," + y + " " + xl + "," + (y + 4) + "V" + (y + bh - 4) + "Q" + xl + "," + (y + bh) + " " + (xl + 4) + "," + (y + bh) + "H" + z + 'Z" fill="' + c + '"/>';
      }
      var labX = (r.v < 0 && !elo ? X(0) : X(r.v)) + 8;
      if (r.ci95) {  // 95% range as a thin whisker with end caps
        var w0 = X(r.ci95[0]), w1 = X(r.ci95[1]), wy = y + bh / 2;
        g += '<line x1="' + w0.toFixed(1) + '" x2="' + w1.toFixed(1) + '" y1="' + wy + '" y2="' + wy + '" stroke="' + INK + '" stroke-width="1.5" opacity=".75"/>' +
          '<line x1="' + w0.toFixed(1) + '" x2="' + w0.toFixed(1) + '" y1="' + (wy - 4) + '" y2="' + (wy + 4) + '" stroke="' + INK + '" stroke-width="1.5" opacity=".75"/>' +
          '<line x1="' + w1.toFixed(1) + '" x2="' + w1.toFixed(1) + '" y1="' + (wy - 4) + '" y2="' + (wy + 4) + '" stroke="' + INK + '" stroke-width="1.5" opacity=".75"/>';
        if (r.v >= 0 || elo) labX = Math.max(labX, w1 + 8);
      }
      g += '<text x="' + labX.toFixed(1) + '" y="' + (y + bh - 4) + '" font-size="12" fill="' + INK + '">' + fmt(r.v, b) + (tied ? '<tspan fill="' + MUTED + '"> ≈ #1</tspan>' : "") + "</text>";
      g += '<rect x="0" y="' + (y - 3) + '" width="' + W + '" height="' + (bh + 6) + '" fill="transparent" tabindex="0" data-tip="' + esc(t) + '"><title>' + esc(t.replace(/<[^>]+>/g, " ")) + "</title></rect>";
    });
    box.innerHTML = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + esc($("ls-r-title").textContent) + '" data-export-title="' + esc($("ls-r-title").textContent) + '">' + g + "</svg>";
    bindTips(box);
    if ($("ls-r-cap")) $("ls-r-cap").textContent = b.what || "";
    box.querySelector("svg").setAttribute("data-export-caption", (b.what || "") + " Source: " + b.src + (b.updated ? ", " + b.updated : "") + "." + (hasCI ? " Whiskers: " + (b.cik || "95% range") + "; ≈ #1 marks a statistical tie with the leader." : ""));
    $("ls-r-note").textContent = "Source: " + b.src + " (" + (b.updated || "") + "). " + (b.hb === false ? "Lower is better. " : "") +
      (hasCI ? "Whiskers show each result's " + (b.cik || "95% range") + "; " + (nTied ? nTied + " model" + (nTied > 1 ? "s are" : " is") + " marked ≈ #1 because the range overlaps the leader's, so the gap to #1 may be chance. " : "no model's range overlaps the leader's. ") : "This board publishes no margin of error. ") + (elo ? "Ratings on an Elo-like scale, so the axis starts at " + num(lo, 0) + " rather than zero. " : "") +
      "Blue: proprietary API; orange: open weights. Each model at its best published setting.";
  }
  ["b", "n", "a"].forEach(function (k) { $("ls-r-" + k).addEventListener("change", function () { rState[k] = this.value; drawRanks(); }); });

  // ---------- tabs ----------
  var tabs = root.querySelectorAll(".ls-tab");
  Array.prototype.forEach.call(tabs, function (t) {
    t.addEventListener("click", function () {
      Array.prototype.forEach.call(tabs, function (u) { var on = u === t; u.setAttribute("aria-selected", on); $(u.getAttribute("aria-controls")).hidden = !on; });
    });
  });

  // ---------- PNG download for every chart on the page ----------
  function savePNG(svg, name, title, caption) {
    var vb = svg.viewBox.baseVal, w = vb && vb.width ? vb.width : svg.clientWidth, h = vb && vb.height ? vb.height : svg.clientHeight;
    var pad = 24, foot = 26, scale = 2, lines = [];
    if (title) {  // wrap the title to the image width (about 10px per character at 18px)
      var maxc = Math.max(30, Math.floor(w / 10)), cur = "";
      title.split(" ").forEach(function (wd) { if ((cur + " " + wd).trim().length > maxc && cur) { lines.push(cur); cur = wd; } else cur = (cur + " " + wd).trim(); });
      if (cur) lines.push(cur);
    }
    var head = lines.length ? 16 + lines.length * 24 : 0, caps = [];
    if (caption) {  // caption under the chart: what the benchmark measures and where the data comes from (~6.4px per character at 12px)
      var mc = Math.max(40, Math.floor(w / 6.4)), cc = "";
      caption.split(" ").forEach(function (wd) { if ((cc + " " + wd).trim().length > mc && cc) { caps.push(cc); cc = wd; } else cc = (cc + " " + wd).trim(); });
      if (cc) caps.push(cc);
    }
    foot += caps.length * 17;
    var clone = svg.cloneNode(true);
    clone.querySelectorAll("[data-tip],title").forEach(function (n) { if (n.tagName.toLowerCase() === "title") n.remove(); });
    var font = getComputedStyle(svg.querySelector("text") || svg).fontFamily || "Arial, sans-serif";
    var wrap = document.createElementNS(NS, "svg");
    wrap.setAttribute("xmlns", NS); wrap.setAttribute("width", w + pad * 2); wrap.setAttribute("height", h + pad * 2 + head + foot);
    wrap.setAttribute("style", "font-family:" + font + ";font-size:12px");
    wrap.innerHTML = '<rect width="100%" height="100%" fill="#ffffff"/>' +
      lines.map(function (ln, i) { return '<text x="' + pad + '" y="' + (pad + 18 + i * 24) + '" font-size="18" font-weight="600" fill="' + INK + '">' + esc(ln) + "</text>"; }).join("") +
      caps.map(function (ln, i) { return '<text x="' + pad + '" y="' + (h + pad * 2 + head + 6 + i * 17) + '" font-size="12" fill="' + INK + '">' + esc(ln) + "</text>"; }).join("") +
      '<text x="' + pad + '" y="' + (h + pad * 2 + head + 10 + caps.length * 17) + '" font-size="11" fill="' + MUTED + '">Chmltech LLM leaderboard · data as of ' + esc(D.as_of) + " · chmltech.com/llm-leaderboard</text>";
    clone.setAttribute("x", pad); clone.setAttribute("y", pad + head); clone.setAttribute("width", w); clone.setAttribute("height", h);
    // carry over page CSS that styles SVG text (token figure, explorer chart)
    clone.querySelectorAll("text").forEach(function (t) {
      var cs = getComputedStyle(svg.querySelectorAll("text")[0] || t);
      if (!t.getAttribute("fill")) t.setAttribute("fill", cs.fill && cs.fill !== "none" ? cs.fill : INK);
      if (!t.getAttribute("font-size")) t.setAttribute("font-size", cs.fontSize || "12px");
    });
    wrap.appendChild(clone);
    var data = new XMLSerializer().serializeToString(wrap);
    var img = new Image();
    img.onload = function () {
      var cv = document.createElement("canvas");
      cv.width = (w + pad * 2) * scale; cv.height = (h + pad * 2 + head + foot) * scale;
      var cx = cv.getContext("2d"); cx.scale(scale, scale); cx.drawImage(img, 0, 0);
      cv.toBlob(function (blob) {
        var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name + ".png";
        document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
      }, "image/png");
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(data);
  }
  function slug(s) { return String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 70); }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("[data-png]") : null;
    if (!btn) return;
    var host = document.getElementById(btn.getAttribute("data-png")), svg = host && host.querySelector("svg");
    if (!svg) return;
    var title = svg.getAttribute("data-export-title") || btn.getAttribute("data-title") || (document.getElementById("ll-chart-title") || {}).textContent || "";
    savePNG(svg, "chmltech-" + slug(title || "chart") + "-" + D.as_of, title, svg.getAttribute("data-export-caption") || btn.getAttribute("data-caption") || "");
  });
  // add a download button to the explorer's score-vs-cost chart
  var head = document.querySelector(".ll-charthead");
  if (head && !head.querySelector("[data-png]")) {
    var bt = document.createElement("button");
    bt.type = "button"; bt.className = "btn btn-ghost ls-png"; bt.setAttribute("data-png", "ll-chart"); bt.textContent = "Download PNG";
    head.appendChild(bt);
  }

  // ---------- start ----------
  kPick.set(["gemini-4-hydrogen", "claude-sonnet-5-5", "gpt-6-1-terra"]);
  drawRanks();
})();
