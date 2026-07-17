# HALLAZGOS — Sistema de Activación Clinera

Última actualización: 2026-07-17
Formato: **§A** supuestos del prompt que no se sostienen · **§B** entorno/repos ·
**§C** datos · **§D** para el equipo de Clinera · **§E** decisiones de Ricardo · **§F** seguridad

---

## §A — SUPUESTOS DEL PROMPT QUE NO SE SOSTIENEN

### A1. La fase 1 ya estaba hecha. No cambié nada.

El prompt la plantea como "el fix más importante, hazlo primero". **Ya está aplicado.**
La fórmula viva del campo 3285 es hoy carácter por carácter la fórmula objetivo: ya incluye
`📞 Verificación Mitzi` y ya no tiene el backdoor.

La aplicó una sesión previa (`worktree clinera-activation-system-30f579`) el 2026-07-17.
Lo verifiqué de forma independiente simulando ambas fórmulas sobre las 105 filas reales:
la simulación estricta reproduce el estado vivo con **0 discrepancias en 105 filas**.

**El número que querías: 61 clientes cambiaron. De 63 ✅ ONBOARDEADO a 2.**
Los 2 que sobreviven: **ARMONIA** y **BELLA VITA** — los únicos con `Mitzi = ✅ Conforme`.

### A2. ⚠️ Los 61 no son 61 mentiras. Esto es lo más importante del documento.

Descomponer el 61 cambia la conclusión por completo:

| Causa | Clientes | Qué significa |
|---|---|---|
| **Backdoor puro** — `Estado Onboarding='Aprobado'` con `AHA=⏳ Pendiente` | **2** | Onboarding falso real. Es el bug que buscabas. |
| **Solo les falta el registro de Mitzi** — `Pasos=6` + `AHA=✅ Validado`, Mitzi sin marcar | **59** | Ambiguo. Ver abajo. |

Los 2 del backdoor puro: **IBRACKETS CLINICA DENTAL** y **MY CLINIC**.

**El dato que rompe el supuesto:** de 105 filas, **100 tienen `📞 Verificación Mitzi`
completamente en blanco** — ni siquiera `⏳ Pendiente`. Solo 5 filas tienen algún valor.

Un campo con 95% de nulos no es un gate que la gente se saltó. Es un gate que **nunca se
operacionalizó**. La lectura honesta de los 59 no es "59 clientes falsos" — es "no sabemos,
porque nadie llenó nunca ese campo". → decisión **§E1**.

### A3. El schema dice que no se pueden crear tablas ni campos. Es falso vía API REST.

`SCHEMA-baserow-activacion.md` §2 afirma que la tabla la tiene que crear Jorge a mano porque
"el conector no expone create_table ni create_field". Eso es cierto **para el conector MCP**,
pero la **API REST con JWT sí puede** (`POST /api/database/tables/database/97/`).
Por eso la fase 2 la ejecuto yo. El doc está desactualizado en ese punto, no equivocado en el resto.

### A4. `🚫 N/A` cuenta como paso listo en la fórmula actual de la 327.

`Pasos listos` (3283) suma `if(or(estado='✅ Listo', estado='🚫 N/A'), 1, 0)`. O sea, N/A regala el paso.
Para la tabla nueva esto importa mucho más: A2 (CAMILA en Vortex), A6 (embed) y A7 (cobros) van a
caer en N/A constantemente. Con el patrón del schema, **un Vortex se lleva 3 checks gratis**. → **§E3**

---

## §B — ENTORNO Y REPOS

### B1. 🔴 Este worktree NO es tech.oacg.cl. Es el repo del sitio de Hebe.

El prompt dice "el repo de tech.oacg.cl (el panel)" y pide `PROGRESO.md` en su raíz.

- Este worktree (`customer-activation-system-5b16d6`) tiene remote
  `github.com/odracirnuzra10/metodo-hebe-web.git` — es el **sitio de marketing de Método Hebe**
  en Vercel. No tiene nada que ver con el panel.
- **tech.oacg.cl no existe como repo git.** Es un HTML único (`/opt/work/site/index.html`,
  2885 líneas, 292KB) en la VM GCP, que se edita bajando/subiendo por scp.

