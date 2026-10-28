## 2026-10-28 — /evaluacion: sin scroll en celulares chicos

En 320×568 (y hasta ~700 px de alto) cada paso cabe sin scroll: se oculta la cinta «Los más solicitados», la imagen del encabezado baja a 96 px y se compactan espacios, el aviso de costo y el formulario. Los campos siguen en 16 px (sin zoom en iOS) y 40 px de alto. De 360 px en adelante con pantallas altas no cambia nada.

## 2026-10-28 — /financiamiento: landing de formas de pago

Página nueva de una vista para clientas: 3, 6, 9 y 12 cuotas precio contado (la de 3 destacada con «Incluye regalo extra»), descuentos del 20% al 30% vigentes en cualquier forma de pago, bloque del regalo extra (solo con 3 cuotas; texto `[REGALO POR DEFINIR]` pendiente), 4 preguntas frecuentes y CTA a `/evaluacion`. Sin precios ni montos de cuotas. `noindex` y fuera del sitemap mientras el regalo esté por definir. Marca: solo el ícono.

## 2026-10-28 — /evaluacion: «Últimos cupos» que rotan

Marketing: al elegir cualquier sede, 1 o 2 días (no seguidos) muestran «Últimos 2 cupos» o «Últimos 3 cupos» (en celular, «Últimos 2»). Al elegir ese día, las franjas reparten esos mismos cupos (1+1 con una franja Full, 1+1+1 o 2+1 con una Full); la franja Full no se puede elegir. Los días cambian en cada visita y se mantienen durante la misma visita (sessionStorage `evalCupos`). No vienen de la agenda. El sábado de Los Ángeles sigue Full. El paso no crece: las etiquetas van sobre el borde de los botones.

## 2026-10-28 — /evaluacion: Los Ángeles no abre los sábados

Si la paciente elige la sede Los Ángeles, el sábado se ve en la grilla de días como «Full», gris y sin poder elegirse. Al tocarlo, la bajada del paso dice «Sábado full de evaluaciones. Elige otro día.» por unos segundos. Concón y Vitacura siguen con sábado. Si cambia de sede a Los Ángeles con el sábado ya elegido, el día se suelta. Lo mismo vale para lo restaurado de la sesión y el prefill por URL (`?sede=losangeles&dia=SÁB …`). El paso no crece: mismo alto que antes en 375×667.

## 2026-10-23 — /evaluacion: conversiones de Meta en USD y sin ClickPagar

El Lead del navegador pasa de $2.000 CLP a US$5, el mismo valor del Lead que n8n manda por CAPI con ese eventID; `generate_lead` de GA4 igual. Se quita el evento `ClickPagar` del clic en pagar: el pago llega a Meta una sola vez, como `Schedule` US$29 cuando el lead pasa a Cita confirmada en Twenty. `eval_pago_evaluacion` sigue en el dataLayer como paso del embudo, sin valor. El webhook de pago a n8n no cambia.

## 2026-10-23 — /evaluacion: pantalla de pago más simple

La pantalla que aparece después de dejar los datos dice una sola cosa: sin pago no hay hora. Arriba, «Hora sin confirmar»; título «Paga para confirmar tu hora»; la sede, el día y la franja elegidos; tres pasos (Datos ✓ → Pago → Hora confirmada) y un botón «Pagar $27.990 y confirmar». El precio aparece una vez (antes, tres) y el descuento y el no reembolso quedan en una línea bajo el botón. En móvil se quita la muestra del análisis y la pantalla cabe sin scroll en 375×667 (antes, 922 px de alto). El cobro no cambia: mismo link de MercadoPago, link propio por paciente y mismos eventos.

## 2026-10-22 — /evaluacion y home: cierre de la auditoría (20, 21, 24, 25, 27)

`/evaluacion`: se quita «3 cupos esta semana» (texto fijo, no venía de la agenda); el resumen del paso 3 pasa a `--teal-darker` (contraste 5,7:1); los pasos ya no llevan `aria-expanded`; el monto de la evaluación ($27.990) sale del paso 1 y del aviso de salud y queda solo en la pantalla de costo y en la de pago. Home: los CTA a `/evaluacion` (menú, hero, cierre y barra fija móvil) pasan de `<button onclick>` a enlaces `<a href>`, el del menú con 44 px de alto, y el enlace de la FAQ dice «la evaluación» en vez de «/evaluacion».

