# -*- coding: utf-8 -*-
"""Contract tests.

El día que el equipo entregue el endpoint ACT-3, esto dice si cumple el contrato:

    CLINERA_STATUS_URL=https://... python3 test/test_contract.py --live <slug>

Sin --live corre contra las fixtures.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import contract                     # noqa: E402
from mapping import map_status      # noqa: E402

FX = os.path.join(os.path.dirname(__file__), "fixtures")
fails, passes = [], 0


def ok(cond, msg):
    global passes
    if cond:
        passes += 1
    else:
        fails.append(msg)
        print("  FAIL", msg)


def test_fixtures_cumplen_contrato():
    for f in sorted(os.listdir(FX)):
        if not f.endswith(".json"):
            continue
        doc = json.load(open(os.path.join(FX, f), encoding="utf-8"))
        errs = contract.validate(doc)
        ok(not errs, "fixture %s no cumple el contrato: %s" % (f, errs))


def test_contrato_detecta_problemas():
    base = json.load(open(os.path.join(FX, "completa.json"), encoding="utf-8"))

    d = json.loads(json.dumps(base)); del d["whatsapp"]
    ok(any("whatsapp" in e for e in contract.validate(d)), "debería detectar grupo faltante")

    d = json.loads(json.dumps(base)); d["sucursales"]["count"] = "dos"
    ok(any("sucursales.count" in e for e in contract.validate(d)), "debería detectar tipo malo")

    d = json.loads(json.dumps(base)); d["sucursales"]["count"] = True
    ok(any("bool" in e for e in contract.validate(d)),
       "debería rechazar bool donde va número (bool es subclase de int en Python)")

    d = json.loads(json.dumps(base)); del d["pacientes"]["count"]
    ok(any("pacientes.count" in e for e in contract.validate(d)), "debería detectar clave faltante")

    # null SIEMPRE es válido: es un dato que no existe, no un error de contrato
    d = json.loads(json.dumps(base)); d["embeds"]["hits_30d"] = None
    ok(not contract.validate(d), "null debe ser válido en el contrato")

    d = json.loads(json.dumps(base)); d["cobros"] = None
    ok(not contract.validate(d), "un grupo entero null debe ser válido")


def test_mapeo_nulls_a_none_nunca_a_cero():
    doc = json.load(open(os.path.join(FX, "amedias.json"), encoding="utf-8"))
    campos, h = map_status(doc)
    ok(campos["Embed hits 30d"] is None, "hits_30d null → None, NUNCA 0")
    ok(campos["Cobros medio configurado"] is None, "cobros null → None, NUNCA '❌ No'")
    ok(any(x["campo"] == "Embed hits 30d" for x in h), "el null debe quedar en hallazgos")
    ok(any(x["campo"] == "Cobros medio configurado" for x in h),
       "el null de cobros debe quedar en hallazgos")


def test_grupo_null_no_revienta_el_mapeo():
    doc = json.load(open(os.path.join(FX, "completa.json"), encoding="utf-8"))
    doc["automatizaciones"] = None
    campos, h = map_status(doc)
    ok(campos["Enviados 24h"] is None, "grupo null → campos None sin excepción")
    ok(campos["Errores 24h"] is None, "grupo null → campos None sin excepción")


def test_timezone_default_argentina_se_caza():
    doc = json.load(open(os.path.join(FX, "tzmala.json"), encoding="utf-8"))
    campos, h = map_status(doc)
    ok(campos["Timezone consistente"] == "❌ No",
       "clínica CL con timezone Buenos Aires debe dar ❌ No, dio %r" % campos["Timezone consistente"])
    ok(any("default del selector" in x["motivo"] for x in h),
       "debe registrar el caso del default de Argentina en hallazgos")

    doc2 = json.load(open(os.path.join(FX, "completa.json"), encoding="utf-8"))
    campos2, _ = map_status(doc2)
    ok(campos2["Timezone consistente"] == "✅ Sí", "CL con America/Santiago debe dar ✅ Sí")


def test_vortex_camila():
    doc = json.load(open(os.path.join(FX, "vortex.json"), encoding="utf-8"))
    campos, _ = map_status(doc)
    ok(campos["CAMILA disponible"] == "❌ No", "vortex: agente_voz.disponible False → ❌ No")
    # el gate por plan lo hace la fórmula de Baserow, no el mapeo


def test_autofalla_escribe_los_crudos():
    doc = json.load(open(os.path.join(FX, "autofalla.json"), encoding="utf-8"))
    campos, _ = map_status(doc)
    ok(campos["Enviados 24h"] == 512 and campos["Errores 24h"] == 58,
       "el job escribe crudos; el 11% lo calcula la fórmula")


def test_vacia_es_cero_no_null():
    """Distinción crítica: 0 real (dato leído) != null (dato ausente)."""
    doc = json.load(open(os.path.join(FX, "vacia.json"), encoding="utf-8"))
    campos, _ = map_status(doc)
    ok(campos["Sucursales cargadas"] == 0, "0 real debe escribirse como 0, no como None")
    ok(campos["Agente texto activo"] == "❌ No", "False real → ❌ No, no None")


if __name__ == "__main__":
    for fn in sorted(k for k in dict(globals()) if k.startswith("test_")):
        print("\n###", fn)
        globals()[fn]()
    print("\n=== %d ok, %d fallos ===" % (passes, len(fails)))
    for f in fails:
        print("  !!", f)
    sys.exit(1 if fails else 0)
