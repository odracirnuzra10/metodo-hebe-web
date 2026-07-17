# PROGRESO — Sistema de Activación Clinera

Última actualización: 2026-07-17

## Estado global

| Fase | Estado | Nota |
|---|---|---|
| 0 · Reconocimiento | ✅ **CERRADA** | Repos, schema 327, tabla 939 y prototipo leídos. |
| 1 · Fix fórmula 3285 | ✅ **YA ESTABA APLICADO** | Lo aplicó una sesión previa. Verificado en vivo: 63 → 2. **No lo re-apliqué.** |
| 2 · Tabla `Activación` | ✅ **CREADA Y VALIDADA** | **Tabla 957**, 166 campos, 0 errores. 29/29 aserciones OK contra filas reales. |
| 3 · Job de sync (fixtures) | ✅ **HECHO Y VERIFICADO** | Adaptador + 6 fixtures + 25 contract tests. Corrido end-to-end contra Baserow, idempotente. |
| 4 · Panel /activacion | ✅ **VIVO + 2ª tanda de cambios** | Etapas clickeables, drawer redimensionable, Mitzi, KPIs. **Correo end-to-end funcionando** (n8n). Ver HALLAZGOS §I. |
| 5 · Screenshot automático | ⏭️ **SIGUIENTE (y cortable)** | No empezada. Es la única fase que falta. |

## Próximo paso concreto

**Fase 5 — screenshots automáticos.** Es la fase cortable y depende de ACT-3.
Cuando el job detecta que un check pasa de ✗ a ✅, sacar captura headless (Playwright)
de la pantalla del panel del cliente y subirla al campo `<check> 📸` de la tabla 957.

Los 17 campos 📸 **ya existen** y ya están bloqueados en el panel. El mapa check→URL está
en el prompt original. Ojo: necesita una sesión de servicio de **solo lectura** contra
app.clinera.io — si Clinera tiene que exponer algo para eso, va a HALLAZGOS, no se construye.

**Antes que la fase 5, esto rinde más:**
1. Borrar las 6 filas DEMO de la tabla 957 (ver abajo).
2. Cablear el alta de clientes desde Stripe/n8n (hoy la tabla se llena a mano).
3. Endpoint `POST /sync/{slug}` en `app.py` para el botón "Sincronizar" (hoy `GACT.sync()`
   solo muestra un toast explicando que el job corre en la VM).

## Fase 4 — el panel (VIVO)

`https://tech.oacg.cl/activacion` · código fuente en **`activacion/panel/`** (ver su README).

- **No se toca `index.html` a mano.** `act_module.js` + `act.css` se inyectan con
  `patch.py`, que es idempotente y aborta si un ancla no calza exactamente 1 vez.
- **Bajar siempre el vivo antes de editar.** Lo comprobé: el `index.html` de la VM tenía
  2930 líneas vs 2885 de la copia local del 16-jul. Editar sobre la copia vieja habría
  borrado trabajo ajeno. `patch.py` verifica md5 antes de subir.
- Backups en la VM: `/opt/work/site/index.html.bak-<TS>` y `app.py.bak-<TS>`.
- `app.py`: se agregó `957` a `TABLAS_PERMITIDAS`. Requiere `docker restart work-workapi-1`
  (**workapi**, no `work-work-1`, que es nginx — me equivoqué la primera vez).

### Verificado en el navegador, no a ojo
- Las 4 vistas cazan **exactamente** la fila correcta — creé filas que disparan cada una
  (sin denominador / D0+20 sin entregar / entrega formal con estado no-ENTREGADO), comprobé,
  y las borré.
- Banner "⏳ N de M sin sincronizar — esperando el endpoint de Clinera (ACT-3)".
- Contadores con denominador y Progreso respetando N/A (Vortex = **16/19**).
- **De 166 campos, solo 25 editables.** `📅 Entrega formal`, los crudos del job y el precio
  de Stripe: bloqueados. Ver HALLAZGOS §H1.
- 0 errores de consola · JS parseado con `vm.Script` antes de cada subida.

## Desplegado en la VM GCP (2026-07-17)

**Decisión de Ricardo: esto NO va a ningún repo. Vive en la VM.**

| | |
|---|---|
| VM | `ricardooyarzun_macair@34.176.251.239` · `ssh -i ~/.ssh/google_compute_engine` · `sudo -n` sin password |
| Ruta | **`/opt/activacion/`** (junto a `/opt/work`, `/opt/task`, etc.) |
| Credenciales | `/opt/activacion/.env` (root, 600). `br.py` lee env primero, archivo después. |
| Verificado en la VM | **25/25** contract tests · `sync.py` lee Baserow OK · Python 3.12 |

**El timer de systemd está escrito pero NO instalado, a propósito.**
`/opt/activacion/deploy/` tiene `.service`, `.timer` e `INSTALAR.md`. Hoy el job lee
**fixtures**: activarlo cada hora solo escribiría datos de prueba en la tabla 957.
Se activa cuando exista ACT-3, siguiendo `INSTALAR.md`.

