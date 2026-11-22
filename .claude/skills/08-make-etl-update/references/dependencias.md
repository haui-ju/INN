# Dependencias del ETL

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/08-etl/<corrida>/`). Las skills de `10` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y a quién llega

| Archivo | Viene de | Lo leen |
|---|---|---|
| `evidencia.json` | el equipo (filas por regla, fuente y tabla, y totales) y `etl_verificacion.py` | 3.1, anexo A, validador, 09 (volumen de datos), 12 |
| `secciones/3.1.md` (reglas `REG`, pasos `PAS`) | evidencia, fuentes del brief, `modelo.json` y `data/respuestas/` | anexos A y B, 09, 11, 12 |
| `anexos/A.md` | 3.1, evidencia y `modelo.json` | 12 |
| `anexos/B.md` | el código que el equipo ejecutó y los `PAS` de 3.1 | 12 |
| `materiales/guia-power-query.md` | `data/respuestas/defectos.csv` y `modelo.json` | el equipo |
| `data/` (fuera de la corrida) | `datagen.py` y `data/parametros.json` | el equipo, el comparador |

## Qué afecta cada cambio

| Cambio | Edición en la corrida | Skills `-update` a ejecutar después |
|---|---|---|
| Corregir las filas antes o después de una regla | `evidencia.json`, fila de la regla en 3.1 y fila del resultado en el anexo A; volver a comparar | — |
| Corregir las filas leídas de una fuente o cargadas de una tabla | `evidencia.json` y la tabla de extracción o de carga de 3.1 | — |
| Agregar una regla de calidad | fila en 3.1 y en el anexo A, `evidencia.json`, el paso que la aplica y su bloque del anexo B | — |
| Eliminar una regla | su fila en 3.1 y en el anexo A y la evidencia; revisar que su defecto siga tratado | — |
| Cambiar el código de un paso | su bloque del anexo B (y su fila de 3.1 si cambia el resultado) | — |
| Agregar o quitar un paso | fila en 3.1 y bloque del anexo B | — |
| Cambiar los totales o la verificación | `evidencia.json` (`totales`), volver a comparar y ajustar la «Verificación» de 3.1 | — |
| Regenerar los datos (otra semilla u otro volumen) | `data/` y `evidencia-desactualizada.json`; el equipo repite el ETL y trae la evidencia nueva | `09-make-dashboard-update` (los valores de los KPI cambian) |
| Cambió una tabla o un campo del modelo (después de `07-make-data-model-kpi-update`) | anexo A (origen de los campos), tabla de carga y evidencia; pasos que lo calculan | — |
| Cambió una fuente o el ETL en la arquitectura (después de `06-make-bi-solution-update` o `01-make-project-brief-update`) | tabla de extracción, diccionario del anexo A y pasos | — |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Fuentes de datos, objetivos o periodo del brief | `01-make-project-brief-update` |
| Componentes de la arquitectura o herramientas | `06-make-bi-solution-update` |
| Tablas, medidas o KPI del modelo | `07-make-data-model-kpi-update` |
| Páginas, medidas DAX o capturas del dashboard | `09-make-dashboard-update` |
