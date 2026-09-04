# Pendientes — puente Hebe → Clinera

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
