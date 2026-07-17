# -*- coding: utf-8 -*-
"""Traduce el JSON del contrato a los campos CRUDOS de la tabla 957.

⚠️ El job NO escribe checks. Los 17 checks automáticos son fórmulas derivadas en
Baserow (decisión de diseño, HALLAZGOS §G1: es la única forma de que no sean
editables a mano). Acá solo se escriben contadores y estados crudos.

REGLA 2 — null explícito:
  Si un dato no viene, se escribe None. Nunca 0, nunca False.
  La fórmula del check ve el null y devuelve '🚫 N/A'.
  Cada null se reporta en `hallazgos` para que quede registrado.
"""
from contract import get

# timezone que trae el selector por defecto. El caso a cazar: clínicas chilenas
# y mexicanas que quedaron con esto. La zona gobierna cuándo salen los
# recordatorios y las difusiones.
TZ_DEFAULT = "America/Argentina/Buenos_Aires"
TZ_PAIS = {
    "CL": ["America/Santiago"],
    "MX": ["America/Mexico_City", "America/Monterrey", "America/Tijuana", "America/Cancun"],
    "PE": ["America/Lima"],
    "CO": ["America/Bogota"],
    "PA": ["America/Panama"],
    "CR": ["America/Costa_Rica"],
    "EC": ["America/Guayaquil"],
    "UY": ["America/Montevideo"],
    "AR": ["America/Argentina/Buenos_Aires", "America/Buenos_Aires"],
    "US": ["America/New_York", "America/Chicago", "America/Denver", "America/Los_Angeles"],
}
MONEDA_PAIS = {"CL": "CLP", "MX": "MXN", "PE": "PEN", "CO": "COP", "PA": "USD",
               "CR": "CRC", "EC": "USD", "UY": "UYU", "AR": "ARS", "US": "USD"}
COLOR_DEFAULT = {"#000000", "#ffffff", "#fff", "#000", ""}


def tri(v):
    """bool → tri-estado. None se mantiene None (= desconocido → N/A)."""
    if v is None:
        return None
    return "✅ Sí" if v else "❌ No"


def _pais(doc):
    p = get(doc, "clinica.pais")
    return p.strip().upper()[:2] if isinstance(p, str) and p.strip() else None


