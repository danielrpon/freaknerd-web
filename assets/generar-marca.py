#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenera los activos gráficos de la marca v2.1 (manual de marca 10-nov-2026):

  favicon.svg, assets/favicon-32.png, assets/favicon-16.png, favicon.ico,
  assets/apple-touch-icon.png, assets/icon-192.png, assets/icon-512.png,
  assets/icon-32.png, assets/icon-16.png, assets/og.png,
  assets/wordmark.svg, assets/wordmark-crema.svg, assets/sig/wordmark.png

    python3 assets/generar-marca.py

Medidas del manual: 3.1 (ícono fn en celda, tirador 0,11 del lado desplazado
0,06 hacia afuera con aro de 0,025; letras 0,54 del lado, tracking -0,05 em,
subidas 3 %), 3.2 (wordmark con tirador de 0,20 em a 0,06 em) y 7.6 (campo de
puntos con los ordenados en los vértices de la retícula). Chrome renderiza los
PNG; las fuentes salen de assets/fonts, sin red.
"""
import math, os, random, shutil, struct, subprocess, sys, tempfile
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, "assets", "fonts")

PIEDRA, PIZARRA, CREMA, NARANJA, AZUL = "#656A66", "#2C312E", "#F4EFE6", "#FF4A1C", "#2E4FA6"


def _chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/usr/bin/google-chrome", "/usr/bin/chromium-browser", "/usr/bin/chromium"):
        if os.path.exists(c):
            return c
    r = shutil.which("google-chrome") or shutil.which("chromium")
    if r:
        return r
    sys.exit("No encontré Chrome. Define la variable CHROME con su ruta.")


# ---------- glifos de Montserrat Black como trazos ----------
_FONT = TTFont(os.path.join(FUENTES, "Montserrat-900.ttf"))
_GS = _FONT.getGlyphSet()
_CMAP = _FONT.getBestCmap()


def texto_trazo(txt, size, tracking_em=0.0, tracking_px=0.0):
    """Devuelve (d, ancho, ymin, ymax): trazo SVG con la línea base en y=0, hacia arriba negativo."""
    s = size / _FONT["head"].unitsPerEm
    x = 0.0
    partes = []
    xmin, xmax, ymin, ymax = 1e9, -1e9, 1e9, -1e9
    for ch in txt:
        g = _CMAP[ord(ch)]
        pen = SVGPathPen(_GS)
        tp = TransformPen(pen, (s, 0, 0, -s, x, 0))
        _GS[g].draw(tp)
        partes.append(pen.getCommands())
        bp = BoundsPen(_GS)
        _GS[g].draw(bp)
        if bp.bounds:
            a, b, c, d = bp.bounds
            xmin, xmax = min(xmin, x + a * s), max(xmax, x + c * s)
            ymin, ymax = min(ymin, -d * s), max(ymax, -b * s)
        x += _GS[g].width * s + tracking_em * size + tracking_px
    return "".join(partes), (xmin, xmax, ymin, ymax)


def fn_en_celda(x, y, lado, fondo, texto="fn", tirador=True, tir_lado=None, tir_afuera=None, aro=None,
                size=None, tracking_em=-0.05, tracking_px=0.0, sube=0.03):
    """Celda naranja con las letras crema centradas ópticamente (subidas 3 % del alto) y el tirador crema."""
    size = size or lado * 0.54
    d, (x0, x1, y0, y1) = texto_trazo(texto, size, tracking_em, tracking_px)
    tx = x + (lado - (x1 - x0)) / 2 - x0
    ty = y + (lado - (y1 - y0)) / 2 - y0 - lado * sube
    out = '<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x, y, lado, lado, NARANJA)
    out += '<path transform="translate(%.3f %.3f)" d="%s" fill="%s"/>' % (tx, ty, d, CREMA)
    if tirador:
        t = tir_lado if tir_lado is not None else lado * 0.11
        f = tir_afuera if tir_afuera is not None else lado * 0.06
        a = aro if aro is not None else lado * 0.025
        tx0, ty0 = x + lado + f - t, y + lado + f - t
        if a:
            out += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="%s"/>' % (tx0 - a, ty0 - a, t + 2 * a, t + 2 * a, fondo)
        out += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="%s"/>' % (tx0, ty0, t, t, CREMA)
    return out


def svg(w, h, cuerpo, vb=None):
    vb = vb or "0 0 %g %g" % (w, h)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" width="%g" height="%g">%s</svg>' % (vb, w, h, cuerpo))


# ---------- íconos ----------
def favicon32():
    # celda sólida 32x32; fn Montserrat Black 17 px, tracking -1 px; tirador crema 6x6 en la esquina
    c = fn_en_celda(0, 0, 32, NARANJA, size=17, tracking_em=0, tracking_px=-1, tirador=False, sube=0.03)
    c += '<rect x="26" y="26" width="6" height="6" fill="%s"/>' % CREMA
    return svg(32, 32, c)


def favicon16():
    # a 16 px, solo la n (Black 11 px); tirador de 3 px
    c = fn_en_celda(0, 0, 16, NARANJA, texto="n", size=11, tracking_em=0, tirador=False, sube=0.03)
    c += '<rect x="13" y="13" width="3" height="3" fill="%s"/>' % CREMA
    return svg(16, 16, c)


def perfil():
    """Ícono de perfil (3.1): lienzo piedra con retícula de 60, celda fn de 120 centrada que cabe en
    el círculo inscrito y un cuadrito con borde azul arriba a la derecha."""
    g = ""
    for k in range(4):
        v = 30 + 60 * k
        g += "M%g 0V240M0 %gH240" % (v + .5, v + .5)
    c = '<rect width="240" height="240" fill="%s"/>' % PIEDRA
    c += '<path d="%s" fill="none" stroke="%s" stroke-opacity=".20" stroke-width="1"/>' % (g, CREMA)
    c += fn_en_celda(60, 60, 120, PIEDRA)
    c += '<rect x="181" y="31" width="28" height="28" fill="none" stroke="%s" stroke-width="2"/>' % AZUL
    return svg(240, 240, c)


# ---------- wordmark ----------
def wordmark(color):
    d, (x0, x1, y0, y1) = texto_trazo("freaknerd", 1000, tracking_em=-0.035)
    ancho = x1 - x0
    # el tirador de 0,20 em apoyado en la línea base, a 0,06 em del último glifo
    tx = x1 + 60
    cuerpo = '<path d="%s" fill="%s"/><rect x="%.1f" y="-200" width="200" height="200" fill="%s"/>' % (d, color, tx, NARANJA)
    vb = "%.0f %.0f %.0f %.0f" % (x0, y0, tx + 200 - x0, -y0)
    ww = (tx + 200 - x0) / 10
    return svg(ww, -y0 / 10, cuerpo, vb=vb)


# ---------- campo de puntos en los vértices (7.6) ----------
def _sm(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def puntos(w, h, step, gx, gy, left, top, seed=3, color=CREMA, vivos=2, r=3.0):
    """Caja (left, top, w, h); retícula con origen (gx, gy). Ordenados = vértices exactos (derecha);
    hacia la izquierda se sueltan dentro de las celdas vecinas, más 1-2 puntos extra por celda."""
    rnd = random.Random(seed)
    i0 = math.ceil((left - gx) / step - 1e-9)
    i1 = math.floor((left + w - gx) / step + 1e-9)
    j0 = math.ceil((top - gy) / step - 1e-9)
    j1 = math.floor((top + h - gy) / step + 1e-9)

    def dis_at(X, Y):
        t = (X - left) / w
        t = max(0.0, min(1.0, t / 0.7))
        return 1.0 - t

    out, cand = [], []

    def put(x, y, rr, op):
        if -0.5 <= x <= w + 0.5 and -0.5 <= y <= h + 0.5:
            out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="%.2f"/>' % (x + left + .5, y + top + .5, rr, color, op))

    for i in range(i0, i1 + 1):
        for j in range(j0, j1 + 1):
            X, Y = gx + i * step, gy + j * step
            dis = dis_at(X, Y)
            s = _sm(dis)
            dx = (rnd.random() * 2 - 1) * .9 * step * s
            dy = (rnd.random() * 2 - 1) * .9 * step * s
            put(X - left + dx, Y - top + dy, r, .95)
            if dis <= 0.05 and (X - left) / w > .55:
                cand.append((X, Y))
    for i in range(i0 - 1, i1 + 1):
        for j in range(j0 - 1, j1 + 1):
            cx, cy = gx + (i + .5) * step, gy + (j + .5) * step
            dis = dis_at(cx, cy)
            k = _sm(dis * 1.25 - .05)
            if k <= 0:
                continue
            for _ in range(1 if rnd.random() < .5 else 2):
                if rnd.random() < k:
                    put(gx + (i + rnd.random()) * step - left, gy + (j + rnd.random()) * step - top, r * .8, .25 + .45 * dis)
    sz = r * 8 / 3
    if cand and vivos:
        for X, Y in [cand[int(len(cand) * .35)], cand[int(len(cand) * .8)]][:vivos]:
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (X - sz / 2 + .5, Y - sz / 2 + .5, sz, sz, NARANJA))
    return "".join(out)


def reticula(w, h, step, ox, oy, color=CREMA, op=.20):
    d = ""
    x = ox % step
    while x <= w:
        d += "M%g 0V%g" % (x + .5, h)
        x += step
    y = oy % step
    while y <= h:
        d += "M0 %gH%g" % (y + .5, w)
        y += step
    return '<path d="%s" fill="none" stroke="%s" stroke-opacity="%.2f" stroke-width="1"/>' % (d, color, op)


def og_html():
    W, H, S = 1200, 630, 66
    oy = 33                                   # 33 + 66 k: simétrica arriba y abajo
    cuerpo = reticula(W, H, S, 0, oy)
    cuerpo += puntos(W - 792, H, S, 0, oy, 792, 0, seed=11)
    cuerpo += fn_en_celda(66, 99, 132, PIEDRA)
    cuerpo += '<rect x="199" y="100" width="130" height="130" fill="none" stroke="%s" stroke-width="2"/>' % NARANJA
    figura = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" style="position:absolute;left:0;top:0">%s</svg>' % (W, H, cuerpo)
    f = FUENTES.replace("\\", "/")
    return """<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><style>
