# add-sprint-plan-ceremonies: Plan de sprints, Gantt, ceremonias y Kanban

**Cambio 9 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-sprint-plan-ceremonies`).

## Valor
Reparte el backlog en los 3 sprints (= 3 avances) con un cronograma de línea base, y define cómo se trabaja: ceremonias y tablero Kanban con sus políticas y métricas. Sus datos alimentan los tableros HTML (cambio 10).

## Skills
- `11-make-sprint-plan` y `11-make-sprint-plan-update`.
- `12-make-ceremonies-kanban` y `12-make-ceremonies-kanban-update`.

## Prerrequisitos
11: `08-make-scrum-setup`, `10-make-user-stories`. 12: `08-make-scrum-setup`, `11-make-sprint-plan`.

## Playbook
Amplía `common/scrum/guia.md` (cambio 7) con planificación (objetivo de sprint, capacidad, dependencias) y ceremonias (Sprint Planning, Daily, Review, Retrospective), y crea `common/kanban/guia.md`: columnas, políticas explícitas, límites WIP, métricas (tiempo de ciclo y rendimiento).

Códigos propuestos: `SPR-nn`, `TAR-nn`, `WIP-nn` (límite por columna), `MKB-nn` (métrica).

## Modelos y formularios
- `common/scrum/models/`: `spr-1-plan-sprint.md`, `spr-2-gantt-linea-base.md`, `spr-3-ceremonias.md`.
- `common/kanban/models/`: `kan-1-tablero.md` (columnas, políticas), `kan-2-wip-metricas.md`, `README.md`.

## Qué pregunta la skill
11: duración y fechas de cada sprint (de `avances`), capacidad del equipo en horas, historias que entran en cada sprint (propone y confirma), dependencias. 12: horarios y duración de las ceremonias, columnas del tablero, límite WIP por columna.

## Salida
- `project/sprint-plan/<corrida>/`: `plan-sprints.md`, `gantt-linea-base.md` y `gantt.json` (tareas con fechas, dependencias y sprint).
- `project/ceremonies-kanban/<corrida>/`: `ceremonias.md`, `kanban.md` y `tablero.json`.

## Índice
Alimenta **4.6.1, 4.6.2, 4.7.1 a 4.7.4 y 4.8.1 a 4.8.3**. Sin cambios al índice.

## Update
Mover una historia de sprint, cambiar fechas, ajustar WIP o una ceremonia; recalcula capacidad y fechas del Gantt.

## Validación
Toda `HU` del backlog asignada o explícitamente diferida, capacidad por sprint no superada, fechas dentro de los avances del config, dependencias sin ciclos, WIP numérico, `gantt.json` y `tablero.json` con el esquema que consume el cambio 10.

## Fuera de alcance
Las vistas HTML (cambio 10) y los valores reales del avance (cambio 12).

## Decisiones abiertas para el proposal
- Esquema exacto de `gantt.json` y `tablero.json` (compartido con el cambio 10).
- Si 11 y 12 se pueden ejecutar en paralelo o 12 depende de 11.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
