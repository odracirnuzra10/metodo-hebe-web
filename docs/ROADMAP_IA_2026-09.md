# Roadmap IA — Método Hebe (`metodohebe.cl`)

**Repo:** `odracirnuzra10/metodo-hebe-web`  
**Horizonte:** 15-sep-2026 → 15-dic-2026  
**Prefijos:** `H` Hebe · `T` transversal · `R` solo Ricardo  
**Prioridad:** P0 esta semana · P1 resto de septiembre · P2 octubre–noviembre · P3 condicional  
**Este documento es autónomo de este repo.** El sibling de Lumina se escribe en `lumina-web`. No copies tareas de Lumina aquí.

**Este PR ya cumple H0.6** (notas fechadas en `CHANGES.md`, `docs/LINK_BUILDING_PLAN_2026.md`, `docs/AEO_CHANGELOG_2026-09.md`, `docs/PROMPTS_PENDIENTES_PUENTE_CLINERA.md`). No vuelvas a abrir un PR solo para esas notas.

**Prohibido en este roadmap:** ejecutar las tareas de código. Quien lea esto es la IA ejecutora de *otro* PR. Una tarea = una rama = un PR.

---

## 0. Prompt maestro para la IA ejecutora

Eres la IA que implementa **una** tarea de este archivo en `metodo-hebe-web`. No improvises el backlog.

### Cómo elegir la siguiente tarea

1. Abre la tabla del §3. Quédate con las filas cuyo **Criterio de aceptación** aún falla en `main`.
2. De esas, toma la de **prioridad más alta** (`P0` > `P1` > `P2` > `P3`).
3. Si hay empate, toma la de **ID menor** cuyo campo **Depende de** esté satisfecho (merge en `main` +, si aplica, decisión `R*` escrita por Ricardo — no la inventes).
4. Si la siguiente es `R*` o está bloqueada por un `R*`, **párate**. Un comentario en el PR o un mensaje: qué falta, de quién, y qué ID queda en cola. Nada más.

### Contrato de trabajo

- **Una tarea = una rama = un PR a `main`.** No mezcles H1.2 con H1.3. No “aprovechas” para limpiar otra cosa.
- Un deploy = **un cambio medible** (un KPI, un bug, un schema). Si no puedes atribuir el resultado a este PR, el PR es demasiado grande: recórtalo.
- No toques HTML/CSS/JS/`vercel.json` si la tarea es de docs. No toques docs ajenos si la tarea es de código, salvo un renglón en `CHANGES.md` cuando el cambio es de producto.
- No implementes `H*`/`T*` que no te asignaron. No “cierres” PRs ajenos salvo que el ID lo pida (H0.1–H0.4).

### Qué leer primero (en este orden)

1. Este archivo: el ID asignado + §1 (intocables) + §4 (si el ID depende de un `R*`).
2. `CLAUDE.md` — si aún no existe, es H0.5; no lo inventes en otro PR. Hasta entonces, §1 de este roadmap es la ley.
3. `docs/PROPUESTA_LANDING_CRIOLIPOLISIS_Y_AUGE.md` §B (B1–B15, B.4) para cualquier cambio en `/criolipolisis` o `/guatita-de-delantal-auge-y-ley`.
4. El archivo que la fila **Archivos** nombra. Verifica cada path con `test -e` antes de editarlo.
5. Reutiliza, no reescribas: `scripts/schema_dates.py`, `public/js/format-schema-date.js`, `hebeAttr`/`hebeTrack` en `public/evaluacion.html`, galería en `public/resultados/index.html`, comentario del sticky en `public/css/shell.css` (líneas 172–186).

### Cómo reportar

En el cuerpo del PR, en este orden:

1. **ID** (ej. `H1.1`) y una frase de qué cambió.
2. **Comando de verificación** de la fila, pegado con su salida.
3. **URLs vivas** tocadas (`curl -sI`) y el código esperado (200 / 301 / 308).
4. **Qué no tocaste** (una línea).
5. Si hay rollback: el comando de **Reversión** de la fila.

### Cuándo parar y preguntar

Una sola pregunta a la vez. Párate si:

- El ID depende de un `R*` sin respuesta escrita de Ricardo.
- Haría falta inventar un registro de Superintendencia, un cm de paciente, una reseña, una dirección, una fecha de apertura o un `ratingCount`.
- El cambio viola B1–B15 o B.4.
- El JSON-LD deja de parsear o dos nodos de la misma página comparten `@id`.
- No estás seguro de si un CTA extra cabe en el tope de 5 puntos de conversión del `<article>` (B.4.5).

Idioma de copy: **español de Chile, sin voseo**. Tratá de usted/tú según el tono ya publicado en esa página; no pases a “vos”.

---

## 1. Reglas del repo

Contrato. Si una implementación choca con esta lista, **gana la regla**. Fuente: `docs/PROPUESTA_LANDING_CRIOLIPOLISIS_Y_AUGE.md` §B.1–B.4 (B1–B15, B.4) y política AEO vigente.

### B1–B15 — intocables (páginas `/criolipolisis` y `/guatita-de-delantal-auge-y-ley`; el espíritu aplica al resto)

| # | Qué no se toca |
|---|---|
| B1 | URL `/criolipolisis` y `/guatita-de-delantal-auge-y-ley`. Ni 301. Están en `public/sitemap.xml`, `public/llms.txt` y en `docs/LINK_BUILDING_PLAN_2026.md`. |
| B2 | `<link rel="canonical">` self-canonical **sin** slash (`trailingSlash: false` en `vercel.json`). |
| B3 | Texto del `<h1>` actual. Se puede restilar, no reescribir. |
| B4 | Todos los `<h2>` y `<h3>` existentes. Se **agregan** nuevos; no se editan, reordenan ni degradan. |
| B5 | `<p>`, `<ul>`, `<ol>`, `<table>` actuales del `<article>`. Cero borrado. El word count solo sube. |
| B6 | Citas bibliográficas (Manstein & Anderson 2008, Ingargiola 2015, Krueger 2014, Jalian 2014). |
| B7 | Disclaimer de fuentes oficiales en AUGE (“no inventamos cifras ni plazos”). |
| B8 | Los 3 nodos JSON-LD de cada página (`MedicalWebPage`, `BreadcrumbList`, `FAQPage`). Solo se **amplía** el `@graph`. |
| B9 | FAQ visible ↔ `FAQPage` 1:1. Schema de contenido no visible = riesgo de acción manual. |
| B10 | Enlaces dofollow a `bcn.cl` y `fonasa.cl`. No `nofollow`, no quitar. |
| B11 | Enlaces internos salientes actuales. Se agregan; no se quitan. |
| B12 | Enlaces internos entrantes del mapa B.5. Sin redirección, sin cambio de anchor, sin borrado. |
| B13 | `meta robots`: `index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1`. |
| B14 | `hreflang` (3 líneas: `es-CL`, `es`, `x-default`). |
| B15 | `window.hebeTrack`: mapa Meta `{'whatsapp_click':'Contact'}`. Los CTA **no** vuelven a disparar `Lead`. El único `Lead` legítimo es el submit del wizard (`public/evaluacion.html`, hoy ~2612). |

### B.4 — límites duros de CTA

1. Sticky móvil ≤ 15 % del viewport (~100 px en 667 px).
2. No aparece antes de `scrollY > 400`.
3. Se oculta al llegar al footer (`IntersectionObserver`; patrón vivo en `public/resultados/index.html` ~1505–1507, clase `.is-hidden`).
4. Cero pop-ups, modales, exit-intent u overlays de pantalla completa.
5. Máximo **5 puntos de conversión** dentro del `<article>`.
6. `body { padding-bottom }` en CSS inicial (no inyectado por JS) para no tapar texto ni generar CLS.

### Prohibiciones transversales

