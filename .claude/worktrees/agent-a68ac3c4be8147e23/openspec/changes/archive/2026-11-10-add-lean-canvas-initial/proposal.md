# Proposal

## Why

El capítulo 1 del informe necesita el modelo de negocio inicial (puntos 1.3.1 y 1.3.2) y el Design Thinking arranca de «el problema del Lean Canvas»: `ENF-01` lo cita y los playbooks piden que el POV sea coherente con él. Hoy ninguna skill produce ese canvas, así que el problema de partida queda sin una fuente única y el canvas validado v1 (3.4) no tiene contra qué compararse. Conviene fijar primero esa hipótesis, con sus supuestos de mayor riesgo marcados, antes de empatizar con usuarios.

## What Changes

- **Nueva skill `02-make-initial-lean-canvas`**: propone un Lean Canvas v0 (nueve bloques) y una cadena de «5 porqués» por problema, a partir del config y de `domain.md`; pide confirmación y escribe `project/initial-lean-canvas/<corrida>/` con `canvas.md`, `cinco-porques.md` y `README.md`. Registra la corrida en el config.
- **Nueva skill `02-make-initial-lean-canvas-update`**: corrige un bloque, un problema, una cadena de porqués o un supuesto de una corrida existente (copia `-fork`), propaga a los archivos que dependen y valida.
- **Nuevo playbook `common/lean/`** (lo crea este cambio): `guia.md` con las secciones de Lean Canvas y 5 porqués (y la reserva de espacio para las de Lean Startup y Lean Change que añade el cambio 6) y `models/` con `lean-0-cinco-porques.md`, `lean-1-canvas.md` y `README.md`, con el formato de las plantillas de Design Thinking.
- **Códigos de trazabilidad propios:** `PRB-nn` (problema), `POR-nn` (cadena de porqués), `SUP-nn` (supuesto de riesgo); el problema principal es `PRB-01` y se resume en una frase que cita `ENF-01`.
- **Validación propia del paso** (`rules/lean_canvas.py`): nueve bloques, cada `PRB` con su cadena `POR`, cada `SUP` definido y ordenado por riesgo, códigos citados definidos.
- **Sin suposiciones sobre la empresa:** la skill lee `proyecto.tipo` y `domain.md`; con proyecto propio no menciona empresa.

## Capabilities

### New Capabilities
- `lean-canvas-initial`: playbook y modelos de Lean Canvas y 5 porqués, skills `02-make-initial-lean-canvas` y su `-update`, estructura de salida, códigos de trazabilidad, supuestos de riesgo, coherencia con el config y validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/lean/guia.md` y `models/`, `.claude/skills/02-make-initial-lean-canvas/`, `.claude/skills/02-make-initial-lean-canvas-update/`, `.claude/skills/_shared/rules/lean_canvas.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/validate_run.py` (solo registra la carpeta `initial-lean-canvas` en `RULES`; el gancho `validar(run)` ya existe desde `add-design-system`).
- **Consumidores:** `03-make-company-chapter` (1.3.1 y 1.3.2), `05-make-design-thinking` (problema de `ENF-01`) y `07-make-lean-plan` (v0 contra v1, `SUP`). Su prerrequisito ya está en `pipeline.json`.
- **Índice:** alimenta 1.3.1 y 1.3.2 sin cambiar `model1.md`.
- **Fuera de alcance:** canvas validado v1, hipótesis y experimentos (cambio 6), capítulo 1 completo (cambio 4), tablero visual del canvas, ejecutar la skill.
- **Supuestos registrados:** el canvas se entrega en markdown; la escala de riesgo es alto, medio o bajo; las cantidades del playbook son referencias, no normas.
