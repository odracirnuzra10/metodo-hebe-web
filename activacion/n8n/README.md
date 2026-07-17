# n8n · Aviso de onboarding completado

Al aprobar Mitzi, el panel llama a `POST /work-api/notify-complete` y `app.py` reenvía a
este webhook, que manda el correo a ricardo@oacg.cl.

| | |
|---|---|
| Instancia | https://n8n.oacg.cl |
| Workflow | `OACG TECH → Activación | Aviso onboarding completado (webhook)` · id `oobPgz0DaQz4jOMy` · **activo** |
| Webhook (prod) | `https://n8n.oacg.cl/webhook/activacion-completada-9f2` |
| Credencial Gmail | `gmailOAuth2` id `Pf3R4wpW3w8FFqYr` (reusada, no creé nueva) |
| Env en la VM | `NOTIFY_WEBHOOK_URL` en `/opt/work/docker-compose.yml` (bloque workapi) |

`aviso-onboarding-completado.json` es el export del workflow (sin secretos) por si hay que
recrearlo. Body que recibe: `{slug, name/cliente, fecha, encargado, nota, subject?}`.

Probado end-to-end 2026-07-17: `/notify-complete` → `{"ok":true}`, ejecución n8n `success`.