- **Nunca** `AggregateRating` nuevo ni `Review` oculto (`display:none` en `reviewRating`). Hoy hay `AggregateRating` solo en `public/clinica-estetica-corporal-vitacura.html` y `Review` microdata con rating oculto en `public/index.html` y `public/planes/index.html` (H1.5).
- **Nunca** inventar registros de Superintendencia, centímetros de pacientes, reseñas, direcciones o fechas. Si no está en GBP / `share.google` / copy ya publicado y reconciliado (R3), no va.
- Español de Chile, sin voseo.
- JSON-LD parseable (`json.loads`). **Un nodo por `@id` por página.** Referenciar un `@id` de otra página (Person, Organization) está bien; **redefinir** el mismo `@id` como nodo completo en 9 archivos (`#faq-local`) no lo está (H1.4).
- Fechas de schema: `scripts/schema_dates.py` / `public/js/format-schema-date.js`. Offset `America/Santiago`. No inventar el día del calendario.
- Un cambio medible por deploy.

---

## 2. Estado verificado (2026-09-13)

Verificado en `main` (`a566232`) y en vivo. No re-auditar este cuadro: usalo como línea base. Re-corrí solo los comandos de la tarea que vas a tocar.

### Hebe + compartido — hecho

| Ítem | Evidencia 2026-09-13 |
|---|---|
| `clinicahebe.cl` → `www.metodohebe.cl` | `curl -sI https://clinicahebe.cl/` y `https://www.clinicahebe.cl/` → **301** `location: https://www.metodohebe.cl/`. X12 / «Redirect pendiente» obsoletos. |
| `hebeAttr` + `hebeTrack` en `/evaluacion` | `public/evaluacion.html` :92–93. `hebeAttr` también en 61 HTML. Payload n8n lleva UTM / `landing_page` / `pagina_origen`. |
| Sticky: hide de `shell.css` **quitado** | Comentario en `public/css/shell.css` :172–186. **No es B.4:** 56 páginas tienen markup; ~10 tienen JS `.visible`; `/resultados` usa `.is-hidden` + observer de footer. |
| Grafo `MedicalBusiness` | Presente en los 66 HTML. |
| Sitemap | `grep -c '<loc>' public/sitemap.xml` = **62**. |
| JSON-LD | 92 bloques; **0** fallos de parse. |
| `/planes/` | **308** → `/planes` por `trailingSlash: false`. **No** hay fila en `vercel.json`. |
| `/fundador/` | **308** → `/fundador`, pero canonical/`og:url` del HTML aún llevan slash (H1.3). |
| `/franquicia` | **200**. Ya no es stub: POST n8n + fallback `mailto` (H0.6 / `CHANGES.md`). Sigue `noindex` hasta R8. |
| Concepción (página) | `/clinica-estetica-corporal-concepcion` **200**. H1: no hay sede. Footer/topbar de otras páginas siguen «próxima» (H1.10). |
| GBP `share.google` | Vitacura `MsZnMY3vYGe6bW1Mo` · Concón `G1xHnaCeC1qxxoc6F` · Los Ángeles `TXyvAWXsTRvMAu9gD`. `curl -sI` → **302**. |
| Clinera caso | `https://www.clinera.io/casos/metodo-hebe` **200**. Host apex `https://clinera.io` mezclado en schema de `/clinica/*` (H1.10). |
| IndexNow | `f0e1ff44b0ff128d2711bf78b0aa90b9.txt` **200**. Huérfana `ab767007d40e7700a59b91b6f690a54f.txt` también **200** (H5.4). |
| `og:image` | 17/66 HTML. Faltan **49** (H1.2). Asset bueno: `https://www.metodohebe.cl/img/og-metodo-hebe.jpg` **200**. |

### Pendiente / roto (no implementar en este PR)

