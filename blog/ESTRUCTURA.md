# Cómo se escribe una entrada del blog

Referencia para escribir en la base de Notion **`Blog · freaknerd.co`**.
Adaptada de la estructura que usa el blog de Propiman, que está armada para
posicionar y funciona.

No es un formulario que haya que llenar entero. Es el orden en que Google y un
lector apurado esperan encontrar las cosas, y **cada pieza está acá porque hace
un trabajo**, no por completar.

---

## 1 · Los campos de Notion

| Campo | Qué es | Regla |
|---|---|---|
| **Título** | El H1 y lo que ve Google | Largo está bien. Mete la palabra clave y, si aplica, el año |
| **Slug** | La URL | Minúsculas, guiones, sin tildes ni eñes. Que se entienda leyéndolo |
| **Descripción** | La meta descripción | 140–160 caracteres. **Empieza con el dolor, no con la solución** |
| **Categoría** | Una de las cinco | Sale en la portada y en el índice |
| **Autor** | Quién firma | Define de quién es la voz |
| **Fecha** | Publicación | Sin ella no se publica |
| **Imagen** | Foto del tema | Opcional. Va de fondo en la portada |
| **Estado** | Borrador / En revisión / Publicado | Solo `Publicado` sale al sitio |

El **tiempo de lectura se calcula solo** y la **portada se genera sola**. No hay
que escribirlos.

### El título

Propiman usa títulos largos con la pregunta completa:

> *Asamblea virtual de propiedad horizontal en Colombia (2026): quórum, convocatoria y validez legal*

Funciona porque la gente busca así. Pero ojo con el equilibrio: el título también
va en la portada y en la barra del navegador. **Entre 55 y 70 caracteres** es la
zona donde Google no lo corta y la lámina no se ahoga.

### La descripción

Esta es la que más se descuida y la que más rinde. Es lo que Google muestra
debajo del título, y es lo que decide si hacen clic.

La fórmula de Propiman: **abre con el dolor en forma de pregunta, cierra con lo
que entrega el artículo.**

> ¿Asambleas sin quórum que se repiten y decisiones que se caen? Guía 2026 de
> asamblea virtual de PH: Ley 675, convocatoria y validez legal.

---

## 2 · La anatomía del cuerpo

### Abre con una escena, no con un contexto

Propiman abre así:

> Son las 7:00 p. m. del día de la asamblea ordinaria. El salón comunal está
> listo, el proyector encendido, el café servido… y solo llegaron 12 de 80
> propietarios. No hay quórum.

Eso es una escena. El lector se reconoce en tres segundos.

Lo contrario —*"En el entorno empresarial actual, la vigilancia regulatoria
cobra cada vez mayor relevancia"*— no lo lee nadie y no dice nada.

**Tres párrafos para arrancar:** la escena, lo que cuesta, y qué va a resolver
este texto.

### Tabla de contenido

Después de la apertura, una lista con enlaces a cada sección.

Hace dos trabajos: le da al lector apurado un mapa, y le da a Google la
estructura en bandeja — de ahí salen los enlaces de salto que aparecen a veces
debajo de un resultado.

```markdown
## Tabla de contenido

- [¿Por qué pasa siempre?](#por-que-pasa-siempre)
- [Qué hacer el lunes](#que-hacer-el-lunes)
```

El ancla es el encabezado en minúsculas, sin tildes, con guiones.

### Los H2 son preguntas

No *"Contexto"*, no *"Antecedentes"*, no *"Consideraciones finales"*. Preguntas
que alguien escribiría en Google:

> ¿Es legal la asamblea virtual en Colombia?
> ¿Quién firma y quién custodia el acta?
> ¿Qué diferencia hay entre preventivo y correctivo?

Google levanta estos encabezados para la caja de *Otras preguntas también*. Un
subtítulo que dice "Contexto" no lo levanta nadie.

### Respuesta rápida

Justo después de una pregunta importante, una cita corta que la conteste en dos
líneas:

```markdown
> **Respuesta rápida:** La validez del acta descansa en la firma del presidente
> y el secretario. La custodia corresponde al administrador.
```

Es lo que Google copia textual al fragmento destacado. Si la respuesta está
enterrada en el tercer párrafo, no la encuentra.

### Tablas para lo que se compara

