# Pendientes — puente Hebe → Clinera

**Verificado en vivo 2026-09-13 (HTTP).** 200: `/`, `/evaluacion`, `/fundador`, `/franquicia`, `/equipo`, `/criolipolisis`, `/guatita-de-delantal-auge-y-ley`, `/clinica/como-confirmamos-tu-hora-por-whatsapp`, `/clinica/por-que-respondemos-en-minutos`, `/clinica/que-pasa-con-tu-ficha-entre-sesiones`, `/clinica-estetica-corporal-concepcion`, `https://www.clinera.io/casos/metodo-hebe`, ambas claves IndexNow. 301: `clinicahebe.cl` → `https://www.metodohebe.cl/`. 308: `/planes/` → `/planes`; `/fundador/` → `/fundador`. Los tres `share.google` de sede: 302.

El lado Clinera **ya está publicado** (2026-09-04):
https://www.clinera.io/casos/metodo-hebe

`/clinica/por-que-respondemos-en-minutos` apunta a esa URL.

Lo que sigue no se cierra desde este repo.

---

## 1) GBP — hecho (2026-09-04)

Ricardo entregó los share oficiales de cada ficha. Van en `sameAs` + `hasMap`
de cada `MedicalClinic` (reemplazan `maps/search/?query=dirección`).

| Sede | URL |
|---|---|
| Los Ángeles | https://share.google/TXyvAWXsTRvMAu9gD |
| Concón | https://share.google/G1xHnaCeC1qxxoc6F |
| Vitacura | https://share.google/MsZnMY3vYGe6bW1Mo |

No hay `?cid=` numérico extraíble (Maps es un shell JS). No inventar CIDs.
Los share resuelven al Knowledge Graph (`kgmid` `/g/11…`).

---

## 2) Post-deploy (Search Console / Rich Results)

Tras merge + deploy de metodohebe.cl, validar en Google Rich Results Test:

- https://www.metodohebe.cl/
- https://www.metodohebe.cl/fundador/
- https://www.metodohebe.cl/clinica/como-confirmamos-tu-hora-por-whatsapp
- https://www.metodohebe.cl/evaluacion

Buscar FAQ, Organization/MedicalBusiness, Article, Person.
Enviar IndexNow / pedir indexación de `/clinica/*` y `/fundador/`.

Cuando Clinera tenga booking público por marca, sustituir `/evaluacion`
en los CTAs de `/clinica/*`. Hoy no existe `URL_RESERVA_HEBE`.
