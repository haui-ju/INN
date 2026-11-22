# Design

## Context

Ver `proposal.md` (Why). Estado del que parte:

- `pipeline.json` ya declara `06-make-bi-solution` (secciones 2.1 a 2.3, carpeta `06-bi-solution`) y `07-make-data-model-kpi` (2.4 y 2.5, carpeta `07-data-model-kpi`), y el índice marca 2.2 y 2.4 con «(incluye imagen)».
- `12-make-report` arma el informe con el contrato de las corridas de contenido (spec `report-assembly`): `secciones/<punto>.md`, `<!-- figura: <visual> -->`, `visuales/<visual>.html`, `leer-imagen/<visual>.md`, `referencias.md` y títulos de tabla `Tabla N: …`.
- El capítulo 1 (`bi-chapter1-diagnosis`) se construye en paralelo; este change lo necesita integrado antes del apply, porque lee sus objetivos y su problemática.
- La forma de construir el capítulo 3 (MCP o manual) y la herramienta de ETL y de almacenamiento siguen sin decidir.

## Goals / Non-Goals

**Goals:**
- Que 2.1 a 2.5 se puedan generar, validar y armar en el informe con la misma calidad que el capítulo 1.
- Trazabilidad verificable: objetivo → componente de la solución → KPI → campos del modelo → fuentes.
- Dejar un `modelo.json` legible por máquina que use después el capítulo 3 (ETL y dashboard).

**Non-Goals:**
- Construir el ETL, el dataset o el dashboard (capítulo 3, congelado).
- Escribir medidas DAX definitivas: 2.5 propone la medida; la versión final va al anexo C con el capítulo 3.
- Decidir por el usuario la herramienta de ETL o de almacenamiento.

## Decisions

**D1. Dos skills, como declara `pipeline.json`.** 06 cubre el «qué y con qué» (propuesta, arquitectura, herramientas) y 07 el «cómo se modela y se mide» (modelo y KPI). Así un cambio de herramienta no obliga a rehacer el modelo, y un KPI nuevo no toca la arquitectura.

**D2. Herramientas pendientes permitidas.** Power BI es obligatorio por la consigna. Las filas de ETL y almacenamiento admiten «Pendiente» con el motivo («se decide con la construcción del capítulo 3»); la validación no lo marca como error, pero `12-make-report` lo verá en el texto. Se completa con `06-make-bi-solution-update`. Alternativa descartada: obligar a elegir ahora, que contradice la decisión del usuario de congelar esa parte.

**D3. Códigos de trazabilidad.** `CAP-nn` (componentes de la arquitectura), `HER-nn` (herramientas), `FCT-nn` (hechos), `DIM-nn` (dimensiones), `REL-nn` (relaciones) y `KPI-nn`. Reutiliza `OE-nn` y `FUE-nn` del brief. Los validadores comprueban que todo código citado esté definido (regla genérica de `validate_run.py` con `PREFIJOS`).

**D4. Modelo en estrella por defecto.** La guía recomienda una estrella con uno o dos hechos y dimensiones conformadas (tiempo, producto, canal, local, cliente, según el rubro); un copo de nieve se acepta si se justifica. La dimensión de tiempo es obligatoria cuando algún KPI tiene frecuencia.

**D5. `modelo.json` como contrato con el capítulo 3.** Esquema: `{schema: 1, hechos: [{codigo, nombre, granularidad, medidas: [{nombre, tipo, agregacion}], claves: [...]}], dimensiones: [{codigo, nombre, clave, atributos: [...], jerarquias: [...]}], relaciones: [{codigo, desde, hacia, campos, cardinalidad, filtro}], kpis: [{codigo, nombre, formula, medida, origen: [tabla.campo], meta, frecuencia, objetivo, decision}]}`. Las secciones en Markdown son la fuente de verdad del texto; el validador exige que `modelo.json` coincida con ellas (mismos códigos y campos).

**D6. Figuras con la misma biblioteca de visuales que el capítulo 1.** `arquitectura-bi` (cuatro carriles de capas con cajas por componente y flechas) y `modelo-datos` (hechos al centro, dimensiones alrededor, cardinalidad en cada relación) se registran en `visuales.py` con plantillas en `common/html/`, construidas de la misma forma que resuelva el change del capítulo 1 (plantillas compiladas en `_build`). Si en ese change la compilación no fue posible, se resuelve antes del apply (ver Open Questions).

**D7. Trazabilidad en dos sentidos dentro de 07.** Todo `OE` del brief tiene al menos un KPI y todo KPI usa campos del modelo. En 06, todo `OE` aparece en la tabla de la propuesta y toda `FUE` del brief aparece en la capa de fuentes. Son las comprobaciones que piden los escenarios de las specs.

## Risks / Trade-offs

- **El capítulo 1 se integra con nombres de archivos distintos de los supuestos** → las skills leen la problemática y los objetivos por sus secciones (`secciones/1.8.md` a `1.10.md`), que fija el contrato común; antes del apply se revisa lo integrado y se ajustan las tareas.
- **Herramientas «Pendiente» en el informe final** → `12-make-report` las muestra tal cual; la guía recuerda completarlas antes de entregar y `faltantes.md` no las lista porque la sección sí existe. Se acepta: es el estado real del proyecto.
- **`modelo.json` y las secciones divergen tras ediciones manuales** → el validador compara ambos y el `-update` edita los dos a la vez.

## Migration Plan

No hay corridas previas. Se aplica después de integrar `bi-chapter1-diagnosis` en `bi-pipeline`.

## Open Questions

Ninguna. La pregunta sobre el mecanismo de las figuras quedó resuelta al integrar `bi-chapter1-diagnosis`: las plantillas se compilan en `common/html/_build` con `npm install && npm run build` (como `bmc`, `pestel`, `foda` e `ishikawa`), y `arquitectura-bi` y `modelo-datos` siguen el mismo camino.
