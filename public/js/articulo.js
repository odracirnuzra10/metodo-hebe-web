/* Mejoras de lectura de los artículos: barra de progreso, índice abierto en escritorio y
   medición de clics del índice. Sin JS todo sigue legible (el índice es un <details>). */
(function () {
  'use strict';
  function track(n, p) { try { if (window.hebeTrack) window.hebeTrack(n, p || {}); } catch (e) {} }
  var art = document.querySelector('article.article-body, article');
  if (!art) return;

  var bar = document.createElement('div');
  bar.className = 'read-progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  var ticking = false;
  function paint() {
    ticking = false;
    var r = art.getBoundingClientRect(), total = r.height - window.innerHeight;
    var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
    bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }, { passive: true });
  window.addEventListener('resize', paint); paint();

  var toc = document.querySelector('details.toc');
  if (toc) {
    if (window.matchMedia && window.matchMedia('(min-width:900px)').matches) toc.open = true;
    toc.addEventListener('click', function (e) {
      var a = e.target.closest('a[href^="#"]');
      if (a) track('toc_click', { destino: a.getAttribute('href'), origen: 'articulo' });
    });
  }
})();
