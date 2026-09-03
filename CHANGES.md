## 2026-09-03 — Refresh AEO trimestral (frescura, entidad, E-E-A-T, FAQ)

Ciclo de septiembre 2026 del brief AEO: se actualizó contenido real (unificación P3 45 min / $27.990), no solo la fecha. Frase de entidad única en meta, schema, llms.txt y `/el-metodo`. `sameAs` de Instagram pasa a `@metodo.hebe`. Un solo slogan schema: «No adivinamos, medimos.» Home con 10 FAQ. Nueva `/equipo` (Ricardo Oyarzún como director fundador; sin inventar registros Superintendencia). Pilares con bloque «Revisado por» y `MedicalWebPage.reviewedBy`. Páginas nuevas: evaluación metabólica, coaching nutricional, seguridad criolipólisis, comparativas, Concepción (próxima). 301 de URLs antiguas del sitemap. Detalle: `docs/AEO_CHANGELOG_2026-09.md`.

## 2026-08-28 — La Evaluación P3 pasa a $27.990 y 45 minutos en todo el sitio

Hasta ahora `index.html` y `/evaluacion` ya cobraban la Evaluación P3 ($27.990, 45 minutos, con descuento contra el plan), pero las otras 48 páginas seguían ofreciéndola como gratuita. Cualquiera que llegara por una landing de sede o por el blog agendaba esperando que no le costara nada. Este cambio alinea el resto del sitio con el precio que ya estaba vivo en el home y en el formulario.

### 50 archivos en `public/` (landings de sede, páginas de tratamiento, blog, `/planes`, `/resultados`, `/formalidad`)
- Se elimina toda declaración de gratuidad de la P3: «sin costo», «sin costo ni compromiso», «Evaluación clínica gratuita», «no tiene costo». Queda el valor `$27.990` y, donde la frase no lo decía ya, la duración de 45 minutos.
- Se conserva «sin compromiso»: pagar la evaluación sigue sin obligar a contratar plan. La coletilla tipo queda como `45 minutos · Valor $27.990 · sin compromiso`, con el mismo separador `·` que ya usaba el home.
- La duración de la cita se unifica en 45 minutos. En `clinica-estetica-corporal-vitacura.html` decía «60-90 minutos» y «60 a 90 minutos» en cinco lugares, incluido el JSON-LD.
- **No se tocaron** las menciones de gratuidad ajenas a la P3: la cirugía por Ley 21.438 / Bono PAD / FONASA, «sin costos ocultos» de los planes, la licencia de Clinera sin costo de la página de franquicia, y «el hábito es gratis» del artículo de caminar. Tampoco los 30, 60-90 y 90 minutos que describen la duración de una **sesión de tratamiento**, que no cambia.

### FAQs que quedaban contradictorias
- `clinica-estetica-corporal-concon.html`, `flacidez-corporal-concon/index.html` y `clinica-estetica-corporal-los-angeles.html` respondían «**No.**» a «¿La Evaluación P3 tiene costo?». Ahora responden «**Sí.**», con el valor, los 45 minutos y la nota de que los $27.990 se descuentan del plan. Se corrigió en el JSON-LD y en el acordeón visible, que son dos copias del mismo texto.
- La de Los Ángeles no decía literalmente «sin costo», así que no la agarraba el barrido: se corrigió aparte. También traía «30 a 45 minutos».

### CTAs de agendamiento
- Barra fija de mobile (40 páginas): el botón pasa a `Agenda tu Evaluación P3 · $27.990` y el micro-copy de abajo a `45 minutos · Sin compromiso · Respuesta inmediata`. Es el mismo patrón que ya tenía el home.
- CTAs en prosa que mandan a agendar por WhatsApp o teléfono llevan ahora `(45 minutos, $27.990)` antes del número.
- Botones del nav (`Agenda evaluación`, 53 apariciones): pasan a `Agenda evaluación · $27.990`. El header queda más ancho; en pantallas chicas conviene mirar que no empuje al hamburguesa.

### Verificación
- Los 64 bloques JSON-LD del sitio siguen parseando.
- Ningún tag HTML cambió en los 50 archivos: el diff es solo texto.
- Sin duplicados de «45 minutos» ni de `$27.990` dentro de una misma frase, y sin ningún «60-90 minutos» que haya quedado hablando de la evaluación.

## 2026-08-20 — `/franquicia` entra al sitemap

### `public/sitemap.xml`
- Se agrega `https://www.metodohebe.cl/franquicia` con `changefreq` mensual y prioridad 0.80, en un bloque propio de franquicias.
- Ojo: la página sigue con `noindex, nofollow` hasta confirmar INAPI. Mientras siga así, Search Console va a reportar la URL como "enviada pero marcada con noindex". Las dos cosas tienen que cambiar juntas.

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

### `public/img/logo-clinera.png`, `public/img/logo-clinera-blanco.png`, `public/img/logo-metricads.png` (nuevos)
- Logos oficiales de Clinera —en sus dos variantes, fondo claro y fondo oscuro— y de Metricads, entregados por el dueño de la marca. En los de Clinera se recortó el margen transparente sobrante y se escalaron a 640 px de ancho; el arte no se tocó. El de Metricads va tal cual.
- Clinera cambia de variante según la superficie; el de Metricads es un tile opaco que se lee igual sobre claro y sobre oscuro, y lleva un radio suave para no parecer una foto recortada. Con eso ninguno necesita placa de contención.

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
