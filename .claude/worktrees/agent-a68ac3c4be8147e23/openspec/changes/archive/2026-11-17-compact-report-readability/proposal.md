# Proposal

## Why

El informe del avance 3 tiene unas 2100 líneas y alrededor de 1300 códigos de trazabilidad (RF-01, CA-14, TAR-23…). Los códigos son útiles como llaves de tablas, pero en la prosa se acumulan ("REQ-01, REQ-02, REQ-03, REQ-04, REQ-05 y 1 más") y hacen pesada la lectura. Además, bloques muy extensos (16 historias con sus criterios, 44 casos de prueba, el Gantt de 38 filas, el glosario) y varias repeticiones (backlog en 4.4.2 y en 4.6.1, resumen de criterios en 4.5, participantes en las cuatro ceremonias) alargan el cuerpo sin aportar. El equipo quiere un informe más claro y rápido de entender sin perder secciones, y decidir qué va en el cuerpo y qué en anexos.

## What Changes

- **Política de densidad de códigos:** en la prosa va primero el nombre y el código una sola vez entre paréntesis, con un máximo de dos códigos por frase; las series consecutivas se colapsan en rangos («TST-01 a TST-08»). Los códigos siguen completos como llaves dentro de las tablas.
- **Colocación por bloque:** los bloques pesados (historias con criterios de aceptación, casos de prueba 5.5.1, Gantt completo 4.6.2, glosario 2.4 y el resumen de criterios 4.5) pueden ir en el cuerpo o en un anexo. `19-make-report` pregunta por cada bloque (por omisión, la colocación vigente del índice) y, si va a anexo, deja en el cuerpo un resumen corto con su enlace.
- **Anexo G, «Detalle de tablas del informe»:** nuevo anexo para recibir esos bloques (G.1 historias y criterios, G.2 casos de prueba, G.3 Gantt completo, G.4 glosario). No se renumeran 3.1.1 a 3.1.8 ni los anexos B, D, E y F; A y C no cambian.
- **Menos repetición:** el backlog por sprint se muestra una vez (4.6.1 cita 4.4.2 en lugar de repetirlo), 4.5 deja de duplicar las historias y 4.7 lista los participantes una sola vez en lugar de cuatro.
- **Validación:** un chequeo de densidad (máximo de códigos por párrafo y por frase, fuera de tablas) y otro de coherencia de la colocación (bloque en anexo sin duplicado en el cuerpo, enlace que resuelve, resumen presente).
- No se eliminan secciones ni se cambian los datos de las corridas fuente. No toca las explicaciones de figuras ni los propósitos de tabla (change `improve-report-figure-explanations`). Código en inglés; textos al usuario y README en español.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `report-assembly`: se añaden la política de densidad de códigos, la colocación por bloque con su pregunta y su resumen en el cuerpo, la eliminación de duplicados entre secciones y las dos validaciones nuevas.
- `report-index-structure`: se añade el anexo G (G.1 a G.4) como destino de los bloques trasladados y se declara qué bloques admiten colocación en anexo, conservando los puntos estables.

## Impact

- Código: `.claude/skills/_shared/report.py` y `report_prosa.py` (colapso de rangos, resumen en el cuerpo, anexo G, deduplicación), `report_map.json` (qué bloques son trasladables y su colocación por omisión), `rules/report.py` (chequeos de densidad y de colocación) y sus pruebas en `_shared/tests/`.
- Documentación: `common/structure/model1.md` (anexo G), `common/report/guia.md`, `common/report/models/` y `.claude/skills/19-make-report/SKILL.md` (nueva pregunta por bloque).
- Corridas existentes de `19-make-report` no cambian; el efecto se ve al armar una corrida nueva.
- Sin dependencias nuevas. Se aplica después de `improve-report-figure-explanations`, con el que comparte `report.py` y `rules/report.py`.
