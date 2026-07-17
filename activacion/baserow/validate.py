# -*- coding: utf-8 -*-
"""Valida la tabla `Activación` creando filas reales y comprobando los derivados.
Crea, asevera y borra. No deja basura."""
import br, json, datetime

tid = int(open('tid.txt').read())
HOY = datetime.date.today()
D0 = (HOY - datetime.timedelta(days=8)).isoformat()


def full(**over):
    """clínica completa (Atlas): todo verde"""
    d = {
        "Name": "TEST completa", "Slug Clinera": "completa", "Plan": "Atlas",
        "Precio plan USD": 379, "Implementación USD": 450, "Créditos/mes": 37000,
        "Fecha Ingreso (D0)": D0, "Cliente activo": "✅ Activo",
        "Sucursales declaradas": 2, "Profesionales declarados": 6,
        "Tratamientos declarados": 24, "Pacientes declarados": 3400,
        "Logo cargado": "✅ Sí", "Color personalizado": "✅ Sí",
        "Timezone consistente": "✅ Sí", "Moneda consistente": "✅ Sí",
        "WhatsApp status": "CONNECTED",
        "Sucursales cargadas": 2, "Sucursales con horarios": 2,
        "Usuarios cargados": 4, "Usuarios con rol": 4,
        "Profesionales cargados": 6, "Profesionales activos": 6,
        "Tratamientos cargados": 24, "Tratamientos con precio": 24, "Tratamientos con duración": 24,
        "Pacientes cargados": 3390, "Citas futuras": 120,
        "Ficha plantilla configurada": "✅ Sí", "Consentimiento cargado": "✅ Sí",
        "Agente texto activo": "✅ Sí", "Agente texto bloques": 3,
        "Agente texto modo": "asistido", "Agente texto respaldo": "Te respondemos pronto",
        "CAMILA disponible": "✅ Sí", "CAMILA activa": "✅ Sí",
        "Plantillas aprobadas Meta": 4,
        "Automatizaciones activas": 3, "Enviados 24h": 512, "Errores 24h": 2,
        "Difusiones audiencias": 2, "Difusiones enviadas": 3, "Difusiones 30d": 3,
        "Embed hits 30d": 340, "Cobros medio configurado": "✅ Sí",
        "E1 · Capacitación": "✅ Completada",
        "E3 · Verificación Mitzi": "✅ Conforme",
        "Citas por IA (total)": 7, "Citas IA últimas 4 sem": 6,
        "AHA verificado Mitzi": "✅ Verificado",
    }
    d.update(over)
    return d