Para re-subir después de editar local:
```bash
KEY=~/.ssh/google_compute_engine; VM=ricardooyarzun_macair@34.176.251.239
cd <worktree> && COPYFILE_DISABLE=1 tar czf /tmp/activacion.tgz activacion
scp -i $KEY /tmp/activacion.tgz $VM:/tmp/
ssh -i $KEY $VM 'sudo -n tar xzf /tmp/activacion.tgz -C /tmp && sudo -n cp -R /tmp/activacion/. /opt/activacion/ && sudo -n find /opt/activacion -name "._*" -delete'
```
⚠️ `COPYFILE_DISABLE=1` es obligatorio: sin eso macOS mete archivos `._*` y el
`FixtureAdapter` los toma como fixtures (`._amedias.json` termina en `.json`).

## Fase 3 — lo construido (`activacion/job/`)

| Archivo | Qué |
|---|---|
| `adapter.py` | `FixtureAdapter` (default) · `HttpAdapter` (si `CLINERA_STATUS_URL`) · loguea el modo en mayúsculas |
| `contract.py` | la forma del JSON de ACT-3 + `validate()` → los contract tests dicen si el endpoint cumple |
| `mapping.py` | contrato → campos crudos. Mapa timezone/moneda por país |
| `sync.py` | el job: diff, congelar denominadores, entrega formal write-once, log por corrida |
| `test/fixtures/` | 6: completa · amedias · vacia · autofalla(11%) · vortex · tzmala |
| `test/test_contract.py` | **25 tests, 25 ok** |

**Verificado end-to-end contra Baserow real** (6 filas demo, slugs = fixtures):

