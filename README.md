# freaknerd.co

Sitio de una página de la consultoría Freaknerd. HTML, CSS y JavaScript planos,
sin framework ni proceso de compilación.

## Estructura

- `index.html` — la página completa (estilos y script en línea)
- `tokens.css` — **activo de marca reutilizable** (manual de marca v1, 10-nov-2026):
  color, tipografía, retícula de 22 px y curvas de movimiento de la casa Freaknerd. Pensado para reusarse
  en otros proyectos, no solo aquí.
- `assets/logos/` — logos de clientes (`azul/`: versión en tinta azul que usa la página)
- `assets/fonts/` — Montserrat y JetBrains Mono locales (portadas del blog)
- `firma/generar.py` — genera `firma/index.html` (no editar a mano)
- `blog/generar.py`, `blog/portadas.py` — HTML y portadas del blog
- `assets/og.png` — tarjeta de compartir (1200×630)
- `mobile-harness.html` — iframe de 390 px para capturar móvil real.
  Chrome headless tiene un ancho mínimo de ventana (~485 px): pedirle
  `--window-size=390` recorta en vez de emular.

## Ver en local

    python3 -m http.server 4321 --directory .

## Publicación

GitHub Pages desde `main`, dominio propio en `CNAME`.
