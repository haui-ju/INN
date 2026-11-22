# add-sprint-execution-reports: Bitácora de implementación e informes de sprint

**Cambio 12 de 14 de la ruta de skills** (el cambio 1, `add-project-config-init`, ya está archivado). Estado: solo definido; falta el proposal (`/opsx:propose add-sprint-execution-reports`).

## Valor
Registra lo que realmente se hizo en cada sprint y lo convierte en los puntos 6.x del informe, sin repetir contenido entre avances. Es el corazón del «avance real».

## Skills
- `15-make-implementation-log` y su `-update`.
- `16-make-sprint-report` y su `-update` (se ejecuta **una vez por sprint**: 3 veces).

## Prerrequisitos
15: `11-make-sprint-plan`, `14-make-system-design`. 16: `11-make-sprint-plan`, `15-make-implementation-log`.

## Playbook
`common/sprint-reports/guia.md` (lo crea este cambio): qué se registra en la bitácora, reglas del informe (cifras con fecha, pies de foto con código de trazabilidad, no repetir contenido ya presentado, lo extenso a anexos), retrospectiva y Sprint Review.

Códigos propuestos: `BIT-nn` (entrada de bitácora), `RIE-nn` (riesgo o cambio); cita `HU`, `CA`, `TAR`.

## Modelos y formularios (`common/sprint-reports/models/`)
- `log-1-bitacora-sprint.md`, `rep-1-informe-avance.md` (los 9 puntos 6.x.1 a 6.x.9, cada uno con «pegar» y «texto»), `rep-2-acta-review-retro.md`, `README.md`.

## Qué pregunta la skill
Sprint en curso, qué historias avanzaron o se terminaron, evidencias disponibles, cifras del tablero, comentarios del Sprint Review, qué fue bien y qué mejorar, riesgos y cambios del plan, plan del siguiente sprint. Si `modo_datos` es `real`, usa solo lo que el usuario aporta.

## Salida
- `project/implementation-log/<corrida>/`: `bitacora.md` y `evidencias/`.
- `project/sprint-report/<corrida>/` por sprint (el config guarda una entrada por sprint): `informe-avance-N.md`, `acta-review-retro.md`.

## Índice
Alimenta **5.4, 6.1, 6.2, 6.3**, el **Anexo A.3** y el **Anexo E**.

## Update
Corregir cifras, agregar una evidencia, mover una historia entre sprints; recalcula totales y el plan del siguiente avance.

## Validación
Fechas dentro del sprint, cifras iguales a las de `tablero.json`/`gantt.json`, cada `HU` citada existe, ningún punto repite texto del avance anterior.

## Fuera de alcance
Análisis consolidado (cambio 13), armado del documento (cambio 14).

## Decisiones abiertas para el proposal
- Cómo representa el config tres corridas de la misma skill (ya existe `sprints` por paso).
- Si 15 y 16 se ejecutan en secuencia en la misma sesión o por separado.

## Patrón común (ya definido y archivado)

Specs principales: `project-config`, `run-versioning` y `skill-pipeline`. Toda skill de este cambio:
- lee `project/config.yaml` (no repite preguntas de tema, enfoque, equipo ni fechas) y comprueba prerrequisitos con `projectcfg.py check` (aviso, no bloqueo);
- pregunta lo necesario y **pide confirmación de sus propuestas** antes de escribir;
- crea `project/<carpeta>/<DD-MM-AAAA-HH-MM-SS>/` con `runs.py new`, escribe un `README.md` de procedencia (único lugar donde se anota) y registra la corrida con `projectcfg.py register`;
- mantiene el texto limpio (`policy.json`) y pasa `validate_run.py` con las reglas de su paso (`rules/<paso>.py`);
- tiene su homóloga `-update` (copia `-fork`, edita solo lo afectado, valida) con `references/dependencias.md`.

Este cambio **define** las skills (specs, playbook y modelos); no las ejecuta. La ejecución es posterior y a petición del usuario.
