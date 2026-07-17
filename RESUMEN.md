# RESUMEN — Sistema de Activación Clinera · 2026-07-17

Fases 0, 1, 2, 3 y 4 cerradas y verificadas. **La 5 no la construí.**
`https://tech.oacg.cl/activacion` está vivo.
Detalle en `PROGRESO.md`, evidencia en `HALLAZGOS.md`.

## 1. El fix de la fase 1: 61 clientes. Pero ya estaba aplicado.

**De 63 → 2 ✅ ONBOARDEADO. Cambiaron 61.** Los 2 que quedan: **ARMONIA** y **BELLA VITA**,
los únicos con `Mitzi = ✅ Conforme`.

Lo aplicó una sesión previa, no yo. Lo verifiqué de forma independiente simulando ambas
fórmulas sobre las 105 filas: la simulación estricta reproduce el estado vivo con **0
discrepancias**. No volví a tocar el campo.

**Y los 61 no son 61 mentiras** — esto es lo que más importa del informe:

| Causa | Clientes |
|---|---|
| **Backdoor puro** (Aprobado con AHA pendiente) → onboarding falso real | **2** — IBRACKETS y MY CLINIC |
| **Solo les falta el registro de Mitzi** (6 pasos + AHA validado) | **59** |

**100 de 105 filas tienen `📞 Verificación Mitzi` en blanco.** Ni ⏳ Pendiente: vacío.
Un campo con 95% de nulos no es un gate que la gente esquivó — es un gate que **nunca se
operacionalizó**. La lectura honesta de los 59 es "no sabemos", no "59 falsos". → decisión tuya.

## 2. La tabla `Uso` (939): **NO sirve** para el gate de adopción. Y no sé quién la alimenta.

Apostabas a que sí. La leí completa y no:
1. **No tiene slug** ni ningún id. El único identificador es `Name`, texto libre.
2. **No joinea con la 327**: dice `Clínica Antuka` vs `ANTUKA`, `Kompass (Jorge Cusme)` vs `KOMPASS`.
   Joinear eso es fuzzy matching sobre clientes que pagan comisiones de US$50. No lo hice.
3. **Taxonomía legacy**: su `Plan` solo tiene `CLINERA` (41) y `ECOSISTEMA` (9). Cero Vortex/Atlas/Summit.
4. Son **50 filas**, no 105. Menos de la mitad de la cartera.
5. `Grupo` tiene **tres** valores, no dos: 🟢 Usando (26) · 🟡 Sin uso · nueva (15) · 🔴 Sin uso · riesgo (9).

**Quién la alimenta y cada cuánto: no lo sé.** No hay workflow n8n en disco que la toque, no hay
credenciales de n8n en esta máquina, y la API no expone `updated_on`. **No lo inventé.**
Sirve como prueba de que alguien ya calcula consumo por clínica; no como fuente enchufable.
Para usarla, la 939 necesita `Slug Clinera`.

## 3. Checks en N/A permanente (hasta que el equipo confirme)

| Check | Por qué |
|---|---|
| **A6 · Embed** | `embeds.hits_30d` casi seguro no existe: hay que construir la telemetría del iframe |
| **A7 · Cobros** | en Marketing → Integraciones, Stripe y MercadoPago dicen "PRÓXIMAMENTE · STAY TUNED". Si la pasarela no se configura dentro de la app, **A7 no puede ser gate** |
| **A2 · CAMILA** | N/A permanente en Vortex **por diseño** — correcto, no es deuda |

Ninguno los puse en verde "para que compile". Van a `🚫 N/A` y salen del denominador
(un Vortex marca 16/19, no 16/20).

## 4. Qué le toca al equipo de Clinera

1. **ACT-3: el endpoint `GET /status/{slug}`.** Es la fase 3 entera. No lo construí ni abrí su repo.
   Cuando exista: setear `CLINERA_STATUS_URL` y listo. Los contract tests dicen si cumple.
2. **`Slug Clinera` en la tabla `Uso` (939)** — sin eso el tramo 3 no se apoya ahí.
3. **Decir quién alimenta la 939 y cada cuánto.** Si es manual, no es un gate de comisión confiable.
4. **Confirmar 4 campos del contrato** que hoy son supuestos: `tratamientos.con_duracion`,
   `plantillas.aprobadas_meta`, `embeds.hits_30d`, `cobros.medio_configurado`.
5. **Telemetría del iframe** (A6) y **confirmar la pasarela de pago** (A7).

## 5. Qué necesitas decidir tú

1. **Los 59 bloqueados solo por Mitzi.** ¿Aceptar el 2/105 (hoy)? ¿Backfill retroactivo?
   ¿O sacar a Mitzi del gate hasta que el proceso exista? Si un onbordero ve su cartera entera
   en amarillo, es por esto y no por su trabajo.
2. **¿Los 61 afectan comisiones ya pagadas?** La 327 tiene `Estado pago comisión`. No lo toqué.
3. **¿`🚫 N/A` suma como check listo?** En la 327 suma. Yo lo saqué del denominador (que es lo
   que hace tu prototipo). Si N/A sumara, un Vortex se llevaría 3 checks gratis.
