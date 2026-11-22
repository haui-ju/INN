# Tasks

## 1. Playbooks y modelos

- [x] 1.1 Verificar en el texto de la Guía de Scrum 2020 los topes de las ceremonias y la definición del objetivo del sprint, y ampliar `common/scrum/guia.md` (secciones de planificación, Gantt, ceremonias y errores/checklist sin renumerar las anteriores); verificar que cubre cada requisito de las specs `sprint-plan` y `ceremonies-kanban` y que solo cita fuentes confirmadas
- [x] 1.2 Crear `common/scrum/models/spr-1-plan-sprints.md`, `spr-2-gantt-linea-base.md` y `spr-3-ceremonias.md` y actualizar `models/README.md`; verificar que cada plantilla tiene ficha, instrucciones, formato, ejemplo y checklist, que el esquema de `gantt.json` queda documentado con ejemplo y que los ejemplos usan las historias, el equipo y las fechas de los ejemplos de `common/user-stories/` y `common/scrum/`
- [x] 1.3 Escribir `common/kanban/guia.md` y crear `common/kanban/models/kan-1-tablero.md`, `kan-2-wip-metricas.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist, documentando el esquema de `tablero.json`; verificar que los términos coinciden con el glosario del marco metodológico y que los enlaces resuelven

## 2. Validación del plan

- [x] 2.1 Registrar la carpeta `sprint-plan` en `RULES` de `validate_run.py` e implementar `rules/sprint_plan.py` (config, backlog, sprints y fechas, reparto, capacidad, dependencias, tareas, ciclos, `gantt.json` igual a las tablas) con pruebas que usen como fixture los ejemplos de las plantillas, un config con tres avances y un backlog de ejemplo; verificar que pasa con un ejemplo completo y que informa archivo y causa con una fecha distinta del config, un sprint sobrecargado, una dependencia invertida, una tarea fuera de su sprint, un ciclo, una historia sin tareas y un `gantt.json` desalineado

## 3. Validación de ceremonias y Kanban

- [x] 3.1 Registrar la carpeta `ceremonies-kanban` en `RULES` e implementar `rules/ceremonies_kanban.py` (ceremonias, topes, fechas, columnas, políticas, WIP, métricas, `tablero.json` contra `kanban.md` y contra el plan vigente) con pruebas con fixtures de las plantillas; verificar que pasa con un ejemplo completo y que informa archivo y causa con una Daily de una hora, una Retrospective antes de la Review, una columna sin política, un WIP no numérico, una métrica ausente, una tarjeta sin tarea y una tarea sin tarjeta

## 4. Skills

- [x] 4.1 Crear `.claude/skills/11-make-sprint-plan/SKILL.md` (fechas del config, preguntas de inicio y capacidad, reparto, tareas, confirmación, escritura, validación y registro); verificar que aparece en la lista y que cada requisito de la spec `sprint-plan` tiene una instrucción
- [x] 4.2 Crear `.claude/skills/12-make-ceremonies-kanban/SKILL.md` (plan vigente, ceremonias, tablero, confirmación, escritura, validación y registro); verificar que aparece en la lista y que cada requisito de la spec `ceremonies-kanban` tiene una instrucción

## 5. Skills update

- [x] 5.1 Crear `.claude/skills/11-make-sprint-plan-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de cada `TAR` y de cada historia, y qué corridas posteriores los citan); verificar que sigue el patrón de `run-versioning` y que mantiene `gantt.json` igual a las tablas
- [x] 5.2 Crear `.claude/skills/12-make-ceremonies-kanban-update/SKILL.md` y `references/dependencias.md`; verificar que sigue el patrón de `run-versioning`, que cubre la resincronización de tarjetas con el plan y que mantiene `tablero.json` igual a `kanban.md`

## 6. Verificación final

- [x] 6.1 Ejecutar `openspec validate add-sprint-plan-ceremonies --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `11-…` y `12-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. Las skills `11-make-sprint-plan` y `12-make-ceremonies-kanban` y sus `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-html-boards`.
