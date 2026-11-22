# Proposal

## Why

Gantt y Kanban ya se obtienen como HTML con botones de imagen, pero el resto de las secciones visuales del informe (FODA, Lean Canvas, mapa de empatía, journey map, matriz de priorización, equipo Scrum, calendario de ceremonias, avance, resultados Lean y cumplimiento de objetivos) solo existen como tablas de markdown. Para exponer el trabajo se necesitan **imágenes** profesionales de cada una, y hoy habría que dibujarlas a mano. La biblioteca `common/html/` ya tiene el mecanismo (plantilla autónoma, tokens, datos, botones de imagen); faltan las plantillas y el camino que las alimenta desde lo que cada skill ya produjo.

## What Changes

- **Diez plantillas nuevas en `common/html/`** (React, Tailwind y componentes shadcn, estilo `DESIGN.md`), cada una con `index.html`, `README.md` y `mock.json` con datos de ejemplo: `foda`, `lean-canvas` (sirve para v0 y para v1 con los cambios resaltados), `mapa-empatia`, `journey-map` (con curva de emoción), `matriz-priorizacion` (dispersión impacto × factibilidad), `equipo-scrum`, `calendario-ceremonias`, `panel-avance`, `resultados-lean` (barras contra umbral y semáforo) y `cumplimiento-objetivos`.
- **El markdown sigue siendo la fuente de verdad.** Un nuevo módulo del kit (`visuales.py`) **extrae** los datos de cada visual de las tablas de las corridas vigentes de las skills de origen (03, 02, 07, 05, 08, 12, 17, 18) y del `data.json` de los tableros; el HTML se obtiene copiando la plantilla con esos datos y los tokens.
- **`13-design-html-boards` y su `-update` generan todos los visuales cuyo origen exista**, en `visuales/` dentro de la corrida (`<visual>.html` y `<visual>.json`). Como algunos orígenes (17 y 18) se producen después del paso 13, cada visual aparece cuando su fuente existe y se suma con `13-design-html-boards-update`; las skills 17 y 18 lo recuerdan al cerrar.
- **Validación:** cada `visuales/<visual>.json` debe ser igual a lo que se extrae hoy de las corridas vigentes y cada HTML debe ser la plantilla con solo los tokens y esos datos.
- **Explicación de cada imagen:** `leer-imagen/<visual>.md` (puntos cortos de qué muestra y qué transmite, más un pie de foto sugerido), derivado solo de los datos, para pegarlo junto a la imagen en el informe.
- **Actualización de datos de un visual:** el dato se cambia con el `-update` de la skill de origen y `13-design-html-boards-update` vuelve a extraer sin tocar lo demás; los `-update` de origen avisan de los visuales que dependen de ellos.
- **Marcas «(incluye imagen)» en el índice** (`common/structure/model1.md`) en los puntos aprobados; `report.py` las expone (`imagen`) para el cambio posterior del informe a marcadores de imagen.
- **Cambios en `html-boards`** (fuentes, plan, estructura de salida, validación y `-update`) y spec nueva `html-visuals`; la spec del índice gana la marca de imagen.

## Capabilities

### New Capabilities
- `html-visuals`: las diez plantillas de visuales, la extracción de sus datos desde las corridas de origen, sus esquemas, la regla de generarlos solo si existe la fuente y su validación.

### Modified Capabilities
- `html-boards`: fuentes y prerrequisitos, plan y confirmación, estructura de salida, validación y `13-design-html-boards-update` incorporan los visuales.
- `report-index-structure`: marca «(incluye imagen)» en los puntos que llevan imagen.

## Impact

- **Archivos nuevos:** diez carpetas en `common/html/` (`foda/`, `lean-canvas/`, `mapa-empatia/`, `journey-map/`, `matriz-priorizacion/`, `equipo-scrum/`, `calendario-ceremonias/`, `panel-avance/`, `resultados-lean/`, `cumplimiento-objetivos/`), sus fuentes en `common/html/_build/src/visuales/`, `.claude/skills/_shared/visuales.py` y sus pruebas.
- **Archivos modificados:** `common/structure/model1.md` (marcas), `report.py` (lee la marca), `rules/html_boards.py` (valida `visuales/`), `boards.py` o el CLI de `visuales.py` (construcción), las `SKILL.md` de `13-design-html-boards`, `13-design-html-boards-update`, `17-make-lean-results` y `18-make-final-analysis`, `common/html-boards/guia.md`, `common/html/README.md`, `common/html/DESIGN.md` y el manifiesto de plantillas.
- **Sin cambio:** los datos de origen y los validadores de las skills 02 a 18; `pipeline.json` (los visuales son opcionales por fuente).
- **Fuera de alcance:** que `19-make-report` use las marcas y deje marcadores en lugar de imágenes (`change-report-image-placeholders`); diagramas Mermaid; pantallas de Miro o Figma; ejecutar las skills.
- **Supuestos registrados:** las imágenes las genera el navegador del usuario con los botones de cada HTML; el chip de prioridad del Kanban y otros datos opcionales aparecen solo si el origen los trae; los visuales de 17 y 18 se agregan al volver a ejecutar `13-design-html-boards-update` cuando esas skills ya tengan corrida.
