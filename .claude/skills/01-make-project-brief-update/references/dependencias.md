# Dependencias del brief

Úsala para armar el plan de un `update`. El brief es la fuente del núcleo: **todas las demás skills lo leen**. Rutas relativas a la corrida (`project/01-project-brief/<corrida>/`). Las skills de `10` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

Si cambian las fuentes o el periodo del brief y ya hay una corrida de `08-make-etl`, ejecuta `08-make-etl-update` (los datos se regeneran con el periodo nuevo y la evidencia del equipo queda desactualizada).

## Qué contiene `brief.md` y a quién llega

| Sección | Se copia al config | La leen |
|---|---|---|
| 1. Tema y empresa | `proyecto.tema` | 03, 05, 06, 12 |
| 2. Problemática | — | 03, 04, 05 |
| 3. Objetivos (`OG-01`, `OE-nn`) | — | 05 (copia), 07, 10, 11, 12 |
| 4. Justificación y alcance | — | 05, 06 |
| 5. Usuarios y decisiones | — | 06, 07, 09, 10 |
| 6. Fuentes de datos previstas | — | 06, 07, 08 |
| 7. Calendario | `calendario.inicio` y `calendario.entrega` | 12 |
| 8. Supuestos y riesgos iniciales | — | 06, 11 |

## Qué afecta cada cambio

| Cambio | Edición en el brief | Copia al config | Skills `-update` a ejecutar después |
|---|---|---|---|
| Tema, empresa o problemática | Secciones 1 y 2 | `tema` | `03-make-business-diagnosis-update`, `04-make-strategic-analysis-update` y `05-make-problem-objectives-update`; `01` rehace `domain.md` si cambió el tema |
| Un objetivo (`OG` u `OE`) o su indicador | Sección 3 | — | `05-make-problem-objectives-update` y `07-make-data-model-kpi-update` |
| Justificación o alcance | Sección 4 | — | `05-make-problem-objectives-update` y `06-make-bi-solution-update` |
| Usuarios o decisiones | Sección 5 | — | `06-make-bi-solution-update` y `07-make-data-model-kpi-update` |
| Una fuente de datos | Sección 6 | — | `06-make-bi-solution-update` y `07-make-data-model-kpi-update` |
| La fecha de inicio o de entrega | Sección 7 y los plazos de los objetivos que la citan | `calendario.inicio` o `entrega` | `05-make-problem-objectives-update` (plazos de los objetivos) |
| Supuestos o riesgos | Sección 8 | — | `06-make-bi-solution-update` |
| Completar algo «Pendiente» | La celda o sección pendiente | según la sección | las de la fila que corresponda |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Nombre del proyecto, rubro, equipo, roles, modo de datos | `00-init-update` |
| Tipo de proyecto o RUC | `00-init-update` y luego rehacer `domain.md` aquí |
| Colores o tipografía de los visuales | `02-design-system-update` |
