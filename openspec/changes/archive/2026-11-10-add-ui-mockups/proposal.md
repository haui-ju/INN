# Proposal

## Why

El Design Thinking deja un prototipo de baja fidelidad en Miro (`PAN-nn`, paso 06) y el diseño del sistema (paso 14) decide, en 5.3, qué pantallas finales `UI-nn` tendrá la app, pero solo como una tabla. Falta ver **cómo debería quedar la app**: un mockup final por pantalla, con el sistema de diseño del proyecto y en HTML (más barato, validable y coherente con el resto del kit que Figma por MCP), listo para capturar como imagen e incluir en el informe.

## What Changes

- **Skill nueva `14b-make-ui-mockups` (y `14b-make-ui-mockups-update`)**, después de `14-make-system-design`. Lee la tabla `UI-nn` de `interfaz.md`, el destino de cada `PAN` y las historias; **propone** por pantalla su formato (móvil o escritorio) y sus bloques, con datos de ejemplo del dominio; el usuario confirma. Guarda `pantallas.json` en `project/ui-mockups/<corrida>/` y genera una pantalla HTML por `UI-nn`, una galería con todas, `leer-imagen/<pantalla>.md`, `inventario-ui.md` y un `README.md`.
- **Dos plantillas nuevas en `common/html/`:** `pantalla/` (la pantalla en un marco de teléfono o de escritorio, con los tokens del sistema de diseño y los botones de imagen) y `galeria-pantallas/` (todas las pantallas en miniatura, una sola imagen resumen). Las pantallas se arman con una lista cerrada de bloques (barra, buscador, chips, pestañas, lista, formulario, tarjeta de datos, cuadrícula, alerta y acciones), sin interfaz libre.
- **Validación:** `pantallas.json` coincide con la tabla `UI` vigente (códigos, nombres, PAN de origen, historias); cada historia de la tabla aparece en su pantalla; cada HTML es la plantilla con solo los tokens y los datos; `leer-imagen/` e `inventario-ui.md` coinciden con los datos.
- **Índice del informe:** 5.3 se divide en **5.3.1 Destino de las pantallas del prototipo** y **5.3.2 Pantallas finales** (imagen: la galería) y se agrega el anexo **D.5 Inventario de pantallas finales** (una imagen por pantalla). `14-make-system-design` numera esos dos encabezados en `interfaz.md`.
- **Informe (`19-make-report`):** 5.3.2 lleva el marcador de la galería con su explicación y D.5 lleva un marcador por pantalla con la suya.
- **Orden y nombre:** el paso entra como `14b-` para no renumerar los demás; el esquema de nombres admite una letra única en los pasos intercalados.
- **Figma:** fuera de alcance; queda como opción posterior sobre los mismos JSON.

## Capabilities

### New Capabilities
- `ui-mockups`: la skill `14b-make-ui-mockups` y su `-update`, los datos de las pantallas, los bloques, las dos plantillas, la explicación de cada imagen y su validación.

### Modified Capabilities
- `system-design`: `interfaz.md` numera 5.3.1 y 5.3.2.
- `report-index-structure`: puntos 5.3.1, 5.3.2 y D.5 y la marca de imagen.
- `report-assembly`: marcadores de la galería y de cada pantalla final.
- `skill-pipeline`: nombre con letra para pasos intercalados y veintiún pasos.

## Impact

- **Archivos nuevos:** `.claude/skills/14b-make-ui-mockups/` y `14b-make-ui-mockups-update/`, `common/ui-mockups/` (guía y modelos), `common/html/pantalla/` y `common/html/galeria-pantallas/` (+ fuentes en `_build/src/visuales/`), `.claude/skills/_shared/mockups.py`, `rules/ui_mockups.py` y sus pruebas.
- **Archivos modificados:** `pipeline.json` (paso nuevo y órdenes siguientes), `validate_run.py` (reglas), `common/system-design/models/sis-3-interfaz.md` y `rules/system_design.py` (encabezados numerados), `common/structure/model1.md`, `report_map.json` y `report.py` (marcadores y fuente D.5), documentos de `common/html/`, `common/report/guia.md` y las pruebas del pipeline.
- **Sin cambio:** `06-make-design-thinking-prototypes` y su tablero de Miro, los visuales de `13-design-html-boards`, el resto de las skills y sus números.
- **Fuera de alcance:** Figma, interfaz libre fuera de la lista de bloques, el sistema real (capturas del incremento: las pone el usuario), ejecutar las skills.
- **Supuestos registrados:** una imagen por pantalla solo en D.5 y una galería en 5.3.2; los datos de ejemplo de cada pantalla los propone la skill desde el dominio y las historias y el usuario los confirma; el único dato de una pantalla que no sale de la tabla `UI` es su contenido (`bloques`), que vive en `pantallas.json` y se cambia con el `-update`.
