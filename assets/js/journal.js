/* Chmltech Online Journal: PDF download with lead capture (V4.17).
   The reader's name, email, company, updates choice and the paper are sent to Chmltech by Web3Forms;
   then the PDF downloads. The details are remembered in this browser so the next paper is one click.
   If the form service can't be reached, the download still goes ahead (the reader is never blocked). */
(function () {
  'use strict';
  var dlg = document.getElementById('jdl');
  if (!dlg) return;
  var WEB3FORMS_KEY = 'c6fc23a3-54c8-4bbc-a5c3-06be5ca70a70';
  var STORE = 'chmltech-journal-reader';
  var form = dlg.querySelector('form'), status = dlg.querySelector('.form-status'), submit = form.querySelector('[type="submit"]');
  var F = function (n) { return form.elements[n]; };
  var pdf = dlg.getAttribute('data-pdf'), fname = dlg.getAttribute('data-fname');
  var title = dlg.getAttribute('data-title'), ref = dlg.getAttribute('data-ref');

  function load() { try { return JSON.parse(localStorage.getItem(STORE)) || null; } catch (e) { return null; } }
  function save(o) { try { localStorage.setItem(STORE, JSON.stringify(o)); } catch (e) { /* storage unavailable */ } }

  function openForm() {
    var r = load();
    if (r) { F('name').value = r.name || ''; F('email').value = r.email || ''; F('company').value = r.company || ''; F('updates').checked = !!r.updates; }
    status.className = 'form-status'; status.textContent = '';
    submit.disabled = false; submit.textContent = 'Download PDF';
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
    (r ? submit : F('name')).focus();
  }
  function closeForm() { if (typeof dlg.close === 'function') dlg.close(); else dlg.removeAttribute('open'); }

  function startDownload() {
    var a = document.createElement('a');
    a.href = pdf; a.download = fname; a.rel = 'noopener';
    document.body.appendChild(a); a.click(); a.remove();
    status.className = 'form-status ok';
    status.innerHTML = '';
    status.appendChild(document.createTextNode('Thank you. Your download has started. '));
    var link = document.createElement('a'); link.href = pdf; link.target = '_blank'; link.rel = 'noopener'; link.textContent = 'Open the PDF';
    status.appendChild(link);
    status.appendChild(document.createTextNode(' if it did not.'));
    submit.textContent = 'Downloaded'; submit.disabled = true;
    status.focus();
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-jdl]'), function (b) { b.addEventListener('click', openForm); });
  dlg.querySelector('.j-dl-close').addEventListener('click', closeForm);
  dlg.addEventListener('click', function (e) { if (e.target === dlg) closeForm(); });   // click on backdrop

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (F('botcheck').checked) return;                                                  // spam honeypot
    var reader = { name: F('name').value.trim(), email: F('email').value.trim(), company: F('company').value.trim(), updates: F('updates').checked };
    save(reader);
    var p = new FormData();
    p.append('access_key', WEB3FORMS_KEY);
    p.append('subject', 'Journal PDF download — ' + ref + ' — ' + reader.name);
    p.append('from_name', 'Chmltech Online Journal');
    p.append('form', 'Journal PDF download');
    p.append('name', reader.name);
    p.append('email', reader.email);
    p.append('company', reader.company || '—');
    p.append('wants_updates', reader.updates ? 'Yes (ticked the updates box)' : 'No');
    p.append('paper', ref + ': ' + title);
    p.append('page', location.href);
    submit.disabled = true; submit.textContent = 'Preparing…';
    var done = false;
    var finish = function () { if (!done) { done = true; startDownload(); } };
    var timer = setTimeout(finish, 6000);                                                // never keep the reader waiting
    fetch('https://api.web3forms.com/submit', { method: 'POST', headers: { 'Accept': 'application/json' }, body: p })
      .catch(function () { /* service unreachable: still give the reader the paper */ })
      .then(function () { clearTimeout(timer); finish(); });
  });
})();
