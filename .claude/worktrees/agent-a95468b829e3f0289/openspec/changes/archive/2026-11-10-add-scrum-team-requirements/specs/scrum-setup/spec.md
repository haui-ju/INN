## Purpose
Define la configuración de Scrum del proyecto (puntos 4.1.1 y 4.1.2 del informe): el playbook y sus modelos, la skill que reparte los roles y define la cadencia y los artefactos, la escritura de los roles en el config y su validación.

## ADDED Requirements

### Requirement: Playbook y modelos de Scrum
El repositorio SHALL incluir `common/scrum/guia.md` (roles, artefactos y compromisos, cadencia de tres sprints, reglas para repartir roles entre cuatro personas, errores frecuentes, checklist y referencias) y `common/scrum/models/` con `scr-1-equipo-roles.md`, `scr-2-artefactos.md` y un `README.md`, cada plantilla con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: Skill que necesita el formato
- **WHEN** `08-make-scrum-setup` va a escribir un archivo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

#### Scenario: Playbook ampliable
- **WHEN** el cambio de planificación añade sprints y ceremonias
- **THEN** amplía `common/scrum/guia.md` sin renumerar las secciones de roles y artefactos

### Requirement: Propuesta y confirmación del reparto de roles
La skill SHALL leer el equipo y los avances del config, proponer un reparto (con cuatro personas, un Product Owner, un Scrum Master y dos del equipo de desarrollo), preguntar si hay un interesado externo y qué integrantes también desarrollan, y esperar la confirmación antes de escribir nada.

#### Scenario: Cuatro integrantes
- **WHEN** el config tiene cuatro integrantes sin rol
- **THEN** la skill propone un reparto 1-1-2 y lo ajusta según la respuesta del usuario

#### Scenario: Equipo distinto
- **WHEN** el equipo tiene tres integrantes
- **THEN** la skill propone un reparto válido de tres y avisa que el equipo de desarrollo queda reducido

### Requirement: Roles en el config
Tras la confirmación, la skill SHALL escribir los roles en `equipo[].rol` del config con la función del kit, y SHALL informar si el config rechazó el reparto sin dejar archivos a medias.

#### Scenario: Roles confirmados
- **WHEN** el usuario confirma el reparto
- **THEN** el config queda con el rol de cada integrante y la corrida se registra

### Requirement: Estructura de salida
La skill SHALL crear cada corrida en `project/scrum-setup/<DD-MM-AAAA-HH-MM-SS>/` con `equipo-scrum.md` (punto 4.1.1), `artefactos.md` (punto 4.1.2) y `README.md`, y SHALL registrarla en el paso `08-make-scrum-setup` del config al terminar.

#### Scenario: Corrida nueva
- **WHEN** el usuario confirma el plan
- **THEN** la corrida contiene los tres archivos y el config la registra

### Requirement: Configuración del equipo Scrum
`equipo-scrum.md` SHALL listar a cada integrante del config con su rol, si también desarrolla y sus responsabilidades; SHALL tener exactamente un Product Owner, exactamente un Scrum Master y al menos un integrante del equipo de desarrollo, y los nombres y roles SHALL coincidir con los del config.

#### Scenario: Rol distinto al del config
- **WHEN** la tabla asigna a un integrante un rol diferente del que tiene el config
- **THEN** la validación informa el nombre y la diferencia

#### Scenario: Integrante ausente
- **WHEN** un integrante del config no figura en la tabla
- **THEN** la validación lo informa

### Requirement: Cadencia de sprints y avances
`equipo-scrum.md` SHALL incluir una tabla de tres filas que relacione cada sprint con su avance y con la fecha de entrega del config, de modo que sprint N corresponda al avance N.

#### Scenario: Fecha distinta
- **WHEN** la tabla indica una fecha de avance distinta de la del config
- **THEN** la validación informa el avance y las dos fechas

### Requirement: Artefactos de Scrum
`artefactos.md` SHALL describir el Product Backlog (compromiso: objetivo del producto), el Sprint Backlog (compromiso: objetivo del sprint) y el Incremento (compromiso: Definition of Done), con su responsable y los puntos del informe donde se desarrolla, y SHALL formular el objetivo del producto a partir de `resultado_esperado` del config.

#### Scenario: Compromiso incorrecto
- **WHEN** el Incremento figura con el compromiso «objetivo del sprint»
- **THEN** la validación informa el artefacto y el compromiso esperado

### Requirement: Validación de la configuración de Scrum
La validación SHALL comprobar la estructura de ambos archivos, la coherencia con el config, que los puntos del informe citados existan en `common/structure/model1.md`, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Dos Scrum Master
- **WHEN** la tabla tiene dos Scrum Master
- **THEN** la validación informa el archivo y la causa

### Requirement: Skill 08-make-scrum-setup-update
La skill `08-make-scrum-setup-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (roles, quién también desarrolla, responsabilidades, artefactos), mostrar el plan con los archivos afectados, esperar confirmación, editar solo lo afectado, actualizar los roles del config si cambian y validar.

#### Scenario: Cambio de Product Owner
- **WHEN** el usuario cambia quién es Product Owner
- **THEN** la copia actualiza la tabla de equipo y los roles del config, y el resto queda idéntico a la base

#### Scenario: Cambio de fechas
- **WHEN** el usuario pide cambiar la fecha de un avance
- **THEN** la skill indica que se hace con `00-init-update` y luego se vuelve a generar la cadencia

### Requirement: Texto limpio en la configuración de Scrum
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba o simulados.

#### Scenario: Responsabilidades del equipo
- **WHEN** la tabla describe las responsabilidades de un rol
- **THEN** usa texto del proyecto sin etiquetas de procedencia
