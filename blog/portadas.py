#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la portada de cada entrada del blog, con identidad freaknerd.

Sigue la receta de las portadas de Propiman (03 Recursos/make_covers.py):
logo como imagen real, doble degradado, resplandor de color, sombra de texto
sobre el titular, y la foto embebida en base64 desde un archivo local.

Ese último punto es el que importa: la foto se descarga UNA vez a
blog/<slug>/fondo.jpg y de ahí en adelante la portada no depende de que ningún
servidor externo siga sirviéndola. Y como todo va embebido, Chrome renderiza
desde un archivo suelto: no hace falta servidor local.

Salen a 2400×1260 (el doble de 1200×630): nítidas en retina y sirven igual
como imagen de compartir.

    python3 blog/portadas.py            # solo las que faltan
    python3 blog/portadas.py --rehacer  # todas, aunque ya existan
"""
import base64, json, os, re, shutil, subprocess, sys, html
import urllib.request, urllib.error

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# El blanco, no el negro: el de la firma de correo va sobre fondo claro y
# sobre la portada oscura solo se vería el guion bajo verde.
WORDMARK = os.path.join(RAIZ, "assets", "sig", "wordmark-blanco.png")


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


def _ssl():
    """El Python de macOS suele venir sin certificados y entonces toda petición
    https falla. Sin esto, descargar la foto fallaría siempre en el Mac."""
    try:
        import ssl, certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return None


def b64(ruta, tipo):
    with open(ruta, "rb") as fh:
        return "data:%s;base64,%s" % (tipo, base64.b64encode(fh.read()).decode())


def traer_fondo(url, destino):
    """Descarga la foto una sola vez. Devuelve la ruta local, o None.

    Guardarla en vez de enlazarla es lo que hace Propiman, y es lo correcto:
    una portada no debería romperse porque un servidor ajeno cambió de idea."""
    if not url:
        return None
    if url.startswith("/"):                       # ruta del propio sitio
        local = os.path.join(RAIZ, url.lstrip("/"))
        return local if os.path.exists(local) else None
    if os.path.exists(destino):
        return destino
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "freaknerd-blog"})
        with urllib.request.urlopen(req, timeout=30, context=_ssl()) as r:
            if r.status != 200 or "image" not in r.headers.get("Content-Type", ""):
                return None
            datos = r.read()
        if len(datos) < 2048:                     # una imagen real pesa más
            return None
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "wb") as fh:
            fh.write(datos)
        return destino
    except Exception as e:
        print("    (no se pudo descargar: %s)" % type(e).__name__)
        return None


def resaltar(titulo):
    """Pone en verde la última palabra larga del titular.

    Propiman escoge la palabra a mano porque su lista está escrita a mano. Acá
    las entradas vienen de Notion, así que se elige sola: la última de más de
    cuatro letras, que casi siempre carga el significado y cae donde la vista
    se detiene."""
    palabras = titulo.split()
    idx = None
    for i in range(len(palabras) - 1, -1, -1):
        if len(re.sub(r'[^\wáéíóúñü]', '', palabras[i], flags=re.I)) > 4:
            idx = i
            break
    partes = [html.escape(p) for p in palabras]
    if idx is not None:
        partes[idx] = '<span class="c">%s</span>' % partes[idx]
    return " ".join(partes)


def tamano(titulo, con_foto=False):
    """Titulares largos bajan de tamaño para no desbordar la lámina.
    Con foto el texto vive en menos ancho, así que baja un escalón más."""
    n = len(titulo)
    base = 76 if n <= 38 else 66 if n <= 52 else 58 if n <= 68 else 50
    return base - 6 if con_foto else base


PLANTILLA = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;800;900&display=swap" rel="stylesheet">
<style>
  :root{{--green:#26E57C;--green2:#7CF4B0;--dim:#9AA3A8;--bone:#F4F6F3;
        --mono:ui-monospace,'SF Mono','Menlo',monospace;}}
  *{{margin:0;padding:0;box-sizing:border-box;-webkit-print-color-adjust:exact;}}
  html,body{{width:1200px;height:630px;overflow:hidden;}}
  .card{{position:relative;width:1200px;height:630px;background:#0A0B0D;
        font-family:'Montserrat',sans-serif;overflow:hidden;}}
  .bg{{position:absolute;inset:0;background-image:url('{fondo}');
      background-size:cover;background-position:center;
      filter:grayscale(.45) contrast(1.1);}}
  /* Dos degradados: el diagonal abre sitio al texto, el de abajo rescata el
     pie. Con uno solo, la URL y la píldora se perdían sobre fotos claras. */
  .velo{{position:absolute;inset:0;background:
        linear-gradient(100deg,rgba(10,11,13,.96) 0%,rgba(10,11,13,.93) 38%,
                        rgba(10,11,13,.60) 66%,rgba(10,11,13,.20) 100%),
        linear-gradient(0deg,rgba(10,11,13,.88) 0%,rgba(10,11,13,0) 32%);}}
  /* Trama de puntos, que es la de la casa. Propiman usa líneas. */
  .grid{{position:absolute;inset:0;
        background-image:radial-gradient(rgba(38,229,124,.16) 1px,transparent 1px);
        background-size:40px 40px;}}
  /* Resplandor verde: da profundidad y ata la lámina al acento de marca. */
  .glow{{position:absolute;top:-240px;right:-180px;width:680px;height:680px;border-radius:50%;
        background:radial-gradient(circle,rgba(38,229,124,.22) 0%,rgba(38,229,124,0) 66%);}}
  .rule{{position:absolute;top:0;left:0;right:0;height:6px;
        background:linear-gradient(90deg,var(--green) 0%,var(--green2) 40%,transparent 76%);}}
  .inner{{position:absolute;inset:0;padding:58px 64px;
         display:flex;flex-direction:column;justify-content:space-between;}}
  .logo{{width:196px;height:auto;display:block;align-self:flex-start;
        filter:drop-shadow(0 2px 12px rgba(0,0,0,.5));}}
  .mid{{margin-top:auto;margin-bottom:auto;}}
  .kicker{{font-family:var(--mono);font-size:17px;font-weight:700;letter-spacing:.24em;
          color:var(--green);text-transform:uppercase;margin-bottom:20px;}}
  .kicker::before{{content:"";display:inline-block;width:34px;height:2px;
                  background:var(--green);vertical-align:middle;
                  margin-right:14px;margin-bottom:4px;}}
  h1{{font-size:{tam}px;line-height:1.05;font-weight:900;color:var(--bone);
     letter-spacing:-.025em;max-width:{ancho}ch;
     text-shadow:0 2px 24px rgba(0,0,0,.55);}}
  h1 .c{{color:var(--green);}}
  .sub{{margin-top:20px;font-size:21px;font-weight:500;color:var(--dim);
       line-height:1.45;max-width:{ancho_sub}ch;
       text-shadow:0 1px 14px rgba(0,0,0,.6);}}
  .foot{{display:flex;align-items:center;justify-content:space-between;}}
  .url{{font-family:var(--mono);font-size:18px;color:var(--dim);
       text-shadow:0 1px 10px rgba(0,0,0,.7);}}
  /* Píldora rellena, no contorneada: sobre foto el contorno desaparecía. */
  .badge{{font-family:var(--mono);font-size:15px;font-weight:700;color:#0A0B0D;
         background:var(--green);padding:9px 18px;border-radius:999px;letter-spacing:.02em;}}
</style></head>
<body><div class="card">
  {bg}
  <div class="velo"></div><div class="grid"></div><div class="glow"></div>
  <div class="rule"></div>
  <div class="inner">
    <img class="logo" src="{logo}" alt="freaknerd">
    <div class="mid">
      <div class="kicker">{cat}</div>
      <h1>{titulo}</h1>
      <div class="sub">{sub}</div>
    </div>
    <div class="foot">
      <div class="url">freaknerd.co/blog</div>
      <div class="badge">{badge}</div>
    </div>
  </div>
</div></body></html>
"""


