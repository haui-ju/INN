# Design

## Context

Ver `proposal.md` (Why) para la motivación. Estado actual relevante:

- Las skills viven en `.claude/skills/NN-...` y comparten el kit `.claude/skills/_shared/` (`pipeline.json`, `projectcfg.py`, `runs.py`, `validate_run.py`, `yamlmini.py`, un módulo y un validador en `rules/` por capacidad, y tests en `tests/`).
- Los playbooks y modelos están en `common/<tema>/` y las corridas se escriben en `project/<carpeta>/<fecha-hora>/`, con la carpeta definida en `pipeline.json`.
- `project/` está vacío en el árbol de trabajo (los archivos figuran borrados en git), así que no hay corridas ni config que migrar.
- Las skills retiradas son el molde de las nuevas de los changes 2 a 4, por lo que su código debe poder consultarse después de borrarlo.

## Goals / Non-Goals

**Goals:**
- Dejar una base ejecutable y coherente: `pipeline.json` de `00` a `13`, config con `informe.secciones`, índice de cinco capítulos y las skills `00`, `01` y `02` con sus `-update`.
- Que todo lo que queda en el repositorio funcione (tests del kit en verde) y que nada cite lo retirado.
- Conservar acceso de solo lectura al código viejo para usarlo de molde.

**Non-Goals:**
- Crear skills de contenido (`03` en adelante), el ensamblado del informe o validadores nuevos del informe: son los changes 2 a 4.
- Decidir la herramienta del ETL o el modo de construcción del dashboard (congelado).
- Migrar corridas existentes: no las hay.

## Decisions

**D1. El molde se conserva con una etiqueta de git, no con copias.**
Antes de borrar se crea la etiqueta `pre-bi-pipeline` sobre el commit actual. Los changes siguientes leen el molde con `git show pre-bi-pipeline:<ruta>`. Alternativas: una carpeta `molde/` dentro del repositorio (ensucia el árbol, hay que acordarse de borrarla y el kit podría cargarla por error) o una rama (equivalente, pero una etiqueta no se mueve por accidente). Como crear una etiqueta es una acción de git, la tarea la pide al usuario antes de ejecutarla; el árbol de trabajo tiene archivos borrados sin commit, así que la etiqueta se pone sobre `HEAD`, donde las skills viejas siguen presentes.

**D2. Las specs de las capacidades retiradas se borran, no se marcan `REMOVED`.**
Son 25 specs con unos 305 requisitos (incluye `html-templates`, `html-visuals` y `report-assembly`, que los changes 2 y 4 vuelven a especificar); un delta `REMOVED` exige razón y migración por cada uno y no vacía el directorio. Se borran sus carpetas en `openspec/specs/` como tarea del apply, y la lista de las borradas queda en `tasks.md` como registro. Alternativa descartada: `REMOVED` requisito por requisito (volumen enorme sin valor de decisión).

**D3. El config sube a `schema: 3`.**
Cambian los campos (se van `enfoque`, `resultado_esperado`, `avances` y los roles de Scrum; llegan `calendario` e `informe`). Un config con `schema: 2` (el actual) se rechaza con el aviso que ya existe para versiones desconocidas y se remite a `00-init`. Alternativa: migrar el config viejo; se descarta porque no hay configs que conservar.

**D4. El registro de secciones se deriva de `pipeline.json` y el config solo guarda el estado.**
`pipeline.json` es la fuente de qué skill aporta qué sección; `informe.secciones` guarda por sección la skill, el `run` y el estado. Así hay una sola lista que mantener, y la validación completa o rechaza diferencias (spec `report-section-registry`). Alternativa: guardar la lista completa solo en el config, que obliga a editar dos sitios al agregar una skill.

**D5. `register` marca las secciones; el estado no se calcula en cada consulta, salvo el chequeo de existencia.**
`register` (ya existente) escribe `run`, `historial` y ahora las secciones de la skill. La consulta de disponibles vuelve a comprobar que la carpeta del `run` exista y degrada a pendiente si no. Alternativa: calcular todo en cada consulta recorriendo `pasos`; es más simple pero pierde el orden de las secciones y obliga a recorrer el disco siempre.

