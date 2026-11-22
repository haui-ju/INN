# Proposal

## Why

El capítulo 2 del informe («Diseño técnico de solución en Inteligencia de Negocios») es el criterio de mayor peso de la rúbrica junto con el dashboard: pide arquitectura de BI, herramientas seleccionadas y sustentadas, modelo de datos con hechos, dimensiones y relaciones, y KPI justificados. Hoy las secciones 2.1 a 2.5 están declaradas en `pipeline.json` (skills `06-make-bi-solution` y `07-make-data-model-kpi`), pero ninguna skill las produce, así que el informe no puede armarlas. Además, el diseño de este capítulo es la entrada de la construcción del ETL y del dashboard (capítulo 3), que sigue congelada.

## What Changes

- **Nueva skill `06-make-bi-solution`** (y su `-update`): produce 2.1 Propuesta de solución en BI (decisiones que apoya, usuarios y cómo responde a la problemática y a cada objetivo), 2.2 Arquitectura de BI por capas (fuentes, ETL, almacenamiento y visualización) con su figura, y 2.3 Herramientas utilizadas (función, capa, justificación y alternativa descartada). Las herramientas del ETL y del almacenamiento pueden quedar «Pendiente» mientras el usuario no decida cómo se construirá el capítulo 3; Power BI es fijo por la consigna.
- **Nueva skill `07-make-data-model-kpi`** (y su `-update`): produce 2.4 Diseño del modelo de datos en estrella (tablas de hechos con su granularidad y medidas, dimensiones con atributos y jerarquías, relaciones con cardinalidad y dirección de filtro) con su figura, y 2.5 KPI (fórmula, medida propuesta, tabla y campos de origen, meta, frecuencia, objetivo al que responde y decisión que apoya).
- **Trazabilidad con el capítulo 1:** cada objetivo específico del brief tiene al menos un KPI que lo mide, y cada KPI usa solo campos del modelo de datos; las fuentes de la arquitectura salen de las fuentes previstas del brief.
- Ambas skills siguen el contrato de las corridas de contenido (`secciones/<punto>.md`, `<!-- figura: … -->`, `visuales/`, `leer-imagen/`, `referencias.md`) y registran sus secciones con `register`, de modo que `12-make-report` las incluye en cuanto existen.
- Playbooks en `common/06-bi-solution/` y `common/07-data-model-kpi/`, validadores en `_shared/rules/` y pruebas.

## Capabilities

### New Capabilities

- `bi-solution-design`: skill `06-make-bi-solution` y su `-update`; propuesta de solución, arquitectura de BI por capas con su figura y tabla de herramientas sustentadas (2.1 a 2.3).
- `data-model-kpi`: skill `07-make-data-model-kpi` y su `-update`; modelo dimensional (hechos, dimensiones, relaciones) con su figura, diccionario preliminar y KPI trazados a los objetivos (2.4 y 2.5).

### Modified Capabilities

(ninguna: las secciones ya están declaradas en `pipeline.json` y en el índice)

## Impact

- **Skills:** `.claude/skills/06-make-bi-solution`, `06-make-bi-solution-update`, `07-make-data-model-kpi`, `07-make-data-model-kpi-update`.
- **Kit:** `_shared/rules/bi_solution.py`, `_shared/rules/data_model_kpi.py`, registros de los visuales `arquitectura-bi` y `modelo-datos` en `_shared/visuales.py` con sus plantillas en `common/html/`, y pruebas en `_shared/tests/`.
- **Playbooks:** `common/06-bi-solution/` y `common/07-data-model-kpi/` con guía y plantillas.
- **Dependencias:** requiere el capítulo 1 (`bi-chapter1-diagnosis`) integrado: lee el brief, la problemática y los objetivos (`05-make-problem-objectives`). Desbloquea el capítulo 3 (`bi-chapter3-etl-dashboard`), que sigue congelado.
