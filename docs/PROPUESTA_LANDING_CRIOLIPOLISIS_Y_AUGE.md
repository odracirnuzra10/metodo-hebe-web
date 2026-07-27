# Propuesta: convertir `/criolipolisis` y `/guatita-de-delantal-auge-y-ley` en páginas híbridas artículo + landing

**Fecha:** 2026-07-27
**Autor:** auditoría técnica SEO + CRO
**Estado:** propuesta. **No se modificó ningún HTML.** El único archivo escrito es este documento.
**Alcance:** `public/criolipolisis/index.html` (786 líneas, 69 KB) y `public/guatita-de-delantal-auge-y-ley/index.html` (618 líneas, 51 KB).

---

## 0. Nota sobre datos de Semrush (léela antes de creerle a cualquier número)

Se intentó consultar Semrush MCP tres veces, con tres herramientas distintas:

| Herramienta | Resultado |
|---|---|
| `url_research` | Falla: el plan Semrush de la cuenta **no incluye acceso MCP** |
| `organic_research` | Falla: mismo motivo |
| `keyword_research` | Falla: mismo motivo |

**Consecuencia: en este documento no hay ni un solo dato de volumen de búsqueda, posición ni CTR proveniente de Semrush.** Para habilitarlo hay que revisar los planes disponibles en `https://www.semrush.com/mcp-access`.

Tampoco existe en el repo ningún export de Search Console, CSV ni JSON de datos SEO (se verificó con `find`).

Por lo tanto, toda afirmación sobre "por qué keywords rankean" en este documento es **deducción a partir del código fuente** (`<title>`, `meta description`, `meta keywords`, encabezados, copy y `sitemap.xml`), y está marcada como tal con la etiqueta **[DEDUCCIÓN]**. Los datos estructurales (conteos de palabras, líneas, presencia de tags, orden del DOM) sí son **[VERIFICADO]** contra el archivo.

**Antes de ejecutar la Fase 2 de esta propuesta hay que traer los datos reales de Search Console** (consultas, impresiones, CTR y posición media por URL, últimos 6 meses, segmentado móvil/desktop). Sin eso, el plan de copy de encabezados va a ciegas.

---

# A. Diagnóstico

## A.1 `/criolipolisis` — estructura actual

### Head y metadatos [VERIFICADO]

| Elemento | Valor | Línea |
|---|---|---|
| `<title>` | `Criolipólisis en Chile: Qué Es, Precio, Resultados y Contraindicaciones \| Método Hebe` | `public/criolipolisis/index.html:42` |
| `meta description` | "Criolipólisis en Chile: cómo funciona, precio real, resultados antes y después, zonas tratables y contraindicaciones. Guía clínica del Método Hebe (Vitacura, Concón, Los Ángeles)." | `:43` |
| `meta keywords` | `criolipolisis, criolipolisis chile, criolipolisis precio, criolipolisis funciona, criolipolisis antes y despues, criolipolisis papada, coolsculpting chile` | `:44` |
| `robots` | `index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1` | `:46` |
| `canonical` | `https://www.metodohebe.cl/criolipolisis` (sin slash — consistente con `trailingSlash:false`) | `:47` |
| Open Graph | `og:title`, `og:description`, `og:type=article`, `og:url`, `og:site_name`, `og:locale=es_CL`, `article:published_time`, `article:modified_time`, `article:section`, 4× `article:tag` | `:50-62` |
| **`og:image`** | **NO EXISTE** | — |
| Twitter | `twitter:card=summary_large_image`, `twitter:title`, `twitter:description` | `:65-67` |
| **`twitter:image`** | **NO EXISTE** | — |
| hreflang | `es-CL`, `es`, `x-default` → todos a la misma URL | `:70-72` |

> ⚠️ **Inconsistencia real:** `og:url` es `.../criolipolisis/` **con** slash (`:53`) mientras el canonical es **sin** slash (`:47`). No es fatal (el canonical manda), pero es ruido. Mismo patrón en el JSON-LD, que usa `https://metodohebe.cl/criolipolisis/` (con slash y sin `www`) en `@id`, `url` y `mainEntityOfPage` (`:87`, `:89`, `:111`, `:117`).

> ⚠️ **`twitter:card` declarado como `summary_large_image` sin ninguna imagen.** El resultado en X/LinkedIn/WhatsApp es una tarjeta rota o degradada a texto plano. Es una pérdida directa de CTR en compartidos y en previews de asistentes de IA.

### Jerarquía de encabezados [VERIFICADO]

```
H1 (:446)  Criolipólisis: qué es, cómo funciona y cuándo realmente elimina grasa
  H2 (:473)  ¿Qué es la criolipólisis?
  H2 (:481)  ¿Cómo funciona paso a paso?
  H2 (:496)  Zonas tratables
    H3 (:500)  Abdomen y flancos
    H3 (:504)  Brazos
    H3 (:508)  Papada (criolipólisis papada)
    H3 (:512)  Muslos y cartucheras
    H3 (:516)  Espalda (rollitos del sostén)
  H2 (:522)  Criolipólisis antes y después: qué resultados esperar
    H3 (:533)  ¿Tu caso es candidato a criolipólisis?      ← H3 dentro del bloque .inline-cta
  H2 (:547)  ¿Cuánto cuesta la criolipólisis en Chile?
  H2 (:555)  ¿Es efectiva? Evidencia clínica
  H2 (:567)  Contraindicaciones y riesgos reales
  H2 (:589)  Criolipólisis vs otras técnicas
  H2 (:616)  Criolipólisis en el Método Hebe
  H2 (:624)  Preguntas frecuentes
H2 (:678)  Evaluación diagnóstica antes de tratar          ← fuera del <article>, en .cta-banner
```

La jerarquía es limpia y sin saltos. El único H3 "impuro" es el del CTA intercalado (`:533`), que es aceptable.

### JSON-LD presente [VERIFICADO]

Un único bloque `application/ld+json` (`:81-199`) con `@graph` de **3 nodos**:

1. **`MedicalWebPage`** (`:86-112`) — `@id`, `name`, `url`, `description`, `datePublished` y `dateModified` ambos `2026-04-23`, `inLanguage: es-CL`, `about` → `MedicalProcedure` ("Criolipólisis", `procedureType: Noninvasive`, `bodyLocation`, `howPerformed`), `publisher` y `author` → `Organization` "Método Hebe", `mainEntityOfPage`.
2. **`BreadcrumbList`** (`:114-119`) — 2 niveles: Inicio → Criolipólisis.
3. **`FAQPage`** (`:121-196`) — **9 `Question`**, con texto idéntico al acordeón visible del cuerpo (`:626-669`). Correcto: el schema FAQ refleja contenido visible.

**Ausentes:** `Article`/`MedicalWebPage.speakable`, `Service`, `Offer`, `MedicalBusiness`/`LocalBusiness`, `ImageObject`, `Person` (autor), `aggregateRating`.

**El `author` es una `Organization`, no una persona.** Para una página médico-estética YMYL eso es un techo de E-E-A-T.

### Volumen de contenido [VERIFICADO]

| Métrica | Valor |
|---|---|
| Palabras dentro de `<article class="article-body">` (`:466-672`) | **3.671** |
| Palabras **antes** del primer CTA intercalado (`:466-531`) | **1.476** (= 40% del artículo) |
| Palabras entre el primer CTA y el banner final (`:532-673`) | 2.195 |
| Imágenes en el cuerpo del artículo | **0** (los únicos 3 `<img>` son el logo en nav `:417`, el logo en footer `:704` y el pixel `noscript` de Meta `:38`) |

### Intención por sección [DEDUCCIÓN a partir del copy]

| Sección | Keyword/intención que ataca | Tipo de intención |
|---|---|---|
| H1 + answer capsule (`:469`) | `criolipolisis`, `criolipolisis qué es` | Informacional |
| ¿Qué es? (`:473`) | `criolipolisis que es`, `coolsculpting` | Informacional |
| ¿Cómo funciona paso a paso? (`:481`) | `criolipolisis como funciona`, `duele` | Informacional |
| Zonas tratables + 5 H3 (`:496-518`) | `criolipolisis abdomen`, `criolipolisis papada`, `criolipolisis brazos`, `cartucheras`, `rollitos del sostén` | Informacional-comercial (long tail por zona) |
| Antes y después (`:522`) | `criolipolisis antes y despues`, `criolipolisis resultados`, `cuantos centimetros` | **Comercial (investigación)** |
| **¿Cuánto cuesta? (`:547`)** | **`criolipolisis precio`, `criolipolisis precio chile`, `cuanto cuesta la criolipolisis`** | **Comercial-transaccional — la sección de mayor valor** |
| ¿Es efectiva? Evidencia (`:555`) | `criolipolisis funciona`, `criolipolisis sirve` | Informacional (alta desconfianza) |
| Contraindicaciones y riesgos (`:567`) | `criolipolisis contraindicaciones`, `hiperplasia adiposa paradojica`, `criolipolisis embarazo` | Informacional (miedo/objeción) |
| Criolipólisis vs otras técnicas (`:589`) | `criolipolisis vs cavitacion`, `vs hifu`, `vs lipo` | **Comercial (comparación)** |
| Criolipólisis en el Método Hebe (`:616`) | `criolipolisis santiago/vitacura/concón`, marca | **Transaccional** |
| FAQ (`:624`) | Consultas long tail + People Also Ask | Mixta |

**[DEDUCCIÓN] Lectura estratégica:** esta página ya es comercial. El `meta keywords` declara explícitamente `criolipolisis precio` y `criolipolisis antes y despues`; el cuerpo tiene una sección de precios con rango de mercado y el precio real de Método Hebe ($1.799.990, `:553`), y una tabla comparativa con costos por técnica (`:593-610`). Convertirla en híbrido artículo+landing **no es un cambio de intención**, es alinear la página con la intención que ya sirve. Riesgo SEO estructuralmente bajo.

### Enlaces internos salientes desde el cuerpo [VERIFICADO]

| Destino | Línea | Anchor |
|---|---|---|
| `/planes` | `:553` | "Plan Zero Rollito" |
| `/el-metodo` | `:565` | "Método Hebe" |
| `/evaluacion` | `:587` | "evaluación clínica previa" |
| `/lipoescultura-sin-cirugia` | `:614` | "lipoescultura sin cirugía en Chile" |
| `/planes` | `:622` | "planes y precios" |

Más los del nav (`:420-424`: `/`, `/el-metodo`, `/planes`, `/resultados`, `/blog`) y los del footer (`:713-741`).

**Observación:** el cuerpo **no enlaza a `/resultados`**, que es exactamente la página que contiene las fotos antes/después. La sección "Criolipólisis antes y después" (`:522`) promete resultados y no enlaza a la galería. Es una fuga obvia, tanto de link equity interno como de conversión.

### Inventario de CTAs y su posición en el scroll [VERIFICADO]

| # | CTA | Línea | Destino | Tracking | Visible en móvil |
|---|---|---|---|---|---|
| 1 | Teléfono en topbar | `:407` | `tel:+56963222683` | `hebeTrack('phone_click',{location:'topbar'})` | **No** (`.topbar-r{display:none}` bajo 600px, `:389`) |
| 2 | "Agenda evaluación" en nav | `:427` | `/evaluacion` | `hebeTrack('evaluacion_click',{location:'nav'})` | Sí (el `.nav-r` no colapsa) |
| 3 | `.inline-cta` "¿Tu caso es candidato a criolipólisis?" | `:532-545` | `/evaluacion` + `wa.me` | `evaluacion_click` / `whatsapp_click`, `location:'inline_cta_resultados'` | Sí |
| 4 | `.cta-banner` "Evaluación diagnóstica antes de tratar" | `:675-696` | `/evaluacion` + `wa.me` | `cta_click` / `whatsapp_click`, `location:'criolipolisis_bottom'` | Sí |
| 5 | `.mobile-sticky-cta` | `:751-754` | `/evaluacion` | `cta_click`, `location:'criolipolisis_mobile_sticky'` | **NO — está roto, ver A.3** |
| 6 | tel / mail en footer | `:709` | — | ninguno | Sí |

**El primer CTA de conversión real dentro del contenido aparece tras 1.476 palabras (40% del artículo).**

**[ESTIMACIÓN, no verificada en navegador]** Modelando móvil 390 px de ancho (`--wrap: 100% - 48px` ≈ 342 px de columna), fuente 15-16 px, `line-height:1.8` ≈ 28 px/línea, ~7 palabras por línea: 1.476 palabras ≈ 210 líneas ≈ **~5.900 px de texto**, más topbar (~30 px) + nav (64 px) + breadcrumb (~45 px) + hero con H1 a 28 px (~380 px) + `<ol>` y márgenes de 5 H2/5 H3. **El primer CTA intercalado cae alrededor de los 6.500–7.000 px de scroll en móvil**, y alrededor de **3.200–3.600 px en desktop** (columna de 820 px, ~16 palabras/línea). Hay que confirmarlo midiendo en el navegador antes de citarlo como dato duro; el número verificable y no discutible es el de palabras.

### Fricción de conversión [VERIFICADO]

| Elemento | ¿Existe? | Comentario |
|---|---|---|
| Prueba social | **Casi nula** | Solo "+30.000 pacientes en Chile" en el footer (`:706`). Cero reseñas, cero estrellas, cero testimonios en el cuerpo. |
| Fotos antes/después | **No** | Aunque `/resultados` tiene 11 pares y existen `resultado-abdomen-cintura.webp`, `resultado-lateral-cintura.webp`, `resultado-contorno-corporal.webp`, etc. sin usar aquí. |
| Foto de la clínica / equipo | **No** | Existe `sesion-criolipolisis-hiems.webp` **sin usar en ninguna parte de esta página**, además de `profesional-tratamiento-abdomen.webp`, `clinica-recepcion-paciente.webp`, `tech-ized.png`. |
| E-E-A-T: autor con nombre y credenciales | **No** | `author` = `Organization`. Ningún profesional identificado. Para YMYL es la debilidad más seria. |
| Precio | Sí | `:549-553`. Rango de mercado + precio propio. Bien hecho. |
| Garantía / política | **No** | |
| Urgencia / escasez | **No** | Coherente con el tono clínico; **no recomiendo introducirla**. |
| Reversión de riesgo | Parcial | "Sin costo, sin compromiso" (`:534`, `:680`). |
| Bibliografía / citas | **Sí, excelente** | Manstein & Anderson 2008, Ingargiola 2015, Krueger 2014, Jalian 2014 (`:560-562`, `:571`). Este es probablemente el activo que más sostiene el ranking. |

---

## A.2 `/guatita-de-delantal-auge-y-ley` — estructura actual

### Head y metadatos [VERIFICADO]

| Elemento | Valor | Línea |
|---|---|---|
| `<title>` | `Ley Guatita de Delantal (Ley Saín) 2026: Cómo Postular y Requisitos \| Método Hebe` | `public/guatita-de-delantal-auge-y-ley/index.html:42` |
| `meta description` | 'Ley 21.438 "Saín" de guatita de delantal en Chile: requisitos, cómo postular, qué hacer si no calificas. Guía actualizada 2026.' | `:43` |
| `meta keywords` | `ley guatita de delantal como postular, guatita de delantal auge, operacion guatita de delantal gratis, donde postular a guatita de delantal, ley sain, ley 21438` | `:44` |
| `canonical` | `https://www.metodohebe.cl/guatita-de-delantal-auge-y-ley` | `:47` |
| Open Graph | `og:title`, `og:description`, `og:type=article`, `og:url` (con slash, `:53`), `og:site_name`, `og:locale`, tiempos, 3× `article:tag` | `:50-61` |
| **`og:image`** | **NO EXISTE** | — |
| Twitter | `summary_large_image` + title + description | `:64-66` |
| **`twitter:image`** | **NO EXISTE** | — |
| hreflang | `es-CL`, `es`, `x-default` | `:69-71` |