**Qué hice:** escribo `PROGRESO.md` / `HALLAZGOS.md` y el código del proyecto en este worktree
porque es el workspace que me diste y necesitas encontrarlos al decir "continúa".
**No voy a commitear ni pushear nada al repo de Hebe** — contaminaría un sitio de producción
con código que no le pertenece.

**Lo que necesito de ti (§E5):** dónde vive de verdad este proyecto. Un repo propio sería lo sano.
El panel `/activacion` lo entregaré como archivo listo para scp, que es el flujo actual del panel.

### B2. Registrar `/activacion` en el panel toca 7 lugares hardcodeados.

El router es una lista de slugs a mano (`work-index.html:283–313`, `BOARD_TIDS` en :342,
más el whitelist `TABLAS_PERMITIDAS` en `work-app.py:18`). No hay registro dinámico:
si se omite uno, `go()` tira excepción. Está mapeado, no es bloqueante, pero no es un one-liner.

---

## §C — DATOS

### C1. 🔴 La tabla `Uso` (939) NO sirve hoy para el gate de adopción. Tres razones duras.

El prompt apuesta a que sí ("si ya lee consumo por clínica, el gate de adopción se puede apoyar ahí").
La leí completa (50 filas). **No se puede, sin trabajo previo:**

1. **No tiene slug ni ningún id de clínica.** El único identificador es `Name`, texto libre.
2. **Los nombres no joinean con la 327.** La 939 dice `Clínica Antuka`, `Kompass (Jorge Cusme)`,
   `Clínica dental Divedent`; la 327 dice `ANTUKA`, `KOMPASS`, `DIVEDENT`. Joinear eso es fuzzy
   matching sobre nombres de clientes que pagan comisiones de US$50. No lo voy a hacer a ciegas.
3. **Taxonomía legacy.** Su campo `Plan` solo tiene `CLINERA` (41) y `ECOSISTEMA` (9).
   Ni rastro de Vortex/Atlas/Summit. Son los clientes viejos, no los nuevos.

**Además:** el prompt describe `Grupo` como (🟢 Usando / 🔴 Sin uso · riesgo). Tiene **tres**
valores, no dos: `🟢 Usando` (26), `🟡 Sin uso · nueva` (15), `🔴 Sin uso · riesgo` (9).

**Y hay 50 filas, no 105.** La 939 cubre menos de la mitad de la cartera.

**Veredicto:** el pipeline de adopción **existe pero no es enchufable**. Sirve como precedente
de que alguien ya calcula consumo por clínica, no como fuente para el tramo 3.
Para usarlo hace falta que la 939 tenga `Slug Clinera`. → tarea para el equipo, **§D1**.

### C2. 🚫 Quién alimenta la 939 y con qué frecuencia: **NO LO SÉ. null explícito.**

El prompt lo pregunta directamente. Lo intenté y no lo pude determinar:
- No hay workflow n8n en disco que referencie la tabla 939.
- No hay credenciales de n8n en esta máquina, así que no pude consultar la instancia.
- La API de filas de Baserow no expone `updated_on`, así que tampoco pude inferir frecuencia.

No lo voy a inventar. **Pregunta abierta para el equipo (§D2).**

### C3. Campos duplicados y typos en la 327 (menores, confirmados)

- Dos dueños: `Especialista` (3241, **texto libre**) y `Encargado` (10514, select con **solo
  Rebeca y Brian** — los 8 nombres del prompt no existen ahí).
  La comisión se paga hoy contra un campo de texto sin validar.
- Dos videos Eureka: `🚨 Video ¡Eureka!` (3250, text) y `🎥 Video Eureka` (10598, file).
- Typo en producción: la opción del select dice `Esperando ¡Euerka!` — 28 clientes.

---

## §D — LE TOCA AL EQUIPO DE CLINERA (no lo construyo yo)

