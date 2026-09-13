# Auditoría UX/UI + CRO — Método Hebe y Protocolo Lumina

**Fecha:** 28 de julio de 2026
**Alcance:** `metodohebe.cl` (repo `metodo-hebe-web`) y `protocololumina.cl` (repo `lumina-web`)

---

## Método

La política de red del entorno bloquea la salida HTTPS a ambos dominios (403 en el CONNECT del proxy), así que no
fue posible auditar las URLs públicas. En su lugar se sirvió **el código fuente real de cada sitio** en localhost y
se renderizó en Chromium vía Playwright, en viewports de 390×844 y 1440×900. Es el mismo HTML, CSS y JS que se
despliega en Vercel.

**Medido:** peso transferido, altura de página, contraste calculado sobre el color computado del DOM, áreas
táctiles, tamaños de fuente aplicados, posición de cada CTA, campos de formulario, scripts de terceros, jerarquía
de headings.

**No medido:** Core Web Vitals reales de producción, cabeceras HTTP que sirve Vercel, y si el commit desplegado
coincide con el del repo. Los fallos de contraste sobre secciones con imagen de fondo se descartaron por no ser
concluyentes: solo se reportan los que ocurren sobre color sólido.

---

## Tablero

| Métrica | Método Hebe | Protocolo Lumina |
|---|---|---|
| Peso home, móvil | **7.233 KB** | 184 KB |
| Alto de página, móvil | 13.422 px (home) | **19.427 px** (`/resultados`) |
| Imágenes sin `width`/`height` | **16 / 19** | 1 / 17 |
| Áreas táctiles < 44 px | 24 | 10 |
| Reglas `:focus` | **0** | **0** |
| Contraste del CTA primario | **2,56 : 1** | **2,71 : 1** |
| Formularios de captura | 3 pasos | 3 pasos, solo en `/evaluacion` |
| Enlaces públicos al wizard | 158 (50 páginas) | **0** |
| Enlaces `tel:` | 2 | **0** |

Los dos sitios fallan en cosas opuestas: a Hebe lo hunde el peso; Lumina es liviano y está mejor diseñado, pero su
contraste de marca no sobrevive a los fondos claros y su wizard vive aislado del recorrido orgánico.

---

## Hallazgos compartidos

### 01 · CRÍTICO — Las dos marcas comparten contenedor de GTM y número de WhatsApp

Lumina carga `GTM-TZC56NQ5` en sus 5 páginas: el mismo contenedor que Hebe carga en sus 51. Los 10 CTA de la home de
Lumina apuntan a `api.whatsapp.com/send?phone=56963222683`, el mismo número que Hebe publica como suyo.

El tráfico facial y el corporal caen en el mismo dataset, con las mismas audiencias y conversiones. No se puede
distinguir qué campaña trajo una paciente de lifting facial y cuál una de guatita de delantal. Y toda conversación de
WhatsApp entra a la misma bandeja sin señal de origen.

**Arreglo:** contenedor GTM propio por marca, o como mínimo una variable `clinica` en el dataLayer usada como
dimensión (Lumina ya la envía en su evento de WhatsApp: `clinica:'lumina'`; falta aprovecharla y replicarla en Hebe).
Número de WhatsApp distinto por marca.

### 02 · ALTO — Las estrellas de reseñas son casi invisibles en ambos sitios

`#FBBC04` sobre blanco = **1,71 : 1**. En Hebe también aparece el dorado `#D4A853` sobre blanco = 2,20 : 1. Es el
elemento de prueba social más citado de ambos sitios.

**Arreglo:** la forma de la estrella ya comunica; usar el color de tinta del sitio y reservar el amarillo para el
relleno con borde oscuro.

### 03 · ALTO — Ninguno de los dos sitios define estilos de foco

Cero reglas `:focus` / `:focus-visible` en la home de Hebe y en las 5 páginas de Lumina. Lumina además usa
`href="javascript:void(0)"` en los botones «VER OPCIONES» de `/planes`, inalcanzables por teclado.

**Arreglo:** `:where(a,button,[role=button],input,select):focus-visible{outline:3px solid …;outline-offset:3px}` y
cambiar los `javascript:void(0)` por `<button type="button">`.

### 04 · MEDIO — Ambas usan Playfair Display, y en Hebe casi no se aplica