### Jerarquía de encabezados [VERIFICADO]

```
H1 (:384)  Ley de guatita de delantal (Ley 21.438 "Saín") en 2026: qué cubre y cómo postular
  H2 (:411)  ¿Qué es la Ley Saín / Ley 21.438?
  H2 (:419)  ¿Está dentro de AUGE/GES?
  H2 (:425)  Requisitos para postular (estado 2026)
  H2 (:442)  Cómo postular paso a paso
  H2 (:456)  Si no calificas o la espera es muy larga: alternativas
    H3 (:465)  ¿La Ley Saín no es para ti? Evaluamos alternativas reales   ← dentro de .inline-cta
  H2 (:479)  Preguntas frecuentes
H2 (:513)  ¿No calificas o la espera es larga? Evaluamos alternativas no invasivas   ← .cta-banner
```

### JSON-LD presente [VERIFICADO]

Un bloque (`:80-167`) con `@graph` de **3 nodos**:

1. **`MedicalWebPage`** (`:85-110`) — `about` → `MedicalProcedure` "Abdominoplastia post-bariátrica con cobertura Ley 21.438", `procedureType: Surgical`, `bodyLocation: Abdomen`. `author`/`publisher` = `Organization`.
2. **`BreadcrumbList`** (`:112-119`) — 4 niveles: Inicio → Blog → Guatita delantal → Ley y AUGE. Coincide con el breadcrumb visible (`:371-378`). Bien.
3. **`FAQPage`** (`:121-164`) — **5 `Question`**, espejo del acordeón visible (`:481-504`).

**Ausentes:** `Legislation`/`GovernmentService`, `HowTo` (hay un procedimiento paso a paso perfecto para ello en `:446-452`), `Service`, `Offer`, `LocalBusiness`, `Person` autor, `ImageObject`.

### Volumen de contenido [VERIFICADO]

| Métrica | Valor |
|---|---|
| Palabras dentro de `<article>` (`:404-507`) | **1.970** |
| Palabras **antes** del primer CTA intercalado (`:404-463`) | **1.460** (= **74% del artículo**) |
| Palabras después del CTA (`:464-509`) | 510 |
| Imágenes en el cuerpo | **0** |

**Este artículo es la mitad de largo que el de criolipólisis y aun así el primer punto de conversión aparece recién en el 74% del contenido.** En términos prácticos: el lector que abandona a mitad de la página —que en un artículo de trámites es la mayoría— nunca ve una oferta.

### Intención por sección [DEDUCCIÓN a partir del copy]

| Sección | Keyword/intención | Tipo |
|---|---|---|
| Answer capsule (`:407`) | disclaimer de fuentes | — |
| ¿Qué es la Ley Saín? (`:411`) | `ley sain`, `ley 21438`, `ley guatita de delantal` | **Informacional-institucional** |
| ¿Está dentro de AUGE/GES? (`:419`) | `guatita de delantal auge`, `guatita auge`, `guatita ges` | **Informacional-institucional** |
| Requisitos para postular (`:425`) | `requisitos ley guatita de delantal` | **Informacional-institucional** |
| Cómo postular paso a paso (`:442`) | `como postular guatita de delantal`, `donde postular` | **Informacional-institucional / transaccional hacia el Estado** |
| Si no calificas: alternativas (`:456`) | `guatita de delantal precio`, `operacion privada`, alternativas | **Único bloque comercial de la página** |
| FAQ (`:479`) | `operacion guatita de delantal gratis`, `lista de espera` | Informacional |

### ⛔ Advertencia estratégica: la intención de este tráfico es estructuralmente no comercial [DEDUCCIÓN]

Se pidió explícitamente verificar esto. Sin Semrush no puedo darte volúmenes, pero **la evidencia del propio código es contundente y apunta en una sola dirección**. Mira las keywords que la página declara perseguir (`:44`):

- `ley guatita de delantal como postular` → quiere hacer un trámite estatal
- `guatita de delantal auge` → quiere saber si el Estado cubre
- **`operacion guatita de delantal gratis`** → literalmente busca **gratis**
- `donde postular a guatita de delantal` → trámite
- `ley sain`, `ley 21438` → consulta normativa

**5 de 6 son informacional-institucionales, y una dice "gratis" de forma explícita.** Y la propia FAQ #1 de la página (`:125-128`) responde: "Puede serlo en el sistema público cuando la paciente cumple los requisitos...".

Hay un segundo problema, más incómodo y más importante, que es **clínico**: el perfil de este lector es paciente **post-bariátrico de FONASA con pannus abdominal y exceso de piel colgante**. El propio artículo dice, con toda razón (`:462`):

> "el tratamiento no invasivo **no reemplaza la cirugía** cuando el problema principal es el exceso de piel colgante o una diástasis grande."

Es decir: **para la mayoría del tráfico que llega a esta URL, el producto de Método Hebe no está indicado.** Empujar agresivamente el Plan Zero Flacidez ($1.977.990, `:462`) a esta audiencia sería (a) de baja conversión por capacidad de pago, (b) de baja conversión por indicación clínica, y (c) contradictorio con el párrafo que le da a la página su credibilidad y probablemente su ranking.

**Recomendación franca: NO conviertas esta página en landing de venta.** Ver sección E para la estrategia alternativa, que sí tiene sentido.

### Enlaces internos salientes desde el cuerpo [VERIFICADO]

| Destino | Línea |
|---|---|
| `https://www.bcn.cl` (externo, `rel="noopener" target="_blank"`) | `:408` |
| `https://www.fonasa.cl` (externo) | `:408` |
| `/guatita-de-delantal-operacion-vs-tratamiento` | `:460` |
| `/planes` | `:462` |
| `/que-es-la-guatita-de-delantal-y-como-puedes-solucionarlo` | `:462` |
| `/flacidez` | `:462` |
| `/ejercicios-para-guatita-de-delantal` | `:462` |

Los enlaces salientes a `bcn.cl` y `fonasa.cl` son **dofollow** y eso está bien: son señales de E-E-A-T hacia fuentes oficiales. No los pongas `nofollow`.

**Fuga:** el cuerpo **no enlaza a `/bono-pad-guatita-de-delantal`** (prioridad 0.90 en `sitemap.xml:46`, la más alta del cluster) ni a `/guatita-de-delantal-fonasa-isapre` (0.85, `sitemap.xml:52`). Son exactamente las dos páginas que este lector necesita después. Es la fuga de arquitectura interna más grave de las dos páginas auditadas.

### Inventario de CTAs [VERIFICADO]

| # | CTA | Línea | Destino | Tracking |
|---|---|---|---|---|
| 1 | tel topbar | `:342` | `tel:` | `phone_click` |
| 2 | Nav "Agenda evaluación" | `:362` | `/evaluacion` | `evaluacion_click`, `location:'nav'` |
| 3 | `.inline-cta` | `:464-477` | `/evaluacion` + WhatsApp | `location:'inline_cta_alternativas'` |
| 4 | `.cta-banner` | `:510-531` | `/evaluacion` + WhatsApp | `location:'cta_banner_final'` |
| 5 | `.mobile-sticky-cta` | `:586-589` | `/evaluacion` | `location:'mobile_sticky'` — **roto, ver A.3** |

### Fricción de conversión [VERIFICADO]

Idéntico cuadro que criolipólisis: cero prueba social en el cuerpo, cero imágenes, cero E-E-A-T personal, sin garantía. **Diferencia crítica:** aquí sí hay un precio ($1.977.990 + "13 cuotas de $149.830", `:462`) puesto delante de una audiencia FONASA que llegó buscando cobertura estatal. El contraste es brutal y sin ningún puente que lo amortigüe.

---

## A.3 🔴 Hallazgo crítico transversal: el sticky CTA móvil NO se está mostrando

Este es un bug de CSS, confirmado leyendo la cascada. Afecta a **ambas páginas objetivo y a ~30 páginas más del sitio**.

**La secuencia [VERIFICADO]:**

1. En `public/criolipolisis/index.html`, el `<style>` inline va de `:201` a `:393`. Dentro, en `:380`:
   ```css
   @media(max-width:900px){ ... .mobile-sticky-cta{display:block} ... }
   ```
2. **Inmediatamente después**, en `:394`:
   ```html
   <link rel="stylesheet" href="/css/shell.css">
   ```
3. En `public/css/shell.css:173` — **fuera de todo `@media`** (verificado: no hay ningún `@media` antes de esa línea en el archivo):
   ```css
   .mobile-sticky-cta{display:none;position:fixed;bottom:0;...;transform:translateY(100%);transition:transform .35s ...}
   ```
   ```css
   .mobile-sticky-cta.visible{transform:translateY(0)}   /* shell.css:174 */
   ```

Ambas reglas tienen especificidad idéntica `(0,1,0)`. Un `@media` **no** aporta especificidad. Al cargarse `shell.css` **después** del `<style>` inline, gana por orden de fuente.

**Resultado: `display:none` en todos los viewports.** Y aunque se corrigiera el `display`, `transform:translateY(100%)` lo dejaría fuera de pantalla, porque **ninguna de las dos páginas tiene JS que agregue la clase `.visible`** (los `<script>` finales, `:757-783` en criolipólisis y `:592-615` en AUGE, solo manejan nav, acordeón FAQ e IntersectionObserver).

Doble bloqueo. El sticky CTA de `criolipolisis/index.html:751` y de `guatita-de-delantal-auge-y-ley/index.html:586` **no es visible para ningún usuario**.

**Comparación con las páginas que sí funcionan [VERIFICADO]:**

| Página | ¿Carga `shell.css`? | Media query después de la regla base | JS que agrega `.visible` | ¿Funciona? |
|---|---|---|---|---|
| `public/index.html` | **No** (0 coincidencias) | Sí, `:500` después de `:477` | Sí, `:981-987` (`scrollY>300`) | ✅ |
| `public/evaluacion.html` | **No** (0 coincidencias) | — | Sí | ✅ |
| `public/resultados/index.html` | Sí (`:467`) | `:429`, antes de shell.css | No (usa `.is-hidden`, `:1174-1181`) | ❌ **también roto** |
| `public/criolipolisis/index.html` | Sí (`:394`) | `:380`, antes | No | ❌ |
| `public/guatita-de-delantal-auge-y-ley/index.html` | Sí (`:329`) | `:318`, antes | No | ❌ |

**Ojo con esto:** `/resultados` fue el rediseño CRO de referencia (`CHANGES.md:9` menciona explícitamente "sticky CTA bar"), y **su sticky bar tampoco se muestra**. Es decir, el patrón de referencia que se pidió copiar está roto en producción. Cualquier lectura de "el sticky CTA de /resultados no movió la aguja" es un falso negativo.

**Esta es la corrección de mayor ROI de toda la propuesta: cero riesgo SEO, ~10 líneas de código, y activa el elemento de conversión más importante en móvil de 30+ páginas.**

---

## A.4 Hallazgo: no hay atribución de origen del lead [VERIFICADO]

En `public/evaluacion.html:1874-1893`, el payload que se envía al webhook n8n (`https://n8n.oacg.cl/webhook/lead-capture`, `:1894`) contiene:

```
nombre, celular, correo, sede, disponibilidad,
fuente: 'Landing Evaluación P3',   ← constante hardcodeada
clinica, sede_slug, event_id,
'landing url': window.location.href,   ← siempre https://www.metodohebe.cl/evaluacion
'fecha de creacion', timestamp,
fbc, fbp, user_agent, event_source_url, event_time
```

**No hay `document.referrer`. No hay lectura de `utm_*`.** El único `URLSearchParams` de todo el archivo (`:1867`) lee `fbclid`, nada más.

**Consecuencia:** hoy es **imposible** saber si un lead vino de `/criolipolisis`, de `/guatita-de-delantal-auge-y-ley`, del home o de un anuncio. `fuente` siempre dice lo mismo.

Esto significa que **no se puede medir el resultado de esta propuesta con los datos actuales**. Arreglarlo es prerrequisito de la Fase 0, no un extra.

## A.5 Hallazgo: `click_location` del evento WhatsApp reporta `'home'` en los artículos [VERIFICADO]

El listener global (`criolipolisis/index.html:9-28`, idéntico en AUGE `:9-28`) hace:

```js
var section = link.closest('section, [data-section], main');
var location = (section && (section.id || (section.dataset && section.dataset.section))) || 'home';
```

- El WhatsApp del `.inline-cta` (`:540`) está dentro de `<article class="article-body">` (`:466`), y `<article>` **no** matchea el selector `section, [data-section], main`. → `section = null` → `location = 'home'`.
- El WhatsApp del `.cta-banner` (`:686`) está dentro de `<section class="cta-banner">` (`:675`), que **no tiene `id` ni `data-section`**. → `section.id` vacío → `location = 'home'`.

Todos los eventos `contacto_whatsapp_2026` de estas páginas llegan a GTM etiquetados como `'home'`. Se arregla agregando `id`/`data-section` a los contenedores. Cero riesgo.

## A.6 Hallazgo: las cifras de prueba social se contradicen entre sí [VERIFICADO]

| Afirmación | Dónde |
|---|---|
| "+30.000 pacientes en Chile" | `criolipolisis/index.html:706`, `guatita-de-delantal-auge-y-ley/index.html:541` (footer) |
| "+30.000 pacientes tratados" / "94% de satisfacción" | `resultados/index.html:525`, `:529` |
| **"+20.000 personas atendidas en nuestras 3 sedes"** | `evaluacion.html:1503` |
| "4,9 ★ promedio · +1.000 reseñas en Google" | `index.html:785` |
| **"5/5 en Google Reviews"** | `evaluacion.html:1508` |
| `aggregateRating: ratingValue 4.9, ratingCount 120` | `clinica-estetica-corporal-vitacura.html:113-117` |
| "+30.000 pacientes, 3 sedes" | `docs/LINK_BUILDING_PLAN_2026.md` |

**20.000 vs 30.000. 4,9 vs 5/5. +1.000 reseñas vs ratingCount 120.** Esto importa mucho para la sección F (schema): antes de propagar `aggregateRating` a más páginas hay que decidir cuál es el número real y verificable.

## A.7 CSS / JS: patrones reutilizables ya existentes [VERIFICADO]

`public/css/shell.css` (18.989 bytes) es la librería compartida y ya trae, listos para usar sin escribir diseño nuevo:

| Componente | Línea en `shell.css` | Uso propuesto |
|---|---|---|
| `.answer-capsule` | — | Ya usado en ambas páginas |
| `.inline-cta` + `.inline-cta-buttons` + `.btn-primary` + `.btn-wa` | `:110-118` | **CTAs intercalados adicionales** |
| `.tech-stack` / `.tech-card` | `:121-122` | Tarjetas de criterios / auto-triage |
| `.faq-item` / `.faq-q` / `.faq-a` / `.faq-toggle` / `.faq-item.open` | — | Acordeón (ya en uso) |
| `.mobile-sticky-cta` + `.visible` | `:173-176` | **Sticky (una vez arreglado)** |
| `.pricing-grid` / `.price-card` / `.price-card.featured` / `.price-amt` / `.price-chips` / `.price-feat-list` / `.price-popular` / `.price-cta` / `.btn-ghost` | `:178-206` | **Bloque de plan/oferta dentro del artículo — ya existe, no hay que diseñarlo** |
| `.chip` / `.chip.muted` | `:193-194` | Badges de prueba social |
| `.cta-banner` / `.cta-btn` / `.cta-btn-wa` / `.cta-trust` | — | Banner final (ya en uso) |

Patrones JS reutilizables ya escritos en el repo:

| Patrón | Origen |
|---|---|
| Sticky que aparece tras `scrollY>300` | `public/index.html:981-987` |
| Sticky que se oculta al llegar al footer vía `IntersectionObserver` | `public/resultados/index.html:1174-1181` |
| Scroll-depth 90% → `gtag('event','view_content')` | `public/index.html:989-996` |
| Acordeón FAQ accesible con `aria-expanded` | `criolipolisis/index.html:763-771` |
| Galería antes/después con toggle táctil + lightbox + lazy `<picture>` | `resultados/index.html:987-1140` |
| Carrusel móvil con contador y flechas | `resultados/index.html:1100-1145` |

**Conclusión de esta sección: no hay que inventar ni un componente.** Todo lo que la propuesta necesita ya está escrito y probado en el repo.

---

# B. Reglas de blindaje SEO

Esto es un contrato. Si alguna tarea de implementación choca con una regla de esta lista, **gana la regla**.

## B.1 🚫 INTOCABLE — no se modifica bajo ninguna circunstancia

| # | Elemento | Por qué |
|---|---|---|
| B1 | **URL** `/criolipolisis` y `/guatita-de-delantal-auge-y-ley` | Nunca. Ni con 301. Ambas están en `sitemap.xml` (`:18` prioridad 0.95 y `:37` prioridad 0.80), en `llms.txt` (`:12`, `:146`, `:155`), en el footer de todo el sitio y en el plan de link building como destino de anchors (`docs/LINK_BUILDING_PLAN_2026.md`, Ángulo B → `/criolipolisis/`). Un cambio de URL tira a la basura el activo. |
| B2 | **`<link rel="canonical">`** (`criolipolisis:47`, `auge:47`) | Self-canonical sin slash, consistente con `vercel.json` (`trailingSlash:false`). Correcto como está. |
| B3 | **Texto del `<h1>`** (`criolipolisis:446`, `auge:384`) | Es el ancla semántica principal. Se puede cambiar el *estilo* (tamaño, color), nunca las palabras. |
| B4 | **Todos los `<h2>` y `<h3>` existentes** | Cada uno mapea a un cluster de consultas. Nuevos H2/H3 **se agregan**; los actuales no se editan, no se reordenan, no se degradan a `<div>`. |
| B5 | **Todos los `<p>`, `<ul>`, `<ol>` y `<table>` actuales del `<article>`** | Cero borrado. El word count solo puede subir: 3.671 y 1.970 son pisos, no techos. |
| B6 | **Las citas bibliográficas** (`criolipolisis:560-562`, `:571`, `:526`) | Manstein & Anderson 2008, Ingargiola 2015, Krueger 2014, Jalian 2014. Es el núcleo de E-E-A-T de la página. **Esto es lo que un editor con prisa borraría por "sonar académico". No se toca.** |
| B7 | **El disclaimer de fuentes oficiales** (`auge:407-409`, `:440`) | La honestidad declarada ("no inventamos cifras ni plazos") sostiene la confianza de una página YMYL-normativa. |
| B8 | **Los 3 nodos JSON-LD de cada página** | `MedicalWebPage`, `BreadcrumbList`, `FAQPage`. Solo se **amplía** el `@graph`. Nunca se elimina ni se reemplaza un nodo. |
| B9 | **Correspondencia FAQ visible ↔ `FAQPage`** | 9 preguntas en criolipólisis, 5 en AUGE. Si se agrega una FAQ visible hay que agregarla también al schema, y viceversa. Schema con contenido no visible = riesgo de acción manual. |
| B10 | **Los enlaces salientes a `bcn.cl` y `fonasa.cl`** (`auge:408`) | Dofollow, hacia fuentes gubernamentales. Son señal de calidad. No poner `nofollow`, no quitar. |
| B11 | **Todos los enlaces internos salientes actuales** | Los 5 de criolipólisis y los 5 de AUGE listados en A.1/A.2. Se agregan más; no se quita ninguno. |
| B12 | **Enlaces internos entrantes** | Ver B.5 para el mapa completo verificado. Ninguna redirección, ningún cambio de anchor, ninguna eliminación. |
| B13 | **`meta robots`** (`index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1`) | Sin `noarchive`, sin `nosnippet`, sin `max-snippet` acotado. Es lo que permite snippets largos y aparición en AI Overviews. |
| B14 | **`hreflang`** (3 líneas por página) | Correcto. No tocar. |
| B15 | **`window.hebeTrack`** (`criolipolisis:34`, `auge:34`) | Post-commit `61403ba`, el mapa Meta es `{'whatsapp_click':'Contact'}` y todo lo demás va por `fbq('trackCustom', ...)`. **Los clics de CTA NO deben volver a disparar `Lead`.** El único `Lead` legítimo del sitio es el submit del wizard (`evaluacion.html:1846`). No revertir. |

## B.2 ⚠️ MODIFICABLE con justificación explícita y medición antes/después

| # | Elemento | Condición |
|---|---|---|
| B16 | `<title>` | Solo si Search Console muestra CTR bajo la media para su posición. Cambio mínimo, un solo elemento a la vez, y **manteniendo la keyword principal en las primeras 40 caracteres**. El de criolipólisis (79 caracteres) ya es largo; el de AUGE (77) también. |
| B17 | `meta description` | Riesgo bajo (no es factor de ranking directo). Se puede iterar por CTR. |
| B18 | Orden visual de bloques **nuevos** | Los nuevos se pueden mover libremente. Los existentes no. |
| B19 | CSS de componentes existentes | Se puede reestilizar sin cambiar el DOM ni el texto. Ojo con CLS (ver I.4). |

## B.3 ✅ SEGURO — se puede agregar sin riesgo apreciable

| # | Acción | Nota |
|---|---|---|
| B20 | **Bloques nuevos intercalados** entre secciones existentes | Regla de oro: **insertar, jamás reemplazar**. |
| B21 | **CTAs adicionales** (`.inline-cta`, banda estrecha, botón contextual) | Suman conversión, no restan texto. Vigilar B.4. |
| B22 | **Nodos JSON-LD adicionales** dentro del mismo `@graph` | Ver sección F. |
| B23 | **Imágenes con `alt`, `width`, `height` y `loading="lazy"`** | Suma para Google Images, para `max-image-preview:large` y para engagement. **`width`/`height` obligatorios** para no romper CLS. |
| B24 | **`og:image` y `twitter:image`** | Hoy no existen. Agregar es puro upside. |
| B25 | **Enlaces internos nuevos** hacia el resto del cluster | Mejora la arquitectura, distribuye equity. |
| B26 | **Nuevas FAQ** (visible + schema, en pareja) | Amplía cobertura de long tail. |
| B27 | **Tracking adicional** (`hebeTrack`, `dataLayer.push`, scroll depth) | Siempre que respete B15. |
| B28 | **Bloque de autor/revisor clínico con nombre real** | Es la mejora de E-E-A-T de mayor impacto disponible. Requiere una persona real que acepte firmar. |

## B.4 🚨 Límites duros de CTA (política de intrusive interstitials)

Google penaliza en móvil los interstitials intrusivos. Un sticky bar **no** cae en la penalización si respeta un tamaño razonable. Reglas autoimpuestas:

1. El sticky móvil ocupa **≤ 15% de la altura del viewport** (≈ 100 px en un viewport de 667 px). El `shell.css:173-176` actual (`padding:10px 16px 14px` + botón de 14px de padding + `trust-text` de 11px) queda en ~90-100 px. **Cumple.**
2. **No aparece antes de `scrollY > 400px`.** Nunca sobre el hero, nunca en la primera pantalla.
3. **Se oculta al llegar al footer** (patrón `IntersectionObserver` de `resultados:1174-1181`), para que nunca tape el `.cta-banner`.
4. **Cero pop-ups, cero modales, cero exit-intent, cero overlay de pantalla completa.** En ninguna circunstancia.
5. **Máximo 5 puntos de conversión dentro del `<article>`** (contando `.inline-cta` y bandas). Más que eso convierte el artículo en publirreportaje y erosiona la señal de calidad.
6. `body{padding-bottom: ...}` correspondiente para que el sticky no tape la última línea de texto.

## B.5 Mapa verificado de enlaces internos entrantes

Ambas URLs reciben **49 enlaces internos entrantes cada una**. Pero la mayoría son del footer sitewide, con anchor idéntico, y Google los descuenta con fuerza. **El link equity real viene de los enlaces contextuales** (`class="inline-link"`, dentro del cuerpo del texto).

### → `/criolipolisis` — 16 enlaces contextuales en 10 archivos [VERIFICADO]

| Archivo | Líneas |
|---|---|
| `public/opciones-para-eliminar-la-grasa-localizada/index.html` | 411, 428, 529 |
| `public/blog/grasa-localizada-eliminar-sin-cirugia.html` | 531, 641 |
| `public/blog/ized-ultrasonido-corporal.html` | 532, 726 |
| `public/tratamientos-corporales-esteticos-para-renovar-tu-cuerpo/index.html` | 418, 502 |
| `public/grasa-localizada.html` | 524, 565 |
| `public/lipoescultura-sin-cirugia/index.html` | 505 |
| `public/grasa-localizada-los-angeles/index.html` | 540 |
| `public/grasa-localizada-concon/index.html` | 548 |
| `public/flacidez-abdominal/index.html` | 509 |
| `public/criolipolisis-los-angeles/index.html` | 492 |

Los otros 39 son de nav/footer con anchor uniforme "Criolipólisis".

### → `/guatita-de-delantal-auge-y-ley` — 10 enlaces contextuales en 6 archivos [VERIFICADO]

| Archivo | Líneas |
|---|---|
| `public/guatita-de-delantal-fonasa-isapre/index.html` | 430, 452, 466 |
| `public/flacidez-abdominal/index.html` | 465, 525, 538 |
| `public/bono-pad-guatita-de-delantal/index.html` | 491, 565 |
| `public/guatita-de-delantal-operacion-vs-tratamiento/index.html` | 535 |
| `public/blog/guatita-delantal-tratamiento-sin-cirugia.html` | 655 |

Los otros 43 son de nav/footer con anchor uniforme "Ley 21.438 (Saín)".

**Consecuencias para esta propuesta:**
1. **No tocar esos 26 enlaces contextuales.** Son el activo real.
2. **Oportunidad barata:** aumentar los enlaces contextuales entrantes es más eficaz que cualquier bloque nuevo. `/criolipolisis` no recibe enlace contextual desde `/resultados` ni desde `/planes`, dos páginas de alta relevancia temática.
3. **Asimetría documentada:** `/guatita-de-delantal-auge-y-ley` recibe 49 entrantes (10 contextuales) con priority 0.80, mientras la pillar declarada del cluster (`/que-es-la-guatita-de-delantal-y-como-puedes-solucionarlo`) tiene priority 0.75. La arquitectura de enlaces y el sitemap no cuentan la misma historia.

---

# C. Nueva arquitectura de página propuesta

Principio guía, en una frase: **el artículo completo se mantiene íntegro y se le inyectan puntos de conversión exactamente donde el lector acaba de recibir la información que genera intención.**

Leyenda: `[INTACTO]` sin cambios · `[NUEVO]` bloque agregado · `[MOD]` modificado (se detalla qué)

---

## C.1 Wireframe: `/criolipolisis`

```
┌──────────────────────────────────────────────────────────────────────┐
│ 01  TOPBAR                                          [INTACTO] :400   │
│ 02  NAV sticky + "Agenda evaluación"                [INTACTO] :414   │
│ 03  BREADCRUMB                                      [INTACTO] :436   │
├──────────────────────────────────────────────────────────────────────┤
│ 04  ARTICLE HERO                                    [MOD]     :443   │
│     H1 intacto (B3). Eyebrow y descripción intactos.                 │
│     ► [NUEVO] fila de 3 .chip bajo .article-meta:                    │
│        "Evaluación sin costo" · "+30.000 pacientes" ·                │
│        "3 sedes: Vitacura · Concón · Los Ángeles"                    │
│       Sin números de rating hasta resolver A.6.                      │
│       Reusa .chip de shell.css:193. Altura fija → sin CLS.           │
├──────────────────────────────────────────────────────────────────────┤
│ 05  ANSWER CAPSULE                                  [INTACTO] :469   │
│ 06  H2 ¿Qué es la criolipólisis? + 3 párrafos       [INTACTO] :473   │
├──────────────────────────────────────────────────────────────────────┤
│ 07  ► [NUEVO] BANDA DE AUTOEVALUACIÓN "¿Eres candidata?"             │
│     Inserción: después de :479, antes del H2 :481                    │
│     ~400 px de scroll. Es el PRIMER punto de conversión.             │
│     Formato: .tech-stack con 2 .tech-card (shell.css:121)            │
│       ✔ SÍ suele funcionar: pliegue pellizcable ≥2,5 cm, IMC 18-30,  │
│         piel elástica, peso estable                                  │
│       ✘ NO es la vía: exceso de piel colgante, IMC >35, objetivo     │
│         de bajar de peso                                             │
│     Cierre: link de texto discreto → /evaluacion                     │
│     ⚠ Este bloque REPITE info del artículo → es un resumen visual,   │
│       no contenido nuevo. Suma ~90 palabras. No canibaliza nada.     │
├──────────────────────────────────────────────────────────────────────┤
│ 08  H2 ¿Cómo funciona paso a paso? + <ol> + 3 párr. [INTACTO] :481   │
│ 09  ► [NUEVO] FIGURA: sesion-criolipolisis-hiems.webp                │
│     Inserción: tras :494. <figure> + <figcaption>.                   │
│     alt="Sesión de criolipólisis con equipo iZED en Método Hebe"     │
│     width/height explícitos + loading="lazy" (B23).                  │
│     Imagen YA EXISTE en /img/ y no se usa en esta página.            │
│     Además sirve de og:image (ver F.6).                              │
├──────────────────────────────────────────────────────────────────────┤
│ 10  H2 Zonas tratables + 5 H3 + párrafo final       [INTACTO] :496   │
│ 11  ► [NUEVO] CTA CONTEXTUAL ESTRECHO (1 línea + botón)              │
│     Inserción: tras :520. "¿Cuál es tu zona? La medimos en la        │
│     evaluación." → /evaluacion.                                      │
│     Formato compacto (NO el .inline-cta completo, para no romper el  │
│     ritmo de lectura ni gastar el "presupuesto" de 5 CTAs de B.4).   │
├──────────────────────────────────────────────────────────────────────┤
│ 12  H2 Criolipólisis antes y después + 4 párrafos   [INTACTO] :522   │
│ 13  ► [NUEVO] GALERÍA DE PRUEBA — 2 o 3 pares antes/después          │
│     Inserción: tras :530, ANTES del .inline-cta existente.           │
│     ★ EL BLOQUE DE MAYOR IMPACTO CRO DE TODA LA PÁGINA.              │
│     Reusa el markup de resultados/index.html:585-610 (.photo-card    │
│     + <picture> webp/jpg + toggle táctil + lazy).                    │
│     Imágenes existentes sin usar aquí:                               │
│       resultado-abdomen-cintura.webp/.jpg                            │
│       resultado-lateral-cintura.webp/.jpg                            │
│       resultado-contorno-corporal.webp/.jpg                          │
│     Mantener el disclaimer de resultados/index.html:566 palabra      │
│     por palabra (resultados variables, foto estandarizada).          │
│     Cierre: "Ver los 11 casos documentados" → /resultados            │
│       ← cierra la fuga de enlace interno detectada en A.1            │
├──────────────────────────────────────────────────────────────────────┤
│ 14  .inline-cta "¿Tu caso es candidato?"            [MOD]     :532   │
│     Se mantiene posición, H3 y ambos botones.                        │
│     Solo se ajusta el copy del <p> (ver D.1) y se agrega             │
│     data-section="cta_resultados" al contenedor (fix A.5).           │
├──────────────────────────────────────────────────────────────────────┤
│ 15  H2 ¿Cuánto cuesta la criolipólisis en Chile?    [INTACTO] :547   │
│     3 párrafos con rango de mercado + Plan Zero Rollito.             │
│ 16  ► [NUEVO] TARJETA DE PLAN — .price-card de shell.css:184         │
│     Inserción: tras :553.                                            │
│     ★ SEGUNDO BLOQUE DE MAYOR IMPACTO. Aquí la intención             │
│       comercial del lector está en su punto máximo.                  │
│     Contenido: Plan Zero Rollito · $1.799.990 CLP · 12 sesiones /    │
│       3 meses · chips: iZED (criolipólisis) · SkinWave MAX ·         │
│       Adipolite · Evaluación P3 y bioimpedancia incluidas            │
│     Datos tomados textual de planes/index.html:107-110, :579-580.    │
│     Doble botón: .btn-primary → /evaluacion  ·  .btn-ghost →/planes  │
│     ⚠ El precio DEBE coincidir con /planes. Si cambia allá, cambia   │
│       acá. Precio contradictorio = pérdida de confianza + riesgo     │
│       si se agrega Offer schema (F.3).                               │
├──────────────────────────────────────────────────────────────────────┤
│ 17  H2 ¿Es efectiva? Evidencia clínica + 3 estudios [INTACTO] :555   │
│     ⚠ NO TOCAR (B6).                                                 │
│ 18  H2 Contraindicaciones y riesgos reales          [INTACTO] :567   │
│     Incluye hiperplasia adiposa paradójica. NO TOCAR (B6).           │
│ 19  ► [NUEVO] MICRO-BLOQUE DE CONFIANZA (no es un CTA)               │
│     Inserción: tras :587.                                            │
│     "Si en la evaluación detectamos una contraindicación, te lo      │
│      decimos y derivamos. No tratar también es cuidar."              │
│     Es reversión de riesgo, no venta. Refuerza justamente el         │
│     atributo que hace única a la página.                             │
├──────────────────────────────────────────────────────────────────────┤
│ 20  H2 Criolipólisis vs otras técnicas + tabla      [INTACTO] :589   │
│ 21  H2 Criolipólisis en el Método Hebe + 3 párrafos [MOD]     :616   │
│     Texto intacto. ► [NUEVO] al final: 3 tarjetas de sede con        │
│     dirección + link a /clinica-estetica-corporal-{vitacura,         │
│     concon,los-angeles} — hoy solo están en el footer.               │
│     Refuerza señal local + da soporte visible al LocalBusiness (F.2).│
├──────────────────────────────────────────────────────────────────────┤
│ 22  ► [NUEVO] BLOQUE AUTOR / REVISIÓN CLÍNICA                        │
│     Inserción: tras :622, antes del H2 FAQ.                          │
│     Nombre real + cargo + credencial + foto + fecha de revisión.     │
│     Da soporte visible al nodo Person del schema (F.4).              │
│     ⚠ BLOQUEANTE: requiere una persona real que acepte firmar.       │
│       Sin persona real → NO se implementa ni el bloque ni el schema. │
├──────────────────────────────────────────────────────────────────────┤
│ 23  H2 Preguntas frecuentes — 9 items               [MOD]     :624   │
│     Las 9 intactas (B4, B9).                                         │
│     ► [NUEVO] 2 FAQ agregadas al final + a FAQPage (F.1):            │
│       "¿La criolipólisis sirve para la guatita de delantal?"         │
│         → puente hacia el cluster guatita, con la verdad clínica     │
│       "¿Cuántas sesiones incluye el plan de Método Hebe?"            │
│         → resuelve la objeción real de compra                        │
├──────────────────────────────────────────────────────────────────────┤
│ 24  </article>                                                       │
│ 25  ► [NUEVO] BLOQUE DE ENLACES RELACIONADOS                         │
│     4-6 tarjetas: /resultados · /lipoescultura-sin-cirugia ·         │
│     /grasa-localizada · /flacidez-abdominal · /planes ·              │
│     /criolipolisis-los-angeles                                       │
│     ⚠ Ver I.5 sobre el anchor de /criolipolisis-los-angeles.         │
│ 26  .cta-banner "Evaluación diagnóstica antes"      [MOD]     :675   │
│     Estructura y copy intactos. Solo se agrega id="cta-final"        │
│     al <section> (fix A.5).                                          │
│ 27  FOOTER                                          [INTACTO] :699   │
│ 28  MOBILE STICKY CTA                               [MOD]     :751   │
│     ★ SE ARREGLA (A.3): mover la media query después de shell.css    │
│       o subir especificidad, + JS que agrega .visible con            │
│       scrollY>400, + IntersectionObserver que la oculta en footer.   │
│     Copy nuevo (D.1). Botón principal + botón WhatsApp secundario,   │
│     como en resultados/index.html:972-980.                           │
│     Respeta todos los límites de B.4.                                │
└──────────────────────────────────────────────────────────────────────┘
```