## 2026-10-22 — /evaluacion: los pasos ocultos ya no reciben foco

Los pasos que no se ven quedan `inert`: con teclado o lector de pantalla, Tab ya no pasa por las sedes del paso 1 estando en el paso 2. Si el foco estaba en el paso que se cierra, pasa al paso nuevo. Sin cambios visuales ni de alto.

## 2026-10-22 — /evaluacion: aviso del número final con 8 dígitos

Si el celular se escribe con 8 dígitos sin el 9 inicial, el wizard sigue guardándolo con un 9 adelante y ahora lo muestra bajo el campo («Quedará como +56 9 2234 5678.»), en gris y en la línea del error, para que la paciente lo corrija si era un teléfono fijo.

## 2026-10-22 — /evaluacion: GA4 recibe el envío del formulario

`generate_lead` va a GA4 (vía `gtag`, mismo bloque que el embudo) cuando n8n confirma el lead, junto con el `Lead` de Meta: valor 2000 CLP, sede y `event_id`. Antes GA4 no tenía ningún evento de envío y no se podía calcular la conversión del wizard.

## 2026-10-22 — Preguntas frecuentes de agendamiento: salen de /evaluacion y pasan a /preguntas-frecuentes

`/evaluacion` deja de mostrar el bloque «Preguntas frecuentes de agendamiento» y su `FAQPage` (`#faq-operacion`): distraía al final del formulario en móvil. Las 5 preguntas pasan a la página nueva `/preguntas-frecuentes`, con su `FAQPage`, enlazada desde el pie de `/fundador` y `/clinica/*` y agregada al `sitemap.xml` (64 `<loc>`). La respuesta de sedes ya no incluye horario: `/evaluacion` y la ficha de Vitacura decían horarios distintos y siguen pendientes del dato oficial.

## 2026-10-22 — /evaluacion: un solo scroll en móvil y recargar no borra el avance

Móvil (≤768 px): la página es el único contenedor con scroll; antes cada paso tenía scroll propio dentro de una columna de 100dvh y el gesto sobre el formulario movía el paso y no la página. Recarga: sede, horario, salud, paso y datos escritos se guardan en `sessionStorage` (solo esa pestaña, 30 minutos) y se restauran al recargar; se borran apenas n8n confirma el lead. Si el día guardado ya no está en la grilla, vuelve al paso de horario.

## 2026-10-21 — GA4: un solo page_view por página

Las 66 páginas que cargan GTM también traían `gtag('config','G-NGW7210RXB',{send_page_view:true})` directo, y GA4 recibía dos `page_view` por carga. Pasa a `send_page_view:false`: el page_view lo manda solo GTM y `gtag()` sigue enviando `hebeTrack` y el embudo de `/evaluacion`. `/blog/estrias-tratamiento-sin-cirugia` no carga GTM y queda con `true`. Desde este deploy las vistas de página en GA4 bajan a la mitad: es la corrección, no una caída de tráfico.

## 2026-10-21 — /evaluacion: marquesina sin precios de tratamientos

La franja «Los más solicitados» de `/evaluacion` (móvil y escritorio) deja de mostrar $2.677.990, $1.977.990 y $1.799.990: el wizard no da precio de tratamiento antes del diagnóstico. Quedan solo los nombres de los planes. El valor de la evaluación P3 ($27.990) sigue igual.

## 2026-10-21 — /evaluacion: celular, correo, envío confirmado y botón atrás

Celular: escribir o pegar el número con 56 o +56 ya no lo convierte en otro número (antes 56912345678 se enviaba como +56 9 5691 2345); se quita el `maxlength` que cortaba el pegado. Correo: exige usuario@dominio.tld y sugiere la corrección de dominios mal escritos (gmial.com, hotmial.com…). Envío: espera la respuesta de `lead-capture` (8 s y un reintento); el Lead de Meta y la pantalla de pago salen solo si n8n confirma; si no, se muestra la salida por WhatsApp con los datos prellenados y se registra `lead_envio_fallido`. El botón atrás del navegador retrocede un paso del wizard en vez de salir de la página.

## 2026-10-14 — Foto del Dr. Eugenio Castro en el home

