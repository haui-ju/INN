## Purpose
Define las ceremonias de Scrum y el diseño del tablero Kanban del proyecto (puntos 4.7 y 4.8 del informe): los playbooks y plantillas, la skill que los genera a partir del plan de sprints, el esquema de datos del tablero y su validación.

## ADDED Requirements

### Requirement: Playbooks y modelos de ceremonias y Kanban
`common/scrum/guia.md` SHALL incluir la sección de ceremonias sin renumerar las anteriores; `common/scrum/models/` SHALL incluir `spr-3-ceremonias.md`; y el repositorio SHALL incluir `common/kanban/guia.md` y `common/kanban/models/` con `kan-1-tablero.md`, `kan-2-wip-metricas.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `12-make-ceremonies-kanban` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Plantilla completa
- **WHEN** se revisa una plantilla de `models/`
- **THEN** contiene ficha, instrucciones, formato, ejemplo y checklist

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer el plan de sprints vigente (`gantt.json` y `plan-sprints.md`), la configuración de Scrum vigente y el config; si falta el plan SHALL avisarlo y ofrecer `11-make-sprint-plan`, porque las tarjetas del tablero son las tareas del Gantt y las fechas de las ceremonias salen de los sprints.

#### Scenario: Sin plan de sprints
- **WHEN** el config no tiene corrida de `11-make-sprint-plan`
- **THEN** la skill lo avisa, ofrece ejecutarlo y no genera el tablero sin tareas de origen

### Requirement: Plan y confirmación antes de escribir
La skill SHALL preguntar el horario y el medio de cada ceremonia, las columnas, políticas y límites de trabajo en curso del tablero y las métricas a seguir, proponer valores por defecto, mostrar el diseño completo y esperar la confirmación antes de crear archivos.

#### Scenario: Límite de trabajo mayor al equipo
- **WHEN** el usuario fija un límite de trabajo en curso de 10 con dos desarrolladores
- **THEN** la skill lo avisa y respeta su decisión

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/ceremonies-kanban/<DD-MM-AAAA-HH-MM-SS>/` con `ceremonias.md` (punto 4.7), `kanban.md` (punto 4.8), `tablero.json` y `README.md`, y SHALL registrarla en el paso `12-make-ceremonies-kanban` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el diseño
- **THEN** la corrida contiene los cuatro archivos y el config la registra

### Requirement: Ceremonias de Scrum
`ceremonias.md` SHALL describir Sprint Planning, Daily Scrum, Sprint Review y Sprint Retrospective, cada una con cuándo ocurre, duración, participantes, entradas y salidas, y un calendario con las fechas de Planning, Review y Retrospective de cada sprint.

#### Scenario: Ceremonia incompleta
- **WHEN** la descripción de la Daily Scrum no indica su duración
- **THEN** la validación informa la ceremonia y la etiqueta

### Requirement: Duraciones y fechas de las ceremonias
Las duraciones SHALL no superar los topes de la Guía de Scrum para un sprint de un mes (Planning 8 horas, Daily 15 minutos, Review 4 horas, Retrospective 3 horas); la Planning SHALL caer en el inicio de su sprint, y la Review y la Retrospective dentro de su sprint, la Retrospective no antes que la Review.

#### Scenario: Daily de una hora
- **WHEN** la Daily Scrum dura 60 minutos
- **THEN** la validación informa la duración y el tope

#### Scenario: Retrospective antes de la Review
- **WHEN** la Retrospective del sprint 2 es anterior a su Review
- **THEN** la validación informa las dos fechas

### Requirement: Columnas y políticas del tablero
`kanban.md` SHALL definir las columnas del tablero con su significado y sus políticas explícitas de entrada y de salida, con al menos una columna inicial, una de trabajo en curso y una final.

#### Scenario: Columna sin política
- **WHEN** una columna no tiene política de salida
- **THEN** la validación informa la columna

### Requirement: Límites de trabajo en curso
Cada columna de trabajo SHALL tener un límite WIP numérico mayor que cero con su motivo (código `WIP-nn`) y las columnas inicial y final SHALL declararse sin límite; los límites SHALL citar columnas definidas.

#### Scenario: Límite no numérico
- **WHEN** el límite de «En curso» es «pocos»
- **THEN** la validación informa el código y la causa

### Requirement: Métricas del tablero
`kanban.md` SHALL definir como mínimo el tiempo de ciclo y el rendimiento (códigos `MKB-nn`) con su definición, cómo se calcula, unidad y frecuencia, de acuerdo con el glosario del marco metodológico, y SHALL dejar sus valores reales para los informes de sprint.

#### Scenario: Métrica obligatoria ausente
- **WHEN** no está definido el rendimiento
- **THEN** la validación informa la métrica faltante

### Requirement: Esquema de tablero.json
`tablero.json` SHALL tener `schema`, `proyecto`, `columnas` (nombre, límite WIP y políticas), `metricas` (código, nombre y unidad) y `tarjetas` (una por cada tarea `TAR` del plan de sprints, con historia, sprint y columna inicial), y SHALL coincidir con `kanban.md` y con el `gantt.json` vigente.

#### Scenario: Tarjeta sin tarea
- **WHEN** `tablero.json` tiene una tarjeta `TAR-40` que el plan de sprints no define
- **THEN** la validación informa el código

#### Scenario: Tarea sin tarjeta
- **WHEN** el plan define `TAR-12` y el tablero no tiene su tarjeta
- **THEN** la validación informa el código

### Requirement: Validación de ceremonias y Kanban
La validación SHALL comprobar la estructura de los archivos, la coherencia con el plan de sprints y la configuración de Scrum vigentes, los puntos del índice, las citas, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Participante que no es del equipo
- **WHEN** una ceremonia lista a una persona que no pertenece al equipo del config
- **THEN** la validación informa el nombre

### Requirement: Skill 12-make-ceremonies-kanban-update
La skill `12-make-ceremonies-kanban-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (ceremonias, columnas, políticas, WIP, métricas o resincronización de tarjetas con el plan), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado, mantener `tablero.json` igual a `kanban.md` y validar.

#### Scenario: Plan de sprints cambió
- **WHEN** el plan vigente tiene tareas nuevas que el tablero no incluye
- **THEN** la copia agrega las tarjetas en la columna inicial y deja el resto idéntico a la base

#### Scenario: Cambio de WIP
- **WHEN** el usuario cambia el límite de «En curso»
- **THEN** la copia actualiza `kanban.md` y `tablero.json` y valida

### Requirement: Texto limpio en ceremonias y Kanban
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Política de columna
- **WHEN** el tablero describe la política de entrada de una columna
- **THEN** usa texto del proyecto sin etiquetas de procedencia
