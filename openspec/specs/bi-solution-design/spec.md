# bi-solution-design Specification

## Purpose
Define la skill `06-make-bi-solution` y su `-update`, que producen las secciones 2.1 a 2.3 del informe: la propuesta de solución en BI, la arquitectura por capas con su figura y las herramientas seleccionadas y sustentadas.

## Requirements

### Requirement: Playbook y modelos de la solución de BI
El repositorio SHALL incluir `common/06-bi-solution/guia.md` (capas de una arquitectura de BI, criterios para elegir herramientas, cómo vincular la propuesta con la problemática y los objetivos, errores frecuentes y checklist) y `common/06-bi-solution/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`.

#### Scenario: Skill que necesita el formato
- **WHEN** `06-make-bi-solution` va a escribir una sección
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

### Requirement: Fuentes de la skill
La skill SHALL leer el config, el brief vigente (usuarios, decisiones, fuentes previstas y objetivos) y la corrida vigente de `05-make-problem-objectives` (problemática central y objetivos), y SHALL avisar sin bloquear cuando falte alguna de ellas.

#### Scenario: Sin capítulo 1
- **WHEN** no hay corrida vigente de `05-make-problem-objectives`
- **THEN** la skill avisa que falta, indica ejecutarla y pregunta si continúa con lo que hay en el brief

### Requirement: Propuesta de solución en BI
La sección 2.1 SHALL describir qué decisiones apoya la solución, quiénes la usarán y cómo responde a la problemática central, con una tabla que vincule cada objetivo específico `OE-nn` con el componente de la solución que lo atiende.

#### Scenario: Objetivo sin componente
- **WHEN** un `OE` del brief no aparece en la tabla de la propuesta
- **THEN** la validación informa el código del objetivo

### Requirement: Arquitectura de BI por capas
La sección 2.2 SHALL describir la arquitectura en cuatro capas en este orden: fuentes, ETL, almacenamiento y visualización, con una tabla `CAP-nn` por componente (capa, componente, función y entrada y salida) y una figura `arquitectura-bi` marcada con `<!-- figura: arquitectura-bi -->`.

#### Scenario: Capa ausente
- **WHEN** la tabla de arquitectura no tiene ningún componente de la capa de almacenamiento
- **THEN** la validación informa la capa que falta

#### Scenario: Fuente del brief no usada
- **WHEN** una fuente `FUE-nn` del brief no figura en la capa de fuentes
- **THEN** la validación informa el código de la fuente

### Requirement: Herramientas sustentadas
La sección 2.3 SHALL listar cada herramienta con su capa, su función en el proyecto, la justificación de su elección y la alternativa que se descartó; Power BI SHALL figurar en la capa de visualización y las herramientas de ETL y de almacenamiento MAY quedar «Pendiente» mientras el usuario no las decida.

#### Scenario: Herramienta sin justificación
- **WHEN** una herramienta no tiene justificación
- **THEN** la validación informa la herramienta

#### Scenario: Herramienta de ETL pendiente
- **WHEN** el usuario aún no decide la herramienta de ETL
- **THEN** la fila queda «Pendiente», la validación no la marca como error y la skill indica que se completa con `06-make-bi-solution-update`

### Requirement: Salida de la corrida de la solución
La skill SHALL crear cada corrida en `project/06-bi-solution/<DD-MM-AAAA-HH-MM-SS>/` según el contrato de las corridas de contenido: `secciones/2.1.md`, `secciones/2.2.md` y `secciones/2.3.md` con su encabezado exacto, `visuales/arquitectura-bi.html`, `leer-imagen/arquitectura-bi.md`, `referencias.md` si cita fuentes y `README.md`, y SHALL registrarla con `register`.

#### Scenario: Corrida registrada
- **WHEN** la corrida pasa la validación y se registra
- **THEN** las secciones 2.1, 2.2 y 2.3 quedan disponibles en `informe.secciones`

### Requirement: Skill 06-make-bi-solution-update
La skill `06-make-bi-solution-update` SHALL bifurcar la corrida vigente, pedir los cambios (una decisión, un componente, una capa o una herramienta, incluida completar una herramienta «Pendiente»), editar solo lo afectado, volver a construir la figura si cambió la arquitectura, validar y registrar.

#### Scenario: Completar la herramienta de ETL
- **WHEN** el usuario decide la herramienta de ETL
- **THEN** el fork cambia la fila de 2.3 y el componente de 2.2, reconstruye la figura y deja el resto idéntico a la base
