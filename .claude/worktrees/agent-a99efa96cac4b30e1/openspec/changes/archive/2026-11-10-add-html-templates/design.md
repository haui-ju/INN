# Design

## Context

Estado observado: `boards.py` calculaba los indicadores y **dibujaba** el marcado del Gantt y del Kanban; `01-design-system/scripts/render_preview.py` hacía lo mismo para `preview.html`. `rules/html_boards.py` y `rules/design_system.py` validaban el HTML buscando variables `--c-*`, el JSON embebido y textos. `sprint_report`, `final_analysis` y `report` usan `boards.calcular` y `boards.textos` pero no el dibujo. El sistema de diseño entrega `tokens.json` (color claro y oscuro, tipografía, espacio, radio, sombra), con roles de color fijos (`fondo`, `superficie`, `texto`, `texto-secundario`, `borde`, `acento`, `acento-texto`, `exito`, `alerta`, `error`) y seis componentes mínimos. El registro de npm responde (React 19, Tailwind 4, esbuild, Radix, lucide y fuentes de `fontsource`) y `node` y `bun` están instalados en la máquina de desarrollo; el kit en sí es Python de la biblioteca estándar. El usuario pide plantillas ya hechas con un diseño moderno y profesional **no genérico, estilo Claude** (naranja, serif para titulares), con React, Tailwind y shadcn/ui, y botones para obtener la imagen de cada visual.

## Goals / Non-Goals

**Goals:** un diseño único y cuidado, pulido una vez; copiar y rellenar en lugar de generar; menos código Python de dibujo; imagen PNG de alta calidad desde cada HTML; infraestructura lista para sumar visuales sin repetir CSS ni componentes.

**Non-Goals:** los visuales nuevos, cambiar el informe a marcadores, diagramas Mermaid, pantallas de Miro o Figma, ejecutar las skills, que el usuario final necesite `node`.

## Decisions

### D1. Biblioteca `common/html/`
```
common/html/
  DESIGN.md            reglas visuales: color, tipografía, espacio, componentes, movimiento
  README.md            contrato de una plantilla y cómo agregar otra
  _build/              fuentes y compilación (package.json, build.mjs, src/…, manifiesto)
  gantt/  kanban/  vista-previa/
      index.html       plantilla compilada y autónoma: es la que se copia
      README.md        qué se cambia y qué no; esquema de datos; cómo capturar
      mock.json        datos de ejemplo con el esquema completo (se ven al abrir index.html)
```
`index.html` se compila con `node _build/build.mjs` y **se versiona**; `node_modules` no. Un manifiesto (`_build/manifiesto.json`) guarda la huella (sha256) de las fuentes y de cada plantilla; una prueba comprueba que coinciden sin necesidad de `node`.

### D2. Pila de las plantillas
React 19 con componentes al estilo shadcn/ui (`Button`, `Card`, `Badge`, `Progress`, `Table`, `Select` nativo con estilo; `class-variance-authority`, `clsx`, `tailwind-merge`, Radix `Slot` y `Progress`, íconos de lucide), Tailwind 4 con un tema que **mapea sus colores y radios a las variables CSS de los tokens** (`--c-fondo`, `--c-acento`…), de modo que cambiar de sistema de diseño es cambiar el bloque de tokens. Se compila con esbuild (JavaScript) y la CLI de Tailwind (CSS) a un único archivo con CSS, JS y fuentes (`@font-face` en base64) incrustados.

### D3. Contrato de la plantilla
Un solo archivo sin recursos externos, con exactamente dos bloques sustituibles delimitados por marcadores:
- **Tokens:** `/*tokens:inicio*/ … /*tokens:fin*/` dentro de un `<style>`, con las variables CSS de color claro y oscuro, tipografía (`--fuente`, `--fuente-titulos`, `--fuente-mono`), espacio, radio y sombra (por defecto, los tokens base).
- **Datos:** `<script type="application/json" id="datos">…</script>`.
Además: `<meta name="viewport">`, tema **claro por defecto** (el oscuro se activa con el botón; la elección se recuerda) con `data-theme` y `prefers-color-scheme` como respaldo sin JavaScript, fondo explícito en `body`, sin desplazamiento horizontal de la página en 360 px, `<noscript>` que avisa que el visual necesita JavaScript, y la fecha de corte («al DD-MM-AAAA» o «Línea base») destacada dentro del área de captura.

### D4. Modelo puro y vista React
Cada visual tiene un **modelo** (`modelo.js`, sin React ni DOM): recibe `datos` y devuelve el modelo de vista (textos de los indicadores a partir de `calculado` **sin recalcular**, filas, posiciones, columnas, marcas de WIP superado, estado vacío «Sin datos»). La vista React solo pinta ese modelo. El cálculo de indicadores sigue en `boards.py`; el modelo solo da formato.

### D5. Botones de imagen
Dos botones, «Copiar imagen» y «Descargar imagen», más un selector ×2, ×3 y ×4 (×2 por defecto; la última elección se guarda en el navegador, con `try/catch`). El área de captura es `[data-captura]`; lo marcado con `[data-no-captura]` queda fuera. Procedimiento sin librerías: clonar el área, expandir el contenido con desplazamiento, envolverlo en un SVG con `foreignObject` con el CSS (tokens, estilos y fuentes incrustadas) y el tema actual, dibujarlo en un canvas a la escala elegida y obtener el PNG. «Descargar» usa un enlace `download` con el nombre `<visual>-<fecha de corte>.png` (`<visual>.png` si no hay fecha); «Copiar» usa `navigator.clipboard.write` y, si falla, descarga y avisa con `role="status"`. La construcción del SVG es una función pura y se prueba; la rasterización y el portapapeles dependen del navegador y se verifican a mano.

