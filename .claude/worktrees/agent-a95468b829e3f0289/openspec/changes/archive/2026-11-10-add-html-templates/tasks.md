## 1. Tema y reglas

- [x] 1.1 Definir el tema base estilo Claude: actualizar `01-design-system/references/tokens-base.json` (acento naranja, `acento-fuerte`, neutros cálidos, `--fuente-titulos`, pares de contraste AA claro y oscuro), `common/design-system/guia.md` y las plantillas `ds-*` (roles de color, tipografía de tres fuentes, tema claro por defecto) y adaptar las pruebas del sistema de diseño
- [x] 1.2 Escribir `common/html/DESIGN.md` (color, tipografía, espacio, forma, componentes, movimiento, accesibilidad y reglas de uso de cada componente) y `common/html/README.md` (contrato de la plantilla y cómo agregar un visual), aplicando las guías de diseño de artefactos y de visualización de datos

## 2. Compilación y componentes

- [x] 2.1 Crear `common/html/_build/` (`package.json`, `build.mjs` con esbuild y la CLI de Tailwind, `src/styles.css` con el tema ligado a las variables de los tokens, fuentes en base64, plantilla de página con los dos bloques, `manifiesto.json` y `.gitignore` de `node_modules`) y el script que escribe cada `index.html`
- [x] 2.2 Crear los componentes compartidos al estilo shadcn/ui (`Button`, `Card`, `Badge`, `Progress`, `Table`, selector de escala, encabezado con fecha de corte) y la barra de acciones con tema, escala y botones de imagen (`captura.js` con la construcción pura del SVG, la rasterización, el portapapeles y el respaldo de descarga)
- [x] 2.3 Implementar `.claude/skills/_shared/html_tpl.py` (`copiar`, `copiar_texto`, `comprobar`, `tokens_css`, CLI) y `tests/test_html_tpl.py`: copia sin otros cambios, tokens base y de un diseño, escape de `</` en los datos, manifiesto de sincronía y sin recursos externos

## 3. Plantillas iniciales

- [x] 3.1 Crear `common/html/gantt/` (`modelo.js`, vista React, `README.md`, `mock.json`, `index.html` compilado) con el mismo contenido del Gantt actual y verificarla en claro, oscuro y 360 px
- [x] 3.2 Crear `common/html/kanban/` con el mismo contenido del Kanban actual y verificarla en claro, oscuro y 360 px
- [x] 3.3 Crear `common/html/vista-previa/` (tokens, tipografía, espaciado y los seis componentes; los datos son los tokens) y verificarla en claro, oscuro y 360 px
- [x] 3.4 Escribir `tests/test_html_templates.py`: modelo con `node` sobre `mock.json` y datos de ejemplo contra `boards.textos` y `boards.superadas`, render en servidor si hay dependencias, construcción del SVG de captura, y omisión con aviso sin `node`

## 4. Integración y validación

- [x] 4.1 Cambiar `boards.py render` y `01-design-system/scripts/render_preview.py` para usar `html_tpl.copiar`; retirar de `boards.py` el código que dibuja el marcado conservando `calcular`, `textos`, `superadas`, `construir` y la CLI; adaptar `test_boards.py` y `test_design_system.py`
- [x] 4.2 Adaptar `rules/html_boards.py` y `rules/design_system.py` a la validación por igualdad con la plantilla y `tests/test_html_boards.py`; verificar que `sprint_report`, `final_analysis` y `report` siguen pasando

## 5. Documentación de las skills

- [x] 5.1 Actualizar `common/html-boards/guia.md` y sus plantillas (botones de imagen, selector de escala, nombre del PNG, límites del navegador), las `SKILL.md` de `13-design-html-boards`, `13-design-html-boards-update`, `01-design-system` y `01-design-system-update`; verificar que no mencionan que la skill genera imágenes

## 6. Verificación

- [x] 6.1 Ejecutar `openspec validate add-html-templates --strict`, `openspec validate --specs --strict` y las pruebas del kit, y revisar a mano las tres plantillas en un navegador (claro, oscuro, teléfono, botones de imagen); anotar lo que solo se pudo comprobar a mano
