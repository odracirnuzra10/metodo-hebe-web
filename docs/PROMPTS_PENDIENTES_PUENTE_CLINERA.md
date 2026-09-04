# Pendientes — puente Hebe → Clinera

El lado Clinera **ya está publicado** (2026-09-04):
https://www.clinera.io/casos/metodo-hebe

`/clinica/por-que-respondemos-en-minutos` apunta a esa URL.

Lo que sigue no se cierra desde este repo.

---

## 1) Off-site / GBP (no es código de este repo)

Obtener el CID real de Google Business Profile de cada sede Método Hebe
(Vitacura, Concón, Los Ángeles) y entregar URLs del tipo:

```
https://maps.google.com/?cid=XXXXXXXX
```

Luego, en el bloque `PUENTE-AEO-GRAPH` y en el schema de home, reemplazar
`sameAs`/`hasMap` de cada MedicalClinic (hoy `maps/search`) por el CID real.
No inventar CIDs.

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
