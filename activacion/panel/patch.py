# -*- coding: utf-8 -*-
"""Registra/actualiza /activacion en el panel tech.oacg.cl.
QUITAR-Y-REPONER: es re-ejecutable aunque el ORIG ya tenga una versión anterior
del módulo (la borra y pone la nueva). No toca el resto del panel."""
import io, re, sys

s = io.open("index.html.ORIG", encoding="utf-8").read()
orig_len = len(s)
MOD = io.open("act_module.js", encoding="utf-8").read()
CSS = io.open("act.css", encoding="utf-8").read()

RESIZE = """/*DWRESIZE*/(function(){var DW=document.getElementById('drawer');if(!DW)return;
var sv=parseInt(localStorage.getItem('work.drawer.w')||'0',10);DW.style.width=(sv>=380?sv:640)+'px';
if(!document.getElementById('drawerGrip')){var g=document.createElement('div');g.id='drawerGrip';DW.appendChild(g);
var drag=false;g.addEventListener('mousedown',function(e){drag=true;document.body.classList.add('dw-resizing');e.preventDefault();});
window.addEventListener('mousemove',function(e){if(!drag)return;var nw=window.innerWidth-e.clientX;
nw=Math.max(380,Math.min(nw,Math.min(1280,window.innerWidth-40)));DW.style.width=nw+'px';});
window.addEventListener('mouseup',function(){if(!drag)return;drag=false;document.body.classList.remove('dw-resizing');
localStorage.setItem('work.drawer.w',parseInt(DW.style.width,10));});}})();/*/DWRESIZE*/"""

PERFIL = "/* ===== Perfil global ===== */"

# ── limpiar versiones anteriores (idempotencia) ─────────────────────────────
# módulo viejo: desde el marcador ACTIVACIÓN hasta (sin incluir) Perfil global
s = re.sub(r"/\* ═+ ACTIVACIÓN · tabla 957.*?(?=" + re.escape(PERFIL) + ")", "", s, flags=re.S)
# css inline viejo (primera versión, terminaba en .actbanner)
s = re.sub(r"/\* ── Activación \(tabla 957\).*?\.actbanner\{[^}]*\}\n?", "", s, flags=re.S)
# style dedicado y resize viejos
s = re.sub(r'<style id="actCSS">.*?</style>\n?', "", s, flags=re.S)
s = re.sub(r"/\*DWRESIZE\*/.*?/\*/DWRESIZE\*/", "", s, flags=re.S)

n = 0
def one(old, new, what):
    global s, n
    if new in s:
        return
    c = s.count(old)
    if c != 1:
        print("  !! ABORTO %s: ancla x%d" % (what, c)); sys.exit(1)
    s = s.replace(old, new); n += 1; print("  +", what)

# ── 7 puntos de registro de la ruta (idempotentes) ──────────────────────────
one("sol:['solicitudes'],mkt:['marketing']};",
    "sol:['solicitudes'],mkt:['marketing'],act:['activacion','activación']};", "SLUGS")
one("if(['ventas','v26','fact','jul','lib','car','mes','onb','uso','mov','scrum','sol','mkt'].includes(h))return h;",
    "if(['ventas','v26','fact','jul','lib','car','mes','onb','uso','mov','scrum','sol','mkt','act'].includes(h))return h;", "modFromPath")
one("['ventas','v26','fact','jul','lib','car','mes','onb','uso','mov','scrum','sol','mkt'].forEach(m=>document.getElementById('mod-'+m).classList.toggle('hidden',m!==mod));",
    "['ventas','v26','fact','jul','lib','car','mes','onb','uso','mov','scrum','sol','mkt','act'].forEach(m=>document.getElementById('mod-'+m).classList.toggle('hidden',m!==mod));", "go() toggle")
one('<div id="mod-mkt" class="hidden"></div>',
    '<div id="mod-mkt" class="hidden"></div>\n    <div id="mod-act" class="hidden"></div>', "<div mod-act>")
one("sol:'Solicitudes',mkt:'Marketing'};",
    "sol:'Solicitudes',mkt:'Marketing',act:'Activación'};", "BOARDS")
one("const BOARDS={ventas:",
    "BOARD_ICONS.act='<svg width=\"15\" height=\"15\" viewBox=\"0 0 256 256\" fill=\"currentColor\">"
    "<path d=\"M128 24a104 104 0 1 0 104 104A104.2 104.2 0 0 0 128 24Zm0 192a88 88 0 1 1 88-88a88.1 88.1 0 0 1-88 88Z\"/>"
    "<path d=\"M173.7 98.3a8 8 0 0 1 0 11.4l-48 48a8 8 0 0 1-11.4 0l-24-24a8 8 0 0 1 11.4-11.4L120 140.7l42.3-42.4a8 8 0 0 1 11.4 0Z\"/></svg>';\n"
    "const BOARDS={ventas:", "BOARD_ICONS.act")
one("const BOARD_TIDS={v26:156,car:612,jul:951,lib:611,onb:327,uso:939,mov:940,scrum:950,sol:952};",
    "const BOARD_TIDS={v26:156,car:612,jul:951,lib:611,onb:327,uso:939,mov:940,scrum:950,sol:952,act:957};", "BOARD_TIDS")
one("if(mod==='onb'&&!GONB.loaded)GONB.init();",
    "if(mod==='onb'&&!GONB.loaded)GONB.init();\n  if(mod==='act'&&!GACT.loaded)GACT.init();", "init GACT")

# ── módulo JS: antes de Perfil global (usa makeGrid/toast/esc/brCol/fdate/brUpload) ──
assert s.count(PERFIL) == 1
s = s.replace(PERFIL, MOD + "\n" + PERFIL); n += 1; print("  + módulo JS")

# ── CSS: style dedicado antes de </head> (fácil de re-strippear) ──
assert s.count("</head>") == 1
s = s.replace("</head>", '<style id="actCSS">\n' + CSS + '\n</style>\n</head>'); n += 1; print("  + CSS (style dedicado)")

# ── drawer redimensionable: después de `let drawerOpen=false;` ──
one("let drawerOpen=false;", "let drawerOpen=false;\n" + RESIZE, "drawer redimensionable")

io.open("index.html", "w", encoding="utf-8").write(s)
print("\n%d cambios · %d -> %d bytes (%+d)" % (n, orig_len, len(s), len(s) - orig_len))
