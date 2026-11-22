# add-user-stories-backlog: Historias de usuario, criterios y backlog

**Cambio 8 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-user-stories-backlog`).

## Valor
Traduce los requerimientos en historias de usuario con criterios de aceptación y un Product Backlog priorizado, que es la entrada directa del plan de sprints.

## Skills
- `10-make-user-stories` y `10-make-user-stories-update`.

## Prerrequisitos
`09-make-requirements`.

## Playbook
`common/user-stories/guia.md` (lo crea este cambio): formato «Como / Quiero / Para», criterios INVEST, criterios de aceptación en Dado/Cuando/Entonces, Definition of Done, escalas de estimación (puntos o tallas, a elegir), técnica de priorización (MoSCoW o valor/esfuerzo).

Códigos propuestos: `HU-nn`, `CA-nn`; cita `RF-nn` y `REQ-nn`.

## Modelos y formularios (`common/user-stories/models/`)
- `hu-1-historia.md` (una por historia), `hu-2-criterios-aceptacion.md`, `hu-3-definition-of-done.md`, `hu-4-product-backlog.md`, `README.md`.

## Qué pregunta la skill
**Acuerdo de historias:** propone la lista de historias por `RF` y espera que el usuario las confirme, quite o agregue; escala de estimación; técnica de priorización; criterio de «hecho». Pregunta antes de generar los criterios de aceptación.

## Salida
`project/user-stories/<corrida>/`: `historias/HU-nn.md`, `backlog.md` (orden, estimación, sprint tentativo vacío), `dod.md`.

## Índice
Alimenta **4.4.1, 4.4.2 y 4.5**. Sin cambios al índice.

## Update
Agregar, quitar o reordenar historias; ajustar criterios o estimaciones; mantiene `backlog.md` y la matriz con los `RF`.

## Validación
Cada `RF` cubierto por al menos una `HU`, cada `HU` con al menos 2 `CA`, orden del backlog sin empates, estimaciones dentro de la escala elegida.

## Fuera de alcance
Asignar historias a sprints (cambio 9).

## Decisiones abiertas para el proposal
- Número de historias por `RF` y límite total razonable para 3 sprints.
- Si la estimación va en puntos o en tallas.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
