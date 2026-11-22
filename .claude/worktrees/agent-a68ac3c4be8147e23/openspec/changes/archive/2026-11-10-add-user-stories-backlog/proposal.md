# Proposal

## Why

Los requerimientos (RF y RNF) dicen qué debe hacer el sistema, pero el equipo construye por historias de usuario ordenadas en un Product Backlog, y cada historia necesita criterios de aceptación y una definición de «terminado». Los puntos 4.4.1, 4.4.2 y 4.5 del informe los piden, y el plan de sprints (cambio 9) parte directamente del backlog. Hoy ninguna skill los produce, y sin una cadena trazable REQ → RF → HU → CA los informes de sprint (con pies de foto «HU-XX nombre (REQ-XX)») no podrían citar nada verificable.

## What Changes

- **Nueva skill `10-make-user-stories`**: parte de los RF de la corrida vigente de `09-make-requirements`, **propone la lista de historias y espera el acuerdo del usuario**, luego propone los criterios de aceptación y pide una segunda confirmación; escribe `project/user-stories/<corrida>/` con `historias/HU-nn.md` (una por historia), `backlog.md`, `criterios-dod.md` y `README.md`. Registra la corrida en el config.
- **Nueva skill `10-make-user-stories-update`**: agrega, quita o corrige historias, criterios, orden, estimaciones o la Definition of Done (copia `-fork`, plan con confirmación, validación).
- **Nuevo playbook `common/user-stories/`**: `guia.md` (formato de la historia, criterios INVEST, criterios Dado/Cuando/Entonces, Definition of Done, escalas de estimación, orden del backlog, errores frecuentes, checklist, referencias) y `models/` con cuatro plantillas (`hu-1` a `hu-4`) y un `README.md`, con el formato de las de Design Thinking.
- **Códigos de trazabilidad propios:** `HU-nn` (historia) y `CA-nn` (criterio de aceptación, numeración única en el proyecto). Cada historia cita los `RF` de los que nace y muestra los `REQ` derivados; puede citar `RNF` aplicables.
- **Backlog priorizado con reglas verificables:** la prioridad de cada historia es la más alta de sus RF (`Debe` > `Debería` > `Podría`), el orden va de mayor a menor prioridad (dentro de un nivel lo fija el Product Owner) y la estimación usa la escala elegida (por defecto puntos 1, 2, 3, 5, 8, 13).
- **Cobertura:** todo `RF` de la corrida vigente de requerimientos tiene al menos una historia o figura en «RF sin historia» con su motivo.
- **Validación propia del paso** (`rules/user_stories.py`): estructura, trazabilidad contra la corrida vigente de requerimientos, coherencia entre historias, backlog y resumen de criterios, y cantidades mínimas.

## Capabilities

### New Capabilities
- `user-stories`: playbook y modelos de historias, criterios de aceptación, backlog y Definition of Done, skills `10-make-user-stories` y su `-update`, trazabilidad y validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/user-stories/`, `.claude/skills/10-make-user-stories/`, `.claude/skills/10-make-user-stories-update/`, `.claude/skills/_shared/rules/user_stories.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/validate_run.py` (registra la carpeta `user-stories`).
- **Consumidores:** `11-make-sprint-plan` (reparte las historias en sprints), `12-make-ceremonies-kanban`, `14-make-system-design` (casos de prueba por criterio), `15-make-implementation-log` y `16-make-sprint-report` (pies de foto con `HU`), `19-make-report`.
- **Índice:** alimenta 4.4.1, 4.4.2 y 4.5; `model1.md` no cambia.
- **Fuera de alcance:** asignar historias a sprints y capacidad (cambio 9), ceremonias y Kanban (cambio 9), ejecutar las skills.
- **Supuestos registrados:** un RF puede originar de una a tres historias; cada historia tiene de dos a cinco criterios; la escala por defecto son puntos de historia; los RNF se vinculan a la historia con una línea «RNF aplicables» y a la Definition of Done, no a cada criterio; las fuentes citables se verifican antes de usarse.
