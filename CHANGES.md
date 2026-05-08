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
