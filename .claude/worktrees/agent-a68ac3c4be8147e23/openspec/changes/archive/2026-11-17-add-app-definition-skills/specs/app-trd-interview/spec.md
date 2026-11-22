## Purpose
Define la skill que realiza la entrevista técnica de la app y genera los documentos de requisitos técnicos (TRD) por componente, la sección común de despliegue y CI y el esquema de datos, preguntando solo lo que aún no está decidido.

## ADDED Requirements

### Requirement: Playbook y modelos de la definición técnica
El repositorio SHALL incluir `common/app-technical-definition/guia.md` y `common/app-technical-definition/models/` con plantillas para el TRD común, el TRD de cada componente (`frontend`, `backend`, `database`, `openrpa`), el esquema de datos y un `README.md`, además del catálogo de preguntas por componente con sus opciones y ventajas y desventajas.

#### Scenario: Catálogo de preguntas
- **WHEN** se revisa la guía
- **THEN** cada componente tiene su lista de preguntas con al menos dos opciones y una recomendación por defecto

### Requirement: Decisiones ya tomadas antes de preguntar
La skill SHALL construir antes de preguntar una tabla de decisiones con su estado (`decided` u `open`) a partir de `override.md`, las decisiones `ADR-nn`, los RNF y la definición de producto vigente, SHALL mostrársela al usuario y SHALL preguntar solo las decisiones `open`; una decisión `decided` SHALL copiarse al TRD con su fuente.

#### Scenario: Stack ya fijado
- **WHEN** `override.md` y `ADR-01` fijan Python, LangGraph y Docker en AWS App Runner
- **THEN** esas decisiones aparecen como `decided` con su fuente y la skill no las vuelve a preguntar

#### Scenario: Decisión abierta
- **WHEN** nadie ha fijado el ORM, el linter ni el formateador del backend
- **THEN** la skill pregunta esas tres decisiones y propone para cada una opciones y una recomendación

### Requirement: Entrevista técnica mínima por componente
La entrevista SHALL cubrir, para cada componente confirmado: **frontend** (empaquetador, lenguaje, framework, frontend único o micro-frontends); **backend** (servicio único o microservicios, lenguaje, framework, empaquetado, Docker u otra herramienta, linter, formateador); **base de datos** (motor, alojamiento en contenedor con el backend, aparte o ya existente, ORM o acceso a datos, caché); y **robot** (herramienta, programación, entradas y salidas).

#### Scenario: Preguntas del backend
- **WHEN** el backend está confirmado y ninguna de sus decisiones está fijada
- **THEN** la skill pregunta servicio único o microservicios, lenguaje, framework, empaquetado, Docker, linter y formateador

### Requirement: Entrevista técnica común y recomendaciones
La entrevista SHALL cubrir además, en común, el destino de despliegue (AWS, Cloudflare, Vercel, contenedores o híbrido), la integración continua (GitHub Actions, Jenkins u otra), el almacenamiento y cómputo adicionales (S3, EC2) y la necesidad de herramientas de scraping. Para cada pregunta, la skill SHALL dar una recomendación razonada con el contexto del proyecto, y el usuario SHALL poder aceptarla con una respuesta corta.

#### Scenario: Base de datos existente
- **WHEN** el usuario indica que ya tiene una base de datos alojada
- **THEN** la skill pide solo el enlace o el nombre del servicio, lo registra sin credenciales y omite las preguntas de alojamiento

#### Scenario: Aceptar la recomendación
- **WHEN** el usuario responde «recomendado» a una pregunta
- **THEN** la skill registra la opción recomendada como decisión con su motivo

#### Scenario: Componente sin frontend
- **WHEN** el proyecto no tiene frontend
- **THEN** la skill no hace las preguntas de frontend ni genera su TRD

### Requirement: Sin secretos en los documentos
Los documentos SHALL listar las variables de entorno que cada componente necesita (nombre, propósito y quién provee el valor) sin escribir ningún valor, y la skill NO SHALL pedir ni guardar contraseñas, claves ni tokens.

#### Scenario: Servicio con clave
- **WHEN** el backend usa un modelo de lenguaje de pago
- **THEN** el TRD lista `OPENAI_API_KEY` con su propósito y indica que la provee el usuario, sin valor