4. **¿Le sacamos a la gente el acceso de escritura directo a la tabla 957 en Baserow?**
   Bloqueé los campos críticos en el panel, pero Baserow no tiene permisos por campo: quien
   entre a `core.oacg.cl` directo puede editar `📅 Entrega formal` y arrancar su reloj de
   comisión. Los checks no (son fórmulas). Recomiendo quitar escritura sobre la 957 salvo al
   usuario del job.

## 6. Qué NO construí — brutalmente honesto

- **Fase 5 (screenshots): NO EMPEZADA.** Cortable por diseño, y la corté. Los 17 campos 📸
  existen y están bloqueados, pero nadie los llena.
- **El botón "Sincronizar" del panel no dispara nada.** El endpoint `POST /sync/{slug}` no
  existe; muestra un toast explicando que el job corre en la VM. No simulé un sync que no ocurre.
- **El alta de clientes no está cableada.** El prototipo dice "entra solo desde Stripe vía
  n8n". Hoy la tabla 957 se llena a mano. No toqué n8n.
- **Los denominadores se pueden editar después de D0+2 desde el panel.** La regla es por fila
  y el bloqueo de `makeGrid` es por campo. Brecha conocida (HALLAZGOS §H3).
- **La frecuencia (1h / 24h) NO está activa.** Dejé el `.service` y el `.timer` de systemd
  escritos en `/opt/activacion/deploy/`, pero **sin instalar a propósito**: hoy el job lee
  fixtures y correrlo cada hora solo escribiría datos de prueba. Se activa con ACT-3, siguiendo
  `INSTALAR.md`. Hoy `sync.py` corre a mano: **nadie lo llama solo.**
- **`📅 Entrega formal` nunca se disparó de verdad.** La lógica está y es write-once, pero
  ninguna fixture llega a las 4 etapas (todas mueren en la etapa 4, que es manual). El camino
  feliz completo **no está probado end-to-end** — requiere subir un archivo real a E1.
- **El job nunca vio datos reales.** Todo es fixture. El día que ACT-3 exista, el contrato puede
  no calzar. Para eso están los contract tests, pero **no es lo mismo que haberlo probado**.
- **Dejé 6 filas DEMO en la tabla 957** (ids 10–15, slugs de fixture). Hay que borrarlas antes
  de operar. El comando está en `PROGRESO.md`.
- **La regla "ningún check editable a mano" la cumplí cambiando el diseño**, no como pedía el
  schema doc: los checks son fórmulas derivadas, no single_select que escribe el job. Baserow no
  tiene permisos por campo — un single_select lo edita cualquiera con dos clics. Es una
  desviación deliberada y es el motivo de que la tabla tenga 166 campos y no ~90.

### Tres bugs de "silencio = éxito" que encontré construyendo, y uno viaja en tu prototipo

1. **Un número en blanco compara como 0** en este Baserow. Sin guarda, una clínica **sin datos**
   daba `0 >= 0` → **todos los checks verdes**. Ahora toda fórmula empieza con `is_null()`.
2. **Una etapa con todos los checks en N/A daba "✅ Completada"** (`0 = 0`). Lo vi en vivo: la
   primera fila vacía mostraba Etapas 1, 2 y 3 completas. **`stageStat()` de tu prototipo tiene
   el mismo fallo** — `[].every()` es `true` en JS. En Baserow está arreglado; **en el prototipo no.
   Si lo portas tal cual a la fase 4, el bug viaja.**
3. **Con 0 sucursales, C4 daba verde** por verdad vacía ("todas tienen horario").

Los tres son el mismo bug que este proyecto existe para matar. Los tres tienen test de regresión.

### Y una que no es mía pero la viste de paso
El **database token de Baserow está hardcodeado en el bundle del cliente** de tech.oacg.cl
(`work-index.html:86`): cualquiera que cargue la página lo lee. Y `task-oacg/vm-info.txt` tiene
el JWT de refresh vivo (exp 2036) y contraseñas en texto plano, en el árbol de trabajo.
No las toqué. Valen rotación.

---

### El agujero que encontré al final (y cerré)
Los checks quedaron read-only solos por ser fórmulas. Pero **`📅 Entrega formal` era
editable a mano desde el drawer** — o sea, un onbordero podía escribir su propia fecha de
entrega y arrancar su reloj de comisión del tramo 3. Y los **crudos** también: poner
`Errores 24h` en 0 dejaba A4 en verde, con el check "bloqueado" y todo. Cerrado: de 166
campos, ahora 25 editables.

⚠️ Pero ese candado es **del panel**. Baserow no tiene permisos por campo: quien entre a
`core.oacg.cl` directo todavía puede editar esos campos. Los checks no (son fórmulas).
→ decisión §E6.

---

**Estado verificable ahora mismo:**
- Tabla **957** `Activación`: 166 campos, 0 errores · **32/32** aserciones contra filas reales
- Job en `/opt/activacion/` de la VM: **25/25** contract tests, idempotente, corriendo ahí
- Panel **`https://tech.oacg.cl/activacion`**: vivo, 4 vistas probadas con filas que las
  disparan, 25/166 campos editables, 0 errores de consola
- **Quedan 6 filas DEMO en la tabla 957** (ids 10–15). Borrarlas antes de operar.