Sección «Equipo médico» en `/` (entre Tecnología y Planes): foto, nombre, cargo (médico estético) y sedes (Vitacura y Concón). Foto nueva en `public/img/eugenio-castro.webp` y `.jpg`. Se descarta `/home2`: no se publica. Pendiente: `/equipo`, `llms.txt` y el schema siguen diciendo que Ricardo es la única persona nombrada.

## 2026-10-12 — Política de privacidad en `/politica-de-privacidad`

Página nueva con la política de privacidad de Método Hebe: responsable (MÉTODO HEBE SpA), datos que se recopilan, finalidades, datos de salud, proveedores, cookies y píxeles, plazos, derechos (Ley 19.628 y Ley 21.719) y contacto. Hace falta para publicar la app de Google que envía el correo de pago aprobado. No se agregó al `sitemap.xml` ni al footer del resto de las páginas.

## 2026-10-07 — Se retira la franja Cyber Hebe del home

Termina el Cyber: se elimina la franja superior de `/` y su estilo. Menú vuelve a `top:0`.

## 2026-10-01 — Precios y planes unificados, P3 de 45 min y páginas de grasa localizada

Planes al precio más alto, según `/planes`: Zero Celulitis y Zero Flacidez $1.977.990 (20 sesiones en 5 meses), Zero Rollito $1.799.990 (12 en 3 meses), Trifásico $1.977.990 (24 en 6 meses). Método Hebe 3D ($2.677.990) queda como plan aparte, sin sesiones publicadas. Se reemplazan los catálogos viejos (Starter/Optimal/Intensive/Premium en Concón y Los Ángeles; $1.697.990 y $1.297.990 en Vitacura; Inicial/Full/Premium en el blog de lipo 3D; $1.697.990 en guatita y estrías). La Evaluación P3 dura 45 minutos (corregido «60-90 min» en el blog de guatita). `/grasa-localizada-vitacura|concon|los-angeles`, `/grasa-localizada` y `/opciones-para-eliminar-la-grasa-localizada`: iZED pasa a ultrasonido focalizado y SkinWave MAX a HIFU (title, meta, schema, cuerpo y FAQ); se quitan las contraindicaciones por frío y las cifras de criolipólisis (20-27% por sesión, 30%); se suma medición de pliegues, composición corporal, edad y permanencia; recuperación de la liposucción 1 a 3 meses. Adipolite sigue en sala (`llms-full.txt` corregido). Pendiente: `/criolipolisis-los-angeles` sigue describiendo iZED como frío.

## 2026-10-01 — Direcciones oficiales de las tres sedes (Q4.6)

Las direcciones quedan iguales en las 27 páginas, `llms*.txt`, schema y widget de agendamiento: Vitacura «Los Abedules 3085, Locales 105 y 106», Los Ángeles «Avenida Gabriela Mistral 269» y Concón «Las Pelargonias 842, piso 11». Desaparecen «Of. 105», «Oficina 105», «local 105-106» y «Oficina 1114». Se mantiene la mención del Edificio Nueva Vitacura donde ya estaba. Horarios y códigos postales no se tocaron: siguen pendientes del dato oficial.

## 2026-10-01 — Plantilla de línea base de menciones en IA (Q4.5)

Nuevo `docs/SHARE_OF_MODEL_2026-10.md`: las 15 preguntas del mes 0 más 3 del plan Q4 (cuánto dura el tratamiento de celulitis, si sirve la criolipolisis para la guatita y cuántas sesiones se necesitan), con columnas para ChatGPT, Gemini y Modo IA. Va en blanco: los resultados los anota quien mida. Es solo documentación; no cambia el sitio.

## 2026-10-01 — Service por plan en /planes (Q4.4)

El schema de `/planes` suma un nodo `Service` por plan (Zero Celulitis, Zero Flacidez, Zero Rollito y Trifásico), cada uno con su `@id`, enlazado a su `Offer` y a la organización de Método Hebe. Los cuatro `Offer` reciben `@id` propio para poder referenciarlos. Precios y descripciones son los ya publicados; no se agregó ningún dato nuevo.

## 2026-10-01 — Sedes de Concón y Los Ángeles como MedicalBusiness (Q4.3)