| # | Tarea | Por qué bloquea |
|---|---|---|
| **D1** | Agregar `Slug Clinera` a la tabla `Uso` (939) | Sin eso el tramo 3 no se puede apoyar en la 939 (§C1) |
| **D2** | Decir quién alimenta la 939 y cada cuánto | Si es manual, no es un gate de comisión confiable (§C2) |
| **D3** | **ACT-3: el endpoint `GET /status/{slug}`** | Es la fase 3 entera. Lo construyen ellos, yo dejo el adaptador listo. |
| **D4** | Confirmar los 6 supuestos del schema §5 | `tratamientos.con_duracion`, `plantillas.aprobadas_meta`, `embeds.hits_30d`, pasarela de pago, "3/3 bloques", y cómo se distingue una cita creada por IA |
| **D5** | Confirmar si la pasarela de pago es configurable hoy | La UI dice "PRÓXIMAMENTE · STAY TUNED" → si no existe, **A7 no puede ser gate**, va a N/A permanente |
| **D6** | Telemetría del iframe (`embeds.hits_30d`) | Probablemente no existe → **A6 a N/A permanente**. Fallback: contar citas con `origen=embed` |

---

## §E — DECISIONES QUE NECESITA RICARDO

### E1. ¿Qué hacemos con los 59 bloqueados solo por Mitzi?
El campo tiene 95% de nulos: nunca se usó. Tres caminos:
- **(a)** Aceptar el 2/105 como la verdad y que Mitzi vaya llamando para desatascar los 59.
- **(b)** Backfill: Mitzi marca retroactivamente los que sí verificó.
- **(c)** Sacar Mitzi del gate hasta que el proceso exista (el fix quedaría en 2 cambios, no 61).

Hoy está aplicado **(a)**, que es literalmente lo que pediste. Pero si mañana un onbordero ve
su cartera entera en amarillo, es por esto y no por su trabajo. **No lo cambio sin que lo digas.**

### E2. ¿Los 61 afectan comisiones ya pagadas?
No lo toqué. La 327 tiene `Estado pago comisión` (3252). Si alguien ya cobró por un cliente que
hoy volvió a 🟡, hay que decidir si se revierte o se respeta.

### E3. ¿`🚫 N/A` suma como check listo en la tabla nueva?
En la 327 suma. A2/A6/A7 van a caer en N/A muy seguido; si N/A suma, un Vortex se lleva 3 checks
gratis y llega a "entregado" más fácil que un Summit. **Mi recomendación: N/A sale del
denominador** (no suma como verde ni cuenta como aplicable) — que es lo que hace `stageStat()`
en tu prototipo. Voy a implementar eso salvo que digas lo contrario.

### E4. `Especialista` (texto) vs `Encargado` (select).
Para la tabla nueva uso solo `Encargado` con los 8 nombres del prompt. La 327 la dejo intacta.

### E5. ~~¿Dónde vive este proyecto?~~ ✅ RESUELTO 2026-07-17
Dijiste: no va a ningún repo, va a la VM. Job en `/opt/activacion/`, panel inyectado en
`/opt/work/site/index.html`. El código fuente del panel queda en `activacion/panel/`
(worktree local, sin commitear).

### E6. ¿Le sacamos a la gente el acceso de escritura directo a la tabla 957 en Baserow?
El candado de campos es del panel (§H2). Quien entre a `core.oacg.cl` directo puede editar
`📅 Entrega formal` y los crudos, y arrancar su propio reloj de comisión. Los checks no
(son fórmulas). Opciones: (a) confiar en el panel + que el job pise los crudos cada hora;
(b) quitar permisos de escritura sobre la 957 en Baserow salvo al usuario del job.
**Recomiendo (b)**, pero implica revisar quién tiene acceso al workspace 30.

---

## §G — FASE 2: lo que descubrí construyendo la tabla (tabla 957, 166 campos)

### G1. 🔴 Baserow no tiene permisos por campo. La REGLA DURA obliga a rediseñar los checks.

El prompt dice: *"Ningún check de etapas 1-3 puede quedar editable a mano en Baserow. Si el job
los escribe pero una persona los puede sobrescribir, no sirvió de nada."*

**Baserow no tiene permisos a nivel de campo.** No hay forma de decir "este single_select solo
lo escribe el job". Si los checks fueran single_select como pide el schema doc, cualquier
onbordero los pone en ✅ Listo con dos clics. Sería el mismo bug del panel anterior con otra cara.

