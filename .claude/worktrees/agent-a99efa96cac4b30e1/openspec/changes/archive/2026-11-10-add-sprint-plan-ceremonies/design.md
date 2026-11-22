# Design

## Context

Estado observado: `pipeline.json` define `11-make-sprint-plan` (requiere `08` y `10`) y `12-make-ceremonies-kanban` (requiere `08` y `11`), ambas con `update`. El config trae las tres fechas de entrega de los avances (pueden ser `null`) y el equipo con roles. `08-make-scrum-setup` escribe la cadencia (`Sprint | Avance | Fecha de entrega`). `10-make-user-stories` aporta `backlog.md` (orden, prioridad, estimación en una escala declarada, `RF sin historia`) y las historias. El marco metodológico define en el glosario Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective, Tablero, Columna, WIP, Tiempo de ciclo y Rendimiento. `common/scrum/guia.md` reserva "Planificación y ceremonias" para este cambio. El cambio de tableros HTML (10) leerá `gantt.json` y `tablero.json`. Las reglas existentes (`scrum_setup.py`, `user_stories.py`) ya leen config y backlog con `projectcfg.current_run` y ofrecen funciones reutilizables.

## Goals / Non-Goals

**Goals:** un reparto de historias en tres sprints verificable; un Gantt de línea base con tareas, fechas y dependencias coherentes; ceremonias y tablero definidos; datos estructurados estables para las vistas HTML y los informes.

**Non-Goals:** las vistas HTML, el avance real y las métricas medidas, ejecutar las skills.

## Decisions

### D1. Salida de 11
`plan-sprints.md` (título `# Plan de sprints · [proyecto]` y `## 4.6.1. Planificación de sprints`): `**Inicio del proyecto.**`, `**Unidad de capacidad.**`, tabla `Sprint | Avance | Inicio | Fin | Capacidad | Objetivo del sprint`, tabla `Sprint | HU | Historia | Estimación | Depende de` y tabla opcional `### Historias diferidas` (`HU | Motivo`). `gantt-linea-base.md` (`## 4.6.2. Diagrama de Gantt`): tabla `Código | Tarea | HU | Sprint | Inicio | Fin | Predecesoras | Responsable`; el diagrama visual lo genera `13-design-html-boards`. `gantt.json` con el esquema D3. Fechas en markdown `DD-MM-AAAA`, en JSON ISO `AAAA-MM-DD`.

### D2. Sprints, capacidad y reparto
Fin de cada sprint = fecha de avance del config. Inicio del sprint 1 = el que da el usuario; inicio de los siguientes = día siguiente al fin del anterior. La capacidad es una cifra de **puntos de historia** por sprint que fija el usuario (la skill propone repartir la carga total en partes parecidas con margen); si el backlog usa tallas, se convierten con XS=1, S=2, M=3, L=5, XL=8. El reparto sigue el orden del backlog (prioridad) respetando dependencias entre historias (`Depende de`), y lo que no cabe se propone como diferido con motivo. Falla si falta una fecha de avance (se pide `00-init-update`).

### D3. Esquemas JSON
`gantt.json`:
```json
{"schema": 1, "proyecto": "...",
 "sprints": [{"n": 1, "avance": 1, "inicio": "2026-11-01", "fin": "2026-11-30", "capacidad": 13, "objetivo": "..."}],
 "tareas": [{"codigo": "TAR-01", "nombre": "...", "hu": "HU-01", "sprint": 1, "inicio": "2026-11-02", "fin": "2026-11-06", "predecesoras": [], "responsable": "ju"}]}
```
`hu` es `null` para tareas del proyecto (por ejemplo la entrega del avance). `tablero.json`:
```json
{"schema": 1, "proyecto": "...",
 "columnas": [{"nombre": "Por hacer", "wip": null, "politica_entrada": "...", "politica_salida": "..."}],
 "metricas": [{"codigo": "MKB-01", "nombre": "Tiempo de ciclo", "unidad": "días"}],
 "tarjetas": [{"codigo": "TAR-01", "titulo": "...", "hu": "HU-01", "sprint": 1, "columna": "Por hacer"}]}
```
Los JSON son **derivados**: su contenido debe ser igual al de las tablas, y el `-update` los mantiene sincronizados. El cambio 10 los toma como entrada sin redefinirlos.

### D4. Tareas del Gantt
`TAR-nn`, de 2 a 4 por historia (por ejemplo diseñar, construir, probar y revisar con el Product Owner), más un hito de entrega por avance (`HU` = «—»). Fechas dentro del sprint de la tarea; inicio ≤ fin; cada predecesora existe, termina **antes** de que empiece la tarea y no hay ciclos (se detectan con un recorrido del grafo). Responsable: un integrante del equipo del config.