def map_status(doc, hallazgos=None):
    """contrato → dict de campos crudos de Baserow. Devuelve (campos, hallazgos)."""
    h = hallazgos if hallazgos is not None else []
    slug = get(doc, "clinica.slug")

    def note(campo, motivo):
        h.append({"slug": slug, "campo": campo, "motivo": motivo})

    def num(path, campo=None):
        v = get(doc, path)
        if v is None:
            note(campo or path, "null en el contrato → check en 🚫 N/A")
        return v

    def trin(path, campo):
        """bool del contrato → tri-estado, registrando el null en hallazgos."""
        v = get(doc, path)
        if v is None:
            note(campo, "null en el contrato → check en 🚫 N/A")
        return tri(v)

    pais = _pais(doc)

    # ── C1 · datos base ──────────────────────────────────────────────
    logo = get(doc, "clinica.logo")
    color = get(doc, "clinica.color_primario")
    tz = get(doc, "clinica.timezone")
    cur = get(doc, "clinica.currency")

    tz_ok = None
    if tz is None or pais is None:
        note("Timezone consistente", "timezone o país null → 🚫 N/A")
    else:
        esperadas = TZ_PAIS.get(pais)
        if esperadas is None:
            note("Timezone consistente", "país '%s' fuera del mapa TZ_PAIS → 🚫 N/A" % pais)
        else:
            tz_ok = tz in esperadas
            if not tz_ok and tz == TZ_DEFAULT:
                note("Timezone consistente",
                     "timezone = default del selector (Argentina GMT-3) pero país = %s. "
                     "Los recordatorios y difusiones salen a la hora equivocada." % pais)

    mon_ok = None
    if cur is None or pais is None:
        note("Moneda consistente", "currency o país null → 🚫 N/A")
    else:
        esperada = MONEDA_PAIS.get(pais)
        mon_ok = (cur.upper() == esperada) if esperada else None
        if esperada is None:
            note("Moneda consistente", "país '%s' fuera del mapa MONEDA_PAIS → 🚫 N/A" % pais)

    campos = {
        "Slug Clinera": slug,
        "Logo cargado": tri(bool(logo)) if logo is not None else None,
        "Color personalizado": (tri(color.strip().lower() not in COLOR_DEFAULT)
                                if isinstance(color, str) else None),
        "Timezone consistente": tri(tz_ok),
        "Moneda consistente": tri(mon_ok),
        "Timezone leída": tz,

        # ── C2 ──
        "WhatsApp status": num("whatsapp.status", "WhatsApp status"),
        "WhatsApp número": get(doc, "whatsapp.numero"),

        # ── C3 · C4 · C5 ──
        "Sucursales cargadas": num("sucursales.count", "Sucursales cargadas"),
        "Sucursales con horarios": num("sucursales.con_horarios", "Sucursales con horarios"),
        "Usuarios cargados": num("usuarios.count", "Usuarios cargados"),
        "Usuarios con rol": num("usuarios.con_rol", "Usuarios con rol"),

        # ── M1..M5 ──
        "Profesionales cargados": num("profesionales.count", "Profesionales cargados"),
        "Profesionales activos": num("profesionales.activos", "Profesionales activos"),
        "Tratamientos cargados": num("tratamientos.count", "Tratamientos cargados"),
        "Tratamientos con precio": num("tratamientos.con_precio", "Tratamientos con precio"),
        "Tratamientos con duración": num("tratamientos.con_duracion", "Tratamientos con duración"),
        "Pacientes cargados": num("pacientes.count", "Pacientes cargados"),
        "Citas futuras": num("citas_futuras.count", "Citas futuras"),
        "Ficha plantilla configurada": trin("fichas.plantilla_configurada", "Ficha plantilla configurada"),
        "Consentimiento cargado": trin("fichas.consentimiento_cargado", "Consentimiento cargado"),

        # ── A1..A7 ──
        "Agente texto activo": trin("agente_texto.activo", "Agente texto activo"),
        "Agente texto bloques": num("agente_texto.bloques_completos", "Agente texto bloques"),
        "Agente texto modo": num("agente_texto.modo", "Agente texto modo"),
        "Agente texto respaldo": num("agente_texto.mensaje_respaldo", "Agente texto respaldo"),
        "CAMILA disponible": trin("agente_voz.disponible", "CAMILA disponible"),
        "CAMILA activa": trin("agente_voz.activo", "CAMILA activa"),
        "Plantillas cargadas": get(doc, "plantillas.count"),
        "Plantillas aprobadas Meta": num("plantillas.aprobadas_meta", "Plantillas aprobadas Meta"),
        "Automatizaciones activas": num("automatizaciones.activas", "Automatizaciones activas"),
        "Enviados 24h": num("automatizaciones.enviados_24h", "Enviados 24h"),
        "Errores 24h": num("automatizaciones.errores_24h", "Errores 24h"),
        "Difusiones audiencias": num("difusiones.audiencias", "Difusiones audiencias"),
        "Difusiones enviadas": num("difusiones.enviadas", "Difusiones enviadas"),
        "Embed hits 30d": num("embeds.hits_30d", "Embed hits 30d"),
        "Cobros medio configurado": trin("cobros.medio_configurado", "Cobros medio configurado"),

        # ── AHA ──
        "Citas por IA (total)": num("citas_ia.total", "Citas por IA (total)"),
        "Citas IA últimas 4 sem": num("citas_ia.ultimas_4_semanas", "Citas IA últimas 4 sem"),
        "Fecha primera cita IA": get(doc, "citas_ia.primera"),
    }
    return campos, h