El schema de las páginas de Concón y Los Ángeles pasa de `LocalBusiness` a `["LocalBusiness","MedicalBusiness"]`, igual que Vitacura. Los `@id` no cambian. No se tocó dirección, horario ni código postal: esos datos tienen diferencias entre páginas y esperan el dato oficial.

## 2026-10-01 — Respuesta corta de 40–60 palabras en 4 páginas (Q4.2)

`/celulitis`, el artículo de celulitis en piernas y glúteos, el de la guatita de delantal y `/planes` abren con una «Respuesta corta» de 48 a 57 palabras que responde la pregunta y dice qué se define en la Evaluación P3 (45 minutos, $27.990). Es lo que extraen ChatGPT, Gemini y Modo IA. Se agrega arriba del resumen existente, que queda intacto; no cambia ningún H1 ni la FAQ. Fechas visibles y `dateModified` alineados al 1 de octubre.

## 2026-10-01 — /celulitis con widget de agendamiento (Q4.1)

El CTA medio de `/celulitis` pasa de dos botones a que la paciente elija sede, día y franja en el mismo lugar (`agenda-widget`, el mismo de los otros tres artículos principales) y sigue a `/evaluacion` con la selección cargada. Sin JS queda el enlace «Agenda tu Evaluación P3». No dispara `Lead`; el `<article>` mantiene 3 puntos de conversión (tope 5). Se agrega «Actualizado: octubre 2026» visible y `dateModified` del schema alineado.
## 2026-10-01 — Correcciones clínicas (feedback de Tamara)

iZED pasa a describirse como ultrasonido focalizado de 60 joules (antes figuraba como criolipólisis en `/planes`, `/criolipolisis` y `/criolipolisis-vs-ized`). Skin Wave Max pasa a HIFU donde decía radiofrecuencia (flacidez, estrías, lipo 3D, planes, el método, qué diferencia a Método Hebe, sede Los Ángeles). Dodo Wave es Endospheres (rodillos con infrarrojo), no ondas de choque (`/blog/celulitis-tipos-grados-tratamientos`). El IMC deja de ser el criterio principal: se indica por composición corporal (bioimpedancia) y medición de pliegues, y se atienden también pacientes con IMC alto trabajando primero el perfil metabólico; en `/criolipolisis` se agrega un recuadro sin borrar texto. Se publica que la edad influye en la respuesta (hay pacientes de 80 años que ven poco o nada). Permanencia: los adipocitos destruidos mueren, pero puede formarse grasa en adipocitos nuevos, incluso en la misma zona; por eso el acompañamiento integral es clave. Recuperación de la liposucción: 1 a 3 meses aproximadamente. Se quita «sin licencia médica». `/lipoescultura-sin-cirugia` suma aparatología (Dodo Wave, iZED, Skin Wave Max) y la sección de personalización por tipo de grasa. No se tocan AUGE ni radiografía (criterios oficiales). Pendiente: las páginas por sede (`grasa-localizada-*`), `/grasa-localizada` y `/opciones-para-eliminar-la-grasa-localizada` siguen llamando «criolipólisis iZED» en título, H1 y texto; requieren reescritura aparte.

## 2026-09-30 — Contenido AEO/SEO en 16 artículos

Cada artículo suma una tabla de datos clave (H2 nuevo con `id`, agregado al índice) y de 1 a 3 preguntas frecuentes, visibles y en `FAQPage` con el mismo texto. Todo sale de datos ya publicados en la propia página o en `/planes`: no hay cifras, plazos ni casos nuevos. `/radiografia-corporal-chile` suma 3 preguntas con cifras de la ENS 2016–2017 y la OMS ya citadas. Se agregan enlaces cruzados dentro de cada grupo (criolipólisis, grasa y contorno, guatita de delantal, piel). `dateModified` (schema), `article:modified_time` y la fecha visible quedan iguales a 2026-09-30 (`scripts/schema_dates.py`). En `/guatita-de-delantal-auge-y-ley` se corrigió voseo («necesitás», «elegís», «pagás», etc.) a tuteo, también en el `HowTo`. `public/llms-full.txt` suma la sección 13 con las respuestas nuevas. No se tocan title, H1, H2/H3 existentes, canonical, robots ni hreflang. Semrush no estuvo disponible: las preguntas se eligieron por lo que ya dice cada página.

