#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la portada de cada entrada del blog con la identidad v1 (manual de
marca, 10-nov-2026): fondo blanco, titular en azul con UNA celda seleccionada,
campo de puntos en el tercio inferior (de disperso a ordenado, de izquierda a
derecha) y el wordmark. Sin fotos, sin degradados, sin verde.

Las fuentes se leen del propio repositorio (assets/fonts), así que la portada
sale igual en el Mac y en GitHub Actions, sin depender de Google Fonts.

Salen a 2400×1260 (el doble de 1200×630): nítidas en retina y sirven igual
como imagen de compartir.

    python3 blog/portadas.py            # solo las que faltan
    python3 blog/portadas.py --rehacer  # todas, aunque ya existan
"""
import json, os, re, shutil, subprocess, sys, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _chrome():
    """Busca Chrome donde suele estar. En GitHub Actions es google-chrome."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"):
        if os.path.exists(c):
            return c
    for n in ("google-chrome", "chromium", "chrome"):
        r = shutil.which(n)
        if r:
            return r
    sys.exit("No encontré Chrome. Define la variable CHROME con su ruta.")


CHROME = _chrome()


def resaltar(titulo):
    """Pone la celda seleccionada en la última palabra larga del titular.

    Las entradas vienen de Notion, así que la palabra se elige sola: la última
    de más de cuatro letras, que casi siempre carga el significado. La celda va
    en un solo renglón (nowrap) y lleva el tirador de la marca."""
    palabras = titulo.split()
    idx = None
    for i in range(len(palabras) - 1, -1, -1):
        if len(re.sub(r'[^\wáéíóúñü]', '', palabras[i], flags=re.I)) > 4:
            idx = i
            break
    partes = [html.escape(p) for p in palabras]
    if idx is not None:
        partes[idx] = '<span class="sel">%s</span>' % partes[idx]
    return " ".join(partes)


def tamano(titulo):
    """(tamaño, interlineado): titulares largos bajan de escalón, siempre en
    múltiplos de 11 para quedar en la retícula."""
    n = len(titulo)
    if n <= 38: return 72, 77
    if n <= 52: return 60, 66
    if n <= 68: return 52, 55
    return 44, 44


FUENTES = os.path.join(RAIZ, "assets", "fonts")

PLANTILLA = """<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<style>
  @font-face{{font-family:Montserrat;font-weight:500;src:url('{f}/Montserrat-500.ttf')}}
  @font-face{{font-family:Montserrat;font-weight:900;src:url('{f}/Montserrat-900.ttf')}}
  @font-face{{font-family:'JetBrains Mono';font-weight:500;src:url('{f}/JetBrainsMono-500.ttf')}}
  :root{{--blanco:#FCFFFF;--azul:#09318D;--azul-texto2:#4B5C8C;--azul-nota:#5A6B94;--rosa:#EED2E2}}
  *{{margin:0;box-sizing:border-box}}
  html,body{{width:1200px;height:630px;overflow:hidden}}
  body{{background:var(--blanco);color:var(--azul);font-family:Montserrat;position:relative}}
  canvas{{position:absolute;left:0;top:0}}
  .mono{{font-family:'JetBrains Mono';font-weight:500;letter-spacing:.14em;text-transform:uppercase;
        font-size:12px;line-height:22px;position:absolute}}
  .wm{{position:absolute;left:66px;top:33px;font:900 30px/44px Montserrat;letter-spacing:-.035em;
      display:inline-flex;align-items:baseline;height:44px}}
  .wm i{{display:inline-block;width:.2em;height:.2em;background:var(--azul);margin-left:.06em}}
  h1{{position:absolute;left:66px;top:154px;width:1068px;font-weight:900;letter-spacing:-.035em;
     font-size:{tam}px;line-height:{lh}px}}
  .sel{{display:inline-block;position:relative;background:var(--rosa);padding:0 .14em;
       box-shadow:inset 0 0 0 4px var(--azul);white-space:nowrap}}
  .sel::after{{content:"";position:absolute;right:-6px;bottom:-6px;width:11px;height:11px;
              background:var(--azul);box-shadow:0 0 0 2px var(--blanco)}}
</style></head>
<body>
<canvas id="d" width="2400" height="1260" style="width:1200px;height:630px"></canvas>
<div class="wm">freaknerd<i></i></div>
<div class="mono" style="right:66px;top:44px;color:var(--azul-texto2)">{cat}</div>
<div class="mono" style="left:66px;top:110px;color:var(--azul-texto2)">Apunte · {fecha}</div>
<h1>{titulo}</h1>
<div class="mono" style="left:66px;width:1068px;top:552px;font-size:11px;color:var(--azul-nota);display:flex;justify-content:space-between"><span>&larr; Así llega</span><span>freaknerd.co/blog</span><span>Así queda &rarr;</span></div>
<script>
// Campo de puntos del manual: retícula de 22 px, de disperso a ordenado de izquierda a derecha.
function dots(X0,X1,Y0,Y1,seed){{var c=document.getElementById('d'),x=c.getContext('2d');x.scale(2,2);
var s=seed;function r(){{return(s=(s*16807)%2147483647)/2147483647}}var G=22;
for(var gx=X0;gx<=X1;gx+=G)for(var gy=Y0;gy<=Y1;gy+=G){{
 var t=Math.min(1,Math.max(0,(gx-X0)/((X1-X0)*.85)));var e=t*t*(3-2*t);var j=(1-e)*14;
 if(r()>0.2+0.8*e)continue;x.globalAlpha=0.15+0.7*e;x.fillStyle='#09318D';
 x.beginPath();x.arc(gx+(r()-.5)*2*j,gy+(r()-.5)*2*j,1.2+1.1*e,0,7);x.fill();}}}}
document.fonts.ready.then(function(){{dots(66,1122,440,528,{semilla})}});
</script>
</body></html>
"""


