/* AI Tools Landscape (ai-tools.html): filters, map, list, cost per output, compare and PNG export (the "AI" menu dropdown is in main.js).
   Data: assets/data/ai-tools.json (built by content/aitools/build_data.py). Page: content/gen/ai_tools_page.py. */
(function () {
  "use strict";

  var root = document.getElementById("at-root");
  if (!root) return;
  var $ = function (id) { return document.getElementById(id); };
  var calm = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var safeUrl = function (u) { return /^https?:\/\//i.test(u || "") ? u : "#"; };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var money = function (v) {
    if (v == null) return "–";
    if (v === 0) return "$0";
    if (v < 0.01) return "$" + v.toPrecision(2);
    if (v < 1) return "$" + v.toFixed(3).replace(/0$/, "");
    if (v < 100) return "$" + v.toLocaleString("en-CA", { minimumFractionDigits: Math.round(v * 100) % 100 ? 2 : 0, maximumFractionDigits: 2 });
    return "$" + Math.round(v).toLocaleString("en-CA");
  };
  var D, T = [], byId = {}, state = { q: "", view: "map", sort: "n", dir: 1 }, picked = [];
  var form = root.querySelector(".gr-form"), panel = $("gr-filters");
  var GROUP_LABEL = { l: "Layer", c: "Category", pm: "Pricing", x: "", ca: "", dep: "", b: "Status" };
  var UNIT_WORD = {
    "per seat per month": ["Seats", "seats"], "per 1M tokens (input; note output)": ["Million input tokens per month", "M tokens"],
    "per image": ["Images per month", "images"], "per minute of video": ["Minutes of video per month", "min"],
    "per hour transcribed": ["Hours transcribed per month", "hours"], "per 1,000 task runs / executions": ["Thousand runs per month", "k runs"],
    "per 1,000 pages": ["Thousand pages per month", "k pages"], "per conversation": ["Conversations per month", "conversations"],
    "per resolution": ["Resolutions per month", "resolutions"], "per 1,000 API calls": ["Thousand API calls per month", "k calls"],
    "per 1,000 traces / spans": ["Thousand traces per month", "k traces"], "per 1M characters": ["Million characters per month", "M chars"],
    "per GPU-hour": ["GPU-hours per month", "GPU-h"], "per 1,000 emails": ["Thousand emails per month", "k emails"],
    "per minute of call": ["Call minutes per month", "min"], "per track": ["Tracks per month", "tracks"], "per browser-hour": ["Browser-hours per month", "hours"],
    "per minute of audio (TTS)": ["Minutes of audio per month", "min"], "per 1,000 words": ["Thousand words per month", "k words"],
    "per contact credit": ["Contacts per month", "contacts"], "per GB stored / month": ["GB stored", "GB"], "per 1M training tokens": ["Million training tokens per month", "M tokens"],
    "per sandbox-hour": ["Sandbox-hours per month", "hours"]
  };
  var DEFAULT_VOL = { "per seat per month": 10, "per image": 500, "per minute of video": 30, "per hour transcribed": 40, "per 1M tokens (input; note output)": 50,
    "per 1,000 task runs / executions": 10, "per 1,000 pages": 5, "per conversation": 1000, "per resolution": 500, "per 1,000 API calls": 50,
    "per 1,000 traces / spans": 100, "per 1M characters": 5, "per GPU-hour": 100, "per 1,000 emails": 20, "per minute of call": 2000, "per track": 20,
    "per minute of audio (TTS)": 60, "per browser-hour": 100, "per GB stored / month": 10, "per 1M training tokens": 20, "per sandbox-hour": 100, "per 1,000 words": 50, "per contact credit": 500 };
  var MAXVOL = 1e9;

  /* ---------- filtering ---------- */
  function checked(name) { return Array.prototype.map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (i) { return i.value; }); }
  function hay(t) { return (t._h = t._h || [t.n, t.v, t.d, t.c, (t.c2 || []).join(" "), (t.tags || []).join(" "), t.dom].join(" ").toLowerCase()); }
  function matches(t, f) {
    if (f.l.length && f.l.indexOf(t.l) < 0) return false;
    if (f.c.length && f.c.indexOf(t.c) < 0 && !(t.c2 || []).some(function (c) { return f.c.indexOf(c) >= 0; })) return false;
    if (f.pm.length && f.pm.indexOf(t.pm) < 0) return false;
    if (f.dep.length && !(t.dep || []).some(function (d) { return f.dep.indexOf(d) >= 0; })) return false;
    for (var i = 0; i < f.x.length; i++) {
      var x = f.x[i];
      if (x === "free" && !t.free) return false;
      if (x === "oss" && !t.oss) return false;
      if (x === "cmp" && !t.cmp) return false;
      if (x === "self" && (t.dep || []).indexOf("self-hosted") < 0) return false;
    }
    if (f.ca.length) {
      var caOk = f.ca.filter(function (v) { return v === "ca-yes" || v === "ca-self"; });
      if (caOk.length && !caOk.some(function (v) { return (v === "ca-yes" && t.ca === "yes") || (v === "ca-self" && t.ca === "self-host"); })) return false;
      if (f.ca.indexOf("fr") >= 0 && t.fr !== "yes") return false;
      if (f.ca.indexOf("cav") >= 0 && !t.cav) return false;
    }
    if (f.b.length) {
      var b = t.b || "none"; if (b === "Merged") b = "Renamed";
      if (f.b.indexOf(b) < 0) return false;
    }
    if (f.q) { var words = f.q.split(/\s+/); for (var w = 0; w < words.length; w++) if (hay(t).indexOf(words[w]) < 0) return false; }
    return true;
  }
  function current() {
    return { l: checked("l"), c: checked("c"), pm: checked("pm"), x: checked("x"), ca: checked("ca"), dep: checked("dep"), b: checked("b"), q: state.q.trim().toLowerCase() };
  }
  var hits = [];
  function apply() {
    var f = current();
    hits = T.filter(function (t) { return matches(t, f); });
    var set = {}; hits.forEach(function (t) { set[t.id] = 1; });
    var any = f.q || f.l.length || f.c.length || f.pm.length || f.x.length || f.ca.length || f.dep.length || f.b.length;
    // map
    root.querySelectorAll(".at-layer").forEach(function (L) {
      var ln = 0;
      L.querySelectorAll(".at-cat").forEach(function (C) {
        var cn = 0;
        C.querySelectorAll(".at-tile").forEach(function (b) { var on = !!set[b.dataset.id]; b.parentNode.hidden = !on; if (on) cn++; });
        C.hidden = cn === 0; C.querySelector("[data-catn]").textContent = cn; ln += cn;
      });
      L.hidden = ln === 0;
    });
    $("at-count").textContent = hits.length.toLocaleString("en-CA") + (hits.length === 1 ? " tool" : " tools") + (any ? " match" : "");
    root.querySelectorAll("[data-close-n]").forEach(function (e) { e.textContent = hits.length; });
    $("at-empty").hidden = hits.length > 0;
    mapFold(any);
    chips(f);
    if (state.view === "list") list();
    syncUrl(f);
  }

  /* ---------- collapsed map: a limited height with a fade until the reader asks for more, searches or filters ---------- */
  var folded = null;
  function setFold(on) {
    var m = $("at-panel-map"), b = $("at-mapmore"); if (!m || !b) return;
    folded = on; m.classList.toggle("at-collapsed", on);
    b.setAttribute("aria-expanded", on ? "false" : "true");
    b.textContent = on ? "Show the full map (" + T.length.toLocaleString("en-CA") + " tools)" : "Collapse the map";
  }
  function mapFold(any) {
    var w = $("at-mapmore-wrap"); if (!w) return;
    if (folded === null) setFold(!any);        // first run: collapsed unless the page opened with a search or filter (?q, ?c, ?l)
    else if (any && folded) setFold(false);    // searching or filtering always shows the whole result
    w.hidden = !!any || state.view !== "map";   // nothing to unfold while searching, filtering or in the list view
  }

  /* ---------- chips ---------- */
  function chips(f) {
    var ul = root.querySelector(".gr-chips"), n = 0, h = "";
    form.querySelectorAll("input:checked").forEach(function (i) {
      n++;
      var lab = i.closest("label").querySelector(".gr-opt-l").textContent, g = GROUP_LABEL[i.name];
      h += '<li><button type="button" class="gr-chip" data-chip="' + esc(i.name) + "|" + esc(i.value) + '"><span>' + esc((g ? g + ": " : "") + lab) +
        '</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg><span class="visually-hidden">Remove filter</span></button></li>';
    });
    if (f.q) { n++; h += '<li><button type="button" class="gr-chip" data-chip="q|"><span>Search: ' + esc(state.q.trim()) + '</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg><span class="visually-hidden">Remove search</span></button></li>'; }
    ul.innerHTML = h; ul.hidden = !n;
    root.querySelectorAll(".gr-statusbar [data-clear]").forEach(function (b) { b.hidden = !n; });
    var badge = root.querySelector("[data-active-n]"); badge.textContent = n; badge.hidden = !n;
    form.querySelectorAll(".gr-group").forEach(function (g) {
      var k = g.querySelectorAll("input:checked").length, s = g.querySelector("[data-sel]");
      s.textContent = k; s.hidden = !k;
    });
  }

  /* ---------- URL state (?q=, ?c=, ?l=) so other pages can link to a filtered view ---------- */
  function syncUrl(f) {
    try {
      var p = new URLSearchParams();
      if (f.q) p.set("q", f.q);
      f.c.forEach(function (c) { p.append("c", c); });
      f.l.forEach(function (l) { p.append("l", l); });
      var s = p.toString();
      history.replaceState(null, "", location.pathname + (s ? "?" + s : "") + location.hash);
    } catch (e) { /* ignore */ }
  }
  function readUrl() {
    try {
      var p = new URLSearchParams(location.search);
      if (p.get("q")) { state.q = p.get("q"); $("at-q").value = state.q; }
      ["c", "l"].forEach(function (k) {
        p.getAll(k).forEach(function (v) { var i = form.querySelector('input[name="' + k + '"][value="' + CSS.escape(v) + '"]'); if (i) { i.checked = true; i.closest("details").open = true; } });
      });
    } catch (e) { /* ignore */ }
  }

  /* ---------- list ---------- */
  var LIST_STEP = 200, listShown = LIST_STEP;
  function list(more) {
    if (!more) listShown = LIST_STEP;
    var k = state.sort, d = state.dir;
    var val = function (t) {
      if (k === "ep") return t.ep != null && t.cur === "USD" ? t.ep : (t.free ? 0 : null);
      if (k === "cpu") return t.cmp ? t.cpu : null;
      return t[k];
    };
    var rows = hits.slice().sort(function (a, b) {
      if (k === "cpu" && a.cmp && b.cmp && a.unit !== b.unit) return a.unit.localeCompare(b.unit);  // compare like with like: group by unit
      var x = val(a), y = val(b);
      if (x == null && y == null) return a.n.localeCompare(b.n);
      if (x == null) return 1; if (y == null) return -1;
      return (typeof x === "string" ? x.localeCompare(y) : x - y) * d || a.n.localeCompare(b.n);
    });
    var shown = rows.slice(0, listShown);
    $("at-tbody").innerHTML = shown.map(function (t) {
      var on = picked.indexOf(t.id) >= 0;
      var from = t.ep != null && t.cur === "USD" ? (t.ep === 0 ? "Free" : money(t.ep)) : (t.free ? "Free" : (t.cur && t.cur !== "USD" && t.ep != null ? esc(t.cur) : "–"));
      return '<tr><td class="at-tname"><button type="button" data-open="' + esc(t.id) + '">' + esc(t.n) + '</button><span class="at-sub">' + esc(t.d) + "</span></td>" +
        '<td class="at-hide-m">' + esc(t.c) + "</td>" +
        '<td class="num">' + from + (t.promo ? '<span class="at-sub">promotion</span>' : "") + "</td>" +
        '<td class="num">' + (t.cmp ? money(t.cpu) + '<span class="at-sub">' + esc(t.unit) + "</span>" : '<span class="at-sub">Not comparable</span>') + "</td>" +
        '<td><span class="at-flags at-hide-m">' + flags(t) + '</span><label class="at-cmpbox"><input type="checkbox" data-pick="' + esc(t.id) + '"' + (on ? " checked" : "") + "> Compare</label></td></tr>";
    }).join("") + (rows.length > shown.length ? '<tr><td colspan="5" class="at-more"><button type="button" class="btn btn-ghost" data-more>Show ' + Math.min(LIST_STEP, rows.length - shown.length) + " more (" + (rows.length - shown.length) + " left)</button></td></tr>" : "");
    root.querySelectorAll(".at-table .ll-th").forEach(function (b) { b.closest("th").setAttribute("aria-sort", b.dataset.sort === k ? (d > 0 ? "ascending" : "descending") : "none"); });
    $("at-cpu-note").hidden = k !== "cpu";
  }
  function flags(t) {
    return (t.free ? '<span class="at-flag on">Free plan</span>' : "") + (t.oss ? '<span class="at-flag on">Open source</span>' : "") +
      (t.ca === "yes" ? '<span class="at-flag ca" title="' + esc(t.can || "") + '">Canada hosting' + (t.cap ? " (some plans)" : "") + "</span>" : t.ca === "self-host" ? '<span class="at-flag">Self-host in Canada</span>' : "") +
      (t.cav ? '<span class="at-flag ca">Canadian</span>' : "") + (t.fr === "yes" ? '<span class="at-flag">Français</span>' : "");
  }

  /* ---------- detail drawer ---------- */
  var YN = { yes: "Yes", no: "No", unknown: "Not confirmed", "self-host": "Only if self-hosted" };
  function logo(t, cls) {
    var img = root.querySelector('.at-tile[data-id="' + t.id + '"] img');
    return img ? '<img src="' + esc(img.getAttribute("src")) + '" alt="" class="' + (cls || "") + '">' :
      '<span class="at-mono" style="background:' + getComputedStyle(root.querySelector('.at-tile[data-id="' + t.id + '"] .at-mono') || document.body).backgroundColor + '">' +
      esc((root.querySelector('.at-tile[data-id="' + t.id + '"] .at-mono') || {}).textContent || t.n.slice(0, 2)) + "</span>";
  }
  var lastFocus = null;
  function open(id) {
    var t = byId[id]; if (!t) return;
    lastFocus = document.activeElement;
    var lay = D.layers.filter(function (l) { return l.id === t.l; })[0];
    var deps = (t.dep || []).map(function (x) { return D.dep[x] || x; }).join(", ");
    var badge = t.b ? '<p><span class="at-d-badge' + (t.b === "Sunsetting" ? " sun" : "") + '">' + esc(t.b) + "</span> " + esc(t.sn || "") + "</p>" : "";
    var cost = t.cmp ? '<div class="at-d-cost"><strong>' + money(t.cpu) + "</strong> " + esc(t.unit) + '<p class="at-d-src">' + esc(t.cbn) + "</p></div>"
      : '<div class="at-d-cost"><strong>Not comparable</strong><p class="at-d-src">' + esc((t.cbn || "").replace(/^Not comparable:\s*/, "")) + "</p></div>";
    var on = picked.indexOf(id) >= 0;
    $("at-d-body").innerHTML = '<div class="at-d-top"><div class="at-d-id">' + logo(t) + '<div><h2 id="at-d-name">' + esc(t.n) + "</h2><p>" + esc(t.v) + "</p></div></div>" +
      '<button type="button" class="at-x" data-x aria-label="Close">×</button></div>' + badge +
      "<p>" + esc(t.d) + "</p>" +
      '<dl class="at-d-grid"><dt>Category</dt><dd>' + esc(t.c) + (t.c2 && t.c2.length ? '<span class="at-d-src"> · also ' + esc(t.c2.join(", ")) + "</span>" : "") + "</dd>" +
      "<dt>Layer</dt><dd>" + esc(lay ? lay.name : "") + "</dd>" +
      "<dt>Pricing</dt><dd>" + esc(D.pm[t.pm] || t.pm) + (t.free && t.pm !== "free" && t.pm !== "freemium" ? " · free plan" : "") + "</dd>" +
      "<dt>Published prices</dt><dd>" + esc(t.pt || "–") + (t.promo ? ' <span class="at-d-src">(promotion shown at check time)</span>' : "") + (t.cur !== "USD" ? ' <span class="at-d-src">(' + esc(t.cur) + ")</span>" : "") + "</dd>" +
      "<dt>Runs as</dt><dd>" + esc(deps || "–") + "</dd>" +
      (t.oss ? "<dt>Licence</dt><dd>" + esc(t.lic || "Open source") + "</dd>" : "") +
      "<dt>Data in Canada</dt><dd>" + esc(t.cap ? "Yes, on some plans" : YN[t.ca] || "Not confirmed") + (t.can ? '<span class="at-d-src"> · ' + esc(t.can.replace(/^SELF-HOST[^:]*:\s*/i, "")) + "</span>" : "") + "</dd>" +
      "<dt>French interface</dt><dd>" + esc(YN[t.fr] || "Not confirmed") + "</dd>" +
      (t.cav ? "<dt>Company</dt><dd>Canadian</dd>" : "") + "</dl>" +
      (t.low ? '<p class="at-d-src">Some details for this tool could not be fully confirmed from the vendor\'s own pages; check before relying on them.</p>' : "") +
      "<h3>Cost per output</h3>" + cost +
      '<div class="at-d-act"><a class="btn" href="' + esc(safeUrl(t.u)) + '" target="_blank" rel="noopener nofollow">Visit ' + esc(t.dom || "website") + "</a>" +
      '<label class="btn btn-ghost at-cmpbox"><input type="checkbox" data-pick="' + esc(id) + '"' + (on ? " checked" : "") + "> Add to compare</label></div>" +
      '<p class="at-d-src">Checked ' + esc(D.checked) + (t.ps ? ' · price source: <a href="' + esc(safeUrl(t.ps)) + '" target="_blank" rel="noopener nofollow">' + esc(t.ps) + "</a>" : "") +
      ((t.cs || []).length ? ' · Canada evidence: ' + t.cs.map(function (u, i) { return '<a href="' + esc(safeUrl(u)) + '" target="_blank" rel="noopener nofollow">[' + (i + 1) + "]</a>"; }).join(" ") : "") + "</p>";
    var dlg = $("at-drawer");
    if (dlg.showModal) { if (!dlg.open) dlg.showModal(); } else dlg.setAttribute("open", "");
    root.querySelectorAll(".at-tile.at-sel").forEach(function (b) { b.classList.remove("at-sel"); });
    var tile = root.querySelector('.at-tile[data-id="' + id + '"]'); if (tile) tile.classList.add("at-sel");
  }
  function closeDlg(d) { if (d.close) d.close(); else d.removeAttribute("open"); }
  ["at-drawer", "at-cmp"].forEach(function (k) {
    var d = $(k);
    d.addEventListener("click", function (e) {
      if (e.target.closest("[data-x]")) { closeDlg(d); return; }
      if (e.target !== d) return;
      var r = d.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) closeDlg(d);
    });
    d.addEventListener("close", function () { if (lastFocus && document.contains(lastFocus)) lastFocus.focus(); });
  });

  /* ---------- compare ---------- */
  function pick(id, on) {
    var i = picked.indexOf(id);
    if (on && i < 0) { if (picked.length >= 3) { alertTray(); return false; } picked.push(id); }
    if (!on && i >= 0) picked.splice(i, 1);
    tray(); return true;
  }
  function alertTray() { var l = $("at-tray-list"); l.textContent = "You can compare up to three tools. Remove one first."; setTimeout(tray, 2200); }
  function tray() {
    var tr = $("at-tray");
    tr.hidden = !picked.length; document.body.classList.toggle("at-tray-on", !!picked.length);
    $("at-tray-list").innerHTML = "<strong>Compare (" + picked.length + "/3):</strong> " + picked.map(function (id) { return esc(byId[id].n); }).join(", ");
    $("at-tray-go").disabled = picked.length < 2;
    document.querySelectorAll("[data-pick]").forEach(function (c) { c.checked = picked.indexOf(c.dataset.pick) >= 0; });
  }
  function compare() {
    var ts = picked.map(function (id) { return byId[id]; });
    var row = function (lab, f) { return "<tr><th scope=\"row\">" + lab + "</th>" + ts.map(function (t) { return "<td>" + f(t) + "</td>"; }).join("") + "</tr>"; };
    $("at-cmp-body").innerHTML = '<div class="at-cmpwrap"><table><thead><tr><th></th>' + ts.map(function (t) { return '<th scope="col">' + esc(t.n) + '<div class="at-d-src">' + esc(t.v) + "</div></th>"; }).join("") + "</tr></thead><tbody>" +
      row("Category", function (t) { return esc(t.c); }) + row("What it does", function (t) { return esc(t.d); }) +
      row("Pricing", function (t) { return esc(D.pm[t.pm] || t.pm) + (t.free && t.pm !== "free" && t.pm !== "freemium" ? " · free plan" : ""); }) +
      row("From (USD/mo)", function (t) { return t.ep != null && t.cur === "USD" ? (t.ep === 0 ? "Free" : money(t.ep)) + (t.promo ? " (promotion)" : "") : "–"; }) +
      row("Cost per output", function (t) { return t.cmp ? money(t.cpu) + " " + esc(t.unit) : "Not comparable"; }) +
      row("Published prices", function (t) { return esc(t.pt); }) +
      row("Runs as", function (t) { return esc((t.dep || []).map(function (x) { return D.dep[x] || x; }).join(", ")); }) +
      row("Open source", function (t) { return t.oss ? "Yes" + (t.lic ? " (" + esc(t.lic) + ")" : "") : "No"; }) +
      row("Data in Canada", function (t) { return esc(t.cap ? "Yes, on some plans" : YN[t.ca] || "Not confirmed") + (t.can ? '<div class="at-d-src">' + esc(t.can.replace(/^SELF-HOST[^:]*:\s*/i, "")) + "</div>" : ""); }) +
      row("French interface", function (t) { return esc(YN[t.fr] || "Not confirmed"); }) +
      row("Canadian company", function (t) { return t.cav ? "Yes" : "–"; }) +
      row("Status", function (t) { return esc(t.b || "Active") + (t.b && t.sn ? '<div class="at-d-src">' + esc(t.sn) + "</div>" : ""); }) +
      row("Website", function (t) { return '<a href="' + esc(safeUrl(t.u)) + '" target="_blank" rel="noopener nofollow">' + esc(t.dom) + "</a>"; }) +
      "</tbody></table></div><p class=\"at-d-src\">Checked " + esc(D.checked) + ". Cost per output is only comparable between tools in the same category and unit.</p>";
    var d = $("at-cmp"); if (d.showModal) d.showModal(); else d.setAttribute("open", "");
  }

  /* ---------- cost per output ---------- */
  function unitsOf(cat) {
    var units = {};
    T.forEach(function (t) { if (t.c === cat && t.cmp) units[t.unit] = (units[t.unit] || 0) + 1; });
    return Object.keys(units).sort(function (a, b) { return units[b] - units[a] || a.localeCompare(b); }).map(function (u) { return [u, units[u]]; });
  }
  function costView() {
    var cat = $("at-cost-cat").value, freeOnly = $("at-cost-free").checked, us = unitsOf(cat), usel = $("at-cost-usel");
    var pool = T.filter(function (t) { return t.c === cat; });
    var bars = $("at-cost-bars"), vol = parseFloat($("at-cost-vol").value);
    usel.parentNode.hidden = us.length < 2;
    var unit = us.length > 1 && us.some(function (u) { return u[0] === usel.value; }) ? usel.value : (us[0] || [])[0];
    if (!unit) {
      $("at-cost-unit").textContent = "Volume per month"; $("at-cost-cap").textContent = "";
      bars.innerHTML = '<p class="at-nc">None of the ' + pool.length + " tools in " + esc(cat) + " publish a price that can be turned into a fair cost per output (they are open source, contact-sales or credit-based). Open the tools on the map for their published prices.</p>";
      $("at-cost-note").textContent = ""; return;
    }
    var w = UNIT_WORD[unit] || ["Units per month", "units"];
    $("at-cost-unit").textContent = w[0];
    if (!(vol >= 0)) vol = 0;
    if (vol > MAXVOL) vol = MAXVOL;
    var seat = unit === "per seat per month";
    var onUnit = pool.filter(function (t) { return t.cmp && t.unit === unit; });
    var rows = onUnit.filter(function (t) { return !freeOnly || t.free; }).map(function (t) { return { t: t, m: vol * t.cpu }; })
      .sort(function (a, b) { return a.m - b.m || a.t.n.localeCompare(b.t.n); });
    var noFree = onUnit.length - rows.length, notCmp = pool.length - onUnit.length;
    var mx = rows.reduce(function (m, r) { return Math.max(m, r.m); }, 0) || 1;
    $("at-cost-cap").textContent = rows.length + (rows.length === 1 ? " tool" : " tools") + " in " + cat + " priced " + unit + ". Monthly estimate for " + vol.toLocaleString("en-CA") + " " + w[1] + ".";
    var pl = function (n, a, b) { return n + " " + (n === 1 ? a : b); };
    bars.innerHTML = rows.map(function (r) {
      return '<div class="at-bar"><button type="button" data-open="' + esc(r.t.id) + '" title="' + esc(r.t.n) + '">' + esc(r.t.n) + '</button>' +
        '<div class="at-track"><div class="at-fill" style="width:' + (r.m / mx * 100).toFixed(1) + '%"></div></div>' +
        '<div class="at-amt">' + money(r.m) + "/mo<small>" + money(r.t.cpu) + " " + esc(unit) + (r.t.promo ? " · promotion" : "") + "</small></div></div>";
    }).join("") +
      (noFree ? '<p class="at-nc">' + pl(noFree, "tool", "tools") + " without a free plan hidden by your filter.</p>" : "") +
      (notCmp ? '<p class="at-nc">' + pl(notCmp, "other tool", "other tools") + " in this category " + (notCmp === 1 ? "is" : "are") + " not shown: " + (notCmp === 1 ? "its" : "their") + " price is on another unit or is not comparable.</p>" : "");
    $("at-cost-note").textContent = seat ? "Seat price times the number of seats, at each tool's cheapest paid plan (some are billed annually)."
      : "Volume times each tool's entry-plan cost per unit. Plan fees, monthly minimums, overage rates, higher tiers and volume discounts are not included, so check the shortlisted vendors' pricing pages.";
  }

  /* ---------- PNG export of the (filtered) map ---------- */
  function png() {
    var W = 2400, pad = 40, colW = 450, gap = 16, cols = Math.floor((W - pad * 2 + gap) / (colW + gap)), lh = 22;
    var C = document.createElement("canvas"), x = C.getContext("2d");
    var colours = { L1: "#0B2A5A", L2: "#0B6FA4", L3: "#B04A12", L4: "#2F6B3A", L5: "#6A3D8F" };
    var layers = D.layers.map(function (L) {
      var cats = D.categories.filter(function (c) { return c.l === L.id; }).map(function (c) {
        return { c: c.c, names: hits.filter(function (t) { return t.c === c.c; }).map(function (t) { return t.n; }) };
      }).filter(function (c) { return c.names.length; });
      return { L: L, cats: cats };
    }).filter(function (l) { return l.cats.length; });
    function catH(c) { return 34 + Math.ceil(c.names.length / 2) * lh + 10; }
    var H = 150;
    layers.forEach(function (l) {
      H += 56; var rows = [];
      for (var i = 0; i < l.cats.length; i += cols) rows.push(Math.max.apply(null, l.cats.slice(i, i + cols).map(catH)));
      H += rows.reduce(function (a, b) { return a + b + gap; }, 0) + 14;
    });
    if (!layers.length) H += 60;
    H += 60; C.width = W; C.height = H;
    x.fillStyle = "#F6F5F1"; x.fillRect(0, 0, W, H);
    x.fillStyle = "#0B2A5A"; x.font = "700 44px 'Space Grotesk', sans-serif"; x.fillText("AI Tools Landscape", pad, 70);
    x.font = "400 22px Inter, sans-serif"; x.fillStyle = "#3F4A5C";
    x.fillText(hits.length + " tools · checked " + D.checked + " · chmltech.com/ai-tools", pad, 108);
    var y = 140;
    if (!layers.length) { x.fillStyle = "#3F4A5C"; x.font = "400 24px Inter, sans-serif"; x.fillText("No tools match the current filters.", pad, y + 40); }
    layers.forEach(function (l) {
      x.fillStyle = colours[l.L.id]; x.fillRect(pad, y, W - pad * 2, 44);
      x.fillStyle = "#fff"; x.font = "600 24px 'Space Grotesk', sans-serif"; x.fillText(l.L.id + "  " + l.L.name, pad + 16, y + 30);
      y += 56;
      for (var i = 0; i < l.cats.length; i += cols) {
        var row = l.cats.slice(i, i + cols), rh = Math.max.apply(null, row.map(catH));
        row.forEach(function (c, j) {
          var cx = pad + j * (colW + gap);
          x.fillStyle = "#fff"; x.strokeStyle = "#E4E1D8"; x.lineWidth = 2; x.fillRect(cx, y, colW, rh); x.strokeRect(cx, y, colW, rh);
          x.fillStyle = colours[l.L.id]; x.font = "600 17px Inter, sans-serif"; x.fillText(c.c + " (" + c.names.length + ")", cx + 12, y + 24);
          x.fillStyle = "#24324A"; x.font = "400 14.5px Inter, sans-serif";
          c.names.forEach(function (n, k) {
            var col = k % 2, rr = Math.floor(k / 2), s = n, maxW = colW / 2 - 20;
            if (x.measureText(s).width > maxW) { while (s.length > 2 && x.measureText(s + "…").width > maxW) s = s.slice(0, -1); s += "…"; }
            x.fillText(s, cx + 12 + col * (colW / 2 - 6), y + 50 + rr * lh);
          });
        });
        y += rh + gap;
      }
      y += 14;
    });
    x.fillStyle = "#5A6475"; x.font = "400 16px Inter, sans-serif";
    x.fillText("Product names belong to their owners. Listing is not an endorsement. Source: Chmltech AI Tools Landscape, checked " + D.checked + ".", pad, H - 24);
    C.toBlob(function (b) {
      var a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = "chmltech-ai-tools-landscape.png";
      document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
  }

  /* ---------- views ---------- */
  function view(v) {
    state.view = v;
    root.querySelectorAll(".at-tabs .ll-tab").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.view === v ? "true" : "false"); });
    $("at-panel-map").hidden = v !== "map"; $("at-panel-list").hidden = v !== "list"; $("at-maplegend").hidden = v !== "map";
    if (folded !== null) { var f = current(); $("at-mapmore-wrap").hidden = v !== "map" || !!(f.q || f.l.length || f.c.length || f.pm.length || f.x.length || f.ca.length || f.dep.length || f.b.length); }
    if (v === "list") list();
  }

  /* ---------- events ---------- */
  function wire() {
    var tq;
    $("at-q").addEventListener("input", function (e) { clearTimeout(tq); tq = setTimeout(function () { state.q = e.target.value; apply(); }, 160); });
    form.addEventListener("change", apply);
    document.addEventListener("click", function (e) {
      var el = e.target;
      var tile = el.closest(".at-tile"); if (tile) { open(tile.dataset.id); return; }
      var o = el.closest("[data-open]"); if (o) { e.preventDefault(); open(o.dataset.open); return; }
      if (el.closest("[data-clear]")) { form.reset(); state.q = ""; $("at-q").value = ""; apply(); return; }
      var ch = el.closest("[data-chip]");
      if (ch) {
        var p = ch.dataset.chip.split("|");
        if (p[0] === "q") { state.q = ""; $("at-q").value = ""; }
        else { var i = form.querySelector('input[name="' + p[0] + '"][value="' + CSS.escape(p[1]) + '"]'); if (i) i.checked = false; }
        apply();
        var nx = root.querySelector(".gr-chip"); (nx || $("at-q")).focus();
        return;
      }
      if (el.closest("[data-more]")) {
        var before = listShown; listShown += LIST_STEP; list(true);
        var nb = $("at-tbody").querySelectorAll("tr")[before]; if (nb && nb.querySelector("button")) nb.querySelector("button").focus();
        return;
      }
      if (el.closest(".gr-filter-btn")) { var op = root.classList.toggle("gr-panel-open"); root.querySelector(".gr-filter-btn").setAttribute("aria-expanded", op); return; }
      if (el.closest("[data-close]")) { root.classList.remove("gr-panel-open"); root.querySelector(".gr-filter-btn").setAttribute("aria-expanded", "false"); $("at-count").scrollIntoView({ block: "start" }); return; }
      var tab = el.closest(".at-tabs .ll-tab"); if (tab) { view(tab.dataset.view); return; }
      var th = el.closest(".at-table .ll-th");
      if (th) { var k = th.dataset.sort; state.dir = state.sort === k ? -state.dir : (k === "n" || k === "c" ? 1 : 1); state.sort = k; list(); return; }
    });
    document.addEventListener("change", function (e) {
      var c = e.target.closest("[data-pick]");
      if (c && !pick(c.dataset.pick, c.checked)) c.checked = false;
    });
    $("at-tray-go").addEventListener("click", compare);
    $("at-tray-clear").addEventListener("click", function () { picked = []; tray(); });
    $("at-png").addEventListener("click", png);
    $("at-mapmore").addEventListener("click", function () {
      var was = folded; setFold(!folded);
      if (!was) { var top = $("at-panel-map").getBoundingClientRect().top; if (top < 0) $("map").scrollIntoView({ behavior: calm ? "instant" : "smooth" }); }
    });
    // keyboard users tabbing past the fold open the full map
    $("at-panel-map").addEventListener("focusin", function (e) {
      if (!folded) return;
      var m = $("at-panel-map"), r = e.target.getBoundingClientRect(), mr = m.getBoundingClientRect();
      if (r.bottom > mr.bottom - 180) setFold(false);
    });
    ["at-cost-cat", "at-cost-free", "at-cost-usel"].forEach(function (k) { $(k).addEventListener("change", function () { if (k !== "at-cost-free") setVol(k === "at-cost-usel"); costView(); }); });
    $("at-cost-vol").addEventListener("input", costView);
  }
  function setVol(keepUnit) {
    var us = unitsOf($("at-cost-cat").value), sel = $("at-cost-usel");
    if (!keepUnit) sel.innerHTML = us.map(function (u) { return '<option value="' + esc(u[0]) + '">' + esc(u[0]) + " (" + u[1] + ")</option>"; }).join("");
    var u = keepUnit ? sel.value : (us[0] || [])[0];
    $("at-cost-vol").value = DEFAULT_VOL[u] != null ? DEFAULT_VOL[u] : 10;
  }

  /* ---------- load ---------- */
  var inline = document.getElementById("at-data");
  (inline ? Promise.resolve(JSON.parse(inline.textContent)) :
    fetch(root.dataset.src || "assets/data/ai-tools.json").then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })).then(function (data) {
    D = data; T = data.tools; T.forEach(function (t) { byId[t.id] = t; });
    document.documentElement.classList.add("at-ready");
    root.classList.add("gr-js");
    readUrl(); wire();
    var sel = $("at-cost-cat"); if (Array.prototype.some.call(sel.options, function (o) { return o.value === "Image Generation"; })) sel.value = "Image Generation";
    setVol(); costView(); apply();
    window.ATools = {
      data: D,
      open: open,
      showCategory: function (cat) {
        form.reset(); state.q = ""; $("at-q").value = "";
        var i = form.querySelector('input[name="c"][value="' + CSS.escape(cat) + '"]');
        if (i) { i.checked = true; i.closest("details").open = true; }
        view("map"); apply(); $("map").scrollIntoView({ behavior: calm ? "instant" : "smooth" });
      }
    };
    document.dispatchEvent(new CustomEvent("at:data", { detail: D }));
  }).catch(function () {
    $("at-count").textContent = "The interactive features could not load. The full list of tools is shown in the map below; reload the page to try again.";
    document.querySelectorAll(".at-chwait").forEach(function (p) { p.textContent = "The chart could not load. Reload the page to try again."; });
    $("at-cost-bars").innerHTML = '<p class="at-nc">The cost comparison could not load. Reload the page to try again.</p>';
  });
})();
