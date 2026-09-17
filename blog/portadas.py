#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la portada de cada entrada del blog, con identidad freaknerd.

Misma estructura que las portadas de Propiman —logo arriba, kicker con raya,
titular con una palabra en el acento, subtítulo, y abajo la URL con una
píldora— pero con el sistema de freaknerd: negro, verde eléctrico, trama de
puntos y el filete degradado superior.

Salen a 2400×1260 (el doble de 1200×630) para que se vean nítidas en pantallas
retina y sirvan igual como imagen de compartir.

    python3 blog/portadas.py            # solo las que faltan
    python3 blog/portadas.py --rehacer  # todas, aunque ya existan

Necesita Chrome y el servidor local en el puerto 4321.
"""
import json, os, re, subprocess, sys, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _chrome():
    """Busca Chrome donde suele estar. En GitHub Actions es google-chrome."""
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    candidatos = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium",
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    import shutil
    for n in ("google-chrome", "chromium", "chrome"):
        r = shutil.which(n)
        if r:
            return r
    sys.exit("No encontré Chrome. Define la variable CHROME con su ruta.")

CHROME = _chrome()
PUERTO = 4321


def resaltar(titulo):
    """Pone en verde la última palabra larga del titular.

    Propiman resalta una palabra a mano. Acá se elige sola: la última de más
    de cuatro letras, que casi siempre es la que carga el significado y además
    cae al final, donde la vista se detiene."""
    palabras = titulo.split()
    idx = None
    for i in range(len(palabras) - 1, -1, -1):
        limpia = re.sub(r'[^\wáéíóúñü]', '', palabras[i], flags=re.I)
        if len(limpia) > 4:
            idx = i
            break
    if idx is None:
        return html.escape(titulo)
    partes = [html.escape(p) for p in palabras]
    partes[idx] = '<em>%s</em>' % partes[idx]
    return " ".join(partes)


PLANTILLA = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&display=swap" rel="stylesheet">
<style>
  :root{{--green:#26E57C;--green2:#7CF4B0;--dim:#8A928C;--bone:#F4F6F3;
        --mono:ui-monospace,'SF Mono','Menlo',monospace;}}
  *{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;}}
  html,body{{width:1200px;height:630px;overflow:hidden;font-family:'Montserrat',sans-serif;}}
  .c{{position:relative;width:1200px;height:630px;background:#0A0B0D;color:var(--bone);overflow:hidden;}}
  /* La foto va al fondo, desaturada para que no le pelee al verde. */
  .foto{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
        filter:grayscale(.45) contrast(1.1) brightness(1.02);z-index:0;}}
  /* Velo en diagonal: opaco donde va el texto, transparente donde se ve la foto. */
  .velo{{position:absolute;inset:0;z-index:1;background:
        linear-gradient(100deg,#0A0B0D 0%,rgba(10,11,13,.96) 38%,
                        rgba(10,11,13,.60) 62%,rgba(10,11,13,.18) 100%);}}
  .grid{{position:absolute;inset:0;width:100%;height:100%;z-index:2;}}
  .rule{{position:absolute;top:0;left:0;right:0;height:6px;z-index:6;
        background:linear-gradient(90deg,var(--green) 0%,var(--green2) 40%,transparent 76%);}}
  .pad{{position:relative;z-index:3;height:100%;padding:56px 64px;display:flex;flex-direction:column;}}
  .wm{{font-weight:800;font-size:34px;letter-spacing:-1px;}}
  .wm i{{font-style:normal;color:var(--green);}}
  .kick{{margin-top:44px;display:flex;align-items:center;gap:16px;
        font-family:var(--mono);font-weight:700;font-size:17px;letter-spacing:3px;
        text-transform:uppercase;color:var(--green);}}
  .kick::before{{content:"";width:34px;height:2px;background:var(--green);}}
  h1{{margin-top:22px;font-weight:900;font-size:{tam}px;line-height:1.04;
      letter-spacing:-2px;max-width:{ancho}ch;}}
  h1 em{{font-style:normal;color:var(--green);}}
  .sub{{margin-top:22px;font-size:21px;font-weight:500;color:var(--dim);
       line-height:1.45;max-width:{ancho_sub}ch;}}
  .pie{{margin-top:auto;display:flex;align-items:center;justify-content:space-between;
       border-top:1px solid rgba(244,246,243,.14);padding-top:26px;}}
  .url{{font-family:var(--mono);font-size:18px;color:var(--dim);}}
  .pill{{font-family:var(--mono);font-size:15px;font-weight:600;letter-spacing:1px;
        color:var(--green);border:1px solid rgba(38,229,124,.4);border-radius:999px;
        padding:10px 20px;}}
</style></head><body>
<div class="c">
  {foto}
  <svg class="grid" viewBox="0 0 1200 630" preserveAspectRatio="none">
    <defs><pattern id="d" width="40" height="40" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="rgba(38,229,124,.13)"/></pattern></defs>
    <rect width="1200" height="630" fill="url(#d)"/></svg>
  <div class="rule"></div>
  <div class="pad">
    <div class="wm">freaknerd<i>_</i></div>
    <div class="kick">{cat}</div>
    <h1>{titulo}</h1>
    <div class="sub">{sub}</div>
    <div class="pie">
      <span class="url">freaknerd.co/blog</span>
      <span class="pill">{pill}</span>
    </div>
  </div>
</div>
</body></html>
"""


def tamano(titulo, con_foto=False):
    """Titulares largos bajan de tamaño para no desbordar la lámina.
    Con foto el texto vive en menos ancho, así que baja un escalón más."""
    n = len(titulo)
    base = 76 if n <= 38 else 66 if n <= 52 else 58 if n <= 68 else 50
    return base - 6 if con_foto else base


def generar(entrada, rehacer=False):
    slug = entrada["slug"]
    destino = os.path.join(RAIZ, "blog", slug, "portada.png")
    if os.path.exists(destino) and not rehacer:
        return False

    temporal = os.path.join(RAIZ, "_portada_tmp.html")
    sub = entrada["descripcion"]
    if len(sub) > 150:
        sub = sub[:147].rsplit(" ", 1)[0] + "…"

    foto = (entrada.get("imagen") or "").strip()
    bloque_foto = ('<img class="foto" src="%s" alt="">\n  <div class="velo"></div>'
                   % html.escape(foto)) if foto else ""

    with open(temporal, "w", encoding="utf-8") as f:
        f.write(PLANTILLA.format(
            cat=html.escape(entrada["categoria"]),
            titulo=resaltar(entrada["titulo"]),
            sub=html.escape(sub),
            pill=entrada["fecha"][:4],
            tam=tamano(entrada["titulo"], bool(foto)),
            ancho=15 if foto else 17,
            ancho_sub=48 if foto else 62,
            foto=bloque_foto))

    os.makedirs(os.path.dirname(destino), exist_ok=True)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2",       # 1200x630 -> 2400x1260
                    "--screenshot=" + destino,
                    "--window-size=1200,630",
                    "--virtual-time-budget=6000",
                    "http://localhost:%d/_portada_tmp.html" % PUERTO],
                   capture_output=True)
    os.remove(temporal)
    return True


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
