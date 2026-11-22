# Plantilla · FODA

Matriz FODA en **dos láminas** dentro de un solo HTML, separadas por un espacio: la matriz clásica de cuatro cuadros (fortalezas y debilidades arriba, oportunidades y amenazas abajo, cada ítem con su código y su enunciado) y las estrategias cruzadas FO, FA, DO y DA con los códigos que combinan. La evidencia de cada ítem no va en la imagen (está en la tabla del informe) para que el texto sea legible. Cada lámina tiene su título y proporción de diapositiva; se copia la captura entera y se recorta la que se necesite. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual foda …` lo hace; en una corrida, `visuales.py construir --visual foda --run <corrida>` lo hace con los datos extraídos de la fuente. **No se edita nada más** del HTML.

## De dónde salen los datos
De las tablas de `secciones/1.6.md` (cuadros `FOR`, `DEB`, `OPO` y `AME` y la tabla `Código | Tipo | Estrategia | Combina`) de la corrida de `04-make-strategic-analysis` (la indicada con `--run` o la vigente). El markdown es la fuente de verdad: si cambia, se corrige con `04-make-strategic-analysis-update` y se vuelve a construir el visual.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `cuadrantes`: `fortalezas`, `debilidades`, `oportunidades` y `amenazas`; cada ítem trae `codigo`, `texto` y `evidencia` (la evidencia no se dibuja).
- `estrategias`: lista de estrategias cruzadas con `codigo`, `tipo` (`FO`, `FA`, `DO` o `DA`), `texto` y `combina` (lista de códigos FODA). Si está vacía, no sale la lámina de estrategias.

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `foda.png`). La imagen incluye el título y el contenido, no los botones.

## Datos de ejemplo y versión vacía
`mock.json` trae la matriz del caso Pollería Don Tito con el esquema completo: es lo que se ve al abrir `index.html` tal cual, para revisar el diseño. **La skill nunca lo usa como datos del proyecto**: extrae los datos reales de la fuente (`visuales.py extraer --visual foda`). La versión vacía (`html_tpl.py limpiar --visual foda`) conserva las claves sin contenido y la plantilla muestra «Sin datos».