def generar(entrada, rehacer=False):
    slug = entrada["slug"]
    carpeta = os.path.join(RAIZ, "blog", slug)
    destino = os.path.join(carpeta, "portada.jpg")
    if os.path.exists(destino) and not rehacer:
        return False
    crudo = os.path.join(carpeta, "_portada.png")

    tam, lh = tamano(entrada["titulo"])
    # La misma entrada siempre da el mismo campo de puntos.
    semilla = 7 + sum(ord(c) for c in slug) % 90
    doc = PLANTILLA.format(
        f=FUENTES.replace("\\", "/"),
        cat=html.escape(entrada["categoria"]),
        fecha=entrada["fecha"][:4],
        titulo=resaltar(entrada["titulo"]),
        tam=tam, lh=lh, semilla=semilla)

    os.makedirs(carpeta, exist_ok=True)
    temporal = os.path.join(carpeta, "_portada.html")
    with open(temporal, "w", encoding="utf-8") as f:
        f.write(doc)

    # Las fuentes salen de assets/fonts por ruta de archivo: Chrome lee el
    # HTML suelto, no hace falta servidor local, ni acá ni en GitHub Actions.
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files",
                    "--force-device-scale-factor=2",
                    "--screenshot=" + crudo,
                    "--window-size=1200,630",
                    "--virtual-time-budget=6000",
                    "file://" + temporal],
                   capture_output=True)
    os.remove(temporal)
    if not os.path.exists(crudo):
        print("  ⚠ %s: Chrome no generó la portada" % slug)
        return False
    comprimir(crudo, destino)
    return True


def comprimir(png, jpg):
    """El PNG de una foto a 2400px pesa cerca de 3 MB y esta imagen aparece en
    el índice del blog y dentro del artículo. Propiman se apoya en un CDN que
    reescala; GitHub Pages no hace eso, así que se comprime acá."""
    try:
        from PIL import Image
    except ImportError:
        os.replace(png, jpg)          # sin Pillow, mejor pesada que ninguna
        print("    (sin Pillow: la portada queda sin comprimir)")
        return
    im = Image.open(png).convert("RGB")
    im.save(jpg, "JPEG", quality=86, optimize=True, progressive=True)
    os.remove(png)


def main():
    rehacer = "--rehacer" in sys.argv
    with open(os.path.join(RAIZ, "blog", "contenido.json"), encoding="utf-8") as f:
        datos = json.load(f)

    hechas, saltadas = [], []
    for e in datos["entradas"]:
        if e.get("estado") != "Publicado":
            continue
        (hechas if generar(e, rehacer) else saltadas).append(e["slug"])

    if hechas:   print("portadas generadas: " + ", ".join(hechas))
    if saltadas: print("ya existían: " + ", ".join(saltadas))
    if not hechas and not saltadas: print("no hay entradas publicadas")


if __name__ == "__main__":
    main()
