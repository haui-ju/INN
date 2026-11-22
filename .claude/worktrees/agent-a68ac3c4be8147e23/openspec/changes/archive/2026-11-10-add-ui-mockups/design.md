# Design

## Context

Estado observado: el prototipo de baja fidelidad vive en Miro (`06-make-design-thinking-prototypes`, `PAN-nn`, 3.1.5.3 y D.3). `14-make-system-design` escribe `interfaz.md` (`sis-3`) con el sistema de diseño, la tabla de destino de cada `PAN` (se conserva, se modifica o se descarta) y la tabla de pantallas finales `UI-nn` (pantalla, PAN de origen o «—», historias, cambios); `rules/system_design.py::check_interfaz` valida esas tablas contra el Design Thinking y las historias. `13-design-html-boards` ya muestra el mecanismo: plantillas compiladas en `common/html/<visual>/`, bloques únicos de tokens y datos, `html_tpl.py copiar`, validación por igualdad con la plantilla, `leer-imagen/` derivado de los datos y botones de imagen. El índice no tiene puntos 5.3.x ni D.5; el informe coloca marcadores «(INCLUIR IMAGEN: …)». El esquema de nombres exige dos dígitos sin letras y `pipeline.json` fija veinte pasos con `orden` consecutivo.

## Goals / Non-Goals

**Goals:** ver cada pantalla final de la app como mockup en HTML con el sistema de diseño; partir de lo que ya existe (tabla `UI`, `PAN`, historias); una imagen resumen en 5.3.2 y una por pantalla en D.5; actualizar solo lo afectado.

**Non-Goals:** Figma, interfaz libre, capturas del sistema real, cambiar el paso 06, ejecutar las skills.

## Decisions

### D1. Skill `14b-make-ui-mockups` en el pipeline
Entra con `orden` 15 en `pipeline.json` (los siguientes suben uno; los nombres no cambian), `carpeta` `ui-mockups`, `verbo` `make`, `update` verdadero y `requiere` `06-make-design-thinking-prototypes`, `10-make-user-stories` y `14-make-system-design`. El esquema de nombres admite una sola letra minúscula tras los dos dígitos para pasos intercalados; el orden por nombre se mantiene (`14-…` < `14b-…` < `15-…`). `19-make-report` la suma a su `requiere_por_avance` solo como aviso.

### D2. Fuente de cada dato
- **Tabla `UI`** (código, nombre, PAN de origen, historias, cambios) y **destinos de `PAN`**: de `interfaz.md` de la corrida vigente de 14; se copian sin cambios a `pantallas.json` y la validación exige que coincidan.
- **Contenido de la pantalla** (`formato`, `titulo`, `bloques`): lo propone la skill **a partir de los mockups previos y de lo ya definido**, y lo confirma el usuario; vive solo en `pantallas.json` y se cambia con el `-update`. Fuentes de la propuesta, en este orden:
  1. Si la pantalla viene de un `PAN` que se conserva o se modifica: su fila de `pantallas.md` del Design Thinking («qué muestra», `REQ`, `FLU`), los textos de `escenarios.md` y, para las que se modifican, los hallazgos `HAL-T` de la fase 5 y la columna «Cambios» de la tabla `UI` (lo que cambia respecto al prototipo de Miro).
  2. Las historias de la fila (criterios de aceptación Dado/Cuando/Entonces): dan los campos, las acciones y los mensajes de la pantalla.
  3. Si la pantalla es nueva (origen «—»): solo sus historias y el dominio.
  Los datos de ejemplo salen del dominio (`domain.md`) y de los ejemplos de las historias. Los llamados numerados del Miro no se guardan como datos del paso 06 (viven en el tablero), así que no se leen; el tablero se cita solo por su enlace.

### D2b. Relación entre pantallas, historias y requerimientos
No hay una pantalla por historia ni por requerimiento: una pantalla `UI-nn` cubre una o más historias (columna «Historias» de la tabla `UI`) y viene de cero o un `PAN`, que a su vez cubre `REQ`. La validación comprueba que cada historia de una fila figure en su pantalla y avisa (sin bloquear) de las historias del backlog que ninguna pantalla cubre, porque algunas (de datos o de soporte) no tienen pantalla propia.

### D3. `pantallas.json`
`schema`, `proyecto`, `diseno` y `pantallas`: `codigo`, `nombre`, `formato` (`movil` o `escritorio`), `origen` (`PAN-nn` o nulo), `destino` (de la tabla de destinos si hay origen), `historias`, `req`, `cambios` y `bloques`. Un bloque es `{tipo, …}` con una lista cerrada: `barra` (título y acciones), `buscador`, `chips`, `pestanas`, `lista` (ítems con título, detalle, etiqueta y tono), `formulario` (campos con rótulo y valor), `tarjeta` (título y pares rótulo-valor), `cuadricula` (celdas con rótulo, valor y tono, p. ej. stock por talla), `alerta` (tono y texto) y `acciones` (botones, uno primario).

