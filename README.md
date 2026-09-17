# freaknerd.co

Sitio de una página de la consultoría Freaknerd. HTML, CSS y JavaScript planos,
sin framework ni proceso de compilación.

## Estructura

- `index.html` — la página completa (estilos y script en línea)
- `tokens.css` — **activo de marca reutilizable**: color, tipografía fluida,
  espaciado y curvas de movimiento de la casa Freaknerd. Pensado para reusarse
  en otros proyectos, no solo aquí.
- `assets/logos/` — logos de clientes
- `assets/og.png` — tarjeta de compartir (1200×630)
- `mobile-harness.html` — iframe de 390 px para capturar móvil real.
  Chrome headless tiene un ancho mínimo de ventana (~485 px): pedirle
  `--window-size=390` recorta en vez de emular.

## Ver en local

    python3 -m http.server 4321 --directory .

## Publicación

GitHub Pages desde `main`, dominio propio en `CNAME`.
