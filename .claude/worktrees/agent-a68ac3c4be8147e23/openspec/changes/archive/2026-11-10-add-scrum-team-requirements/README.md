# add-scrum-team-requirements: Equipo Scrum y requerimientos

**Cambio 7 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-scrum-team-requirements`).

## Valor
Define quién hace qué (roles confirmados con el usuario) y qué debe cumplir el sistema (RF y RNF trazados a los `REQ` del Design Thinking). Es la base de las historias y del plan de sprints.

## Skills
- `08-make-scrum-setup` y `08-make-scrum-setup-update`.
- `09-make-requirements` y `09-make-requirements-update`.

## Prerrequisitos
08: `00-init`, `05-make-design-thinking`. 09: `05-make-design-thinking`, `08-make-scrum-setup`.

## Playbooks
- `common/scrum/guia.md` (lo crea este cambio; lo amplía el cambio 9): roles (Product Owner, Scrum Master, equipo de desarrollo), artefactos (Product Backlog, Sprint Backlog, Incremento), **3 sprints = 3 avances**, duración tomada de `avances` del config, reglas para asignar roles a 4 personas.
- `common/requirements/guia.md` (lo crea este cambio): RF derivados de `REQ`, RNF por categoría de calidad (por ejemplo ISO 25010), redacción verificable, prioridad.

Códigos propuestos: `RF-nn`, `RNF-nn`; cita `REQ-nn`.

## Modelos y formularios
- `common/scrum/models/`: `scr-1-equipo-roles.md`, `scr-2-artefactos.md`, `README.md`.
- `common/requirements/models/`: `req-1-rf.md`, `req-2-rnf.md`, `req-3-matriz-trazabilidad.md` (REQ→RF), `README.md`.

## Qué pregunta la skill
08: quién es Product Owner y quién Scrum Master (propone según `equipo` del config y espera confirmación), duración del sprint, si hay stakeholder externo. **Escribe los roles confirmados en `equipo[].rol` del config** (único paso que modifica el equipo). 09: prioridad de cada RF, qué RNF aplican (rendimiento, usabilidad, seguridad, etc.) y el criterio medible de cada uno.

## Salida
- `project/scrum-setup/<corrida>/`: `equipo-scrum.md`, `artefactos.md`.
- `project/requirements/<corrida>/`: `rf.md`, `rnf.md`, `matriz-trazabilidad.md`.

## Índice
Alimenta **4.1.1, 4.1.2, 4.2 y 4.3**. Sin cambios al índice.

## Update
Cambiar un rol (también actualiza el config), agregar/quitar/corregir un RF o RNF y su fila en la matriz.

## Validación
08: un Product Owner y un Scrum Master, ningún integrante sin rol, roles solo de miembros del config. 09: cada `REQ` cubierto por al menos un `RF`, cada `RNF` con criterio medible, códigos citados definidos.

## Fuera de alcance
Historias y criterios de aceptación (cambio 8), planificación (cambio 9).

## Decisiones abiertas para el proposal
- Un integrante puede tener más de un rol de desarrollo; confirmar qué combinaciones se permiten.
- Marco de categorías para RNF (ISO 25010 u otro).

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