Hebe carga Inter + Playfair Display + Pacifico; Lumina carga Sora + Playfair Display. Al medir las familias realmente
computadas en el DOM de la home de Hebe: **Inter 106 nodos, Playfair 4**. Una regla `!important` en `shell.css` fuerza
todos los `h1`–`h6` a la sans, anulando el acento serif que se está descargando.

**Arreglo:** o se quita Playfair y se ahorra la descarga, o se corrige el `!important`. Hoy no ocurre ninguna.

---

## Método Hebe

### 05 · CRÍTICO — La home pesa 7,2 MB en móvil; el LCP es un PNG de 2,6 MB

`angelica-testimonio.png`: 2.642 KB, origen 938×1668 px, render 500×600, `loading="eager"`. Los seis `tech-*.png`
suman ~9 MB para renderizarse en tarjetas de ~333 px. `angelica.png` es un duplicado byte a byte: 2,6 MB muertos.
El 88,9 % del peso de imagen está en PNG/JPG legacy.

El sitio ya sabe hacerlo bien: en `img/blog/` conviven 10 pares JPG/AVIF con ratio real de 0,28. La infraestructura
`<picture>` con AVIF+WebP existe, pero solo llegó a 5 de 51 páginas.

**Arreglo:** redimensionar al tamaño real de render, convertir a AVIF+WebP con el `<picture>` que ya usan,
`fetchpriority="high"` + `preload` en el LCP. La home baja de ~12,3 MB a ~2,1 MB de imagen. Añadir
`Cache-Control: immutable` para `/img/` en `vercel.json` (hoy solo cubre `robots.txt` y `sitemap.xml`).

### 06 · CRÍTICO — La home es la única de 51 páginas que no lleva al formulario

Las otras 50 contienen 158 enlaces a `/evaluacion`. La home contiene cero: sus cuatro CTA son
`<button onclick="window.open(wa.me…)">`.

Existe un funnel de 3 pasos que captura nombre, celular, correo, sede y horario, dispara
`ViewContent → InitiateCheckout → Lead` con deduplicación de `event_id` entre Pixel y CAPI, y envía a un webhook. La
página con más tráfico lo puentea entero.

**Arreglo:** CTA primario a `<a href="/evaluacion">`, WhatsApp como secundario. Usar `<a>` y no `button onclick`: no
son rastreables, no permiten abrir en pestaña nueva, y en iOS Safari `window.open` fuera de un gesto directo puede
quedar bloqueado.

### 07 · CRÍTICO — El CTA primario tiene contraste 2,56 : 1

Blanco sobre `#14B5A7`. Confirmado sobre fondo sólido en `/planes`, `/resultados` y las landings de síntoma. Es el
CTA sticky móvil. `--cyan` se usa 1.124 veces en el sitio.

**Arreglo:** invertir el texto a tinta `#14201F` sobre el mismo teal da **6,53 : 1** sin perder el color de marca.
Alternativa: blanco sobre `--cyan-dd` (`#0A6B65`), ya definido en `shell.css`, da 6,36 : 1.

### 08 · ALTO — El formulario no es un `<form>` y el error dura 600 ms

`evaluacion.html` no contiene ningún `<form>`. Los tres campos son inputs sueltos sin `required`, sin `label for`,
sin `aria-invalid`. Al fallar la validación el único feedback es un borde rojo que se borra a los 600 ms, sin texto
que explique qué corregir. Las tres tarjetas de sede del paso 1 son `<div onclick>` sin `tabindex`: el funnel no se
puede completar con teclado desde el primer paso.

**Arreglo:** envolver en `<form>`, asociar labels, sustituir el `setTimeout` por mensajes persistentes con
`role="alert"`.

### 09 · ALTO — El badge «Más elegido» señala planes distintos según la página

En la home está sobre **Zero Flacidez**; en `/planes` sobre **Zero Celulitis**. Además las cifras de confianza se
contradicen: la home dice «+30.000 pacientes» y «4,9 Google»; `/evaluacion` dice «+20.000 personas atendidas» y
«5/5 en Google Reviews», a cinco líneas de distancia.

**Arreglo:** una sola cifra real en todo el sitio, el badge en un solo plan, y convertir el chip de reseñas de la
home (hoy un `<span>`) en enlace al perfil real de Google.

### 10 · ALTO — El precio se muestra en crudo, sin cuota

