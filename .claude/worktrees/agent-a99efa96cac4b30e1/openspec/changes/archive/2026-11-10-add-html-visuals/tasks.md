## 1. Base y extracción
- [x] 1.1 Crear `visuales.py` en `_shared/` con `extraer(visual, raiz)`, `disponibles(raiz)`, `construir(visual, raiz)` (plantilla + datos + tokens) y CLI `extraer|disponibles|construir`
- [x] 1.2 Implementar los extractores de foda, lean-canvas (v0 y v1), mapa-empatia, journey-map, matriz-priorizacion, equipo-scrum, calendario-ceremonias, panel-avance, resultados-lean y cumplimiento-objetivos, con error claro si falta la fuente
- [x] 1.3 Pruebas de los extractores con ejemplos de las plantillas de origen

## 2. Plantillas
- [x] 2.1 Agregar el manifiesto y las fuentes `_build/src/visuales/<visual>/` (meta, modelo puro, Vista, index) de los diez visuales
- [x] 2.2 Diseñar y construir `foda`, `lean-canvas`, `mapa-empatia`, `journey-map` y `matriz-priorizacion` con README y `mock.json` de ejemplo
- [x] 2.3 Diseñar y construir `equipo-scrum`, `calendario-ceremonias`, `panel-avance`, `resultados-lean` y `cumplimiento-objetivos` con README y `mock.json` de ejemplo
- [x] 2.4 Pruebas de modelo (node) y montaje (jsdom) con datos de ejemplo y vacíos; revisar en navegador en claro, oscuro y 360 px y capturar un PNG a ×2

## 3. Validación y skills
- [x] 3.1 Ampliar `rules/html_boards.py` para validar `visuales/` (JSON igual a la extracción, HTML igual a la plantilla, sin HTML sin JSON)
- [x] 3.2 Actualizar `13-design-html-boards`, `13-design-html-boards-update`, `17-make-lean-results` y `18-make-final-analysis` (recordatorio de agregar su visual) y `common/html-boards/guia.md`
- [x] 3.3 Actualizar `common/html/README.md` y `DESIGN.md` con los nuevos visuales

## 4. Índice y cierre
- [x] 4.1 Agregar «(incluye imagen)» en `common/structure/model1.md` y leerlo en `report.py` (`imagen` en `cargar_indice`)
- [x] 4.2 Ejecutar la suite completa, `openspec validate add-html-visuals --strict` y `openspec validate --specs --strict`

## 5. Explicación de las imágenes y actualización de datos
- [x] 5.1 Generar `leer-imagen/<visual>.md` desde los datos (`visuales.py`: `leer_imagen`, `construir_boards`, CLI `leer`) para los 11 visuales, el Gantt y el Kanban
- [x] 5.2 Validar `leer-imagen/` en `rules/html_boards.py` (existe, coincide con los datos, sin sobrantes) y probarlo
- [x] 5.3 `visuales.py origen` y el modo «cambiar un dato de un visual» en `13-design-html-boards-update`; aviso de imágenes dependientes en los `-update` de 02, 03, 05, 07, 08, 12, 17 y 18
- [x] 5.4 Prueba de que cambiar un dato en la fuente solo actualiza lo que depende de él

