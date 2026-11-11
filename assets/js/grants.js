/* Chmltech funding finder (funding.html). Vanilla JS, no network.
   Reads the embedded dataset (#grants-data), filters the server-rendered cards, keeps state in the URL hash. */
(function () {
  "use strict";
  var root = document.getElementById("gr-finder");
  var dataEl = document.getElementById("grants-data");
  if (!root || !dataEl) return;
  var DATA;
  try { DATA = JSON.parse(dataEl.textContent); } catch (e) { return; }

  var CLOSED = "Closed to new applications";
  var GROUPS = ["j", "t", "a", "i", "p", "s"];
  var FIELD = { j: "jurisdiction", t: "funding_types", a: "applicant_types", i: "industries", p: "purposes", s: "status" };
  var LABEL = { j: "Jurisdiction", t: "Funding type", a: "Who can apply", i: "Industry", p: "Purpose", s: "Status" };

  var q = document.getElementById("gr-q");
  var sortSel = document.getElementById("gr-sort");
  var fed = document.getElementById("gr-fed");
  var closed = document.getElementById("gr-closed");
  var countEl = document.getElementById("gr-count");
  var list = root.querySelector(".gr-list");
  var chipsEl = root.querySelector(".gr-chips");
  var empty = root.querySelector(".gr-empty");
  var panel = document.getElementById("gr-filters");
  var toggleBtn = root.querySelector(".gr-filter-btn");
  var badge = root.querySelector("[data-active-n]");
  var closeN = root.querySelector("[data-close-n]");
  var form = root.querySelector(".gr-form");

  // Index records and their cards; precompute lower-case search text.
  var cards = {};
  DATA.forEach(function (r) {
    r._card = document.getElementById("p-" + r.id);
    r._text = [r.name, r.administrator, r.summary, r.eligibility, (r.industries || []).join(" ")].join(" ").toLowerCase();
    cards[r.id] = r._card;
  });
  var recs = DATA.filter(function (r) { return r._card; });

  function boxes(g) { return root.querySelectorAll('input[type="checkbox"][name="' + g + '"]'); }
  function selected(g) {
    var out = [];
    Array.prototype.forEach.call(boxes(g), function (b) { if (b.checked) out.push(b.value); });
    return out;
  }
  function state() {
    var s = { q: q.value.trim(), sort: sortSel.value, fed: fed ? fed.checked : true, closed: closed ? closed.checked : false };
    GROUPS.forEach(function (g) { s[g] = selected(g); });
    return s;
  }
  function arr(v) { return Array.isArray(v) ? v : (v ? [v] : []); }
  function any(a, b) { for (var i = 0; i < a.length; i++) if (b.indexOf(a[i]) > -1) return true; return false; }

  // Does record r pass group g under state s?
  function passGroup(r, g, s) {
    var sel = s[g];
    if (g === "s") {
      if (r.status === CLOSED) return s.closed;
      return !sel.length || sel.indexOf(r.status) > -1;
    }
    if (!sel.length) return true;
    if (g === "j") {
      if (sel.indexOf(r.jurisdiction) > -1) return true;
      if (r.jurisdiction === "Federal" && s.fed) {
        var provs = arr(r.provinces);
        var picked = sel.filter(function (x) { return x !== "Federal"; });
        return picked.length > 0 && (provs.indexOf("All") > -1 || any(picked, provs));
      }
      return false;
    }
    var vals = arr(r[FIELD[g]]);
    if (g === "i" && vals.indexOf("All industries") > -1) return true;
    return any(sel, vals);
  }
  function passSearch(r, s) {
    if (!s.q) return true;
    var words = s.q.toLowerCase().split(/\s+/);
    for (var i = 0; i < words.length; i++) if (r._text.indexOf(words[i]) < 0) return false;
    return true;
  }
  function pass(r, s, skip) {
    if (!passSearch(r, s)) return false;
    for (var i = 0; i < GROUPS.length; i++) if (GROUPS[i] !== skip && !passGroup(r, GROUPS[i], s)) return false;
    return true;
  }

  var SORTS = {
    az: function (a, b) { return a.name.localeCompare(b.name, "en-CA"); },
    amount: function (a, b) {
      var x = a.max_amount_cad, y = b.max_amount_cad;
      if (x == null && y == null) return SORTS.az(a, b);
      if (x == null) return 1; if (y == null) return -1;
      return y - x || SORTS.az(a, b);
    },
    recent: function (a, b) { return (b.source_checked || "").localeCompare(a.source_checked || "") || SORTS.az(a, b); }
  };

  function chip(label, onRemove) {
    var li = document.createElement("li");
    var b = document.createElement("button");
    b.type = "button"; b.className = "gr-chip";
    b.setAttribute("aria-label", "Remove filter: " + label);
    b.innerHTML = '<span></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    b.firstChild.textContent = label;
    b.addEventListener("click", function () {
      var idx = Array.prototype.indexOf.call(chipsEl.children, li);
      onRemove(); update();
      // keep keyboard focus in the chip list, or return it to the search box when none are left
      var items = chipsEl.querySelectorAll("button");
      if (items.length) items[Math.min(idx, items.length - 1)].focus(); else q.focus();
    });
    li.appendChild(b);
    return li;
  }

  function activeCount(s) {
    var n = s.q ? 1 : 0;
    GROUPS.forEach(function (g) { n += s[g].length; });
    if (s.closed) n++;
    if (!s.fed) n++;
    return n;
  }

  function update(opts) {
    var s = state();
    // filter + sort
    var shown = recs.filter(function (r) { return pass(r, s); }).sort(SORTS[s.sort] || SORTS.az);
    var on = {};
    shown.forEach(function (r) { on[r.id] = 1; list.appendChild(r._card); });
    recs.forEach(function (r) { if (!on[r.id]) { r._card.hidden = true; list.appendChild(r._card); } else r._card.hidden = false; });
    var n = shown.length;
    var txt = n + (n === 1 ? " program" : " programs");
    countEl.textContent = txt;
    if (closeN) closeN.textContent = n;
    empty.hidden = n > 0;

    // facet counts: how many results each option would give with the other filters unchanged
    GROUPS.forEach(function (g) {
      var base = recs.filter(function (r) { return pass(r, s, g); });
      Array.prototype.forEach.call(boxes(g), function (b) {
        var probe = {}; for (var k in s) probe[k] = s[k];
        probe[g] = [b.value];
        var c = 0;
        base.forEach(function (r) { if (passGroup(r, g, probe)) c++; });
        var el = b.parentNode.querySelector("[data-n]");
        if (el) el.textContent = c;
        b.parentNode.classList.toggle("gr-zero", c === 0 && !b.checked);
      });
      var sel = root.querySelector('[data-group="' + g + '"] [data-sel]');
      if (sel) { sel.hidden = !s[g].length; sel.textContent = s[g].length ? s[g].length + " selected" : ""; }
    });

    // active-filter chips
    chipsEl.innerHTML = "";
    if (s.q) chipsEl.appendChild(chip('Search: "' + s.q + '"', function () { q.value = ""; }));
    GROUPS.forEach(function (g) {
      s[g].forEach(function (v) {
        chipsEl.appendChild(chip(v, function () {
          Array.prototype.forEach.call(boxes(g), function (b) { if (b.value === v) b.checked = false; });
        }));
      });
    });
    if (s.closed) chipsEl.appendChild(chip("Showing closed programs", function () { closed.checked = false; }));
    if (!s.fed) chipsEl.appendChild(chip("Federal programs excluded", function () { fed.checked = true; }));
    var act = activeCount(s);
    chipsEl.hidden = act === 0;
    Array.prototype.forEach.call(root.querySelectorAll(".gr-statusbar [data-clear]"), function (b) { b.hidden = act === 0; });
    if (badge) { badge.hidden = act === 0; badge.textContent = act; }
    if (toggleBtn) toggleBtn.setAttribute("aria-label", act ? "Filters, " + act + " active" : "Filters");

    if (!(opts && opts.noHash)) writeHash(s);
  }

  // ---------- URL hash (shareable state) ----------
  function writeHash(s) {
    var p = new URLSearchParams();
    if (s.q) p.append("q", s.q);
    GROUPS.forEach(function (g) { s[g].forEach(function (v) { p.append(g, v); }); });
    if (!s.fed) p.append("fed", "0");
    if (s.closed) p.append("closed", "1");
    if (s.sort && s.sort !== "az") p.append("sort", s.sort);
    var h = p.toString();
    if (!h && location.hash.indexOf("=") < 0) return;   // keep plain anchors such as #finder
    var url = location.pathname + location.search + (h ? "#" + h : "");
    if (url !== location.pathname + location.search + location.hash) {
      try { history.replaceState(null, "", url); } catch (e) { /* file:// or sandboxed */ }
    }
  }
  function readHash() {
    var h = location.hash.replace(/^#/, "");
    if (!h || h.indexOf("=") < 0) return false;   // plain anchors like #finder
    var p;
    try { p = new URLSearchParams(h); } catch (e) { return false; }
    q.value = p.get("q") || "";
    GROUPS.forEach(function (g) {
      var vals = p.getAll(g);
      Array.prototype.forEach.call(boxes(g), function (b) { b.checked = vals.indexOf(b.value) > -1; });
    });
    if (fed) fed.checked = p.get("fed") !== "0";
    if (closed) closed.checked = p.get("closed") === "1";
    var so = p.get("sort");
    sortSel.value = SORTS[so] ? so : "az";
    // open groups that have selections so restored state is visible
    GROUPS.forEach(function (g) {
      if (p.getAll(g).length) { var d = root.querySelector('[data-group="' + g + '"]'); if (d) d.open = true; }
    });
    if (p.get("closed") === "1") { var ds = root.querySelector('[data-group="s"]'); if (ds) ds.open = true; }
    return true;
  }

  function clearAll() {
    q.value = "";
    GROUPS.forEach(function (g) { Array.prototype.forEach.call(boxes(g), function (b) { b.checked = false; }); });
    if (fed) fed.checked = true;
    if (closed) closed.checked = false;
    update();
  }

  // ---------- mobile filter panel ----------
  var mq = window.matchMedia("(max-width: 900px)");
  function setPanel(open, focusBack) {
    root.classList.toggle("gr-panel-open", open);
    toggleBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) { var f = panel.querySelector("summary, input, button"); if (f) f.focus(); }
    else if (focusBack) toggleBtn.focus();
  }

  // ---------- wire up ----------
  root.classList.add("gr-js");
  var t;
  q.addEventListener("input", function () { clearTimeout(t); t = setTimeout(update, 150); });
  sortSel.addEventListener("change", function () { update(); });
  form.addEventListener("change", function () { update(); });
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  Array.prototype.forEach.call(root.querySelectorAll("[data-clear]"), function (b) { b.addEventListener("click", clearAll); });
  toggleBtn.addEventListener("click", function () { setPanel(!root.classList.contains("gr-panel-open")); });
  var closeBtn = root.querySelector("[data-close]");
  if (closeBtn) closeBtn.addEventListener("click", function () {
    setPanel(false, true);
    var r = root.querySelector(".gr-results");
    if (r && r.scrollIntoView) r.scrollIntoView({ block: "start" });
  });
  panel.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && mq.matches && root.classList.contains("gr-panel-open")) setPanel(false, true);
  });
  window.addEventListener("hashchange", function () { if (readHash()) update({ noHash: true }); });

  readHash();
  update();
})();