**Balance del rediseño de `/criolipolisis`:**

| | Antes | Después |
|---|---|---|
| Palabras del artículo | 3.671 | ~3.950 (**solo suma**) |
| Palabras antes del 1er punto de conversión | 1.476 (40%) | **~180 (5%)** |
| Puntos de conversión en el `<article>` | 1 | 4 (banda triage, CTA zonas, `.inline-cta`, tarjeta de plan) — dentro del límite de 5 de B.4 |
| Imágenes en el cuerpo | 0 | 3-4 |
| Sticky móvil funcional | ❌ | ✅ |
| Enlace a `/resultados` | ❌ | ✅ ×2 |
| Bloques de texto eliminados | — | **0** |
| Encabezados existentes alterados | — | **0** |

---

## C.2 Wireframe: `/guatita-de-delantal-auge-y-ley`

**Marco distinto.** Aquí el objetivo **no** es vender. Es (1) proteger y ampliar un activo informativo que rankea y que alimenta el Ángulo A del plan de link building, y (2) **segmentar** al 5-15% del tráfico que sí es lead cualificado, sin maltratar al 85-95% que no lo es. Ver sección E para el razonamiento completo.

```
┌──────────────────────────────────────────────────────────────────────┐
│ 01  TOPBAR / NAV / BREADCRUMB (4 niveles)           [INTACTO] :335   │
├──────────────────────────────────────────────────────────────────────┤
│ 02  ARTICLE HERO                                    [MOD]     :381   │
│     H1 intacto (B3).                                                 │
│     ► [NUEVO] chips de credibilidad, NO comerciales:                 │
│        "Fuentes: BCN · Minsal · FONASA" ·                            │
│        "Actualizado abril 2026" · "Sin costo consultar"              │
│     El registro correcto aquí es institucional, no clínica privada.  │
├──────────────────────────────────────────────────────────────────────┤
│ 03  ANSWER CAPSULE (disclaimer de fuentes)          [INTACTO] :407   │
│     ⚠ NO TOCAR (B7). Es el activo de confianza de la página.         │
├──────────────────────────────────────────────────────────────────────┤
│ 04  ► [NUEVO] ÍNDICE / "SALTA A LO QUE NECESITAS"                    │
│     Inserción: tras :409.                                            │
│     5-6 anchors a los H2 existentes (requiere agregarles id, lo      │
│     cual NO altera el texto → permitido por B4).                     │
│     ► Función CRO: reduce rebote y lleva al usuario directo a su     │
│       necesidad; los lectores de trámites escanean, no leen.         │
│     ► Función SEO: habilita sitelinks de anchor en la SERP.          │
│     Último item: "¿No calificas? Alternativas" → ancla la sección    │
│     comercial desde la primera pantalla, SIN venderle a nadie.       │
│     ★ Este bloque es el que resuelve el problema del 74%: pone       │
│       la ruta comercial al alcance en el primer scroll, y deja       │
│       que el usuario decida si la toma.                              │
├──────────────────────────────────────────────────────────────────────┤
│ 05  H2 ¿Qué es la Ley Saín / Ley 21.438?            [INTACTO] :411   │
│ 06  H2 ¿Está dentro de AUGE/GES?                    [INTACTO] :419   │
│     ⚠ SECCIÓN MÁS VALIOSA PARA EL RANKING. Es la respuesta al        │
│       error de nomenclatura "guatita AUGE". No tocar ni una coma.    │
│ 07  ► [NUEVO] TABLA COMPARATIVA AUGE/GES vs LEY 21.438               │
│     Inserción: tras :423.                                            │
│     Filas: qué es · qué cubre · garantía de plazo · dónde se pide ·  │
│       requisito principal                                            │
│     100% informativa, sin mención comercial.                         │
│     ► Es el bloque con mayor probabilidad de ganar featured snippet  │
│       y de ser citado por AI Overviews / ChatGPT / Perplexity.       │
│     Reusa .comparison-table (ya definida en el <style> de la página).│
├──────────────────────────────────────────────────────────────────────┤
│ 08  H2 Requisitos para postular + <ul> 8 items      [INTACTO] :425   │
│     + disclaimer :440. NO TOCAR (B7).                                │
│ 09  ► [NUEVO] CHECKLIST DESCARGABLE / IMPRIMIBLE                     │
│     Inserción: tras :440.                                            │
│     "Checklist de documentos para tu cita en el CESFAM"              │
│     ► Utilidad genuina y gratis. Es el lead magnet CORRECTO para     │
│       esta audiencia: pide un correo/WhatsApp a cambio de algo que   │
│       sirve para su trámite ESTATAL, no para comprarnos.             │
│     ► Convierte a un KPI secundario (contacto) sin fricción          │
│       comercial ni contradicción con el contenido.                   │
│     ⚠ Requiere endpoint. Reusar el webhook n8n de evaluacion.html    │
│       :1894 con un `fuente` distinto para no ensuciar el pipeline    │
│       de leads P3 (ver G.4).                                         │
│     ⚠ Si no hay capacidad de construirlo: versión sin fricción,      │
│       botón "Imprimir esta lista" (window.print), cero captura.      │
│       Sigue siendo mejor que nada.                                   │
├──────────────────────────────────────────────────────────────────────┤
│ 10  H2 Cómo postular paso a paso + <ol> 5 pasos     [INTACTO] :442   │
│     ► [MOD] agregar itemscope HowTo al <ol> existente (F.5)          │
│       — solo atributos, cero cambio de texto.                        │
│ 11  ► [NUEVO] BLOQUE PUENTE HONESTO (no es CTA)                      │
│     Inserción: tras :454, justo después de "los tiempos de espera    │
│     son reales y pueden ser largos: meses o incluso años".           │
│     ★ ESTE ES EL MOMENTO DE MÁXIMA INTENCIÓN DE LA PÁGINA.           │
│       El lector acaba de leer que puede esperar años.                │
│     Copy: reconoce la espera, NO vende, ofrece orientación.          │
│     Ver D.2 para el texto exacto.                                    │
│     Un solo enlace, de texto, hacia la sección de alternativas       │
│     (que está 2 pantallas abajo). No hacia /evaluacion todavía.      │
├──────────────────────────────────────────────────────────────────────┤
│ 12  H2 Si no calificas o la espera es muy larga     [INTACTO] :456   │
│     Párrafos (a) cirugía privada y (b) no invasivo. NO TOCAR:        │
│     el párrafo :462 con "no reemplaza la cirugía" es lo que hace     │
│     que esta página sea creíble. Es su blindaje ético Y su ranking.  │
│ 13  ► [NUEVO] AUTO-TRIAGE DE 3 RUTAS  ★ EL BLOQUE CLAVE              │
│     Inserción: tras :462, ANTES del .inline-cta existente.           │
│     3 .tech-card (shell.css:121), lado a lado. Segmenta al lector    │
│     por su propio cuadro clínico y le da a cada uno lo que le sirve: │
│                                                                       │
│     ┌ RUTA 1 — Piel colgante marcada, post-bariátrica ─────────────┐ │
│     │ "Tu caso es quirúrgico. La Ley 21.438 es tu mejor vía."      │ │
│     │ → /guatita-de-delantal-fonasa-isapre                         │ │
│     │ → /bono-pad-guatita-de-delantal                              │ │
│     │ CERO oferta comercial. Se le ayuda y punto.                  │ │
│     └──────────────────────────────────────────────────────────────┘ │
│     ┌ RUTA 2 — Grasa + flacidez leve/moderada, piel elástica ──────┐ │
│     │ "Tu caso puede no ser quirúrgico. Vale la pena medirlo."     │ │
│     │ → /evaluacion  ·  → /guatita-de-delantal-operacion-vs-trat.  │ │
│     │ ★ ESTA es la ruta comercial. El único segmento cualificado.  │ │
│     └──────────────────────────────────────────────────────────────┘ │
│     ┌ RUTA 3 — En lista de espera, quiere llegar mejor a pabellón ─┐ │
│     │ "Mantener peso estable mejora tu indicación quirúrgica."     │ │
│     │ → /ejercicios-para-guatita-de-delantal                       │ │
│     │ → /que-es-la-guatita-de-delantal-y-como-puedes-solucionarlo  │ │
│     └──────────────────────────────────────────────────────────────┘ │
│                                                                       │
│     ► Cierra las 2 fugas de enlace interno de A.2 (bono-pad y        │
│       fonasa-isapre, prioridades 0.90 y 0.85 en el sitemap).         │
│     ► Consolida el cluster: esta página pasa a ser el hub de         │
│       distribución de "guatita de delantal + cobertura".             │
│     ► Convierte a quien corresponde y ayuda a quien no. Es la única  │
│       forma de monetizar este tráfico sin mentirle.                  │
├──────────────────────────────────────────────────────────────────────┤
│ 14  .inline-cta "¿La Ley Saín no es para ti?"       [MOD]     :464   │
│     Posición y H3 intactos. Copy del <p> ajustado (D.2) para bajar   │
│     la presión comercial y subir el énfasis en orientación.          │
│     + data-section="cta_alternativas" (fix A.5).                     │
├──────────────────────────────────────────────────────────────────────┤
│ 15  H2 Preguntas frecuentes — 5 items               [MOD]     :479   │
│     Las 5 intactas (B4, B9).                                         │
│     ► [NUEVO] 3 FAQ agregadas + a FAQPage (F.1):                     │
│       "¿Cuánto cuesta operarse de guatita de delantal en el sistema  │
│         privado en Chile?"     ← alto volumen [DEDUCCIÓN]            │
│       "¿Puedo tratarme mientras espero mi cupo quirúrgico?"          │
│         ← única FAQ con ángulo comercial legítimo                    │
│       "¿La Ley Saín cubre también brazos, mamas o muslos?"           │
│         ← duda real y frecuente en post-bariátricas                  │
├──────────────────────────────────────────────────────────────────────┤
│ 16  </article>                                                       │
│ 17  ► [NUEVO] BLOQUE "SIGUE LEYENDO" — hub del cluster completo      │
│     6 tarjetas a las 6 URLs hermanas de guatita.                     │
│ 18  .cta-banner                                     [MOD]     :510   │
│     H2 intacto. Copy del <p> ajustado (D.2). + id="cta-final".       │
│ 19  FOOTER                                          [INTACTO] :534   │
│ 20  MOBILE STICKY CTA                               [MOD]     :586   │
│     ★ SE ARREGLA (A.3) — pero con COPY DISTINTO al de criolipólisis. │
│     Aquí el sticky NO dice "Agenda" (a esta audiencia le suena a     │
│     que le van a cobrar). Dice orientación. Ver D.2.                 │
│     ⚠ Aparece más tarde: scrollY > 800 en vez de 400. Que el lector  │
│       reciba primero la información institucional que vino a buscar. │
└──────────────────────────────────────────────────────────────────────┘
```

**Balance del rediseño de `/guatita-de-delantal-auge-y-ley`:**

