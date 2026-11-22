# Design

## Context

Estado observado: `common/html/` ya contiene `gantt`, `kanban` y `vista-previa` (React, Tailwind, componentes shadcn, tokens y datos en dos bloques, botones de imagen, `limpiar` y manifiesto de sincronía); `13-design-html-boards` genera `gantt.html` y `kanban.html` en `project/html-boards/<corrida>/` desde `data.json`. Las fuentes de los nuevos visuales ya existen como markdown validado: FODA en tablas `FOR`/`DEB`/`OPO`/`AME` del capítulo 1 (`bloques/1-2-diagnostico.md` y `capitulo-1.md`), `canvas.md` y `canvas-v1.md` con la tabla «Cambios respecto al v0», `mapa-empatia.md`, `journey-map.md` y `matriz-priorizacion.md` del Design Thinking, `equipo-scrum.md`, `ceremonias.md` con su calendario, `resultados.md` y `decision.md` de los resultados Lean y `analisis-consolidado.md` (6.4.1 y 6.4.3). El paso 13 corre antes de 14 a 18, de modo que 17 y 18 aún no existen cuando se ejecuta por primera vez. El índice marca cada punto con `[A1]`… y paréntesis descriptivos; `report.py` lo lee con expresiones regulares.

## Goals / Non-Goals

**Goals:** una imagen profesional por cada sección visual del informe sin dibujar nada a mano; los datos salen siempre de las tablas ya validadas; un solo lugar (`13`) que las genera y las actualiza.

**Non-Goals:** que el informe inserte las imágenes, diagramas Mermaid, pantallas de Miro o Figma, crear una skill nueva, ejecutar las skills.

## Decisions

### D1. Diez plantillas, once visuales
| Plantilla | Visual en la corrida | Origen (corrida vigente) | Puntos |
|---|---|---|---|
| `foda` | `foda.html` | 03 `capitulo-1.md` (1.2.1 y 1.2.2) | 1.2 |
| `lean-canvas` | `lean-canvas-v0.html` | 02 `canvas.md` | 1.3.2 |
| `lean-canvas` | `lean-canvas-v1.html` (cambios resaltados) | 07 `canvas-v1.md` y 02 `canvas.md` | 3.4 |
| `mapa-empatia` | `mapa-empatia.html` | 05 `mapa-empatia.md` | 3.1.2.2, D.1 |
| `journey-map` | `journey-map.html` | 05 `journey-map.md` | 3.1.3.2, D.1 |
| `matriz-priorizacion` | `matriz-priorizacion.html` | 05 `matriz-priorizacion.md` | 3.1.4.2 |
| `equipo-scrum` | `equipo-scrum.html` | 08 `equipo-scrum.md` | 4.1.1 |
| `calendario-ceremonias` | `calendario-ceremonias.html` | 12 `ceremonias.md` y 11 `gantt.json` (sprints) | 4.7 |
| `panel-avance` | `panel-avance.html` | `data.json` de la propia corrida | 6.N.2, 6.N.4 |
| `resultados-lean` | `resultados-lean.html` | 17 `resultados.md` y `decision.md` | 3.2.3, 3.2.4 |
| `cumplimiento-objetivos` | `cumplimiento-objetivos.html` | 18 `analisis-consolidado.md` (6.4.1 y 6.4.3) | 6.4.1 a 6.4.3 |

### D2. Extracción desde el markdown (`visuales.py`)
Una función por visual (`extraer(visual, raiz)`) lee la corrida vigente de su origen, reutiliza los ayudantes de tablas de las reglas existentes y devuelve un JSON con `schema`, `proyecto` y los datos del visual; falla con un mensaje claro si falta la fuente o una tabla. Los datos opcionales (por ejemplo `prioridad`) solo se incluyen si el origen los trae. CLI: `visuales.py extraer --visual foda --raiz . --salida datos.json` y `visuales.py disponibles --raiz .` (qué visuales tienen fuente y cuáles no).

### D3. Salida de `13` y `13-update`
Los visuales van en `visuales/` dentro de la corrida de `project/html-boards/`: `<visual>.json` (los datos extraídos) y `<visual>.html` (la plantilla copiada con esos datos y los tokens). `gantt.html`, `kanban.html` y `data.json` no cambian de sitio. La skill muestra qué visuales tienen fuente, pregunta cuáles generar (por defecto todos los disponibles) y los lista en el `README.md`. Los visuales cuya fuente aparece después (17 y 18) se suman con `13-design-html-boards-update`, que bifurca la corrida, extrae de nuevo todo y vuelve a copiar; `17-make-lean-results` y `18-make-final-analysis` lo recuerdan en su cierre.

### D4. Validación
`rules/html_boards.py` recorre `visuales/`: cada `<visual>.json` debe ser **igual** a `extraer` sobre las corridas vigentes (si la fuente ya no existe o cambió, informa que hay que actualizar con el `-update`), cada `<visual>.html` debe ser la plantilla con solo el bloque de tokens (los de `diseno`) y el de datos (el JSON del par) sustituidos, y no puede haber un HTML sin su JSON. El `panel-avance` usa `data.json` de la corrida como datos.