## 2026-09-30 — Botón fijo móvil con letras blancas

El botón del sticky móvil («Agenda tu Evaluación P3 · $27.990») pasa a letra e ícono blancos sobre `#0B8076` (contraste 4,8:1; blanco sobre el turquesa anterior daba 2,6:1). 47 páginas. No cambia umbral de aparición, ocultamiento en footer ni tracking.

## 2026-09-30 — UI/UX de lectura en 16 artículos (móvil y escritorio)

Sin desbordes horizontales a 390 px: las tablas van en `.table-scroll` (scroll lateral con sombra de borde, enfocable con teclado). Índice «En esta guía» (`<details>`, abierto en escritorio ≥900 px) con `id` en los H2 existentes, sin cambiar su texto; AUGE y `/radiografia-corporal-chile` conservan su `page-toc`. Barra de progreso de lectura de 3 px, texto de 17 px en móvil, medida de ~68ch en escritorio y objetivos táctiles ≥44 px. Evento `toc_click` (ya documentado) mide el índice. Se quita del párrafo de `/criolipolisis` la frase interna «Este resumen no dispara Lead.». `public/js/articulo.js` + `public/css/articulo.css`.

## 2026-09-30 — Widget de agendamiento en 16 artículos

Los botones del `.inline-cta` de los 16 artículos SEO pasan a un widget (`public/js/agenda-widget.js`, `public/css/articulo.css`): sede → día y horario → «Continuar a mi evaluación». Conserva el `<h3>` y el `<p>` de cada bloque y cuenta como el mismo punto de conversión (B.4.5). `/ejercicios-para-guatita-de-delantal` y `/blog/transformacion-corporal-renata-metodo-hebe` suman un bloque nuevo. En escritorio ≥1360 px aparece una tarjeta lateral (sede → continuar) después de `scrollY > 400`, se oculta cerca del CTA final/footer y mientras el widget del artículo está a la vista; no va en AUGE. `/evaluacion` lee `?sede=&dia=&franja=`, marca la selección con las mismas funciones del wizard y salta el paso de horario (registrado con `prefill:true`) en ambos órdenes del A/B de salud. Eventos nuevos: `widget_interact`, `evaluacion_prefill`. Sin JS queda un enlace normal a `/evaluacion`. Sin `Lead` ni `whatsapp_click`.

## 2026-09-30 — Logo en Google y byline de marca en 16 artículos

Favicon pasa de SVG `data:` inline (que Google no rastrea y reemplaza por el globo) a archivos: `/favicon.ico` (16/32/48), `/favicon.svg`, `/img/apple-touch-icon.png`, `/img/icon-192.png` e `/img/icon-512.png`, en las 66 páginas. `Organization.logo` (home y Los Ángeles) apunta al ícono cuadrado. Los 16 artículos SEO muestran el logo y «Clínica de estética corporal» arriba del hero (`public/css/articulo.css`). El favicon en la SERP cambia cuando Google vuelve a rastrear el home.

## 2026-09-29 — /evaluacion: letra blanca en botones y salud arriba en móvil

`.confirm-btn` (No, ninguna · Continuar · Confirmo) pasa a fondo `#0B8076` con letra blanca (4.8:1). El centrado vertical de `#stepSalud` queda solo en escritorio: en móvil todos los pasos parten a la misma altura.

## 2026-09-29 — /evaluacion: aviso antes de "No, ninguna"

Aviso ámbar con ícono sobre el botón del paso de salud: si tiene alguna condición, no podremos tratarla y los $27.990 no son reembolsables.

## 2026-09-29 — /evaluacion: filtro de salud antes del pago

Paso nuevo `#stepSalud` entre horario y costo: una pregunta, un toque. Embarazo, cáncer/tumor o infarto/ACV/trombosis en los últimos 6 meses → no se agenda (`evaluacion_no_apta`, sin `Lead`). Anticoagulantes, inmunosupresores o corticoides → se atiende con aviso de resultado más lento y `salud_revisar`. "Ninguna" avanza sola. Payload n8n suma `salud` y `salud_revisar`.

