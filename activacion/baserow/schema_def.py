# -*- coding: utf-8 -*-
"""Definición declarativa de la tabla `Activación` (Baserow tabla 957).

Principios de diseño (ver HALLAZGOS §G):
  1. Los 17 checks automáticos son FORMULAS derivadas de campos crudos que escribe
     el job. Baserow no tiene permisos por campo, así que la única forma real de
     cumplir la REGLA DURA ("ningún check editable a mano") es que sean derivados:
     una fórmula es read-only por construcción.
  2. TODA fórmula de check empieza con guardas is_null(). En este Baserow un número
     en blanco compara como 0 (verificado), así que sin guarda una clínica sin datos
     daría todos los checks en verde.
  3. Los booleanos que escribe el job son single_select tri-estado (blanco/✅ Sí/❌ No).
     El tipo boolean de Baserow NO es nullable: un dato desconocido se leería como
     false y bajaría el check a rojo. Eso viola "null → N/A, nunca rojo por timeout".
  4. is_blank NO existe en esta versión → is_null. and() acepta exactamente 2 args.
"""

TRI = [{"value": "✅ Sí", "color": "green"}, {"value": "❌ No", "color": "red"}]
EST = [{"value": "⏳ Pendiente", "color": "light-gray"},
       {"value": "🟡 En proceso", "color": "yellow"},
       {"value": "✅ Listo", "color": "green"},
       {"value": "🚫 N/A", "color": "gray"}]


def AND(*a):
    """Baserow and() toma exactamente 2 args -> anidar."""
    if len(a) == 1:
        return a[0]
    return "and(%s, %s)" % (a[0], AND(*a[1:]))


def OR(*a):
    if len(a) == 1:
        return a[0]
    return "or(%s, %s)" % (a[0], OR(*a[1:]))


def NN(*names):
    """not-null guard sobre varios campos"""
    return AND(*["not(is_null(field('%s')))" % n for n in names])


def check(guard_fields, cond, na_when=None):
    """Patrón estándar de check con guarda de nulos.
    Sin datos -> '🚫 N/A' (nunca verde, nunca rojo)."""
    body = "if(%s, '✅ Listo', '⏳ Pendiente')" % cond
    guarded = "if(%s, %s, '🚫 N/A')" % (NN(*guard_fields), body)
    if na_when:
        guarded = "if(%s, '🚫 N/A', %s)" % (na_when, guarded)
    return guarded


SI = lambda f: "totext(field('%s')) = '✅ Sí'" % f

