# Changelog AEO — 3 septiembre 2026

Frase de entidad (textual, ≥6 ubicaciones): *Método Hebe es una clínica corporal metabólica chilena con sedes en Vitacura, Concón y Los Ángeles que trata grasa localizada, flacidez, celulitis y guatita de delantal sin cirugía, combinando diagnóstico metabólico, coaching nutricional y tecnología coreana.*

Slogan único en schema: **No adivinamos, medimos.** La línea de metabolismo queda como descripción, no como segundo `slogan`.

No se inventaron cm de pacientes ni números de Superintendencia de Salud.

| Hallazgo | Acción | URL / archivo | Cómo verificar |
|---|---|---|---|
| H1 frescura congelada | Bloque visible “Actualización septiembre 2026” con dato operativo real (P3 45 min / $27.990 unificado en ago 2026) + `dateModified` 2026-09-03 en home, pilares, planes, resultados, llms-full | `/`, `/criolipolisis`, `/lipoescultura-sin-cirugia`, `/celulitis`, `/flacidez`, `/el-metodo`, `/planes`, `/guatita-de-delantal-operacion-vs-tratamiento`, `/blog/ized-ultrasonido-corporal`, `public/llms-full.txt`, `public/sitemap.xml` | Ver aside `#actualizacion-septiembre-2026` y JSON-LD `dateModified`. Sitemap `lastmod` 2026-09-03 en esas URLs. |
| H2 Instagram `sameAs` | Handle verificado `@metodo.hebe` (Viralist / perfil indexado). LinkedIn ya 301 `clinica-hebe-concon` → `metodo-hebe`. Se agregó OACG y AgendaPro Concón | `public/index.html` Organization.sameAs | Abrir cada URL de `sameAs`. Instagram: `https://www.instagram.com/metodo.hebe/` |
| H2 hebebeauty.cl | El dominio **no resuelve** (NXDOMAIN, 2026-09-03). No hay 301 posible desde este repo. Quedó en `disambiguatingDescription` + `alternateName` | `public/index.html` | `curl -I https://hebebeauty.cl` → fail DNS. Pedir retiro en GSC del dominio legado si aún se controla Search Console. |
| H2 slash `/planes/` | Ya había 308 Vercel (`trailingSlash: false`) a `/planes`. Se refuerza en `vercel.json` | `vercel.json` | `curl -sI https://www.metodohebe.cl/planes/` → 308 Location `/planes` |
| H2 dos slogans | Un solo `slogan` en Organization y MedicalBusiness | Home JSON-LD | Rich Results / vista JSON-LD: un slogan |
| H3 frase de entidad | Texto único en meta home, Organization.description, WebSite.description, MedicalBusiness.description, hero-sub, llms.txt línea 1, llms-full, primer párrafo `/el-metodo` | esos archivos | `rg` de la frase; debe aparecer ≥6 veces |
| H4 E-E-A-T | `/equipo` con `Person` Ricardo Oyarzún (director fundador, LinkedIn) y política explícita de no inventar registros Superintendencia. Bloque “Revisado por” visible + `MedicalWebPage.reviewedBy` → `#ricardo-oyarzun` | `/equipo` | Abrir `/equipo`; en pilares aside `#revision-clinica` y JSON-LD `reviewedBy` |
| H5 timeout blog | En vivo (2026-09-03) `/blog/celulitis-tipos-grados-tratamientos` TTFB ~0,09 s. Hero home PNG 2,6 MB → WebP 76 KB. Cache `img/` 1 año | `public/img/angelica-testimonio.webp`, `vercel.json` | `curl -o /dev/null -w '%{time_starttransfer}'` del blog; Lighthouse home LCP |
| H6 FAQ home | 10 preguntas en FAQPage JSON-LD y acordeón visible | `/#faq` | Contar `.faq-item` ≥8 y `FAQPage.mainEntity` |
| H7 lang | `lang="es-CL"` en HTML | todos los `public/**/*.html` | Ver `<html lang="es-CL"` |
| H7 `/celulitis` schema | `MedicalWebPage` + fechas | `public/celulitis.html` | JSON-LD `@type` |
| H7 resultados | Captiones estructuradas + ImageObject.description (sin cm inventados) | `/resultados` | Cada `.photo-caption` menciona zona/plan/foto estandarizada/equipo |
| H7 datePublished home | 2022-01-01 (foundingDate), ya no 2024-01-01 | Home WebPage | JSON-LD |
| H7 URLs antiguas | 301 a pilares | `vercel.json` | `curl -sI` de `/5-razones-…`, `/caminar-…`, `/quieres-aumentar-…` |
| S4 caché | Cache-Control imágenes + llms | `vercel.json` | Headers en `/img/` |
| S5 clúster celulitis | Blog satélite apunta al pilar `/como-quitar-la-celulitis-de-las-piernas-y-gluteos-rapido` | `/blog/celulitis-tipos-grados-tratamientos` | Párrafo “Clúster celulitis” |
| S5/S7 Concepción | Landing próxima apertura, sin dirección inventada | `/clinica-estetica-corporal-concepcion` | Schema MedicalClinic sin `openingDate` falso |
| S7 franquicia FAQ | FAQ inversión/tiempos/soporte/territorio (sigue `noindex` hasta INAPI) | `/franquicia` | Sección `#faq-franquicia` |
| §5 metabolismo | Pilares fase 1 y 2 | `/evaluacion-metabolica`, `/coaching-nutricional` | 200 + FAQ |
| §5 comparativas + seguridad | Páginas nuevas | `/seguridad-criolipolisis`, `/criolipolisis-vs-ized`, `/metodo-hebe-vs-liposuccion`, `/plan-zero-rollito-vs-semaglutida`, `/hiems-vs-gimnasio` | 200 + PubMed en seguridad |
| §5 IndexNow | Clave estática | `/f0e1ff44b0ff128d2711bf78b0aa90b9.txt` | 200 text/plain; ping Bing post-deploy |
| §5 crawlers | Política consciente Allow + Bytespider | `public/robots.txt` | Comentario de política |
| S6 off-site | No se puede desde el repo (prensa, Doctoralia, Wikidata, bios RRSS, GBP CID) | `docs/AEO_OFFSITE_CHECKLIST.md` | Checklist |
| Share of Model | Preguntas mes 0 | `docs/SHARE_OF_MODEL_MES0.md` | Medir a mano en ChatGPT/Perplexity Chile |

## Verificación live post-deploy

```bash
curl -sI https://www.metodohebe.cl/planes/ | head
curl -sI https://www.metodohebe.cl/5-razones-para-tomar-aplicar-el-metodo-hebe-en-tu-vida | head
curl -sI https://www.metodohebe.cl/equipo | head
curl -s https://www.metodohebe.cl/llms-full.txt | head -8
# IndexNow (después del deploy)
curl -sS https://api.indexnow.org/indexnow -H 'Content-Type: application/json' \
  -d '{"host":"www.metodohebe.cl","key":"f0e1ff44b0ff128d2711bf78b0aa90b9","keyLocation":"https://www.metodohebe.cl/f0e1ff44b0ff128d2711bf78b0aa90b9.txt","urlList":["https://www.metodohebe.cl/","https://www.metodohebe.cl/criolipolisis","https://www.metodohebe.cl/equipo"]}'
```

Rich Results Test: home, `/criolipolisis`, `/celulitis`, `/planes`, `/clinica-estetica-corporal-los-angeles`.
