# Proposal

## Why

Los HTML del proyecto (Gantt, Kanban y vista previa del sistema de diseño) se generan desde cero en cada corrida con código Python que dibuja el marcado completo. Eso obliga a mantener y probar mucha lógica de dibujo en el kit, vuelve costoso agregar más visuales y no permite pulir el diseño una sola vez. Además, el usuario necesita **imágenes** de estos visuales para exponer y para el informe, y hoy tiene que capturarlas a mano desde el navegador.

## What Changes

- **Nueva biblioteca `common/html/`**: una carpeta por visual con `index.html` (plantilla ya hecha y autónoma), `README.md` (qué se cambia y qué no, y el esquema de datos) y `mock.json` (datos de ejemplo con el esquema completo, que son lo que se ve al abrir la plantilla; `html_tpl.py limpiar` los deja vacíos y la skill siempre parte de esa versión vacía), un `DESIGN.md` con las reglas visuales de la biblioteca y una carpeta `_build/` con las fuentes de las plantillas.
- **Pila de las plantillas: React 19, Tailwind 4 y componentes al estilo shadcn/ui** (Radix, class-variance-authority, lucide). Se **compilan una sola vez en desarrollo** (esbuild y la CLI de Tailwind) a un único HTML autónomo con el CSS, el JavaScript y las fuentes incrustados; el usuario final nunca necesita `node`: el kit solo copia la plantilla.
- **Estilo Claude, moderno y no genérico**: acento naranja (relleno con texto oscuro y una variante más oscura para texto, ambas AA), neutros cálidos, **titulares en una serif abierta incrustada (Newsreader), texto en una sans (Instrument Sans) y códigos en monoespaciada**, tema **claro por defecto** y oscuro opcional. Las reglas viven en `common/html/DESIGN.md`.
- **Tema base para todo el proyecto:** los tokens base de `01-design-system` (`tokens-base.json`), su guía y su vista previa pasan a ese estilo, de modo que tableros, informe y demás visuales comparten un solo aspecto.
- **Copiar y rellenar, no generar:** la corrida copia la plantilla tal cual y solo sustituye dos bloques: el de **tokens** (variables CSS del sistema de diseño vigente o los base) y el de **datos** (el JSON embebido). Los componentes leen esos tokens a través del tema de Tailwind.
- **Botones de imagen en todo HTML:** «Copiar imagen» y «Descargar imagen» con un selector de escala ×2, ×3 y ×4 (×2 por defecto; recuerda la última elección). El PNG se llama `<visual>-<fecha de corte>.png`. Los botones no salen en la imagen. Si el navegador no permite copiar, descarga y lo avisa. El kit nunca genera PNG: lo hace el navegador del usuario.
- **Migración de los tres HTML existentes** a plantillas: `gantt`, `kanban` y `vista-previa` (esta última para `01-design-system`), con el mismo contenido que hoy y el nuevo estilo.
- **Script del kit `html_tpl.py`** (`copiar` y comprobación de sincronía): copia una plantilla sustituyendo los dos bloques. `boards.py render` y `render_preview.py` pasan a usarlo y se retira de `boards.py` el código que dibuja el marcado.
- **Validación por igualdad con la plantilla:** un HTML de corrida es válido si es la plantilla con solo el bloque de tokens y el de datos sustituidos. La lógica de cada visual (modelo de datos → vista) se prueba en el repositorio con `node`, y un manifiesto con la huella de las fuentes detecta plantillas desactualizadas.
- **Cambios en `html-boards` y en `design-system`:** el HTML pasa de «generado» a «plantilla copiada»; el sistema de diseño gana el tema base descrito.

## Capabilities

### New Capabilities
- `html-templates`: biblioteca de plantillas HTML de `common/html/` (React, Tailwind y componentes shadcn compilados a un archivo autónomo), su contrato (bloques de tokens y de datos, botones de imagen, modelo puro de datos), el `DESIGN.md` de sus reglas, el script de copia y la comprobación de sincronía, `mock.json` y `README.md` por plantilla, y las tres plantillas iniciales.

### Modified Capabilities
- `html-boards`: HTML autónomo, indicadores calculados, validación de los tableros y la skill `13-design-html-boards-update` pasan al mecanismo de plantillas.
- `design-system`: tema base estilo Claude (acento naranja con variante para texto, neutros cálidos, serif para titulares, sans para texto y mono para códigos, claro por defecto).

## Impact

- **Archivos nuevos:** `common/html/` (`DESIGN.md`, `README.md`, `_build/`, `gantt/`, `kanban/`, `vista-previa/`), `.claude/skills/_shared/html_tpl.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/boards.py` (se retira el dibujo), `rules/html_boards.py` y `rules/design_system.py` (validación por igualdad), `01-design-system/references/tokens-base.json`, `01-design-system/scripts/render_preview.py`, la guía y las plantillas de `common/design-system/`, las `SKILL.md` de `13-design-html-boards`, su `-update` y `01-design-system`, `common/html-boards/guia.md` y las pruebas de tableros y de diseño.
- **Dependencias de desarrollo:** `node` y paquetes npm (React, Tailwind, esbuild, Radix, lucide, fuentes) solo para reconstruir las plantillas; `node_modules` no se versiona y el kit sigue siendo Python de la biblioteca estándar.
- **Consumidores:** `19-make-report` sigue copiando `gantt.html` y `kanban.html` a `anexos/tableros/`; `16-make-sprint-report` y `18-make-final-analysis` siguen usando `boards.calcular` y `boards.textos`.
- **Fuera de alcance:** los visuales nuevos (FODA, canvas, equipo Scrum, mapa de empatía, journey, matriz, panel de avance, resultados) y las marcas «(incluye imagen)» del índice (cambio `add-html-visuals`); el cambio del informe a marcadores de imagen (`change-report-image-placeholders`); diagramas Mermaid; pantallas de Miro o Figma; ejecutar las skills.
- **Supuestos registrados:** las fuentes de Claude (Tiempos, Styrene) son propietarias y no se incluyen: se usan alternativas abiertas con licencia OFL, incrustadas; el diseño de Claude Design (claude.ai/design) no se puede invocar desde esta sesión, así que se aplican las guías de diseño de artefactos y, si el usuario crea un proyecto allí, puede leerse con `DesignSync` para alinear los tokens; copiar al portapapeles depende del navegador y su fallback es descargar; la calidad visual se verifica abriendo cada plantilla en un navegador.
