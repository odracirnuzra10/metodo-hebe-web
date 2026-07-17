# Panel /activacion — tech.oacg.cl

**Desplegado y vivo.** `https://tech.oacg.cl/activacion`

El panel es un HTML único en la VM (`/opt/work/site/index.html`), servido por nginx
(`try_files $uri /index.html`, así que la ruta resuelve sola) detrás de oauth2-proxy.
**No hay repo git.** Se edita bajando/subiendo por scp.

## Los archivos de acá

| | |
|---|---|
| `act_module.js` | el módulo entero (GACT) — makeGrid + override de render, igual que GONB |
| `act.css` | estilos, con los tokens del panel (no los del prototipo) |
| `patch.py` | **inyecta los dos en `index.html.ORIG` → `index.html`. Idempotente.** |

## Cómo hacer un cambio

```bash
KEY=~/.ssh/google_compute_engine; VM=ricardooyarzun_macair@34.176.251.239

# 1. BAJAR SIEMPRE el vivo primero — la copia local se desactualiza
ssh -i $KEY $VM 'sudo -n cp /opt/work/site/index.html /tmp/i.html && sudo -n chmod 644 /tmp/i.html'
scp -i $KEY $VM:/tmp/i.html index.html.ORIG

# 2. editar act_module.js / act.css, y re-inyectar
python3 patch.py

# 3. validar el JS ANTES de subir (un error rompe el panel entero, no solo /activacion)
node -e "const fs=require('fs'),vm=require('vm');const h=fs.readFileSync('index.html','utf8');
const re=/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g;let m,i=0,bad=0;
while((m=re.exec(h))){i++;try{new vm.Script(m[1]);}catch(e){bad++;console.log(e.message);}}
console.log(i+' scripts, '+bad+' errores');process.exit(bad?1:0)"

# 4. subir con backup
TS=$(date +%Y%m%d-%H%M%S)
scp -i $KEY index.html $VM:/tmp/new.html
ssh -i $KEY $VM "sudo -n cp /opt/work/site/index.html /opt/work/site/index.html.bak-$TS && sudo -n cp /tmp/new.html /opt/work/site/index.html && sudo -n chmod 644 /opt/work/site/index.html"
```

`app.py` solo cambia si hay que tocar `TABLAS_PERMITIDAS`. Si lo cambias:
`sudo docker restart work-workapi-1` (**workapi**, no `work-work-1`, que es nginx).

## Los 7 puntos de registro de una ruta (los toca `patch.py`)

1. `SLUGS` → `act:['activacion','activación']`
2. `modFromPath()` → lista de mods (hash)
3. `go()` → lista de mods (toggle hidden)
4. `<div id="mod-act">`
5. `BOARDS` + `BOARD_ICONS.act`
6. `BOARD_TIDS` → `act:957`
7. `go()` → `if(mod==='act'&&!GACT.loaded)GACT.init();`

\+ `TABLAS_PERMITIDAS` en `app.py` (957).

## Qué es editable y qué no

**De 166 campos, solo 25 son editables desde el panel.** El resto está bloqueado:

- **Los 20 checks, las 4 etapas, 🚦 Estado, Progreso, SLA, ok_/ap_**: son campos
  FÓRMULA en Baserow → `makeGrid` los marca `ro` solo. Read-only por construcción.
- **Los campos crudos del job** (`Errores 24h`, `Pacientes cargados`, …), **`📅 Entrega
  formal`**, **`Última sync`**, **los 📸** y **el precio de Stripe**: los bloquea
  `ACT_JOB_FIELDS` + el override de `refreshSchema` en `act_module.js`.
  Sin eso, editar `Errores 24h` a 0 pondría A4 en verde, y escribir `📅 Entrega formal`
  a mano arrancaría el reloj de comisión del tramo 3.

**Editable a propósito:** identidad/comercial, los 4 denominadores, la etapa 4
(E1/E2/E3 + Nota Mitzi + AHA verificado Mitzi), `Cliente activo`, tramos de comisión.

⚠️ El candado de los crudos es del **panel**. Baserow directo sigue permitiendo
editarlos (no tiene permisos por campo). Ver HALLAZGOS §H2.

## Verificado en vivo

- Las 4 vistas cazan la fila correcta (probado con filas que las disparan, no a ojo):
  Vencidos · Sin denominador · Esperando Mitzi · Regresión
- Banner "⏳ N de M sin sincronizar — esperando el endpoint de Clinera (ACT-3)"
- Contadores con denominador: `3390/3400 pacientes` en verde, `1200/3400` en rojo
- Progreso respeta los N/A: un Vortex marca **16/19**, no 16/20
- `/schema/957` por workapi devuelve 166 campos (77 fórmulas)

---

## Actualización 2026-07-17 (segunda tanda de Ricardo)

- **Etapas clickeables**: la flecha de cada etapa abre el drawer con sus checks
  (`GACT.openStage`), inputs de cantidad + botón foto/video (`<check> 📸`).
- **Drawer redimensionable system-wide**: `#drawer` con handle (`#drawerGrip`), ancho en
  `localStorage work.drawer.w`. Aplica a todo el panel, no solo activación.
- **KPIs**: Total / En proceso / Completado + 4 chips-filtro.
- **Encargados**: solo Brian, Rebeca, Catalina, Nohelymar, Jesús, Micaela.
- **Columna Mitzi**: aprobar/observar → modal de nota → fija `📅 Entrega formal`, contador
  `D+N` y comisión a 60 días. Guard: no aprueba sin etapas 1-3 + E1 con grabación + AHA.
- **Correo al aprobar** ✅ funcionando: `POST /work-api/notify-complete` → n8n webhook
  `https://n8n.oacg.cl/webhook/activacion-completada-9f2` (workflow `oobPgz0DaQz4jOMy`) → Gmail
  a ricardo@oacg.cl. Env `NOTIFY_WEBHOOK_URL` ya seteada en el docker-compose de la VM.

`app.py.deployed` es copia de referencia del app.py con el endpoint `/notify-complete`.
