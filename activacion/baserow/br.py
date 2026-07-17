"""Minimal Baserow REST client with JWT auto-refresh. Read/write schema."""
import json, time, urllib.request, urllib.error, os, re

BR = os.environ.get("BASEROW_URL", "https://core.oacg.cl")


def _load_creds():
    """Entorno primero (así corre en la VM), archivo después (así corre local)."""
    c = {k: os.environ[k] for k in ("BASEROW_EMAIL", "BASEROW_PASSWORD")
         if os.environ.get(k)}
    if len(c) == 2:
        return c
    for p in (os.environ.get("BASEROW_CREDENTIALS"),
              "/opt/activacion/.env",
              os.path.expanduser("~/.config/baserow/credentials")):
        if p and os.path.exists(p):
            for line in open(p):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    c.setdefault(k.strip(), v.strip())
            if c.get("BASEROW_EMAIL") and c.get("BASEROW_PASSWORD"):
                return c
    raise RuntimeError(
        "Faltan credenciales de Baserow. Setea BASEROW_EMAIL y BASEROW_PASSWORD, "
        "o deja un archivo en /opt/activacion/.env o ~/.config/baserow/credentials")


_creds = _load_creds()

_tok = {"v": None, "t": 0}


def jwt():
    if _tok["v"] and time.time() - _tok["t"] < 240:
        return _tok["v"]
    r = urllib.request.Request(
        BR + "/api/user/token-auth/",
        data=json.dumps({"email": _creds["BASEROW_EMAIL"],
                         "password": _creds["BASEROW_PASSWORD"]}).encode(),
        headers={"Content-Type": "application/json"})
    _tok["v"] = json.loads(urllib.request.urlopen(r, timeout=30).read())["token"]
    _tok["t"] = time.time()
    return _tok["v"]


def call(method, path, body=None, _retry=True):
    r = urllib.request.Request(
        BR + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "JWT " + jwt(), "Content-Type": "application/json"},
        method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as x:
            raw = x.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        if e.code == 401 and _retry:
            _tok["v"] = None
            return call(method, path, body, _retry=False)
        raise RuntimeError("HTTP %s %s -> %s" % (e.code, path, e.read().decode()[:600]))


# ---- schema helpers ----
def tables(db):
    return call("GET", "/api/database/tables/database/%s/" % db)

def fields(tid):
    return call("GET", "/api/database/fields/table/%s/" % tid)

def create_table(db, name):
    return call("POST", "/api/database/tables/database/%s/" % db, {"name": name})

def create_field(tid, spec):
    return call("POST", "/api/database/fields/table/%s/" % tid, spec)

def update_field(fid, spec):
    return call("PATCH", "/api/database/fields/%s/" % fid, spec)

def delete_field(fid):
    return call("DELETE", "/api/database/fields/%s/" % fid)

def rows(tid, size=200):
    return call("GET", "/api/database/rows/table/%s/?user_field_names=true&size=%s" % (tid, size))

def delete_row(tid, rid):
    return call("DELETE", "/api/database/rows/table/%s/%s/" % (tid, rid))


def probe_formula(tid, formula):
    """Create a temp formula field, report error, delete it. Returns (ok, error)."""
    name = "__probe_%d" % (time.time() * 1000 % 1e9)
    try:
        f = create_field(tid, {"name": name, "type": "formula", "formula": formula})
    except RuntimeError as e:
        return False, str(e)
    err = f.get("error")
    try:
        delete_field(f["id"])
    except Exception:
        pass
    return (err is None), err
