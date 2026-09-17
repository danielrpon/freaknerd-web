#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el blog de freaknerd.co a partir de blog/contenido.json.

El JSON es el puente con Notion: hoy lo llena Claude leyendo la base por el
conector; mañana lo puede llenar un script con un token de la API de Notion
sin cambiar nada de aquí. El generador nunca habla con Notion directamente.

Solo salen las entradas con estado "Publicado".

    python3 blog/generar.py            # solo publicadas
    python3 blog/generar.py --todas    # incluye borradores, para revisar en local
"""
import json, os, re, sys, html, datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://freaknerd.co"
MESES = ["enero","febrero","marzo","abril","mayo","junio",
         "julio","agosto","septiembre","octubre","noviembre","diciembre"]


# ---------- Markdown mínimo ----------
# El repositorio no tiene dependencias y no vale la pena estrenar una por
# esto: el contenido que llega de Notion usa encabezados, párrafos, negrita,
# cursiva y enlaces. Nada más.

def en_linea(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', t)
    return t

def a_html(md):
    salida = []
    for linea in md.split("\n"):
        l = linea.strip()
        if not l:
            continue
        if l.startswith("### "):
            salida.append("<h3>%s</h3>" % en_linea(l[4:]))
        elif l.startswith("## "):
            salida.append("<h2>%s</h2>" % en_linea(l[3:]))
        elif l.startswith("> "):
            salida.append("<blockquote><p>%s</p></blockquote>" % en_linea(l[2:]))
        elif l.startswith("|") and l.endswith("|"):
            salida.append(("TR", [c.strip() for c in l.strip("|").split("|")]))
        elif re.match(r'^[-*] ', l):
            salida.append(("LI", en_linea(l[2:])))
        else:
            salida.append("<p>%s</p>" % en_linea(l))
    # agrupa los sueltos: <li> en listas, filas en tablas
    final, lista, tabla = [], [], []

    def cerrar():
        if lista:
            final.append("<ul>%s</ul>" % "".join(lista)); lista.clear()
        if tabla:
            final.append(armar_tabla(tabla)); tabla.clear()

    for b in salida:
        if isinstance(b, tuple) and b[0] == "LI":
            if tabla: cerrar()
            lista.append("<li>%s</li>" % b[1])
        elif isinstance(b, tuple) and b[0] == "TR":
            if lista: cerrar()
            tabla.append(b[1])
        else:
            cerrar(); final.append(b)
    cerrar()
    return "\n      ".join(final)


def armar_tabla(filas):
    """La fila de guiones que separa el encabezado no se pinta: solo marca
    que la primera fila es encabezado."""
    def es_separador(f):
        return all(re.fullmatch(r':?-{2,}:?', c) for c in f if c)

    cuerpo = [f for f in filas if not es_separador(f)]
    if not cuerpo:
        return ""
    con_encabezado = len(filas) > 1 and es_separador(filas[1])
    partes = ["<table>"]
    if con_encabezado:
        partes.append("<thead><tr>%s</tr></thead>"
                      % "".join("<th>%s</th>" % en_linea(c) for c in cuerpo[0]))
        cuerpo = cuerpo[1:]
    partes.append("<tbody>")
    for f in cuerpo:
        partes.append("<tr>%s</tr>" % "".join("<td>%s</td>" % en_linea(c) for c in f))
    partes.append("</tbody></table>")
    return "".join(partes)


def fecha_larga(iso):
    d = datetime.date.fromisoformat(iso)
    return "%d de %s de %d" % (d.day, MESES[d.month - 1], d.year)

def minutos(md):
    return max(1, round(len(md.split()) / 200))


# ---------- Plantillas ----------

CABEZA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtipo}">
<meta property="og:site_name" content="freaknerd">
<meta property="og:locale" content="es_CO">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{imagen}">
<meta property="og:image:width" content="2400">
<meta property="og:image:height" content="1260">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0A0B0D">
<link rel="alternate" type="application/rss+xml" title="freaknerd" href="/blog/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/tokens.css">
{extra}<link rel="stylesheet" href="/blog/blog.css">
</head>
<body>
<header class="wrap topbar">
  <a class="wordmark" href="/">freaknerd<i>_</i></a>
  <nav><a class="nav" href="/blog/">Blog</a><a class="nav" href="/#contacto">Contacto</a></nav>
</header>
"""

