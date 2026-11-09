/* Render interactive figures on solution pages (V4.4). */
(function () {
  'use strict';
  if (!window.ChmFig) return;
  Array.prototype.forEach.call(document.querySelectorAll('figure[data-svc-fig]'), function (f) {
    try {
      var cfg = JSON.parse(f.getAttribute('data-svc-fig'));
      f.setAttribute('data-ready-host', '1');
      window.ChmFig.render(f.querySelector('.fig-host'), cfg);
    } catch (e) { if (window.console) console.error(e); }
  });
})();
