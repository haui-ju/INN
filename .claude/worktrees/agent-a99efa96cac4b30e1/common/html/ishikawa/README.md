# Plantilla · Ishikawa

Diagrama de causa y efecto: el efecto (problema central) a la derecha, la espina central con su flecha y las categorías repartidas arriba y abajo con sus causas codificadas y una espina oblicua cada una. Dibujo propio con rejilla y SVG por token, sin librerías. Ocupa todo el ancho, la imagen se arma a 1560 px y en teléfono el diagrama se desplaza dentro de su cuadro. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual ishikawa …` lo hace; en una corrida, `visuales.py construir --visual ishikawa --run <corrida>`. **No se edita nada más** del HTML.

## De dónde salen los datos
Del rótulo `**Efecto.**` y de la tabla `Código | Categoría | Causa | Evidencia` de `secciones/1.7.md` de la corrida de `04-make-strategic-analysis`. Las categorías salen en el orden 6M (Método, Mano de obra, Materiales, Maquinaria, Medición, Medio ambiente) y se omiten las que no tienen causas. Si cambia, se corrige con `04-make-strategic-analysis-update` y se vuelve a construir.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `efecto`: el problema principal del brief.
- `categorias`: lista de objetos con `nombre` y `causas` (cada una con `codigo` y `texto`).

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `ishikawa.png`). La imagen sale completa aunque el diagrama se desplace en pantalla.

## Datos de ejemplo y versión vacía
`mock.json` trae el Ishikawa del caso Pollería Don Tito, para revisar el diseño. **La skill nunca lo usa como datos del proyecto.** `html_tpl.py limpiar --visual ishikawa` da la versión vacía, que muestra «Sin datos».
