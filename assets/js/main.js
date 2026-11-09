/* Chmltech Ltd. website — shared behaviour (V2) */
(function () {
  'use strict';

  /* Mobile navigation */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* Footer year */
  var y = document.querySelectorAll('[data-year]');
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();

  /* Pre-select a service from ?service= on forms */
  var params = new URLSearchParams(location.search);
  var svc = params.get('service');
  if (svc) {
    var sel = document.querySelector('select[name="service"]');
    if (sel) for (var j = 0; j < sel.options.length; j++) if (sel.options[j].value === svc) sel.selectedIndex = j;
  }

  /* Forms: post to Formspree (or any JSON endpoint) set in data-endpoint.
     Until a real endpoint is configured, fall back to opening an email draft. */
  var CONTACT_EMAIL = 'info@chmltech.com';
  var forms = document.querySelectorAll('form[data-endpoint]');
  Array.prototype.forEach.call(forms, function (form) {
    var status = form.querySelector('.form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      if (data.get('_gotcha')) return; // spam honeypot
      var endpoint = form.getAttribute('data-endpoint');
      var btn = form.querySelector('[type="submit"]');

      if (!endpoint || endpoint.indexOf('YOUR_FORM_ID') !== -1) {
        var lines = [];
        data.forEach(function (v, k) { if (k.charAt(0) !== '_' && v) lines.push(k.replace(/_/g, ' ') + ': ' + v); });
        var subject = (form.getAttribute('data-subject') || 'Website enquiry') + ' — ' + (data.get('name') || '');
        location.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
        show('ok', 'Your email app should open with your message ready to send. If it does not, email us at ' + CONTACT_EMAIL + '.');
        return;
      }

      btn.disabled = true; var label = btn.textContent; btn.textContent = 'Sending…';
      fetch(endpoint, { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('Request failed');
          form.reset();
          show('ok', form.getAttribute('data-success') || 'Thank you. We will be in touch within one business day.');
        })
        .catch(function () {
          show('err', 'Sorry, something went wrong. Please email us at ' + CONTACT_EMAIL + '.');
        })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
    function show(kind, msg) {
      if (!status) return;
      status.className = 'form-status ' + kind;
      status.textContent = msg;
      status.focus();
    }
  });

  /* Pre-fill message when arriving from a course page (?course=) */
  var course = params.get('course');
  if (course) {
    var msg = document.querySelector('textarea[name="message"]');
    if (msg && !msg.value) msg.value = 'I would like to join the free course: ' + course;
  }

  /* Searchable, filterable lists (insights articles, practice exams) */
  Array.prototype.forEach.call(document.querySelectorAll('[data-list]'), function (list) {
    var items = Array.prototype.slice.call(list.querySelectorAll('[data-items] > *'));
    var chips = list.querySelectorAll('.chip[data-cat]');
    var input = list.querySelector('[data-search-input]');
    var countEl = list.querySelector('[data-count]');
    var empty = list.querySelector('[data-empty]');
    var more = list.querySelector('[data-more]');
    var size = parseInt(list.getAttribute('data-page-size'), 10) || 24;
    var noun = list.getAttribute('data-list') === 'exams' ? 'exams' : 'articles';
    var state = { cat: 'all', q: '', shown: size };

    function apply() {
      var words = state.q.toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; });
      var matches = items.filter(function (it) {
        var cats = (it.getAttribute('data-cats') || '').split(' ');
        if (state.cat !== 'all' && cats.indexOf(state.cat) === -1) return false;
        var hay = it.getAttribute('data-search') || '';
        return words.every(function (w) { return hay.indexOf(w) !== -1; });
      });
      items.forEach(function (it) { it.hidden = true; });
      matches.forEach(function (it, i) { it.hidden = i >= state.shown; });
      if (countEl) countEl.textContent = matches.length + ' ' + noun;
      if (empty) empty.style.display = matches.length ? 'none' : 'block';
      if (more) more.parentNode.style.display = matches.length > state.shown ? '' : 'none';
    }
    function setCat(cat) {
      var found = false;
      Array.prototype.forEach.call(chips, function (c) { var on = c.getAttribute('data-cat') === cat; if (on) found = true; c.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      if (!found) { cat = 'all'; if (chips[0]) chips[0].setAttribute('aria-pressed', 'true'); }
      state.cat = cat; state.shown = size; apply();
    }
    Array.prototype.forEach.call(chips, function (chip) {
      chip.addEventListener('click', function () {
        var cat = chip.getAttribute('data-cat');
        setCat(cat);
        if (history.replaceState) history.replaceState(null, '', cat === 'all' ? location.pathname + location.search : '#cat=' + cat);
      });
    });
    if (input) input.addEventListener('input', function () { state.q = input.value; state.shown = size; apply(); });
    if (more) more.addEventListener('click', function () { state.shown += size; apply(); });
    var m = location.hash.match(/cat=([\w-]+)/);
    setCat(m ? m[1] : 'all');
    window.addEventListener('hashchange', function () { var h = location.hash.match(/cat=([\w-]+)/); setCat(h ? h[1] : 'all'); });
  });
})();
