# Proposal

## Why

El capítulo 4 del informe empieza por quién hace qué en Scrum (4.1) y qué debe cumplir el sistema (4.2 y 4.3). Hoy ninguna skill lo produce, y todo lo que sigue (historias, plan de sprints, ceremonias) depende de ello: las historias parten de los requerimientos y el plan de sprints necesita saber quién es Product Owner, quién Scrum Master y quién desarrolla. Además, `equipo[].rol` del config existe pero nadie lo completa y nada valida sus valores, aunque `00-init` y `00-init-update` ya indican que lo confirma `08-make-scrum-setup`.

## What Changes

- **Nueva skill `08-make-scrum-setup`**: propone el reparto de roles (Product Owner, Scrum Master y equipo de desarrollo) entre las personas del config, la cadencia de los tres sprints (= tres avances, con las fechas del config) y los artefactos de Scrum; pide confirmación y escribe `project/scrum-setup/<corrida>/` con `equipo-scrum.md`, `artefactos.md` y `README.md`. **Escribe los roles confirmados en `equipo[].rol` del config.**
- **Nueva skill `09-make-requirements`**: deriva los requerimientos funcionales (RF) de los `REQ` del Design Thinking y propone los no funcionales (RNF) con métrica, meta y categoría; pide confirmación y escribe `project/requirements/<corrida>/` con `rf.md`, `rnf.md`, `matriz-trazabilidad.md` y `README.md`.
- **Dos skills `-update`**: `08-make-scrum-setup-update` (cambia roles, que también actualiza el config, y artefactos) y `09-make-requirements-update` (agrega, quita o corrige RF y RNF y su matriz).
- **Dos playbooks nuevos** con plantillas, en el formato de las de Design Thinking: `common/scrum/` (`guia.md`, `scr-1-equipo-roles`, `scr-2-artefactos`, `README.md`) y `common/requirements/` (`guia.md`, `req-1-rf`, `req-2-rnf`, `req-3-matriz-trazabilidad`, `README.md`). El playbook de Scrum lo ampliará después el cambio de planificación y ceremonias.
- **Códigos de trazabilidad propios:** `RF-nn` y `RNF-nn`; los RF citan `REQ-nn` del Design Thinking.
- **Función del config para los roles:** `projectcfg.set_roles` y `projectcfg.py set-roles` validan que el reparto tenga exactamente un Product Owner, exactamente un Scrum Master y al menos un integrante de desarrollo, solo con personas del equipo; el campo `rol` solo acepta esos tres valores.
- **Validación propia de cada paso** (`rules/scrum_setup.py`, `rules/requirements.py`): estructura, coherencia con el config y con la corrida vigente de Design Thinking, cobertura de los `REQ`, y métricas verificables.

## Capabilities

### New Capabilities
- `scrum-setup`: playbook y modelos de Scrum, skills `08-make-scrum-setup` y su `-update`, roles en el config, cadencia, artefactos y validación.
- `requirements`: playbook y modelos de requerimientos, skills `09-make-requirements` y su `-update`, RF y RNF trazables, matriz y validación.

### Modified Capabilities
- `project-config`: el campo `rol` del equipo solo admite los tres roles de Scrum y se define cómo se escriben.

## Impact

- **Archivos nuevos:** `common/scrum/`, `common/requirements/`, `.claude/skills/08-make-scrum-setup/`, `08-make-scrum-setup-update/`, `09-make-requirements/`, `09-make-requirements-update/`, `.claude/skills/_shared/rules/scrum_setup.py`, `requirements.py` y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/projectcfg.py` (validación de roles, `set_roles`, comando `set-roles`) y sus pruebas, `.claude/skills/_shared/validate_run.py` (registra las dos carpetas), y el texto de `00-init-update` sobre roles.
- **Consumidores:** `10-make-user-stories` (RF), `11-make-sprint-plan` y `12-make-ceremonias-kanban` (roles y cadencia), `14-make-system-design`, `19-make-report`.
- **Índice:** alimenta 4.1.1, 4.1.2, 4.2 y 4.3; `model1.md` no cambia.
- **Fuera de alcance:** historias de usuario, criterios de aceptación y Definition of Done (cambio 8), planificación de sprints y ceremonias (cambio 9), ejecutar las skills.
- **Supuestos registrados:** con cuatro personas la propuesta por defecto es un Product Owner, un Scrum Master y dos del equipo de desarrollo, y una persona tiene un solo rol en el config (puede indicar que también desarrolla); la prioridad de los RF usa tres niveles (Debe, Debería, Podría); las categorías de RNF y las fuentes se verifican antes de escribirlas.
