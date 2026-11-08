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

  /* Insights topic filter */
  var chips = document.querySelectorAll('.chip[data-filter]');
  var items = document.querySelectorAll('[data-topic]');
  Array.prototype.forEach.call(chips, function (chip) {
    chip.addEventListener('click', function () {
      var f = chip.getAttribute('data-filter');
      Array.prototype.forEach.call(chips, function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      Array.prototype.forEach.call(items, function (it) {
        it.hidden = !(f === 'all' || it.getAttribute('data-topic') === f);
      });
    });
  });
})();
