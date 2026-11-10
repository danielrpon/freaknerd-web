#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera firma/index.html: las firmas de correo de freaknerd (manual de marca v1,
sección 11.4). Se generan, no se editan a mano: cuatro bloques casi idénticos
editados uno por uno terminan desalineados.

    python3 firma/generar.py

11.4: 600 px máx. Nombre en Montserrat 900 16 px azul, cargo en mono 11 azul
nota, datos de contacto COMO TEXTO, wordmark como imagen pequeña (120 px),
filete tinte. Sin campo de puntos ni naranja. Los clientes de correo no cargan
fuentes web: el nombre cae a Arial Black / Arial, que conserva el peso.
"""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://freaknerd.co"

AZUL, TEXTO2, NOTA, TINTE = "#09318D", "#4B5C8C", "#5A6B94", "#D8E0EE"
FONT = "Montserrat,'Arial Black',Arial,sans-serif"
MONO = "'JetBrains Mono',Menlo,Consolas,'Courier New',monospace"

FIRMAS = [
    dict(id="sig-1", etiqueta="DANIEL RESTREPO", titulo="1 · Daniel Restrepo",
         nombre="Daniel Restrepo", cargo="Estrategia / Analítica / Automatización",
         tel="+57 311 719 1394", wa="573117191394"),
    dict(id="sig-2", etiqueta="ANDRÉS ARDILA", titulo="2 · Andrés Ardila",
         nombre="Andrés Ardila", cargo="Operaciones / Procesos / Mejora continua",
         tel="+57 350 695 9144", wa="573506959144"),
    dict(id="sig-3", etiqueta="JOHN RESTREPO", titulo="3 · John Restrepo",
         nombre="John Restrepo", cargo="Dirección estratégica / Gobierno corporativo / Finanzas",
         tel="+57 311 719 1406", wa="573117191406"),
    dict(id="sig-4", etiqueta="INSTITUCIONAL", titulo="4 · Institucional",
         nombre="Estrategia que se vuelve estructura.", cargo="Consultoría de estrategia / Medellín",
         tel="+57 311 719 1394", wa="573117191394",
         nota="Para el buzón compartido, cuando no firma una persona en particular."),
]

REDES = [
    ("ig", "Instagram", "https://instagram.com/freaknerd.co", ""),
    ("li", "LinkedIn", "https://www.linkedin.com/in/daniel-restrepo-nunez/",
     "<!-- LinkedIn: hoy apunta a un perfil personal. Cuando exista la página de empresa, cambia esta URL en generar.py. -->"),
    ("x", "X", "https://x.com/freaknerd_co",
     "<!-- X: cuenta pendiente de crear. Si no la vas a abrir, quita su entrada de REDES en generar.py. -->"),
    ("tt", "TikTok", "https://www.tiktok.com/@freaknerd.co",
     "<!-- TikTok: cuenta pendiente de crear. Si no la vas a abrir, quita su entrada de REDES en generar.py. -->"),
]


def redes():
    celdas = []
    for i, (k, nombre, url, comentario) in enumerate(REDES):
        pad = "padding-right:12px;" if i < len(REDES) - 1 else ""
        pre = comentario + "\n          " if comentario else ""
        celdas.append('          %s<td style="%s"><a href="%s"><img src="%s/assets/social/%s.png" width="18" height="18" alt="%s" style="display:block;border:0;width:18px;height:18px;"></a></td>'
                      % (pre, pad, url, BASE, k, nombre))
    return "\n".join(celdas)


PLANTILLA_FIRMA = """
<!-- ========== FIRMA · {etiqueta} — copiar desde aquí ========== -->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;max-width:600px;font-family:Arial,Helvetica,sans-serif;">
  <tr>
    <td valign="top" style="padding:0;">
      <img src="{base}/assets/sig/wordmark.png" width="120" height="17" alt="freaknerd"
           style="display:block;border:0;width:120px;height:17px;">
      <div style="height:16px;line-height:16px;font-size:0;">&nbsp;</div>
      <div style="font-family:{font};font-size:16px;line-height:22px;font-weight:900;color:{azul};letter-spacing:-.02em;">{nombre}</div>
      <div style="font-family:{mono};font-size:11px;line-height:22px;color:{nota};letter-spacing:.14em;text-transform:uppercase;">{cargo}</div>
      <div style="height:11px;line-height:11px;font-size:0;">&nbsp;</div>
      <div style="border-top:1px solid {tinte};width:320px;font-size:0;line-height:0;">&nbsp;</div>
      <div style="height:11px;line-height:11px;font-size:0;">&nbsp;</div>
      <div style="font-size:13px;color:{texto2};line-height:22px;">
        <a href="mailto:contacto@freaknerd.co" style="color:{texto2};text-decoration:none;">contacto@freaknerd.co</a><br>
        <a href="https://wa.me/{wa}" style="color:{texto2};text-decoration:none;">{tel}</a><br>
        <a href="https://freaknerd.co" style="color:{azul};text-decoration:none;font-weight:700;">freaknerd.co</a>
      </div>
      <div style="height:11px;line-height:11px;font-size:0;">&nbsp;</div>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
        <tr>
{redes}
        </tr>
      </table>
    </td>
  </tr>