### Requirement: Propuesta y confirmación antes de escribir
La skill SHALL presentar el resumen de decisiones (las `decided` y las respondidas) y los documentos que generará, y SHALL esperar la confirmación del usuario antes de escribir; si el usuario corrige una decisión, SHALL ajustarla y volver a presentar el resumen.

#### Scenario: Corrección antes de escribir
- **WHEN** el usuario cambia el formateador en el resumen
- **THEN** la skill lo ajusta y presenta el resumen otra vez sin escribir archivos

### Requirement: Estructura de salida de la definición técnica
La skill SHALL escribir en la corrida de definición vigente del proyecto, copiada como nueva corrida de `project/app/definition/`, `common/trd.md` (despliegue, CI, entornos y variables compartidas), un `trd.md` por componente confirmado y el esquema de datos en `database/data-schema.md` si existe el componente `database` o en `backend/data-schema.md` en caso contrario, y SHALL registrar la corrida en el config. Los nombres y el contenido SHALL estar en inglés y el `README.md` en español.

#### Scenario: Proyecto con base de datos
- **WHEN** hay backend, base de datos y robot
- **THEN** existen `common/trd.md`, `backend/trd.md`, `database/trd.md`, `openrpa/trd.md` y `database/data-schema.md`

### Requirement: TRD coherente con las decisiones de arquitectura
Cada TRD SHALL citar la `ADR-nn` o el RNF que respalda cada decisión técnica que corresponda; una decisión del usuario que contradiga una `ADR-nn` SHALL señalarse como conflicto y resolverse con el usuario antes de escribir, proponiendo `14-make-system-design-update` cuando cambie la arquitectura.

#### Scenario: Conflicto con una ADR
- **WHEN** el usuario elige microservicios y `ADR-03` fija un solo backend
- **THEN** la skill lo informa como conflicto y pregunta si se cambia la decisión o se mantiene la `ADR-03`

### Requirement: Esquema de datos
`data-schema.md` SHALL describir, para cada tabla `TBL-nn` del diseño del sistema, sus campos con tipo, clave y restricciones, sus índices, sus relaciones con cardinalidad y el flujo de vida de sus datos (quién la escribe, quién la lee, cuándo y con qué retención), y SHALL cubrir todas las tablas del diseño del sistema.

#### Scenario: Tabla sin flujo
- **WHEN** una tabla del diseño del sistema no tiene quién la escribe ni quién la lee
- **THEN** la validación informa la tabla

#### Scenario: Tabla no documentada
- **WHEN** `TBL-07` existe en el diseño del sistema y no está en el esquema
- **THEN** la validación informa la tabla ausente

### Requirement: Validación de la definición técnica
La validación SHALL comprobar la estructura, que cada componente tenga su TRD y solo ellos, que no haya decisiones `open` sin respuesta, que las citas `ADR`, `RNF` y `TBL` existan, que no haya valores de secretos en los documentos, los enlaces y el texto limpio, e informar cada incidencia con archivo y causa.

#### Scenario: Secreto escrito
- **WHEN** un TRD contiene una cadena con forma de clave de API
- **THEN** la validación informa el archivo

### Requirement: Skill 22-make-app-technical-definition-update
La skill `22-make-app-technical-definition-update` SHALL tomar la corrida base del config (o la que indique el usuario), bifurcarla, pedir los cambios (una decisión técnica, un componente, una variable o el esquema), aplicarlos solo a los archivos afectados, validar y registrar el fork.

#### Scenario: Cambio de ORM
- **WHEN** el usuario cambia el ORM del backend
- **THEN** el fork modifica `backend/trd.md`, `database/trd.md` si lo cita y deja idénticos los demás archivos

### Requirement: Texto limpio en la definición técnica
Ningún archivo de la corrida, salvo su `README.md`, SHALL calificar los datos o ejemplos como falsos, inventados, de prueba, simulados o de relleno.

#### Scenario: Término prohibido
- **WHEN** un TRD usa un término prohibido
- **THEN** la validación lo informa con archivo y línea
