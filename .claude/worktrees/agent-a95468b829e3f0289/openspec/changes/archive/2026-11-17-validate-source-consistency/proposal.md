# Proposal

## Why

La revisión del informe del avance 3 encontró inconsistencias que nacen en las skills fuente y que sus validaciones no detectan: cadenas de «5 porqués» con 3 niveles, supuestos del canvas v1 que siguen «pendientes» pese a haber decisiones, 7 ideas incluidas frente a 6 requerimientos, ceremonias que se solapan, una tarea terminada con su predecesora sin terminar, criterios de decisión con un hueco («iterar»), un objetivo medido con una métrica distinta a su indicador, casos de prueba declarados que nunca se ejecutan y códigos con huecos de numeración. Corregir cada dato con su `-update` arregla el informe de hoy, pero sin validaciones el problema reaparece en el siguiente proyecto.

## What Changes

- Se agregan comprobaciones a los validadores de las skills fuente para que estas incoherencias fallen con archivo y causa:
  - `02`: la cadena de porqués anuncia cinco niveles o registra un cierre anticipado con motivo.
  - `05`: toda idea incluida en el MVP corresponde a un `REQ`, el conteo ideas → requerimientos se explica, y los códigos `HAL-T` no tienen huecos.
  - `07`: cada hipótesis define sus tres zonas (perseverar, iterar, pivotar) sin huecos ni solapes.
  - `17`: «Iterar» cita la zona definida en el plan, y el estado de los supuestos del canvas v1 coincide con las decisiones.
  - `12`: ninguna ceremonia se solapa con otra en el mismo día y las fechas caen en día hábil.
  - `13`: una tarea no puede estar terminada si alguna predecesora no lo está.
  - `14`: los códigos `CP` son consecutivos y no hay dos casos con el mismo tipo y la misma verificación.
  - `15`: todo `CP` del plan tiene resultado o figura «No ejecutado» con motivo.
  - `00b`: cada objetivo declara qué se mide y con qué fuente, y su plazo coincide con el avance en que se mide.
  - `18`: la métrica medida de cada objetivo coincide con su indicador (o la valoración es Parcial con la diferencia explicada), y todo componente sin avance aparece en las conclusiones y en los trabajos futuros.
- Cada comprobación se acompaña de pruebas con el caso real encontrado en el informe.
- **No** se corrigen los datos de las corridas actuales: eso se hace ejecutando los `-update` existentes (02, 05, 07, 12, 13, 14, 15, 17, 18) una vez implementadas las reglas.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `lean-canvas-initial`: los porqués deben tener cinco niveles o un cierre anticipado justificado.
- `design-thinking-package-generation`: coherencia entre ideas incluidas y requerimientos, y numeración continua de los hallazgos de prueba.
- `lean-plan`: los criterios de decisión cubren perseverar, iterar y pivotar sin huecos.
- `lean-results`: «Iterar» cita su zona, y el canvas v1 debe reflejar las decisiones.
- `ceremonies-kanban`: sin solapes entre ceremonias ni fechas en fin de semana.
- `html-boards`: una tarea terminada exige predecesoras terminadas.
- `system-design`: numeración continua de casos de prueba y sin casos duplicados.
- `implementation-log`: todo caso de prueba tiene resultado o un «No ejecutado» con motivo.
- `project-brief`: cada objetivo declara su métrica de medición y su plazo coincide con ella.
- `final-analysis`: la métrica medida coincide con el indicador y todo componente sin avance se refleja en conclusiones y trabajos futuros.

## Impact

- Código: módulos de `.claude/skills/_shared/rules/` (`lean_canvas.py`, `design_thinking.py`, `lean_plan.py`, `lean_results.py`, `ceremonies_kanban.py`, `html_boards.py`, `system_design.py`, `implementation_log.py`, `project_brief.py`, `final_analysis.py`) y sus pruebas en `_shared/tests/`.
- Documentación: los playbooks de `common/` de cada paso y los `SKILL.md` afectados mencionan la nueva regla.
- Las corridas existentes pueden empezar a fallar la validación hasta ejecutar su `-update`; ninguna se modifica en este change.
- Sin dependencias nuevas.
