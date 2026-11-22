# Proposal

## Why

Cada skill de generación pregunta hoy lo mismo (tema, enfoque, cuál corrida usar) y no recuerda nada de las anteriores. El proyecto va a tener unas 20 skills encadenadas (capítulo 1, Design Thinking, Lean, Scrum, sprints, resultados y armado del informe), cada una con su corrida versionada, y hace falta una fuente única que diga qué corrida es la vigente de cada paso, quién forma el equipo y cuáles son los 3 avances. También falta una forma barata de corregir una corrida ya hecha sin volver a generarla, y un orden claro de ejecución en los nombres de las skills.

## What Changes

- **Nueva skill `00-init`** que crea y mantiene `project/config.json` preguntando al usuario lo necesario (tema, empresa, rubro, enfoque A/B/C, resultado esperado, equipo y fechas de los 3 avances).
- **Esquema de `config.json`:** `schema`, `proyecto`, `enfoque`, `resultado_esperado`, `equipo`, `avances` (3 avances = 3 sprints, con fecha), `modo_datos` (`generado` o `real`), `diseno` y `pasos`, con `{run, fijada, historial}` por skill. La última corrida de cada paso se registra salvo que `fijada` sea `true`; el usuario puede editar el config a mano para preferir otra versión.
- **Kit compartido** en `.claude/skills/_shared/`: lectura y escritura del config, creación de carpetas de corrida `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/`, bifurcación de una corrida (`<fecha-hora>-fork`), validador de coherencia, `pipeline.json` con el orden y los prerrequisitos de cada skill, y la regla compartida de texto limpio.
- **Patrón de skills `-update`:** cada skill tiene una homóloga con sufijo `-update` que toma la corrida base del config, la copia como `-fork`, pide al usuario los cambios (agrega, quita, corrige), edita solo lo afectado y valida la coherencia, sin regenerar todo. `00-init` y `19-make-report` no tienen `update`. En este cambio se crea `05-make-design-thinking-update`.
- **Esquema de nombres** `[orden de dos dígitos]-[verbo]-[nombre]` (verbos `init`, `make` y `design`), con `-update` al final si aplica y sin letras. Orden: `00-init`, `01-design-system`, `02-make-initial-lean-canvas`, `03-make-company-chapter`, `04-make-methodological-framework`, `05-make-design-thinking`, `06-make-design-thinking-prototypes`, `07-make-lean-plan`, `08-make-scrum-setup`, `09-make-requirements`, `10-make-user-stories`, `11-make-sprint-plan`, `12-make-ceremonies-kanban`, `13-design-html-boards`, `14-make-system-design`, `15-make-implementation-log`, `16-make-sprint-report` (una vez por sprint), `17-make-lean-results`, `18-make-final-analysis`, `19-make-report`.
- **Renombre** de las dos skills existentes a `05-make-design-thinking` y `06-make-design-thinking-prototypes`, con todas sus referencias, y para que lean y escriban el config: dejan de preguntar tema y enfoque, registran su corrida al terminar y la de mockups usa la corrida de Design Thinking del config en lugar de preguntar cuál.
- **Comprobación de prerrequisitos:** cada skill verifica en el config que sus pasos anteriores estén hechos y avisa si no.
- **Principios para las skills futuras**, escritos en la spec: preguntan lo necesario y piden confirmación de las propuestas (roles, sprints, historias); si necesitan un playbook lo crean como el de Design Thinking (`common/<tema>/guia.md` y `models/`); si hace falta ampliar el índice o los anexos, se amplía.

## Capabilities

### New Capabilities
- `project-config`: contrato de `project/config.json` y de la skill `00-init` (campos, punteros de corrida, versión fijada, datos y confirmación de equipo, avances y prerrequisitos).
- `run-versioning`: corridas versionadas por fecha y hora, bifurcación (`-fork`), patrón de las skills `-update`, validación de coherencia y regla de texto limpio con el `README.md` de procedencia.
- `skill-pipeline`: esquema de nombres y orden de las skills, prerrequisitos entre pasos y principios que cumplen todas las skills de generación.

### Modified Capabilities
- `design-thinking-package-generation`: la recogida de información lee el config y la corrida se registra en él (requisitos «Recogida de información» y «Estructura de salida»).
- `design-thinking-prototype-mockups`: la corrida base sale del config y los nombres de skill cambian (requisitos «Selección de la corrida» e «Insumos de la corrida»).

## Impact

- **Archivos nuevos:** `.claude/skills/00-init/`, `.claude/skills/_shared/` (scripts y datos), `.claude/skills/05-make-design-thinking-update/` y `project/config.json`.
- **Renombrados y modificados:** `.claude/skills/make-design-thinking/` → `05-make-design-thinking/`; `.claude/skills/make-design-thinking-prototypes/` → `06-make-design-thinking-prototypes/`; sus `SKILL.md`, README, scripts y plantilla `dt-4b-inventario-pantallas.md`.
- **Migración:** la corrida existente `project/design-thinking/10-11-2026-00-00-46/` se registra en el config como la vigente del paso 05; el generador por defecto debe seguir produciendo exactamente ese paquete.
- **Fuera de alcance:** las skills `01` a `04`, `07` a `19`, el playbook de cada una, el `update` de la skill 06 (modifica tableros de Miro; queda para el cambio de los tableros) y el contenido de los capítulos. La hoja de ruta posterior (cambio 2 sistema de diseño; 3 capítulo 1 y canvas inicial; 4 marco metodológico; 5 Lean; 6 Scrum con sprints = avances, donde 5.4 pasa a `[A1+]`; 7 HTML de Gantt y Kanban; 8 diseño e implementación del sistema; 9 sprint report, análisis final y ensamblado) se tratará en cambios propios.
- **Relación con `reorder-report-index`:** ese cambio sigue activo y no se solapa; este no toca el índice.
