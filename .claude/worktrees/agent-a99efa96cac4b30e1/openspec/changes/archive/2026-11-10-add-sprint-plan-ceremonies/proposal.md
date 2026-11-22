# Proposal

## Why

Con los requerimientos y las historias definidos, falta decidir **cuándo** se construye cada historia y **cómo trabaja** el equipo: el reparto en tres sprints (= tres avances) con un cronograma de línea base (puntos 4.6.1 y 4.6.2), las ceremonias de Scrum (4.7) y el diseño del tablero Kanban con sus límites y métricas (4.8). Hoy ninguna skill los produce. Además, los tableros HTML (cambio 10) y los informes de sprint (cambio 12) necesitan datos estructurados y estables —tareas con fechas, columnas y tarjetas— que este cambio fija.

## What Changes

- **Nueva skill `11-make-sprint-plan`**: reparte las historias del backlog en los tres sprints (fechas de entrega del config, capacidad en puntos, dependencias), define el objetivo de cada sprint y propone el Gantt de línea base con tareas `TAR-nn`; pide confirmación y escribe `project/sprint-plan/<corrida>/` con `plan-sprints.md`, `gantt-linea-base.md`, `gantt.json` y `README.md`.
- **Nueva skill `12-make-ceremonies-kanban`**: define las ceremonias (Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective) con su calendario sobre los sprints, y el tablero Kanban (columnas y políticas, límites WIP, métricas de tiempo de ciclo y rendimiento); escribe `project/ceremonies-kanban/<corrida>/` con `ceremonias.md`, `kanban.md`, `tablero.json` y `README.md`. **Depende del plan de sprints**: las tarjetas del tablero son las tareas del Gantt.
- **Dos skills `-update`**: `11-make-sprint-plan-update` (mover historias, capacidad, dependencias, tareas y fechas de tareas) y `12-make-ceremonies-kanban-update` (ceremonias, columnas, WIP, métricas y resincronización de tarjetas).
- **Playbooks:** se **amplía** `common/scrum/guia.md` (secciones de planificación y ceremonias, sin renumerar las de roles y artefactos) con las plantillas `spr-1-plan-sprints`, `spr-2-gantt-linea-base` y `spr-3-ceremonias`; se **crea** `common/kanban/` con `guia.md` y las plantillas `kan-1-tablero` y `kan-2-wip-metricas`.
- **Esquemas de datos fijados aquí** (los consume el cambio de tableros HTML): `gantt.json` (sprints, tareas con fechas ISO, dependencias y responsable) y `tablero.json` (columnas con WIP, métricas, tarjetas). Cada archivo `.json` debe coincidir con sus tablas de markdown.
- **Códigos de trazabilidad propios:** `TAR-nn` (tarea del Gantt), `WIP-nn` (límite de una columna) y `MKB-nn` (métrica Kanban); citan las `HU` del backlog.
- **Reglas verificables:** toda historia del backlog queda asignada a un sprint o diferida con motivo; la carga de cada sprint no supera su capacidad; las fechas de los sprints salen del config y no se solapan; las tareas caen dentro de su sprint y respetan sus dependencias sin ciclos; las duraciones de las ceremonias no superan los topes de la Guía de Scrum para un sprint de un mes.
- **Validación propia de cada paso** (`rules/sprint_plan.py`, `rules/ceremonies_kanban.py`).

## Capabilities

### New Capabilities
- `sprint-plan`: planificación de sprints y Gantt de línea base, su playbook y plantillas, la skill `11-make-sprint-plan` y su `-update`, el esquema de `gantt.json` y su validación.
- `ceremonies-kanban`: ceremonias de Scrum y diseño del tablero Kanban, sus playbooks y plantillas, la skill `12-make-ceremonies-kanban` y su `-update`, el esquema de `tablero.json` y su validación.

### Modified Capabilities
- Ninguna. La spec `scrum-setup` ya prevé que el playbook de Scrum se amplíe sin renumerar sus secciones.

## Impact

- **Archivos nuevos:** `common/scrum/models/spr-1` a `spr-3`, `common/kanban/`, `.claude/skills/11-make-sprint-plan/`, `11-make-sprint-plan-update/`, `12-make-ceremonies-kanban/`, `12-make-ceremonies-kanban-update/`, `.claude/skills/_shared/rules/sprint_plan.py`, `ceremonies_kanban.py` y sus pruebas.
- **Archivos modificados:** `common/scrum/guia.md` y `common/scrum/models/README.md` (ampliación), `.claude/skills/_shared/validate_run.py` (registra las dos carpetas).
- **Consumidores:** `13-design-html-boards` (lee `gantt.json` y `tablero.json`), `14-make-system-design`, `15-make-implementation-log`, `16-make-sprint-report`, `17-make-lean-results` (experimentos por avance), `19-make-report`.
- **Índice:** alimenta 4.6.1, 4.6.2, 4.7.1 a 4.7.4 y 4.8.1 a 4.8.3; `model1.md` no cambia.
- **Fuera de alcance:** las vistas HTML del Gantt y el Kanban (cambio 10), los valores reales de avance, tiempo de ciclo y rendimiento (cambio 12), ejecutar las skills.
- **Supuestos registrados:** la capacidad se mide en puntos de historia (las tallas se convierten con XS=1, S=2, M=3, L=5, XL=8); el inicio del sprint 1 lo da el usuario y cada sprint siguiente empieza el día después de la entrega anterior; las fechas del plan usan días calendario; exige las tres fechas de avance en el config.