| Ítem | Dónde | Tarea |
|---|---|---|
| `knowsAbout` ausente en Organization del home | `public/index.html` · PR #37 sucio | H0.1 |
| PR #43 draft, duplicado de `8b44c01` | pago P3 ya en `main` | H0.2 |
| PR #51 draft, catálogo equipos | merge solo con R7 | H0.3 |
| Auditoría UX solo en PR #4 | 50 archivos; rescatar **solo** el md | H0.4 |
| `CLAUDE.md` no existe | raíz del repo | H0.5 |
| Sticky **no** cumple B.4 | 56 markup / ~10 JS / umbral 300 vs 400 | H1.1 |
| 49 páginas sin `og:image`; 7 URLs de schema **404** | ver H1.2 | H1.2 |
| Slash / `www` en `@id` y `og:url` | 13 `og:url` ≠ canonical; 61 `@id` sin `www` | H1.3 |
| `@id` reutilizado entre páginas | `#faq-local` ×9; locations ×3–4 | H1.4 |
| `AggregateRating` Vitacura 4.9/120; Review oculto | home + `/planes` | H1.5 |
| Residuos P3 + cifras | `/evaluacion` dice +20.000; footer +30.000; «gratuita» residual | H1.6 |
| Enlaces Fase 1 (propuesta 1.5–1.6) | criolipólisis ↛ `/resultados`; AUGE ↛ PAD/FONASA en cuerpo | H1.7 |
| `whatsapp_click` en botones a `/evaluacion` | p.ej. `public/resultados/index.html` :1305; landings `btn-wa` | H1.8 |
| AUGE `dateModified` 2026-04-23 | no contrastado con Ley 21.438 vigente | H1.9 |
| Concepción «próxima» vs «no hay sede» | footers/topbars vs landing | H1.10 |
| Contraste AA CTA | blanco sobre `#14B5A7` ~2,56:1 (auditoría PR #4) | H2.1 |
| `/evaluacion` a11y | `<label>` sin `for`; H1 clip; sede-cards `div`+`onclick` | H2.2 |
| Cuota mensual bajo precios | no está; FAQ de `/planes` la difiere a P3 | H2.3 + R1 |
| `<picture>` AVIF/WebP; 4 `.webm` huérfanos | 8 páginas con `<picture>`; `public/video/*.webm` sin referencias | H2.4 |
| `/formalidad` es deck Lumina | `noindex`, title «Protocolo Lumina» | H5.3 |

### Comandos de línea base (corren en `main` hoy)

```bash
# JSON-LD parseable — debe imprimir "fails 0"
python3 - <<'PY'
import json, re
from pathlib import Path
fails = 0
for p in Path('public').rglob('*.html'):
    t = p.read_text(errors='replace')
    for i, b in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)):
        try:
            json.loads(b)
        except Exception as e:
            fails += 1
            print(p, i, e)
print('fails', fails)
PY

# Sitemap
test "$(grep -c '<loc>' public/sitemap.xml)" -eq 62 && echo 'sitemap loc=62 OK'

# Aún DEBEN permanecer (no son la tarea de este PR)
test ! -f CLAUDE.md && echo 'CLAUDE.md ausente (H0.5)'
! grep -q knowsAbout public/index.html && echo 'knowsAbout ausente (H0.1)'
grep -n 'AggregateRating' public/clinica-estetica-corporal-vitacura.html
grep -n 'display:none' public/index.html public/planes/index.html | grep -i rating || true
```

---

## 3. Bloques de trabajo

Formato fijo por tarea. IDs únicos.

### Bloque 0 — P0 higiene de PRs y docs (esta semana)

#### H0.1 · Prioridad P0 · Esfuerzo S · Depende de — · Archivos `public/index.html`

**Prompt para la IA.** PR #37 (`https://github.com/odracirnuzra10/metodo-hebe-web/pull/37`, rama `claude/seo-ai-crawlers-audit-7lex09`) está **open** y `dirty` contra `main`. El único cambio útil es `knowsAbout` en el nodo `Organization` de `public/index.html`. En `main` hoy `knowsAbout` **no está**. Reaplica el array del PR (sin claims nuevos: tratamientos corporales no invasivos, grasa localizada, celulitis, flacidez, salud metabólica, guatita de delantal, tecnología coreana). No reabras el resto de esa rama. Después del merge, cierra #37 como completado por este PR.

**Criterio de aceptación.** `Organization.knowsAbout` existe, parsea, y no inventa categorías que el sitio no describa. #37 cerrado.

**Verificación (comando).**

```bash
python3 - <<'PY'
import json, re
from pathlib import Path
t = Path('public/index.html').read_text()
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
found = False
for b in blocks:
    data = json.loads(b)
    nodes = data.get('@graph', [data]) if isinstance(data, dict) else data
    for n in nodes:
        if n.get('@type') in ('Organization', ['Organization']) or 'Organization' in (n.get('@type') if isinstance(n.get('@type'), list) else [n.get('@type')]):
            assert 'knowsAbout' in n and len(n['knowsAbout']) >= 5, n
            found = True
print('knowsAbout OK' if found else 'FAIL')
PY
curl -sI https://www.metodohebe.cl/ | head -3   # expect 200 post-deploy
```

**Reversión.** `git revert` del commit de este ID. Reabrir #37 solo si el revert deja el home otra vez sin `knowsAbout`.

#### H0.2 · Prioridad P0 · Esfuerzo S · Depende de — · Archivos — (comentario GitHub)

**Prompt para la IA.** PR #43 (`https://github.com/odracirnuzra10/metodo-hebe-web/pull/43`, draft, `cursor/pay-cta-evaluacion-2574`) es duplicado de `8b44c01` («CTA de pago más visible post-wizard en `/evaluacion`»), ya en `main`. No merges. Adjunta en un comentario el `git diff 8b44c01...dc4e568` (o `main...cursor/pay-cta-evaluacion-2574` acotado a `public/evaluacion.html`) y cierra #43 como *not planned* / duplicado. Cero cambios de código.

**Criterio de aceptación.** Comentario con diff. #43 cerrado. `main` sin tocar.

**Verificación (comando).**

```bash
git log --oneline -1 8b44c01
gh pr view 43 --json state,title,closedAt
```

**Reversión.** Reabrir #43. No hay diff de sitio.

#### H0.3 · Prioridad P0 · Esfuerzo M · Depende de R7 · Archivos PR #51 (`public/index.html`, `public/el-metodo.html`, `public/llms.txt`, `public/llms-full.txt`, `public/img/tech-*.webp`)

**Prompt para la IA.** PR #51 (`https://github.com/odracirnuzra10/metodo-hebe-web/pull/51`, draft, `cursor/update-hebe-technologies-20d6`) actualiza el catálogo según fotos de sala: iZED, Corpo Hera, Carbox CK, Crio CK, Skin Wave Max, Cuorpo Lift, Cuky Body, Sculpt DD, Sculpt DD Firm + Laser Trimax en llms. **No merges sin R7.** Antes: tabla de consistencia nombre-en-máquina vs copy vs `llms-full.txt` vs `/franquicia` (ya corregido en #50, `a566232`). Si un nombre no está en la foto o contradice `/franquicia`, no lo inventes: lista la duda en el PR y espera R7. Tras R7, marca listo y mergea.

**Criterio de aceptación.** Tabla en el PR. Cero nombres no fotografiados. Merge solo con R7 explícito.

**Verificación (comando).**

```bash
gh pr view 51 --json state,mergeable,files
# Tras merge, en main:
rg -n 'Cuorpo Lift|Corpo Lift|iZED|Adipolite|Skin Wave Max|SkinWave' public/index.html public/el-metodo.html public/llms-full.txt public/franquicia/index.html
curl -sI https://www.metodohebe.cl/ | head -3   # 200
```

**Reversión.** `git revert` del merge de #51.

#### H0.4 · Prioridad P0 · Esfuerzo S · Depende de — · Archivos `docs/AUDITORIA_UX_UI_HEBE_LUMINA_2026.md` (nuevo en `main`)

**Prompt para la IA.** PR #4 (`https://github.com/odracirnuzra10/metodo-hebe-web/pull/4`, rama `claude/ux-ui-analysis-metodohebe-ngct7n`) dice “solo docs” pero el diff toca **50 archivos**. **Rescata únicamente** `docs/AUDITORIA_UX_UI_HEBE_LUMINA_2026.md` sobre `main`. Cero HTML/CSS/JS. Cierra #4 después. No “arregles” contraste ni peso en este PR (eso es H2.1 / H2.4).

**Criterio de aceptación.** El md existe en `main`. `git diff main -- public` vacío en este PR. #4 cerrado.

**Verificación (comando).**

```bash
test -e docs/AUDITORIA_UX_UI_HEBE_LUMINA_2026.md && echo OK
git diff origin/main --name-only | grep -E '^(public/|vercel.json|scripts/)' && echo 'FAIL tocó código' || echo 'docs only'
```

**Reversión.** Borrar el md; reabrir #4.

#### H0.5 · Prioridad P0 · Esfuerzo S · Depende de — · Archivos `CLAUDE.md` (nuevo)

**Prompt para la IA.** Crea `CLAUDE.md` en la raíz. Contenido mínimo: qué es el repo (estático, `public/` = output Vercel); leer este roadmap + §1; B15 / Lead; no inventar Superintendencia/cm/reseñas/direcciones/fechas; español CL sin voseo; JSON-LD parseable y un `@id` por nodo por página; fechas con `scripts/schema_dates.py`; sticky B.4; una tarea = un PR; comandos de línea base del §2. No copies políticas de Lumina. No implementes H1–H5 aquí.

**Criterio de aceptación.** `test -e CLAUDE.md`. Un PR que solo añade ese archivo.

**Verificación (comando).**

```bash
test -e CLAUDE.md && wc -l CLAUDE.md
grep -q 'B15\|hebeTrack\|ROADMAP_IA_2026-09' CLAUDE.md && echo refs_ok
```

**Reversión.** `git rm CLAUDE.md`.

#### H0.6 · Prioridad P0 · Esfuerzo S · Depende de — · Archivos notas fechadas

**Ya hecho en el PR que introduce este roadmap.** No abras otro PR. Si alguien lo “rehace”, está duplicando trabajo.

**Criterio de aceptación.** Notas 2026-09-13 en los cuatro archivos del encabezado.

**Verificación (comando).**

```bash
rg -n '2026-09-13' CHANGES.md docs/LINK_BUILDING_PLAN_2026.md docs/AEO_CHANGELOG_2026-09.md docs/PROMPTS_PENDIENTES_PUENTE_CLINERA.md
```

**Reversión.** Revertir solo esos hunks de notas, no el roadmap.

---

### Bloque 1 — P1 septiembre

#### H1.1 · Prioridad P1 · Esfuerzo M · Depende de — · Archivos `public/css/shell.css` (solo lectura del comentario), páginas con `.mobile-sticky-cta`, patrón `public/resultados/index.html` :1505–1507 y `public/index.html` :1417

**Prompt para la IA.** El hide global de `shell.css` ya no existe. **Esto no es B.4.** Implementá B.4 de verdad y **desplegá solo este cambio**: JS `.visible` (o el `.is-hidden` de `/resultados`) con `scrollY > 400` (el home usa 300: subilo a 400 donde toques), `IntersectionObserver` del footer, `padding-bottom` en CSS inicial, alto ≤15 % del viewport a 390 px. Unificá el evento del sticky de criolipólisis a `evaluacion_click` + `location:'mobile_sticky'` (propuesta 1.2). No agregues bloques nuevos. Medí 7 días antes de H3.

**Criterio de aceptación.** En 390 px el sticky no está en el hero, aparece after 400 px, se oculta en el footer, no tapa el `.cta-banner`, CLS estable. Un solo PR.

**Verificación (comando).**

```bash
rg -n 'scrollY\s*>\s*400|mobile-sticky-cta' public/criolipolisis/index.html public/guatita-de-delantal-auge-y-ley/index.html public/resultados/index.html public/index.html
# Playwright 390px (local): sticky hidden at y=0, visible at y=500, hidden when footer in view
curl -sI https://www.metodohebe.cl/criolipolisis | head -3   # 200
```

**Reversión.** `git revert`. El comentario de `shell.css` :172–186 debe seguir advirtiendo que no se reintroduzca `transform:translateY(100%)` global.

#### H1.2 · Prioridad P1 · Esfuerzo M · Depende de — · Archivos 49 HTML sin `og:image`; JSON-LD con imágenes 404; `public/franquicia/index.html`

**Prompt para la IA.** Añadí `og:image` + `twitter:image` a las 49 páginas que no tienen `property="og:image"` (lista en el script del §2 / recuento 17 vs 49). Preferí `https://www.metodohebe.cl/img/og-metodo-hebe.jpg` (**200**) salvo que la página ya tenga foto de sede real. Corregí las **7** URLs de schema que hoy 404: ` /og-vitacura.jpg`, `/img/hebe-og.jpg`, `/img/hebe-concon.jpg`, `/img/metodo-hebe-concon.jpg`, `/img/metodo-hebe-vitacura.jpg`, `/img/logo.png`, y la de franquicia `https://metodohebe.cl/img/LOS%20ANGELES.avif` (sin `www`, AVIF). Franquicia: JPG/WebP con host `www`. No inventes fotos de Concepción.

**Criterio de aceptación.** 0 HTML sin `og:image`. `curl -sI` de cada URL de imagen en JSON-LD → 200. Franquicia `og:image` es `https://www.metodohebe.cl/img/...jpg` o `.webp`.

**Verificación (comando).**

```bash
python3 - <<'PY'
from pathlib import Path
miss=[p for p in Path('public').rglob('*.html') if 'property="og:image"' not in p.read_text(errors='replace')]
print('missing', len(miss))
for p in miss: print(p)
PY
# Las 7 no deben permanecer:
for u in \
  https://www.metodohebe.cl/og-vitacura.jpg \
  https://www.metodohebe.cl/img/hebe-og.jpg \
  https://www.metodohebe.cl/img/hebe-concon.jpg \
  https://www.metodohebe.cl/img/metodo-hebe-concon.jpg \
  https://www.metodohebe.cl/img/metodo-hebe-vitacura.jpg \
  https://www.metodohebe.cl/img/logo.png
 do curl -sI "$u" | head -1; done
# hoy: 404. Tras el PR: no deben aparecer en el HTML.
rg -n 'og-vitacura\.jpg|hebe-og\.jpg|hebe-concon\.jpg|metodo-hebe-concon\.jpg|metodo-hebe-vitacura\.jpg|img/logo\.png|LOS%20ANGELES' public --glob '*.html' && echo 'FAIL still referenced' || echo 'gone'
```

**Reversión.** `git revert`. No borres `img/og-metodo-hebe.jpg`.

#### H1.3 · Prioridad P1 · Esfuerzo S · Depende de — · Archivos `public/fundador/index.html` + 13 HTML con `og:url` ≠ canonical + JSON-LD `@id` sin `www`

**Prompt para la IA.** Higiene de URL. Canonical y `og:url` = `https://www.metodohebe.cl/<path>` **sin** slash final (`trailingSlash: false`). `/fundador` hoy: canonical y `og:url` con slash, vivo 308 a `/fundador`. Alineá `@id` al host `www` (hoy 61 `@id` apex). No cambies el path (B1). No toques `vercel.json` salvo que H5 lo pida en otro PR.

**Criterio de aceptación.** `og:url` == canonical en los 66 HTML. Cero `@id` `https://metodohebe.cl/` (apex) en nodos de página. `/fundador` sin slash.

**Verificación (comando).**

```bash
python3 - <<'PY'
import re
from pathlib import Path
bad=0
for p in Path('public').rglob('*.html'):
    t=p.read_text(errors='replace')
    c=re.search(r'rel="canonical" href="([^"]+)"',t)
    o=re.search(r'property="og:url" content="([^"]+)"',t)
    if c and o and c.group(1)!=o.group(1):
        bad+=1; print('mismatch', p, c.group(1), o.group(1))
print('mismatches', bad)
PY
rg -n '"@id": "https://metodohebe.cl/' public --glob '*.html' | head
curl -sI https://www.metodohebe.cl/fundador/ | head -5   # 308 Location: /fundador
curl -sI https://www.metodohebe.cl/fundador | head -3     # 200
```

**Reversión.** `git revert`.

#### H1.4 · Prioridad P1 · Esfuerzo M · Depende de H1.3 · Archivos 66 HTML

**Prompt para la IA.** Un nodo por `@id` **por página**. Referencias (`{"@id":"...#person"}` sin redefinir el Person) están bien. Hoy `#faq-local` se **define** en 9 archivos; `#location-vitacura` / `#location-losangeles` / `#losangeles` se redefinen en landings de sede. Desduplicá: o bien `@id` único por página (`…/celulitis-vitacura#faq`), o deja el nodo completo solo en el home y el resto solo referencia. Parseable. No borres nodos B8.

**Criterio de aceptación.** Ningún `@id` aparece como nodo completo más de una vez en el mismo HTML. Los `@id` de FAQ/location de landings no colisionan con el home.

**Verificación (comando).**

```bash
python3 - <<'PY'
import json, re
from pathlib import Path
from collections import Counter, defaultdict
cross=defaultdict(set)
for p in Path('public').rglob('*.html'):
    ids=[]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', p.read_text(errors='replace'), re.S):
        try: data=json.loads(b)
        except Exception as e:
            print('PARSE', p, e); continue
        nodes=data.get('@graph',[data]) if isinstance(data,dict) else data
        if not isinstance(nodes,list): nodes=[nodes]
        for n in nodes:
            if isinstance(n,dict) and n.get('@id') and set(n)-{'@id','@type'}:
                ids.append(n['@id']); cross[n['@id']].add(str(p))
    d=[i for i,c in Counter(ids).items() if c>1]
    if d: print('INPAGE', p, d)
print('cross-defined', {k: len(v) for k, v in cross.items() if len(v) > 1})
PY
```

**Reversión.** `git revert`.

#### H1.5 · Prioridad P1 · Esfuerzo S · Depende de R3 · Archivos `public/clinica-estetica-corporal-vitacura.html`, `public/index.html`, `public/planes/index.html`

**Prompt para la IA.** Quitá `AggregateRating` de Vitacura y el `reviewRating` `display:none` de home y `/planes`. No agregues `AggregateRating` en Concón/Los Ángeles. La cifra visible de reseñas (si R3 entrega número de GBP) va en texto visible, no en schema, hasta que R3 diga lo contrario. Sin R3: solo borrás el schema/microdata oculto; **no** inventás “+1.000 reseñas” nuevo.

**Criterio de aceptación.** `rg AggregateRating public` vacío. Cero `itemtype="https://schema.org/Review"` con `display:none`. Copy visible de rating solo si R3.

**Verificación (comando).**

```bash
rg -n 'AggregateRating|aggregateRating' public --glob '*.html' && echo FAIL || echo 'no AggregateRating'
rg -n 'itemtype="https://schema.org/Review"' public --glob '*.html'
rg -n 'display:none' public/index.html public/planes/index.html | rg -i 'rating|review' && echo 'hidden rating remains' || echo 'no hidden rating'
```

**Reversión.** `git revert`.

#### H1.6 · Prioridad P1 · Esfuerzo S · Depende de R3 (cifras) · Archivos landings con «gratuita» / «sin costo»; `public/evaluacion.html` (+20.000)

**Prompt para la IA.** No está “sin residuos P3”. Barré menciones de evaluación gratuita que contradigan $27.990 / 45 min (`CHANGES.md` 2026-08-28). Conservá gratuidades **ajenas** a P3: Ley 21.438 / Bono PAD, «sin costos ocultos» de planes, licencia Clinera en `/franquicia`, «el hábito es gratis» de caminar, bioimpedancia «sin costo adicional al contratar plan» en `public/blog/sede-los-angeles/index.html`. Cifras: `/evaluacion` dice «+20.000 personas»; el footer sitewide dice «+30.000». **No unifiques sin R3.** Con R3, un solo número en `/evaluacion` y el resto.

**Criterio de aceptación.** Cero «Evaluación clínica gratuita» / «sin costo ni compromiso» referidos a P3. Cifras de pacientes tocadas solo con R3.

**Verificación (comando).**

```bash
rg -n -i 'evaluación clínica gratuita|sin costo ni compromiso|evaluaci[oó]n .*gratuita' public --glob '*.html'
rg -n '+20.000|+30.000' public/evaluacion.html public/index.html
```

**Reversión.** `git revert`.

#### H1.7 · Prioridad P1 · Esfuerzo S · Depende de — · Archivos `public/criolipolisis/index.html`, `public/guatita-de-delantal-auge-y-ley/index.html` (+ destinos ya existentes)

**Prompt para la IA.** Fase 1 de enlaces internos (propuesta 1.5–1.6). En la sección «antes y después» de `/criolipolisis`, enlace contextual a `/resultados` (la galería ya vive en `public/resultados/index.html`). En AUGE, enlaces contextuales a `/bono-pad-guatita-de-delantal` y `/guatita-de-delantal-fonasa-isapre`. Insertar, no reemplazar (B11, B20). No toques H1/H2 (B3–B4). No es Fase 2.

**Criterio de aceptación.** Los tres destinos aparecen como `inline-link` (o equivalente en cuerpo). B.5 no pierde anchors.

**Verificación (comando).**

```bash
rg -n 'href="/resultados"' public/criolipolisis/index.html
rg -n 'bono-pad-guatita-de-delantal|guatita-de-delantal-fonasa-isapre' public/guatita-de-delantal-auge-y-ley/index.html
curl -sI https://www.metodohebe.cl/resultados | head -3   # 200
curl -sI https://www.metodohebe.cl/bono-pad-guatita-de-delantal | head -3   # 200
```

**Reversión.** `git revert`.

#### H1.8 · Prioridad P1 · Esfuerzo M · Depende de — · Archivos landings con `hebeTrack('whatsapp_click'` hacia `/evaluacion`; `public/evaluacion.html` (listener :11–27); `data-section`

**Prompt para la IA.** Tres cosas, un PR de medición (no de copy): (1) `scroll_depth` 25/50/75/90 vía `hebeTrack` (propuesta G.3; ampliar el patrón de `public/index.html` :1426). (2) `id` / `data-section` en secciones de conversión para que `click_location` no caiga en `'home'` (A.5 / G.5). (3) **Dejá de disparar `whatsapp_click` en botones que van a `/evaluacion`** (ej. `public/resultados/index.html` :1305 `mobile-sticky-wa` → `/evaluacion`; `btn-wa` / `cta-btn-wa` en pilares). Esos son `evaluacion_click`. Respetá B15: no `Lead` en CTA. En `/evaluacion`, el submit del wizard sigue siendo el único `Lead`.

**Criterio de aceptación.** `rg "hebeTrack\('whatsapp_click'" public` solo en `href` que contienen `wa.me` o `whatsapp`. `scroll_depth` en `/criolipolisis` y `/guatita-de-delantal-auge-y-ley` como mínimo.

**Verificación (comando).**

```bash
rg -n "hebeTrack\('whatsapp_click'" public --glob '*.html' | rg -v 'wa.me|whatsapp.com' && echo 'FAIL click on non-WA' || echo 'whatsapp_click only on WA'
rg -n "hebeTrack\('scroll_depth'" public/criolipolisis/index.html public/guatita-de-delantal-auge-y-ley/index.html
```

**Reversión.** `git revert`.

#### H1.9 · Prioridad P1 · Esfuerzo M · Depende de — · Archivos `public/guatita-de-delantal-auge-y-ley/index.html`

**Prompt para la IA.** Refresh normativo Ley 21.438. `dateModified` visible y schema siguen en **2026-04-23**. Contrastá el texto con `bcn.cl` (B7, B10: no quites esos enlaces). Actualizá solo hechos que la ley/reglamento vigente confirmen. Si un plazo o requisito no está en fuente oficial, no lo escribas. `dateModified` con `format_schema_date` (hoy real). Esto **no** es Fase 3 (H4). No cambies el H1 (B3).

**Criterio de aceptación.** Disclaimer intacto. Enlaces `bcn.cl`/`fonasa.cl` dofollow. `dateModified` ≥ 2026-09. FAQ visible = schema.

**Verificación (comando).**

```bash
rg -n 'bcn.cl|fonasa.cl|Ley 21.438' public/guatita-de-delantal-auge-y-ley/index.html
rg -n 'dateModified|datetime=' public/guatita-de-delantal-auge-y-ley/index.html
python3 -c "import json,re; t=open('public/guatita-de-delantal-auge-y-ley/index.html').read();
print('parse', all(json.loads(b) for b in re.findall(r'<script type=\"application/ld\\+json\">(.*?)</script>',t,re.S)))"
curl -sI https://www.metodohebe.cl/guatita-de-delantal-auge-y-ley | head -3   # 200
```

**Reversión.** `git revert` + recrawl.

#### H1.10 · Prioridad P1 · Esfuerzo M · Depende de R9 (si hubiera fecha/dirección) · Archivos footers/topbars «Concepción (próxima)»; `public/clinica-estetica-corporal-concepcion.html`; `public/clinica/*`; schema `share.google` / `clinera.io`

**Prompt para la IA.** Alineá Concepción: la landing dice **no hay sede**; topbars/footers dicen «próxima». Un solo mensaje: no opera en Concepción; Biobío = Los Ángeles. **Sin R9 no inventes** apertura, Maps ni calle. Maps: los tres `share.google` ya están y 302; no inventes `?cid=`. `/clinica/*`: unificá host Clinera a `https://www.clinera.io` (caso 200) y, si hay CTA WhatsApp, usá `wa.me/56963222683` (el mismo número del sitio) sin disparar `Lead`. No pongas `URL_RESERVA_HEBE` hasta R10.

**Criterio de aceptación.** Cero «Concepción (próxima)» que contradigan la landing. Schema de Concepción sin `PostalAddress` inventado. Clinera `www` en `/clinica/*`.

**Verificación (comando).**

```bash
rg -n 'Concepción \(próxima\)|próxima: Concepción' public --glob '*.html'
rg -n 'https://clinera.io[^\.]' public/clinica --glob '*.html'
curl -sI https://www.metodohebe.cl/clinica-estetica-corporal-concepcion | head -3   # 200
curl -sI https://www.clinera.io/casos/metodo-hebe | head -3   # 200
curl -sI https://share.google/MsZnMY3vYGe6bW1Mo | head -5   # 302
```

**Reversión.** `git revert`.

---

### Bloque 2 — P2 octubre (calidad)

#### H2.1 · Prioridad P2 · Esfuerzo M · Depende de H0.4 (leer la auditoría) · Archivos CSS de CTAs (teal `#14B5A7` / `--cyan`)

**Prompt para la IA.** Contraste WCAG AA. La auditoría (PR #4 / H0.4) midió CTA primario blanco sobre `#14B5A7` ≈ 2,56:1. Arreglo propuesto: tinta sobre el mismo teal ≈ 6,53:1, o teal más oscuro. No cambies la marca a otro hue. Estrellas `#FBBC04` sobre blanco ≈ 1,71:1: no las uses como único indicador; texto visible al lado. Un PR de color, no de copy.

**Criterio de aceptación.** Texto de CTA ≥ 4,5:1. Playwright 390 y 1440 no rompe el sticky (H1.1).

**Verificación (comando).**

```bash
# Contraste del color computado del botón primario (local Playwright o script de luminancia).
# No debe quedar color:#fff sobre background:#14B5A7 en .btn / .cta-btn / .mobile-sticky-main
rg -n 'color:#fff|color:\s*#fff' public/css/shell.css public/index.html | head
```

**Reversión.** `git revert`.

#### H2.2 · Prioridad P2 · Esfuerzo M · Depende de — · Archivos `public/evaluacion.html`

**Prompt para la IA.** Accesibilidad del wizard. Hoy: `<label>` sin `for`; H1 clippeado :2120; sede-cards son `div`+`onclick`; `#btnSubmit` parece WhatsApp (`.wa-btn` + SVG) pero envía el form. Asociá labels, `button`/`fieldset` en sedes y slots, foco visible, `aria-expanded` donde haya pasos, no uses el H1 clip como única heading visible. No cambies precio ni MercadoPago. No dispares `whatsapp_click` en `#btnSubmit`.

**Criterio de aceptación.** Labels asociados. Sedes operables por teclado. Lighthouse a11y del form sin errores críticos. Mismo payload n8n.

**Verificación (comando).**

```bash
rg -n '<label' public/evaluacion.html | head
rg -n 'for="inputNombre"|id="inputNombre"' public/evaluacion.html
rg -n 'hebeTrack\(.whatsapp_click' public/evaluacion.html && echo FAIL || echo 'no WA track on wizard'
curl -sI https://www.metodohebe.cl/evaluacion | head -3   # 200
```

**Reversión.** `git revert`.

#### H2.3 · Prioridad P2 · Esfuerzo S · Depende de R1 · Archivos `public/planes/index.html` (y fichas de precio que R1 nombre)

**Prompt para la IA.** **Sin R1 no hagas este PR.** Si R1 entrega monto, número de cuotas y letra chica, mostrá la cuota mensual **bajo** el precio actual, no en el hero. `/planes` FAQ ya dice que las cuotas se informan en P3: no contradigas a R1. No inventes CAF ni “desde $X”.

**Criterio de aceptación.** Cuota visible solo con cifras de R1. FAQ y schema `Offer` coinciden con el visible.

**Verificación (comando).**

```bash
rg -n 'cuota' public/planes/index.html
# JSON-LD Offer price == texto visible (no automatizable del todo: revisar a mano)
```

**Reversión.** `git revert`.

#### H2.4 · Prioridad P2 · Esfuerzo M · Depende de — · Archivos páginas con `<img>` LCP/galería; `public/video/*.webm`

**Prompt para la IA.** Extender `<picture>` AVIF/WebP+JPG (ya hay 8 páginas y 10 pares en `img/blog/` según la auditoría). `width`/`height` obligatorios (B23). `loading="lazy"` bajo el fold; nunca en LCP. Borrá los 4 webm huérfanos (`public/video/plan-celulitis.webm`, `plan-flacidez.webm`, `plan-trifasico.webm`, `plan-grasa.webm`: **cero** referencias en el repo). No toques el markup de galería de `/resultados` salvo para envolver en `<picture>` si aún falta.

**Criterio de aceptación.** Los 4 webm no existen. Páginas de pilar con LCP en `<picture>`. CLS sin regresión.

**Verificación (comando).**

```bash
ls public/video/*.webm 2>/dev/null && echo FAIL || echo 'no orphan webm'
rg -n '<picture' public/criolipolisis/index.html public/index.html public/resultados/index.html
```

**Reversión.** `git revert` (restaurará los webm).

---

### Bloque 3 — P2 `/criolipolisis` híbrido Fase 2

**Prerrequisitos (todos):** Bloque 1 en `main` · ≥7 días post-H1.1 · R5 (baseline Search Console 6 meses, móvil/desktop) escrito.  
**Un PR por sub-bloque.** Máximo 5 puntos de conversión dentro del `<article>` (B.4.5). Insertar, jamás reemplazar (B20). Citas B6 intactas. Reusar galería de `public/resultados/index.html` (`.zone-gallery`, `<picture>`). Fechas con `scripts/schema_dates.py`.

| ID | Prioridad | Esfuerzo | Depende de | Archivos | Prompt para la IA | Criterio de aceptación | Verificación (comando) | Reversión |
|---|---|---|---|---|---|---|---|---|
| H3.1 | P2 | S | Bloque 1 + 7d H1.1 + R5 | `public/criolipolisis/index.html` | Chips en el hero (propuesta bloque 04). No tocar H1 (B3). | Chips visibles; word count no baja; ≤5 CTAs artículo | `rg -n 'chip\|hero' public/criolipolisis/index.html`; word count ≥ 3671 | `git revert` |
| H3.2 | P2 | S | H3.1 o paralelo si no comparte hunks | idem | Banda de autoevaluación (bloque 07). No es el 6º CTA: cuenta contra B.4.5. | Autoevalúa; no popup; evento `hebeTrack` ≠ Lead | contar `.inline-cta`+bandas ≤5 | `git revert` |
| H3.3 | P2 | S | — (imágenes) | idem + `public/img/sesion-criolipolisis-hiems.webp` (existe en `main`) | Figura con `width`/`height` (bloque 09). No inventes otra foto. | `width`/`height` + lazy; 200 | `test -e public/img/sesion-criolipolisis-hiems.webp`; `curl -sI` 200 | `git revert` |
| H3.4 | P2 | S | H3.1 | idem | CTA contextual de zonas (bloque 11). Cuenta como punto de conversión. | Destino `/evaluacion`; `evaluacion_click` no `whatsapp_click` | `rg -n 'evaluacion_click' public/criolipolisis/index.html` | `git revert` |
| H3.5 | P2 | M | H3.3 | idem + markup `public/resultados/index.html` | Galería antes/después: **reusar** `.zone-gallery` / `<picture>` / observer. Sin cm inventados. | Mismas fotos ya públicas en `/resultados`; alt honestos | `rg -n 'zone-gallery\|resultado-' public/criolipolisis/index.html` | `git revert` |
| H3.6 | P2 | S | — | idem + `/planes` | Tarjeta Plan Zero Rollito (bloque 16). Precio = el de `/planes`. | Un `Offer` que coincide con el visible | `rg -n 'Zero Rollito\|1.799' public/criolipolisis/index.html public/planes/index.html` | `git revert` |
| H3.7 | P2 | S | R3 si cita rating | idem | Micro-bloque de confianza (bloque 19). Sin AggregateRating. | Texto sin estrellas schema | `rg AggregateRating public/criolipolisis/index.html` vacío | `git revert` |
| H3.8 | P2 | S | H1.10 | idem | Tarjetas de sede (bloque 21). 3 sedes reales + Concepción solo si H1.10. | Direcciones = las ya publicadas | `rg -n 'Vitacura\|Concón\|Los Ángeles' public/criolipolisis/index.html` | `git revert` |
| H3.9 | P2 | S | H1.7 | idem | Bloque enlaces relacionados (bloque 25). Suma, no quita B11. | Links a `/resultados`, `/seguridad-criolipolisis`, cluster | `rg -n 'href="/' public/criolipolisis/index.html` | `git revert` |
| H3.10 | P2 | S | — | idem | 2 FAQ nuevas, visible + schema (B9). | 11 Question visibles = 11 schema | `python3` contar FAQPage vs `.faq-item` | `git revert` |
| H3.11 | P2 | S | — | idem | Ajuste de copy del `<p>` del `.inline-cta` (bloque 14). No el H3 (B4). | Solo el párrafo; tracking igual | `git diff -U3` acotado a ese `<p>` | `git revert` |
| H3.12 | P2 | M | H3.3–H3.6 | idem | Schema extra: `Service`+`Offer`, `ImageObject`, FAQ ampliado (F.1–F.3, F.6). `MedicalBusiness` ya existe: no dupliques `@id`. Fechas vía `schema_dates.py`. | Parse 0 fails; un `@id` por nodo; Offer = precio visible | comando JSON-LD del §2 + Rich Results a mano | `git revert` + recrawl |

Tras H3.5+H3.6: medir 7 días antes del resto (propuesta Fase 2).

---

### Bloque 4 — P3 AUGE Fase 3 (solo si R4)

Prerrequisitos: Fase 0/1 (H1.1, H1.7, H1.9) + **R4** (KPI y go/no-go). Riesgo de tono (propuesta I.2): 2 de 3 rutas del triage **no venden**. Pregunta de merge: *¿un periodista de BBCL enlazaría esta página?* Si no, no merges. Un PR por sub-bloque. Monitoreo 8 semanas, no 4.

| ID | Prioridad | Esfuerzo | Depende de | Archivos | Prompt para la IA | Criterio de aceptación | Verificación (comando) | Reversión |
|---|---|---|---|---|---|---|---|---|
| H4.1 | P3 | S | R4 | `public/guatita-de-delantal-auge-y-ley/index.html` | Chips de credibilidad hero (3.1). No tocar H1. | Chips; B3 intacto | `rg -n '<h1' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.2 | P3 | S | R4 | idem | Índice + `id` en H2 existentes (3.2). No reescribir H2 (B4). | `id` en cada H2 actual | `rg -n '<h2' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.3 | P3 | M | R4 | idem | Tabla AUGE/GES vs Ley 21.438 (3.3). Solo hechos de `bcn.cl`. | B7/B10 intactos | `rg -n 'bcn.cl\|GES\|21.438' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.4 | P3 | S | R4 | idem | Bloque puente honesto (3.4). No vende cirugía ni P3 como “equivalente”. | Fila honesta visible | lectura humana BBCL | `git revert` |
| H4.5 | P3 | M | R4 | idem | Auto-triage 3 rutas (3.5). 2/3 no comerciales. Eventos G.3. | 2 rutas → PAD / ejercicios; 1 → `/evaluacion` | `rg -n 'triage_click\|evaluacion_click' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.6 | P3 | M | H4.5 | idem | Tabla rutas costo/tiempo/recuperación (E.3.2). Fila «resuelve piel colgante: No» obligatoria. | Esa fila existe | `rg -n 'piel colgante' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.7 | P3 | S | R4 | idem | 3 FAQ nuevas visible+schema (3.7, B9). | Conteos iguales | script FAQ vs `.faq-item` | `git revert` |
| H4.8 | P3 | S | H1.7 | idem | «Sigue leyendo» del cluster (3.8). | Links cluster | `rg -n 'bono-pad\|fonasa-isapre\|ejercicios-para-guatita' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.9 | P3 | S | R4 | idem | Copy `.inline-cta` / `.cta-banner` (3.9) sin mentir gratuidad P3. | $27.990 si menciona P3 | `rg -n '27.990\|sin costo' public/guatita-de-delantal-auge-y-ley/index.html` | `git revert` |
| H4.10 | P3 | M | H4.2, H4.5 | idem | Schema `HowTo` + FAQ ampliado (3.10). HowTo = pasos **visibles**. No `AggregateRating`. Fechas `schema_dates.py`. | Parse OK; HowTo espeja el ol visible | JSON-LD §2 + Rich Results | `git revert` |
| H4.11 | P3 | M | R4 + R2/n8n | idem + endpoint | Checklist descargable (3.11 / G.4). `fuente: 'Checklist Ley 21.438'`. **Nunca** `Lead` Meta. Diferible. | Pipeline distinto a P3 | no `fbq('track','Lead')` en el checklist | `git revert` |

---

### Bloque 5 — P2/P3 contenidos y housekeeping

#### H5.1 · Prioridad P2 · Esfuerzo M · Depende de — · Archivos `public/blog/*` (8 artículos + index)

**Prompt para la IA.** Refresh de blog: `dateModified` real (contenido tocado, no solo la fecha), frase de entidad donde falte, enlaces a pilares (celulitis → `/como-quitar-la-celulitis-de-las-piernas-y-gluteos-rapido`, ya hay clúster). No reescribas H1. Un PR por artículo si el diff es grande; si es solo frescura + 1 enlace, podés agrupar **un** clúster temático, no los 8.

**Criterio de aceptación.** Cada artículo tocado tiene cambio de copy verificable + `dateModified` via `schema_dates.py`.

**Verificación (comando).**

```bash
rg -n 'dateModified' public/blog --glob '*.html'
python3 - <<'PY'
import json,re
from pathlib import Path
fails=0
for p in Path('public/blog').rglob('*.html'):
  for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', p.read_text(), re.S):
    try: json.loads(b)
    except Exception as e:
      fails+=1; print(p,e)
print('fails',fails)
PY
```

**Reversión.** `git revert`.

#### H5.2 · Prioridad P2 · Esfuerzo L · Depende de R2 (si hay data) / Ricardo para el PDF · Archivos nuevo asset + landing (paths a crear)

**Prompt para la IA.** Activos de `docs/LINK_BUILDING_PLAN_2026.md` Tier 3. **No inventes** la «Radiografía Corporal Chile 2026» con cm ni tablas de 30.000 pacientes sin R3/R2. Lo ejecutable sin data nueva: infografía/guía visual con hechos ya publicados, o la estructura de la calculadora **sin** diagnóstico médico. Pitcheo de prensa (Tier 1) es R12, no este PR. Nunca comprar links.

**Criterio de aceptación.** Asset linkable publicado o explícitamente bloqueado a la espera de data. Sitemap + IndexNow de la URL nueva.

**Verificación (comando).**

```bash
test "$(grep -c '<loc>' public/sitemap.xml)" -ge 62
curl -sI "https://www.metodohebe.cl/<url-nueva>" | head -3   # 200
```

**Reversión.** Quitar URL del sitemap + `git revert`.

#### H5.3 · Prioridad P2 · Esfuerzo S · Depende de — · Archivos `public/formalidad/index.html`

**Prompt para la IA.** `/formalidad` es un deck de **Protocolo Lumina** (`title` «Estándar de presentación · Protocolo Lumina», `noindex`). O bien: (a) reescribirlo como estándar Hebe (teal, copy Hebe, sin marca Lumina), o (b) 301 a `/` y sacarlo de circulación. Está **200** hoy. Elegí (a) o (b) en el PR; no dejes un deck Lumina en este dominio.

**Criterio de aceptación.** Cero «Protocolo Lumina» en `public/formalidad`. O 301 + `curl` 301.

**Verificación (comando).**

```bash
rg -n 'Protocolo Lumina|Lumina' public/formalidad/index.html && echo FAIL || echo clean
curl -sI https://www.metodohebe.cl/formalidad | head -5
```

**Reversión.** `git revert`.

#### H5.4 · Prioridad P3 · Esfuerzo S · Depende de — · Archivos `public/ab767007d40e7700a59b91b6f690a54f.txt`, `public/f0e1ff44b0ff128d2711bf78b0aa90b9.txt`, `public/robots.txt` si apunta

**Prompt para la IA.** Dos claves IndexNow viven y dan **200**. La vigente del changelog es `f0e1ff44b0ff128d2711bf78b0aa90b9`. Confirmá en Bing/IndexNow cuál está registrada. La otra es huérfana: borrala solo si ningún ping la usa. No toques `vercel.json` salvo header de `text/plain`.

**Criterio de aceptación.** Una sola clave referenciada en docs de ping. La huérfana o se documenta o se elimina.

**Verificación (comando).**

```bash
curl -sI https://www.metodohebe.cl/f0e1ff44b0ff128d2711bf78b0aa90b9.txt | head -3   # 200
curl -sI https://www.metodohebe.cl/ab767007d40e7700a59b91b6f690a54f.txt | head -3
rg -n 'ab767007|f0e1ff44' docs public/robots.txt docs/AEO_CHANGELOG_2026-09.md
```

**Reversión.** Restaurar el `.txt`.

---

### Bloque 6 — Transversal medición (R2, n8n)

No es código de landing. No asumas dashboards ni webhooks que Ricardo no haya dado (R2).

#### T6.1 · Prioridad P1 · Esfuerzo S · Depende de R2 · Archivos — (GA4 / GTM; opcional nota en `CHANGES.md`)

**Prompt para la IA.** Con acceso R2: inventario de eventos reales (`evaluacion_click`, `whatsapp_click`, `Lead`, `scroll_depth`, `franquicia_*`, `contacto_whatsapp_2026`). Marcá cuáles están duplicados o mal tipados (H1.8). No crees eventos nuevos aquí salvo que R2 lo pida. No toques el mapa B15.

**Criterio de aceptación.** Tabla evento → disparador → destino (GA4/Meta/n8n) pegada en el PR. Cero cambios de sitio si no hace falta.

**Verificación (comando).**

```bash
rg -n "hebeTrack\(|fbq\('track'" public/evaluacion.html public/index.html | head
```

**Reversión.** N/A si solo docs; si tocaste GTM, revertir el contenedor (fuera de git — R2).

#### T6.2 · Prioridad P2 · Esfuerzo M · Depende de R2 · Archivos n8n (fuera de repo) + comentarios en `public/evaluacion.html` / `public/franquicia/index.html`

**Prompt para la IA.** Verificar webhooks: `lead-capture`, `link-pago-evaluacion`, `franquicia-lead` (este último aún `[REDACTED]` + TODO en `/franquicia` :1243). No pegues URLs secretas en el PR. Confirmá que `fuente: 'Landing Evaluación P3'` no se mezcla con franquicia. Sin R2/R11 no “completes” el webhook.

**Criterio de aceptación.** Lead de prueba (datos fake) llega o se documenta el fallo. Franquicia fallback `mailto` sigue si n8n no existe.

**Verificación (comando).**

```bash
rg -n 'webhook/lead-capture|webhook/franquicia-lead|mailto:contacto@metodohebe.cl' public/evaluacion.html public/franquicia/index.html
```

**Reversión.** No dejes un webhook de producción apuntando a un test.

#### T6.3 · Prioridad P2 · Esfuerzo S · Depende de R2 + R12 · Archivos `docs/SHARE_OF_MODEL_MES0.md`

**Prompt para la IA.** No “midás” Share of Model vos: es cuenta humana (ChatGPT/Perplexity/Gemini, VPN Chile). Este ID solo: dejar la tabla mes 0 lista para que Ricardo la llene, y el recordatorio de **mes 3 en diciembre 2026** (mismas 15 preguntas). No inventes filas sí/no.

**Criterio de aceptación.** Tabla vacía con columnas fecha / modelo / marca / URL / competidor. Cero respuestas inventadas.

**Verificación (comando).**

```bash
test -e docs/SHARE_OF_MODEL_MES0.md
wc -l docs/SHARE_OF_MODEL_MES0.md
```

**Reversión.** Revertir solo el md.

---

## 4. Solo Ricardo

La IA **no asume** estas decisiones ni crea cuentas. Si un ID `H*`/`T*` depende de un `R*` sin nota escrita (comentario de PR, issue o mensaje), se detiene.

| ID | Decisión / cuenta | Bloquea |
|---|---|---|
| R1 | Autorizar cuota mensual visible: monto, nº de cuotas, letra chica, dónde. | H2.3 |
| R2 | Acceso GA4/GTM/n8n y qué se considera “medido”. Sin R2 no hay baseline inventado ni workflows nuevos. | T6.1 T6.2 T6.3; H4.11 |
| R3 | Cifra oficial de reseñas/rating (GBP) y de pacientes (20.000 vs 30.000). Visible vs schema. | H1.5 H1.6 H3.7 H5.2 |
| R4 | KPI y go/no-go de Fase 3 AUGE (propuesta 0.7 / E.5). | Bloque 4 entero |
| R5 | Export Search Console 6 meses, móvil/desktop, de `/criolipolisis` (y AUGE si pide). | Bloque 3 |
| R6 | Nombres, fotos y registros Superintendencia del equipo clínico. Sin R6 no se inventan fichas en `/equipo`. | extras de `/equipo` |
| R7 | Sí/no al catálogo de equipos del PR #51 (nombres en máquina vs copy). | H0.3 merge |
| R8 | INAPI: cuándo quitar `noindex` de `/franquicia`. | indexar franquicia |
| R9 | Concepción: si hay apertura, fecha, dirección, Maps. Si no hay, el copy es el de H1.10. | cualquier sede Concepción |
| R10 | URL pública de reserva Clinera (`URL_RESERVA_HEBE`). Hoy no existe (`docs/PROMPTS_PENDIENTES_PUENTE_CLINERA.md`). | reemplazar `/evaluacion` en `/clinica/*` |
| R11 | Crear y apuntar el webhook `franquicia-lead` en n8n. | T6.2 cierre |
| R12 | Off-site: bios RRSS, GBP Q&A, Doctoralia, Wikidata, GSC `hebebeauty.cl`, pitcheo prensa, llenar Share of Model mes 0 y mes 3 (diciembre). | T6.3; `docs/AEO_OFFSITE_CHECKLIST.md` |

---

## 5. Checklist post-deploy (después de cada merge)

Correr en las URLs que el PR tocó, no en las 62 por costumbre.

1. `curl -sI https://www.metodohebe.cl/<path>` → 200 (o 301/308 si el cambio era redirect). Seguí `location` una vez.
2. Ping IndexNow (clave vigente):

```bash
curl -sS https://api.indexnow.org/indexnow -H 'Content-Type: application/json' \
  -d '{"host":"www.metodohebe.cl","key":"f0e1ff44b0ff128d2711bf78b0aa90b9","keyLocation":"https://www.metodohebe.cl/f0e1ff44b0ff128d2711bf78b0aa90b9.txt","urlList":["https://www.metodohebe.cl/<url-tocada>"]}'
```

3. `grep -c '<loc>' public/sitemap.xml` — hoy **62**. Si creaste URL, el conteo sube y la `<loc>` usa `https://www.metodohebe.cl/...` sin slash.
4. JSON-LD: comando de parse del §2 → `fails 0`. Un `@id` por nodo en cada página tocada.
5. Playwright **390 px**: sticky (si H1.1+), CLS al cargar imágenes nuevas (`width`/`height`), CTA no cubre el hero (B.4).

---

## 6. Calendario y ventana de evaluación

No se juzga SEO antes de **30 días** (propuesta H.6). Share of Model **mes 3 = diciembre 2026** (mes 0: 3-sep-2026, `docs/SHARE_OF_MODEL_MES0.md`).

### Ventanas T+

| Momento | Qué se mira | Qué se decide |
|---|---|---|
| T+0 | Línea base (R5, T6.1) | No deployar Fase 2/3 sin esto |
| T+7 | Indexación, schema, CWV, clics a `/evaluacion` | Rollback si cae indexación o schema |
| T+14 | Posición/CTR, primeros leads con `pagina_origen` | Ajustes de copy |
| T+30 | Primera evaluación real | Seguir / revertir |
| T+60 | Tendencia y calidad de lead | Escalar patrón o revertir |
| T+90 | Consolidación + Ángulo A de links (R12) | Decisión estratégica |

### Calendario 15-sep → 15-dic (Hebe + Transversal)

| Ventana | Fechas | Hebe | Transversal |
|---|---|---|---|
| P0 esta semana | 15–21 sep 2026 | H0.1 reaplica `knowsAbout` y cierra #37 · H0.2 cierra #43 · H0.3 pre-review #51 (merge solo R7) · H0.4 rescata auditoría · H0.5 `CLAUDE.md` · H0.6 ya está | — |
| P1 septiembre | 15–30 sep 2026 | H1.1 sticky B.4 **solo** + medir 7 d · H1.2 og/404s · H1.3 higiene URL · H1.4 `@id` · H1.5 schema reviews (R3) · H1.6 residuos P3 (R3 cifras) · H1.7 enlaces Fase 1 · H1.8 tracking · H1.9 Ley 21.438 · H1.10 Concepción/Maps/Clinera | T6.1 inventario eventos si R2 |
| P2 octubre | 1–31 oct 2026 | H2.1 contraste · H2.2 a11y `/evaluacion` · H2.4 `<picture>` + borrar webm · H5.1 blog (por clúster) · H5.3 `/formalidad` · inicio H3 si prereqs | T6.2 n8n (R2/R11) · T6.3 plantilla SoM |
| P2 noviembre | 1–30 nov 2026 | H3.x un PR por sub-bloque si R5 + 7 d post-H1.1 · H5.2 asset linkable (sin inventar data) · H5.4 clave IndexNow | Off-site R12 (no es código) |
| P3 condicional | oct–dic 2026 | H2.3 cuotas **si R1** · H4.x AUGE **si R4** · extras `/equipo` **si R6** · index `/franquicia` **si R8** | — |
| SoM mes 3 | diciembre 2026 (≈ 3-dic) | No hay deploy de “SoM” | R12 + T6.3: mismas 15 preguntas, VPN Chile |
| Cierre horizonte | 15 dic 2026 | T+90 de H1.1 / H3 | Lectura estratégica, no más Fase 2/3 nueva |

Fin del roadmap. La IA ejecutora toma **un** ID y abre **un** PR.
