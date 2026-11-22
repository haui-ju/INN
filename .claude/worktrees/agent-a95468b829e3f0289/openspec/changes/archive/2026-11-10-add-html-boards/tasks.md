# Tasks

## 1. Playbook y modelos

- [x] 1.1 Escribir `common/html-boards/guia.md` (reglas, HTML autónomo, línea base y estado, Gantt, Kanban, cálculos, capturas, publicación opcional, errores y checklist); verificar que cubre cada requisito de la spec `html-boards` y que no cita fuentes sin verificar
- [x] 1.2 Crear `common/html-boards/models/html-1-gantt.md`, `html-2-kanban.md`, `html-3-esquema-datos.md` y `README.md` con ficha, instrucciones, formato, ejemplo y checklist; verificar que el ejemplo de `data.json` es coherente con los ejemplos de `gantt.json` y `tablero.json` de `common/scrum/` y `common/kanban/` y que sus indicadores coinciden con los que calcula el kit

## 2. Kit de generación

- [x] 2.1 Implementar `.claude/skills/_shared/boards.py` (cálculo de indicadores, generación determinista de `gantt.html` y `kanban.html` desde `data.json` y los tokens, y comandos `calcular` y `render`) con pruebas; verificar el cálculo con casos conocidos (promedios, semanas, atrasadas, WIP), que el HTML generado no tiene recursos externos, que lleva el JSON embebido igual a `data.json`, que alterna el tema y que dos ejecuciones producen el mismo archivo

## 3. Validación

- [x] 3.1 Registrar la carpeta `html-boards` en `RULES` e implementar `rules/html_boards.py` (`data.json` contra el plan y el tablero vigentes, reglas de estado, indicadores recalculados, tokens, HTML autónomo, datos embebidos, tareas y tarjetas presentes, fecha de corte) con pruebas con fixtures de las plantillas y de los ejemplos de plan y tablero; verificar que pasa con un ejemplo completo y que informa archivo y causa con una tarea del plan ausente, un estado incoherente, un indicador desactualizado, un recurso externo, un color distinto al token, un JSON embebido distinto y una fecha de corte ausente

## 4. Skills

- [x] 4.1 Crear `.claude/skills/13-design-html-boards/SKILL.md` (fuentes, tokens, preguntas de estado y fecha de corte, resumen con confirmación, escritura con `boards.py`, validación, registro, capturas y publicación opcional); verificar que aparece en la lista y que cada requisito de la spec tiene una instrucción
- [x] 4.2 Crear `.claude/skills/13-design-html-boards-update/SKILL.md` y `references/dependencias.md` (qué archivos dependen de qué y qué corridas posteriores los citan); verificar que sigue el patrón de `run-versioning`, que cubre los modos de estado, resincronización y diseño, y que siempre regenera los HTML tras editar `data.json`

## 5. Verificación final

- [x] 5.1 Ejecutar `openspec validate add-html-boards --strict`, `openspec validate --specs --strict`, las pruebas del kit y la comprobación de que las skills `13-…` aparecen ordenadas en `.claude/skills/`; verificar que todo pasa

## Workflow follow-up

- Archivar el cambio. La skill `13-design-html-boards` y su `-update` se ejecutan solo cuando el usuario lo pida.
- Continuar con el cambio `add-system-design`.