# ─────────────────────────── GRUPO 1: campos base ───────────────────────────
BASE = [
    # identidad
    ("Slug Clinera", {"type": "text"}),
    ("Nombre cliente", {"type": "text"}),
    ("Email cuenta", {"type": "email"}),
    ("Teléfono", {"type": "phone_number"}),
    ("País", {"type": "single_select", "select_options": [
        {"value": v, "color": "blue"} for v in
        ["🇨🇱 CL", "🇲🇽 MX", "🇵🇪 PE", "🇨🇴 CO", "🇵🇦 PA", "🇨🇷 CR", "🇪🇨 EC", "🇺🇾 UY", "🇦🇷 AR", "🇺🇸 US"]]}),
    ("Stripe Subscription ID", {"type": "text"}),
    ("Encargado", {"type": "single_select", "select_options": [
        {"value": v, "color": "dark-blue"} for v in
        ["Brian", "Rebeca", "Catalina", "Nohelymar", "Jesús", "Micaela"]  # Franco despedido, Frine fuera (2026-07-17)]}),
    ("Fecha Ingreso (D0)", {"type": "date", "date_format": "ISO"}),

    # plan
    ("Plan", {"type": "single_select", "select_options": [
        {"value": "Vortex", "color": "light-blue"}, {"value": "Atlas", "color": "blue"},
        {"value": "Summit", "color": "dark-blue"}, {"value": "Corporativo", "color": "dark-gray"}]}),
    ("Precio plan USD", {"type": "number", "number_decimal_places": 0}),
    ("Implementación USD", {"type": "number", "number_decimal_places": 0}),
    ("Créditos/mes", {"type": "number", "number_decimal_places": 0}),

    # denominadores
    ("Sucursales declaradas", {"type": "number", "number_decimal_places": 0}),
    ("Profesionales declarados", {"type": "number", "number_decimal_places": 0}),
    ("Tratamientos declarados", {"type": "number", "number_decimal_places": 0}),
    ("Pacientes declarados", {"type": "number", "number_decimal_places": 0}),
    ("Denominadores congelados", {"type": "boolean"}),

    # ── crudos etapa 1 (job) ──
    ("Logo cargado", {"type": "single_select", "select_options": TRI}),
    ("Color personalizado", {"type": "single_select", "select_options": TRI}),
    ("Timezone consistente", {"type": "single_select", "select_options": TRI}),
    ("Moneda consistente", {"type": "single_select", "select_options": TRI}),
    ("Timezone leída", {"type": "text"}),
    ("WhatsApp status", {"type": "text"}),
    ("WhatsApp número", {"type": "text"}),
    ("Sucursales cargadas", {"type": "number", "number_decimal_places": 0}),
    ("Sucursales con horarios", {"type": "number", "number_decimal_places": 0}),
    ("Usuarios cargados", {"type": "number", "number_decimal_places": 0}),
    ("Usuarios con rol", {"type": "number", "number_decimal_places": 0}),

    # ── crudos etapa 2 ──
    ("Profesionales cargados", {"type": "number", "number_decimal_places": 0}),
    ("Profesionales activos", {"type": "number", "number_decimal_places": 0}),
    ("Tratamientos cargados", {"type": "number", "number_decimal_places": 0}),
    ("Tratamientos con precio", {"type": "number", "number_decimal_places": 0}),
    ("Tratamientos con duración", {"type": "number", "number_decimal_places": 0}),
    ("Pacientes cargados", {"type": "number", "number_decimal_places": 0}),
    ("Citas futuras", {"type": "number", "number_decimal_places": 0}),
    ("Ficha plantilla configurada", {"type": "single_select", "select_options": TRI}),
    ("Consentimiento cargado", {"type": "single_select", "select_options": TRI}),

    # ── crudos etapa 3 ──
    ("Agente texto activo", {"type": "single_select", "select_options": TRI}),
    ("Agente texto bloques", {"type": "number", "number_decimal_places": 0}),
    ("Agente texto modo", {"type": "text"}),
    ("Agente texto respaldo", {"type": "text"}),
    ("CAMILA disponible", {"type": "single_select", "select_options": TRI}),
    ("CAMILA activa", {"type": "single_select", "select_options": TRI}),
    ("Plantillas cargadas", {"type": "number", "number_decimal_places": 0}),
    ("Plantillas aprobadas Meta", {"type": "number", "number_decimal_places": 0}),
    ("Automatizaciones activas", {"type": "number", "number_decimal_places": 0}),
    ("Enviados 24h", {"type": "number", "number_decimal_places": 0}),
    ("Errores 24h", {"type": "number", "number_decimal_places": 0}),
    ("Difusiones audiencias", {"type": "number", "number_decimal_places": 0}),
    ("Difusiones enviadas", {"type": "number", "number_decimal_places": 0}),
    ("Difusiones 30d", {"type": "number", "number_decimal_places": 0}),
    ("Embed hits 30d", {"type": "number", "number_decimal_places": 0}),
    ("Cobros medio configurado", {"type": "single_select", "select_options": TRI}),

    # ── etapa 4: manual ──
    ("E1 · Capacitación", {"type": "single_select", "select_options": [
        {"value": "🕐 Pendiente", "color": "light-gray"}, {"value": "📅 Agendada", "color": "yellow"},
        {"value": "✅ Completada", "color": "green"}]}),
    ("E1 · Grabación", {"type": "file"}),
    ("E2 · Video ¡Eureka!", {"type": "file"}),
    ("E3 · Verificación Mitzi", {"type": "single_select", "select_options": [
        {"value": "⏳ Pendiente", "color": "light-gray"}, {"value": "✅ Conforme", "color": "green"},
        {"value": "⚠️ Con observaciones", "color": "orange"}]}),
    ("Nota Mitzi", {"type": "long_text"}),

    # ── AHA ──
    ("Citas por IA (total)", {"type": "number", "number_decimal_places": 0}),
    ("Citas IA últimas 4 sem", {"type": "number", "number_decimal_places": 0}),
    ("Fecha primera cita IA", {"type": "date", "date_format": "ISO"}),
    ("AHA verificado Mitzi", {"type": "single_select", "select_options": [
        {"value": "⏳ Pendiente", "color": "light-gray"}, {"value": "✅ Verificado", "color": "green"}]}),

    # ── entrega / ops ──
    ("📅 Entrega formal", {"type": "date", "date_format": "ISO"}),
    ("Uso IA 30d US$", {"type": "number", "number_decimal_places": 2}),
    ("Cliente activo", {"type": "single_select", "select_options": [
        {"value": "✅ Activo", "color": "green"}, {"value": "❌ Inactivo", "color": "red"},
        {"value": "⏸️ Pausado", "color": "yellow"}]}),
    ("Última sync", {"type": "date", "date_format": "ISO", "date_include_time": True}),
    ("📝 Actualizaciones", {"type": "long_text"}),
    ("Monday ID", {"type": "text"}),
    ("Tramo 1 · Venta US$30", {"type": "single_select", "select_options": [
        {"value": "⏳ Pendiente", "color": "light-gray"}, {"value": "📅 Programado", "color": "yellow"},
        {"value": "✅ Pagado", "color": "green"}]}),
    ("Tramo 2 · Config US$40", {"type": "single_select", "select_options": [
        {"value": "⏳ Pendiente", "color": "light-gray"}, {"value": "📅 Programado", "color": "yellow"},
        {"value": "✅ Pagado", "color": "green"}]}),
    ("Tramo 3 · Adopción US$50", {"type": "single_select", "select_options": [
        {"value": "⏳ Pendiente", "color": "light-gray"}, {"value": "📅 Programado", "color": "yellow"},
        {"value": "✅ Pagado", "color": "green"}]}),
]

# screenshots de los 17 checks automáticos
SHOTS = ["C1", "C2", "C3", "C4", "C5", "M1", "M2", "M3", "M4", "M5",
         "A1", "A2", "A3", "A4", "A5", "A6", "A7"]

# ─────────────────────────── GRUPO 2: los 20 checks ───────────────────────────
CHECKS = [
    ("C1 · Datos base", check(
        ["Slug Clinera", "Logo cargado", "Color personalizado", "Timezone consistente", "Moneda consistente"],
        AND(SI("Logo cargado"), SI("Color personalizado"), SI("Timezone consistente"), SI("Moneda consistente")))),

    ("C2 · WhatsApp", check(["WhatsApp status"], "totext(field('WhatsApp status')) = 'CONNECTED'")),

    ("C3 · Sucursales", check(["Sucursales cargadas", "Sucursales declaradas"],
                              "field('Sucursales cargadas') >= field('Sucursales declaradas')")),

    # ⚠️ exige count > 0: con 0 sucursales, "todas tienen horario" es verdad vacía
    # y pintaría el check de verde en una clínica sin datos.
    ("C4 · Horarios", check(["Sucursales con horarios", "Sucursales cargadas"],
                            AND("field('Sucursales cargadas') > 0",
                                "field('Sucursales con horarios') = field('Sucursales cargadas')"))),

    ("C5 · Usuarios y permisos", check(["Usuarios con rol"], "field('Usuarios con rol') >= 2")),

    ("M1 · Profesionales", check(["Profesionales activos", "Profesionales declarados"],
                                 "field('Profesionales activos') >= field('Profesionales declarados')")),

    ("M2 · Tratamientos", check(
        ["Tratamientos cargados", "Tratamientos declarados", "Tratamientos con precio", "Tratamientos con duración"],
        AND("field('Tratamientos cargados') >= field('Tratamientos declarados')",
            "field('Tratamientos con precio') = field('Tratamientos cargados')",
            "field('Tratamientos con duración') = field('Tratamientos cargados')"))),

    ("M3 · Pacientes", check(["Pacientes cargados", "Pacientes declarados"],
                             "field('Pacientes cargados') >= field('Pacientes declarados') * 0.95")),

    ("M4 · Citas futuras", check(["Citas futuras"], "field('Citas futuras') > 0")),

    ("M5 · Ficha y consentimientos", check(
        ["Ficha plantilla configurada", "Consentimiento cargado"],
        AND(SI("Ficha plantilla configurada"), SI("Consentimiento cargado")))),

    ("A1 · Agente texto", check(
        ["Agente texto activo", "Agente texto bloques", "Agente texto modo", "Agente texto respaldo"],
        AND(SI("Agente texto activo"), "field('Agente texto bloques') = 3",
            "totext(field('Agente texto modo')) != ''", "totext(field('Agente texto respaldo')) != ''"))),

    # A2: N/A si el plan no incluye CAMILA, o si CAMILA no está disponible todavía.
    # Un Vortex NUNCA puede quedar bloqueado por esto.
    ("A2 · Agente voz · CAMILA", check(
        ["CAMILA activa"], SI("CAMILA activa"),
        na_when=OR("not(%s)" % OR("totext(field('Plan')) = 'Atlas'", "totext(field('Plan')) = 'Summit'"),
                   "is_null(field('CAMILA disponible'))",
                   "totext(field('CAMILA disponible')) = '❌ No'"))),

    ("A3 · Plantillas", check(["Plantillas aprobadas Meta"], "field('Plantillas aprobadas Meta') >= 3")),

    # A4 · EL CRÍTICO: "activa" no es "funcionando". Tasa de error < 5%.
    ("A4 · Automatizaciones", check(
        ["Automatizaciones activas", "Enviados 24h", "Errores 24h"],
        AND("field('Automatizaciones activas') >= 2", "field('Enviados 24h') > 0",
            "field('Errores 24h') / field('Enviados 24h') < 0.05"))),

    ("A5 · Difusiones", check(["Difusiones audiencias", "Difusiones enviadas"],
                              AND("field('Difusiones audiencias') >= 1", "field('Difusiones enviadas') >= 1"))),

    ("A6 · Embed", check(["Embed hits 30d"], "field('Embed hits 30d') > 0")),

    ("A7 · Cobros y pagos", check(["Cobros medio configurado"], SI("Cobros medio configurado"))),

    # etapa 4 (manuales) — expuestos como check para el patrón ok_/ap_
    ("E1 · Check", "if(%s, '✅ Listo', '⏳ Pendiente')" % AND(
        "totext(field('E1 · Capacitación')) = '✅ Completada'", "count(field('E1 · Grabación')) > 0")),
    ("E2 · Check", "if(count(field('E2 · Video ¡Eureka!')) > 0, '✅ Listo', '⏳ Pendiente')"),
    ("E3 · Check", "if(totext(field('E3 · Verificación Mitzi')) = '✅ Conforme', '✅ Listo', '⏳ Pendiente')"),
]

CHECK_IDS = ["C1 · Datos base", "C2 · WhatsApp", "C3 · Sucursales", "C4 · Horarios", "C5 · Usuarios y permisos",
             "M1 · Profesionales", "M2 · Tratamientos", "M3 · Pacientes", "M4 · Citas futuras",
             "M5 · Ficha y consentimientos",
             "A1 · Agente texto", "A2 · Agente voz · CAMILA", "A3 · Plantillas", "A4 · Automatizaciones",
             "A5 · Difusiones", "A6 · Embed", "A7 · Cobros y pagos",
             "E1 · Check", "E2 · Check", "E3 · Check"]

S1 = CHECK_IDS[0:5]
S2 = CHECK_IDS[5:10]
S3 = CHECK_IDS[10:17]
S4 = CHECK_IDS[17:20]


def short(n):
    return n.split(" ·")[0]


# GRUPO 3 — ok_/ap_ por check.  N/A NO suma como verde y SALE del denominador
# (decisión §E3: es lo que hace stageStat() del prototipo).
OKAP = []
for n in CHECK_IDS:
    OKAP.append(("ok_%s" % short(n), "if(totext(field('%s')) = '✅ Listo', 1, 0)" % n))
    OKAP.append(("ap_%s" % short(n), "if(totext(field('%s')) = '🚫 N/A', 0, 1)" % n))


def stage_formula(names):
    ok = " + ".join("field('ok_%s')" % short(n) for n in names)
    ap = " + ".join("field('ap_%s')" % short(n) for n in names)
    return "if(%s = %s, '✅ Completada', '🟡 En proceso')" % (ok, ap)


ALL_OK = " + ".join("field('ok_%s')" % short(n) for n in CHECK_IDS)
ALL_AP = " + ".join("field('ap_%s')" % short(n) for n in CHECK_IDS)

# GRUPO 4 — etapas
STAGES = [
    ("Etapa 1 · Conexión", stage_formula(S1)),
    ("Etapa 2 · Migración", stage_formula(S2)),
    ("Etapa 3 · Activación", stage_formula(S3)),
    ("AHA detectado", "if(is_null(field('Citas por IA (total)')), '⏳ Sin datos', "
                      "if(field('Citas por IA (total)') > 0, '✅ Detectado', '⏳ Sin citas IA'))"),
]

# Etapa 4 exige: E1 completada CON archivo, E3 Mitzi Conforme, citas_ia>=1,
# y AHA verificado por Mitzi. La doble llave del AHA.
STAGES4 = [
    ("Etapa 4 · Entrega", "if(%s, '✅ Completada', '🟡 En proceso')" % AND(
        "field('ok_E1') = 1", "field('ok_E3') = 1",
        "totext(field('AHA detectado')) = '✅ Detectado'",
        "totext(field('AHA verificado Mitzi')) = '✅ Verificado'")),
]

# GRUPO 5 — derivados finales
FINAL = [
    ("Plan · detalle", "concat(totext(field('Plan')), ' · US$', totext(field('Precio plan USD')), '/mes"
                       " + US$', totext(field('Implementación USD')), ' implementación · ',"
                       " totext(field('Créditos/mes')), ' créditos/mes')"),
    ("Checks verdes", ALL_OK),
    ("Checks aplicables", ALL_AP),
    ("Progreso", "concat(totext(field('Checks verdes')), '/', totext(field('Checks aplicables')))"),
    ("Error automatizaciones %", "if(%s, field('Errores 24h') / field('Enviados 24h') * 100, 0)" %
     AND("not(is_null(field('Enviados 24h')))", "field('Enviados 24h') > 0")),
    ("Días desde D0", "if(is_null(field('Fecha Ingreso (D0)')), 0, "
                      "date_diff('day', field('Fecha Ingreso (D0)'), today()))"),

    # 🚦 Estado — SIN override manual. 100% derivado de las 4 etapas.
    ("🚦 Estado", "if(totext(field('Cliente activo')) = '❌ Inactivo', '⛔ CANCELADO', %s)" %
     ("if(%s, '✅ ENTREGADO', '🟡 EN PROCESO')" % AND(
         "totext(field('Etapa 1 · Conexión')) = '✅ Completada'",
         "totext(field('Etapa 2 · Migración')) = '✅ Completada'",
         "totext(field('Etapa 3 · Activación')) = '✅ Completada'",
         "totext(field('Etapa 4 · Entrega')) = '✅ Completada'"))),

    ("SLA", "if(not(is_null(field('📅 Entrega formal'))), '✅ Entregado', "
            "if(field('Días desde D0') > 10, '🔴 Vencido', "
            "if(field('Días desde D0') > 7, '🟡 En riesgo', '🟢 En plazo')))"),

    ("D+60 adopción", "if(is_null(field('📅 Entrega formal')), todate('', 'YYYY-MM-DD'), "
                      "field('📅 Entrega formal') + date_interval('60 days'))"),

    ("Gate tramo 2", "if(totext(field('Etapa 3 · Activación')) != '✅ Completada', '⏳ Etapa 3 abierta', "
                     "if(field('Días desde D0') <= 10, '✅ Pagar US$40', "
                     "if(field('Días desde D0') <= 20, '⚠️ Pagar US$20 (atraso)', '❌ Vencido — US$0')))"),

    ("Gate tramo 3", "if(is_null(field('📅 Entrega formal')), '⏳ Sin entrega formal', "
                     "if(today() < field('D+60 adopción'), "
                     "concat('⏳ Faltan ', totext(date_diff('day', today(), field('D+60 adopción'))), ' días'), "
                     "if(%s, '✅ Pagar US$50', '❌ No cumple adopción')))" % AND(
                         "totext(field('Cliente activo')) = '✅ Activo'",
                         "field('Citas IA últimas 4 sem') >= 4",
                         "field('Error automatizaciones %') < 5",
                         "field('Difusiones 30d') >= 1")),

    ("Comisión total US$", "if(totext(field('Tramo 1 · Venta US$30')) = '✅ Pagado', 30, 0) + "
                           "if(totext(field('Tramo 2 · Config US$40')) = '✅ Pagado', 40, 0) + "
                           "if(totext(field('Tramo 3 · Adopción US$50')) = '✅ Pagado', 50, 0)"),
]
