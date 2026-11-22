# Proposal

## Why

El capítulo 2 del informe (marco metodológico) explica qué metodologías se usan, por qué se eligieron y cómo se integran, y su glosario (2.4) sirve de referencia a todo el documento. Hoy nada lo produce. Además, el flujo del proyecto (Design Thinking → Lean → Scrum y Kanban) ya está definido en las skills, así que el capítulo debe describir lo que de verdad se aplica y no una lista genérica. El glosario crece a medida que se añaden capítulos (requerimientos, historias, Gantt, Kanban), por lo que necesita un mecanismo de ampliación.

## What Changes

- **Nueva skill `04-make-methodological-framework`**: propone el capítulo 2 a partir del config, del `pipeline.json` (qué metodologías se aplican) y de `domain.md`; pide confirmación y escribe `project/methodological-framework/<corrida>/` con `capitulo-2.md`, `glosario.md`, `referencias.md` y `README.md`. Registra la corrida en el config.
- **Nueva skill `04-make-methodological-framework-update`**: agrega, quita o corrige un término; cambia las metodologías aplicadas; o **amplía el glosario** con términos de capítulos posteriores a partir de las corridas vigentes (copia `-fork`, plan con confirmación, validación).
- **Nuevo playbook `common/methodological-framework/`**: `guia.md` (qué debe cubrir cada metodología, criterio de elección, integración, glosario, **lista cerrada de fuentes** verificadas) y `models/` con cuatro plantillas más un `README.md`, con el formato de las plantillas de Design Thinking.
- **Estructura fija por metodología** (qué es, principios, cuándo se usa, en este proyecto, más lo propio de cada una: fases, ciclo, roles, eventos, artefactos, prácticas y métricas) para que el capítulo sea comparable y validable.
- **Integración trazable (2.3):** tabla `Metodología | Recibe | Produce | Dónde en el informe`, con los puntos del informe validados contra `common/structure/model1.md`.
- **Glosario con términos obligatorios** por metodología aplicada, orden alfabético, origen y puntos donde se usa; se mantiene idéntico en `glosario.md` y en 2.4.
- **Validación propia del paso** (`rules/methodological_framework.py`): secciones 2.1 a 2.4, estructura de cada metodología, coherencia entre secciones y tabla de integración, glosario, puntos existentes en el índice y citas dentro de la lista cerrada (máximo 2 por metodología y 2 en 2.3 y 2.4, con su entrada en `referencias.md`).

## Capabilities

### New Capabilities
- `methodological-framework`: playbook y modelos del capítulo 2, skills `04-make-methodological-framework` y su `-update`, estructura por metodología, integración, glosario ampliable, citas de lista cerrada y validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/methodological-framework/guia.md` y `models/`, `.claude/skills/04-make-methodological-framework/`, `.claude/skills/04-make-methodological-framework-update/`, `.claude/skills/_shared/rules/methodological_framework.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/validate_run.py` (solo registra la carpeta `methodological-framework` en `RULES`).
- **Consumidores:** `19-make-report` (capítulo 2 y referencias) y todas las skills que añaden términos al glosario mediante el `-update`.
- **Índice:** alimenta 2.1 a 2.4; `model1.md` no cambia.
- **Fuera de alcance:** aplicar las metodologías (cambios 6 a 9), el Lean Canvas, la lista global de referencias del informe (la arma el cambio 14 a partir de `referencias.md`), ejecutar la skill.
- **Supuestos registrados:** las cinco metodologías por defecto son Design Thinking, Lean Startup, Lean Change Management, Scrum y Kanban, y el usuario puede quitar alguna; la profundidad (resumen o detallado) cambia la extensión, no la estructura; los subtítulos de metodología no se numeran para no cambiar el índice.