PIE = """<footer class="wrap">
  <span><a href="/">freaknerd_</a></span>
  <span class="foot-links">
    <a href="/blog/feed.xml">RSS</a>
    <a href="https://instagram.com/freaknerd.co" target="_blank" rel="noopener noreferrer">@freaknerd.co</a>
    <a href="mailto:contacto@freaknerd.co">contacto@freaknerd.co</a>
  </span>
</footer>
</body>
</html>
"""


def bloque_visual(e):
    """La portada, dentro del artículo.

    Es el mismo archivo que sirve de tarjeta de compartir. Se muestra acá igual
    que en Propiman: una sola pieza en vez de dos tratamientos parecidos."""
    return """  <div class="post-visual">
    <div class="wrap">
      <img class="visual" src="/blog/{slug}/portada.jpg" alt=""
           width="2400" height="1260" loading="lazy">
    </div>
  </div>""".format(slug=e["slug"])


def pagina_entrada(e):
    url = "%s/blog/%s/" % (BASE, e["slug"])
    portada = "%s/blog/%s/portada.jpg" % (BASE, e["slug"])
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": e["titulo"], "description": e["descripcion"],
        "datePublished": e["fecha"], "dateModified": e.get("actualizado", e["fecha"])[:10],
        "author": {"@type": "Person", "name": e["autor"]},
        "publisher": {"@type": "Organization", "name": "freaknerd",
                      "logo": {"@type": "ImageObject", "url": BASE + "/assets/icon-512.png"}},
        "mainEntityOfPage": url, "image": portada,
        "inLanguage": "es-CO",
    }, ensure_ascii=False, indent=2)
    extra = '<script type="application/ld+json">\n%s\n</script>\n' % ld
    return (CABEZA.format(titulo=html.escape(e["titulo"] + " · freaknerd"),
                          desc=html.escape(e["descripcion"]), url=url, imagen=portada,
                          ogtipo="article", BASE=BASE, extra=extra)
        + """
<main class="post">
  <header class="post-head">
    <div class="wrap">
      <p class="kicker">{cat} · {fecha}</p>
      <h1>{titulo}</h1>
      <p class="lead dim">{desc}</p>
      <p class="meta">{autor} · {mins} min de lectura</p>
    </div>
  </header>

  {visual}

  <div class="post-body light">
    <div class="wrap">
      {cuerpo}
    </div>
  </div>

  <section class="post-cta">
    <div class="wrap">
      <h2>¿Esto le está pasando a tu operación?</h2>
      <p class="lead dim">La primera charla no se cobra.</p>
      <a class="btn" href="/#contacto">Hablemos del problema</a>
      <p class="volver"><a href="/blog/">← Todas las entradas</a></p>
    </div>
  </section>
</main>
""".format(cat=html.escape(e["categoria"]), fecha=fecha_larga(e["fecha"]),
           titulo=html.escape(e["titulo"]), desc=html.escape(e["descripcion"]),
           autor=html.escape(e["autor"]), mins=minutos(e["cuerpo"]),
           cuerpo=a_html(e["cuerpo"]), visual=bloque_visual(e), BASE=BASE)
        + PIE.format(BASE=BASE))


