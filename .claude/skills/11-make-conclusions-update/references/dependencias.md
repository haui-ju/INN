# Dependencias de las conclusiones

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/11-conclusions/<corrida>/`). Las conclusiones son el cierre del informe: **nada depende de ellas** salvo `12-make-report`.

## Qué contiene `secciones/5.md` y de dónde sale

| Parte | Sale de | Se recalcula cuando cambia |
|---|---|---|
| Estado y conclusión de cada `OE-nn` (`CNC-nn`) | el valor real de `valores.json` (09) frente a la meta de 2.5 (07), de los KPI con ese `OE-nn` | un valor del dashboard, una meta, el objetivo que mide un KPI |
| Respaldo (valor, meta y estado de cada KPI) | `valores.json` y `modelo.json` | un valor, una meta, un KPI agregado o eliminado |
| Conclusión del objetivo general (`OG-nn`) | los estados de las conclusiones de los `OE-nn` | el estado de cualquiera de ellas |
| Recomendaciones `REC-nn` | la conclusión a la que se ligan, los usuarios y los KPI | el estado de su conclusión, los usuarios del brief |
| Lecciones `LEC-nn` y limitaciones | el proceso y `modo_datos` | un cambio del proceso (3.1, 3.2) o del modo de datos |

## Qué afecta cada cambio

| Cambio | Edición en `5.md` | Skills `-update` a ejecutar antes o después |
|---|---|---|
| Cambió un valor real (`09-make-dashboard-update`) | La conclusión y el respaldo del objetivo que mide ese KPI; su recomendación; el objetivo general si cambia su estado | — (esta skill es la última) |
| Se cerró una meta pendiente (`07-make-data-model-kpi-update`, luego `09-make-dashboard-update`) | La conclusión deja de ser «Sin meta» o «Parcial por meta»: ahora se concluye con el valor frente a la meta; su respaldo y su recomendación | — |
| Cambió el objetivo de un KPI en 2.5 (`07-make-data-model-kpi-update`) | El respaldo de las dos conclusiones involucradas y su estado | — |
| Cambió un objetivo del brief (`01-make-project-brief-update`, `05-make-problem-objectives-update`) | La fila del objetivo, su conclusión y las recomendaciones ligadas | `10-make-storytelling-update` si el relato cita ese objetivo |
| Cambió un hallazgo de 4 (`10-make-storytelling-update`) | Las citas `HLZ-nn` de la conclusión que lo cita | — |
| Cambió una recomendación o una lección | La fila correspondiente | — |
| Cambió el modo de datos (`00-init-update`) | La limitación | — |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Cambiar el valor de un KPI o su captura | `09-make-dashboard-update` (lo entrega el equipo) |
| Cerrar o cambiar una meta | `07-make-data-model-kpi-update` (la propone `09-make-dashboard`) |
| Cambiar el relato de los hallazgos | `10-make-storytelling-update` |
