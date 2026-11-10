#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la portada de cada entrada del blog con la identidad v2.1 (manual de
marca, 10-nov-2026): ambiente piedra con retícula visible de 66, celda fn, titular
crema con UNA palabra clave en naranja (el titular nunca baja de 44 px) y campo de
puntos en el tercio inferior, con los ordenados exactamente en los vértices de la
retícula. Sin fotos, sin degradados, sin verde.

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
    """Pone en naranja la última palabra larga del titular.

    Las entradas vienen de Notion, así que la palabra se elige sola: la última
    de más de cuatro letras, que casi siempre carga el significado. El naranja
    solo va en titulares grandes (manual 4): aquí el mínimo es 44 px."""
    palabras = titulo.split()
    idx = None
    for i in range(len(palabras) - 1, -1, -1):
        if len(re.sub(r'[^\wáéíóúñü]', '', palabras[i], flags=re.I)) > 4:
            idx = i
            break
    partes = [html.escape(p) for p in palabras]
    if idx is not None:
        partes[idx] = '<b>%s</b>' % partes[idx]
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
  :root{{--piedra:#656A66;--crema:#F4EFE6;--naranja:#FF4A1C}}
  *{{margin:0;box-sizing:border-box}}
  html,body{{width:1200px;height:630px;overflow:hidden}}
  body{{background:var(--piedra);color:var(--crema);font-family:Montserrat;position:relative}}
  canvas{{position:absolute;left:0;top:0}}
  .mono{{font-family:'JetBrains Mono';font-weight:500;letter-spacing:.14em;text-transform:uppercase;
        font-size:12px;line-height:22px;position:absolute;white-space:nowrap}}
  .wm{{position:absolute;right:66px;top:44px;font:900 30px/44px Montserrat;letter-spacing:-.035em;
      display:inline-flex;align-items:baseline;height:44px}}
  .wm i{{display:inline-block;width:.2em;height:.2em;background:var(--naranja);margin-left:.06em}}
  .fn{{position:absolute;left:66px;top:33px;width:66px;height:66px;background:var(--naranja);display:grid;place-items:center}}
  .fn b{{font:900 35.6px/1 Montserrat;letter-spacing:-.05em;color:var(--crema);display:block;transform:translateY(-2px)}}
  .fn i{{position:absolute;right:-4px;bottom:-4px;width:7px;height:7px;background:var(--crema);outline:1.5px solid var(--piedra)}}
  .sig{{position:absolute;left:132px;top:33px;width:66px;height:66px;border:2px solid var(--naranja)}}
  h1{{position:absolute;left:66px;top:165px;width:1068px;font-weight:900;letter-spacing:-.035em;
     font-size:{tam}px;line-height:{lh}px}}
  h1 b{{color:var(--naranja);font-weight:900}}
</style></head>
<body>
<canvas id="d" width="2400" height="1260" style="width:1200px;height:630px"></canvas>
<div class="fn"><b>fn</b><i></i></div><div class="sig"></div>
<div class="wm">freaknerd<i></i></div>
<div class="mono" style="left:66px;top:110px">{cat} &middot; {fecha}</div>
<h1>{titulo}</h1>
<div class="mono" style="left:66px;width:1068px;top:582px;font-size:11px;display:flex;justify-content:space-between"><span>&larr; Así llega</span><span>freaknerd.co/blog</span><span>Así queda &rarr;</span></div>
<script>
// Campo de puntos (manual 7.6): retícula de 66 con origen (0,33). Los ordenados caen EXACTO en los
// vértices (a la derecha); hacia la izquierda se sueltan dentro de las celdas vecinas, más 1-2 puntos
// extra por celda. Crema sobre piedra; dos puntos vivos naranja sobre vértices de la zona ordenada.
function campo(L,T,W,H,seed){{
  var c=document.getElementById('d'),x=c.getContext('2d');
  var s=seed;function r(){{s=(s*16807)%2147483647;return s/2147483647}}
  function sm(v){{v=Math.max(0,Math.min(1,v));return v*v*(3-2*v)}}
  var G=66,GX=0,GY=33,R=3,i,j,cand=[];
  function dis(X){{var t=Math.max(0,Math.min(1,(X-L)/W/.7));return 1-t}}
  function put(px,py,rr,a){{if(px<L-.5||px>L+W+.5||py<T-.5||py>T+H+.5)return;
    x.globalAlpha=a;x.fillStyle='#F4EFE6';x.beginPath();x.arc(px+.5,py+.5,rr,0,7);x.fill();}}
  var i0=Math.ceil((L-GX)/G),i1=Math.floor((L+W-GX)/G),j0=Math.ceil((T-GY)/G),j1=Math.floor((T+H-GY)/G);
  for(i=i0;i<=i1;i++)for(j=j0;j<=j1;j++){{
    var X=GX+i*G,Y=GY+j*G,d=dis(X),e=sm(d);
    put(X+(r()*2-1)*.9*G*e,Y+(r()*2-1)*.9*G*e,R,.95);
    if(d<=.05&&(X-L)/W>.55)cand.push([X,Y]);}}
  for(i=i0-1;i<=i1;i++)for(j=j0-1;j<=j1;j++){{
    var cx=GX+(i+.5)*G,cy=GY+(j+.5)*G,dd=dis(cx),k=sm(dd*1.25-.05);if(k<=0)continue;
    var n=r()<.5?1:2;for(var q=0;q<n;q++)if(r()<k)put(GX+(i+r())*G,GY+(j+r())*G,R*.8,.25+.45*dd);}}
  if(cand.length>4){{x.globalAlpha=1;x.fillStyle='#FF4A1C';var z=R*8/3;
    [cand[Math.floor(cand.length*.35)],cand[Math.floor(cand.length*.8)]].forEach(function(p){{x.fillRect(p[0]+.5-z/2,p[1]+.5-z/2,z,z)}});}}
}}
function reticula(){{
  var c=document.getElementById('d'),x=c.getContext('2d');
  x.strokeStyle='rgba(244,239,230,.20)';x.lineWidth=1;x.beginPath();
  for(var gx=0;gx<=1200;gx+=66){{x.moveTo(gx+.5,0);x.lineTo(gx+.5,630)}}
  for(var gy=33;gy<=630;gy+=66){{x.moveTo(0,gy+.5);x.lineTo(1200,gy+.5)}}
  x.stroke();
}}
document.fonts.ready.then(function(){{
  document.getElementById('d').getContext('2d').scale(2,2);
  reticula();
  campo(66,429,1068,132,{semilla});
}});
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
