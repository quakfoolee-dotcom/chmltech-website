/* AI Tools Landscape charts (ai-tools.html): bubble map, cost-per-output spread, open source vs paid by layer, v8 -> V9 flow.
   Drawn from the same data file as the map (assets/data/ai-tools.json). Every chart redraws at its container width and has a
   Download PNG button. The shared helpers (tooltips, data table, money formats, PNG export) are exposed as window.ATCharts for
   assets/js/ai-tools-decide.js (price ladder, scorecard, Canada check, vendor risk). Loaded before ai-tools.js, which fires "at:data". */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var INK = "#0B2A5A", MUTED = "#5A6475", GRID = "#E4E1D8", FONT = "Inter, Arial, sans-serif";
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  // plan prices (USD per month): whole dollars from $10 up, cents below $10 ("$7.50", "$8")
  var usd = function (v) {
    if (v == null) return "–";
    if (v >= 10) return "$" + Math.round(v).toLocaleString("en-CA");
    var c = Math.round(v * 100) / 100; return "$" + (c % 1 ? c.toFixed(2) : String(c));
  };
  // costs per unit of output: two significant figures throughout ("$0.0049", "$0.39", "$3.9", "$12", "$3,900")
  var sig2 = function (v) {
    if (v == null) return "–";
    if (v === 0) return "$0";
    var p = Number(v.toPrecision(2));
    return "$" + (p >= 100 ? Math.round(p).toLocaleString("en-CA") : String(p));
  };
  var money = sig2;
  var median = function (a) { a = a.slice().sort(function (x, y) { return x - y; }); var m = a.length >> 1; return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2; };
  var D, layerName = {};
  var charts = {};
  var bubbleOff = {}; // layers hidden in the bubble chart (legend toggles)

  function text(x, y, s, o) {
    o = o || {};
    return '<text x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" font-family="' + FONT + '" font-size="' + (o.size || 12) + '" fill="' + (o.fill || INK) + '"' +
      (o.anchor ? ' text-anchor="' + o.anchor + '"' : "") + (o.weight ? ' font-weight="' + o.weight + '"' : "") + (o.extra || "") + ">" + esc(s) + "</text>";
  }
  function tipOn(card, html, ev, anchor) {
    var t = card.querySelector(".at-tip"); if (!t) return;
    t.innerHTML = html; t.hidden = false;
    var r = card.getBoundingClientRect(), a = ev ? { x: ev.clientX, y: ev.clientY } : (function () { var q = anchor.getBoundingClientRect(); return { x: q.right, y: q.bottom }; })();
    var x = a.x - r.left + 14, y = a.y - r.top + 14;
    if (x + t.offsetWidth > r.width - 8) x = a.x - r.left - t.offsetWidth - 14;
    t.style.left = Math.max(4, x) + "px"; t.style.top = y + "px";
  }
  function tipOff(card) { var t = card.querySelector(".at-tip"); if (t) t.hidden = true; }
  function bindTips(card, lookup) {
    var svg = card.querySelector(".at-fig svg");
    svg.addEventListener("mousemove", function (e) { var k = e.target.getAttribute && e.target.getAttribute("data-k"); if (k && lookup[k]) tipOn(card, lookup[k], e); else tipOff(card); });
    svg.addEventListener("mouseleave", function () { tipOff(card); });
    svg.addEventListener("focusin", function (e) { var k = e.target.getAttribute && e.target.getAttribute("data-k"); if (k && lookup[k]) tipOn(card, lookup[k], null, e.target); });
    svg.addEventListener("focusout", function () { tipOff(card); });
  }
  function legend(items) {
    return '<ul class="at-legend">' + items.map(function (i) { return "<li>" + i + "</li>"; }).join("") + "</ul>";
  }
  function dataTable(head, rows) {
    return '<details class="at-dtable"><summary>Show the data as a table</summary><div class="ll-tablewrap"><table class="ll-table"><thead><tr>' +
      head.map(function (h, i) { return '<th scope="col"' + (i ? ' class="num"' : "") + ">" + esc(h) + "</th>"; }).join("") + "</tr></thead><tbody>" +
      rows.map(function (r) { return "<tr>" + r.map(function (v, i) { return (i ? '<td class="num">' : '<th scope="row">') + esc(v) + (i ? "</td>" : "</th>"); }).join("") + "</tr>"; }).join("") +
      "</tbody></table></div></details>";
  }
  function pctRound(vals) {  // largest-remainder rounding so shares add up to 100
    var tot = vals.reduce(function (a, b) { return a + b; }, 0) || 1, raw = vals.map(function (v) { return v / tot * 100; }), fl = raw.map(Math.floor);
    var left = 100 - fl.reduce(function (a, b) { return a + b; }, 0);
    raw.map(function (v, i) { return [v - fl[i], i]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, left).forEach(function (x) { fl[x[1]]++; });
    return fl;
  }
  var dot = function (c, hollow) { return '<svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="' + (hollow ? 4.5 : 5) + '" fill="' + (hollow ? "#fff" : c) + '" stroke="' + c + '" stroke-width="' + (hollow ? 2 : 0) + '"/></svg>'; };
  var sq = function (c) { return '<svg width="12" height="12" aria-hidden="true"><rect x="1" y="1" width="10" height="10" rx="2" fill="' + c + '"/></svg>'; };

  /* ---------- 1. category bubble map: one highlighted layer in brand blue, the rest light grey (colour-blind safe) ---------- */
  var bubbleHi = "";  // "" = all layers in one neutral colour; otherwise the highlighted layer id
  var HI = "#0B6FA4", LO = "#868E9A", NEUTRAL = "#5A7A96";  // grey dots keep 3:1 against white (they are focusable)
  function bubbleRows() {
    var rows = [], none = [];
    D.categories.forEach(function (c) {
      var ts = D.tools.filter(function (t) { return t.c === c.c; });
      var ps = ts.filter(function (t) { return t.ep > 0 && (t.cur || "USD") === "USD"; }).map(function (t) { return t.ep; });
      var free = Math.round(100 * ts.filter(function (t) { return t.free; }).length / ts.length);
      if (!ps.length) { none.push(c.c); return; }
      rows.push({ c: c.c, l: c.l, n: ts.length, np: ps.length, med: median(ps), free: free });
    });
    // outliers: the categories farthest from the middle of the cloud (log price and free share, each scaled 0-1)
    var px = function (r) { return (Math.log(Math.max(5, Math.min(500, r.med))) - Math.log(5)) / (Math.log(500) - Math.log(5)); };
    var cx = median(rows.map(px)), cy = median(rows.map(function (r) { return r.free / 100; }));
    rows.forEach(function (r) { r.dist = Math.sqrt(Math.pow(px(r) - cx, 2) + Math.pow(r.free / 100 - cy, 2)); });
    rows.slice().sort(function (a, b) { return b.dist - a.dist || a.c.localeCompare(b.c); }).slice(0, 8).forEach(function (r) { r.out = true; });
    return { rows: rows, none: none };
  }
  function bubble(card) {
    var fig = card.querySelector(".at-fig"), narrow = window.matchMedia && matchMedia("(max-width:599px)").matches;
    card.classList.toggle("at-bub-small", !!narrow);
    // on phones the plot is hidden (a pointer to the price ladder shows instead), but it is still drawn at a readable width for the PNG
    var W = narrow ? 760 : fig.clientWidth, small = W < 500, H = small ? 420 : 520;
    var m = { l: small ? 44 : 56, r: 24, t: 34, b: 48 }, iw = W - m.l - m.r, ih = H - m.t - m.b;
    var x0 = Math.log(5), x1 = Math.log(500);
    var X = function (v) { return m.l + (Math.log(Math.max(5, Math.min(500, v))) - x0) / (x1 - x0) * iw; };
    var Y = function (p) { return m.t + (1 - p / 100) * ih; };
    var BR = bubbleRows(), rows = BR.rows, R0 = 7;
    var isHi = function (r) { return bubbleHi && r.l === bubbleHi; };
    var colour = function (r) { return !bubbleHi ? NEUTRAL : isHi(r) ? HI : LO; };
    var s = '<svg xmlns="' + NS + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="group" aria-label="Scatter chart of AI tool categories: typical entry price against share with a free plan' + (bubbleHi ? ", " + esc(layerName[bubbleHi]) + " highlighted" : "") + '">';
    s += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    [5, 10, 20, 50, 100, 200, 500].forEach(function (v) {
      var x = X(v); s += '<line x1="' + x + '" x2="' + x + '" y1="' + m.t + '" y2="' + (m.t + ih) + '" stroke="' + GRID + '"/>' + text(x, H - m.b + 18, "$" + v, { anchor: "middle", fill: MUTED, size: 11 });
    });
    [0, 25, 50, 75, 100].forEach(function (p) {
      var y = Y(p); s += '<line x1="' + m.l + '" x2="' + (m.l + iw) + '" y1="' + y + '" y2="' + y + '" stroke="' + GRID + '"/>' + text(m.l - 8, y + 4, p + "%", { anchor: "end", fill: MUTED, size: 11 });
    });
    s += text(m.l + iw / 2, H - 8, small ? "Typical entry price, USD/month (log)" : "Typical entry price, USD per month (median of published cheapest paid plans, log scale)", { anchor: "middle", fill: MUTED, size: small ? 10.5 : 12 });
    s += text(14, m.t + ih / 2, "Tools with a free plan", { anchor: "middle", fill: MUTED, size: small ? 10.5 : 12, extra: ' transform="rotate(-90 14 ' + (m.t + ih / 2) + ')"' });
    var tips = {};
    // grey first, highlighted last so they sit on top
    rows.slice().sort(function (a, b) { return (isHi(a) - isHi(b)) || b.n - a.n; }).forEach(function (r, i) {
      var k = "b" + i, hol = r.np < 4, col = colour(r), x = X(r.med).toFixed(1), y = Y(r.free).toFixed(1);
      var all2 = D.tools.filter(function (t) { return t.c === r.c || (t.c2 || []).indexOf(r.c) >= 0; }).length;
      tips[k] = "<strong>" + esc(r.c) + "</strong><br>" + esc(layerName[r.l]) + "<br>" + r.n + " tools" + (all2 > r.n ? " (" + all2 + " including secondary uses)" : "") + " · " + r.free + "% with a free plan<br>Typical entry price " + usd(r.med) + "/mo (from " + r.np + " published price" + (r.np > 1 ? "s" : "") + ")" + (hol ? "<br><em>Few published prices: read with care</em>" : "") + "<br><span>Select to show on the map</span>";
      s += '<circle cx="' + x + '" cy="' + y + '" r="' + R0 + '" fill="' + (hol ? "#fff" : col) + '" stroke="' + (hol ? col : "#fff") + '" stroke-width="2" pointer-events="none"/>';
      s += '<circle class="at-hit" data-k="' + k + '" data-cat="' + esc(r.c) + '" cx="' + x + '" cy="' + y + '" r="12" fill="transparent" tabindex="0" role="button" aria-label="' + esc(r.c) + ": typical entry price " + usd(r.med) + " a month, " + r.free + '% with a free plan" style="cursor:pointer"/>';
    });
    // labels: the highlighted layer first, then the outliers; greedy, never over another label, skipped when no room (hover and the table carry the rest)
    var placed = [], fs = small ? 10 : 11.5;
    var discs = rows.map(function (r) { return [X(r.med), Y(r.free), R0 + 1, r.c]; });
    var hitsDisc = function (bx, by, w, h, own) {
      return discs.some(function (d) {
        if (d[3] === own) return false;
        var nx = Math.max(bx, Math.min(d[0], bx + w)), ny = Math.max(by, Math.min(d[1], by + h));
        return (nx - d[0]) * (nx - d[0]) + (ny - d[1]) * (ny - d[1]) < d[2] * d[2];
      });
    };
    var want = rows.filter(function (r) { return isHi(r); }).concat(rows.filter(function (r) { return r.out && !isHi(r); }).sort(function (a, b) { return b.dist - a.dist; }));
    want.forEach(function (r) {
      var cx = X(r.med), cy = Y(r.free), w = r.c.length * fs * 0.58 + 4, h = fs + 4, g = R0 + 4;
      var opts = [[cx + g, cy + fs / 2 - 1, "start"], [cx - g, cy + fs / 2 - 1, "end"], [cx, cy - g - 2, "middle"], [cx, cy + g + fs, "middle"]];
      var done = false;
      for (var pass = 0; pass < 2 && !done; pass++) {  // first clear of every dot; then allowed over a dot (the white halo keeps it legible), never over a label
        for (var i = 0; i < opts.length; i++) {
          var o = opts[i], bx = o[2] === "start" ? o[0] : o[2] === "end" ? o[0] - w : o[0] - w / 2, by = o[1] - fs;
          if (bx < m.l - 4 || bx + w > W - 2 || by < 2 || by + h > m.t + ih + 4) continue;
          if (placed.some(function (p) { return bx < p[0] + p[2] && bx + w > p[0] && by < p[1] + p[3] && by + h > p[1]; })) continue;
          if (!pass && hitsDisc(bx, by, w, h, r.c)) continue;
          placed.push([bx, by, w, h]);
          s += text(o[0], o[1], r.c, { anchor: o[2], size: fs, fill: isHi(r) || !bubbleHi ? INK : MUTED, weight: isHi(r) ? 600 : null, extra: ' paint-order="stroke" stroke="#fff" stroke-width="3" pointer-events="none"' });
          done = true; break;
        }
      }
    });
    s += "</svg>";
    fig.innerHTML = s + (narrow ? '<p class="ll-chartnote at-bub-ptr">This chart needs a wider screen. The <a href="#at-ch-ladder">price ladder</a> shows the same prices by category; the table below has every point.</p>' : "");
    var lgItems = bubbleHi ? [dot(HI) + esc(layerName[bubbleHi]), dot(LO) + "Other layers"] : [dot(NEUTRAL) + "Category"];
    lgItems.push(dot("#5A6475", true) + "Hollow: fewer than 4 published prices");
    card.querySelector(".at-figfoot").innerHTML = '<div class="at-seg" role="group" aria-label="Highlight a layer"><span class="at-seg-h">Highlight a layer:</span>' +
      '<button type="button" data-hl="" aria-pressed="' + !bubbleHi + '">All layers</button>' +
      D.layers.map(function (l) { return '<button type="button" data-hl="' + l.id + '" aria-pressed="' + (bubbleHi === l.id) + '">' + esc(l.name) + "</button>"; }).join("") + "</div>" +
      legend(lgItems) +
      '<p class="ll-chartnote">Each dot is one category; it carries no size, and the number of tools is in the tooltip and the table. Labels show the highlighted layer and the categories farthest from the crowd.' +
      (BR.none.length ? " Not shown (no published entry prices, mostly contact-sales or free): " + esc(BR.none.join(", ")) + "." : "") + "</p>" +
      dataTable(["Category", "Layer", "Tools", "With a free plan", "Typical entry price (USD/mo)", "Published prices"],
        rows.slice().sort(function (a, b) { return a.c.localeCompare(b.c); }).map(function (r) { return [r.c, layerName[r.l] || r.l, r.n, r.free + "%", usd(r.med), r.np]; }));
    card.querySelectorAll(".at-figfoot [data-hl]").forEach(function (b) {
      b.addEventListener("click", function () {
        bubbleHi = b.getAttribute("data-hl"); bubble(card);
        var f = card.querySelector('.at-figfoot [data-hl="' + bubbleHi + '"]'); if (f) f.focus();
      });
    });
    bindTips(card, tips);
    var svg = fig.querySelector("svg");
    svg.addEventListener("click", function (e) { var c = e.target.getAttribute("data-cat"); if (c && window.ATools) window.ATools.showCategory(c); });
    svg.addEventListener("keydown", function (e) { var c = e.target.getAttribute && e.target.getAttribute("data-cat"); if (c && (e.key === "Enter" || e.key === " ") && window.ATools) { e.preventDefault(); window.ATools.showCategory(c); } });
  }
  /* ---------- 2. cost-per-output spread (cheapest and dearest tool named in each row) ---------- */
  function spreadRows() {
    var rows = [];
    D.categories.forEach(function (c) {
      var units = {};
      D.tools.forEach(function (t) { if (t.c === c.c && t.cmp && t.cpu > 0) units[t.unit] = (units[t.unit] || 0) + 1; });
      var u = Object.keys(units).sort(function (a, b) { return units[b] - units[a] || a.localeCompare(b); })[0];
      if (!u || u === "per seat per month" || units[u] < 4) return;
      var ts = D.tools.filter(function (t) { return t.c === c.c && t.cmp && t.cpu > 0 && t.unit === u; });
      var vals = ts.map(function (t) { return t.cpu; }), md = median(vals), mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals);
      var by = ts.slice().sort(function (a, b) { return a.cpu - b.cpu || a.n.localeCompare(b.n); });
      rows.push({ c: c.c, l: c.l, u: u, ts: ts, md: md, mn: mn, mx: mx, ratio: mx / mn, lo: by[0], hi: by[by.length - 1] });
    });
    return rows.sort(function (a, b) { return b.ratio - a.ratio || a.c.localeCompare(b.c); });
  }
  function spread(card) {
    var W = card.querySelector(".at-fig").clientWidth, small = W < 620, BLUE = "#0B6FA4";
    var rows = spreadRows();
    var seat = D.tools.filter(function (t) { return t.cmp && t.unit === "per seat per month" && t.cpu > 0; }).map(function (t) { return t.cpu; });
    var lw = small ? 0 : 210, rw = small ? 0 : 170, rh = small ? 78 : 50, m = { l: (small ? 26 : 12) + lw, r: (small ? 26 : 12) + rw, t: 26, b: 40 };
    var H = m.t + rows.length * rh + m.b, iw = W - m.l - m.r;
    var x0 = Math.log(0.01), x1 = Math.log(100), X = function (v) { return m.l + (Math.log(Math.max(0.01, Math.min(100, v))) - x0) / (x1 - x0) * iw; };
    var unitTxt = function (u) { return u.replace(/ \(input; note output\)/, ""); };
    var s = '<svg xmlns="' + NS + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="group" aria-label="Spread of cost per output within each category">';
    s += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    var tips = {}, k = 0, body = "";
    rows.forEach(function (r, i) {
      var y0 = m.t + i * rh, yc = y0 + (small ? 44 : 18);
      if (i % 2) s += '<rect x="0" y="' + y0 + '" width="' + W + '" height="' + rh + '" fill="#F6F5F1"/>';
      var range = sig2(r.mn) + " – " + sig2(r.mx);
      if (small) body += text(12, y0 + 15, r.c, { size: 11.5, weight: 600 }) + text(12, y0 + 29, range + " " + unitTxt(r.u), { size: 10.5, fill: MUTED });
      else {
        body += text(m.l - 14, yc + 4, r.c, { anchor: "end", size: 12.5, weight: 600 });
        body += text(W - rw, yc - 1, range, { size: 12, weight: 600 }) + text(W - rw, yc + 13, unitTxt(r.u), { size: 10.5, fill: MUTED });
      }
      body += '<line x1="' + X(r.mn / r.md) + '" x2="' + X(r.mx / r.md) + '" y1="' + yc + '" y2="' + yc + '" stroke="' + BLUE + '" stroke-opacity=".3" stroke-width="3"/>';
      r.ts.forEach(function (t, j) {
        var key = "s" + (k++), rel = t.cpu / r.md;
        tips[key] = "<strong>" + esc(t.n) + "</strong><br>" + sig2(t.cpu) + " " + esc(t.unit) + "<br>" + (rel < 1 ? rel.toFixed(2) : rel.toFixed(1)) + "× the category median<br><span>Select to open the tool</span>";
        body += '<circle data-k="' + key + '" data-id="' + esc(t.id) + '" cx="' + X(rel).toFixed(1) + '" cy="' + (yc + ((j % 3) - 1) * 3).toFixed(1) + '" r="5" fill="' + BLUE + '" fill-opacity=".85" stroke="#fff" stroke-width="1.5" tabindex="0" role="button" aria-label="' + esc(t.n) + ", " + sig2(t.cpu) + " " + esc(t.unit) + '" style="cursor:pointer"/>';
      });
      // direct labels: cheapest at the left end, dearest at the right end, on the line under the strip
      var fs = 10.5, cw = fs * 0.56, ly = yc + 17, xl = X(r.mn / r.md), xr = X(r.mx / r.md);
      var nl = r.lo.n, nr = r.hi.n, fit = function (n, max) { return n.length * cw <= max ? n : n.slice(0, Math.max(3, Math.floor(max / cw) - 1)) + "…"; };
      var minX = small ? 8 : m.l - 6, maxX = small ? W - 8 : W - m.r + 6;
      var lx = Math.max(minX, xl - 4), rx = Math.min(maxX, xr + 4), need = (nl.length + nr.length) * cw + 14;
      if (rx - lx < need) {  // short strip: let the two names spread outwards from the middle, inside the plot
        var mid = (lx + rx) / 2; lx = Math.max(minX, mid - need / 2); rx = Math.min(maxX, lx + need); lx = Math.max(minX, rx - need);
      }
      var room = rx - lx - 14;
      if ((nl.length + nr.length) * cw > room) { nl = fit(nl, Math.max(room / 2, room - nr.length * cw)); nr = fit(nr, room - nl.length * cw); }
      body += text(lx, ly, nl, { size: fs, fill: MUTED, extra: ' pointer-events="none"' });
      body += text(rx, ly, nr, { size: fs, fill: MUTED, anchor: "end", extra: ' pointer-events="none"' });
    });
    [[0.01, "1/100×"], [0.1, "1/10×"], [1, "median"], [10, "10×"], [100, "100×"]].forEach(function (t) {
      var x = X(t[0]), st = ' stroke="' + (t[0] === 1 ? "#9AA6B8" : GRID) + '"' + (t[0] === 1 ? ' stroke-width="1.5"' : "");
      if (small) rows.forEach(function (r, i) { var y0 = m.t + i * rh; s += '<line x1="' + x + '" x2="' + x + '" y1="' + (y0 + 34) + '" y2="' + (y0 + rh) + '"' + st + "/>"; });  // keep the row titles clear of the grid
      else s += '<line x1="' + x + '" x2="' + x + '" y1="' + (m.t - 6) + '" y2="' + (H - m.b) + '"' + st + "/>";
      s += text(x, H - m.b + 18, t[1], { anchor: "middle", fill: MUTED, size: 11 });
    });
    s += body + text(m.l + iw / 2, H - 6, small ? "Relative to the category median (log)" : "Cost per output relative to the category's median tool (log scale)", { anchor: "middle", fill: MUTED, size: small ? 10.5 : 12 });
    s += "</svg>";
    card.querySelector(".at-fig").innerHTML = s;
    card.querySelector(".at-figfoot").innerHTML = '<p class="ll-chartnote">Categories with at least four tools priced on the same unit. ' +
      "Each dot is one tool's entry-plan cost per unit, divided by the category median; the cheapest and dearest tool in each row are named. Vendors define units a little differently (for example a trace versus a log record, or a small versus a flagship model), so the widest spreads partly reflect different products. " +
      "Seat-priced software is left out of this chart (the price ladder above covers it); across all categories, seat prices run from " + sig2(Math.min.apply(null, seat)) + " to " + sig2(Math.max.apply(null, seat)) + " per user per month. Costs are rounded to two significant figures. <strong>Select a dot to open the tool.</strong></p>";
    card.querySelector(".at-figfoot").insertAdjacentHTML("beforeend", dataTable(["Category", "Unit", "Tools", "Cheapest tool", "Cheapest", "Median", "Dearest", "Dearest tool"],
      rows.map(function (r) { return [r.c, r.u, r.ts.length, r.lo.n, sig2(r.mn), sig2(r.md), sig2(r.mx), r.hi.n]; })));
    bindTips(card, tips);
    var svg = card.querySelector(".at-fig svg");
    svg.addEventListener("click", function (e) { var id = e.target.getAttribute("data-id"); if (id && window.ATools) window.ATools.open(id); });
    svg.addEventListener("keydown", function (e) { var id = e.target.getAttribute && e.target.getAttribute("data-id"); if (id && (e.key === "Enter" || e.key === " ") && window.ATools) { e.preventDefault(); window.ATools.open(id); } });
  }

  /* ---------- shared horizontal stacked bars ---------- */
  function hbars(card, rows, segs, opt) {
    var W = card.querySelector(".at-fig").clientWidth, small = W < 560, lw = small ? 0 : 210, rh = small ? 58 : 44;
    var m = { l: 12 + lw, r: opt.pct ? 16 : 110, t: 10, b: 30 }, iw = W - m.l - m.r, H = m.t + rows.length * rh + m.b;
    var max = opt.pct ? 100 : Math.max.apply(null, rows.map(function (r) { return segs.reduce(function (a, g) { return a + (r.v[g.k] || 0); }, 0); }));
    var s = '<svg xmlns="' + NS + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + esc(opt.aria) + '">', tips = {}, k = 0;
    if (!opt.pct) { var tk = ticks(max); max = tk[tk.length - 1]; }
    (opt.pct ? [0, 25, 50, 75, 100] : ticks(max)).forEach(function (t) {
      var x = m.l + t / max * iw; s += '<line x1="' + x + '" x2="' + x + '" y1="' + m.t + '" y2="' + (H - m.b) + '" stroke="' + GRID + '"/>' + text(x, H - m.b + 16, t + (opt.pct ? "%" : ""), { anchor: "middle", size: 11, fill: MUTED });
    });
    rows.forEach(function (r, i) {
      var y = m.t + i * rh + (small ? 22 : 8), bh = small ? 24 : 26, x = m.l, tot = segs.reduce(function (a, g) { return a + (g.side ? 0 : (r.v[g.k] || 0)); }, 0);
      var pr = opt.pct ? pctRound(segs.map(function (g) { return r.v[g.k] || 0; })) : null;
      if (small) s += text(12, y - 6, r.label, { size: 11.5, weight: 600 }); else s += text(m.l - 12, y + bh / 2 + 4, r.label, { anchor: "end", size: 12.5, weight: 600 });
      segs.forEach(function (g, gi) {
        var v = r.v[g.k] || 0; if (!v) return;
        var w = (opt.pct ? v / r.total * 100 : v) / max * iw, key = "h" + (k++);
        tips[key] = "<strong>" + esc(r.label) + "</strong><br>" + esc(g.n) + ": " + v + (opt.pct ? " of " + r.total + " tools (" + Math.round(v / r.total * 100) + "%)" : "");
        s += '<rect data-k="' + key + '" x="' + x.toFixed(1) + '" y="' + y + '" width="' + Math.max(1, w).toFixed(1) + '" height="' + bh + '" fill="' + g.c + '"/>';
        if (w > 30) s += text(x + w / 2, y + bh / 2 + 4, opt.pct ? pr[gi] + "%" : String(v), { anchor: "middle", size: 11, fill: g.dark ? INK : "#fff", weight: 600, extra: ' pointer-events="none"' });
        x += w;
      });
      if (!opt.pct) s += text(x + 8, y + bh / 2 + 4, tot + " of " + r.total + " (" + Math.round(tot / r.total * 100) + "%)", { size: 11.5, fill: MUTED });
      r.pr = pr;
    });
    s += "</svg>";
    card.querySelector(".at-fig").innerHTML = s;
    card.querySelector(".at-figfoot").innerHTML = legend(segs.map(function (g) { return sq(g.c) + esc(g.n); })) + (opt.note ? '<p class="ll-chartnote">' + opt.note + "</p>" : "") +
      dataTable(["Layer"].concat(segs.map(function (g) { return g.n; })).concat([opt.pct ? "Tools" : "Tools in layer"]),
        rows.map(function (r) { return [r.label].concat(segs.map(function (g, gi) { var v = r.v[g.k] || 0; return opt.pct ? v + " (" + r.pr[gi] + "%)" : v; })).concat([r.total]); }));
    bindTips(card, tips);
  }
  function ticks(max) { var st = max > 120 ? 50 : max > 60 ? 20 : 10, out = []; for (var t = 0; t < max + st; t += st) out.push(t); return out; }

  /* ---------- 4. open source vs paid ---------- */
  function openPaid(card) {
    var G = [{ k: "open-source", n: "Open source", c: "#2F6B3A" }, { k: "open-core", n: "Open source + paid cloud", c: "#8DC63F", dark: true },
      { k: "freemium", n: "Free plan + paid", c: "#0B6FA4" }, { k: "paid", n: "Paid (subscription or pay as you go)", c: "#071C3D" }, { k: "enterprise", n: "Contact sales", c: "#9AA6B8", dark: true }];
    var map = { free: "freemium", subscription: "paid", usage: "paid" };
    var rows = D.layers.map(function (l) {
      var ts = D.tools.filter(function (t) { return t.l === l.id; }), v = {};
      ts.forEach(function (t) { var g = map[t.pm] || t.pm; v[g] = (v[g] || 0) + 1; });
      return { label: l.name, v: v, total: ts.length };
    });
    hbars(card, rows, G, { pct: true, aria: "Pricing model mix by layer",
      note: "Shares of each layer's current tools, rounded so each row adds up to 100%. Free plan + paid includes the few completely free tools." });
  }

  /* ---------- 5. v8 -> V9 flow ---------- */
  function flow(card) {
    var F = D.flow, W = card.querySelector(".at-fig").clientWidth, small = W < 560, H = small ? 360 : 380;
    var m = { t: 24, b: 20 }, gap = 18, nw = 14, ih = H - m.t - m.b - gap * 2;
    var scale = (ih) / (F.prev_total + F.new), xL = small ? 90 : 150, xM = W / 2 - nw / 2, xR = W - (small ? 76 : 150) - nw;
    var yv8 = m.t, hv8 = F.prev_total * scale, ynew = yv8 + hv8 + gap * 2, hnew = F.new * scale;
    var mids = [{ k: "kept", n: "Kept as is", v: F.kept, c: "#2F6B3A" }, { k: "updated", n: "Updated", v: F.updated, c: "#0B6FA4" }, { k: "retired", n: "Removed", v: F.prev_removed, c: "#9AA6B8" }];
    var y = m.t; mids.forEach(function (d) { d.y = y; d.h = d.v * scale; y += d.h + gap; });
    var hv9 = F.total * scale, yv9 = m.t + ih + gap * 2 - hv9;
    var band = function (x0, y0, x1, y1, h, c, k) {
      var cx = (x0 + x1) / 2;
      return '<path data-k="' + k + '" d="M' + x0 + "," + y0 + " C" + cx + "," + y0 + " " + cx + "," + y1 + " " + x1 + "," + y1 + " L" + x1 + "," + (y1 + h) + " C" + cx + "," + (y1 + h) + " " + cx + "," + (y0 + h) + " " + x0 + "," + (y0 + h) + ' Z" fill="' + c + '" fill-opacity=".32"/>';
    };
    var s = '<svg xmlns="' + NS + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="How the previous list of ' + F.prev_total + ' tools became this list of ' + F.total + '">', tips = {};
    var off = 0;
    mids.forEach(function (d) { s += band(xL + nw, yv8 + off, xM, d.y, d.h, d.c, "f-" + d.k); tips["f-" + d.k] = esc(d.n) + ": " + d.v + " of the " + F.prev_total + " tools on the previous list"; off += d.h; });
    var off9 = 0;
    mids.slice(0, 2).forEach(function (d) { s += band(xM + nw, d.y, xR, yv9 + off9, d.h, d.c, "g-" + d.k); tips["g-" + d.k] = esc(d.n) + ": " + d.v + " tools carried into this list"; off9 += d.h; });
    s += band(xL + nw, ynew, xR, yv9 + off9, hnew, "#C2571A", "g-new"); tips["g-new"] = "New: " + F.new + " tools added in this review";
    s += '<rect x="' + xL + '" y="' + yv8 + '" width="' + nw + '" height="' + hv8 + '" fill="' + INK + '"/><rect x="' + xL + '" y="' + ynew + '" width="' + nw + '" height="' + hnew + '" fill="#C2571A"/>';
    mids.forEach(function (d) { s += '<rect x="' + xM + '" y="' + d.y + '" width="' + nw + '" height="' + d.h + '" fill="' + d.c + '"/>'; });
    s += '<rect x="' + xR + '" y="' + yv9 + '" width="' + nw + '" height="' + hv9 + '" fill="' + INK + '"/>';
    var fs = small ? 11 : 13;
    s += text(xL - 8, yv8 + hv8 / 2, "Previous list", { anchor: "end", size: fs, weight: 600 }) + text(xL - 8, yv8 + hv8 / 2 + 16, String(F.prev_total), { anchor: "end", size: fs + 2, weight: 700 });
    s += text(xL - 8, ynew + hnew / 2, "New tools", { anchor: "end", size: fs, weight: 600, fill: "#C2571A" }) + text(xL - 8, ynew + hnew / 2 + 16, String(F.new), { anchor: "end", size: fs + 2, weight: 700, fill: "#C2571A" });
    mids.forEach(function (d) { s += text(xM + nw + 6, d.y + Math.max(d.h / 2, 6) + 4, d.n + " " + d.v, { size: fs - 1, weight: 600, extra: ' paint-order="stroke" stroke="#fff" stroke-width="3"' }); });
    s += text(xR + nw + 8, yv9 + hv9 / 2, "This list", { size: fs, weight: 600 }) + text(xR + nw + 8, yv9 + hv9 / 2 + 16, String(F.total), { size: fs + 2, weight: 700 });
    s += "</svg>";
    card.querySelector(".at-fig").innerHTML = s;
    var nl = {}; D.tools.forEach(function (t) { if (t.ch === "new") nl[t.l] = (nl[t.l] || 0) + 1; });
    var top2 = Object.keys(nl).sort(function (a, b) { return nl[b] - nl[a]; }).slice(0, 2);
    card.querySelector(".at-figfoot").innerHTML = '<p class="ll-chartnote">' + Math.round((F.kept + F.updated) / F.prev_total * 100) + "% of the previous list survived the review, and most of those needed an update (new price, name, owner or category). " +
      Math.round(F.new / F.total * 100) + "% of the tools on this list are new, mostly in " + top2.map(function (k) { return (layerName[k] || k) + " (" + nl[k] + ")"; }).join(" and ") + ".</p>" +
      dataTable(["Step", "Tools"], [["Previous list", F.prev_total], ["Kept as is", F.kept], ["Updated", F.updated], ["Removed (" + F.prev_removed_ev + " retired products, " + (F.prev_removed - F.prev_removed_ev) + " duplicates or clean-ups)", F.prev_removed], ["New tools added", F.new], ["This list", F.total]]);
    bindTips(card, tips);
  }

  /* ---------- PNG export: title, wrapped caption, the chart, the legend (each swatch copied from the on-page legend) and a footer ----------
     A card whose chart is HTML (scorecard, Canada check) sets card._atPng = function () { return {W, H, svg: "<svg inner markup>"}; }. */
  function exportPng(card) {
    var W, H, inner;
    if (typeof card._atPng === "function") { var p = card._atPng(); if (!p) return; W = p.W; H = p.H; inner = p.svg; }
    else {
      var svg = card.querySelector(".at-fig svg"); if (!svg) return;
      W = +svg.getAttribute("width"); H = +svg.getAttribute("height"); inner = svg.innerHTML;
    }
    var title = card.querySelector("h3").textContent, cap = (card.querySelector(".at-cap") || {}).textContent || "";
    var per = Math.max(30, Math.floor((W - 32) / 6.9)), capL = [], cw = cap.split(" "), ln = "";
    cw.forEach(function (w) { if ((ln + " " + w).trim().length > per) { capL.push(ln.trim()); ln = w; } else ln += " " + w; }); if (ln.trim()) capL.push(ln.trim());
    var tper = Math.max(20, Math.floor((W - 32) / 11.5)), tL = [], tw = title.split(" "), tl = "";  // title wraps like the caption (20px bold)
    tw.forEach(function (w) { if ((tl + " " + w).trim().length > tper) { tL.push(tl.trim()); tl = w; } else tl += " " + w; }); if (tl.trim()) tL.push(tl.trim());
    var th = (tL.length - 1) * 25, titleSvg = tL.map(function (l, i) { return text(16, 30 + i * 25, l, { size: 20, weight: 700 }); }).join("");
    var head = 50 + th + capL.length * 18, capSvg = capL.map(function (l, i) { return text(16, 54 + th + i * 18, l, { size: 12.5, fill: MUTED }); }).join("");
    var items = [];
    card.querySelectorAll(".at-legend li").forEach(function (li) {
      if (li.closest("details")) return;
      var sw = li.querySelector("svg"), lab = Array.prototype.filter.call(li.childNodes, function (n) { return n.nodeName.toLowerCase() !== "svg"; }).map(function (n) { return n.textContent; }).join("").trim();
      if (!lab) return;
      items.push({ sw: sw ? sw.innerHTML : "", sw_w: sw ? +sw.getAttribute("width") || 12 : 0, sw_h: sw ? +sw.getAttribute("height") || 12 : 0, t: lab });
    });
    var lx = 16, rowsL = [[]], maxW = W - 32;
    items.forEach(function (it) { var w = (it.sw ? it.sw_w + 6 : 0) + it.t.length * 6.6 + 18; if (lx + w > maxW && rowsL[rowsL.length - 1].length) { rowsL.push([]); lx = 16; } it.x = lx; lx += w; rowsL[rowsL.length - 1].push(it); });
    var legH = items.length ? rowsL.length * 20 + 10 : 0, leg = "";
    rowsL.forEach(function (r, ri) {
      r.forEach(function (it) {
        var yy = H + head + 14 + ri * 20;
        if (it.sw) leg += '<g transform="translate(' + it.x + "," + (yy - 4 - it.sw_h / 2) + ')">' + it.sw + "</g>";
        leg += text(it.x + (it.sw ? it.sw_w + 6 : 0), yy, it.t, { size: 11.5, fill: INK });
      });
    });
    var footL = ["Chmltech AI Tools Landscape · checked " + D.checked + " · chmltech.com/ai-tools"];
    if (footL[0].length * 6.6 > W - 32) footL = ["Chmltech AI Tools Landscape · checked " + D.checked, "chmltech.com/ai-tools"];
    var foot = 34 + legH + (footL.length - 1) * 16;
    var full = '<svg xmlns="' + NS + '" width="' + W + '" height="' + (H + head + foot) + '"><rect width="100%" height="100%" fill="#fff"/>' +
      titleSvg + capSvg +
      '<g transform="translate(0,' + head + ')">' + inner + "</g>" + leg +
      footL.map(function (l, i) { return text(16, H + head + legH + 22 + i * 16, l, { size: 11.5, fill: MUTED }); }).join("") + "</svg>";
    var img = new Image(), sc = 2;
    img.onload = function () {
      var c = document.createElement("canvas"); c.width = W * sc; c.height = (H + head + foot) * sc;
      var x = c.getContext("2d"); x.scale(sc, sc); x.drawImage(img, 0, 0);
      c.toBlob(function (b) {
        var a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = "chmltech-ai-tools-" + card.id.replace(/^at-ch-/, "") + ".png";
        document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
      });
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(full);
  }

  /* ---------- wiring ---------- */
  var DRAW = { "at-ch-bubble": bubble, "at-ch-spread": spread, "at-ch-open": openPaid, "at-ch-flow": flow };
  window.ATCharts = { NS: NS, INK: INK, MUTED: MUTED, GRID: GRID, FONT: FONT, esc: esc, usd: usd, sig2: sig2, median: median, text: text,
    tipOn: tipOn, tipOff: tipOff, bindTips: bindTips, legend: legend, dataTable: dataTable, pctRound: pctRound, exportPng: exportPng };
  function init(data) {
    if (D) return; D = data;
    D.layers.forEach(function (l) { layerName[l.id] = l.name; });
    Object.keys(DRAW).forEach(function (id) {
      var card = document.getElementById(id); if (!card) return;
      var w = 0, draw = function () { var nw = card.querySelector(".at-fig").clientWidth; if (nw && nw !== w) { w = nw; DRAW[id](card); } };
      charts[id] = new ResizeObserver(draw); charts[id].observe(card.querySelector(".at-fig"));
      var b = card.querySelector("[data-png]"); if (b) b.addEventListener("click", function () { exportPng(card); });
    });
    // redraw the bubble chart when the phone breakpoint is crossed (its width may not change at the switch)
    if (window.matchMedia) { var mq = matchMedia("(max-width:599px)"), bc = document.getElementById("at-ch-bubble"); if (bc && mq.addEventListener) mq.addEventListener("change", function () { if (D) bubble(bc); }); }
  }
  document.addEventListener("at:data", function (e) { init(e.detail); });
  if (window.ATools) init(window.ATools.data);
})();