@font-face{font-family:Montserrat;font-weight:900;src:url('%(f)s/Montserrat-900.ttf')}
@font-face{font-family:Montserrat;font-weight:500;src:url('%(f)s/Montserrat-500.ttf')}
@font-face{font-family:'JetBrains Mono';font-weight:500;src:url('%(f)s/JetBrainsMono-500.ttf')}
*{margin:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden;background:%(p)s}
body{position:relative;color:%(c)s;font-family:Montserrat}
h1{position:absolute;left:66px;top:308px;width:700px;font:900 64px/66px Montserrat;letter-spacing:-.035em}
h1 b{color:%(n)s;font-weight:900}
.wm{position:absolute;left:66px;top:528px;font:900 36px/44px Montserrat;letter-spacing:-.035em;display:inline-flex;align-items:baseline;height:44px}
.wm i{display:inline-block;width:.2em;height:.2em;background:%(n)s;margin-left:.06em}
.mono{position:absolute;font:500 12px/22px 'JetBrains Mono';letter-spacing:.14em;text-transform:uppercase;white-space:nowrap}
</style></head><body>%(fig)s
<h1>Estrategia que se vuelve <b>estructura</b></h1>
<div class="wm">freaknerd<i></i></div>
<div class="mono" style="left:792px;top:588px">&larr; Así llega · Así queda &rarr;</div>
<div class="mono" style="left:66px;top:264px">Consultoría de estrategia · Medellín</div>
</body></html>""" % dict(f=f, p=PIEDRA, c=CREMA, n=NARANJA, fig=figura)


# ---------- render ----------
CHROME = None


def render(html, ancho, alto, destino, transparente=False):
    """Chrome headless; la ventana no baja de ~500 px de ancho, así que se recorta."""
    global CHROME
    CHROME = CHROME or _chrome()
    tmp = tempfile.mkdtemp()
    ph = os.path.join(tmp, "p.html")
    with open(ph, "w", encoding="utf-8") as fh:
        fh.write(html)
    crudo = os.path.join(tmp, "p.png")
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
           "--force-device-scale-factor=1", "--virtual-time-budget=4000",
           "--window-size=%d,%d" % (max(ancho, 600), max(alto, 400)), "--screenshot=" + crudo]
    if transparente:
        cmd.append("--default-background-color=00000000")
    subprocess.run(cmd + ["file://" + ph], capture_output=True)
    im = Image.open(crudo).convert("RGBA" if transparente else "RGB").crop((0, 0, ancho, alto))
    im.save(destino, optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)


def png_de_svg(texto_svg, n, destino, transparente=False):
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{margin:0}html,body{background:%s}'
            'svg{display:block;width:%dpx;height:%dpx}</style></head><body>%s</body></html>'
            % ("transparent" if transparente else "#fff", n, n, texto_svg))
    render(html, n, n, destino, transparente)


def escribir(ruta, texto):
    with open(os.path.join(RAIZ, ruta), "w", encoding="utf-8") as fh:
        fh.write(texto)


def ico(entradas, destino):
    """favicon.ico a mano: cada tamaño es su propio PNG (16 con la n, 32 con fn)."""
    datos = []
    for p in entradas:
        with open(p, "rb") as fh:
            datos.append(fh.read())
    cab = struct.pack("<HHH", 0, 1, len(datos))
    off = 6 + 16 * len(datos)
    dire, cuerpo = b"", b""
    for p, d in zip(entradas, datos):
        w, h = Image.open(p).size
        dire += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(d), off + len(cuerpo))
        cuerpo += d
    with open(destino, "wb") as fh:
        fh.write(cab + dire + cuerpo)


def main():
    A = lambda *p: os.path.join(RAIZ, "assets", *p)
    f32, f16, pf = favicon32(), favicon16(), perfil()
    escribir("favicon.svg", f32)
    png_de_svg(f32, 32, A("favicon-32.png"))
    png_de_svg(f16, 16, A("favicon-16.png"))
    shutil.copy(A("favicon-32.png"), A("icon-32.png"))
    shutil.copy(A("favicon-16.png"), A("icon-16.png"))
    ico([A("favicon-16.png"), A("favicon-32.png")], os.path.join(RAIZ, "favicon.ico"))
    for n, nombre in ((180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        png_de_svg(pf, n, A(nombre))
    render(og_html(), 1200, 630, A("og.png"))
    escribir("assets/wordmark.svg", wordmark(PIZARRA))
    escribir("assets/wordmark-crema.svg", wordmark(CREMA))
    # firma de correo: wordmark pizarra con tirador naranja, 480x68 sobre transparente
    w = wordmark(PIZARRA).replace('width="', 'data-w="', 1)
    html = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{margin:0}html,body{background:transparent}'
            'svg{display:block;width:480px;height:auto}</style></head><body>%s</body></html>' % w)
    render(html, 480, 68, A("sig", "wordmark.png"), transparente=True)
    print("listo")


if __name__ == "__main__":
    main()
