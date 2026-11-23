# Dependencias del storytelling

Úsala para armar el plan de un `update`. Rutas relativas a la corrida (`project/10-storytelling/<corrida>/`). Menciona un `-update` solo si ya existe en `.claude/skills/`.

## Qué contiene la corrida y quién lo lee

| Archivo | Se origina en | Lo leen |
|---|---|---|
| `secciones/4.md` (hallazgos `HLZ`, tabla y narrativa) | `valores.json` y capturas de `09-make-dashboard`, `modelo.json` (meta y objetivo de cada KPI), brief (objetivos, usuarios y decisiones) | `11-make-conclusions` (conclusiones y recomendaciones), 12 |
| `capturas/pag-nn.png` | copia de la de `09-make-dashboard` | 12 (marcadores de captura de la sección 4) |
| `referencias.md` | las citas de la sección | 12 |

## Qué afecta cada cambio

| Cambio | Edición | Skills `-update` a ejecutar después |
|---|---|---|
| Cambió el valor real de un KPI en `09-make-dashboard-update` | fila del hallazgo (valor y estado), cifras de su «Qué muestra» (valor, meta y brecha) y, si cambió el estado, su decisión y las prioridades | `11-make-conclusions-update` |
| Cambió una captura en `09-make-dashboard-update` | `capturas/pag-nn.png` (y su pie) | — |
| Se cerró una meta pendiente en `07-make-data-model-kpi-update` | meta y estado del hallazgo de ese KPI, y quitarlo de «Metas pendientes» | `11-make-conclusions-update` |
| Cambió un objetivo o un KPI del modelo | hallazgos que lo citan; cada objetivo debe seguir con un hallazgo | `11-make-conclusions-update` |
| Cambió un usuario o una decisión del brief | columna «Quién decide» y «Decisión que apoya» de los hallazgos afectados | `11-make-conclusions-update` |
| Agregar un hallazgo | fila en la tabla, narrativa `### HLZ-nn`, captura (copiada y marcada una vez) y prioridades | `11-make-conclusions-update` |
| Quitar un hallazgo | fila, narrativa, captura si nadie más la usa y prioridades; su objetivo debe seguir con otro hallazgo | `11-make-conclusions-update` |
| Cambiar la decisión de un hallazgo | su fila y su «Qué decisión apoya» | `11-make-conclusions-update` si una recomendación la cita |
| Cambió el modo de datos (generado o real) | declaración del primer párrafo | — |

## Qué NO se hace aquí

| Cambio pedido | Dónde se hace |
|---|---|
| Corregir un valor o una captura del dashboard | `09-make-dashboard-update` (los entrega el equipo) |
| Cambiar la meta de un KPI | `07-make-data-model-kpi-update` |
| Cambiar la problemática o un objetivo | `01-make-project-brief-update` y `05-make-problem-objectives-update` |
| Cambiar cómo se limpian o cargan los datos | `08-make-etl-update` |
