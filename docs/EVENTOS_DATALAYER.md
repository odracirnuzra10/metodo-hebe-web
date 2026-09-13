# Eventos dataLayer — Método Hebe

Inventario de lo que el sitio **ya dispara** (T6.1) y especificación de los eventos de la propuesta G.3 / G.6 (T6.2).

No hay un cuadro de mando construido en este repo. G.6 lista **fuentes** (Search Console, GA4, n8n, CrUX) que Ricardo consulta con sus cuentas. Esta página no es ese tablero.

Contenedor único: GTM `GTM-TZC56NQ5`. WhatsApp único: `56963222683`. Medir por URL (R2). No crear un GTM Hebe-only.

Helper: `hebeTrack(nombre, params)` → `gtag('event', …)` (GA4) y, si existe Pixel, `fbq('track','Contact')` solo si el nombre es `whatsapp_click`; el resto va como `fbq('trackCustom', nombre)`. El único `fbq('track','Lead')` está en el submit del wizard de `/evaluacion` (B15).

Snippet JSON de la especificación: `docs/datalayer-spec.json`.

## T6.3 — n8n

Host `n8n.oacg.cl`. Los dos magnet/franquicia ya aceptan POST (2026-09-13):

| Path | Destino | Qué no hace |
|---|---|---|
| `POST /webhook/franquicia-lead` | Gmail `contacto@metodohebe.cl` | No Clinera, no tabla P3, no Meta Lead |
| `POST /webhook/checklist-ley-21438` | Gmail `contacto@metodohebe.cl` · `fuente: 'Checklist Ley 21.438'` | Igual. Nunca `fbq('Lead')` |

`/franquicia` apunta al primero; si el POST falla, queda `mailto:contacto@metodohebe.cl`. AUGE (`#checklist`) apunta al segundo y muestra la lista de documentos en la página.

Los webhooks P3 de `/evaluacion` (`lead-capture`, `link-pago-evaluacion`, `pago-evaluacion`) no se tocan aquí.

## Evento → disparador → destino

| Evento | Disparador | Destino | Notas |
|---|---|---|---|
| `page_view` / `gtm.js` | Carga de página | GA4 `G-NGW7210RXB`, GTM, Pixel PageView | Por path (R2) |
| `evaluacion_click` | Clic a `/evaluacion` (nav, hero, inline, sticky, triage ruta 2, tarjeta de plan, etc.) | GA4 + Meta `trackCustom` | `location` distingue el bloque. En AUGE: `triage_ruta2`, `inline_cta_alternativas`, `cta_banner_final` + `?origen=auge_ley` (KPI R4, comentar no tablero) |
| `whatsapp_click` | Clic a `wa.me` / WhatsApp **real** | GA4 + Meta `Contact` | No usarlo en botones que van a `/evaluacion` |
| `contacto_whatsapp_2026` | Listener global en `a[href*="whatsapp"], a[href*="wa.me"]` | `dataLayer` → GTM | `click_location` usa `section` / `[data-section]` / `main`; si no hay, cae en `'home'` |
| `cta_click` | CTAs que no son evaluación (planes, resultados, banner criolipólisis) | GA4 + Meta `trackCustom` | p. ej. `location:'criolipolisis_bottom'` |
| `internal_link_click` | Galería → `/resultados`, relacionados, sedes, ghost de plan | GA4 + Meta `trackCustom` | `{location, destino}` |
| `gallery_interact` | Toggle de la galería en `/criolipolisis` | GA4 + Meta `trackCustom` | `{location:'criolipolisis', zona:'abdomen'}` |
| `triage_click` | Rutas 1 y 3 del auto-triage AUGE | GA4 + Meta `trackCustom` | No comercial. `{ruta, destino}` |
| `toc_click` | Índice de AUGE | GA4 + Meta `trackCustom` | `{destino:'#…'}` |
| `phone_click` | `tel:` del topbar | GA4 + Meta `trackCustom` | |
| `scroll_depth` | 25 / 50 / 75 / 90 % en criolipólisis y AUGE | GA4 + Meta `trackCustom` | `{page, pct}` |
| `Lead` | Submit del wizard `/evaluacion` (paso 3) | Meta `Lead` + n8n `lead-capture` | **Único Lead.** No en sticky, no en checklist |
| `InitiateCheckout` / `ViewContent` | Pasos del wizard `/evaluacion` | Meta estándar | No son `hebeTrack` |
| n8n `lead-capture` | Mismo submit P3 | n8n → pipeline agenda | `fuente: 'Landing Evaluación P3'` |
| n8n `link-pago-evaluacion` / `pago-evaluacion` | Pago P3 | n8n | URLs `[REDACTED]` |
| n8n `franquicia-lead` | Submit `/franquicia` | n8n → Gmail clínica | Mailto solo si el POST falla |
| `lead_magnet_click` / `lead_magnet_submit` | Checklist AUGE `#checklist` (G.3 / G.4) | GA4 + Meta `trackCustom` + n8n `checklist-ley-21438` | Nunca `Lead` |

## G.3 — bloques de las landings híbridas

### `/criolipolisis`

| Bloque | Evento | Parámetros |
|---|---|---|
| Autoeval | `evaluacion_click` | `{location:'banda_triage'}` |
| CTA zonas | `evaluacion_click` | `{location:'cta_zonas'}` |
| Galería | `gallery_interact` | `{location:'criolipolisis', zona:'abdomen'}` |
| Galería → resultados | `internal_link_click` | `{location:'galeria', destino:'/resultados'}` |
| `.inline-cta` | `evaluacion_click` | `{location:'inline_cta_resultados'}` |
| Tarjeta plan | `evaluacion_click` / `internal_link_click` | `{location:'tarjeta_plan'}` |
| Sticky | `evaluacion_click` | `{location:'mobile_sticky'}` |
| Banner | `cta_click` | `{location:'criolipolisis_bottom'}` |

### `/guatita-de-delantal-auge-y-ley`

| Bloque | Evento | Parámetros |
|---|---|---|
| Índice | `toc_click` | `{destino:'#…'}` |
| Checklist | `lead_magnet_click` / `lead_magnet_submit` | `{location:'checklist_documentos'}` / `{tipo:'checklist_ley_sain'}` |
| Triage 1 / 3 | `triage_click` | `{ruta:'quirurgico'\|'espera', destino}` |
| Triage 2 | `evaluacion_click` | `{location:'triage_ruta2'}` |
| `.inline-cta` | `evaluacion_click` | `{location:'inline_cta_alternativas'}` |
| Sticky | `evaluacion_click` | `{location:'mobile_sticky'}` |
| Banner | `evaluacion_click` | `{location:'cta_banner_final'}` |

## G.6 — qué mirar (no es un dashboard)

Cuando Ricardo tenga GSC / GA4 abiertos:

| Métrica | Fuente |
|---|---|
| Posición, impresiones, CTR, consultas | Search Console por URL |
| Sesiones y `scroll_depth` | GA4 |
| Clic a `/evaluacion` por `location` | GA4 |
| Leads con `origen` / `fuente` | n8n (P3 ≠ franquicia ≠ checklist) |
| LCP / CLS / INP | PageSpeed + CrUX |
| Clic a páginas del cluster AUGE | GA4 `internal_link_click` / `triage_click` |

KPI R4 (solo comentario de tracking en AUGE): % de sesiones AUGE que llegan a `/evaluacion` con origen AUGE; +20 % relativo vs semana 1; 8 semanas; guardrail WhatsApp no sube.

Share of Model mes 0: `docs/SHARE_OF_MODEL_MES0.md` (Ricardo llena; no inventar filas).
