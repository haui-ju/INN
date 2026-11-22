# Dependencias de la problemática y los objetivos

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/05-problem-objectives/<corrida>/`). Las skills de `06` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y de dónde sale

| Archivo | Viene de | Lo leen |
|---|---|---|
| `secciones/1.8.md` (enunciado, afectados, causas principales `CAU`, evidencia) | brief (sección 2), Ishikawa de `04` (1.7) | 06 (propuesta de solución), 11 (conclusiones), 12 |
| `secciones/1.9.md` (`OG-01`) | brief (sección 3.1), copiado | 07 (KPI), 11, 12 |
| `secciones/1.10.md` (`OE-nn` y matriz de articulación) | brief (sección 3.2), corridas de `03` (Canvas) y `04` (PESTEL, FODA, estrategias, Ishikawa) | 06, 07 (cada KPI responde a un `OE`), 11, 12 |

## Qué cambio aguas arriba obliga a este update

| Cambio en | Qué se edita aquí |
|---|---|
| Brief: problema principal, afectados o evidencia (`01-make-project-brief-update`) | **Enunciado**, **Afectados** y **Evidencia** de 1.8 |
| Brief: un objetivo, su meta o su indicador | la fila en 1.9 o 1.10 (copiada de nuevo) y el indicador de su fila en la matriz |
| Brief: un `OE` nuevo o eliminado | su fila en la tabla de 1.10 y su fila en la matriz; revisar la cobertura de las causas principales |
| Ishikawa: causa corregida o eliminada (`04-make-strategic-analysis-update`) | la fila de causas principales de 1.8 y las celdas de la matriz que la citan |
| FODA, estrategia o PESTEL: código corregido o eliminado | las celdas de la matriz que lo citan |
| Canvas: bloque renombrado o con otro contenido (`03-make-business-diagnosis-update`) | la columna Canvas de la matriz si cambió la articulación |

## Qué afecta cada cambio de esta skill

| Cambio | Edición | Skills `-update` a ejecutar después |
|---|---|---|
| Causas principales | tabla de 1.8 y cobertura en la matriz | `06-make-bi-solution-update` si la propuesta de solución las cita |
| Una fila de la matriz | 1.10 | `07-make-data-model-kpi-update` si cambia el indicador o la causa que un KPI mide |
| Enunciado o evidencia | 1.8 | `11-make-conclusions-update` si las conclusiones lo citan |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Redactar o cambiar un objetivo, su meta o su indicador | `01-make-project-brief-update` |
| Agregar o cambiar una causa del Ishikawa, un ítem FODA o un hallazgo PESTEL | `04-make-strategic-analysis-update` |
| Cambiar un bloque del Canvas | `03-make-business-diagnosis-update` |
