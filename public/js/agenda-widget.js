/* Widget de agendamiento de los artículos: sede + día/horario y sigue en /evaluacion con la
   selección precargada. No crea Lead (el único Lead es el submit del wizard en /evaluacion).
   Sin JS queda el <a> de respaldo que ya viene en el HTML. */
(function () {
  'use strict';
  var SEDES = [
    { slug: 'vitacura', nombre: 'Vitacura', dir: 'Los Abedules 3085' },
    { slug: 'concon', nombre: 'Concón', dir: 'Las Pelargonias 842' },
    { slug: 'losangeles', nombre: 'Los Ángeles', dir: 'Av. Gabriela Mistral 269' }
  ];
  var FRANJAS = [
    { n: 1, label: 'Mañana', hora: '10:00 – 13:00' },
    { n: 2, label: 'Tarde', hora: '15:00 – 18:00' },
    { n: 3, label: 'Final tarde', hora: '18:00 – 20:00' }
  ];
  var DIAS = ['DOM', 'LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB'];
  var PIN = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>';
  var ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>';
  var LOGO = '<picture><source type="image/avif" srcset="/img/logo-hebe-stacked.avif"><source type="image/webp" srcset="/img/logo-hebe-stacked.webp"><img src="/img/logo-hebe-stacked.png" alt="Método Hebe" width="44" height="34" decoding="async" loading="lazy"></picture>';

  function track(n, p) { try { if (window.hebeTrack) window.hebeTrack(n, p || {}); } catch (e) {} }

  // Mismo criterio que generateDays() de /evaluacion: 5 días hábiles desde mañana, sin domingo.
  function dias() {
    var out = [], d = new Date(); d.setDate(d.getDate() + 1);
    while (out.length < 5) {
      if (d.getDay() !== 0) out.push({ dow: DIAS[d.getDay()], num: d.getDate(), label: DIAS[d.getDay()] + ' ' + d.getDate() });
      d.setDate(d.getDate() + 1);
    }
    return out;
  }

  function url(origen, bloque, sede, dia, franja) {
    var q = 'origen=' + encodeURIComponent(origen) + '&bloque=' + bloque;
    if (sede) q += '&sede=' + sede.slug;
    if (dia) q += '&dia=' + encodeURIComponent(dia.label);
    if (franja) q += '&franja=' + franja.n;
    return '/evaluacion?' + q;
  }

  function sedeButtons(uid) {
    return SEDES.map(function (s) {
      return '<button type="button" class="aw-sede" data-sede="' + s.slug + '"><span class="aw-sede-ico">' + PIN + '</span><span class="aw-sede-txt"><strong>' + s.nombre + '</strong><small>' + s.dir + '</small></span></button>';
    }).join('');
  }

  function build(root) {
    var origen = root.getAttribute('data-origen') || 'articulo';
    var loc = root.getAttribute('data-location') || 'inline_cta';
    var st = { sede: null, dia: null, franja: null };
    var days = dias();

    root.innerHTML =
      '<div class="aw-head">' + LOGO + '<div><p class="aw-title">Agenda tu Evaluación P3</p><p class="aw-sub">45 min · $27.990 · tu hora se confirma por WhatsApp</p></div></div>' +
      '<p class="aw-step" aria-live="polite">Paso 1 de 2 · Elige tu sede</p>' +
      '<div class="aw-pane aw-pane-1">' + sedeButtons() + '</div>' +
      '<div class="aw-pane aw-pane-2" hidden>' +
        '<p class="aw-chosen"></p>' +
        '<p class="aw-label" id="' + (root.id || 'aw') + '-dlbl">Día</p>' +
        '<div class="aw-days" role="group" aria-labelledby="' + (root.id || 'aw') + '-dlbl">' + days.map(function (d, i) {
          return '<button type="button" class="aw-day" data-i="' + i + '"><span>' + d.dow + '</span><strong>' + d.num + '</strong></button>';
        }).join('') + '</div>' +
        '<p class="aw-label">Horario</p>' +
        '<div class="aw-slots">' + FRANJAS.map(function (f) {
          return '<button type="button" class="aw-slot" data-n="' + f.n + '"><strong>' + f.label + '</strong><small>' + f.hora + '</small></button>';
        }).join('') + '</div>' +
        '<a class="aw-go" href="#" aria-disabled="true">Continuar a mi evaluación ' + ARROW + '</a>' +
        '<button type="button" class="aw-back">Cambiar sede</button>' +
      '</div>';

    var p1 = root.querySelector('.aw-pane-1'), p2 = root.querySelector('.aw-pane-2');
    var step = root.querySelector('.aw-step'), chosen = root.querySelector('.aw-chosen');
    var go = root.querySelector('.aw-go');

    function refresh() {
      var ok = st.sede && st.dia && st.franja;
      go.setAttribute('aria-disabled', ok ? 'false' : 'true');
      go.href = ok ? url(origen, 'widget', st.sede, st.dia, st.franja) : '#';
      chosen.innerHTML = PIN + ' ' + (st.sede ? st.sede.nombre + ' · ' + st.sede.dir : '');
    }
    function pick(list, sel, cls) {
      Array.prototype.forEach.call(list, function (b) { var on = b === sel; b.classList.toggle(cls, on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
    }

    p1.addEventListener('click', function (e) {
      var b = e.target.closest('.aw-sede'); if (!b) return;
      st.sede = SEDES.filter(function (s) { return s.slug === b.getAttribute('data-sede'); })[0];
      pick(p1.querySelectorAll('.aw-sede'), b, 'is-on');
      track('widget_interact', { location: loc, origen: origen, paso: 'sede', sede: st.sede.slug });
      p1.hidden = true; p2.hidden = false; step.textContent = 'Paso 2 de 2 · Día y horario';
      refresh(); root.classList.add('is-step2');
      var first = p2.querySelector('.aw-day'); if (first) first.focus({ preventScroll: true });
    });
    p2.addEventListener('click', function (e) {
      var d = e.target.closest('.aw-day'), f = e.target.closest('.aw-slot');
      if (d) { st.dia = days[+d.getAttribute('data-i')]; pick(p2.querySelectorAll('.aw-day'), d, 'is-on'); track('widget_interact', { location: loc, origen: origen, paso: 'dia', sede: st.sede.slug }); }
      if (f) { st.franja = FRANJAS[+f.getAttribute('data-n') - 1]; pick(p2.querySelectorAll('.aw-slot'), f, 'is-on'); track('widget_interact', { location: loc, origen: origen, paso: 'horario', sede: st.sede.slug }); }
      refresh();
    });
    root.querySelector('.aw-back').addEventListener('click', function () {
      p2.hidden = true; p1.hidden = false; step.textContent = 'Paso 1 de 2 · Elige tu sede'; root.classList.remove('is-step2');
    });
    go.addEventListener('click', function (e) {
      if (go.getAttribute('aria-disabled') === 'true') { e.preventDefault(); return; }
      track('evaluacion_click', { location: loc, origen: origen, sede: st.sede.slug, widget: 1 });
    });
    root.classList.add('is-ready');
  }

  // Versión lateral (solo escritorio ancho, fuera del <article>): sede → continuar. Aparece
  // tras scrollY > 400 (B.4.2), se oculta cerca del footer/CTA final y cuando el widget del
  // artículo está a la vista.
  function sidebar(origen, loc, anchor) {
    if (window.matchMedia && !window.matchMedia('(min-width:1360px)').matches) return;
    var el = document.createElement('aside');
    el.className = 'aw-side'; el.setAttribute('aria-label', 'Agenda tu evaluación');
    el.innerHTML = '<div class="aw-head">' + LOGO + '<div><p class="aw-title">Agenda tu Evaluación P3</p><p class="aw-sub">45 min · $27.990</p></div></div><p class="aw-step">Elige tu sede</p>' +
      SEDES.map(function (s) { return '<a class="aw-sede" href="' + url(origen, 'widget_lateral', s) + '" data-sede="' + s.slug + '"><span class="aw-sede-ico">' + PIN + '</span><span class="aw-sede-txt"><strong>' + s.nombre + '</strong><small>' + s.dir + '</small></span></a>'; }).join('');
    document.body.appendChild(el);
    el.addEventListener('click', function (e) {
      var a = e.target.closest('.aw-sede'); if (a) track('evaluacion_click', { location: loc + '_lateral', origen: origen, sede: a.getAttribute('data-sede'), widget: 1 });
    });
    var hide = { footer: false, inline: false };
    function paint() { el.classList.toggle('is-on', window.scrollY > 400 && !hide.footer && !hide.inline); }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (x) { hide[x.target === anchor ? 'inline' : 'footer'] = x.isIntersecting; }); paint();
      });
      io.observe(anchor);
      var f = document.querySelector('.cta-banner') || document.querySelector('footer'); if (f) io.observe(f);
    }
    window.addEventListener('scroll', paint, { passive: true }); paint();
  }

  function init() {
    var roots = document.querySelectorAll('.agenda-widget');
    Array.prototype.forEach.call(roots, function (r, i) {
      if (!r.id) r.id = 'aw' + i;
      build(r);
      if (r.getAttribute('data-sidebar') === '1') sidebar(r.getAttribute('data-origen') || 'articulo', r.getAttribute('data-location') || 'inline_cta', r);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
