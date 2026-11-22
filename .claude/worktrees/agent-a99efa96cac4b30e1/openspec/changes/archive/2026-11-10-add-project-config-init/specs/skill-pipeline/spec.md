# Spec Delta

## Purpose

Define el esquema de nombres, el orden y los prerrequisitos de las skills del proyecto y los principios comunes que cumple toda skill de generación: preguntar lo necesario, confirmar las propuestas y crear su propio playbook con modelos y formularios.

## ADDED Requirements

### Requirement: Esquema de nombres de skills
Las skills del proyecto SHALL llamarse `[orden de dos dígitos]-[verbo]-[nombre]`, con los verbos `init`, `make` y `design`, y con el sufijo `-update` si son la homóloga de actualización de otra skill, sin letras ni otros marcadores.

#### Scenario: Nombre de una skill de actualización
- **WHEN** se nombra la homóloga de actualización de `05-make-design-thinking`
- **THEN** se llama `05-make-design-thinking-update` y conserva el número de su skill

### Requirement: Orden de las skills
El orden de ejecución de las skills SHALL ser una secuencia fija de veinte pasos, de `00-init` a `19-make-report`, definida en `pipeline.json`.

#### Scenario: Secuencia completa
- **WHEN** se consulta `pipeline.json`
- **THEN** lista en orden `00-init`, `01-design-system`, `02-make-initial-lean-canvas`, `03-make-company-chapter`, `04-make-methodological-framework`, `05-make-design-thinking`, `06-make-design-thinking-prototypes`, `07-make-lean-plan`, `08-make-scrum-setup`, `09-make-requirements`, `10-make-user-stories`, `11-make-sprint-plan`, `12-make-ceremonies-kanban`, `13-design-html-boards`, `14-make-system-design`, `15-make-implementation-log`, `16-make-sprint-report`, `17-make-lean-results`, `18-make-final-analysis` y `19-make-report`

#### Scenario: Listado de las skills
- **WHEN** se listan las carpetas de `.claude/skills/` ordenadas por nombre
- **THEN** las skills del proyecto aparecen en el orden de ejecución

### Requirement: Skills sin homóloga de actualización
`00-init` y `19-make-report` SHALL NOT tener homóloga `-update`: el config se edita o se vuelve a ejecutar `00-init`, y el armado del informe se ejecuta de nuevo cada vez.

#### Scenario: Corrección del armado del informe
- **WHEN** el usuario necesita rehacer el documento de un avance
- **THEN** ejecuta de nuevo `19-make-report` en lugar de una skill de actualización

### Requirement: Prerrequisitos entre pasos
El kit compartido SHALL declarar en `pipeline.json` el orden, la carpeta y los prerrequisitos de cada skill, y cada skill SHALL comprobar en el config que los pasos anteriores que ya existen como skill estén hechos y avisar al usuario de los que falten, sin bloquear la ejecución.

#### Scenario: Paso anterior sin hacer
- **WHEN** el usuario ejecuta una skill cuyo prerrequisito instalado no tiene corrida en el config
- **THEN** la skill avisa cuál falta y pregunta si continúa

#### Scenario: Prerrequisito aún no creado
- **WHEN** un prerrequisito todavía no existe como skill
- **THEN** la comprobación lo omite y no avisa

### Requirement: Preguntar y confirmar
Toda skill de generación SHALL preguntar al usuario lo que necesite y no esté en el config, y SHALL presentar sus propuestas (por ejemplo roles, sprints o historias) para que el usuario las acepte, rechace o corrija antes de generar.

#### Scenario: Propuesta rechazada
- **WHEN** el usuario rechaza una propuesta
- **THEN** la skill la ajusta con sus correcciones y vuelve a presentarla antes de continuar

### Requirement: Playbook propio con modelos y formularios
Toda skill de generación que necesite un método SHALL apoyarse en un playbook propio en `common/<tema>/guia.md` con sus plantillas en `common/<tema>/models/`, con la misma estructura que el de Design Thinking: reglas, pasos, cantidades de referencia, formularios y checklist.

#### Scenario: Skill sin playbook
- **WHEN** se crea una skill de generación sin playbook
- **THEN** su creación incluye el playbook y las plantillas correspondientes

### Requirement: Ampliación del índice del informe
Cuando una skill requiera puntos o anexos que el índice (`common/structure/model1.md`) no contempla, el cambio que crea la skill SHALL ampliar el índice, respetando las secciones estables del Design Thinking y las letras de anexo existentes.

#### Scenario: Skill que necesita un anexo nuevo
- **WHEN** una skill produce evidencias que no caben en los anexos actuales
- **THEN** su cambio agrega el anexo al índice con su marca de avance