**Lo que hice:** los 17 checks automáticos son **fórmulas derivadas de campos crudos**.
El job escribe `Sucursales cargadas = 2`; el check `C3 · Sucursales` es una fórmula
`if(cargadas >= declaradas, '✅ Listo', ...)`. **Las fórmulas son read-only por construcción**
— Baserow no deja editarlas ni por UI ni por API.

Para falsear un check ahora hay que falsear el contador crudo, y el job lo pisa en la sync
siguiente. Es la única forma de cumplir la regla de verdad dentro de Baserow.

**Costo:** el job es más simple (escribe números, no decide), pero la lógica de negocio queda en
fórmulas de Baserow en vez de en Python. Si mañana cambia un umbral, se toca `schema_def.py`
y se re-corre `build.py`.

### G2. 🔴 En este Baserow un número en blanco compara como 0. Casi meto el bug exacto que el proyecto combate.

Verificado a mano: con el campo vacío, `if(field('_n') >= 0, ...)` devuelve **verdadero**.

Sin guarda de nulos, `C3 = if(cargadas >= declaradas, '✅ Listo', ...)` en una clínica **sin
ningún dato** da `0 >= 0` → **✅ Listo**. Una clínica vacía se pintaría entera de verde y pasaría
a cobrar comisión.

**Lo que hice:** *todas* las fórmulas de check empiezan con `is_null()` sobre cada campo del que
dependen. Sin dato → `🚫 N/A`. Nunca verde, nunca rojo.

### G3. 🔴 El tipo `boolean` de Baserow no es nullable → lo reemplacé por tri-estado.

Un `boolean` en blanco se lee `false`, indistinguible de un "No" real. Si el endpoint devuelve
`null` en `cobros.medio_configurado`, un boolean lo leería como `❌ No` → check rojo. Eso viola
"null → N/A" y "nunca lo bajes a rojo por un timeout".

**Lo que hice:** todos los booleanos que escribe el job son `single_select` de tres estados:
blanco (= desconocido → N/A) · `✅ Sí` · `❌ No`.

### G4. 🔴 BUG QUE ENCONTRÉ Y ARREGLÉ: una etapa 100% N/A daba "✅ Completada".

La fórmula de etapa del schema doc es `if(sum(ok) = sum(ap), '✅ Completada', ...)`.
Con una clínica sin datos, todos los checks caen en N/A → `ok=0`, `ap=0` → **`0 = 0` → ✅ Completada**.

Lo verifiqué en vivo: la primera fila vacía mostraba **Etapas 1, 2 y 3 en ✅ Completada**.
Solo la Etapa 4 (que exige a Mitzi) impedía que dijera ENTREGADO.

**Es exactamente la clase de bug que este proyecto existe para matar**: silencio interpretado como éxito.

**El prototipo tiene el mismo fallo.** `stageStat()` hace `done: app.every(...)`, y
`[].every()` es `true` en JavaScript. No se nota porque el mock siempre trae datos.
**Si portas `stageStat()` tal cual al panel, el bug viaja con ella.** Lo arreglé en Baserow
(`and(sum(ap) > 0, sum(ok) = sum(ap))`) y hay que arreglarlo igual en la Fase 4.

### G5. La sintaxis de fórmulas de tu Baserow: lo que probé, no lo que supuse

| Función | ¿Existe? | Nota |
|---|---|---|
| `is_blank` | ❌ **NO** | **El schema doc la usa en 3 fórmulas. Fallarían.** Usar `is_null`. |
| `is_null` | ✅ | |
| `and()` / `or()` | ✅ pero **exactamente 2 args** | Confirmado, hay que anidar |
| `date_diff` · `date_interval` · `today()` · `todate()` | ✅ | |
| `count(field(<file>))` | ✅ | Por esto E1 "exige archivo" **sí es verificable por fórmula** |
| `is_null(<file>)` | ⚠️ siempre falso | Un campo file nunca es null; hay que usar `count() = 0` |

### G7. 🔴 SEGUNDO BUG DEL MISMO TIPO: con 0 sucursales, C4 daba verde.

`C4 · Horarios` es "todas las sucursales tienen horario". Con **0 sucursales**, eso es
**verdad vacía** → `0 == 0` → ✅ Listo. Una clínica sin nada cargado mostraba C4 en verde.