| | Antes | Después |
|---|---|---|
| Palabras del artículo | 1.970 | ~2.700 (**solo suma**; sale de la zona de riesgo de thin content) |
| Palabras antes del 1er punto de decisión | 1.460 (74%) | **~120 (índice navegable, 4%)** |
| Enlaces internos al cluster desde el cuerpo | 5 | 9 (+`bono-pad`, +`fonasa-isapre`, ×2 refuerzos) |
| Ruta para lector NO cualificado | ninguna (solo se le vende) | 2 rutas útiles y gratuitas |
| Presión comercial | media, mal ubicada | baja, bien segmentada |
| Bloques informativos eliminados | — | **0** |

---

# D. Copy concreto de los CTAs

Tono Método Hebe: clínico-cercano, sin promesas médicas, sin urgencia artificial, español de Chile neutro (sin "che", sin "vos", sin exceso de modismos). Voseo chileno informal: **no**. Trato de "tú": **sí**.

Reglas transversales:
- Nunca "elimina la grasa para siempre", "resultados garantizados", "adelgaza X kilos".
- Siempre "medimos", "evaluamos", "te decimos con honestidad", "sin costo, sin compromiso".
- Nunca urgencia falsa ("últimos cupos", "oferta por 24 horas"). El sitio no la usa hoy y no debe empezar.

## D.1 `/criolipolisis` — lector con intención comercial

**1. Chips del hero (bloque 04)**
```
Evaluación sin costo   ·   +30.000 pacientes   ·   Vitacura · Concón · Los Ángeles
```
> ⚠ El "+30.000" está en el footer actual (`:706`), pero `evaluacion.html:1503` dice "+20.000". Resolver A.6 y usar **una sola cifra en todo el sitio** antes de publicar.

**2. Banda de autoevaluación (bloque 07) — primer punto de conversión**
```
Antes de seguir leyendo: ¿tu caso es de criolipólisis?

✔  Suele funcionar cuando…
   Puedes pellizcar un pliegue de 2,5 cm o más en la zona
   Tu IMC está entre 18 y 30
   Tu piel mantiene elasticidad
   Tu peso lleva algunos meses estable

✘  No es la vía cuando…
   El problema principal es piel colgante o sobrante
   Tu IMC supera 35
   Lo que buscas es bajar de peso

Si dudas en cuál de las dos columnas estás, lo medimos en 45 minutos
y te lo decimos.  →  Agenda tu Evaluación P3 (sin costo)
```

**3. CTA contextual de zonas (bloque 11)**
```
¿Cuál es tu zona? En la evaluación medimos el pliegue de cada una
y te decimos cuántas aplicaciones necesitaría realmente.

[ Medir mi zona → ]
```

**4. Galería antes/después (bloque 13) — texto de cierre**
```
Estos son casos reales documentados con fotografía estandarizada.
Los resultados varían según el caso, el perfil metabólico y la
adherencia al plan.

[ Ver los 11 casos documentados → ]
```

**5. `.inline-cta` existente (bloque 14) — H3 intacto, `<p>` ajustado**

H3 (**no se toca**): `¿Tu caso es candidato a criolipólisis?`

`<p>` propuesto:
```
En 45 minutos hacemos bioimpedancia, medimos el pliegue de la zona que
te preocupa y te decimos con honestidad si la criolipólisis basta, si
conviene combinarla con otra tecnología, o si tu caso debería tomar
otra vía. Sin costo y sin compromiso.
```
Botones (**intactos**): `Agenda tu Evaluación P3` · `Pregunta por WhatsApp`

**6. Tarjeta de plan (bloque 16) — el bloque comercial**
```
┌─────────────────────────────────────────────────────────┐
│                                        MÁS SOLICITADO   │
│  Plan Zero Rollito                                      │
│  $1.799.990  CLP / plan                                 │
│  12 sesiones en 3 meses para grasa localizada.          │
│                                                          │
│  [iZED · criolipólisis]  [SkinWave MAX]  [Adipolite]    │
│                                                          │
│  ✓ Evaluación P3 con bioimpedancia incluida             │
│  ✓ Fotografía estandarizada a los 30, 60 y 90 días      │
│  ✓ Acompañamiento nutricional durante el protocolo      │
│  ✓ Disponible en Vitacura, Concón y Los Ángeles         │
│                                                          │
│  [ Agendar evaluación sin costo ]                       │
│  [ Ver los 4 planes y sus precios ]                     │
│                                                          │
│  El plan definitivo se define después de la evaluación, │
│  según tu diagnóstico. No adivinamos, medimos.          │
└─────────────────────────────────────────────────────────┘
```

**7. Micro-bloque de confianza (bloque 19) — no es CTA**
```
Si en la evaluación encontramos una contraindicación —relativa o
absoluta— te lo decimos y derivamos. No tratar también es una forma
de cuidar al paciente.
```

**8. Sticky móvil (bloque 28)**
```
Copy:    ¿Es criolipólisis lo que necesitas? Lo medimos en 45 min.
Botón 1: Agenda sin costo
Botón 2: [ícono WhatsApp]
```

**9. `.cta-banner` final (bloque 26)** — **intacto**. El copy actual (`:678-693`) es bueno: "No adivinamos, medimos", "Sin costo ni compromiso", "Te decimos con honestidad si la criolipólisis es la ruta correcta". No hay nada que mejorar ahí.

---

## D.2 `/guatita-de-delantal-auge-y-ley` — lector con expectativa de cobertura estatal

**Cambio de registro, y es deliberado.** Este lector no viene a comprar. Muchos vienen del sistema público, muchos ya fueron rechazados o llevan años esperando, y varios no pueden pagar $1.977.990. Un CTA que suene a "agenda y te vendemos" quema la página. Los CTAs de abajo venden **claridad**, no tratamiento.

**1. Chips del hero (bloque 02)**
```
Fuentes: BCN · Minsal · FONASA   ·   Actualizado abril 2026   ·   Consultar no tiene costo
```

**2. Índice navegable (bloque 04)**
```
Salta a lo que necesitas:

→ Qué es la Ley 21.438 (Saín)
→ Por qué NO es lo mismo que AUGE/GES
→ Requisitos para postular en 2026
→ Cómo postular, paso a paso
→ Qué hacer si no calificas o la espera es larga
```

**3. Checklist descargable (bloque 09)**
```
Antes de ir al consultorio: lleva esto contigo

Preparamos una lista con los documentos y antecedentes que
habitualmente te van a pedir en el CESFAM y en la unidad de bariatría.
Te la enviamos por WhatsApp para que la tengas a mano.

[ Recibir la lista por WhatsApp ]

Es gratis y no implica agendar nada con nosotros.
```
> La última línea es la que hace que este bloque funcione: elimina la sospecha de que es un embudo comercial disfrazado.

**4. Bloque puente honesto (bloque 11) — máximo momento de intención**
```
Sobre la espera

Si te dijeron "varios meses" o "un par de años", no es un trámite mal
hecho: es la capacidad instalada del sistema. Mientras tanto hay dos
cosas que sí dependen de ti — mantener el peso estable y llegar a
pabellón en buenas condiciones — y una tercera que conviene saber:
no todos los casos que llegan buscando esta ley son quirúrgicos.
Algunos sí. Otros no.

Más abajo explicamos cómo distinguir un caso del otro. →
```
> Cero venta. Cero enlace a `/evaluacion`. Solo prepara el terreno para el auto-triage.

**5. Auto-triage de 3 rutas (bloque 13) — el bloque clave**

Encabezado del bloque:
```
Tres situaciones distintas. Estas son las rutas de cada una.
```

Tarjeta 1:
```
Tienes piel colgante marcada tras una baja de peso importante

Tu caso es probablemente quirúrgico y el tratamiento no invasivo no
lo va a resolver. Te decimos derecho: la vía pública es tu mejor
opción y vale la pena insistir.

→ Qué cubre FONASA e Isapre en guatita de delantal
→ Bono PAD: qué es y cuándo conviene
```

Tarjeta 2:
```
Tu abdomen es más grasa y flacidez que piel sobrante

Puede que tu caso no sea quirúrgico. Cuando el componente principal
es grasa subcutánea y flacidez con piel elástica, hay una vía no
invasiva proporcional. Pero eso hay que medirlo, no suponerlo.

→ Agenda una evaluación sin costo y sale de la duda
→ Compara operación vs tratamiento no invasivo
```

Tarjeta 3:
```
Ya estás en lista de espera y quieres llegar bien a la cirugía

Mantener peso estable y trabajar la musculatura abdominal mejora tu
indicación quirúrgica y tu recuperación. No cambia tu lugar en la
lista, pero sí cómo llegas.

→ Ejercicios para guatita de delantal
→ Guía completa: qué es y cómo se aborda
```

**6. `.inline-cta` existente (bloque 14) — H3 intacto, `<p>` ajustado**

H3 (**no se toca**): `¿La Ley Saín no es para ti? Evaluamos alternativas reales`

`<p>` actual (`:466`):
> "En 45 minutos te decimos si tu caso es quirúrgico, si calificas a la Ley 21.438, o si un tratamiento no invasivo es una alternativa proporcional. Medición clínica completa, sin costo."

`<p>` propuesto:
```
En 45 minutos medimos tu caso y te decimos una de tres cosas: que es
quirúrgico y debes seguir por la vía pública, que podrías calificar a
la Ley 21.438, o que un tratamiento no invasivo es proporcional a lo
que tienes. Es una medición, no una venta. Sin costo.
```
> "Es una medición, no una venta" hace el trabajo pesado con esta audiencia.

**7. `.cta-banner` final (bloque 18) — H2 intacto, `<p>` ajustado**

H2 (**no se toca**): `¿No calificas o la espera es larga? Evaluamos alternativas no invasivas`

`<p>` propuesto:
```
Evaluación clínica sin costo con bioimpedancia, cintometría y revisión
de calidad de piel. Si tu caso es quirúrgico te lo decimos y te
orientamos hacia la vía pública. Si no lo es, te explicamos qué
alternativa proporcional existe y cuánto cuesta, sin rodeos.
```

**8. Sticky móvil (bloque 20)**
```
Copy:    ¿Tu caso califica a la Ley 21.438? Te orientamos gratis.
Botón 1: Consultar mi caso
Botón 2: [ícono WhatsApp]
```
> Nota deliberada: dice **"Consultar mi caso"**, no "Agenda". Y **"te orientamos"**, no "te evaluamos". A una audiencia que llegó buscando cobertura estatal, "agendar" le suena a arancel.

---

# E. Estrategia específica para el artículo AUGE/Ley

## E.1 El problema, sin adornos

Se pidió franqueza, así que va sin filtro:

**Este es el peor candidato del sitio para convertirse en landing, y hay tres razones independientes que apuntan a lo mismo.**

**Razón 1 — La intención de búsqueda es institucional, no comercial. [DEDUCCIÓN]**
Las keywords declaradas (`:44`) incluyen literalmente `operacion guatita de delantal gratis`. Quien busca eso no está evaluando proveedores; está averiguando si el Estado le paga. La distancia entre esa intención y "pagar $1.977.990" es la máxima posible dentro del sitio.

**Razón 2 — Perfil socioeconómico. [DEDUCCIÓN]**
Uno de los requisitos que el propio artículo lista es "**Estar inscrito en FONASA** y tener red de atención pública asignada" (`:435`). El público objetivo de la página es, por construcción, usuario del sistema público.

**Razón 3 — y esta es la decisiva: contraindicación clínica.**
El artículo mismo dice (`:462`): el tratamiento no invasivo "no reemplaza la cirugía cuando el problema principal es el exceso de piel colgante o una diástasis grande". El paciente post-bariátrico con pannus **es exactamente ese caso**. Para la mayoría de este tráfico, el producto no está indicado.

Con eso sobre la mesa: **una landing agresiva en esta URL convertiría mal, y de los pocos que convirtiera, una fracción importante sería gente a la que después habría que decirle que no en la evaluación.** Ese es el peor resultado posible: gasto de agenda clínica, frustración del paciente y desgaste reputacional en una audiencia que habla entre sí en grupos de post-bariátricas.

## E.2 Y además, hay algo que perder

Esta URL no es solo tráfico. Según `docs/LINK_BUILDING_PLAN_2026.md`, el **Ángulo A** de la estrategia de prensa —el de máxima prioridad, dirigido a BBCL, Publimetro, La Tercera, Meganoticias, CHV y Cooperativa— es literalmente:

> "La alternativa no invasiva que buscan las chilenas que no califican al AUGE"

Un periodista de BBCL que llegue a esta URL y encuentre un publirreportaje no la enlaza. Encuentra una guía honesta con disclaimers, fuentes oficiales y un párrafo que dice "esto no reemplaza a la cirugía", **y ahí sí la enlaza**. La credibilidad de esta página **es** el activo de link building. Convertirla en landing destruye el Ángulo A.

## E.3 La estrategia recomendada: segmentar, no vender

Cuatro movimientos, en orden de importancia:

### E.3.1 Auto-triage por cuadro clínico (bloque 13 del wireframe)

En vez de un CTA único para todos, tres rutas según lo que el lector tiene. Solo una de las tres lleva a `/evaluacion`. Las otras dos entregan recursos gratuitos y útiles.

Por qué funciona:
- **No engaña.** No le dice a nadie que el tratamiento no invasivo reemplaza la cirugía. Al contrario, se lo dice explícitamente a quien corresponde.
- **No contradice el contenido.** Es la operacionalización visual del párrafo `:462`, que es justamente lo que hace creíble a la página.
- **Sube la calidad del lead.** Los que lleguen a `/evaluacion` por la Ruta 2 se auto-seleccionaron como "grasa + flacidez leve", que es el perfil real del producto.
- **Sube la señal de calidad para Google.** Un lector que hace clic a otra página del cluster en vez de rebotar a la SERP es exactamente la señal que se quiere.
- **Consolida el cluster.** Enlaza a `/bono-pad-guatita-de-delantal` (prioridad 0.90) y `/guatita-de-delantal-fonasa-isapre` (0.85), que hoy no reciben ni un enlace desde este artículo.

### E.3.2 Reencuadre costo/tiempo, no costo/precio

El error de framing sería comparar `$0 (Estado)` contra `$1.977.990 (Hebe)`. Se pierde siempre.

El encuadre correcto compara **rutas completas**:

| | Ley 21.438 (pública) | Cirugía privada | No invasivo (cuando está indicado) |
|---|---|---|---|
| Costo directo | Copago FONASA según tramo | $3.000.000 – $8.000.000 (`:460`) | $1.977.990 (`:462`) |
| Tiempo hasta empezar | Meses a años (`:454`) | Semanas | Días |
| Recuperación | 3-6 semanas, licencia | 3-6 semanas, licencia | Ninguna |
| Requisitos | Bariátrica previa + IMC estable + informes | Aptitud quirúrgica | Piel elástica, componente graso |
| **Resuelve piel colgante** | **Sí** | **Sí** | **No** |
| Anestesia general | Sí | Sí | No |

La última fila es la que hace honesta la tabla. Sin ella, la tabla es marketing. Con ella, es información — y de paso deja claro para quién sí sirve la vía no invasiva.

> ⚠ Los rangos de $3.000.000–$8.000.000 vienen del propio artículo (`:460`). Los copago FONASA **no** deben inventarse: si no hay fuente oficial verificable, la celda dice "según tu tramo FONASA" y se enlaza a fonasa.cl. **No poner cifras que no se puedan respaldar** — sería violar el compromiso declarado en `:408` y `:440`, que es el activo de confianza de la página.

### E.3.3 El lead magnet correcto: checklist de trámite, no descuento

Para esta audiencia, el "sin compromiso" clásico igual huele a venta. Lo que sí tiene valor percibido inmediato es algo que le sirva **para su trámite estatal**: la lista de documentos que le van a pedir en el CESFAM.

- Utilidad genuina, cero costo de producción (la información ya está en `:429-438`).
- Captura contacto para un KPI secundario, sin pedir intención de compra.
- Genera una relación que puede madurar: si en 8 meses sigue en lista de espera, ya existe un canal abierto.
- **No contradice nada.** Ayuda a postular mejor a la ley. Es lo opuesto a canibalizarla.