### D5. Salida de 12
`ceremonias.md` (`## 4.7. Ceremonias de Scrum`): una subsección `### 4.7.n. Nombre` por ceremonia con etiquetas `**Cuándo.**`, `**Duración.**`, `**Participantes.**`, `**Entradas.**` y `**Salidas.**`, y la tabla de calendario `Ceremonia | Sprint | Fecha | Hora | Duración`. `kanban.md` (`## 4.8. Kanban: diseño del tablero`): `### 4.8.1. Columnas y políticas` (`Columna | Significado | Política de entrada | Política de salida`), `### 4.8.2. Límites de trabajo en curso (WIP)` (`Código | Columna | Límite | Motivo`) y `### 4.8.3. Métricas definidas` (`Código | Métrica | Definición | Cómo se calcula | Unidad | Frecuencia`). `tablero.json` según D3.

### D6. Ceremonias
Topes para un sprint de un mes (Schwaber y Sutherland, 2020; a confirmar en el texto de la guía): Planning 8 h, Daily 15 min, Review 4 h, Retrospective 3 h. Calendario: Planning en la fecha de inicio del sprint; Review y Retrospective dentro del sprint, Retrospective no antes que la Review. Participantes: personas del equipo del config (con su rol) y, en la Review, el interesado externo de `equipo-scrum.md` si existe.

### D7. Kanban
Columnas por defecto: Por hacer, En curso, En pruebas y Hecho (el usuario las ajusta). La columna inicial y la final no tienen límite; cada columna de trabajo tiene `WIP-nn` numérico > 0 con motivo; se avisa si un límite supera el tamaño del equipo de desarrollo. Métricas mínimas: `MKB-nn` Tiempo de ciclo y Rendimiento (coherentes con el glosario); se definen aquí y se miden en los informes de sprint (Anderson y Carmichael, 2016). Tarjetas: una por cada `TAR` del `gantt.json` vigente, en la columna inicial.

### D8. Dependencia entre 11 y 12
12 requiere 11 (decidido): las tarjetas y las fechas salen del plan. No se ejecutan en paralelo. Si el plan cambia después, el tablero queda desalineado (la validación lo marca) y se resincroniza con `12-make-ceremonies-kanban-update`.

### D9. Playbooks y plantillas
`common/scrum/guia.md`: se reemplaza la sección reservada por **5. Planificación de sprints**, **6. Gantt de línea base**, **7. Ceremonias** y **8. Errores y checklist de planificación**; secciones 1 a 4 sin cambios. `common/kanban/guia.md`: 0 reglas, 1 columnas y políticas, 2 WIP, 3 métricas, 4 errores y checklist, referencias. Plantillas: `spr-1-plan-sprints`, `spr-2-gantt-linea-base`, `spr-3-ceremonias`, `kan-1-tablero`, `kan-2-wip-metricas` y los `README`.

### D10. Validación
`rules/sprint_plan.py` (`PREFIJOS = ["TAR"]`): config (fechas, equipo), backlog vigente (HU, estimaciones, escala), estructura, reparto, capacidad, dependencias de historias y de tareas, fechas de tareas, `gantt.json` igual a las tablas. `rules/ceremonies_kanban.py` (`PREFIJOS = ["WIP", "MKB"]`): estructura, plan vigente (`gantt.json`), topes y fechas de ceremonias, columnas, WIP, métricas obligatorias, `tablero.json` igual a `kanban.md` y a las tareas del plan. Sin config, backlog o plan vigente, un aviso por cada comprobación imposible.

### D11. Fuentes
Schwaber y Sutherland (2020) para ceremonias, sprint y objetivo del sprint (verificada; los topes se confirman en el texto de la guía). Anderson (2010) y Anderson y Carmichael (2016) para Kanban (verificadas). Máximo 1 o 2 citas por archivo. No se citan fuentes nuevas salvo que se verifiquen.

### D12. `-update`
Patrón del cambio 1. `11-…-update`: modos de historias entre sprints, capacidad, dependencias, tareas y fechas, objetivos; mantiene `gantt.json`. `12-…-update`: ceremonias, columnas/políticas, WIP, métricas y resincronización de tarjetas; mantiene `tablero.json`. Cada uno con `references/dependencias.md`.

## Risks / Trade-offs

- [Capacidad en puntos poco realista sin historial] → La skill pregunta y propone un margen; los informes de sprint muestran el rendimiento real y el `-update` ajusta.
- [Plan y tablero se desalinean al editar el plan] → La validación del tablero compara con el plan vigente; la resincronización es un modo del `-update`.
- [JSON y markdown divergen] → Validación de igualdad exacta; el JSON se deriva del markdown.
- [Tareas genéricas] → 2 a 4 por historia, pedidas al usuario; las edita el `-update`.
- [Fechas de avance vacías en el config] → La skill se detiene e indica `00-init-update`.
- [Change grande (dos skills, dos playbooks)] → Dos capacidades con tareas separadas, aplicables en orden.

## Migration Plan

Se amplía `common/scrum/guia.md` sin tocar sus secciones 1 a 4. Sin migración de datos: ambos pasos son nuevos.

## Open Questions

- Si algún día la capacidad debe medirse en horas además de puntos (por ahora no).
- Si el Gantt debe distinguir días hábiles (por ahora días calendario).
