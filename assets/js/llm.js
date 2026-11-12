/* Chmltech LLM Leaderboard (llm-leaderboard.html). Vanilla JS, no network.
   Reads the embedded dataset (#llm-data) and draws the leaderboard, the agent-type rankings and the
   score-versus-cost Pareto chart. State is kept in the URL hash. */
(function () {
  "use strict";
  var root = document.getElementById("ll-root");
  var dataEl = document.getElementById("llm-data");
  if (!root || !dataEl) return;
  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var MODELS = D.models, BENCH = D.benchmarks, GROUPS = D.groups;
  var BY = {};
  BENCH.forEach(function (b) { BY[b.id] = b; });

  var $ = function (id) { return document.getElementById(id); };
  var q = $("ll-q"), benchSel = $("ll-bench"), axisSel = $("ll-axis"), untested = $("ll-untested");
  var countEl = $("ll-count"), tbody = $("ll-tbody"), benchBox = $("ll-benchbox"), scoreTh = $("ll-score-th");
  var panelTable = $("ll-panel-table"), panelChart = $("ll-panel-chart"), chartEl = $("ll-chart"), frontEl = $("ll-front");
  var chartTitle = $("ll-chart-title"), empty = $("ll-empty"), form = root.querySelector(".gr-form");
  var panel = $("gr-filters"), toggleBtn = root.querySelector(".gr-filter-btn"), badge = root.querySelector("[data-active-n]");
  var closeN = root.querySelector("[data-close-n]"), chipsEl = root.querySelector(".gr-chips");
  var tabs = root.querySelectorAll(".ll-tab");
  var CHECKS = ["d", "a", "t", "c"];
  var LABEL = { d: "Developer", a: "Access", t: "Model type", c: "Capability" };
  var view = "table", sortKey = "score", sortDir = -1, openId = null;

  MODELS.forEach(function (m) {
    m._text = [m.name, m.dev, m.tier, m.access, m.license, (m.caps || []).join(" ")].join(" ").toLowerCase();
    m.blend = (m.pin != null && m.pout != null) ? (3 * m.pin + m.pout) / 4 : null;
  });

  /* ---------- formatting ---------- */
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fmtScore(v, b) {
    if (v == null) return "–";
    var u = b.unit || "";
    if (u === "%") return (Math.round(v * 10) / 10).toFixed(1) + "%";
    if (u === "USD") return money(v);
    var s = Math.abs(v) >= 100 ? String(Math.round(v)) : String(Math.round(v * 10) / 10);
    return s + (u && u !== "Elo" && u !== "points" ? " " + u : "");
  }
  function money(v) {
    if (v == null) return "–";
    if (v === 0) return "$0";
    if (v >= 100) return "$" + Math.round(v).toLocaleString("en-CA");
    if (v >= 1) return "$" + v.toFixed(2);
    if (v >= 0.1) return "$" + v.toFixed(2);
    return "$" + v.toFixed(3);
  }
  function ctx(n) {
    if (!n) return "–";
    if (n >= 1e6) return (Math.round(n / 1e5) / 10) + "M";
    return Math.round(n / 1000) + "K";
  }
  /* "95% CI 1516.36 to 1535.55" -> "95% CI 1,516 to 1,536"; "stderr 0.0128" on a fraction board -> "± 1.3" */
  function ciText(c, b) {
    var m = /^95% CI ([\d.-]+) to ([\d.-]+)$/.exec(c);
    if (m) return "95% CI " + fmtScore(+m[1] * (b.unit === "%" && +m[2] <= 1 ? 100 : 1), b) + " to " + fmtScore(+m[2] * (b.unit === "%" && +m[2] <= 1 ? 100 : 1), b);
    m = /^stderr ([\d.]+)$/.exec(c);
    if (m) return "± " + (+m[1] * (b.unit === "%" && +m[1] < 1 && b.id !== "vals" ? 100 : 1)).toFixed(1) + " (std. error)";
    return c;
  }
  function month(d) {
    if (!d) return "–";
    var p = d.split("-"), M = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    return (p[1] ? M[+p[1] - 1] + " " : "") + p[0];
  }

  /* ---------- state ---------- */
  function selected(g) {
    var out = [];
    Array.prototype.forEach.call(root.querySelectorAll('input[type="checkbox"][name="' + g + '"]'), function (b) { if (b.checked) out.push(b.value); });
    return out;
  }
  function radio(n) { var r = root.querySelector('input[name="' + n + '"]:checked'); return r ? r.value : ""; }
  function state() {
    var s = { q: q.value.trim().toLowerCase(), b: benchSel.value, x: axisSel.value, ctx: +radio("ctx") || 0, price: +radio("price") || 0 };
    CHECKS.forEach(function (g) { s[g] = selected(g); });
    return s;
  }
  function field(m, g) {
    if (g === "d") return [m.dev];
    if (g === "a") return [m.access];
    if (g === "t") return [m.tier];
    return m.caps || [];
  }
  function pass(m, s, skip) {
    if (s.q && m._text.indexOf(s.q) < 0) return false;
    if (s.ctx && !(m.ctx >= s.ctx)) return false;
    if (s.price && !(m.blend != null && m.blend <= s.price)) return false;
    for (var i = 0; i < CHECKS.length; i++) {
      var g = CHECKS[i], sel = s[g];
      if (g === skip || !sel.length) continue;
      var f = field(m, g), ok;
      if (g === "c") { ok = sel.every(function (v) { return f.indexOf(v) > -1; }); }   // capabilities: must have all
      else { ok = sel.some(function (v) { return f.indexOf(v) > -1; }); }
      if (!ok) return false;
    }
    return true;
  }
  function score(m, bid) { var r = m.s && m.s[bid]; return r ? r.v : null; }
  function better(a, b, bench) { return bench.hb === false ? a < b : a > b; }
  function xval(m, s) {
    if (s.x === "task") { var r = m.s && m.s[s.b]; return r && r.cost != null ? r.cost : null; }
    if (s.x === "out") return m.pout;
    if (s.x === "in") return m.pin;
    return m.blend;
  }
  var XLABEL = { blend: "Blended price, US$ per 1M tokens (3 input : 1 output)", out: "Output price, US$ per 1M tokens", "in": "Input price, US$ per 1M tokens", task: "Cost per task, US$ (as published by the benchmark)", taskd: "Cost per task, US$ (derived from the published total)" };

  /* Pareto frontier: cheapest first, keep each model that beats every cheaper model's score. */
  function frontier(pts, bench) {
    var a = pts.slice().sort(function (p, r) { return p.x - r.x || (p.y === r.y ? 0 : better(p.y, r.y, bench) ? -1 : 1); });
    var out = [], best = null;
    a.forEach(function (p) { if (best === null || better(p.y, best, bench)) { out.push(p); best = p.y; } });
    return out;
  }

  /* ---------- leaderboard ---------- */
  function chips(m, isFront) {
    var c = "";
    if (isFront) c += '<span class="ll-chip ll-chip-front" title="No cheaper model in this list scores higher on this benchmark">Best value</span>';
    if (m.access === "Open weights") c += '<span class="ll-chip ll-chip-open">Open weights</span>';
    if (m.tier) c += '<span class="ll-chip">' + esc(m.tier) + "</span>";
    return c ? '<span class="ll-chips">' + c + "</span>" : "";
  }
  function detail(m) {
    var specs = [["Developer", m.dev], ["Access", m.access + (m.license ? " (" + m.license + ")" : "")], ["Parameters", m.params], ["Released", month(m.released)],
      ["Status", m.status], ["Context window", m.ctx ? m.ctx.toLocaleString("en-CA") + " tokens" : null], ["Maximum output", m.maxout ? m.maxout.toLocaleString("en-CA") + " tokens" : null],
      ["Accepts", (m.inp || []).join(", ")], ["Reasoning mode", m.reasoning], ["Knowledge cut-off", m.cutoff],
      ["List price", m.pin != null ? money(m.pin) + " input / " + money(m.pout) + " output per 1M tokens" + (m.pprov ? " (" + m.pprov + ")" : "") : null]];
    var dl = specs.filter(function (r) { return r[1]; }).map(function (r) { return "<dt>" + r[0] + "</dt><dd>" + esc(r[1]) + "</dd>"; }).join("");
    var src = [];
    if (m.surl) src.push('<a href="' + esc(m.surl) + '" target="_blank" rel="noopener">Specification source</a>');
    if (m.purl && m.purl !== m.surl) src.push('<a href="' + esc(m.purl) + '" target="_blank" rel="noopener">Price source</a>');
    var rows = BENCH.filter(function (b) { return m.s && m.s[b.id]; }).map(function (b) {
      var r = m.s[b.id];
      return "<tr><td>" + esc(b.name) + (r.self ? '<span class="ll-self" title="Reported by the developer, not the benchmark maintainer">Developer-reported</span>' : "") +
        (r.set ? '<span class="ll-sub">' + esc(r.set) + "</span>" : "") + (r.flag ? '<span class="ll-sub ll-warn" title="' + esc(r.flag) + '">Pre-launch result</span>' : "") + '</td><td class="num">' + fmtScore(r.v, b) + (r.ci ? '<span class="ll-sub">' + esc(ciText(r.ci, b)) + "</span>" : "") + '</td><td class="num">' + (r.cost != null ? money(r.cost) + (b.derived ? '<span class="ll-sub">derived</span>' : "") : "–") +
        '</td><td><a href="' + esc(r.url) + '" target="_blank" rel="noopener" aria-label="Source for ' + esc(b.name) + '">Source</a></td></tr>';
    }).join("");
    return '<div class="ll-dgrid"><div><h4>Specifications</h4><dl class="ll-specs">' + dl + "</dl>" + (src.length ? '<p class="ll-note">' + src.join(" · ") + "</p>" : "") +
      (m.notes ? '<p class="ll-note">' + esc(m.notes) + "</p>" : "") + "</div><div><h4>Benchmark results</h4>" +
      (rows ? '<table class="ll-mini"><thead><tr><th>Benchmark</th><th class="num">Score</th><th class="num">Cost per task</th><th>Link</th></tr></thead><tbody>' + rows + "</tbody></table>" : '<p class="ll-note">No independent benchmark results recorded yet.</p>') +
      "</div></div>";
  }
  function sortVal(m, key, s) {
    if (key === "score") return score(m, s.b);
    if (key === "blend") return m.blend;
    if (key === "ctx") return m.ctx || null;
    if (key === "released") return m.released || null;
    return m.name.toLowerCase();
  }
  function renderTable(list, s, frontIds) {
    var bench = BY[s.b];
    var rows = list.slice();
    var dir = sortDir;
    rows.sort(function (a, b) {
      var x = sortVal(a, sortKey, s), y = sortVal(b, sortKey, s);
      if (x == null && y == null) return a.name < b.name ? -1 : 1;
      if (x == null) return 1;
      if (y == null) return -1;
      var d = x < y ? -1 : x > y ? 1 : 0;
      if (sortKey === "score" && bench.hb === false) d = -d;
      return d * dir || (a.name < b.name ? -1 : 1);
    });
    // rank by score within the filtered list, whatever the sort order
    var ranked = list.filter(function (m) { return score(m, s.b) != null; }).sort(function (a, b) { return better(score(a, s.b), score(b, s.b), bench) ? -1 : 1; });
    var rank = {}, vals = ranked.map(function (m) { return score(m, s.b); });
    ranked.forEach(function (m, i) { rank[m.id] = (i && score(ranked[i - 1], s.b) === score(m, s.b)) ? rank[ranked[i - 1].id] : i + 1; });
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
    var h = "";
    rows.forEach(function (m) {
      var v = score(m, s.b), r = m.s && m.s[s.b];
      if (v == null && untested.checked) return;
      var w = v == null ? 0 : hi === lo ? 100 : Math.round(12 + 88 * (bench.hb === false ? (hi - v) : (v - lo)) / (hi - lo));
      var isFront = frontIds[m.id];
      h += '<tr class="ll-row' + (isFront ? " is-front" : "") + '" data-id="' + esc(m.id) + '">' +
        '<td class="ll-rank">' + (rank[m.id] || "–") + "</td>" +
        '<td><button type="button" class="ll-name" aria-expanded="' + (openId === m.id) + '">' + esc(m.name) + '</button><span class="ll-dev">' + esc(m.dev) + "</span>" + chips(m, isFront) + "</td>" +
        '<td class="num">' + (v == null ? '<span class="ll-none">Not tested</span>' : '<span class="ll-score">' + fmtScore(v, bench) + "</span>" + (r.set ? '<span class="ll-sub">' + esc(r.set) + "</span>" : "") + (r.flag ? '<span class="ll-sub ll-warn">Pre-launch result</span>' : "") + '<span class="ll-bar"><i style="width:' + w + '%"></i></span>') + "</td>" +
        '<td class="num">' + (m.blend != null ? money(m.blend) + '<span class="ll-sub">' + money(m.pin) + " in / " + money(m.pout) + " out</span>" : '<span class="ll-none">–</span>') + "</td>" +
        '<td class="num ll-hide-m">' + ctx(m.ctx) + "</td>" +
        '<td class="num ll-hide-m">' + month(m.released) + "</td></tr>";
      if (openId === m.id) h += '<tr class="ll-detail"><td colspan="6">' + detail(m) + "</td></tr>";
    });
    tbody.innerHTML = h;
    scoreTh.textContent = bench.short || bench.name;
    Array.prototype.forEach.call(root.querySelectorAll(".ll-th"), function (b) {
      if (b.getAttribute("data-sort") === sortKey) b.setAttribute("aria-sort", sortDir < 0 ? "descending" : "ascending"); else b.removeAttribute("aria-sort");
    });
    return ranked.length;
  }

  /* ---------- chart ---------- */
  function ticksLog(lo, hi) {
    var out = [], e = Math.floor(Math.log(lo) / Math.LN10), steps = [1, 2, 5];
    for (; e <= Math.ceil(Math.log(hi) / Math.LN10); e++) steps.forEach(function (k) { var v = k * Math.pow(10, e); if (v >= lo && v <= hi) out.push(v); });
    if (out.length > 9) out = out.filter(function (v) { return /^1/.test(v.toExponential()); });
    return out;
  }
  function ticksLin(lo, hi, n) {
    var span = hi - lo || 1, step = Math.pow(10, Math.floor(Math.log(span / n) / Math.LN10)), err = span / n / step;
    step *= err >= 7.5 ? 10 : err >= 3.5 ? 5 : err >= 1.5 ? 2 : 1;
    var out = [], v = Math.ceil(lo / step) * step;
    for (; v <= hi + 1e-9; v += step) out.push(Math.round(v * 1e6) / 1e6);
    return out;
  }
  function tickMoney(v) { return v >= 1 ? "$" + (v >= 1000 ? (v / 1000) + "K" : v) : "$" + v.toFixed(v < 0.1 ? (v < 0.01 ? 3 : 2) : 1); }
  var tip, pinned = null;
  function renderChart(list, s) {
    var bench = BY[s.b];
    var pts = [];
    list.forEach(function (m) {
      var r = m.s && m.s[s.b];
      if (s.x === "task" && r && r.alt) { r.alt.forEach(function (a) { if (a[1] > 0) pts.push({ m: m, x: a[1], y: a[0], set: a[2] }); }); return; }
      var x = xval(m, s), y = score(m, s.b); if (x != null && x > 0 && y != null) pts.push({ m: m, x: x, y: y, set: r && r.set });
    });
    chartTitle.textContent = (bench.short || bench.name) + " versus " + (s.x === "task" ? (bench.id === "tbench" ? "cost per trial" : "cost per task") : "price");
    var plotted = {}; pts.forEach(function (p) { plotted[p.m.id] = 1; });
    var missing = list.filter(function (m) { return score(m, s.b) != null && !plotted[m.id]; }).length;
    if (pts.length < 2) {
      chartEl.innerHTML = '<p class="ll-empty">Fewer than two models in this selection have both a result on this benchmark and a ' + (s.x === "task" ? "published cost per task" : "list price") + ". Choose another benchmark or cost measure, or remove a filter.</p>";
      frontEl.innerHTML = ""; return {};
    }
    var fr = frontier(pts, bench), fid = {}, mid = {};
    function key(p) { return p.m.id + "|" + p.x + "|" + p.y; }
    fr.forEach(function (p) { fid[key(p)] = 1; mid[p.m.id] = 1; });
    var W = Math.max(320, chartEl.clientWidth || 760), H = W < 520 ? 360 : 470, ml = 52, mr = 18, mt = 16, mb = 46;
    var xs = pts.map(function (p) { return p.x; }), ys = pts.map(function (p) { return p.y; });
    var x0 = Math.min.apply(null, xs) / 1.5, x1 = Math.max.apply(null, xs) * 1.5;
    var yl = Math.min.apply(null, ys), yh = Math.max.apply(null, ys), pad = (yh - yl || 1) * 0.1; yl -= pad; yh += pad;
    var X = function (v) { return ml + (Math.log(v) - Math.log(x0)) / (Math.log(x1) - Math.log(x0)) * (W - ml - mr); };
    var Y = function (v) { var t = (v - yl) / (yh - yl); if (bench.hb === false) t = 1 - t; return H - mb - t * (H - mt - mb); };
    var g = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Scatter chart of ' + esc(bench.name) + " against cost for " + pts.length + ' models. The models on the Pareto frontier are listed in the table below.">';
    ticksLin(yl, yh, 5).forEach(function (v) { g += '<line x1="' + ml + '" x2="' + (W - mr) + '" y1="' + Y(v) + '" y2="' + Y(v) + '" stroke="#E4E1D8"/><text x="' + (ml - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end">' + fmtScore(v, bench).replace(/\.0%/, "%") + "</text>"; });
    ticksLog(x0, x1).forEach(function (v) { g += '<line x1="' + X(v) + '" x2="' + X(v) + '" y1="' + mt + '" y2="' + (H - mb) + '" stroke="#EFEDE6"/><text x="' + X(v) + '" y="' + (H - mb + 18) + '" text-anchor="middle">' + tickMoney(v) + "</text>"; });
    g += '<line x1="' + ml + '" x2="' + (W - mr) + '" y1="' + (H - mb) + '" y2="' + (H - mb) + '" stroke="#B9C0CC"/>';
    g += '<text class="ll-axt" x="' + ((ml + W - mr) / 2) + '" y="' + (H - 6) + '" text-anchor="middle">' + esc(XLABEL[s.x === "task" && bench.derived ? "taskd" : s.x]) + " · log scale</text>";
    // frontier step line
    var d = "";
    fr.forEach(function (p, i) { d += (i ? "H" + X(p.x) + "V" + Y(p.y) : "M" + X(p.x) + "," + Y(p.y)); });
    d += "H" + (W - mr);
    g += '<path d="' + d + '" fill="none" stroke="#0B2A5A" stroke-width="2" stroke-linejoin="round"/>';
    function mark(p, on) {
      var cx = X(p.x), cy = Y(p.y), open = p.m.access === "Open weights", col = open ? "#C2571A" : "#0B6FA4", r = on ? 6 : 5;
      var a = ' fill="' + col + '" stroke="#fff" stroke-width="2" opacity="' + (on ? 1 : 0.5) + '"';
      return open ? '<rect x="' + (cx - r) + '" y="' + (cy - r) + '" width="' + 2 * r + '" height="' + 2 * r + '" transform="rotate(45 ' + cx + " " + cy + ')"' + a + "/>" : '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '"' + a + "/>";
    }
    pts.forEach(function (p) { if (!fid[key(p)]) g += mark(p, false); });
    fr.forEach(function (p) { g += mark(p, true); });
    // direct labels for frontier points, skipping any that would collide
    var boxes = [];
    fr.slice().reverse().forEach(function (p) {
      var lab = p.m.name + (s.x === "task" && p.set ? " · " + p.set : ""), w = lab.length * 6.6 + 6, cx = X(p.x), cy = Y(p.y);
      var opts = [[cx - 9 - w, cy - 18, "end", cx - 9], [cx + 10, cy + 6, "start", cx + 10], [cx - 9 - w, cy + 6, "end", cx - 9]];
      for (var i = 0; i < opts.length; i++) {
        var b = { x: opts[i][0], y: opts[i][1], w: w, h: 15 };
        if (b.x < 2 || b.x + w > W - 2 || b.y < 2) continue;
        if (boxes.some(function (o) { return b.x < o.x + o.w && o.x < b.x + b.w && b.y < o.y + o.h && o.y < b.y + b.h; })) continue;
        if (pts.some(function (o) { return o !== p && X(o.x) > b.x - 6 && X(o.x) < b.x + w + 6 && Y(o.y) > b.y - 6 && Y(o.y) < b.y + 21; })) continue;
        boxes.push(b);
        g += '<text class="ll-lab" x="' + opts[i][3] + '" y="' + (b.y + 12) + '" text-anchor="' + opts[i][2] + '" paint-order="stroke" stroke="#fff" stroke-width="3">' + esc(lab) + "</text>";
        break;
      }
    });
    g += '<circle id="ll-hl" r="10" fill="none" stroke="#0B2A5A" stroke-width="2" visibility="hidden"/></svg>';
    chartEl.innerHTML = g + '<div class="ll-tip" hidden></div>';
    tip = chartEl.querySelector(".ll-tip");
    var svg = chartEl.querySelector("svg"), hl = chartEl.querySelector("#ll-hl");
    function nearest(ev) {
      var r = svg.getBoundingClientRect(), k = W / r.width, px = (ev.clientX - r.left) * k, py = (ev.clientY - r.top) * k, best = null, bd = 40 * 40;
      pts.forEach(function (p) { var dx = X(p.x) - px, dy = Y(p.y) - py, dd = dx * dx + dy * dy; if (dd < bd) { bd = dd; best = p; } });
      return best;
    }
    function show(p) {
      if (!p) { tip.hidden = true; hl.setAttribute("visibility", "hidden"); return; }
      var r = svg.getBoundingClientRect(), k = r.width / W, cx = X(p.x) * k, cy = Y(p.y) * k;
      hl.setAttribute("cx", X(p.x)); hl.setAttribute("cy", Y(p.y)); hl.setAttribute("visibility", "visible");
      tip.innerHTML = "<b>" + esc(p.m.name) + "</b><span>" + esc(p.m.dev) + " · " + esc(p.m.access) + "</span><br>" + esc(bench.short || bench.name) + ": " + fmtScore(p.y, bench) +
        (p.set ? " <span>(" + esc(p.set) + ")</span>" : "") + "<br>" + (s.x === "task" ? (bench.id === "tbench" ? "Cost per trial: " : "Cost per task: ") : s.x === "blend" ? "Blended price: " : s.x === "out" ? "Output price: " : "Input price: ") + money(p.x) +
        (s.x !== "task" && p.m.pnote ? "<br><span>" + esc(p.m.pnote) + "</span>" : "") +
        (fid[key(p)] ? "<br><span>On the Pareto frontier</span>" : "");
      tip.hidden = false;
      var tw = tip.offsetWidth, th = tip.offsetHeight, left = cx + 14, top = cy - th - 10;
      if (left + tw > r.width) left = cx - tw - 14;
      if (left < 0) left = 0;
      if (top < 0) top = cy + 14;
      tip.style.left = left + "px"; tip.style.top = top + "px";
    }
    svg.addEventListener("mousemove", function (ev) { if (!pinned) show(nearest(ev)); });
    svg.addEventListener("mouseleave", function () { if (!pinned) show(null); });
    svg.addEventListener("click", function (ev) { var p = nearest(ev); pinned = p && pinned !== p ? p : null; show(pinned); });
    pinned = null;
    // frontier table
    var t = '<h3>On the Pareto frontier (' + fr.length + ')</h3><div class="ll-tablewrap"><table class="ll-table"><thead><tr><th>Model</th><th class="num">' + esc(bench.short || bench.name) + '</th><th class="num">' + (s.x === "task" ? (bench.id === "tbench" ? "Cost per trial" : "Cost per task") : "Price per 1M tokens") + '</th><th class="num ll-hide-m">Step up from the cheaper option</th></tr></thead><tbody>';
    fr.forEach(function (p, i) {
      var prev = fr[i - 1], step = "Cheapest in this list";
      if (prev) { var dy = Math.abs(p.y - prev.y), ratio = p.x / prev.x; step = (ratio >= 10 ? Math.round(ratio) : ratio.toFixed(1)) + "× the cost for " + (bench.hb === false ? "−" : "+") + fmtScore(dy, bench); }
      t += '<tr><td><button type="button" class="ll-name" data-open="' + esc(p.m.id) + '">' + esc(p.m.name) + '</button><span class="ll-dev">' + esc(p.m.dev) + " · " + esc(p.m.access) + '</span></td><td class="num"><span class="ll-score">' + fmtScore(p.y, bench) + '</span>' + (p.set ? '<span class="ll-sub">' + esc(p.set) + '</span>' : '') + '</td><td class="num">' + money(p.x) + (s.x !== "task" && p.m.pnote ? '<span class="ll-sub ll-warn">Introductory or conditional price; see details</span>' : '') + '</td><td class="num ll-hide-m">' + step + "</td></tr>";
    });
    t += "</tbody></table></div>" + '<p class="ll-chartnote">A model is on the frontier when no cheaper model in the current selection scores higher. ' + pts.length + " models are plotted" + (missing > 0 ? "; " + missing + " with a result but no " + (s.x === "task" ? "published cost per task" : "list price") + " are left out" : "") + ". " + (s.x === "task" ? "Each published setting of a model is plotted as its own point. " : "Per-token price ignores how many tokens each setting uses; switch the cost measure to cost per task where a benchmark publishes it. ") + "Changing a filter redraws the frontier.</p>";
    frontEl.innerHTML = t;
    return mid;
  }

  /* ---------- filters UI ---------- */
  function updateCounts(s) {
    CHECKS.forEach(function (g) {
      var c = {};
      MODELS.forEach(function (m) { if (pass(m, s, g)) field(m, g).forEach(function (v) { c[v] = (c[v] || 0) + 1; }); });
      Array.prototype.forEach.call(root.querySelectorAll('input[name="' + g + '"]'), function (b) {
        var lab = b.closest(".gr-opt"), n = c[b.value] || 0;
        lab.querySelector("[data-n]").textContent = n;
        lab.classList.toggle("gr-zero", !n && !b.checked);
      });
      var gs = root.querySelector('.gr-group[data-group="' + g + '"] [data-sel]');
      if (gs) { gs.hidden = !s[g].length; gs.textContent = s[g].length; }
    });
  }
  function chipHtml(label, attrs) {
    return '<li><button type="button" class="gr-chip" ' + attrs + ' aria-label="Remove filter: ' + esc(label) + '"><span>' + esc(label) + '</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></li>';
  }
  function renderChips(s) {
    var h = "", n = 0;
    CHECKS.forEach(function (g) { s[g].forEach(function (v) { n++; h += chipHtml(LABEL[g] + ": " + v, 'data-g="' + g + '" data-v="' + esc(v) + '"'); }); });
    if (s.ctx) { n++; h += chipHtml("Context: at least " + ctx(s.ctx), 'data-r="ctx"'); }
    if (s.price) { n++; h += chipHtml("Price: up to $" + s.price + " per 1M", 'data-r="price"'); }
    if (s.q) { n++; h += chipHtml("Search: " + s.q, 'data-r="q"'); }
    chipsEl.innerHTML = h; chipsEl.hidden = !n;
    if (badge) { badge.hidden = !n; badge.textContent = n; }
    Array.prototype.forEach.call(root.querySelectorAll("[data-clear]"), function (b) { if (b.closest(".gr-statusbar")) b.hidden = !n; });
  }
  function writeHash(s) {
    var p = [];
    if (s.b !== D.default_benchmark) p.push("b=" + encodeURIComponent(s.b));
    if (view !== "table") p.push("v=" + view);
    if (s.x !== "blend") p.push("x=" + s.x);
    if (s.q) p.push("q=" + encodeURIComponent(s.q));
    CHECKS.forEach(function (g) { if (s[g].length) p.push(g + "=" + s[g].map(encodeURIComponent).join("|")); });
    if (s.ctx) p.push("ctx=" + s.ctx);
    if (s.price) p.push("price=" + s.price);
    try { history.replaceState(null, "", p.length ? "#" + p.join("&") : location.pathname + location.search); } catch (e) {}
  }
  function readHash() {
    var h = location.hash.replace(/^#/, "");
    if (!h || h.indexOf("=") < 0) return;
    h.split("&").forEach(function (kv) {
      var i = kv.indexOf("="), k = kv.slice(0, i), v = kv.slice(i + 1);
      if (k === "b" && BY[decodeURIComponent(v)]) benchSel.value = decodeURIComponent(v);
      else if (k === "v" && v === "chart") view = "chart";
      else if (k === "x") axisSel.value = v;
      else if (k === "q") q.value = decodeURIComponent(v);
      else if (k === "ctx" || k === "price") { var r = root.querySelector('input[name="' + k + '"][value="' + v + '"]'); if (r) r.checked = true; }
      else if (CHECKS.indexOf(k) > -1) v.split("|").map(decodeURIComponent).forEach(function (x) {
        Array.prototype.forEach.call(root.querySelectorAll('input[name="' + k + '"]'), function (b) { if (b.value === x) b.checked = true; });
      });
    });
  }

  function update() {
    var s = state(), bench = BY[s.b];
    // cost per task is only offered when the benchmark publishes it
    var taskOpt = axisSel.querySelector('option[value="task"]');
    taskOpt.disabled = !bench.cost;
    if (!bench.cost && s.x === "task") { axisSel.value = "blend"; s.x = "blend"; }
    var list = MODELS.filter(function (m) { return pass(m, s); });
    benchBox.innerHTML = "<strong>" + esc(bench.name) + "</strong><span>" + esc(bench.what) + (bench.caveat ? " " + esc(bench.caveat) : "") + '</span><span>Source: <a href="' + esc(bench.url) + '" target="_blank" rel="noopener">' + esc(bench.src) + "</a>" + (bench.updated ? " · " + esc(bench.updated) : "") + (bench.hb === false ? " · lower is better" : "") + "</span>";
    var fid = renderChart(list, s);
    var ranked = renderTable(list, s, fid);
    var shown = untested.checked ? ranked : list.length;
    countEl.textContent = shown + (shown === 1 ? " model" : " models") + (untested.checked && list.length > ranked ? " · " + (list.length - ranked) + " more match but have no result on this benchmark" : "");
    if (closeN) closeN.textContent = shown;
    empty.hidden = shown > 0;
    panelTable.hidden = view !== "table" || !shown;
    panelChart.hidden = view !== "chart";
    if (view === "chart") empty.hidden = true;
    Array.prototype.forEach.call(tabs, function (t) { t.setAttribute("aria-selected", t.getAttribute("data-view") === view); });
    updateCounts(s); renderChips(s); writeHash(s);
  }

  /* ---------- events ---------- */
  root.classList.add("gr-js");
  readHash();
  form.addEventListener("change", update);
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  [benchSel, axisSel, untested].forEach(function (el) { el.addEventListener("change", function () { if (el === benchSel) { sortKey = "score"; sortDir = -1; } update(); }); });
  var qt; q.addEventListener("input", function () { clearTimeout(qt); qt = setTimeout(update, 120); });
  Array.prototype.forEach.call(tabs, function (t) { t.addEventListener("click", function () { view = t.getAttribute("data-view"); update(); }); });
  root.addEventListener("click", function (e) {
    var el = e.target.closest ? e.target : e.target.parentNode;
    var clear = el.closest("[data-clear]");
    if (clear) {
      Array.prototype.forEach.call(root.querySelectorAll('.gr-form input[type="checkbox"]'), function (b) { b.checked = false; });
      Array.prototype.forEach.call(root.querySelectorAll('input[name="ctx"][value=""],input[name="price"][value=""]'), function (b) { b.checked = true; });
      q.value = ""; update(); return;
    }
    var chip = el.closest(".gr-chip");
    if (chip) {
      var g = chip.getAttribute("data-g"), r = chip.getAttribute("data-r");
      if (g) Array.prototype.forEach.call(root.querySelectorAll('input[name="' + g + '"]'), function (b) { if (b.value === chip.getAttribute("data-v")) b.checked = false; });
      else if (r === "q") q.value = "";
      else root.querySelector('input[name="' + r + '"][value=""]').checked = true;
      update(); return;
    }
    var th = el.closest(".ll-th");
    if (th) {
      var k = th.getAttribute("data-sort");
      if (k === sortKey) sortDir = -sortDir; else { sortKey = k; sortDir = (k === "name" || k === "blend") ? 1 : -1; }
      update(); return;
    }
    var op = el.closest("[data-open]");
    if (op) { openId = op.getAttribute("data-open"); view = "table"; untested.checked = false; update(); var rw = tbody.querySelector('[data-id="' + openId + '"]'); if (rw) rw.scrollIntoView({ block: "center" }); return; }
    if (el.closest("a")) return;
    var row = el.closest(".ll-row");
    if (row) { var id = row.getAttribute("data-id"); openId = openId === id ? null : id; update(); var nb = tbody.querySelector('[data-id="' + id + '"] .ll-name'); if (nb && el.closest(".ll-name")) nb.focus(); return; }
    if (el.closest(".gr-filter-btn")) { var o = root.classList.toggle("gr-panel-open"); toggleBtn.setAttribute("aria-expanded", o); return; }
    if (el.closest("[data-close]")) { root.classList.remove("gr-panel-open"); toggleBtn.setAttribute("aria-expanded", "false"); root.scrollIntoView(); }
  });
  // "See the full ranking" links in the agent-type cards
  Array.prototype.forEach.call(document.querySelectorAll("[data-bench]"), function (b) {
    b.addEventListener("click", function () { benchSel.value = b.getAttribute("data-bench"); view = "table"; sortKey = "score"; sortDir = -1; update(); $("explorer").scrollIntoView(); });
  });
  var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { if (view === "chart") update(); }, 150); });
  update();
})();
