## ADDED Requirements

### Requirement: Playbook y modelos de los mockups
El repositorio SHALL incluir `common/ui-mockups/guia.md` y `common/ui-mockups/models/` con `ui-1-pantallas.md` (esquema de `pantallas.json` y lista de bloques), `ui-2-inventario.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir el paso del prototipo a las pantallas finales, los bloques, los formatos y las reglas de contenido.

#### Scenario: Skill que necesita el formato
- **WHEN** `14b-make-ui-mockups` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer la tabla de pantallas finales `UI-nn` y los destinos de `PAN` de `interfaz.md` vigente, las historias vigentes, el tablero del prototipo y los tokens del sistema de diseño; sin `interfaz.md` SHALL detenerse e indicar `14-make-system-design`, y sin sistema de diseño SHALL avisarlo y usar los tokens base.

#### Scenario: Sin diseño del sistema
- **WHEN** el config no tiene corrida de `14-make-system-design`
- **THEN** la skill se detiene e indica ejecutar ese paso

#### Scenario: Sin sistema de diseño
- **WHEN** `diseno` está vacío en el config
- **THEN** la skill lo avisa, ofrece `01-design-system` y, si continúa, usa los tokens base y lo anota en el `README.md`

### Requirement: Propuesta y confirmación antes de escribir
La skill SHALL proponer por cada `UI-nn` su formato, su título y sus bloques a partir de la fila del `PAN` de origen, los cambios de la tabla `UI`, los hallazgos que la modifican y los criterios de aceptación de sus historias, con datos de ejemplo del dominio, mostrar el resumen y esperar la confirmación del usuario.

#### Scenario: Pantalla que viene de un PAN
- **WHEN** `UI-02` viene de `PAN-02` con destino «se modifica»
- **THEN** la propuesta parte de lo que `PAN-02` muestra, aplica los cambios de la tabla `UI` y usa los criterios de sus historias para los campos y las acciones

#### Scenario: Cambio pedido por el usuario
- **WHEN** el usuario pide que `UI-02` sea de escritorio y sin buscador
- **THEN** la skill ajusta la propuesta y vuelve a mostrar el resumen antes de escribir

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/ui-mockups/<DD-MM-AAAA-HH-MM-SS>/` con `pantallas.json`, `pantallas/<UI-nn>.html`, `galeria.html`, `leer-imagen/`, `inventario-ui.md` y `README.md`, y SHALL registrarla en el paso `14b-make-ui-mockups` del config.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el resumen
- **THEN** la corrida contiene un HTML por pantalla, la galería, las explicaciones, el inventario y el `README.md`, y el config la registra

### Requirement: Datos de las pantallas
`pantallas.json` SHALL contener por pantalla `codigo`, `nombre`, `formato` (`movil` o `escritorio`), `origen`, `destino`, `historias`, `req`, `cambios` y `bloques`, con código, nombre, origen, historias y cambios iguales a la fila `UI` de `interfaz.md` vigente.

#### Scenario: Pantalla ausente
- **WHEN** `interfaz.md` vigente tiene `UI-04` y `pantallas.json` no
- **THEN** la validación informa el código

#### Scenario: Historia sin cubrir
- **WHEN** la fila `UI-02` cita `HU-03` y la pantalla no la incluye en `historias`
- **THEN** la validación informa la pantalla y la historia

#### Scenario: Historia del backlog sin pantalla
- **WHEN** `HU-09` del backlog no figura en ninguna pantalla
- **THEN** la skill lo avisa sin bloquear, porque una historia puede no tener pantalla propia

### Requirement: Bloques de la interfaz
Cada pantalla SHALL componerse solo de bloques de la lista cerrada (`barra`, `buscador`, `chips`, `pestanas`, `lista`, `formulario`, `tarjeta`, `cuadricula`, `alerta`, `acciones`), cada uno con sus campos obligatorios, y SHALL llevar al menos una barra y una acción o un contenido de datos.

#### Scenario: Bloque desconocido
- **WHEN** una pantalla incluye un bloque `mapa`
- **THEN** la validación informa la pantalla y los tipos permitidos

### Requirement: Plantillas de pantalla y galería
`common/html/pantalla/` SHALL mostrar una pantalla dentro de un marco móvil o de escritorio con los tokens del sistema de diseño, y `common/html/galeria-pantallas/` SHALL mostrar todas en miniatura con su código, ambas con los botones de imagen, modo claro y oscuro y adaptación a teléfono.

#### Scenario: Botones de imagen
- **WHEN** se abre una pantalla o la galería
- **THEN** ofrece «Copiar imagen» y «Descargar imagen» con escala ×2, ×3 y ×4

#### Scenario: Sin datos
- **WHEN** se monta una plantilla con su versión vacía
- **THEN** muestra «Sin datos» sin errores

### Requirement: Explicación de cada imagen
La skill SHALL escribir `leer-imagen/<UI-nn>.md` y `leer-imagen/galeria.md` derivados solo de `pantallas.json`: qué pantalla es, qué historias y requerimientos resuelve, su `PAN` de origen y qué cambió, y qué acciones tiene; la galería indica cuántas pantallas se conservan, se modifican o son nuevas.

#### Scenario: Pantalla modificada
- **WHEN** `UI-02` viene de `PAN-02` con destino «se modifica»
- **THEN** su explicación cita `PAN-02` y los cambios

### Requirement: Validación de los mockups
La validación SHALL comprobar `pantallas.json` contra la tabla `UI` vigente, los bloques, que cada HTML sea la plantilla con solo el bloque de tokens (los de `diseno`) y el de datos sustituidos, que `leer-imagen/` e `inventario-ui.md` coincidan con los datos, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: HTML modificado a mano
- **WHEN** `pantallas/UI-01.html` tiene cambios fuera de los bloques de tokens y de datos
- **THEN** la validación informa el archivo y que debe volver a copiarse la plantilla

#### Scenario: Tabla UI cambió
- **WHEN** 14 tiene una corrida nueva con una pantalla más
- **THEN** la validación informa que `pantallas.json` está desalineado y sugiere el `-update`

### Requirement: Skill 14b-make-ui-mockups-update
La skill `14b-make-ui-mockups-update` SHALL bifurcar la corrida base, pedir los cambios (texto o dato de ejemplo, bloque, formato, resincronizar con la tabla `UI`, diseño), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado de `pantallas.json`, volver a construir lo que depende y validar, sin tocar lo demás.

#### Scenario: Cambiar un dato de ejemplo
- **WHEN** el usuario pide que el stock de una talla en `UI-02` sea 4 y no 2
- **THEN** solo cambian `pantallas.json`, `pantallas/UI-02.html`, la galería y las explicaciones que dependen del dato

#### Scenario: Cambió la tabla UI
- **WHEN** 14 agregó `UI-05`
- **THEN** la copia agrega la pantalla pidiendo su contenido y conserva el de las demás

### Requirement: Texto limpio en los mockups
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Dato de una lista
- **WHEN** una pantalla muestra una prenda de ejemplo
- **THEN** usa el texto sin etiquetas de procedencia
