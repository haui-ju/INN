# Dependencias del modelo de datos y los KPI

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/07-data-model-kpi/<corrida>/`). Las skills de `10` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

Si cambian el modelo o los KPI y ya hay corridas de `08-make-etl` o `09-make-dashboard`, ejecuta `08-make-etl-update` y `09-make-dashboard-update` (la evidencia del ETL, las medidas y los valores del equipo dependen del modelo). Las metas «Pendiente» de 2.5 se cierran aquí con los valores reales que propone `09-make-dashboard`.

## Qué contiene la corrida y a quién llega

| Archivo | Viene de | Lo leen |
|---|---|---|
| `secciones/2.4.md` (hechos `FCT`, dimensiones `DIM`, relaciones `REL`) | fuentes y objetivos del brief, arquitectura de `06` | 2.5 (campos de origen de los KPI), `modelo.json`, visual `modelo-datos`, capítulo 3 (ETL y dashboard), 12 |
| `secciones/2.5.md` (KPI `KPI`) | indicadores, metas y decisiones del brief, modelo de 2.4 | `modelo.json`, capítulo 3 (páginas del dashboard y medidas DAX), 12 |
| `modelo.json` | 2.4 y 2.5 (copia exacta) | visual `modelo-datos`, capítulo 3 |
| `visuales/modelo-datos.html`, `.json` y `leer-imagen/modelo-datos.md` | `modelo.json` (`visuales.py construir`) | 12 |
| `referencias.md` | marcos citados | 12 |

## Qué afecta cada cambio

| Cambio | Edición en la corrida | Figura | Skills `-update` a ejecutar después |
|---|---|---|---|
| Agregar una medida a un hecho | fila del hecho en 2.4 y `modelo.json` | `modelo-datos` | — (el capítulo 3 la calcula) |
| Cambiar la granularidad de un hecho | fila del hecho en 2.4 y `modelo.json`; revisar sus medidas y los KPI que las usan | `modelo-datos` | `06-make-bi-solution-update` si cambia lo que cargará el ETL |
| Agregar una dimensión | fila de la dimensión, su(s) relación(es) en 2.4 y la clave en los hechos; `modelo.json` | `modelo-datos` | — |
| Agregar o corregir un atributo | fila de la dimensión en 2.4 y `modelo.json`; revisar los KPI que lo usan | `modelo-datos` | — |
| Eliminar una tabla o un campo | su fila, las relaciones y los KPI que lo citan; `modelo.json` | `modelo-datos` | — |
| Agregar un KPI | filas en las dos tablas de 2.5 y en `modelo.json`; si usa campos nuevos, antes el modelo | ninguna (si el modelo no cambia) | — |
| Cambiar una meta o la frecuencia de un KPI | fila de la tabla de gestión en 2.5 y `modelo.json`; si la frecuencia pasa a periódica, comprobar la dimensión de tiempo | ninguna | — |
| Un `OE` nuevo o cambiado en el brief (después de `01-make-project-brief-update`) | un KPI con el nombre de su indicador en las dos tablas y en `modelo.json` | ninguna | — |
| Cambió una fuente o el almacenamiento en la arquitectura (después de `06-make-bi-solution-update`) | hechos o dimensiones que dependían de ella | `modelo-datos` | — |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Objetivos, indicadores del brief, fuentes o decisiones | `01-make-project-brief-update` |
| Componentes de la arquitectura o herramientas | `06-make-bi-solution-update` |
| Problemática o matriz de articulación | `05-make-problem-objectives-update` |
| Colores o tipografía de la figura | `02-design-system-update` y volver a construir la figura |
