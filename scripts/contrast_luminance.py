#!/usr/bin/env python3
"""H2.1 — WCAG luminance of CTA / stars / greys on 12 pages at 390×844.

Uses Chrome headless + DevTools Protocol when available; otherwise
reports the locked token pairs (ink on teal = 6.53:1).
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
VIEWPORT = (390, 844)
MIN_AA = 4.5
PAGES = [
    "/",
    "/evaluacion",
    "/criolipolisis",
    "/guatita-de-delantal-auge-y-ley",
    "/planes",
    "/resultados",
    "/clinica-estetica-corporal-vitacura",
    "/clinica-estetica-corporal-concon",
    "/clinica-estetica-corporal-los-angeles",
    "/flacidez",
    "/celulitis",
    "/lipoescultura-sin-cirugia",
]
SELECTORS = [
    ".nav-cta",
    ".cta-btn",
    ".inline-cta .btn-primary",
    ".mobile-sticky-cta button",
    ".mobile-sticky-main",
    ".btn-plan-cta",
    ".wa-btn.enabled",
    ".success-wa-btn",
    ".confirm-btn",
    ".review-stars",
    ".greviews .stars",
]


def rel_lum(rgb: tuple[float, float, float]) -> float:
    def f(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    l1, l2 = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def parse_rgb(s: str) -> tuple[float, float, float] | None:
    s = (s or "").strip()
    if s in ("transparent", "rgba(0, 0, 0, 0)"):
        return None
    if s.startswith("rgb"):
        nums = s[s.find("(") + 1 : s.find(")")].split(",")
        return tuple(float(x) for x in nums[:3])  # type: ignore[return-value]
    return None


def hex_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def token_pairs() -> list[tuple[str, float]]:
    pairs = [
        ("CTA ink #14201F on teal #14B5A7", contrast(hex_rgb("14201F"), hex_rgb("14B5A7"))),
        ("CTA ink on cyan-d #0FA094", contrast(hex_rgb("14201F"), hex_rgb("0FA094"))),
        ("WA ink on #25D366", contrast(hex_rgb("14201F"), hex_rgb("25D366"))),
        ("stars #8A6100 on white", contrast(hex_rgb("8A6100"), hex_rgb("FFFFFF"))),
        ("grey #5A6B6B on white", contrast(hex_rgb("5A6B6B"), hex_rgb("FFFFFF"))),
        ("teal-darker #0A6B65 on cream", contrast(hex_rgb("0A6B65"), hex_rgb("FAF9F7"))),
    ]
    return pairs


EVAL_JS = r"""
(() => {
  const sels = %s;
  const out = [];
  const seen = new Set();
  for (const sel of sels) {
    document.querySelectorAll(sel).forEach((el, i) => {
      const cs = getComputedStyle(el);
      const key = sel + '|' + i + '|' + cs.color + '|' + cs.backgroundColor;
      if (seen.has(key)) return;
      seen.add(key);
      const r = el.getBoundingClientRect();
      out.push({
        sel, i,
        color: cs.color,
        bg: cs.backgroundColor,
        w: Math.round(r.width),
        h: Math.round(r.height),
        text: (el.innerText || '').trim().slice(0, 48)
      });
    });
  }
  return out;
})()
""" % json.dumps(SELECTORS)


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def start_server(port: int) -> ThreadingHTTPServer:
    os.chdir(PUBLIC)

    class H(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            return

        def do_GET(self):
            raw = self.path.split("?", 1)[0]
            if raw.endswith("/"):
                raw = raw[:-1] or "/"
            candidate = PUBLIC / raw.lstrip("/")
            if raw != "/" and not candidate.exists():
                html = PUBLIC / (raw.lstrip("/") + ".html")
                if html.exists():
                    self.path = "/" + html.name
            return super().do_GET()

    httpd = ThreadingHTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def chrome_cdp(http_port: int) -> tuple[subprocess.Popen, int] | None:
    debug = free_port()
    chrome = os.environ.get("CHROME", "google-chrome")
    data_dir = Path("/tmp/hebe-contrast-chrome")
    data_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        f"--user-data-dir={data_dir}",
        f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
        f"--remote-debugging-port={debug}",
        "--remote-debugging-address=127.0.0.1",
        "--remote-allow-origins=*",
        "about:blank",
    ]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        return None
    for _ in range(40):
        try:
            socket.create_connection(("127.0.0.1", debug), 0.2).close()
            return proc, debug
        except OSError:
            time.sleep(0.1)
    proc.kill()
    return None


def cdp_eval(debug_port: int, url: str) -> list[dict]:
    try:
        import websocket  # type: ignore
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "websocket-client"])
        import websocket  # type: ignore

    import urllib.request

    listing = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{debug_port}/json/list", timeout=5).read())
    ws_url = listing[0]["webSocketDebuggerUrl"]
    ws = websocket.create_connection(ws_url, timeout=20)
    mid = 0

    def call(method: str, params: dict | None = None, wait: str | None = None):
        nonlocal mid
        mid += 1
        ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        wanted = mid
        last = None
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == wanted:
                return msg
            last = msg

    call("Page.enable")
    call("Runtime.enable")
    call("Emulation.setDeviceMetricsOverride", {
        "width": VIEWPORT[0],
        "height": VIEWPORT[1],
        "deviceScaleFactor": 1,
        "mobile": True,
    })
    call("Page.navigate", {"url": url})
    deadline = time.time() + 12
    while time.time() < deadline:
        mid += 1
        ws.send(json.dumps({
            "id": mid,
            "method": "Runtime.evaluate",
            "params": {"expression": "document.readyState", "returnByValue": True},
        }))
        wanted = mid
        state = None
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == wanted:
                state = ((msg.get("result") or {}).get("result") or {}).get("value")
                break
        if state == "complete":
            break
        time.sleep(0.15)
    time.sleep(0.2)
    res = call("Runtime.evaluate", {"expression": EVAL_JS, "returnByValue": True})
    ws.close()
    return res.get("result", {}).get("result", {}).get("value") or []


def main() -> int:
    print(f"viewport {VIEWPORT[0]}x{VIEWPORT[1]}")
    print("token pairs (locked):")
    fails = 0
    for name, ratio in token_pairs():
        ok = ratio + 1e-9 >= MIN_AA
        print(f"  {'PASS' if ok else 'FAIL'} {ratio:.2f}:1  {name}")
        if not ok:
            fails += 1

    http_port = free_port()
    httpd = start_server(http_port)
    chrome = chrome_cdp(http_port)
    if not chrome:
        print("chrome CDP unavailable — token pairs only")
        httpd.shutdown()
        return 1 if fails else 0

    proc, debug = chrome
    print("live computed styles:")
    try:
        for path in PAGES:
            url = f"http://127.0.0.1:{http_port}{path}"
            try:
                rows = cdp_eval(debug, url)
            except Exception as e:
                print(f"  {path} ERROR {e}")
                fails += 1
                continue
            print(f"  {path}")
            if not rows:
                print("    (no matching CTA/stars in viewport)")
                continue
            for row in rows:
                fg = parse_rgb(row["color"])
                bg = parse_rgb(row["bg"])
                if not fg or not bg:
                    continue
                ratio = contrast(fg, bg)
                ok = ratio + 1e-9 >= MIN_AA
                if not ok:
                    fails += 1
                label = row["sel"]
                print(f"    {'PASS' if ok else 'FAIL'} {ratio:.2f}:1  {label}  {row['color']} / {row['bg']}")
    finally:
        proc.kill()
        httpd.shutdown()

    print("fails", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
