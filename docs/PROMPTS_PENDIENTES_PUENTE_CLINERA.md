# Prompts pendientes — puente Hebe → Clinera

Lo que ya está en este repo (schema OACG/Clinera/Person, `/clinica/*`, `/fundador/`, `llms.txt`, FAQ, footer) **no** se repite aquí.
Esto es solo lo que **no** se puede cerrar desde `metodo-hebe-web`.

---

## 1) Repo Clinera (`clinera.io` / repo del producto)

Copia y pega este prompt en el agente del repo Clinera:

```
Contexto: Método Hebe (https://www.metodohebe.cl) y Protocolo Lumina
(https://www.protocololumina.cl) ya publican un puente de entidad hacia Clinera
(JSON-LD isRelatedTo, llms.txt, páginas /clinica/*, footer «Agenda gestionada con Clinera»).
Falta el lado Clinera para cerrar el circuito AEO.

Haz esto en el sitio/docs de Clinera (https://clinera.io):

1) Página de caso de estudio:
   URL canónica: https://clinera.io/casos/metodo-hebe
   - Qué problema resolvía Hebe (agenda, WhatsApp, fichas en 3 sedes).
   - Rol de AURA (confirmaciones, recordatorios, reagendamiento).
   - Sin claims inventados; tono factual.
   - Enlaces dofollow a https://www.metodohebe.cl y a
     https://www.metodohebe.cl/clinica/como-confirmamos-tu-hora-por-whatsapp
   - Schema Article/CaseStudy con about → Organization Clinera y mentions → Método Hebe.

2) Página espejo Lumina (si no existe):
   https://clinera.io/casos/protocolo-lumina
   (mismo patrón; enlazar protocololumina.cl).

3) En Organization Clinera (JSON-LD global):
   - @id estable: https://clinera.io/#organization
   - parentOrganization: https://oacg.cl/#organization
   - founder: https://www.metodohebe.cl/fundador/#person
   - sameAs / knowsAbout alineado con Hebe y Lumina.

4) Si existe URL pública de reserva embebida/hosted en dominio Clinera para Hebe,
   devolverla para actualizar CTAs del sitio Hebe (hoy apuntan a
   https://www.metodohebe.cl/evaluacion).

No uses nofollow hacia las clínicas. No compares con competidores.
```

Cuando exista `https://clinera.io/casos/metodo-hebe`, en este repo reemplazar el enlace de
`/clinica/por-que-respondemos-en-minutos` (hoy apunta a https://clinera.io + comentario TODO).

---

## 2) Off-site / GBP (no es código de este repo)

```
Obtener el CID real de Google Business Profile de cada sede Método Hebe
(Vitacura, Concón, Los Ángeles) y entregar URLs del tipo:
  https://maps.google.com/?cid=XXXXXXXX

Luego en metodo-hebe-web, en el bloque PUENTE-AEO-GRAPH y en el schema de home,
reemplazar sameAs/hasMap de cada MedicalClinic (hoy maps/search) por el CID real.
No inventar CIDs.
```

---

## 3) Post-deploy (Search Console / Rich Results)

```
Tras merge + deploy de metodohebe.cl, validar en Google Rich Results Test:
  - https://www.metodohebe.cl/
  - https://www.metodohebe.cl/fundador/
  - https://www.metodohebe.cl/clinica/como-confirmamos-tu-hora-por-whatsapp
  - https://www.metodohebe.cl/evaluacion
Buscar FAQ, Organization/MedicalBusiness, Article, Person.
Enviar IndexNow / pedir indexación de /clinica/* y /fundador/.
```