Apareció al correr el job contra la fixture `vacia`: daba `1/17` en vez de `0/17`.
Arreglado exigiendo `Sucursales cargadas > 0`. Hay test de regresión.

Los otros checks no tienen este problema porque su denominador los tapa (C3 `0>=2` es falso,
C5 `0>=2` falso, M4 `0>0` falso). C4 era el único sin denominador propio.

**Patrón a vigilar en la Fase 4:** los tres bugs que encontré (§G2, §G4, §G7) son el mismo —
*ausencia de datos interpretada como éxito*. Cualquier check nuevo hay que probarlo contra
la clínica vacía antes de darlo por bueno.

### G8. El equipo va a necesitar esto: el contrato tiene campos que nadie confirmó.

`contract.py` implementa el contrato tal como lo dictaste. Pero 4 de sus campos son los
supuestos sin confirmar del schema doc §5 (→ §D4): `tratamientos.con_duracion`,
`plantillas.aprobadas_meta`, `embeds.hits_30d`, `cobros.medio_configurado`.

Si ACT-3 llega sin esos campos, los contract tests lo van a decir de inmediato — que es
exactamente para lo que sirven. Los checks correspondientes (M2, A3, A6, A7) caerían a
`🚫 N/A` en vez de romper. Está diseñado para degradar, no para explotar.

### G6. El schema doc dice que no se pueden crear tablas ni campos. Vía API REST sí.

Ya está en §A3. Lo confirmo desde el otro lado: la tabla 957 con sus 166 campos la creé por API.
**Jorge no tiene que crear nada a mano.** `build.py` es idempotente y re-ejecutable.

---

## §H — FASE 4: lo que apareció construyendo el panel

### H1. 🔴 AGUJERO QUE ENCONTRÉ Y CERRÉ: `📅 Entrega formal` era editable a mano.

Los checks quedaron read-only solos (son fórmulas — `makeGrid` marca `formula` como `ro`).
Pero al inspeccionar el schema que el panel computa, **29 campos quedaban editables**, y
entre ellos estaban:

- **`📅 Entrega formal`** — el reloj de la comisión del tramo 3. El prompt es explícito:
  *"ningún humano puede escribir este campo — sería dejar que el onbordero arranque su
  propio reloj de pago"*. **Era escribible desde el drawer.**
- **Todos los campos crudos del job** (`Errores 24h`, `Pacientes cargados`, …). Los checks
  no son editables, pero los datos de los que dependen **sí lo eran**: poner `Errores 24h`
  en 0 dejaba `A4 · Automatizaciones` en verde. El candado de los checks servía de poco.
- **`Precio plan USD`** — el prompt dice que se lee de Stripe y jamás se edita a mano.

**Cerrado** con `ACT_JOB_FIELDS` + un override de `refreshSchema` en `act_module.js`.
Ahora **25 de 166** campos son editables, y son exactamente los que corresponden:
identidad/comercial, los 4 denominadores, la etapa 4 y los tramos de comisión.

### H2. ⚠️ El candado es del PANEL, no de Baserow. Limitación real, no la puedo cerrar.

Baserow **no tiene permisos por campo** (ya en §G1). Lo que hice bloquea la edición *desde
tech.oacg.cl*, que es por donde trabaja el equipo. Pero quien entre a Baserow directo
(`core.oacg.cl`) o use la API con el token puede editar cualquier cosa, incluida
`📅 Entrega formal`.

Los checks sí son inmunes en todos lados (son fórmulas, Baserow no deja escribirlas).
Los **crudos** no. La defensa real ahí es que **el job los pisa en la sync siguiente** —
pero eso solo funciona **cuando el job corra automático**, y hoy no corre (§H4).

→ Decisión tuya (**§E6**): ¿alcanza con el candado del panel, o hay que sacarle a la
gente el acceso de escritura directo a la tabla 957 en Baserow?

### H3. `Denominadores congelados` en D0+2: no lo puedo forzar por fila en el panel.

Los denominadores deben ser editables **solo antes de D0+2**. Eso es una regla **por fila**,
y el `ro` de `makeGrid` es **por campo para toda la tabla**. No hay dónde colgarlo sin
reescribir el drawer.

