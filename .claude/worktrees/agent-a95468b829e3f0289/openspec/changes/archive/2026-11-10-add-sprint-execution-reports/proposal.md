# Proposal

## Why

El plan, el diseño y los tableros dicen qué se **va** a hacer; falta registrar lo que **realmente** se hizo en cada sprint y convertirlo en el capítulo 6 del informe. Hoy ninguna skill produce la bitácora de implementación (5.4), los resultados de las pruebas por sprint, los riesgos y cambios del plan, ni los informes de avance (6.1, 6.2 y 6.3) con su Sprint Review y retrospectiva (anexo A.3). Sin ellos el «avance real» sale improvisado, con cifras que no coinciden con los tableros y con el mismo texto repetido en los tres avances.

## What Changes

- **Nueva skill `15-make-implementation-log`**: pregunta qué se avanzó en cada sprint y registra los módulos (5.4), las entradas de bitácora `BIT-nn` (fecha, historia, tarea, estado y evidencia), los resultados de los casos de prueba `CP-nn` y los riesgos y cambios `RIE-nn`; escribe `project/implementation-log/<corrida>/` con `bitacora.md`, `evidencias/` y `README.md`. Con `modo_datos` en `real` usa solo lo que el usuario aporta.
- **Nueva skill `15-make-implementation-log-update`**: agrega un sprint, corrige una entrada, suma una evidencia, mueve una historia entre sprints o actualiza resultados de pruebas.
- **Nueva skill `16-make-sprint-report`**: se ejecuta **una vez por sprint** (tres veces); genera `informe-avance-N.md` con los puntos 6.N.1 a 6.N.9 (cada uno con su parte «pegar» y su parte «texto») y `acta-review-retro.md` (anexo A.3), en `project/sprint-report/<corrida>/`, y registra la corrida con `--sprint N`. Las cifras salen de la bitácora, del plan y de los tableros HTML vigentes, no de la memoria del usuario.
- **Nueva skill `16-make-sprint-report-update`**: corrige cifras, evidencias, comentarios de la Review, retrospectiva o el plan del siguiente avance de un sprint.
- **Nuevo playbook `common/sprint-reports/`**: `guia.md` (qué se registra, reglas del informe, retrospectiva y Sprint Review, errores frecuentes, referencias) y `models/` con `log-1-bitacora-sprint`, `rep-1-informe-avance`, `rep-2-acta-review-retro` y `README.md`.
- **Códigos de trazabilidad propios:** `BIT-nn` (entrada de bitácora) y `RIE-nn` (riesgo o cambio); se citan `HU`, `CA`, `TAR`, `CP`, `TBL` y `UI`.
- **Reglas del informe verificables:** las cifras del Gantt y del Kanban son las de `data.json` del tablero vigente; cada captura lleva el pie «Figura X: HU-XX nombre (REQ-XX)»; el avance no repite texto del anterior (se remite por número de punto); lo extenso va a los anexos.
- **Prerrequisitos:** `16-make-sprint-report` pasa a requerir también `12-make-ceremonies-kanban` y `13-design-html-boards` en `pipeline.json` (aviso, no bloqueo).
- **Validación propia de los dos pasos** (`rules/implementation_log.py` y `rules/sprint_report.py`).

## Capabilities

### New Capabilities
- `implementation-log`: playbook y modelos de la bitácora, skills `15-make-implementation-log` y su `-update`, módulos, entradas, resultados de pruebas, riesgos y cambios, evidencias y su validación.
- `sprint-report`: skills `16-make-sprint-report` y su `-update`, informe de avance por sprint, acta de Sprint Review y retrospectiva, cifras trazables y su validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/sprint-reports/`, `.claude/skills/15-make-implementation-log{,-update}/`, `.claude/skills/16-make-sprint-report{,-update}/`, `.claude/skills/_shared/rules/implementation_log.py` y `sprint_report.py`, y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/pipeline.json` (prerrequisitos de la skill 16) y `.claude/skills/_shared/validate_run.py` (registra las carpetas `implementation-log` y `sprint-report`).
- **Consumidores:** `17-make-lean-results` (bitácora), `18-make-final-analysis` (informes y resultados de pruebas), `19-make-report` (5.4, 6.1 a 6.3 y anexos A.3 y E).
- **Índice:** alimenta 5.4, 5.5.2 (insumo), 6.1 a 6.3 y el anexo A.3.
- **Fuera de alcance:** el análisis consolidado (6.4), los resultados Lean, las conclusiones, el armado del documento, generar capturas o imágenes y ejecutar las skills.
- **Supuestos registrados:** el usuario aporta las evidencias (archivos que coloca en `evidencias/`; el kit no las genera); la bitácora es acumulada y cada sprint nuevo se agrega con el `-update`; las fuentes se limitan a las ya verificadas (Schwaber y Sutherland 2020; Anderson 2010).