### D5. Diseño de cada visual (con `DESIGN.md` y las guías de visualización)
- **FODA:** cuadrícula 2×2 (interno: fortalezas y debilidades; externo: oportunidades y amenazas) con tarjetas de ítem, código mono y evidencia; cada cuadrante con su tono.
- **Lean Canvas:** los nueve bloques en la disposición clásica del canvas, problemas con su código, supuestos de mayor riesgo con riesgo y estado; en v1, los bloques cambiados resaltados con «v0 → v1» y su evidencia.
- **Mapa de empatía:** cuatro cuadrantes (dice, piensa, hace, siente) alrededor del usuario, con citas y su código de evidencia, y dolores y ganancias abajo.
- **Journey map:** etapas en columnas, filas de acciones, pensamientos y puntos de contacto, **curva de emoción** de −2 a +2 en SVG y los puntos de dolor señalados.
- **Matriz de priorización:** dispersión impacto × factibilidad con las ideas como puntos etiquetados, cuadrantes nombrados y las incluidas en el MVP destacadas.
- **Equipo Scrum:** tarjetas de rol (Product Owner, Scrum Master, Equipo de desarrollo) con integrantes, «también desarrolla» y responsabilidades, el interesado externo y la línea de los tres sprints con sus fechas.
- **Calendario de ceremonias:** los tres sprints como carriles con Planning, Daily (recurrente), Review y Retrospective ubicadas en su fecha, con duración y participantes.
- **Panel de avance:** indicadores, avance por sprint (barras), rendimiento semanal (columnas), tiempo de ciclo y WIP por columna frente a su límite; cifras de `calculado`.
- **Resultados Lean:** por experimento, barra del resultado contra la línea del criterio de éxito, semáforo de cumplimiento y la decisión por hipótesis (perseverar, pivotar, iterar).
- **Cumplimiento de objetivos:** por objetivo, meta frente a resultado, valoración, base de la evidencia y, debajo, la tabla de métricas acumuladas por avance.
Cada plantilla reutiliza los componentes de `_build/src/ui/`, respeta el ancho completo cuando es grande (`anchoImagen`) y lleva sus botones de imagen.

### D6. Marca «(incluye imagen)» en el índice
Se agrega, entre paréntesis y dentro de la línea del punto, a: 1.2, 1.3.2, 3.1.2.2, 3.1.3.2, 3.1.4.2, 3.2.3, 3.2.4, 3.4, 4.1.1, 4.6.2, 4.7, 4.8, 6.N.2, 6.N.4, 6.4.1, 6.4.2 y 6.4.3 (imagen de un HTML) y a 3.1.5.3, 5.3, 6.N.3, 6.N.5, 6.N.7 y D.3 (imagen que aporta el usuario). `report.py` lee la marca y `cargar_indice` devuelve `imagen` por punto; no cambia el armado.

### D7. Pruebas
Por visual: extracción desde el ejemplo de su plantilla de origen (y desde la referencia del Design Thinking), igualdad entre el modelo del visual y sus datos, montaje en jsdom con datos de ejemplo y vacíos, y el HTML de la corrida igual a la plantilla con sus datos. Se omiten con aviso sin `node` o sin dependencias, como las de las plantillas actuales.

### D8. Calidad visual
Cada plantilla se verifica abriéndola en un navegador en claro, oscuro y 360 px y capturando su PNG a ×2 con los botones, y se compara con el `DESIGN.md`.

### D9. Explicación de cada imagen (`leer-imagen/`)
`visuales.py` deriva de los datos de cada imagen un `leer-imagen/<visual>.md` (también para `gantt` y `kanban`, desde `data.json`): título, cuatro o cinco puntos con etiqueta en negrita (qué muestra, cómo leerla, qué transmite, dato clave) y el pie de foto sugerido. Es texto determinista (sin redacción libre) para que no invente nada y se pueda validar por igualdad con lo que se deriva de los datos; si cambian los datos, cambia la explicación. `construir` lo escribe junto al visual y `visuales.py leer --run` lo hace para el Gantt y el Kanban. La validación exige que exista uno por imagen, que coincida y que no sobre ninguno. El informe lo usa en el cambio posterior de marcadores de imagen.

### D10. Cambio de un dato de un visual
El dato vive en el markdown de la skill de origen (o en `data.json` para panel, Gantt y Kanban). `13-design-html-boards-update` gana un modo «cambiar un dato de un visual»: ubica el origen con `visuales.py origen`, muestra el cambio, deja que el `-update` de origen modifique solo ese dato (ya edita solo lo afectado en una copia «-fork») y después vuelve a extraer todo; una prueba comprueba que solo cambian el visual afectado y lo que depende del dato. Cada `-update` de origen avisa al cerrar qué visuales quedan desactualizados.

## Risks / Trade-offs

- [Formato de una tabla de origen cambia] → la extracción falla con mensaje claro y la validación lo marca; las pruebas usan los ejemplos de las plantillas de cada skill.
- [17 y 18 llegan después de 13] → los visuales son opcionales por fuente y se suman con el `-update`; las skills lo recuerdan.
- [Diez plantillas pesan cerca de 4 MB en total] → cada archivo es independiente y solo se copia el visual que se usa.
- [Visuales con gráficos propios (curva, dispersión, barras)] → SVG dentro de React, sin librerías de gráficos, reutilizando los tokens; el modelo calcula posiciones y es puro y probado.
- [El chip de prioridad y otros datos opcionales no existen en el origen] → se muestran solo si vienen; no se inventan.

## Migration Plan

Se agregan las plantillas y el módulo de extracción, se amplían `13`, su `-update` y la validación, y se marcan los puntos del índice. No hay corridas en `project/` que migrar.

## Open Questions

- Si más adelante conviene incrustar estos visuales como fragmentos en el HTML del informe.
