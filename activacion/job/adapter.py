# -*- coding: utf-8 -*-
"""Capa de adaptador para leer el estado de una clínica.

Dos implementaciones:
  · FixtureAdapter → lee JSONs de test/fixtures/   (DEFAULT hoy)
  · HttpAdapter    → GET {CLINERA_STATUS_URL}/{slug} con service token

Se elige por entorno: si CLINERA_STATUS_URL está seteada → HTTP; si no → fixtures.

⚠️ El endpoint NO existe todavía. Lo construye el equipo de Clinera (ACT-3).
El día que exista, esto es cambiar UNA variable de entorno. No se toca código.
"""
import json
import logging
import os
import urllib.error
import urllib.request

log = logging.getLogger("activacion.adapter")

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "test", "fixtures")


class StatusUnavailable(Exception):
    """No se pudo leer el estado. El caller NO debe degradar checks a rojo."""


class FixtureAdapter:
    mode = "FIXTURE"

    def __init__(self, path=FIXTURE_DIR):
        self.path = path

    def slugs(self):
        return sorted(f[:-5] for f in os.listdir(self.path) if f.endswith(".json"))

    def fetch(self, slug):
        p = os.path.join(self.path, slug + ".json")
        if not os.path.exists(p):
            raise StatusUnavailable("fixture no encontrada: %s" % p)
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)


class HttpAdapter:
    mode = "HTTP"

    def __init__(self, base=None, token=None, timeout=30):
        self.base = (base or os.environ["CLINERA_STATUS_URL"]).rstrip("/")
        self.token = token or os.environ.get("CLINERA_SERVICE_TOKEN", "")
        self.timeout = timeout

    def slugs(self):
        # El contrato no define un índice de slugs. La lista de clientes sale de
        # Baserow (columna `Slug Clinera`), no del endpoint.
        raise NotImplementedError("los slugs salen de Baserow, no del endpoint")

    def fetch(self, slug):
        req = urllib.request.Request(
            "%s/%s" % (self.base, slug),
            headers={"Authorization": "Bearer %s" % self.token,
                     "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise StatusUnavailable("HTTP %s para %s: %s" % (e.code, slug, e.read()[:200]))
        except Exception as e:                       # timeout, DNS, TLS, JSON roto
            raise StatusUnavailable("%s para %s: %s" % (type(e).__name__, slug, e))


def get_adapter():
    """Selecciona el adaptador por entorno y lo dice fuerte en el log."""
    url = os.environ.get("CLINERA_STATUS_URL")
    if url:
        log.warning("ADAPTER=HTTP · leyendo de %s (endpoint real)", url)
        return HttpAdapter(url)
    log.warning("ADAPTER=FIXTURE · leyendo de %s · "
                "el endpoint de Clinera (ACT-3) todavía no existe. "
                "Setea CLINERA_STATUS_URL para cambiar a HTTP.", FIXTURE_DIR)
    return FixtureAdapter()
