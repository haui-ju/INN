# Proposal

## Why

El índice del informe (`common/structure/model1.md`) tiene capítulos saltados (1, 3, 4, 6, 7), numeración repetida (`4.1.2` y `4.1.3` aparecen dos veces), títulos con erratas y notas de trabajo dentro de los títulos, y el capítulo de resultados está vacío. Además, el equipo desarrolla el sistema y entrega el documento en **tres avances** (avance 1, avance 2 y final); hace falta un esqueleto estable que se vaya llenando en cada avance y que diga qué pegar (capturas, Gantt, tablero Kanban) y qué texto escribir.

## What Changes

- **Nuevo orden de capítulos** (formato libre, sin plantilla del profesor):
  1. La empresa y el problema (con el Lean Canvas inicial y los 5 porqués).
  2. Marco metodológico (innovación, gestión ágil, cómo se integran, glosario).
  3. Innovación: Design Thinking (se mantiene en `3.1`, con su numeración `3.1.1` a `3.1.8`), Lean Startup, Lean Change y Lean Canvas validado.
  4. Gestión ágil: lo planificado (Scrum, requerimientos funcionales y no funcionales, historias y backlog, criterios de aceptación y DoD, planificación de sprints con Gantt como línea base, ceremonias, diseño del Kanban).
  5. Desarrollo del sistema (arquitectura, modelo de datos, diseño de interfaz, implementación por módulos, pruebas).
  6. Resultados y avance: lo real (6.1 avance 1, 6.2 avance 2, 6.3 avance final, 6.4 análisis consolidado).
  7. Conclusiones, recomendaciones y trabajos futuros.
- **Marcas de avance** `[A1]`, `[A2]`, `[A3]` en cada punto (y `+` cuando el punto se actualiza en avances posteriores) y un **historial de versiones** del documento.
- **Plantilla de 9 bloques** para 6.1, 6.2 y 6.3 (resumen, Gantt actualizado, incremento del sistema, tablero Kanban, Sprint Review, retrospectiva, pruebas, riesgos y cambios, plan del siguiente avance), cada uno con una nota breve de qué pegar.
- **Reglas de contenido** del informe: no repetir contenido entre avances, lo grande va a anexos, toda captura con pie de foto y código de trazabilidad, toda cifra con su fecha.
- **Se quitan** «Tipo y diseño de la investigación», «Población y muestra» y la «Matriz de consistencia»; **el Anexo A pasa a ser** «Evidencias de gestión ágil» para conservar las letras B a F de los anexos que usan las skills.
- Se corrigen erratas y numeración, y las **notas de trabajo** de los títulos (herramienta para el Gantt, MCP de Trello, Miro) pasan a `apuntes.md` como decisiones pendientes.
- Se actualizan las **referencias cruzadas viejas** (`5.1`, `5.2.3`, `5.4.2`) en el índice, en el generador de `make-design-thinking` y en el paquete ya generado.

## Capabilities

### New Capabilities
- `report-index-structure`: contrato del índice maestro del informe: orden y numeración de capítulos, estabilidad de las secciones que usan las skills, marcas de avance, historial de versiones, plantilla de avance y reglas de contenido.

### Modified Capabilities
<!-- Ninguna: design-thinking-package-generation sigue exigiendo los puntos 3.1.x y los anexos B, D, E y F, que se conservan. -->

## Impact

- **Archivos modificados:** `common/structure/model1.md` (reescritura), `apuntes.md` (decisiones pendientes y correspondencia de temas), `.claude/skills/make-design-thinking/scripts/reference/build.py` (3 referencias cruzadas) y el paquete `project/design-thinking/10-11-2026-00-00-46/` (las mismas referencias, para mantener la regresión idéntica).
- **No cambian:** la numeración `3.1.x` del Design Thinking, las letras de anexos B a F, `patch_run.py`, `read_run.py` ni las specs existentes.
- **Riesgo:** quien edite el índice podría renumerar el Design Thinking o los anexos y romper las skills; la spec nueva lo declara como restricción.
- **Fuera de alcance:** redactar el contenido de los capítulos, generar datos o modificar el playbook de Design Thinking.
