# Plan de Link Building Método Hebe — 4 meses (2026)

Documento operativo interno. No es contenido del sitio público. Complementa el plan SEO/AEO ejecutado el 2026-04-23.

## Diagnóstico

- AS propio (metodohebe.cl): 10/100.
- Competidores con perfiles igualmente pobres (URL shorteners moldavos, spam SEO en .sbs / .top / .icu).
- Espacio abierto: con 15-25 backlinks de calidad el dominio supera el promedio del mercado estético chileno.
- Dominio antiguo **clinicahebe.cl** con 46 backlinks de 24 dominios — la equidad se preserva sólo si hay 301 real a metodohebe.cl (ver sección "Redirect Pendiente" al final).

## TIER 1 — Prensa chilena (máxima prioridad, 2-3 meses)

Pitchear a 5-6 medios con 3 ángulos diferenciados.

### Ángulo A — AUGE / Ley Saín (news-worthy)
- **Asunto sugerido**: "La alternativa no invasiva que buscan las chilenas que no califican al AUGE"
- **Medios**: BBCL, Publimetro, La Tercera (sección Mujer), Meganoticias, CHV, Cooperativa
- **Oferta**: entrevista directora clínica + casos de pacientes AUGE-rechazadas
- **Anchor text deseado**: "Método Hebe" / "guatita de delantal sin cirugía"

### Ángulo B — Médico honesto (criolipólisis sin hype)
- **Asunto**: "Lo que no te dicen sobre la criolipólisis: riesgos reales y cuándo realmente funciona"
- **Medios**: Revista Paula, Ya Magazine, Elle Chile, Vogue Chile
- **Oferta**: artículo firmado con datos clínicos (hiperplasia paradójica, expectativas por IMC)
- **Anchor text deseado**: "criolipólisis Chile" → /criolipolisis/

### Ángulo C — Emprendimiento (founder-led)
- **Asunto**: "Cómo construí una clínica corporal con 3 sedes desregulando el mercado estético chileno"
- **Medios**: El Mercurio Economía, Diario Financiero, Pauta, Pulso
- **Oferta**: entrevista fundadora + métricas (30.000 pacientes, 3 sedes)

## TIER 2 — Directorios médicos y locales (1 mes)

Perfiles con backlink dofollow a metodohebe.cl:

- Doctoralia Chile (perfil profesional + página clínica)
- Clínicas.cl
- Reservo.cl
- Agenda Pro directorio público
- Yelp Chile, Cylex Chile, Superpages Chile
- Google Business Profile perfecto en las 3 sedes (schema + link)
- Cámara de Comercio de Santiago / Viña / Los Ángeles

## TIER 3 — Contenido linkable (atrae backlinks pasivos, 6-12 meses)

### Activo 1: "Radiografía Corporal Chile 2026"
Informe propio con data agregada anonimizada de 30.000 pacientes (zonas tratadas, edades, IMC, correlación post-parto). PDF + landing page. Predicción: 8-15 backlinks en 6 meses.

### Activo 2: Calculadora "¿Eres candidata a tratamiento no invasivo?"
Quiz de 8 preguntas → recomendación + captura email. Shareable.

### Activo 3: Infografía "Guía visual de tratamientos corporales no invasivos"
Ilustrada. Publicar en Pinterest (dofollow) + Behance.

## TIER 4 — Colaboraciones profesionales (2-3 meses)

- SOCHIMED (Sociedad Chilena de Medicina Estética) — membresía + listing
- Colegio de Kinesiólogos de Chile
- Universidades con nutrición/kinesiología (UChile, UAndes, PUCV) — caso clínico o convenio pasantías → citación académica (backlink alta autoridad)
- Podcasts invitada: "Enfoque Emprendedor", "Emprende tu Vida", "Capital Humano", "Café para 3"

## TIER 5 — HARO / Respondent

- Registrar marca en plataformas donde periodistas piden fuentes expertas.
- Responder consultas sobre "experto estética no invasiva", "clínica corporal Chile", "tratamiento post-parto".

## KPIs (medir mensual)

| Hito | Plazo | Meta |
|---|---|---|
| Backlinks dofollow nuevos (DR>30) | 3 meses | +10 |
| AS propio | 6 meses | 10 → 25 |
| AS propio | 12 meses | 35+ (umbral donde los LLMs empiezan a citar) |

## Lo que NO hacer

- **Nunca comprar backlinks** (Fiverr, Link-Assistant, marketplaces) — penalización Google.
- **Nunca PBN** (redes privadas de blogs).
- **Nunca link exchange masivo**.
- **Nunca guest posts** en sitios fuera de nicho con AS <15.
- Los backlinks actuales de URL shorteners (.sbs, .top, .icu, blinks.monster) son spam SEO — considera **disavow** en Search Console si siguen creciendo.

## Redirect pendiente — clinicahebe.cl → metodohebe.cl

**Estado actual (verificado 2026-04-23):** el dominio antiguo **NO está redirigiendo** a metodohebe.cl. Sirve su propio sitio (título: "Método Hebe — Clínica Corporal Metabólica en Chile...") desde Vercel, sobre un deployment independiente.

Esto deja en suspenso los 46 backlinks de 24 dominios que apuntan al dominio viejo — su equidad no fluye a metodohebe.cl.

**Acción requerida (fuera del repo actual):**

1. En el dashboard de Vercel del proyecto clinicahebe.cl (o del hosting que corresponda), configurar redirect 301 de todo el dominio hacia metodohebe.cl manteniendo paths equivalentes.
2. Configuración tipo (vercel.json del deployment de clinicahebe.cl):

   ```json
   {
     "redirects": [
       { "source": "/(.*)", "destination": "https://metodohebe.cl/$1", "statusCode": 301 }
     ]
   }
   ```

3. Agregar redirects específicos para URLs antiguas conocidas que no mantienen el mismo path, ej.:
   - `clinicahebe.cl/celulitis` → `https://metodohebe.cl/como-quitar-la-celulitis-de-las-piernas-y-gluteos-rapido/`
   - Cualquier otra URL legacy identificada en Search Console del dominio viejo.

4. Verificar con `curl -I https://clinicahebe.cl` que devuelva `HTTP/2 301` y `location: https://metodohebe.cl/...`, no 307 ni 302.

5. Una vez confirmado el 301, reenviar sitemap del dominio nuevo en Search Console para acelerar consolidación.