Marcar estos contactos con un `fuente` distinto en el webhook (ver G.4) para que **no** ensucien las métricas de leads P3 ni el CPL de Meta. Son de naturaleza distinta.

### E.3.4 La evaluación como "segunda opinión", no como consulta de venta

El framing verbal importa. En esta página, `/evaluacion` no se presenta como el primer paso de un plan de tratamiento sino como **una medición objetiva para saber en qué categoría estás**. De ahí el copy de D.2: *"Es una medición, no una venta"*.

## E.4 Lo que explícitamente NO se debe hacer en esta URL

| ❌ | Por qué |
|---|---|
| Poner el precio del Plan Zero Flacidez arriba, en el hero o en un sticky | Choque frontal con la expectativa de gratuidad. Rebote inmediato. |
| Sugerir que el tratamiento no invasivo "reemplaza" la cirugía | Falso, contradice `:462` y es riesgo sanitario y reputacional. |
| Insinuar que Método Hebe gestiona, agiliza o tramita la Ley 21.438 | Falso y potencialmente denunciable. |
| Cambiar el H1 o el title hacia algo comercial | Se pierde el ranking que produce el tráfico. Regla B3/B16. |
| Diluir o borrar el disclaimer de fuentes (`:407-409`, `:440`) | Es lo que hace linkeable la página para el Ángulo A. Regla B7. |
| Pop-up de captura | Regla B.4. Y en esta audiencia, mortal. |
| Poner cifras de copago o de lista de espera sin fuente oficial | Rompe el compromiso declarado en `:408`. |

## E.5 Expectativa realista de resultado

Con esta estrategia, **la tasa de conversión a lead P3 de esta URL va a seguir siendo baja** — [ESTIMACIÓN] muy por debajo de la de `/criolipolisis`, y eso es correcto y esperable.

Lo que sí debe subir:

| KPI | Hoy | Meta |
|---|---|---|
| Clic a otra página del cluster | ~0 (no hay enlaces a bono-PAD ni fonasa-isapre) | métrica principal |
| Contactos vía checklist | 0 | KPI secundario nuevo |
| **Calidad** del lead que sí llega a `/evaluacion` | desconocida (A.4) | debe ser medible y alta |
| Tiempo en página / scroll depth | desconocido | ↑ |
| Backlinks de prensa (Ángulo A) | 0 | 1-3 en 6 meses |

**Si alguien mide el éxito de esta página solo por leads P3, va a concluir que el rediseño fracasó.** Hay que acordar los KPI **antes** de implementar. Esto es un punto de conversación con el negocio, no una decisión técnica.

---

# F. Schema / JSON-LD a agregar

Reglas: se **amplía** el `@graph` existente, no se reemplaza (B8). Todo lo declarado en schema debe estar **visible** en la página (B9). Validar con `validator.schema.org` y con el Rich Results Test antes de mergear.

## F.1 Ampliar `FAQPage` (ambas páginas) — 🟢 riesgo nulo, valor alto

- **Criolipólisis:** de 9 a 11 preguntas. Nodo en `:121-196`.
- **AUGE:** de 5 a 8 preguntas. Nodo en `:121-164`.

**Regla dura:** cada `Question` nueva del schema debe tener su `.faq-item` visible correspondiente en el DOM, con el mismo texto. Sin excepción.

## F.2 Agregar `MedicalBusiness` con referencia a las 3 sedes — 🟢 riesgo bajo

Solo tiene sentido si se implementa el bloque de sedes visible (bloque 21 en criolipólisis). Copiar la estructura ya validada de `public/index.html:76-103` (que sobrevivió al fix del commit `b3b3fa0`, "corrige schema MedicalBusiness — 7 errores resueltos en validator.schema.org").

```jsonc
{
  "@type": "MedicalBusiness",
  "@id": "https://metodohebe.cl/#business",   // mismo @id del home → consolida la entidad
  "name": "Método Hebe",
  "url": "https://www.metodohebe.cl",
  "telephone": "+56963222683",
  "email": "contacto@metodohebe.cl",
  "priceRange": "$$",
  "image": "https://www.metodohebe.cl/img/logo-metodo-hebe.png",
  "address": { /* idéntico a index.html:88-95 */ },
  "areaServed": {"@type": "Country", "name": "Chile"}
  // ⚠ SIN aggregateRating — ver F.7
}
```

Reusar el mismo `@id` es intencional: los nodos con `@id` idéntico se consolidan como una sola entidad en el knowledge graph.

> 💡 **Ya existe un modelo interno probado.** `public/criolipolisis-los-angeles/index.html` tiene un nodo `["LocalBusiness","MedicalBusiness"]` con `@id` `#location-losangeles`, `PostalAddress`, `GeoCoordinates`, `OpeningHoursSpecification`, `areaServed` ×4 y `parentOrganization`. Es el único de las 7 páginas del cluster con schema local. Se puede tomar como referencia estructural — pero **con `@id` distinto** (`#business` nacional vs `#location-losangeles`), para no colisionar entidades ni reforzar la canibalización descrita en I.5.

## F.3 `Service` + `Offer` — 🟡 riesgo medio, solo en `/criolipolisis`

**Solo si se implementa la tarjeta de plan visible (bloque 16).** Precio en pantalla y precio en schema deben coincidir exactamente; un `Offer` sin precio visible es motivo de acción manual por structured data spam.

```jsonc
{
  "@type": "Service",
  "@id": "https://metodohebe.cl/criolipolisis/#service",
  "serviceType": "Criolipólisis",
  "name": "Criolipólisis en Método Hebe",
  "provider": {"@id": "https://metodohebe.cl/#business"},
  "areaServed": [
    {"@type":"City","name":"Santiago"},
    {"@type":"City","name":"Concón"},
    {"@type":"City","name":"Los Ángeles"}
  ],
  "offers": {
    "@type": "Offer",
    "name": "Plan Zero Rollito",
    "price": "1799990",
    "priceCurrency": "CLP",
    "availability": "https://schema.org/InStock",
    "url": "https://www.metodohebe.cl/planes",
    "description": "12 sesiones en 3 meses. iZED (criolipólisis), SkinWave MAX y Adipolite para grasa localizada."
  }
}
```
Valores tomados textualmente de `public/planes/index.html:109` y `:579-580`.

**❌ NO agregar `Offer` a `/guatita-de-delantal-auge-y-ley`.** Una página sobre cobertura estatal con un `Offer` de $1.977.990 en el schema es exactamente el tipo de señal contradictoria que erosiona la confianza — de Google y del lector.

## F.4 `Person` como autor / revisor médico — 🟢 riesgo nulo, **el de mayor valor E-E-A-T**

Hoy `author` es una `Organization` (`criolipolisis:106-110`, `auge:104-108`). En contenido YMYL médico eso es un techo.

```jsonc
"author": {
  "@type": "Person",
  "name": "NOMBRE REAL",
  "jobTitle": "CARGO REAL",
  "worksFor": {"@id": "https://metodohebe.cl/#organization"},
  "url": "https://www.metodohebe.cl/el-metodo"
},
"reviewedBy": {
  "@type": "Person",
  "name": "NOMBRE REAL",
  "jobTitle": "CARGO REAL"
}
```

> 🚨 **Bloqueante y no negociable.** Esto requiere una persona real, con nombre real, cargo real y credencial verificable, que acepte figurar públicamente, y su bloque visible correspondiente en la página (bloque 22). **Inventar un autor es fraude y es peor que no tener autor.** Si no hay persona disponible, este punto se descarta completo — schema y bloque visible — y se deja `Organization`.

## F.5 `HowTo` en el paso a paso de AUGE — 🟡 riesgo bajo-medio

El `<ol>` de `:446-452` es un procedimiento de 5 pasos, un caso de uso canónico de `HowTo`.

```jsonc
{
  "@type": "HowTo",
  "name": "Cómo postular a la Ley 21.438 (Ley Saín) de guatita de delantal",
  "totalTime": "P1Y",
  "step": [
    {"@type":"HowToStep","position":1,"name":"Consulta inicial en tu consultorio o CESFAM","text":"..."},
    /* ... 5 pasos, texto EXACTO del <ol> visible ... */
  ]
}
```

Google recortó fuertemente el rich result de `HowTo` en escritorio, así que el beneficio en SERP tradicional es limitado. **El valor real hoy es de AEO/GEO**: da a los LLM una estructura clara y citable del procedimiento. Alineado con el `llms.txt` que ya mantiene el sitio.

⚠ El texto de cada `HowToStep` debe ser el del `<ol>` visible, palabra por palabra.

## F.6 `ImageObject` + `og:image` + `twitter:image` — 🟢 riesgo nulo

Hoy **ninguna de las dos páginas tiene `og:image` ni `twitter:image`**, pese a declarar `twitter:card="summary_large_image"`. Es un bug de metadatos, no una decisión.

| Página | Imagen propuesta | Estado |
|---|---|---|
| `/criolipolisis` | `/img/sesion-criolipolisis-hiems.webp` | ya existe, sin usar |
| `/guatita-de-delantal-auge-y-ley` | `/img/resultado-flacidez-abdomen.webp` o una imagen editorial neutra | ya existe |

⚠ Idealmente generar versiones JPG/PNG 1200×630 (algunos scrapers de OG no leen WEBP). Ya existe el patrón de fallback JPG↔WEBP documentado en `CHANGES.md:12-13`.

Y agregar `ImageObject` al `@graph` para las imágenes del cuerpo, replicando lo que ya hace `resultados/index.html:182-242`.

## F.7 🔴 `aggregateRating` — **NO agregar. Recomendación en contra.**

Se pidió verificar antes de proponerlo. Verificado, y la respuesta es **no**, por tres motivos:

**1. Las cifras del propio sitio se contradicen.** Ver A.6: 20.000 vs 30.000 pacientes; 4,9★ vs 5/5; "+1.000 reseñas" vs `ratingCount: 120`. Hoy es imposible saber cuál es el número correcto leyendo el repo. Publicar un `aggregateRating` sobre una base que el propio sitio desmiente en otras cuatro páginas es indefendible si Google o el SERNAC preguntan.

**2. Elegibilidad.** El `aggregateRating` debe colgar de una entidad reseñable (`Product`, `LocalBusiness`, `Service`). En estas páginas la entidad principal es `MedicalWebPage`, sobre un **procedimiento médico**. Un rating agregado sobre "Criolipólisis" como procedimiento no es elegible para rich result y sí es candidato a acción manual por structured data spam.

**3. Riesgo asimétrico.** El upside es una estrellita en la SERP. El downside es una acción manual que puede afectar al dominio completo. Para un dominio con Authority Score 10 (`docs/LINK_BUILDING_PLAN_2026.md`), esa apuesta es mala.

**En su lugar:**
- Mantener `aggregateRating` **solo** donde ya está y donde sí corresponde: la ficha `LocalBusiness`/`MedicalClinic` de sede (`clinica-estetica-corporal-vitacura.html:113-117`), **después** de reconciliar el número con el Google Business Profile real.
- En los artículos, usar prueba social **visual sin schema**: chips, un testimonio con nombre y foto, la mención a "+X pacientes". Convierte igual y no expone a nada.
- Auditar por qué las otras dos sedes (Concón, Los Ángeles) **no** tienen `aggregateRating` mientras Vitacura sí. O lo tienen las tres con datos reales de su GBP, o ninguna.

## F.8 Resumen de schema

| Nodo | `/criolipolisis` | `/auge-y-ley` | Riesgo | Prioridad |
|---|---|---|---|---|
| `MedicalWebPage` (existente) | intacto | intacto | — | — |
| `BreadcrumbList` (existente) | intacto | intacto | — | — |
| `FAQPage` (existente) | ampliar 9→11 | ampliar 5→8 | 🟢 | Alta |
| `MedicalBusiness` | agregar | agregar | 🟢 | Media |
| `Service` + `Offer` | agregar | **❌ no** | 🟡 | Media |
| `Person` autor/revisor | agregar* | agregar* | 🟢 | **Alta** |
| `HowTo` | — | agregar | 🟡 | Baja |
| `ImageObject` | agregar | agregar | 🟢 | Media |
| `og:image` / `twitter:image` | agregar | agregar | 🟢 | **Alta** |
| `aggregateRating` | **❌ no** | **❌ no** | 🔴 | — |

\* solo con persona real que acepte figurar.

---

# G. Tracking y medición

## G.1 Restricción heredada — no romper (regla B15)

Estado actual, tras el commit `61403ba`:

```js
window.hebeTrack=function(n,p){
  gtag('event',n,p||{});
  if(typeof fbq!=='undefined'){
    var m={'whatsapp_click':'Contact'};
    if(m[n]) fbq('track',m[n],p||{});
    else     fbq('trackCustom',n,p||{});
  }
};
```

- GA4: **todos** los eventos pasan por `gtag('event', n, p)`.
- Meta: **solo** `whatsapp_click` → evento estándar `Contact`. Todo lo demás → `trackCustom`.
- El **único** `fbq('track','Lead')` legítimo del sitio está en `evaluacion.html:1846`, tras el submit del wizard, con `eventID` para deduplicación con CAPI.

**Todo evento nuevo debe pasar por `hebeTrack()`.** Nunca llamar `fbq('track','Lead')` directo desde un artículo. Nunca reintroducir `'evaluacion_click':'Lead'` ni `'cta_click':'Lead'` en el mapa.

## G.2 🔴 Prerrequisito bloqueante: arreglar la atribución de origen (hallazgo A.4)

Sin esto, **nada de lo que sigue se puede medir**, porque el lead que llega a n8n dice siempre `fuente: 'Landing Evaluación P3'` y `landing url: .../evaluacion`.

**Dos cambios, ambos en `public/evaluacion.html`:**

**(a)** Agregar al payload (`:1874-1893`):
```js
referrer: document.referrer || '',
origen_pagina: new URLSearchParams(location.search).get('origen') || '',
utm_source:   new URLSearchParams(location.search).get('utm_source')   || '',
utm_medium:   new URLSearchParams(location.search).get('utm_medium')   || '',
utm_campaign: new URLSearchParams(location.search).get('utm_campaign') || '',
```

**(b)** En los artículos, agregar un parámetro de origen a los enlaces hacia `/evaluacion`:
```
https://www.metodohebe.cl/evaluacion?origen=criolipolisis&bloque=tarjeta_plan
https://www.metodohebe.cl/evaluacion?origen=auge_ley&bloque=triage_ruta2
```

> ⚠ **Verificar antes de mergear** que agregar un query string no rompa nada del wizard. `evaluacion.html` es self-canonical (`:38`), así que Google no indexará las variantes; y el único `URLSearchParams` existente (`:1867`) solo lee `fbclid`, por lo que no debería haber conflicto. Aun así: probar el flujo completo hasta el submit antes de publicar.

**Nomenclatura sugerida de `bloque`:** `nav`, `banda_triage`, `cta_zonas`, `galeria`, `inline_cta`, `tarjeta_plan`, `cta_final`, `sticky`, `triage_ruta1|2|3`, `checklist`.

## G.3 Eventos GA4 nuevos por bloque

Todos vía `hebeTrack()` → llegan a GA4 y a Meta como `trackCustom`.

### `/criolipolisis`

