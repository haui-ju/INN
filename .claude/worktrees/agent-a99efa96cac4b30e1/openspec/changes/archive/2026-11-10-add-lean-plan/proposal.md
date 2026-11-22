# Proposal

## Why

Los puntos 3.2 a 3.4 del informe (Lean Startup, Lean Change Management y Lean Canvas validado) convierten lo aprendido con el Design Thinking en hipótesis, un MVP, experimentos y un plan de cambio para las personas afectadas. Hoy ninguna skill los produce. Además, el canvas inicial (v0) lista los supuestos de mayor riesgo (`SUP`) pero nada los transforma en algo comprobable, y el canvas validado (v1) debe mostrar qué cambió y con qué evidencia. El plan es el puente entre innovación y gestión ágil: de él salen los requisitos que se priorizan y los experimentos que los sprints ejecutan.

## What Changes

- **Nueva skill `07-make-lean-plan`**: a partir del canvas v0 vigente, de la corrida vigente de Design Thinking, del config y de `domain.md`, propone hipótesis falsables, el MVP textual, los experimentos y métricas, los criterios para pivotar o perseverar, el ciclo de cambio y los actores afectados, y el canvas v1 con su tabla de cambios. Pide confirmación y escribe `project/lean-plan/<corrida>/` con `seccion-3-2.md`, `seccion-3-3.md`, `canvas-v1.md` y `README.md`. Registra la corrida.
- **Nueva skill `07-make-lean-plan-update`**: agrega, quita o corrige hipótesis, experimentos, métricas, actores o el canvas v1 (copia `-fork`, plan con confirmación, validación).
- **Ampliación del playbook `common/lean/`**: `guia.md` pasa de la sección reservada a las secciones de Lean Startup, Lean Change Management y Canvas validado v1, más errores y checklist del plan; `models/` suma cinco plantillas (`lean-2` a `lean-6`) y actualiza su `README.md`. Las secciones de Lean Canvas y 5 porqués no se renumeran.
- **Códigos de trazabilidad propios:** `HIP` (hipótesis), `MET` (métrica), `EXP` (experimento), `CAM` (cambio en el negocio), `INS` (insight), `OPC` (opción) y `ACT` (actor); reutiliza `SUP` y `PRB` del canvas v0 y cita `HAL-E`, `PP` y `REQ` del Design Thinking.
- **MVP textual:** parte de los `REQ` de 3.1.4.3, indica qué incluye y qué no, y qué hipótesis prueba cada requerimiento; no es una versión de software.
- **Canvas v1 trazable:** mismos nueve bloques que el v0, con el estado de cada supuesto (validado, refutado o pendiente) y una tabla `Bloque | v0 | v1 | Evidencia` que debe coincidir con las diferencias reales entre ambos canvas.
- **Corrección de marcas del índice** (`common/structure/model1.md`): 3.2.3, 3.2.4, 3.3 y 3.4 pasan a `[A1+]`, porque el plan y los criterios de decisión se redactan en el avance 1 y los resultados y la decisión final se añaden después.
- **Validación propia del paso** (`rules/lean_plan.py`): estructura, trazabilidad entre códigos, coherencia con el canvas v0 y con la corrida vigente de Design Thinking, y cantidades.

## Capabilities

### New Capabilities
- `lean-plan`: playbook ampliado y modelos del plan Lean, skills `07-make-lean-plan` y su `-update`, hipótesis, MVP, experimentos, criterios de decisión, gestión del cambio, canvas v1 y su validación.

### Modified Capabilities
- Ninguna. El spec `lean-canvas-initial` ya prevé que el playbook se amplíe sin renumerar sus secciones, y las marcas del índice se corrigen sin cambiar el contrato de `report-index-structure`.

## Impact

- **Archivos nuevos:** `common/lean/models/lean-2` a `lean-6`, `.claude/skills/07-make-lean-plan/`, `.claude/skills/07-make-lean-plan-update/`, `.claude/skills/_shared/rules/lean_plan.py` y sus pruebas.
- **Archivos modificados:** `common/lean/guia.md` y `common/lean/models/README.md` (ampliación), `common/structure/model1.md` (cuatro marcas) y `.claude/skills/_shared/validate_run.py` (registra la carpeta `lean-plan`).
- **Consumidores:** `17-make-lean-results` (completa 3.2.3 y 3.2.4 con los resultados), `09-make-requirements` y `10-make-user-stories` (usan MVP y requerimientos), `19-make-report`.
- **Fuera de alcance:** los resultados de los experimentos y la decisión final (cambio 13), el Design Thinking, ejecutar la skill.
- **Supuestos registrados:** las cantidades son referencias (3 a 6 hipótesis, 2 a 4 experimentos de negocio, 2 a 4 de cambio, 2 a 5 actores); los experimentos se asignan a los tres avances del config; las fuentes citables son Ries (2011), Little (2014) y Maurya (2012), ya verificadas.
