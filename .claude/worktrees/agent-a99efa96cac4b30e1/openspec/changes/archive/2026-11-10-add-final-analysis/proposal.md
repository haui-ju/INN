# Proposal

## Why

El plan Lean fijó hipótesis, experimentos y criterios de decisión **antes** de ejecutar; los informes de sprint registraron lo real. Falta cerrar el ciclo: poner los resultados de cada experimento frente a lo que se había definido, decidir si se persevera o se pivota con esos criterios, y comparar lo planificado con lo real (objetivos, Gantt, métricas Kanban) para llegar a conclusiones, recomendaciones y trabajos futuros con evidencia. Hoy ninguna skill produce los puntos 3.2.3 y 3.2.4 (resultados), 6.4.1 a 6.4.5 ni el capítulo 7, y sin ellas las conclusiones se redactan de memoria y sin trazabilidad.

## What Changes

- **Nueva skill `17-make-lean-results`**: pide el resultado de cada experimento del plan, lo compara con su criterio de éxito (copiado tal como se fijó), propone la decisión por hipótesis aplicando los criterios de pivotar o perseverar y espera la confirmación; escribe `project/lean-results/<corrida>/` con `resultados.md`, `decision.md`, `evidencias/` y `README.md`.
- **Nueva skill `17-make-lean-results-update`**: corrige un resultado, una evidencia o una decisión y propaga a lo que depende.
- **Nueva skill `18-make-final-analysis`**: arma el análisis consolidado (6.4.1 a 6.4.5) y las conclusiones (capítulo 7). Las cifras salen de los `data.json` de los informes de sprint y de los resultados Lean, no de la memoria; el usuario confirma cada valoración de objetivo, la validación con usuarios disponible y las limitaciones. Escribe `project/final-analysis/<corrida>/` con `analisis-consolidado.md`, `conclusiones.md` y `README.md`.
- **Nueva skill `18-make-final-analysis-update`**: corrige una valoración, una cifra o una conclusión y recalcula lo que la cita.
- **Nuevo playbook `common/final-analysis/`**: `guia.md` (comparar contra la línea base, métricas acumuladas, valoración de objetivos, base de la evidencia, validación con usuarios, discusión de limitaciones, conclusiones con evidencia, errores, referencias) y `models/` con `fin-1-resultados-decision`, `fin-2-cumplimiento-objetivos`, `fin-3-gantt-metricas`, `fin-4-validacion-discusion`, `fin-5-conclusiones` y `README.md`.
- **Códigos de trazabilidad propios:** `RES-nn` (resultado de experimento), `CNC-nn` (conclusión; no se usa `CON`, que es del Design Thinking), `REC-nn` (recomendación) y `TRF-nn` (trabajo futuro).
- **Objetivos con base de evidencia:** cada objetivo se valora como Cumplido, Parcial, No cumplido o No evaluable, indicando si la medición fue en el sistema, en un piloto, en un prototipo o no existe; lo que no es del sistema completo debe figurar como limitación.
- **Análisis parcial explícito:** si falta el informe de algún sprint, el análisis declara los avances incluidos y se valida solo contra ellos.
- **Prerrequisitos:** `18-make-final-analysis` pasa a requerir también `03-make-company-chapter` en `pipeline.json` (los objetivos); solo aviso.
- **Validación propia de los dos pasos** (`rules/lean_results.py` y `rules/final_analysis.py`).

## Capabilities

### New Capabilities
- `lean-results`: skills `17-make-lean-results` y su `-update`, resultados de experimentos, decisión de pivotar o perseverar con los criterios fijados, evidencias y su validación.
- `final-analysis`: playbook y modelos del análisis final, skills `18-make-final-analysis` y su `-update`, cumplimiento de objetivos, Gantt y métricas acumuladas, validación con usuarios, discusión, conclusiones, recomendaciones, trabajos futuros y su validación.

### Modified Capabilities
- Ninguna.

## Impact

- **Archivos nuevos:** `common/final-analysis/`, `.claude/skills/17-make-lean-results{,-update}/`, `.claude/skills/18-make-final-analysis{,-update}/`, `.claude/skills/_shared/rules/lean_results.py` y `final_analysis.py`, y sus pruebas.
- **Archivos modificados:** `.claude/skills/_shared/pipeline.json` (prerrequisito de la skill 18) y `.claude/skills/_shared/validate_run.py` (registra las carpetas `lean-results` y `final-analysis`).
- **Consumidores:** `19-make-report` (3.2.3, 3.2.4, 6.4 y capítulo 7).
- **Índice:** alimenta 3.2.3 y 3.2.4 (resultados y decisión), 6.4.1 a 6.4.5 y 7.1 a 7.3.
- **Fuera de alcance:** actualizar el Lean Canvas validado (3.4) con los resultados, armar el documento, generar imágenes y ejecutar las skills.
- **Supuestos registrados:** el usuario aporta los resultados y las evidencias de cada experimento; la decisión de pivotar o perseverar la propone la skill con los criterios fijados en el plan y la confirma el usuario; las fuentes se limitan a las ya verificadas (Ries 2011, Little 2014 y Doran 1981).
