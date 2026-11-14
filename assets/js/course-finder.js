/* Courses page: "Find your course" quiz and level/topic filters.
   Data comes from <script id="finder-data">, written by content/gen/course_finder.py
   from content/courses/finder.json. Everything runs in the browser; the last
   answers are kept in localStorage (chm_finder) so a returning visitor sees
   their suggested path again. */
(function () {
  "use strict";
  var el = document.getElementById("finder-data");
  if (!el) return;
  var D;
  try { D = JSON.parse(el.textContent); } catch (e) { return; }
  var C = D.courses, Q = D.questions;
  var KEY = "chm_finder";

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function track(name, val) {
    try { if (typeof window.clarity === "function") { if (val) window.clarity("set", name, val); else window.clarity("event", name); } } catch (e) {}
  }
  function save(a) { try { localStorage.setItem(KEY, JSON.stringify({ a: a, t: Date.now() })); } catch (e) {} }
  function load() { try { var v = JSON.parse(localStorage.getItem(KEY) || "null"); return v && v.a ? v.a : null; } catch (e) { return null; } }
  function forget() { try { localStorage.removeItem(KEY); } catch (e) {} }

  /* ---------------- Filters ---------------- */
  var grid = document.getElementById("course-grid");
  var filters = $(".course-filters");
  var cards = grid ? $$("article.program[data-key]", grid) : [];
  var F = { level: "all", topic: "all" };
  function applyFilters() {
    var n = 0;
    cards.forEach(function (c) {
      var ok = (F.level === "all" || c.getAttribute("data-level") === F.level) &&
               (F.topic === "all" || c.getAttribute("data-topic") === F.topic);
      c.hidden = !ok; if (ok) n++;
    });
    var cnt = $(".filter-count", filters);
    if (cnt) cnt.textContent = n === cards.length ? "Showing all " + n + " courses" :
      n ? "Showing " + n + " of " + cards.length + " courses" : "No courses match. Try another level or topic.";
  }
  if (filters && cards.length) {
    filters.hidden = false;
    ["level", "topic"].forEach(function (g) {
      $$("[data-" + g + "]", filters).forEach(function (b) {
        b.addEventListener("click", function () {
          F[g] = b.getAttribute("data-" + g);
          $$("[data-" + g + "]", filters).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          applyFilters();
        });
      });
    });
    applyFilters();
  }

  /* ---------------- Quiz ---------------- */
  var sec = document.getElementById("finder");
  if (!sec) return;
  sec.hidden = false;
  var box = $(".finder", sec), intro = $(".finder-intro", sec), quiz = $(".finder-quiz", sec), res = $(".finder-result", sec);
  var optsBox = $(".finder-opts", sec), qtext = $(".finder-qtext", sec), legend = $(".finder-q legend", sec);
  var stepTxt = $(".finder-step", sec), bar = $(".finder-bar span", sec);
  var btnNext = $('[data-finder="next"]', sec), btnBack = $('[data-finder="back"]', sec);
  var A = {}, idx = 0;

  function show(part) {
    box.setAttribute("data-state", part);
    intro.hidden = part !== "intro"; quiz.hidden = part !== "quiz"; res.hidden = part !== "result";
  }
  function renderQ(focus) {
    var q = Q[idx];
    stepTxt.textContent = "Question " + (idx + 1) + " of " + Q.length;
    bar.style.width = ((idx + 1) / Q.length * 100) + "%";
    qtext.textContent = q.q; legend.textContent = q.q;
    optsBox.innerHTML = q.opts.map(function (o) {
      return '<label class="finder-opt"><input type="radio" name="fq-' + q.id + '" value="' + esc(o[0]) + '"' +
        (A[q.id] === o[0] ? " checked" : "") + '><span>' + esc(o[1]) + "</span></label>";
    }).join("");
    $$("input", optsBox).forEach(function (i) {
      i.addEventListener("change", function () { A[q.id] = i.value; btnNext.disabled = false; });
    });
    btnNext.disabled = !A[q.id];
    btnNext.textContent = idx === Q.length - 1 ? "See my courses →" : "Next →";
    btnBack.style.visibility = idx === 0 ? "hidden" : "visible";
    if (focus) { var f = $("input:checked", optsBox) || $("input", optsBox); if (f) f.focus(); }
  }
  $('[data-finder="start"]', sec).addEventListener("click", function () {
    A = {}; idx = 0; show("quiz"); renderQ(true); track("finder_start");
  });
  btnBack.addEventListener("click", function () { if (idx > 0) { idx--; renderQ(true); } });
  btnNext.addEventListener("click", function () {
    if (!A[Q[idx].id]) return;
    if (idx < Q.length - 1) { idx++; renderQ(true); return; }
    save(A); renderResult(A, false); track("finder_complete");
  });

  /* ---------------- Recommendation ---------------- */
  function label(qid, val) {
    var q = Q.filter(function (x) { return x.id === qid; })[0];
    var o = q && q.opts.filter(function (x) { return x[0] === val; })[0];
    return o ? o[1] : "";
  }
  function recommend(a) {
    var pid = D.goal_path[a.goal] || "ai-starter", P = D.paths[pid];
    var list = P.courses.slice(), note = "";
    if (P.ai && a.exp === "none" && list.indexOf(D.beginner_intro) < 0) {
      list.unshift(D.beginner_intro);
      note = "Since you're new to AI tools, the path starts with the basics.";
    }
    if (P.ai && a.exp === "builder") {
      var before = list.length;
      var adv = list.filter(function (k) { return C[k].level > 1; });
      list = adv.length >= 3 ? adv : list.filter(function (k) { return k !== D.beginner_intro; });
      if (list.length < before) note = "You've already built AI tools, so the path skips the beginner courses.";
    }
    if (pid === "operations" && a.role === "leader") {
      list = ["operational-excellence"].concat(list.filter(function (k) { return k !== "operational-excellence"; }));
      note = "As a leader, you start with the big picture of operational excellence, then the workplace tools.";
    }
    var extra = D.industry_extra[a.industry];
    if (extra && list.indexOf(extra) >= 0) extra = null;
    return { pid: pid, P: P, list: list, note: note, extra: extra };
  }
  function tags(c) {
    return '<span class="tag tag-level lv' + c.level + '">' + esc(D.levels[c.level]) + '</span><span class="tag">' + c.lessons + " lessons</span>";
  }
  function renderResult(a, returning) {
    var r = recommend(a), first = C[r.list[0]];
    var rest = a.time === "one" ? r.list.slice(1, 3) : r.list.slice(1);
    var why = "Your goal: \u201c" + label("goal", a.goal) + "\u201d.";
    var h = '<div class="finder-res-head stack">' +
      '<p class="eyebrow">' + (returning ? "Your suggested path (from your last visit)" : "Your suggested learning path") + "</p>" +
      '<h2 class="h-lg">' + esc(r.P.name) + "</h2>" +
      '<p class="lead">' + esc(r.P.blurb) + "</p>" +
      '<p class="finder-why muted">' + esc(why) + (r.note ? " " + esc(r.note) : "") + "</p></div>";
    h += '<div class="finder-start"><p class="finder-kicker">Start here</p>' +
      '<h3 class="h-md">' + esc(first.title) + "</h3><p>" + esc(first.tagline) + '</p><div class="facts">' + tags(first) + "</div>" +
      '<a class="btn" data-go="' + esc(r.list[0]) + '" href="' + esc(first.url) + '">Start this course →</a></div>';
    if (rest.length) {
      h += '<div class="finder-next"><p class="finder-kicker">' + (a.time === "one" ? "When you're ready, take next" : "Then continue with") + "</p><ol>" +
        rest.map(function (k) {
          var c = C[k];
          return '<li><a data-go="' + esc(k) + '" href="' + esc(c.url) + '">' + esc(c.title) + '</a><span class="facts">' + tags(c) + "</span></li>";
        }).join("") + "</ol></div>";
    }
    if (r.extra) {
      var x = C[r.extra];
      h += '<p class="finder-extra">Also useful in ' + esc((D.industry_names || {})[a.industry] || "your industry") +
        ': <a data-go="' + esc(r.extra) + '" href="' + esc(x.url) + '">' + esc(x.title) + "</a></p>";
    }
    h += '<div class="finder-cta"><p><strong>Want help applying this in your business?</strong> Talk it through with Chmltech in a free strategy call.</p>' +
      '<a class="btn btn-navy" href="book.html">Book a free strategy call</a></div>';
    h += '<div class="btn-row finder-actions"><button type="button" class="btn btn-ghost" data-finder="retake">Retake the quiz</button>' +
      '<a class="btn btn-ghost" href="#programs">Browse all courses</a></div>';
    res.innerHTML = h;
    show("result");
    markCards(r.list);
    $('[data-finder="retake"]', res).addEventListener("click", function () {
      forget(); markCards([]); A = {}; idx = 0; show("quiz"); renderQ(true); track("finder_retake");
    });
    $$("[data-go]", res).forEach(function (l) {
      l.addEventListener("click", function () { track("finder_course", l.getAttribute("data-go")); track("finder_start_course"); });
    });
    track("finder_path", r.pid);
    if (!returning) res.focus();
  }
  function markCards(keys) {
    cards.forEach(function (c) {
      var on = keys.indexOf(c.getAttribute("data-key")) >= 0;
      c.classList.toggle("in-path", on);
      var b = $(".path-badge", c);
      if (on && !b) { b = document.createElement("span"); b.className = "path-badge"; b.textContent = "In your path"; c.insertBefore(b, c.firstChild); }
      if (!on && b) b.remove();
    });
  }

  var saved = load();
  if (saved && saved.goal && D.goal_path[saved.goal]) renderResult(saved, true); else show("intro");
})();
