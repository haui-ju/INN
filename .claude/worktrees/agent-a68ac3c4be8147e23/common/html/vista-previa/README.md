# Plantilla · Vista previa del sistema de diseño

Muestra los tokens del sistema de diseño (color, tipografía, espacio, radio y sombra) y los componentes mínimos (tarjeta, barra de progreso, tabla con etiquetas de estado y botones) con el estilo de [`../DESIGN.md`](../DESIGN.md). La usa `02-design-system` para `preview.html`.

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `render_preview.py <tokens.json> <preview.html> --titulo "<proyecto>"` lo hace. **No se edita nada más** del HTML.

## Esquema de datos 
- `schema`: 1.
- `proyecto`: nombre que se muestra bajo el título.
- `tokens`: el contenido de `tokens.json` (color claro y oscuro, tipografía, espacio, radio, sombra).

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `vista-previa.png`, sin fecha).

## Datos de ejemplo y versión vacía
`mock.json` trae datos de ejemplo (los tokens base): son los que se ven al abrir `index.html` tal cual. **La skill nunca los usa como datos del proyecto**: usa los tokens del sistema de diseño vigente (`render_preview.py`). La versión vacía (`python3 .claude/skills/_shared/html_tpl.py limpiar --visual vista-previa`) conserva las claves y muestra «Sin datos».
