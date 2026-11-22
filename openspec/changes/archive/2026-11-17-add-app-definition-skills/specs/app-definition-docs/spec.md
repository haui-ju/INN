## Purpose
Define la skill que genera los documentos de producto de la app (PRD, APP-FLOW y brief de diseño) a partir de los requerimientos, las historias y el diseño del sistema, creando solo las carpetas de los componentes que el proyecto tiene.

## ADDED Requirements

### Requirement: Playbook y modelos de la definición de la app
El repositorio SHALL incluir `common/app-definition/guia.md` y `common/app-definition/models/` con una plantilla por documento (`prd.md`, `app-flow.md`, `design-brief.md`) y un `README.md`, con la estructura de los demás playbooks: reglas, pasos, cantidades de referencia, formularios y checklist.

#### Scenario: Skill sin playbook
- **WHEN** se revisa `21-make-app-definition`
- **THEN** su `SKILL.md` cita `common/app-definition/guia.md` y las plantillas existen

### Requirement: Fuentes y prerrequisitos de la definición
La skill SHALL leer la corrida vigente de requerimientos (RF y RNF), la de historias (HU y CA), la de diseño del sistema (componentes, decisiones `ADR-nn` y pantallas `UI-nn`), el brief, el config y, si existe, el archivo `override.md` con las decisiones de arquitectura ya fijadas por el usuario; si falta la corrida de requerimientos, historias o diseño del sistema, SHALL avisarlo y preguntar si continúa.

#### Scenario: Diseño del sistema ausente
- **WHEN** el config no tiene corrida de `14-make-system-design`
- **THEN** la skill avisa que falta y pregunta si continúa antes de generar

### Requirement: Detección y confirmación de componentes
La skill SHALL proponer la lista de componentes de la app (`frontend`, `backend`, `database`, `openrpa`) deducida de los componentes del diseño del sistema y de `override.md`, con el motivo de cada uno, y SHALL esperar la confirmación del usuario antes de escribir; solo se crearán las carpetas de los componentes confirmados.

#### Scenario: Proyecto solo de Telegram
- **WHEN** el diseño del sistema no tiene aplicación web y declara un bot de Telegram, un backend, PostgreSQL y un robot de OpenRPA
- **THEN** la propuesta lista `backend`, `database` y `openrpa`, no lista `frontend`, y tras la confirmación no se crea la carpeta `frontend/`

#### Scenario: Componente rechazado
- **WHEN** el usuario rechaza el componente `openrpa`
- **THEN** la skill lo quita, ajusta los documentos y vuelve a presentar la propuesta antes de escribir

### Requirement: Estructura de salida de la definición
La skill SHALL crear cada corrida en `project/app/definition/<DD-MM-AAAA-HH-MM-SS>/` con `common/prd.md`, `common/app-flow.md`, `common/design-brief.md` solo si hay interfaz propia, las subcarpetas de los componentes confirmados y un `README.md` en español con la procedencia, y SHALL registrarla en el config. Los nombres de carpetas y archivos SHALL estar en inglés.

#### Scenario: Corrida nueva
- **WHEN** termina la skill en un proyecto con backend, base de datos y robot
- **THEN** existen `common/prd.md`, `common/app-flow.md`, las carpetas `backend/`, `database/` y `openrpa/` y el `README.md`, y no existe `design-brief.md`

### Requirement: PRD
`prd.md` SHALL abrir con un resumen de la idea en pocas líneas y SHALL listar cada funcionalidad que se construye con un código `FEAT-nn`, su descripción, las historias `HU-nn` y los requerimientos `RF-nn` que la sustentan y su prioridad; las historias diferidas o fuera de alcance SHALL figurar en una sección «Out of scope» con su motivo.

#### Scenario: Historia diferida
- **WHEN** la corrida de historias difiere `HU-09` por capacidad
- **THEN** el PRD la lista en «Out of scope» con ese motivo y no como funcionalidad

#### Scenario: Funcionalidad sin sustento
- **WHEN** una `FEAT-nn` no cita ninguna `HU` ni `RF`
- **THEN** la validación informa la funcionalidad

### Requirement: APP-FLOW
`app-flow.md` SHALL describir el recorrido del usuario y, para cada punto de entrada, comando, botón o acción, qué lo dispara, qué hace el sistema exactamente, qué pantalla, mensaje o estado sigue y qué ocurre ante un error; cuando el canal es una conversación, SHALL cubrir cada comando y cada estado de la conversación. Cada historia `HU-nn` del alcance SHALL aparecer en al menos un flujo.

#### Scenario: Bot de Telegram
- **WHEN** el canal es un bot con los comandos `/start`, `/ayuda` y `/vendedor`
- **THEN** `app-flow.md` describe qué responde el bot a cada uno, el estado siguiente y el flujo de pedido, aclaración, resultados y derivación

#### Scenario: Historia sin flujo
- **WHEN** una historia del alcance no aparece en ningún flujo
- **THEN** la validación informa la historia

### Requirement: Brief de diseño condicionado a la interfaz
`design-brief.md` SHALL generarse solo si el proyecto tiene interfaz propia (frontend); SHALL describir aspecto y sensación, paleta, tipografía, componentes y estilos tomándolos del sistema de diseño vigente (`diseno` del config) y SHALL escribir «Undefined» en lo que no esté definido en lugar de inventarlo. Si no hay interfaz propia, la skill SHALL omitirlo y dejar la razón en el `README.md`.

#### Scenario: Sin interfaz propia
- **WHEN** el único canal es Telegram
- **THEN** no se genera `design-brief.md` y el `README.md` explica que el canal usa la interfaz de Telegram

#### Scenario: Con frontend y sistema de diseño
- **WHEN** hay frontend y el config apunta a un sistema de diseño
- **THEN** el brief cita su paleta, tipografías y componentes tal como están allí

### Requirement: Idioma de la definición
Los nombres de carpetas y archivos, los códigos y el contenido de los documentos SHALL estar en inglés; el `README.md` y todo texto que la skill muestre al usuario SHALL estar en español.

#### Scenario: Revisión de idioma
- **WHEN** se revisa una corrida
- **THEN** los documentos `.md` de `common/` y de los componentes están en inglés y el `README.md` en español

### Requirement: Validación de la definición
La validación SHALL comprobar la estructura, que las carpetas existentes correspondan a los componentes confirmados, que las citas `HU`, `RF`, `RNF`, `UI` y `ADR` existan en las corridas vigentes, la trazabilidad del PRD y del APP-FLOW, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Cita inexistente
- **WHEN** el PRD cita `HU-99` y la corrida de historias no la define
- **THEN** la validación informa el archivo y el código

### Requirement: Skill 21-make-app-definition-update
La skill `21-make-app-definition-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (funcionalidades, flujos, componentes o brief de diseño), aplicarlos solo a los archivos afectados, validar y registrar el fork.

#### Scenario: Cambio de un flujo
- **WHEN** el usuario corrige el flujo del comando `/vendedor`
- **THEN** el fork modifica `common/app-flow.md` y deja idénticos los demás archivos

### Requirement: Texto limpio en la definición
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba, simulados o de relleno.

#### Scenario: Término prohibido
- **WHEN** un documento usa un término prohibido
- **THEN** la validación lo informa con archivo y línea