Hoy: los 4 denominadores quedan editables siempre desde el panel; el job pone el flag
`Denominadores congelados` en D0+2 pero **nadie lo hace cumplir en la UI**. La vista
"Sin denominador" sí funciona y muestra quién no puede avanzar.

Es una brecha conocida. Cerrarla es un trabajo aparte sobre el drawer de `makeGrid`.

### H4. El botón "Sincronizar" no dispara nada. A propósito.

El prototipo tiene `POST /sync/{slug}`. Ese endpoint **no existe** en `app.py` y no lo
construí. `GACT.sync()` muestra un toast explicando que el job corre en la VM
(`/opt/activacion/job`) y hay que llamarlo a mano. **No simulé un sync que no ocurre.**

### H5. La copia local del panel estaba desactualizada. Casi piso trabajo ajeno.

`~/Documents/Claude/OACG CLINIC/task-oacg/vm/work-index.html` (16-jul, 2885 líneas) vs el
vivo en la VM (**2930 líneas**). Si parcheaba sobre la copia local y subía, borraba 45
líneas de cambios de otra persona.

`patch.py` ahora exige bajar el vivo y **compara md5 antes de subir**; si el vivo cambió
desde que lo bajaste, aborta.

---

## §I — FASE 4b: cambios pedidos por Ricardo (2026-07-17, segunda tanda)

Implementado y desplegado en `tech.oacg.cl/activacion`. Los 6 puntos:

1. **Cómo se llena el tablero.** Hoy: a mano, desde el drawer de cada etapa (inputs de
   cantidad + evidencia foto/video). Vía API cuando exista ACT-3 — ahí el job pisa los
   crudos. Los checks/etapas/estado NO se escriben: son fórmula, se derivan.
2. **Etapas clickeables** → drawer lateral con los checks de esa etapa, cada uno con sus
   inputs de cantidad y botón 📎 foto/video (se guarda en el campo `<check> 📸`).
3. **Drawer redimensionable, system-wide.** Es el `#drawer` compartido: el cambio aplica a
   TODO el panel (leads, onboarding, etc.), no solo a activación. Ancho por defecto 640px,
   handle a la izquierda, se persiste en `localStorage work.drawer.w`.
4. **Encargados:** quitados Franco (despedido) y Frine. Quedan Brian, Rebeca, Catalina,
   Nohelymar, Jesús, Micaela.
5. **Totales:** Total · En proceso · Completado. Los 4 operativos (Vencidos, Sin
   denominador, Esperando Mitzi, Regresión) quedaron como chips-filtro debajo.
6. **Columna Mitzi** aprobar/observar → modal de nota → al aprobar fija `📅 Entrega formal`
   = hoy, marca AHA verificado, y muestra el contador `D+N desde entrega` + `comisión en
   (60−N)d / ✅ lista`. Guard: Mitzi solo puede aprobar si las etapas 1-3 están verdes,
   E1 tiene grabación y el sistema detectó el AHA (spec original).

### I1. ✅ EL CORREO FUNCIONA END-TO-END (resuelto 2026-07-17 con la n8n key).

Ricardo pasó la API key de n8n. Circuito completo montado y probado:

**panel (aprueba Mitzi) → `POST /work-api/notify-complete` → n8n webhook → Gmail → ricardo@oacg.cl**

- **Workflow n8n creado:** `OACG TECH → Activación | Aviso onboarding completado (webhook)`
  (id `oobPgz0DaQz4jOMy`, **activo**), en `https://n8n.oacg.cl`.
- **Webhook (producción):** `https://n8n.oacg.cl/webhook/activacion-completada-9f2`
- **Nodo Gmail** reusa la credencial `gmailOAuth2` `Pf3R4wpW3w8FFqYr` (la misma del workflow
  activo "OACG TAREAS | Avisos por correo"). No creé credenciales nuevas.
- **Env en la VM:** `NOTIFY_WEBHOOK_URL` seteada en `/opt/work/docker-compose.yml`
  (bloque `workapi:`, estilo mapa `KEY: "valor"`) y contenedor recreado.
- **Probado:** llamada real `docker exec work-workapi-1 → /notify-complete` devolvió
  `{"ok": true}` y la ejecución n8n quedó en `success` (Gmail messageId devuelto).
  Se enviaron ~4 correos de prueba a ricardo@oacg.cl.