| Plan | Precio | Sesiones | Por sesión |
|---|---|---|---|
| Zero Rollito | $1.799.990 | 12 | **$149.999** |
| Zero Celulitis | $1.977.990 | 20 | $98.900 |
| Zero Flacidez | $1.977.990 | 20 | $98.900 |
| Trifásico | $1.977.990 | 24 | **$82.416** |

Tres de cuatro planes cuestan lo mismo, dejando al plan de entrada como el peor valor por sesión (+82 % frente al
Trifásico). La única mención a cuotas está enterrada en un acordeón de FAQ.

**Arreglo:** equivalente mensual bajo cada precio («desde $164.832/mes en 12 cuotas») y corregir la escala para que
el plan de entrada no sea el peor negocio.

---

## Protocolo Lumina

### 11 · CORREGIDO — El wizard existe; lo que no existe es un camino orgánico hacia él

> **Corrección.** La primera versión de este informe afirmaba que Lumina no tenía ningún formulario en todo el
> sitio. Era falso: se verificó solo en 4 de las 5 páginas. `protocololumina.cl/evaluacion` **sí tiene el wizard de
> 3 pasos**, con los mismos campos que el de Hebe (`inputNombre`, `inputCelular`, `inputCorreo`) y la misma
> estructura «PASO 1 DE 3».

Lo verificable es más acotado: las 4 páginas públicas (`/`, `/planes`, `/resultados`, `/tratamientos`) tienen
**0 enlaces a `/evaluacion`**. El wizard solo recibe tráfico de campañas pagadas. Entre 5 y 11 CTA por página apuntan
al mismo enlace de WhatsApp, y no hay ningún enlace `tel:` en el sitio.

**Esto es una decisión de funnel, no un defecto:** el tráfico orgánico que llega al home se deriva a WhatsApp a
propósito, y el de campañas entra al wizard. Con ese diseño, el evento `Lead` y la captura de datos siguen
existiendo donde importan para optimizar Meta.

**Lo que sí conviene revisar:** `/planes` es la página donde alguien compara precios y decide, y hoy solo ofrece
WhatsApp. Es la candidata natural para enlazar el wizard sin tocar el resto del funnel.

**Nota heredada:** el wizard de Lumina arrastra el mismo defecto que el de Hebe (hallazgo 08) — no está envuelto en
un `<form>`, sin `label for` ni `required`.

### 12 · CRÍTICO — El acento de marca falla contraste en las cuatro páginas

| Combinación | Ratio | Mínimo | Dónde |
|---|---|---|---|
| `#E8B4B8` sobre `#F4EEEB` | **1,57** | 4,50 | «Ellos y ellas lo vivieron» |
| `#C48B90` sobre `#F4EEEB` | **2,46** | 4,50 | eyebrows, 4 páginas |
| `#C48B90` sobre `#FBF6F4` | **2,63** | 4,50 | 10 tamaños distintos, de 8 px a 140 px |
| Blanco sobre `#4CAF7D` | **2,71** | 4,50 | CTA sticky «Agenda tu hora» |
| Blanco sobre `#C48B90` | **2,82** | 4,50 | badge «Premium» |

El rosa funciona bien sobre el fondo oscuro del hero — ahí no falla. El error es haberlo llevado tal cual a las
secciones claras.

**Arreglo:** segunda versión del acento, más oscura, para fondo claro (≈ `#8E4F55` da 5,4 : 1 conservando el tono).
El rosa claro queda solo para fondos oscuros. El verde del CTA sticky debe oscurecerse hasta al menos `#2E7D52`.

### 13 · ALTO — 2.908 px de scroll antes del primer CTA en la página de precios

`/planes` mide 13.490 px de alto en móvil; el primer «AGENDAR ESTE PLAN» aparece a los 2.908 px. `/resultados` es más
extremo: 19.427 px de alto con el primer CTA a los 15.464 px — aunque esa página sí tiene un CTA sticky en
`position:fixed` que compensa parcialmente. `/planes` no lo tiene, y es donde se decide la compra.

**Arreglo:** CTA sticky en `/planes` igual que en `/resultados`, y un precio visible antes de los 900 px. Hoy la
página de precios no muestra ningún precio sin scroll.

### 14 · ALTO — La guía de intensidad está codificada solo por color

