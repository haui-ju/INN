# Plantilla · Business Model Canvas

Los nueve bloques del lienzo en su disposición clásica (socios, actividades y recursos a la izquierda; propuesta de valor al centro; relaciones, canales y segmentos a la derecha; costos e ingresos abajo), cada uno con sus elementos. Ocupa todo el ancho y la imagen se arma a 1560 px. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual bmc …` lo hace; en una corrida, `visuales.py construir --visual bmc --run <corrida>` lo hace con los datos extraídos de la fuente. **No se edita nada más** del HTML.

## De dónde salen los datos
De la tabla `Bloque | Contenido` de `secciones/1.4.md` de la corrida de `03-make-business-diagnosis` (la indicada con `--run` o la vigente); el nombre comercial sale de la tabla de `secciones/1.1.md`. Si cambia el Canvas, se corrige con `03-make-business-diagnosis-update` y se vuelve a construir.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `empresa`: nombre comercial (subtítulo del lienzo; si está vacío se usa `proyecto`).
- `bloques`: nueve objetos con `clave` (`segmentos`, `propuesta`, `canales`, `relaciones`, `ingresos`, `recursos`, `actividades`, `socios`, `costos`), `nombre` e `items` (lista de textos).

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `bmc.png`). La imagen incluye el título y el lienzo, no los botones.

## Datos de ejemplo y versión vacía
`mock.json` trae el lienzo del caso Pollería Don Tito con el esquema completo, para revisar el diseño. **La skill nunca lo usa como datos del proyecto.** La versión vacía (`html_tpl.py limpiar --visual bmc`) conserva las claves sin contenido y la plantilla muestra «Sin datos».
