# Proposal

## Why

El capítulo 1 del informe (la empresa y el problema) se entrega en el avance 1 y es la base de los objetivos que el análisis final evalúa al cierre. Hoy nada lo produce, y el diseño original daba por hecho que el proyecto pertenece a una empresa, cuando puede ser un proyecto propio o innovador. `project/domain.md` ya reúne los datos del dominio (por RUC, o de la solución) y el Lean Canvas v0 fija el modelo de negocio inicial; falta convertirlos en un capítulo coherente, con diagnóstico, objetivos medibles, justificación y alcances.

## What Changes

- **Nueva skill `03-make-company-chapter`**: arma el capítulo 1 a partir del config, `domain.md` y el canvas v0. **Confirma al ejecutarse si el proyecto se aplica a una empresa o es propio**, muestra qué secciones salen de datos modelados y deja que el usuario los reemplace, y escribe `project/company-chapter/<corrida>/` con `capitulo-1.md`, `bloques/` y `README.md`. Registra la corrida en el config.
- **Nueva skill `03-make-company-chapter-update`**: corrige un dato, un ítem del FODA, un objetivo o una justificación de una corrida existente (copia `-fork`), propaga a los archivos que dependen y valida.
- **Nuevo playbook `common/company/`**: `guia.md` (presentación, FODA, objetivos medibles, justificación, alcances y limitaciones, adaptación a proyecto propio, referencias, checklist) y `models/` con cuatro plantillas más un `README.md`, con el formato de las plantillas de Design Thinking.
- **Códigos de trazabilidad propios:** `FOR`/`DEB` (microentorno), `OPO`/`AME` (macroentorno), `OG` (objetivo general) y `OE` (objetivo específico). Los `OE` los evalúa el cambio 13 en 6.4.1.
- **Adaptación a proyecto propio:** con `tipo: propio`, el capítulo mantiene la numeración 1.1 a 1.6 pero titula 1.1 «Presentación del proyecto» y adapta sus subpuntos (origen, propósito, visión, valores) sin mencionar una empresa inexistente.
- **Capítulo sin marcadores:** los datos de `domain.md` marcados «(modelado por el agente, …)» se copian al capítulo sin el marcador; la procedencia consta solo en el `README.md` de la corrida (qué secciones salieron de datos modelados).
- **Validación propia del paso** (`rules/company.py`): secciones 1.1 a 1.6 presentes, objetivos medibles, `OE` ligados a un `OG`, códigos del FODA definidos y 1.3 idéntica al canvas v0 vigente.

## Capabilities

### New Capabilities
- `company-chapter`: playbook y modelos del capítulo 1, skills `03-make-company-chapter` y su `-update`, estructura de salida, adaptación a proyecto con o sin empresa, FODA y objetivos con trazabilidad y validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/company/guia.md` y `models/`, `.claude/skills/03-make-company-chapter/`, `.claude/skills/03-make-company-chapter-update/`, `.claude/skills/_shared/rules/company.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/validate_run.py` (solo registra la carpeta `company-chapter` en `RULES`; el gancho `validar(run)` ya existe desde `add-design-system`).
- **Consumidores:** `19-make-report` (capítulo 1 del informe), `18-make-final-analysis` (evalúa los `OE`) y `07-make-lean-plan` (contexto).
- **Índice:** alimenta 1.1, 1.2, 1.4, 1.5 y 1.6 y reproduce 1.3 desde el canvas; `model1.md` no cambia (el título de 1.1 para proyecto propio se adapta solo en el capítulo generado).
- **Fuera de alcance:** el marco metodológico (cambio 5), la evaluación de los objetivos (cambio 13), el Lean Canvas (cambio 3), ejecutar la skill.
- **Supuestos registrados:** el FODA no lleva puntaje, solo código y evidencia; el rango de referencia es 1 `OG` y 3 a 5 `OE`; las referencias bibliográficas son una lista cerrada verificada al implementar.