def generar(entrada, rehacer=False):
    slug = entrada["slug"]
    carpeta = os.path.join(RAIZ, "blog", slug)
    destino = os.path.join(carpeta, "portada.jpg")
    if os.path.exists(destino) and not rehacer:
        return False
    crudo = os.path.join(carpeta, "_portada.png")

    url_foto = (entrada.get("imagen") or "").strip()
    fondo = traer_fondo(url_foto, os.path.join(carpeta, "fondo.jpg"))
    if url_foto and not fondo:
        print("  ⚠ %s: la foto no se pudo traer; la portada sale sin ella\n    %s"
              % (slug, url_foto))

    sub = entrada["descripcion"]
    if len(sub) > 150:
        sub = sub[:147].rsplit(" ", 1)[0] + "…"

    tipo = "image/png" if (fondo or "").lower().endswith(".png") else "image/jpeg"
    doc = PLANTILLA.format(
        fondo=b64(fondo, tipo) if fondo else "",
        bg='<div class="bg"></div>' if fondo else "",
        logo=b64(WORDMARK, "image/png"),
        cat=html.escape(entrada["categoria"]),
        titulo=resaltar(entrada["titulo"]),
        sub=html.escape(sub),
        badge="Guía práctica " + entrada["fecha"][:4],
        tam=tamano(entrada["titulo"], bool(fondo)),
        ancho=15 if fondo else 17,
        ancho_sub=48 if fondo else 62)

    os.makedirs(carpeta, exist_ok=True)
    temporal = os.path.join(carpeta, "_portada.html")
    with open(temporal, "w", encoding="utf-8") as f:
        f.write(doc)

    # Todo va embebido en base64, así que Chrome lee el archivo directo:
    # no hace falta servidor local, ni acá ni en GitHub Actions.
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2",
                    "--screenshot=" + crudo,
                    "--window-size=1200,630",
                    "--virtual-time-budget=6000",
                    "file://" + temporal],
                   capture_output=True)
    os.remove(temporal)
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