En `/planes` la profundidad del tratamiento se comunica con tres chips (verde, amarillo, rojo) y la instrucción
literal «Mira el color en cada plan para saber qué tan profundo va el tratamiento». Para alguien con daltonismo
rojo-verde (~8 % de los hombres) esa instrucción no se puede seguir. Falla WCAG 1.4.1, y la propia página declara que
el servicio es «para hombres y mujeres».

**Arreglo:** segundo canal además del color — tres puntos rellenos (●○○ / ●●○ / ●●●) o la palabra de intensidad como
etiqueta permanente en cada tarjeta.

### 15 · MEDIO — `/tratamientos` sin canonical, sin Open Graph, sin JSON-LD

Es la página que presenta las 14 tecnologías y la única de las cinco sin `<link rel=canonical>`, con **0** etiquetas
`og:` y **0** bloques JSON-LD. Compartida en WhatsApp o Instagram sale sin miniatura ni título.

**Arreglo:** copiar el bloque `<head>` de `/planes`, que ya está bien resuelto.

### 16 · MEDIO — Texto bajo 15 px y coreano decorativo sin marcar

73 elementos con texto de lectura bajo 15 px en `/planes`; 43 en la home y en `/tratamientos`. Hay etiquetas de 8 y
9 px. El sitio usa texto coreano decorativo (환영합니다, 아름다움) sin `lang="ko"`: un lector de pantalla en español
intentará pronunciarlo con fonética castellana. En el hero de `/planes` la marca de agua coreana queda además detrás
del párrafo, restándole legibilidad.

**Arreglo:** mínimo 15 px para texto de lectura, `lang="ko"` en los fragmentos coreanos —o `aria-hidden="true"` si son
decorativos— y bajar la opacidad de la marca de agua donde cruza texto.

---

## Competencia

14 competidores chilenos verificados con URL real e indexada (Corpórea, Kintegra, BeYou, Dra. Zaror, Corpoclinic,
Dubó, Beunique, Cialo, Dermapiel, Blume, Meu, La Parva, Lucrecia Michaud, Lumina Clinic).

### Patrones que usan y estas dos marcas no

| Patrón | Quién lo usa | Hebe / Lumina |
|---|---|---|
| Financiamiento comunicado («12 cuotas sin interés») | BeYou | Solo en una FAQ de Hebe; ausente en Lumina |
| Escalón de entrada barato ($49.990–$199.990) | Kintegra, Meu, Blume | Ticket mínimo de Hebe: $1.799.990 |
| Credenciales SEREMI y Superintendencia exhibidas | Corpórea, Beunique, Dermapiel | Ninguna las muestra |
| Médico con nombre y rostro | Dra. Zaror, Dermapiel | Ambas son protocolos sin rostro clínico |
| Garantía de satisfacción con página propia | Corpoclinic | Ninguna |
| Fichas en agregadores (Doctoralia, AgendaPro) | 6 de los 14 | Ninguna aparece |
| Landing dedicada para tráfico pagado | Dra. Zaror (`ad.` subdominio) | Ambas mandan los ads al sitio principal |

### Lo que sí tienen y nadie más

- Hebe es la única del mercado que publica el precio completo de sus planes con sesiones y duración.
- Tiene un mecanismo propietario con nombre («protocolo de 3 fases», «no adivinamos, medimos») en un mercado donde
  todos venden aparatos sueltos.
- Es dueña del cluster de «guatita de delantal», donde compite contra hospitales públicos y no contra clínicas.
- Tiene `llms.txt` y `llms-full.txt`, que ningún competidor mostró: está preparada para ser citada por motores de IA.

### Tres huecos que nadie ocupa

1. **Precio publicado + cómo pagarlo.** El mercado se parte entre premium que esconden el precio y volumen que
   publica precios bajos de sesión suelta. Nadie ocupa «precio alto publicado, con ruta de pago resuelta».
2. **Garantía medida en centímetros, no en satisfacción.** La única garantía del mercado es subjetiva. Hebe hace
   bioimpedancia y cintometría antes de tratar: es la única con medición objetiva instalada, y por tanto la única que
   puede garantizar un número.
3. **El paciente post-GLP-1.** Nadie posiciona para quien bajó de peso con semaglutida y quedó con flacidez, pérdida
   de volumen facial y pannus residual — exactamente lo que Hebe trata en el cuerpo y Lumina en el rostro.

---

## Dirección de diseño

Las dos marcas comparten hoy la paleta más transitada del rubro (teal/rosa + dorado + serif clásica). Diferenciarlas
importa más que embellecerlas.

