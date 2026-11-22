# Plantilla · Modelo de datos en estrella

Diagrama de base de datos estándar, en blanco: la tabla de hechos con más relaciones en el centro exacto y las demás tablas alrededor (la posición se calcula para evitar cruces y líneas sobre otras tablas), cada una con su cabecera gris, una fila por columna (llave primaria `PK`, llaves foráneas `FK` y medidas `Σ` con su tipo y agregación) y una línea gris por cada relación, con «1» en la dimensión y «∗» en el hecho. Usa los valores del tema claro (`forzar-claro`) aunque el visual abra en oscuro. La tabla de relaciones no va en la imagen (ya está en la sección 2.4) para que la proporción quepa en una diapositiva. Ancho fijo de 1600 px. Estilo en [`../DESIGN.md`](../DESIGN.md).

## Qué se cambia
**Solo** el bloque de tokens y el bloque de datos. `python3 .claude/skills/_shared/html_tpl.py copiar --visual modelo-datos …` lo hace; en una corrida, `visuales.py construir --visual modelo-datos --run <corrida>` lo hace con los datos extraídos de la fuente. **No se edita nada más** del HTML.

## De dónde salen los datos
De `modelo.json` de la corrida de `07-make-data-model-kpi` (la indicada con `--run` o la vigente), que repite lo escrito en `secciones/2.4.md`. Si el modelo cambia, se corrige con `07-make-data-model-kpi-update` y se vuelve a construir el visual.

## Esquema de datos
Siempre `schema` (1) y `proyecto`, y además:
- `hechos`: cada uno con `codigo`, `nombre`, `granularidad`, `medidas` (`nombre`, `tipo` y `agregacion`) y `claves`.
- `dimensiones`: cada una con `codigo`, `nombre`, `clave`, `atributos` y `jerarquias`.
- `relaciones`: cada una con `codigo`, `desde` (hecho), `hacia` (dimensión), `campos`, `cardinalidad` y `filtro`.

## Cómo obtener la imagen
Abre el HTML y usa **Copiar imagen** o **Descargar imagen** (×2, ×3 o ×4; `modelo-datos.png`). La imagen incluye el título y el contenido, no los botones.

## Datos de ejemplo y versión vacía
`mock.json` trae el modelo del caso Pollería Don Tito con el esquema completo: es lo que se ve al abrir `index.html` tal cual, para revisar el diseño. **La skill nunca lo usa como datos del proyecto**: extrae los datos reales de la fuente (`visuales.py extraer --visual modelo-datos`). La versión vacía (`html_tpl.py limpiar --visual modelo-datos`) conserva las claves sin contenido y la plantilla muestra «Sin datos».
