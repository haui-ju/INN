# report-conclusions Specification

## Purpose
Define la skill `11-make-conclusions` y su `-update`, que redactan la sección 5 del informe: una conclusión por objetivo según el valor real del KPI, recomendaciones accionables y lecciones aprendidas del proceso, sin afirmar lo que los datos no muestran.

## Requirements

### Requirement: Playbook y modelos de las conclusiones
El repositorio SHALL incluir `common/11-conclusions/guia.md` (cómo concluir cumplimiento con KPI y meta, cómo redactar recomendaciones accionables y lecciones, límites de datos generados y errores frecuentes) y `common/11-conclusions/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`.

#### Scenario: Skill que necesita el formato
- **WHEN** `11-make-conclusions` va a escribir la sección
- **THEN** lee antes la guía y la plantilla y respeta su formato

### Requirement: Fuentes de la skill de conclusiones
La skill SHALL leer el brief vigente (objetivos con su indicador), la corrida vigente de `05-make-problem-objectives` (problemática y matriz), los KPI con sus metas de `07-make-data-model-kpi`, y las de `09-make-dashboard` y `10-make-storytelling`, y SHALL avisar sin bloquear cuando falte alguna.

#### Scenario: Sin storytelling
- **WHEN** no hay corrida vigente de `10-make-storytelling`
- **THEN** la skill avisa y pregunta si continúa solo con los valores del dashboard

### Requirement: Una conclusión por objetivo
La sección 5 SHALL definir una conclusión `CNC-nn` por cada `OE-nn` del brief, con su estado (cumplido, parcial o no cumplido) justificado por el valor real del KPI frente a su meta, y una conclusión del objetivo general `OG-nn`.

#### Scenario: Objetivo sin conclusión
- **WHEN** un `OE-nn` del brief no tiene conclusión
- **THEN** la validación informa el objetivo

#### Scenario: Estado sin respaldo
- **WHEN** una conclusión dice «cumplido» y el valor real no alcanza la meta
- **THEN** la validación informa la conclusión, el valor y la meta

### Requirement: Metas pendientes declaradas
Cuando un KPI no tiene meta, la conclusión del objetivo que lo mide SHALL decir que no puede concluirse el cumplimiento y SHALL referirse a la meta pendiente en lugar de inventarla.

#### Scenario: KPI sin meta
- **WHEN** KPI-02 sigue con meta «Pendiente»
- **THEN** la conclusión de su objetivo declara que no hay meta contra la cual concluir y la validación no la marca como error

### Requirement: Recomendaciones accionables
Cada recomendación `REC-nn` SHALL ligarse a una conclusión `CNC-nn`, nombrar la decisión o la acción, quién la toma (dueño o jefe de cocina, según el brief) y el indicador que mostrará si funcionó.

#### Scenario: Recomendación suelta
- **WHEN** una recomendación no cita ninguna conclusión
- **THEN** la validación informa la recomendación

### Requirement: Lecciones aprendidas del proceso
La sección SHALL incluir lecciones `LEC-nn` sobre el proceso y SHALL declarar como limitación que los datos fueron generados y que los resultados dependen de esa calibración.

#### Scenario: Sin limitación declarada
- **WHEN** `modo_datos` es `generado` y la sección no declara la limitación
- **THEN** la validación informa que falta

### Requirement: Sección 5 y registro
La corrida SHALL escribir `secciones/5.md` con su encabezado exacto, títulos de tabla `Tabla N: …` y `referencias.md` si cita, SHALL registrar la sección con `register` y SHALL tener una homóloga `11-make-conclusions-update` que copia la corrida vigente como «-fork» y cambia solo lo pedido.

#### Scenario: Corrida completa
- **WHEN** la skill termina
- **THEN** el validador no informa incidencias, `12-make-report` incluye la sección 5 y `faltantes.md` ya no lista capítulos pendientes