Medición y A/B del mismo paso: `evaluacion_paso` (`paso`: sede, horario, salud, costo, datos) y `salud_respuesta`, ambos con `salud_orden`. Sorteo 50/50 persistido en `localStorage` (`hebe_ab_salud_orden`): salud antes o después del horario; `?salud=antes|despues` lo fuerza. Payload suma `ab_salud_orden`. En escritorio el visor de pasos mide lo que el paso activo (mínimo 380 px) en vez de 620 px fijos.

## 2026-09-25 — AUGE: checklist visible, sin formulario

`/guatita-de-delantal-auge-y-ley` `#checklist` muestra la lista en la página. Ya no pide datos ni POSTea a `checklist-ley-21438`. Enlace a Instagram `@metodo.hebe`, con el logo al lado del texto. La agenda sigue en `/evaluacion`.

## 2026-09-13 — H5.2: Radiografía corporal Chile (ENS + OMS)

`/radiografia-corporal-chile`. Tablas de mediana ENS 2016–2017 (Minsal) y cortes IMC OMS. Etiquetado promedio referencial, no diagnóstico. Sin cm de pacientes Hebe ni Superintendencia.

## 2026-09-13 — T6.3: webhooks franquicia + checklist AUGE

`/franquicia` POSTea a `franquicia-lead` (n8n → `contacto@metodohebe.cl`). AUGE `#checklist` POSTea a `checklist-ley-21438` (`fuente: 'Checklist Ley 21.438'`, `lead_magnet_*`, nunca `Lead`). Mailto solo si el POST falla. Sin Clinera.

## 2026-09-13 — T6.2: spec dataLayer (G.3 / G.6)

`docs/EVENTOS_DATALAYER.md` + `docs/datalayer-spec.json`. Inventario evento → destino. No hay dashboard. T6.3: Ricardo crea `franquicia-lead` y el checklist AUGE en n8n.

## 2026-09-13 — H5.3: borrar /formalidad (deck Lumina) y 301 a home

El leftover noindex era un deck de Protocolo Lumina en este dominio. Se elimina y redirige a `/`. Sin destino Lumina inventado.

## 2026-09-13 — Fase 4.5: sticky B.4 en páginas que ya lo tenían

Home y 8 satélites: `scrollY>400`, observer del footer, `evaluacion_click` `mobile_sticky`. Sin barras nuevas. AUGE se queda en 800.

## 2026-09-13 — H4.1–H4.10: AUGE segmenta, no vende

Chips de fuentes, índice, tabla GES vs Ley 21.438, puente honesto, triage 3 rutas (2 no comerciales), tabla de rutas con “resuelve piel colgante: No”, 3 FAQ, sigue leyendo, HowTo + reviewedBy. Sin Offer ni precio arriba del pliegue. Sin checklist (T6.3).

## 2026-09-13 — H3.12: schema extra en criolipólisis

ImageObject de la figura iZED, speakable en la cápsula, FAQPage con @id. Service+Offer ya coinciden con el precio visible. Sin MedicalBusiness duplicado ni AggregateRating.

## 2026-09-13 — H3.11: copy del párrafo del inline-cta en criolipólisis

Solo el `<p>` (D.1). H3 y botones intactos. Precio $27.990, no “sin costo”. Tracking igual.

## 2026-09-13 — H3.10: dos FAQ nuevas en criolipólisis

Guatita de delantal (no como arreglo de piel) y sesiones del Plan Zero Rollito (12 / 3 meses / $1.799.990). 11 visibles = 11 schema.

## 2026-09-13 — H3.9: enlaces relacionados en criolipólisis

Seis tarjetas fuera del article (resultados, lipo sin cirugía, grasa, flacidez, planes, criolipólisis Los Ángeles). Suma B11, no quita.

## 2026-09-13 — H3.8: tarjetas de sede en criolipólisis

Tres fichas (Vitacura, Concón, Los Ángeles) con las direcciones ya publicadas. Sin Concepción. Enlaces internos, no un quinto CTA.

## 2026-09-13 — H3.7: micro-bloque de confianza en criolipólisis

Más de 30.000 pacientes y 5/5 en Google. Sin AggregateRating ni Review oculto. No es un CTA.

## 2026-09-13 — H3.4: CTA de zonas en criolipólisis

Una línea + botón a `/evaluacion`. Evento `evaluacion_click`, no `whatsapp_click`.

