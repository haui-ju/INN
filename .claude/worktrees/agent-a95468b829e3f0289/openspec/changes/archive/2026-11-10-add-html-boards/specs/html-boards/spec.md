## Purpose
Define los tableros HTML del proyecto (Gantt y Kanban): su playbook y modelos, las skills que los generan y actualizan a partir del plan y el tablero vigentes y del sistema de diseño, el esquema de datos con la línea base y el estado real, los indicadores calculados y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos de los tableros HTML
El repositorio SHALL incluir `common/html-boards/guia.md` y `common/html-boards/models/` con `html-1-gantt.md`, `html-2-kanban.md`, `html-3-esquema-datos.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist; la guía SHALL cubrir las reglas del HTML autónomo, el contenido de cada tablero, la separación de línea base y estado, los cálculos, las capturas y la publicación opcional.

#### Scenario: Skill que necesita el formato
- **WHEN** `13-design-html-boards` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer el plan de sprints vigente (`gantt.json`), el tablero vigente (`tablero.json`), los tokens del sistema de diseño al que apunta `diseno` y el config; cada tablero SHALL generarse solo si existe su fuente, y si falta el sistema de diseño SHALL avisarlo y usar los tokens base de `01-design-system`.

#### Scenario: Sin sistema de diseño
- **WHEN** `diseno` está vacío en el config
- **THEN** la skill lo avisa, ofrece `01-design-system` y, si continúa, usa los tokens base y lo anota en el `README.md`

#### Scenario: Sin tablero Kanban
- **WHEN** el config no tiene corrida de `12-make-ceremonies-kanban`
- **THEN** la skill genera solo el Gantt y avisa que el Kanban necesita ese paso

### Requirement: Plan y confirmación antes de escribir
La skill SHALL preguntar la fecha de corte y el estado real (avance de las tareas, columna de las tarjetas y fechas reales) o si se muestra solo la línea base, presentar un resumen con los indicadores resultantes y esperar la confirmación antes de crear archivos.

#### Scenario: Solo línea base
- **WHEN** el usuario no tiene avance que informar
- **THEN** la skill genera los tableros con 0 % de avance y todas las tarjetas en la columna inicial, sin fecha de corte

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/html-boards/<DD-MM-AAAA-HH-MM-SS>/` con `gantt.html`, `kanban.html` (los que correspondan), `data.json` y `README.md`, y SHALL registrarla en el paso `13-design-html-boards` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el resumen
- **THEN** la corrida contiene los tableros pedidos, `data.json` y el `README.md`, y el config la registra

### Requirement: Datos y estado real
`data.json` SHALL contener `schema`, `proyecto`, `fecha_corte`, `diseno`, la línea base copiada sin cambios (`gantt` y `tablero`), el `estado` real (por tarea: avance de 0 a 100 y fechas reales; por tarjeta: columna y fechas de entrada a la primera columna de trabajo y de llegada a la final) y lo `calculado`, y SHALL coincidir con el plan y el tablero vigentes.

#### Scenario: Línea base desalineada
- **WHEN** el plan vigente tiene una tarea que `data.json` no incluye
- **THEN** la validación informa el código y que hay que resincronizar con el `-update`

#### Scenario: Estado incoherente
- **WHEN** una tarea tiene avance 100 y su tarjeta no está en la columna final
- **THEN** la validación informa la tarea y la tarjeta

### Requirement: Indicadores calculados
El kit SHALL calcular el avance global y por sprint, las tareas hechas, el tiempo de ciclo promedio en días, el rendimiento por semana, la cantidad de tarjetas por columna comparada con su límite WIP y las tareas atrasadas, y la validación SHALL recalcularlos y exigir que coincidan con `data.json` y con lo mostrado en el HTML.

#### Scenario: Indicador desactualizado
- **WHEN** `calculado` indica 3 tareas hechas y el estado tiene 4
- **THEN** la validación informa el indicador y los dos valores

### Requirement: HTML autónomo con el sistema de diseño
Cada HTML SHALL ser un único archivo que funciona sin conexión y sin recursos externos, usar como variables CSS los tokens de color claro y oscuro, alternar entre ambos temas, adaptarse a pantalla de teléfono sin desplazamiento horizontal de la página y llevar embebido `data.json`.

#### Scenario: Recurso externo
- **WHEN** un HTML carga un script o una hoja de estilos externa
- **THEN** la validación informa el archivo y el recurso

#### Scenario: Color distinto al token
- **WHEN** una variable `--c-acento` tiene un valor que no es el de los tokens
- **THEN** la validación informa la variable

### Requirement: Contenido del Gantt
`gantt.html` SHALL mostrar los tres sprints con sus fechas y capacidad, cada tarea como una barra en su fecha con su avance real marcado, los hitos, las predecesoras, el responsable y la historia, y una marca de la fecha de corte.

#### Scenario: Tarea ausente
- **WHEN** una tarea del plan no aparece en el HTML
- **THEN** la validación informa el código

### Requirement: Contenido del Kanban
`kanban.html` SHALL mostrar las columnas con sus tarjetas, el contador de cada columna frente a su límite WIP con una indicación visible cuando se supera, y las métricas definidas con sus valores a la fecha de corte.

#### Scenario: WIP superado
- **WHEN** hay 4 tarjetas en una columna con límite 3
- **THEN** el tablero marca la columna como superada y muestra 4 de 3

### Requirement: Fecha de corte visible
Cada tablero SHALL mostrar de forma destacada «al DD-MM-AAAA» cuando hay fecha de corte, o «Línea base» cuando no la hay, de modo que una captura del tablero quede fechada.

#### Scenario: Captura para el informe
- **WHEN** el usuario captura el tablero para 6.1.4
- **THEN** la captura incluye la fecha de corte

### Requirement: Validación de los tableros
La validación SHALL comprobar `data.json` contra el plan y el tablero vigentes, el estado, los indicadores, los HTML (autonomía, tokens, datos embebidos iguales a `data.json`, tareas y tarjetas presentes, fecha de corte), los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Datos embebidos distintos
- **WHEN** el JSON embebido en `kanban.html` difiere de `data.json`
- **THEN** la validación informa el archivo

### Requirement: Publicación privada opcional
Tras validar, la skill SHALL ofrecer publicar una vista privada de un tablero con Artifact, SHALL hacerlo solo con la confirmación explícita del usuario para ese tablero y SHALL anotar el enlace en el `README.md` de la corrida y no en el config.

#### Scenario: El usuario no quiere publicar
- **WHEN** el usuario rechaza la publicación
- **THEN** la skill no publica nada y no vuelve a ofrecerla en esa ejecución

### Requirement: Skill 13-design-html-boards-update
La skill `13-design-html-boards-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (estado real, fecha de corte, resincronizar con el plan y el tablero, cambiar de diseño), mostrar el plan con los archivos afectados, esperar confirmación, editar `data.json`, volver a generar los HTML y validar.

#### Scenario: Actualizar el avance
- **WHEN** el usuario informa que `TAR-05` está al 60 % y la fecha de corte nueva
- **THEN** la copia actualiza `estado`, recalcula los indicadores, regenera los HTML y deja el resto idéntico a la base

#### Scenario: Cambió el diseño
- **WHEN** el config apunta a un sistema de diseño nuevo
- **THEN** la copia regenera los HTML con sus tokens sin tocar el estado

### Requirement: Texto limpio en los tableros
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Tarjeta de un tablero
- **WHEN** el tablero muestra el título de una tarea
- **THEN** usa el texto del plan sin etiquetas de procedencia