| Bloque | Evento | Parámetros |
|---|---|---|
| Banda autoevaluación (07) | `evaluacion_click` | `{location:'banda_triage'}` |
| CTA zonas (11) | `evaluacion_click` | `{location:'cta_zonas'}` |
| Galería (13) — interacción | `gallery_interact` | `{location:'criolipolisis', zona:'abdomen'}` |
| Galería (13) — link a resultados | `internal_link_click` | `{location:'galeria', destino:'/resultados'}` |
| `.inline-cta` (14) | `evaluacion_click` | `{location:'inline_cta_resultados'}` ← **ya existe, no cambiar** |
| Tarjeta de plan (16) — primario | `evaluacion_click` | `{location:'tarjeta_plan'}` |
| Tarjeta de plan (16) — ghost | `internal_link_click` | `{location:'tarjeta_plan', destino:'/planes'}` |
| Sticky (28) | `evaluacion_click` | `{location:'mobile_sticky'}` ← **unificar**: hoy dispara `cta_click` con `location:'criolipolisis_mobile_sticky'` (`:752`), inconsistente con AUGE que usa `evaluacion_click`+`mobile_sticky` (`:587`) |
| Banner final (26) | `cta_click` | `{location:'criolipolisis_bottom'}` ← **ya existe** |

### `/guatita-de-delantal-auge-y-ley`

| Bloque | Evento | Parámetros |
|---|---|---|
| Índice (04) | `toc_click` | `{destino:'#requisitos'}` |
| Checklist (09) | `lead_magnet_click` | `{location:'checklist_documentos'}` |
| Checklist — envío | `lead_magnet_submit` | `{tipo:'checklist_ley_sain'}` ⚠ **no** debe disparar `Lead` en Meta |
| Triage ruta 1 (13) | `triage_click` | `{ruta:'quirurgico', destino:'/bono-pad-guatita-de-delantal'}` |
| Triage ruta 2 (13) | `evaluacion_click` | `{location:'triage_ruta2'}` ← la única comercial |
| Triage ruta 3 (13) | `triage_click` | `{ruta:'espera', destino:'/ejercicios-para-guatita-de-delantal'}` |
| `.inline-cta` (14) | `evaluacion_click` | `{location:'inline_cta_alternativas'}` ← **ya existe** |
| Sticky (20) | `evaluacion_click` | `{location:'mobile_sticky'}` ← **ya existe** |
| Banner final (18) | `evaluacion_click` | `{location:'cta_banner_final'}` ← **ya existe** |

### Scroll depth (ambas)

Reusar el patrón de `index.html:989-996`, ampliado a 25 / 50 / 75 / 90 %:
```js
hebeTrack('scroll_depth',{page:'criolipolisis', pct:50});
```
Es lo que permite responder "¿cuánta gente llega al bloque de precio?" — hoy imposible de saber.

## G.4 Segregar el lead del checklist (solo AUGE)

El contacto del checklist **no es** un lead P3. Mezclarlos rompe el CPL de Meta y las métricas comerciales.

- `fuente: 'Checklist Ley 21.438'` en el payload de n8n (distinto de `'Landing Evaluación P3'`).
- En Meta: `trackCustom('lead_magnet_submit')`. **Nunca** `fbq('track','Lead')`.
- En GA4: conversión **secundaria**, no la primaria.
- Ruta de n8n separada, o un branch por `fuente`, para que no entre al pipeline de agendamiento.

## G.5 Fix menor: `click_location` del evento WhatsApp (hallazgo A.5)

Agregar `id` o `data-section` a los contenedores para que el listener global (`:9-28`) deje de reportar `'home'`:

| Elemento | Atributo a agregar |
|---|---|
| `<div class="inline-cta">` (`criolipolisis:532`) | `data-section="cta_resultados"` |
| `<section class="cta-banner">` (`criolipolisis:675`) | `id="cta-final"` |
| `<div class="inline-cta">` (`auge:464`) | `data-section="cta_alternativas"` |
| `<section class="cta-banner">` (`auge:510`) | `id="cta-final"` |
| Cada bloque nuevo con enlace WhatsApp | `data-section="..."` |

Cero riesgo SEO. Recupera una dimensión de análisis que hoy está inutilizada.

## G.6 Cuadro de mando

| Métrica | Fuente | Antes | Después | Frecuencia |
|---|---|---|---|---|
| Posición media por consulta | Search Console | **capturar HOY** | comparar | Semanal |
| Impresiones y CTR por URL | Search Console | **capturar HOY** | comparar | Semanal |
| Consultas que traen tráfico | Search Console | **capturar HOY** | vigilar pérdidas | Semanal |
| Sesiones y scroll depth | GA4 | — | nuevo | Semanal |
| Clic a `/evaluacion` por bloque | GA4 (`location`) | parcial | completo | Semanal |
| Leads con `origen_pagina` | n8n | **imposible hoy** | nuevo | Semanal |
| Tasa lead → agendado → asistió | CRM | — | por origen | Mensual |
| INP / LCP / CLS | PageSpeed + CrUX | **capturar HOY** | comparar | Quincenal |
| Clic a otras páginas del cluster | GA4 | — | nuevo (KPI de AUGE) | Semanal |

**"Capturar HOY" significa antes de tocar una sola línea de HTML.** Sin línea base, cualquier cambio de posición se va a atribuir mal, en cualquiera de las dos direcciones.

---

# H. Plan de implementación por fases

## Fase 0 — Instrumentación y línea base (antes de cualquier cambio visible)

**Duración: 2-3 días. Riesgo SEO: nulo.**

| # | Tarea | Reversible |
|---|---|---|
| 0.1 | Exportar de Search Console: consultas, impresiones, CTR y posición de ambas URLs, últimos 6 meses, segmentado móvil/desktop | n/a |
| 0.2 | Correr PageSpeed Insights móvil y desktop en ambas. Guardar LCP, CLS, INP | n/a |
| 0.3 | **Arreglar la atribución de origen** (G.2) en `evaluacion.html` | Sí |
| 0.4 | Agregar `id`/`data-section` para el fix de `click_location` (G.5) | Sí |
| 0.5 | Implementar `scroll_depth` en ambas páginas (G.3) | Sí |
| 0.6 | Resolver A.6: decidir la cifra oficial de pacientes y de rating. Verificar contra el Google Business Profile real | n/a |
| 0.7 | Definir con el negocio los KPI de la página AUGE (ver E.5). **Decisión de negocio, no técnica** | n/a |

> Sin 0.1 no hay con qué comparar. Sin 0.3 no se puede atribuir ni un lead. **Fase 0 no es opcional.**

## Fase 1 — Quick wins de riesgo cero

**Duración: 1 día. Riesgo SEO: nulo. Todo reversible con `git revert`.**

| # | Tarea | Impacto esperado |
|---|---|---|
| 1.1 | **Arreglar el sticky CTA móvil** (A.3) en ambas páginas: mover la media query después de `shell.css`, agregar JS de `.visible` con `scrollY>400` (criolipólisis) / `>800` (AUGE), agregar `IntersectionObserver` que lo oculta en el footer, agregar `body{padding-bottom}` | 🔥 **El más alto de toda la propuesta** |
| 1.2 | Unificar el evento del sticky de criolipólisis a `evaluacion_click` + `location:'mobile_sticky'` | Coherencia analítica |
| 1.3 | Agregar `og:image` y `twitter:image` a ambas (F.6) | CTR en compartidos y previews |
| 1.4 | Corregir `og:url` para que coincida con el canonical (sin slash) | Higiene |
| 1.5 | Agregar enlace `/criolipolisis` → `/resultados` en la sección "antes y después" | Arquitectura interna |
| 1.6 | Agregar enlaces `/auge-y-ley` → `/bono-pad-guatita-de-delantal` y `/guatita-de-delantal-fonasa-isapre` | Arquitectura interna |

> **Recomendación fuerte: 1.1 se despliega solo, sin acompañamiento.** Es el cambio de mayor impacto de conversión de todo el plan y conviene poder atribuírselo limpiamente. Además revela si el sticky bar realmente funciona, dato que hoy nadie tiene porque nunca se ha mostrado.

## Fase 2 — Bloques nuevos en `/criolipolisis`

**Duración: 3-5 días. Riesgo SEO: bajo. Prerrequisito: Fases 0 y 1, más ≥7 días de datos post-1.1.**

| # | Tarea | Bloque |
|---|---|---|
| 2.1 | Chips en el hero | 04 |
| 2.2 | Banda de autoevaluación | 07 |
| 2.3 | Figura `sesion-criolipolisis-hiems.webp` con `width`/`height` | 09 |
| 2.4 | CTA contextual de zonas | 11 |
| 2.5 | **Galería antes/después** (reusa el markup de `resultados`) | 13 |
| 2.6 | **Tarjeta Plan Zero Rollito** | 16 |
| 2.7 | Micro-bloque de confianza | 19 |
| 2.8 | Tarjetas de sede | 21 |
| 2.9 | Bloque de enlaces relacionados | 25 |
| 2.10 | 2 FAQ nuevas (visible + schema) | 23 |
| 2.11 | Ajuste de copy del `<p>` del `.inline-cta` | 14 |
| 2.12 | Schema: `MedicalBusiness`, `Service`+`Offer`, `ImageObject`, `FAQPage` ampliado | F.1-F.3, F.6 |

**Orden interno recomendado:** 2.5 y 2.6 primero (mayor impacto), medir 7 días, después el resto. **No desplegar los 12 cambios el mismo día**; si la posición se mueve, no habrá forma de saber cuál lo causó.

## Fase 3 — Bloques nuevos en `/guatita-de-delantal-auge-y-ley`

**Duración: 3-5 días. Riesgo SEO: bajo-medio. Prerrequisitos: Fase 0, Fase 1, y KPI acordados (0.7).**

| # | Tarea | Bloque |
|---|---|---|
| 3.1 | Chips de credibilidad en el hero | 02 |
| 3.2 | Índice navegable + `id` en los H2 existentes | 04 |
| 3.3 | Tabla comparativa AUGE/GES vs Ley 21.438 | 07 |
| 3.4 | Bloque puente honesto | 11 |
| 3.5 | **Auto-triage de 3 rutas** | 13 |
| 3.6 | Tabla comparativa de rutas (costo/tiempo/recuperación) | E.3.2 |
| 3.7 | 3 FAQ nuevas (visible + schema) | 15 |
| 3.8 | Bloque "sigue leyendo" del cluster | 17 |
| 3.9 | Ajustes de copy de `.inline-cta` y `.cta-banner` | 14, 18 |
| 3.10 | Schema: `HowTo`, `MedicalBusiness`, `FAQPage` ampliado | F.1, F.2, F.5 |
| 3.11 | Checklist descargable (**diferible a Fase 4** si no hay endpoint) | 09 |

**Regla especial para esta página: monitoreo semanal durante 8 semanas, no 4.** Es contenido normativo, más frágil ante cambios de tono, y es el activo del Ángulo A de link building.

## Fase 4 — E-E-A-T y activos adicionales

**Duración: variable. Depende de disponibilidad de personas reales.**

| # | Tarea |
|---|---|
| 4.1 | Bloque autor/revisor con persona real + schema `Person` (F.4). **Bloqueado hasta que haya persona** |
| 4.2 | Checklist descargable con endpoint n8n (E.3.3, G.4) |
| 4.3 | Reconciliar `aggregateRating` en las 3 sedes con datos reales de GBP (F.7) |
| 4.4 | Fotos de sede reales en las tarjetas del bloque 21 |
| 4.5 | Propagar el fix del sticky CTA a las otras ~28 páginas afectadas (A.3) |

## H.5 Reversibilidad

| Cambio | Cómo se revierte | Coste |
|---|---|---|
| Bloques nuevos de HTML | `git revert` | Trivial |
| CSS y JS | `git revert` | Trivial |
| Ajustes de copy en CTAs | `git revert` | Trivial |
| Nodos JSON-LD nuevos | `git revert` + re-crawl | Bajo (días) |
| `og:image` / `twitter:image` | `git revert` | Trivial |
| Cambio de `<title>` o `meta description` | `git revert` + re-crawl | **Medio** (1-3 semanas para reconsolidar) |
| **Cambio de URL o canonical** | **Prácticamente irreversible** | **Alto** — por eso es regla B1/B2 |

Todo lo que propone este documento está en las filas reversibles. **Nada toca URL ni canonical.**

## H.6 Ventana de evaluación

| Momento | Qué se mira | Qué se decide |
|---|---|---|
| **T+0** | Línea base (Fase 0) | — |
| **T+7 días** | Indexación (`site:` + Search Console), errores de schema, Core Web Vitals, clics a `/evaluacion` | Rollback inmediato si hay caída de indexación o error de schema |
| **T+14 días** | Posición media, CTR, primeros leads con `origen_pagina` | Ajustes de copy |
| **T+30 días** | Posición media estabilizada, tasa de clic a `/evaluacion`, scroll depth | **Primera evaluación real.** Antes de 30 días la variabilidad de la SERP domina la señal |
| **T+60 días** | Tendencia de posiciones, leads por origen, calidad del lead | Escalar el patrón al resto del cluster, o revertir |
| **T+90 días** | Consolidación, backlinks del Ángulo A | Decisión estratégica |

> **No se juzga nada antes de los 30 días.** Es el error más común y lleva a revertir cambios buenos por ruido normal de la SERP.

---

# I. Riesgos SEO reales y mitigación

## I.1 🟡 Dilución de la señal editorial → percepción de contenido comercial

**Riesgo real.** Los sistemas de Google (y los LLM) evalúan la proporción entre contenido informativo y promocional. Se pasa de 1 bloque comercial a 4 en criolipólisis.

**Por qué el riesgo es acotado aquí:**
- El word count **solo sube** (3.671 → ~3.950 y 1.970 → ~2.700). La proporción comercial/informativo se mantiene razonable.
- Los bloques nuevos no son puro CTA: la banda de autoevaluación, la galería y las tarjetas de sede son contenido con valor propio.
- Las citas científicas quedan intactas (B6).

**Mitigación:**
- Límite duro de 5 puntos de conversión dentro del `<article>` (B.4.5).
- Nunca reemplazar texto por CTA. Solo insertar (B20).
- Ningún CTA entre un H2 y su primer párrafo — eso sí lee como publirreportaje.
- Auditar el ratio tras la Fase 2: si los bloques comerciales superan ~15% del alto de la página, retirar uno.

## I.2 🔴 Riesgo mayor: cambio de tono en la página AUGE

**Este es el riesgo más serio de toda la propuesta, y no es técnico.**

`/guatita-de-delantal-auge-y-ley` rankea porque es honesta: dice que la ley no es AUGE, que las esperas son largas, que el tratamiento no invasivo no reemplaza la cirugía, y declara sus fuentes. Si el rediseño baja aunque sea un poco esa honestidad, se pierde justo lo que la hace única.

**Mitigación:**
- Reglas B7 y B10: disclaimer y enlaces a `bcn.cl`/`fonasa.cl` intocables.
- Las 3 rutas del triage: **2 de 3 no venden nada**. Es la garantía estructural del equilibrio.
- La fila "resuelve piel colgante: No" en la tabla comparativa (E.3.2). Sin ella, la tabla es marketing.
- Prohibiciones explícitas de E.4.
- **Revisión editorial humana antes del merge**, con una sola pregunta: *"¿un periodista de BBCL enlazaría esta página?"* Si la respuesta es no, se retrocede.

## I.3 🟡 Intrusive interstitials en móvil

Google penaliza interstitials intrusivos. Un sticky bar razonable no cae ahí, pero un sticky mal dimensionado sí.

**Mitigación:** las 6 reglas de B.4. Especialmente: ≤15% del viewport, nunca antes de 400 px de scroll, se oculta en el footer, cero pop-ups. Medir el alto real en un iPhone SE (667 px) antes de publicar.

## I.4 🟡 Regresión de Core Web Vitals (CLS y LCP)

Agregar imágenes y bloques nuevos puede degradar CLS y LCP. Ya hubo un commit dedicado a esto: `aca5b29` "fix(seo): optimizar carga de páginas lentas (>6s)".

