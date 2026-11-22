# Proposal

## Why

Hoy el núcleo del proyecto está repartido: `00-init` pregunta el tema, el resultado esperado, el enfoque y las fechas de entrega y arma `domain.md`; `02` vuelve a preguntar el problema; `03` propone los objetivos; `11` pregunta el inicio del proyecto. No hay un lugar donde el usuario defina, con calma y puliéndolo, **de qué trata el proyecto, cuál es su problemática, qué objetivos persigue, qué entra y qué no, quiénes son los usuarios, cuándo son los tres sprints y qué se espera lograr**. Esa información debe ser **única** y todas las demás skills deben leerla.

## What Changes

- **Skill nueva `00b-make-project-brief` (y `00b-make-project-brief-update`)**, justo después de `00-init`. Pregunta al usuario sección por sección, propone una redacción, la pule con él y, tras su confirmación, escribe `project/project-brief/<corrida>/brief.md` (el núcleo) y `project/domain.md` (datos de la empresa por RUC o de la solución, que necesitan el tema ya definido). Guarda en `project/config.yaml` las copias que ya leen otras skills (tema, resultado esperado, enfoque y fechas).
- **El brief** tiene ocho secciones: Tema, Problemática, Objetivos (`OG-01` y `OE-nn` medibles, con métrica, meta y plazo), Justificación y alcance, Usuarios y enfoque, Resultado esperado, **Calendario de los tres sprints** (inicio y entrega de cada uno) y Supuestos y riesgos iniciales (`INI-nn`).
- **Validación del brief:** secciones y tablas, objetivos medibles con plazo dentro del calendario, sprints ordenados y sin solaparse con la entrega dentro de su sprint, coherencia con el config y texto limpio.
- **`00-init` queda técnica:** nombre, rubro, tipo (empresa o propio), RUC, equipo y modo de datos. Deja de preguntar tema, enfoque, resultado y fechas y de armar `domain.md`. `00-init-update` cambia esos datos técnicos y, para los del núcleo, remite a `00b-make-project-brief-update`.
- **Todas las demás skills leen el brief:** `02` toma tema, problemática y resultado; `03` copia `OG-01` y los `OE-nn` y la justificación y el alcance; `05` el enfoque y los usuarios; `07` y `17` el resultado esperado y los supuestos; `08`, `11`, `12`, `13` y `19` el calendario; `18` los objetivos. Cada `SKILL.md` lo lista en sus fuentes y el kit avisa (sin bloquear) cuando falta.
- **Config:** `avances[].inicio` nuevo (inicio de cada sprint, opcional); `11-make-sprint-plan` deja de preguntar el inicio del proyecto y lo toma de ahí.
- **Pipeline:** paso `00b-make-project-brief` entre `00-init` y `01-design-system` (22 pasos).

## Capabilities

### New Capabilities
- `project-brief`: la skill `00b-make-project-brief` y su `-update`, el brief y sus secciones, el calendario de sprints, la creación de `domain.md`, la lectura obligatoria por las demás skills y la validación.

### Modified Capabilities
- `project-config`: campos (`inicio` por avance), `00-init` técnica, avances y sprints, `domain.md` y `00-init-update`.
- `skill-pipeline`: orden de 22 pasos y lectura del brief por todas las skills.
- `company-chapter`: fuentes y objetivos copiados del brief.
- `lean-canvas-initial`: lectura del tema, la problemática y el resultado del brief.
- `sprint-plan`: el primer inicio sale del config.

## Impact

- **Archivos nuevos:** `.claude/skills/00b-make-project-brief/` y `00b-make-project-brief-update/`, `common/project-brief/` (guía y modelos), `.claude/skills/_shared/brief.py` y `rules/project_brief.py` con sus pruebas.
- **Archivos modificados:** `pipeline.json`, `projectcfg.py` (campo `inicio`, `set-nucleo`, aviso de brief ausente), `validate_run.py`, las skills `00-init`, `00-init-update`, `02`, `03`, `05`, `07`, `08`, `11`, `12`, `13`, `17`, `18` y `19` (fuentes), `rules/company.py` y `rules/sprint_plan.py` (leen el brief y el inicio), la plantilla `domain-plantilla.md` y las pruebas del flujo.
- **Sin cambio:** el formato de los capítulos y de los demás entregables; el config sigue siendo la fuente que leen las skills para equipo, tipo y modo de datos.
- **Fuera de alcance:** ejecutar las skills; cambiar los objetivos ya redactados en corridas existentes (no hay corridas).
- **Decisiones que tomé por defecto:** el brief es una corrida versionada (`project/project-brief/<corrida>/`, con `-fork` y `-update` como las demás); `domain.md` pasa a crearlo 00b porque sus secciones modeladas (misión, visión, valores) necesitan el tema; el tema, el resultado esperado, el enfoque y las fechas viven en el brief y 00b los copia al config, y la validación exige que coincidan.