| slug | Progreso | Etapas 1/2/3/4 | Lo que demuestra |
|---|---|---|---|
| `completa` | 17/20 | ✅ ✅ ✅ 🟡 | etapa 4 bloqueada: falta Mitzi/E1 (correcto) |
| `autofalla` | 16/20 | ✅ ✅ 🟡 🟡 | **11.33% de error → A4 NO verde**. El check crítico funciona. |
| `tzmala` | 16/20 | 🟡 ✅ ✅ 🟡 | clínica CL con timezone de Argentina → C1 cae. Cazado. |
| `vortex` | 16/**19** | ✅ ✅ ✅ 🟡 | A2 = 🚫 N/A y **sale del denominador**. Vortex nunca bloqueado por CAMILA. |
| `amedias` | 11/**18** | ✅ 🟡 🟡 🟡 | `hits_30d` y `cobros` null → A6/A7 en N/A + registrados en hallazgos |
| `vacia` | 0/17 | 🟡 🟡 🟡 🟡 | sin datos = 🟡, **nunca verde** |

Idempotencia comprobada: segunda corrida = `{'sin-cambios': 6}`.

**Las 6 filas DEMO siguen en la tabla 957** (ids 10–15). Son datos de fixture, no clientes
reales. Hay que borrarlas antes de operar de verdad:
`python3 -c "import sys;sys.path.insert(0,'activacion/baserow');import br;[br.delete_row(957,r['id']) for r in br.rows(957)['results']]"`

## Fase 2 — lo construido (tabla 957)

`Activación` en database 97. **166 campos, 0 con error.** Filas: 0 (limpia).

| Grupo | Campos | Qué es |
|---|---|---|
| Base | 71 | identidad, plan, denominadores, **crudos que escribe el job**, etapa 4 manual, AHA, ops, tramos |
| Screenshots | 17 | `C1 📸` … `A7 📸` (file, los escribe el job) |
| Checks | 20 | C1–C5, M1–M5, A1–A7 (**fórmulas derivadas**) + E1/E2/E3 · Check |
| ok_/ap_ | 40 | patrón del schema: `ok_X` (verde=1) y `ap_X` (N/A=0) |
| Etapas | 5 | Etapa 1–4 + `AHA detectado` |
| Finales | 12 | `🚦 Estado`, Progreso, SLA, D+60, Gate tramo 2/3, Comisión total, Plan · detalle |

Código: `activacion/baserow/` — `schema_def.py` (definición declarativa),
`build.py` (idempotente, re-ejecutable), `validate.py` (29 aserciones), `schema_final.json` (dump).

### Validación (29/29, contra filas reales, creadas y borradas)
- **clínica vacía** → las 4 etapas 🟡, checks 🚫 N/A. **No verde.**
- **automatizaciones al 11%** → `A4 · Automatizaciones` NO verde, Etapa 3 bloqueada. El check crítico funciona.
- **Vortex** → `A2 CAMILA` = 🚫 N/A, `ap_A2`=0 (sale del denominador), Etapa 3 igual se completa.
  Un Vortex nunca queda bloqueado por CAMILA.
- **E1 marcada "✅ Completada" sin archivo** → `ok_E1`=0, Etapa 4 bloqueada.
- **AHA sin verificar por Mitzi** → Etapa 4 bloqueada.
- **Mitzi verifica un AHA que el sistema no detectó** (citas IA = 0) → Etapa 4 bloqueada.
  Es la doble llave: impide firmar un Eureka de compromiso.
- **a medias** → M2/M3/A3 en ⏳, A6/A7 en 🚫 N/A por null.

## Dónde encontré las cosas (esto costó tiempo, no lo repitas)

| Qué | Dónde |
|---|---|
| `SCHEMA-baserow-activacion.md` | `~/Library/Application Support/Claude/local-agent-mode-sessions/53c4fefc-.../local_dc6649c1-.../outputs/` |
| `activacion-prototipo.html` | misma carpeta (601 líneas, mock puro, sin endpoints reales) |
| Sesión previa (fase 1 aplicada) | `.claude/worktrees/clinera-activation-system-30f579/` → su `PROGRESO.md` y `HALLAZGOS.md` |
| Panel tech.oacg.cl (copia local) | `~/Documents/Claude/OACG CLINIC/task-oacg/vm/work-index.html` (2885 líneas) + `work-app.py` |
| Baserow | `https://core.oacg.cl` · creds en `~/.config/baserow/credentials` |

## Acceso Baserow — verificado

- El `BASEROW_TOKEN` de credentials es un **database token**: sirve para filas, **no** para
  crear tablas/campos.
- Para schema hay que sacar JWT:
  `POST /api/user/token-auth/` con `BASEROW_EMAIL`/`BASEROW_PASSWORD` → `Authorization: JWT <token>`.
- **El schema doc afirma que "no se pueden crear tablas ni campos".** Eso es cierto para el
  conector MCP, pero **falso para la API REST con JWT**. La fase 2 sí es ejecutable por mí.
  (→ HALLAZGOS §A1)

## Fase 1 — verificación independiente (no re-aplicada)

La fórmula viva de 3285 hoy es **carácter por carácter** la fórmula objetivo del prompt.
Ya tiene el gate de Mitzi y ya no tiene el backdoor `or(... = 'Aprobado', ...)`.

Simulé ambas fórmulas en Python sobre las 105 filas reales:

| | Backdoor (simulado) | Estricta (simulado) | **Vivo hoy (real)** |
|---|---|---|---|
| ✅ ONBOARDEADO | 63 | 2 | **2** |
| 🟡 EN PROCESO | 40 | 101 | **101** |
| ⛔ CANCELADO | 2 | 2 | **2** |

La simulación estricta coincide con el estado vivo en **las 105 filas, 0 discrepancias**.
Eso confirma que el fix ya está aplicado y que el número de la sesión previa (61 cambios) es correcto.
**No volví a tocar el campo 3285.**

## Decisiones tomadas y por qué

1. **No re-apliqué la fase 1.** Ya estaba. Re-patchear un campo correcto es riesgo sin beneficio.
   Lo que sí hice fue verificarlo de forma independiente en vez de creerle al doc de la sesión previa.
2. **Escribo el proyecto en este worktree, pero NO lo commiteo al repo de Hebe.**
   Este worktree es `metodo-hebe-web` (sitio de marketing en Vercel), no tech.oacg.cl.
   tech.oacg.cl no existe como repo. (→ HALLAZGOS §B1)
3. **La tabla 939 `Uso` NO sirve hoy para el gate de adopción**, por 3 razones duras
   (sin slug, taxonomía legacy, nombres que no joinean). (→ HALLAZGOS §C1)
4. **No inventé el feeder de la 939.** No pude determinarlo. Queda como null explícito.
5. **Los 17 checks automáticos son FÓRMULAS derivadas, no single_select que escribe el job.**
   Es una desviación deliberada del `SCHEMA-baserow-activacion.md`. Razón: la REGLA DURA dice
   "ningún check de etapas 1-3 puede quedar editable a mano". Baserow **no tiene permisos por
   campo**, así que un single_select que escribe el job es editable por cualquiera con acceso —
   exactamente la falla del panel anterior. Una fórmula es read-only por construcción.
   El job escribe solo los **campos crudos** (contadores y estados); el check se deriva.
   Para falsear un check habría que falsear el contador, y el job lo pisa en la sync siguiente.
   (→ HALLAZGOS §G1)
6. **Los booleanos que escribe el job son single_select tri-estado, no boolean.**
   El `boolean` de Baserow no es nullable: un dato desconocido se leería como `false` y bajaría
   el check a rojo. Eso viola "null → N/A, nunca rojo por timeout". (→ HALLAZGOS §G3)
7. **N/A sale del denominador** (no suma como verde ni como aplicable), que es lo que hace
   `stageStat()` del prototipo. Pendiente de tu confirmación en HALLAZGOS §E3.
</content>
</invoke>
