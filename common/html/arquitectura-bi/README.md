# Plantilla · Arquitectura de BI

Arquitectura de la solución en cuatro capas en orden (fuentes, ETL, almacenamiento y visualización), cada una con sus componentes (código, función y entrada y salida), las flechas del flujo del dato y las herramientas elegidas (o «Pendiente»). Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual arquitectura-bi …` lo hace; en una corrida, `visuales.py construir --visual arquitectura-bi --run <corrida>` lo hace con los datos extraídos de la fuente. **No se edita nada más** del HTML.

## De dónde salen los datos
De las tablas de `secciones/2.2.md` (componentes por capa) y `secciones/2.3.md` (herramientas por capa) de la corrida de `06-make-bi-solution` (la indicada con `--run` o la vigente). El markdown es la fuente de verdad: si cambia, se corrige con `06-make-bi-solution-update` y se vuelve a construir el visual.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además `capas`: lista de cuatro capas con `clave` (`fuentes`, `etl`, `almacenamiento`, `visualizacion`), `nombre`, `herramientas` (lista de textos; «Pendiente» se marca como pendiente) y `componentes` (cada uno con `codigo`, `nombre`, `funcion` y `entrada_salida`).

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `arquitectura-bi.png`). La imagen incluye el título y el contenido, no los botones.

## Datos de ejemplo y versión vacía
`mock.json` trae la arquitectura del caso Pollería Don Tito con el esquema completo: es lo que se ve al abrir `index.html` tal cual, para revisar el diseño. **La skill nunca lo usa como datos del proyecto**: extrae los datos reales de la fuente (`visuales.py extraer --visual arquitectura-bi`). La versión vacía (`html_tpl.py limpiar --visual arquitectura-bi`) conserva las claves sin contenido y la plantilla muestra «Sin datos».
