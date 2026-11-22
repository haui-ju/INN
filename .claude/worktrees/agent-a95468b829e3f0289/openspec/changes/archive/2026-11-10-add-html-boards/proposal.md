# Proposal

## Why

El plan de sprints (`gantt.json`) y el diseño del tablero (`tablero.json`) ya existen como datos, pero el informe necesita verlos: el Gantt y el Kanban con el progreso marcado y fechado (puntos 6.x.2 y 6.x.4, y los anexos A.1 y A.2), y el equipo necesita una vista de trabajo que pueda actualizar sin rehacer nada. Además, el diseño visual del proyecto (`01-design-system`) todavía no se usa en ninguna pieza. Hace falta una skill que convierta esos datos en dos tableros HTML autónomos con la identidad del proyecto, y que separe la **línea base** (el plan) del **estado real** (lo avanzado a una fecha de corte).

## What Changes

- **Nueva skill `13-design-html-boards`**: lee el plan de sprints y el tablero Kanban vigentes y los tokens del sistema de diseño, pregunta qué estado real mostrar (tareas, columnas, fechas) y la fecha de corte, pide confirmación y escribe `project/html-boards/<corrida>/` con `gantt.html`, `kanban.html`, `data.json` y `README.md`. Registra la corrida en el config.
- **Nueva skill `13-design-html-boards-update`**: actualiza el estado real o la fecha de corte, resincroniza con el plan y el tablero vigentes, cambia el diseño o corrige datos (copia `-fork`); el HTML es **derivado** de `data.json` y se vuelve a generar, lo demás queda idéntico.
- **Nuevo playbook `common/html-boards/`**: `guia.md` (reglas de HTML autónomo, qué muestra cada tablero, separación de línea base y estado, cálculos, capturas para el informe, publicación opcional, errores frecuentes, checklist) y `models/` con `html-1-gantt`, `html-2-kanban`, `html-3-esquema-datos` y un `README.md`, con el formato de las plantillas anteriores.
- **Kit de generación** (`.claude/skills/_shared/boards.py`): calcula los indicadores del estado (avance, tareas hechas, tiempo de ciclo, rendimiento semanal, WIP actual, tareas atrasadas) y genera los dos HTML a partir de `data.json` y de los tokens; lo usan la skill y el validador, para que no haya dos implementaciones.
- **`data.json` único** con la línea base copiada de `gantt.json` y `tablero.json`, el `estado` real (separado) y lo `calculado`; el HTML lo lleva embebido.
- **Fecha de corte visible:** cada tablero muestra «al DD-MM-AAAA» y la leyenda de lo que representa, para que las capturas del informe vayan fechadas. La skill **no** genera imágenes: el usuario captura desde su navegador; la corrida explica cómo.
- **Publicación privada opcional:** tras validar, la skill ofrece publicar una vista privada con Artifact; solo con confirmación explícita y el enlace se anota en el `README.md` de la corrida.
- **Validación propia del paso** (`rules/html_boards.py`): `data.json` coherente con el plan y el tablero vigentes, estado consistente, indicadores recalculados, HTML autónomo con los tokens correctos y fecha de corte visible.

## Capabilities

### New Capabilities
- `html-boards`: playbook y modelos de los tableros HTML, skills `13-design-html-boards` y su `-update`, esquema de `data.json`, estado real, indicadores, HTML autónomo con el sistema de diseño y su validación.

### Modified Capabilities
- Ninguna. Los esquemas de `gantt.json` y `tablero.json` (specs `sprint-plan` y `ceremonies-kanban`) se consumen sin cambios.

## Impact

- **Archivos nuevos:** `common/html-boards/`, `.claude/skills/13-design-html-boards/`, `.claude/skills/13-design-html-boards-update/`, `.claude/skills/_shared/boards.py`, `.claude/skills/_shared/rules/html_boards.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/validate_run.py` (registra la carpeta `html-boards`).
- **Consumidores:** `16-make-sprint-report` (capturas y cifras de 6.x.2 y 6.x.4), `15-make-implementation-log`, `19-make-report` (anexos A.1 y A.2).
- **Índice:** alimenta los anexos A.1 y A.2 y las capturas de 6.x.2 y 6.x.4; `model1.md` no cambia.
- **Fuera de alcance:** generar imágenes, el `-update` de `06-make-design-thinking-prototypes`, aplicar el diseño a otras piezas, ejecutar las skills.
- **Supuestos registrados:** el avance de una tarea es un entero de 0 a 100 que informa el usuario; el estado real inicial está vacío (línea base pura); sin sistema de diseño vigente se usan los tokens base de `01-design-system` y se avisa; las cifras se calculan con días calendario.