def pagina_indice(entradas):
    if entradas:
        tarjetas = "\n".join(
            """      <li class="card">
        <a href="/blog/{slug}/">
          <img class="thumb" src="/blog/{slug}/portada.jpg" alt="" loading="lazy" width="2400" height="1260">
          <div>
            <p class="kicker">{cat} · {fecha}</p>
            <h2>{titulo}</h2>
            <p class="dim">{desc}</p>
            <span class="mas">Leer →</span>
          </div>
        </a>
      </li>""".format(BASE=BASE, slug=e["slug"], cat=html.escape(e["categoria"]),
                      fecha=fecha_larga(e["fecha"]), titulo=html.escape(e["titulo"]),
                      desc=html.escape(e["descripcion"])) for e in entradas)
        lista = '<ul class="cards">\n%s\n    </ul>' % tarjetas
    else:
        lista = '<p class="dim">Todavía no hay entradas publicadas.</p>'

    return (CABEZA.format(titulo="Blog · freaknerd",
                          desc="Notas sobre estrategia, operaciones y datos para empresas medianas colombianas.",
                          url=BASE + "/blog/", ogtipo="website", BASE=BASE, extra="",
                          imagen=BASE + "/assets/og.png")
        + """
<main class="blog-index">
  <section>
    <div class="wrap">
      <p class="kicker">Blog</p>
      <h1>Lo que vemos adentro.</h1>
      <p class="lead dim">Notas cortas sobre estrategia, operaciones y datos.
      Escritas desde lo que nos encontramos en las empresas, no desde la teoría.</p>
      {lista}
    </div>
  </section>
</main>
""".format(lista=lista)
        + PIE.format(BASE=BASE))


def rss(entradas):
    items = []
    for e in entradas:
        url = "%s/blog/%s/" % (BASE, e["slug"])
        d = datetime.date.fromisoformat(e["fecha"])
        items.append("""    <item>
      <title>{t}</title>
      <link>{u}</link>
      <guid isPermaLink="true">{u}</guid>
      <description>{d}</description>
      <pubDate>{p}</pubDate>
    </item>""".format(t=html.escape(e["titulo"]), u=url,
                      d=html.escape(e["descripcion"]),
                      p=d.strftime("%a, %d %b %Y") + " 09:00:00 -0500"))
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>freaknerd</title>
  <link>{BASE}/blog/</link>
  <description>Notas sobre estrategia, operaciones y datos.</description>
  <language>es-co</language>
{items}
</channel></rss>
""".format(BASE=BASE, items="\n".join(items))


def sitemap(entradas):
    urls = ['  <url><loc>%s/</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>'
            % (BASE, datetime.date.today().isoformat())]
    if entradas:
        urls.append('  <url><loc>%s/blog/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>'
                    % (BASE, max(e["fecha"] for e in entradas)))
    for e in entradas:
        urls.append('  <url><loc>%s/blog/%s/</loc><lastmod>%s</lastmod><priority>0.7</priority></url>'
                    % (BASE, e["slug"], e.get("actualizado", e["fecha"])[:10]))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main():
    todas = "--todas" in sys.argv
    with open(os.path.join(RAIZ, "blog", "contenido.json"), encoding="utf-8") as f:
        datos = json.load(f)

    entradas = [e for e in datos["entradas"]
                if todas or e.get("estado") == "Publicado"]
    faltantes = [e["titulo"] for e in entradas if not e.get("slug") or not e.get("fecha")]
    if faltantes:
        sys.exit("Sin slug o sin fecha: " + ", ".join(faltantes))
    entradas.sort(key=lambda e: e["fecha"], reverse=True)

    for e in entradas:
        carpeta = os.path.join(RAIZ, "blog", e["slug"])
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
            f.write(pagina_entrada(e))

    for ruta, contenido in [("blog/index.html", pagina_indice(entradas)),
                            ("blog/feed.xml", rss(entradas)),
                            ("sitemap.xml", sitemap(entradas))]:
        with open(os.path.join(RAIZ, ruta), "w", encoding="utf-8") as f:
            f.write(contenido)

    print("%d entrada(s): %s" % (len(entradas), ", ".join(e["slug"] for e in entradas)))
    if todas:
        print("  (modo --todas: incluye borradores, no subir así)")


if __name__ == "__main__":
    main()