### D6. Estilo Claude (`DESIGN.md` y tokens base)
- **Color:** fondo marfil cálido, superficies blancas, texto casi negro cálido, bordes arena; acento naranja terracota para **rellenos** con texto oscuro (`acento` y `acento-texto`) y una variante más oscura para **texto y enlaces** (`acento-fuerte`, rol nuevo, AA sobre `fondo` y `superficie`); estados (`exito`, `alerta`, `error`) apagados y legibles. El tema oscuro no es el claro invertido: fondo carbón cálido y acento más claro.
- **Tipografía:** titulares en **Newsreader** (serif variable abierta), texto en **Instrument Sans** y códigos (`TAR-05`, `HU-02`) en monoespaciada del sistema; las fuentes se incrustan en latín (cubre el español).
- **Forma:** radios medios y generosos, sombras suaves, espacio amplio, jerarquía clara, un solo color de acento, sin degradados ni adornos; íconos de lucide solo con función.
- El tema reemplaza los tokens base de `01-design-system` para todo el proyecto; la guía, la plantilla `ds-1-tokens` y la vista previa se actualizan.

### D7. Script `html_tpl.py`
- `copiar_texto(visual, datos, tokens)` y `copiar(...)`: leen `common/html/<visual>/index.html` y sustituyen el bloque de tokens (con `tokens_css`) y el de datos (JSON con `</` escapado); no tocan nada más.
- `limpiar(datos)`: devuelve unos datos (p. ej. un `mock.json`) sin contenido: mismas claves, listas y textos vacíos, `fecha_corte` nula; conserva `schema` y `diseno`. La skill parte de esa versión vacía y nunca usa los datos de ejemplo como datos del proyecto.
- `comprobar()`: verifica el manifiesto de sincronía (huella de las fuentes y de cada plantilla).
- CLI: `html_tpl.py copiar --visual gantt --datos data.json --tokens base|ruta --salida archivo`, `html_tpl.py limpiar --visual gantt [--salida datos.json]` y `html_tpl.py comprobar`.
- `boards.py render` mantiene su interfaz y llama a `copiar` para `gantt` y `kanban`; `render_preview.py` llama a `copiar` para `vista-previa` con los tokens como datos.

### D8. Validación por igualdad
Para un HTML de corrida, `rules/html_boards.py` reconstruye el esperado (la plantilla con los dos bloques sustituidos por los tokens de `diseno` y por el `data.json` de la corrida) y exige igualdad exacta; informa qué bloque difiere. La comprobación de recursos externos ignora los espacios de nombres de `www.w3.org`. La plantilla en sí se prueba una vez en el repositorio.

### D9. Pruebas
`tests/test_html_templates.py` ejecuta con `node` el modelo de cada visual sobre `mock.json` (con datos) y sobre su versión vaciada con `limpiar`, y sobre otros datos de ejemplo y comprueba que coincide con el cálculo de `boards.py`; si `_build/node_modules` existe, además renderiza la vista con `react-dom/server` y comprueba el contenido (tareas y tarjetas con `data-codigo`, indicadores de `calculado`, WIP superado, «Línea base» o «al DD-MM-AAAA», «Sin datos»). Sin `node` o sin dependencias instaladas esas pruebas se omiten con aviso; el resto del kit no depende de ellas.

### D10. Calidad visual
Cada plantilla se construye aplicando las guías de diseño de artefactos y de visualización de datos y el `DESIGN.md`, y se verifica abriéndola en un navegador en claro, oscuro y 360 px de ancho.

### D11. Cambios en `html-boards` y `design-system`
`html-boards`: el HTML pasa a ser una copia de la plantilla; los indicadores del HTML son los de `calculado`; la validación compara con la plantilla; el `-update` vuelve a copiar. `design-system`: nuevo requisito del tema base. Se conserva la separación de línea base y estado, los cálculos y la publicación opcional.

### D12. Compatibilidad
`data.json`, los nombres de archivo de la corrida (`gantt.html`, `kanban.html`, `preview.html`), `boards.calcular`, `boards.textos` y `boards.construir` no cambian, de modo que `report.py`, `sprint_report.py` y `final_analysis.py` siguen funcionando.

## Risks / Trade-offs

- [Cada HTML pesa unos 400 a 600 KB (React, CSS y fuentes incrustados)] → es aceptable para un archivo que se abre local; se minifica y las fuentes se limitan a latín.
- [Sin JavaScript no se ve el visual] → `<noscript>` lo avisa; los datos siguen en el md y en `data.json`.
- [Copiar imagen no funciona en algún navegador] → cae a descargar y avisa; se documenta en cada `README.md`.
- [La rasterización no se puede probar sin navegador] → se prueba la función pura que arma el SVG y se verifica a mano; es una limitación explícita.
- [Dependencias de npm para reconstruir] → solo en desarrollo; la plantilla compilada está versionada y una prueba de huella detecta desincronía sin `node`.
- [Contraste del naranja] → `acento` solo con texto oscuro y `acento-fuerte` para texto; la validación de contraste del sistema de diseño lo exige.
- [Regresión visual al migrar] → mismo contenido que hoy y comprobación manual en claro, oscuro y teléfono antes de archivar.

## Migration Plan

Se crean el `DESIGN.md`, los tokens base nuevos y la compilación de plantillas, se cambian `boards.py render`, `render_preview.py` y la validación, y se actualizan las pruebas y las guías. No hay corridas en `project/` que migrar.

## Open Questions

- Si más adelante conviene incrustar los visuales como fragmentos en el HTML del informe (se decide en un cambio posterior).
