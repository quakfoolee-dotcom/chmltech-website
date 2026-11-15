/* Typesets LaTeX equations in articles with KaTeX: \[ ... \] for display equations and \( ... \) inline. */
(function () {
  'use strict';
  function go() {
    if (!window.renderMathInElement) return;
    var el = document.querySelector('article.prose') || document.body;
    window.renderMathInElement(el, { delimiters: [{ left: '\\[', right: '\\]', display: true }, { left: '\\(', right: '\\)', display: false }], throwOnError: false });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
})();