## 2026-09-13 — H3.3: figura de sesión iZED en criolipólisis

`sesion-criolipolisis-hiems.webp` con width/height 1600×2400 y lazy. No se inventa otra foto.

## 2026-09-13 — H3.2: banda de autoevaluación en criolipólisis

Dos tarjetas (suele funcionar / no es la vía) y un enlace de texto a P3. Evento `evaluacion_click`, no Lead.

## 2026-09-13 — H3.1: chips del hero en criolipólisis

Fila de chips bajo el meta: $27.990 · sin compromiso; más de 30.000 pacientes; 3 sedes. H1 intacto.

## 2026-09-13 — H3.6: tarjeta Plan Zero Rollito en criolipólisis

Precio visible $1.799.990 (12 sesiones / 3 meses), igual que `/planes`. Offer schema con el mismo monto. CTA a P3 + enlace a /planes.

## 2026-09-13 — H3.5: galería antes/después en criolipólisis

Tres pares de `/resultados` (abdomen-cintura, lateral-cintura, contorno) con el disclaimer de fotografía estandarizada. Enlace a los 11 casos. Sin cm inventados.

## 2026-09-13 — H5.4: borrar clave IndexNow huérfana

Se elimina `public/ab767007d40e7700a59b91b6f690a54f.txt`. No aparece en robots ni en pings. Queda la clave vigente `f0e1ff44b0ff128d2711bf78b0aa90b9`.

## 2026-09-13 — H5.2: cuestionario «¿Eres candidata?»

Nueva URL `/eres-candidata`: 8 preguntas, orientación a un plan publicado, captura por mailto, enlace compartible. No es diagnóstico. Sin webhook nuevo. Radiografía Corporal no se publica.

## 2026-09-13 — X20: satélite del blog vs pilar de guatita

La guía `/blog/guatita-delantal-tratamiento-sin-cirugia` declara al pilar como documento canónico del cluster (`rel=related`, `isPartOf`, aside visible). H1s distintos. Ambas URLs 200. Sitemap del satélite baja a 0.55.

## 2026-09-13 — X10: pilar de guatita más largo y prioridad 0.90

Se agregan H2 de Ley 21.438, plan publicado en `/planes`, tres sedes y lectura pilar vs satélite del blog. Sitemap de la URL pasa de 0.75 a 0.90. Sin reescribir H1/H2 existentes ni inventar centímetros.

## 2026-09-13 — H5.1: refresh de 7 posts de blog (abril)

Cada artículo recibe un hecho operativo ya publicado (P3 45 min / $27.990, planes vigentes o Ley 21.438 ≠ abdominoplastia) más `dateModified` 2026-09-13 y `<time>` visible. Sin cm, reseñas ni Superintendencia inventados.

## 2026-09-13 — H2.4: `<picture>` AVIF/WebP y peso

Las `tech-*.png` de home pasan a `<picture>` AVIF/WebP con `width`/`height`. LCP de home y `/criolipolisis` tienen preload `fetchpriority="high"`. Se borran PNG duplicados, `angelica.png` / `angelica-testimonio.png` y los 4 `.webm` huérfanos.

## 2026-09-13 — H2.2: a11y del wizard `/evaluacion`

El wizard es un `<form>` real: `label for`, `required`, errores persistentes `role="alert"`, sedes `role=button` + teclado, `fieldset` en sedes y franjas. `#btnSubmit` no dispara `whatsapp_click`. Mismo payload n8n.

## 2026-09-13 — H2.1: contraste AA de CTAs, WhatsApp, estrellas y grises

Texto de CTA en tinta `#14201F` sobre teal (6,53:1). WhatsApp usa la misma tinta sobre `#25D366`. Estrellas `#8A6100`. Gris `--ink-4` `#5A6B6B`. En `/evaluacion`, `--teal` queda en `#14B5A7`.

## 2026-09-13 — H1.10 leftover: Maps, wa.me y Clinera www

Los enlaces visibles de Maps usan los `share.google` del schema. En `/clinica/*`, WhatsApp apunta a `wa.me/56963222683` y las tres páginas enlazan el caso Clinera en `https://www.clinera.io`.

## 2026-09-13 — H1.9: refresh AUGE vs BCN / Minsal / FONASA

