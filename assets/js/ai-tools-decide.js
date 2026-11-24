/* AI Tools Landscape (ai-tools.html): the "decide" charts.
   atl  price ladder        (What it costs)      every tool's cheapest paid plan by category, median tick and middle-half band
   ats  category scorecard  (Compare categories) heatmap table: free plan, open source, self-host, hidden price, typical price, Canada, churn
   atc  Canada check        (Canada check)       coverage bar + matrix of tools with Canadian hosting, French interface or Canadian-company evidence
   atr  vendor risk         (Vendor risk)        share of each category's tools that were acquired, renamed, sunsetting or shut down
   Data: window.ATools.data (event "at:data" from ai-tools.js). Helpers (tooltips, data table, money, PNG export): window.ATCharts from
   ai-tools-charts.js, which loads first. Every caption is computed here from the data; content/gen/ai_tools_page.py writes the same
   numbers into the static page for the default view. */
(function () {
  "use strict";
  var D, K, layerName = {};
  var HI = "#0B6FA4", LO = "#868E9A", BAND = "#DCEAF4", INK = "#0B2A5A", MUTED = "#5A6475", GRID = "#E4E1D8";
  var LADDER_MIN = 6, MED_MIN = 4, RISK_MIN = 8, RISK_TOP = 15;

  var q = function (a, p) { a = a.slice().sort(function (x, y) { return x - y; }); var i = (a.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i); return a[lo] + (a[hi] - a[lo]) * (i - lo); };
  var priced = function (t) { return t.ep > 0 && (t.cur || "USD") === "USD"; };
  var pct = function (k, n) { return n ? Math.round(100 * k / n) : 0; };
  var andList = function (a) { return a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]; };
  var el = function (id) { return document.getElementById(id); };
  function onKeyActivate(root, attr, fn) {
    root.addEventListener("keydown", function (e) {
      var t = e.target.closest && e.target.closest("[" + attr + "]");
      if (t && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); fn(t.getAttribute(attr)); }
    });
  }
  function svgDot(c, r) { return '<svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="' + (r || 5) + '" fill="' + c + '"/></svg>'; }

  /* ================= 1. price ladder ================= */
  var LBL = { free: "Has a free plan", oss: "Open source or open core", cav: "Canadian company" };
  var lad = { hi: "free", layer: "" };
  function ladderRows(layer) {
    var out = [];
    D.categories.forEach(function (c) {
      if (layer && c.l !== layer) return;
      var ts = D.tools.filter(function (t) { return t.c === c.c && priced(t); });
      if (ts.length < LADDER_MIN) return;
      var ps = ts.map(function (t) { return t.ep; });
      out.push({ c: c.c, l: c.l, n: c.n, np: ts.length, tools: ts, med: K.median(ps), q1: q(ps, 0.25), q3: q(ps, 0.75) });
    });
    return out.sort(function (a, b) { return a.med - b.med || a.c.localeCompare(b.c); });
  }
  function ladderCaption(layer) {
    var R = ladderRows(layer), all = D.tools.filter(function (t) { return priced(t) && (!layer || t.l === layer); });
    if (!R.length) return all.length ? "Too few tools in this layer publish a price to draw a ladder; the table below lists what there is." : "No tool in this layer publishes a US-dollar price.";
    var head = "Half of the " + all.length + " tools with a published price start at " + K.usd(K.median(all.map(function (t) { return t.ep; }))) + " a month or less. ";
    if (R.length === 1) return head + "The typical plan in " + R[0].c + " (median of " + R[0].np + " published prices) is " + K.usd(R[0].med) + ".";
    var lo = R[0].med, hi = R[R.length - 1].med;
    var los = R.filter(function (r) { return K.usd(r.med) === K.usd(lo); }).map(function (r) { return r.c; });
    var his = R.filter(function (r) { return K.usd(r.med) === K.usd(hi); }).map(function (r) { return r.c; });
    if (K.usd(lo) === K.usd(hi)) return head + "The typical plan is " + K.usd(lo) + " in every category shown (" + andList(los) + ").";
    return head + "The typical plan (median of at least " + LADDER_MIN + " published prices) runs from " + K.usd(lo) + " (" + andList(los) + ") to " + K.usd(hi) + " (" + andList(his) + ").";
  }
  function ladder(card) {
    var fig = card.querySelector(".at-fig"), R = ladderRows(lad.layer), isHi = function (t) { return lad.hi === "" ? true : !!t[lad.hi]; };
    var W = fig.clientWidth, small = W < 620, X0 = 2, X1 = 3000;
    var longest = R.reduce(function (a, r) { return Math.max(a, (r.c + " (" + r.np + ")").length); }, 20);
    var m = { l: small ? 8 : Math.min(330, Math.round(longest * 7.3 + 24)), r: small ? 8 : 70, t: 26, b: 48 };
    var rowH = small ? 52 : 30, iw = W - m.l - m.r, H = m.t + Math.max(1, R.length) * rowH + m.b;
    var lx0 = Math.log(X0), lx1 = Math.log(X1);
    var X = function (v) { return m.l + (Math.log(Math.max(X0, Math.min(X1, v))) - lx0) / (lx1 - lx0) * iw; };
    var s = '<svg xmlns="' + K.NS + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="group" aria-label="Strip chart: cheapest paid plan of each tool, per category, with the category median and middle half">';
    s += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    R.forEach(function (r, i) { if (i % 2 === 0) s += '<rect x="0" y="' + (m.t + i * rowH) + '" width="' + W + '" height="' + rowH + '" fill="#FAF9F6"/>'; });  // row bands under the grid
    [2, 5, 10, 20, 50, 100, 200, 500, 1000].forEach(function (v) {
      if (small && (v === 5 || v === 200 || v === 500)) return;
      var x = X(v);
      if (small) R.forEach(function (r, i) { var y0 = m.t + i * rowH; s += '<line x1="' + x + '" x2="' + x + '" y1="' + (y0 + 21) + '" y2="' + (y0 + rowH) + '" stroke="' + GRID + '"/>'; });  // row titles stay clear
      else s += '<line x1="' + x + '" x2="' + x + '" y1="' + (m.t - 6) + '" y2="' + (H - m.b + 4) + '" stroke="' + GRID + '"/>';
      s += K.text(x, H - m.b + 20, "$" + v.toLocaleString("en-CA"), { anchor: "middle", size: 11, fill: MUTED });
    });
    s += K.text(m.l + iw / 2, H - 6, small ? "Cheapest paid plan, USD/month (log scale)" : "Cheapest paid plan, USD per month (log scale; some plans include more than one seat)", { anchor: "middle", size: small ? 11 : 12, fill: MUTED });
    if (!small) s += K.text(m.l - 12, m.t - 10, "Category (tools with a price)", { anchor: "end", size: 11, fill: MUTED }) + K.text(W - 4, m.t - 10, "Median", { anchor: "end", size: 11, fill: MUTED });
    if (!R.length) s += K.text(W / 2, m.t + 20, "No category in this layer has " + LADDER_MIN + " or more published prices", { anchor: "middle", size: 13, fill: MUTED });
    var tips = {}, k = 0, table = [];
    R.forEach(function (r, i) {
      var y0 = m.t + i * rowH, cy = small ? y0 + 36 : y0 + rowH / 2;
      var lab = small ? r.c + " · " + r.np + " prices · median " + K.usd(r.med) : r.c;
      s += K.text(small ? m.l : m.l - 12, small ? y0 + 15 : cy + 4, lab + (small ? "" : " (" + r.np + ")"), { anchor: small ? "start" : "end", size: small ? 12.5 : 13, weight: 600,
        extra: ' class="atl-cat" data-cat="' + K.esc(r.c) + '" tabindex="0" role="link" aria-label="Show ' + K.esc(r.c) + ' on the map" style="cursor:pointer"' });
      if (!small) s += K.text(W - 4, cy + 4, K.usd(r.med), { anchor: "end", size: 13, weight: 600 });
      s += '<rect x="' + X(r.q1).toFixed(1) + '" y="' + (cy - 9) + '" width="' + Math.max(2, X(r.q3) - X(r.q1)).toFixed(1) + '" height="18" rx="4" fill="' + BAND + '"/>';
      s += '<line x1="' + X(r.med).toFixed(1) + '" x2="' + X(r.med).toFixed(1) + '" y1="' + (cy - 11) + '" y2="' + (cy + 11) + '" stroke="' + INK + '" stroke-width="2" stroke-linecap="round"/>';
      var ts = r.tools.slice().sort(function (a, b) { return (isHi(a) - isHi(b)) || a.ep - b.ep || a.n.localeCompare(b.n); }), placed = [];
      ts.forEach(function (t) {
        var x = X(t.ep), kk = 0; placed.forEach(function (p) { if (Math.abs(p - x) < 7) kk++; }); placed.push(x);
        var off = kk === 0 ? 0 : (kk % 2 ? -1 : 1) * Math.ceil(kk / 2) * 4, y = cy + Math.max(-10, Math.min(10, off)), on = isHi(t), key = "l" + (k++);
        var flags = [t.free ? "Free plan" : "No free plan", t.oss ? "Open source" : "", t.cav ? "Canadian company" : ""].filter(Boolean).join(" · ");
        tips[key] = "<strong>" + K.usd(t.ep) + "/mo</strong> · " + K.esc(t.n) + "<br><span>" + K.esc(t.c) + "</span>" +
          (t.pp ? "<br>Next plan up: " + K.usd(t.pp) + "/mo" : "") + (t.pt ? "<br><span>" + K.esc(t.pt) + "</span>" : "") + "<br>" + flags + "<br><span>Select to open the tool</span>";
        s += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (on ? 5 : 4) + '" fill="' + (on ? HI : LO) + '" stroke="#fff" stroke-width="2" pointer-events="none"/>';
        s += '<circle class="at-hit" data-k="' + key + '" data-id="' + K.esc(t.id) + '" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + (small ? 8 : 11) + '" fill="transparent" tabindex="0" role="button" aria-label="' +
          K.esc(t.n) + ": " + K.usd(t.ep) + " a month" + (t.free ? ", free plan" : "") + '" style="cursor:pointer"/>';
        if (t.ep > X1) s += K.text(x + 8, y + 4, "›", { size: 11, fill: MUTED });
        if (t.ep < X0) s += K.text(x - 8, y + 4, "‹", { anchor: "end", size: 11, fill: MUTED });
      });
      table.push([r.c, layerName[r.l], r.np + " of " + r.n, K.usd(r.q1), K.usd(r.med), K.usd(r.q3),
        r.tools.filter(function (t) { return t.free; }).length, r.tools.filter(function (t) { return t.oss; }).length, r.tools.filter(function (t) { return t.cav; }).length]);
    });
    s += "</svg>";
    fig.innerHTML = s;
    card.querySelector(".at-cap").textContent = ladderCaption(lad.layer);
    var lg = lad.hi ? [svgDot(HI) + LBL[lad.hi], svgDot(LO, 4) + "Other tools"] : [svgDot(HI) + "Tool"];
    lg.push('<svg width="12" height="14" aria-hidden="true"><line x1="6" x2="6" y1="1" y2="13" stroke="' + INK + '" stroke-width="2" stroke-linecap="round"/></svg>Median');
    lg.push('<svg width="18" height="12" aria-hidden="true"><rect x="0" y="1" width="18" height="10" rx="3" fill="' + BAND + '"/></svg>Middle half of tools');
    card.querySelector(".atl-legend").innerHTML = K.legend(lg);
    var ncat = D.categories.filter(function (c) { return !lad.layer || c.l === lad.layer; }).length;
    card.querySelector(".at-figfoot").innerHTML = '<p class="ll-chartnote">Each dot is one tool\'s cheapest paid plan as published in ' + K.esc(D.checked) +
      "; the dark tick is the category median and the shaded band holds the middle half of tools. Shown: categories with at least " + LADDER_MIN + " published US-dollar prices (" + R.length + " of " + ncat +
      (small ? "; each row gives how many" : "; the number after each name is how many") + "). Contact-sales and usage-only tools have no entry price and are not shown; some plans are billed annually or include several seats. <strong>Select a dot to open the tool, or a category name to see it on the map.</strong></p>" +
      K.dataTable(["Category", "Layer", "Priced / tools", "25th percentile", "Median", "75th percentile", "Free plan", "Open source", "Canadian company"], table);
    K.bindTips(card, tips);
  }
  function ladderWire(card) {
    var fig = card.querySelector(".at-fig");
    fig.addEventListener("click", function (e) {
      var id = e.target.getAttribute && e.target.getAttribute("data-id"), cat = e.target.getAttribute && e.target.getAttribute("data-cat");
      if (id && window.ATools) window.ATools.open(id); else if (cat && window.ATools) window.ATools.showCategory(cat);
    });
    onKeyActivate(fig, "data-id", function (id) { if (window.ATools) window.ATools.open(id); });
    onKeyActivate(fig, "data-cat", function (c) { if (window.ATools) window.ATools.showCategory(c); });
    card.querySelectorAll("[data-atl-h]").forEach(function (b) {
      b.addEventListener("click", function () {
        lad.hi = b.getAttribute("data-atl-h");
        card.querySelectorAll("[data-atl-h]").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        ladder(card);
      });
    });
    el("atl-layer").addEventListener("change", function (e) { lad.layer = e.target.value; ladder(card); });
  }

  /* ================= shared: churn per category (market events only; list clean-ups excluded) ================= */
  function churn(cat) {
    var ts = D.tools.filter(function (t) { return t.c === cat; }), v = { acq: 0, ren: 0, sun: 0, gone: 0 };
    ts.forEach(function (t) {
      if (t.b === "Acquired" || t.b === "Acquisition pending") v.acq++;
      else if (t.b === "Renamed" || t.b === "Merged") v.ren++;
      else if (t.b === "Sunsetting") v.sun++;
    });
    var ret = D.retired.filter(function (r) { return r.ev && r.cc === cat; });
    ret.forEach(function (r) {
      if (r.status === "acquired") v.acq++; else if (r.status === "renamed") v.ren++; else if (r.status === "sunsetting") v.sun++; else v.gone++;
    });
    v.k = v.acq + v.ren + v.sun + v.gone; v.n = ts.length + ret.length; v.cur = ts.length; v.share = v.n ? v.k / v.n : 0;
    return v;
  }

  /* ================= 2. category scorecard ================= */
  var STOPS = [[236, 244, 249], [158, 200, 226], [11, 111, 164], [6, 60, 96]];
  function rampRaw(p) {
    p = Math.max(0, Math.min(1, p)); var f = p * (STOPS.length - 1), i = Math.min(STOPS.length - 2, Math.floor(f)), u = f - i;
    return "rgb(" + STOPS[i].map(function (a, j) { return Math.round(a + (STOPS[i + 1][j] - a) * u); }).join(",") + ")";
  }
  // one hue, light -> dark; the mid-tones where neither navy nor white text reaches 4.5:1 are skipped, so the step falls at 50% ("most")
  function ramp(p) { return p < 0.5 ? rampRaw(p) : rampRaw(0.65 + (p - 0.5) * 0.7); }
  var inkOn = function (p) { return p < 0.5 ? INK : "#fff"; };
  var COLS = [
    { k: "free", h: "Free plan", s: "share of tools", pct: true, tip: "have a free plan" },
    { k: "oss", h: "Open source", s: "or open core", pct: true, tip: "are open source or open core" },
    { k: "self", h: "Can self-host", s: "on your servers", pct: true, tip: "can be self-hosted" },
    { k: "sales", h: "Price hidden", s: "contact sales only", pct: true, tip: "only quote through sales" },
    { k: "med", h: "Typical entry", s: "median, USD/mo", pct: false },
    { k: "cav", h: "Canadian companies", s: "tools", pct: false },
    { k: "ca", h: "Canada hosting", s: "confirmed of checked", pct: false },
    { k: "churn", h: "Vendor changes", s: "acquired, renamed, sunsetting, gone", pct: true, tip: "saw a vendor change: acquired (incl. pending), renamed or merged, sunsetting, or shut down or folded in (share of current plus gone tools)" }
  ];
  var sc = { sortK: null, dir: -1, layer: "" }, scRows = null;
  function scoreRows() {
    if (scRows) return scRows;
    scRows = D.categories.map(function (c) {
      var ts = D.tools.filter(function (t) { return t.c === c.c; }), n = ts.length, ps = ts.filter(priced).map(function (t) { return t.ep; }), ch = churn(c.c);
      var cnt = function (f) { return ts.filter(f).length; };
      return { c: c.c, l: c.l, n: n,
        free: cnt(function (t) { return t.free; }), oss: cnt(function (t) { return t.oss; }), self: cnt(function (t) { return (t.dep || []).indexOf("self-hosted") >= 0; }),
        sales: cnt(function (t) { return t.pm === "enterprise"; }), med: ps.length >= MED_MIN ? K.median(ps) : null, np: ps.length, cav: cnt(function (t) { return t.cav; }),
        caY: cnt(function (t) { return t.ca === "yes"; }), caS: cnt(function (t) { return t.ca === "self-host"; }), caK: cnt(function (t) { return t.ca && t.ca !== "unknown"; }),
        churnK: ch.k, churnN: ch.n };
    });
    return scRows;
  }
  function share(r, k) { return k === "churn" ? (r.churnN ? r.churnK / r.churnN : 0) : r[k] / r.n; }
  function count(r, k) { return k === "churn" ? r.churnK + " of " + r.churnN : r[k] + " of " + r.n; }
  function scoreCaption(layer) {
    var R = scoreRows().filter(function (r) { return !layer || r.l === layer; });
    var open = R.filter(function (r) { return r.self / r.n >= 0.5; }).length, hid = R.filter(function (r) { return r.sales / r.n > 0.5; })
      .sort(function (a, b) { return b.sales / b.n - a.sales / a.n || a.c.localeCompare(b.c); }).map(function (r) { return r.c; });
    return open + " of " + R.length + " categories let you self-host at least half their tools; " +
      (hid.length ? "in " + hid.length + " (" + hid.slice(0, 3).join(", ") + (hid.length > 3 ? " and " + (hid.length - 3) + " more" : "") + ") most vendors hide the price behind a sales call." : "in none of them do most vendors hide the price behind a sales call.");
  }
  function scoreVisible() {
    var R = scoreRows().filter(function (r) { return !sc.layer || r.l === sc.layer; });
    var val = function (r) { return sc.sortK === "med" ? (r.med == null ? -1 : r.med) : sc.sortK === "ca" ? r.caY + r.caS + r.caK / 1000 : sc.sortK === "cav" ? r.cav : share(r, sc.sortK); };
    if (sc.sortK) R = R.slice().sort(function (a, b) { return sc.dir * (val(a) - val(b)) || a.c.localeCompare(b.c); });
    return R;
  }
  function scorecard(card) {
    var R = scoreVisible(), h = '<thead><tr><th scope="col" class="ats-cat">Category</th>';
    COLS.forEach(function (col) {
      var on = sc.sortK === col.k;
      h += '<th scope="col" aria-sort="' + (on ? (sc.dir < 0 ? "descending" : "ascending") : "none") + '"><button type="button" data-ats-sort="' + col.k + '"><span class="ats-ar" aria-hidden="true">' + (on ? (sc.dir < 0 ? "▼" : "▲") : "") + "</span><span>" + K.esc(col.h) + "</span><small>" + K.esc(col.s) + "</small></button></th>";
    });
    h += "</tr></thead>" + (sc.sortK ? "<tbody>" : "");
    var last = null;
    R.forEach(function (r) {
      if (!sc.sortK && r.l !== last) { h += (last ? "</tbody>" : "") + '<tbody><tr class="ats-grp"><th scope="rowgroup" colspan="' + (COLS.length + 1) + '" class="ats-cat">' + K.esc(r.l + " · " + layerName[r.l]) + "</th></tr>"; last = r.l; }
      h += '<tr><th scope="row" class="ats-cat"><a href="#map" data-ats-cat="' + K.esc(r.c) + '">' + K.esc(r.c) + '</a><span class="ats-n">' + r.n + " tools</span></th>";
      COLS.forEach(function (col) {
        if (col.pct) {
          var v = share(r, col.k), p = Math.round(v * 100);
          h += '<td class="ats-h"><div style="background:' + ramp(v) + ";color:" + inkOn(v) + '" data-tip="' + K.esc("<strong>" + p + "%</strong> of " + K.esc(r.c) + " tools " + col.tip + " <span>(" + count(r, col.k) + ")</span>") +
            '">' + p + '%<span class="visually-hidden"> (' + count(r, col.k) + ")</span></div></td>";
        } else if (col.k === "med") {
          h += r.med == null ? '<td class="ats-v ats-dim">–<small>' + r.np + (r.np === 1 ? " price" : " prices") + "</small></td>"
            : '<td class="ats-v' + (r.np < LADDER_MIN ? " ats-few" : "") + '">' + K.usd(r.med) + (r.np < LADDER_MIN ? "<small>from " + r.np + " prices</small>" : "") + "</td>";
        } else if (col.k === "cav") {
          h += '<td class="ats-v' + (r.cav ? "" : " ats-dim") + '">' + (r.cav ? r.cav : "–") + "</td>";
        } else {
          h += r.caK ? '<td class="ats-v ats-ca" data-tip="' + K.esc("<strong>" + (r.caY + r.caS) + " of " + r.caK + "</strong> checked tools can keep data in Canada: " + r.caY + " in the vendor's Canadian cloud, " + r.caS + " if you self-host. <span>" + (r.n - r.caK) + " of the category's " + r.n + " tools are not checked yet.</span>") + '"><b>' + (r.caY + r.caS) + "</b> of " + r.caK + " checked<small>" + r.caY + " cloud · " + r.caS + " self-host</small></td>"
            : '<td class="ats-v ats-dim">not checked</td>';
        }
      });
      h += "</tr>";
    });
    h += "</tbody>";
    card.querySelector(".ats-t").innerHTML = h;
    card.querySelector(".at-cap").textContent = scoreCaption(sc.layer);
  }
  function scoreLegendSvg() {
    var s = ""; for (var i = 0; i < 10; i++) s += '<rect x="' + (i * 14) + '" y="1" width="14" height="10" fill="' + ramp((i + 0.5) / 10) + '"/>';
    return '<svg width="140" height="12" aria-hidden="true">' + s + "</svg>";
  }
  function scorePng(card) {
    var R = scoreVisible(), cw = 120, c0 = 340, W = c0 + cw * COLS.length + 16, rh = 30, hh = 62, rows = [], last = null;
    R.forEach(function (r) { if (!sc.sortK && r.l !== last) { last = r.l; rows.push({ g: r.l + " · " + layerName[r.l] }); } rows.push(r); });
    var H = hh + rows.length * rh + 8, s = "";
    s += K.text(16, hh - 10, "Category", { size: 11.5, weight: 600, fill: "#3F4A5C" });
    COLS.forEach(function (col, i) {
      var x = c0 + i * cw + cw / 2, words = col.h.split(" "), l1 = col.h, l2 = "";
      if (col.h.length > 14) { l1 = words.slice(0, Math.ceil(words.length / 2)).join(" "); l2 = words.slice(Math.ceil(words.length / 2)).join(" "); }
      s += (l2 ? K.text(x, hh - 38, l1, { anchor: "middle", size: 11.5, weight: 600, fill: "#3F4A5C" }) + K.text(x, hh - 24, l2, { anchor: "middle", size: 11.5, weight: 600, fill: "#3F4A5C" })
        : K.text(x, hh - 24, l1, { anchor: "middle", size: 11.5, weight: 600, fill: "#3F4A5C" })) + K.text(x, hh - 10, col.s, { anchor: "middle", size: 10, fill: MUTED });
    });
    s += '<line x1="8" x2="' + (W - 8) + '" y1="' + hh + '" y2="' + hh + '" stroke="#D9D5CA"/>';
    rows.forEach(function (r, i) {
      var y = hh + i * rh, ty = y + rh / 2 + 4;
      if (r.g) { s += '<rect x="8" y="' + y + '" width="' + (W - 16) + '" height="' + rh + '" fill="#F6F5F1"/>' + K.text(16, ty, r.g, { size: 12, weight: 600 }); return; }
      s += K.text(16, ty, r.c, { size: 12.5, weight: 600 }) + K.text(c0 - 10, ty, r.n + " tools", { anchor: "end", size: 11, fill: MUTED });
      COLS.forEach(function (col, j) {
        var x = c0 + j * cw;
        if (col.pct) { var v = share(r, col.k); s += '<rect x="' + (x + 2) + '" y="' + (y + 2) + '" width="' + (cw - 4) + '" height="' + (rh - 4) + '" rx="4" fill="' + ramp(v) + '"/>' + K.text(x + cw / 2, ty, Math.round(v * 100) + "%", { anchor: "middle", size: 12, fill: inkOn(v) }); }
        else if (col.k === "ca" && r.caK) {
          s += K.text(x + cw / 2, y + 13, (r.caY + r.caS) + " of " + r.caK + " checked", { anchor: "middle", size: 11.5, fill: INK }) +
            K.text(x + cw / 2, y + 25, r.caY + " cloud · " + r.caS + " self-host", { anchor: "middle", size: 9.5, fill: MUTED });
        } else {
          var t = col.k === "med" ? (r.med == null ? "–" : K.usd(r.med) + (r.np < LADDER_MIN ? " (" + r.np + " prices)" : "")) : col.k === "cav" ? (r.cav ? String(r.cav) : "–") : "not checked";
          var dim = col.k === "med" ? r.med == null : col.k === "cav" ? !r.cav : true;
          s += K.text(x + cw / 2, ty, t, { anchor: "middle", size: col.k === "med" && r.np < LADDER_MIN ? 11 : 12, fill: dim ? MUTED : INK });
        }
      });
      s += '<line x1="8" x2="' + (W - 8) + '" y1="' + (y + rh) + '" y2="' + (y + rh) + '" stroke="#EEECE6"/>';
    });
    var notes = ["Shares are of each category's current tools; Vendor changes is a share of current plus gone tools (acquired incl. pending, renamed or merged, sunsetting,",
      "shut down or folded in; duplicates and list clean-ups not counted). Typical entry: median of at least " + MED_MIN + " published US-dollar prices (fewer than " + LADDER_MIN + " shown in brackets).",
      "Canada hosting: tools that can keep data in Canada out of the tools checked so far; most tools are not checked yet, and not checked does not mean not available."];
    notes.forEach(function (l, i) { s += K.text(16, H + 14 + i * 16, l, { size: 11, fill: MUTED }); });
    H += 18 + notes.length * 16;
    return { W: W, H: H, svg: '<rect width="' + W + '" height="' + H + '" fill="#fff"/>' + s };
  }
  function scoreWire(card) {
    var t = card.querySelector(".ats-t");
    card._atPng = function () { return scorePng(card); };
    card.querySelector(".ats-scale").innerHTML = K.legend([scoreLegendSvg() + "0% to 100% of the category's tools (the step marks half)"]);
    t.addEventListener("click", function (e) {
      var b = e.target.closest("[data-ats-sort]");
      if (b) {
        var k = b.getAttribute("data-ats-sort");
        if (sc.sortK === k) { sc.dir = -sc.dir; if (sc.dir < 0) sc.sortK = null; } else { sc.sortK = k; sc.dir = -1; }
        scorecard(card); var f = t.querySelector('[data-ats-sort="' + k + '"]'); if (f) f.focus(); return;
      }
      var a = e.target.closest("[data-ats-cat]");
      if (a && window.ATools) { e.preventDefault(); window.ATools.showCategory(a.getAttribute("data-ats-cat")); }
    });
    var show = function (d, e) { K.tipOn(card, d.getAttribute("data-tip"), e, d); };
    t.addEventListener("pointermove", function (e) { var d = e.target.closest && e.target.closest("[data-tip]"); if (d) show(d, e); else K.tipOff(card); });
    t.addEventListener("pointerleave", function () { K.tipOff(card); });
    el("ats-layer").addEventListener("change", function (e) { sc.layer = e.target.value; scorecard(card); });
  }

  /* ================= 3. Canada check ================= */
  var NAVY = "#0B2A5A", GREY = "#5A6475", FAINT = "#868E9A";
  var MARK = {
    yes: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="' + HI + '"/></svg>',
    some: '<svg width="22" height="16" viewBox="0 0 22 16" aria-hidden="true"><circle cx="8" cy="8" r="6" fill="' + HI + '"/><text x="18" y="9" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="13" font-weight="700" fill="' + NAVY + '">*</text></svg>',
    self: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="5.25" fill="#fff" stroke="' + HI + '" stroke-width="1.5"/><path d="M8 2.75a5.25 5.25 0 0 1 0 10.5z" fill="' + HI + '"/></svg>',
    no: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 5l6 6M11 5l-6 6" stroke="' + GREY + '" stroke-width="1.8" stroke-linecap="round"/></svg>',
    unk: '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 8h6" stroke="' + FAINT + '" stroke-width="1.8" stroke-linecap="round"/></svg>',
    flag: '<svg width="22" height="16" viewBox="0 0 22 16" aria-hidden="true"><rect x="0.5" y="1" width="21" height="14" rx="3" fill="' + NAVY + '"/><text x="11" y="11.5" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="8.5" font-weight="700" fill="#fff">CA</text></svg>'
  };
  var CLAB = { yes: "Yes", some: "Yes, on some plans only", self: "Self-host only", no: "No", unk: "Not checked" };
  var hostK = function (t) { return t.ca === "yes" ? (t.cap ? "some" : "yes") : t.ca === "self-host" ? "self" : t.ca === "no" ? "no" : "unk"; };
  var frK = function (t) { return t.fr === "yes" ? "yes" : t.fr === "no" ? "no" : "unk"; };
  var cf = { host: true, cav: false, fr: false, free: false }, carea = "";
  function caPool() { return D.tools.filter(function (t) { return (t.ca && t.ca !== "unknown") || (t.fr && t.fr !== "unknown") || t.cav; }); }
  // the price column names the pricing model when there is no US-dollar entry price; "free plan" is only an extra tag
  function priceText(t) {
    if (priced(t)) return "from " + K.usd(t.ep);
    if (t.ep > 0 && t.cur && t.cur !== "USD") return "priced in " + t.cur;
    return { enterprise: "contact sales", "open-source": "open source", "open-core": "open source + paid cloud", usage: "usage-based", subscription: "see pricing", freemium: "free plan + paid", free: "free" }[t.pm] || "see pricing";
  }
  function caScore(t) { return (t.ca === "yes" ? 4 : t.ca === "self-host" ? 3 : 0) + (t.fr === "yes" ? 2 : 0) + (t.cav ? 1 : 0); }
  function caCoverage() {
    var T = D.tools, n = T.length, y = T.filter(function (t) { return t.ca === "yes"; }).length, s = T.filter(function (t) { return t.ca === "self-host"; }).length, no = T.filter(function (t) { return t.ca === "no"; }).length;
    return { n: n, parts: [["Hosted in Canada (vendor cloud)", y, HI, "#fff"], ["Self-host only", s, "#6FA9CF", INK], ["Checked: no", no, "#B9BFC9", INK], ["Not checked yet", n - y - s - no, "#EEECE6", MUTED]] };
  }
  function caVisible() {
    var R = caPool().filter(function (t) {
      return (!carea || t.l === carea) && (!cf.host || t.ca === "yes" || t.ca === "self-host") && (!cf.cav || t.cav) && (!cf.fr || t.fr === "yes") && (!cf.free || t.free);
    });
    var cats = {}; R.forEach(function (t) { (cats[t.c] = cats[t.c] || []).push(t); });
    return D.categories.map(function (c) { return c.c; }).filter(function (c) { return cats[c]; }).map(function (c) {
      return { c: c, ts: cats[c].sort(function (a, b) { return caScore(b) - caScore(a) || a.n.localeCompare(b.n); }) };
    });
  }
  function canada(card) {
    var G = caVisible(), n = 0, h = '<thead><tr><th scope="col" class="atc-nm">Tool</th><th scope="col">Hosted in Canada</th><th scope="col">French interface</th><th scope="col">Canadian company</th><th scope="col" class="atc-hide-sm">Free plan</th><th scope="col" class="atc-pr">Price</th></tr></thead>';
    var mk = function (k, cls) { return '<td' + (cls ? ' class="' + cls + '"' : "") + '><span class="atc-mk' + (k === "some" ? " atc-mk-w" : "") + '">' + (MARK[k] || "") + '</span><span class="visually-hidden">' + (k === "flag" ? "Yes" : CLAB[k] || "") + "</span></td>"; };
    G.forEach(function (g) {
      h += '<tbody><tr class="atc-grp"><th scope="rowgroup" colspan="6">' + K.esc(g.c) + " · " + g.ts.length + "</th></tr>";
      g.ts.forEach(function (t) {
        n++;
        var pt = priceText(t);
        h += '<tr class="atc-row" data-atc-id="' + K.esc(t.id) + '"><th scope="row" class="atc-nm"><button type="button" data-atc-open="' + K.esc(t.id) + '">' + K.esc(t.n) + '</button><span class="atc-v">' + K.esc(t.v) + "</span>" +
          '<span class="atc-mp">' + K.esc(pt + (t.free && !/free/.test(pt) ? " · free plan" : "")) + "</span></th>" +
          mk(hostK(t)) + mk(frK(t)) + (t.cav ? mk("flag") : '<td><span class="visually-hidden">No</span></td>') + mk(t.free ? "yes" : "no", "atc-hide-sm") + '<td class="atc-pr">' + K.esc(pt) + "</td></tr>";
      });
      h += "</tbody>";
    });
    if (!n) h += '<tbody><tr><td colspan="6" class="atc-empty">No checked tool meets all of these filters yet. Remove a filter, or <a href="contact">ask us to check a tool you use</a>.</td></tr></tbody>';
    card.querySelector(".atc-t").innerHTML = h;
    el("atc-count").textContent = n + (n === 1 ? " tool" : " tools") + " shown";
  }
  function canadaPng(card) {
    var G = caVisible(), W = 820, rh = 22, cov = caCoverage(), cx = [470, 570, 670, 760], s = "", y = 8;
    s += K.text(16, y + 12, "Canadian hosting, all " + cov.n + " tools on the map", { size: 12, weight: 600, fill: "#3F4A5C" }); y += 20;
    var x = 16, bw = W - 32 - 6;
    cov.parts.forEach(function (p) {
      var w = p[1] / cov.n * bw; s += '<rect x="' + x.toFixed(1) + '" y="' + y + '" width="' + Math.max(1, w).toFixed(1) + '" height="24" rx="3" fill="' + p[2] + '"/>';
      if (w > 34) s += K.text(x + 8, y + 16, String(p[1]), { size: 12, weight: 600, fill: p[3] });
      x += w + 2;
    });
    y += 30; x = 16;
    cov.parts.forEach(function (p) { s += '<rect x="' + x + '" y="' + y + '" width="10" height="10" rx="2" fill="' + p[2] + '"/>' + K.text(x + 14, y + 9, p[0] + " (" + p[1] + ")", { size: 11, fill: MUTED }); x += 26 + (p[0].length + 6) * 5.9; });
    y += 36;
    ["Hosted in Canada", "French interface", "Canadian company", "Free plan"].forEach(function (hd, i) { s += K.text(cx[i], y, hd, { anchor: "middle", size: 11, weight: 600, fill: "#3F4A5C" }); });
    s += K.text(16, y, "Tool", { size: 11, weight: 600, fill: "#3F4A5C" }); y += 8;
    var mark = function (k, xx, yy) { if (!k) return ""; var w = k === "flag" || k === "some" ? 22 : 16; return '<g transform="translate(' + (xx - w / 2) + "," + (yy - 8) + ')">' + MARK[k].replace(/<svg[^>]*>/, "").replace("</svg>", "") + "</g>"; };
    G.forEach(function (g) {
      s += '<rect x="8" y="' + y + '" width="' + (W - 16) + '" height="' + rh + '" fill="#F6F5F1"/>' + K.text(16, y + 15, g.c + " · " + g.ts.length, { size: 11.5, weight: 600 }); y += rh;
      g.ts.forEach(function (t) {
        var nm = t.n.length > 44 ? t.n.slice(0, 43) + "…" : t.n;
        s += K.text(16, y + 15, nm, { size: 12, weight: 600 });
        s += mark(hostK(t), cx[0], y + rh / 2) + mark(frK(t), cx[1], y + rh / 2) + mark(t.cav ? "flag" : "", cx[2], y + rh / 2) + mark(t.free ? "yes" : "no", cx[3], y + rh / 2);
        s += '<line x1="8" x2="' + (W - 8) + '" y1="' + (y + rh) + '" y2="' + (y + rh) + '" stroke="#EEECE6"/>'; y += rh;
      });
    });
    if (!G.length) { s += K.text(16, y + 16, "No checked tool meets the selected filters.", { size: 12, fill: MUTED }); y += 24; }
    var f = []; if (carea) f.push(layerName[carea]); if (cf.host) f.push("hosted in Canada (incl. self-host)"); if (cf.cav) f.push("Canadian company"); if (cf.fr) f.push("French interface"); if (cf.free) f.push("free plan");
    y += 18; s += K.text(16, y, "Filters: " + (f.length ? f.join(", ") : "none") + ". * Hosting on some plans only.", { size: 11, fill: MUTED }); y += 16;
    s += K.text(16, y, "A dash means not checked yet (not a no); a blank Canadian company cell means not Canadian.", { size: 11, fill: MUTED }); y += 8;
    return { W: W, H: y, svg: '<rect width="' + W + '" height="' + y + '" fill="#fff"/>' + s };
  }
  function canadaWire(card) {
    var cov = caCoverage(), box = card.querySelector(".atc-cov");
    box.innerHTML = '<p class="atc-covh">Canadian hosting, all ' + cov.n + ' tools on the map</p><div class="atc-bar" role="img" aria-label="' + K.esc(cov.parts.map(function (p) { return p[0] + ": " + p[1]; }).join(", ")) + '">' +
      cov.parts.map(function (p) { return '<div style="flex:' + p[1] + ' 1 0;background:' + p[2] + ";color:" + p[3] + '" title="' + K.esc(p[0] + ": " + p[1]) + '">' + (p[1] / cov.n > 0.06 ? p[1] : "") + "</div>"; }).join("") + "</div>" +
      '<ul class="atc-covlg">' + cov.parts.map(function (p) { return '<li><span class="atc-sw" style="background:' + p[2] + '"></span>' + K.esc(p[0]) + " (" + p[1] + ")</li>"; }).join("") + "</ul>";
    card.querySelector(".atc-keys").innerHTML = K.legend([MARK.yes + "Yes", MARK.some + "Yes, on some plans only (hosting)", MARK.self + "Self-host only (hosting)", MARK.no + "Checked: no",
      MARK.unk + "Not checked yet (not a no)", MARK.flag + "Canadian company (blank: not Canadian)"]);
    card._atPng = function () { return canadaPng(card); };
    card.querySelectorAll("[data-atc-f]").forEach(function (c) {
      c.addEventListener("click", function () { var k = c.getAttribute("data-atc-f"); cf[k] = !cf[k]; c.setAttribute("aria-pressed", String(cf[k])); canada(card); });
    });
    el("atc-area").addEventListener("change", function (e) { carea = e.target.value; canada(card); });
    var t = card.querySelector(".atc-t");
    t.addEventListener("click", function (e) { var r = e.target.closest("[data-atc-id]"); if (r && window.ATools && !e.target.closest("a")) window.ATools.open(r.getAttribute("data-atc-id")); });
    var byId = {}; D.tools.forEach(function (x) { byId[x.id] = x; });
    var tip = function (row, e, anchor) {
      var x = byId[row.getAttribute("data-atc-id")];
      K.tipOn(card, "<strong>" + K.esc(x.n) + "</strong><br>Hosted in Canada: " + CLAB[hostK(x)] + "<br>French interface: " + CLAB[frK(x)] + (x.cav ? "<br>Canadian company" : "") +
        (x.can ? "<br><span>" + K.esc(x.can.replace(/^SELF-HOST[^:]*:\s*/i, "")) + "</span>" : ""), e, anchor);
    };
    t.addEventListener("pointermove", function (e) { var r = e.target.closest && e.target.closest("[data-atc-id]"); if (r) tip(r, e); else K.tipOff(card); });
    t.addEventListener("pointerleave", function () { K.tipOff(card); });
    t.addEventListener("focusin", function (e) { var b = e.target.closest("[data-atc-open]"); if (b) tip(b.closest("tr"), null, b); });
    t.addEventListener("focusout", function () { K.tipOff(card); });
  }

  /* ================= 4. vendor risk by category ================= */
  var riskAll = false;
  function riskRows() {
    return D.categories.filter(function (c) { return c.n >= RISK_MIN; }).map(function (c) { var v = churn(c.c); v.c = c.c; v.l = c.l; return v; })
      .sort(function (a, b) { return b.share - a.share || b.k - a.k || a.c.localeCompare(b.c); });
  }
  function risk(card) {
    var all = riskRows(), R = riskAll ? all : all.slice(0, RISK_TOP), fig = card.querySelector(".at-fig");
    var W = fig.clientWidth, small = W < 520, CW = 6.9;
    var longest = R.reduce(function (a, r) { return Math.max(a, r.c.length); }, 10);
    var want = Math.round(longest * 7.2 + 20), lw = small ? 0 : Math.min(want, Math.round(W * 0.42)), rh = small ? 44 : 28, tipW = 104;
    var fitLab = function (c) { if (small || lw >= want) return c; var mx = Math.floor((lw - 20) / 7.2); return c.length <= mx ? c : c.slice(0, mx - 1).replace(/[\s,&]+$/, "") + "…"; };
    var m = { l: (small ? 16 : 8) + lw, r: tipW, t: 8, b: 34 }, iw = Math.max(60, W - m.l - m.r), H = m.t + R.length * rh + m.b;
    var max = Math.max(0.1, Math.ceil(Math.max.apply(null, all.map(function (r) { return r.share; })) * 10) / 10);
    var X = function (v) { return m.l + v / max * iw; };
    var s = '<svg xmlns="' + K.NS + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="group" aria-label="Share of each category\'s tools that saw a vendor change: acquired, renamed, sunsetting or shut down">';
    s += '<rect width="' + W + '" height="' + H + '" fill="#fff"/>';
    for (var g = 0; g <= max + 1e-9; g += 0.1) {
      var x = X(g).toFixed(1);
      if (small) R.forEach(function (r, i) { var y0 = m.t + i * rh; s += '<line x1="' + x + '" x2="' + x + '" y1="' + (y0 + 16) + '" y2="' + (y0 + rh) + '" stroke="' + GRID + '"/>'; });  // category names stay clear
      else s += '<line x1="' + x + '" x2="' + x + '" y1="' + m.t + '" y2="' + (H - m.b) + '" stroke="' + GRID + '"/>';
      s += K.text(+x, H - m.b + 16, Math.round(g * 100) + "%", { anchor: "middle", size: 11, fill: MUTED });
    }
    s += K.text(small ? 16 : m.l + iw / 2, H - 4, small ? "Share of tools (current plus gone)" : "Share of the category's tools (current plus gone)", { anchor: small ? "start" : "middle", size: 11, fill: MUTED });
    var tips = {};
    R.forEach(function (r, i) {
      var y = m.t + i * rh + (small ? 20 : 5), bh = small ? 16 : 18, key = "r" + i, w = r.share / max * iw;
      s += K.text(small ? 16 : m.l - 10, small ? y - 5 : y + bh / 2 + 4, fitLab(r.c), { anchor: small ? "start" : "end", size: small ? 12 : 12.5, weight: 600,
        extra: ' data-cat="' + K.esc(r.c) + '" data-k="' + key + '" tabindex="0" role="link" aria-label="' + K.esc(r.c) + ": " + r.k + " of " + r.n + ' tools saw a vendor change. Show on the map" style="cursor:pointer"' });
      tips[key] = "<strong>" + K.esc(r.c) + "</strong><br>" + r.k + " of " + r.n + " tools (" + pct(r.k, r.n) + "%) saw a vendor change:<br>" +
        [["acquired or acquisition pending", r.acq], ["renamed or merged", r.ren], ["sunsetting", r.sun], ["shut down or folded into another product", r.gone]]
          .filter(function (p) { return p[1]; }).map(function (p) { return p[1] + " " + p[0]; }).join("<br>") +
        (r.k ? "" : "none") + "<br><span>" + r.cur + " current tools plus " + (r.n - r.cur) + " now gone. Select to show on the map.</span>";
      s += '<rect x="' + m.l + '" y="' + y + '" width="' + Math.max(r.k ? 3 : 0, w).toFixed(1) + '" height="' + bh + '" rx="3" fill="' + HI + '" pointer-events="none"/>';
      s += '<rect data-k="' + key + '" data-cat="' + K.esc(r.c) + '" x="' + m.l + '" y="' + (y - 4) + '" width="' + iw + '" height="' + (bh + 8) + '" fill="transparent" style="cursor:pointer"/>';
      s += K.text(m.l + Math.max(r.k ? 3 : 0, w) + 6, y + bh / 2 + 4, r.k + " of " + r.n + " (" + pct(r.k, r.n) + "%)", { size: 11.5, fill: INK, extra: ' pointer-events="none"' });
    });
    s += "</svg>";
    fig.innerHTML = s;
    var foot = card.querySelector(".at-figfoot"), cl = D.retired.filter(function (x) { return !x.ev; }).length;
    var ns = all.map(function (r) { return r.n; });
    foot.innerHTML = (all.length > RISK_TOP ? '<button type="button" class="gr-link atr-more" aria-expanded="' + riskAll + '">' + (riskAll ? "Show the top " + RISK_TOP + " only" : "Show all " + all.length + " categories") + "</button>" : "") +
      '<p class="ll-chartnote">Vendor changes: current tools marked acquired, acquisition pending, renamed, merged or sunsetting, plus tools that shut down, were folded into another product, acquired, renamed or are being retired and are now gone. ' +
      "Shown: the " + all.length + " categories with at least " + RISK_MIN + " current tools; they hold " + Math.min.apply(null, ns) + " to " + Math.max.apply(null, ns) + " tools each (current plus gone), so a difference of one or two tools is noise. " +
      "Each product counts once: " + cl + " removed entries that were duplicates or list clean-ups (not AI products, out of scope) are not counted.</p>" +
      K.dataTable(["Category", "Vendor changes", "Tools (current + gone)", "Share", "Acquired", "Renamed or merged", "Sunsetting", "Shut down or folded in"],
        all.map(function (r) { return [r.c, r.k, r.n, pct(r.k, r.n) + "%", r.acq, r.ren, r.sun, r.gone]; }));
    var more = foot.querySelector(".atr-more");
    if (more) more.addEventListener("click", function () { riskAll = !riskAll; risk(card); var b = card.querySelector(".atr-more"); if (b) b.focus(); });
    K.bindTips(card, tips);
  }
  function riskWire(card) {
    var fig = card.querySelector(".at-fig");
    fig.addEventListener("click", function (e) { var c = e.target.getAttribute && e.target.getAttribute("data-cat"); if (c && window.ATools) window.ATools.showCategory(c); });
    onKeyActivate(fig, "data-cat", function (c) { if (window.ATools) window.ATools.showCategory(c); });
  }

  /* ================= wiring ================= */
  var CARDS = { "at-ch-ladder": [ladder, ladderWire, true], "at-ch-score": [scorecard, scoreWire, false], "at-ch-canada": [canada, canadaWire, false], "at-ch-risk": [risk, riskWire, true] };
  function init(data) {
    if (D || !window.ATCharts) return; D = data; K = window.ATCharts;
    D.layers.forEach(function (l) { layerName[l.id] = l.name; });
    Object.keys(CARDS).forEach(function (id) {
      var card = el(id); if (!card) return;
      var c = CARDS[id];
      card.querySelectorAll(".at-chwait").forEach(function (p) { p.remove(); });
      c[1](card);
      if (c[2]) { var w = 0; new ResizeObserver(function () { var nw = card.querySelector(".at-fig").clientWidth; if (nw && nw !== w) { w = nw; c[0](card); } }).observe(card.querySelector(".at-fig")); }
      else c[0](card);
      var b = card.querySelector("[data-png]"); if (b) b.addEventListener("click", function () { K.exportPng(card); });
    });
  }
  document.addEventListener("at:data", function (e) { init(e.detail); });
  if (window.ATools) init(window.ATools.data);
})();