</table>
<!-- ========== FIRMA · {etiqueta} — hasta aquí ========== -->
"""


def firma(f):
    return PLANTILLA_FIRMA.format(base=BASE, font=FONT, mono=MONO, azul=AZUL, texto2=TEXTO2,
                                  nota=NOTA, tinte=TINTE, redes=redes(), **f)


CABEZA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Firmas de correo · freaknerd</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#FCFFFF">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700;900&family=JetBrains+Mono:wght@500&display=swap">
<style>
  *{box-sizing:border-box}
  body{margin:0;background:#FCFFFF;color:#09318D;
       font:500 16px/22px Montserrat,-apple-system,"Segoe UI",sans-serif;
       padding:44px 22px;}
  .page{max-width:760px;margin:0 auto;}
  h1{font-size:30px;line-height:33px;font-weight:900;margin:0 0 11px;letter-spacing:-.02em;}
  .lead{color:#4B5C8C;margin:0 0 44px;}
  h2{font:500 12px/22px "JetBrains Mono",ui-monospace,Menlo,monospace;text-transform:uppercase;
     letter-spacing:.14em;color:#4B5C8C;margin:0;}
  .hint{color:#4B5C8C;font-size:14px;margin:0 0 11px;}
  .box{background:#fff;border:1px dashed #D8E0EE;padding:22px;overflow-x:auto;}
  .head{display:flex;align-items:center;justify-content:space-between;gap:16px;margin:44px 0 11px;}
  /* min-width fijo: sin él el botón cambia de tamaño al cambiar la etiqueta. */
  .copy{font:500 11px/1 "JetBrains Mono",ui-monospace,Menlo,monospace;letter-spacing:.14em;
        text-transform:uppercase;color:#09318D;background:#FCFFFF;
        border:2px solid #09318D;border-radius:0;height:44px;padding:0 16px;
        cursor:pointer;min-width:148px;white-space:nowrap;
        transition:transform 140ms cubic-bezier(.2,.8,.2,1);}
  .copy:active{transform:scale(.98);}
  .copy:focus-visible{outline:2px solid #09318D;outline-offset:3px;}
  .copy[data-ok="true"]{background:#09318D;color:#FCFFFF;}
  .copy[data-ok="false"]{border-color:#C23A00;color:#C23A00;}
  @media (prefers-reduced-motion:reduce){.copy:active{transform:none;}}
  ol{color:#4B5C8C;font-size:15px;padding-left:22px;}
  ol b{color:#09318D;}
  code{background:#D8E0EE;padding:2px 6px;font-size:14px;color:#09318D;}
</style>
</head>
<body>
<div class="page">

  <h1>Firmas de correo · freaknerd</h1>
  <p class="lead">Selecciona el contenido de un recuadro completo, cópialo y pégalo
     en tu cliente de correo. No copies el recuadro punteado: es solo el borde de esta página.
     Los tres consultores comparten <b>contacto@freaknerd.co</b> y se distinguen por el teléfono.</p>
"""

