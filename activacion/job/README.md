# Job de sync — `Activación`

Lee el estado real de cada clínica y lo escribe en Baserow tabla **957** (`Activación`).

## El punto entero

**El job NO decide si un check está verde.** Escribe solo **datos crudos**
(`Sucursales cargadas = 2`, `Errores 24h = 58`). Los 17 checks automáticos son
**fórmulas derivadas en Baserow**, y por lo tanto **read-only**: nadie los puede
editar a mano, ni por la UI ni por la API.

Esa fue la falla del panel anterior — si una persona puede sobrescribir el check,
el auto-reporte vuelve por la ventana. Baserow no tiene permisos por campo, así
que derivarlos es la única forma real de cumplir la regla.

## Correr

```bash
python3 sync.py                 # todas las filas con Slug Clinera
python3 sync.py completa        # una sola (esto llama el botón "Sincronizar")
python3 sync.py --dry           # no escribe, reporta el diff
python3 test/test_contract.py   # contract tests (25)
```

## Modo fixture vs HTTP

| Env | Modo | Qué hace |
|---|---|---|
| *(nada)* | **FIXTURE** ← hoy | Lee `test/fixtures/*.json` |
| `CLINERA_STATUS_URL=https://…` | **HTTP** | `GET {URL}/{slug}` con `Authorization: Bearer $CLINERA_SERVICE_TOKEN` |

**El endpoint todavía no existe** — lo construye el equipo de Clinera (ACT-3).
El día que exista: setear `CLINERA_STATUS_URL` y `CLINERA_SERVICE_TOKEN`. **Nada más.**
El job loguea en mayúsculas en qué modo corre, para que nunca haya duda de si los
datos son reales o de fixture.

Para saber si el endpoint cumple el contrato:
```bash
CLINERA_STATUS_URL=https://… python3 test/test_contract.py
```

## Fixtures

| Fixture | Para qué |
|---|---|
| `completa` | Atlas con todo verde |
| `amedias` | migración incompleta · `embeds.hits_30d` y `cobros` en **null** → N/A |
| `vacia` | clínica recién creada, todo en 0 |
| `autofalla` | **512 enviados, 58 errores (11.3%)** — el caso crítico real |
| `vortex` | plan sin CAMILA → A2 debe ser N/A, nunca bloqueante |
| `tzmala` | clínica chilena con el timezone default de Argentina |

## Garantías

- **Idempotente.** Solo hace PATCH de lo que cambió. Segunda corrida = "sin cambios".
- **Un fallo de lectura no baja nada a rojo.** Si el fetch falla o el JSON no cumple el
  contrato, no se escribe nada y se registra el error. Los checks quedan como estaban.
- **`📅 Entrega formal` es write-once.** Se setea el primer día que se cumplen las 4 etapas
  y no se reescribe ni se borra jamás. Si el cliente regresa, la fecha queda y se ve en la
  vista Regresión. Desde esa fecha corren los 60 días del tramo 3 — por eso ningún humano
  la escribe: sería dejar que el onbordero arranque su propio reloj de pago.
- **Denominadores congelados en D0+2.** Si en D0+2 falta algún denominador, **no** congela
  y lo dice en el log (esa fila cae en la vista "Sin denominador").
- **null nunca se convierte en 0.** Se escribe `None`, la fórmula lo ve y devuelve `🚫 N/A`,
  y el null queda registrado en `hallazgos-ultima-corrida.json`.

## Frecuencia (pendiente de cablear — ver PROGRESO)

| Cuándo | Cada |
|---|---|
| etapas 1-3 | 1h |
| entregados | 24h (detectar regresión) |
| botón "Sincronizar" | `sync.py <slug>` |

## Archivos

| | |
|---|---|
| `adapter.py` | `FixtureAdapter` / `HttpAdapter` + `get_adapter()` |
| `contract.py` | la forma del JSON de ACT-3 + `validate()` |
| `mapping.py` | contrato → campos crudos. Acá vive el mapa de timezone/moneda por país |
| `sync.py` | el job |
| `test/test_contract.py` | 25 tests |
| `../baserow/validate.py` | 32 aserciones del schema contra filas reales |