Responsabilidades, opciones, antes y después. Una tabla se lee en dos segundos
y el mismo contenido en prosa toma dos párrafos.

### En resumen

Antes de cerrar, los puntos en viñetas. Y después, **la tesis en una sola
línea**, en cita:

> **La tesis:** un edificio no se cae por una falla; se cae por una falla que
> nadie previó ni registró.

Esa frase es la que la gente reenvía.

### Preguntas frecuentes

Cuatro o cinco, cada una en negrita con su respuesta corta debajo. Alimentan
directo la caja de *Otras preguntas* y capturan búsquedas de cola larga que el
cuerpo no alcanza.

### El cierre

Una cita con la invitación y el enlace:

```markdown
> **¿Esto le está pasando a tu operación?** La primera charla no se cobra.
> 👉 [Cuéntanos qué se está rompiendo → freaknerd.co](https://freaknerd.co/#contacto)
```

---

## 3 · Lo que cambia respecto de Propiman

**Ellos citan normas; nosotros citamos operaciones.** Su autoridad viene de la
Ley 675. La nuestra viene de haber estado adentro. Donde ellos ponen *"art. 51,
Ley 675"*, nosotros ponemos una cifra, un caso o un plazo real.

**Nada de aviso legal al final.** Propiman lo necesita porque habla de derecho.
Si alguna entrada toca terreno legal o financiero, se pone una línea; si no,
sobra.

**El CTA no es una demo.** No vendemos software. Se invita a una conversación.

**Y el tic del sitio también aplica acá:** la construcción *"no es X, es Y"* es
potente una vez y muletilla a la tercera. Lo mismo con "capacidad instalada",
"mover la aguja" y los adjetivos de relleno.

---

## 4 · Qué soporta el formato

El conversor entiende:

- Encabezados `##` y `###`
- Párrafos, **negrita**, *cursiva*, [enlaces](https://freaknerd.co)
- Listas con `-`
- Citas con `>`
- **Tablas** con `|`

No entiende columnas, incrustados ni bloques desplegables de Notion: eso se
pierde en el sitio.

---

## 5 · El esqueleto, para copiar

```markdown
[Escena concreta: alguien, un momento, un número.]

[Qué cuesta cuando pasa eso.]

[Qué resuelve este texto.]

## Tabla de contenido

- [Primera pregunta](#primera-pregunta)
- [Segunda pregunta](#segunda-pregunta)
- [Qué hacer el lunes](#que-hacer-el-lunes)

## ¿Primera pregunta?

> **Respuesta rápida:** [dos líneas que contesten de una]

[Desarrollo.]

## ¿Segunda pregunta?

[Desarrollo. Tabla si hay algo que comparar.]

## Qué hacer el lunes

**[Verbo en imperativo.]** [Una línea.]

**[Verbo en imperativo.]** [Una línea.]

## En resumen

- [Punto]
- [Punto]

> **La tesis:** [una línea que alguien quiera reenviar]

## Preguntas frecuentes

**¿[Pregunta]?**
[Respuesta corta.]

**¿[Pregunta]?**
[Respuesta corta.]

> **¿Esto le está pasando a tu operación?** La primera charla no se cobra.
> 👉 [Cuéntanos qué se está rompiendo → freaknerd.co](https://freaknerd.co/#contacto)
```

---

## 6 · Antes de poner Publicado

- [ ] ¿El primer párrafo es una escena, no un contexto?
- [ ] ¿Los H2 son preguntas que alguien escribiría en Google?
- [ ] ¿Hay una *respuesta rápida* en la pregunta principal?
- [ ] ¿Hay al menos un dato, una cifra o un caso concreto?
- [ ] ¿La descripción tiene entre 140 y 160 caracteres y abre con el dolor?
- [ ] ¿El slug está sin tildes ni eñes?
- [ ] ¿Hay FAQ y cierre con invitación?
- [ ] ¿Enlacé alguna otra entrada del blog? *(el enlace interno reparte autoridad)*
- [ ] ¿Entre 800 y 1.500 palabras?

---

*Referencia: `Propiedad Manager/07 Marketing y Ventas/Blog SEO` en Drive —
`01 Artículos MD`, `03 Recursos/propiman_seo_articulos_julio2026.md` y
`_borradores-con-frontmatter`.*
