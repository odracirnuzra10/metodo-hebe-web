# -*- coding: utf-8 -*-
"""El contrato del endpoint `GET {CLINERA_STATUS_URL}/{slug}` (tarea ACT-3).

Esto es la fuente de verdad de la FORMA del JSON. Cuando el equipo entregue el
endpoint, `validate()` dice si cumple. No valida valores de negocio, solo forma.

REGLA: cualquier campo puede venir null. Un null NO es un error de contrato —
es un dato que no existe, y el mapeo lo traduce a '🚫 N/A'. Lo que sí es error
de contrato es que falte la CLAVE o que el tipo no calce.
"""

# tipo esperado por campo. None en la tupla = admite null.
NUM = (int, float)
SPEC = {
    "clinica": {"slug": (str,), "plan": (str,), "pais": (str,), "timezone": (str,),
                "currency": (str,), "logo": (str,), "color_primario": (str,),
                "created_at": (str,)},
    "whatsapp": {"status": (str,), "numero": (str,)},
    "sucursales": {"count": NUM, "con_horarios": NUM},
    "usuarios": {"count": NUM, "con_rol": NUM},
    "profesionales": {"count": NUM, "activos": NUM},
    "tratamientos": {"count": NUM, "con_precio": NUM, "con_duracion": NUM},
    "pacientes": {"count": NUM},
    "citas_futuras": {"count": NUM},
    "fichas": {"plantilla_configurada": (bool,), "consentimiento_cargado": (bool,)},
    "agente_texto": {"activo": (bool,), "bloques_completos": NUM, "modo": (str,),
                     "mensaje_respaldo": (str,), "promos_activas": (bool,)},
    "agente_voz": {"disponible": (bool,), "activo": (bool,)},
    "plantillas": {"count": NUM, "aprobadas_meta": NUM},
    "automatizaciones": {"activas": NUM, "enviados_24h": NUM, "errores_24h": NUM},
    "difusiones": {"audiencias": NUM, "enviadas": NUM, "ultima": (str,)},
    "embeds": {"default_generado": (bool,), "personalizados": NUM, "hits_30d": NUM},
    "cobros": {"medio_configurado": (bool,)},
    "citas_ia": {"total": NUM, "ultimos_30d": NUM, "primera": (str,),
                 "ultimas_4_semanas": NUM},
}


def validate(doc, strict_keys=True):
    """Devuelve lista de errores de contrato. Vacía = cumple."""
    errs = []
    if not isinstance(doc, dict):
        return ["la raíz no es un objeto JSON (es %s)" % type(doc).__name__]

    for grupo, campos in SPEC.items():
        if grupo not in doc:
            errs.append("falta el grupo '%s'" % grupo)
            continue
        g = doc[grupo]
        if g is None:
            continue                      # grupo entero null: legítimo -> todo N/A
        if not isinstance(g, dict):
            errs.append("'%s' debería ser objeto, es %s" % (grupo, type(g).__name__))
            continue
        for campo, tipos in campos.items():
            if campo not in g:
                if strict_keys:
                    errs.append("falta '%s.%s'" % (grupo, campo))
                continue
            v = g[campo]
            if v is None:
                continue                  # null siempre permitido
            # bool es subclase de int en Python: no dejar que un bool pase por número
            if tipos is NUM and isinstance(v, bool):
                errs.append("'%s.%s' es bool, se esperaba número" % (grupo, campo))
                continue
            if not isinstance(v, tipos):
                errs.append("'%s.%s' es %s, se esperaba %s"
                            % (grupo, campo, type(v).__name__,
                               "/".join(t.__name__ for t in tipos)))

    extra = set(doc) - set(SPEC)
    if extra:
        errs.append("grupos no contemplados en el contrato: %s (no rompe, pero revisar)"
                    % ", ".join(sorted(extra)))
    return errs


def get(doc, path, default=None):
    """Lee 'grupo.campo' tolerando grupo null / clave ausente. Devuelve None si no hay dato."""
    cur = doc
    for part in path.split("."):
        if not isinstance(cur, dict) or cur.get(part) is None:
            return default
        cur = cur[part]
    return cur