**Mitigación:**
- `width` y `height` explícitos en **toda** imagen nueva (B23). Es la causa #1 de CLS.
- `loading="lazy"` en todo lo que esté bajo el fold; **nunca** en la imagen LCP.
- La galería antes/después reusa el `<picture>` webp+jpg con lazy `IntersectionObserver` de `resultados/index.html:997-1008` — ya probado.
- El sticky es `position:fixed` → **no** aporta CLS. Pero el `body{padding-bottom}` correspondiente debe estar en el CSS inicial, no agregado por JS (eso sí genera shift).
- Las animaciones de entrada por `IntersectionObserver` (`criolipolisis:774-782`) usan `opacity` + `transform`, que no provocan layout shift. Mantener ese patrón.
- Medir con PageSpeed antes y después de cada fase.
- Ninguna fuente nueva. Ya se cargan Inter + Playfair Display + Pacifico (`:78`) — de hecho, `Pacifico` se carga pero **el CSS declara `--sans:'DM Sans'`, que no está en el `<link>` de Google Fonts**. Hay peso desperdiciado ahí; vale una auditoría aparte.

## I.5 🟡 Canibalización con `/criolipolisis-los-angeles`

Se auditó `public/criolipolisis-los-angeles/index.html` (804 líneas, ~2.371 palabras) contra `/criolipolisis` (786 líneas, 3.671 palabras).

| | `/criolipolisis` | `/criolipolisis-los-angeles` |
|---|---|---|
| `<title>` | Criolipólisis en Chile: Qué Es, **Precio**, Resultados y Contraindicaciones | Criolipólisis en **Los Ángeles**: grasa localizada sin cirugía con **iZED** |
| H1 | `:446` Criolipólisis: qué es, cómo funciona y cuándo realmente elimina grasa | `:461` Criolipólisis en Los Ángeles: grasa localizada sin cirugía con tecnología iZED |
| Intención | Informacional-comercial nacional | **Transaccional local** (Biobío) |
| Canonical | self, sin slash | self, sin slash (`:51`) |
| Schema distintivo | — | **`["LocalBusiness","MedicalBusiness"]`** con `GeoCoordinates`, `OpeningHoursSpecification` y `areaServed` ×4 (Los Ángeles, Angol, Nacimiento, Mulchén) |
| Precio | $1.799.990 vía enlace a `/planes` (`:553`) | `.price-card` propia, $1.799.990 (`:547`) |
| Prioridad sitemap | 0.95 (`sitemap.xml:21`) | 0.80 (`sitemap.xml:228`) |
| `lastmod` | 2026-04-23 | 2026-04-17 |

**Solapamiento medido: 5 de 13 H2 son conceptualmente equivalentes** (qué es, mecanismo/apoptosis, zonas tratables, contraindicaciones, FAQ). En las FAQ solo hay **1 pregunta casi idéntica**, y está geo-modificada ("¿Cuánto cuesta la criolipólisis en Los Ángeles?"), no duplicada.

### Veredicto: riesgo BAJO-MODERADO y gestionable

**Lo que ya protege:**
- Canonicals correctos, self-referencing y distintos.
- Modificador geográfico presente en title, H1, description, URL y schema.
- El bloque `LocalBusiness` + `GeoCoordinates` es exclusivo de la local: señal inequívoca para Google de que esa URL sirve consultas locales.
- La local **enlaza contextualmente hacia la nacional** (`:492`, `inline-link`), estableciendo la jerarquía hijo→padre correcta.

**Lo que sí genera riesgo [VERIFICADO]:**
1. **~35-40% del cuerpo de la local es explicación genérica del mecanismo** (apoptosis, temperaturas, tiempos) prácticamente 1:1 con la nacional. Para la consulta `criolipolisis` a secas, Google puede oscilar entre ambas.
2. **La nacional NO enlaza a la local.** `criolipolisis/index.html:737` enlaza a `/guatita-de-delantal-auge-y-ley` pero no a `/criolipolisis-los-angeles`. Falta el vínculo padre→hijo que consolidaría el cluster local.
3. **El sitemap contradice la intención:** la local tiene menor prioridad (0.80) y `lastmod` más antiguo, siendo la de intención comercial más alta.

**El riesgo aumenta ligeramente con esta propuesta**, porque el bloque 21 agrega contenido de sedes a la página nacional.

**Mitigación:**
- Tarjetas de sede del bloque 21 **breves**: nombre, dirección, enlace. Nada de párrafos sobre "criolipólisis en Los Ángeles".
- Anchor **local-específico** hacia la página local ("Criolipólisis en Los Ángeles", nunca "criolipólisis" a secas). Esto además cierra el punto 2 y es una mejora neta de arquitectura.
- La nacional **no** optimiza para `criolipolisis los angeles`; la local **no** intenta rankear para `criolipolisis`.
- **Acción recomendada, fuera del alcance de esta propuesta:** recortar las secciones de mecanismo de la local a 2-3 párrafos de resumen + enlace a la nacional como fuente canónica, y expandirla con contenido genuinamente local (cómo llegar, referencias del Biobío, casos de la sede). Hoy la local ni siquiera enlaza a `/grasa-localizada-los-angeles`, su hermana local natural.
- ⚠ El mismo patrón existe para celulitis, flacidez y grasa localizada (`celulitis-vitacura`, `celulitis-concon`, `celulitis-los-angeles`, `grasa-localizada-*`, `flacidez-corporal-*`). Es una decisión de arquitectura previa; esta propuesta no la resuelve, solo evita empeorarla.

## I.6 🟡 Canibalización dentro del cluster guatita

Seis URLs sobre el mismo tema, con contenido y prioridad medidos:

| URL | Prioridad | Palabras | `.inline-cta` | Ángulo único |
|---|---|---|---|---|
| `/que-es-la-guatita-de-delantal-y-como-puedes-solucionarlo` | **0.75** (`:289`) | **~1.416** | 1 | Hub / visión general |
| `/guatita-de-delantal-auge-y-ley` | 0.80 (`:40`) | 1.970 | 1 | Normativa Ley 21.438 |
| `/ejercicios-para-guatita-de-delantal` | 0.80 (`:28`) | ~1.883 | **0** | Rutina casera |
| `/guatita-de-delantal-operacion-vs-tratamiento` | 0.85 (`:34`) | ~2.629 | 1 | Decisión clínica |
| `/guatita-de-delantal-fonasa-isapre` | 0.85 (`:52`) | ~2.158 | 1 | Cobertura de seguros |
| `/bono-pad-guatita-de-delantal` | **0.90** (`:46`) | ~2.506 | 1 | Mecanismo de financiamiento |

**Buena noticia: cada página tiene un ángulo único y defendible.** El cluster está bien concebido temáticamente y el riesgo de canibalización por contenido duplicado es bajo. El problema es de arquitectura, no de solapamiento:

> 🔴 **Anomalía confirmada:** la pillar page declarada en `llms.txt:147` es `/que-es-la-guatita-de-delantal-y-como-puedes-solucionarlo`, y es simultáneamente **la más corta del cluster (~1.416 palabras, un 40% menos que sus hijas) y la de menor prioridad en el sitemap (0.75)**, por debajo de sus 5 satélites. Es la que recibe todos los enlaces internos del cluster y la que menos autoridad declara. Una pillar page no puede ser el contenido más delgado de su propio cluster. Debería estar en 0.90-0.95 y con contenido acorde a ese rol. **Fuera del alcance de esta propuesta, pero es el problema estructural más grande del cluster guatita.**

**Riesgo específico de esta propuesta:** el auto-triage (bloque 13) puede solaparse con `/guatita-de-delantal-operacion-vs-tratamiento`, que ya trae una tabla comparativa completa (`:463-490`) y ~2.629 palabras sobre esa decisión.

**Mitigación:**
- El triage debe ser **navegacional** (2-3 líneas por ruta + enlaces), **no** un ensayo comparativo. La comparación profunda vive en la otra URL: hay que enlazarla, no duplicarla.
- Mismo criterio para la tabla costo/tiempo de E.3.2: breve, enfocada en las tres **rutas de acceso** (pública / privada / no invasiva), no en la comparación clínica detallada. Si crece, se recorta o se reemplaza por un enlace.
- Cada página conserva su ángulo: AUGE = normativa; operacion-vs-tratamiento = decisión clínica; fonasa-isapre = cobertura de seguros; bono-pad = financiamiento; ejercicios = complemento; hub = visión general.
- La propuesta **refuerza** el cluster al agregar los enlaces internos que hoy faltan desde AUGE (`bono-pad`, `fonasa-isapre`).

## I.7 🟢 Thin content — riesgo bajo, pero vale nombrarlo

`/guatita-de-delantal-auge-y-ley` tiene 1.970 palabras. No es thin, pero está en la zona baja para una consulta normativa donde compiten fuentes gubernamentales y medios.

La propuesta lo lleva a ~2.700 sin borrar nada. **Esto reduce el riesgo, no lo aumenta.**

⚠ Cuidado con el sentido contrario: si al implementar se decide "simplificar" alguna sección para hacer espacio a los bloques nuevos, se vuelve a caer. Regla B5: el word count solo sube.

## I.8 🟡 Riesgo de contenido normativo desactualizado

Ambas páginas declaran `dateModified: 2026-04-23`. La de AUGE dice "estado 2026" y "requisitos vigentes". Estamos a **2026-07-27**: tres meses de antigüedad en contenido normativo que puede cambiar por circular del Minsal.

**Mitigación:**
- Al tocar la página, **actualizar `dateModified`** en el JSON-LD (`:91-92`) y en `article:modified_time` (`:57`) — pero **solo si el contenido realmente se revisó**. Cambiar la fecha sin revisar es un patrón que Google detecta y castiga.
- Aprovechar el rediseño para **verificar el reglamento vigente en bcn.cl**. Es la ocasión natural.
- Establecer una revisión trimestral de esta URL. Es la única del sitio cuyo contenido puede quedar factualmente incorrecto por un acto administrativo ajeno.

## I.9 🟢 Riesgo de schema

`Offer` con precio que no coincide con el visible, `aggregateRating` no elegible, `HowTo` con texto que no está en la página.

**Mitigación:** reglas B9 y F.7. Validar en `validator.schema.org` **y** en el Rich Results Test antes de mergear. Precedente: el commit `b16059c` ("12 errores SEMrush") muestra que este tipo de deuda ya apareció antes en este repo.

## I.10 Matriz resumen

| Riesgo | Prob. | Impacto | Mitigación principal |
|---|---|---|---|
| Cambio de tono en AUGE | Media | **Alto** | B7 + revisión editorial humana + 2 de 3 rutas no venden |
| Dilución editorial en criolipólisis | Baja | Medio | Límite de 5 CTAs, solo insertar |
| Interstitial intrusivo móvil | Baja | Medio | 6 reglas de B.4 |
| Regresión de CLS/LCP | Media | Medio | `width`/`height`, lazy, medir por fase |
| Canibalización local | Baja | Bajo | Anchors local-específicos, tarjetas breves |
| Canibalización de cluster | Media | Bajo | Triage navegacional, no comparativo |
| Schema inválido | Baja | Medio | Validar antes de mergear |
| Contenido normativo desactualizado | **Alta** | Medio | Verificar en bcn.cl + revisión trimestral |
| **No poder medir nada (A.4)** | **Alta si se salta la Fase 0** | **Alto** | **Fase 0 es obligatoria** |

---

# Anexo — Resumen de hallazgos accionables fuera del alcance directo

Detectados durante la auditoría. No son parte de la propuesta, pero conviene registrarlos.

| # | Hallazgo | Evidencia | Severidad |
|---|---|---|---|
| X1 | El sticky CTA móvil está roto en ~30 páginas que cargan `shell.css` | A.3 | 🔴 Alta |
| X2 | `/resultados` —el patrón CRO de referencia— también lo tiene roto | A.3 | 🔴 Alta |
| X3 | El lead de n8n no captura origen, referrer ni UTM | A.4 | 🔴 Alta |
| X4 | `click_location` del evento WhatsApp reporta `'home'` en todos los artículos | A.5 | 🟡 Media |
| X5 | Cifras de prueba social contradictorias (20.000 vs 30.000; 4,9 vs 5/5; 120 vs +1.000 reseñas) | A.6 | 🟡 Media |
| X6 | Ninguna de las 2 páginas (ni `/resultados`) tiene `og:image` pese a declarar `summary_large_image` | A.1, A.2 | 🟡 Media |
| X7 | `--sans:'DM Sans'` declarado en CSS pero no cargado en el `<link>` de Google Fonts; sí se carga `Pacifico`, aparentemente sin uso | `criolipolisis:78`, `:216` | 🟢 Baja |
| X8 | `og:url` con trailing slash vs canonical sin slash | `criolipolisis:47` vs `:53` | 🟢 Baja |
| X9 | JSON-LD usa `https://metodohebe.cl/...` (sin `www`, con slash) mientras el canonical usa `https://www.metodohebe.cl/...` (con `www`, sin slash) | `criolipolisis:87-89` vs `:47` | 🟢 Baja |
| X10 | **La pillar del cluster guatita es la página más corta (~1.416 palabras) y la de menor prioridad (0.75) de su propio cluster** | I.6 | 🟡 Media |
| X11 | `aggregateRating` solo en la sede Vitacura; Concón y Los Ángeles no lo tienen | F.7 | 🟢 Baja |
| X12 | `clinicahebe.cl` sigue sin redirigir 301 → 46 backlinks de 24 dominios sin consolidar | `docs/LINK_BUILDING_PLAN_2026.md` | 🔴 Alta (fuera del repo) |
| X13 | Semrush MCP no disponible en el plan actual | Sección 0 | 🟡 Media |
| X14 | **`/ejercicios-para-guatita-de-delantal` no tiene ningún `.inline-cta`**: 1.883 palabras hasta el primer CTA real (el `.cta-banner` del final). Única del cluster sin CTA intermedio | `public/ejercicios-para-guatita-de-delantal/index.html` | 🟡 Media |
| X15 | Contradicción de precios **dentro del mismo documento**: `public/lipoescultura-sin-cirugia/index.html:597` dice protocolo completo `$800.000–$2.500.000` y `:611` dice `$800.000–$3.000.000` | — | 🟡 Media |
| X16 | Falta schema `HowTo` en `/ejercicios-para-guatita-de-delantal`: una rutina de 8 ejercicios estructurada sin marcado de instrucciones | — | 🟢 Baja |
| X17 | Auto-enlaces en el footer de contenidos relacionados: `que-es-la-guatita.../index.html:654`, `bono-pad-guatita-de-delantal/index.html:633`, `lipoescultura-sin-cirugia/index.html:697` enlazan a sí mismas | — | 🟢 Baja |
| X18 | `/criolipolisis` no enlaza a `/criolipolisis-los-angeles` (falta el vínculo padre→hijo); `/criolipolisis-los-angeles` tampoco enlaza a `/grasa-localizada-los-angeles` | I.5 | 🟢 Baja |
| X19 | El anchor de los 49 enlaces de footer hacia cada URL objetivo es idéntico y sitewide. Google los descuenta: el equity real viene de los 16 (criolipólisis) y 10 (AUGE) enlaces contextuales | B.5 | 🟢 Baja (informativo) |
| X20 | `/blog/guatita-delantal-tratamiento-sin-cirugia` (sitemap `:144`) coexiste con la pillar del cluster. Revisar solapamiento temático | — | 🟢 Baja |

**Falso positivo descartado durante la auditoría:** se sospechó que `ejercicios-para-guatita-de-delantal/index.html:519` → `/flacidez` estaba roto, porque existe `public/flacidez.html` y no un directorio `flacidez/`. **Verificado: no está roto.** `vercel.json` tiene `"cleanUrls": true`, que resuelve `/flacidez` → `public/flacidez.html`. Lo mismo aplica al enlace `/flacidez` de `guatita-de-delantal-auge-y-ley/index.html:462`.

---

**Fin del documento.**
