## 2026-08-20 — Landing de captación de franquiciados en `/franquicia`

### `public/franquicia/index.html` (nuevo)
- Landing B2B de captación de franquiciados, mobile-first, con un solo CTA («Agenda una conversación») repetido 7 veces: nav, hero, después del bloque de acompañamiento, después de la sección de pagos, formulario y barra fija de mobile.
- Ocho secciones, cada una desactivando una objeción: hero, dato de operación (facturación y margen de sede propia), tres modalidades, acompañamiento punta a punta —el bloque de mayor peso visual, sobre fondo oscuro—, payback con la rampa declarada, qué se paga cada mes, territorio y formulario.
- Identidad tomada del sitio: misma paleta teal + tinta + oro, mismo `em` en Playfair Display dentro de los títulos, mismo topbar oscuro. Tipografía de texto en Instrument Sans y cifras en Playfair, para un registro de documento de negocio.
- Atributos `data-cro` en `hero`, `hero-headline`, `primary-cta`, `acompanamiento` y `form`. Copy del CTA y su micro-copy en dos constantes al inicio del script, para poder testearlos sin tocar el markup.
- Formulario de cinco campos (nombre, teléfono, email, ciudad o zona, rango de inversión). El handler es un stub: no envía nada y avisa en pantalla y en consola, para que sea imposible publicarlo creyendo que los leads llegan.
- Medición con el mismo stack del sitio (GTM, GA4, Meta Pixel, `hebeTrack`, `hebeAttr`), con los eventos `franquicia_cta_click` y `franquicia_form_submit`.
- `noindex, nofollow` mientras no esté confirmada la inscripción de las marcas en INAPI. El bloqueo está comentado arriba del meta.
- Imágenes bajo el fold con `loading="lazy"` y `decoding="async"`; el logo del nav usa la versión optimizada (37 KB en vez de 361 KB).

### `public/img/logo-clinera.png`, `public/img/logo-clinera-blanco.png` (nuevos)
- Logo oficial de Clinera en sus dos variantes (fondo claro y fondo oscuro), sacadas de Drive. Se recortó el margen transparente sobrante y se escalaron a 640 px de ancho; el arte no se tocó.
- Como cada marca trae su propia variante, los logos van directos sobre la superficie: no hacen falta placas de contención.
- El logo de Metricads queda como placeholder marcado. El que sirve `metricads.com` es una versión antigua y no hay archivo del actual ni en Drive ni en Canva.

## 2026-05-08 — SEO overhaul + mobile redesign for `/resultados`

### `/Users/ricardooyarzun_macair/Documents/Codex/N8N/Hebe/public/resultados/index.html`
- Updated title, meta description, keywords, and `og:title` to target `lipo sin cirugía`, `metodo hebe antes y despues`, and related before/after intent.
- Added `Article`, `FAQPage`, and `ImageObject` JSON-LD blocks for richer indexing and image understanding.
- Reworked the top of the page into a hybrid editorial + gallery format with new H1, snippet-style answer, contextual intro copy, and internal links to criolipólisis and lipoescultura sin cirugía.
- Kept the existing gallery structure but upgraded each zone heading with stronger keyword coverage.
- Added a visible FAQ accordion near the end of the article while preserving the existing clinical disclaimer and bottom evaluation CTA.
- Implemented mobile-only before/after interaction with tap/swipe state changes, sticky CTA bar, footer-aware hide behavior, and IntersectionObserver-based lazy activation for below-fold gallery media.
- Added explicit `width`/`height`, lazy loading, and `<picture>` fallbacks so the gallery is more stable and more compatible with older iOS WebViews.

### `/Users/ricardooyarzun_macair/Documents/Codex/N8N/Hebe/public/img/*.jpg`
- Created JPG fallback companions for the existing before/after WEBP assets used on `/resultados`, so older iOS WebViews have a non-WEBP fallback without changing the original image paths.