**D6. `pipeline.json` declara las catorce skills aunque las de `08` en adelante no existan aún.**
El kit ya omite los prerrequisitos que no existen como skill. Declararlas desde ahora fija los números y las secciones, y evita que cada change posterior reabra el esquema del registro. La skill se considera existente si su carpeta está en `.claude/skills/`.

**D7. Kit compartido: se queda lo genérico, se retira lo específico y se rehace en su change.**

| Se queda (y se adapta si hace falta) | Se retira (consultable en la etiqueta) |
|---|---|
| `yamlmini.py`, `runs.py`, `validate_run.py`, `projectcfg.py`, `policy.json`, `brief.py`, `rules/project_brief.py`, `rules/design_system.py` | `boards.py`, `mockups.py`, `app_scaffold.py`, `plan_schema.py`, `report.py`, `report_prosa.py`, `report_map.json`, el resto de `rules/` |
| `html_tpl.py`, `doc_html.py`, `visuales.py` (solo si importan sin errores tras el borrado; si no, se recortan a lo reutilizable) | `rules/report.py` y sus tests |

El ensamblado actual (`report*.py`) se retira porque depende de 18 pasos que dejan de existir; el change 4 lo rehace desde la etiqueta con la lógica por secciones. Entre los changes 1 y 3 no hay skill de informe, y eso es esperado.

**D8. `common/` y `common/html/`.**
Se renombran `common/project-brief` a `common/01-project-brief` y `common/design-system` a `common/02-design-system`; se reescribe `common/structure/model1.md`; se conservan `citation-style` y `document-html`; en `common/html/` se conservan `DESIGN.md`, `README.md`, `_build`, `vista-previa` y `foda` (se adapta en el change 2) y se borran los demás visuales. Las demás carpetas de `common/` se borran.

**D9. Anexos A a D del índice se fijan ahora.**
A Diccionario y calidad de datos, B Scripts del ETL, C Medidas y cálculos, D Especificación y capturas del dashboard. Son lo mínimo que los changes 3 y 5 necesitan para saber a dónde van sus salidas, y se pueden ampliar después sin renumerar (spec `skill-pipeline`, «Ampliación del índice»).

**D10. `scripts/check-pipeline.mjs`** se adapta al nuevo `pipeline.json` (orden consecutivo, carpetas numeradas, secciones únicas) en lugar de borrarse, porque es el comprobador del pipeline fuera de Python.

## Risks / Trade-offs

- **Borrado masivo sin marcha atrás fácil** → la etiqueta `pre-bi-pipeline` se crea y se verifica (`git show` de un archivo de una skill retirada) antes de borrar nada; el borrado va en su propio grupo de tareas, después de que lo nuevo funcione.
- **Referencias huérfanas a lo retirado** (por ejemplo `00b`, `01-design-system`, «avance», rutas viejas) → grupo final de integración con búsqueda de textos prohibidos en `.claude/skills/`, `common/` y `scripts/`.
- **El kit se rompe a mitad del trabajo** (módulos que se importan entre sí) → antes de borrar un módulo se busca quién lo importa; los tests del kit corren al cerrar cada grupo, no solo al final.
- **El molde queda fuera del árbol** y es fácil olvidarlo → cada change siguiente lista en sus tareas qué archivos de la etiqueta toma como base.
- **`visuales.py` podría estar muy acoplado a lo retirado** → si no importa limpio, se recorta a la parte reutilizable y se anota para el change 2.
- **Dos listas de secciones desincronizadas** (`pipeline.json` y config) → la validación las reconcilia (D4).

## Migration Plan

1. Crear la etiqueta `pre-bi-pipeline` y verificar que contiene las skills viejas.
2. Construir lo nuevo con el árbol actual aún intacto (pipeline, config, registro, índice, skills `00` a `02`).
3. Adaptar los tests del kit a lo nuevo y ponerlos en verde.
4. Borrar lo retirado (skills, `common/`, módulos del kit, tests, specs) y volver a correr los tests.
5. Búsqueda final de referencias huérfanas y validación del change.

Reversión: restaurar desde la etiqueta con `git checkout pre-bi-pipeline -- <ruta>`; el borrado no se commitea hasta que el usuario lo decida.
