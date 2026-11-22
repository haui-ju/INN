# Plantilla · FODA

Diagnóstico FODA en cuatro cuadrantes (fortalezas y debilidades arriba como análisis interno; oportunidades y amenazas como análisis externo), cada ítem con su código y su evidencia. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual foda …` lo hace; en una corrida, `visuales.py construir` lo hace con los datos extraídos de la fuente. **No se edita nada más** del HTML.

## De dónde salen los datos
Los extrae `.claude/skills/_shared/visuales.py` de la corrida vigente de la skill del capítulo 1 que produce la matriz FODA (punto 1.6 del informe); el extractor se registra en `visuales.py` junto con esa skill. El markdown es la fuente de verdad: si cambia, se corrige con el `-update` de esa skill y se vuelve a construir el visual.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `cuadrantes`: `fortalezas`, `debilidades`, `oportunidades` y `amenazas`; cada ítem trae `codigo`, `texto` y `evidencia`.

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `foda.png`). La imagen incluye el título y el contenido, no los botones.

## Datos de ejemplo y versión vacía
`mock.json` trae datos de ejemplo con el esquema completo: son los que se ven al abrir `index.html` tal cual, para revisar el diseño. **La skill nunca los usa como datos del proyecto**: extrae los datos reales de la fuente (`visuales.py extraer --visual foda`). La versión vacía (`html_tpl.py limpiar --visual foda`) conserva las claves sin contenido y la plantilla muestra «Sin datos».
