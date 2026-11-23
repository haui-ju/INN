# dashboard-construction Specification

## Purpose
Define la skill `09-make-dashboard` y su `-update`, que entregan al equipo la especificación de páginas y las medidas DAX de los KPI, recogen los valores y las capturas reales del dashboard construido en Power BI y redactan la sección 3.2 y los anexos C y D, sin inventar ningún resultado.

## Requirements

### Requirement: Playbook y modelos del dashboard
El repositorio SHALL incluir `common/09-dashboard/guia.md` (páginas, tipos de visual según la pregunta, filtros, semáforo contra la meta, DAX por patrón, evidencia a conservar y errores frecuentes) y `common/09-dashboard/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`.

#### Scenario: Skill que necesita el formato
- **WHEN** `09-make-dashboard` va a escribir la sección o un anexo
- **THEN** lee antes la guía y la plantilla correspondiente y respeta su formato

### Requirement: Fuentes de la skill del dashboard
La skill SHALL leer el brief vigente (usuarios y decisiones), `modelo.json` y los KPI de `07-make-data-model-kpi` y la corrida vigente de `08-make-etl`, y SHALL bloquear cuando falte `modelo.json` y avisar cuando falte el ETL.

#### Scenario: Sin ETL
- **WHEN** no hay corrida vigente de `08-make-etl`
- **THEN** la skill avisa y pregunta si continúa solo con la especificación, sin valores reales

### Requirement: Especificación de páginas
La skill SHALL proponer páginas `PAG-nn` con su pregunta de negocio, el usuario que la consulta, sus visualizaciones, sus filtros y los KPI que muestra, y SHALL esperar la confirmación del usuario antes de escribir.

#### Scenario: KPI sin página
- **WHEN** un KPI del modelo no aparece en ninguna página
- **THEN** la validación informa el KPI

#### Scenario: Página sin usuario
- **WHEN** una página no indica qué usuario del brief la consulta
- **THEN** la validación informa la página

### Requirement: Medidas DAX de cada KPI
La skill SHALL entregar una medida `MED-nn` por cada KPI con su fórmula DAX propuesta, escrita solo con tablas y campos de `modelo.json`, y SHALL declarar que el equipo la prueba en Power BI.

#### Scenario: Campo fuera del modelo
- **WHEN** una medida usa una tabla o un campo que no existe en `modelo.json`
- **THEN** la validación informa la medida y el nombre

#### Scenario: Medida del equipo
- **WHEN** el equipo trae una medida final distinta de la propuesta
- **THEN** el anexo C conserva la del equipo, que es la que se ejecutó

### Requirement: Dashboard de referencia en HTML
La skill SHALL generar un HTML autónomo, con el sistema de diseño del proyecto en claro y oscuro, que muestre cada página del dashboard con sus visuales y los valores esperados calculados desde los datos generados, y SHALL indicar en cada visual qué tabla y campo van en cada eje.

#### Scenario: Página de referencia
- **WHEN** el equipo abre el HTML
- **THEN** ve cada página con sus KPI contra su meta, sus gráficos con los valores esperados y, bajo cada visual, el tipo de visual, los campos de sus ejes, la medida y los filtros

#### Scenario: Valores comparables
- **WHEN** el equipo calcula un KPI en Power BI
- **THEN** puede compararlo con el valor esperado que muestra el HTML y con la hoja de respuestas

### Requirement: Guía de construcción por visual, KPI y columna calculada
La skill SHALL entregar una guía paso a paso que explique, por cada visual, su tipo, los campos de sus ejes, la medida y los filtros; por cada KPI, su cálculo en lenguaje claro, su medida DAX y sus tablas de origen; y por cada columna calculada, de qué tabla y de qué campos sale.

#### Scenario: Columna calculada
- **WHEN** un visual usa una columna que no existe en las fuentes
- **THEN** la guía indica en qué tabla se crea, con qué fórmula y de qué campos sale

### Requirement: Valores reales y capturas del equipo
Antes de redactar, la skill SHALL pedir al equipo el valor real de cada KPI y una captura por página, SHALL guardarlos en la corrida y SHALL citar en 3.2 solo esos valores.

#### Scenario: Sin valores
- **WHEN** el equipo no entregó los valores reales
- **THEN** la skill deja 3.2 y el anexo D sin escribir y entrega solo la especificación y las medidas

#### Scenario: Valor sin captura
- **WHEN** 3.2 cita el valor de un KPI que no aparece en ninguna captura entregada
- **THEN** la skill avisa y pide la captura de la página que lo muestra

### Requirement: Metas pendientes de los KPI
Cuando un KPI tiene meta «Pendiente» en 2.5, la skill SHALL proponer la meta a partir del valor real, SHALL pedir la confirmación del usuario y SHALL indicar que se cierra con `07-make-data-model-kpi-update` antes de entregar el informe.

#### Scenario: Meta propuesta
- **WHEN** KPI-02 tiene meta «Pendiente» y el equipo entrega su valor real
- **THEN** la skill propone una meta con su justificación y avisa que se registra con la skill de actualización del modelo

### Requirement: Sección 3.2 y anexos C y D
La corrida SHALL escribir `secciones/3.2.md` (páginas, visualizaciones, filtros y KPI, con las capturas marcadas con `<!-- captura: <id> -->`), `anexos/C.md` (medidas DAX y columnas calculadas) y `anexos/D.md` (especificación y una captura por página con su descripción), con títulos de tabla `Tabla N: …`.

#### Scenario: Corrida completa
- **WHEN** la skill termina con valores y capturas
- **THEN** la corrida trae las tres piezas, el validador no informa incidencias y `12-make-report` incluye 3.2 y los anexos C y D

### Requirement: Registro y actualización
La skill SHALL registrar la sección 3.2 con `register` y SHALL tener una homóloga `09-make-dashboard-update` que copia la corrida vigente como «-fork», cambia solo lo pedido (una página, una medida, un valor o una captura) y deja el resto idéntico.

#### Scenario: Reemplazar una captura
- **WHEN** el equipo entrega una captura nueva de una página
- **THEN** el fork cambia esa captura y la sección 3.2, y deja idénticas las medidas del anexo C