**Trampa que encontré (por si hay que reeditar el workflow):** al crear el nodo Gmail vía API,
las expresiones `{{ $json.body.* }}` se me rompieron dos veces —
(a) un heredoc de shell sin comillas se comió los `$json` (quedó `.body`, "invalid syntax"),
y (b) comillas dobles escapadas en el HTML del mensaje. Solución: editar el workflow desde un
archivo Python (sin heredoc) y HTML sin comillas dobles. El nodo Gmail que funciona no lleva
`emailType`, solo `sendTo/subject/message/options`.

**Sigue siendo enchufable:** si el webhook cambia, se actualiza `NOTIFY_WEBHOOK_URL` y
`docker compose up -d workapi`. Si la env no está, el endpoint responde `{ok:false}` sin
romper la aprobación.

### I2. ⚠️ La entrada manual reabre (a propósito) la edición de los crudos.

En §H1/H2 bloqueé los crudos para que nadie los tocara. Ahora el punto 2 pide cargarlos a
mano. Solución: los crudos siguen **read-only en el drawer genérico**, pero el **drawer de
etapa** es la superficie sancionada que los escribe (`GACT.setRaw`). `📅 Entrega formal`,
`Última sync` y el precio de Stripe siguen bloqueados **también** ahí (lista `ACT_HARD_LOCK`);
Entrega formal solo la escribe la aprobación de Mitzi. La integridad en modo manual la da la
**evidencia foto/video por check** + la revisión de Mitzi. Cuando llegue ACT-3, el job pisa
los crudos y la entrada manual pasa a ser el fallback.

### I3. Lo que NO pude probar end-to-end (honesto).

El **upload de evidencia** y el **correo** pasan por `/work-api/*`, que solo existe en la VM
(mi server local no lo proxya) y `tech.oacg.cl` exige login Google que no puedo hacer
headless. Probé contra la VM que el endpoint `/notify-complete` responde bien y que `/upload`
+ la tabla 957 están habilitados, y toda la lógica (guard de Mitzi, fijar Entrega formal,
contador, escritura de crudos) contra Baserow real desde el navegador. **El flujo completo
"subir grabación real → aprobar → estado ENTREGADO" en producción con sesión autenticada
no lo ejecuté yo.** Queda por validar con un login real.

---

## §J — CONTRASTE app.clinera.io vs panel /activacion (2026-07-17, solo lectura)

Leí el código real de `clinera-web` (hands-off, **no modifiqué nada**) y lo comparé contra los
20 checks y el contrato ACT-3. Es un **frontend Next.js que proxya un backend externo** (no hay
Prisma acá; el modelo vive en servicios TS + backend remoto), así que "existe" = el campo/ruta
está en el contrato de este front.

### Lo que YA es real (bajo riesgo, el dato existe)
C3 Sucursales · C5 Usuarios+roles · M1 Profesionales · M2 Tratamientos (**`duracionPorSesion`
+ `precio` existen** — era el gran desconocido) · M3 Pacientes · M4 Citas futuras (query) ·
M5 Ficha+consentimientos · A1 Agente texto · A3 Plantillas (**estado Meta APPROVED existe** vía
Fluentia) · A5 Difusiones+audiencias. C2 WhatsApp existe pero como booleano `connected`, no enum.

### Lo que NO existe y le toca construir al equipo de Clinera (para que ACT-3 sirva)

