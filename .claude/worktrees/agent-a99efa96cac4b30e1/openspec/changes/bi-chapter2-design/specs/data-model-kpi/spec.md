# Spec Delta

## Purpose

Define la skill `07-make-data-model-kpi` y su `-update`, que producen las secciones 2.4 y 2.5 del informe: el modelo de datos dimensional con su figura y los indicadores clave de rendimiento trazados a los objetivos del proyecto.

## ADDED Requirements

### Requirement: Playbook y modelos del modelo de datos y los KPI
El repositorio SHALL incluir `common/07-data-model-kpi/guia.md` (modelado en estrella, granularidad, tipos de medidas, cardinalidad y dirección de filtro, cómo formular un KPI y errores frecuentes) y `common/07-data-model-kpi/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`.

#### Scenario: Skill que necesita el formato
- **WHEN** `07-make-data-model-kpi` va a escribir una sección
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

### Requirement: Fuentes de la skill del modelo
La skill SHALL leer el brief vigente (objetivos con su indicador y fuentes previstas), la corrida vigente de `05-make-problem-objectives` y la de `06-make-bi-solution` (arquitectura y fuentes), y SHALL avisar sin bloquear cuando falte alguna.

#### Scenario: Sin arquitectura
- **WHEN** no hay corrida vigente de `06-make-bi-solution`
- **THEN** la skill avisa que falta y pregunta si continúa solo con las fuentes del brief

### Requirement: Tablas de hechos
La sección 2.4 SHALL definir al menos una tabla de hechos `FCT-nn` con su nombre, su granularidad (qué representa una fila), sus medidas con tipo de agregación y las claves hacia sus dimensiones.

#### Scenario: Hecho sin granularidad
- **WHEN** una tabla de hechos no declara su granularidad
- **THEN** la validación informa la tabla

### Requirement: Dimensiones
La sección 2.4 SHALL definir las dimensiones `DIM-nn` con su clave, sus atributos y, cuando existan, sus jerarquías, e incluir una dimensión de tiempo cuando algún KPI se mide por periodo.

#### Scenario: Falta la dimensión de tiempo
- **WHEN** un KPI tiene frecuencia mensual y no hay dimensión de tiempo
- **THEN** la validación informa el KPI y la dimensión que falta

### Requirement: Relaciones del modelo
La sección 2.4 SHALL listar cada relación entre un hecho y una dimensión con sus campos, su cardinalidad y su dirección de filtro, y toda dimensión SHALL estar relacionada con al menos un hecho; la figura `modelo-datos` SHALL marcarse con `<!-- figura: modelo-datos -->`.

#### Scenario: Dimensión suelta
- **WHEN** una dimensión no participa en ninguna relación
- **THEN** la validación informa la dimensión

#### Scenario: Relación a una tabla inexistente
- **WHEN** una relación cita una tabla que no está definida
- **THEN** la validación informa la relación y la tabla

### Requirement: KPI formulados y trazados
La sección 2.5 SHALL definir cada indicador `KPI-nn` con nombre, fórmula, medida propuesta, tabla y campos de origen, meta, frecuencia, objetivo `OE-nn` al que responde y decisión que apoya; cada `OE` del brief SHALL tener al menos un KPI y cada KPI SHALL usar solo campos definidos en el modelo.

#### Scenario: Objetivo sin KPI
- **WHEN** un `OE` del brief no tiene ningún KPI asociado
- **THEN** la validación informa el código del objetivo

#### Scenario: Campo fuera del modelo
- **WHEN** un KPI cita un campo que no está en ninguna tabla del modelo
- **THEN** la validación informa el KPI y el campo

#### Scenario: KPI sin meta
- **WHEN** un KPI no tiene meta ni «Pendiente»
- **THEN** la validación informa el KPI

### Requirement: Salida de la corrida del modelo
La skill SHALL crear cada corrida en `project/07-data-model-kpi/<DD-MM-AAAA-HH-MM-SS>/` según el contrato de las corridas de contenido: `secciones/2.4.md` y `secciones/2.5.md` con su encabezado exacto, `visuales/modelo-datos.html`, `leer-imagen/modelo-datos.md`, `modelo.json` con hechos, dimensiones, relaciones y KPI (lo leerán las skills del capítulo 3), `referencias.md` si cita fuentes y `README.md`, y SHALL registrarla con `register`.

#### Scenario: Corrida registrada
- **WHEN** la corrida pasa la validación y se registra
- **THEN** las secciones 2.4 y 2.5 quedan disponibles en `informe.secciones`

#### Scenario: modelo.json desalineado
- **WHEN** `modelo.json` tiene una tabla o un KPI que no figura en las secciones
- **THEN** la validación informa la diferencia

### Requirement: Skill 07-make-data-model-kpi-update
La skill `07-make-data-model-kpi-update` SHALL bifurcar la corrida vigente, pedir los cambios (una tabla, un atributo, una relación o un KPI), editar solo lo afectado manteniendo `modelo.json` igual a las secciones, reconstruir la figura si cambió el modelo, validar y registrar.

#### Scenario: Agregar un KPI
- **WHEN** el usuario agrega un KPI para un objetivo
- **THEN** el fork agrega la fila en 2.5 y en `modelo.json`, valida la trazabilidad y deja el resto idéntico a la base
