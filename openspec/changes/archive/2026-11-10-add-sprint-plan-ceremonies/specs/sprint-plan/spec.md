## Purpose
Define la planificación de sprints y el Gantt de línea base del proyecto (puntos 4.6.1 y 4.6.2 del informe): el playbook ampliado y sus plantillas, la skill que reparte el backlog en los tres sprints, el esquema de datos del cronograma y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos de la planificación
`common/scrum/guia.md` SHALL incluir las secciones de planificación de sprints y de Gantt de línea base (con errores frecuentes y checklist) sin renumerar las de roles y artefactos, y `common/scrum/models/` SHALL incluir `spr-1-plan-sprints.md` y `spr-2-gantt-linea-base.md`, cada una con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `11-make-sprint-plan` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Playbook previo intacto
- **WHEN** se compara la guía con la de la configuración de Scrum
- **THEN** las secciones de roles y artefactos conservan su numeración

### Requirement: Fuentes y prerrequisitos
La skill SHALL leer el backlog vigente de `10-make-user-stories`, la configuración de Scrum vigente, el equipo y los tres avances del config y, si existe, el plan Lean vigente; SHALL exigir las tres fechas de avance y, si falta alguna, indicar `00-init-update` sin generar el plan.

#### Scenario: Fecha de avance pendiente
- **WHEN** el config tiene el avance 2 sin fecha
- **THEN** la skill lo informa, indica `00-init-update` y no genera el plan

#### Scenario: Sin backlog
- **WHEN** el config no tiene corrida de `10-make-user-stories`
- **THEN** la skill lo avisa y ofrece ejecutarla antes de continuar

### Requirement: Plan y confirmación antes de escribir
La skill SHALL preguntar la fecha de inicio del proyecto y la capacidad de cada sprint, proponer el reparto de historias, el objetivo de cada sprint y las tareas del Gantt, mostrar el plan completo y esperar la confirmación antes de crear archivos.

#### Scenario: Backlog que no cabe
- **WHEN** la suma de las historias supera la capacidad de los tres sprints
- **THEN** la skill propone diferir las de menor prioridad con su motivo y espera la decisión del usuario

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/sprint-plan/<DD-MM-AAAA-HH-MM-SS>/` con `plan-sprints.md` (punto 4.6.1), `gantt-linea-base.md` (punto 4.6.2), `gantt.json` y `README.md`, y SHALL registrarla en el paso `11-make-sprint-plan` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene los cuatro archivos y el config la registra

### Requirement: Sprints y fechas
`plan-sprints.md` SHALL tener tres sprints cuyo fin coincida con la fecha de su avance en el config, cuyo primer inicio sea el del proyecto y cuyos inicios siguientes sean el día posterior al fin del sprint anterior, cada uno con una capacidad en puntos y un objetivo del sprint.

#### Scenario: Sprint que no termina en la fecha del avance
- **WHEN** el sprint 2 termina el 20-12-2026 y el config indica 31-12-2026
- **THEN** la validación informa el sprint y las dos fechas

### Requirement: Reparto de historias
Cada historia del backlog vigente SHALL asignarse a un sprint o figurar como diferida con motivo; la suma de las estimaciones de cada sprint SHALL no superar su capacidad, y una historia SHALL asignarse a un sprint no anterior al de las historias de las que depende.

#### Scenario: Sprint sobrecargado
- **WHEN** el sprint 1 tiene 14 puntos y su capacidad es 13
- **THEN** la validación informa el sprint, la carga y la capacidad

#### Scenario: Dependencia invertida
- **WHEN** `HU-03` depende de `HU-02` y está en un sprint anterior
- **THEN** la validación informa las dos historias

### Requirement: Gantt de línea base
`gantt-linea-base.md` SHALL listar tareas `TAR-nn` con su historia (o «—» si es una tarea del proyecto), sprint, inicio, fin, predecesoras y responsable; las fechas SHALL caer dentro del sprint de la tarea, cada historia asignada SHALL tener al menos una tarea y las predecesoras SHALL existir, terminar antes de que empiece la tarea y no formar ciclos.

#### Scenario: Tarea fuera de su sprint
- **WHEN** una tarea del sprint 1 termina después del fin del sprint 1
- **THEN** la validación informa la tarea y las fechas

#### Scenario: Ciclo de dependencias
- **WHEN** `TAR-04` depende de `TAR-05` y `TAR-05` de `TAR-04`
- **THEN** la validación informa el ciclo

### Requirement: Esquema de gantt.json
`gantt.json` SHALL tener `schema`, `proyecto`, `sprints` (número, avance, inicio, fin, capacidad y objetivo) y `tareas` (código, nombre, historia, sprint, inicio, fin, predecesoras y responsable) con fechas ISO, y SHALL coincidir exactamente con las tablas de `plan-sprints.md` y `gantt-linea-base.md`.

#### Scenario: JSON desalineado
- **WHEN** `gantt.json` tiene para `TAR-02` una fecha distinta de la del markdown
- **THEN** la validación informa la tarea y la diferencia

### Requirement: Cantidades de referencia
El playbook SHALL dar cantidades de referencia (dos a cuatro tareas por historia y un hito de entrega por avance) que no son normas, y la skill SHALL avisar en una línea cuando una elección las supere o no las alcance y SHALL dejar la decisión al usuario.

#### Scenario: Historia con ocho tareas
- **WHEN** el usuario pide ocho tareas para una historia
- **THEN** la skill avisa que el rango de referencia es de dos a cuatro y respeta su decisión

### Requirement: Validación del plan de sprints
La validación SHALL comprobar la estructura de los archivos, la coherencia con el config, con el backlog vigente y con la configuración de Scrum vigente, los puntos del índice, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Historia inexistente
- **WHEN** el plan asigna `HU-09` y el backlog vigente no la define
- **THEN** la validación informa el código y la corrida

### Requirement: Skill 11-make-sprint-plan-update
La skill `11-make-sprint-plan-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (mover historias, capacidad, dependencias, tareas, fechas de tareas, objetivos), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado, mantener `gantt.json` igual a las tablas y validar.

#### Scenario: Mover una historia de sprint
- **WHEN** el usuario mueve `HU-03` del sprint 2 al 3
- **THEN** la copia actualiza el reparto, sus tareas y fechas y `gantt.json`, y avisa de las ceremonias y el tablero que citan esas tareas

#### Scenario: Cambio de fechas de avance
- **WHEN** el usuario pide cambiar la fecha de un avance
- **THEN** la skill indica `00-init-update` y luego una corrida nueva o un update para recalcular los sprints

### Requirement: Texto limpio en el plan de sprints
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Objetivo del sprint
- **WHEN** el plan describe el objetivo de un sprint
- **THEN** usa contenido del proyecto sin etiquetas de procedencia
