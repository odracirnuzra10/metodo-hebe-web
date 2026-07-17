# -*- coding: utf-8 -*-
"""Job de sync: contrato → tabla `Activación` (Baserow 957).

  python3 sync.py            # todas las filas con Slug Clinera
  python3 sync.py <slug>     # una sola (lo que llama POST /sync/{slug} del panel)
  python3 sync.py --dry      # no escribe, solo reporta el diff

Garantías:
  · Idempotente. Solo hace PATCH de los campos que realmente cambian.
  · Si la lectura falla, NO toca los checks. Los deja como estaban y registra el error.
    Un timeout jamás baja un check a rojo.
  · `📅 Entrega formal` es write-once. Una vez seteada, nunca se reescribe ni se borra.
  · Los denominadores se congelan en D0+2.
  · Log de qué cambió por cliente y por corrida.
"""
import argparse
import datetime
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "baserow"))

import br                                    # noqa: E402
import contract                              # noqa: E402
from adapter import StatusUnavailable, get_adapter   # noqa: E402
from mapping import map_status               # noqa: E402

TABLA = 957
log = logging.getLogger("activacion.sync")

DENOMINADORES = ["Sucursales declaradas", "Profesionales declarados",
                 "Tratamientos declarados", "Pacientes declarados"]
ETAPAS = ["Etapa 1 · Conexión", "Etapa 2 · Migración",
          "Etapa 3 · Activación", "Etapa 4 · Entrega"]


def sv(row, k):
    v = row.get(k)
    return v.get("value") if isinstance(v, dict) else v


def rows_by_slug():
    out = {}
    r = br.call("GET", "/api/database/rows/table/%s/?user_field_names=true&size=200" % TABLA)
    for row in r["results"]:
        s = sv(row, "Slug Clinera")
        if s:
            out[s] = row
    return out


def _norm(v):
    """Normaliza para comparar lo que está en Baserow con lo que queremos escribir."""
    if isinstance(v, dict):
        v = v.get("value")
    if isinstance(v, str) and v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return v
    return v


def diff_campos(row, nuevos):
    """Solo lo que cambia de verdad. Idempotencia."""
    d = {}
    for k, v in nuevos.items():
        if _norm(row.get(k)) != _norm(v):
            d[k] = v
    return d


def congelar_denominadores(row, hoy):
    """En D0+2 se congelan. Después son read-only para el equipo (lo enforcea el panel)."""
    if sv(row, "Denominadores congelados"):
        return {}
    d0 = sv(row, "Fecha Ingreso (D0)")
    if not d0:
        return {}
    dias = (hoy - datetime.date.fromisoformat(d0)).days
    if dias < 2:
        return {}
    faltan = [c for c in DENOMINADORES if sv(row, c) in (None, "")]
    if faltan:
        log.warning("  ⚠️  D+%s y sin denominador: %s — NO congelo, quedaría en 'sin denominador'",
                    dias, ", ".join(faltan))
        return {}
    return {"Denominadores congelados": True}


def entrega_formal(row_post, hoy):
    """Setea 📅 Entrega formal el PRIMER día que se cumplen las 4 etapas.
    Write-once: si ya tiene fecha, no se toca jamás. Si el cliente regresa, la
    fecha NO se borra — eso se ve en la vista Regresión.
    Desde esta fecha corren los 60 días del tramo 3. Por eso ningún humano la escribe.
    """
    if sv(row_post, "📅 Entrega formal"):
        return {}
    if all(sv(row_post, e) == "✅ Completada" for e in ETAPAS):
        return {"📅 Entrega formal": hoy.isoformat()}
    return {}


def sync_slug(slug, row, adapter, hoy, dry=False):
    """Devuelve (estado, detalle). Nunca lanza."""
    res = {"slug": slug, "cambios": {}, "hallazgos": [], "error": None}
    try:
        doc = adapter.fetch(slug)
    except StatusUnavailable as e:
        # NO degradar. Los checks quedan como estaban.
        res["error"] = str(e)
        log.error("  ❌ %s — lectura falló: %s · checks intactos, no se toca nada", slug, e)
        return "error", res

    errs = contract.validate(doc)
    if errs:
        res["error"] = "contrato: " + "; ".join(errs[:5])
        log.error("  ❌ %s — el JSON no cumple el contrato: %s · no escribo", slug, errs[:5])
        return "contrato", res

    campos, hallazgos = map_status(doc)
    res["hallazgos"] = hallazgos
    campos["Última sync"] = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    d = diff_campos(row, campos)
    d.update(congelar_denominadores(row, hoy))
    res["cambios"] = {k: v for k, v in d.items() if k != "Última sync"}
    # `Última sync` cambia siempre; no cuenta como cambio de negocio.
    solo_timestamp = not res["cambios"]
    if dry:
        if solo_timestamp:
            log.info("  = %s — DRY, sin cambios", slug)
            return "sin-cambios", res
        log.info("  ~ %s — DRY, %d campos cambiarían: %s", slug, len(res["cambios"]),
                 ", ".join(sorted(res["cambios"])[:8]))
        return "dry", res

    post = br.call("PATCH", "/api/database/rows/table/%s/%s/?user_field_names=true"
                   % (TABLA, row["id"]), d)

    # segunda pasada: las etapas son fórmulas, se recalculan al escribir los crudos
    ef = entrega_formal(post, hoy)
    if ef:
        br.call("PATCH", "/api/database/rows/table/%s/%s/?user_field_names=true"
                % (TABLA, row["id"]), ef)
        res["cambios"].update(ef)
        log.warning("  🎉 %s — ENTREGA FORMAL seteada en %s (arranca el reloj D+60)",
                    slug, ef["📅 Entrega formal"])

    if solo_timestamp:
        log.info("  = %s — sin cambios", slug)
        return "sin-cambios", res
    log.info("  ✓ %s — %d campos: %s", slug, len(res["cambios"]),
             ", ".join(sorted(res["cambios"])[:8]))
    return "ok", res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO if not a.verbose else logging.DEBUG,
                        format="%(message)s")

    adapter = get_adapter()
    hoy = datetime.date.today()
    todas = rows_by_slug()
    objetivo = {a.slug: todas[a.slug]} if a.slug else todas
    if a.slug and a.slug not in todas:
        log.error("slug '%s' no existe en la tabla %s (o su fila no tiene Slug Clinera)",
                  a.slug, TABLA)
        return 2

    log.info("── sync %s · %d clínica(s) · modo %s%s",
             hoy, len(objetivo), adapter.mode, " · DRY" if a.dry else "")
    if not objetivo:
        log.warning("No hay filas con `Slug Clinera` en la tabla %s. "
                    "El alta de clientes entra por Stripe vía n8n, no por este job.", TABLA)

    resumen, hallazgos = {}, []
    for slug, row in sorted(objetivo.items()):
        estado, res = sync_slug(slug, row, adapter, hoy, a.dry)
        resumen[estado] = resumen.get(estado, 0) + 1
        hallazgos.extend(res["hallazgos"])

    log.info("── resumen: %s", resumen)
    if hallazgos:
        log.warning("── %d dato(s) null → check en 🚫 N/A:", len(hallazgos))
        for h in hallazgos[:20]:
            log.warning("   · %s · %s — %s", h["slug"], h["campo"], h["motivo"])
        with open(os.path.join(os.path.dirname(__file__), "hallazgos-ultima-corrida.json"),
                  "w", encoding="utf-8") as f:
            json.dump(hallazgos, f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
