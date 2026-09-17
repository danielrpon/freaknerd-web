#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae las entradas desde Notion y escribe blog/contenido.json.

Este es el paso que vuelve el blog autónomo: sin esto hay que pedirle a Claude
que lea Notion. Con esto, escribir en Notion y poner Estado = Publicado basta.

Necesita un token de integración de Notion en la variable NOTION_TOKEN.
Sin dependencias: usa urllib.

    export NOTION_TOKEN='ntn_...'
    python3 blog/sincronizar.py
"""
import json, os, sys, urllib.request, urllib.error

BASE_DATOS = "0e68c9bb-9ba5-4f8e-9ac6-061577b69654"
VERSION = "2022-06-28"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN = os.environ.get("NOTION_TOKEN")
if not TOKEN:
    sys.exit("Falta NOTION_TOKEN. Es el token de la integración de Notion, "
             "no se guarda en el repositorio.")


def api(ruta, metodo="GET", cuerpo=None):
    req = urllib.request.Request(
        "https://api.notion.com/v1" + ruta, method=metodo,
        data=json.dumps(cuerpo).encode() if cuerpo else None,
        headers={"Authorization": "Bearer " + TOKEN,
                 "Notion-Version": VERSION,
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("Notion respondió %s en %s:\n%s" % (e.code, ruta, e.read().decode()[:400]))


# ---------- texto enriquecido -> markdown ----------

def texto(rich):
    salida = []
    for t in rich:
        s = t.get("plain_text", "")
        a = t.get("annotations", {})
        if a.get("code"):      s = "`%s`" % s
        if a.get("bold"):      s = "**%s**" % s
        if a.get("italic"):    s = "*%s*" % s
        if t.get("href"):      s = "[%s](%s)" % (s, t["href"])
        salida.append(s)
    return "".join(salida)


def bloques_a_md(page_id):
    lineas, cursor = [], None
    while True:
        ruta = "/blocks/%s/children?page_size=100" % page_id
        if cursor:
            ruta += "&start_cursor=" + cursor
        datos = api(ruta)
        for b in datos["results"]:
            t = b["type"]
            if t == "divider":
                continue
            contenido = b.get(t, {})
            rich = contenido.get("rich_text", [])
            cuerpo = texto(rich)
            if not cuerpo and t != "divider":
                continue
            if   t == "heading_1":          lineas.append("## " + cuerpo)   # h1 lo pone el sitio
            elif t == "heading_2":          lineas.append("## " + cuerpo)
            elif t == "heading_3":          lineas.append("### " + cuerpo)
            elif t == "bulleted_list_item": lineas.append("- " + cuerpo)
            elif t == "numbered_list_item": lineas.append("- " + cuerpo)
            elif t == "quote":              lineas.append("> " + cuerpo)
            elif t == "code":               lineas.append(cuerpo)
            else:                           lineas.append(cuerpo)
        if not datos.get("has_more"):
            break
        cursor = datos["next_cursor"]
    return "\n".join(lineas)


def valor(props, nombre):
    p = props.get(nombre)
    if not p:
        return None
    t = p["type"]
    if t == "title":     return texto(p["title"])
    if t == "rich_text": return texto(p["rich_text"])
    if t == "select":    return (p["select"] or {}).get("name")
    if t == "date":      return (p["date"] or {}).get("start")
    if t == "url":       return p["url"]
    if t == "last_edited_time": return p["last_edited_time"]
    return None


def main():
    entradas, cursor = [], None
    while True:
        cuerpo = {"page_size": 100}
        if cursor:
            cuerpo["start_cursor"] = cursor
        datos = api("/databases/%s/query" % BASE_DATOS, "POST", cuerpo)
        for pg in datos["results"]:
            props = pg["properties"]
            estado = valor(props, "Estado")
            if estado != "Publicado":
                continue
            slug, fecha = valor(props, "Slug"), valor(props, "Fecha")
            titulo = valor(props, "Título")
            if not slug or not fecha:
                print("  omitida (sin slug o sin fecha): %s" % titulo)
                continue
            entradas.append({
                "notion_id": pg["id"],
                "titulo": titulo,
                "slug": slug.strip(),
                "estado": estado,
                "fecha": fecha[:10],
                "actualizado": (valor(props, "Actualizado") or fecha)[:10],
                "descripcion": valor(props, "Descripción") or "",
                "categoria": valor(props, "Categoría") or "",
                "autor": valor(props, "Autor") or "freaknerd",
                "imagen": valor(props, "Imagen") or "",
                "cuerpo": bloques_a_md(pg["id"]),
            })
        if not datos.get("has_more"):
            break
        cursor = datos["next_cursor"]

    entradas.sort(key=lambda e: e["fecha"], reverse=True)
    salida = {
        "_origen": "Notion · base 'Blog · freaknerd.co'. Lo escribe blog/sincronizar.py.",
        "_sincronizado": __import__("datetime").date.today().isoformat(),
        "entradas": entradas,
    }
    destino = os.path.join(RAIZ, "blog", "contenido.json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print("%d entrada(s) publicada(s): %s" % (len(entradas), ", ".join(e["slug"] for e in entradas)))


if __name__ == "__main__":
    main()