CASES = {
    # nombre: (payload, asserts)
    # REGRESIÓN (bug encontrado 2026-07-17): una etapa con TODOS los checks en N/A
    # daba '✅ Completada' porque sum(ok)=0 = sum(ap)=0. Una clínica sin datos se
    # pintaba entera de verde. La fórmula ahora exige sum(ap) > 0.
    "vacia": ({"Name": "TEST vacia", "Slug Clinera": "vacia"}, {
        "Etapa 1 · Conexión": "🟡 En proceso", "Etapa 2 · Migración": "🟡 En proceso",
        "Etapa 3 · Activación": "🟡 En proceso", "🚦 Estado": "🟡 EN PROCESO",
        "C1 · Datos base": "🚫 N/A", "C3 · Sucursales": "🚫 N/A",
    }),

    # REGRESIÓN (bug encontrado 2026-07-17): con 0 sucursales, "todas tienen horario"
    # es verdad vacía y C4 daba '✅ Listo' en una clínica sin nada cargado.
    "cero_sucursales": ({"Name": "TEST cero sucursales", "Slug Clinera": "cerosuc",
                         "Sucursales declaradas": 2, "Sucursales cargadas": 0,
                         "Sucursales con horarios": 0}, {
        "C3 · Sucursales": "⏳ Pendiente",
        "C4 · Horarios": "⏳ Pendiente",     # NO '✅ Listo' por verdad vacía
    }),

    # Un número en blanco compara como 0 en este Baserow: sin guarda is_null,
    # 'cargadas >= declaradas' daría 0>=0 -> verde. La guarda lo manda a N/A.
    "sin_denominador": ({"Name": "TEST sin denom", "Slug Clinera": "sindenom",
                         "Sucursales cargadas": 5}, {
        "C3 · Sucursales": "🚫 N/A",         # declaradas es null -> N/A, NUNCA verde
    }),
    "completa_sin_E1archivo": (full(), {
        "Etapa 1 · Conexión": "✅ Completada", "Etapa 2 · Migración": "✅ Completada",
        "Etapa 3 · Activación": "✅ Completada",
        # E1 marcada Completada pero SIN grabación -> ok_E1=0 -> etapa 4 bloqueada
        "ok_E1": "0", "Etapa 4 · Entrega": "🟡 En proceso", "🚦 Estado": "🟡 EN PROCESO",
        "A2 · Agente voz · CAMILA": "✅ Listo",
    }),
    "automatizaciones_11pct": (full(Name="TEST auto11", **{"Enviados 24h": 512, "Errores 24h": 58}), {
        "A4 · Automatizaciones": "⏳ Pendiente",   # 11.3% > 5% -> NO verde
        "Etapa 3 · Activación": "🟡 En proceso",
        "🚦 Estado": "🟡 EN PROCESO",
    }),
    "vortex_camila_na": (full(Name="TEST vortex", Plan="Vortex", **{
        "Precio plan USD": 279, "Créditos/mes": 28000,
        "CAMILA disponible": "❌ No", "CAMILA activa": None}), {
        "A2 · Agente voz · CAMILA": "🚫 N/A",       # Vortex NUNCA bloqueado por CAMILA
        "ap_A2": "0",                                # y sale del denominador
        "Etapa 3 · Activación": "✅ Completada",
    }),
    "medias": (full(Name="TEST medias", **{
        "Pacientes cargados": 1200,                 # 1200 < 3400*0.95 -> rojo
        "Tratamientos con precio": 20,              # 20 != 24 -> rojo
        "Plantillas aprobadas Meta": 2,             # < 3 -> rojo
        "Embed hits 30d": None,                     # null -> N/A
        "Cobros medio configurado": None}), {
        "M2 · Tratamientos": "⏳ Pendiente",
        "M3 · Pacientes": "⏳ Pendiente",
        "A3 · Plantillas": "⏳ Pendiente",
        "A6 · Embed": "🚫 N/A",
        "A7 · Cobros y pagos": "🚫 N/A",
        "Etapa 2 · Migración": "🟡 En proceso",
    }),
    "aha_sin_verificar": (full(Name="TEST aha", **{"AHA verificado Mitzi": "⏳ Pendiente"}), {
        "AHA detectado": "✅ Detectado",
        "Etapa 4 · Entrega": "🟡 En proceso",   # Mitzi no verificó -> no entrega
    }),
    "sin_citas_ia": (full(Name="TEST sincitas", **{
        "Citas por IA (total)": 0, "AHA verificado Mitzi": "✅ Verificado"}), {
        "AHA detectado": "⏳ Sin citas IA",
        # Mitzi NO puede verificar un AHA que el sistema no detectó
        "Etapa 4 · Entrega": "🟡 En proceso",
    }),
}


def sv(row, k):
    v = row.get(k)
    return v.get('value') if isinstance(v, dict) else v


created, fails, passes = [], [], 0
for name, (payload, asserts) in CASES.items():
    payload = {k: v for k, v in payload.items() if v is not None}
    r = br.call("POST", "/api/database/rows/table/%s/?user_field_names=true" % tid, payload)
    created.append(r['id'])
    print("\n### %s (row %s)" % (name, r['id']))
    for k, exp in asserts.items():
        got = sv(r, k)
        if str(got) == str(exp):
            passes += 1
            print("   ok   %-28s = %r" % (k, got))
        else:
            fails.append((name, k, exp, got))
            print("   FAIL %-28s esperado %r, obtuve %r" % (k, exp, got))

# caso especial: completa CON archivo E1 -> debe ser ENTREGADO. Se prueba en el job (necesita upload real).
print("\n=== limpieza ===")
for rid in created:
    br.delete_row(tid, rid)
print("borradas", len(created), "filas de prueba")

print("\n=== RESULTADO: %d ok, %d fallos ===" % (passes, len(fails)))
for f in fails:
    print("  !!", f)
