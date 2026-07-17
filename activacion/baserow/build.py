# -*- coding: utf-8 -*-
"""Construye la tabla `Activación`. Idempotente: salta lo que ya existe."""
import sys, br, schema_def as S

tid = int(open('tid.txt').read())
CACHE = {f['name']: f for f in br.fields(tid)}
errs = []


def mk(name, spec):
    if name in CACHE:
        return 'skip'
    try:
        f = br.create_field(tid, dict(spec, name=name))
    except RuntimeError as e:
        errs.append((name, str(e)))
        print('  FAIL %-30s %s' % (name, str(e)[:150]), flush=True)
        return 'fail'
    CACHE[name] = f
    if f.get('error'):
        errs.append((name, f['error']))
        print('  ERR  %-30s %s' % (name, str(f['error'])[:150]), flush=True)
        return 'err'
    return 'ok'


# 0) limpieza
for junk in ['_d', '_f', '_n', '_s', 'Notas', 'Activo']:
    if junk in CACHE:
        br.delete_field(CACHE.pop(junk)['id'])
        print('drop', junk, flush=True)
if 'Nombre' in CACHE:
    br.update_field(CACHE['Nombre']['id'], {'name': 'Name'})
    CACHE['Name'] = CACHE.pop('Nombre')
    print('rename Nombre -> Name', flush=True)

groups = [
    ('GRUPO 1 base', [(n, sp) for n, sp in S.BASE]),
    ('screenshots', [('%s 📸' % c, {'type': 'file'}) for c in S.SHOTS]),
    ('GRUPO 2 checks', [(n, {'type': 'formula', 'formula': f}) for n, f in S.CHECKS]),
    ('GRUPO 3 ok/ap', [(n, {'type': 'formula', 'formula': f}) for n, f in S.OKAP]),
    ('GRUPO 4 etapas', [(n, {'type': 'formula', 'formula': f}) for n, f in S.STAGES + S.STAGES4]),
    ('GRUPO 5 final', [(n, {'type': 'formula', 'formula': f}) for n, f in S.FINAL]),
]

for gname, items in groups:
    print('\n=== %s (%d) ===' % (gname, len(items)), flush=True)
    stats = {}
    for n, sp in items:
        r = mk(n, sp)
        stats[r] = stats.get(r, 0) + 1
    print('  ', stats, flush=True)

print('\n=== RESUMEN ===', flush=True)
print('campos totales:', len(br.fields(tid)), flush=True)
print('errores:', len(errs), flush=True)
for n, e in errs:
    print('  !!', n, '::', str(e)[:300], flush=True)