INSTRUCCIONES = r"""  <h2>Cómo instalarla</h2>
  <ol>
    <li><b>Gmail:</b> Configuración → Ver toda la configuración → General → Firma → Crear.
        Pega dentro del editor y asóciala a <code>contacto@freaknerd.co</code>.</li>
    <li><b>iPhone:</b> Ajustes → Aplicaciones → Mail → Firma. El editor del iPhone no
        conserva el formato al pegar: mejor configúrala desde el computador si usas
        la misma cuenta en ambos.</li>
    <li><b>Titan / GoDaddy:</b> Configuración → Firma → pega en el editor enriquecido.</li>
  </ol>

  <h2>Antes de usarlas</h2>
  <ol>
    <li>Las cuentas de <b>X</b> y <b>TikTok</b> todavía no existen: esos dos íconos
        apuntan a URLs que hoy no cargan. Créalas o borra esas dos celdas del HTML
        (están marcadas con comentarios).</li>
    <li>El ícono de <b>LinkedIn</b> lleva a un perfil personal porque la página de
        empresa aún no existe. Cuando la crees, cambia esa sola URL en las cuatro firmas.</li>
    <li>Mientras el correo sea compartido, quien responda debería <b>firmar con su
        propia firma</b>: es lo único que le dice al cliente con quién está hablando.</li>
    <li>Muchos clientes <b>bloquean imágenes</b> hasta que el destinatario las acepta.
        Por eso todos los datos de contacto son texto, no parte del logo:
        aunque no cargue una sola imagen, la firma sigue siendo legible y clicable.</li>
  </ol>

"""

SCRIPT = r"""<script>
(function () {
  var ETIQUETA = 'Copiar firma';

  function limpiar(html) {
    // Los comentarios guían a quien edita el archivo, no tienen por qué
    // viajar dentro de la firma de cada correo que se envíe.
    return html.replace(/<!--[\s\S]*?-->/g, '').trim();
  }

  async function copiar(caja) {
    var html = limpiar(caja.innerHTML);
    var texto = caja.innerText.trim();
    // La firma tiene que llegar CON formato: si solo se copia texto plano,
    // al pegarla en Gmail aparece el código fuente en vez de la firma.
    if (navigator.clipboard && window.ClipboardItem && window.isSecureContext) {
      try {
        await navigator.clipboard.write([new ClipboardItem({
          'text/html':  new Blob([html],  { type: 'text/html'  }),
          'text/plain': new Blob([texto], { type: 'text/plain' })
        })]);
        return true;
      } catch (e) { /* cae al respaldo */ }
    }
    // Respaldo para navegadores viejos: seleccionar el nodo y copiar.
    try {
      var sel = window.getSelection(), rango = document.createRange();
      rango.selectNodeContents(caja);
      sel.removeAllRanges(); sel.addRange(rango);
      var ok = document.execCommand('copy');
      sel.removeAllRanges();
      return ok;
    } catch (e) { return false; }
  }

  document.querySelectorAll('.copy').forEach(function (btn) {
    btn.addEventListener('click', async function () {
      var caja = document.getElementById(btn.getAttribute('data-sig'));
      if (!caja) return;
      var ok = await copiar(caja);
      btn.textContent = ok ? 'Copiado ✓' : 'Selecciónala a mano';
      btn.setAttribute('data-ok', String(ok));
      clearTimeout(btn._t);
      btn._t = setTimeout(function () {
        btn.textContent = ETIQUETA;
        btn.removeAttribute('data-ok');
      }, 2200);
    });
  });
})();
</script>"""


def main():
    partes = [CABEZA]
    for f in FIRMAS:
        partes.append('\n  <div class="head">\n    <h2>%s</h2>\n    <button class="copy" type="button" data-sig="%s" aria-live="polite">Copiar firma</button>\n  </div>\n'
                      % (f["titulo"], f["id"]))
        if f.get("nota"):
            partes.append('  <p class="hint">%s</p>\n' % f["nota"])
        partes.append('  <div class="box" id="%s">\n%s\n  </div>\n' % (f["id"], firma({k: v for k, v in f.items() if k not in ("id", "titulo", "nota")})))
    partes.append(INSTRUCCIONES)
    partes.append("</div>\n\n" + SCRIPT + "\n</body>\n</html>\n")
    with open(os.path.join(RAIZ, "firma", "index.html"), "w", encoding="utf-8") as fh:
        fh.write("".join(partes))
    print("firma/index.html: %d firmas" % len(FIRMAS))


if __name__ == "__main__":
    main()