### D4. Plantillas
`pantalla/`: la pantalla de un `UI-nn` dentro de un marco (teléfono 390 px o escritorio 1280 px) con el título de la barra, los bloques con los componentes shadcn y los tokens; fuera del marco, una cinta con el código, el nombre y las historias que cubre; botones de imagen y `ancho` fijo. `galeria-pantallas/`: todas las pantallas en miniatura (los mismos bloques a escala reducida) en una rejilla con su código; ancho completo e `anchoImagen` 1560. Se agregan como los demás visuales (`_build/src/visuales/<nombre>/`, `mock.json` de ejemplo y `README.md`) y el manifiesto los incluye.

### D5. Salida y validación
`project/ui-mockups/<corrida>/`: `pantallas.json`, `pantallas/<UI-nn>.html`, `galeria.html`, `leer-imagen/<UI-nn>.md` y `leer-imagen/galeria.md`, `inventario-ui.md` (tabla UI, pantalla, formato, REQ y HU, archivo sugerido `<UI-nn>.png`) y `README.md`. `mockups.py` construye todo desde `pantallas.json`; `rules/ui_mockups.py` valida: códigos y datos iguales a la tabla `UI` vigente, cada HU de la fila presente en la pantalla, bloques de la lista cerrada con sus campos, HTML igual a la plantilla con sus tokens y datos, `leer-imagen` e `inventario-ui.md` iguales a los derivados, y texto limpio.

### D6. Explicación de cada imagen
Derivada solo de los datos, como en 13: qué pantalla es (código, nombre y formato), qué historias y requerimientos resuelve, de qué `PAN` viene y qué cambió respecto al prototipo, y qué acciones y bloques tiene. La galería explica cuántas pantallas hay, cuántas se conservan, se modifican o son nuevas y cómo leer la rejilla.

### D7. `14b-make-ui-mockups-update`
Bifurca la corrida y edita solo lo afectado de `pantallas.json` (un texto, un dato de ejemplo, un bloque, el formato), vuelve a construir lo que depende y valida; lo demás queda byte a byte igual. Si cambió la tabla `UI` (otra corrida de 14), propone el modo de resincronizar: copia la tabla nueva, conserva el contenido de las pantallas que siguen y pide el de las nuevas. Una prueba comprueba que cambiar un dato solo cambia esa pantalla, la galería y las explicaciones que dependen del dato.

### D8. Índice e informe
`sis-3` y el validador de 14 numeran `### 5.3.1. Destino de las pantallas del prototipo` y `### 5.3.2. Pantallas finales`; el índice agrega 5.3.1, 5.3.2 `(incluye imagen)` y D.5 `(incluye imagen)` y quita la marca de 5.3. `report_map.json` agrega la fuente de D.5 (`inventario-ui.md`) y el visual `galeria-pantallas` para 5.3.2; `19-make-report` genera para 5.3.2 el marcador de la galería con su explicación y para D.5 un marcador por pantalla (archivo sugerido `<UI-nn>.png`) con la suya, solo si coinciden con la tabla `UI` vigente.

### D9. Pruebas
Fixtures de `UI`, `PAN`, historias y `pantallas.json` de ejemplo; pruebas de la construcción, la validación (códigos, historias, bloques, plantilla, explicaciones), el modelo de cada plantilla (node) y su montaje (jsdom) con datos y vacíos, el `-update`, el pipeline (orden y nombre con letra) y el informe (marcadores de 5.3.2 y D.5).

## Risks / Trade-offs

- [Contenido de pantalla que parece inventado] → se propone a partir de historias, criterios y dominio, el usuario lo confirma y la procedencia solo consta en el `README.md`.
- [La tabla `UI` cambia en 14 después de crear los mockups] → la validación lo informa y el `-update` resincroniza.
- [Lista cerrada de bloques limita el diseño] → cubre las pantallas típicas de una app de gestión; agregar un bloque es agregar una entrada a la lista y a la plantilla.
- [Nombre con letra rompe la convención] → se registra en el esquema como excepción para pasos intercalados; evita renumerar cinco skills y sus referencias.

## Migration Plan

Se agregan el paso, las plantillas y las reglas; se cambian los encabezados de `sis-3` y el índice. No hay corridas en `project/` que migrar.

## Open Questions

- Si más adelante conviene exportar `pantallas.json` a Figma por MCP.