La Ley 21.438 no cubre abdominoplastia (BCN: Día de la Inclusión Social). GES son 90 problemas (Minsal); la guatita no está en el listado. La vía documentada es el Bono PAD FONASA. Se actualizan `dateModified`, `article:modified_time` y el hero a septiembre 2026. Sin cifras de copago ni espera sin fuente.

## 2026-09-13 — H1.8: tracking scroll, sección y evaluación

`scroll_depth` 25/50/75/90 en criolipólisis y AUGE. Los CTA llevan `data-section`. Los botones a `/evaluacion` disparan `evaluacion_click`, no `whatsapp_click`. Los enlaces del artículo a `/evaluacion` llevan `?origen=&bloque=`.

## 2026-09-13 — H1.7: enlaces Fase 1

`/criolipolisis` enlaza a `/resultados` y a `/criolipolisis-los-angeles`. AUGE enlaza a Bono PAD y FONASA/Isapre, con `id` en los H2. Se corrigen tres auto-enlaces de footer (X17). `/criolipolisis-los-angeles` enlaza a `/grasa-localizada-los-angeles`.

## 2026-09-13 — H1.4: un @id por entidad por página

El grafo puente deja de redefinir Organization, Person y sedes: solo referencia los `@id` del home. `fundador#person` tiene un solo cargo (Fundador y CEO). Los FAQ y locations de landing usan `@id` de esa URL, no el del home.

## 2026-09-13 — H1.3: higiene de URL

`og:url` queda igual al canonical y sin slash final (el home conserva `/`). Los `@id` de página usan `www`. `/fundador/` pasa a `/fundador` en sitemap, canonical y enlaces internos.

## 2026-09-13 — H1.2: og:image en todas las páginas

Las 49 páginas sin `og:image` ahora usan `https://www.metodohebe.cl/img/og-metodo-hebe.jpg` (las de Los Ángeles, la foto de fachada). Se corrigieron las URLs de schema que 404 (`og-vitacura.jpg`, `hebe-og.jpg`, `logo.png`, etc.) y `/franquicia` deja el AVIF de og por el JPG con `www`.

## 2026-09-13 — H1.6: /evaluacion al par R3

En `/evaluacion`, «+20.000 personas» pasa a «más de 30.000 pacientes» y el chip de Google a «5/5 estrellas en Google». Las gratuidades ajenas a P3 (Ley 21.438, Clinera, «sin costos ocultos», bioimpedancia al contratar plan) se conservan.

## 2026-09-13 — H1.1: sticky B.4 en criolipólisis, AUGE y /resultados

El CTA móvil usa `.visible`, `scrollY > 400` (AUGE `> 800`) e `IntersectionObserver` del footer. Evento unificado `evaluacion_click` + `location:'mobile_sticky'`. No se propaga al resto de páginas.

## 2026-09-13 — R8: se borra Concepción

Se elimina `/clinica-estetica-corporal-concepcion` (página, nav, sitemap, schema). La URL leftover hace 301 a la sede de Los Ángeles. `/franquicia` ya no anuncia «próxima apertura».

## 2026-09-13 — R6: una sola persona nombrada

En página, la única persona con nombre es el CEO **Ricardo Alfredo Oyarzún Acuña**. El resto del staff se describe como profesionales altamente capacitados. Se quitaron promesas de registros Superintendencia en `/equipo` y en los bloques «Revisado por».

## 2026-09-13 — Estado (docs)

`/franquicia` ya no es stub: el formulario POSTea a n8n (`franquicia-lead`) y, si el webhook no responde, ofrece `mailto:contacto@metodohebe.cl`. **H1.6 hecho:** `/evaluacion` usa el par R3. Quedan solo gratuidades ajenas a P3 (Ley 21.438 / Bono PAD, «sin costos ocultos», Clinera, bioimpedancia al contratar plan).

## 2026-09-03 — Foto del fundador en `/equipo`

Ricardo Alfredo Oyarzún Acuña aparece en `/equipo` como director fundador, con retrato profesional (`/img/ricardo-oyarzun.webp` + `.jpg`), ficha de staff y `Person.image` en schema. El home declara `Organization.founder` hacia el mismo `@id`. No se inventan registros de Superintendencia ni se presenta como profesional tratante.

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