**Hebe — «calidez clínica».** Base arena `#F7F4F0`, jade institucional `#0E5C55`, terracota de acción `#A85026`
(blanco encima: 5,47 : 1). Fotografía 4:5 vertical. Sale del teal-dorado genérico y resuelve el fallo de contraste.

**Lumina — «luz medida».** Deliberadamente opuesta: porcelana `#FAF8F5`, acento bronce `#8F6229`, CTA en tinta
`#171514` (blanco encima: 18,20 : 1) — negro, no dorado. Fotografía 3:4 high-key. La luminosidad se produce con
blanco y fotografía, no con brillos.

**Fotografía, que importa más que la paleta.** Para antes/después la condición es protocolo estandarizado: misma
distancia focal, mismo fondo, misma luz, mismos ángulos. Esa consistencia *es* la señal de precisión clínica y lo que
impide que el «después» se lea como retoque. Hebe ya declara «mismo ángulo, misma luz» en la home; `/resultados` —la
página que existe para mostrar resultados— es la única que no lo dice ni advierte que los resultados varían.

---

## Prioridad

| # | Acción | Esfuerzo | Severidad |
|---|---|---|---|
| 1 | ~~Invertir el texto del CTA sticky de Hebe a tinta sobre teal (2,56 → 6,53 : 1)~~ | ✅ hecho | Crítico |
| 2 | ~~CTA de la home como enlaces reales~~ (destino WhatsApp, por diseño de funnel) | ✅ hecho | Crítico |
| 3 | Separar el GTM y el WhatsApp de las dos marcas | 1 h | Crítico |
| 4 | Convertir el LCP de Hebe a AVIF y borrar el duplicado (−2,6 MB) | 1,5 h | Crítico |
| 5 | Crear el acento rosa oscuro de Lumina para fondos claros | 1 h | Crítico |
| 6 | ~~Regla global de `:focus-visible`~~ (Hebe; falta Lumina) | ✅ Hebe | Alto |
| 7 | Enlazar el wizard de Lumina desde `/planes` (ya existe en `/evaluacion`) | 30 min | Alto |
| 8 | Cuota mensual bajo cada precio, en ambas marcas | 40 min | Alto |
| 9 | Unificar cifras de prueba social y alinear el badge «Más elegido» | 25 min | Alto |
| 10 | CTA sticky en `/planes` de Lumina y precio antes de los 900 px | 1 h | Alto |

---

## Estado de implementación

Aplicado en Método Hebe y verificado renderizando 12 páginas en Chromium a 390×844:

| Página | Fallos de contraste antes | Después |
|---|---|---|
| `/planes` | 13 | **0** |
| `/celulitis` | 9 | **0** |
| `/blog` | 7 | **0** |
| `/resultados` | 6 | **0** |
| `/` (home) | 6 | **0** |
| `/evaluacion` | 3 | **0** |
| `/flacidez`, `/grasa-localizada`, `/tonificar`, `/el-metodo`, `/criolipolisis`, `/…-vitacura` | — | **0** |

También verificado: `button[onclick="window.open"]` en 0 páginas, regla `:focus-visible` presente en las 51 páginas,
bloque `prefers-reduced-motion` en las 51, y el paso 1 de `/evaluacion` completable con teclado (Enter selecciona
sede).

**Un falso positivo descartado:** `.badge-ba` en `/resultados` aparecía como 1,19 : 1. Su fondo es
`rgba(11,30,30,.78)` sobre una foto, y el detector lo ignoró por tener alpha bajo el umbral de 0,85. Componiendo el
alpha real da **8,44 : 1 en el peor caso** (foto blanca debajo). No requiere cambio.

**Una regresión detectada y corregida durante el trabajo:** al oscurecer la escala de grises, `.trust-text` —que vive
sobre la barra sticky oscura— cayó a 3,16 : 1. Se le asignó un gris claro propio (`#C4D2D0`) en lugar del token
general.

**Pendiente en Lumina:** todos los arreglos de contraste y foco. Requiere acceso de escritura al repo `lumina-web`.

---

*Escaneo ejecutado con Chromium 1194 vía Playwright sobre el código fuente de ambos repositorios servido en
localhost. Contraste calculado con la fórmula de luminancia relativa WCAG 2.1 sobre el color computado del DOM,
descartando los casos sobre imagen de fondo.*
