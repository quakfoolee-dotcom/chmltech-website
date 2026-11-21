/* Warehouse layout series, Part 1: sizes the embedded Layout Lab (assets/sim/layout-lab.html#embed) to its content.
   The simulator posts its height; the frame follows. No libraries. */
(function () {
  var f = document.getElementById('wl-sim');
  if (!f) return;
  window.addEventListener('message', function (e) {
    if (e.source === f.contentWindow && e.data && e.data.wlHeight) f.style.height = (e.data.wlHeight + 2) + 'px';
  });
  var ask = function () { try { f.contentWindow.postMessage('wlSize?', '*'); } catch (err) {} };
  f.addEventListener('load', ask); ask();
})();
