# Plantilla · FODA

Matriz FODA en cuatro cuadrantes (fortalezas y debilidades como análisis interno; oportunidades y amenazas como análisis externo), cada ítem con su código y su evidencia, y debajo las estrategias cruzadas FO, FA, DO y DA con los códigos que combinan. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual foda …` lo hace; en una corrida, `visuales.py construir --visual foda --run <corrida>` lo hace con los datos extraídos de la fuente. **No se edita nada más** del HTML.

## De dónde salen los datos
De las tablas de `secciones/1.6.md` (cuadros `FOR`, `DEB`, `OPO`, `AME` y la tabla `Código | Tipo | Estrategia | Combina`) de la corrida de `04-make-strategic-analysis` (la indicada con `--run` o la vigente). El markdown es la fuente de verdad: si cambia, se corrige con `04-make-strategic-analysis-update` y se vuelve a construir el visual.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `cuadrantes`: `fortalezas`, `debilidades`, `oportunidades` y `amenazas`; cada ítem trae `codigo`, `texto` y `evidencia`.
- `estrategias`: lista de estrategias cruzadas con `codigo`, `tipo` (`FO`, `FA`, `DO` o `DA`), `texto` y `combina` (lista de códigos FODA). Si está vacía, el visual muestra solo los cuadrantes.

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `foda.png`). La imagen incluye el título y el contenido, no los botones.

## Datos de ejemplo y versión vacía
`mock.json` trae la matriz del caso Pollería Don Tito con el esquema completo: es lo que se ve al abrir `index.html` tal cual, para revisar el diseño. **La skill nunca lo usa como datos del proyecto**: extrae los datos reales de la fuente (`visuales.py extraer --visual foda`). La versión vacía (`html_tpl.py limpiar --visual foda`) conserva las claves sin contenido y la plantilla muestra «Sin datos».
