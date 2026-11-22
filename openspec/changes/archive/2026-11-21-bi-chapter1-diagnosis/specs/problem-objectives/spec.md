# Spec Delta

## Purpose

Produce las secciones 1.8 a 1.10 del informe de BI (problemática central, objetivo general y objetivos específicos con su matriz de articulación) con la skill `05-make-problem-objectives` y su `-update`, a partir del brief y del análisis estratégico vigentes.

## ADDED Requirements

### Requirement: Playbook y modelos de la problemática y los objetivos
El repositorio SHALL incluir `common/05-problem-objectives/guia.md` (problemática, causas principales, copia de objetivos, matriz de articulación, errores y checklist) y `common/05-problem-objectives/models/` con un `README.md` y una plantilla por sección (1.8, 1.9 y 1.10) con ficha, instrucciones, formato, ejemplo y checklist.

#### Scenario: El ejemplo de cada plantilla valida
- **WHEN** se arma una corrida con los ejemplos de las tres plantillas sobre el brief y el análisis estratégico de ejemplo
- **THEN** el validador del paso no informa incidencias

### Requirement: Secciones de la corrida de problemática y objetivos
Cada corrida SHALL contener `secciones/1.8.md`, `1.9.md` y `1.10.md` con el encabezado `## <punto>. <título del índice>` como primera línea y solo texto final, más `README.md` y, si hay citas, `referencias.md`.

#### Scenario: Falta una sección
- **WHEN** la corrida no tiene `secciones/1.9.md`
- **THEN** el validador informa el archivo que falta

### Requirement: Problemática central con causas del Ishikawa
La sección 1.8 SHALL tener un enunciado, los afectados, entre dos y cuatro causas principales tomadas del Ishikawa vigente (mismo código, categoría y texto) y al menos una evidencia.

#### Scenario: Causa que no está en el Ishikawa
- **WHEN** la tabla de causas principales cita `CAU-09` y el Ishikawa vigente no la tiene
- **THEN** el validador lo informa y remite a `04-make-strategic-analysis-update`

### Requirement: Objetivos copiados del brief
Las secciones 1.9 y 1.10 SHALL reproducir sin cambios el `OG-01` y los `OE-nn` del brief vigente (objetivo, métrica, meta, plazo, aporte e indicador); la skill no los vuelve a proponer.

#### Scenario: Objetivo editado en el capítulo
- **WHEN** la meta de `OE-02` en 1.10 difiere de la del brief
- **THEN** el validador lo informa y remite a `01-make-project-brief-update`

### Requirement: Matriz de articulación
La sección 1.10 SHALL incluir una matriz con una fila por cada `OE` del brief que cite causas del Ishikawa, ítems o estrategias FODA, factores PESTEL (o «—»), bloques del Canvas y el indicador del objetivo; todos los códigos y bloques SHALL existir en las corridas vigentes y cada causa principal de 1.8 SHALL quedar atendida por algún objetivo.

#### Scenario: Causa principal sin objetivo
- **WHEN** ninguna fila de la matriz cita la causa principal `CAU-03`
- **THEN** el validador informa que esa causa no está articulada con un objetivo

#### Scenario: Indicador distinto
- **WHEN** el indicador de una fila no coincide con el del `OE` en el brief
- **THEN** el validador lo informa

### Requirement: Validación de la problemática y los objetivos
El validador del paso SHALL comprobar encabezados, la problemática, la copia de los objetivos, la matriz contra las corridas vigentes de `03` y `04`, el marcador de datos modelados y las citas, e informar cada incidencia con archivo y causa; si falta una corrida de origen, SHALL decir cuál.

#### Scenario: Sin análisis estratégico vigente
- **WHEN** no hay corrida vigente de `04-make-strategic-analysis`
- **THEN** el validador informa que no puede comprobar la matriz sin esa corrida

### Requirement: Skill 05-make-problem-objectives-update
La skill `05-make-problem-objectives-update` SHALL bifurcar la corrida vigente, volver a copiar los objetivos del brief si cambiaron, ajustar solo las filas afectadas de la matriz o de las causas principales, validar, registrar e indicar con `references/dependencias.md` qué skills siguen.

#### Scenario: Cambió un objetivo en el brief
- **WHEN** el brief vigente cambia la meta de `OE-01`
- **THEN** el fork actualiza esa fila en 1.10, conserva lo demás y sugiere revisar los KPI en `07-make-data-model-kpi-update` si esa skill existe
