# Método Hebe — instrucciones para la IA

Repo estático de `metodohebe.cl`. `public/` es el output que despliega Vercel (`outputDirectory: public` en `vercel.json`). No hay build de framework. Una tarea del roadmap = una rama = un PR a `main`.

## Qué leer primero

1. `docs/ROADMAP_IA_2026-09.md` — el ID asignado + §1 (intocables) + §4 (decisiones `R*`).
2. Este archivo.
3. `docs/PROPUESTA_LANDING_CRIOLIPOLISIS_Y_AUGE.md` §B (B1–B15, B.4) si tocás `/criolipolisis` o `/guatita-de-delantal-auge-y-ley`.
4. El path que nombra la fila del roadmap. Verificá con `test -e` antes de editar.

No copies políticas de Protocolo Lumina (`lumina-web`). Este documento es autónomo.

## Contrato

- **Una tarea = un PR.** Un deploy = un cambio medible. No mezcles IDs.
- Copy: **español de Chile, sin voseo.** Tratá de usted/tú según el tono ya publicado en esa página.
- **No inventes** registros de Superintendencia, centímetros de pacientes, reseñas, direcciones ni fechas de apertura. Cifras de prueba social (R3): **más de 30.000 pacientes** y **5/5 estrellas en Google**, en texto visible.
- **Nunca** `AggregateRating` ni `Review` oculto (`display:none` en `reviewRating`).
- JSON-LD parseable (`json.loads`). **Un nodo completo por `@id` por página.** Referenciar un `@id` de otra página está bien; redefinirlo no.
- Fechas de schema: `scripts/schema_dates.py` / `public/js/format-schema-date.js`. Offset `America/Santiago`.
- No toques HTML/CSS/JS/`vercel.json` si la tarea es de docs. No toques docs ajenos si la tarea es de código, salvo un renglón en `CHANGES.md` cuando el cambio es de producto.

## /evaluacion: breve, sin scroll

El wizard de `/evaluacion` existe para que la paciente deje sus datos sin hacer scroll. **Nunca extiendas el largo vertical de la página ni de sus pasos.** Vale para cualquier cambio de UX/UI, SEO o AEO.

- Nada de bloques nuevos dentro, entre o debajo de los pasos: FAQ, testimonios, texto SEO/AEO, banners, carruseles ni secciones de confianza.
- El contenido nuevo va en otra página (`/preguntas-frecuentes`, `/clinica/*`, fichas de sede) y se enlaza desde allá, no desde el wizard.
- `/evaluacion` no lleva `FAQPage`. Las preguntas de agendamiento viven en `/preguntas-frecuentes`.
- Un paso o un campo nuevo en el formulario necesita aprobación explícita de Ricardo.
- Antes de abrir un PR que toque `/evaluacion`, compara en 375x667 contra `main`: ningún paso puede quedar más alto.

## B15 / Lead

`window.hebeTrack` mapea Meta `{'whatsapp_click':'Contact'}`. Los CTA **no** disparan `Lead`. El único `Lead` legítimo es el submit del wizard en `public/evaluacion.html`.

## Sticky B.4

1. Alto ≤ 15 % del viewport (~100 px en 667 px).
2. No aparece antes de `scrollY > 400` (AUGE: `> 800`).
3. Se oculta al llegar al footer (`IntersectionObserver`).
4. Cero pop-ups, modales, exit-intent u overlays de pantalla completa.
5. Máximo 5 puntos de conversión dentro del `<article>`.
6. `body { padding-bottom }` en CSS inicial (no inyectado por JS).

No reintroduzcas `transform:translateY(100%)` global en `public/css/shell.css` (comentario :172–186).

## Reutilizá, no reescribas

`scripts/schema_dates.py`, `public/js/format-schema-date.js`, `hebeAttr`/`hebeTrack` en `public/evaluacion.html`, galería en `public/resultados/index.html`.

## Comandos de línea base

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
test "$(grep -c '<loc>' public/sitemap.xml)" -eq 64 && echo 'sitemap loc=64 OK'
```

No implementes H1–H5 desde este archivo. Tomá un ID del roadmap y abrí un PR.