| # | Gap | Impacto en el panel |
|---|---|---|
| **J1** | **AHA: la cita NO registra si la creó la IA.** `TurnoOrigen` es canal de marketing (instagram/web/whatsapp…), no `ia \| manual \| embed`. | **Es el más grave.** Sin esto, el "dato duro" del AHA no se puede detectar → la Entrega formal y la comisión del tramo 3 no se pueden gatear de forma automática. Hoy se suple a mano. |
| **J2** | **A2 CAMILA no existe en absoluto** — ni modelo, ni feature flag, ni integración de voz. | Correcto que A2 esté en 🚫 N/A. Confirma que CAMILA es 100% futuro. |
| **J3** | **A7 pasarela de pago al paciente: "planned / próximamente".** El Stripe/MercadoPago del código es para la suscripción de Clinera, no para que la clínica cobre. `medios-pago` son solo etiquetas. | A7 debe quedar 🚫 N/A permanente hasta que exista. |
| **J4** | **A4 sin contadores `enviados_24h` / `errores_24h`.** El modelo solo tiene `is_active`. | El check crítico (error<5%) no se puede computar sin esos contadores. |
| **J5** | **A6 embed sin telemetría `hits_30d`.** Las páginas embed existen pero no cuentan hits. | A6 en N/A hasta que haya telemetría. |
| **J6** | **C1 timezone no está en la clínica**, solo por sucursal (`Sucursal.timezone`). | ACT-3 tiene que decidir si el timezone es a nivel clínica o sucursal. |
| **J7** | **No hay un endpoint ACT-3 único todavía**, pero **NO es de cero**: ya existen `GET /clinica/{slug}/onboarding/status` (pasos booleanos) y `GET /clinica/{slug}/estadisticas` (conteos agregados). El equipo puede **extender esos** en vez de partir en blanco. |

### Aclaraciones de Ricardo (2026-07-17, mirando el dashboard real)

- **J1 CORREGIDO — mi análisis se equivocó.** El dashboard de Clinera **SÍ tiene un panel
  "Agendados por IA"** (mostró 41, 3.7% este mes). O sea el **dato duro del AHA existe** como
  conteo por clínica. Lo que el agente no encontró fue el flag *por cita*, pero el **agregado
  `citas_ia.total` sí está disponible** — que es justo lo que necesita el check del AHA. ACT-3
  lo puede exponer. **J1 deja de ser bloqueante.**
- **J2 y J3 confirmados por Ricardo:** CAMILA (voz) y la pasarela de pago **aún no existen**.
  A2 y A7 quedan 🚫 N/A. Correcto.
- **J4 es prioridad de Ricardo → lo marqué CLAVE en el panel.** Dijo textual: "falta
  revisar/testear que las automatizaciones lleguen sin errores, eso es importante colocar como
  clave". **Hecho:** A4 ahora tiene badge `⚠️ CLAVE`, tarjeta resaltada, muestra la **tasa de
  error 24h en rojo** (ej. 11.3% = 58/512 con el aviso "el cliente pierde citas y no lo sabe"),
  y un flag `⚠️ automatiz.` en la fila cuando supera 5%. Falta que Clinera exponga
  `enviados_24h`/`errores_24h` para que sea automático (hoy se carga a mano).
- **J8 RESUELTO — el panel está correcto.** Ricardo: "próximamente cambiaremos los planes
  actuales a los nuevos (Vortex, Atlas y Summit)". El panel ya usa la taxonomía nueva; el
  producto se renombra después. **No hay nada que cambiar.**
- **J9 — dejar flexible.** Ricardo: "el agente de texto próximamente se va a mejorar". El
  número de bloques está en cambio, así que no fijar 3 vs 4 hasta que se estabilice. Cuando
  ACT-3 exponga `bloques_completos`, se ajusta el umbral en un solo lugar.

**Conclusión actualizada:** el panel está bien y con A4 ya resaltado como clave. Lo que falta
es del lado de Clinera para ACT-3: **J4** (contadores de envío/error — el más importante),
**J5** (telemetría embed), **J6** (timezone a nivel clínica) y **J7** (unificar el endpoint,
extendiendo `onboarding/status` + `estadisticas` + "Agendados por IA"). J1/J2/J3/J8/J9 ya no
requieren acción del panel.

---

## §F — SEGURIDAD (encontrado de paso, no lo toqué)

1. **El database token de Baserow está hardcodeado en el bundle del cliente**
   (`work-index.html:86`: `const TOKEN='Token Zhvuqh5QzRRW9eRYNMji8dw68mUOxuaJ'`).
   Cualquiera que cargue tech.oacg.cl lo puede leer. El único gate es oauth2-proxy.
2. **`~/Documents/Claude/OACG CLINIC/task-oacg/vm-info.txt` tiene el JWT de refresh vivo
   (exp 2036) y las contraseñas en texto plano** de `work` y `clinic`, en el árbol de trabajo.

Ninguna de las dos la causé ni la modifiqué. Valen rotación y `.gitignore`.
</content>
</invoke>
