# Dependencias de la solución de BI

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/06-bi-solution/<corrida>/`). Las skills de `08` en adelante se crean más adelante: menciona su `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y a quién llega

| Archivo | Viene de | Lo leen |
|---|---|---|
| `secciones/2.1.md` (decisiones, usuarios, respuesta y tabla `OE` → `CAP`) | brief (usuarios, decisiones, objetivos), 1.8 y 1.10 de `05` | 07 (objetivos y decisiones de los KPI), 12 |
| `secciones/2.2.md` (componentes `CAP-nn` por capa) | fuentes `FUE-nn` del brief, objetivos, decisiones del usuario | 2.1 (columna Componentes), 07 (fuentes y almacenamiento del modelo), visual `arquitectura-bi`, 12 |
| `secciones/2.3.md` (herramientas `HER-nn`) | decisiones del usuario, alcance del brief | visual `arquitectura-bi` (herramientas por capa), capítulo 3 (ETL y dashboard), 12 |
| `visuales/arquitectura-bi.html`, `.json` y `leer-imagen/arquitectura-bi.md` | 2.2 y 2.3 (`visuales.py construir`) | 12 |
| `referencias.md` | marcos y herramientas citados | 12 |

## Qué afecta cada cambio

| Cambio | Edición en la corrida | Figura | Skills `-update` a ejecutar después |
|---|---|---|---|
| Decidir una herramienta «Pendiente» (por ejemplo, ETL) | fila de `secciones/2.3.md` y, si el nombre del componente la menciona, la fila de 2.2 | `arquitectura-bi` | `07-make-data-model-kpi-update` si el almacenamiento cambia el modelo |
| Cambiar una herramienta decidida | fila de 2.3 (función, justificación y alternativa) y el componente de 2.2 que la nombre | `arquitectura-bi` | `07-make-data-model-kpi-update` si cambia el almacenamiento |
| Agregar, corregir o eliminar un componente | fila de `secciones/2.2.md` y las filas de 2.1 que lo citan | `arquitectura-bi` | `07-make-data-model-kpi-update` si es una fuente o el almacenamiento |
| Agregar una fuente (después de `01-make-project-brief-update`) | componente de la capa de fuentes en 2.2 (cita su `FUE`) | `arquitectura-bi` | `07-make-data-model-kpi-update` (hechos o dimensiones nuevos) |
| Un `OE` nuevo o cambiado en el brief | fila de la tabla de 2.1 | ninguna | `07-make-data-model-kpi-update` (su KPI) |
| Decisiones o usuarios nuevos en el brief | `**Decisiones que apoya.**` o `**Usuarios.**` de 2.1 | ninguna | `07-make-data-model-kpi-update` si un KPI citaba la decisión |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Fuentes de datos, objetivos, usuarios o decisiones | `01-make-project-brief-update` |
| Problemática o causas principales | `05-make-problem-objectives-update` |
| Hechos, dimensiones, relaciones o KPI | `07-make-data-model-kpi-update` |
| Colores o tipografía de la figura | `02-design-system-update` y volver a construir la figura |
